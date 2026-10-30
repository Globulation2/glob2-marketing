"""Export approved pre-title colony art for Microsoft Store image fields.

Uses only retained approved PNG layers. No original asset is rewritten.
Pillow is the sole dependency; run this script from any working directory.
"""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageFilter, ImageOps

HERE = Path(__file__).resolve().parent
MARKETING = HERE.parents[2]
SOURCE = MARKETING / "assets/epic-v5/colony-native.png"
LOGO = MARKETING / "assets/epic-v5/product-logo-960x540.png"
LOGO_CROP = (30, 204, 930, 335)


def wordmark(width):
    with Image.open(LOGO) as source:
        assert source.size == (960, 540)
        title = source.convert("RGBA").crop(LOGO_CROP)
    return title.resize((width, round(width * 131 / 900)), Image.Resampling.LANCZOS)


def with_title(scene, width, top):
    # The same original-title and shadow treatment as the approved v5 script.
    scene = scene.convert("RGBA")
    title = wordmark(width)
    x = (scene.width - width) // 2
    alpha = Image.new("L", scene.size)
    alpha.paste(title.getchannel("A"), (x, top))
    shadow = Image.new("RGBA", scene.size, (7, 11, 25, 0))
    shadow.putalpha(alpha.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(6)))
    scene.alpha_composite(shadow)
    scene.alpha_composite(title, (x, top))
    return scene.convert("RGB")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


with Image.open(SOURCE) as source:
    scene = source.convert("RGB")
assert scene.size == (1672, 941)

poster_crop = (554, 0, 1178, 936)
poster = scene.crop(poster_crop).resize((1440, 2160), Image.Resampling.LANCZOS)
poster = with_title(poster, 1296, 190)
box_crop = (365, 0, 1306, 941)
box = scene.crop(box_crop).resize((1080, 1080), Image.Resampling.LANCZOS)
box = with_title(box, 972, 60)
# Start from the approved pre-title scene; no text is erased or painted over.
hero = ImageOps.fit(scene, (1920, 1080), method=Image.Resampling.LANCZOS)

specs = [
    ("poster-1440x2160.png", poster, {"source_crop": list(poster_crop), "title_width": 1296, "title_top": 190}),
    ("box-art-1080x1080.png", box, {"source_crop": list(box_crop), "title_width": 972, "title_top": 60}),
    ("super-hero-titleless-1920x1080.png", hero, {"source_fit": "centered ImageOps.fit, preserving aspect ratio", "title": "None; approved pre-title scene used directly"}),
]
images = []
for filename, image, treatment in specs:
    output = HERE / filename
    image.save(output, optimize=True)
    images.append({"file": filename, "dimensions": list(image.size), "mode": image.mode,
                   "format": "PNG", "bytes": output.stat().st_size, "sha256": digest(output),
                   "treatment": treatment})

manifest = {
    "prepared": "2026-10-30",
    "purpose": "Dedicated Microsoft Store poster, box-art and titleless Super hero fields",
    "source": "../../epic-v5/colony-native.png",
    "source_dimensions": list(scene.size),
    "source_sha256": digest(SOURCE),
    "title_source": "../../epic-v5/product-logo-960x540.png",
    "title_source_sha256": digest(LOGO),
    "title_source_crop": list(LOGO_CROP),
    "resampling": "Lanczos",
    "source_notice": "Approved promotional illustration and existing real-unit composite; not gameplay. No new generation, inpainting, retouching or unit-anatomy editing.",
    "images": images,
}
(HERE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
