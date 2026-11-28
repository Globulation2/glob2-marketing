#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Film trailer shots frame by frame through the game's embedded MCP UI server.

usage: capture_shot.py SHOTS.json OUT_DIR --matches DIR --profile DIR
                       [--only ID[,ID]] [--port N] [--preview EVERY] [--frames N]

The off-screen game must already run (launch-record-game.sh). The game's own
recorder cannot read the off-screen renderer's framebuffer, and a real window
cannot reach 3840x2160 on this machine, so every frame is one ui_screenshot:

  1. join a local player to the shot's colony in the headless all-AI save
     MATCHES/<match>/checkpoint-<checkpoint>.game.gz (join-seat.py from the
     desktop capture tools) and load it through the game's Load game dialog;
  2. run the match to `start_tick` (fast-forward, then normal speed), frame the
     camera with game_view;
  3. hold the match with game_time pause, then for every frame: game_time
     step ticks=1 (one simulation tick), perform the shot's scripted inputs for
     that frame, and save the next rendered frame at native pixels.

One frame per tick played back at 30 frames a second is the game's normal
speed (30 ticks a second): nothing is sped up or slowed down. While the match is
held between ticks the game prints "Paused" at the bottom of the map; the
window is therefore 4256x2800 and the edit keeps the HUD-free map rectangle
3840x2160 at (0, 200), clear of the top bar, the event list, the sidebar and that
label (see ../README.md). Health and food bars are switched off after each load
(the in-game toggle, key I).

Shot fields:
  id, match, checkpoint, team, start_tick, frames, view {x, y, zoom}
  erase_zones   bool: the seat erases the colony's forbidden, clearing and guard
                area markings in and around the view (a player action), in the
                lead-in and repeated while filming
  zones         optional list of the zone kinds to erase
  erase_per_frame, erase_every   optional: erase N chunks every K frames (the
                co-play shot erases rarely so its standing order's orders fit
                in the human order queue)
  pan           {dx, dy}: native pixels the camera moves per frame, done with a
                short middle-button drag (the game's own map pan)
  actions       list of {frame, ...}:
                  {"act": KEY}                 press an inspected control (palette, tab)
                  {"move_tile": [x, y], "over": N}   glide the pointer to a tile over N frames
                  {"click_tile": [x, y]}       left click a tile
                  {"key": NAME}                press a key
                  {"skip_ticks": N}            let N ticks pass unfilmed (a cut inside the take)
                  {"tool": NAME, "args": {...}}    any MCP tool call (token added)
                  {"hive_install": {name, source, plan, interval, description}}
                      install a Hive standing order (source file in this
                      directory, __PLAN__ replaced by the plan) through the MCP
                      server; request and response go to mcp-transcript.json
                  {"hive_list": true}          list the standing orders (transcript)
  --preview EVERY  scouting: step EVERY ticks per frame and save 1920-wide frames
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CTOOLS = os.environ.get("GLOB2_CAPTURE_TOOLS") or os.path.normpath(
    os.path.join(HERE, "..", "..", "captures", "desktop", "tools"))
sys.path.insert(0, CTOOLS)
import mcp  # noqa: E402
import session  # noqa: E402

RENAMES = ["maxima=Maxima", "cortex=Cortex", "cabino=Cabino", "castor=Castor", "nicowar=Nicowar"]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def joined_save(matches, out, shot):
    name = f"{shot['match']}-{shot['checkpoint']}-t{shot['team']}"
    src = os.path.join(matches, shot["match"], f"checkpoint-{shot['checkpoint']}.game.gz")
    dst = os.path.join(out, "saves", name + ".game.gz")
    if not os.path.exists(dst):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        cmd = [sys.executable, os.path.join(CTOOLS, "join-seat.py"), src, dst, str(shot["team"])]
        for r in RENAMES:
            cmd += ["--rename", r]
        subprocess.run(cmd, check=True, stderr=subprocess.DEVNULL)
    return src, dst


_tok = {"value": None, "at": 0.0}


def token():
    """The control token, renewed at most once a minute (the lease lasts 300 s)."""
    if _tok["value"] is None or time.time() - _tok["at"] > 60:
        _tok["value"] = _raw_token()
        _tok["at"] = time.time()
    return _tok["value"]


_raw_token = mcp.token
mcp.token = lambda port=None: token()   # session.py helpers use the cached token too


def call(tool, args=None, tok=True, timeout=120):
    args = dict(args or {})
    if tok:
        args["token"] = token()
    data, images, err = mcp.call(tool, args, timeout=timeout)
    if err:
        raise RuntimeError(f"{tool}: {str(data)[:300]}")
    return data, images


def shot_png(path, max_width=8192, tries=30):
    for attempt in range(tries):
        data, images, err = mcp.call("ui_screenshot", {"max_width": max_width, "max_height": max_width}, timeout=120)
        if not err and images:
            with open(path, "wb") as fh:
                fh.write(images[0])
            return data
        time.sleep(2.0)   # a busy machine can miss the encoder deadline; the match is held, so retry
    raise RuntimeError(f"screenshot failed: {str(data)[:300]}")


def run_until(tick):
    """Fast-forward towards an absolute tick and hold the match a little before it.

    8x while far away, 2x closer in; the match is then held (game_time pause) at
    least 300 ticks early, because a speed change takes a moment to arrive on a
    busy machine. step_to() covers the rest at normal speed, exactly.
    """
    now = session.gtime()["tick"]
    if tick - now > 1500:
        session.gtime("resume")
    if tick - now > 3000:
        session.speed(7)
        while session.gtime()["tick"] < tick - 2400:
            time.sleep(0.05)
        session.speed(0)
    if tick - session.gtime()["tick"] > 1500:
        session.speed(3)
        while session.gtime()["tick"] < tick - 1100:
            time.sleep(0.05)
        session.speed(0)
    session.gtime("pause")


def step_to(tick):
    """Exact positioning: hold the match, then step tick by tick to `tick`."""
    st = session.gtime("pause")
    while st["tick"] < tick:
        session.gtime("step", ticks=min(3000, tick - st["tick"]))
        while True:
            st = session.gtime()
            if st["steps_remaining"] == 0:
                break
            time.sleep(0.02)
    return st["tick"]


def step_one(n=1):
    session.gtime("step", ticks=n)
    while True:
        st = session.gtime()
        if st["steps_remaining"] == 0:
            return st["tick"]
        time.sleep(0.005)


def map_centre():
    for _, ctl in mcp.walk(mcp.inspect()):
        if ctl.get("key") == "game/map":
            b = ctl["bounds"]
            return b["x"] + b["w"] / 2, b["y"] + b["h"] / 2
    raise RuntimeError("no map canvas")


class Camera:
    """Native-pixel position of map tiles for the current camera."""

    def __init__(self, view, centre, map_size, scale):
        self.px = view["tile_pixels"]
        self.centre = list(centre)
        self.map_size = map_size
        self.scale = scale
        self.mx, self.my = map_centre()
        self.pan = [0.0, 0.0]  # native pixels the camera has moved since game_view

    def tile(self, t):
        def delta(a, b, size):
            d = (a - b) % size
            return d - size if d > size / 2 else d
        lx = self.mx + delta(t[0], self.centre[0], self.map_size[0]) * self.px
        ly = self.my + delta(t[1], self.centre[1], self.map_size[1]) * self.px
        return lx * self.scale - self.pan[0], ly * self.scale - self.pan[1]


def erase_chunks(view_tiles, map_size, margin=3, chunk=32, zones=("forbidden", "clearing")):
    x0, y0 = view_tiles["x"] - margin, view_tiles["y"] - margin
    w = min(view_tiles["width"] + 2 * margin, map_size[0])
    h = min(view_tiles["height"] + 2 * margin, map_size[1])

    def spans(start, length, size):
        out, done = [], 0
        while done < length:
            pos = (start + done) % size
            n = min(chunk, length - done, size - pos)
            out.append((pos, n))
            done += n
        return out
    return [(zone, x, y, cw, ch) for x, cw in spans(x0, w, map_size[0]) for y, ch in spans(y0, h, map_size[1])
            for zone in zones]


def erase(chunks, pause=0.0):
    """Erase zone chunks; a full order queue skips the rest (the next frame retries)."""
    done = 0
    for zone, x, y, cw, ch in chunks:
        args = {"zone": zone, "mode": "erase", "x": x, "y": y, "width": cw, "height": ch, "token": token()}
        data, _, err = mcp.call("game_zone", args, timeout=120)
        if err:
            if "queue full" in str(data):
                erase.skipped += 1
                return done
            raise RuntimeError(f"game_zone: {str(data)[:300]}")
        done += 1
        if pause:
            time.sleep(pause)
    return done


erase.skipped = 0


def film(shot, args):
    out = os.path.join(args.out, shot["id"] + ("-preview" if args.preview else ""))
    os.makedirs(out, exist_ok=True)
    src, save = joined_save(args.matches, args.out, shot)
    session.load_save(save, args.profile, settle=0.5)
    session.gtime("pause")           # hold while the match-intro card fades
    if session.gtime()["speed"] != "1x":
        session.speed(0)
    time.sleep(4.5)
    if not film.clouds_set:
        session.set_clouds(False, False)
        film.clouds_set = True
    # Health and food bars off: the in-game "draw information" toggle (key I) starts on
    # with every loaded match; one press switches it off (desktop capture protocol).
    call("ui_key", {"key": "I"})
    world = session.world("summary")
    map_size = (world["map"]["width"], world["map"]["height"])
    v = shot["view"]
    view = session.view(v["x"], v["y"], v.get("zoom", 1.0))
    start = shot["start_tick"]
    lead = 150 if shot.get("erase_zones") else 0
    run_until(start - lead - 300)
    if session.gtime()["tick"] > start - lead:
        raise RuntimeError(f"overshot: tick {session.gtime()['tick']} is past {start - lead}")
    step_to(start - lead)
    view = session.view(v["x"], v["y"], v.get("zoom", 1.0))
    zones = shot.get("zones") or ("forbidden", "clearing", "guard")
    chunks = erase_chunks(view["view"], map_size, zones=zones) if shot.get("erase_zones") else []
    pan = shot.get("pan") or {}
    if chunks:
        if pan:  # cover the ground the pan will reach
            wide = dict(view["view"])
            reach = int(abs(pan.get("dx", 0)) * shot["frames"] / (view["tile_pixels"] * args.ui_scale)) + 2
            reachy = int(abs(pan.get("dy", 0)) * shot["frames"] / (view["tile_pixels"] * args.ui_scale)) + 2
            wide["x"] = (wide["x"] - reach) % map_size[0]
            wide["y"] = (wide["y"] - reachy) % map_size[1]
            wide["width"] += 2 * reach
            wide["height"] += 2 * reachy
            chunks = erase_chunks(wide, map_size, zones=zones)
        # Spread over the lead-in ticks: the game drops orders when too many queue up.
        for k in range(0, len(chunks), 3):
            erase(chunks[k:k + 3])
            step_one(2)
    tick = step_to(start)
    cam = Camera(view, (v["x"], v["y"]), map_size, args.ui_scale)
    actions = sorted(shot.get("actions", []), key=lambda a: a["frame"])
    glide = None       # (frame0, frames, from_xy, to_xy)
    pointer = None
    frames = args.frames or shot["frames"]
    every = args.preview or 1
    log = []
    transcript = []
    frame_ticks = []
    hive_session = None
    t0 = time.time()
    centre_px = (cam.mx * args.ui_scale, cam.my * args.ui_scale)
    n = 0
    for f in range(0, frames, every):
        if f > 0:
            tick = step_one(every)
        # the seat's zone erase, a few brush orders per tick, cycling over the view
        epf = shot.get("erase_per_frame", args.erase_per_frame)
        every_n = shot.get("erase_every", 1)
        if chunks and epf > 0 and (n % every_n == 0):
            per = max(1, min(len(chunks), epf))
            for k in range(per):
                erase([chunks[(n * per + k) % len(chunks)]])
        if pan and f > 0:
            dx, dy = pan.get("dx", 0) * every, pan.get("dy", 0) * every
            call("ui_drag", {"button": "middle", "duration_ms": 1, "points": [
                {"x": centre_px[0], "y": centre_px[1]}, {"x": centre_px[0] + dx, "y": centre_px[1] + dy}]})
            cam.pan[0] += dx
            cam.pan[1] += dy
            if pointer:  # leave the pointer where the shot had it
                call("ui_move", {"x": pointer[0], "y": pointer[1]})
        for a in [a for a in actions if f <= a["frame"] < f + every]:
            if "act" in a:
                mcp.act(a["act"])
            elif "move_tile" in a:
                to = cam.tile(a["move_tile"])
                frm = pointer or (to[0] + a.get("from_dx", -500), to[1] + a.get("from_dy", 300))
                glide = (f, max(1, a.get("over", 1)), frm, to)
            elif "click_tile" in a:
                x, y = cam.tile(a["click_tile"])
                call("ui_click", {"x": x, "y": y, **({"button": a["button"]} if a.get("button") else {})})
                pointer = (x, y)
            elif "key" in a:
                call("ui_key", {"key": a["key"]})
            elif "skip_ticks" in a:
                # Let game time pass without filming (a cut inside the take): the
                # match steps on at normal speed and the seat keeps its areas erased.
                left = a["skip_ticks"]
                while left > 0:
                    k = min(15, left)
                    tick = step_one(k)
                    left -= k
                    if chunks:
                        erase(chunks[:len(chunks) // 2] if (left // 15) % 2 else chunks[len(chunks) // 2:])
            elif "hive_install" in a:
                # A real standing order, installed through the game's MCP server by the
                # agent filming this shot. Request and response go to the shot's transcript.
                h = a["hive_install"]
                hive_src = open(os.path.join(HERE, h["source"])).read().replace("__PLAN__", json.dumps(h["plan"]))
                st, _ = call("hive_status", {}, tok=False)
                transcript.append({"frame": f, "tick": tick, "tool": "hive_status", "result": st})
                req = {"action": "install", "session": st["session"], "operation_key": f"{shot['id']}-{int(time.time())}",
                       "name": h["name"], "description": h.get("description", ""), "source": hive_src,
                       "interval_ticks": h.get("interval", 25)}
                data, _ = call("hive_program", req)
                transcript.append({"frame": f, "tick": tick, "tool": "hive_program", "arguments": req, "result": data})
                a["result"] = data
                hive_session = st["session"]
            elif "hive_list" in a:
                data, _ = call("hive_program", {"action": "list", "session": hive_session})
                transcript.append({"frame": f, "tick": tick, "tool": "hive_program", "arguments": {"action": "list"}, "result": data})
            elif "tool" in a:
                data, _ = call(a["tool"], a.get("args", {}))
                a["result"] = {k: data[k] for k in list(data)[:12]} if isinstance(data, dict) else str(data)[:300]
            log.append({"frame": f, "tick": tick, "action": {k: a[k] for k in a if k != "frame"}})
        if glide:
            f0, nfr, frm, to = glide
            t = min(1.0, (f - f0 + every) / nfr)
            t = t * t * (3 - 2 * t)  # ease in and out
            pointer = (frm[0] + (to[0] - frm[0]) * t, frm[1] + (to[1] - frm[1]) * t)
            call("ui_move", {"x": pointer[0], "y": pointer[1]})
            if f - f0 + every >= nfr:
                glide = None
        shot_png(os.path.join(out, f"f{n:04d}.png"), 1920 if args.preview else 8192)
        frame_ticks.append(tick)
        n += 1
        if n % 30 == 0:
            print(f"  {shot['id']}: {n} frames, tick {tick}, {(time.time() - t0) / n:.2f} s/frame", flush=True)
    state = session.gtime()
    sidecar = {
        "id": shot["id"], "shot": shot, "frames": n, "ticks_per_frame": every,
        "first_tick": start, "last_tick": state["tick"],
        "speed": state["speed"], "ticks_per_second": state["ticks_per_second"],
        "source_save": os.path.relpath(src, args.matches), "source_save_sha256": sha256(src),
        "seat": f"local player sharing colony {shot['team']} with its AI",
        "camera": {"centre_tile": [v["x"], v["y"]], "zoom": view["zoom"], "view_tiles": view["view"],
                   "pan_native_px_per_frame": pan or None},
        "map": world["map"], "window": None, "ui_scale": args.ui_scale,
        "frame_ticks": frame_ticks,
        "erase_zones": sorted(set(c[0] for c in chunks)), "health_food_bars": "off (key I after load)",
        "inputs": log,
    }
    status, _, _ = mcp.call("ui_status")
    sidecar["window"] = [status.get("width"), status.get("height")]
    if hive_session:  # the standing order's own record of what it did while filmed
        data, _ = call("hive_program", {"action": "inspect", "session": hive_session, "name": [
            a for a in actions if "hive_install" in a][0]["hive_install"]["name"]})
        transcript.append({"frame": n, "tick": state["tick"], "tool": "hive_program", "arguments": {"action": "inspect"},
                           "result": data})
    if transcript:
        with open(os.path.join(out, "mcp-transcript.json"), "w") as fh:
            json.dump(transcript, fh, indent=1)
    with open(os.path.join(out, "shot.json"), "w") as fh:
        json.dump(sidecar, fh, indent=1)
    session.gtime("resume")
    print(f"{shot['id']}: {n} frames, ticks {start}..{state['tick']}, {(time.time() - t0) / max(1, n):.2f} s/frame")


film.clouds_set = False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("shots")
    ap.add_argument("out")
    ap.add_argument("--matches", required=True)
    ap.add_argument("--profile", required=True)
    ap.add_argument("--only")
    ap.add_argument("--port", type=int, default=47814)
    ap.add_argument("--ui-scale", type=float, default=2.0)
    ap.add_argument("--preview", type=int, default=0)
    ap.add_argument("--frames", type=int, default=0)
    ap.add_argument("--erase-per-frame", type=int, default=2)
    ap.add_argument("--refilm", action="store_true", help="film shots again even if already finished")
    args = ap.parse_args()
    mcp.PORT = args.port
    os.environ.setdefault("GLOB2_MCP_TOKEN_FILE", os.path.join(args.profile, "mcp-token"))
    shots = json.load(open(args.shots))
    only = args.only.split(",") if args.only else None
    for shot in shots:
        if only and shot["id"] not in only:
            continue
        # Resume: a finished shot (its sidecar is written last) is kept. A take is one
        # continuous run of ticks, so an unfinished shot is filmed again from its start.
        done = os.path.join(args.out, shot["id"] + ("-preview" if args.preview else ""), "shot.json")
        if os.path.exists(done) and not args.refilm:
            print(f"{shot['id']}: already filmed ({done}); --refilm to film it again")
            continue
        try:
            film(shot, args)
        except Exception as exc:
            print(f"{shot['id']}: FAILED {exc}", file=sys.stderr)


if __name__ == "__main__":
    main()
