#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Round-2 scene scan: clashes, three-colony windows and the top-bar worker stat.

usage: scan2.py MATCH TICK TEAM OUT.json [--span TICKS] [--step TICKS] [--w 36 --h 20]

Loads the joined save through scene.py, fast-forwards and, every STEP ticks,
reads the colony's own fog-filtered view with a one-shot Hive script (a read, no
orders) and the top bar's "Workers free/total" through ui_inspect. For each
sample it reports the best window (W x H tiles, about a 3840x2160 frame at
100-125%) for a clash (own warriors against another colony's units) and for
colour count (distinct colonies with at least 3 units or buildings in view).
"""
import argparse
import json
import os
import sys
import time

import mcp
import scene
import session
import importlib.util

_spec = importlib.util.spec_from_file_location(
    "battle_scan", os.path.join(os.path.dirname(os.path.abspath(__file__)), "battle-scan.py"))
_bs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_bs)
read_units = _bs.read_units


def windows(out, mw, mh, w, h):
    my = out["my"]
    units = out["units"]
    builds = out["buildings"]

    def near(px, py, cx, cy):
        dx = abs(px - cx); dy = abs(py - cy)
        return min(dx, mw - dx) <= w / 2 and min(dy, mh - dy) <= h / 2
    best_clash, best_colours = None, None
    g = 4 if mw <= 128 else 8
    for cx in range(0, mw, g):
        for cy in range(0, mh, g):
            own_w = sum(1 for t, ty, x, y in units if t == my and ty == 2 and near(x, y, cx, cy))
            own_all = sum(1 for t, ty, x, y in units if t == my and near(x, y, cx, cy))
            own_b = sum(1 for t, x, y in builds if t == my and near(x, y, cx, cy))
            per = {}
            for t, ty, x, y in units:
                if t != my and near(x, y, cx, cy):
                    per.setdefault(t, [0, 0, 0])
                    per[t][0] += 1
                    per[t][1] += ty == 2
            for t, x, y in builds:
                if t != my and near(x, y, cx, cy):
                    per.setdefault(t, [0, 0, 0])
                    per[t][2] += 1
            foe_w = sum(v[1] for v in per.values())
            foe = sum(v[0] for v in per.values())
            clash = (min(own_w, foe_w), own_w, foe_w, own_b, cx, cy)
            if best_clash is None or clash > best_clash:
                best_clash = clash
            colonies = [t for t, v in per.items() if v[0] + v[2] >= 3]
            if own_all + own_b >= 3:
                colonies.append(my)
            col = (len(colonies), min(own_w, foe_w), foe + own_all, cx, cy, sorted(colonies))
            if best_colours is None or col > best_colours:
                best_colours = col
    return best_clash, best_colours


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("match"); ap.add_argument("tick"); ap.add_argument("team")
    ap.add_argument("out")
    ap.add_argument("--span", type=int, default=6000)
    ap.add_argument("--step", type=int, default=300)
    ap.add_argument("--speed", type=int, default=7)
    ap.add_argument("--w", type=int, default=36)
    ap.add_argument("--h", type=int, default=20)
    args = ap.parse_args()
    scene.load(args.match, args.tick, args.team)
    m = session.world("summary")["map"]
    start = session.gtime()["tick"]
    session.speed(args.speed)
    rows = []
    nxt = start
    try:
        while True:
            now = session.gtime()["tick"]
            if now >= start + args.span or session.has("outcome/reason"):
                break
            if now < nxt:
                time.sleep(0.05)
                continue
            hud = scene.hud_state()
            try:
                tick, out = read_units()
            except Exception as exc:  # e.g. a Hive worker that failed to start: skip the sample
                print(json.dumps({"skipped": str(exc)[:120]}), flush=True)
                nxt = now + args.step
                continue
            clash, colours = windows(out, m["width"], m["height"], args.w, args.h)
            row = {"tick": tick, "free": hud["free"], "rows": hud["events"], "clash": clash, "colours": colours}
            rows.append(row)
            print(json.dumps(row), flush=True)
            nxt = now + args.step
    finally:
        try:
            session.speed(0)
        except Exception:
            pass
    json.dump(rows, open(args.out, "w"), indent=1)


if __name__ == "__main__":
    main()
