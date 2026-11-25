#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Write ../manifest.json for the app previews: deliverables with SHA-256, spec and cadence
checks, the takes behind every segment (from capture_frames.py's take.json), build, tools
and sources.

    python3 make_manifest.py --renders DIR --raw RAW --cards CARDS --checks CHECK.json[,...] \
        --cadence CADENCE.json[,...] [--superseded DIR]
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--renders", required=True)
    ap.add_argument("--raw", required=True)
    ap.add_argument("--cards", required=True)
    ap.add_argument("--checks", required=True)
    ap.add_argument("--cadence", default="")
    ap.add_argument("--superseded", default="")
    ap.add_argument("--worktree", default=str(Path.home() / "glob2/glob2-wt-mobile-capture"))
    args = ap.parse_args()
    cfg = json.loads((HERE / "previews.json").read_text())
    checks = {}
    for c in args.checks.split(","):
        for r in json.loads(Path(c).read_text()):
            checks[r["file"]] = r
    cadence = {}
    for c in [c for c in args.cadence.split(",") if c]:
        for r in json.loads(Path(c).read_text()):
            cadence[r["file"]] = r
    wt = Path(args.worktree)
    commit = subprocess.run(["git", "-C", str(wt), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    app = wt / "build/ios/simulator/arm64/15.0/client/release/xcode-project/build/Release-iphonesimulator/Glob2.app"
    manifest = {
        "generated_by": "tools/make_manifest.py",
        "made": "2026-11-25",
        "version": 2,
        "what": "App Store app previews (iPhone 6.9-inch and iPad 13-inch, portrait), filmed frame by frame from "
                "the iOS app in the iOS Simulator: one game tick per frame at 30 fps, so the match plays at its "
                "normal speed; every frame is a simctl screenshot of the app",
        "footage_label": "Player view of a shared colony (You + Nicowar AI) against AI colonies; the colony was grown "
                         "by the co-controlling AI, the scripted touch inputs listed per take are the player's. "
                         "Not human-versus-human play.",
        "build": {
            "version": "0.11.8.0", "commit": commit, "public_release": False,
            "note": "origin/master release commit 5e96273ff62f plus two capture-only patches that never ship: "
                    "../captures/mobile/tools/capture-build.patch (compiles the loopback MCP automation listener into "
                    "the simulator build so scripts can tap the real touch controls) and tools/capture-frame-clock.patch "
                    "(the capture clock: while switched on over MCP, the match view draws two frames per tick that "
                    "runs and nothing in between, the presentation clocks advance 1/60 s per drawn frame, and the "
                    "'Paused' label an agent's hold would show is not drawn). Neither changes the simulation; with the "
                    "capture clock off the app behaves as the release",
            "app_executable_sha256": sha256(app / "Glob2") if (app / "Glob2").exists() else None,
            "renderer": "portable SDL renderer (the SDL GPU/Metal renderer devices use is not available in the Simulator)",
            "hd_artwork": "forced on (highResolutionArtworkChoice=on in the capture profile)",
        },
        "superseded": {
            "what": "Version 1 (2026-11-25): real-time simctl io recordVideo captures on a heavily loaded Mac; the "
                    "owner found hitches and stutters. Moved, not deleted.",
            "location": "../storefront-v2-renders/app-previews/superseded/",
            "files": {p.name: {"bytes": p.stat().st_size, "sha256": sha256(p)}
                      for p in sorted(Path(args.superseded).glob("*.mp4"))} if args.superseded else {},
        },
        "apple_spec": {
            "source": "https://developer.apple.com/help/app-store-connect/reference/app-preview-specifications "
                      "and https://developer.apple.com/app-store/app-previews/ (read 2026-11-25)",
            "iphone_6.9": "886x1920 portrait (or 1920x886)", "ipad_13": "1200x1600 portrait (or 1600x1200)",
            "length": "15-30 s", "frame_rate": "at most 30 fps", "max_size": "500 MB",
            "video": "H.264 up to High profile level 4.0, progressive, .mov/.m4v/.mp4, target 10-12 Mbps",
            "audio": "stereo AAC 256 kbps, 44.1 or 48 kHz, all tracks enabled",
        },
        "storage": "The MP4s are not committed (see .gitignore); they live in ../storefront-v2-renders/app-previews/ "
                   "relative to the repository root. Their bytes and SHA-256 here identify the exact files.",
        "deliverables": [],
        "takes": {},
        "cards": {c.stem[6:]: json.loads(c.read_text()) for c in sorted(Path(args.cards).glob("cards-*.json"))},
        "music": {"source": "content/data/zik/original/a2.opus (building) and a3.opus (combat), the game's original "
                            "soundtrack by Jacques-Paul Grivaz, GPL-3.0-or-later (as the trailer)"},
        "tools": {p.name: sha256(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.suffix in (".py", ".json")
                  and p.name != "make_manifest.py"} | {"make_manifest.py": sha256(HERE / "make_manifest.py")},
    }
    used = set()
    for device, cut in cfg["cuts"].items():
        mp4 = Path(args.renders) / f"{cut['file']}.mp4"
        poster = OUT / f"poster-{device}-{cfg['devices'][device]['size'][0]}x{cfg['devices'][device]['size'][1]}.png"
        entry = {"device": device, "file": mp4.name, "location": f"../storefront-v2-renders/app-previews/{mp4.name}",
                 "bytes": mp4.stat().st_size if mp4.exists() else None, "sha256": sha256(mp4) if mp4.exists() else None,
                 "duration_s": cut["duration"], "timeline": [], "text": cut["text"], "wordmark": cut.get("wordmark"),
                 "music_plan": cut["music"], "poster": dict(cut["poster"], file=poster.name,
                                                            sha256=sha256(poster) if poster.exists() else None),
                 "spec_check": checks.get(mp4.name), "cadence_check": cadence.get(mp4.name)}
        t = 0.0
        for s in cut["timeline"]:
            entry["timeline"].append(dict(s, start=round(t, 3), end=round(t + s["frames"] / 30, 3)))
            t += s["frames"] / 30
            used.add((device, s["take"]))
        manifest["deliverables"].append(entry)
    for device, take in sorted(used):
        side = json.loads((Path(args.raw) / device / take / "take.json").read_text())
        frames = side.pop("frame_log")
        ticks = [r["tick"] for r in frames]
        rows = [r["event_rows"] for r in frames if "event_rows" in r]
        side["frame_ticks"] = {"first": ticks[0], "last": ticks[-1],
                               "steps": sorted({b - a for a, b in zip(ticks, ticks[1:])}),
                               "note": "tick of every frame; a step above 1 is the declared cut of a skip input"}
        side["drawn_frames_per_filmed_frame"] = sorted({b["drawn_frame"] - a["drawn_frame"]
                                                        for a, b in zip(frames, frames[1:]) if b["tick"] - a["tick"] == 1})
        side["event_rows_range"] = [min(rows), max(rows)] if rows else None
        side["frames_sha256"] = hashlib.sha256("".join(
            sha256(Path(args.raw) / device / take / f"f{r['n']:05d}.png") for r in frames
            if not r.get("discarded")).encode()).hexdigest()
        side["frames_discarded"] = sum(1 for r in frames if r.get("discarded"))
        side["frames_note"] = ("PNG frames kept in the session scratch directory, not committed; frames_sha256 is the "
                               "SHA-256 of the concatenated per-frame SHA-256 hex digests in order")
        manifest["takes"][f"{device}/{take}"] = side
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n")
    print(OUT / "manifest.json")


if __name__ == "__main__":
    main()
