#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "playwright==1.63.0",
#   "pillow==13.0.0",
#   "fonttools==4.68.0",
#   "brotli==1.2.1",
# ]
# ///
"""Turn raw gameplay captures into captioned store screenshots for every language.

    uv run screenshots.py render --locale en            # every store set, English
    uv run screenshots.py render --locale all           # every locale in translations/platforms.json
    uv run screenshots.py fit --locale all              # preflight: fit every caption, write nothing
    uv run screenshots.py fit --locale ja --min-scale 0.85   # legibility gate for caption editors
    uv run screenshots.py verify --locale all
    uv run screenshots.py contact-sheet --locale en

gallery.json maps each store set to a device class and each device class to its ordered
slots (capture file + caption role); captures/mobile/selection.json replaces those slots
when it exists. Caption text is read from translations/<locale>.md (shot_overlay_<role>).
The capture is trimmed of flat system-bar margins, scaled down (never up) and composited by
Pillow; headless Chromium draws only the brand background and the caption, so HarfBuzz
shapes every script and the capture's pixels never pass through a browser. See README.md.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
from importlib.metadata import version as package_version
import io
import json
import os
from pathlib import Path
import re
import sys
import unicodedata

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
TRANSLATIONS = REPO / 'translations'
FONT_CACHE = HERE / '.cache' / 'fonts'
ORIGIN = 'http://caption.invalid'
NAME_PATTERN = re.compile(r'^\d\d-[a-z_]+-\d+x\d+\.(png|jpg)$')

sys.path.insert(0, str(TRANSLATIONS / 'tools'))
import storefront  # noqa: E402  (the catalog parser; not modified here)

# ---------------------------------------------------------------------------------------
# Design. Colours are the design system's Night colony tokens (glob2-design-system
# tokens/dark.json). Per image size, gallery.json gives the card width ('card', share of the image
# width), the caption band ('band', share of the image height) and the caption's full type size
# ('caption_px'). Below, 'radius' is a fraction of the image's shorter side, 'ring' and 'pad_x' of
# the image width, 'pad_y' of the band height. 'two_max' and 'two_min' bound a two-line caption and
# 'one_floor' a one-line caption, as fractions of the full size.
VARIANTS = {
    # Cream heading on aubergine, the card edged in translucent cream so its top reads against the HUD.
    'night': {
        'background': 'radial-gradient(130% 62% at 50% 0%, #34234f 0%, #2b1c42 38%, #1b1229 100%)',
        'ink': '#f9e8bb', 'ring': 'rgba(249, 232, 187, 0.6)', 'ring_scale': 1, 'shadow': 'rgba(8, 4, 16, 0.55)',
    },
    # The fair-deal slide: the same night, the caption and a double-width ring in the action gold.
    'gold': {
        'background': 'radial-gradient(130% 62% at 50% 0%, #34234f 0%, #2b1c42 38%, #1b1229 100%)',
        'ink': '#e3c077', 'ring': '#e3c077', 'ring_scale': 2, 'shadow': 'rgba(8, 4, 16, 0.55)',
    },
}
LAYOUTS = {
    # The capture as a card fitted to the image width, running off the bottom edge; caption band above.
    'framed': {
        'portrait': {'radius': 0.028, 'ring': 0.004, 'shadow': True, 'pad_x': 0.04, 'pad_y': 0.06,
                     'two_max': 1.0, 'two_min': 0.62, 'one_floor': 0.68},
        'landscape': {'radius': 0.026, 'ring': 0.004, 'shadow': True, 'pad_x': 0.04, 'pad_y': 0.10,
                      'two_max': 0.64, 'two_min': 0.48, 'one_floor': 0.60},
    },
}
INK_MARGIN_X = 0.03    # caption ink must stay this far (of image width) from the left and right edges
INK_MARGIN_Y = 0.05    # and this far (of band height) from the band's top and bottom
RADIUS_CAP = 40        # px: card corners stay small so they never bite into a HUD element drawn in the corner
SHRINK = 0.97          # when measured ink leaves the band, every caption of the set and locale shrinks by this step
KEEP_CLAUSE = 0.95     # a set gives up at most 5% of its type size to keep a caption broken between clauses
# sRGB output, plain grey anti-aliasing, whole-tile raster; the last three flags make a screenshot
# wait until every tile of the page has been rastered.
CHROMIUM_ARGS = ['--force-color-profile=srgb', '--disable-lcd-text', '--font-render-hinting=none', '--disable-partial-raster',
                 '--run-all-compositor-stages-before-draw', '--disable-checker-imaging', '--disable-new-content-rendering-timeout']
# Chromium re-rasters only what changed, and after many captions a few anti-aliased pixels of the
# card's ring can differ by a few levels from the first capture. Ink is therefore whatever differs
# from the empty band by more than this, and only the ink's own rectangle is taken from the capture.
INK_THRESHOLD = 32
REPORT_SETS = ('apple-iphone-6.9', 'google-play-phone')  # the phone-portrait sets `fit` reports on; the first is the tightest
CLAUSE_END = re.compile(r'[,.;:!?\u060c\u061b\u06d4\u0964] ')  # as caption.html's clause break
SMALL_SCALE = 0.85     # `fit` marks a caption set below this share of full size as SMALL
STABLE_TRIES = 6       # captures allowed before two consecutive screenshots must agree
JPEG_QUALITY = 95


class Problem(Exception):
    """A caption or input the tool refuses to turn into an image."""


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    return sha256_bytes(Path(path).read_bytes())


def repo_path(path):
    path = Path(path).resolve()
    return path.relative_to(REPO).as_posix() if path.is_relative_to(REPO) else path.name


# ---------------------------------------------------------------------------------------
# Configuration and selection
# ---------------------------------------------------------------------------------------
def read_gallery(gallery, platforms):
    """Ordered slots per device class: from the capture engineer's selection file when it exists,
    otherwise gallery.json's provisional_gallery in the order of asset_text.mobile_gallery_order in
    translations/platforms.json. Returns ({device_class: [{'capture', 'role'}]}, source)."""
    path = (HERE / gallery['selection_file']).resolve()
    needed = sorted({store_set['device_class'] for store_set in gallery['store_sets'].values()})
    if not path.is_file():
        order = platforms['asset_text'].get('mobile_gallery_order', [])
        rank = lambda slot: order.index(slot['role']) if slot['role'] in order else len(order)
        return ({name: sorted(gallery['provisional_gallery'][name], key=rank) for name in needed},
                {'file': 'assets/storefront-v2/tools/gallery.json', 'key': 'provisional_gallery', 'order': order})
    try: data = json.loads(path.read_text(encoding='utf-8'))
    except ValueError as error: raise Problem(f'{path}: {error}')
    for key in ('device_classes', 'galleries', 'gallery', 'selection'):
        if isinstance(data, dict) and isinstance(data.get(key), dict): data = data[key]
    result, problems = {}, []
    for name in needed:
        entry = data.get(name) if isinstance(data, dict) else None
        if isinstance(entry, dict):
            entry = next((entry[key] for key in ('slots', 'gallery', 'portrait', 'landscape') if isinstance(entry.get(key), list)), None)
        if not isinstance(entry, list) or not entry:
            problems.append(f'{path.name}: no ordered slot list for device class {name!r}')
            continue
        slots = []
        for index, item in enumerate(entry, 1):
            capture = role = None
            if isinstance(item, dict):
                capture = next((item[key] for key in ('capture', 'file', 'capture_file', 'image') if isinstance(item.get(key), str)), None)
                role = next((item[key] for key in ('role', 'caption_role', 'caption') if isinstance(item.get(key), str)), None)
            elif isinstance(item, list) and len(item) >= 2 and all(isinstance(value, str) for value in item[:2]):
                capture, role = item[:2]
            if not capture or not role: problems.append(f'{path.name}: {name} slot {index} needs a capture file name and a caption role, got {item!r}')
            else:
                slots.append({'capture': capture, 'role': role})
                # Optional per-slot trim mode (see resolve_trim_modes), with its reason.
                if isinstance(item, dict) and 'trim' in item:
                    slots[-1]['selection_trim'] = {'trim': item['trim'], 'why': item.get('trim_why')}
        result[name] = slots
    if problems:
        raise Problem('\n'.join(problems) + '\nexpected: {"<device class>": [{"capture": "<file in captures/mobile/<device class>/>", "role": "<hero|build|...>"}, ...]}')
    return result, {'file': repo_path(path), 'sha256': sha256_file(path)}


def load_config():
    gallery = json.loads((HERE / 'gallery.json').read_text())
    fonts = json.loads((HERE / 'fonts.json').read_text())
    platforms = json.loads((TRANSLATIONS / 'platforms.json').read_text())
    assets = platforms['asset_text']
    problems = []
    if gallery['layout'] not in LAYOUTS: problems.append(f'gallery.json: unknown layout {gallery["layout"]!r}')
    for name, store_set in gallery['store_sets'].items():
        if store_set['store'] not in gallery['stores']: problems.append(f'{name}: unknown store {store_set["store"]!r}')
        if store_set['device_class'] not in gallery['device_classes']: problems.append(f'{name}: unknown device class {store_set["device_class"]!r}')
    if problems: raise Problem('\n'.join(problems))
    gallery['slots'], gallery['gallery_source'] = read_gallery(gallery, platforms)
    order = assets.get('mobile_gallery_order', [])
    for device_class, slots in gallery['slots'].items():
        seen = set()
        for index, slot in enumerate(slots, 1):
            where = f'{gallery["gallery_source"]["file"]}: {device_class} slot {index}'
            if slot['role'] not in assets['screenshot_roles']: problems.append(f'{where}: unknown role {slot["role"]!r}; roles are {assets["screenshot_roles"]}')
            elif slot['role'] in assets.get('desktop_only_roles', []): problems.append(f'{where}: role {slot["role"]!r} is desktop-only and these are mobile store sets')
            elif slot['role'] not in order: problems.append(f'{where}: role {slot["role"]!r} is not in asset_text.mobile_gallery_order in translations/platforms.json {order}, so it is not a mobile slide')
            if slot['role'] in seen: problems.append(f'{where}: role {slot["role"]!r} appears twice')
            seen.add(slot['role'])
        # The store order is asset_text.mobile_gallery_order; a class may leave a role out (iPhone has no territory slide).
        roles = [slot['role'] for slot in slots]
        if roles != [role for role in order if role in roles]:
            problems.append(f'{gallery["gallery_source"]["file"]}: {device_class} slots are {roles}; they must follow asset_text.mobile_gallery_order {order}')
            path = capture_path(gallery, device_class, slot)
            if not path.is_file(): problems.append(f'{where}: missing capture {path}')
            elif not path.is_relative_to((HERE / gallery['captures_root']).resolve()): problems.append(f'{where}: {slot["capture"]} is outside the captures directory')
    resolve_trim_modes(gallery, problems)
    for store in gallery['stores'].values():
        for rule in store['banned']:
            if rule not in gallery['banned']: problems.append(f'gallery.json: store refers to unknown banned list {rule!r}')
    for locale, profile in fonts['locale_profiles'].items():
        if profile not in fonts['profiles']: problems.append(f'fonts.json: {locale} uses unknown profile {profile!r}')
    for name, profile in fonts['profiles'].items():
        for family in profile['stack']:
            if family not in fonts['fonts']: problems.append(f'fonts.json: profile {name} uses unknown font {family!r}')
    if problems: raise Problem('\n'.join(problems))
    return gallery, fonts, platforms


def capture_path(gallery, device_class, slot):
    root = HERE / gallery['captures_root']
    # A bare file name lives in its device class's folder; a path is taken from the captures root.
    return (root / slot['capture'] if '/' in slot['capture'] else root / device_class / slot['capture']).resolve()


# How the system-bar strips of a capture are handled. Every slot uses 'flat-margins' unless gallery.json's
# slot_trim (or a "trim" key on the slot in selection.json) names another mode for that capture, with a reason.
TRIM_MODES = {
    'flat-margins': 'trims the size\'s configured system-bar strips only where each strip is a flat margin; refuses otherwise',
    'status-bar': 'trims exactly the size\'s configured top strip (the iOS status bar) although it is not flat, because the capture '
                  'runs background art under the clock and battery; trims nothing else, so the bottom runs off the image edge untrimmed',
}
FLAT_SHARE = 0.9  # 'flat-margins': at least this share of a trimmed strip must be one colour


def resolve_trim_modes(gallery, problems):
    """Give every slot its trim mode: 'flat-margins' (the strict default), or the mode gallery.json's slot_trim
    or the slot in selection.json names for that capture. A non-default mode needs a reason; an entry may pin
    the capture's sha256 so that a re-captured file falls back to being decided again."""
    overrides = gallery.get('slot_trim', {})
    for device_class, entries in overrides.items():
        if device_class not in gallery['device_classes']: problems.append(f'gallery.json slot_trim: unknown device class {device_class!r}')
        named = {slot['capture'] for slot in gallery['slots'].get(device_class, [])}
        for capture in entries:
            if capture not in named: problems.append(f'gallery.json slot_trim: {device_class}/{capture} is not in the gallery; remove the stale entry')
    for device_class, slots in gallery['slots'].items():
        for index, slot in enumerate(slots, 1):
            where = f'{device_class} slot {index} ({slot["capture"]})'
            chosen = overrides.get(device_class, {}).get(slot['capture'])
            from_selection = slot.pop('selection_trim', None)
            if chosen and from_selection and from_selection['trim'] != chosen.get('trim'):
                problems.append(f'{where}: selection.json asks for trim {from_selection["trim"]!r} but gallery.json slot_trim says {chosen.get("trim")!r}')
            entry = chosen or from_selection or {'trim': 'flat-margins'}
            mode = entry.get('trim')
            slot['trim_mode'] = mode
            slot['trim_why'] = entry.get('why')
            slot['trim_source'] = 'gallery.json slot_trim' if chosen else gallery['gallery_source']['file'] if from_selection else 'default'
            if mode not in TRIM_MODES:
                problems.append(f'{where}: unknown trim mode {mode!r}; modes are {sorted(TRIM_MODES)}')
                continue
            if mode == 'flat-margins': continue
            if not slot['trim_why']: problems.append(f'{where}: trim {mode!r} needs a reason ("why") saying what the strip holds')
            sizes = gallery['device_classes'][device_class]
            if not all(spec.get('trim', {}).get('top') for spec in sizes.values()):
                problems.append(f'{where}: trim {mode!r} needs a configured top (status-bar) trim for {device_class} in device_classes')
            pinned = (chosen or {}).get('sha256')
            path = capture_path(gallery, device_class, slot)
            if pinned and path.is_file() and sha256_file(path) != pinned:
                problems.append(f'{where}: the capture changed since its trim {mode!r} was decided (sha256 pinned in gallery.json slot_trim); '
                                'look at its top strip again and update or remove the entry')


def slot_trim(spec, slot):
    """The pixels to trim from each edge of this slot's capture, as {edge: px}."""
    if slot.get('trim_mode', 'flat-margins') == 'status-bar':
        return {'top': spec['trim']['top']}
    return dict(spec.get('trim', {}))


def strip_shares(image, trim):
    """{edge: share of the strip taken by its most common colour} for each trimmed edge."""
    width, height = image.size
    boxes = {'left': (0, 0, trim.get('left', 0), height), 'top': (0, 0, width, trim.get('top', 0)),
             'right': (width - trim.get('right', 0), 0, width, height), 'bottom': (0, height - trim.get('bottom', 0), width, height)}
    shares = {}
    for edge, box in boxes.items():
        if not trim.get(edge): continue
        strip = image.crop(box)
        colours = strip.getcolors(maxcolors=strip.width * strip.height)
        shares[edge] = round(max(count for count, _ in colours) / (strip.width * strip.height), 4)
    return shares


def check_trims(gallery, names):
    """Before anything is rendered: every slot of every device class used by these store sets, with its trim
    mode, the pixels it trims and how flat each strip is. Returns (rows, problems)."""
    from PIL import Image
    rows, problems, seen = [], [], set()
    for name in names:
        device_class = gallery['store_sets'][name]['device_class']
        if device_class in seen: continue
        seen.add(device_class)
        for index, slot, path, canvas, spec in slot_plan(gallery, name):
            with Image.open(path) as image: shares = strip_shares(image.convert('RGB'), slot_trim(spec, slot))
            trim = slot_trim(spec, slot)
            strict = [edge for edge in trim if slot['trim_mode'] == 'flat-margins']
            bad = [edge for edge in strict if shares[edge] < FLAT_SHARE]
            for edge in bad:
                problems.append(f'{device_class} slot {index} ({slot["capture"]}): trimming {trim[edge]}px from the {edge} would remove game pixels '
                                f'(only {shares[edge]:.0%} of that strip is flat margin). If the capture runs background art under the iOS status bar '
                                f'(a menu screen) and its top strip holds only the clock, signal and battery over that art, set "trim": "status-bar" '
                                f'for it in gallery.json slot_trim with the reason; otherwise fix the capture or the size\'s trim')
            rows.append((device_class, index, slot, trim, shares, bad))
    return rows, problems


def capture_descriptions(gallery):
    """{repo path of a capture: its 'kind' ('gameplay', 'menu screen', ...)} from the captures' own manifest.json,
    for files whose bytes still match that manifest; empty when there is none."""
    root = (HERE / gallery['captures_root']).resolve()
    try: files = json.loads((root / 'manifest.json').read_text(encoding='utf-8')).get('files', [])
    except (OSError, ValueError): return {}
    kinds = {}
    for entry in files:
        path = (root / entry.get('file', '')).resolve()
        if entry.get('kind') and path.is_file() and entry.get('sha256') == sha256_file(path): kinds[repo_path(path)] = entry['kind']
    return kinds


def select(args, gallery, platforms):
    """(set names, locales, roles or None) for the command line."""
    sets = gallery['store_sets']
    if args.set == 'all':
        names = list(sets)
    else:
        names = args.set.split(',')
        unknown = [name for name in names if name not in sets]
        if unknown: raise Problem(f'unknown store set {unknown}; choose from {list(sets)}')
    known = platforms['locales']
    if args.locale == 'all':
        locales = list(known)
    else:
        locales = args.locale.split(',')
        unknown = [code for code in locales if code not in known]
        if unknown: raise Problem(f'unknown locale {unknown}; translations/platforms.json lists {known}')
    roles = args.role.split(',') if args.role else None
    return names, locales, roles


def output_name(index, slot, canvas, image_format):
    return f'{index:02d}-{slot["role"]}-{canvas[0]}x{canvas[1]}.{"jpg" if image_format == "jpeg" else "png"}'


def banned_words(gallery, store, locale, text):
    """Reasons this caption may not ship to this store."""
    reasons = []
    for name in gallery['stores'][store]['banned']:
        rule = gallery['banned'][name]
        if rule['locales'] != 'all' and locale not in rule['locales']: continue
        match = re.search(rule['pattern'], text, 0 if rule.get('case_sensitive') else re.I)
        if match: reasons.append(f'banned for {store} ({name}): {match.group(0)!r}')
    return reasons


class Catalogs:
    """Caption text straight from translations/<locale>.md, parsed with translations/tools/storefront.py."""

    def __init__(self, root, platforms):
        self.root = Path(root).resolve()
        self.platforms = platforms
        self.field = platforms['asset_text']['overlay_fields']
        self.cache = {}

    def path(self, locale):
        return self.root / f'{locale}.md'

    def caption(self, locale, role):
        if locale not in self.cache:
            try: self.cache[locale] = storefront.read_fields(self.path(locale))
            except (OSError, ValueError) as error: raise Problem(f'cannot read catalog: {error}')
        key = self.field.format(role=role)
        if key not in self.cache[locale]: raise Problem(f'{self.path(locale).name} has no field {key}')
        text = self.cache[locale][key]
        if '\n' in text: raise Problem(f'{key} spans more than one line')
        # The length limit is whatever translations/platforms.json and storefront.py say it is.
        over = storefront.field_limit_errors(self.platforms, locale, {key: text})
        if over: raise Problem('; '.join(over))
        return key, text


# ---------------------------------------------------------------------------------------
# Geometry and capture preparation (Pillow)
# ---------------------------------------------------------------------------------------
def geometry(canvas, trimmed, spec, layout):
    """Where the capture and the caption go. All values are whole pixels of the output image.

    The card is fitted to spec['card'] of the image width (never scaled up) and starts right under
    the caption band; whatever does not fit runs off the bottom edge."""
    width, height = canvas
    cw, ch = trimmed
    style = LAYOUTS[layout]['portrait' if height >= width else 'landscape']
    unit = min(width, height)
    w = min(cw, round(spec['card'] * width))
    if (width - w) % 2: w += 1 if w < cw else -1  # equal side margins
    scale = w / cw
    scaled_h = ch if w == cw else round(ch * scale)
    band = round(spec['band'] * height)  # the caption band is everything above the capture, full width
    x, y = (width - w) // 2, band
    h = min(scaled_h, height - y)
    full = spec['caption_px']
    return {
        'canvas': [width, height], 'capture': [x, y, w, h], 'scaled': [w, scaled_h], 'scale': round(scale, 6),
        'band': [0, 0, width, band], 'area': round(band / height, 6), 'gameplay': round(w * h / (width * height), 6),
        'radius': min(round(style['radius'] * unit), RADIUS_CAP), 'ring': max(2, round(style['ring'] * width)),
        'shadow': style['shadow'], 'unit': unit,
        'max_width': width - 2 * round(style['pad_x'] * width), 'max_height': band - 2 * round(style['pad_y'] * band),
        'full': full, 'one_floor': round(full * style['one_floor']),
        'two': [round(full * style['two_max']), round(full * style['two_min'])],
    }


def prepare_capture(path, trim, geo, mode='flat-margins'):
    """The capture, trimmed, scaled and cut to its slot, plus the rounded-corner mask it is pasted through.
    In 'flat-margins' mode every trimmed strip must be a flat margin; 'status-bar' trims only the top strip
    and does not ask it to be flat (see TRIM_MODES)."""
    from PIL import Image, ImageDraw
    image = Image.open(path)
    image.load()
    if image.mode == 'RGBA':
        if image.getchannel('A').getextrema() != (255, 255): raise Problem(f'{path.name}: capture has transparent pixels')
        image = image.convert('RGB')
    elif image.mode != 'RGB':
        raise Problem(f'{path.name}: unexpected image mode {image.mode}')
    width, height = image.size
    left, top, right, bottom = (trim.get(key, 0) for key in ('left', 'top', 'right', 'bottom'))
    if mode == 'status-bar' and (left or right or bottom): raise Problem(f'{path.name}: trim mode status-bar trims only the top, got {trim}')
    if mode == 'flat-margins':
        for edge, share in strip_shares(image, trim).items():
            if share < FLAT_SHARE:
                raise Problem(f'{path.name}: trimming {trim[edge]}px from the {edge} would remove game pixels (only {share:.0%} of that strip is flat margin)')
    elif mode not in TRIM_MODES:
        raise Problem(f'{path.name}: unknown trim mode {mode!r}')
    image = image.crop((left, top, width - right, height - bottom))
    x, y, w, h = geo['capture']
    sw, sh = geo['scaled']
    if (sw, sh) != image.size:
        if sw > image.width or sh > image.height: raise Problem(f'{path.name}: refusing to upscale a capture')
        image = image.resize((sw, sh), Image.Resampling.LANCZOS)
    if h < sh: image = image.crop((0, 0, w, h))  # the part below the canvas edge
    mask = None
    if geo['radius']:
        over = 4
        mask = Image.new('L', (w * over, h * over), 0)
        corners = (True, True, y + h < geo['canvas'][1], y + h < geo['canvas'][1])
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, w * over - 1, h * over - 1), geo['radius'] * over, fill=255, corners=corners)
        mask = mask.resize((w, h), Image.Resampling.LANCZOS)
    return image, mask


# ---------------------------------------------------------------------------------------
# Fonts
# ---------------------------------------------------------------------------------------
class Fonts:
    def __init__(self, config):
        self.config = config
        self.cmaps = {}
        self.family_names = {}
        missing = [name for name, font in config['fonts'].items()
                   if not (FONT_CACHE / font['file']).is_file() or sha256_file(FONT_CACHE / font['file']) != font['sha256']]
        if missing: raise Problem(f'fonts missing or changed in {FONT_CACHE}: {missing}\nrun: python3 {HERE.name}/fetch_fonts.py')

    def covers(self, family):
        if family not in self.cmaps:
            from fontTools.ttLib import TTFont
            self.cmaps[family] = set(TTFont(FONT_CACHE / self.config['fonts'][family]['file'], lazy=True).getBestCmap())
        return self.cmaps[family]

    def names(self, family):
        """The family names a bundled font file gives itself (Chromium reports DejaVu Sans Bold as 'DejaVu Sans')."""
        if family not in self.family_names:
            from fontTools.ttLib import TTFont
            table = TTFont(FONT_CACHE / self.config['fonts'][family]['file'], lazy=True)['name']
            self.family_names[family] = {str(record) for record in table.names if record.nameID in (1, 4, 16)}
        return self.family_names[family]

    def plan(self, locale, text):
        """(profile, font stack) for a caption; every character must be in a bundled font."""
        profile = self.config['profiles'][self.config['locale_profiles'].get(locale, self.config['default_profile'])]
        stack = list(profile['stack'])
        needed = {ord(char) for char in text if char != ' ' and unicodedata.category(char) not in ('Cf', 'Cc')}  # no-break spaces need a glyph too
        if profile.get('single_font'):
            # Prefer one font for the whole caption so kerning and rhythm never change mid-word.
            for family in stack:
                if needed <= self.covers(family):
                    stack = [family]
                    break
        missing = sorted(code for code in needed if not any(code in self.covers(family) for family in stack))
        if missing:
            raise Problem('no bundled font has ' + ', '.join(f'U+{code:04X} {chr(code)!r}' for code in missing) + f' (stack: {stack})')
        return profile, stack

    def short_rule(self, locale):
        """The short-word line-break rule for this locale: a two-line caption never ends its first line with a
        word of max_letters letters or fewer, or with a word from the locale's list (fonts.json short_words)."""
        rule = self.config.get('short_words', {})
        own = rule.get('locales', {}).get(locale, {})
        return {'maxLetters': own.get('max_letters', rule.get('max_letters', 0)), 'words': own.get('words', [])}

    def face_css(self):
        rules = []
        for family, font in self.config['fonts'].items():
            # A variable font serves every weight; a static one only its own (DejaVu Sans Bold: 700).
            weight = '100 900' if '[' in font['file'] else str(font.get('weight', 400))
            rules.append(f"@font-face {{ font-family: '{family}'; src: url('/fonts/{font['sha256']}'); "
                         f"font-weight: {weight}; font-style: normal; font-display: block; }}")
        return '\n'.join(rules)


# ---------------------------------------------------------------------------------------
# Caption layer (headless Chromium)
# ---------------------------------------------------------------------------------------
class CaptionLayer:
    def __init__(self, fonts):
        from playwright.sync_api import sync_playwright
        self.fonts = fonts
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(args=CHROMIUM_ARGS)
        self.page = self.browser.new_page(viewport={'width': 800, 'height': 600}, device_scale_factor=1)
        by_hash = {font['sha256']: FONT_CACHE / font['file'] for font in fonts.config['fonts'].values()}

        def serve(route):
            path = route.request.url[len(ORIGIN):]
            if path == '/caption.html':
                route.fulfill(status=200, content_type='text/html; charset=utf-8', body=(HERE / 'caption.html').read_bytes())
            elif path.startswith('/fonts/') and path[7:] in by_hash:
                route.fulfill(status=200, content_type='font/ttf', body=by_hash[path[7:]].read_bytes())
            else:
                route.abort()
        self.page.route('**/*', serve)
        self.page.goto(ORIGIN + '/caption.html')
        self.page.evaluate('css => { document.getElementById("faces").textContent = css; }', fonts.face_css())
        self.cdp = self.page.context.new_cdp_session(self.page)
        self.cdp.send('DOM.enable')
        self.cdp.send('CSS.enable')
        self.loaded = set()
        self.state = None
        self.bases = {}
        self.unstable_frames = 0
        self.version = self.browser.version
        self.self_test()

    def close(self):
        self.browser.close()
        self.playwright.stop()

    def self_test(self):
        """A flat brand colour must come back as exactly that colour (no display colour management)."""
        from PIL import Image
        self.page.set_viewport_size({'width': 64, 'height': 64})
        self.page.evaluate('vars => setCanvas(vars)', {'--w': '64px', '--h': '64px', '--background': '#1b1229', '--card-w': '0px', '--card-h': '0px', '--card-shadow': 'none'})
        self.state = None
        pixel = Image.open(io.BytesIO(self.page.screenshot(type='png'))).convert('RGB').getpixel((32, 32))
        if pixel != (0x1b, 0x12, 0x29): raise Problem(f'Chromium returned {pixel} for #1b1229; colour management is altering output')

    def set_canvas(self, geo, variant):
        key = (json.dumps(geo, sort_keys=True), variant)
        if self.state == key: return key
        colours = VARIANTS[variant]
        width, height = geo['canvas']
        x, y, w, h = geo['capture']
        radius = f'{geo["radius"]}px'
        if y + h >= height: radius = f'{geo["radius"]}px {geo["radius"]}px 0 0'
        shadow = []
        if geo['ring']: shadow.append(f'0 0 0 {geo["ring"] * colours["ring_scale"]}px {colours["ring"]}')
        if geo['shadow']: shadow.append(f'0 {round(0.022 * geo["unit"])}px {round(0.07 * geo["unit"])}px {colours["shadow"]}')
        self.page.set_viewport_size({'width': width, 'height': height})
        self.page.evaluate('vars => setCanvas(vars)', {
            '--w': f'{width}px', '--h': f'{height}px', '--background': colours['background'],
            '--ink': colours['ink'], '--ring': colours['ring'],
            '--card-x': f'{x}px', '--card-y': f'{y}px', '--card-w': f'{w}px', '--card-h': f'{h}px',
            '--card-radius': radius, '--card-shadow': ', '.join(shadow) or 'none',
            '--band-x': '0px', '--band-y': '0px', '--band-w': f'{geo["band"][2]}px', '--band-h': f'{geo["band"][3]}px',
        })
        # A resize repaints asynchronously; do not screenshot a stale frame.
        settled = self.page.evaluate('''size => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(() =>
            resolve(window.innerWidth === size[0] && window.innerHeight === size[1]))))''', [width, height])
        if not settled: raise Problem(f'Chromium viewport did not settle at {width}x{height}')
        self.state = key
        return key

    def stable_screenshot(self, clip=None):
        """A screenshot that two consecutive captures agree on, as an RGB image."""
        from PIL import Image
        options = {'type': 'png', 'clip': clip} if clip else {'type': 'png'}
        previous = self.page.screenshot(**options)
        for _ in range(STABLE_TRIES):
            current = self.page.screenshot(**options)
            if current == previous: return Image.open(io.BytesIO(current)).convert('RGB')
            self.unstable_frames += 1
            previous = current
        raise Problem(f'Chromium did not produce a stable frame in {STABLE_TRIES} captures')

    def base(self, geo, variant):
        """The whole image without caption or capture: background, card ring and shadow."""
        key = self.set_canvas(geo, variant)
        if key not in self.bases:
            self.page.evaluate('document.body.classList.add("no-text")')
            self.bases[key] = self.stable_screenshot()
            if self.bases[key].size != tuple(geo['canvas']): raise Problem(f'Chromium returned {self.bases[key].size} for a {geo["canvas"]} canvas')
            self.page.evaluate('document.body.classList.remove("no-text")')
        return self.bases[key]

    @staticmethod
    def full_size(geo, profile):
        """The caption's full type size in px for this image size and script."""
        return round(geo['full'] * profile.get('size', 1.0))

    @staticmethod
    def fit_request(geo, profile, stack, locale, text, short=None):
        """What caption.html's measureCaption and setCaption need to lay one caption out. `short` is the
        locale's short-word line-break rule ({'maxLetters', 'words'}; see short_rule)."""
        full = CaptionLayer.full_size(geo, profile)
        one_floor = round(geo['one_floor'] / geo['full'] * full)
        if 'one_line_floor' in profile: one_floor = min(one_floor, round(full * profile['one_line_floor']))
        return {
            'text': text, 'lang': locale, 'dir': profile.get('dir', 'ltr'),
            'family': ', '.join(f'"{family}"' for family in stack), 'weight': profile.get('weight', 400),
            'letterSpacing': profile.get('letter_spacing', '0'), 'lineHeight': profile.get('line_height', 1.16),
            'wordBreak': profile.get('word_break', 'normal'), 'lineBreak': profile.get('line_break', 'auto'),
            'shift': profile.get('shift', 0), 'wrap': profile.get('wrap', 'free'),
            'short': short or {'maxLetters': 0, 'words': []},
            'maxWidth': geo['max_width'], 'maxHeight': geo['max_height'],
            'one': {'max': full, 'floor': one_floor},
            'two': {'max': round(geo['two'][0] / geo['full'] * full), 'min': round(geo['two'][1] / geo['full'] * full)},
        }

    def load_fonts(self, stack, weight):
        for family in stack:
            if (family, weight) in self.loaded: continue
            spec = f'{weight} 40px "{family}"'
            self.page.evaluate('spec => document.fonts.load(spec)', spec)
            if not self.page.evaluate('spec => document.fonts.check(spec)', spec):
                raise Problem(f'font {family!r} failed to load in Chromium')
            self.loaded.add((family, weight))

    def measure(self, geo, variant, locale, text):
        """(largest size in px at which this caption fits the band in at most two lines, its full size,
        largest size on one line, largest size broken between clauses); 0 where a way does not fit."""
        profile, stack = self.fonts.plan(locale, text)
        self.base(geo, variant)
        self.load_fonts(stack, profile.get('weight', 400))
        fit = self.page.evaluate('request => measureCaption(request)', self.fit_request(geo, profile, stack, locale, text, self.fonts.short_rule(locale)))
        if not fit['ok']: raise Problem(fit['reason'])
        return fit['size'], self.full_size(geo, profile), fit['one'], fit['clause']

    def caption(self, geo, variant, locale, text, size):
        """Shape and render one caption at exactly `size` px. Returns (ink patch, its top-left corner in
        the image, details), or None when the measured ink leaves the band and its margins."""
        from PIL import ImageChops
        profile, stack = self.fonts.plan(locale, text)
        base = self.base(geo, variant)
        self.load_fonts(stack, profile.get('weight', 400))
        band = geo['band']
        clip = {'x': band[0], 'y': band[1], 'width': band[2], 'height': band[3]}
        blank = base.crop((band[0], band[1], band[0] + band[2], band[1] + band[3]))
        margin_x, margin_y = round(INK_MARGIN_X * geo['canvas'][0]), round(INK_MARGIN_Y * band[3])
        fit = self.page.evaluate('args => setCaption(args[0], args[1])', [self.fit_request(geo, profile, stack, locale, text, self.fonts.short_rule(locale)), size])
        if not fit['ok']: raise Problem(fit['reason'])
        rendered = self.rendered_fonts()
        for font in rendered:
            # Chromium names a variable font after its default instance ("Noto Sans JP Thin"); map it back.
            matches = [family for family in stack if font['familyName'].startswith(family) or font['familyName'] in self.fonts.names(family)]
            if not font['isCustomFont'] or not matches:
                raise Problem(f'Chromium drew {font["glyphCount"]} glyph(s) with {font["familyName"]!r}, which is not one of the bundled fonts {stack}')
            font['family'] = max(matches, key=len)
        layer = self.stable_screenshot(clip)
        red, green, blue = ImageChops.difference(layer, blank).split()
        ink = ImageChops.lighter(ImageChops.lighter(red, green), blue).point(lambda value: 255 if value >= INK_THRESHOLD else 0).getbbox()
        if ink is None: raise Problem('caption rendered no ink')
        if not (ink[0] >= margin_x and ink[2] <= band[2] - margin_x and ink[1] >= margin_y and ink[3] <= band[3] - margin_y): return None
        squeeze = lambda value: re.sub(r'[ \u200b]', '', value)
        if squeeze(''.join(fit['lines'])) != squeeze(text):
            raise Problem(f'laid-out lines {fit["lines"]} do not reproduce the caption text')
        # Take the ink's rectangle, with room for the faint edge of the anti-aliasing, and nothing else.
        pad = max(8, round(0.25 * fit['size']))
        box = (max(0, ink[0] - pad), max(0, ink[1] - pad), min(band[2], ink[2] + pad), min(band[3], ink[3] + pad))
        patch, corner = layer.crop(box), (band[0] + box[0], band[1] + box[1])
        details = {
            'text': text, 'lines': fit['lines'], 'fit': fit['wrap'], 'font_size': fit['size'],
            **({'short_word_letters': fit['level']} if fit['wrap'] in ('safe', 'relaxed', 'loose') else {}),
            'full_size': self.full_size(geo, profile), 'direction': profile.get('dir', 'ltr'), 'font_weight': profile.get('weight', 400),
            'fonts': [{'family': font['family'], 'glyphs': font['glyphCount']} for font in rendered],
            'font_stack': stack, 'variant': variant, 'rect': band, 'ink': [ink[0] + band[0], ink[1] + band[1], ink[2] + band[0], ink[3] + band[1]],
            'area': geo['area'],
        }
        return patch, corner, details

    def rendered_fonts(self):
        root = self.cdp.send('DOM.getDocument', {'depth': 0})['root']['nodeId']
        node = self.cdp.send('DOM.querySelector', {'nodeId': root, 'selector': '#text'})['nodeId']
        return sorted(self.cdp.send('CSS.getPlatformFontsForNode', {'nodeId': node})['fonts'], key=lambda font: font['familyName'])


# ---------------------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------------------
def tool_fingerprint(layer=None):
    info = {name: sha256_file(HERE / name) for name in ('screenshots.py', 'caption.html', 'gallery.json', 'fonts.json')}
    info['pillow'] = package_version('pillow')
    info['playwright'] = package_version('playwright')
    if layer: info['chromium'] = layer.version
    return info


def encode(image, path, image_format):
    if image_format == 'jpeg':
        image.save(path, 'JPEG', quality=JPEG_QUALITY, subsampling=0, optimize=True)
    else:
        image.save(path, 'PNG', compress_level=9)
    return path


def slot_plan(gallery, name):
    """Per slot of a store set: (index, slot, capture path, canvas size, layout spec for that size)."""
    from PIL import Image
    device_class = gallery['store_sets'][name]['device_class']
    for index, slot in enumerate(gallery['slots'][device_class], 1):
        path = capture_path(gallery, device_class, slot)
        with Image.open(path) as probe: canvas = probe.size
        spec = gallery['device_classes'][device_class].get(f'{canvas[0]}x{canvas[1]}')
        if spec is None:
            raise Problem(f'{name}: {slot["capture"]} is {canvas[0]}x{canvas[1]}, which is not a store size configured for {device_class} '
                          f'({sorted(gallery["device_classes"][device_class])}); add it to device_classes in gallery.json with its trim and band')
        yield index, slot, path, canvas, spec


def render(args):
    gallery, fonts_config, platforms = load_config()
    names, locales, roles = select(args, gallery, platforms)
    layout = args.layout or gallery['layout']
    out_root = Path(args.out).resolve() if args.out else (HERE / gallery['output_root']).resolve()
    catalogs = Catalogs(args.translations or TRANSLATIONS, platforms)
    # Every slot's system-bar trim is checked before any caption is set, so a refused strip stops the run
    # at once instead of after hours of other locales.
    _, trim_problems = check_trims(gallery, names)
    if trim_problems: raise Problem('\n'.join(trim_problems))
    described = capture_descriptions(gallery)
    fonts = Fonts(fonts_config)
    layer = CaptionLayer(fonts)
    fingerprint = tool_fingerprint(layer)
    failures, notes, written = [], [], 0
    dry = args.command == 'fit'
    fitted = []  # (store set, locale, slot, role, caption details or None, problem or None, own size or None), for the fit report
    pool = ThreadPoolExecutor(max_workers=args.jobs)
    try:
        for name in names:
            store_set = gallery['store_sets'][name]
            image_format = store_set.get('format', 'png')
            manifests = {locale: [] for locale in locales}
            failed = set()
            pending = []
            # Every slot of the set: its layout and, when writing, the capture composited onto the background.
            slots = []
            for index, slot, path, canvas, spec in slot_plan(gallery, name):
                trim = slot_trim(spec, slot)
                trimmed = (canvas[0] - trim.get('left', 0) - trim.get('right', 0), canvas[1] - trim.get('top', 0) - trim.get('bottom', 0))
                geo = geometry(canvas, trimmed, spec, layout)
                if geo['area'] > gallery['caption_area_limit']:
                    raise Problem(f'{name} {canvas[0]}x{canvas[1]}: caption band is {geo["area"]:.1%} of the image; the limit is {gallery["caption_area_limit"]:.0%}')
                slots.append({'index': index, 'slot': slot, 'path': path, 'canvas': canvas, 'trim': trim, 'geo': geo,
                              'variant': gallery['role_variants'].get(slot['role'], 'night'), 'render': not roles or slot['role'] in roles})
            for locale in locales:
                # 1. The largest size each caption of this locale can take; every slide uses the smallest of
                #    them. With --role, the other roles still count, so the size matches the full set.
                texts, sizes = {}, {}
                for item in slots:
                    role = item['slot']['role']
                    try:
                        key, text = catalogs.caption(locale, role)
                        reasons = banned_words(gallery, store_set['store'], locale, text)
                        if reasons: raise Problem('; '.join(reasons))
                        texts[role] = (key, text)
                        sizes[role] = layer.measure(item['geo'], item['variant'], locale, text)
                    except Problem as problem:
                        if not item['render']: continue
                        failures.append(f'{name} / {locale} / {role}: {problem}')
                        failed.add(locale)
                        fitted.append((name, locale, item['index'], role, None, str(problem), None))
                # 2. Set every caption at that size. If one caption's ink leaves the band (tall marks the
                #    font metrics did not promise), that caption's own size steps down and all are set again.
                captions, problems = {}, {}
                # own: the largest size each caption allows. A caption that has a clause break ("No ads, /
                # no in-app purchases") but would be broken inside a clause at the set's size allows only
                # its clause break's size, if that costs the set at most 1 - KEEP_CLAUSE of its size.
                largest = min((size for size, *_ in sizes.values()), default=None)
                own = {role: clause if largest and one < largest and KEEP_CLAUSE * largest <= clause < largest else size
                       for role, (size, full, one, clause) in sizes.items()}
                uniform = min(own.values(), default=None)
                while uniform:
                    captions, problems, outside = {}, {}, None
                    for item in slots:
                        role = item['slot']['role']
                        if not item['render'] or role not in sizes: continue
                        try:
                            result = layer.caption(item['geo'], item['variant'], locale, texts[role][1], uniform)
                        except Problem as problem:
                            problems[item['index'], role] = str(problem)
                            continue
                        if result is None:
                            outside = role
                            break
                        captions[role] = result
                    if not outside: break
                    if uniform * SHRINK < 0.4 * min(full for _, full, *_ in sizes.values()):
                        problems[0, '(all)'] = f'caption ink does not stay inside the band with its margins, even at {uniform}px'
                        captions = {}
                        break
                    # That caption cannot be set at this size after all; the report names it as the limit.
                    own[outside] = int(uniform * SHRINK)
                    uniform = min(own.values())
                for (index, role), problem in problems.items():
                    failures.append(f'{name} / {locale} / {role}: {problem}')
                    failed.add(locale)
                    fitted.append((name, locale, index, role, None, problem, None))
                for item in slots:
                    role = item['slot']['role']
                    if role not in captions: continue
                    patch, corner, caption = captions[role]
                    caption['own_size'] = own[role]
                    fitted.append((name, locale, item['index'], role, caption, None, own[role]))
                    if caption['fit'] in ('relaxed', 'loose'):
                        notes.append(f'{name} / {locale} / {role}: {" | ".join(caption["lines"])}  ({caption["font_size"]}px, the short-word rule was '
                                     + (f'relaxed to words of {caption["short_word_letters"]} letters or fewer' if caption['fit'] == 'relaxed' else 'dropped')
                                     + ': no break that keeps every short word off the end of the first line fits; check the break, '
                                     'and put a U+200B where it should go or reword if it reads badly)')
                    elif caption['fit'] not in ('none', 'hint', 'clause', 'safe'):
                        notes.append(f'{name} / {locale} / {role}: {" | ".join(caption["lines"])}  ({caption["font_size"]}px, line break by the {caption["fit"]!r} rule)')
                    elif caption['fit'] == 'safe' and CLAUSE_END.search(caption['text']):
                        notes.append(f'{name} / {locale} / {role}: {" | ".join(caption["lines"])}  ({caption["font_size"]}px, broken inside a clause: '
                                     'the break after the punctuation does not fit at the set\'s size)')
                    if dry:
                        written += 1
                        continue
                    if 'composed' not in item:
                        capture, mask = prepare_capture(item['path'], item['trim'], item['geo'], item['slot']['trim_mode'])
                        item['capture_hash'] = sha256_file(item['path'])
                        from PIL import Image
                        with Image.open(item['path']) as source: item['trim_shares'] = strip_shares(source.convert('RGB'), item['trim'])
                        item['composed'] = layer.base(item['geo'], item['variant']).copy()
                        item['composed'].paste(capture, tuple(item['geo']['capture'][:2]), mask)
                    image = item['composed'].copy()
                    image.paste(patch, corner)
                    target = out_root / name / locale / output_name(item['index'], item['slot'], item['canvas'], image_format)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    pending.append((pool.submit(encode, image, target, image_format), locale))
                    caption['field'] = texts[role][0]
                    geo = item['geo']
                    manifests[locale].append({
                        'file': target.name, 'slot': item['index'], 'role': role, 'pixels': f'{item["canvas"][0]}x{item["canvas"][1]}', 'format': image_format,
                        'capture': {'file': repo_path(item['path']), 'sha256': item['capture_hash'],
                                    **({'kind': described[repo_path(item['path'])]} if repo_path(item['path']) in described else {}),
                                    'trim': item['trim'], 'trim_mode': item['slot']['trim_mode'], 'trim_rule': TRIM_MODES[item['slot']['trim_mode']],
                                    'trim_flat_share': item['trim_shares'],
                                    **({'trim_why': item['slot']['trim_why'], 'trim_decided_in': item['slot']['trim_source']} if item['slot']['trim_why'] else {}),
                                    'placed': geo['capture'], 'scaled': geo['scaled'], 'scale': geo['scale'], 'corner_radius': geo['radius'],
                                    'gameplay_share': geo['gameplay']},
                        'caption': caption,
                    })
                    if len(pending) >= args.jobs * 3:
                        for future, _ in pending: future.result()
                        pending.clear()
            for future, _ in pending: future.result()
            for locale in locales:
                folder = out_root / name / locale
                if not dry and locale in failed:
                    # No partial sets: drop what this run wrote for the locale, and its manifest.
                    for entry in manifests[locale]: (folder / entry['file']).unlink(missing_ok=True)
                    (folder / 'manifest.json').unlink(missing_ok=True)
                if dry or locale in failed or not manifests[locale]: continue
                for entry in manifests[locale]:
                    data = (folder / entry['file']).read_bytes()
                    entry['sha256'], entry['bytes'] = sha256_bytes(data), len(data)
                    if len(data) > gallery['stores'][store_set['store']]['max_bytes']:
                        failures.append(f'{name} / {locale} / {entry["role"]}: {entry["file"]} is {len(data):,} bytes; the {store_set["store"]} ceiling is {gallery["stores"][store_set["store"]]["max_bytes"]:,} (set "format": "jpeg" on the store set)')
                catalog = catalogs.path(locale)
                manifest = {
                    'generated_by': 'assets/storefront-v2/tools/screenshots.py', 'tool': fingerprint,
                    'store_set': name, 'store': store_set['store'], 'device_class': store_set['device_class'], 'locale': locale,
                    'layout': layout, 'partial': bool(roles), 'gallery': gallery['gallery_source'],
                    'catalog': {'file': repo_path(catalog), 'sha256': sha256_file(catalog), 'in_repository': catalog.is_relative_to(REPO)},
                    'fonts': {family: {'file': font['file'], 'sha256': font['sha256'], 'licence': font['licence']} for family, font in fonts_config['fonts'].items()
                              if any(family in entry['caption']['font_stack'] for entry in manifests[locale])},
                    'images': manifests[locale],
                }
                (folder / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
                if not roles:
                    keep = {entry['file'] for entry in manifests[locale]}
                    for stale in folder.iterdir():
                        if NAME_PATTERN.match(stale.name) and stale.name not in keep: stale.unlink()
                written += len(manifests[locale])
            done = [locale for locale in locales if locale not in failed]
            print(f'{name}: {len(done)} locale(s) {"fit" if dry else "rendered"}' + (f', {len(failed)} failed' if failed else ''), flush=True)
    finally:
        pool.shutdown()
        layer.close()
    small = fit_report(fitted, names, locales, gallery, platforms, args.min_scale) if dry else []
    if layer.unstable_frames: print(f'note: Chromium returned {layer.unstable_frames} unsettled frame(s); each was captured again until two captures agreed')
    if notes:
        print(f'\n{len(notes)} caption(s) worth a look (a fallback line break, a short word left at a line end, or a break inside a clause):')
        for note in notes: print('  ' + note)
    print(f'{written} captions fit' if dry else f'{written} images in {out_root}')
    if failures:
        print(f'\n{len(failures)} caption(s) could not be rendered' + ('' if dry else '; nothing was written for those locales') + ':', file=sys.stderr)
        for failure in failures: print('  ' + failure, file=sys.stderr)
    gated = small if args.min_scale is not None else []
    if gated:
        print(f'\n{len(gated)} caption(s) below --min-scale {args.min_scale:g} on the phone sets:', file=sys.stderr)
        for line in gated: print('  ' + line, file=sys.stderr)
    return 1 if failures or gated else 0


def overlay_limits(platforms, locale):
    """(limit, target or None) for shot_overlay captions in this locale, from translations/platforms.json."""
    pattern = platforms['asset_text']['overlay_fields'].format(role='*')
    for rule in platforms.get('field_limits', []):
        if rule['fields'] != pattern: continue
        for group in rule.get('script_groups', {}).values():
            if locale in group.get('locales', []): return group.get('limit', rule['limit']), group.get('target')
        return rule['limit'], None
    return None, None


def fit_report(fitted, names, locales, gallery, platforms, min_scale):
    """Print every caption as it would be set on the two phone-portrait sets, the tightest first.

    Every caption of a store set and locale is set at one size (the largest at which all of them
    fit), so each line shows that size. SMALL marks the captions that, on their own, could not be set
    at the threshold: they are the ones holding the whole set below it, and shortening them raises
    every slide. Returns those captions (below min_scale, or below SMALL_SCALE when no minimum was asked for)."""
    reported = [name for name in REPORT_SETS if name in names] or list(names)
    # A set that shares a reported set's captures (fdroid-phone) would only repeat its lines.
    same_layout = {name for name in names if gallery['store_sets'][name]['device_class'] in {gallery['store_sets'][other]['device_class'] for other in reported}}
    threshold = SMALL_SCALE if min_scale is None else min_scale
    percent = lambda scale: int(scale * 100 + 1e-9)
    small = []
    for locale in locales:
        limit, target = overlay_limits(platforms, locale)
        print(f'\n{locale}: caption type size as a share of full size, one size per store set'
              + (f' (limit {limit} characters' + (f', target {target}' if target else '') + ')' if limit else ''))
        for name in reported:
            rows = sorted((row for row in fitted if row[0] == name and row[1] == locale), key=lambda row: row[2])
            set_rows = [row for row in rows if row[4]]
            uniform = min((row[4]['font_size'] / row[4]['full_size'] for row in set_rows), default=None)
            limiting = {row[3] for row in set_rows if row[6] / row[4]['full_size'] < threshold - 1e-9}
            if uniform is not None and uniform < threshold - 1e-9 and not limiting:
                limiting = {min(set_rows, key=lambda row: row[6])[3]}
            print(f'  {name}' + (' (tightest)' if name == REPORT_SETS[0] else '')
                  + (f': every caption at {percent(uniform)}%' if uniform is not None and len(set_rows) == len(rows) else ''))
            for _, _, _, role, caption, problem, own in rows:
                if caption is None:
                    print(f'    {role:<10} FAILED         {problem}')
                    continue
                scale = caption['font_size'] / caption['full_size']
                is_small = role in limiting
                count = len(caption['lines'])
                print(f'    {role:<10} {percent(scale):>3}%  {"SMALL" if is_small else "     "}  {count} line{"s" if count > 1 else " "}  '
                      f'{len(caption["text"]):>2} chars  {" / ".join(caption["lines"])}'
                      + (f'  (on its own {percent(own / caption["full_size"])}%)' if is_small else ''))
                if is_small: small.append(f'{name} / {locale} / {role}: {percent(own / caption["full_size"])}% on its own, so every caption is set at {percent(scale)}%  {" / ".join(caption["lines"])}')
        others = [(row[4]['font_size'] / row[4]['full_size'], row[0], row[6] / row[4]['full_size'], row[3]) for row in fitted
                  if row[1] == locale and row[0] not in same_layout and row[4]]
        if others:
            scale, name, _, role = min(others)
            print(f'  tablet sets, for information: smallest {percent(scale)}% ({name}, set by {role})')
    return small


def verify(args):
    from PIL import Image, ImageChops, ImageStat
    gallery, fonts_config, platforms = load_config()
    names, locales, roles = select(args, gallery, platforms)
    out_root = Path(args.out).resolve() if args.out else (HERE / gallery['output_root']).resolve()
    catalogs = Catalogs(args.translations or TRANSLATIONS, platforms)
    errors, checked = [], 0
    current = tool_fingerprint()
    for name in names:
        store_set = gallery['store_sets'][name]
        store = gallery['stores'][store_set['store']]
        image_format = store_set.get('format', 'png')
        for locale in locales:
            folder = out_root / name / locale
            where = f'{name} / {locale}'
            try: manifest = json.loads((folder / 'manifest.json').read_text(encoding='utf-8'))
            except (OSError, ValueError) as error: errors.append(f'{where}: no readable manifest ({error})'); continue
            layout = manifest['layout']
            for key in ('screenshots.py', 'caption.html', 'gallery.json', 'fonts.json'):
                if manifest['tool'].get(key) != current[key]: errors.append(f'{where}: rendered with a different {key}; render again')
            entries = {entry['file']: entry for entry in manifest['images']}
            expected = set()
            for index, slot, path, canvas, spec in slot_plan(gallery, name):
                if roles and slot['role'] not in roles: continue
                file_name = output_name(index, slot, canvas, image_format)
                expected.add(file_name)
                here = f'{where} / {file_name}'
                entry = entries.get(file_name)
                target = folder / file_name
                if entry is None or not target.is_file(): errors.append(f'{here}: missing'); continue
                checked += 1
                data = target.read_bytes()
                # File: untouched since render, within the store's size ceiling.
                if sha256_bytes(data) != entry['sha256']: errors.append(f'{here}: file changed since it was rendered')
                if len(data) > store['max_bytes']: errors.append(f'{here}: {len(data):,} bytes exceeds the {store_set["store"]} ceiling of {store["max_bytes"]:,}')
                # Pixels: exact store size, 24-bit, no alpha.
                image = Image.open(io.BytesIO(data))
                if image.size != canvas: errors.append(f'{here}: {image.size[0]}x{image.size[1]}, expected {canvas[0]}x{canvas[1]}')
                if image.mode != 'RGB' or 'transparency' in image.info: errors.append(f'{here}: mode {image.mode} (alpha or palette); stores need 24-bit RGB')
                if image.format != ('JPEG' if image_format == 'jpeg' else 'PNG'): errors.append(f'{here}: format {image.format}')
                # Caption: the catalog's current text, within the field limit, no banned words, band within the area limit.
                caption = entry['caption']
                try:
                    key, text = catalogs.caption(locale, slot['role'])
                    if caption['text'] != text: errors.append(f'{here}: caption {caption["text"]!r} is not the catalog text {text!r}')
                except Problem as problem:
                    errors.append(f'{here}: {problem}')
                errors.extend(f'{here}: {reason}' for reason in banned_words(gallery, store_set['store'], locale, caption['text']))
                band = caption['rect']
                area = band[2] * band[3] / (canvas[0] * canvas[1])
                if area > gallery['caption_area_limit']: errors.append(f'{here}: caption band is {area:.1%} of the image; the limit is {gallery["caption_area_limit"]:.0%}')
                ink = caption['ink']
                if not (ink[0] >= band[0] and ink[1] >= band[1] and ink[2] <= band[0] + band[2] and ink[3] <= band[1] + band[3]):
                    errors.append(f'{here}: caption ink {ink} leaves the band {band}')
                # Capture: same input file, same slot, and its pixels sit in the output exactly where the manifest says.
                capture = entry['capture']
                if entry['role'] != slot['role'] or capture['file'] != repo_path(path): errors.append(f'{here}: the gallery now maps this slot to {slot["capture"]} / {slot["role"]}; render again')
                elif sha256_file(path) != capture['sha256']: errors.append(f'{here}: the capture file changed since it was rendered')
                elif capture.get('trim_mode', 'flat-margins') != slot['trim_mode'] or capture.get('trim') != slot_trim(spec, slot):
                    errors.append(f'{here}: rendered with trim {capture.get("trim_mode", "flat-margins")} {capture.get("trim")}, '
                                  f'the gallery now asks for {slot["trim_mode"]} {slot_trim(spec, slot)}; render again')
                elif image.size == canvas and image.mode == 'RGB':
                    trim = slot_trim(spec, slot)
                    trimmed = (canvas[0] - trim.get('left', 0) - trim.get('right', 0), canvas[1] - trim.get('top', 0) - trim.get('bottom', 0))
                    geo = geometry(canvas, trimmed, spec, layout)
                    if geo['capture'] != capture['placed'] or geo['band'] != band: errors.append(f'{here}: layout differs from the manifest')
                    else:
                        x, y, w, h = geo['capture']
                        if y < band[1] + band[3]: errors.append(f'{here}: capture overlaps the caption band')
                        try: source, mask = prepare_capture(path, trim, geo, slot['trim_mode'])
                        except Problem as problem: errors.append(f'{here}: {problem}'); continue
                        inset = geo['radius']  # compare inside the rounded corners
                        box = (inset, inset, w - inset, h - inset)
                        difference = ImageChops.difference(source.crop(box), image.crop((x + inset, y + inset, x + w - inset, y + h - inset)))
                        worst = max(high for _, high in difference.getextrema())
                        mean = sum(ImageStat.Stat(difference).mean) / 3
                        if (image_format == 'png' and worst != 0) or (image_format == 'jpeg' and mean > 2.0):
                            errors.append(f'{here}: gameplay pixels differ from the capture (max {worst}, mean {mean:.2f})')
            extra = sorted(item.name for item in folder.iterdir() if NAME_PATTERN.match(item.name) and item.name not in expected) if not roles else []
            if extra: errors.append(f'{where}: files not in gallery.json: {extra}')
            sizes = sorted({entry['caption']['font_size'] for entry in manifest['images']})
            if len(sizes) > 1: errors.append(f'{where}: captions use {len(sizes)} type sizes {sizes}; a store set and locale uses one')
    if errors:
        print(f'{len(errors)} problem(s) in {out_root}:', file=sys.stderr)
        for error in errors: print('  ' + error, file=sys.stderr)
        return 1
    print(f'verified {checked} images in {out_root}: exact store pixel size, 24-bit without alpha, caption band within {gallery["caption_area_limit"]:.0%}, '
          'caption text equals the catalog, one caption size per set and locale, no banned words, under the size ceiling, gameplay pixels equal the capture')
    return 0


def contact_sheet(args):
    """One JPEG per store set and locale: the gallery in order at thumbnail size, as a store strip shows it."""
    from PIL import Image
    gallery, _, platforms = load_config()
    names, locales, _ = select(args, gallery, platforms)
    out_root = Path(args.out).resolve() if args.out else (HERE / gallery['output_root']).resolve()
    for name in names:
        for locale in locales:
            folder = out_root / name / locale
            files = sorted(item for item in folder.iterdir() if NAME_PATTERN.match(item.name)) if folder.is_dir() else []
            if not files: print(f'{name} / {locale}: nothing rendered', file=sys.stderr); return 1
            thumbs = []
            for item in files:
                image = Image.open(item).convert('RGB')
                scale = args.height / image.height
                thumbs.append(image.resize((round(image.width * scale), args.height), Image.Resampling.LANCZOS))
            gap = 24
            sheet = Image.new('RGB', (gap + sum(thumb.width + gap for thumb in thumbs), args.height + 2 * gap), '#17171c')
            x = gap
            for thumb in thumbs:
                sheet.paste(thumb, (x, gap))
                x += thumb.width + gap
            target = out_root / name / f'contact-sheet-{locale}.jpg'
            sheet.save(target, 'JPEG', quality=88, optimize=True)
            print(target)
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('command', choices=['render', 'fit', 'verify', 'contact-sheet', 'check-config'])
    parser.add_argument('--locale', default='en', help='one locale, a comma-separated list, or "all" (default: en)')
    parser.add_argument('--set', default='all', help='one store set, a comma-separated list, or "all" (default)')
    parser.add_argument('--role', help='only these caption roles (comma-separated); leaves other files alone and marks the manifest partial')
    parser.add_argument('--out', help='output root (default: assets/storefront-v2/store-screenshots)')
    parser.add_argument('--translations', help='directory of <locale>.md catalogs (default: translations/); for test strings')
    parser.add_argument('--layout', choices=sorted(LAYOUTS), help='override gallery.json layout')
    parser.add_argument('--min-scale', type=float, help='fit only: exit non-zero if a caption on the phone sets is set below this share of full size (for example 0.85)')
    parser.add_argument('--jobs', type=int, default=max(2, min(8, (os.cpu_count() or 4) - 2)), help='PNG encoder threads')
    parser.add_argument('--height', type=int, default=640, help='contact-sheet thumbnail height')
    args = parser.parse_args()
    try:
        if args.command in ('render', 'fit'): return render(args)
        if args.command == 'verify': return verify(args)
        if args.command == 'contact-sheet': return contact_sheet(args)
        gallery, _, platforms = load_config()
        print(f'gallery from {gallery["gallery_source"]["file"]}; {len(platforms["locales"])} locales')
        for name, store_set in gallery['store_sets'].items():
            print(f'  {name}: ' + ', '.join(f'{index:02d} {slot["role"]} <- {slot["capture"]} ({canvas[0]}x{canvas[1]})' for index, slot, _, canvas, _ in slot_plan(gallery, name)))
        # Dry run of the system-bar trim for every slot of every device class, as render will do it.
        rows, problems = check_trims(gallery, list(gallery['store_sets']))
        print('\nsystem-bar trim per slot (share of each trimmed strip that is one flat colour):')
        for device_class, index, slot, trim, shares, bad in rows:
            strips = ', '.join(f'{edge} {trim[edge]}px {shares[edge]:.0%} flat' for edge in trim) or 'nothing to trim'
            print(f'  {device_class} {index:02d} {slot["role"]:<10} {slot["trim_mode"]:<12} {strips}' + ('  REFUSED' if bad else '')
                  + (f'\n      why ({slot["trim_source"]}): {slot["trim_why"]}' if slot['trim_why'] else ''))
        if problems:
            print(f'\n{len(problems)} slot(s) would stop render:', file=sys.stderr)
            for problem in problems: print('  ' + problem, file=sys.stderr)
            return 1
        return 0
    except Problem as problem:
        print(f'error: {problem}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
