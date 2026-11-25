#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Spectator-view captures (all colonies AI, fog of war off): frame and shoot.

usage: spectator.py MATCH TICK X Y OUT_PREFIX SECONDS [MAXSHOTS]

Loads the unmodified all-AI checkpoint (the game opens it in spectator view),
switches the Health and food bars lens off (key I), centres the camera on tile
X,Y by clicking the minimap (the minimap is drawn with team 0's start position
at its centre), lets the match run at normal speed and saves a frame whenever
the event list has at most two rows. Spectator view shows every colony's
buildings and units without fog; its "Show areas" option is off by default, so
no zone outlines are drawn. Label these frames as spectator view.
"""
import json
import os
import sys
import time

import mcp
import session

mcp.PORT = int(os.environ.get("GLOB2_MCP_PORT", "47815"))
MATCHES = os.environ["CAPTURE_MATCHES"]
PROFILE = os.environ["CAPTURE_PROFILE"]


def rows():
    n, labels, free = 0, [], None
    for _, c in mcp.walk(mcp.inspect()):
        k = c.get("key", "")
        if k.startswith("game/events/"):
            n += 1
            labels.append(c.get("label"))
        elif k == "game/stats/worker-count":
            free = c.get("value")
    return n, labels, free


def main(a):
    match, tick, x, y, prefix, secs = a[0], a[1], int(a[2]), int(a[3]), a[4], float(a[5])
    maxshots = int(a[6]) if len(a) > 6 else 3
    res = json.load(open(os.path.join(MATCHES, match, "result.json")))
    sx, sy = res["teams"][0]["start"]
    w = h = None
    for t in res["teams"]:
        pass
    src = os.path.join(MATCHES, match, f"checkpoint-{tick}.game.gz")
    session.load_save(src, PROFILE, settle=4)
    mcp.call("ui_key", {"token": mcp.token(), "key": "I"})
    view_team = os.environ.get("SPECTATOR_TEAM")
    if view_team is not None:
        mcp.act(f"spectator/team/{view_team}")  # whose statistics and event list the HUD shows
        time.sleep(0.5)
    mm = [c for _, c in mcp.walk(mcp.inspect()) if c.get("key") == "game/minimap"][0]["bounds"]
    mw = mm["w"]  # one logical pixel per tile on a 128-tile map
    scale = mw / 128.0
    size = 128
    mx = ((x - sx + size // 2) % size) * scale
    my = ((y - sy + size // 2) % size) * scale
    mcp.call("ui_click", {"token": mcp.token(), "x": (mm["x"] + mx) * 2 + 1, "y": (mm["y"] + my) * 2 + 1})
    time.sleep(1)
    end = time.time() + secs
    kept = 0
    last = 0
    while time.time() < end and kept < maxshots:
        n, labels, free = rows()
        if n <= 2 and time.time() - last > 4:
            path = f"{prefix}-{int(time.time())}.png"
            meta = mcp.screenshot(path)
            n2, labels2, free2 = rows()
            json.dump({"file": os.path.basename(path), "match": match, "source_tick": int(tick),
                       "seat": "spectator view (all colonies AI, fog of war off)", "camera_centre_tile": [x, y],
                       "zoom": 1.0, "rows_before": labels, "rows_after": labels2, "team0_workers_free": free,
                       "spectator_team_shown": os.environ.get("SPECTATOR_TEAM", "0"),
                       "player_actions_before_capture": ["pressed I: health and food bars off",
                                                         "clicked the minimap to centre the camera"],
                       "window": [meta.get("native_width"), meta.get("native_height")]},
                      open(path[:-4] + ".json", "w"), indent=1)
            print("kept", path, n, n2, free, flush=True)
            kept += 1
            last = time.time()
        time.sleep(0.2)


if __name__ == "__main__":
    main(sys.argv[1:])
