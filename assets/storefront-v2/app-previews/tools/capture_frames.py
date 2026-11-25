#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Film App Store app-preview takes from the iOS app in the Simulator, one game tick per frame.

    GLOB2_SCRATCH=... uv run --with pillow --with numpy python capture_frames.py DEVICE TAKE[,TAKE...] [--tag T]

DEVICE is iphone-6.9 or ipad-13; TAKEs are names from takes.json. This replaces the
first version's real-time `simctl io recordVideo` capture, which stuttered when the
Mac was busy. Every frame here is one `xcrun simctl io screenshot` of the running
app, taken while the match is held between ticks:

  1. load the take's save through the game's own Load game screen, switch the
     Health and food bars lens off, press Continue playing where the match has been
     won, point the camera (game_view) and erase the co-controlling AI's zones;
  2. hold the match (game_time pause), run a short lead-in tick by tick so the
     erase orders apply, then start the capture clock (game_time capture_clock,
     a capture-build-only switch: see capture-frame-clock.patch). From then on the
     app draws exactly two frames for every tick that runs (a 60 Hz display at the
     normal 30 ticks a second) and nothing in between, and the presentation
     clocks (water, clouds, the event list's lifetimes, the tick-rate readout,
     fog fades) advance by exactly 1/60 s per drawn frame;
  3. for every frame: perform that frame's scripted player inputs (real touch
     controls through the app's MCP listener), step exactly one tick
     (game_time step ticks=1), wait until the app has drawn that tick's two frames,
     and save the simulator screen at native pixels with simctl io screenshot.
     The second of each tick's two drawn frames is the one on screen, so the
     movie is a 30 fps sampling of what a 60 Hz device shows, at real game speed.

`skip` entries let game time pass unfilmed (a declared cut inside a take): the
ticks are stepped as usual and the frames drawn, but no screenshot is kept; the
zones keep being erased. `until_inn` skips until the placed Inn's site lacks at most that many units of
building material (game_world's own site stock). A `roll` input then films on,
keeping only the newest `keep` frames (older ones are discarded, never edited
together), until game_world reports the Inn finished, and stops `after` frames
later: the site completes the moment its last material arrives, which cannot be
predicted, so this is how the finishing moment is caught without a second cut.

Writes RAW/<device>/<take><tag>/f00000.png ... and take.json (the tick, event rows
and inputs of every frame, the camera, the lead-in, the capture clock's own
counters).
"""
import argparse
import hashlib
import json
import os
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
ap.add_argument("--frames", type=int, default=0, help="film at most this many frames per take (scouting)")
ap.add_argument("--verify-every", type=int, default=50,
                help="every N frames, take a second screenshot 0.4 s later and require it to be identical")
args = ap.parse_args()

g2, mcp, SIM = pv.setup(args.device)
DEV = pv.DEVICES[args.device]
plan = json.loads(Path(args.plan).read_text())
RAW = g2.SCRATCH / "raw-frames" / args.device
RAW.mkdir(parents=True, exist_ok=True)
WIDTH, HEIGHT = DEV["native"]
lock = threading.Lock()
STATUS_TIME = (__import__("datetime").datetime(2007, 1, 9, 9, 41).astimezone(__import__("datetime").timezone.utc)
               .strftime("%Y-%m-%dT%H:%M:%S.000Z"))
FRAMES_PER_TICK = 2


def call(fn, *a, **k):
    """One MCP request; a busy app ("UI operation deadline exceeded") is asked again."""
    for attempt in range(8):
        try:
            with lock:
                return fn(*a, **k)
        except (RuntimeError, OSError) as error:
            if ("deadline" not in str(error) and "timed out" not in str(error)) or attempt == 7:
                raise
            time.sleep(1.0)


def controls():
    return call(g2.controls)


def keys():
    return {c.get("key"): c for _, c in controls()}


def event_rows(ctls=None):
    return [c.get("label") for _, c in (ctls or controls()) if str(c.get("key")).startswith("game/events/")]


def continue_playing():
    for _, control in controls():
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


def erase_boxes(around=None):
    if around is None:
        return [(x, y, min(64, map_w - x), min(64, map_h - y)) for x in range(0, map_w, 64) for y in range(0, map_h, 64)]
    boxes = []
    x0, y0 = (around[0] - 24) % map_w, (around[1] - 32) % map_h
    for x, w in ((x0, min(48, map_w - x0)), (0, 48 - min(48, map_w - x0))):
        for y, h in ((y0, min(64, map_h - y0)), (0, 64 - min(64, map_h - y0))):
            if w > 0 and h > 0:
                boxes.append((x, y, w, h))
    return boxes


def erase_zones(around=None):
    """Erase the forbidden, clearing and guard zones (the Flags-and-areas tool's
    erase, an ordinary player action) over the whole map or a window around the
    camera. The orders apply as the next ticks run."""
    for zone in ("forbidden", "clearing", "guard"):
        for x, y, w, h in erase_boxes(around):
            try:
                call(g2.tcall, "game_zone", zone=zone, mode="erase", x=x, y=y, width=w, height=h)
            except RuntimeError as error:
                if "queue full" not in str(error):
                    raise


def calibrate():
    reply = call(g2.view, zoom=1.0)
    logical_width = 2 * reply["tile_screen"]["x"]
    return logical_width / (WIDTH / DEV["points"])  # logical units per point


def zoom_for(points):
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


# ------------------------------------------------------------------ the clock

def gtime(action="pause", **extra):
    return call(g2.tcall, "game_time", action=action, **extra)


def wait_drawn(min_frames=0, timeout=60.0):
    """Wait until the steps have run and the app has drawn every frame they earned
    (two per tick), so the screen holds the newest tick's frame."""
    end = time.time() + timeout
    while time.time() < end:
        st = call(g2.call, "game_time", action="status")
        cc = st.get("capture_clock") or {}
        if (st["steps_remaining"] == 0 and cc.get("pending_frames", 1) == 0
                and cc.get("last_drawn_tick") == st["tick"] and cc.get("drawn_frames", 0) >= min_frames):
            return st
        time.sleep(0.01)
    raise RuntimeError(f"the app did not draw the held tick: {st}")


def step_ticks(n, expected_drawn=0):
    """Run n ticks (game_time step), then wait for their frames. Returns the status."""
    before = call(g2.call, "game_time", action="status")["tick"]
    gtime("step", ticks=n)
    st = wait_drawn(expected_drawn)
    if st["tick"] != before + n:
        raise RuntimeError(f"stepped from {before} to {st['tick']}, not {n} ticks")
    return st


def screenshot(path):
    g2.simctl("io", SIM, "screenshot", "--type=png", str(path))


def island_present(path):
    """The simulator sometimes paints the Dynamic Island cut-out into its framebuffer
    (a device screenshot never contains it): a black pill between the clock and the
    status icons, where the status bar is navy (0, 0, 32)."""
    if args.device != "iphone-6.9":
        return False
    import numpy as np
    from PIL import Image
    a = np.asarray(Image.open(path).convert("RGB"))[50:140, 520:800].astype(int)
    return float(a[..., 2].mean()) < 20


def same_png(a, b):
    import numpy as np
    from PIL import Image
    return np.array_equal(np.asarray(Image.open(a).convert("RGB")), np.asarray(Image.open(b).convert("RGB")))


def shoot(path, verify=False):
    """Save the held frame; retake while the simulator shows its island. With verify,
    a second screenshot 0.4 s later must be identical (the frame is really held)."""
    for attempt in range(20):
        screenshot(path)
        if not island_present(path):
            break
        time.sleep(0.3)
    else:
        raise RuntimeError("the Dynamic Island stayed in the screenshot")
    if verify:
        time.sleep(0.4)
        check = path.with_name(path.stem + "-verify.png")
        screenshot(check)
        ok = same_png(path, check) or island_present(check)
        check.unlink()
        if not ok:
            raise RuntimeError(f"{path.name}: the screen changed while the frame was held")
        return True
    return attempt


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


# ------------------------------------------------------------------ actions

def do(action, reply, log, frame, tick):
    kind = action["do"]
    if kind == "act":
        call(g2.act, action["key"])
    elif kind == "tap_tile":
        tile = action["tile"]
        if tile == "site":
            tile = [site["x"] + site["w"] // 2, site["y"] + site["h"] // 2]
        px, py = tile_point(reply, *tile)
        call(g2.click, px, py, space="logical")
    elif kind == "close":
        close_panels()
    elif kind == "check_site":
        state = inn_state()
        if not state:
            raise RuntimeError("the building was not placed")
        action = dict(action, found=state)
    elif kind == "view":
        reply.update(call(g2.view, x=action["camera"][0], y=action["camera"][1],
                          zoom=zoom_for(action.get("tile_points", take_points))))
    else:
        raise ValueError(kind)
    log.append({"frame": frame, "tick": tick, "action": {k: v for k, v in action.items() if k != "frame"}})


def inn_state():
    """The Inn (site or building) whose footprint covers the placed site, if any."""
    for b in call(g2.call, "game_world", include=["colony"])["colony"]["buildings"]:
        if b.get("type") == "inn" and abs(b["x"] - site["x"]) <= 1 and abs(b["y"] - site["y"]) <= 1:
            return {k: b.get(k) for k in ("type", "x", "y", "hp", "max_hp", "level", "site", "stock", "workers")}
    return None


def find_site(take, reply):
    """Before filming, with the match held: arm the take's building in the build
    palette and tap each candidate tile until the placement's Ok is enabled (the
    game's own check that the ground is free), then cancel. Nothing is placed or
    destroyed; the filmed placement then taps the tile found."""
    tried = []
    close_panels()
    call(g2.act, "touch/navigation/buildings")
    time.sleep(0.8)
    call(g2.act, take.get("palette_key", "touch/palette/inn.0.site"))
    time.sleep(0.8)
    found = None
    for tile in take["site_candidates"]:
        px, py = tile_point(reply, tile[0] + 1, tile[1] + 1)
        call(g2.click, px, py, space="logical")
        time.sleep(1.0)
        confirm = keys().get("touch/placement/confirm") or {}
        ok = (bool(confirm) and confirm.get("enabled", True) is not False
              and "activate" in confirm.get("actions", ["activate"]))
        tried.append({"tile": tile, "ok_enabled": ok})
        if ok:
            found = tile
            break
    close_panels()
    time.sleep(0.5)
    close_panels()
    if not found:
        raise RuntimeError(f"no free site among {tried}")
    print(f"   site {found} (tried {tried})", flush=True)
    return {"tile": found, "tried": tried,
            "note": "found before filming by arming the building and tapping candidate tiles until Ok was enabled, "
                    "then cancelling; nothing was placed"}


def skip(a, log, f, cx, cy):
    """Let ticks run unfilmed (a declared cut), three at a time, erasing the zones as
    during filming; until_inn ends once the placed Inn's site lacks at most that many
    units of material."""
    log.append({"frame": f, "tick": call(g2.call, "game_time", action="status")["tick"],
                "action": {k: v for k, v in a.items() if k != "frame"}})
    ran, inn = 0, None
    while True:
        st = step_ticks(3)
        ran += 3
        if ran % 45 == 0:
            erase_zones((cx, cy))
        if a.get("until_inn"):
            if ran % 6 == 0:
                inn = inn_state()
                if inn and not inn.get("site"):
                    raise RuntimeError(f"the Inn was finished before filming resumed: {inn}")
                left = sum(int(v.split("/")[1]) - int(v.split("/")[0]) for v in (inn or {}).get("stock", {}).values())
                if inn and left <= a["until_inn"]:
                    break
            if ran > 9000:
                raise RuntimeError(f"the Inn was not built: {inn}")
        elif ran >= a.get("ticks", 0):
            break
    log.append({"frame": f, "tick": st["tick"], "skip_ended": True, "ticks_skipped": ran, "inn": inn})
    return st


def film(take_name, take, tag):
    global site, take_points
    take = dict(take, **take.get("overrides", {}).get(args.device, {}))
    out = RAW / f"{take_name}{tag}"
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("f*.png"):
        old.unlink()
    take_points = take["tile_points"][args.device]
    zoom = zoom_for(take_points)
    cx, cy = take["camera"][args.device]
    site = None
    gtime("pause")
    close_panels()
    reply = call(g2.view, x=cx, y=cy, zoom=zoom)
    site_probe = None
    if take.get("site_candidates"):
        site_probe = find_site(take, reply)
        site = {"x": site_probe["tile"][0], "y": site_probe["tile"][1], "w": 3, "h": 3}
        off = take.get("camera_offset", [1, 1])
        cx, cy = site["x"] + off[0], site["y"] + off[1]
        reply = call(g2.view, x=cx, y=cy, zoom=zoom)
    erase_zones()
    # Lead-in, unfilmed, with the capture clock already running: the erase orders
    # apply, the tick-rate readout fills its 3 s window with frame-clock time, and
    # the view settles.
    st = gtime("pause", capture_clock=True, frames_per_tick=FRAMES_PER_TICK)
    st = wait_drawn(FRAMES_PER_TICK)
    lead = take.get("lead_ticks", 120)
    for k in range(0, lead, 3):
        st = step_ticks(3)
        if k % 30 == 27:
            erase_zones((cx, cy))
    close_panels()
    st = step_ticks(1)
    drawn = st["capture_clock"]["drawn_frames"]
    actions = sorted(take.get("actions_" + args.device, take.get("actions", [])), key=lambda a: a["frame"])
    erase_every = take.get("erase_every_frames", 45)
    frames = take["frames"] if not args.frames else min(args.frames, take["frames"])
    log, frame_log = [], []
    t0 = time.time()
    n = 0          # filmed frames
    f = 0          # timeline frames (filmed or skipped)
    verified = 0
    rolling = None
    while n < frames:
        for a in [a for a in actions if a["frame"] == f]:
            if a["do"] == "roll":
                # Film on, keeping only the newest `keep` frames, until the placed Inn is
                # finished; then film `after` more frames and stop.
                rolling = dict(a, started=n)
                frames = n + a.get("max_frames", 1800)
                log.append({"frame": f, "tick": st["tick"], "action": {k: v for k, v in a.items() if k != "frame"}})
                continue
            if a["do"] == "skip":
                st = skip(a, log, f, cx, cy)
                drawn = st["capture_clock"]["drawn_frames"]
            else:
                do(a, reply, log, f, st["tick"])
        if f > 0 and (f % erase_every == 0):
            erase_zones((cx, cy))
        if f > 0:
            drawn += FRAMES_PER_TICK
            st = step_ticks(1, drawn)
        path = out / f"f{n:05d}.png"
        verify = args.verify_every and n % args.verify_every == 0
        retakes = shoot(path, verify=verify)
        verified += 1 if verify else 0
        rows = None
        if n % take.get("rows_every", 3) == 0:
            try:
                rows = event_rows()
            except RuntimeError:
                rows = None
        frame_log.append({"n": n, "f": f, "tick": st["tick"], "drawn_frame": st["capture_clock"]["drawn_frames"],
                          "virtual_ms": st["capture_clock"]["virtual_ms"],
                          **({"event_rows": len(rows), "labels": rows} if rows is not None else {}),
                          **({"island_retakes": retakes} if isinstance(retakes, int) and retakes else {})})
        if rolling and not rolling.get("done_at") and n % 6 == 0:
            inn = inn_state()
            if inn and not inn.get("site"):
                rolling["done_at"] = n
                frames = n + rolling.get("after", 120)
                log.append({"frame": f, "tick": st["tick"], "roll_ended": True, "filmed_frame": n, "inn": inn})
        if rolling and not rolling.get("done_at") and n - rolling["keep"] >= rolling["started"]:
            old = out / f"f{n - rolling['keep']:05d}.png"
            if old.exists():
                old.unlink()
                frame_log[n - rolling["keep"]]["discarded"] = True
        n += 1
        f += 1
        if n % 30 == 0:
            print(f"  {take_name}{tag}: {n}/{frames} frames, tick {st['tick']}, "
                  f"{(time.time() - t0) / n:.2f} s/frame", flush=True)
    end_status = gtime("pause", capture_clock=False)
    side = {"take": take_name + tag, "device": args.device, "model": DEV["model"], "save": take["save"],
            "loaded_tick": loaded_tick, "lead_in_ticks": lead, "first_tick": frame_log[0]["tick"],
            "last_tick": frame_log[-1]["tick"], "frames": n,
            "camera": {"tile": [cx, cy], "zoom": reply["zoom"], "tile_points": take_points},
            "method": "frame-stepped: game_time step ticks=1 per frame with the capture clock on (two drawn frames "
                      "per tick, presentation clocks at 1/60 s per drawn frame), xcrun simctl io screenshot of each "
                      "held frame at native pixels",
            "verified_held_frames": verified,
            "hd_artwork": g2.HD_ARTWORK,
            "player_actions": ["Tools strip: Health and food bars lens switched off",
                               "zone tool: erased the co-controlling AI's forbidden, guard and clearing zones before "
                               f"the take and every {erase_every} frames ({erase_every / 30:.1f} s of game time) during it"]
            + [a["action"]["note"] for a in log
               if "action" in a and a["action"].get("note") and a["action"]["do"] not in ("check_site", "skip", "roll")],
            "inputs": log, "frame_log": frame_log, "capture_clock_end": end_status.get("capture_clock"),
            "note": take.get("note", "")}
    if site:
        side["site"] = dict(site, probe=site_probe)
        side["inn_after"] = inn_state()
    if continue_used:
        side["player_actions"].insert(0, "end-of-match dialog (You have won): Continue playing")
    (out / "take.json").write_text(json.dumps(side, indent=1))
    ticks = [r["tick"] for r in frame_log]
    jumps = sorted({b - a for a, b in zip(ticks, ticks[1:])})
    print(f"{take_name}{tag}: {n} frames, ticks {ticks[0]}-{ticks[-1]}, tick steps {jumps}, "
          f"{(time.time() - t0) / max(1, n):.2f} s/frame", flush=True)


target = g2.IOS(SIM)
target.boot()
g2.simctl("status_bar", SIM, "override", "--time", STATUS_TIME)
target.install()
current = None
continue_used = False
loaded_tick = None
site = None
take_points = None
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
        if take.get("after_victory") and not continue_used:
            end = time.time() + take.get("victory_wait", 240)
            while time.time() < end and not continue_used:
                continue_used = continue_playing()
                time.sleep(1.0)
            time.sleep(1.0)
            bars_off()
        if take.get("run_seconds"):  # let the match run live a little before the take
            gtime("resume")
            time.sleep(take["run_seconds"])
        film(name, take, args.tag)
finally:
    try:
        call(g2.tcall, "game_time", action="resume", capture_clock=False)
    except Exception:
        pass
    if not args.keep:
        target.close()
