#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""1920x1080 JPEG web exports of the clean desktop gallery and the side-by-side
co-play alternate, for stores with per-file caps (Epic, Snap, itch.io, Steam,
AppStream). The 3840x2160 PNGs stay the masters (Microsoft Store).

usage: uv run --with pillow python web-export.py CAPTURES_DIR

Reads CAPTURES_DIR/selection.json (gallery order) and manifest.json (the
alternates: every 16:9 file whose role is in the gallery but is not itself in
selection.json, i.e. 08b), and writes CAPTURES_DIR/web-1920/:
  <name>-1920x1080.jpg   Lanczos reduction (exactly 1/2 of 3840x2160), RGB, no
                         alpha, no ICC profile (untagged = sRGB, as the game's
                         framebuffer PNGs are), 4:4:4 chroma, quality 95, lowered
                         in steps to no less than 92 only if a file would exceed
                         the 4 MB cap
  manifest.json          source file and SHA-256, quality, bytes, SHA-256
Nothing else is changed: no crop, sharpening, grade or text.
"""
import hashlib
import io
import json
import os
import sys

from PIL import Image

SIZE = (1920, 1080)
CAP = 4_000_000
QUALITIES = (95, 94, 93, 92)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def main():
    root = sys.argv[1]
    out_dir = os.path.join(root, "web-1920")
    os.makedirs(out_dir, exist_ok=True)
    selection = json.load(open(os.path.join(root, "selection.json")))
    manifest = json.load(open(os.path.join(root, "manifest.json")))
    gallery = [e["capture"] for e in selection]
    roles = {e["role"] for e in selection}
    alternates = [f["file"] for f in manifest["files"]
                  if f.get("aspect") == "16:9" and f.get("role") in roles and f["file"] not in gallery
                  and not f["file"].startswith("keyart-")]
    items = []
    for name in gallery + alternates:
        src = os.path.join(root, name)
        raw = open(src, "rb").read()
        with Image.open(io.BytesIO(raw)) as im:
            assert im.size == (3840, 2160), (name, im.size)
            small = im.convert("RGB").resize(SIZE, Image.LANCZOS)
        for q in QUALITIES:
            buf = io.BytesIO()
            small.save(buf, "JPEG", quality=q, subsampling=0, optimize=True, progressive=False)
            if buf.tell() <= CAP:
                break
        data = buf.getvalue()
        if len(data) > CAP:
            raise SystemExit(f"{name}: {len(data)} bytes at quality {q} exceeds {CAP}")
        stem = name.rsplit("-", 1)[0]
        dst = f"{stem}-1920x1080.jpg"
        open(os.path.join(out_dir, dst), "wb").write(data)
        with Image.open(io.BytesIO(data)) as chk:
            assert chk.size == SIZE and chk.mode == "RGB" and chk.format == "JPEG" and "icc_profile" not in chk.info
        role = next((e["role"] for e in selection if e["capture"] == name),
                    next(f["role"] for f in manifest["files"] if f["file"] == name))
        items.append({
            "file": dst,
            "position": gallery.index(name) + 1 if name in gallery else None,
            "role": role,
            "alternate_of": None if name in gallery else next(e["capture"] for e in selection if e["role"] == role),
            "source": name,
            "source_sha256": sha256(raw),
            "size": list(SIZE),
            "format": "JPEG (baseline, 4:4:4, no alpha, no ICC profile: sRGB)",
            "quality": q,
            "bytes": len(data),
            "sha256": sha256(data),
        })
        print(dst, q, len(data))
    json.dump({
        "kind": "1920x1080 JPEG web exports of the clean desktop gallery (in selection.json order) and its "
                "side-by-side co-play alternate",
        "made_by": "tools/web-export.py",
        "treatment": "Lanczos reduction to exactly half of the 3840x2160 master; nothing else",
        "cap_bytes": CAP,
        "use": "Epic, Snap, itch.io, Steam and AppStream, or any store with a per-file cap; the 3840x2160 PNG "
               "masters stay the Microsoft Store files",
        "files": items,
    }, open(os.path.join(out_dir, "manifest.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
