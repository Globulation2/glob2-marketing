#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Build-shot sequence: the seat places a building site, sets its workers, and the
frame is taken while workers carry materials to it.

usage: build-shot.py BUILDING X Y ZOOM OUT_PREFIX [--arm OTHER --hover HX HY] [--workers N] [--wait S]

Without --arm the new site is selected (the panel shows its materials and the
Working slider). With --arm the panel shows the palette with OTHER armed and the
pointer over HX,HY draws its placement preview; the site stays in view.
"""
import argparse
import json
import time

import mcp
import scene
import session

ap = argparse.ArgumentParser()
ap.add_argument("building"); ap.add_argument("x", type=int); ap.add_argument("y", type=int)
ap.add_argument("zoom", type=float); ap.add_argument("out")
ap.add_argument("--arm"); ap.add_argument("--hover", type=float, nargs=2)
ap.add_argument("--workers", type=int)
ap.add_argument("--wait", type=float, default=5.0)
ap.add_argument("--shots", type=int, default=3)
a = ap.parse_args()

before = {b["id"] for b in session.world("summary")["colony"]["buildings"]}
r, _, err = mcp.call("game_place", {"token": mcp.token(), "building": a.building, "x": a.x, "y": a.y, "near": True})
if err:
    raise SystemExit(r)
scene.act_log(f"placed a {a.building} construction site at ({r['x']}, {r['y']}) from the build palette (game_place)")
site = None
for _ in range(40):
    time.sleep(0.25)
    for b in session.world("summary")["colony"]["buildings"]:
        if b["id"] not in before and b["type"] == a.building:
            site = b
    if site:
        break
print("site", site)
if a.workers:
    mcp.call("game_building", {"token": mcp.token(), "id": site["id"], "generation": site["generation"], "workers": a.workers})
    scene.act_log(f"set the site's workers to {a.workers}")
cx, cy = site["x"] + site["width"] / 2.0, site["y"] + site["height"] / 2.0
v = session.view(int(cx), int(cy), a.zoom)
s = scene.state(); s["camera"] = {"centre_tile": [int(cx), int(cy)], "zoom": v["zoom"], "view_tiles": v["view"]}; scene.save_state(s)
if a.arm:
    mcp.act(f"game/buildings/{a.arm}.0.site")
    scene.act_log(f"armed the {a.arm} in the build palette")
else:
    scene.click_tile(site["x"] + (site["width"] - 1) / 2, site["y"] + (site["height"] - 1) / 2)
    scene.act_log(f"selected the {a.building} site")
time.sleep(a.wait)
for i in range(a.shots):
    if a.arm and a.hover:
        scene.click_tile(a.hover[0], a.hover[1], "ui_move")
    t = session.gtime()["tick"]
    side = scene.clean_shot(f"{a.out}-{t}.png")
    h = scene.hud_state()
    w = [b for b in session.world("summary")["colony"]["buildings"] if b["id"] == site["id"]]
    print(f"{a.out}-{t}.png", side["zone_outline_share_per_10000"], h["free"], h["events"], w[0].get("stock") if w else "built")
    time.sleep(2)
