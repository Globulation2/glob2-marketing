"""Shared reading of the player's session transcripts ($LOG_DIR/player/*.jsonl.gz).

Each transcript is the `claude -p --output-format stream-json` output of one session. One API
call can span several "assistant" events with the same message id, so usage is counted once
per id. A transcript still being written may end mid-line or mid-gzip-block; readers stop there.
"""
import glob
import gzip
import json
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import rigconfig  # noqa: E402

USAGE_KEYS = ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")


def log_dir() -> pathlib.Path:
    return pathlib.Path(rigconfig.load()["LOG_DIR"])


def player_logs() -> list:
    """Transcript paths, oldest first."""
    return sorted(glob.glob(str(log_dir() / "player" / "*.jsonl.gz")), key=os.path.getmtime)


def events(path):
    """Yield the transcript's JSON events, tolerating a file still being written."""
    try:
        with gzip.open(path, "rt") as fh:
            for line in fh:
                try:
                    yield json.loads(line)
                except ValueError:
                    continue
    except (EOFError, OSError):
        return


def calls(path):
    """Yield (message, usage) once per model call: usage has the four USAGE_KEYS plus
    cache_write_1h (the part of cache creation written with the one-hour TTL)."""
    seen = set()
    for e in events(path):
        if e.get("type") != "assistant":
            continue
        m = e.get("message") or {}
        if m.get("id") in seen:
            continue
        seen.add(m.get("id"))
        u = m.get("usage") or {}
        usage = {k: u.get(k, 0) or 0 for k in USAGE_KEYS}
        usage["cache_write_1h"] = (u.get("cache_creation") or {}).get("ephemeral_1h_input_tokens", 0) or 0
        yield m, usage


def tool_names(message) -> list:
    return [c["name"].split("__")[-1] for c in message.get("content", []) if c.get("type") == "tool_use"]
