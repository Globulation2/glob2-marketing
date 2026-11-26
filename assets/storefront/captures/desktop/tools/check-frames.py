#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Sanity checks for captured frames.

usage: uv run --with pillow --with numpy python check-frames.py FILE.png ...

Reports, per frame: size and aspect, the share of pure-black pixels in the map
area (unexplored fog), and page seams: full-height or full-width one-pixel dark
lines, which the portable-sdl renderer draws between terrain pages at zooms
whose tile size is not a whole number of pixels (use zooms that are multiples
of 1/8).
"""
import sys

import numpy as np
from PIL import Image


def seams(lum, axis):
    """Indices of one-pixel lines much darker than both neighbours along most of their length."""
    a = lum if axis == 0 else lum.T
    mid, prev, nxt = a[:, 1:-1], a[:, :-2], a[:, 2:]
    dark = (mid + 18 < prev) & (mid + 18 < nxt) & (mid < 60)
    share = dark.mean(axis=0)
    return [int(i) + 1 for i in np.nonzero(share > 0.45)[0]]


def main():
    bad = 0
    for path in sys.argv[1:]:
        im = Image.open(path).convert("RGB")
        w, h = im.size
        arr = np.asarray(im).astype(np.int16)
        side = int(round(406 * w / 3840)) if w >= 2880 else 406  # sidebar is 203 points at UI scale 2
        area = arr[40:, : w - 406]
        lum = area.sum(axis=2) // 3
        black = float((lum < 6).mean())
        cols, rows = seams(lum, 0), seams(lum, 1)
        flag = "SEAMS" if cols or rows else "ok"
        if cols or rows or black > 0.12:
            bad += 1
        print(f"{path.split('/')[-1]}: {w}x{h} ({w / h:.4f}) black {black:.1%} {flag}"
              + (f" cols {cols[:4]} rows {rows[:4]}" if cols or rows else ""))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
