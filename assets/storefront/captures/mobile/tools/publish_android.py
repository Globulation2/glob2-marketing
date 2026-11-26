#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Publish the Android emulator classes into captures/mobile/ without touching the other classes.

    GLOB2_SCRATCH=... GLOB2_WT=... uv run --with pillow python publish_android.py

Reads tools/picks-android.json ({"<class>": [{"role", "candidate", "description", ...}]},
gallery order hero, battle, fair_deal, build, economy, territory, maps), copies each
candidate byte for byte to ../<class>/NN-<role>-WxH.png, re-checks pixel size, sha256,
HD artwork and the clean-state protocol from the sidecar, replaces only these classes'
entries in ../manifest.json (files and classes) and writes their contact sheets.
selection.json is not touched.
"""
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import g2  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
MAPS = {
    "bigpond-n": {"name": "A big pond", "colonies": "You + Nicowar AI (red) vs Cortex AI (green), Cabino AI (blue)"},
    "foursquares-n": {"name": "FourSquares1", "colonies": "You + Nicowar AI (red) vs Nicowar AI, Cortex AI, Cabino AI"},
}
CLASSES = {
    "android-phone-emulator": {"orientation": "portrait", "replaces": "android-phone",
                               "stores": ["Google Play phone", "Amazon Appstore phone", "F-Droid phoneScreenshots"]},
    "android-tablet-7-emulator": {"orientation": "landscape", "replaces": "android-tablet-7",
                                  "stores": ["Google Play 7-inch tablet", "Amazon Fire 7/8"]},
    "android-tablet-10-emulator": {"orientation": "landscape", "replaces": "android-tablet-10",
                                   "stores": ["Google Play 10-inch tablet", "Amazon Fire 10/11 (1920x1200 and 2560x1600 landscape accepted)"]},
}
ROLES = ["hero", "battle", "fair_deal", "build", "economy", "territory", "maps"]


def git(*args):
    return subprocess.check_output(["git", "-C", str(g2.WT), *args], text=True).strip()


def main():
    picks = json.loads((Path(__file__).resolve().parent / "picks-android.json").read_text())
    commit = git("rev-parse", "HEAD")
    version = (g2.WT / "buildsys/build_layout.py").read_text().split('PACKAGE_VERSION = "', 1)[1].split('"', 1)[0]
    manifest = json.loads((ROOT / "manifest.json").read_text())
    manifest["files"] = [f for f in manifest["files"] if f["device_class"] not in picks]
    manifest["build"]["android_emulator"] = (
        f"Android release APK {version} from origin/master commit {commit[:12]} (platforms/mobile/android.py build "
        "--arch arm64-v8a --release, then sign with the local developer key), plus tools/capture-build.patch "
        "(capture-only MCP listener; no rendering, HUD or simulation change), run in the pinned Android emulator "
        "(platforms/mobile/emulator.json: emulator 37.1.11, Android 15 API 35 arm64-v8a default image) with "
        "host GPU rendering (-gpu host)")
    for device_class, spec in CLASSES.items():
        if device_class not in picks:
            continue
        manifest["classes"][device_class] = {k: v for k, v in spec.items()}
        slots = picks[device_class]
        roles = [p["role"] for p in slots]
        if roles != [r for r in ROLES if r in roles]:
            raise SystemExit(f"{device_class}: slots {roles} are not in gallery order")
        directory = ROOT / device_class
        directory.mkdir(exist_ok=True)
        for old in directory.glob("*.png"):
            old.unlink()
        for number, pick in enumerate(slots, 1):
            source = g2.SCRATCH / "candidates2" / device_class / pick["candidate"]
            meta = json.loads(source.with_suffix(".json").read_text())
            with Image.open(source) as image:
                size = image.size
            if list(size) != meta["pixels"]:
                raise SystemExit(f"{source}: {size} is not the device size {meta['pixels']}")
            if not str(meta.get("hd_artwork", "")).startswith("on"):
                raise SystemExit(f"{source}: captured without HD artwork forced on")
            target = directory / f"{number:02d}-{pick['role']}-{size[0]}x{size[1]}.png"
            shutil.copyfile(source, target)
            digest = hashlib.sha256(target.read_bytes()).hexdigest()
            if digest != meta["sha256"]:
                raise SystemExit(f"{source}: changed since capture")
            shown = pick.get("rows_in_frame", len(meta["event_rows"]))
            problems = []
            if shown > 2:
                problems.append(f"{shown} event rows")
            if meta["zone_outline_pixels"]:
                problems.append("zone squares")
            if str(meta["first_stat"]).startswith("-"):
                problems.append("negative first stat")
            if meta["paused"] or meta["speed"] != "1x":
                problems.append("not live at 1x")
            if problems:
                raise SystemExit(f"{source}: " + ", ".join(problems))
            scenario = meta["save"].rsplit("-t", 1)[0]
            android = meta.get("android", {})
            record = {
                "file": f"{device_class}/{target.name}",
                "device_class": device_class,
                "slot": number,
                "role": pick["role"],
                "orientation": meta["orientation"],
                "pixels": f"{size[0]}x{size[1]}",
                "description": pick["description"],
                "kind": "gameplay",
                "build": "android-emulator",
                "build_version": version,
                "build_commit": commit,
                "device": meta["device"],
                "emulator": {"avd": android.get("avd"), "android_version": android.get("android"),
                             "api": android.get("api"), "system_image": android.get("fingerprint"),
                             "display": android.get("wm_size"), "density": android.get("wm_density"),
                             "gpu": "host (-gpu host, Apple GPU through the emulator's gfxstream)"},
                "capture_method": meta["method"],
                "real_device_capture": False,
                "emulator_capture": True,
                "interim": None,
                "hd_artwork": meta["hd_artwork"],
                "sha256": digest,
                "map": MAPS.get(scenario, {}).get("name", scenario),
                "colonies": MAPS.get(scenario, {}).get("colonies", ""),
                "save": f"saves/{meta['save']}.game.gz",
                "tick": meta["tick"],
                "game_speed": meta["speed"],
                "paused": meta["paused"],
                "camera": meta["camera"],
                "view": "player view (local human player; colony co-controlled by the Nicowar AI through the "
                        "lobby's You + AI option); not a spectator view",
                "event_rows_in_frame": shown,
                "event_rows": meta["event_rows"],
                "first_stat": meta["first_stat"],
                "zone_outline_pixels": meta["zone_outline_pixels"],
                "fog_dimmed_fraction": meta.get("fog_dimmed_fraction"),
                "player_actions_before_capture": meta["actions"] + (pick.get("extra_actions") or []),
            }
            for key in ("selected", "also_in_view", "buildings_in_view", "rival_units_in_view_by_team",
                        "enemy_buildings_near", "flag_placed_at"):
                if key in meta:
                    record[key] = meta[key]
            if pick.get("note"):
                record["note"] = pick["note"]
            manifest["files"].append(record)
        subprocess.run([sys.executable, str(Path(__file__).resolve().parent / "contact_sheet.py"), str(directory)],
                       check=True)
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
    print(sum(f["device_class"] in CLASSES for f in manifest["files"]), "emulator files")


if __name__ == "__main__":
    main()
