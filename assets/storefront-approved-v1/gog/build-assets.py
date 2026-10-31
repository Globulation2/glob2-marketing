"""GOG product-format derivatives of approved art; Pillow and psd-tools required.

No source image is rewritten. PSDs contain separate raster background, shadow
and original-wordmark layers; the colony composite itself remains flattened.
"""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageOps, ImageFilter, ImageChops
from psd_tools import PSDImage
from psd_tools.api.layers import PixelLayer

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SCENE = ROOT / 'assets/epic-v5/colony-native.png'
LOGO = ROOT / 'assets/epic-v5/product-logo-960x540.png'
CROP = (30, 204, 930, 335)
scene = Image.open(SCENE).convert('RGBA')
mark = Image.open(LOGO).convert('RGBA').crop(CROP)
assert scene.size == (1672, 941) and mark.size == (900, 131)
records = []


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(path, size, treatment, layers=None):
    records.append(dict(file=path.name, dimensions=list(size), bytes=path.stat().st_size,
                        sha256=sha(path), treatment=treatment, layers=layers))


def layout(size, title_width=None, title_top=None, crop=None):
    bg = ImageOps.fit(scene.crop(crop) if crop else scene, size, method=Image.Resampling.LANCZOS)
    layers = [('Approved colony composite (flattened raster)', bg)]
    if title_width:
        title = mark.resize((title_width, round(title_width * 131 / 900)), Image.Resampling.LANCZOS)
        pos = ((size[0]-title.width)//2, title_top if title_top is not None else (size[1]-title.height)//2)
        title_canvas = Image.new('RGBA', size)
        title_canvas.alpha_composite(title, pos)
        shadow = Image.new('RGBA', size, (7, 11, 25, 0))
        shadow.putalpha(title_canvas.getchannel('A').filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(6)))
        layers += [('Wordmark shadow (same approved treatment)', shadow), ('Approved original wordmark (raster)', title_canvas)]
    result = Image.new('RGBA',size)
    for _, layer in layers:
        result.alpha_composite(layer)
    return result,layers


specs = [
    ('prod-main-banner-1600x740', (1600,740), 1280, None, None),
    ('prod-box-342x482', (342,482), 290, None, (483,0,1189,941)),
    ('prod-galaxy-background-2560x670', (2560,670), None, None, None),
    ('key-art-layered-2560x1440', (2560,1440), 1940, 115, None),
]
for name,size,width,top,crop in specs:
    result,layers = layout(size,width,top,crop)
    out = HERE / (name+'.png')
    result.convert('RGB').save(out,optimize=True)
    treatment = dict(fit='centered aspect-preserving crop and Lanczos resample', source_crop=crop,
                     title_width=width,title_top=top if top is not None else 'centered')
    record(out,size,treatment)
    if width:
        psd = PSDImage.new('RGBA',size)
        for label,im in layers:
            PixelLayer.frompil(im,psd,label)
        path = HERE / (name+'.psd')
        psd.save(path)
        check = PSDImage.open(path)
        assert len(check)==3 and check.size==size
        difference = ImageChops.difference(check.composite().convert('RGB'),result.convert('RGB'))
        # PSD compositor and Pillow alpha rounding can differ by one code value.
        assert max(hi for lo,hi in difference.getextrema()) <= 1
        record(path,size,treatment,[layer.name for layer in check])

# The template's red prod_bg board shares the Galaxy source, with 15 bottom
# pixels excluded by its own artboard bounds. Do not invent a second crop.
bg = Image.open(HERE/'prod-galaxy-background-2560x670.png').crop((0,0,2560,655))
path=HERE/'prod-bg-2560x655.png'; bg.save(path,optimize=True)
record(path,bg.size,dict(source='prod-galaxy-background-2560x670.png',crop=[0,0,2560,655]))
logo = Image.new('RGBA',(1600,740))
# Keep the true 900x131 cropped wordmark pixels, centered with no upscaling.
logo.alpha_composite(mark,((1600-900)//2,(740-131)//2))
path=HERE/'prod-logo-1600x740.png';logo.save(path,optimize=True)
record(path,logo.size,dict(source_crop=list(CROP),paste=[350,304],resampling='none; native 900x131 visible raster'))
manifest=dict(prepared='2026-10-31',status='Locally visually reviewed 2026-10-31; not uploaded or portal-accepted',
 source='../../epic-v5/colony-native.png',source_dimensions=list(scene.size),source_sha256=sha(SCENE),
 logo_source='../../epic-v5/product-logo-960x540.png',logo_source_sha256=sha(LOGO),logo_source_crop=list(CROP),
 template_url='https://items.gog.com/templates/gog_art_assets.zip',
 template_sha256='50222fd566382488f2b7888ece1c0ae5596bf84d73b86600be229a587c9a2468',
 qualification='Promotional artwork, not gameplay. Raster source is 1672x941, visible logo 900x131. Larger canvases resample those sources; no native-high-resolution/vector or independently editable colony elements claimed.',
 images=records)
(HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
