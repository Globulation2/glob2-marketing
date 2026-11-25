#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Cut HUD-free key-art plates out of single native frames.

usage: uv run --with pillow python crop-keyart.py FRAMES_DIR OUT_DIR EXTRA.json [--size WxH]

For key art the game is run in a window larger than the plate (for example
4256x2600 for a 3840x2160 plate, at UI scale 2). The sidebar takes the right
406 pixels and the event list the top left corner, so the plate is the
bottom-left WxH pixels of the frame: one rectangle of one frame, not scaled,
not retouched, nothing composited. Reads every "90-keyart-*.png" with its
capture.py sidecar, writes "keyart-<name>-WxH.png" and manifest entries.
"""
import argparse
import glob
import hashlib
import json
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))


def sha256(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("frames"); ap.add_argument("out"); ap.add_argument("extra")
    ap.add_argument("--size", default="3840x2160")
    args = ap.parse_args()
    w, h = (int(v) for v in args.size.split("x"))
    matches = json.load(open(os.path.join(HERE, "matches.json")))
    entries = []
    for src in sorted(glob.glob(os.path.join(args.frames, "90-keyart-*.png"))):
        side = json.load(open(src[:-4] + ".json"))
        recipe = side["recipe"]
        with Image.open(src) as im:
            fw, fh = im.size
            if fw - 406 < w or fh < h:
                raise SystemExit(f"{src}: frame {fw}x{fh} is too small for a {w}x{h} plate")
            box = (0, fh - h, w, fh)
            plate = im.crop(box)
            name = "keyart-" + recipe["id"].split("90-keyart-")[1] + f"-{w}x{h}.png"
            plate.save(os.path.join(args.out, name), optimize=True)
        match = matches[recipe["match"]]
        zoom = side["camera"]["zoom"]
        entries.append({
            "file": name,
            "shot": "keyart",
            "description": recipe.get("description", ""),
            "window_pixels": [w, h],
            "aspect": "16:9",
            "kind": "HUD-free plate: one rectangle cropped from a single native frame; not scaled or retouched",
            "cropped_from": {"frame_pixels": [fw, fh], "box": list(box), "frame_sha256": side["sha256"]},
            "tile_pixels": 64 * zoom,
            "match": recipe["match"],
            "map": match["map"],
            "game_seed": match["game_seed"],
            "players": [{"team": i, "controller": "AI " + ai} for i, ai in enumerate(match["ais_by_team"])],
            "seat": f"player seat on colony {recipe['team']}, shared with its AI ({match['ais_by_team'][recipe['team']]})",
            "source_save": f"matches/{recipe['match']}/checkpoint-{recipe['tick']}.game.gz",
            "source_save_sha256": side.get("source_save_sha256"),
            "source_save_tick": recipe["tick"],
            "tick_at_capture": side["tick_at_capture"],
            "camera": side["camera"],
            "player_actions_before_capture": ["erased the colony's forbidden and clearing area markings in view"],
            "recipe_id": recipe["id"],
            "sha256": sha256(os.path.join(args.out, name)),
        })
        print(name, fw, fh, box)
    with open(args.extra, "w") as fh:
        json.dump(entries, fh, indent=1)


if __name__ == "__main__":
    main()
