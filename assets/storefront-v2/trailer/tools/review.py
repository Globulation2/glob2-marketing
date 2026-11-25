#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# /// script
# requires-python = ">=3.10"
# dependencies = ["pillow==13.0.0", "numpy==2.3.4"]
# ///
"""Editor's review aids for a finished trailer file.

usage: uv run review.py VIDEO.mp4 --sheet OUT.jpg [--every 0.5] [--cols 6] [--tile 640]
       uv run review.py VIDEO.mp4 --timing            (JSON report on stdout)

--sheet   one frame every --every seconds, each stamped with its time, as a contact sheet.
--timing  frame timing and motion: every frame's timestamp step (constant frame rate),
          the frames that repeat the one before (a stutter or dropped frame), the share
          of near-black pixels per sampled frame (fog-black, black frames) and the mean
          luma change between consecutive frames (0 would be a frozen picture).
"""
import argparse
import json
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def frames(path, width, height, vf):
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-i", path, "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                            stdout=subprocess.PIPE)
    size = width * height * 3
    while True:
        buf = proc.stdout.read(size)
        if len(buf) < size:
            break
        yield np.frombuffer(buf, np.uint8).reshape(height, width, 3)
    proc.wait()


def sheet(args, info):
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    w, h = v["width"], v["height"]
    tw = args.tile
    th = round(h * tw / w / 2) * 2
    tiles = []
    vf = f"fps=1/{args.every}:start_time=0:round=down,scale={tw}:{th}:flags=lanczos"
    for i, frame in enumerate(frames(args.video, tw, th, vf)):
        im = Image.fromarray(frame)
        d = ImageDraw.Draw(im)
        label = f"{i * args.every:05.2f}s"
        d.rectangle([0, 0, 8 * len(label) + 8, 16], fill=(0, 0, 0))
        d.text((4, 2), label, fill=(255, 255, 255))
        tiles.append(im)
    cols = args.cols
    rows = (len(tiles) + cols - 1) // cols
    out = Image.new("RGB", (cols * tw, rows * th), (16, 12, 24))
    for i, im in enumerate(tiles):
        out.paste(im, ((i % cols) * tw, (i // cols) * th))
    out.save(args.sheet, quality=88)
    print(f"{args.sheet}: {len(tiles)} frames, {out.size[0]}x{out.size[1]}")


def timing(args, info):
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    pts = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "frame=pts_time",
                          "-of", "csv=p=0", args.video], capture_output=True, text=True, check=True).stdout.split()
    times = [float(t.strip(",")) for t in pts if t.strip(",")]
    steps = np.diff(times)
    w, h = 480, round(v["height"] * 480 / v["width"] / 2) * 2
    prev = None
    diffs, black = [], []
    for frame in frames(args.video, w, h, f"scale={w}:{h}:flags=area"):
        luma = frame.astype(np.float32) @ np.array([0.2126, 0.7152, 0.0722], np.float32)
        black.append(float((luma < 12).mean()))
        if prev is not None:
            diffs.append(float(np.abs(luma - prev).mean()))
        prev = luma
    diffs = np.array(diffs)
    repeats = [i + 1 for i, d in enumerate(diffs) if d < 0.02]
    report = {
        "file": args.video, "frames": len(times), "avg_frame_rate": v["avg_frame_rate"], "r_frame_rate": v["r_frame_rate"],
        "duration": float(info["format"]["duration"]),
        "frame_step_ms": {"min": round(float(steps.min()) * 1000, 3), "max": round(float(steps.max()) * 1000, 3)},
        "constant_frame_rate": bool(steps.max() - steps.min() < 1e-4),
        "repeated_frames": repeats,
        "luma_change_between_frames": {"min": round(float(diffs.min()), 3), "median": round(float(np.median(diffs)), 3),
                                       "max": round(float(diffs.max()), 3)},
        "cuts_detected_at_s": [round(times[i + 1], 3) for i, d in enumerate(diffs) if d > 6 * np.median(diffs) and d > 12],
        "near_black_share": {"max": round(max(black), 4), "mean": round(float(np.mean(black)), 4),
                             "frames_over_15_percent": [i for i, b in enumerate(black) if b > 0.15]},
    }
    print(json.dumps(report, indent=1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--sheet")
    ap.add_argument("--timing", action="store_true")
    ap.add_argument("--every", type=float, default=0.5)
    ap.add_argument("--cols", type=int, default=6)
    ap.add_argument("--tile", type=int, default=640)
    args = ap.parse_args()
    info = probe(args.video)
    if args.sheet:
        sheet(args, info)
    if args.timing:
        timing(args, info)
    return 0


if __name__ == "__main__":
    sys.exit(main())
