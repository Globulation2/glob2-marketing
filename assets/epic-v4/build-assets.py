"""Native review covers: exact existing game scene + existing title masks.

No generated creatures, scene retouching, sprite enlargement or store export upscale.
Requires Pillow and the sibling website/design-system repositories.
"""
from pathlib import Path
from PIL import Image, ImageFilter

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parents[2]
DESIGN = WORKSPACE / "glob2-design-system"
WEBSITE = WORKSPACE / "glob2-online-website"
SCENE = WEBSITE / "public/images/home-thriving-colony.webp"


def wordmark(width):
    art = Image.new("RGBA", (900, 131))
    for name, color in (("wordmark-letters.webp", "#f9e8bb"), ("wordmark-two.webp", "#e2b85f")):
        mask = Image.open(DESIGN / "assets" / name).convert("RGBA").getchannel("A")
        layer = Image.new("RGBA", art.size, color)
        layer.putalpha(mask)
        art.alpha_composite(layer)
    assert width <= art.width
    return art.resize((width, round(width * 131 / 900)), Image.Resampling.LANCZOS)


def cover(scene, logo_width, top):
    result = scene.convert("RGBA")
    title = wordmark(logo_width)
    x = (result.width - title.width) // 2
    alpha = Image.new("L", result.size)
    alpha.paste(title.getchannel("A"), (x, top))
    # Contour-following shadow only: no rectangular panel or scene color treatment.
    glow_alpha = alpha.filter(ImageFilter.MaxFilter(17)).filter(ImageFilter.GaussianBlur(9))
    glow_alpha = glow_alpha.point(lambda p: round(p * .86))
    glow = Image.new("RGBA", result.size, (10, 7, 16, 0))
    glow.putalpha(glow_alpha)
    result.alpha_composite(glow)
    edge = Image.new("RGBA", result.size, (17, 9, 24, 0))
    edge.putalpha(alpha.filter(ImageFilter.MaxFilter(5)))
    result.alpha_composite(edge)
    result.alpha_composite(title, (x, top))
    return result.convert("RGB")


source = Image.open(SCENE).convert("RGB")
assert source.size == (1280, 720)
landscape = cover(source, 900, 283)
landscape.save(HERE / "landscape-native-1280x720.png", optimize=True)

# A native 3:4 crop preserves scene scale; no reframing by invented scenery.
portrait_source = source.crop((315, 0, 855, 720))
portrait = cover(portrait_source, 488, 286)
portrait.save(HERE / "portrait-native-540x720.png", optimize=True)

# Side-by-side review sheet. Actual cover files contain title only.
sheet = Image.new("RGB", (1420, 816), "#111114")
sheet.paste(landscape.resize((960, 540), Image.Resampling.LANCZOS), (20, 20))
sheet.paste(portrait.resize((405, 540), Image.Resampling.LANCZOS), (995, 20))
sheet.paste(landscape.resize((384, 216), Image.Resampling.LANCZOS), (280, 580))
sheet.paste(portrait.resize((162, 216), Image.Resampling.LANCZOS), (995, 580))
sheet.save(HERE / "review-contact-sheet.jpg", quality=94)
