#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Check that no unwanted HUD reaches into any cut's picture.

usage: uv run --with pillow --with numpy python check_hud.py RAW_DIR [--data trailer.json] [--step 3]

For every segment of every cut (as build_trailer.py expands it, so the vertical's
reframes and the per-segment punch-ins are checked as cut), and every STEP-th frame:

- the event list: its exact text colours (red 200,30,30 and green 30,200,30) in the
  band along the top of the crop;
- the Hive card's button fill (66,44,94) along the bottom of the crop;
- the "Paused" label of tick stepping and the top bar: the crop must lie below y 36
  and above y 2600 of the 4256x2800 frame;
- for a segment with an "inset" (the desktop co-play beat), the inset crop of the Hive
  card itself: the button fill (65,43,88) and gold border (199,165,87) may appear only
  in its bottom 90 rows, where the card's own Pause and Cancel buttons are; the
  "Reports / details" and "Stop commander" buttons stacked above the card would show
  up higher, so none of them is in the picture. The main window of that segment must
  also end above the card stack (y 2380).

The right-hand build palette is in frame on purpose in the placement segments.
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build_trailer import card_top, expand  # noqa: E402


def near(a, rgb, tol):
    return (np.abs(a.astype(int) - np.array(rgb)) <= tol).all(axis=-1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("raw")
    ap.add_argument("--data", default=str(HERE / "trailer.json"))
    ap.add_argument("--step", type=int, default=3)
    args = ap.parse_args()
    data = json.loads(Path(args.data).read_text())
    used = {}
    for name in data["cuts"]:
        cut = expand(data, name)
        for seg in cut["timeline"]:
            crop = tuple(seg.get("crop") or data["frame"]["crop"])
            key = (seg["shot"], crop, json.dumps(seg.get("inset"), sort_keys=True))
            used.setdefault(key, set()).update(range(seg["in"], seg["in"] + seg["frames"]))
    bad, n, insets = [], 0, 0
    for (shot, (cw, ch, cx, cy), inset), frames in sorted(used.items()):
        inset = json.loads(inset)
        if cy < 36 or cy + ch > 2600:
            bad.append({"shot": shot, "crop": [cw, ch, cx, cy], "problem": "crop reaches the top bar or the Paused label"})
        for f in sorted(frames)[::args.step]:
            a = np.asarray(Image.open(Path(args.raw) / shot / f"f{f:04d}.png").convert("RGB"))
            top = a[cy:cy + 120, cx:cx + min(cw, 1200)].astype(int)
            text = (((top[..., 0] == 200) & (top[..., 1] == 30) & (top[..., 2] == 30)) |
                    ((top[..., 0] == 30) & (top[..., 1] == 200) & (top[..., 2] == 30))).sum()
            bot = a[cy + ch - 80:cy + ch, cx:cx + min(cw, 700)].astype(int)
            panel = ((abs(bot[..., 0] - 66) < 10) & (abs(bot[..., 1] - 44) < 10) & (abs(bot[..., 2] - 94) < 12)).sum()
            n += 1
            prob = {}
            if text > 20:
                prob["event_text_px"] = int(text)
            if panel > 2000:
                prob["panel_px"] = int(panel)
            if inset:
                insets += 1
                t = card_top(a, inset)
                region = a[t:inset["bottom"], inset["region_x"][0]:inset["region_x"][1]][:-90]
                button = int(near(region, (65, 43, 88), 3).sum())
                gold = int(near(region, (199, 165, 87), 6).sum())
                if button or gold or cy + ch > 2380:
                    prob.update({"inset_button_px_above_card_buttons": button, "inset_gold_px_above_card_buttons": gold})
            if prob:
                bad.append(dict({"shot": shot, "frame": f, "crop": [cw, ch, cx, cy]}, **prob))
    print(json.dumps({"frames_checked": n, "inset_frames_checked": insets, "problems": bad}, indent=1))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
