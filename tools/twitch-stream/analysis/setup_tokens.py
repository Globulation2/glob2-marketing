#!/usr/bin/env python3
"""Token usage of player sessions: until the match starts, and for the whole session.

  analysis/setup_tokens.py [TRANSCRIPT ...]      default: the five newest

"Until playing" ends at the first match_setup_done, or for a recovery session (one resuming a
running match) at the first game-changing call. Use it to see what the brief, notes and menu
setup cost before any play, e.g. when trimming the brief.
"""
import os
import sys

import transcripts

ACTIONS = ("game_place", "game_building", "game_zone", "match_wait")
COLS = (("calls", "calls"), ("input_tokens", "input"), ("cache_creation_input_tokens", "cache_write"),
        ("cache_read_input_tokens", "cache_read"), ("output_tokens", "output"))


def main():
    paths = sys.argv[1:] or transcripts.player_logs()[-5:]
    for path in paths:
        tot = {k: 0 for k, _ in COLS}
        at_start = None
        for m, u in transcripts.calls(path):
            tot["calls"] += 1
            for k in USAGE if (USAGE := [k for k, _ in COLS[1:]]) else ():
                tot[k] += u[k]
            if at_start is None and any(n == "match_setup_done" or n in ACTIONS for n in transcripts.tool_names(m)):
                at_start = dict(tot)
        print(os.path.basename(path))
        for label, d in (("until playing", at_start), ("whole session", tot)):
            if d:
                print(f"  {label:14s} " + " ".join(f"{name}={d[k]:,}" for k, name in COLS))


if __name__ == "__main__":
    main()
