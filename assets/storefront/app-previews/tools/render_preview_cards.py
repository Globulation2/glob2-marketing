#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Render the app-preview text cards with the trailer's card renderer, one size at a time.

    uv run render_preview_cards.py --locale en[,ja,...|all] --out CARDS [--size 886x1920,1200x1600]

previews.json holds the card style ("text", the trailer's fields, fonts and colours) and,
per preview size, the portrait layout changes in "text_layout_by_size" (the iPad has no
bottom navigation bar, so its lines sit lower: 83 % of the height instead of 74 %). For
each size this writes a temporary data file with that layout and runs
../../trailer/tools/render_cards.py on it, so every card is laid out by Chromium at
its own size. Output: CARDS/<locale>/<WxH>/<field>.png, CARDS/wordmark-<WxH>.png and
CARDS/cards-<WxH>.json (the renderer's report).
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RENDER = HERE.parents[1] / "trailer" / "tools" / "render_cards.py"

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("--locale", default="en")
ap.add_argument("--out", required=True)
ap.add_argument("--size", default="886x1920,1200x1600")
args = ap.parse_args()
cfg = json.loads((HERE / "previews.json").read_text())
out = Path(args.out)
for size in args.size.split(","):
    data = {"text": dict(cfg["text"])}
    data["text"]["portrait"] = dict(cfg["text"]["portrait"], **cfg.get("text_layout_by_size", {}).get(size, {}))
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(data, f)
    try:
        subprocess.run(["uv", "run", *(["--offline"] if os.environ.get("UV_OFFLINE") else []), str(RENDER),
                        "--locale", args.locale, "--out", str(out), "--size", size, "--data", f.name], check=True)
    finally:
        os.unlink(f.name)
    (out / "cards.json").rename(out / f"cards-{size}.json")
sys.exit(0)
