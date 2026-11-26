#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Storefront-v2 key art: concept comps and the per-store derivative set.

    uv run --with pillow python build-assets.py [--only concepts|derivatives]

Writes concepts/ (three 16:9 concept comps and two contact sheets), derivatives/
(the per-store set of the recommended concept) and manifest.json. See README.md.

Every picture is a rectangle of one real in-engine capture (a "plate"), scaled
down or kept at native pixels, with design treatment on top: a colour grade,
blur toward the edges, a night-colour scrim or vignette, and the game's own
wordmark. No game object is added, removed, moved or redrawn, nothing is
scaled up beyond WORDMARK_MAX_UPSCALE (wordmark only; plates are never scaled
up), and the wordmark is the only text. Pillow is the only dependency.

The script is deterministic: gradients are dithered with a seeded generator,
so a rebuild gives byte-identical files on the same Pillow build (JPEG bytes
may differ with another libjpeg). It verifies every output's pixel size, format and file-size limit and
writes manifest.json.
"""
import argparse
import hashlib
import math
import json
import random
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageMath

Image.MAX_IMAGE_PIXELS = None
HERE = Path(__file__).resolve().parent
MARKETING = HERE.parents[2]
GAME = MARKETING.parent / "glob2"
CAPTURES = MARKETING / "assets/storefront/captures/desktop"
PLATES = HERE / "plates"
WORDMARK_SRC = GAME / "content/data/gfx/menu-wordmark.png"

# Brand colours (glob2-design-system, night colony theme).
NIGHT = (0x1B, 0x12, 0x29)
SURFACE = (0x2B, 0x1C, 0x42)
CREAM = (0xF9, 0xE8, 0xBB)
GOLD = (0xE2, 0xB8, 0x5F)
GOLD_EDGE = (0xC6, 0x9E, 0x4C)

WORDMARK_MAX_UPSCALE = 1.15
LANCZOS = Image.Resampling.LANCZOS
BICUBIC = Image.Resampling.BICUBIC


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


# ---------------------------------------------------------------- wordmark

_WM = {}


def wordmark_masks():
    """Alpha masks of the game's title art: the letters and the "2".

    menu-wordmark.png is dark green letters and a gold "2" on a pale paper
    background (RGB, no alpha). The letters are un-mixed on the red channel
    (paper 231 -> ink 28), the "2" on the blue channel (paper 217 -> ink 91);
    the two are separated at the gap between "n" and "2". Result: two "L"
    masks cropped to the wordmark's bounding box, 1941 x 268 px.
    """
    if not _WM:
        src = Image.open(WORDMARK_SRC).convert("RGB")
        assert src.size == (2103, 748), src.size
        r, _, b = src.split()

        def ramp(channel, paper, ink, noise=12):
            lo = paper - noise
            return channel.point([max(0, min(255, round((lo - v) * 255 / (lo - ink)))) for v in range(256)])
        split = 1842
        letters = Image.new("L", src.size)
        letters.paste(ramp(r, 231, 34).crop((0, 0, split, src.height)), (0, 0))
        two = Image.new("L", src.size)
        two.paste(ramp(b, 217, 97).crop((split, 0, src.width, src.height)), (split, 0))
        box = ImageChops.lighter(letters, two).getbbox()
        _WM["letters"], _WM["two"], _WM["box"] = letters.crop(box), two.crop(box), box
    return _WM["letters"], _WM["two"]


def wordmark_native_width():
    return wordmark_masks()[0].width


def wordmark_layer(width, style="outline"):
    """RGBA wordmark at `width` px with its contrast treatment, plus its inner offset.

    Returns (layer, (dx, dy)): paste the layer at (x - dx, y - dy) to put the
    letters' bounding box at (x, y). Treatment, all in brand colours:
      * a wide soft night glow that calms whatever is behind the letters;
      * a solid night outline and a short drop shadow for hard-edged contrast;
      * cream letters and the gold "2", flat as in the game's own title.
    style "plain" leaves out the glow, outline and shadow (transparent logos).
    """
    letters, two = wordmark_masks()
    scale = width / letters.width
    assert scale <= WORDMARK_MAX_UPSCALE, f"wordmark scaled up {scale:.3f}x"
    height = round(letters.height * scale)
    letters = letters.resize((width, height), LANCZOS)
    two = two.resize((width, height), LANCZOS)
    pad = round(height * 1.1) if style != "plain" else 0
    size = (width + 2 * pad, height + 2 * pad)
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    ink = Image.new("L", size)
    ink.paste(ImageChops.lighter(letters, two), (pad, pad))
    if style == "outline":
        # wide glow
        glow = ink.filter(ImageFilter.GaussianBlur(height * 0.30)).point(lambda v: min(255, round(v * 2.1)))
        layer.alpha_composite(solid(size, NIGHT, glow.point(lambda v: round(v * 0.62))))
    if style in ("outline", "logo"):
        # drop shadow
        off = max(2, round(height * 0.045))
        shadow = ImageChops.offset(ink.filter(ImageFilter.GaussianBlur(height * 0.035)), 0, off)
        layer.alpha_composite(solid(size, NIGHT, shadow.point(lambda v: min(255, round(v * 1.5)))))
        # outline: blur then a steep ramp gives a smooth, round-cornered stroke
        stroke = height * 0.040
        outline = ink.filter(ImageFilter.GaussianBlur(stroke)).point(
            lambda v: max(0, min(255, round((v - 22) * 255 / 34))))
        layer.alpha_composite(solid(size, NIGHT, outline))
    for mask, colour in ((letters, CREAM), (two, GOLD)):
        tile = Image.new("L", size)
        tile.paste(mask, (pad, pad))
        layer.alpha_composite(solid(size, colour, tile))
    return layer, (pad, pad)


def solid(size, colour, alpha):
    im = Image.new("RGBA", size, colour + (0,))
    im.putalpha(alpha)
    return im


def place_wordmark(img, width, x, y, style="outline", anchor="lt"):
    """Composite the wordmark; (x, y) is the letters' box corner named by anchor
    ("lt", "ct", "rt": left/centre/right, top). Returns the letters' box."""
    layer, (dx, dy) = wordmark_layer(width, style)
    h = layer.height - 2 * dy
    if anchor[0] == "c":
        x -= width // 2
    elif anchor[0] == "r":
        x -= width
    base = img.convert("RGBA")
    base.alpha_composite(layer, (x - dx, y - dy)) if x - dx >= 0 and y - dy >= 0 else _composite_clipped(base, layer, x - dx, y - dy)
    return base.convert("RGB"), (x, y, x + width, y + h)


def _composite_clipped(base, layer, x, y):
    sx, sy = max(0, -x), max(0, -y)
    layer = layer.crop((sx, sy, min(layer.width, base.width - x), min(layer.height, base.height - y)))
    base.alpha_composite(layer, (max(0, x), max(0, y)))


# ---------------------------------------------------------------- masks

def noise(size, seed):
    return Image.frombytes("L", size, random.Random(seed).randbytes(size[0] * size[1]))


def fmask(size, fn, seed=1, grid=96):
    """Dithered "L" mask from fn(u, v) -> 0..1, u and v in 0..1 across the image.

    fn is sampled on a coarse grid, enlarged with bicubic interpolation in
    floating point and rounded with seeded noise, so slow gradients do not band.
    """
    w, h = size
    gw = grid
    gh = max(2, round(grid * h / w))
    coarse = Image.new("F", (gw, gh))
    coarse.putdata([max(0.0, min(1.0, fn(i / (gw - 1), j / (gh - 1)))) * 254.0 for j in range(gh) for i in range(gw)])
    big = coarse.resize(size, BICUBIC)
    out = ImageMath.lambda_eval(lambda a: a["m"] + a["n"] / 255.0, m=big, n=noise(size, seed).convert("F"))
    return out.convert("L")


def smooth(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


# ---------------------------------------------------------------- treatment

def grade(img, contrast=1.06, saturation=1.10, lift=0.0):
    """Gentle global grade: a touch more contrast and colour."""
    img = ImageEnhance.Color(img).enhance(saturation)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    if lift:
        img = ImageEnhance.Brightness(img).enhance(1 + lift)
    return img


def night_version(img, depth=0.55):
    """The picture as it would look under the brand night colour: multiplied by a
    violet tint and pulled toward NIGHT, so shapes stay visible but quiet."""
    tint = Image.new("RGB", img.size, (118, 96, 168))
    dark = ImageChops.multiply(img, tint)
    return Image.blend(dark, Image.new("RGB", img.size, NIGHT), depth)


def scrim(img, mask, depth=0.55):
    return Image.composite(night_version(img, depth), img, mask)


def defocus(img, mask, radius):
    """Blur toward the edges (mask 255 = fully blurred)."""
    return Image.composite(img.filter(ImageFilter.GaussianBlur(radius)), img, mask)


def cut(plate, box, size):
    """One rectangle of a plate at native pixels or scaled down; never up."""
    x, y, w, h = box
    assert x >= 0 and y >= 0 and x + w <= plate.width and y + h <= plate.height, (box, plate.size)
    assert abs(w / h - size[0] / size[1]) < 0.004, f"aspect {w}x{h} vs {size}"
    assert w >= size[0] - 1 and h >= size[1] - 1, f"upscale: box {w}x{h} -> {size}"
    part = plate.crop((x, y, x + w, y + h))
    return part if part.size == tuple(size) else part.resize(size, LANCZOS, reducing_gap=3.0)


# ---------------------------------------------------------------- plates

# Each plate is one rectangle of one native in-engine frame (see README.md).
PLATE_FILES = {
    "shoreline": PLATES / "plate-shoreline-foursquares-red-z150-t88344.png",
    "oasis": PLATES / "plate-oasis-clash-honeycomb-z150-t70320.png",
    "cabino": CAPTURES / "keyart-foursquares-cabino-zoom150-3840x2160.png",
}
_PLATE_CACHE = {}


def plate(name):
    if name not in _PLATE_CACHE:
        _PLATE_CACHE[name] = Image.open(PLATE_FILES[name]).convert("RGB")
    return _PLATE_CACHE[name]


def frame_box(pl, size, centre, height=None):
    """The crop box of the output's aspect: `height` plate px tall (default: as large
    as the plate allows), centred on `centre` and slid inside the plate."""
    W, H = size
    aspect = W / H
    max_h = min(pl.height, pl.width / aspect)
    h = min(height or max_h, max_h)
    w = h * aspect
    if w > pl.width:
        w = pl.width
        h = w / aspect
    w, h = int(round(w)), int(round(h))
    w, h = min(w, pl.width), min(h, pl.height)
    x = int(round(min(max(centre[0] - w / 2, 0), pl.width - w)))
    y = int(round(min(max(centre[1] - h / 2, 0), pl.height - h)))
    return (x, y, w, h)


# ---------------------------------------------------------------- composition

def ellipse(cx, cy, rx, ry, inner=0.55, soft=0.9):
    """fn(u, v): 1 inside an ellipse core, smooth fall-off outside (u, v in 0..1)."""
    def fn(u, v):
        d = math.hypot((u - cx) / rx, (v - cy) / ry)
        return smooth(1 - (d - inner) / soft)
    return fn


def compose(spec, size, text=True):
    """Render one picture. spec keys:
      plate      plate name
      centre     crop centre in plate px; height: crop height in plate px (optional)
      focus      (u, v) of the sharp centre in the output; dof: blur radius as a share of
                 the output width (0 = none); sharp: radius of the sharp zone
      wm         (cx, cy, width) of the wordmark, all as shares of the output width/height
      halo       scrim strength behind the wordmark; vignette: edge darkening strength
      lift       extra top or bottom night gradient: {"top": (depth, reach)} etc.
    """
    pl = plate(spec["plate"])
    W, H = size
    box = frame_box(pl, size, spec["centre"], spec.get("height"))
    img = cut(pl, box, size)
    img = grade(img, contrast=spec.get("contrast", 1.05), saturation=spec.get("saturation", 1.08))
    asp = W / H
    # depth of field: sharp around the focus, softer toward the edges (a lens effect, no content change)
    dof = spec.get("dof", 0.0016)
    if dof:
        fx, fy = spec.get("focus", (0.5, 0.55))
        sharp = spec.get("sharp", 0.62)
        def blur_fn(u, v):
            d = math.hypot((u - fx) * min(asp, 1.8) / 1.8 * 1.25, (v - fy) * 1.25)
            return smooth((d - sharp * 0.5) / 0.55)
        img = defocus(img, fmask(size, blur_fn, seed=11), max(1.0, dof * W))
    # scrim: night colour behind the wordmark, an edge vignette, optional bands
    wm = spec.get("wm") if text else None
    halo = spec.get("halo", 0.85) if text else 0.0
    vig = spec.get("vignette", 0.55)
    bands = spec.get("bands", {})
    wm_h_share = None
    if wm:
        letters, _ = wordmark_masks()
        wm_h_share = wm[2] * W * letters.height / letters.width / H
    def scrim_fn(u, v):
        m = 0.0
        if wm:
            cx, cy, ww = wm
            m = max(m, halo * ellipse(cx, cy, ww * 0.62, max(wm_h_share * 1.6, 0.12), inner=0.6, soft=0.8)(u, v))
        r = math.hypot((u - 0.5) / 0.5, (v - 0.5) / 0.5) / math.sqrt(2)
        m = max(m, vig * smooth((r - 0.55) / 0.45))
        if "top" in bands:
            d, reach = bands["top"]
            m = max(m, d * smooth((reach - v) / reach))
        if "bottom" in bands:
            d, reach = bands["bottom"]
            m = max(m, d * smooth((v - (1 - reach)) / reach))
        if "left" in bands:
            d, reach = bands["left"]
            m = max(m, d * smooth((reach - u) / reach))
        if "right" in bands:
            d, reach = bands["right"]
            m = max(m, d * smooth((u - (1 - reach)) / reach))
        return m
    img = scrim(img, fmask(size, scrim_fn, seed=23), depth=spec.get("depth", 0.55))
    wm_box = None
    if wm:
        cx, cy, ww = wm
        width = int(round(ww * W))
        letters, _ = wordmark_masks()
        hh = round(letters.height * width / letters.width)
        img, wm_box = place_wordmark(img, width, int(round(cx * W)), int(round(cy * H - hh / 2)), anchor="ct")
    return img, {"plate": spec["plate"], "crop_box": list(box), "scale": round(W / box[2], 4), "wordmark_box": wm_box}


# ---------------------------------------------------------------- concepts (16:9 comps)

# Plate pixel landmarks of the shoreline plate (4396 x 2600), for the framings below:
#   water L (fogged sea): x >= 1923 for y <= 790, and the channel x 3455-4115 below it;
#   a rival island's edge from x ~4020; swarm (1153, 640); four schools (1579, 1139);
#   barracks row y ~1720 (x 904-1766); swimming pool (1870, 2198); inns by the forest (2265, 1596).
CONCEPTS = {
    "a-shoreline": {
        "title": "Shoreline colony",
        "spec": {"plate": "shoreline", "centre": [1995, 1222], "height": 2244, "focus": [0.36, 0.58],
                 "wm": [0.665, 0.165, 0.56]},
    },
    "b-pool-and-swarm": {
        "title": "Pool and swarm",
        "spec": {"plate": "cabino", "centre": [1920, 1080], "focus": [0.4, 0.5], "wm": [0.5, 0.15, 0.58],
                 "bands": {"top": [0.5, 0.32]}},
    },
    "c-oasis-clash": {
        "title": "Oasis clash",
        "spec": {"plate": "oasis", "centre": [2198, 1364], "focus": [0.52, 0.4], "wm": [0.5, 0.85, 0.58],
                 "bands": {"bottom": [0.5, 0.32]}},
    },
}
RECOMMENDED = "a-shoreline"


# ---------------------------------------------------------------- derivatives of the recommended concept

def S(centre, height, wm=None, **kw):
    d = {"plate": "shoreline", "centre": list(centre), "height": height, "wm": wm}
    d.update(kw)
    return d


# Wide frames keep the top-left aligned on the colony and put the wordmark on the water L;
# tall and square frames move left to hold the swarm, barracks and pool, and carry the
# wordmark across a darkened top band (the fogged fields and the sea).
WIDE = S((1995, 1222), 2244, (0.665, 0.165, 0.56), focus=(0.36, 0.58))
PORTRAIT = S((1680, 1300), 2600, (0.5, 0.11, 0.84), focus=(0.45, 0.6), bands={"top": (0.55, 0.30)}, halo=0.9)
# Steam header, GOG banner and similar ~2:1 frames: a tighter crop (about 0.28x) so the
# swarm and schools read as characters at 460 px wide.
HEADER = S((2250, 880), 1560, (0.66, 0.19, 0.58), focus=(0.35, 0.6))
SQUARE = S((2000, 1300), 2600, (0.5, 0.125, 0.76), focus=(0.42, 0.6), bands={"top": (0.5, 0.30)}, halo=0.9)
# Google Play feature graphic and Amazon promotional image (both 1024x500): the header crop
# moved right so the wordmark sits whole on the water, with the letters at least 80 px from
# the right edge and 60 px from the top (Play crops and overlays this graphic; Amazon wants
# text at least 50 px from every edge). Checked by MARGINS below.
PLAY_FEATURE = S((2330, 900), 1560, (0.62, 0.225, 0.56), focus=(0.33, 0.6))

DERIVATIVES = [
    # name, size, format, spec (None wm = no text)
    ("master-3840x2160", (3840, 2160), "png", WIDE),
    ("master-no-text-3840x2160", (3840, 2160), "png", dict(WIDE, wm=None)),
    ("google-play-feature-1024x500", (1024, 500), "jpg", PLAY_FEATURE),
    ("amazon-promo-1024x500", (1024, 500), "png", PLAY_FEATURE),
    ("epic-offer-landscape-2560x1440", (2560, 1440), "jpg", WIDE),
    ("epic-offer-portrait-1200x1600", (1200, 1600), "jpg", S((1720, 1300), 2600, (0.5, 0.115, 0.82), focus=(0.45, 0.6), bands={"top": (0.55, 0.30)}, halo=0.9)),
    ("epic-social-preview-1200x1200", (1200, 1200), "jpg", SQUARE),
    ("microsoft-poster-1440x2160", (1440, 2160), "png", PORTRAIT),
    ("microsoft-box-art-2160x2160", (2160, 2160), "png", SQUARE),
    ("microsoft-box-art-1080x1080", (1080, 1080), "png", SQUARE),
    ("microsoft-super-hero-3840x2160", (3840, 2160), "png", dict(WIDE, wm=None)),
    ("microsoft-super-hero-1920x1080", (1920, 1080), "png", dict(WIDE, wm=None)),
    ("snap-banner-1440x480", (1440, 480), "jpg", S((2250, 650), 1100, (0.665, 0.27, 0.56), focus=(0.35, 0.6))),
    ("itch-cover-630x500", (630, 500), "jpg", S((1938, 1300), 2600, (0.6, 0.14, 0.64), focus=(0.4, 0.6), bands={"top": (0.35, 0.25)})),
    ("gog-main-banner-1600x740", (1600, 740), "jpg", HEADER),
    ("gog-box-342x482", (342, 482), "jpg", S((1700, 1300), 2600, (0.5, 0.11, 0.86), focus=(0.45, 0.6), bands={"top": (0.55, 0.30)}, halo=0.9)),
    ("gog-background-2560x670", (2560, 670), "jpg", S((1995, 822), 1044, None, focus=(0.4, 0.6))),
    ("gog-background-2560x655", (2560, 655), "jpg", S((1995, 822), 1020, None, focus=(0.4, 0.6))),
    ("steam-header-920x430", (920, 430), "jpg", HEADER),
    ("steam-small-capsule-462x174", (462, 174), "jpg", S((2200, 590), 980, (0.55, 0.32, 0.8), focus=(0.4, 0.6), bands={"top": (0.45, 0.5)}, halo=0.95)),
    ("steam-main-capsule-1232x706", (1232, 706), "jpg", S((1995, 1222), 2244, (0.665, 0.165, 0.56), focus=(0.36, 0.58))),
    ("steam-vertical-capsule-748x896", (748, 896), "jpg", S((1800, 1300), 2600, (0.5, 0.115, 0.8), focus=(0.45, 0.6), bands={"top": (0.55, 0.30)}, halo=0.9)),
    ("steam-library-capsule-600x900", (600, 900), "jpg", PORTRAIT),
    ("steam-library-hero-3840x1240", (3840, 1240), "jpg", S((1995, 894), 1288, None, focus=(0.4, 0.55))),
    ("open-graph-1200x630", (1200, 630), "jpg", S((2250, 880), 1560, (0.665, 0.19, 0.56), focus=(0.35, 0.6))),
    ("promo-tile-1024x1024", (1024, 1024), "jpg", SQUARE),
    # GamePix cover (Assets tab, 2026-11-26): 1360x850 JPG or PNG, at most 1.5 MB. 16:10, so
    # the wide framing a little taller; the wordmark stays on the water L.
    ("gamepix-cover-1360x850", (1360, 850), "jpg", S((1995, 1280), 2440, (0.665, 0.17, 0.56), focus=(0.36, 0.58))),
]

# Transparent wordmark logos: name, canvas size (None = tight to the letters), letters width.
LOGOS = [
    ("epic-product-logo-960x540", (960, 540), 860),
    ("gog-logo-1600x740", (1600, 740), 1440),
    ("steam-logo-1280", ("width", 1280), None),
]

# Minimum distance in px of the wordmark's letters from each edge (left, top, right, bottom),
# checked on top of the general 3% rule.
MARGINS = {
    "google-play-feature-1024x500": (50, 60, 80, 50),
    "amazon-promo-1024x500": (50, 60, 80, 50),
}

# Store limits checked after writing (bytes).
SIZE_LIMITS = {
    "epic-product-logo-960x540": 1_000_000,
    "google-play-feature-1024x500": 15_000_000,
    "amazon-promo-1024x500": 15_000_000,
    "snap-banner-1440x480": 2_000_000,
    "gamepix-cover-1360x850": 1_500_000,
    "microsoft-": 50_000_000,
}
JPEG_QUALITY = 95


def logo(canvas, letters_width):
    """The wordmark alone on transparency, with a crisp night outline and a short shadow
    (no wide glow) so it reads on light and dark store backgrounds."""
    if canvas is not None and canvas[0] == "width":
        # Steam library logo: exactly `width` px wide ("1280px wide and/or 720px tall"), tight
        # in height. Shrink the letters until the outlined logo plus its pad fits, then pad
        # left and right to the exact width.
        target, w = canvas[1], canvas[1]
        while True:
            img = logo(None, w)
            if img.width <= target:
                break
            w -= max(1, (img.width - target) // 2)
        out = Image.new("RGBA", (target, img.height), (0, 0, 0, 0))
        out.alpha_composite(img, ((target - img.width) // 2, 0))
        return out
    layer, (dx, dy) = wordmark_layer(letters_width, style="logo")
    box = layer.getbbox()
    layer = layer.crop(box)
    if canvas is None:
        pad = round(layer.height * 0.04)
        out = Image.new("RGBA", (layer.width + 2 * pad, layer.height + 2 * pad), (0, 0, 0, 0))
        out.alpha_composite(layer, (pad, pad))
        return out
    out = Image.new("RGBA", canvas, (0, 0, 0, 0))
    assert layer.width <= canvas[0] and layer.height <= canvas[1], (layer.size, canvas)
    out.alpha_composite(layer, ((canvas[0] - layer.width) // 2, (canvas[1] - layer.height) // 2))
    return out


# ---------------------------------------------------------------- sheets

def label(img, text, colour=CREAM):
    """Sheet captions only (never on a deliverable): Pillow's default bitmap font."""
    from PIL import ImageFont
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.load_default(size=22)
    except TypeError:
        font = ImageFont.load_default()
    d.text((0, 0), text, fill=colour, font=font)
    return img


def sheet(rows, bg=NIGHT, gap=24, cap=34):
    """rows: list of lists of (caption, image). Returns one RGB sheet."""
    width = max(sum(im.width for _, im in r) + gap * (len(r) + 1) for r in rows)
    height = sum(max(im.height for _, im in r) + cap + gap for r in rows) + gap
    out = Image.new("RGB", (width, height), bg)
    y = gap
    for r in rows:
        x = gap
        for caption, im in r:
            out.paste(label(Image.new("RGB", (im.width, cap), bg), caption), (x, y))
            out.paste(im.convert("RGB"), (x, y + cap))
            x += im.width + gap
        y += max(im.height for _, im in r) + cap + gap
    return out


COMPARABLES = Path("/private/tmp/claude-501/-Users-bradley-glob2/4d02c18b-dc3e-4981-ab5e-77b65e7adafe/scratchpad/keyart/comparables")


def thumb(img, w, h):
    """Centre-cover resize used only for the comparison sheets."""
    s = max(w / img.width, h / img.height)
    r = img.resize((max(w, round(img.width * s)), max(h, round(img.height * s))), LANCZOS)
    x, y = (r.width - w) // 2, (r.height - h) // 2
    return r.crop((x, y, x + w, y + h))


# Width at which each store shows a derivative (approximate, for the review sheet only).
DISPLAY_WIDTH = {
    "google-play-feature-1024x500": 512, "amazon-promo-1024x500": 512, "steam-header-920x430": 460,
    "steam-small-capsule-462x174": 231, "steam-main-capsule-1232x706": 616, "steam-vertical-capsule-748x896": 249,
    "steam-library-capsule-600x900": 200, "steam-library-hero-3840x1240": 960, "epic-offer-landscape-2560x1440": 480,
    "epic-offer-portrait-1200x1600": 240, "epic-social-preview-1200x1200": 200, "microsoft-poster-1440x2160": 200,
    "microsoft-box-art-2160x2160": 150, "microsoft-box-art-1080x1080": 150, "microsoft-super-hero-3840x2160": 480,
    "microsoft-super-hero-1920x1080": 480, "snap-banner-1440x480": 480, "itch-cover-630x500": 315,
    "gog-main-banner-1600x740": 400, "gog-box-342x482": 171, "gog-background-2560x670": 960,
    "gog-background-2560x655": 960, "open-graph-1200x630": 400, "promo-tile-1024x1024": 256,
    "master-3840x2160": 480, "master-no-text-3840x2160": 480, "gamepix-cover-1360x850": 340,
}


def derivatives_sheet(deriv_dir):
    """Every derivative at its store display width, logos on dark and light grounds."""
    rows, row, row_w = [], [], 0
    for name, size, fmt, _ in DERIVATIVES:
        w = DISPLAY_WIDTH[name]
        with Image.open(deriv_dir / f"{name}.{fmt}") as im:
            t = im.convert("RGB").resize((w, round(w * size[1] / size[0])), LANCZOS)
        if row and row_w + w > 2000:
            rows.append(row); row, row_w = [], 0
        row.append((f"{name} @{w}", t)); row_w += w + 24
    if row:
        rows.append(row)
    logos = []
    for name, _, _ in LOGOS:
        with Image.open(deriv_dir / f"{name}.png") as im:
            lw = 320
            lt = im.resize((lw, round(lw * im.height / im.width)), LANCZOS)
        for label_, ground in (("dark", NIGHT), ("light", (236, 236, 236))):
            g = Image.new("RGBA", lt.size, ground + (255,))
            g.alpha_composite(lt)
            logos.append((f"{name} on {label_}", g.convert("RGB")))
    rows.append(logos[:4]); rows.append(logos[4:])
    return sheet(rows)


# ---------------------------------------------------------------- main

def save(img, path, fmt):
    if fmt == "jpg":
        img.convert("RGB").save(path, "JPEG", quality=JPEG_QUALITY, subsampling=0, optimize=True)
    else:
        img.save(path, "PNG", optimize=True)


def verify(path, size, fmt, name):
    with Image.open(path) as im:
        assert im.size == tuple(size), f"{path.name}: {im.size} != {size}"
        assert im.format == ("JPEG" if fmt == "jpg" else "PNG"), f"{path.name}: {im.format}"
        mode = im.mode
    n = path.stat().st_size
    for prefix, limit in SIZE_LIMITS.items():
        if name.startswith(prefix):
            assert n <= limit, f"{path.name}: {n} bytes > {limit}"
    return {"file": path.relative_to(HERE).as_posix(), "size": list(size), "format": fmt.upper().replace("JPG", "JPEG"),
            "mode": mode, "bytes": n, "sha256": sha256(path)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=["concepts", "derivatives", "sheets"])
    a = ap.parse_args()
    outputs = []
    concepts_dir = HERE / "concepts"
    deriv_dir = HERE / "derivatives"
    concepts_dir.mkdir(exist_ok=True)
    deriv_dir.mkdir(exist_ok=True)
    renders = {}
    if a.only in (None, "concepts", "sheets"):
        for key, c in CONCEPTS.items():
            img, info = compose(c["spec"], (3840, 2160))
            p = concepts_dir / f"concept-{key}-3840x2160.jpg"
            save(img, p, "jpg")
            outputs.append(dict(verify(p, (3840, 2160), "jpg", p.stem), kind="concept", concept=key, **info))
            renders[key] = img
        # contact sheet: the three comps at half size, then at store thumbnail sizes
        full = [[(f"{k}: {c['title']}" + ("  (recommended)" if k == RECOMMENDED else ""),
                  renders[k].resize((1280, 720), LANCZOS))] for k, c in CONCEPTS.items()]
        p = concepts_dir / "contact-sheet-full.jpg"
        save(sheet(full), p, "jpg")
        # Thumbnails as a store shows them: each concept re-framed for the Steam header
        # (920x430, shown at 460x215) and small capsule (462x174, shown at 231x87 and 184x69).
        # The recommended concept uses its real derivative framings; the others reuse their
        # 16:9 spec at the new aspect.
        spec_of = {n: s for n, _, _, s in DERIVATIVES}
        small_shots = {}
        for k, c in CONCEPTS.items():
            hs = spec_of["steam-header-920x430"] if k == RECOMMENDED else c["spec"]
            ss = spec_of["steam-small-capsule-462x174"] if k == RECOMMENDED else c["spec"]
            small_shots[k] = (compose(hs, (920, 430))[0].resize((460, 215), LANCZOS),
                              compose(ss, (462, 174))[0].resize((231, 87), LANCZOS))
        rows = []
        for k in CONCEPTS:
            h, s = small_shots[k]
            rows.append([(f"{k} 460x215", h), ("231x87", s), ("184x69", s.resize((184, 69), LANCZOS))])
        p2 = concepts_dir / "contact-sheet-thumbnails.jpg"
        save(sheet(rows), p2, "jpg")
        # beside the comparables, all at the same Steam sizes
        comp = []
        games = ["against-the-storm", "timberborn", "northgard", "they-are-billions", "factorio", "mindustry"]
        row_h, row_s = [], []
        for k in CONCEPTS:
            row_h.append((k, small_shots[k][0]))
            row_s.append((k, small_shots[k][1]))
        for g in games:
            hdr = COMPARABLES / f"{g}-header.jpg"
            small = COMPARABLES / f"{g}-capsule_231x87.jpg"
            if hdr.exists():
                row_h.append((g, thumb(Image.open(hdr).convert("RGB"), 460, 215)))
            if small.exists():
                row_s.append((g, thumb(Image.open(small).convert("RGB"), 231, 87)))
        comp = [row_h[:5], row_h[5:], row_s]
        # Other games' store art is third-party material: the comparison sheet is written
        # next to the downloaded thumbnails, outside this public repository.
        if COMPARABLES.exists():
            save(sheet(comp), COMPARABLES.parent / "comparison-with-comparables.jpg", "jpg")
        for q in (p, p2):
            with Image.open(q) as im:
                outputs.append({"file": q.relative_to(HERE).as_posix(), "size": list(im.size), "kind": "review-sheet",
                                "bytes": q.stat().st_size, "sha256": sha256(q)})
    if a.only in (None, "derivatives"):
        for name, size, fmt, spec in DERIVATIVES:
            img, info = compose(spec, size, text=spec.get("wm") is not None)
            if info["wordmark_box"]:
                # the letters keep at least 3% of the frame clear on every side
                x0, y0, x1, y1 = info["wordmark_box"]
                mx, my = 0.03 * size[0], 0.03 * size[1]
                assert x0 >= mx and y0 >= my and x1 <= size[0] - mx and y1 <= size[1] - my, (name, info["wordmark_box"])
                if name in MARGINS:
                    ml, mt, mr, mb = MARGINS[name]
                    assert x0 >= ml and y0 >= mt and size[0] - x1 >= mr and size[1] - y1 >= mb, (name, info["wordmark_box"])
                    info["wordmark_margins_px"] = {"left": x0, "top": y0, "right": size[0] - x1, "bottom": size[1] - y1}
            p = deriv_dir / f"{name}.{fmt}"
            save(img, p, fmt)
            outputs.append(dict(verify(p, size, fmt, name), kind="derivative", concept=RECOMMENDED, text=bool(spec.get("wm")), **info))
            print(name, info["crop_box"], info["scale"], info["wordmark_box"])
        for name, canvas, width in LOGOS:
            img = logo(canvas, width)
            if canvas is not None and canvas[0] == "width":
                assert img.width == canvas[1], (name, img.size)
            p = deriv_dir / f"{name}.png"
            save(img, p, "png")
            outputs.append(dict(verify(p, img.size, "png", name), kind="logo", transparent=True))
        q = HERE / "contact-sheet-derivatives.jpg"
        save(derivatives_sheet(deriv_dir), q, "jpg")
        with Image.open(q) as im:
            outputs.append({"file": q.relative_to(HERE).as_posix(), "size": list(im.size), "kind": "review-sheet",
                            "note": "every derivative at its store display width; logos on dark and light",
                            "bytes": q.stat().st_size, "sha256": sha256(q)})
    if a.only is None:
        write_manifest(outputs)


def write_manifest(outputs):
    inputs = [{"role": "plate", "name": k, "file": str(v.relative_to(MARKETING)), "size": list(Image.open(v).size),
               "sha256": sha256(v)} for k, v in PLATE_FILES.items()]
    inputs.append({"role": "wordmark", "file": "glob2/" + str(WORDMARK_SRC.relative_to(GAME)), "size": [2103, 748],
                   "sha256": sha256(WORDMARK_SRC)})
    manifest = {
        "generated_by": "build-assets.py (uv run --with pillow python build-assets.py)",
        "recommended_concept": RECOMMENDED,
        "plate_capture_build": {
            "description": "Globulation 2 0.11.7.0 + 15 commits (revision 5bf966285aa8), the installed build at "
                           "/Applications/Glob2.app; maps, AI roster and simulation identical to the v0.11.7.0 tag. "
                           "Not the public 0.11.7.0 release binary.",
            "version": "0.11.7.0", "revision": "5bf966285aa8",
            "executable_sha256": "252fd7d7ff8383c2f72760eccb418b4792bfdfe9f820cd8925b8d8cb69cb7c7f",
            "source": "glob2 info version on the installed build; facts/storefront-claims.md R13",
        },
        "inputs": inputs,
        "outputs": outputs,
    }
    (HERE / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")


if __name__ == "__main__":
    sys.exit(main())
