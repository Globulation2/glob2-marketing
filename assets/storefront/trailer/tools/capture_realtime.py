#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Film trailer shots in real time with the game's own recorder.

usage: capture_realtime.py SHOTS.json REALTIME.json OUT_DIR --matches DIR
                           [--only ID[,ID]] [--port N] [--refilm] [--extract-only]

For each take in REALTIME.json ("takes", one per shot of SHOTS.json plus extra
takes of the same ticks), this script:

  1. launches the game in a real window with its gameplay recorder on
     (launch-record-game.sh, GLOB2_WINDOW=window; the window fills the screen,
     3024x1666 on the capture Mac), recording at 30 frames a second, with a
     recording chapter every `chapter_ticks` ticks;
  2. joins a local player to the shot's colony in the headless all-AI save
     (as capture_shot.py), loads it, holds the match (game_time pause), switches
     health and food bars off, frames the camera at the old zoom times `scale`
     on the same tile and nudges it down `nudge_y` pixels, runs the match to the
     lead-in and erases the colony's zone markings in and around the view;
  3. lets the match run at normal speed from `preroll_ticks` before the shot's
     start tick to `postroll_ticks` after its last tick, performing the shot's
     scripted inputs when their tick comes up (the Inn ghost's glide in a thread
     of its own at about 30 moves a second) and erasing markings as it goes;
  4. stops the game (SIGTERM; the recorder finalizes the file) and extracts
     OUT/<take>/f%04d.png: frame n is the recorded frame shown when the match
     reached the tick capture_shot.py would have filmed as frame n (start + n,
     plus any declared skip), found from the recording's chapter times. The
     recording itself is kept as OUT/<take>/take.mp4 with its .json sidecar.

The edit (build_trailer.py with trailer-realtime.json) reads the same frame
numbers as the tick-stepped capture. Camera pans are done there, as a sliding
crop of the recorded frame; the game's camera stays still while recording.

A take whose OUT/<take>/shot.json exists is kept (--refilm films it again).
Move the mouse away from the game window while a take records: the window is
real, so a real pointer over it would be seen by the game.
"""
import argparse
import json
import os
import signal
import subprocess
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import capture_shot as cs  # noqa: E402  (also sets up mcp/session and the cached token)

mcp, session = cs.mcp, cs.session


def frame_ticks(shot, frames):
    """The tick capture_shot.py films as frame n: start + n plus the skips declared so far."""
    skips = sorted((a["frame"], a["skip_ticks"]) for a in shot.get("actions", []) if "skip_ticks" in a)
    out = []
    for n in range(frames):
        out.append(shot["start_tick"] + n + sum(k for f, k in skips if f <= n))
    return out


def launch(take_dir, port, rt):
    profile = os.path.join(take_dir, "profile")
    env = dict(os.environ, GLOB2_WINDOW="window", GLOB2_RECORD_CHAPTER_TICKS=str(rt["chapter_ticks"]))
    log = open(os.path.join(take_dir, "game.log"), "w")
    proc = subprocess.Popen([os.path.join(HERE, "launch-record-game.sh"), profile, "1920x1080", "1", str(port),
                             os.path.join(take_dir, "take.mp4"), "30"], env=env, stdout=log, stderr=subprocess.STDOUT)
    os.environ["GLOB2_MCP_TOKEN_FILE"] = os.path.join(profile, "mcp-token")
    cs._tok["value"] = None
    for _ in range(120):
        time.sleep(0.5)
        try:
            data, _, err = mcp.call("ui_status", timeout=5)
        except Exception:
            data, err = None, True
        if not err and isinstance(data, dict) and data.get("width"):
            return proc, profile, (data["width"], data["height"])
        if proc.poll() is not None:
            raise RuntimeError("game exited during start; see game.log")
    raise RuntimeError("game did not start")


def stop(proc, take_dir):
    proc.send_signal(signal.SIGTERM)
    try:
        proc.wait(timeout=60)
    except subprocess.TimeoutExpired:
        proc.kill()
    meta = json.load(open(os.path.join(take_dir, "take.mp4.json")))
    if not meta.get("complete") or meta.get("error"):
        raise RuntimeError(f"recording incomplete: {meta.get('error')}")
    return meta


def tick_times(meta):
    """(tick, time in s) at each gameplay chapter start of the recording."""
    pts = []
    for c in meta["chapters"]:
        if c.get("phase") == "gameplay" and "start_tick" in c:
            pts.append((c["start_tick"], c["start_us"] / 1e6))
    return pts


def time_of(tick, pts):
    """Recording time at which the match reached `tick`, from the nearest chapter starts
    around it (linear between them, the game's 30 ticks a second outside)."""
    before = [p for p in pts if p[0] <= tick]
    after = [p for p in pts if p[0] > tick]
    if before and after:
        (t0, s0), (t1, s1) = before[-1], after[0]
        return s0 + (s1 - s0) * (tick - t0) / (t1 - t0)
    t0, s0 = (before[-1] if before else after[0])
    return s0 + (tick - t0) / 30.0


def extract(take_dir, ticks, meta):
    """Write f%04d.png for each wanted tick: the recorded frame shown at that tick's time."""
    from PIL import Image
    pts = tick_times(meta)
    if not pts:
        raise RuntimeError("no gameplay chapters with ticks in the recording")
    fps = meta["fps"]
    want = [time_of(t, pts) for t in ticks]
    # A chapter starts at the first frame whose tick crossed the boundary, so the time
    # found is that frame's start; take the frame shown at that time.
    idx = [int(round(t * fps)) for t in want]
    tmp = os.path.join(take_dir, "decode")
    os.makedirs(tmp, exist_ok=True)
    for f in os.listdir(tmp):
        os.remove(os.path.join(tmp, f))
    # Decode each contiguous run of wanted frames once (the f-place take has a skip).
    runs, start = [], 0
    for k in range(1, len(idx) + 1):
        if k == len(idx) or idx[k] - idx[k - 1] > 30:
            runs.append((idx[start], idx[k - 1]))
            start = k
    for a, b in runs:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(take_dir, "take.mp4"), "-vf",
                        f"select='between(n,{a},{b})'", "-fps_mode", "passthrough", "-start_number", str(a),
                        os.path.join(tmp, "v%06d.png")], check=True)
    used = []
    for n, i in enumerate(idx):
        src = os.path.join(tmp, f"v{i:06d}.png")
        Image.open(src).save(os.path.join(take_dir, f"f{n:04d}.png"), compress_level=1)
        used.append(i)
    for f in os.listdir(tmp):
        os.remove(os.path.join(tmp, f))
    os.rmdir(tmp)
    repeats = sum(1 for k in range(1, len(used)) if used[k] == used[k - 1])
    return {"video_frames": used, "repeated_frames": repeats, "tick_time_points": len(pts)}


def layout_key_for_i():
    """The physical key (SDL scancode name) that types "i" on the Mac's current layout.

    ui_key sends a physical key and a real window reads it through the Mac's own
    layout; the game binds the bar toggle to the character "i". On the capture Mac
    the layout is Colemak, where "i" is on the QWERTY L key."""
    try:
        out = subprocess.run(["defaults", "read", "com.apple.HIToolbox", "AppleSelectedInputSources"],
                             capture_output=True, text=True).stdout
    except Exception:
        out = ""
    for layout, key in (("Colemak", "L"), ("Dvorak", "G")):
        if layout in out:
            return key
    return "I"


def blue_circle_pixels():
    """Pixels of the flag range circles (pure blue), drawn only with the health and food bars."""
    import io
    import numpy as np
    from PIL import Image
    _, images, err = mcp.call("ui_screenshot", {"max_width": 1512, "max_height": 1512}, timeout=60)
    if err or not images:
        return None
    a = np.asarray(Image.open(io.BytesIO(images[0])).convert("RGB")).astype(int)
    return int(((a[..., 0] < 30) & (a[..., 1] < 30) & (a[..., 2] > 220)).sum())


def bars_off(args):
    """Switch health and food bars off (the in-game toggle, one press) and check it took
    where flag circles are in view (they go with the bars)."""
    key = args.bars_key or layout_key_for_i()
    before = blue_circle_pixels()
    cs.call("ui_key", {"key": key})
    time.sleep(0.8)
    after = blue_circle_pixels()
    print(f"  bars toggle: key {key}, flag-circle pixels {before} -> {after}", flush=True)
    if before and before > 2000 and after is not None and after > before * 0.6:
        raise RuntimeError(f"health and food bars did not switch off with key {key} (--bars-key to override)")


class Glide(threading.Thread):
    """The pointer's eased glide, at about 30 moves a second on its own thread."""

    def __init__(self, frm, to, seconds):
        super().__init__(daemon=True)
        self.frm, self.to, self.seconds = frm, to, seconds
        self.pos = frm

    def run(self):
        t0 = time.time()
        while True:
            t = min(1.0, (time.time() - t0) / self.seconds)
            e = t * t * (3 - 2 * t)
            self.pos = (self.frm[0] + (self.to[0] - self.frm[0]) * e, self.frm[1] + (self.to[1] - self.frm[1]) * e)
            mcp.call("ui_move", {"x": self.pos[0], "y": self.pos[1], "token": cs.token()})
            if t >= 1.0:
                return
            time.sleep(1 / 30)


def film(shot, take, rt, args):
    take_dir = os.path.join(args.out, take["id"])
    os.makedirs(take_dir, exist_ok=True)
    frames = take.get("frames", shot["frames"])
    ticks = frame_ticks(shot, frames)
    start, last = ticks[0], ticks[-1]
    src, save = cs.joined_save(args.matches, args.out, shot)
    proc, profile, size = launch(take_dir, args.port, rt)
    try:
        if list(size) != rt["window"]:
            raise RuntimeError(f"window is {size}, expected {rt['window']}: the edit's crops assume that size")
        session.load_save(save, profile, settle=0.5)
        session.gtime("pause")
        if session.gtime()["speed"] != "1x":
            session.speed(0)
        time.sleep(4.5)
        session.set_clouds(False, False)
        # Back on the map with no menu or dialog open before any key press.
        for _ in range(40):
            ins = mcp.inspect()
            if ins.get("screen") == "game_session" and not ins.get("dialog"):
                break
            time.sleep(0.25)
        time.sleep(0.8)
        world = session.world("summary")
        map_size = (world["map"]["width"], world["map"]["height"])
        v = shot["view"]
        zoom = v.get("zoom", 1.0) * take["scale"]
        lead = 150 if shot.get("erase_zones") else 0
        cs.run_until(start - lead - 300)
        if session.gtime()["tick"] > start - lead:
            raise RuntimeError(f"overshot: tick {session.gtime()['tick']} is past {start - lead}")
        cs.step_to(start - lead)
        view = session.view(v["x"], v["y"], zoom)
        mx, my = cs.map_centre()
        centre_px = (mx * args.ui_scale, my * args.ui_scale)
        nudge = take.get("nudge_y", 0)
        if nudge:   # move the map content down by `nudge` native pixels: the game's own middle-button
            # drag, which moves the camera with the pointer, so the drag goes up
            cs.call("ui_drag", {"button": "middle", "duration_ms": 1, "points": [
                {"x": centre_px[0], "y": centre_px[1]}, {"x": centre_px[0], "y": centre_px[1] - nudge}]})
        cs.call("ui_move", {"x": rt["window"][0] - 4, "y": rt["window"][1] - 4})   # pointer out of the picture
        bars_off(args)   # with the shot framed, so flag circles in view can confirm it
        zones = shot.get("zones") or ("forbidden", "clearing", "guard")
        chunks = (cs.erase_chunks(view["view"], map_size, margin=6, zones=zones)
                  if shot.get("erase_zones") and rt.get("erase_zones", True) else [])
        for k in range(0, len(chunks), 3):
            cs.erase(chunks[k:k + 3])
            cs.step_one(2)
        cs.step_to(start - rt["preroll_ticks"])
        cam = cs.Camera(view, (v["x"], v["y"]), map_size, args.ui_scale)
        cam.pan = [0.0, -float(nudge)]
        frame_of = {f: ticks[min(f, frames - 1)] for f in range(frames)}
        actions = sorted([a for a in shot.get("actions", []) if "skip_ticks" not in a and a["frame"] < frames],
                         key=lambda a: a["frame"])
        for a in actions:
            a["_tick"] = frame_of[a["frame"]]
        log, transcript, samples = [], [], []
        hive_session = None
        glide = None
        pointer = None
        every_n = shot.get("erase_every", 1)
        epf = shot.get("erase_per_frame", 2)
        erase_gap = max(1, round(every_n / max(1, epf)))   # ticks between single-chunk erases
        last_erase, ci = 0, 0
        end = last + rt["postroll_ticks"]
        session.gtime("resume")
        t_resume = time.time()
        while True:
            st = session.gtime()
            tick = st["tick"]
            samples.append([round(time.time() - t_resume, 3), tick])
            while actions and actions[0]["_tick"] <= tick:
                a = actions.pop(0)
                if "act" in a:
                    mcp.act(a["act"])
                elif "move_tile" in a:
                    to = cam.tile(a["move_tile"])
                    frm = pointer or (to[0] + a.get("from_dx", -500), to[1] + a.get("from_dy", 300))
                    glide = Glide(frm, to, max(1, a.get("over", 1)) / 30.0)
                    glide.start()
                    pointer = to
                elif "click_tile" in a:
                    if glide:
                        glide.join()
                    x, y = cam.tile(a["click_tile"])
                    cs.call("ui_click", {"x": x, "y": y, **({"button": a["button"]} if a.get("button") else {})})
                    pointer = (x, y)
                elif "key" in a:
                    cs.call("ui_key", {"key": a["key"]})
                elif "hive_install" in a:
                    h = a["hive_install"]
                    hive_src = open(os.path.join(HERE, h["source"])).read().replace("__PLAN__", json.dumps(h["plan"]))
                    hs, _ = cs.call("hive_status", {}, tok=False)
                    transcript.append({"frame": a["frame"], "tick": tick, "tool": "hive_status", "result": hs})
                    req = {"action": "install", "session": hs["session"],
                           "operation_key": f"{take['id']}-{int(time.time())}", "name": h["name"],
                           "description": h.get("description", ""), "source": hive_src,
                           "interval_ticks": h.get("interval", 25)}
                    data, _ = cs.call("hive_program", req)
                    transcript.append({"frame": a["frame"], "tick": tick, "tool": "hive_program", "arguments": req,
                                       "result": data})
                    hive_session = hs["session"]
                elif "hive_list" in a:
                    data, _ = cs.call("hive_program", {"action": "list", "session": hive_session})
                    transcript.append({"frame": a["frame"], "tick": tick, "tool": "hive_program",
                                       "arguments": {"action": "list"}, "result": data})
                elif "tool" in a:
                    cs.call(a["tool"], a.get("args", {}))
                log.append({"frame": a["frame"], "planned_tick": a["_tick"], "tick": tick,
                            "action": {k: v for k, v in a.items() if not k.startswith("_") and k != "frame"}})
            if chunks and tick - last_erase >= erase_gap and (glide is None or not glide.is_alive()):
                cs.erase([chunks[ci % len(chunks)]])
                ci += 1
                last_erase = tick
            if tick >= end:
                break
            time.sleep(0.01)
        session.gtime("pause")
        if hive_session:
            name = [a for a in shot["actions"] if "hive_install" in a][0]["hive_install"]["name"]
            data, _ = cs.call("hive_program", {"action": "inspect", "session": hive_session, "name": name})
            transcript.append({"frame": frames, "tick": session.gtime()["tick"], "tool": "hive_program",
                               "arguments": {"action": "inspect"}, "result": data})
        time.sleep(1.0)
    finally:
        meta = stop(proc, take_dir)
    got = extract(take_dir, ticks, meta)
    late = [e["tick"] - e["planned_tick"] for e in log]
    sidecar = {
        "id": take["id"], "shot": shot, "take": take, "frames": frames, "method": "real time, game recorder",
        "first_tick": start, "last_tick": last, "frame_ticks": ticks,
        "source_save": os.path.relpath(src, args.matches), "source_save_sha256": cs.sha256(src),
        "seat": f"local player sharing colony {shot['team']} with its AI",
        "camera": {"centre_tile": [v["x"], v["y"]], "zoom": zoom, "old_zoom": v.get("zoom", 1.0),
                   "nudge_y_px": take.get("nudge_y", 0), "view_tiles": view["view"],
                   "edit_pan_px_per_frame": shot.get("pan")},
        "map": world["map"], "window": list(size), "ui_scale": 1, "pixel_scale": args.ui_scale,
        "erase_zones": sorted(set(c[0] for c in chunks)), "health_food_bars": "off (key I after load)",
        "inputs": log, "input_lateness_ticks": late,
        "recording": {k: meta.get(k) for k in ("fps", "width", "height", "encoder", "crf", "dropped_frames",
                                                "dropped_audio_samples", "duration_us")},
        "extraction": got, "tick_samples": samples[::10],
    }
    if transcript:
        json.dump(transcript, open(os.path.join(take_dir, "mcp-transcript.json"), "w"), indent=1)
    json.dump(sidecar, open(os.path.join(take_dir, "shot.json"), "w"), indent=1)
    print(f"{take['id']}: {frames} frames, ticks {start}..{last}, dropped {meta.get('dropped_frames')}, "
          f"repeated {got['repeated_frames']}, inputs late by {late} ticks", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("shots")
    ap.add_argument("realtime")
    ap.add_argument("out")
    ap.add_argument("--matches", required=True)
    ap.add_argument("--only")
    ap.add_argument("--port", type=int, default=47815)
    ap.add_argument("--ui-scale", type=float, default=2.0, help="native pixels per logical pixel (Retina: 2)")
    ap.add_argument("--refilm", action="store_true")
    ap.add_argument("--bars-key", help="physical key that types 'i' (default: from the Mac's keyboard layout)")
    args = ap.parse_args()
    mcp.PORT = args.port
    shots = {s["id"]: s for s in json.load(open(args.shots))}
    rt = json.load(open(args.realtime))
    only = args.only.split(",") if args.only else None
    failed = 0
    for take in rt["takes"]:
        if only and take["id"] not in only:
            continue
        if os.path.exists(os.path.join(args.out, take["id"], "shot.json")) and not args.refilm:
            print(f"{take['id']}: already filmed; --refilm to film it again")
            continue
        shot = shots[take.get("from", take["id"])]
        take_dir = os.path.join(args.out, take["id"])
        if os.path.isdir(take_dir):   # an earlier or unfinished take of this id: the recorder never overwrites
            import shutil
            shutil.rmtree(take_dir)
        try:
            film(shot, take, rt, args)
        except Exception as exc:
            failed += 1
            print(f"{take['id']}: FAILED {exc}", file=sys.stderr, flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
