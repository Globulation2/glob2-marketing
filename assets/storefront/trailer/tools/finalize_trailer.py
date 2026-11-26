#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Write the trailer's manifest.json: deliverables, shots, edit, music, build.

usage: finalize_trailer.py OUT_DIR --raw RAW_DIR [--data trailer.json] [--transcript RAW/f-coplay/mcp-transcript.json]

For every MP4/WebM/PNG/JPG in OUT_DIR: SHA-256, size and (for video) the ffprobe facts a
store checks (codec, profile, size, frame rate, pixel format, audio, duration), whether
the moov atom precedes mdat (fast start, MP4 only), and the audio's integrated
loudness and true peak (ffmpeg ebur128, peak=true). For every shot the cuts use: the
capture sidecar (match, checkpoint, seat, ticks, camera, the seat's inputs) and a
tick-continuity check (each frame is exactly one simulation tick after the one
before, except where the take declares a skip).
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def faststart(path):
    """True when the moov box comes before mdat at the top level."""
    with open(path, "rb") as fh:
        pos = 0
        while True:
            fh.seek(pos)
            head = fh.read(16)
            if len(head) < 8:
                return None
            size = int.from_bytes(head[:4], "big")
            kind = head[4:8].decode("latin-1")
            if size == 1:
                size = int.from_bytes(head[8:16], "big")
            if kind == "moov":
                return True
            if kind == "mdat":
                return False
            if size < 8:
                return None
            pos += size


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
                         capture_output=True, text=True, check=True).stdout
    info = json.loads(out)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    a = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    res = {"duration_s": round(float(info["format"]["duration"]), 3), "video": {
        "codec": v["codec_name"], "profile": v.get("profile"), "level": v.get("level"), "width": v["width"],
        "height": v["height"], "frame_rate": v["r_frame_rate"], "avg_frame_rate": v["avg_frame_rate"],
        "frames": int(v.get("nb_frames", 0)), "pix_fmt": v["pix_fmt"], "color_space": v.get("color_space"),
        "bit_rate": int(v.get("bit_rate", 0))}}
    if a:
        res["audio"] = {"codec": a["codec_name"], "profile": a.get("profile"), "channels": a["channels"],
                        "channel_layout": a.get("channel_layout"), "sample_rate": int(a["sample_rate"]),
                        "bit_rate": int(a.get("bit_rate", 0))}
    res["fast_start"] = faststart(path) if path.suffix.lower() == ".mp4" else None
    if a:
        res["audio_loudness"] = loudness(path)
    return res


def loudness(path):
    """Integrated loudness (LUFS) and true peak (dBTP) of the file's audio."""
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-map", "0:a:0",
                          "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    summary = err[err.rfind("Summary:"):]
    i = re.search(r"I:\s+(-?[\d.]+) LUFS", summary)
    tp = re.search(r"True peak:\s+Peak:\s+(-?[\d.]+|-inf) dBFS", summary)
    return {"integrated_lufs": float(i.group(1)) if i else None,
            "true_peak_dbtp": float(tp.group(1)) if tp else None}


def shot_record(raw, shot_id):
    side = json.loads((raw / shot_id / "shot.json").read_text())
    ticks = side.get("frame_ticks") or []
    skips = [a for a in side["shot"].get("actions", []) if "skip_ticks" in a]
    jumps = [(i, ticks[i] - ticks[i - 1]) for i in range(1, len(ticks)) if ticks[i] - ticks[i - 1] != 1]
    declared = {a["frame"] for a in skips}
    rec = {k: side[k] for k in ("id", "frames", "first_tick", "last_tick", "speed", "ticks_per_second", "source_save",
                                 "source_save_sha256", "seat", "camera", "map", "window", "ui_scale", "erase_zones",
                                 "health_food_bars") if k in side}
    rec["match"] = side["shot"]["match"]
    rec["checkpoint"] = side["shot"]["checkpoint"]
    rec["team"] = side["shot"]["team"]
    rec["seat_inputs"] = side.get("inputs", [])
    rec["tick_continuity"] = {
        "every_frame_one_tick": not [j for j in jumps if j[0] not in declared],
        "declared_cuts_inside_take": [{"at_frame": i, "ticks_skipped": d - 1} for i, d in jumps if i in declared],
        "undeclared_jumps": [{"at_frame": i, "ticks": d} for i, d in jumps if i not in declared]}
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--raw", required=True)
    ap.add_argument("--data", default=str(HERE / "trailer.json"))
    ap.add_argument("--cards", help="render_cards.py output dir (its cards.json is folded in)")
    ap.add_argument("--extra", help="JSON file merged into the manifest (build, capture conditions, labels)")
    ap.add_argument("--timing", help="directory of review.py --timing reports named timing-<video>.json")
    ap.add_argument("--hud-check", help="check_hud.py report")
    ap.add_argument("--work", help="build_trailer.py work dir (its *-inset.json: the Hive card's top edge per frame)")
    args = ap.parse_args()
    out, raw = Path(args.out), Path(args.raw)
    data = json.loads(Path(args.data).read_text())
    manifest = json.loads(Path(args.extra).read_text()) if args.extra else {}
    files = []
    for p in sorted(out.rglob("*")):
        if p.is_file() and p.suffix.lower() in (".mp4", ".webm", ".png", ".jpg") and "tools" not in p.parts:
            rec = {"file": str(p.relative_to(out)), "bytes": p.stat().st_size, "sha256": sha256(p)}
            if p.suffix.lower() in (".mp4", ".webm"):
                rec.update(probe(p))
            files.append(rec)
    manifest["deliverables"] = files
    used = []
    sys.path.insert(0, str(HERE))
    from build_trailer import expand
    for name in data["cuts"]:
        for seg in expand(data, name).get("timeline", []):
            if seg["shot"] not in used:
                used.append(seg["shot"])
    manifest["shots"] = [shot_record(raw, s) for s in used]
    for shot in used:
        tr = raw / shot / "mcp-transcript.json"
        if tr.exists():
            manifest.setdefault("mcp_transcripts", {})[shot] = json.loads(tr.read_text())
    if args.timing:
        manifest["review_timing"] = {p.stem.replace("timing-", ""): json.loads(p.read_text())
                                     for p in sorted(Path(args.timing).glob("timing-*.json"))}
    if args.hud_check:
        manifest["review_hud_check"] = json.loads(Path(args.hud_check).read_text())
    manifest["edit"] = data
    insets = {p.name: json.loads(p.read_text()) for p in sorted(Path(args.work).glob("*-inset.json"))} if args.work else {}
    if insets:
        manifest["inset_card_tops"] = insets
    if args.cards:
        cj = json.loads((Path(args.cards) / "cards.json").read_text())
        manifest["text_cards"] = cj
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    bad = [s["id"] for s in manifest["shots"] if not s["tick_continuity"]["every_frame_one_tick"]]
    print(f"{out / 'manifest.json'}: {len(files)} files, {len(manifest['shots'])} shots" +
          (f"; tick gaps in {bad}" if bad else "; every shot one tick per frame"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
