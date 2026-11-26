#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Build a labelled contact sheet for one device-class directory.

    uv run --with pillow python contact_sheet.py DIRECTORY [--out FILE] [--cell 420]

Every PNG named NN-slug-WxH.png is scaled down (for review only; the sheet is
not a store asset) and labelled with its filename, portrait and landscape in
separate rows. The
sheet is written to DIRECTORY/contact-sheet.jpg.
"""
import argparse
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

NAME = re.compile(r"^(\d\d|alt)-.*-\d+x\d+\.png$")


def font(size):
    for candidate in ("/System/Library/Fonts/Helvetica.ttc", "/System/Library/Fonts/SFNS.ttf"):
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            pass
    return ImageFont.load_default()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--cell", type=int, default=560, help="portrait thumbnail height in pixels")
    parser.add_argument("--pattern", default=None, help="regex for file names (default NN-slug-WxH.png)")
    args = parser.parse_args()
    pattern = re.compile(args.pattern) if args.pattern else NAME
    files = sorted(p for p in args.directory.glob("*.png") if pattern.match(p.name))
    if not files:
        raise SystemExit(f"no captures in {args.directory}")
    # One row per orientation, every thumbnail scaled (down only) to the row height.
    groups = {"portrait": [], "landscape": []}
    for path in files:
        with Image.open(path) as image:
            image = image.convert("RGB")
            portrait = image.height >= image.width
            height = args.cell if portrait else round(args.cell * 0.62)
            image = image.resize((round(image.width * height / image.height), height), Image.LANCZOS)
            groups["portrait" if portrait else "landscape"].append((path.name, image))
    pad, label = 16, 30
    rows = [row for row in groups.values() if row]
    width = max(sum(t.width + pad for _, t in row) for row in rows) + pad
    total = pad + sum(row[0][1].height + label + pad for row in rows)
    sheet = Image.new("RGB", (width, total), (24, 26, 30))
    draw = ImageDraw.Draw(sheet)
    text = font(13)
    y = pad
    for row in rows:
        x = pad
        for name, thumb in row:
            sheet.paste(thumb, (x, y))
            draw.text((x, y + thumb.height + 6), name[:-4][:max(12, thumb.width // 7)], fill=(230, 232, 236), font=text)
            x += thumb.width + pad
        y += row[0][1].height + label + pad
    thumbs = [t for row in rows for t in row]
    out = args.out or args.directory / "contact-sheet.jpg"
    sheet.save(out, quality=88)
    print(out, sheet.size, len(thumbs), "captures")


if __name__ == "__main__":
    main()
