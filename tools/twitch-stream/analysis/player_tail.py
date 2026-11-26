#!/usr/bin/env python3
"""Show what the player is doing: the last tool calls, errors and text of its newest session.

  analysis/player_tail.py [N]      last N events (default 40)

Tool arguments are shortened, and any `token` argument is dropped. Faster than reading the
gzipped transcript by hand when checking whether the player is stuck or looping.
"""
import json
import os
import sys

import transcripts


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    logs = transcripts.player_logs()
    if not logs:
        sys.exit("no player transcripts yet")
    out = []
    for ev in transcripts.events(logs[-1]):
        if ev.get("type") == "assistant":
            for c in (ev.get("message") or {}).get("content", []):
                if c.get("type") == "tool_use":
                    args = dict(c.get("input") or {})
                    args.pop("token", None)
                    out.append(f"TOOL {c['name'].split('__')[-1]} {json.dumps(args)[:150]}")
                elif c.get("type") == "text" and c["text"].strip():
                    out.append("SAY  " + c["text"].strip().replace("\n", " ")[:200])
        elif ev.get("type") == "user" and isinstance((ev.get("message") or {}).get("content"), list):
            for c in ev["message"]["content"]:
                if c.get("type") == "tool_result" and c.get("is_error"):
                    t = c.get("content")
                    out.append("ERR  " + (t if isinstance(t, str) else json.dumps(t))[:160])
    print(os.path.basename(logs[-1]), f"({len(out)} events)")
    print("\n".join(out[-n:]))


if __name__ == "__main__":
    main()
