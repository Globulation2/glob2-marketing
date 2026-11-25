#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Capture candidate store screenshots of live touch gameplay under the clean-state protocol.

    uv run --with pillow --with numpy python capture.py DEVICE --save NAME --slots hero,build,... [--tag T]
    uv run --with pillow --with numpy python capture.py DEVICE --menus

DEVICE: iphone-6.9, ipad-13 (the iOS app in the Simulator, portrait), android-phone
(portrait), android-tablet-7, android-tablet-10 (landscape); the Android classes are
host renders, see ../README.md.

The match is loaded through the game's own Load game screen and runs at normal
speed (1x) throughout; nothing is paused, stepped, composited or retouched. A frame
is kept only when, at the moment it is read:
  * the zone tool has just erased the co-controlling AI's zones and the saved image
    contains no zone outline (checked on the pixels);
  * the event list holds at most --rows rows (2 for colony shots, 3 for fights);
  * the first stat (free workers) is not negative.
Until then the script simply waits and tries again, so every kept frame is an
ordinary moment of the running match. Each frame gets a JSON sidecar recording
tick, camera, event rows, the stat and the player actions that preceded it.
"""
import argparse
import hashlib
import json
import math
import os
import subprocess
import sys
import time
from pathlib import Path

DEVICES = {
    "iphone-6.9": {"kind": "ios", "pixels": (1320, 2868), "points": 3, "sim": "IPHONE", "orientation": "portrait",
                   "model": "iPhone 17 Pro Max simulator, iOS 26.5"},
    "ipad-13": {"kind": "ios", "pixels": (2064, 2752), "points": 2, "sim": "IPAD", "orientation": "portrait",
                "model": "iPad Pro 13-inch (M5) simulator, iOS 26.5"},
    "android-phone": {"kind": "host", "pixels": (1080, 1920), "points": 2.625, "orientation": "portrait",
                      "model": "host render at 1080x1920 px, density 2.625 (420 dpi, 411x731 dp)"},
    "android-tablet-7": {"kind": "host", "pixels": (1920, 1200), "points": 2, "orientation": "landscape",
                         "model": "host render at 1920x1200 px, density 2.0 (960x600 dp)"},
    "android-tablet-10": {"kind": "host", "pixels": (2560, 1600), "points": 2, "orientation": "landscape",
                          "model": "host render at 2560x1600 px, density 2.0 (1280x800 dp)"},
}

# Screen geometry as fractions (x0, y0, x1, y1) of the frame, with at most two
# event rows showing. "free" is the map area no HUD covers; "palette" is where the
# build or flags palette opens; "card" where the inspector's dial or card sits;
# "clear" is the map area still uncovered while an inspector (header and dial, or card) is open.
LAYOUTS = {
    "iphone-6.9": {"free": (0.00, 0.265, 1.00, 0.905), "palette": (0.00, 0.57, 0.33, 0.905), "card": (0.22, 0.56, 1.0, 0.905),
                   "clear": (0.0, 0.375, 1.0, 0.53), "log": (0.0, 0.20, 1.0, 0.265)},
    "android-phone": {"free": (0.00, 0.205, 1.00, 0.925), "palette": (0.00, 0.49, 0.35, 0.925), "card": (0.22, 0.50, 1.0, 0.925),
                      "clear": (0.0, 0.325, 1.0, 0.50), "log": (0.0, 0.213, 1.0, 0.275)},
    "ipad-13": {"free": (0.045, 0.115, 1.00, 0.985), "palette": (0.045, 0.37, 0.29, 0.74), "card": (0.62, 0.43, 1.0, 0.77),
                "clear": (0.045, 0.115, 0.62, 0.985), "log": (0.33, 0.07, 0.75, 0.115)},
    "android-tablet-7": {"free": (0.085, 0.07, 1.00, 1.00), "palette": (0.085, 0.37, 0.49, 0.87), "card": (0.78, 0.32, 1.0, 0.88),
                         "clear": (0.085, 0.07, 0.78, 1.0), "log": (0.32, 0.23, 0.76, 0.33)},
    "android-tablet-10": {"free": (0.065, 0.05, 1.00, 1.00), "palette": (0.065, 0.40, 0.375, 0.78), "card": (0.83, 0.37, 1.0, 0.79),
                          "clear": (0.065, 0.05, 0.83, 1.0), "log": (0.36, 0.20, 0.71, 0.27)},
}
# On-screen size of one map tile in points: (overview shots, close shots).
TILE_POINTS = {"iphone-6.9": (21, 26), "android-phone": (21, 26), "android-tablet-7": (25, 30),
               "android-tablet-10": (28, 34), "ipad-13": (30, 36)}

parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("device", choices=sorted(DEVICES))
parser.add_argument("--save", help="save name in SCRATCH/saves (without .game.gz)")
parser.add_argument("--slots", default="hero,build,economy,fair_deal")
parser.add_argument("--menus", action="store_true", help="capture the map chooser and opponent picker instead of a match")
parser.add_argument("--tag", default="")
parser.add_argument("--rows", type=int, default=2, help="event rows allowed in colony shots")
parser.add_argument("--fight-rows", type=int, default=3, help="event rows allowed in battle, territory and opponents shots")
parser.add_argument("--wait", type=float, default=150, help="seconds to wait for a clean moment per frame")
parser.add_argument("--frames", type=int, default=3, help="clean frames to keep per shot")
parser.add_argument("--economy-rows", type=int, default=0, help="event rows allowed around the economy shot")
parser.add_argument("--fair-zoom", choices=("overview", "close"), default="overview", help="zoom for the fair_deal frame")
parser.add_argument("--fair-at", help="X,Y map tile to centre the fair_deal frame on instead of the best-scoring view")
parser.add_argument("--hero-fit", action="store_true",
                    help="frame the hero on every swimming pool and racetrack, zooming out (to 16 pt tiles at most) "
                         "until all of them fit whole in the free map area")
parser.add_argument("--fight-at", help="X,Y map tile of a known front (for example the colony's own border, which "
                                        "it sees lit) to aim the battle and territory frames at instead of the "
                                        "busiest rival window")
parser.add_argument("--maps-at", help="X,Y,POINTS: centre tile of the maps frame (placed at the centre of the free "
                                       "map area) and on-screen tile size in points")
parser.add_argument("--territory-at", help="X,Y map tile on the colony's own frontier to place the territory "
                                            "frame's war flag at")
parser.add_argument("--territory-max-dim", type=float, default=0.2,
                    help="largest fog-dimmed share of the free map area accepted in --territory-at frames")
parser.add_argument("--territory-delay", type=float, default=8.0,
                    help="seconds between placing the flag and the first frame, so warriors are on their way")
parser.add_argument("--fight-zoom", choices=("fight", "close", "overview"), default="fight",
                    help="zoom for battle frames")
parser.add_argument("--rows-margin", type=int, default=0,
                    help="ask for this many fewer event rows before the frame than the limit, so a row arriving "
                         "while a slow simulator screenshot is taken does not push the frame over the limit")
parser.add_argument("--keep", action="store_true", help="leave the game running afterwards")
args = parser.parse_args()

device = DEVICES[args.device]
layout = LAYOUTS[args.device]
if device["kind"] == "ios" and not os.environ.get("GLOB2_IOS_OWN_PORT"):
    # The simulator app shares the Mac's loopback; one fixed port unless the
    # caller runs the iPhone and iPad simulators at once (GLOB2_IOS_OWN_PORT=1
    # keeps GLOB2_MCP_PORT).
    os.environ["GLOB2_MCP_PORT"] = "47912"
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy  # noqa: E402
from PIL import Image  # noqa: E402

import g2  # noqa: E402
import mcp  # noqa: E402

width, height = device["pixels"]
orientation = device["orientation"]
out = g2.SCRATCH / "candidates2" / args.device
out.mkdir(parents=True, exist_ok=True)
tag = f"-{args.tag}" if args.tag else ""


# ------------------------------------------------------------------ target

if device["kind"] == "ios":
    ids = dict(line.split("=", 1) for line in (g2.SCRATCH / "sim.env").read_text().split())
    target = g2.IOS(ids[device["sim"]], orientation)
    target.boot()
    target.install()
    target.launch(saves=[g2.SAVES / f"{args.save}.game.gz"] if args.save else [])
    method = "simctl io screenshot of the iOS Simulator framebuffer"
else:
    profile = g2.SCRATCH / "profiles" / f"{args.device}-{g2.PORT}"
    subprocess.run(["rm", "-rf", str(profile)])
    g2.write_profile(profile, [g2.SAVES / f"{args.save}.game.gz"] if args.save else [])
    target = g2.Host(width, height, device["points"], "touch", profile)
    method = "game ui_screenshot (renderer output at native pixels)"


def island_visible(path):
    """The simulator intermittently paints the Dynamic Island into its framebuffer;
    device screenshots never contain it, so such frames are retaken."""
    if args.device != "iphone-6.9":
        return False
    with Image.open(path) as image:
        image = image.convert("RGB")
        return all(image.getpixel(p) == (0, 0, 0) for p in ((660, 95), (600, 95), (720, 95)))


def grab(path):
    if device["kind"] == "ios":
        for _ in range(10):
            target.shot(path)
            if not island_visible(path):
                return True
            time.sleep(0.3)
        return False
    g2.host_shot(path)
    return True


def zone_outline_pixels(path, run, thick):
    """Pixels on thin straight runs of the forbidden (255,0,0) and clearing (255,255,0)
    outline colours at least `run` pixels long. Zero means no zone square is drawn.
    Thick red shapes (Swarm crystals, buttons) are not lines and do not count."""
    a = numpy.asarray(Image.open(path).convert("RGB")).astype(numpy.int16)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    total = 0
    for colour in ((r > 225) & (g < 60) & (b < 60), (r > 225) & (g > 225) & (b < 100)):
        for mask in (colour, colour.T):
            before = numpy.zeros_like(mask)
            before[thick:, :] = mask[:-thick, :]
            after = numpy.zeros_like(mask)
            after[:-thick, :] = mask[thick:, :]
            thin = mask & ~before & ~after
            c = numpy.cumsum(thin, axis=1)
            total += int(((c[:, run:] - c[:, :-run]) >= run).sum())
    return total


def dim_fraction(path):
    """Share of the free map area drawn as fog-dimmed grass (dark and green)."""
    free = LAYOUTS[args.device]["free"]
    with Image.open(path) as image:
        w, h = image.size
        crop = image.convert("RGB").crop((int(free[0] * w), int(free[1] * h), int(free[2] * w), int(free[3] * h)))
    a = numpy.asarray(crop.resize((crop.width // 4, crop.height // 4))).astype(numpy.int16)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    luminance = 0.3 * r + 0.59 * g + 0.11 * b
    return round(float(((luminance < 70) & (g > r) & (g > b)).mean()), 3)


# ------------------------------------------------------------------ helpers

camera = {}
actions = set()
map_w = map_h = 128
overview_zoom = close_zoom = fight_zoom = 1.0
units_per_point = 1.0


def calibrate():
    global overview_zoom, close_zoom, fight_zoom, units_per_point
    reply = g2.view(zoom=1.0)
    logical_width = max(reply["view"]["width"] * reply["tile_pixels"], 2 * reply["tile_screen"]["x"])
    units_per_point = logical_width / (width / device["points"])
    overview, close = TILE_POINTS[args.device]
    overview_zoom = round(overview * units_per_point / 32, 3)
    close_zoom = round(close * units_per_point / 32, 3)
    fight_zoom = round(close * 1.25 * units_per_point / 32, 3)
    print(f"{units_per_point:.3f} units/pt, zoom overview {overview_zoom} close {close_zoom}", flush=True)


def view_tiles(zoom):
    """Width and height of the screen in map tiles at this zoom."""
    tile_points = 32 * zoom / units_per_point
    return (width / device["points"]) / tile_points, (height / device["points"]) / tile_points


def torus_delta(a, b, size):
    d = (a - b) % size
    return d - size if d > size / 2 else d


def look(x, y, zoom, at=(0.5, 0.5)):
    """Put map tile (x, y) at the screen fraction `at`."""
    global camera
    vw, vh = view_tiles(zoom)
    cx = (x - (at[0] - 0.5) * vw) % map_w
    cy = (y - (at[1] - 0.5) * vh) % map_h
    for attempt in range(3):
        try:
            reply = g2.view(x=int(round(cx)) % map_w, y=int(round(cy)) % map_h, zoom=zoom)
            break
        except RuntimeError:  # "Input dispatch interrupted": the game was busy; ask again
            if attempt == 2:
                raise
            time.sleep(1.5)
    camera = {"tile": [int(round(cx)) % map_w, int(round(cy)) % map_h], "zoom": reply["zoom"], "view_tiles": reply["view"]}
    return reply


def tap_tile(reply, x, y):
    px = reply["tile_screen"]["x"] + torus_delta(x, camera["tile"][0], map_w) * reply["tile_pixels"]
    py = reply["tile_screen"]["y"] + torus_delta(y, camera["tile"][1], map_h) * reply["tile_pixels"]
    g2.click(px, py, space="logical")


def keys():
    return {c.get("key"): c for _, c in g2.controls()}


def event_rows():
    return [c.get("label") for _, c in g2.controls() if str(c.get("key")).startswith("game/events/")]


def first_stat():
    return g2.call("game_world", include=["status"])["status"]["hud_sampled"]["workers"]


def colony_buildings():
    return g2.call("game_world", include=["colony"])["colony"]["buildings"]


def continue_playing():
    """The late save is won about 80 seconds after loading; the end-of-match dialog
    offers Continue playing, which a player who wants to keep going would press."""
    for _, control in g2.controls():
        if control.get("label") == "Continue playing" and control.get("key"):
            g2.act(control["key"])
            time.sleep(1.0)
            actions.add("end-of-match dialog (You have won): Continue playing")
            print("   match won: Continue playing", flush=True)
            return True
    return False


def close_panels():
    continue_playing()
    for _ in range(4):
        present = keys()
        if "touch/inspector/close" in present:
            g2.act("touch/inspector/close")
        elif any(present.get(f"touch/navigation/{k}", {}).get("selected") for k in ("buildings", "flags", "tools")):
            for k in ("buildings", "flags", "tools"):
                if present.get(f"touch/navigation/{k}", {}).get("selected"):
                    g2.act(f"touch/navigation/{k}")
        else:
            return
        time.sleep(0.5)


def bars_off():
    """The Tools strip's "Health and food bars" lens, as a player would toggle it."""
    close_panels()
    g2.act("touch/navigation/tools")
    time.sleep(0.6)
    lens = keys().get("touch/lens/6")
    if lens is not None and lens.get("selected"):
        g2.act("touch/lens/6")
        time.sleep(0.4)
    close_panels()
    actions.add("Tools strip: Health and food bars lens switched off")


def erase_zones():
    """Zone tool, erase mode, whole map: the co-controlling AI repaints within seconds."""
    for zone in ("forbidden", "clearing", "guard"):
        for x in range(0, map_w, 64):
            for y in range(0, map_h, 64):
                g2.tcall("game_zone", zone=zone, mode="erase", x=x, y=y,
                         width=min(64, map_w - x), height=min(64, map_h - y))
    actions.add("zone tool: erased the forbidden, guard and clearing zones painted by the co-controlling AI")


def clean_frames(name, note, max_rows, count=None, gap=2.0, extra=None, check=None, max_dim=1.0, arm=None,
                 disarm=None):
    """Wait for clean moments and keep up to `count` frames; returns how many were kept.

    The event list is not readable while a building inspector is open, so a
    shot that needs one passes `arm` (open it; false if that failed) and
    `disarm` (close it): rows are then counted with the inspector closed just
    before it opens and again just after the frame, inside the time a row stays
    on screen."""
    count = count or args.frames
    kept, tries, least = 0, 0, 99
    rejected = {}
    deadline = time.time() + args.wait
    run = max(18, int(0.7 * 32 * camera["zoom"] / units_per_point * device["points"]))
    scratch = out / f".{name}{tag}.tmp.png"
    while kept < count and time.time() < deadline:
        if disarm:
            disarm()
        elif continue_playing():
            continue
        erase_zones()
        time.sleep(0.25)
        rows = event_rows()
        least = min(least, len(rows))
        stat = first_stat()
        if len(rows) > max_rows - args.rows_margin or stat.startswith("-"):
            time.sleep(0.2)
            continue
        if (arm and not arm()) or (check and not check()):
            time.sleep(0.2)
            continue
        if arm:
            # The AI may have repainted while the inspector opened.
            erase_zones()
        status = g2.game_time()
        tries += 1
        if not grab(scratch):
            continue
        if disarm:
            disarm()
        after = event_rows()
        squares = zone_outline_pixels(scratch, run, max(8, int(3.5 * device["points"])))
        dim = dim_fraction(scratch)
        if squares or len(after) > max_rows or dim > max_dim:
            why = "zone squares" if squares else "rows after" if len(after) > max_rows else "fog"
            rejected[why] = rejected.get(why, 0) + 1
            if os.environ.get("GLOB2_CAPTURE_DEBUG"):
                scratch.replace(out / f".reject-{name}{tag}.png")
            continue
        kept += 1
        path = out / f"{name}{tag}-{kept}.png"
        scratch.replace(path)
        meta = {
            "file": path.name, "shot": name, "note": note, "device_class": args.device, "orientation": orientation,
            "pixels": [width, height], "device": device["model"], "method": method, "save": args.save,
            "tick": status["tick"], "speed": status["speed"], "paused": status["paused"], "camera": camera,
            "event_rows": max(rows, after, key=len), "event_rows_before": rows, "event_rows_after": after,
            "first_stat": stat, "zone_outline_pixels": squares,
            "fog_dimmed_fraction": dim,
            "hd_artwork": g2.HD_ARTWORK,
            "actions": sorted(actions), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }
        meta.update(extra or {})
        path.with_suffix(".json").write_text(json.dumps(meta, indent=1) + "\n")
        print(f"   {path.name} tick {status['tick']} rows {len(rows)} stat {stat} dim {dim}", flush=True)
        if kept < count:
            time.sleep(gap)
    if scratch.exists():
        scratch.unlink()
    if kept < count:
        print(f"   {name}: kept {kept}/{count} (fewest rows seen {least}, frames tried {tries}, rejected {rejected})", flush=True)
    return kept


# ------------------------------------------------------------------ view choice

WEIGHT = {"swimmingpool": 5, "racetrack": 5, "school": 4, "barracks": 4, "swarm": 3, "defencetower": 2, "market": 3}


def rect_of(fractions, left, top, vw, vh):
    return (left + fractions[0] * vw, top + fractions[1] * vh, left + fractions[2] * vw, top + fractions[3] * vh)


def overlap(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def inside(a, b, margin=0.3):
    return a[0] >= b[0] + margin and a[1] >= b[1] + margin and a[2] <= b[2] - margin and a[3] <= b[3] - margin


def best_view(buildings, zoom, occluders=(), avoid=(), separation=0, need=()):
    """Screen-centre tile showing the most colony in the free map area: whole core
    buildings count most, half-cut ones and an empty lower third count against."""
    vw, vh = view_tiles(zoom)
    ox = sum(math.cos(2 * math.pi * (b["x"] + b["width"] / 2) / map_w) for b in buildings)
    oy = sum(math.sin(2 * math.pi * (b["x"] + b["width"] / 2) / map_w) for b in buildings)
    home_x = (math.atan2(oy, ox) / (2 * math.pi) * map_w) % map_w
    ox = sum(math.cos(2 * math.pi * (b["y"] + b["height"] / 2) / map_h) for b in buildings)
    oy = sum(math.sin(2 * math.pi * (b["y"] + b["height"] / 2) / map_h) for b in buildings)
    home_y = (math.atan2(oy, ox) / (2 * math.pi) * map_h) % map_h
    boxes = []
    for b in buildings:
        x0 = torus_delta(b["x"], home_x, map_w)
        y0 = torus_delta(b["y"], home_y, map_h)
        boxes.append((b["type"], bool(b.get("site")), (x0, y0, x0 + b["width"], y0 + b["height"])))
    span_x = range(int(min(r[0] for _, _, r in boxes)) - 2, int(max(r[2] for _, _, r in boxes)) + 3)
    span_y = range(int(min(r[1] for _, _, r in boxes)) - 2, int(max(r[3] for _, _, r in boxes)) + 3)
    best = None
    for cy in span_y:
        for cx in span_x:
            if any(abs(cx - torus_delta(ax, home_x, map_w)) < separation and abs(cy - torus_delta(ay, home_y, map_h)) < separation
                   for ax, ay in avoid):
                continue
            left, top = cx - vw / 2, cy - vh / 2
            screen = (left, top, left + vw, top + vh)
            free = rect_of(layout["free"], left, top, vw, vh)
            hidden = [rect_of(layout[o], left, top, vw, vh) for o in occluders]
            soft = rect_of(layout["log"], left, top, vw, vh)
            lower_from = free[1] + (free[3] - free[1]) * 2 / 3
            score, lower, kinds = 0.0, 0, set()
            for kind, site, box in boxes:
                weight = WEIGHT.get(kind, 1.2) * (0.5 if site else 1)
                large = kind in WEIGHT
                if inside(box, free):
                    if any(overlap(box, h) for h in hidden):
                        score -= 3 if large else 1
                    elif overlap((box[0], box[1] - 0.6 * (box[3] - box[1]), box[2], box[3]), soft):
                        # Under the event list: the rows would sit on the building.
                        score -= 2 if large else 1
                    else:
                        score += weight
                        kinds.add(kind)
                        lower += (box[1] + box[3]) / 2 >= lower_from
                elif overlap(box, screen) and overlap(box, (screen[0], free[1], screen[2], screen[3])):
                    score -= 7 if large else 0.8
            score += 2 * min(lower, 4) - (6 if lower == 0 else 0) + len(kinds)
            score -= 8 * sum(1 for kind in need if kind not in kinds)
            if best is None or score > best[0]:
                best = (score, (cx + home_x) % map_w, (cy + home_y) % map_h, sorted(kinds), lower)
    return best


def settle_view(x, y, zoom):
    reply = look(x, y, zoom)
    time.sleep(1.2)
    return reply


# ------------------------------------------------------------------ colony shots

chosen = {}


def own_buildings():
    return [b for b in colony_buildings() if b.get("width", 0) > 0 and "flag" not in b["type"]]


def fit_core(buildings):
    """Centre tile and zoom that show every pool and racetrack whole in the free map area."""
    core = [b for b in buildings if b["type"] in ("swimmingpool", "racetrack") and not b.get("site")]
    if not core:
        return None
    ax, ay = core[0]["x"], core[0]["y"]
    x0 = min(ax + torus_delta(b["x"], ax, map_w) for b in core)
    y0 = min(ay + torus_delta(b["y"], ay, map_h) for b in core)
    x1 = max(ax + torus_delta(b["x"], ax, map_w) + b["width"] for b in core)
    y1 = max(ay + torus_delta(b["y"], ay, map_h) + b["height"] for b in core)
    free = layout["free"]
    screen_w, screen_h = width / device["points"], height / device["points"]
    points = min(TILE_POINTS[args.device][0],
                 screen_w * (free[2] - free[0]) / (x1 - x0 + 2.5),
                 screen_h * (free[3] - free[1]) / (y1 - y0 + 2.5))
    points = max(points, 16)
    zoom = round(points * units_per_point / 32, 3)
    # The core sits on the bottom of the free area so the rest of the colony
    # fills the band above it (south of the core is the colony's edge).
    vh = view_tiles(zoom)[1]
    at = ((free[0] + free[2]) / 2, max((free[1] + free[3]) / 2, free[3] - ((y1 - y0) / 2 + 1.3) / vh))
    return ((x0 + x1) / 2) % map_w, ((y0 + y1) / 2) % map_h, zoom, at, round(points, 1), len(core)


def shot_hero():
    close_panels()
    buildings = own_buildings()
    if args.hero_fit:
        fit = fit_core(buildings)
        if fit:
            x, y, zoom, at, points, n = fit
            print(f"   hero fit on {n} pools/racetracks: centre {x:.0f},{y:.0f} tile {points} pt zoom {zoom}", flush=True)
            chosen["hero"] = (x, y)
            look(x, y, zoom, at=at)
            time.sleep(1.2)
            clean_frames("hero", "every pool and racetrack of the colony core in view", args.rows, gap=4.0,
                         max_dim=0.15, extra={"buildings_in_view": ["swimmingpool", "racetrack"]})
            return
    score, x, y, kinds, lower = best_view(buildings, overview_zoom,
                                          need=("swimmingpool", "racetrack", "barracks", "school"))
    print(f"   hero view {x:.0f},{y:.0f} score {score:.1f} kinds {kinds} lower-third buildings {lower}", flush=True)
    chosen["hero"] = (x, y)
    settle_view(x, y, overview_zoom)
    clean_frames("hero", "colony core with the touch HUD", args.rows, gap=4.0, max_dim=0.15, extra={"buildings_in_view": kinds})


def shot_fair_deal():
    close_panels()
    buildings = own_buildings()
    avoid = [chosen[k] for k in ("hero", "build") if k in chosen]
    if "hero" not in chosen:
        avoid.append(best_view(buildings, overview_zoom, need=("swimmingpool", "racetrack", "barracks", "school"))[1:3])
    # Far enough from the hero and build views that the frames barely overlap.
    zoom = close_zoom if args.fair_zoom == "close" else overview_zoom
    apart = max(14, 0.6 * min(view_tiles(zoom)))
    score, x, y, kinds, lower = best_view(buildings, zoom, avoid=avoid, separation=apart)
    if args.fair_at:
        x, y = (float(v) for v in args.fair_at.split(","))
    print(f"   fair_deal view {x:.0f},{y:.0f} score {score:.1f} kinds {kinds} lower {lower}", flush=True)
    chosen["fair_deal"] = (x, y)
    settle_view(x, y, zoom)
    clean_frames("fair_deal", "a different part of the colony", args.rows, gap=4.0, max_dim=0.15, extra={"buildings_in_view": kinds})


def shot_build():
    close_panels()
    buildings = own_buildings()
    avoid = [chosen["hero"]] if "hero" in chosen else []
    score, x, y, kinds, lower = best_view(buildings, overview_zoom, occluders=("palette",), avoid=avoid, separation=5)
    print(f"   build view {x:.0f},{y:.0f} score {score:.1f} kinds {kinds} lower {lower}", flush=True)
    chosen["build"] = (x, y)
    settle_view(x, y, overview_zoom)
    g2.act("touch/navigation/buildings")
    time.sleep(1.0)
    clean_frames("build", "build palette open over the live colony", args.rows, gap=4.0,
                 check=lambda: bool(keys().get("touch/navigation/buildings", {}).get("selected")),
                 extra={"buildings_in_view": kinds})
    close_panels()


def food(b):
    try:
        return int(str(b.get("stock", {}).get("food", "0/0")).split("/")[0])
    except ValueError:
        return 0


def shot_economy():
    """An Inn that is not upgrading, so the inspector shows its food lines, placed so
    that a Swarm and, where the map allows, a wheat field share the uncovered area."""
    close_panels()
    # With an inspector open the navigation keeps the last opened section
    # marked; after the Tools strip that leaves a stray marker on Tools.
    g2.act("touch/navigation/buildings")
    time.sleep(0.6)
    close_panels()
    buildings = own_buildings()
    swarms = [b for b in buildings if b["type"] == "swarm"]
    wheat = g2.call("game_world", include=["resources"], resource_fields=10).get("resources", {}).get("wheat", {})
    fields = [(f["x"], f["y"], math.sqrt(max(f.get("tiles", 1), 1) / math.pi)) for f in wheat.get("fields", [])]
    vw, vh = view_tiles(close_zoom)
    clear = layout["clear"]
    spots = [(clear[0] + (clear[2] - clear[0]) * fx, clear[1] + (clear[3] - clear[1]) * fy)
             for fx in (0.2, 0.35, 0.5, 0.65, 0.8) for fy in ((0.5,) if orientation == "portrait" and args.device != "ipad-13"
                                                               else (0.3, 0.5, 0.7))]
    options = []
    for inn in buildings:
        if inn["type"] != "inn" or inn.get("site"):
            continue
        bx, by = inn["x"] + inn["width"] / 2, inn["y"] + inn["height"] / 2
        for at in spots:
            left, top = bx - at[0] * vw, by - at[1] * vh
            area = rect_of(clear, left, top, vw, vh)
            screen = (left, top, left + vw, top + vh)
            score, seen = 0.0, []
            for b in buildings:
                x0 = bx + torus_delta(b["x"], bx, map_w)
                y0 = by + torus_delta(b["y"], by, map_h)
                box = (x0, y0, x0 + b["width"], y0 + b["height"])
                if inside(box, area, 0.1):
                    score += 3 if b["type"] == "swarm" and "swarm" not in seen else 0.3
                    seen.append(b["type"])
            for fx, fy, radius in fields:
                x0, y0 = bx + torus_delta(fx, bx, map_w), by + torus_delta(fy, by, map_h)
                reach = min(radius, 6)
                if overlap((x0 - reach, y0 - reach, x0 + reach, y0 + reach), area):
                    score += 2
                    seen.append("wheat")
                    break
            score += (food(inn) > 0) + 0.3 * inn.get("level", 1)
            options.append((score, inn["id"], at, inn, sorted(set(seen))))
    options.sort(key=lambda o: -o[0])
    done, used = 0, set()
    for score, _, at, inn, seen in options:
        if inn["id"] in used:
            continue
        used.add(inn["id"])
        close_panels()
        bx, by = inn["x"] + inn["width"] / 2, inn["y"] + inn["height"] / 2
        print(f"   inn {inn['x']},{inn['y']} level {inn.get('level')} score {score:.1f} with {seen}", flush=True)
        reply = look(bx, by, close_zoom, at=at)
        time.sleep(1.0)

        def select(reply=reply, bx=bx, by=by):
            for dx in (0, -0.4):
                tap_tile(reply, bx + dx, by + dx)
                time.sleep(1.0)
                if any(k and k.startswith("touch/building/") for k in keys()):
                    return True
            if os.environ.get("GLOB2_CAPTURE_DEBUG"):
                print("   select failed; controls:", [k for k in keys() if k and k.startswith("touch/")], flush=True)
                grab(out / f".debug-select{tag}.png")
            return False

        if not select():
            print("   inspector did not open", flush=True)
            continue
        now = next((b for b in colony_buildings() if b["id"] == inn["id"]), inn)
        if now.get("site"):
            continue
        kept = clean_frames(f"economy{done + 1}", "Inn selected: food and fruit stock, workers and priority",
                            args.economy_rows, count=2, gap=3.0, arm=select, disarm=close_panels,
                            extra={"selected": {"type": "inn", "x": inn["x"], "y": inn["y"], "level": inn.get("level"),
                                                "stock": now.get("stock")}, "also_in_view": seen})
        done += kept > 0
        if done >= 3 or len(used) >= 6:
            break
    close_panels()


# ------------------------------------------------------------------ fights

def enemy_windows(min_teams=1, kinds=("warrior",)):
    """Windows the size of the free map area holding the most rival units in sight."""
    vw, vh = view_tiles(fight_zoom)
    free = layout["free"]
    w = max(8, min(40, int(vw * (free[2] - free[0]) * 0.9)))
    h = max(8, min(40, int(vh * (free[3] - free[1]) * 0.8)))
    found = []
    for y in range(0, map_h - h + 1, 4):
        for x in range(0, map_w - w + 1, 4):
            reply = g2.call("game_world", area={"x": x, "y": y, "width": w, "height": h}, include=["others", "counts"])
            teams = {}
            for key, n in (reply["others"].get("units_by_team_and_type") or {}).items():
                team, kind = key.split(":")
                if kind in kinds:
                    teams[team] = teams.get(team, 0) + n
            strong = {t: n for t, n in teams.items() if n >= 3}
            if len(strong) >= min_teams and sum(teams.values()) >= 8:
                found.append({"x": x + w / 2, "y": y + h / 2, "teams": teams, "strong": len(strong),
                              "units": sum(teams.values()), "enemy_buildings": reply["counts"].get("enemy_buildings", 0),
                              "own_buildings": reply["counts"].get("buildings", 0)})
    return found


def recent_fights():
    recent = g2.call("game_world", detail="alerts", since_tick=max(0, g2.tick() - 300))
    return [a for a in recent.get("alerts", []) if a.get("kind") in ("unit_attacked", "building_attacked")
            and "Explorer" not in (a.get("event") or "")]


def nearest_fight(window, fights, reach=14):
    near = [a for a in fights if abs(torus_delta(a["x"], window["x"], map_w)) < reach
            and abs(torus_delta(a["y"], window["y"], map_h)) < reach]
    return max(near, key=lambda a: a.get("n") or 0) if near else None


def free_centre():
    free = layout["free"]
    return ((free[0] + free[2]) / 2, free[1] + (free[3] - free[1]) * 0.55)


def pinned_site():
    """The --fight-at front, with the rival units and buildings around it."""
    fx, fy = (float(v) for v in args.fight_at.split(","))
    vw, vh = view_tiles(fight_zoom)
    w, h = int(min(40, vw * 0.9)), int(min(40, vh * 0.6))
    reply = g2.call("game_world", area={"x": int(fx - w / 2) % map_w, "y": int(fy - h / 2) % map_h, "width": w,
                                        "height": h}, include=["others", "counts"])
    teams = {}
    for key, n in (reply["others"].get("units_by_team_and_type") or {}).items():
        team, kind = key.split(":")
        if kind == "warrior":
            teams[team] = teams.get(team, 0) + n
    return {"x": fx, "y": fy, "teams": teams, "strong": sum(1 for n in teams.values() if n >= 3),
            "units": sum(teams.values()), "enemy_buildings": reply["counts"].get("enemy_buildings", 0),
            "own_buildings": reply["counts"].get("buildings", 0), "pinned": True}


def fight_site(min_teams, kinds):
    if args.fight_at:
        return [pinned_site()]
    fights = recent_fights()
    windows = []
    for window in enemy_windows(min_teams, kinds):
        fight = nearest_fight(window, fights)
        if fight:
            # Aim at our own units under attack: that is where the two lines meet.
            window["x"] += torus_delta(fight["x"], window["x"], map_w) * 0.8
            window["y"] += torus_delta(fight["y"], window["y"], map_h) * 0.8
            window["reports"] = fight.get("n") or 0
            windows.append(window)
    windows.sort(key=lambda w: (-w["strong"], -(w["units"] + 3 * min(w["enemy_buildings"], 3) + 2 * min(w["own_buildings"], 3))))
    return windows


def shot_battle(name="battle", min_teams=1, rounds=3, kinds=("warrior",), patience=300):
    """Up to `rounds` fights; the front comes and goes, so keep looking for `patience` seconds."""
    close_panels()
    found, until = 0, time.time() + patience
    while found < rounds and time.time() < until:
        windows = fight_site(min_teams, kinds)
        if not windows:
            print("   no fight with enough rival units in sight", flush=True)
            time.sleep(8)
            continue
        found += 1
        site = windows[0]
        print(f"   {name} site {site}", flush=True)
        zoom = {"fight": fight_zoom, "close": close_zoom, "overview": overview_zoom}[args.fight_zoom]
        look(site["x"], site["y"], zoom, at=free_centre())
        time.sleep(1.0)
        clean_frames(f"{name}{found}", "fight at the rival colony", args.fight_rows, count=4, gap=1.5,
                     extra={"rival_units_in_view_by_team": site["teams"], "enemy_buildings_near": site["enemy_buildings"]})
        time.sleep(3)


def shot_opponents():
    shot_battle("opponents", min_teams=3, rounds=4, kinds=("warrior", "worker"))


def shot_territory_at():
    """--territory-at: a war flag placed by the player on the colony's own frontier
    (which the colony sees lit), then the Flags palette opened over the warriors
    walking out to it."""
    close_panels()
    fx, fy = (int(float(v)) for v in args.territory_at.split(","))
    session = g2.call("game_world", include=["status"])["session"]
    g2.tcall("game_place", building="warflag", x=fx, y=fy, near=True, search_radius=4, workers=12, range=5,
             session=session)
    action = f"placed a war flag at {fx},{fy} (12 warriors, range 5)"
    actions.add(action)
    zoom = {"fight": fight_zoom, "close": close_zoom, "overview": overview_zoom}[args.fight_zoom]
    look(fx, fy, zoom, at=free_centre())
    time.sleep(args.territory_delay)
    g2.act("touch/navigation/flags")
    time.sleep(2.0)
    clean_frames("territory9", "Flags palette open, a war flag just placed at the front", args.rows,
                 count=4, gap=3.0, check=lambda: bool(keys().get("touch/navigation/flags", {}).get("selected")),
                 max_dim=args.territory_max_dim, extra={"flag_placed_at": [fx, fy]})
    close_panels()
    actions.discard(action)


def shot_territory():
    """A war flag placed at the front as the player, then the Flags palette opened
    over the warriors answering it. (The game draws a flag's range circle only while
    the flag is selected or being placed, so no circle shows in this state.)"""
    if args.territory_at:
        return shot_territory_at()
    close_panels()
    for attempt in range(2):
        windows = fight_site(1, ("warrior",))
        if not windows:
            time.sleep(8)
            continue
        site = windows[0]
        session = g2.call("game_world", include=["status"])["session"]
        g2.tcall("game_place", building="warflag", x=int(site["x"]), y=int(site["y"]), near=True, search_radius=6,
                 workers=12, range=5, session=session)
        actions.add("placed a war flag at the front (12 warriors, range 5)")
        look(site["x"], site["y"], close_zoom, at=free_centre())
        g2.act("touch/navigation/flags")
        time.sleep(3.0)
        clean_frames(f"territory{attempt + 1}", "Flags palette open at the front, a war flag just placed", args.fight_rows,
                     count=3, gap=2.0, check=lambda: bool(keys().get("touch/navigation/flags", {}).get("selected")),
                     extra={"flag_near": [int(site["x"]), int(site["y"])], "rival_units_in_view_by_team": site["teams"]})
        close_panels()
        actions.discard("placed a war flag at the front (12 warriors, range 5)")
        time.sleep(4)


def shot_maps():
    """The second map: the colony itself, same rules as the hero."""
    close_panels()
    buildings = own_buildings()
    fit = fit_core(buildings) if args.hero_fit else None
    if args.maps_at:
        mx, my, points = (float(v) for v in args.maps_at.split(","))
        fit = (mx, my, round(points * units_per_point / 32, 3), free_centre(), points, 0)
    if fit:
        x, y, zoom, at, points, n = fit
        print(f"   maps fit on {n} pools/racetracks: centre {x:.0f},{y:.0f} tile {points} pt zoom {zoom}", flush=True)
        look(x, y, zoom, at=at)
        time.sleep(1.2)
        clean_frames("maps", "colony on a second map, every pool and racetrack in view", args.rows, gap=4.0,
                     max_dim=0.15, extra={"buildings_in_view": ["swimmingpool", "racetrack"]})
        return
    score, x, y, kinds, lower = best_view(buildings, overview_zoom)
    print(f"   maps view {x:.0f},{y:.0f} score {score:.1f} kinds {kinds} lower {lower}", flush=True)
    settle_view(x, y, overview_zoom)
    clean_frames("maps", "colony on a second map", args.rows, gap=4.0, max_dim=0.15, extra={"buildings_in_view": kinds})


SHOTS = {"hero": shot_hero, "build": shot_build, "economy": shot_economy, "fair_deal": shot_fair_deal,
         "battle": shot_battle, "territory": shot_territory, "maps": shot_maps, "opponents": shot_opponents}


# ------------------------------------------------------------------ menus

def menu_frame(name, note):
    path = out / f"{name}-1.png"
    grab(path)
    meta = {"file": path.name, "shot": name, "note": note, "device_class": args.device, "orientation": orientation,
            "pixels": [width, height], "device": device["model"], "method": method, "save": None, "tick": None,
            "speed": None, "paused": None, "camera": None, "event_rows": [], "first_stat": None,
            "zone_outline_pixels": 0, "actions": [], "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "menu": True,
            "hd_artwork": g2.HD_ARTWORK}
    path.with_suffix(".json").write_text(json.dumps(meta, indent=1) + "\n")
    print("  ", path.name, flush=True)


def menus():
    g2.wait_screen("main_menu", 120)
    time.sleep(1.0)
    g2.act("menu/3")
    g2.wait_screen("custom_game")
    time.sleep(5)
    # Maps: the landscape picker with one generated preview per map generator.
    g2.act("generator/landscape")
    g2.wait_screen("landscape_picker")
    time.sleep(3)
    for name, amount in (("maps-menu-top", -20000), ("maps-menu-mid", 2400), ("maps-menu-low", 2400)):
        try:
            g2.act("landscape/grid", "scroll", amount)
        except RuntimeError as error:
            print("   scroll:", str(error)[:160])
        time.sleep(6)
        menu_frame(name, "landscape picker (the map generators) in the custom game setup")
    for _, control in g2.controls():
        label = str(control.get("label") or "")
        if control.get("key") and "activate" in control.get("actions", []) and (label.startswith("Use") or label == "Back"):
            g2.act(control["key"])
            break
    g2.wait_screen("custom_game")
    time.sleep(1.5)
    # Opponents last (the open picker is left for the process exit to discard).
    g2.act("tab/1")
    time.sleep(1.5)
    menu_frame("opponents-menu-players", "custom game Players tab")
    g2.act("players/ai")
    time.sleep(1.5)
    menu_frame("opponents-menu-picker", "computer opponent picker in the custom game setup")


try:
    if args.menus:
        menus()
    else:
        g2.wait_screen("main_menu", 120)
        time.sleep(1.0)
        g2.act("menu/2")
        g2.wait_screen("choose_map")
        time.sleep(0.8)
        g2.act("files", "select", args.save)
        time.sleep(0.8)
        g2.act("ok")
        g2.wait_screen("game_session", 120)
        time.sleep(12)  # the loading fade has finished
        size = g2.call("game_world", include=["map"])["map"]
        map_w, map_h = size["width"], size["height"]
        calibrate()
        bars_off()
        for slot in args.slots.split(","):
            print(slot, flush=True)
            SHOTS[slot]()
finally:
    if not args.keep:
        target.close()
