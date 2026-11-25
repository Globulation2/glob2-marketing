#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Record App Store app-preview takes from the iOS app in the Simulator, in real time.

    GLOB2_SCRATCH=... uv run --with pillow --with numpy python record.py DEVICE TAKE[,TAKE...] [--tag T]

DEVICE is iphone-6.9 or ipad-13; TAKEs are names from takes.json. Each take loads
its save through the game's own Load game screen (unless the previous take used the
same save and the take does not ask for "fresh"), points the camera with the
touch interface's camera (game_view), and records the simulator display with
`simctl io recordVideo` (H.264, the display's native pixels, variable frame rate)
while the match runs at normal speed (1x). Nothing is paused or stepped.

During a take the script performs the take's scripted player inputs (opening the
build palette, arming a building, tapping the map, confirming) at the listed
seconds after recording started, erases the co-controlling AI's forbidden, guard
and clearing zones every few seconds (an ordinary Flags-and-areas action, the
clean-state protocol of the mobile captures), and logs the event-list rows and
the match tick twice a second. Every take writes RAW/<device>/<take><tag>.mov and
a JSON sidecar with the log.
"""
import argparse
import json
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import pv  # noqa: E402

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("device", choices=sorted(pv.DEVICES))
ap.add_argument("takes")
ap.add_argument("--plan", default=str(HERE / "takes.json"))
ap.add_argument("--tag", default="")
ap.add_argument("--keep", action="store_true", help="leave the app running afterwards")
args = ap.parse_args()

g2, mcp, SIM = pv.setup(args.device)
DEV = pv.DEVICES[args.device]
plan = json.loads(Path(args.plan).read_text())
RAW = g2.SCRATCH / "raw" / args.device
RAW.mkdir(parents=True, exist_ok=True)
WIDTH, HEIGHT = DEV["native"]
lock = threading.Lock()
# simctl wants ISO 8601 with fractional seconds and shows it in the Mac's time zone.
STATUS_TIME = (__import__("datetime").datetime(2007, 1, 9, 9, 41).astimezone(__import__("datetime").timezone.utc)
               .strftime("%Y-%m-%dT%H:%M:%S.000Z"))


def call(fn, *a, **k):
    """One MCP request; a busy app ("UI operation deadline exceeded") is asked again."""
    for attempt in range(6):
        try:
            with lock:
                return fn(*a, **k)
        except RuntimeError as error:
            if "deadline" not in str(error) or attempt == 5:
                raise
            time.sleep(1.0)


def keys():
    return {c.get("key"): c for _, c in call(g2.controls)}


def event_rows():
    return [c.get("label") for _, c in call(g2.controls) if str(c.get("key")).startswith("game/events/")]


def continue_playing():
    for _, control in call(g2.controls):
        if control.get("label") == "Continue playing" and control.get("key"):
            call(g2.act, control["key"])
            time.sleep(1.0)
            return True
    return False


def close_panels():
    continue_playing()
    for _ in range(4):
        present = keys()
        if "touch/placement/cancel" in present:
            call(g2.act, "touch/placement/cancel")
        elif "touch/inspector/close" in present:
            call(g2.act, "touch/inspector/close")
        elif any(present.get(f"touch/navigation/{k}", {}).get("selected") for k in ("buildings", "flags", "tools")):
            for k in ("buildings", "flags", "tools"):
                if present.get(f"touch/navigation/{k}", {}).get("selected"):
                    call(g2.act, f"touch/navigation/{k}")
        else:
            return
        time.sleep(0.5)


def bars_off():
    """The Tools strip's "Health and food bars" lens, switched off as a player would."""
    close_panels()
    call(g2.act, "touch/navigation/tools")
    time.sleep(0.6)
    lens = keys().get("touch/lens/6")
    if lens is not None and lens.get("selected"):
        call(g2.act, "touch/lens/6")
        time.sleep(0.4)
    close_panels()


def erase_zones(around=None):
    """Erase the zones over the whole map, or over a 48x64-tile window around the
    camera centre (three calls, quick enough to repeat during a take)."""
    if around is None:
        boxes = [(x, y, min(64, map_w - x), min(64, map_h - y)) for x in range(0, map_w, 64) for y in range(0, map_h, 64)]
    else:
        boxes = []
        x0, y0 = (around[0] - 24) % map_w, (around[1] - 32) % map_h
        for x, w in ((x0, min(48, map_w - x0)), (0, 48 - min(48, map_w - x0))):
            for y, h in ((y0, min(64, map_h - y0)), (0, 64 - min(64, map_h - y0))):
                if w > 0 and h > 0:
                    boxes.append((x, y, w, h))
    for zone in ("forbidden", "clearing", "guard"):
        for x, y, w, h in boxes:
            call(g2.tcall, "game_zone", zone=zone, mode="erase", x=x, y=y, width=w, height=h)


def calibrate():
    reply = call(g2.view, zoom=1.0)
    # The camera centre sits at the middle of the screen; the view's tile count rounds up
    # partial tiles, so it would overstate the width (1056 for 1032 on iPad).
    logical_width = 2 * reply["tile_screen"]["x"]
    return logical_width / (WIDTH / DEV["points"])  # logical units per point


def zoom_for(points):
    """game_view zoom at which one map tile is `points` points on screen."""
    return round(points * units_per_point / 32, 3)


def load(save):
    target.launch(saves=sorted(g2.SAVES.glob("*.game.gz")))
    call(g2.wait_screen, "main_menu", 120)
    time.sleep(1.0)
    call(g2.act, "menu/2")
    call(g2.wait_screen, "choose_map")
    time.sleep(0.8)
    call(g2.act, "files", "select", save)
    time.sleep(0.8)
    call(g2.act, "ok")
    call(g2.wait_screen, "game_session", 120)
    loaded = g2.tick()
    time.sleep(12)  # the loading fade has finished
    return loaded


def tile_point(reply, x, y):
    def delta(a, b, size):
        d = (a - b) % size
        return d - size if d > size / 2 else d
    return (reply["tile_screen"]["x"] + delta(x, reply["centre"]["x"], map_w) * reply["tile_pixels"],
            reply["tile_screen"]["y"] + delta(y, reply["centre"]["y"], map_h) * reply["tile_pixels"])


def do(action, reply, log):
    kind = action["do"]
    if kind == "act":
        call(g2.act, action["key"])
    elif kind == "tap_tile":
        tile = action["tile"]
        if tile == "site":  # the centre of the footprint found by probe_site
            tile = [site["x"] + site["w"] // 2, site["y"] + site["h"] // 2]
        px, py = tile_point(reply, *tile)
        call(g2.click, px, py, space="logical")
    elif kind == "drag_tiles":
        # A one-finger pan of the camera, as a player drags the map.
        (x0, y0), (x1, y1) = action["from"], action["to"]
        a, b = tile_point(reply, x0, y0), tile_point(reply, x1, y1)
        steps = max(2, int(action.get("steps", 20)))
        pts = [[a[0] + (b[0] - a[0]) * i / steps, a[1] + (b[1] - a[1]) * i / steps] for i in range(steps + 1)]
        call(g2.drag, pts, duration_ms=int(action.get("ms", 1500)), space="logical")
    elif kind == "close":
        close_panels()
    else:
        raise ValueError(kind)
    log.append({"t": round(time.time() - t0, 2), "action": action})


def probe_site(spec):
    """Find ground where the building can go right now, the way the game itself
    searches (game_place with near), then cancel that probe site at once (Destroy,
    as the building panel does) so the take can place the real one by touch. The
    match's continuation differs on every load, so a fixed tile is often taken."""
    near = spec["near"][args.device] if isinstance(spec["near"], dict) else spec["near"]
    placed = []
    for attempt in range(3):
        session = call(g2.call, "game_world", include=["status"])["session"]
        before = {p.get("id") for p in call(g2.call, "game_world", detail="brief",
                                              include=["placements"]).get("placements", [])}
        reply = call(g2.tcall, "game_place", building=spec["building"], x=near[0], y=near[1], near=True,
                     search_radius=spec.get("radius", 8) + 4 * attempt, session=session)
        print("   probe:", json.dumps(reply)[:300], flush=True)
        for _ in range(30):
            time.sleep(0.3)
            placed = [p for p in call(g2.call, "game_world", detail="brief", include=["placements"]).get("placements", [])
                      if p.get("building") == spec["building"] and p.get("id") is not None and p.get("id") not in before]
            if placed:
                break
        if placed:
            break
    if not placed:
        raise RuntimeError("probe site was not placed")
    p = placed[-1]
    call(g2.tcall, "game_building", id=p["id"], generation=p["generation"], action="destroy")
    # Wait until the probe site is gone from the ground (a destroyed site burns down for a
    # few seconds and still blocks the footprint), so the touch placement can use it.
    size = spec.get("size", 3)
    for _ in range(60):
        time.sleep(0.5)
        blocking = [b for b in call(g2.call, "game_world", include=["colony"])["colony"]["buildings"]
                    if b["x"] < p["x"] + size and p["x"] < b["x"] + b.get("width", 1)
                    and b["y"] < p["y"] + size and p["y"] < b["y"] + b.get("height", 1)]
        if not blocking:
            break
    time.sleep(1.0)
    return {"x": p["x"], "y": p["y"], "w": spec.get("size", 3), "h": spec.get("size", 3)}


def record(take_name, take, tag=None):
    global t0, site
    take = dict(take, **take.get("overrides", {}).get(args.device, {}))
    tag = args.tag if tag is None else tag
    out = RAW / f"{take_name}{tag}.mov"
    zoom = zoom_for(take["tile_points"][args.device])
    cx, cy = take["camera"][args.device] if isinstance(take["camera"], dict) else take["camera"]
    site = None
    if take.get("probe_site"):
        close_panels()
        spec = dict(take["probe_site"], **take["probe_site"].get("device", {}).get(args.device, {}))
        if spec.get("fixed"):
            # Ground known to be clear (game_place near returns this very tile): no probe site.
            size = spec.get("size", 3)
            site = {"x": spec["fixed"][0], "y": spec["fixed"][1], "w": size, "h": size}
        else:
            site = probe_site(spec)
        off = take["probe_site"].get("camera_offset", {}).get(args.device, [0, 0])
        cx, cy = site["x"] + site["w"] // 2 + off[0], site["y"] + site["h"] // 2 + off[1]
        print(f"   site {site}, camera {cx},{cy}", flush=True)
    close_panels()
    reply = call(g2.view, x=cx, y=cy, zoom=zoom)
    for setup_action in take.get("setup", []):
        do(setup_action, reply, [])
        time.sleep(0.6)
    erase_zones()
    time.sleep(1.0)
    env = dict(__import__("os").environ, DEVELOPER_DIR=g2.DEVELOPER_DIR)
    proc = subprocess.Popen(["xcrun", "simctl", "--set", str(g2.SIMSET), "io", SIM, "recordVideo", "--codec=h264",
                             "--mask=ignored", "--force", str(out)], env=env, stderr=subprocess.PIPE, text=True)
    for line in proc.stderr:
        if "Recording started" in line:
            break
    t0 = time.time()
    tick0 = g2.tick()
    actions, samples = [], []
    pending = sorted(take.get("actions_" + args.device, take.get("actions", [])), key=lambda a: a["t"])
    next_erase = take.get("erase_every", 3.0)
    next_sample = 0.0
    duration = take["seconds"]
    while True:
        now = time.time() - t0
        if now >= duration:
            break
        if pending and now >= pending[0]["t"]:
            do(pending.pop(0), reply, actions)
            continue
        quiet = take.get("no_erase_between")  # keep the zone tool out of the way while placing
        if quiet and quiet[0] <= now < quiet[1]:
            next_erase = max(next_erase, quiet[1])
        if take.get("erase_every") and now >= next_erase:
            erase_zones((cx, cy))
            next_erase += take["erase_every"]
            continue
        if now >= next_sample:
            try:
                rows = event_rows()
                samples.append({"t": round(now, 2), "tick": g2.tick(), "event_rows": len(rows), "labels": rows})
            except Exception as error:  # a busy frame: skip this sample
                samples.append({"t": round(now, 2), "error": str(error)[:120]})
            next_sample += take.get("sample_every", 0.5)
            continue
        time.sleep(0.05)
    print(f"   take loop ended at {time.time() - t0:.1f} s", flush=True)
    proc.send_signal(signal.SIGINT)
    proc.wait(60)
    side = {"take": take_name + tag, "device": args.device, "model": DEV["model"], "save": take["save"],
            "loaded_tick": loaded_tick, "first_tick": tick0, "camera": {"tile": [cx, cy], "zoom": reply["zoom"],
                                                                         "tile_points": take["tile_points"][args.device]},
            "recorder": "xcrun simctl io recordVideo --codec=h264 --mask=ignored",
            "speed": "1x (normal), live; never paused or stepped", "hd_artwork": g2.HD_ARTWORK,
            "player_actions": ["Tools strip: Health and food bars lens switched off",
                               "zone tool: erased the co-controlling AI's forbidden, guard and clearing zones "
                               f"before the take{' and every %.1f s during it' % take['erase_every'] if take.get('erase_every') else ''}"]
            + [a["action"].get("note", a["action"]["do"]) for a in actions],
            "actions": actions, "samples": samples, "note": take.get("note", "")}
    if site:
        side["probe_site"] = dict(site, note=("fixed tile, clear ground (no probe site)" if spec.get("fixed") else
                                              "found with game_place near and destroyed at once, before the take; "
                                              "the take then places the building there by touch"))
        if not spec.get("fixed"):
            side["player_actions"].insert(1, "before the take (off the recording): a probe site placed and destroyed "
                                             "to find clear ground")
        side["buildings_at_site_after"] = [
            {k: b.get(k) for k in ("type", "x", "y", "hp", "max_hp", "level")}
            for b in call(g2.call, "game_world", include=["colony"])["colony"]["buildings"]
            if b.get("type") == take["probe_site"]["building"]
            and abs(b["x"] - site["x"]) <= 1 and abs(b["y"] - site["y"]) <= 1]
    if continue_used:
        side["player_actions"].insert(0, "end-of-match dialog (You have won): Continue playing")
    out.with_suffix(".json").write_text(json.dumps(side, indent=1))
    rows = [s.get("event_rows", -1) for s in samples]
    print(f"{take_name}{tag}: {out.stat().st_size / 1e6:.0f} MB, ticks {tick0}-{samples[-1].get('tick') if samples else '?'}, "
          f"event rows {rows}", flush=True)
    return not site or bool(side["buildings_at_site_after"])


target = g2.IOS(SIM)
target.boot()
# Apple's preview guidance asks for no dates; the iPad status bar shows one next to the
# time, so it is pinned to Apple's own marketing date and time (Tue Jan 9, 9:41).
g2.simctl("status_bar", SIM, "override", "--time", STATUS_TIME)
target.install()
current = None
continue_used = False
t0 = 0.0
try:
    for name in args.takes.split(","):
        take = plan["takes"][name]
        if take.get("fresh") or take["save"] != current:
            loaded_tick = load(take["save"])
            current = take["save"]
            size = call(g2.call, "game_world", include=["map"])["map"]
            map_w, map_h = size["width"], size["height"]
            units_per_point = calibrate()
            bars_off()
            continue_used = False
        if take.get("after_victory"):
            end = time.time() + take.get("victory_wait", 240)
            while time.time() < end and not continue_used:
                continue_used = continue_playing()
                time.sleep(1.0)
            time.sleep(1.0)
            bars_off()
        if take.get("min_tick"):
            while g2.tick() < take["min_tick"]:
                time.sleep(0.5)
        for attempt in range(take.get("attempts", 1)):
            tag = args.tag + (f"-a{attempt + 1}" if take.get("attempts", 1) > 1 else "")
            ok = record(name, take, tag)
            if ok:
                break
            print(f"   {name}{tag}: the building was not placed; trying again", flush=True)
finally:
    if not args.keep:
        target.close()
