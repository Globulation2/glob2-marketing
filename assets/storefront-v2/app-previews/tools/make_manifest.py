#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Write ../manifest.json for the app previews: deliverables with SHA-256 and spec checks,
the takes behind every segment (from record.py's sidecars), build, tools and sources.

    python3 make_manifest.py --renders DIR --raw RAW --cards CARDS --checks CHECK.json[,...]
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
    ap.add_argument("--worktree", default=str(Path.home() / "glob2/glob2-wt-mobile-capture"))
    args = ap.parse_args()
    cfg = json.loads((HERE / "previews.json").read_text())
    checks = {}
    for c in args.checks.split(","):
        for r in json.loads(Path(c).read_text()):
            checks[r["file"]] = r
    wt = Path(args.worktree)
    commit = subprocess.run(["git", "-C", str(wt), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    app = wt / "build/ios/simulator/arm64/15.0/client/release/xcode-project/build/Release-iphonesimulator/Glob2.app"
    manifest = {
        "generated_by": "tools/make_manifest.py",
        "made": "2026-11-25",
        "what": "App Store app previews (iPhone 6.9-inch and iPad 13-inch, portrait), recorded from the iOS app "
                "in the iOS Simulator during live play at normal speed",
        "footage_label": "Player view of a shared colony (You + Nicowar AI) against AI colonies; the colony was grown "
                         "by the co-controlling AI, the scripted touch inputs listed per take are the player's. "
                         "Not human-versus-human play.",
        "build": {
            "version": "0.11.8.0", "commit": commit, "public_release": False,
            "note": "origin/master release commit 5e96273ff62f plus the capture-only patch "
                    "(../captures/mobile/tools/capture-build.patch) that compiles the loopback MCP automation listener "
                    "into the simulator build so scripts can tap the real touch controls; it changes no rendering, HUD "
                    "or simulation code and never ships",
            "app_executable_sha256": sha256(app / "Glob2") if (app / "Glob2").exists() else None,
            "renderer": "portable SDL renderer (the SDL GPU/Metal renderer devices use is not available in the Simulator)",
            "hd_artwork": "forced on (highResolutionArtworkChoice=on in the capture profile)",
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
                 "spec_check": checks.get(mp4.name)}
        t = 0.0
        for s in cut["timeline"]:
            entry["timeline"].append(dict(s, start=round(t, 3), end=round(t + s["seconds"], 3)))
            t += s["seconds"]
            used.add((device, s["take"]))
        manifest["deliverables"].append(entry)
    for device, take in sorted(used):
        side = json.loads((Path(args.raw) / device / f"{take}.json").read_text())
        mov = Path(args.raw) / device / f"{take}.mov"
        samples = [s for s in side["samples"] if "tick" in s]
        side["raw_movie"] = {"file": mov.name, "bytes": mov.stat().st_size, "sha256": sha256(mov),
                             "note": "kept in the session scratch directory, not committed"}
        side["event_rows_range"] = [min(s["event_rows"] for s in samples), max(s["event_rows"] for s in samples)]
        side["ticks_per_second_min"] = min(round((b["tick"] - a["tick"]) / (b["t"] - a["t"]), 1)
                                           for a, b in zip(samples, samples[1:]) if b["t"] - a["t"] > 0.3)
        side["samples"] = [{"t": s["t"], "tick": s["tick"], "event_rows": s["event_rows"]} for s in samples]
        manifest["takes"][f"{device}/{take}"] = side
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n")
    print(OUT / "manifest.json")


if __name__ == "__main__":
    main()
