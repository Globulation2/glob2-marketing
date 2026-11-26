#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Copy the chosen candidates into captures/mobile/<device-class>/ and write the indexes.

    GLOB2_SCRATCH=... uv run --with pillow python publish.py

Reads tools/picks.json:
  {"<device-class>": [{"role": "hero", "candidate": "hero-hd45-2.png", "description": "..."}, ...]}
in gallery slot order (hero, battle, fair_deal, build, economy, territory, maps;
the order of asset_text.mobile_gallery_order in translations/platforms.json since
the round 2 review, 2026-11-24, which also dropped the opponents menu slide).
Candidates and their JSON sidecars come from capture.py
(SCRATCH/candidates2/<device-class>/). Files are copied byte for byte (never
re-encoded, scaled or cropped) to NN-<role>-WxH.png and their pixel size and
sha256 are checked against the sidecar; the clean-state protocol and the HD
artwork setting are checked again from the sidecar. Writes:
  ../manifest.json   provenance of every file (build, device, map, save, tick,
                     camera, event rows, first stat, zone check, HD artwork,
                     player actions)
  ../selection.json  {"<device class>": [{"capture": "<file name>", "role": "<role>"}, ...]}
  ../<class>/contact-sheet.jpg
fdroid-phone has no files of its own: the manifest points it at android-phone.
Only the files named in picks.json stay in the class folders and only the
saves they came from stay in ../saves.
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
    "iphone-6.9": {"orientation": "portrait", "stores": ["App Store (iPhone 6.9-inch)"]},
    "ipad-13": {"orientation": "portrait", "stores": ["App Store (iPad 13-inch)"]},
    "android-phone": {"orientation": "portrait", "stores": ["Google Play phone", "Amazon Appstore phone", "F-Droid phoneScreenshots"]},
    "android-tablet-7": {"orientation": "landscape", "stores": ["Google Play 7-inch tablet", "Amazon Fire 7/8"]},
    "android-tablet-10": {"orientation": "landscape", "stores": ["Google Play 10-inch tablet", "Amazon Fire 10/11"]},
}
# Slot order of every class; must match asset_text.mobile_gallery_order in translations/platforms.json.
ROLES = ["hero", "battle", "fair_deal", "build", "economy", "territory", "maps"]
INTERIM = ("Interim: a host render of the shared touch interface at this Android pixel size and density, "
           "not an emulator or device screenshot. Replace when an Android toolchain is available.")


def git(*args):
    return subprocess.check_output(["git", "-C", str(g2.WT), *args], text=True).strip()


def main():
    picks = json.loads((Path(__file__).resolve().parent / "picks.json").read_text())
    build = {
        "version": "0.11.8.0",
        "commit": git("rev-parse", "HEAD"),
        "worktree_changes": "tools/capture-build.patch (capture-only: lets the iOS Simulator build expose the "
                            "loopback MCP automation listener; no rendering, HUD or simulation change)",
        "ios": "iOS Simulator release build (platforms/mobile/ios.py build --environment simulator --release), "
               "portable SDL renderer",
        "host": "macOS desktop release build of the same commit (tools/dev_build.py release=1), SDL dummy video "
                "driver, game software renderer, --interface touch --ui-scale <density>",
    }
    manifest = {"generated_by": "captures/mobile/tools/publish.py", "round": 2, "build": build,
                "hd_artwork": "HD artwork was active in every file. Files marked 'on (highResolutionArtworkChoice=on ...)' "
                              "were captured with the setting forced on in the capture profile, so the session "
                              "step-down that turns Auto HD artwork off after frame hitches or memory pressure could "
                              "not apply. Files marked 'on (Auto ...)' are iOS Simulator frames from sessions whose "
                              "simulator log was checked: the device profile resolved Auto to HD and no step-down "
                              "event was logged.",
                "slot_order": ROLES, "classes": CLASSES,
                "aliases": {"fdroid-phone": "android-phone"}, "files": []}
    selection = {}
    shutil.rmtree(ROOT / "fdroid-phone", ignore_errors=True)
    saves = set()
    for device_class in CLASSES:
        slots = picks[device_class]
        roles = [pick["role"] for pick in slots]
        if roles != [role for role in ROLES if role in roles]:
            raise SystemExit(f"{device_class}: slots {roles} are not in gallery order")
        directory = ROOT / device_class
        directory.mkdir(exist_ok=True)
        for old in directory.glob("*.png"):
            old.unlink()
        selection[device_class] = []
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
            menu = bool(meta.get("menu"))
            if not menu:
                # The clean-state protocol, checked again from the sidecar.
                limit = 2  # the clean-state protocol: at most two event rows in every frame
                problems = []
                # Older sidecars list the union of the rows before and after the
                # frame, which overcounts when a counter ticks ("x18" then "x19");
                # picks.json then gives the number of rows visible in the frame.
                shown = pick.get("rows_in_frame", len(meta["event_rows"]))
                if shown > limit:
                    problems.append(f"{shown} event rows (limit {limit})")
                if meta["zone_outline_pixels"]:
                    problems.append("zone squares")
                if str(meta["first_stat"]).startswith("-"):
                    problems.append("negative first stat")
                if meta["paused"] or meta["speed"] != "1x":
                    problems.append("not live at 1x")
                if problems:
                    raise SystemExit(f"{source}: " + ", ".join(problems))
            host = "simulator" not in meta["device"]
            scenario = (meta["save"] or "").rsplit("-t", 1)[0]
            record = {
                "file": f"{device_class}/{target.name}",
                "device_class": device_class,
                "slot": number,
                "role": pick["role"],
                "orientation": meta["orientation"],
                "pixels": f"{size[0]}x{size[1]}",
                "description": pick["description"],
                "kind": "menu screen" if menu else "gameplay",
                "build": "host" if host else "ios",
                "device": meta["device"],
                "capture_method": meta["method"],
                "real_device_capture": False,
                "interim": INTERIM if host else None,
                "hd_artwork": meta["hd_artwork"],
                "sha256": digest,
            }
            if not menu:
                saves.add(meta["save"])
                record.update({
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
                    "player_actions_before_capture": meta["actions"],
                })
                for key in ("selected", "also_in_view", "buildings_in_view", "rival_units_in_view_by_team", "spot"):
                    if key in meta:
                        record[key] = meta[key]
            if pick.get("note"):
                record["note"] = pick["note"]
            manifest["files"].append(record)
            selection[device_class].append({"capture": target.name, "role": pick["role"]})
        subprocess.run([sys.executable, str(Path(__file__).resolve().parent / "contact_sheet.py"), str(directory)],
                       check=True)
    # Keep only the saves the published frames came from, with their lobby
    # setup and fast-forward telemetry.
    store = ROOT / "saves"
    store.mkdir(exist_ok=True)
    scenarios = {save.rsplit("-t", 1)[0] for save in saves}
    wanted = {f"{save}.game.gz" for save in saves}
    wanted |= {f"{scenario}{suffix}" for scenario in scenarios for suffix in (".lobby.txt", ".telemetry.jsonl")}
    for old in store.iterdir():
        if old.name not in wanted:
            old.unlink()
    for name in sorted(wanted):
        if (g2.SAVES / name).exists():
            shutil.copyfile(g2.SAVES / name, store / name)
        elif not (store / name).exists():
            raise SystemExit(f"missing {name}")
    manifest["saves"] = sorted(f"saves/{name}" for name in wanted)
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
    (ROOT / "selection.json").write_text(json.dumps(selection, indent=1) + "\n")
    print(len(manifest["files"]), "files")


if __name__ == "__main__":
    main()
