#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Per-frame metrics of a frame-stepped take, for choosing in points.

    uv run --with pillow --with numpy python take_metrics.py RAW/<device>/<take> [--window FRAMES] [--every N]

Prints, every N frames: the event-list rows (counted from the game's own
controls by capture_frames.py, every third frame), the share of the map area that
is fog-dimmed (dark green pixels, as in the mobile captures' clean-state check),
and the share of red and blue unit pixels; then the best windows of the given
length by fewest rows, then least fog.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image

AREA = {"iphone-6.9": (0.0, 0.24, 1.0, 0.86), "ipad-13": (0.08, 0.16, 1.0, 0.97)}

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("take")
ap.add_argument("--window", type=int, default=90)
ap.add_argument("--every", type=int, default=15)
args = ap.parse_args()
take = Path(args.take)
side = json.loads((take / "take.json").read_text())
area = AREA[side["device"]]
rows = {}
last = None
for r in side["frame_log"]:
    if "event_rows" in r:
        last = r["event_rows"]
    rows[r["n"]] = last
fog, red, blue = {}, {}, {}
for r in side["frame_log"]:
    n = r["n"]
    if n % 5:
        continue
    im = Image.open(take / f"f{n:05d}.png").convert("RGB")
    w, h = im.size
    a = np.asarray(im.crop((int(area[0] * w), int(area[1] * h), int(area[2] * w), int(area[3] * h)))
                   .resize((w // 8, int((area[3] - area[1]) * h) // 8))).astype(int)
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    lum = 0.3 * R + 0.59 * G + 0.11 * B
    fog[n] = float(((lum < 70) & (G > R) & (G > B)).mean())
    red[n] = float(((R > 170) & (G < 120) & (B < 120)).mean())
    blue[n] = float(((B > 150) & (R < 110) & (G < 120)).mean())
for n in sorted(fog):
    if n % args.every == 0:
        print(f"{n:4d} tick {side['frame_log'][n]['tick']} rows {rows[n]} fog {fog[n]:.2f} red {red[n]:.3f} blue {blue[n]:.3f}")
cands = []
N = len(side["frame_log"])
for s in range(0, N - args.window + 1, 5):
    rr = [rows[k] for k in range(s, s + args.window) if rows[k] is not None]
    ff = [fog[k] for k in range(s, s + args.window) if k in fog]
    cands.append((max(rr), round(float(np.mean(ff)), 3), s))
cands.sort()
print("best windows (max rows, mean fog, start):", cands[:8])
