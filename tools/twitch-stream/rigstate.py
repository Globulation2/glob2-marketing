"""Shared match state for the stream supervisor, stream_ctl.py and status.py.

Everything lives in $STATE_DIR (default ~/glob2-stream/state):
  current.json               the supervisor's assignment for the match being played
  games.jsonl                one line per finished or aborted match (the score source)
  status.json                written by the supervisor every few seconds; read by the chat agent
  chat.json                  written by the chat agent
  viewer-relay*.jsonl        the chat side's relayed viewer messages and their acks (viewer_relay.py)
"""
import datetime
import json
import os
import pathlib
import tempfile

# The only opponents the stream plays (user rule, 2026-11-24): the four stronger AIs.
OPPONENTS = ("Cortex", "Nicowar", "Cabino", "Maxima")
RESULTS = ("win", "loss", "draw", "aborted")


def now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def state_dir(cfg: dict) -> pathlib.Path:
    path = pathlib.Path(cfg["STATE_DIR"])
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json(path: pathlib.Path, data) -> None:
    """Replace path atomically so readers never see a partial file."""
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=path.name + ".")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    os.chmod(tmp, 0o664)  # the operator and the sandboxed agent share these files (README "Security and sandboxing")
    os.replace(tmp, path)


def write_text(path: pathlib.Path, text: str, mode: int = 0o664) -> None:
    """Replace a text file atomically; works on shared files the other side created.

    mode 0o644 makes a file the agent can read but not change (see the notes dir's sticky bit)."""
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=path.name + ".")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(text)
    os.chmod(tmp, mode)
    os.replace(tmp, path)


def read_json(path: pathlib.Path, default=None):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def read_jsonl(path: pathlib.Path) -> list:
    rows = []
    try:
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    try:
                        rows.append(json.loads(line))
                    except ValueError:
                        pass  # a torn line from a crash; skip it
    except OSError:
        pass
    return rows


def append_jsonl(path: pathlib.Path, row: dict) -> None:
    line = json.dumps(row, ensure_ascii=False) + "\n"
    if not path.exists() or os.access(path, os.W_OK):
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(line)
        try:
            os.chmod(path, 0o664)
        except PermissionError:
            pass  # created by the other side, which already made it shareable
        return
    # Created by the other side and not writable by us: replace it (the directory is shared).
    write_text(path, path.read_text(encoding="utf-8") + line)


def games(cfg: dict) -> list:
    return read_jsonl(state_dir(cfg) / "games.jsonl")


def record(all_games: list, opponent: str = None) -> str:
    """Wins, losses and draws, overall or against one opponent; aborted games never count."""
    counts = {"win": 0, "loss": 0, "draw": 0}
    for g in all_games:
        if (opponent is None or g.get("opponent") == opponent) and g.get("result") in counts:
            counts[g["result"]] += 1
    return f"{counts['win']}W–{counts['loss']}L–{counts['draw']}D"


def decided(all_games: list) -> int:
    """Games with a real outcome; aborted ones (operator restarts, setup failures) aren't games to viewers."""
    return sum(1 for g in all_games if g.get("result") in ("win", "loss", "draw"))


def caption_record(all_games: list, number=None) -> str:
    """The caption's record field: the viewer-facing game number (decided games so far, plus this one)
    and the overall record. The internal match number also counts aborted matches, so it isn't shown."""
    return f"Game {decided(all_games) + 1} · overall {record(all_games)}"


def next_opponent(all_games: list) -> str:
    """Least recently played of the four; never-played first, ties in list order."""
    last = {name: -1 for name in OPPONENTS}
    for i, g in enumerate(all_games):
        if g.get("opponent") in last:
            last[g["opponent"]] = i
    return min(OPPONENTS, key=lambda name: (last[name], OPPONENTS.index(name)))


def previous_generators(all_games: list, n: int = 5) -> list:
    return [g["generator"] for g in reversed(all_games) if g.get("generator")][:n]


def current(cfg: dict) -> dict:
    return read_json(state_dir(cfg) / "current.json", {}) or {}


def save_current(cfg: dict, data: dict) -> None:
    write_json(state_dir(cfg) / "current.json", data)


