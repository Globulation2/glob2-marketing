#!/usr/bin/env python3
"""How the player uses its tools: calls, response sizes, errors, waits, setup and compaction cost.

  analysis/tool_usage.py                          every archived transcript ($LOG_DIR/player-archive)
  analysis/tool_usage.py --from 58 --to 140       only these match numbers
  analysis/tool_usage.py --json out.json          also write every table as JSON
  analysis/tool_usage.py --section errors         print one section (see --help for names)

Reads the player transcripts (`claude -p --output-format stream-json --verbose`), the match log
($STATE_DIR/games.jsonl) and the supervisor log, and reports, per tool and per session phase
(setup menus, playing, fast-forward, wrap-up after the result):

- calls, share, per match and per wall-clock minute of play;
- response size: characters, a chars/4 estimate, and the measured tokens: the cache write of the
  model call right after a tool result (cache_creation + uncached input), which is that result plus
  the previous call's output. Measured only for calls that were alone in their message, with no
  compaction in between;
- errors (is_error) clustered into a taxonomy, soft refusals that are not flagged as errors
  (narrations "not sent", placements moved away from the asked tile), same-call retries, and
  calls to tools that don't exist in the session;
- match_wait use and wake reasons, screenshots, setup cost, compactions, recovery sessions,
  arguments (detail levels, include filters), repeated (unchanged) response content, and a
  per-match table joined with outcomes.

File names are match-<session stamp>-<match>-<turn>.jsonl.gz: one stamp per supervisor session, and
turn > 01 is the same session resumed with --resume after the model ended its turn early. A second
stamp for the same match is a recovery session. Usage is counted once per message id. The per-event
output_tokens in stream-json are a snapshot taken when the message starts, not the final count, so
output and thinking tokens come from each turn's `result` event, and compaction calls (which never
appear as assistant events) from the difference between the result's modelUsage and its usage.
Costs use cost_report.PRICES (API list prices; the stream runs on a subscription).
"""
import argparse
import collections
import datetime
import glob
import json
import os
import pathlib
import re
import statistics

import transcripts
from cost_report import PRICES

FILE_RE = re.compile(r"match-(\d{8}-\d{6})-(\d{5})-(\d{2})\.jsonl\.gz$")
# Calls that change or advance the match: the first one marks a recovery session as playing.
PLAY_TOOLS = {"game_place", "game_building", "game_zone", "match_wait", "camera_show", "narrate",
              "match_caption", "game_time", "match_fast_forward"}
FF_MARK = "Fast-forwarding to the end of a lost match"
EARLY_MIN = 10              # outcome comparison also uses each match's first minutes of play (same length for all)
# Token-like strings: 24+ characters mixing upper case, lower case and digits, or 32+ hex digits.
LONG_TOKEN = re.compile(r"\b(?=[A-Za-z0-9_\-]*[a-z])(?=[A-Za-z0-9_\-]*[A-Z])(?=[A-Za-z0-9_\-]*\d)[A-Za-z0-9_\-]{24,}\b"
                        r"|\b[0-9a-fA-F]{32,}\b")
SECTIONS = ("coverage", "tools", "phases", "sizes", "fields", "errors", "refusals", "efficiency",
            "waits", "screenshots", "args", "setup", "compaction", "recovery", "matches", "outcomes")

# Error taxonomy: first matching pattern wins. Applied to the error text (the "error" field of a
# JSON reply, else the whole text).
ERROR_CLASSES = [
    ("unknown tool (name not in session)", r"No such tool available"),
    ("UI control stale (revision changed)", r"Stale control"),
    ("UI control hidden/blocked/unknown", r"Hidden control|Blocked control|Unknown surface|Unsupported action"),
    ("invalid argument (schema range/type)", r"Invalid argument"),
    ("unknown building/flag name", r"Unknown building or flag"),
    ("placement: no room / unexplored", r"No room for|not all explored|needs clear ground"),
    ("stale or foreign building id", r"was not reported in this match|now generation|no building with id"),
    ("action not valid for building", r"does not produce units|Cannot cancel|Nothing to change"),
    ("camera rate limit", r"camera moved \d+ s ago"),
    ("camera unavailable", r"camera unavailable|camera move refused"),
    ("fast-forward refused (too early/high)", r"^not yet: fast-forward"),
    ("no match running / no control", r"No match is running|no game control"),
    ("bookkeeping order (setup-done first)", r"setup-done"),
    ("caption: coordinates refused", r"no coordinates or building ids"),
    ("UI wait timed out", r"Wait timed out"),
    ("file too large to Read", r"exceeds maximum allowed tokens"),
    ("transport (connection closed)", r"Connection closed|game unavailable"),
    ("hive script/operation", r"Operation key|Return an object|TypeError|ReferenceError|SyntaxError"),
    ("input dispatch failed", r"Input dispatch"),
]


def redact(text: str) -> str:
    return LONG_TOKEN.sub("<redacted>", text)


def pct(part, whole) -> float:
    return 100.0 * part / whole if whole else 0.0


def quant(values, q):
    """Nearest-rank quantile (q in 0..1) of a non-empty list."""
    v = sorted(values)
    return v[min(len(v) - 1, max(0, int(round(q * (len(v) - 1)))))]


def dist(values) -> dict:
    values = [v for v in values if v is not None]
    if not values:
        return {"n": 0}
    return {"n": len(values), "median": statistics.median(values), "p90": quant(values, 0.9),
            "max": max(values), "mean": statistics.fmean(values), "total": sum(values)}


def ts(s):
    try:
        return datetime.datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()
    except (AttributeError, ValueError):
        return None


def short(name: str) -> str:
    return name.split("__")[-1]


def result_text(block) -> tuple:
    """(text, image count, image base64 chars) of a tool_result block."""
    c = block.get("content")
    if isinstance(c, str):
        return c, 0, 0
    text, imgs, ib = [], 0, 0
    for x in c or []:
        if x.get("type") == "text":
            text.append(x.get("text", ""))
        elif x.get("type") == "image":
            imgs += 1
            ib += len((x.get("source") or {}).get("data", ""))
    return "".join(text), imgs, ib


def parse_json_tail(text: str):
    """The JSON object in a reply, also when stream-ctl prefixed note lines (match_wait)."""
    i = text.find("{")
    if i < 0:
        return None, text
    try:
        value = json.loads(text[i:])
        return (value if isinstance(value, dict) else None), text[:i]
    except ValueError:
        return None, text[:i]


def error_text(text: str) -> str:
    obj, _ = parse_json_tail(text)
    if obj and isinstance(obj.get("error"), str):
        return obj["error"]
    return text


def classify(text: str) -> str:
    for label, pat in ERROR_CLASSES:
        if re.search(pat, text):
            return label
    return "other"


def norm_message(text: str) -> str:
    t = re.sub(r"\d+", "N", text)
    t = re.sub(r'"[^"]{1,40}"', '"S"', t)
    return redact(t[:90])


# --- extraction ----------------------------------------------------------------------------------
def archive_logs(log_dir) -> list:
    return sorted(glob.glob(str(pathlib.Path(log_dir) / "*.jsonl.gz")))


def load_games(path) -> dict:
    games = {}
    try:
        with open(path) as fh:
            for line in fh:
                try:
                    g = json.loads(line)
                    games[g["number"]] = g
                except (ValueError, KeyError):
                    continue
    except OSError:
        pass
    return games


def load_supervisor(path) -> list:
    """(local time, message) lines that matter for sessions: starts, exits, timeouts, fast-forwards."""
    out = []
    try:
        with open(path, errors="replace") as fh:
            for line in fh:
                if re.search(r"player (session|turn)|game timeout|fast-forward|ending its turn", line):
                    out.append((line[:19], line[24:].strip()))
    except OSError:
        pass
    return out


class Session:
    def __init__(self, stamp, match, recovery):
        self.stamp, self.match, self.recovery = stamp, match, recovery
        self.turns = []            # per turn: dict(path, part, start, end, result, compactions)
        self.calls = []            # tool calls (dicts)
        self.api = []              # model calls: dict(id, ts, usage, n_tools, phase, after_compact)
        self.compactions = []      # compact_metadata dicts with phase
        self.phase = "setup"
        self.phase_t = {}          # phase -> first timestamp
        self.max_tick = 0
        self.init_tools = set()

    @property
    def key(self):
        return f"{self.stamp}-{self.match:05d}"


def extract(paths, keep_text=False) -> list:
    """Sessions with their calls, in time order."""
    sessions, seen_matches = {}, set()
    parsed = []
    for p in paths:
        m = FILE_RE.search(os.path.basename(p))
        if m:
            parsed.append((m.group(1), int(m.group(2)), int(m.group(3)), p))
    for stamp, match, part, path in sorted(parsed):
        key = (stamp, match)
        if key not in sessions:
            sessions[key] = Session(stamp, match, recovery=match in seen_matches)
            seen_matches.add(match)
        read_turn(sessions[key], part, path, keep_text)
    return list(sessions.values())


def read_turn(s: Session, part: int, path: str, keep_text: bool):
    turn = {"path": os.path.basename(path), "part": part, "start": None, "end": None, "result": None,
            "truncated": False}
    s.turns.append(turn)
    pending = {}               # tool_use id -> call dict
    seen_ids = set()
    last_results = []          # calls whose results arrived since the last model call
    compact_since = False
    prev_api = None
    n = 0
    for e in transcripts.events(path):
        n += 1
        t = e.get("type")
        when = ts(e.get("timestamp"))
        if when:
            turn["start"] = turn["start"] or when
            turn["end"] = when
        if t == "system":
            if e.get("subtype") == "init":
                s.init_tools = set(e.get("tools", []))
            elif e.get("subtype") == "compact_boundary":
                md = dict(e.get("compact_metadata") or {})
                s.compactions.append({"phase": s.phase, "pre_tokens": md.get("pre_tokens"),
                                      "post_tokens": md.get("post_tokens"), "duration_ms": md.get("duration_ms"),
                                      "trigger": md.get("trigger")})
                compact_since = True
        elif t == "assistant":
            msg = e.get("message") or {}
            mid = msg.get("id")
            if mid not in seen_ids:
                seen_ids.add(mid)
                u = msg.get("usage") or {}
                usage = {k: u.get(k, 0) or 0 for k in transcripts.USAGE_KEYS}
                usage["cache_write_1h"] = (u.get("cache_creation") or {}).get("ephemeral_1h_input_tokens", 0) or 0
                api = {"id": mid, "ts": when, "usage": usage, "n_tools": 0, "phase": s.phase,
                       "after_compact": compact_since, "part": part, "prev": prev_api}
                s.api.append(api)
                written = usage["cache_creation_input_tokens"] + usage["input_tokens"]
                if last_results and not compact_since:
                    share = written / len(last_results)
                    for c in last_results:
                        c["next_written"] = share
                        c["next_alone"] = len(last_results) == 1 and c["msg_tools"] == 1
                if prev_api is not None:
                    prev_api["next_ts"] = when
                last_results, compact_since = [], False
                prev_api = api
            for c in msg.get("content", []):
                if c.get("type") != "tool_use":
                    continue
                args = dict(c.get("input") or {})
                args.pop("token", None)
                call = {"session": s.key, "match": s.match, "part": part, "recovery": s.recovery,
                        "name": short(c.get("name", "?")), "full_name": c.get("name", "?"), "args": args,
                        "phase": s.phase, "ts": when, "msg_id": mid, "msg_tools": 0, "known": None,
                        "is_error": None, "chars": 0, "images": 0, "image_b64": 0, "text": "",
                        "next_written": None, "next_alone": False, "tick": None}
                call["known"] = call["full_name"] in s.init_tools
                pending[c.get("id")] = call
                s.calls.append(call)
                s.api[-1]["n_tools"] += 1
                for other in s.calls[-s.api[-1]["n_tools"]:]:
                    other["msg_tools"] = s.api[-1]["n_tools"]
        elif t == "user":
            content = (e.get("message") or {}).get("content")
            if not isinstance(content, list):
                continue
            for b in content:
                if b.get("type") != "tool_result":
                    continue
                call = pending.pop(b.get("tool_use_id"), None)
                if call is None:
                    continue
                text, imgs, ib = result_text(b)
                call.update(is_error=bool(b.get("is_error")), chars=len(text), images=imgs, image_b64=ib,
                            result_ts=when)
                call["text"] = text if keep_text or call["is_error"] or len(text) < 400 else text[:400]
                analyse_result(s, call, text)
                last_results.append(call)
        elif t == "result":
            turn["result"] = {k: e.get(k) for k in ("total_cost_usd", "usage", "modelUsage", "duration_ms",
                                                     "duration_api_ms", "num_turns", "permission_denials",
                                                     "stop_reason", "terminal_reason", "subtype")}
    if n == 0 or turn["result"] is None:
        turn["truncated"] = True


def analyse_result(s: Session, call: dict, text: str):
    """Phase changes, ticks and per-tool details read from a result."""
    name = call["name"]
    obj, prefix = parse_json_tail(text) if name in ("game_world", "match_wait", "game_time", "game_place",
                                                     "game_building", "game_stats") else (None, "")
    if obj:
        tick = obj.get("tick")
        if isinstance(tick, int):
            call["tick"] = tick
            s.max_tick = max(s.max_tick, tick)
        if name in ("game_world", "match_wait"):
            call["sections"] = {k: len(json.dumps(v, separators=(",", ":"))) for k, v in obj.items()}
            call["obj"] = obj
        if name == "match_wait":
            call["wake"] = obj.get("reason")
            call["waited"] = obj.get("waited_ticks")
            call["wait_prefix"] = prefix
            call["trigger_kind"] = (obj.get("trigger") or {}).get("kind") if isinstance(obj.get("trigger"), dict) else None
        if name == "game_place":
            call["moved"] = obj.get("moved")
    elif name == "match_wait":
        call["wait_prefix"] = prefix
    if call["is_error"]:
        return
    if name == "match_setup_done" and s.phase == "setup":
        set_phase(s, "playing", call["ts"])
    elif s.phase == "setup" and s.recovery and name in PLAY_TOOLS:
        set_phase(s, "playing", call["ts"])
    if name == "match_fast_forward" or (name == "match_wait" and FF_MARK in text[:400]):
        if s.phase in ("setup", "playing"):
            set_phase(s, "fastforward", call["ts"])
    if name == "match_result":
        set_phase(s, "wrapup", call["ts"])


def set_phase(s: Session, phase: str, when):
    s.phase = phase
    s.phase_t.setdefault(phase, when)


# --- analysis ------------------------------------------------------------------------------------
MU_KEYS = {"input_tokens": "inputTokens", "output_tokens": "outputTokens",
           "cache_read_input_tokens": "cacheReadInputTokens", "cache_creation_input_tokens": "cacheCreationInputTokens"}


def cost_turns(sessions):
    """Set turn["cost"]: tokens and list-price cost of each turn, split into model calls and compaction.

    In a resumed session (--resume) a turn's `usage` covers that turn only, but `total_cost_usd` and
    `modelUsage` are cumulative over the session's turns, so those are differenced. A turn the supervisor
    killed has no result: its cost is estimated from its calls' input usage plus the mean output per call."""
    for s in sessions:
        prev_mu, prev_cost = {}, 0.0
        for t in s.turns:
            r = t["result"]
            api = [a for a in s.api if a["part"] == t["part"]]
            c = {"cost": 0.0, "output": 0, "thinking": 0, "compact_cost": 0.0, "compact_in": 0, "compact_out": 0,
                 "estimated": r is None, "input": 0, "cache_read": 0, "cache_write_1h": 0, "cache_write_5m": 0}
            for a in api:
                u = a["usage"]
                c["input"] += u["input_tokens"]
                c["cache_read"] += u["cache_read_input_tokens"]
                c["cache_write_1h"] += u["cache_write_1h"]
                c["cache_write_5m"] += u["cache_creation_input_tokens"] - u["cache_write_1h"]
            if r is None:
                c["output"] = len(api) * 200          # ~ the measured mean output per model call
                c["cost"] = sum(input_cost(a["usage"]) for a in api) + c["output"] * PRICES["output_tokens"] / 1e6
                t["cost"] = c
                prev_mu = None                         # later cumulative figures can't be differenced
                continue
            u = r.get("usage") or {}
            mu = next(iter((r.get("modelUsage") or {}).values()), {}) or {}
            cum = r.get("total_cost_usd") or 0.0
            if prev_mu is None:                       # after a killed turn: treat as not cumulative
                prev_mu, prev_cost = {}, 0.0
            delta = {k: (mu.get(v, 0) or 0) - (prev_mu.get(v, 0) or 0) for k, v in MU_KEYS.items()}
            c["cost"] = cum - prev_cost
            c["output"] = u.get("output_tokens", 0) or 0
            c["thinking"] = (u.get("output_tokens_details") or {}).get("thinking_tokens", 0) or 0
            d = {k: delta[k] - (u.get(k, 0) or 0) for k in MU_KEYS}
            c["compact_in"] = d["input_tokens"] + d["cache_read_input_tokens"] + d["cache_creation_input_tokens"]
            c["compact_out"] = d["output_tokens"]
            c["compact_cost"] = (d["input_tokens"] * PRICES["input_tokens"] + d["cache_read_input_tokens"]
                                 * PRICES["cache_read_input_tokens"] + d["cache_creation_input_tokens"]
                                 * PRICES["cache_write_5m"] + d["output_tokens"] * PRICES["output_tokens"]) / 1e6
            t["cost"] = c
            prev_mu, prev_cost = mu, cum


def input_cost(u) -> float:
    w5 = u["cache_creation_input_tokens"] - u["cache_write_1h"]
    return (u["input_tokens"] * PRICES["input_tokens"] + u["cache_read_input_tokens"] * PRICES["cache_read_input_tokens"]
            + u["cache_write_1h"] * PRICES["cache_write_1h"] + w5 * PRICES["cache_write_5m"]) / 1e6


def session_minutes(s: Session) -> dict:
    """Wall minutes per phase, from tool call timestamps."""
    out = collections.Counter()
    times = sorted((c["ts"], c["phase"]) for c in s.calls if c["ts"])
    for (t0, ph), (t1, _) in zip(times, times[1:]):
        gap = t1 - t0
        if gap < 600:                       # a resumed turn or a stall longer than 10 min isn't play
            out[ph] += gap / 60
    return dict(out)


def analyse(sessions, games, supervisor) -> dict:
    calls = [c for s in sessions for c in s.calls]
    R = {}
    matches = sorted({s.match for s in sessions})
    turns = [t for s in sessions for t in s.turns]
    cost_turns(sessions)
    costs = [t["cost"] for t in turns]
    minutes = collections.Counter()
    for s in sessions:
        minutes.update(session_minutes(s))
    play_min = minutes["playing"] + minutes["fastforward"]
    total_cost = sum(c["cost"] for c in costs)
    parts = {"cache_write_1h": sum(c["cache_write_1h"] for c in costs) * PRICES["cache_write_1h"] / 1e6,
             "cache_write_5m": sum(c["cache_write_5m"] for c in costs) * PRICES["cache_write_5m"] / 1e6,
             "cache_read": sum(c["cache_read"] for c in costs) * PRICES["cache_read_input_tokens"] / 1e6,
             "input": sum(c["input"] for c in costs) * PRICES["input_tokens"] / 1e6,
             "output": sum(c["output"] for c in costs) * PRICES["output_tokens"] / 1e6,
             "compaction": sum(c["compact_cost"] for c in costs)}
    hours = sum(minutes.values()) / 60
    outcomes = collections.Counter(games.get(m, {}).get("result", "unrecorded") for m in matches)
    R["coverage"] = {
        "sessions": len(sessions), "recovery_sessions": sum(s.recovery for s in sessions),
        "turns": len(turns), "unfinished_turns": sum(t["truncated"] for t in turns),
        "matches": len(matches), "first_match": matches[0] if matches else None,
        "last_match": matches[-1] if matches else None, "outcomes": dict(outcomes),
        "first": min((t["start"] for t in turns if t["start"]), default=None),
        "last": max((t["end"] for t in turns if t["end"]), default=None),
        "tool_calls": len(calls), "model_calls": sum(len(s.api) for s in sessions),
        "wall_minutes": dict(minutes), "cost_usd": total_cost,
        "cost_usd_estimated_part": sum(c["cost"] for c in costs if c["estimated"]),
        "cost_parts_usd": parts, "cost_parts_pct": {k: pct(v, total_cost) for k, v in parts.items()},
        "cost_per_hour": total_cost / hours if hours else 0,
        "cost_per_match": total_cost / max(1, len(matches)),
        "output_tokens": sum(c["output"] for c in costs), "thinking_tokens": sum(c["thinking"] for c in costs),
    }
    R["coverage"]["first"] = fmt_time(R["coverage"]["first"])
    R["coverage"]["last"] = fmt_time(R["coverage"]["last"])

    # tools
    by = collections.defaultdict(list)
    for c in calls:
        by[c["name"]].append(c)
    rows = []
    for name, cs in sorted(by.items(), key=lambda kv: -len(kv[1])):
        ph = collections.Counter(c["phase"] for c in cs)
        rows.append({"tool": name, "calls": len(cs), "share": pct(len(cs), len(calls)),
                     "per_match": len(cs) / max(1, len(matches)),
                     "per_play_min": sum(1 for c in cs if c["phase"] in ("playing", "fastforward")) / play_min if play_min else 0,
                     "setup": ph["setup"], "playing": ph["playing"], "fastforward": ph["fastforward"],
                     "wrapup": ph["wrapup"], "errors": sum(1 for c in cs if c["is_error"]),
                     "error_rate": pct(sum(1 for c in cs if c["is_error"]), len(cs)),
                     "unknown_name": sum(1 for c in cs if not c["known"])})
    R["tools"] = rows

    # phases
    prow = []
    api_all = [a for s in sessions for a in s.api]
    for ph in ("setup", "playing", "fastforward", "wrapup"):
        cs = [c for c in calls if c["phase"] == ph]
        ap = [a for a in api_all if a["phase"] == ph]
        prow.append({"phase": ph, "wall_min": minutes[ph], "tool_calls": len(cs), "model_calls": len(ap),
                     "tool_calls_per_min": len(cs) / minutes[ph] if minutes[ph] else 0,
                     "result_chars": sum(c["chars"] for c in cs),
                     "cache_write_tokens": sum(a["usage"]["cache_creation_input_tokens"] for a in ap),
                     "cache_read_tokens": sum(a["usage"]["cache_read_input_tokens"] for a in ap),
                     "input_side_cost": sum(input_cost(a["usage"]) for a in ap)})
    R["phases"] = prow

    # sizes
    srows = []
    for name, cs in sorted(by.items(), key=lambda kv: -sum(c["chars"] for c in kv[1])):
        ch = [c["chars"] for c in cs]
        meas = [c["next_written"] for c in cs if c["next_alone"] and c["next_written"] is not None]
        ratio = [c["next_written"] / (c["chars"] / 4) for c in cs
                 if c["next_alone"] and c["next_written"] and c["chars"] >= 400 and not c["images"]]
        srows.append({"tool": name, "calls": len(cs), "chars_median": dist(ch).get("median"),
                      "chars_p90": dist(ch).get("p90"), "chars_max": dist(ch).get("max"),
                      "chars_total": sum(ch), "chars_share": 0.0, "est_tokens_total": sum(ch) / 4,
                      "images": sum(c["images"] for c in cs),
                      "measured_n": len(meas), "measured_median": dist(meas).get("median"),
                      "measured_p90": dist(meas).get("p90"),
                      "measured_over_est": statistics.median(ratio) if ratio else None,
                      "written_total": sum(c["next_written"] or 0 for c in cs)})
    tot_chars = sum(r["chars_total"] for r in srows) or 1
    tot_written = sum(r["written_total"] for r in srows) or 1
    for r in srows:
        r["chars_share"] = pct(r["chars_total"], tot_chars)
        r["written_share"] = pct(r["written_total"], tot_written)
    R["sizes"] = srows
    all_written = sum(a["usage"]["cache_creation_input_tokens"] + a["usage"]["input_tokens"] for a in api_all)
    R["sizes_summary"] = {"cache_write_after_tool_results": sum(c["next_written"] or 0 for c in calls),
                          "all_cache_write_and_input": all_written,
                          "calls_per_compaction": len(api_all) / max(1, sum(len(s.compactions) for s in sessions))}

    R["fields"] = field_report(calls)
    R["errors"] = error_report(calls)
    R["refusals"] = refusal_report(calls, sessions)
    R["efficiency"] = efficiency_report(sessions, turns, costs, calls, play_min)
    R["waits"] = wait_report(calls)
    R["screenshots"] = screenshot_report(calls)
    R["args"] = args_report(calls)
    R["setup"] = setup_report(sessions)
    R["compaction"] = compaction_report(sessions, costs)
    R["recovery"] = recovery_report(sessions, supervisor)
    R["matches"] = match_report(sessions, games)
    R["outcomes"] = outcome_report(R["matches"])
    return R


def fmt_time(t):
    return datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M") if t else None


def leaves(obj, prefix="", depth=0):
    """(path, compact JSON of value) for dict leaves down to depth 3; lists count as one leaf."""
    for k, v in obj.items():
        path = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict) and v and depth < 3:
            yield from leaves(v, path, depth + 1)
        else:
            yield path, json.dumps(v, separators=(",", ":"))


def field_report(calls) -> dict:
    """game_world and match_wait replies: which sections and fields take the space, and how much of each
    is identical to the same field in the previous reply of that tool in the session (what a delta
    reply would drop)."""
    out = {}
    for tool in ("game_world", "match_wait"):
        size, present, same, leaf_size, leaf_same, leaf_n = (collections.Counter() for _ in range(6))
        n, last = 0, {}
        for c in calls:
            if c["name"] != tool or not c.get("sections"):
                continue
            n += 1
            for k, v in c["sections"].items():
                size[k] += v
                present[k] += 1
            prev = last.get(c["session"], {})
            cur = dict(leaves(c["obj"]))
            for path, val in cur.items():
                chars = len(path.split(".")[-1]) + len(val) + 4
                leaf_size[path] += chars
                leaf_n[path] += 1
                if prev.get(path) == val:
                    leaf_same[path] += chars
            last[c["session"]] = cur
        total = sum(size.values()) or 1
        ltotal = sum(leaf_size.values()) or 1
        out[tool] = {"replies": n, "chars_total": total,
                     "sections": [{"section": k, "present_pct": pct(present[k], n), "chars_share": pct(v, total),
                                   "mean_chars": v / present[k]} for k, v in size.most_common(14)],
                     "fields": [{"field": k, "present_pct": pct(leaf_n[k], n), "chars_share": pct(v, ltotal),
                                 "unchanged_pct": pct(leaf_same[k], v)} for k, v in leaf_size.most_common(22)],
                     "unchanged_share_of_all": pct(sum(leaf_same.values()), ltotal)}
    notes = collections.Counter()
    for c in calls:
        if c["name"] in ("game_place", "game_building", "game_zone") and not c["is_error"] and c["text"].startswith("{"):
            obj, _ = parse_json_tail(c["text"])
            if obj and isinstance(obj.get("note"), str):
                notes[(c["name"], len(obj["note"]))] += 1
    out["action_notes"] = [{"tool": k[0], "note_chars": k[1], "replies": v} for k, v in notes.most_common(6)]
    used = collections.Counter(k for c in calls for k in c["args"] if k in ("session", "since_tick"))
    out["reply_fields_passed_back"] = dict(used)
    return out


def error_report(calls) -> dict:
    errs = [c for c in calls if c["is_error"]]
    cls = collections.Counter()
    examples = {}
    per_tool = collections.defaultdict(collections.Counter)
    for c in errs:
        et = error_text(c["text"])
        k = classify(et)
        cls[k] += 1
        per_tool[c["name"]][norm_message(et)] += 1
        examples.setdefault(k, (c["name"], redact(et[:160])))
    # retries and recovery: what follows an error in the same session
    retry_same, retry_tool, recover_calls = 0, 0, []
    by_session = collections.defaultdict(list)
    for c in calls:
        by_session[c["session"]].append(c)
    for cs in by_session.values():
        for i, c in enumerate(cs):
            if not c["is_error"]:
                continue
            nxt = cs[i + 1] if i + 1 < len(cs) else None
            if nxt and nxt["name"] == c["name"]:
                retry_tool += 1
                if nxt["args"] == c["args"]:
                    retry_same += 1
            # calls until the same tool succeeds again (within 8 calls), the cost of recovering
            for j in range(i + 1, min(len(cs), i + 9)):
                if cs[j]["name"] == c["name"] and not cs[j]["is_error"]:
                    recover_calls.append(j - i)
                    break
    return {"errors": len(errs), "calls": len(calls), "rate": pct(len(errs), len(calls)),
            "classes": [{"class": k, "count": v, "share": pct(v, len(errs)), "example_tool": examples[k][0],
                         "example": examples[k][1]} for k, v in cls.most_common()],
            "by_tool": {t: [{"message": m, "count": n} for m, n in cnt.most_common(6)]
                        for t, cnt in sorted(per_tool.items(), key=lambda kv: -sum(kv[1].values()))},
            "next_call_same_tool": retry_tool, "next_call_identical": retry_same,
            "calls_until_same_tool_succeeds": dist(recover_calls)}


def refusal_report(calls, sessions) -> dict:
    out = {}
    nar = [c for c in calls if c["name"] == "narrate"]
    not_sent = [c for c in nar if not c["is_error"] and c["text"].startswith("not sent")]
    out["narrate"] = {"calls": len(nar), "not_sent": len(not_sent), "not_sent_pct": pct(len(not_sent), len(nar))}
    gaps = []
    for c in not_sent:
        m = re.search(r"was (\d+) s ago", c["text"])
        if m:
            gaps.append(int(m.group(1)))
    out["narrate"]["seconds_since_last_when_refused"] = dist(gaps)
    cam = [c for c in calls if c["name"] == "camera_show" and c["known"]]
    cam_rl = [c for c in cam if c["is_error"] and "camera moved" in c["text"]]
    waits = []
    for c in cam_rl:
        m = re.search(r"wait (\d+) s", c["text"])
        if m:
            waits.append(int(m.group(1)))
    out["camera_show"] = {"calls": len(cam), "rate_limited": len(cam_rl), "rate_limited_pct": pct(len(cam_rl), len(cam)),
                          "said_wait_0_s": sum(1 for w in waits if w == 0), "wait_seconds": dist(waits)}
    gp = [c for c in calls if c["name"] == "game_place" and not c["is_error"]]
    moved = [c for c in gp if c.get("moved")]
    tiles = [c["moved"].get("tiles") for c in moved if isinstance(c["moved"], dict) and c["moved"].get("tiles") is not None]
    why = collections.Counter(norm_message(str(c["moved"].get("requested_refused", "?")))[:60]
                              for c in moved if isinstance(c["moved"], dict))
    gp_all = [c for c in calls if c["name"] == "game_place"]
    out["game_place"] = {"calls": len(gp_all), "errors": sum(1 for c in gp_all if c["is_error"]),
                         "succeeded": len(gp), "moved": len(moved), "moved_pct_of_success": pct(len(moved), len(gp)),
                         "near_used_pct": pct(sum(1 for c in gp_all if c["args"].get("near")), len(gp_all)),
                         "moved_tiles": dist(tiles), "moved_because": [{"reason": k, "n": v} for k, v in why.most_common(4)]}
    hr = [c for c in calls if c["name"] == "hive_run"]
    out["hive_run"] = {"calls": len(hr), "error_in_reply": sum(1 for c in hr if '"error"' in c["text"][:200])}
    unknown = [c for c in calls if not c["known"]]
    out["unknown_tools"] = [{"name": redact(k), "calls": v} for k, v in
                            collections.Counter(c["full_name"] for c in unknown).most_common()]
    denials = collections.Counter()
    for s in sessions:
        for t in s.turns:
            for d in (t["result"] or {}).get("permission_denials") or []:
                denials[d.get("tool_name", "?")] += 1
    out["permission_denials"] = dict(denials)
    return out


def efficiency_report(sessions, turns, costs, calls, play_min) -> dict:
    api = [a for s in sessions for a in s.api]
    with_tools = [a for a in api if a["n_tools"]]
    gaps_model, gaps_tool, gaps_next = [], [], []
    for c in calls:
        if c.get("result_ts") and c["ts"]:
            gaps_tool.append(c["result_ts"] - c["ts"])
    for s in sessions:
        cs = [c for c in s.calls if c["ts"] and c.get("result_ts")]
        for a, b in zip(cs, cs[1:]):
            if b["msg_id"] != a["msg_id"] and b["part"] == a["part"]:
                gaps_model.append(b["ts"] - a["result_ts"])        # model thinking time
                gaps_next.append(b["ts"] - a["ts"])
    by_tool_latency = collections.defaultdict(list)
    for c in calls:
        if c.get("result_ts") and c["ts"]:
            by_tool_latency[c["name"]].append(c["result_ts"] - c["ts"])
    in_tool = collections.Counter()
    for c in calls:
        if c.get("result_ts") and c["ts"] and c["phase"] in ("playing", "fastforward"):
            in_tool[c["name"]] += c["result_ts"] - c["ts"]
    decisions = [c for c in calls if c["name"] in ("game_place", "game_building", "game_zone")
                 and c["phase"] == "playing" and not c["is_error"]]
    play_api = [a for a in api if a["phase"] == "playing"]
    out_tok = sum(c["output"] for c in costs)
    think = sum(c["thinking"] for c in costs)
    fin_api = sum(1 for s in sessions for a in s.api
                  if any(t["result"] and t["part"] == a["part"] for t in s.turns))
    return {"model_calls": len(api), "model_calls_with_tools": len(with_tools),
            "tools_per_model_call": len(calls) / max(1, len(with_tools)),
            "parallel_calls_pct": pct(sum(1 for a in with_tools if a["n_tools"] > 1), len(with_tools)),
            "decisions_playing": len(decisions),
            "model_calls_per_decision": len(play_api) / max(1, len(decisions)),
            "decisions_per_play_min": len(decisions) / play_min if play_min else 0,
            "output_tokens_finished_turns": out_tok, "thinking_tokens_finished_turns": think,
            "output_per_model_call": out_tok / max(1, fin_api), "thinking_share_of_output": pct(think, out_tok),
            "seconds_model_between_calls": dist(gaps_model), "seconds_tool_latency": dist(gaps_tool),
            "seconds_call_to_call": dist(gaps_next),
            "play_wall_share_in_tools_pct": {k: round(pct(v, play_min * 60), 1) for k, v in in_tool.most_common(6)},
            "play_wall_share_model_pct": pct(sum(gaps_model), play_min * 60),
            "tool_latency_median": {k: statistics.median(v) for k, v in by_tool_latency.items() if len(v) >= 10}}


def wait_report(calls) -> dict:
    waits = [c for c in calls if c["name"] == "match_wait" and c["known"]]
    ok = [c for c in waits if not c["is_error"]]
    asked = [c["args"].get("ticks") for c in waits if isinstance(c["args"].get("ticks"), int)]
    wake = collections.Counter(c.get("wake") or "?" for c in ok)
    trig = collections.Counter(c.get("trigger_kind") or "-" for c in ok if c.get("wake") not in ("ticks", None))
    notes = collections.Counter()
    prefix_chars = 0
    for c in ok:
        p = c.get("wait_prefix") or ""
        prefix_chars += len(p)
        for line in p.splitlines():
            if line.startswith("Game speed"):
                notes["speed line"] += 1
            elif line.startswith("The camera hasn't moved"):
                notes["camera nudge"] += 1
            elif line.startswith("Fast-forwarding"):
                notes["fast-forward reminder"] += 1
            elif line.startswith("Something critical"):
                notes["auto slow-down"] += 1
            elif "Twitch chat" in line:
                notes["viewer relay"] += 1
    by_session = collections.defaultdict(list)
    for c in calls:
        by_session[c["session"]].append(c)
    back_to_back = 0
    woke = collections.Counter()
    woke_then_wait = collections.Counter()
    for cs in by_session.values():
        for a, b in zip(cs, cs[1:]):
            if a["name"] == "match_wait" and not a["is_error"]:
                woke[a.get("wake")] += 1
                if b["name"] == "match_wait":
                    back_to_back += 1
                    woke_then_wait[a.get("wake")] += 1
    waited = [c.get("waited") for c in ok if isinstance(c.get("waited"), int)]
    return {"calls": len(waits), "share_of_calls": pct(len(waits), len(calls)), "ticks_asked": dist(asked),
            "ticks_asked_common": collections.Counter(asked).most_common(6), "waited_ticks": dist(waited),
            "wake_reasons": dict(wake.most_common()), "event_triggers": dict(trig.most_common(8)),
            "also_until_used_pct": pct(sum(1 for c in waits if c["args"].get("also_until")), len(waits)),
            "include_used_pct": pct(sum(1 for c in waits if c["args"].get("include")), len(waits)),
            "notes": dict(notes), "prefix_chars_total": prefix_chars,
            "back_to_back_waits": back_to_back, "back_to_back_pct": pct(back_to_back, len(waits)),
            "next_call_is_wait_pct_by_wake": {k: round(pct(woke_then_wait[k], v), 1) for k, v in woke.most_common(8)},
            "reply_chars": dist([c["chars"] for c in ok])}


def screenshot_report(calls) -> dict:
    shots = [c for c in calls if c["name"] == "ui_screenshot" or (c["images"] and c["name"] != "ui_screenshot")]
    meas = [c["next_written"] for c in shots if c["next_alone"] and c["next_written"]]
    widths = collections.Counter(c["args"].get("max_width", "default") for c in shots if c["name"] == "ui_screenshot")
    return {"calls_with_images": len(shots), "by_tool": dict(collections.Counter(c["name"] for c in shots)),
            "by_phase": dict(collections.Counter(c["phase"] for c in shots)), "max_width": dict(widths.most_common()),
            "image_b64_chars": dist([c["image_b64"] for c in shots if c["image_b64"]]),
            "measured_tokens": dist(meas), "measured_tokens_total_est": (statistics.median(meas) * len(shots)) if meas else None,
            "per_match": dict(collections.Counter(c["match"] for c in shots).most_common(5))}


def args_report(calls) -> dict:
    out = {}
    gw = [c for c in calls if c["name"] == "game_world" and c["known"]]
    def detail(c):
        return c["args"].get("detail", "summary(default)")
    sizes = collections.defaultdict(list)
    for c in gw:
        k = detail(c) + (" +include" if c["args"].get("include") else "")
        sizes[k].append(c["chars"])
    out["game_world_detail"] = [{"variant": k, "calls": len(v), "share": pct(len(v), len(gw)),
                                 "chars_median": statistics.median(v), "chars_p90": quant(v, 0.9),
                                 "chars_total_share": pct(sum(v), sum(c["chars"] for c in gw))}
                                for k, v in sorted(sizes.items(), key=lambda kv: -len(kv[1]))]
    inc = collections.Counter(",".join(sorted(c["args"]["include"])) for c in gw if c["args"].get("include"))
    out["game_world_include"] = inc.most_common(10)
    keys = collections.Counter(k for c in gw for k in c["args"])
    out["game_world_args"] = {k: pct(v, len(gw)) for k, v in keys.most_common()}
    out["game_world_since_tick_with_alerts_pct"] = pct(sum(1 for c in gw if c["args"].get("detail") == "alerts"
                                                           and "since_tick" in c["args"]),
                                                       sum(1 for c in gw if c["args"].get("detail") == "alerts"))
    # how fresh is the information: game_world right after a match_wait (whose reply already had status/alerts)
    by_session = collections.defaultdict(list)
    for c in calls:
        by_session[c["session"]].append(c)
    after_wait = 0
    for cs in by_session.values():
        for a, b in zip(cs, cs[1:]):
            if a["name"] == "match_wait" and b["name"] == "game_world":
                after_wait += 1
    out["game_world_right_after_wait"] = after_wait
    for tool in ("ui_inspect", "ui_act", "camera_show", "game_place", "game_building", "game_time", "ui_screenshot"):
        cs = [c for c in calls if c["name"] == tool and c["known"]]
        kc = collections.Counter(k for c in cs for k in c["args"])
        out[tool + "_args"] = {k: round(pct(v, len(cs)), 1) for k, v in kc.most_common(12)}
    zooms = collections.Counter(c["args"].get("zoom", "-") for c in calls if c["name"] == "camera_show")
    out["camera_zoom"] = zooms.most_common(8)
    gb = [c for c in calls if c["name"] == "game_building" and c["known"]]
    act = collections.Counter(c["args"].get("action") or "+".join(sorted(k for k in c["args"] if k not in ("id", "generation")))
                              for c in gb)
    out["game_building_changes"] = act.most_common(10)
    gt = [c for c in calls if c["name"] == "game_time" and c["known"]]
    out["game_time_speed"] = collections.Counter(str(c["args"].get("speed", c["args"].get("action", "status")))
                                                 for c in gt).most_common(8)
    return out


def setup_report(sessions) -> dict:
    rows = []
    for s in sessions:
        start = s.phase_t.get("playing")
        cs = [c for c in s.calls if c["phase"] == "setup"]
        ap = [a for a in s.api if a["phase"] == "setup"]
        t0 = min((c["ts"] for c in s.calls if c["ts"]), default=None)
        reads = [c for c in cs if c["name"] == "Read"]
        rows.append({"session": s.key, "recovery": s.recovery, "reached_play": start is not None,
                     "tool_calls": len(cs), "model_calls": len(ap),
                     "minutes": (start - t0) / 60 if start and t0 else None,
                     "ui_calls": sum(1 for c in cs if c["name"].startswith("ui_")),
                     "read_calls": len(reads), "read_chars": sum(c["chars"] for c in reads),
                     "screenshots": sum(1 for c in cs if c["images"]),
                     "first_cache_write": ap[0]["usage"]["cache_creation_input_tokens"] + ap[0]["usage"]["cache_read_input_tokens"] if ap else None,
                     "cache_write": sum(a["usage"]["cache_creation_input_tokens"] for a in ap),
                     "input_side_cost": sum(input_cost(a["usage"]) for a in ap)})
    fresh = [r for r in rows if not r["recovery"] and r["reached_play"]]
    ui_tools = collections.Counter(c["name"] for s in sessions if not s.recovery for c in s.calls if c["phase"] == "setup")
    reads = collections.Counter()
    read_chars = collections.Counter()
    for s in sessions:
        for c in s.calls:
            if c["name"] == "Read":
                f = os.path.basename(str(c["args"].get("file_path", "?")))
                reads[(f, c["phase"])] += 1
                read_chars[f] += c["chars"]
    return {"fresh_sessions": len(fresh),
            "tool_calls": dist([r["tool_calls"] for r in fresh]), "model_calls": dist([r["model_calls"] for r in fresh]),
            "minutes": dist([r["minutes"] for r in fresh]), "ui_calls": dist([r["ui_calls"] for r in fresh]),
            "input_side_cost": dist([r["input_side_cost"] for r in fresh]),
            "first_call_context_tokens": dist([r["first_cache_write"] for r in fresh]),
            "tools": ui_tools.most_common(14),
            "reads_by_file_phase": [{"file": k[0], "phase": k[1], "reads": v} for k, v in reads.most_common(12)],
            "read_chars_by_file": dict(read_chars.most_common(6))}


def compaction_report(sessions, costs) -> dict:
    comp = [c for s in sessions for c in s.compactions]
    per_session = [len(s.compactions) for s in sessions]
    per_hour = []
    for s in sessions:
        m = sum(session_minutes(s).values())
        if m > 20:
            per_hour.append(len(s.compactions) / (m / 60))
    # what the model does right after a compaction: rereads and re-queries
    after = collections.Counter()
    reread_chars = 0
    for s in sessions:
        api_after = {a["id"] for a in s.api if a["after_compact"]}
        flagged = False
        window = 0
        for c in s.calls:
            if c["msg_id"] in api_after:
                flagged, window = True, 0
            if flagged:
                window += 1
                if window <= 6:
                    after[c["name"]] += 1
                    if c["name"] == "Read":
                        reread_chars += c["chars"]
                else:
                    flagged = False
    first_after = [a["usage"]["cache_creation_input_tokens"] for s in sessions for a in s.api if a["after_compact"]]
    return {"compactions": len(comp), "per_session": dist(per_session), "per_hour_of_play": dist(per_hour),
            "pre_tokens": dist([c["pre_tokens"] for c in comp]), "post_tokens": dist([c["post_tokens"] for c in comp]),
            "duration_s": dist([(c["duration_ms"] or 0) / 1000 for c in comp]),
            "by_phase": dict(collections.Counter(c["phase"] for c in comp)),
            "summary_cost_usd": sum(c["compact_cost"] for c in costs),
            "summary_cost_share_pct": pct(sum(c["compact_cost"] for c in costs), sum(c["cost"] for c in costs)),
            "cost_per_compaction": sum(c["compact_cost"] for c in costs) / max(1, len(comp)),
            "summary_tokens_in": sum(c["compact_in"] for c in costs), "summary_tokens_out": sum(c["compact_out"] for c in costs),
            "rebuild_cache_write_after": dist(first_after),
            "first_6_calls_after": after.most_common(10), "reread_chars_after": reread_chars}


def recovery_report(sessions, supervisor) -> dict:
    by_match = collections.defaultdict(list)
    for s in sessions:
        by_match[s.match].append(s)
    resumed_turns = sum(max(0, len(s.turns) - 1) for s in sessions)
    reasons = collections.Counter()
    for when, msg in supervisor:
        if "game timeout" in msg:
            reasons["game timeout (supervisor ended the session)"] += 1
        elif "ending its turn immediately" in msg:
            reasons["model kept ending its turn (3 quick turns)"] += 1
    multi = {m: ss for m, ss in by_match.items() if len(ss) > 1}
    rows = []
    for m, ss in sorted(multi.items()):
        rows.append({"match": m, "sessions": len(ss), "turns": sum(len(s.turns) for s in ss),
                     "cost": sum(t["cost"]["cost"] for s in ss for t in s.turns),
                     "recovery_cost": sum(t["cost"]["cost"] for s in ss if s.recovery for t in s.turns),
                     "tool_calls": sum(len(s.calls) for s in ss)})
    ended_early = []
    for s in sessions:
        for t in s.turns[:-1]:
            r = t["result"] or {}
            ended_early.append({"session": s.key, "part": t["part"], "terminal": r.get("terminal_reason"),
                                "stop": r.get("stop_reason"),
                                "minutes": ((t["end"] or 0) - (t["start"] or 0)) / 60})
    return {"recovery_sessions": sum(s.recovery for s in sessions), "matches_with_recovery": len(multi),
            "resumed_turns": resumed_turns, "supervisor_reasons_all_time": dict(reasons),
            "matches": rows, "turns_ended_before_result": len(ended_early),
            "ended_turn_stop_reasons": dict(collections.Counter(f"{e['terminal']}/{e['stop']}" for e in ended_early)),
            "ended_turn_minutes": dist([e["minutes"] for e in ended_early])}


def match_report(sessions, games) -> list:
    by_match = collections.defaultdict(list)
    for s in sessions:
        by_match[s.match].append(s)
    rows = []
    for m, ss in sorted(by_match.items()):
        cs = [c for s in ss for c in s.calls]
        mins = collections.Counter()
        for s in ss:
            mins.update(session_minutes(s))
        play = mins["playing"]
        pc = [c for c in cs if c["phase"] == "playing"]
        g = games.get(m, {})
        n = collections.Counter(c["name"] for c in pc)
        t0 = min((c["ts"] for c in pc if c["ts"]), default=None)
        early = [c for c in pc if t0 and c["ts"] and c["ts"] - t0 <= EARLY_MIN * 60]
        ne = collections.Counter(c["name"] for c in early)
        rows.append({"match": m, "result": g.get("result", "unrecorded"), "opponent": g.get("opponent"),
                     "generator": g.get("generator"), "sessions": len(ss), "play_min": play,
                     "ff_min": mins["fastforward"], "setup_min": mins["setup"],
                     "max_tick": max(s.max_tick for s in ss),
                     "fast_forward": any("fastforward" in s.phase_t for s in ss),
                     "calls": len(cs), "play_calls": len(pc), "play_calls_per_min": len(pc) / play if play else None,
                     "errors": sum(1 for c in cs if c["is_error"]),
                     "error_rate": pct(sum(1 for c in cs if c["is_error"]), len(cs)),
                     "wait_share": pct(n["match_wait"], len(pc)), "world_share": pct(n["game_world"], len(pc)),
                     "action_share": pct(n["game_place"] + n["game_building"] + n["game_zone"], len(pc)),
                     "show_share": pct(n["narrate"] + n["camera_show"] + n["match_caption"], len(pc)),
                     "screenshots": sum(1 for c in cs if c["images"]),
                     "early_calls_per_min": len(early) / EARLY_MIN if play >= EARLY_MIN else None,
                     "early_error_rate": pct(sum(1 for c in early if c["is_error"]), len(early)) if play >= EARLY_MIN else None,
                     "early_world_share": pct(ne["game_world"], len(early)) if play >= EARLY_MIN else None,
                     "early_wait_share": pct(ne["match_wait"], len(early)) if play >= EARLY_MIN else None,
                     "early_action_share": pct(ne["game_place"] + ne["game_building"] + ne["game_zone"], len(early))
                     if play >= EARLY_MIN else None,
                     "compactions": sum(len(s.compactions) for s in ss),
                     "result_chars": sum(c["chars"] for c in cs),
                     "cost": sum(t["cost"]["cost"] for s in ss for t in s.turns)})
    return rows


def med(values):
    values = [v for v in values if v is not None]
    return statistics.median(values) if values else None


def outcome_report(rows) -> dict:
    out = {}
    decided = [r for r in rows if r["result"] in ("win", "loss") and r["play_min"] > 3]
    cols = ("play_min", "max_tick", "play_calls_per_min", "error_rate", "wait_share", "world_share", "action_share",
            "show_share", "screenshots", "compactions", "cost", "early_calls_per_min", "early_error_rate",
            "early_world_share", "early_wait_share", "early_action_share")
    for res in ("win", "loss"):
        rs = [r for r in decided if r["result"] == res]
        out[res] = {"n": len(rs), **{c: med([r[c] for r in rs]) for c in cols}}
    # Cortex wins often come from the AI quitting early: show the comparison without Cortex too
    nc = [r for r in decided if r["opponent"] != "Cortex"]
    for res in ("win", "loss"):
        rs = [r for r in nc if r["result"] == res]
        out[res + "_excl_cortex"] = {"n": len(rs), **{c: med([r[c] for r in rs]) for c in cols}}
    # first-20-minute rates, comparable across long and short games
    out["by_opponent"] = {}
    for opp in sorted({r["opponent"] for r in decided if r["opponent"]}):
        rs = [r for r in decided if r["opponent"] == opp]
        out["by_opponent"][opp] = {"n": len(rs), "wins": sum(r["result"] == "win" for r in rs),
                                   "median_play_min": statistics.median([r["play_min"] for r in rs])}
    return out


# --- printing ------------------------------------------------------------------------------------
def table(rows, cols, fmt=None):
    fmt = fmt or {}
    if not rows:
        print("  (none)")
        return
    def cell(r, c):
        v = r.get(c)
        if v is None:
            return "-"
        if c in fmt:
            return fmt[c].format(v)
        if isinstance(v, float):
            return f"{v:,.1f}"
        if isinstance(v, int):
            return f"{v:,}"
        return str(v)
    cells = [[cell(r, c) for c in cols] for r in rows]
    widths = [max(len(c), *(len(x[i]) for x in cells)) for i, c in enumerate(cols)]
    print("  " + "  ".join(c.rjust(w) if i else c.ljust(w) for i, (c, w) in enumerate(zip(cols, widths))))
    for x in cells:
        print("  " + "  ".join(v.rjust(w) if i else v.ljust(w) for i, (v, w) in enumerate(zip(x, widths))))


def kv(d, indent="  "):
    for k, v in d.items():
        if isinstance(v, dict) and v and all(isinstance(x, (int, float)) for x in v.values()):
            v = ", ".join(f"{a} {b:,.1f}" if isinstance(b, float) else f"{a} {b:,}" for a, b in v.items())
        elif isinstance(v, float):
            v = f"{v:,.2f}"
        print(f"{indent}{k}: {v}")


def show(R, only=None):
    def head(name, title):
        if only and name != only:
            return False
        print(f"\n== {title} ==")
        return True

    if head("coverage", "Coverage"):
        kv(R["coverage"])
    if head("tools", "Calls per tool"):
        table(R["tools"], ["tool", "calls", "share", "per_match", "per_play_min", "setup", "playing", "fastforward",
                           "wrapup", "errors", "error_rate", "unknown_name"],
              {"share": "{:.1f}%", "error_rate": "{:.1f}%", "per_play_min": "{:.2f}"})
    if head("phases", "By session phase"):
        table(R["phases"], ["phase", "wall_min", "tool_calls", "model_calls", "tool_calls_per_min", "result_chars",
                            "cache_write_tokens", "cache_read_tokens", "input_side_cost"],
              {"input_side_cost": "${:,.2f}", "tool_calls_per_min": "{:.2f}"})
    if head("sizes", "Response size per tool (chars; measured = next call's cache write, single-call messages)"):
        table(R["sizes"], ["tool", "calls", "chars_median", "chars_p90", "chars_max", "chars_total", "chars_share",
                           "est_tokens_total", "measured_median", "measured_p90", "measured_over_est",
                           "written_total", "written_share"],
              {"chars_share": "{:.1f}%", "written_share": "{:.1f}%", "measured_over_est": "{:.2f}",
               "chars_median": "{:,.0f}", "measured_median": "{:,.0f}", "est_tokens_total": "{:,.0f}",
               "written_total": "{:,.0f}", "measured_p90": "{:,.0f}"})
        kv(R["sizes_summary"])
    if head("fields", "Reply sections (game_world, match_wait): size and unchanged since the previous reply"):
        for tool in ("game_world", "match_wait"):
            f = R["fields"][tool]
            print(f"  {tool}: {f['replies']} replies, {f['chars_total']:,} chars; "
                  f"{f['unchanged_share_of_all']:.1f}% of field characters identical to the previous {tool} reply")
            table(f["sections"], ["section", "present_pct", "chars_share", "mean_chars"],
                  {"present_pct": "{:.0f}%", "chars_share": "{:.1f}%", "mean_chars": "{:,.0f}"})
            table(f["fields"], ["field", "present_pct", "chars_share", "unchanged_pct"],
                  {"present_pct": "{:.0f}%", "chars_share": "{:.1f}%", "unchanged_pct": "{:.0f}%"})
        table(R["fields"]["action_notes"], ["tool", "note_chars", "replies"])
        print("  reply fields passed back as arguments:", R["fields"]["reply_fields_passed_back"])
    if head("errors", "Errors"):
        e = R["errors"]
        print(f"  {e['errors']} errors in {e['calls']} calls ({e['rate']:.2f}%); next call same tool {e['next_call_same_tool']}, "
              f"identical args {e['next_call_identical']}; calls until that tool succeeds: {e['calls_until_same_tool_succeeds']}")
        table(e["classes"], ["class", "count", "share", "example_tool", "example"], {"share": "{:.1f}%"})
        for tool, msgs in list(e["by_tool"].items())[:8]:
            print(f"  {tool}:")
            for m in msgs[:4]:
                print(f"    {m['count']:4d}  {m['message']}")
    if head("refusals", "Soft refusals and unknown tools"):
        for k, v in R["refusals"].items():
            print(f"  {k}: {v}")
    if head("efficiency", "Efficiency"):
        kv(R["efficiency"])
    if head("waits", "match_wait"):
        kv(R["waits"])
    if head("screenshots", "Screenshots"):
        kv(R["screenshots"])
    if head("args", "Arguments"):
        table(R["args"]["game_world_detail"], ["variant", "calls", "share", "chars_median", "chars_p90", "chars_total_share"],
              {"share": "{:.1f}%", "chars_total_share": "{:.1f}%", "chars_median": "{:,.0f}"})
        for k, v in R["args"].items():
            if k != "game_world_detail":
                print(f"  {k}: {v}")
    if head("setup", "Setup (fresh sessions, until match_setup_done)"):
        kv(R["setup"])
    if head("compaction", "Compaction"):
        kv(R["compaction"])
    if head("recovery", "Recovery sessions and resumed turns"):
        rec = dict(R["recovery"])
        rows = rec.pop("matches")
        kv(rec)
        table(rows, ["match", "sessions", "turns", "tool_calls", "cost", "recovery_cost"],
              {"cost": "${:,.2f}", "recovery_cost": "${:,.2f}"})
    if head("matches", "Per match"):
        table(R["matches"], ["match", "result", "opponent", "generator", "sessions", "play_min", "ff_min", "max_tick",
                             "play_calls_per_min", "error_rate", "wait_share", "world_share", "action_share",
                             "show_share", "screenshots", "compactions", "cost"],
              {"play_calls_per_min": "{:.1f}", "error_rate": "{:.1f}", "wait_share": "{:.0f}", "world_share": "{:.0f}",
               "action_share": "{:.0f}", "show_share": "{:.0f}", "cost": "${:.2f}", "play_min": "{:.0f}", "ff_min": "{:.0f}"})
    if head("outcomes", "Outcomes (medians; decided matches with 3+ minutes of play)"):
        o = R["outcomes"]
        rows = [{"group": k, **v} for k, v in o.items() if k != "by_opponent"]
        table(rows, ["group", "n", "play_min", "max_tick", "play_calls_per_min", "error_rate", "wait_share",
                     "world_share", "action_share", "show_share", "screenshots", "compactions", "cost"],
              {"cost": "${:.2f}", "max_tick": "{:,.0f}"})
        print(f"  first {EARLY_MIN} minutes of play only:")
        table(rows, ["group", "n", "early_calls_per_min", "early_error_rate", "early_world_share", "early_wait_share",
                     "early_action_share"])
        print("  by opponent:", o["by_opponent"])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", help="transcripts (default: every file in --dir)")
    ap.add_argument("--dir", help="transcript directory (default $LOG_DIR/player-archive)")
    ap.add_argument("--games", help="games.jsonl (default $STATE_DIR/games.jsonl)")
    ap.add_argument("--supervisor", help="supervisor log (default $LOG_DIR/supervisor.log)")
    ap.add_argument("--from", dest="first", type=int, help="first match number")
    ap.add_argument("--to", dest="last", type=int, help="last match number")
    ap.add_argument("--section", choices=SECTIONS, help="print only this section")
    ap.add_argument("--json", help="also write all tables as JSON to this path")
    a = ap.parse_args()
    cfg = None
    if not (a.dir and a.games and a.supervisor) and not a.paths:
        import rigconfig
        cfg = rigconfig.load()
    log_dir = pathlib.Path(cfg["LOG_DIR"]) if cfg else None
    paths = a.paths or archive_logs(a.dir or log_dir / "player-archive")
    def keep(p):
        m = FILE_RE.search(os.path.basename(p))
        return m and (a.first is None or int(m.group(2)) >= a.first) and (a.last is None or int(m.group(2)) <= a.last)
    paths = [p for p in paths if keep(p)]
    if not paths:
        raise SystemExit("no transcripts")
    games = load_games(a.games or pathlib.Path(cfg["STATE_DIR"]) / "games.jsonl") if (a.games or cfg) else {}
    sup = load_supervisor(a.supervisor or log_dir / "supervisor.log") if (a.supervisor or cfg) else []
    sessions = extract(paths)
    R = analyse(sessions, games, sup)
    show(R, a.section)
    if a.json:
        with open(a.json, "w") as fh:
            json.dump(R, fh, indent=1, default=str)
        print(f"\nwrote {a.json}")


if __name__ == "__main__":
    main()
