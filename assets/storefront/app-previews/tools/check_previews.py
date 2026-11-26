#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Check finished app previews against Apple's App Preview specification and make review sheets.

    uv run --with pillow --with numpy python check_previews.py FILE.mp4 [...] --device iphone-6.9|ipad-13 \
        [--sheets DIR] [--json OUT.json]

For each file: ffprobe facts (container, codec, profile, level, size, pixel format,
scan, frame rate, frame count, duration, bit rates, audio codec, channels, sample rate),
every frame's timestamp (constant 30 fps, no gaps or repeats of timestamps), EBU R128
loudness and true peak, and, for iPhone, that the status bar between the clock and
the status icons is plain status-bar colour (no Dynamic Island pill from the simulator)
in every sampled frame. Each check is pass or fail against
the values Apple publishes (App Store Connect Help, "App preview specifications",
read 2026-11-25): accepted resolution for the device class, 15-30 s, at most 30 fps,
H.264 up to High profile level 4.0, progressive, .mp4/.mov/.m4v, at most 500 MB,
stereo AAC 256 kbps at 44.1 or 48 kHz; video bit rate target 10-12 Mbps.

With --sheets it writes, per file, one frame per second at full size
(contact-<name>-full.jpg), at phone-thumbnail size (contact-<name>-thumb.jpg,
240 px wide: about the width a preview plays at in App Store search results), and
four frames per second at 160 px (contact-<name>-4fps.jpg, one row per 5 s).
"""
import argparse
import json
import re
import subprocess
from pathlib import Path

SPEC = {
    "iphone-6.9": {"sizes": [[886, 1920], [1920, 886]]},
    "ipad-13": {"sizes": [[1200, 1600], [1600, 1200]]},
}
ISLAND = {"x": 314, "y": 24, "w": 260, "h": 82}  # where the simulator would draw the island, in 886x1920 output pixels


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)],
                         check=True, capture_output=True, text=True).stdout
    return json.loads(out)


def frame_times(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "frame=pts_time",
                          "-of", "csv=p=0", str(path)], check=True, capture_output=True, text=True).stdout
    return [float(x) for x in out.split() if x.strip()]


def loudness(path):
    err = subprocess.run(["ffmpeg", "-nostats", "-i", str(path), "-map", "0:a", "-af", "ebur128=peak=true",
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    summary = err[err.rfind("Summary:"):]
    i = re.search(r"I:\s+(-?[\d.]+) LUFS", summary)
    tp = re.search(r"Peak:\s+(-?[\d.]+) dBFS", summary)
    return {"integrated_lufs": float(i.group(1)) if i else None, "true_peak_dbtp": float(tp.group(1)) if tp else None}


def island_check(path, duration):
    import numpy as np
    from PIL import Image
    import io
    worst = 0.0
    for t in [x + 0.5 for x in range(int(duration))]:
        png = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", str(path), "-frames:v", "1", "-f", "image2pipe",
                              "-vcodec", "png", "-"], check=True, capture_output=True).stdout
        a = np.asarray(Image.open(io.BytesIO(png)).convert("RGB")).astype(float)
        i = ISLAND
        box = a[i["y"] + 4:i["y"] + i["h"] - 4, i["x"] + 4:i["x"] + i["w"] - 4].reshape(-1, 3).mean(0)
        bar = np.concatenate([a[i["y"]:i["y"] + i["h"], i["x"] - 40:i["x"] - 8].reshape(-1, 3),
                              a[4:i["y"] - 6, i["x"]:i["x"] + i["w"]].reshape(-1, 3)]).mean(0)
        worst = max(worst, float(np.abs(box - bar).max()))
    return {"max_channel_difference_box_vs_bar": round(worst, 2), "pass": worst <= 3.0}


def sheets(path, out_dir, duration):
    name = Path(path).stem
    n = int(round(duration))
    cols = 5
    rows = -(-n // cols)
    full = out_dir / f"contact-{name}-full.jpg"
    thumb = out_dir / f"contact-{name}-thumb.jpg"
    # One frame per second, at 0.5 s, 1.5 s, ... (the middle of each second), left to right, top to bottom.
    sel = "select='" + "+".join(f"eq(n\\,{int(30 * (k + 0.5))})" for k in range(n)) + "'"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(path), "-vf",
                    f"{sel},tile={cols}x{rows}:padding=8:color=0x222222",
                    "-fps_mode", "vfr", "-frames:v", "1", "-q:v", "3", str(full)], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(path), "-vf",
                    f"{sel},scale=240:-1:flags=area,tile={min(n, 13)}x{-(-n // 13)}:padding=6:color=0x222222",
                    "-fps_mode", "vfr", "-frames:v", "1", "-q:v", "3", str(thumb)], check=True)
    # Four frames a second (frames 0, 7/8, 15, 22/23 of each second), one row of 20 per 5 s,
    # 160 px wide: every quarter second of the preview at a glance.
    quarter = out_dir / f"contact-{name}-4fps.jpg"
    nq = int(round(duration * 4))
    selq = "select='" + "+".join(f"eq(n\\,{int(round(k * 7.5))})" for k in range(nq)) + "'"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(path), "-vf",
                    f"{selq},scale=160:-1:flags=area,tile=20x{-(-nq // 20)}:padding=4:color=0x222222",
                    "-fps_mode", "vfr", "-frames:v", "1", "-q:v", "3", str(quarter)], check=True)
    return [full.name, thumb.name, quarter.name]


def check(path, device, sheet_dir):
    p = probe(path)
    v = next(s for s in p["streams"] if s["codec_type"] == "video")
    a = [s for s in p["streams"] if s["codec_type"] == "audio"]
    fmt = p["format"]
    dur = float(fmt["duration"])
    times = frame_times(path)
    steps = [round((b - a_) * 1000, 3) for a_, b in zip(times, times[1:])]
    size = [int(v["width"]), int(v["height"])]
    facts = {
        "file": Path(path).name, "bytes": int(fmt["size"]), "container": fmt["format_name"],
        "duration_s": round(dur, 3), "video": {k: v.get(k) for k in (
            "codec_name", "profile", "level", "width", "height", "pix_fmt", "field_order", "r_frame_rate",
            "avg_frame_rate", "nb_frames", "bit_rate", "color_primaries", "color_transfer", "color_space")},
        "audio": [{k: s.get(k) for k in ("codec_name", "profile", "channels", "channel_layout", "sample_rate", "bit_rate",
                                          "disposition")} for s in a],
        "frames": len(times), "frame_step_ms": sorted(set(steps)), **loudness(path),
    }
    checks = {
        "resolution": size in SPEC[device]["sizes"],
        "duration_15_30s": 15.0 <= dur <= 30.0,
        "frame_rate_30_constant": v["r_frame_rate"] == "30/1" and v["avg_frame_rate"] == "30/1"
                                  and all(abs(s - 33.333) < 0.01 for s in steps),
        "frame_count_matches_duration": abs(len(times) - dur * 30) <= 1,
        "codec_h264": v["codec_name"] == "h264",
        "profile_high_or_lower": v.get("profile") in ("High", "Main", "Constrained Baseline", "Baseline"),
        "level_at_most_4_0": int(v.get("level", 99)) <= 40,
        "progressive": v.get("field_order", "progressive") == "progressive",
        "pix_fmt_yuv420p": v.get("pix_fmt") == "yuv420p",
        "colour_tags_bt709": (v.get("color_primaries"), v.get("color_transfer"), v.get("color_space")) == ("bt709",) * 3,
        "container_mp4": Path(path).suffix in (".mp4", ".mov", ".m4v") and "mp4" in fmt["format_name"],
        "size_under_500MB": int(fmt["size"]) < 500 * 1024 * 1024,
        "video_bitrate_10_12_mbps": 10_000_000 <= int(v["bit_rate"]) <= 12_500_000,
        "audio_one_stereo_track": len(a) == 1 and a[0]["channels"] == 2,
        "audio_aac_256k": bool(a) and a[0]["codec_name"] == "aac" and 240_000 <= int(a[0]["bit_rate"]) <= 270_000,
        "audio_44_1_or_48_khz": bool(a) and a[0]["sample_rate"] in ("44100", "48000"),
        "audio_track_enabled": bool(a) and a[0].get("disposition", {}).get("default") == 1,
    }
    if device == "iphone-6.9":
        facts["status_bar_island_check"] = island_check(path, dur)
        checks["no_island_in_status_bar"] = facts["status_bar_island_check"]["pass"]
    if sheet_dir:
        facts["sheets"] = sheets(path, Path(sheet_dir), dur)
    facts["checks"] = checks
    facts["all_pass"] = all(checks.values())
    return facts


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--device", required=True, choices=sorted(SPEC))
    ap.add_argument("--sheets")
    ap.add_argument("--json")
    args = ap.parse_args()
    results = [check(f, args.device, args.sheets) for f in args.files]
    text = json.dumps(results, indent=1)
    if args.json:
        Path(args.json).write_text(text + "\n")
    for r in results:
        bad = [k for k, ok in r["checks"].items() if not ok]
        print(f"{r['file']}: {'PASS' if r['all_pass'] else 'FAIL ' + ', '.join(bad)}  "
              f"{r['video']['width']}x{r['video']['height']} {r['duration_s']} s {r['frames']} frames "
              f"{int(r['video']['bit_rate']) / 1e6:.2f} Mbps, {r['integrated_lufs']} LUFS, TP {r['true_peak_dbtp']}")


if __name__ == "__main__":
    main()
