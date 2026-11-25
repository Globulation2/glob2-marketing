#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Round-2/3 finalizer: copy the chosen frames, write manifest.json, selection.json
and contact-sheet.jpg.

usage: uv run --with pillow python finalize2.py FINAL.json OUT_DIR [KEYART_ENTRIES.json]

$SCRATCH in FINAL.json source paths is expanded from the environment.

FINAL.json: [{"role", "name", "files": {"3840x2160": SRC, "2880x1800": SRC}, "description",
              "caption_check", "map", "match", "seat", "kind", "notes"}]
Each SRC is a native frame with its JSON sidecar next to it (scene.py, spectator.py,
build-shot.py) or, for the side-by-side, the composed image with a sidecar.
Frames are copied byte for byte. The first 16:9 file of each role, in order, goes
into selection.json, unless the entry says "gallery": false (an alternate, such as
the side-by-side co-play image). Each selection entry names its position, role,
the caption field of that role (shot_caption_<role>), its 16:10 twin and its
1920x1080 web export, so a store packager pairs every image with its own role's
caption whatever the order. An entry's "transcript" (a coplay-session.py JSON
Lines file) is copied into coplay-transcripts/ next to the frames.
"""
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
APP = "/Applications/Glob2.app/Contents/MacOS/glob2"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def build_info():
    out = subprocess.run([APP, "info", "version"], capture_output=True, text=True).stdout
    info = dict(line.split(": ", 1) for line in out.splitlines() if ": " in line)
    return {"version": info.get("version"), "revision": info.get("revision"),
            "save_version": info.get("save_version"), "executable": APP,
            "executable_sha256": sha256(APP)}


def main():
    final = json.load(open(sys.argv[1]))
    out = sys.argv[2]
    matches = json.load(open(os.path.join(HERE, "matches.json")))
    files, selection, sheet = [], [], []
    for entry in final:
        for size, src in entry["files"].items():
            name = f"{entry['name']}-{size}.png"
            dst = os.path.join(out, name)
            src = os.path.expandvars(src)
            shutil.copyfile(src, dst)
            side_path = src[:-4] + ".json"
            side = json.load(open(side_path)) if os.path.exists(side_path) else {}
            with Image.open(dst) as im:
                px = list(im.size)
            m = matches.get(entry.get("match"), {})
            item = {
                "file": name,
                "role": entry["role"],
                "kind": entry.get("kind", "gameplay frame (player seat)"),
                "description": entry["description"],
                "caption_check": entry.get("caption_check"),
                "window_pixels": px,
                "aspect": "16:9" if abs(px[0] / px[1] - 16 / 9) < 0.01 else "16:10",
                "map": entry.get("map"),
                "match": entry.get("match"),
                "game_seed": m.get("game_seed"),
                "ais_by_team": m.get("ais_by_team"),
                "seat": entry.get("seat"),
                "source_save": (f"matches/{entry['match']}/checkpoint-{side.get('source_tick')}.game.gz"
                                if side.get("source_tick") is not None else None),
                "tick_at_capture": side.get("tick_at_capture"),
                "camera": side.get("camera") or ({"centre_tile": side.get("camera_centre_tile"), "zoom": side.get("zoom")}
                                                 if side.get("camera_centre_tile") else None),
                "colony_status_at_capture": side.get("colony_status"),
                "hud_check": side.get("hud"),
                "zone_outline_share_per_10000": side.get("zone_outline_share_per_10000"),
                "fog_of_war_in_view": side.get("fog_of_war_in_view"),
                "player_actions_before_capture": side.get("player_actions_before_capture"),
                "notes": entry.get("notes"),
                "sha256": sha256(dst),
            }
            if "agent_flag" in side:  # coplay-session.py sidecar
                item["coplay_session"] = {k: side.get(k) for k in (
                    "inspect_observation_tick", "transcript_calls", "agent_flag", "hive_card", "hive_card_after_shot",
                    "warflags_before_shot", "warflags_after_shot", "other_warflags_in_colony", "checks", "attempts")
                    if k in side}
            if entry.get("extra"):
                item.update(entry["extra"])
            files.append(item)
            if item["aspect"] == "16:9":
                in_gallery = entry.get("gallery", True) and not any(s["role"] == entry["role"] for s in selection)
                pos = len(selection) + 1 if in_gallery else None
                sheet.append((dst, (f"{pos}. " if pos else "alternate: ") + f"{entry['role']}  {name}"))
                if in_gallery:
                    twin = [f"{entry['name']}-{k}.png" for k in entry["files"] if k != size]
                    selection.append({"capture": name, "role": entry["role"], "position": pos,
                                      "caption_field": f"shot_caption_{entry['role']}",
                                      "capture_16_10": twin[0] if twin else None,
                                      "web_1920": f"web-1920/{entry['name']}-1920x1080.jpg"})
        for size, tsrc in (entry.get("transcripts") or {}).items():
            tdir = os.path.join(out, "coplay-transcripts")
            os.makedirs(tdir, exist_ok=True)
            tname = f"{entry['name']}-{size}.jsonl"
            shutil.copyfile(os.path.expandvars(tsrc), os.path.join(tdir, tname))
            for item in files:
                if item["file"] == f"{entry['name']}-{size}.png":
                    item["transcript"] = f"coplay-transcripts/{tname}"
                    item["transcript_sha256"] = sha256(os.path.join(tdir, tname))
    if len(sys.argv) > 3:  # ready-made entries carried over unchanged (key-art plates)
        files += json.load(open(sys.argv[3]))
    manifest = {
        "schema_version": 3,
        "captured": "2026-11-24",
        "round": 3,
        "round_note": "Round 3 (fix round after the round-2 final review): the spectator opponents frame is out "
                      "of the gallery, the gallery is reordered, and the co-play frames 08 and 08b are new "
                      "sessions that end on the standing order moving its flag. All other frames are the "
                      "round-2 files, unchanged.",
        "kind": "native desktop gameplay captures for storefront-v2",
        "build": dict(build_info(), description=(
            "Globulation 2 0.11.7.0 + 15 commits (revision 5bf966285aa8), the installed build; maps, AI "
            "roster and simulation identical to the v0.11.7.0 tag. Not the public 0.11.7.0 release binary "
            "(facts/storefront-v2-claims.md R13).")),
        "platform": {"os": "macOS " + platform.mac_ver()[0], "machine": platform.machine()},
        "capture_method": {
            "summary": "Installed build run off-screen (SDL dummy video driver, --renderer portable-sdl, "
                       "--ui-scale 2, HD artwork forced on, clouds and cloud shadows off), driven and captured "
                       "through its embedded MCP server (port 47815, fresh profile); ui_screenshot saves the "
                       "next rendered frame at native pixels.",
            "launch": "tools/launch-capture-game.sh PROFILE 3840x2160 2 47815 (2880x1800 for the 16:10 set)",
            "clean_state": [
                "Health and food bars lens off (key I, the in-game 'toggle draw information')",
                "forbidden, clearing and guard areas erased in view just before each frame, then the frame is "
                "checked for zone-outline colours and re-shot if any remain",
                "frames kept only while the top bar's workers stat is not negative and the event list shows at "
                "most two rows (read through ui_inspect before and after the frame), except where noted",
                "zoom a multiple of 1/8; normal speed (1x); never paused",
            ],
            "aspect_16_10": "captured in a 2880x1800 window at the same zoom as the 16:9 frame (fewer tiles "
                            "in view); a separate run of the same recipe, so units differ in detail",
        },
        "files": files,
    }
    json.dump(manifest, open(os.path.join(out, "manifest.json"), "w"), indent=1)
    json.dump(selection, open(os.path.join(out, "selection.json"), "w"), indent=1)
    cols, tw = 2, 1200
    th = tw * 9 // 16
    rows = (len(sheet) + cols - 1) // cols
    canvas = Image.new("RGB", (cols * tw, rows * (th + 40)), (16, 12, 24))
    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 24)
    except OSError:
        font = ImageFont.load_default()
    for n, (path, label) in enumerate(sheet):
        with Image.open(path) as im:
            thumb = im.convert("RGB").resize((tw, th), Image.LANCZOS)
        x, y = (n % cols) * tw, (n // cols) * (th + 40)
        canvas.paste(thumb, (x, y + 40))
        draw.text((x + 10, y + 8), label, fill=(249, 232, 187), font=font)
    canvas.save(os.path.join(out, "contact-sheet.jpg"), quality=86)
    print(len(files), "files;", len(selection), "gallery entries")


if __name__ == "__main__":
    main()
