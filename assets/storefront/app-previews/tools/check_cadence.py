#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Frame cadence of the app previews: repeated, frozen or jumping frames in the gameplay area.

    uv run --with pillow --with numpy python check_cadence.py FILE.mp4 [...] --device iphone-6.9|ipad-13 \
        [--json OUT.json] [--cuts 3.0,9.6,...]
    uv run --with pillow --with numpy python check_cadence.py --frames RAW_TAKE_DIR [...] --device ...

For every pair of consecutive frames it measures the mean absolute difference of
the gameplay area (the map between the HUD's top cards and the bottom bar, in
8-bit levels, on a half-size greyscale copy). A frame that repeats the one before
(difference below --still, encoder noise aside) is a held frame; in a
frame-stepped take the game moves every tick, so held frames should not occur
except where the game itself is static. A hitch in a live recording shows as a
run of held frames followed by a jump (a difference far above its neighbours).
Reported per file: the frame count, every run of held frames with its time, the
largest jumps relative to the local median (cuts given with --cuts are expected
jumps and are excluded), and summary statistics.
"""
import argparse
import json
import subprocess
from pathlib import Path

import numpy as np

AREA = {  # gameplay area as fractions of the frame (x0, y0, x1, y1)
    "iphone-6.9": (0.0, 0.24, 1.0, 0.80),
    "ipad-13": (0.08, 0.16, 1.0, 0.70),
}


def decode(path, size):
    w, h = size
    cmd = ["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"scale={w // 2}:{h // 2}:flags=area,format=gray",
           "-f", "rawvideo", "-"]
    raw = subprocess.run(cmd, check=True, capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h // 2, w // 2)


def png_frames(directory, step=2):
    from PIL import Image
    files = sorted(Path(directory).glob("f*.png"))
    frames = []
    for f in files:
        im = Image.open(f).convert("L")
        frames.append(np.asarray(im.resize((im.width // step, im.height // step), Image.BOX)))
    return np.stack(frames), [f.name for f in files]


def analyse(frames, device, fps=30, cuts=(), still=0.05):
    h, w = frames.shape[1:]
    x0, y0, x1, y1 = AREA[device]
    a = frames[:, int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)].astype(np.int16)
    diffs = np.abs(np.diff(a, axis=0)).mean(axis=(1, 2))
    held = diffs < still
    runs, k = [], 0
    while k < len(held):
        if held[k]:
            j = k
            while j < len(held) and held[j]:
                j += 1
            runs.append({"from_frame": int(k + 1), "frames": int(j - k), "time_s": round((k + 1) / fps, 3)})
            k = j
        else:
            k += 1
    cut_frames = {int(round(c * fps)) for c in cuts}
    jumps = []
    for i, d in enumerate(diffs):
        if (i + 1) in cut_frames or any(abs(i + 1 - c) <= 1 for c in cut_frames):
            continue
        lo, hi = max(0, i - 15), min(len(diffs), i + 16)
        neighbours = np.concatenate([diffs[lo:i], diffs[i + 1:hi]])
        med = float(np.median(neighbours)) if len(neighbours) else float(d)
        if med > 0:
            jumps.append((float(d) / med, i + 1, float(d), med))
    jumps.sort(reverse=True)
    return {
        "frames": int(len(frames)),
        "pairs": int(len(diffs)),
        "held_frames": int(held.sum()),
        "held_runs": runs,
        "difference_min": round(float(diffs.min()), 3),
        "difference_median": round(float(np.median(diffs)), 3),
        "difference_p5": round(float(np.percentile(diffs, 5)), 3),
        "jump_ratio_max": round(jumps[0][0], 2) if jumps else None,
        "largest_jumps": [{"frame": f, "time_s": round(f / fps, 3), "ratio": round(r, 2), "difference": round(d, 3),
                           "local_median": round(m, 3)} for r, f, d, m in jumps[:6]],
        "jumps_over_2x": int(sum(1 for r, *_ in jumps if r > 2.0)),
        "jumps_over_3x": int(sum(1 for r, *_ in jumps if r > 3.0)),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--device", required=True, choices=sorted(AREA))
    ap.add_argument("--frames", action="store_true", help="the arguments are raw take directories of PNG frames")
    ap.add_argument("--cuts", default="", help="edit points in seconds, excluded from the jump list")
    ap.add_argument("--still", type=float, default=0.05)
    ap.add_argument("--json")
    args = ap.parse_args()
    size = {"iphone-6.9": (886, 1920), "ipad-13": (1200, 1600)}[args.device]
    cuts = [float(c) for c in args.cuts.split(",") if c]
    results = []
    for f in args.files:
        frames = png_frames(f)[0] if args.frames else decode(f, size)
        r = {"file": Path(f).name, **analyse(frames, args.device, cuts=cuts, still=args.still)}
        results.append(r)
        print(f"{r['file']}: {r['frames']} frames, held {r['held_frames']} in {len(r['held_runs'])} runs "
              f"{[(x['time_s'], x['frames']) for x in r['held_runs']][:8]}, diff median {r['difference_median']} "
              f"min {r['difference_min']}, jumps >2x {r['jumps_over_2x']}, >3x {r['jumps_over_3x']}, "
              f"max {r['jump_ratio_max']}")
    if args.json:
        Path(args.json).write_text(json.dumps(results, indent=1) + "\n")


if __name__ == "__main__":
    main()
