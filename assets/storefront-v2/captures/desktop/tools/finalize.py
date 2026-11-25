#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Copy chosen candidate frames into the capture directory and write its manifest.

usage: uv run --with pillow python finalize.py SELECTION.json OUT_DIR \
           --candidates DIR [--candidates DIR ...] [--extra EXTRA.json]

SELECTION.json: [{"candidate": "<recipe id or id+n>", "description": "one honest line"} ...]
Every candidate directory is searched for "<candidate>-<W>x<H>.png" and its JSON
sidecar (written by capture.py); each match is copied unchanged (byte-identical)
to OUT_DIR. EXTRA.json holds ready-made manifest entries (key-art plates).
Writes OUT_DIR/manifest.json and OUT_DIR/contact-sheet.jpg (the 16:9 frames).
"""
import argparse
import glob
import hashlib
import json
import os
import platform
import shutil
import subprocess

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
APP = "/Applications/Glob2.app/Contents/MacOS/glob2"
AI_NAMES = {"maxima": "Maxima (Hard)", "cabino": "Cabino (Medium)", "nicowar": "Nicowar (Medium)",
            "cortex": "Cortex (Medium)", "castor": "Castor (Easy)", "numbi": "Numbi (Easy)"}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def build_info():
    out = subprocess.run([APP, "info", "version"], capture_output=True, text=True).stdout
    info = dict(line.split(": ", 1) for line in out.splitlines() if ": " in line)
    return {
        "version": info.get("version"),
        "revision": info.get("revision"),
        "save_version": info.get("save_version"),
        "executable": APP,
        "executable_sha256": sha256(APP),
        "public_release": "0.11.7.0, the installed release named in the capture brief",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("selection")
    ap.add_argument("out")
    ap.add_argument("--candidates", action="append", required=True)
    ap.add_argument("--extra")
    args = ap.parse_args()
    matches = json.load(open(os.path.join(HERE, "matches.json")))
    selection = json.load(open(args.selection))
    files = []
    sheet = []
    for entry in selection:
        found = []
        for d in args.candidates:
            found += glob.glob(os.path.join(d, entry["candidate"] + "-*x*.png"))
        if not found:
            raise SystemExit(f"no candidate file for {entry['candidate']}")
        for src in sorted(found):
            side = json.load(open(src[:-4] + ".json"))
            recipe = side["recipe"]
            name = os.path.basename(src)
            if entry.get("rename"):
                name = name.replace(entry["candidate"], entry["rename"])
            dst = os.path.join(args.out, name)
            shutil.copyfile(src, dst)
            match = matches[recipe["match"]]
            with Image.open(dst) as im:
                size = list(im.size)
            spectator = bool(recipe.get("spectator"))
            team = recipe["team"]
            steps = recipe.get("steps", [])
            item = {
                "file": name,
                "shot": recipe["shot"],
                "description": entry["description"],
                "window_pixels": size,
                "aspect": "16:9" if abs(size[0] / size[1] - 16 / 9) < 0.01 else "16:10",
                "match": recipe["match"],
                "map": match["map"],
                "game_seed": match["game_seed"],
                "players": [{"team": i, "controller": "AI " + AI_NAMES.get(ai, ai)}
                            for i, ai in enumerate(match["ais_by_team"])],
                "seat": ("spectator view: every colony is played by an AI, fog of war off, "
                         "Statistics tab shown instead of the spectator options") if spectator else
                        (f"player seat on colony {team}: a local human player record added to the save, "
                         f"sharing the colony with its AI ({AI_NAMES.get(match['ais_by_team'][team])}); "
                         "normal player interface and fog of war"),
                "source_save": f"matches/{recipe['match']}/checkpoint-{recipe['tick']}.game.gz",
                "source_save_sha256": side.get("source_save_sha256"),
                "source_save_tick": recipe["tick"],
                "tick_at_capture": side["tick_at_capture"],
                "camera": side.get("camera") or {"centre_tile": [recipe["view"]["x"], recipe["view"]["y"]],
                                                 "zoom": recipe["view"].get("zoom", 1.0)},
                "player_actions_before_capture":
                    (["erased the colony's forbidden and clearing area markings (Flags and areas)"]
                     if recipe.get("erase_zones") else []) + [json.dumps(s) for s in steps],
                "recipe_id": recipe["id"],
                "hd_artwork": side.get("hd_artwork"),
                "sha256": sha256(dst),
            }
            files.append(item)
            if item["aspect"] == "16:9":
                sheet.append((dst, name))
    if args.extra:
        files += json.load(open(args.extra))
    manifest = {
        "schema_version": 1,
        "captured": "2026-11-24",
        "kind": "native desktop gameplay captures for storefront-v2",
        "build": build_info(),
        "platform": {"os": "macOS " + platform.mac_ver()[0], "machine": platform.machine(),
                     "note": "macOS desktop build; the same renderer and artwork ship on Windows and Linux"},
        "capture_method": {
            "summary": "Released game run off-screen (SDL dummy video driver) with its portable-sdl renderer "
                       "at UI scale 2, driven and captured through its embedded MCP UI server "
                       "(game_view to frame, ui_screenshot for the PNG of the next rendered frame).",
            "launch": "tools/launch-capture-game.sh PROFILE 3840x2160 2 47811 (2880x1800 for the 16:10 set)",
            "pixels": "native: the PNG is the game's own framebuffer, never scaled, cropped or retouched",
            "ui_scale": 2,
            "equivalent_window": {"3840x2160": "1920x1080 points on a 2x display",
                                  "2880x1800": "1440x900 points on a 2x (Retina) display"},
            "artwork": "HD artwork layers (HD sprite policy: density 2 at 100% zoom), forced on with "
                       "highResolutionArtworkChoice=on; each session's log was checked for an artwork step-down",
            "graphics_settings": {"artwork": "High resolution (explicit)", "clouds": False,
                                  "cloud_shadows": False, "everything_else": "defaults"},
            "aspect_16_10": "captured in a 2880x1800 window with every recipe zoom multiplied by 0.75 (heroes "
                            "0.86) and snapped to 1/8, to keep the framing; not a crop of the 16:9 frame",
            "match_speed": "normal (1x) for at least the 20 seconds before each capture; never paused",
            "matches": "headless `glob2 game run` AI matches (tools/run-match.sh, tools/matches.json)",
            "player_seat": "tools/join-seat.py adds a local player to one colony of a headless save",
        },
        "files": files,
    }
    with open(os.path.join(args.out, "manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=1)
        fh.write("\n")

    # contact sheet of the 16:9 frames
    cols, tw = 3, 960
    th = tw * 9 // 16
    rows = (len(sheet) + cols - 1) // cols
    canvas = Image.new("RGB", (cols * tw, rows * (th + 34)), (16, 12, 24))
    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 20)
    except OSError:
        font = ImageFont.load_default()
    for n, (path, name) in enumerate(sheet):
        with Image.open(path) as im:
            thumb = im.convert("RGB").resize((tw, th), Image.LANCZOS)
        x, y = (n % cols) * tw, (n // cols) * (th + 34)
        canvas.paste(thumb, (x, y + 34))
        draw.text((x + 8, y + 6), name, fill=(249, 232, 187), font=font)
    canvas.save(os.path.join(args.out, "contact-sheet.jpg"), quality=88)
    print(f"{len(files)} files in manifest, {len(sheet)} on the contact sheet")


if __name__ == "__main__":
    main()
