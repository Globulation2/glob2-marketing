#!/usr/bin/env python3
"""Show what the stream rig is doing: display, game, stream, supervisor, player, chat, results.

  status.py          human-readable summary
  status.py --json   the same as JSON

Read-only: it inspects processes, the game's MCP endpoint and $STATE_DIR, and changes nothing.
"""
import argparse
import json
import os
import pathlib
import shutil
import subprocess
import urllib.request

import rigconfig
import rigstate


def alive(pid_file: pathlib.Path):
    try:
        pid = int(pid_file.read_text().strip())
        os.kill(pid, 0)
        return pid
    except (OSError, ValueError):
        return None


def game_status(cfg):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                       "params": {"name": "ui_status", "arguments": {}}}).encode()
    req = urllib.request.Request(f"http://127.0.0.1:{cfg['MCP_PORT']}/mcp", body, {
        "Content-Type": "application/json", "Accept": "application/json, text/event-stream",
        "MCP-Protocol-Version": "2025-11-25", "Mcp-Method": "tools/call", "Mcp-Name": "ui_status"})
    try:
        out = json.load(urllib.request.urlopen(req, timeout=3))
        return json.loads(out["result"]["content"][0]["text"])
    except Exception:  # noqa: BLE001 - unreachable for any reason
        return None


def collect(cfg):
    log_dir, state = pathlib.Path(cfg["LOG_DIR"]), pathlib.Path(cfg["STATE_DIR"])
    xenv = dict(os.environ, **({"XAUTHORITY": cfg["STREAM_XAUTHORITY"]} if cfg.get("STREAM_DISPLAY_BACKEND") == "xorg" else {}))
    xvfb = subprocess.run(["xdpyinfo", "-display", cfg["STREAM_DISPLAY"]], capture_output=True, env=xenv).returncode == 0
    ui = game_status(cfg)
    status = rigstate.read_json(state / "status.json", {}) or {}
    sup_pid = alive(log_dir / "supervisor.pid")
    games = rigstate.read_jsonl(state / "games.jsonl")
    by_opp = {o: rigstate.record(games, o) for o in rigstate.OPPONENTS}
    disk = {str(p): round(shutil.disk_usage(p).free / 1024 ** 3, 1) for p in {log_dir, state} if p.exists()}
    return {
        "display": {"name": cfg["STREAM_DISPLAY"], "backend": cfg.get("STREAM_DISPLAY_BACKEND"), "up": xvfb},
        "game": {"mcp": ui is not None, "size": f"{ui['width']}x{ui['height']}" if ui else None,
                 "controller": ui.get("controller") if ui else None,
                 "screen": (status.get("game") or {}).get("screen")},
        "supervisor": {"running": bool(sup_pid), "pid": sup_pid, "mode": status.get("mode") if sup_pid else "offline",
                       "status_updated": status.get("updated")},
        "stream": status.get("stream") if sup_pid else {"running": bool(alive(log_dir / "stream.pid"))},
        "match": status.get("match") or rigstate.current(cfg),
        "player_agent": status.get("player_agent") if sup_pid else {"running": False},
        "chat": rigstate.read_json(state / "chat.json"),
        "recent_results": games[-5:],
        "record_by_opponent": by_opp,
        "disk_free_gib": disk,
    }


def show(s):
    yes = lambda b: "yes" if b else "no"  # noqa: E731
    print(f"display  {s['display']['name']} up: {yes(s['display']['up'])}")
    g = s["game"]
    print(f"game     MCP: {yes(g['mcp'])}  size: {g['size'] or '-'}  screen: {g['screen'] or '-'}  controller: {g['controller'] or '-'}")
    sup = s["supervisor"]
    print(f"super    running: {yes(sup['running'])}{' (pid %s)' % sup['pid'] if sup['pid'] else ''}  mode: {sup['mode']}"
          f"  status updated: {sup['status_updated'] or '-'}")
    st = s["stream"] or {}
    print(f"stream   running: {yes(st.get('running'))}  since: {st.get('since') or '-'}")
    m = s["match"] or {}
    print(f"match    #{m.get('number') or '-'} vs {m.get('opponent') or '-'} ({m.get('record') or '-'})  "
          f"generator: {m.get('generator') or '-'}  phase: {m.get('phase') or '-'}")
    if m.get("goal") or m.get("last_move"):
        print(f"         goal: {m.get('goal') or '-'}  last move: {m.get('last_move') or '-'}")
    p = s["player_agent"] or {}
    print(f"player   running: {yes(p.get('running'))}  since: {p.get('since') or '-'}")
    c = s["chat"]
    if c:
        print(f"chat     connected: {yes(c.get('connected'))}  can send: {yes(c.get('can_send'))}  "
              f"replies: {c.get('replies_sent', 0)}  last reply: {c.get('last_reply_at') or '-'}  updated: {c.get('updated') or '-'}")
    else:
        print("chat     no chat agent state")
    print("record   " + "  ".join(f"{o} {r}" for o, r in s["record_by_opponent"].items()))
    for r in s["recent_results"]:
        print(f"         #{r.get('number')} {str(r.get('date', ''))[:16]} vs {r.get('opponent')} on {r.get('generator')}: "
              f"{r.get('result')}{' - ' + r['note'] if r.get('note') else ''}")
    print("disk     " + "  ".join(f"{p}: {gib} GiB free" for p, gib in s["disk_free_gib"].items()))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--json", action="store_true")
    s = collect(rigconfig.load())
    if parser.parse_args().json:
        print(json.dumps(s, ensure_ascii=False, indent=1))
    else:
        show(s)


if __name__ == "__main__":
    main()
