#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "playwright==1.63.0",
#   "pillow==13.0.0",
#   "fonttools==4.68.0",
#   "brotli==1.2.1",
# ]
# ///
"""Render the trailer's on-screen text as transparent full-frame PNG cards.

usage: uv run render_cards.py --locale en[,ja,ar|all] --out DIR [--size 3840x2160[,1920x1080,1080x1920]]

For every locale and frame size this writes DIR/<locale>/<WxH>/<field>.png for the
fields named in trailer.json ("text.fields": trailer_line_1..4 and
trailer_line_ai_coplay, read from translations/<locale>.md) and one
DIR/wordmark-<WxH>.png. build_trailer.py lays the cards over the text-free cut
(each output size gets the cards rendered at its own size).

A line that needs two lines and holds two sentences breaks between them; a card whose
two lines split a sentence is reported as a problem. Fields in "text.top_fields" are
laid out at the top of landscape frames ("text.landscape_top").

Text is laid out and drawn by headless Chromium (HarfBuzz shaping, ICU bidi), with
the caption tool's fonts (../../tools/fonts.json, fetched by ../../tools/fetch_fonts.py)
at heavy weights, and Nunito from the design system for locales whose lines it
covers. The wordmark is the game's menu wordmark (menu-wordmark.png) keyed into two
masks and coloured cream and gold, as the design system does with its smaller masks.
"""
import argparse
import base64
import hashlib
import io
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = Path(os.environ.get("GLOB2_MARKETING") or HERE.parents[3])
CAPTION_TOOLS = REPO / "assets" / "storefront-v2" / "tools"
FONT_CACHE = CAPTION_TOOLS / ".cache" / "fonts"
DESIGN_SYSTEM = Path(os.environ.get("GLOB2_DESIGN_SYSTEM") or REPO.parent / "glob2-design-system")
GAME = Path(os.environ.get("GLOB2_GAME") or REPO.parent / "glob2")
ORIGIN = "http://cards.invalid"
CHROMIUM_ARGS = ["--force-color-profile=srgb", "--disable-lcd-text", "--font-render-hinting=none",
                 "--run-all-compositor-stages-before-draw"]


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def catalog(locale):
    """Fields of translations/<locale>.md: '## key' headings followed by the value."""
    text = (REPO / "translations" / f"{locale}.md").read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r"^## ([a-z0-9_]+)\n\n(.*?)(?=\n## |\Z)", text, re.S | re.M):
        out[m.group(1)] = m.group(2).strip()
    return out


def all_locales():
    plat = json.loads((REPO / "translations" / "platforms.json").read_text())
    found = sorted(p.stem for p in (REPO / "translations").glob("*.md")
                   if p.stem not in ("README", "glossary", "media-audit", "storefront-v2-field-map"))
    listed = plat.get("locales")
    if isinstance(listed, dict):
        listed = list(listed)
    return [c for c in (listed or found) if (REPO / "translations" / f"{c}.md").exists()]


class Fonts:
    def __init__(self, style):
        from fontTools.ttLib import TTFont
        self.config = json.loads((CAPTION_TOOLS / "fonts.json").read_text())
        self.style = style
        self.files = {name: FONT_CACHE / font["file"] for name, font in self.config["fonts"].items()}
        self.files["Nunito"] = DESIGN_SYSTEM / "assets" / "nunito.woff2"
        missing = [str(p) for p in self.files.values() if not p.exists()]
        if missing:
            raise SystemExit("missing fonts (run ../../tools/fetch_fonts.py; set GLOB2_DESIGN_SYSTEM): " + ", ".join(missing))
        self.cmaps = {}
        self._ttfont = TTFont

    def covers(self, family, text):
        if family not in self.cmaps:
            self.cmaps[family] = set(self._ttfont(self.files[family], lazy=True).getBestCmap())
        return all(ord(c) in self.cmaps[family] or c in "​‌‍‎‏ \n" for c in text)

    def plan(self, locale, texts):
        """Font stack and metrics for a locale; every line of a locale uses the same font."""
        name = self.config["locale_profiles"].get(locale, self.config["default_profile"])
        profile = self.config["profiles"][name]
        heavy = self.style["weights"]
        if name == self.config["default_profile"]:
            joined = "".join(texts)
            for family in self.style["latin_stack"]:
                if self.covers(family, joined):
                    return {"profile": name, "stack": [family], "weight": heavy.get(family, heavy["default"]),
                            "size": self.style["latin_size"].get(family, 1.0), "line_height": 1.14,
                            "dir": "ltr", "letter_spacing": "0"}
            raise SystemExit(f"{locale}: no single font in {self.style['latin_stack']} covers its trailer lines")
        return {"profile": name, "stack": profile["stack"], "weight": heavy.get(profile["stack"][0], heavy["default"]),
                "size": profile.get("size", 1.0), "line_height": profile.get("line_height", 1.2),
                "dir": profile.get("dir", "ltr"), "word_break": profile.get("word_break")}

    def face_css(self):
        rules = []
        for family, path in self.files.items():
            variable = "[" in path.name or family == "Nunito"
            rules.append(f"@font-face {{ font-family: '{family}'; src: url('/fonts/{family.replace(' ', '_')}'); "
                         f"font-weight: {'100 1000' if variable else '400'}; font-style: normal; font-display: block; }}")
        return "\n".join(rules)


def wordmark_masks():
    """Key the game's menu wordmark (dark green letters, gold 2, cream paper) into two alpha masks."""
    from PIL import Image
    src = GAME / "content" / "data" / "gfx" / "menu-wordmark.png"
    im = Image.open(src).convert("RGB")
    w, h = im.size
    px = im.load()
    paper = px[4, 4]
    green = min((px[x, y] for x in range(0, w, 7) for y in range(0, h, 7)), key=lambda c: c[0] + c[2])
    gold = max((px[x, y] for x in range(0, w, 7) for y in range(0, h, 7)), key=lambda c: c[0] - c[2])
    letters = Image.new("L", (w, h))
    two = Image.new("L", (w, h))
    lp, tp = letters.load(), two.load()
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            a = (paper[0] - r) / max(1, paper[0] - green[0])          # red falls only on the green letters
            c = (paper[2] - b) / max(1, paper[2] - gold[2]) - a * (paper[2] - green[2]) / max(1, paper[2] - gold[2])
            lp[x, y] = max(0, min(255, round((a - 0.06) / 0.88 * 255)))
            tp[x, y] = max(0, min(255, round((c - 0.06) / 0.88 * 255)))
    lb, tb = letters.getbbox(), two.getbbox()
    box = (min(lb[0], tb[0]), min(lb[1], tb[1]), max(lb[2], tb[2]), max(lb[3], tb[3]))
    pad = 12
    box = (max(0, box[0] - pad), max(0, box[1] - pad), min(w, box[2] + pad), min(h, box[3] + pad))
    out = []
    for mask in (letters.crop(box), two.crop(box)):
        rgba = Image.new("RGBA", mask.size, (255, 255, 255, 0))
        rgba.putalpha(mask)
        buf = io.BytesIO()
        rgba.save(buf, "PNG")
        out.append("data:image/png;base64," + base64.b64encode(buf.getvalue()).decode())
    return out[0], out[1], (box[2] - box[0], box[3] - box[1]), sha256(src)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--locale", default="en")
    ap.add_argument("--out", required=True)
    ap.add_argument("--size", default="3840x2160")
    ap.add_argument("--data", default=str(HERE / "trailer.json"))
    ap.add_argument("--no-wordmark", action="store_true")
    args = ap.parse_args()
    data = json.loads(Path(args.data).read_text())
    style = data["text"]
    locales = all_locales() if args.locale == "all" else args.locale.split(",")
    sizes = [tuple(int(v) for v in s.split("x")) for s in args.size.split(",")]
    fonts = Fonts(style)
    out = Path(args.out)

    from playwright.sync_api import sync_playwright
    report = {"tool": {n: sha256(HERE / n) for n in ("render_cards.py", "cards.html")}, "cards": [], "wordmark": {}}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=CHROMIUM_ARGS)
        report["chromium"] = browser.version
        page = browser.new_page(viewport={"width": 800, "height": 600}, device_scale_factor=1)

        def serve(route):
            path = route.request.url[len(ORIGIN):]
            if path == "/cards.html":
                route.fulfill(status=200, content_type="text/html; charset=utf-8", body=(HERE / "cards.html").read_bytes())
            elif path.startswith("/fonts/") and path[7:].replace("_", " ") in fonts.files:
                route.fulfill(status=200, content_type="font/ttf", body=fonts.files[path[7:].replace("_", " ")].read_bytes())
            else:
                route.abort()
        page.route("**/*", serve)
        page.goto(ORIGIN + "/cards.html")
        page.evaluate('css => { document.getElementById("faces").textContent = css; }', fonts.face_css())
        problems = []
        masks = None
        for w, h in sizes:
            page.set_viewport_size({"width": w, "height": h})
            portrait = h > w
            lay = style["portrait" if portrait else "landscape"]
            base = round(lay["size"] * (w if portrait else h))
            if not args.no_wordmark:
                masks = masks or wordmark_masks()
                letters, two, (mw, mh), src_hash = masks
                mark_w = round(lay["wordmark_width"] * w)
                page.evaluate("o => setWordmark(o)", {"w": w, "h": h, "ink": style["ink"], "accent": style["accent"],
                                                       "markW": mark_w, "markH": round(mark_w * mh / mw),
                                                       "letters": letters, "two": two})
                path = out / f"wordmark-{w}x{h}.png"
                path.parent.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(path), omit_background=True)
                report["wordmark"][f"{w}x{h}"] = {"file": path.name, "source_sha256": src_hash, "sha256": sha256(path)}
            for locale in locales:
                cat = catalog(locale)
                missing = [f for f in style["fields"] if not cat.get(f)]
                if missing:
                    problems.append(f"{locale}: missing {missing}")
                    continue
                plan = fonts.plan(locale, [cat[f] for f in style["fields"]])
                for field in style["fields"]:
                    # A field listed in top_fields is laid out at the top of a landscape frame
                    # (the desktop co-play line: the Hive card sits at the bottom left).
                    top = not portrait and field in style.get("top_fields", [])
                    fl = dict(lay, **style["landscape_top"]) if top else lay
                    fit = page.evaluate("o => setCard(o)", {
                        "w": w, "h": h, "ink": style["ink"], "accent": style["accent"], "top": top,
                        "scrimH": round(fl["scrim_height"] * h), "centreY": round(fl["centre_y"] * h),
                        "maxW": round(lay["max_width"] * w), "text": cat[field], "lang": locale, "dir": plan["dir"],
                        "stack": plan["stack"], "weight": plan["weight"], "size": round(base * plan["size"]),
                        "lineHeight": plan["line_height"], "letterSpacing": plan.get("letter_spacing"),
                        "wordBreak": plan.get("word_break"),
                        "oneLineFloor": lay["one_line_floor"], "twoLineFloor": lay["two_line_floor"],
                        "ruleW": style["rule"]["width"], "ruleH": style["rule"]["height"], "ruleGap": style["rule"]["gap"]})
                    if fit.get("failed"):
                        problems.append(f"{locale} {field} {w}x{h}: does not fit")
                        continue
                    path = out / locale / f"{w}x{h}" / f"{field}.png"
                    path.parent.mkdir(parents=True, exist_ok=True)
                    page.screenshot(path=str(path), omit_background=True)
                    # Two sentences on two lines must break between the sentences ("No ads. /
                    # No in-app purchases."), never inside one.
                    sentences = [s for s in re.split(r"\s+" if locale == "th" else r"(?<=[.!?。！？।۔؟])\s*",
                                                     cat[field]) if s]
                    split_inside = (len(sentences) == 2 and fit["lines"] == 2 and
                                    [s.replace(" ", "") for s in fit["line_texts"]] !=
                                    [s.replace(" ", "") for s in sentences])
                    if split_inside:
                        problems.append(f"{locale} {field} {w}x{h}: two sentences split inside one: {fit['line_texts']}")
                    report["cards"].append({"locale": locale, "size": f"{w}x{h}", "field": field, "text": cat[field],
                                            "font": plan["stack"][0], "weight": plan["weight"], "dir": plan["dir"],
                                            "placement": "top" if top else "bottom",
                                            "font_px": fit["px"], "scale": round(fit["scale"], 2), "lines": fit["lines"],
                                            "line_texts": fit["line_texts"], "sentence_break": fit["sentence_break"],
                                            "file": str(path.relative_to(out)), "sha256": sha256(path)})
                    print(f"{locale:8} {w}x{h} {field:24} {plan['stack'][0]:22} {fit['px']:4}px "
                          f"{fit['lines']} line(s)  {' / '.join(fit['line_texts'])}")
        browser.close()
    (out / "cards.json").write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
