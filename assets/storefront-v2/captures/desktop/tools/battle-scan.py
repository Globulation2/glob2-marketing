#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Find the moments and places where a colony's warriors clash with another's.

usage: battle-scan.py MATCH_DIR TICK TEAM PROFILE_DIR OUT_DIR [--span TICKS] [--step TICKS]

Loads the joined save (see explore.py), fast-forwards the match and, every
STEP ticks, reads the units the colony can see through a one-shot Hive script
(a read: it issues no orders, so the match stays identical to an unobserved
run). For each sample it scores the 28 x 18 tile window with the most fighting:
min(own warriors, other colonies' units) there. Prints the best samples; feed a
tick and tile to a capture recipe.
"""
import argparse
import json
import os
import subprocess
import sys
import time

import mcp
import session

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = """function step(ctx){
  const us=ctx.game.units({limit:6000}); const out=[];
  for(const u of us) out.push([u.team,u.type,u.x,u.y]);
  const bs=ctx.game.buildings({limit:2000}).map(b=>[b.team,b.x,b.y]);
  return {output:{my:ctx.myTeam,units:out,buildings:bs}};
}"""


def read_units():
    st, _, _ = mcp.call("hive_status", {})
    key = "scan-%d" % int(time.time() * 1000)
    mcp.call("hive_run", {"token": mcp.token(), "session": st["session"], "operation_key": key, "source": SCRIPT})
    for _ in range(60):
        time.sleep(0.15)
        res, _, _ = mcp.call("hive_result", {"session": st["session"], "operation_key": key})
        if res.get("status") == "completed":
            return res["observation_tick"], res["output"]
        if res.get("status") == "failed":
            raise RuntimeError(res.get("error"))
    raise RuntimeError("hive_result timed out")


def best_clash(out, mw, mh, w=28, h=18):
    my = out["my"]
    own = [(x, y) for t, ty, x, y in out["units"] if t == my and ty == 2]
    foe = [(x, y, ty) for t, ty, x, y in out["units"] if t != my]
    builds = out["buildings"]
    best = (0, 0, 0, 0, 0, 0)
    if not own or not foe:
        return best

    def near(px, py, cx, cy):
        dx = abs(px - cx); dy = abs(py - cy)
        return min(dx, mw - dx) <= w / 2 and min(dy, mh - dy) <= h / 2
    for cx in range(0, mw, 4):
        for cy in range(0, mh, 4):
            a = sum(1 for x, y in own if near(x, y, cx, cy))
            if a < 4:
                continue
            b = sum(1 for x, y, ty in foe if near(x, y, cx, cy))
            bw = sum(1 for x, y, ty in foe if ty == 2 and near(x, y, cx, cy))
            nb = sum(1 for t, x, y in builds if near(x, y, cx, cy))
            score = min(a, b) + min(a, bw) + min(nb, 6)
            if min(a, b) >= 4 and score > best[0]:
                best = (score, cx, cy, a, b, nb)
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("match"); ap.add_argument("tick"); ap.add_argument("team", type=int)
    ap.add_argument("profile"); ap.add_argument("out")
    ap.add_argument("--span", type=int, default=6000)
    ap.add_argument("--step", type=int, default=200)
    ap.add_argument("--speed", type=int, default=8)
    args = ap.parse_args()
    name = os.path.basename(os.path.normpath(args.match))
    label = f"{name}-{args.tick}-t{args.team}"
    src = os.path.join(args.match, f"checkpoint-{args.tick}.game.gz")
    dst = os.path.join(args.out, "saves", label + ".game.gz")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not os.path.exists(dst):
        subprocess.run([sys.executable, os.path.join(HERE, "join-seat.py"), src, dst, str(args.team),
                        "--rename", "maxima=Maxima", "--rename", "cortex=Cortex", "--rename", "cabino=Cabino",
                        "--rename", "castor=Castor", "--rename", "nicowar=Nicowar"], check=True,
                       stderr=subprocess.DEVNULL)
    session.load_save(dst, args.profile, settle=2)
    m = session.world("summary")["map"]
    start = session.gtime()["tick"]
    session.speed(args.speed)
    samples = []
    nxt = start
    try:
        while True:
            now = session.gtime()["tick"]
            if now >= start + args.span or session.has("outcome/reason"):
                break
            if now >= nxt:
                tick, out = read_units()
                samples.append((best_clash(out, m["width"], m["height"]), tick))
                nxt = now + args.step
            else:
                time.sleep(0.05)
    finally:
        try:
            session.speed(0)
        except Exception:
            pass
    samples.sort(reverse=True)
    print(f"{label}: {len(samples)} samples from tick {start}")
    for (score, cx, cy, a, b, nb), tick in samples[:8]:
        print(f"  tick {tick} tile [{cx}, {cy}] score {score}: own warriors {a}, others {b}, buildings {nb}")
    with open(os.path.join(args.out, label + "-battles.json"), "w") as fh:
        json.dump([{"tick": t, "tile": [s[1], s[2]], "score": s[0], "own_warriors": s[3], "others": s[4],
                    "buildings": s[5]} for s, t in samples], fh, indent=1)


if __name__ == "__main__":
    main()
