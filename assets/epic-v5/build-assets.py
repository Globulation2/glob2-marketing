"""Compose original Glob2 units and title over the illustrated environment.

The only generated content is environment-native.png. Character alpha silhouettes
and proportions come from unchanged source renders retained in unit-references.
Pillow is required; source title masks live in the sibling design-system checkout.
"""
from pathlib import Path
import colorsys
from PIL import Image, ImageDraw, ImageFilter, ImageOps

HERE = Path(__file__).resolve().parent
MARKETING = HERE.parents[1]
DESIGN = MARKETING.parent / "glob2-design-system" / "assets"
UNITS = HERE.parent / "epic-v2" / "unit-references"


def wordmark(width):
    title = Image.new("RGBA", (900, 131))
    for name, color in (("wordmark-letters.webp", "#f9e8bb"),
                        ("wordmark-two.webp", "#e2b85f")):
        mask = Image.open(DESIGN / name).convert("RGBA").getchannel("A")
        layer = Image.new("RGBA", title.size, color)
        layer.putalpha(mask)
        title.alpha_composite(layer)
    return title.resize((width, round(width * 131 / 900)), Image.Resampling.LANCZOS)


def source_unit(role, direction, size):
    image = Image.open(UNITS / f"{role}-direction-{direction}-pose-0.png").convert("RGBA")
    pixels = []
    for r, g, b, a in (image.getpixel((x, y)) for y in range(image.height) for x in range(image.width)):
        # Source exports use alpha=1 as an empty-background sentinel.
        if a <= 1:
            pixels.append((0, 0, 0, 0))
        else:
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            rgb = colorsys.hsv_to_rgb((h + .325) % 1, s * .88, v * .94)
            pixels.append((*[round(c * 255) for c in rgb], a))
    image.putdata(pixels)
    return image.resize((size, size), Image.Resampling.LANCZOS)


def place_unit(scene, role, direction, x, y, size):
    unit = source_unit(role, direction, size)
    shadow = Image.new("RGBA", scene.size)
    d = ImageDraw.Draw(shadow)
    d.ellipse((x-size*.18, y-size*.06, x+size*.18, y+size*.045), fill=(8, 18, 20, 80))
    scene.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(1.4)))
    scene.alpha_composite(unit, (round(x-size/2), round(y-size*.88)))


def with_title(scene, width, top):
    scene = scene.convert("RGBA")
    title = wordmark(width)
    x = (scene.width-width)//2
    alpha = Image.new("L", scene.size)
    alpha.paste(title.getchannel("A"), (x, top))
    shadow = Image.new("RGBA", scene.size, (7, 11, 25, 0))
    shadow.putalpha(alpha.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(6)))
    scene.alpha_composite(shadow)
    scene.alpha_composite(title, (x, top))
    return scene.convert("RGB")


scene = Image.open(HERE / "environment-native.png").convert("RGBA")
assert scene.size == (1672, 941)
# Existing game frames at environmental scale; their role-specific silhouettes
# are not generated or re-drawn. Coordinates anchor the sprite's ground contact.
workers = [
    (0, 833, 665, 53), (1, 852, 648, 49), (3, 859, 623, 47),
    (0, 823, 600, 46), (1, 960, 610, 47), (3, 1030, 607, 45),
    (0, 496, 555, 45), (1, 477, 529, 43), (3, 532, 483, 40),
    (0, 285, 553, 40), (1, 1010, 455, 36), (3, 938, 363, 29),
    (0, 690, 396, 31), (1, 907, 738, 55), (3, 786, 763, 57),
]
for direction, x, y, size in workers:
    place_unit(scene, "worker", direction, x, y, size)
for direction, x, y, size in [(0, 1264, 466, 35), (3, 435, 450, 35)]:
    place_unit(scene, "warrior", direction, x, y, size)

scene.convert("RGB").save(HERE / "colony-native.png", optimize=True)
landscape_scene = ImageOps.fit(scene, (2560, 1440), method=Image.Resampling.LANCZOS)
landscape = with_title(landscape_scene, 1940, 115)
landscape.save(HERE / "offer-landscape-2560x1440.png", optimize=True)
landscape.save(HERE / "offer-landscape-2560x1440.jpg", quality=95, subsampling=0, optimize=True)

# Intentional central crop keeps the primary hive, economy and native units.
# Title is freshly placed for portrait, never baked into the source crop.
portrait_scene = scene.crop((483, 0, 1189, 941)).resize((1200, 1600), Image.Resampling.LANCZOS)
portrait = with_title(portrait_scene, 1080, 160)
portrait.save(HERE / "offer-portrait-1200x1600.png", optimize=True)
portrait.save(HERE / "offer-portrait-1200x1600.jpg", quality=95, subsampling=0, optimize=True)

logo_canvas = Image.new("RGBA", (960, 540))
logo = wordmark(900)
logo_canvas.alpha_composite(logo, (30, (540-logo.height)//2))
logo_canvas.save(HERE / "product-logo-960x540.png", optimize=True)

sheet = Image.new("RGB", (1500, 1100), "#10131a")
sheet.paste(landscape.resize((1024, 576), Image.Resampling.LANCZOS), (20, 20))
sheet.paste(portrait.resize((420, 560), Image.Resampling.LANCZOS), (1060, 20))
sheet.paste(landscape.resize((400, 225), Image.Resampling.LANCZOS), (20, 630))
sheet.paste(landscape.resize((200, 113), Image.Resampling.LANCZOS), (460, 630))
sheet.paste(portrait.resize((200, 267), Image.Resampling.LANCZOS), (720, 630))
sheet.save(HERE / "review-contact-sheet.jpg", quality=94)
