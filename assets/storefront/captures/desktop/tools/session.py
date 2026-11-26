#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Capture-session helpers on top of mcp.py: load a save, frame, wait, shoot.

usage:
  session.py load SAVE_LABEL            load profile/games/SAVE_LABEL.game.gz
  session.py view X Y [ZOOM]            centre the camera on a tile
  session.py shot OUT.png               native-resolution frame
  session.py world [detail]             game_world as JSON
  session.py speed N                    top-bar speed level (-3..10)
  session.py tick                       current tick / pause state
  session.py run TICKS                  let TICKS pass (polls game_time)
"""
import json
import sys
import time

import mcp


def screen():
    return mcp.inspect().get("screen")


def controls():
    return list(mcp.walk(mcp.inspect()))


def has(key):
    return any(c.get("key") == key for _, c in controls())


def dismiss_message():
    for _ in range(3):
        if screen() != "message":
            return
        mcp.act("choice/0")
        time.sleep(0.5)


def load(label, timeout=90):
    dismiss_message()
    scr = screen()
    if scr == "audio_preference":  # first-run question of a fresh profile
        mcp.act("audio.silence")
        time.sleep(1.0)
        scr = screen()
    if scr == "introduction_offer":
        mcp.act("intro/menu")
        time.sleep(1.0)
        scr = screen()
    if scr == "game_session" and has("outcome/reason"):  # "You have won/lost" card of a finished match
        mcp.act("continue")
        time.sleep(0.8)
    if scr == "game_session":
        # Leave through the main menu. Loading from inside a match would print
        # "<player> has quit the game" into the next one for half a minute.
        for _ in range(20):
            if has("quit"):
                break
            if has("game/menu"):
                mcp.act("game/menu")
            time.sleep(0.6)
        mcp.act("quit")
        # A busy match (large map at high speed) can take many seconds to leave.
        for _ in range(60):
            time.sleep(0.5)
            scr = screen()
            if scr != "game_session":
                break
    if scr == "end_game":
        mcp.act("quit")
        time.sleep(1.5)
        scr = screen()
    if scr == "main_menu":
        mcp.act("menu/2")
    elif scr != "choose_map":
        raise RuntimeError(f"cannot load from screen {scr}")
    time.sleep(1.0)
    index = None
    for _, ctl in mcp.walk(mcp.inspect(compact=False)):  # full tree: lists may scroll
        if ctl.get("role") == "option" and ctl.get("label") == label:
            index = int(ctl["key"].split("/")[-1])
    if index is None:
        raise RuntimeError(f"save {label!r} is not listed")
    mcp.act("files", "select", index)
    time.sleep(0.4)
    mcp.act("ok")
    deadline = time.time() + timeout
    while time.time() < deadline:
        time.sleep(1.0)
        insp = mcp.inspect()
        if insp.get("screen") == "message":
            raise RuntimeError("load failed: " + json.dumps(insp)[:400])
        if insp.get("screen") == "game_session" and any(c.get("key") == "game/map" for _, c in mcp.walk(insp)):
            if not any(c.get("key") in ("files", "load") for _, c in mcp.walk(insp)):
                return True
    raise RuntimeError("load timed out")


WORK_LABEL = "a-capture"  # sorts first, so the save list always shows it


def load_save(path, profile, settle=4.5):
    """Copy a .game.gz into the capture profile as the working save and load it.

    Waits `settle` seconds afterwards: the match-intro card (map name and
    players) fades out over the first seconds of a loaded match.
    """
    import os
    import shutil
    games = os.path.join(profile, "games")
    os.makedirs(games, exist_ok=True)
    shutil.copyfile(path, os.path.join(games, WORK_LABEL + ".game.gz"))
    load(WORK_LABEL)
    time.sleep(settle)


def view(x, y, zoom=None):
    args = {"x": int(x), "y": int(y)}
    if zoom is not None:
        args["zoom"] = float(zoom)
    args["token"] = mcp.token()
    data, _, err = mcp.call("game_view", args)
    if err:
        raise RuntimeError(f"game_view: {data}")
    return data


def shot(path):
    return mcp.screenshot(path)


def world(detail="summary", **extra):
    data, _, err = mcp.call("game_world", dict(detail=detail, **extra))
    if err:
        raise RuntimeError(f"game_world: {data}")
    return data


def gtime(action="status", **extra):
    args = dict(action=action, **extra)
    if action != "status":
        args["token"] = mcp.token()
    data, _, err = mcp.call("game_time", args)
    if err:
        raise RuntimeError(f"game_time: {data}")
    return data


def erase_zones(area, map_size, zones=("forbidden", "clearing"), chunk=32, pause=0.02):
    """Erase the local colony's zone markings over a tile rectangle, as the player.

    The AI sharing the colony paints forbidden and clearing areas around its
    buildings; the Flags and areas panel lets a player erase them. `area` is
    (x, y, width, height) in tiles and may cross the map's wrap-around. Each
    game_zone call is one brush order; squares of at most 32 tiles are used
    because larger masks were not applied reliably.
    """
    x0, y0, w, h = area
    w, h = min(w, map_size[0]), min(h, map_size[1])

    def spans(start, length, size):
        """Split [start, start+length) on the torus into chunks that do not wrap."""
        out, done = [], 0
        while done < length:
            pos = (start + done) % size
            n = min(chunk, length - done, size - pos)
            out.append((pos, n))
            done += n
        return out
    for zone in zones:
        for x, cw in spans(x0, w, map_size[0]):
            for y, ch in spans(y0, h, map_size[1]):
                data, _, err = mcp.call("game_zone", {"token": mcp.token(), "zone": zone, "mode": "erase",
                                                      "x": x, "y": y, "width": cw, "height": ch})
                if err:
                    raise RuntimeError(f"game_zone: {data}")
                time.sleep(pause)


def set_clouds(clouds=True, shadows=True):
    """Settings > Display & graphics > Clouds / Cloud shadows, from a running match."""
    if screen() != "settings":
        if not has("settings"):
            mcp.act("game/menu")
            time.sleep(0.6)
        mcp.act("settings")
        time.sleep(1.0)
    for key, want in (("graphics.clouds", clouds), ("graphics.shadows", shadows)):
        current = [c for _, c in controls() if c.get("key") == key][0].get("value")
        if bool(current) != bool(want):
            mcp.act(key, "set_value", bool(want))
            time.sleep(0.3)
    mcp.act("done")
    time.sleep(0.8)
    if has("return"):
        mcp.act("return")
        time.sleep(0.4)


def speed(level):
    """Set the top-bar speed level (0 is 1x, 3 is 2x, 5 is 4x, 7 is 8x) and confirm it took.

    While a match fast-forwards, the control's revision can change under the
    call and the action is refused, so retry until game_time reports the change.
    """
    want_normal = int(level) == 0
    for _ in range(8):
        try:
            mcp.act("game/speed", "set_value", int(level))
        except Exception:
            pass
        time.sleep(0.25)
        if (gtime()["speed"] == "1x") == want_normal:
            return
    raise RuntimeError(f"could not set speed level {level}")


def run(ticks, poll=0.25, timeout=600):
    """Let `ticks` game ticks pass at the current speed; returns the tick reached."""
    start = gtime()["tick"]
    deadline = time.time() + timeout
    while time.time() < deadline:
        now = gtime()["tick"]
        if now - start >= ticks:
            return now
        time.sleep(poll)
    raise RuntimeError("run timed out")


def main(argv):
    cmd = argv[0]
    if cmd == "load":
        print(load(argv[1]))
    elif cmd == "view":
        print(json.dumps(view(*argv[1:])))
    elif cmd == "shot":
        meta = shot(argv[1])
        print(json.dumps({k: meta[k] for k in ("native_width", "native_height", "frame_id") if k in meta}))
    elif cmd == "world":
        print(json.dumps(world(*(argv[1:2])), indent=1))
    elif cmd == "speed":
        print(json.dumps(speed(argv[1])[0])[:200])
    elif cmd == "tick":
        print(json.dumps(gtime()))
    elif cmd == "run":
        print(run(int(argv[1])))
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
