#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Write trailer-realtime.json: the edit of trailer.json, re-framed for the real-time takes.

usage: make_realtime_edit.py [--data trailer.json] [--realtime realtime.json] [--shots shots.json]
                             [--out trailer-realtime.json]

The tick-stepped capture filmed a 4256x2800 window; the real-time takes
(capture_realtime.py) are 3024x1666 recordings in which the map is drawn at
`scale` of its old size, centred on the same tile and nudged down `nudge_y`
pixels. A point (X, Y) of an old frame is therefore at

    x = cx_new + (X - cx_old) * scale,   y = cy_new + (Y - cy_old) * scale + nudge_y

in the take (cx, cy: the map canvas centres in realtime.json). Each segment's
crop keeps its old centre and its old size times `scale`, moved as little as
needed to stay inside the map canvas below `safe_top` (clear of the top bar and
the event list) and left of the sidebar. Segment-specific choices that cannot be
mapped (the build palette shot includes the sidebar, which does not scale with
the map) are set here explicitly. Camera pans (shots.json "pan") become a crop
that slides `pan.dx * scale` pixels a frame over the recorded frame.

Only 1080p is made from these takes ("uhd": false): the largest 16:9 map window
in a take is 2560x1440. The vertical cut's 9:16 windows are 810x1440 and are
upscaled to 1080x1920.
"""
import argparse
import copy
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

# The punch-in segments use the second, full-scale take of the oasis fight.
CLOSE = {"f-battle-honey": "f-battle-honey-close"}
# The build-palette segment: a 16:9 window flush with the right edge of the frame,
# so the whole palette in the sidebar is in it, below the event list.
PALETTE = [2304, 1296, 720, 214]
# Real time moves a few starts: in the real-time co-play take the standing order's
# install is queued and the game's Hive card first shows at frame 18, not 15, so the
# desktop cut starts that shot 3 frames later and gives the 3 frames to the next shot.
RETIME = {("desktop", "f-coplay2"): {"in": 18, "frames": 132},
          ("desktop", "f-econ"): {"frames": 123}}
# The co-play shot's main window, set by hand: in the real-time take the HUD's
# "Stop commander" button (Commander is a paid service no listing may show) sits at
# x 32-632, y 1326-1393 above the Hive card, so the window ends above it (y 1300),
# still centred on the four Inn sites, and is native pixels at 1080p.
COPLAY_WINDOW = [1920, 1080, 405, 220]


def setup(rt, shots):
    takes = {t["id"]: t for t in rt["takes"]}
    return takes, {s["id"]: s for s in shots}


def to_new(p, take, rt):
    (ox, oy), (nx, ny) = rt["old_canvas_centre"], rt["new_canvas_centre"]
    s = take["scale"]
    return nx + (p[0] - ox) * s, ny + (p[1] - oy) * s + take.get("nudge_y", 0)


def fit(w, h, cx, cy, rt, slide=0.0):
    """Top-left of a w x h window centred near (cx, cy), inside the map canvas below
    safe_top, with room for `slide` pixels of horizontal travel (sign = direction)."""
    mx, my, mw, mh = rt["map_canvas"]
    top, bottom = max(my, rt["safe_top"]), my + mh
    lo, hi = mx, mx + mw - w
    x = round(cx - w / 2)
    if slide > 0:
        x = min(max(x, lo), hi - int(slide + 1))
    elif slide < 0:
        x = max(min(x, hi), lo - int(slide - 1))
    x = min(max(x, lo), hi)
    y = min(max(round(cy - h / 2), top), bottom - h)
    if x < lo or y < top:
        raise SystemExit(f"window {w}x{h} does not fit the map canvas")
    return x, y


def map_segment(seg, cut_default, takes, shots, rt, size=(1920, 1080)):
    out = {k: v for k, v in seg.items() if k not in ("crop", "note")}
    shot_id = seg["shot"]
    if seg.get("crop") and shot_id in CLOSE and seg.get("upscale"):
        shot_id = CLOSE[shot_id]           # a punch-in: the full-scale take
    out["shot"] = shot_id
    take = takes[shot_id]
    s = take["scale"]
    old = seg.get("crop") or cut_default
    w, h = old[0] * s, old[1] * s
    if seg["shot"] == "f-place" and old == [2848, 1602, 1408, 40]:
        out["crop"] = list(PALETTE)
        out["note"] = "build palette: window flush with the frame's right edge, so the sidebar palette (HUD, not scaled) is whole"
        return out
    if abs(w / h - size[0] / size[1]) > 0.01:
        h = round(w * size[1] / size[0])
    w, h = round(w), round(h)
    cx, cy = to_new((old[2] + old[0] / 2, old[3] + old[1] / 2), take, rt)
    pan = (shots[take.get("from", shot_id)].get("pan") or {}).get("dx", 0) * s
    frames_end = seg["in"] + seg["frames"]
    x, y = fit(w, h, cx, cy, rt, slide=pan * frames_end)
    out["crop"] = [w, h, x, y]
    if pan:
        out["pan_x"] = round(pan, 4)       # crop x = x + pan_x * (frame number in the take)
    if w < size[0] or h < size[1]:
        out["upscale"] = True
    elif "upscale" in out:
        del out["upscale"]
    if seg.get("inset"):
        out["crop"] = list(COPLAY_WINDOW)
        out.pop("upscale", None)
        ins = dict(seg["inset"])
        shift = 2800 - rt["window"][1]     # the HUD is anchored to the bottom-left corner
        ins["bottom"] -= shift
        out["inset"] = ins
    return out


def vertical(master, takes, shots, rt):
    """9:16 windows (810x1440) centred where the master's segment is, upscaled to 1080x1920."""
    segs = []
    for seg in master["timeline"]:
        take = takes[seg["shot"]]
        w, h = seg["crop"][0], seg["crop"][1]
        cx = seg["crop"][2] + w / 2
        cy = seg["crop"][3] + h / 2
        vw, vh = 810, 1440
        pan = seg.get("pan_x", 0)
        x, y = fit(vw, vh, cx, cy, rt, slide=pan * (seg["in"] + seg["frames"]))
        v = {"shot": seg["shot"], "in": seg["in"], "frames": seg["frames"], "crop": [vw, vh, x, y], "upscale": True}
        if pan:
            v["pan_x"] = pan
        segs.append(v)
    return segs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=str(HERE / "trailer.json"))
    ap.add_argument("--realtime", default=str(HERE / "realtime.json"))
    ap.add_argument("--shots", default=str(HERE / "shots.json"))
    ap.add_argument("--out", default=str(HERE / "trailer-realtime.json"))
    args = ap.parse_args()
    data = json.loads(Path(args.data).read_text())
    rt = json.loads(Path(args.realtime).read_text())
    takes, shots = setup(rt, json.loads(Path(args.shots).read_text()))
    new = copy.deepcopy(data)
    new["frame"] = {"native": rt["window"], "size": [1920, 1080], "crop": None,
                    "note": "Real-time takes (capture_realtime.py): 3024x1666 recordings; every segment names its "
                            "own crop, computed by make_realtime_edit.py from trailer.json. 1080p only.",
                    # For check_hud.py: no "Paused" label in real time; the top bar ends at
                    # y 32 and the co-play take's card stack ("Stop commander") starts at y 1326.
                    "hud_limits": {"top": 32, "bottom": rt["window"][1], "card_stack_top": 1320,
                                   "inset_text_px": 20}}
    default = data["frame"]["crop"]
    for name, cut in new["cuts"].items():
        if cut.get("timeline_from"):
            continue
        cut["uhd"] = False
        cut["timeline"] = [map_segment(dict(seg, **RETIME.get((name, seg["shot"]), {})), default, takes, shots, rt)
                           for seg in cut["timeline"]]
    for name, cut in list(new["cuts"].items()):
        src = cut.get("timeline_from")
        if not src:
            continue
        base = new["cuts"][src]
        for key in ("text", "wordmark", "music", "duration"):
            cut.setdefault(key, copy.deepcopy(base.get(key)))
        cut.pop("timeline_from")
        cut.pop("reframe", None)
        cut["timeline"] = vertical(base, takes, shots, rt)
        cut["note"] = "9:16 windows of 810x1440 native pixels centred on the master's framing, upscaled to 1080x1920"
    p = data["poster"]
    take = takes[CLOSE[p["shot"]]]
    seg0 = new["cuts"]["master"]["timeline"][0]
    new["poster"] = dict(p, shot=CLOSE[p["shot"]], crop=list(seg0["crop"]),
                         note=p["note"] + "; real-time take at native pixels, so the 3840x2160 file is a 1.5x upscale")
    Path(args.out).write_text(json.dumps(new, indent=1, ensure_ascii=False) + "\n")
    for name, cut in new["cuts"].items():
        print(name)
        for seg in cut["timeline"]:
            print("  ", seg["shot"], seg["in"], seg["frames"], seg["crop"], "pan" if seg.get("pan_x") else "",
                  "upscale" if seg.get("upscale") else "")


if __name__ == "__main__":
    main()
