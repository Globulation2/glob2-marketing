#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Step-by-step scene control for round-2 captures (one command per call).

The capture game must already run (launch-capture-game.sh) on GLOB2_MCP_PORT.

usage:
  scene.py load MATCH TICK TEAM          join the seat (join-seat.py) and load the save
  scene.py clean                          bars lens off, clouds off (once per load)
  scene.py goto TICK                      run (8x/2x, then 1x) to an absolute tick
  scene.py view X Y ZOOM                  centre the camera
  scene.py erase X Y W H                  erase forbidden, clearing and guard areas in a tile rectangle
  scene.py shot OUT.png                   native frame + sidecar with tick, camera, status
  scene.py status                         tick, speed, colony status (free/total units...)
  scene.py key NAME                       press a key by SDL scancode name
  scene.py battles MATCH TICK TEAM        print the clashes battle-scan found

Environment: GLOB2_MCP_PORT (default 47815), GLOB2_MCP_TOKEN_FILE,
CAPTURE_MATCHES (headless match dir), CAPTURE_WORK (dir for joined saves),
CAPTURE_PROFILE (the game's profile dir).
"""
import json
import os
import subprocess
import sys
import time

import mcp
import session

mcp.PORT = int(os.environ.get("GLOB2_MCP_PORT", "47815"))
HERE = os.path.dirname(os.path.abspath(__file__))
MATCHES = os.environ.get("CAPTURE_MATCHES", "matches")
WORK = os.environ.get("CAPTURE_WORK", "work")
PROFILE = os.environ.get("CAPTURE_PROFILE", "profile")
STATE = os.path.join(WORK, "scene-state.json")
RENAMES = ["maxima=Maxima", "cortex=Cortex", "cabino=Cabino", "castor=Castor", "nicowar=Nicowar"]


def state():
    try:
        return json.load(open(STATE))
    except (OSError, ValueError):
        return {}


def save_state(s):
    os.makedirs(WORK, exist_ok=True)
    json.dump(s, open(STATE, "w"), indent=1)


def load(match, tick, team):
    src = os.path.join(MATCHES, match, f"checkpoint-{tick}.game.gz")
    dst = os.path.join(WORK, "saves", f"{match}-{tick}-t{team}.game.gz")
    if not os.path.exists(dst):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        cmd = [sys.executable, os.path.join(HERE, "join-seat.py"), src, dst, str(team)]
        for r in RENAMES:
            cmd += ["--rename", r]
        subprocess.run(cmd, check=True, stderr=subprocess.DEVNULL)
    session.load_save(dst, PROFILE, settle=0.5)
    session.gtime("pause")
    if session.gtime()["speed"] != "1x":
        session.speed(0)
    time.sleep(4.5)
    session.gtime("resume")
    save_state({"match": match, "tick": int(tick), "team": int(team), "actions": [], "src": src})
    clean()


def act_log(text):
    s = state()
    s.setdefault("actions", [])
    if text not in s["actions"]:
        s["actions"].append(text)
    save_state(s)


def clean():
    """Health and food bars off (the in-game toggle, key I) and clouds off."""
    # The toggle starts on with every loaded match; one press of I switches it off.
    data, _, err = mcp.call("ui_key", {"token": mcp.token(), "key": "I"})
    if err:
        raise RuntimeError(f"ui_key: {data}")
    act_log("pressed I (toggle draw information): health and food bars off")
    session.set_clouds(False, False)


def erase(x, y, w, h):
    world = session.world("summary")
    size = (world["map"]["width"], world["map"]["height"])
    session.erase_zones((int(x), int(y), int(w), int(h)), size, zones=("forbidden", "clearing", "guard"))
    act_log("erased the colony's forbidden, clearing and guard areas in view (Flags and areas)")


def goto(tick):
    # capture.run_until, inlined to avoid importing capture's argparse globals
    tick = int(tick)
    now = session.gtime()["tick"]
    changed = False
    if tick - now > 4500:
        session.speed(7)
        changed = True
        while session.gtime()["tick"] < tick - 3200:
            time.sleep(0.1)
    if tick - session.gtime()["tick"] > 1900:
        session.speed(3)
        changed = True
        while session.gtime()["tick"] < tick - 1100:
            time.sleep(0.1)
    if changed:
        session.speed(0)
    while session.gtime()["tick"] < tick:
        time.sleep(0.05)
    return session.gtime()["tick"]


def status():
    t = session.gtime()
    w = session.world("summary")
    return {"time": t, "status": w.get("status"), "map": w.get("map")}


def tile_native(tx, ty):
    """Native pixel of a tile's centre for the current camera (state camera)."""
    cam = state()["camera"]
    cx, cy = cam["centre_tile"]
    world = session.world("summary")
    mw, mh = world["map"]["width"], world["map"]["height"]
    px = 64 * cam["zoom"] / 2  # logical pixels per tile at UI scale 2
    for _, ctl in mcp.walk(mcp.inspect()):
        if ctl.get("key") == "game/map":
            b = ctl["bounds"]
            mx, my = b["x"] + b["w"] / 2, b["y"] + b["h"] / 2
    def delta(a, b, size):
        d = (a - b) % size
        return d - size if d > size / 2 else d
    return (mx + delta(tx, cx, mw) * px) * 2, (my + delta(ty, cy, mh) * px) * 2


def click_tile(tx, ty, tool="ui_click"):
    x, y = tile_native(tx, ty)
    data, _, err = mcp.call(tool, {"token": mcp.token(), "x": x, "y": y})
    if err:
        raise RuntimeError(f"{tool}: {data}")
    return data


def fog_share(vt=None):
    """Share of the view's tiles that the colony does not currently see (dimmed
    fog of war) and that are unexplored (black), read through a one-shot Hive
    script (a read: no orders)."""
    vt = vt or state()["camera"]["view_tiles"]
    # every 3rd tile in each direction (the full region exceeds the Hive work budget)
    src = ("function step(ctx){let n=0,f=0,b=0;for(let y=%d;y<%d;y+=3)for(let x=%d;x<%d;x+=3){"
           "const t=ctx.game.map.tile(x,y);n++;if(!t.explored)b++;else if(!t.visible)f++;}"
           "return {output:{n:n,fog:f,black:b}};}") % (vt["y"] + 1, vt["y"] + vt["height"], vt["x"] + 1,
                                                       vt["x"] + vt["width"])
    st, _, _ = mcp.call("hive_status", {})
    key = "fog-%d" % int(time.time() * 1000)
    mcp.call("hive_run", {"token": mcp.token(), "session": st["session"], "operation_key": key, "source": src})
    for _ in range(80):
        time.sleep(0.15)
        res, _, _ = mcp.call("hive_result", {"session": st["session"], "operation_key": key})
        if res.get("status") == "completed":
            o = res["output"]
            return {"fog": round(o["fog"] / o["n"], 3), "black": round(o["black"] / o["n"], 3)}
        if res.get("status") == "failed":
            return {"error": str(res.get("error"))[:100]}
    return {"error": "timeout"}


def hud_state():
    """The top bar's workers free/total and the number of event-list rows on screen."""
    free, events, rows = None, 0, []
    for _, ctl in mcp.walk(mcp.inspect()):
        key = ctl.get("key", "")
        if key == "game/stats/worker-count":
            free = int(str(ctl.get("value")).split("/")[0])
        elif key.startswith("game/events/"):
            events += 1
            rows.append(ctl.get("label"))
    return {"free": free if free is not None else -999, "events": events, "rows": rows}


def zone_share(path):
    """Per-10,000 share of the map area drawn in pure zone-outline colours
    (forbidden yellow, clearing red, guard blue). Needs Pillow and NumPy."""
    import numpy as np
    from PIL import Image
    with Image.open(path) as im:
        w = im.size[0]
        a = np.asarray(im.convert("RGB")).astype(int)[40:, : w - int(round(406 * w / 3840))]
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    yellow = ((r > 235) & (g > 235) & (b < 40)).mean() * 1e4
    red = ((r > 230) & (g < 30) & (b < 30)).mean() * 1e4
    blue = ((r < 30) & (g < 30) & (b > 200)).mean() * 1e4
    return round(float(yellow + red + blue), 3)


def clean_shot(path, tries=6, limit=1.0, note=""):
    """Erase the view's zones, shoot, and repeat while outlines remain."""
    vt = state()["camera"]["view_tiles"]
    share = None
    for i in range(tries):
        erase(vt["x"] - 2, vt["y"] - 2, vt["width"] + 4, vt["height"] + 4)
        time.sleep(0.6)
        side = shot(path, note)
        share = zone_share(path)
        if share <= limit:
            break
    side["zone_outline_share_per_10000"] = share
    side["erase_attempts"] = i + 1
    try:
        side["fog_of_war_in_view"] = fog_share()
    except Exception as exc:
        side["fog_of_war_in_view"] = {"error": str(exc)[:100]}
    json.dump(side, open(path[:-4] + ".json", "w"), indent=1)
    return side


def shot(path, note=""):
    meta = session.shot(path)
    t = session.gtime()
    w = session.world("summary")
    s = state()
    side = {"file": os.path.basename(path), "match": s.get("match"), "source_tick": s.get("tick"),
            "team": s.get("team"), "tick_at_capture": t["tick"], "speed": t["speed"], "paused": t["paused"],
            "camera": s.get("camera"), "colony_status": w.get("status"),
            "player_actions_before_capture": s.get("actions", []), "note": note,
            "window": [meta.get("native_width"), meta.get("native_height")]}
    json.dump(side, open(path[:-4] + ".json", "w"), indent=1)
    return side


def main(argv):
    cmd, rest = argv[0], argv[1:]
    if cmd == "load":
        load(*rest)
        print(json.dumps(status()["status"]))
    elif cmd == "clean":
        clean()
    elif cmd == "goto":
        print(goto(rest[0]))
    elif cmd == "view":
        v = session.view(rest[0], rest[1], rest[2] if len(rest) > 2 else 1.0)
        s = state()
        s["camera"] = {"centre_tile": [int(rest[0]), int(rest[1])], "zoom": v["zoom"], "view_tiles": v["view"]}
        save_state(s)
        print(json.dumps(v["view"]), v["zoom"])
    elif cmd == "erase":
        erase(*rest)
    elif cmd == "eraseview":
        vt = state()["camera"]["view_tiles"]
        erase(vt["x"] - 2, vt["y"] - 2, vt["width"] + 4, vt["height"] + 4)
    elif cmd == "shot":
        print(json.dumps(shot(rest[0], " ".join(rest[1:]))["colony_status"]))
    elif cmd == "burst":
        # burst PREFIX N GAP [x y zoom]: N frames GAP seconds apart, each right after an
        # erase of the view; keeps only frames whose colony has no negative free workers
        prefix, n, gap = rest[0], int(rest[1]), float(rest[2])
        for i in range(n):
            if len(rest) >= 6:
                session.view(rest[3], rest[4], rest[5])
            vt = state()["camera"]["view_tiles"]
            erase(vt["x"] - 2, vt["y"] - 2, vt["width"] + 4, vt["height"] + 4)
            time.sleep(0.3)
            st = session.world("summary")["status"]
            free = int(st["workers_free_total"].split("/")[0])
            if free < 0:
                print(i, "skip", st["workers_free_total"])
                time.sleep(gap)
                continue
            t = session.gtime()["tick"]
            path = f"{prefix}-{t}.png"
            side = shot(path)
            print(i, path, side["colony_status"]["workers_free_total"])
            time.sleep(gap)
    elif cmd == "hunt":
        # hunt PREFIX SECONDS MAXSHOTS [MINGAP]: shoot whenever the HUD's first stat
        # (workers free/total) is not negative and the event list has at most two rows;
        # every shot is preceded by an erase of the view's zones and checked for outlines.
        prefix, secs, maxshots = rest[0], float(rest[1]), int(rest[2])
        mingap = float(rest[3]) if len(rest) > 3 else 4.0
        end = time.time() + secs
        last_shot = last_erase = 0
        kept = 0
        maxrows = int(os.environ.get("HUNT_MAX_ROWS", "2"))
        minfree = int(os.environ.get("HUNT_MIN_FREE", "0"))
        vt = state()["camera"]["view_tiles"]
        while time.time() < end and kept < maxshots:
            if time.time() - last_erase > 2.5:
                erase(vt["x"] - 2, vt["y"] - 2, vt["width"] + 4, vt["height"] + 4)
                last_erase = time.time()
            hud = hud_state()
            if hud["free"] >= minfree and hud["events"] <= maxrows and time.time() - last_shot > mingap:
                t = session.gtime()["tick"]
                path = f"{prefix}-{t}.png"
                side = shot(path)
                share = zone_share(path)
                if share > 1.0:
                    side = clean_shot(path)
                else:
                    side["zone_outline_share_per_10000"] = share
                after = hud_state()
                if after["free"] < minfree or after["events"] > maxrows or side["zone_outline_share_per_10000"] > 1.0:
                    os.remove(path)
                    os.remove(path[:-4] + ".json")
                    print("discard", t, hud["free"], after["free"], side["zone_outline_share_per_10000"], flush=True)
                else:
                    last_erase = time.time()
                    side["hud"] = {"before": hud, "after": after}
                    json.dump(side, open(path[:-4] + ".json", "w"), indent=1)
                    kept += 1
                    last_shot = time.time()
                    print("kept", path, hud["free"], hud["events"], after["free"], after["events"],
                          side["zone_outline_share_per_10000"], flush=True)
            time.sleep(0.1)
    elif cmd == "cshot":
        side = clean_shot(rest[0], note=" ".join(rest[1:]))
        print(side["zone_outline_share_per_10000"], side["erase_attempts"], hud_state())
    elif cmd == "click":
        click_tile(float(rest[0]), float(rest[1]))
        act_log(f"clicked tile ({rest[0]}, {rest[1]})")
    elif cmd == "hover":
        click_tile(float(rest[0]), float(rest[1]), "ui_move")
    elif cmd == "select":
        # select TYPE X Y: click the colony's building of TYPE nearest tile X,Y
        want, nx, ny = rest[0], float(rest[1]), float(rest[2])
        bs = [b for b in session.world("summary")["colony"]["buildings"] if b["type"] == want]
        b = min(bs, key=lambda b: abs(b["x"] - nx) + abs(b["y"] - ny))
        click_tile(b["x"] + (b["width"] - 1) / 2, b["y"] + (b["height"] - 1) / 2)
        act_log(f"selected the {want} at ({b['x']}, {b['y']})")
        print(b)
    elif cmd == "act":
        print(mcp.act(rest[0], *(rest[1:2] or ["activate"]))[0])
        act_log(f"pressed {rest[0]}")
    elif cmd == "fog":
        print(fog_share())
    elif cmd == "hud":
        print(hud_state())
    elif cmd == "status":
        print(json.dumps(status(), indent=1))
    elif cmd == "key":
        data, _, err = mcp.call("ui_key", {"token": mcp.token(), "key": rest[0]})
        print(data)
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
