#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Capture storefront frames from recipes, through the game's MCP UI server.

usage: capture.py RECIPES.json OUT_DIR --matches DIR --profile DIR [--only ID[,ID]]

The capture game must already run (launch-capture-game.sh). For every recipe:

  1. join a local player to the recipe's colony in the headless save
     MATCHES/<match>/checkpoint-<tick>.game.gz (join-seat.py; cached under
     OUT_DIR/saves) and load it through the game's own Load game dialog;
  2. optionally erase the colony's forbidden/clearing area markings, as a
     player would from the Flags and areas panel;
  3. let the match run, at normal speed for the last stretch, until the
     recipe's capture tick;
  4. frame the camera with game_view and perform the recipe's interface steps
     (open a panel, select a building, arm a building or flag from the palette,
     hover a tile);
  5. save the next rendered frame at native pixels, with a JSON sidecar.

The match is never paused for a capture: a paused match shows a "Paused" label.

Recipe fields: id, shot, match, tick, team, at (absolute capture tick), view
{x, y, zoom}, erase_zones (bool), steps (list), description. Steps:
  {"panel": N}                      sidebar tab N (0 construction, 1 flags and areas, 2 statistics, 3 graphs)
  {"click_tile": [x, y]}            left click a map tile (selects what is there)
  {"click_building": {"type": T, "near": [x, y]}}   click the colony's building of type T nearest a tile
  {"arm": "KEY"}                    press a palette control, e.g. game/buildings/inn.0.site
  {"hover_tile": [x, y]}            move the pointer over a map tile
  {"act": "KEY"}                    press any inspected control
  {"sleep": seconds}
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time

import mcp
import session

HERE = os.path.dirname(os.path.abspath(__file__))
RENAMES = ["maxima=Maxima", "cortex=Cortex", "cabino=Cabino", "castor=Castor", "nicowar=Nicowar"]


CLOUDS_SET = False


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def joined_save(matches, out, recipe):
    name = f"{recipe['match']}-{recipe['tick']}-t{recipe['team']}"
    src = os.path.join(matches, recipe["match"], f"checkpoint-{recipe['tick']}.game.gz")
    dst = os.path.join(out, "saves", name + ".game.gz")
    if not os.path.exists(dst):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        cmd = [sys.executable, os.path.join(HERE, "join-seat.py"), src, dst, str(recipe["team"])]
        for r in RENAMES:
            cmd += ["--rename", r]
        subprocess.run(cmd, check=True, stderr=subprocess.DEVNULL)
    return src, dst


def zone_marks(path):
    """Share (per 10,000 map pixels) of the pure yellow that outlines forbidden areas.

    Needs Pillow and NumPy (`uv run --with pillow --with numpy`); returns None
    without them, and the erase is then not verified.
    """
    try:
        import numpy as np
        from PIL import Image
    except ImportError:
        return None
    with Image.open(path) as im:
        a = np.asarray(im.convert("RGB")).astype(int)[40:, : im.size[0] - 410]
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return float(((r > 235) & (g > 235) & (b < 40)).mean() * 1e4)


def map_centre():
    """Logical pixel at the middle of the map canvas: where game_view puts its tile."""
    for _, ctl in mcp.walk(mcp.inspect()):
        if ctl.get("key") == "game/map":
            b = ctl["bounds"]
            return b["x"] + b["w"] / 2, b["y"] + b["h"] / 2
    raise RuntimeError("no map canvas")


def tile_to_native(view, centre, tile, map_size, scale):
    """Native window pixel of a tile's centre, for a camera centred on `centre`.

    game_view centres the camera on a tile's centre; its tile_screen is not used
    because it can name an off-screen copy of a tile on the map's wrap-around.
    """
    def delta(a, b, size):
        d = (a - b) % size
        return d - size if d > size / 2 else d
    px = view["tile_pixels"]
    mx, my = map_centre()
    lx = mx + delta(tile[0], centre[0], map_size[0]) * px
    ly = my + delta(tile[1], centre[1], map_size[1]) * px
    return lx * scale, ly * scale


def run_until(tick):
    """Run to an absolute tick: 8x while far away, 2x closer in, then normal speed.

    A speed change takes a second or two to arrive while the match fast-forwards,
    so each stage ends well short of the target. The last 900 ticks or more run
    at normal speed, so the "Game speed" notice a change prints has left the
    screen before the capture.
    """
    now = session.gtime()["tick"]
    changed = False
    if tick - now > 4500:
        session.speed(7)  # 8x
        changed = True
        while session.gtime()["tick"] < tick - 3200:
            time.sleep(0.1)
    if tick - session.gtime()["tick"] > 1900:
        session.speed(3)  # 2x
        changed = True
        while session.gtime()["tick"] < tick - 1100:
            time.sleep(0.1)
    if changed:
        session.speed(0)
    while session.gtime()["tick"] < tick:
        time.sleep(0.05)
    return session.gtime()["tick"]


def capture(recipe, args, status):
    if recipe.get("spectator"):
        # The unmodified all-AI save: the game opens it in spectator view.
        src = save = os.path.join(args.matches, recipe["match"], f"checkpoint-{recipe['tick']}.game.gz")
    else:
        src, save = joined_save(args.matches, args.out, recipe)
    session.load_save(save, args.profile, settle=0.5)
    if not recipe.get("spectator"):
        # Hold the match (hard pause: not an order, nothing in the simulation
        # changes) while the match-intro card fades, and make sure it runs at
        # normal speed: the top-bar speed is a saved preference.
        session.gtime("pause")
        if session.gtime()["speed"] != "1x":
            session.speed(0)
        time.sleep(4.5)
        session.gtime("resume")
        global CLOUDS_SET
        if not CLOUDS_SET:
            # Once per run: Settings > Display & graphics > Clouds / Cloud shadows.
            # (--graphics-detail full or a fresh profile turns them on.)
            session.set_clouds(args.clouds == "on", args.clouds == "on")
            CLOUDS_SET = True
    if recipe.get("spectator"):
        mcp.act("game/panel/1")  # Statistics tab instead of the spectator options
    if recipe.get("spectator"):
        world = {"status": None}
        map_size = tuple(recipe["map_size"])
    else:
        world = session.world("summary")
        map_size = (world["map"]["width"], world["map"]["height"])
    scale = args.ui_scale
    v = dict(recipe["view"])
    if args.zoom_factor != 1.0:
        # A narrower window shows fewer tiles: pull back to keep the framing,
        # staying on the seam-free multiples of 1/8.
        # Not below 62.5%: further out the game switches to its icon overview.
        v["zoom"] = max(0.625, round(v.get("zoom", 1.0) * args.zoom_factor * 8) / 8)
    view = session.view(v["x"], v["y"], v.get("zoom", 1.0))
    run_until(recipe["at"] - (40 if recipe.get("erase_zones") else 0))
    view = session.view(v["x"], v["y"], v.get("zoom", 1.0))
    vt = view["view"]
    area = (vt["x"] - 2, vt["y"] - 2, vt["width"] + 4, vt["height"] + 4)

    def erase():
        # The colony's AI repaints its areas whenever it replans, sometimes within
        # seconds, and the game drops orders when too many queue up: erase just the
        # view, then check the frame and try again if the outlines are still there.
        session.erase_zones(area, map_size)
        time.sleep(0.5)
    if recipe.get("erase_zones"):
        erase()
    token = mcp.token()
    for step in recipe.get("steps", []):
        if "panel" in step:
            mcp.act(f"game/panel/{step['panel']}")
        elif "act" in step:
            mcp.act(step["act"])
        elif "arm" in step:
            mcp.act(step["arm"])
        elif "click_building" in step:
            want = step["click_building"]
            near = want.get("near", [v["x"], v["y"]])
            def dist(b):
                dx = abs(b["x"] - near[0]); dy = abs(b["y"] - near[1])
                return min(dx, map_size[0] - dx) + min(dy, map_size[1] - dy)
            own = [b for b in session.world("summary")["colony"]["buildings"]
                   if b["type"] == want["type"] and not b.get("site")]
            b = min(own, key=dist)
            tile = (b["x"] + (b["width"] - 1) / 2, b["y"] + (b["height"] - 1) / 2)
            x, y = tile_to_native(view, (v["x"], v["y"]), tile, map_size, scale)
            data, _, err = mcp.call("ui_click", {"token": token, "x": x, "y": y})
            if err:
                raise RuntimeError(f"ui_click: {data}")
            step["resolved"] = {"id": b["id"], "x": b["x"], "y": b["y"], "level": b["level"]}
        elif "click_tile" in step or "hover_tile" in step:
            tile = step.get("click_tile") or step.get("hover_tile")
            x, y = tile_to_native(view, (v["x"], v["y"]), tile, map_size, scale)
            tool = "ui_click" if "click_tile" in step else "ui_move"
            data, _, err = mcp.call(tool, {"token": token, "x": x, "y": y})
            if err:
                raise RuntimeError(f"{tool}: {data}")
        elif "sleep" in step:
            time.sleep(step["sleep"])
        time.sleep(0.25)
    time.sleep(recipe.get("settle", 0.4))
    name = f"{recipe['id']}-{status['width']}x{status['height']}.png"
    path = os.path.join(args.out, name)
    meta = session.shot(path)
    marks = zone_marks(path)
    attempts = 1
    while recipe.get("erase_zones") and marks is not None and marks > args.max_zone_marks and attempts < 8:
        erase()
        meta = session.shot(path)
        marks = zone_marks(path)
        attempts += 1
    state = session.gtime()
    tick = state["tick"]
    if state["speed"] != "1x" or state["paused"]:
        raise RuntimeError(f"not at normal speed at capture: {state}")
    # Further moments of the same scene: "also_at" ticks give <id>+<n> files.
    for n, later in enumerate(recipe.get("also_at", []), 1):
        run_until(later)
        extra = os.path.join(args.out, f"{recipe['id']}+{n}-{status['width']}x{status['height']}.png")
        if recipe.get("erase_zones"):
            erase()
        session.shot(extra)
        with open(extra[:-4] + ".json", "w") as fh:
            json.dump({"file": os.path.basename(extra), "recipe": dict(recipe, at=later), "tick_at_capture":
                       session.gtime()["tick"], "sha256": sha256(extra)}, fh, indent=1)
    sidecar = {
        "file": name,
        "recipe": recipe,
        "source_save": os.path.relpath(src, args.matches),
        "source_save_sha256": sha256(src),
        "seat": "spectator view (all colonies AI)" if recipe.get("spectator") else
                f"local player sharing colony {recipe['team']} with its AI",
        "joined_save": None if recipe.get("spectator") else os.path.relpath(save, args.out),
        "tick_at_capture": tick,
        "camera": {"centre_tile": [v["x"], v["y"]], "zoom": view["zoom"], "view_tiles": view["view"]},
        "zoom_factor": args.zoom_factor,
        "zone_outline_share_per_10000": marks,
        "erase_attempts": attempts if recipe.get("erase_zones") else 0,
        "window": [meta["native_width"], meta["native_height"]],
        "ui_scale": args.ui_scale,
        "clouds": args.clouds,
        "hd_artwork": "on (explicit setting); no step-down in the session log" if args.game_log else "not checked",
        "colony_status": world["status"],
        "sha256": sha256(path),
    }
    with open(path[:-4] + ".json", "w") as fh:
        json.dump(sidecar, fh, indent=1)
    print(f"{name}: tick {tick} zoom {view['zoom']} zone marks {marks} attempts {attempts}")
    return sidecar


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("recipes")
    ap.add_argument("out")
    ap.add_argument("--matches", required=True)
    ap.add_argument("--profile", required=True)
    ap.add_argument("--only")
    ap.add_argument("--ui-scale", type=float, default=2.0)
    ap.add_argument("--game-log", help="the capture game's log file; the run stops if it reports that HD "
                    "artwork was stepped down")
    ap.add_argument("--zoom-factor", type=float, default=1.0,
                    help="multiply every recipe zoom (snapped to 1/8), e.g. 0.75 for the 16:10 window")
    ap.add_argument("--max-zone-marks", type=float, default=6.0,
                    help="retry the erase while the frame's zone-outline share (per 10,000) is above this")
    ap.add_argument("--clouds", default="off", choices=["off", "on"],
                    help="cloud cover and cloud shadows; set through the game's settings and recorded")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    recipes = json.load(open(args.recipes))
    only = set(args.only.split(",")) if args.only else None
    status, _, _ = mcp.call("ui_status")

    def artwork_stepped_down():
        # With Artwork on Automatic the game turns HD artwork off for the session
        # when frames hitch (it logs "Device adaptation: ... stepped_down=1"), and
        # every later frame is magnified 32-pixel art. Refuse to go on.
        if not args.game_log:
            return False
        with open(args.game_log, errors="replace") as fh:
            return any("stepped_down=1" in line for line in fh)
    if artwork_stepped_down():
        raise SystemExit("the game log reports stepped_down=1: HD artwork is off in this session; set "
                         "highResolutionArtworkChoice=on in the profile's preferences.txt and relaunch")
    for recipe in recipes:
        if only and recipe["id"] not in only:
            continue
        try:
            capture(recipe, args, status)
        except Exception as exc:  # keep going: one bad recipe must not lose the rest
            print(f"{recipe['id']}: FAILED {exc}", file=sys.stderr)
        if artwork_stepped_down():
            raise SystemExit("HD artwork was stepped down during this run: discard its frames")


if __name__ == "__main__":
    main()
