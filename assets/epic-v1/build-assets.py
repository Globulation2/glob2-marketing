"""Rebuild review artwork from sibling project assets; requires Pillow.

Run from any directory. No game image is enlarged or represented as a fresh capture.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parents[2]
DESIGN = WORKSPACE / "glob2-design-system"
WEBSITE = WORKSPACE / "glob2-online-website"
INK = "#f9e8bb"
GOLD = "#e2b85f"
BACKGROUND = "#1b1229"
PANEL = "#2b203c"
FONT = DESIGN / "assets/glob2-sans.woff2"


def logo(width=900):
    result = Image.new("RGBA", (900, 131))
    for name, color in [("wordmark-letters.webp", INK), ("wordmark-two.webp", GOLD)]:
        mask = Image.open(DESIGN / "assets" / name).convert("RGBA").getchannel("A")
        layer = Image.new("RGBA", result.size, color)
        layer.putalpha(mask)
        result.alpha_composite(layer)
    assert width <= 900
    return result.resize((width, round(width * 131 / 900)), Image.Resampling.LANCZOS)


def background(size):
    image = Image.new("RGB", size, BACKGROUND)
    draw = ImageDraw.Draw(image)
    width, height = size
    draw.ellipse((width * .62, -height * .2, width * 1.5, height * 1.2), fill=PANEL)
    return image


def text(image, xy, content, size, fill=INK, spacing=18):
    ImageDraw.Draw(image).multiline_text(
        xy, content, font=ImageFont.truetype(str(FONT), size), fill=fill, spacing=spacing
    )


def scene(image, xy, width):
    source = Image.open(WEBSITE / "public/images/home-thriving-colony.webp").convert("RGB")
    assert width <= source.width
    source = source.resize((width, round(source.height * width / source.width)), Image.Resampling.LANCZOS)
    x, y = xy
    draw = ImageDraw.Draw(image)
    draw.rectangle((x-3, y-3, x+source.width+2, y+source.height+2), fill=GOLD)
    image.paste(source, xy)


# Native-size wordmark centered on the required transparent product-logo canvas.
product = Image.new("RGBA", (960, 540))
product.alpha_composite(logo(), (30, 204))
product.save(HERE / "product-logo-960x540.png", optimize=True)

# Key-art compositions: native/downsampled scene in a branded frame, not carousel captures.
landscape = background((2560, 1440))
landscape.paste(logo(), (140, 170), logo())
text(landscape, (140, 470), "Build a thriving\ncolony in contested\nterritory.", 88, spacing=25)
text(landscape, (145, 1160), "REAL-TIME STRATEGY", 31, GOLD)
scene(landscape, (1160, 355), 1280)
landscape.save(HERE / "offer-landscape-2560x1440.png", optimize=True)

portrait = background((1200, 1600))
portrait.paste(logo(), (150, 180), logo())
text(portrait, (120, 430), "Build a thriving\ncolony in contested\nterritory.", 76, spacing=20)
scene(portrait, (80, 840), 1040)
text(portrait, (120, 1490), "REAL-TIME STRATEGY", 25, GOLD)
portrait.save(HERE / "offer-portrait-1200x1600.png", optimize=True)

# Review-only contact sheet, deliberately excluded from store upload slots.
sheet = Image.new("RGB", (1600, 1000), "#101014")
sheet.paste(landscape.resize((1120, 630), Image.Resampling.LANCZOS), (20, 80))
sheet.paste(portrait.resize((420, 560), Image.Resampling.LANCZOS), (1160, 80))
product_preview = Image.new("RGBA", product.size, BACKGROUND)
product_preview.alpha_composite(product)
sheet.paste(product_preview.convert("RGB").resize((480, 270), Image.Resampling.LANCZOS), (340, 710))
text(sheet, (25, 20), "EPIC ARTWORK / V1 REVIEW", 24)
text(sheet, (25, 940), "Key-art layouts use an existing replay crop. Fresh gameplay carousel capture still needed.", 20)
sheet.save(HERE / "review-contact-sheet.jpg", quality=92)
