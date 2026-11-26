#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Scout one saved match from a player seat and dump candidate frames.

usage: explore.py MATCH_DIR TICK TEAM PROFILE_DIR OUT_DIR [--zoom Z ...] [--wait TICKS]

Joins a local player to TEAM of MATCH_DIR/checkpoint-TICK.game.gz (join-seat.py),
loads it in the running capture game, then frames and captures:
  dense-N   the windows holding the most of the colony's buildings
  alert-N   places the colony's event journal reports attacks
  front-N   the colony's buildings closest to another colony's buildings
Each frame is saved at native pixels in OUT_DIR with a JSON sidecar.
"""
import argparse
import json
import os
import subprocess
import sys
import time

import session

HERE = os.path.dirname(os.path.abspath(__file__))


def wrap_delta(a, b, size):
    d = (a - b) % size
    return d - size if d > size / 2 else d


def densest(points, w, h, mw, mh, count=2, step=2, exclude=()):
    """Centres of the windows (w x h tiles, on the torus) holding the most weight."""
    found = list(exclude)
    out = []
    for _ in range(count):
        best = None
        for cx in range(0, mw, step):
            for cy in range(0, mh, step):
                if any(abs(wrap_delta(cx, fx, mw)) < w * 0.6 and abs(wrap_delta(cy, fy, mh)) < h * 0.6
                       for fx, fy in found):
                    continue
                score = sum(wt for x, y, wt in points
                            if abs(wrap_delta(x, cx, mw)) <= w / 2 and abs(wrap_delta(y, cy, mh)) <= h / 2)
                if best is None or score > best[0]:
                    best = (score, cx, cy)
        if not best or best[0] <= 0:
            break
        out.append(best)
        found.append((best[1], best[2]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("match")
    ap.add_argument("tick")
    ap.add_argument("team", type=int)
    ap.add_argument("profile")
    ap.add_argument("out")
    ap.add_argument("--zoom", type=float, action="append")
    ap.add_argument("--wait", type=int, default=0, help="ticks to let pass before scouting")
    ap.add_argument("--kinds", default="dense,alert,front")
    ap.add_argument("--erase", action="store_true", help="erase the colony's zone markings first")
    args = ap.parse_args()
    zooms = args.zoom or [1.0]
    name = os.path.basename(os.path.normpath(args.match))
    label = f"{name}-{args.tick}-t{args.team}"
    src = os.path.join(args.match, f"checkpoint-{args.tick}.game.gz")
    if args.tick == "final":
        src = os.path.join(args.match, "final.game.gz")
    os.makedirs(os.path.join(args.out, "saves"), exist_ok=True)
    dst = os.path.join(args.out, "saves", label + ".game.gz")
    subprocess.run([sys.executable, os.path.join(HERE, "join-seat.py"), src, dst, str(args.team),
                    "--rename", "maxima=Maxima", "--rename", "cortex=Cortex", "--rename", "cabino=Cabino",
                    "--rename", "castor=Castor", "--rename", "nicowar=Nicowar"], check=True)
    os.makedirs(args.out, exist_ok=True)
    session.load_save(dst, args.profile)
    if args.erase:
        session.erase_zones()
    if args.wait:
        session.run(args.wait)
    w = session.world("summary")
    mw, mh = w["map"]["width"], w["map"]["height"]
    own = [(b["x"] + b["width"] / 2, b["y"] + b["height"] / 2, b["width"] * b["height"])
           for b in w["colony"]["buildings"] if b["width"] > 1]
    others = [(b["x"] + b["width"] / 2, b["y"] + b["height"] / 2, b["width"] * b["height"])
              for b in w["others"]["buildings"] if b.get("enemy") and b["width"] > 1]
    print(f"{label}: tick {w['tick']} own buildings {len(own)} enemy seen {len(others)} status {w['status']}")
    shots = []
    kinds = args.kinds.split(",")
    for zoom in zooms:
        tw, th = 54 / zoom, 34 / zoom
        if "dense" in kinds:
            for i, (score, cx, cy) in enumerate(densest(own, tw, th, mw, mh, 2)):
                shots.append((f"dense{i}-z{zoom:g}", cx, cy, zoom, f"own building tiles in view {score:g}"))
        if "front" in kinds and others:
            both = own + [(x, y, wt * 1.5) for x, y, wt in others]
            # windows that hold both colours: weight by the smaller side
            best = []
            for cx in range(0, mw, 3):
                for cy in range(0, mh, 3):
                    a = sum(wt for x, y, wt in own if abs(wrap_delta(x, cx, mw)) <= tw / 2 and abs(wrap_delta(y, cy, mh)) <= th / 2)
                    b = sum(wt for x, y, wt in others if abs(wrap_delta(x, cx, mw)) <= tw / 2 and abs(wrap_delta(y, cy, mh)) <= th / 2)
                    if a and b:
                        best.append((min(a, b) * 2 + a + b, cx, cy))
            best.sort(reverse=True)
            if best:
                shots.append((f"front0-z{zoom:g}", best[0][1], best[0][2], zoom, f"mixed-colony score {best[0][0]:g}"))
    if "alert" in kinds:
        seen = []
        for a in w.get("alerts", []):
            if "attack" not in a.get("kind", "") or "Explorer" in a.get("event", ""):
                continue
            if any(abs(wrap_delta(a["x"], x, mw)) < 14 and abs(wrap_delta(a["y"], y, mh)) < 10 for x, y in seen):
                continue
            seen.append((a["x"], a["y"]))
            shots.append((f"alert{len(seen) - 1}-z1", a["x"], a["y"], 1.0, a["event"] + f" x{a['count']}"))
            if len(seen) >= 3:
                break
    for tag, x, y, zoom, why in shots:
        view = session.view(int(x) % mw, int(y) % mh, zoom)
        time.sleep(0.4)
        path = os.path.join(args.out, f"{label}-{tag}.png")
        session.shot(path)
        tick = session.gtime()["tick"]
        meta = dict(save=dst, source=src, team=args.team, tag=tag, tile=[int(x) % mw, int(y) % mh],
                    zoom=view["zoom"], tick=tick, why=why, status=w["status"])
        with open(path[:-4] + ".json", "w") as fh:
            json.dump(meta, fh, indent=1)
        print(f"  {os.path.basename(path)} tile {meta['tile']} zoom {view['zoom']} tick {tick}: {why}")


if __name__ == "__main__":
    main()
