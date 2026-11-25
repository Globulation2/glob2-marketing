# /// script
# requires-python = ">=3.10"
# dependencies = ["pillow==11.3.0", "resvg-py==0.5.0"]
# ///
"""Assemble and verify the storefront-v2 upload package for every store.

    uv run assets/storefront-v2/store-packages/build.py            # build all, then verify
    uv run assets/storefront-v2/store-packages/build.py verify     # re-check what is on disk
    uv run assets/storefront-v2/store-packages/build.py --store snap,itch

Everything is data: stores.json (rules, slots, file names), the review's
"Final galleries" tables (order and per-store selection), the desktop
selection.json, the mobile render manifests, platforms.json switches and locale
maps, and a fresh `storefront.py export` for captions and listing text.

Large files go to output_root (outside the repository). The repository gets one
manifest per store in manifests/. Exit status: 0 clean, 1 errors (a store rule
is broken or a file does not match its manifest), 2 pending items only (inputs
the review asked to change have not changed yet; pass --allow-pending to accept).
Blocked slots (trailer URLs that need a hosted video, Amazon screenshots) are reported but never fail.
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
CONFIG = HERE / "stores.json"
MANIFESTS = HERE / "manifests"
TOKEN_RE = re.compile(r"`(\d{2}[a-z]?)`")


# ---------------------------------------------------------------- helpers

def rp(p: str | Path) -> Path:
    p = Path(p)
    return p if p.is_absolute() else (REPO / p).resolve()


def rel(p: Path) -> str:
    """Repository-relative path, or a symbolic one for the configured outside roots."""
    p = Path(os.path.abspath(p))
    for name, root in ROOTS.items():
        try:
            return f"{name}:{p.relative_to(root).as_posix()}"
        except ValueError:
            pass
    try:
        return p.relative_to(REPO).as_posix()
    except ValueError:
        return p.as_posix()


ROOTS: dict[str, Path] = {}
CFG: dict = {}
MS_MISMATCH: list[str] = []


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def image_info(path: Path) -> dict:
    with Image.open(path) as im:
        alpha = im.mode in ("RGBA", "LA", "PA", "RGBa") or (im.mode == "P" and "transparency" in im.info) \
            or "transparency" in im.info
        return {"size": list(im.size), "format": im.format, "mode": im.mode, "alpha": bool(alpha)}


def save_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


class Report:
    def __init__(self):
        self.errors: list[str] = []
        self.pending: list[str] = []
        self.blocked: list[str] = []
        self.notes: list[str] = []

    def store(self, name):
        return StoreReport(self, name)


class StoreReport:
    def __init__(self, parent: Report, name: str):
        self.parent, self.name = parent, name
        self.errors, self.pending, self.blocked, self.notes = [], [], [], []

    def _add(self, kind, msg):
        getattr(self, kind).append(msg)
        getattr(self.parent, kind).append(f"{self.name}: {msg}")

    def error(self, m): self._add("errors", m)
    def pend(self, m): self._add("pending", m)
    def block(self, m): self._add("blocked", m)
    def note(self, m): self._add("notes", m)


# ---------------------------------------------------------------- review tables

def table_rows(text: str, heading: str, after: str = "## Final galleries") -> list[list[str]]:
    lines = text.splitlines()
    base = next((i for i, l in enumerate(lines) if l.strip() == after), None)
    if base is None:
        raise SystemExit(f"review: no '{after}' section")
    start = next((i for i, l in enumerate(lines) if i > base and l.startswith(f"### {heading}")), None)
    if start is None:
        raise SystemExit(f"review: no '### {heading}' section")
    rows = []
    for line in lines[start + 1:]:
        if line.startswith("#"):
            break
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(set(c) <= set("-: ") for c in cells):
            continue
        rows.append(cells)
    return rows[1:]  # drop the header row


def parse_review(path: Path, roles: list[str]) -> dict:
    text = path.read_text(encoding="utf-8")
    desktop, mobile = {}, {}
    for cells in table_rows(text, "Desktop"):
        name = re.sub(r"\s*\(.*?\)\s*$", "", cells[0].replace("**", "")).strip()
        body = cells[1]
        alias = re.match(r"^As (.+?)\.?$", body.strip())
        if alias:
            desktop[name] = {"alias": alias.group(1).strip(), "raw": body}
        else:
            desktop[name] = {"tokens": TOKEN_RE.findall(body.split(";")[0]), "raw": body}
    # frame-number-to-role pairs the review spells out ("`04` battle"), used to catch renumbered files
    words = {"co-play": "ai_coplay", "coplay": "ai_coplay"}
    token_roles = {}
    for row in desktop.values():
        for tok, word in re.findall(r"`(\d{2}[a-z]?)`\s+([a-z][a-z-]*)", row["raw"]):
            role = words.get(word, word)
            if role in roles:
                token_roles[tok] = role
    for name, row in desktop.items():
        if "alias" in row:
            target = desktop.get(row["alias"])
            if not target or "tokens" not in target:
                raise SystemExit(f"review: desktop row {name!r} says 'As {row['alias']}', which has no list")
            row["tokens"] = list(target["tokens"])
    for cells in table_rows(text, "Mobile"):
        m = re.search(r"\(`([^`]+)`\)", cells[0])
        if not m:
            continue
        body = re.sub(r"\([^)]*\)", "", cells[1].replace("**", ""))
        if "·" not in body:
            # "Same seven as the 10-inch set, after ..." / "Same seven as Google Play phone": the slides of
            # the row whose name contains that phrase, resolved below.
            same = re.match(r"^Same \w+ as (?:the )?(.+?)(?: set)?(?:[,.;]|$)", body.strip())
            mobile[m.group(1)] = {"roles": None, "raw": cells[1], "same_as": same.group(1).strip() if same else None,
                                  "name": cells[0]}
            continue
        found = []
        for part in body.split("·"):
            word = part.strip().lower().replace(" ", "_")
            if word not in roles:
                raise SystemExit(f"review: mobile row {m.group(1)!r} names unknown role {part.strip()!r}")
            found.append(word)
        mobile[m.group(1)] = {"roles": found, "raw": cells[1], "name": cells[0]}
    for key, row in mobile.items():
        if row["roles"] is None and row.get("same_as"):
            matches = [r for k, r in mobile.items() if k != key and r["roles"] and row["same_as"].lower() in r["name"].lower()]
            if len(matches) == 1:
                row["roles"] = list(matches[0]["roles"])
    return {"desktop": desktop, "mobile": mobile, "token_roles": token_roles, "sha256": sha256(path)}


# ---------------------------------------------------------------- inputs

class Inputs:
    def __init__(self, cfg: dict, out: Path, report: Report):
        self.cfg = cfg
        self.out = out
        self.platforms = json.loads(rp(cfg["platforms"]).read_text(encoding="utf-8"))
        roles = self.platforms["asset_text"]["screenshot_roles"]
        self.review = parse_review(rp(cfg["review"]), roles)
        d = cfg["desktop"]
        self.captures = rp(d["captures"])
        self.selection_path = rp(d["selection"])
        self.selection = json.loads(self.selection_path.read_text(encoding="utf-8"))
        self.web1920 = rp(d["web_1920"])
        self.alternatives = d["alternatives"]
        self.desktop_manifest = {e["file"]: e for e in json.loads(rp(d["manifest"]).read_text())["files"]}
        self.key_art = rp(cfg["key_art"]["dir"])
        self.key_art_manifest = {}
        km = rp(cfg["key_art"]["manifest"])
        if km.exists():
            for o in json.loads(km.read_text()).get("outputs", []):
                self.key_art_manifest[Path(o["file"]).name] = o
        self.icon_dir = rp(cfg["icon"]["dir"])
        self.renders = rp(cfg["renders_root"])
        self.export = out / "_export"
        self.report = report
        self.trailer_entries: list[dict] = []

    def run_export(self):
        if self.export.exists():
            shutil.rmtree(self.export)
        cmd = list(self.cfg["export_command"]) + ["--out", str(self.export)]
        r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
        if r.returncode != 0:
            raise SystemExit(f"export failed ({' '.join(cmd)}):\n{r.stdout}\n{r.stderr}")

    def selection_tokens(self) -> list[str]:
        return [e["capture"].split("-", 1)[0] for e in self.selection]

    def capture_for(self, token: str, aspect: str) -> Path | None:
        w, h = self.cfg["desktop"]["aspects"][aspect]
        hits = sorted(self.captures.glob(f"{token}-*-{w}x{h}.png"))
        return hits[0] if len(hits) == 1 else None

    def role_for(self, token: str, sr: StoreReport) -> tuple[str, str | None]:
        if token in self.alternatives:
            a = self.alternatives[token]
            return a["role"], a.get("variant")
        named = self.review["token_roles"].get(token)
        for e in self.selection:
            if e["capture"].startswith(token + "-"):
                if named and named != e["role"]:
                    sr.error(f"review names frame `{token}` {named}, but selection.json gives {e['capture']} the role "
                             f"{e['role']}: were the capture files renumbered? Update the review table or the files")
                return e["role"], None
        f = self.capture_for(token, "16:9")
        role = self.desktop_manifest.get(f.name, {}).get("role") if f else None
        sr.pend(f"review lists frame `{token}`, which captures/desktop/selection.json does not list"
                f" (role taken from the capture manifest: {role})")
        return role or "unknown", None

    def export_listing(self, platform: str, locale_dir: str) -> Path:
        return self.export / platform / locale_dir / "listing.json"

    def switch(self, platform: str | None, name: str) -> bool:
        if platform is None:
            return bool(self.platforms["appstream"]["switches"].get(name, False))
        return bool(self.platforms["platforms"][platform].get("switches", {}).get(name, False))


# ---------------------------------------------------------------- image production

def encode_jpeg(im: Image.Image, cfg: dict, limit: int | None) -> tuple[bytes, int]:
    data, q = b"", None
    for q in cfg["jpeg"]["quality"]:
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=q, subsampling=cfg["jpeg"]["subsampling"], optimize=True)
        data = buf.getvalue()
        if limit is None or len(data) <= limit:
            break
    return data, q


def resized(src: Path, size: list[int]) -> Image.Image:
    with Image.open(src) as im:
        im = im.convert("RGB")
        if list(im.size) == list(size):
            return im.copy()
        if im.size[0] < size[0] or im.size[1] < size[1]:
            raise SystemExit(f"refusing to upscale {src.name} {im.size} to {size}")
        if abs(im.size[0] / im.size[1] - size[0] / size[1]) > 0.002:
            raise SystemExit(f"refusing to change aspect of {src.name} {im.size} to {size}")
        return im.resize(tuple(size), Image.Resampling.LANCZOS)


def render_icon(inp: Inputs, spec: dict) -> bytes:
    size, frac, bg = spec["size"], spec["fraction"], spec.get("background")
    side = round(size * frac)
    if spec["method"] == "vector":
        import resvg_py
        png = resvg_py.svg_to_bytes(svg_string=rp(inp.cfg["icon"]["svg"]).read_text(), width=side, height=side)
        art = Image.open(io.BytesIO(bytes(png))).convert("RGBA")
    else:  # master-resize: the game's own icons.py method
        with Image.open(rp(inp.cfg["icon"]["master"])) as m:
            art = m.convert("RGBa").resize((side, side), Image.Resampling.LANCZOS).convert("RGBA")
    if bg:
        rgb = tuple(int(bg[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
        canvas = Image.new("RGBA", (size, size), rgb)
    else:
        canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    canvas.alpha_composite(art, ((size - side) // 2, (size - side) // 2))
    buf = io.BytesIO()
    (canvas.convert("RGB") if bg else canvas).save(buf, "PNG", optimize=True)
    return buf.getvalue()


# ---------------------------------------------------------------- rules

def rules_for(spec: dict) -> dict:
    keep = ("size", "format", "alpha", "mode", "max_bytes", "min_side", "max_side", "max_size", "aspect_range")
    r = {k: spec[k] for k in keep if k in spec}
    if isinstance(r.get("format"), str):
        r["format"] = [r["format"]]
    return r


def check_file(path: Path, rules: dict, expect_sha: str | None = None, expect_bytes: int | None = None) -> list[str]:
    probs = []
    if not path.exists():
        return [f"{path.name}: missing" + (" (dangling link)" if path.is_symlink() else "")]
    info = image_info(path)
    n = path.stat().st_size
    if expect_bytes is not None and n != expect_bytes:
        probs.append(f"{path.name}: {n} bytes, manifest says {expect_bytes}")
    if expect_sha is not None and sha256(path) != expect_sha:
        probs.append(f"{path.name}: sha256 differs from manifest")
    w, h = info["size"]
    if "size" in rules and [w, h] != list(rules["size"]):
        probs.append(f"{path.name}: {w}x{h}, needs {rules['size'][0]}x{rules['size'][1]}")
    if "format" in rules and info["format"] not in rules["format"]:
        probs.append(f"{path.name}: {info['format']}, needs {'/'.join(rules['format'])}")
    if rules.get("alpha") == "forbid" and info["alpha"]:
        probs.append(f"{path.name}: has an alpha channel ({info['mode']}), store needs none")
    if rules.get("alpha") == "require" and not info["alpha"]:
        probs.append(f"{path.name}: no alpha channel, transparent PNG needed")
    if "mode" in rules and info["mode"] != rules["mode"]:
        probs.append(f"{path.name}: mode {info['mode']}, needs {rules['mode']}")
    if "max_bytes" in rules and n > rules["max_bytes"]:
        probs.append(f"{path.name}: {n:,} bytes, over the {rules['max_bytes']:,}-byte limit")
    if "min_side" in rules and min(w, h) < rules["min_side"]:
        probs.append(f"{path.name}: side under {rules['min_side']}")
    if "max_side" in rules and max(w, h) > rules["max_side"]:
        probs.append(f"{path.name}: side over {rules['max_side']}")
    if "max_size" in rules and (w > rules["max_size"][0] or h > rules["max_size"][1]):
        probs.append(f"{path.name}: over {rules['max_size'][0]}x{rules['max_size'][1]}")
    if "aspect_range" in rules and not (rules["aspect_range"][0] <= w / h <= rules["aspect_range"][1]):
        probs.append(f"{path.name}: aspect {w / h:.3f} outside {rules['aspect_range']}")
    return probs


def entry_for(pkg: Path, dst: Path, rules: dict, **extra) -> dict:
    info = image_info(dst)
    e = {"file": dst.relative_to(pkg).as_posix()}
    e.update(extra)
    e.update({"pixels": f"{info['size'][0]}x{info['size'][1]}", "format": info["format"], "mode": info["mode"],
              "bytes": dst.stat().st_size, "sha256": sha256(dst), "rules": rules})
    return e


# ---------------------------------------------------------------- assets (key art and icons)

def resolve_asset(inp: Inputs, spec: dict) -> Path | None:
    if "icon_file" in spec:
        p = inp.icon_dir / spec["icon_file"]
        return p if p.exists() else None
    cands = spec["file"] if isinstance(spec["file"], list) else [spec["file"]]
    names = sorted(p.name for p in inp.key_art.iterdir()) if inp.key_art.exists() else []
    for c in cands:
        hits = [n for n in names if fnmatch.fnmatch(n, c)]
        if hits:
            return inp.key_art / hits[0]
    return None


def wordmark_margins(inp: Inputs, src: Path) -> dict | None:
    o = inp.key_art_manifest.get(src.name)
    if not o or not o.get("wordmark_box"):
        return None
    x0, y0, x1, y1 = o["wordmark_box"]
    w, h = o["size"]
    return {"left": x0, "top": y0, "right": w - x1, "bottom": h - y1}


def package_assets(inp: Inputs, store: dict, pkg: Path, sr: StoreReport, subdir: str = "") -> list[dict]:
    out = []
    for spec in store.get("assets", []):
        rules = rules_for(spec)
        if "render_icon" in spec:
            data = render_icon(inp, spec["render_icon"])
            ext = "png"
            dst = pkg / subdir / f"{spec['slot']}-{spec['size'][0]}x{spec['size'][1]}.{ext}"
            save_bytes(dst, data)
            how = spec["render_icon"]
            source = {"file": rel(rp(inp.cfg["icon"]["svg"] if how["method"] == "vector" else inp.cfg["icon"]["master"])),
                      "sha256": sha256(rp(inp.cfg["icon"]["svg"] if how["method"] == "vector" else inp.cfg["icon"]["master"])),
                      "treatment": (f"vector rendered at {round(how['size'] * how['fraction'])} px with resvg-py and centred on "
                                    f"{how['background']}" if how["method"] == "vector" else
                                    f"master reduced to {round(how['size'] * how['fraction'])} px (premultiplied Lanczos, "
                                    f"as the game's platforms/mobile/icons.py) on a transparent canvas")}
        else:
            src = resolve_asset(inp, spec)
            if src is None:
                sr.error(f"{spec['slot']}: no source file ({spec.get('file') or spec.get('icon_file')})")
                continue
            info = image_info(src)
            w, h = info["size"]
            ext = {"JPEG": "jpg", "PNG": "png"}[info["format"]]
            dst = pkg / subdir / f"{spec['slot']}-{w}x{h}.{ext}"
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
            source = {"file": rel(src), "sha256": sha256(src), "treatment": "copied unchanged"}
            if "wordmark_margin" in spec:
                m = wordmark_margins(inp, src)
                if m is None:
                    sr.note(f"{spec['slot']}: wordmark margin not checked ({src.name} has no wordmark_box in the key-art manifest)")
                else:
                    low = {k: v for k, v in m.items() if v < spec["wordmark_margin"]}
                    if low:
                        sr.error(f"{spec['slot']}: wordmark {low} px from the edge, store needs {spec['wordmark_margin']}")
                    source["wordmark_margins"] = m
            if "review_wordmark_margin" in spec:
                m = wordmark_margins(inp, src)
                if m is not None:
                    source["wordmark_margins"] = m
                    low = {k: m[k] for k, v in spec["review_wordmark_margin"].items() if m[k] < v}
                    if low:
                        sr.pend(f"{spec['slot']}: wordmark {low} px from the edge; review fix {spec['review_fix']}")
            if "review_width" in spec and w != spec["review_width"]:
                sr.pend(f"{spec['slot']}: {src.name} is {w}x{h}; review fix {spec['review_fix']}")
        e = entry_for(pkg, dst, rules, slot=spec["slot"], source=source)
        if "text" in spec:
            e["contains_text"] = spec["text"]
        if "optional_slot" in spec:
            e["note"] = spec["optional_slot"]
        for p in check_file(dst, rules):
            sr.error(p)
        out.append(e)
    return out


# ---------------------------------------------------------------- trailer

def trailer_records(cfg: dict) -> dict:
    m = json.loads(rp(cfg["trailer"]["manifest"]).read_text(encoding="utf-8"))
    return {e["file"]: e for e in m["deliverables"]}


def trailer_source(cfg: dict, name: str) -> Path | None:
    for d in (cfg["trailer"]["dir"], cfg["trailer"]["outside_dir"]):
        p = rp(d) / name
        if p.exists():
            return p
    return None


def check_video(path: Path, rec: dict | None, rules: dict, expect_sha: str | None = None,
                expect_bytes: int | None = None) -> list[str]:
    """Bytes and SHA-256 against the trailer manifest (or the package manifest), and the store's rules
    against the trailer manifest's ffprobe facts."""
    if not path.exists():
        return [f"{path.name}: missing" + (" (dangling link)" if path.is_symlink() else "")]
    if rec is None:
        return [f"{path.name}: not in the trailer manifest"]
    probs = []
    n = path.stat().st_size
    if n != (expect_bytes if expect_bytes is not None else rec["bytes"]):
        probs.append(f"{path.name}: {n} bytes, manifest says {expect_bytes or rec['bytes']}")
    if sha256(path) != (expect_sha or rec["sha256"]):
        probs.append(f"{path.name}: sha256 differs from the manifest")
    v = rec.get("video", {})
    if "size" in rules and [v.get("width"), v.get("height")] != list(rules["size"]):
        probs.append(f"{path.name}: {v.get('width')}x{v.get('height')}, needs {rules['size'][0]}x{rules['size'][1]}")
    if "container" in rules and path.suffix.lower().lstrip(".") not in rules["container"]:
        probs.append(f"{path.name}: container {path.suffix}, needs {'/'.join(rules['container'])}")
    if "codec" in rules and v.get("codec") not in rules["codec"]:
        probs.append(f"{path.name}: codec {v.get('codec')}, needs {'/'.join(rules['codec'])}")
    if "max_bytes" in rules and n > rules["max_bytes"]:
        probs.append(f"{path.name}: {n:,} bytes, over the {rules['max_bytes']:,}-byte limit")
    if "fps" in rules:
        fr = v.get("avg_frame_rate", "0/1").split("/")
        fps = float(fr[0]) / float(fr[1] or 1)
        if round(fps, 3) not in [float(x) for x in rules["fps"]]:
            probs.append(f"{path.name}: {fps:g} fps, needs {' or '.join(str(x) for x in rules['fps'])}")
    return probs


def link_into(pkg: Path, sub: str, src: Path) -> Path:
    dst = pkg / sub / src.name
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.is_symlink() or dst.exists():
        dst.unlink()
    os.symlink(src, dst)
    return dst


def package_trailer(inp: Inputs, key: str, store: dict, pkg: Path, sr: StoreReport) -> list[dict]:
    slots = store.get("trailer", [])
    if not slots:
        return []
    recs = trailer_records(inp.cfg)
    out = []
    for spec in slots:
        rules = spec.get("rules", {})
        if spec.get("coplay"):
            plat = store.get("switch") if store["kind"] == "desktop" else store.get("platform")
            on = inp.switch(plat, "ai_coplay") if plat is not None else inp.switch(None, "ai_coplay")
            if not on:
                sr.error(f"trailer {spec['slot']}: {spec['file']} shows AI co-play, but the ai_coplay switch is off "
                         f"for this store in platforms.json")
                continue
        src = trailer_source(inp.cfg, spec["file"])
        if src is None:
            sr.error(f"trailer {spec['slot']}: {spec['file']} is in neither {inp.cfg['trailer']['dir']} nor "
                     f"{inp.cfg['trailer']['outside_dir']}")
            continue
        rec = recs.get(spec["file"])
        for p in check_video(src, rec, rules):
            sr.error(f"trailer {spec['slot']}: {p}")
        dst = link_into(pkg, "trailer", src)
        e = {"slot": spec["slot"], "file": dst.relative_to(pkg).as_posix(), "link_to": rel(src),
             "in_repository": src.is_relative_to(rp(inp.cfg["trailer"]["dir"])),
             "bytes": rec["bytes"] if rec else None, "sha256": rec["sha256"] if rec else None,
             "duration_s": rec.get("duration_s") if rec else None,
             "pixels": f"{rec['video']['width']}x{rec['video']['height']}" if rec and rec.get("video") else None,
             "codec": rec.get("video", {}).get("codec") if rec else None,
             "shows_ai_coplay": bool(spec.get("coplay")), "rules": rules,
             "source": {"manifest": inp.cfg["trailer"]["manifest"], "review": inp.cfg["trailer"]["review"]}}
        if spec.get("lead"):
            e["carousel_position"] = 1
        if spec.get("repo_url"):
            path = f"{inp.cfg['trailer']['dir']}/{spec['file']}"
            if not e["in_repository"]:
                sr.error(f"trailer {spec['slot']}: {spec['file']} needs a repository URL but is outside the repository")
            e["repo_path"] = path
            e["intended_url"] = inp.cfg["appstream"]["url_base"] + path
        if spec.get("hosted"):
            e["needs_hosted_url"] = spec["hosted"]
            sr.block(f"trailer {spec['slot']}: needs a hosted video URL ({spec['hosted']}); upload {spec['file']} "
                     f"(linked at {e['file']}) there and enter the URL")
        if "thumbnail" in spec:
            th = spec["thumbnail"]
            tsrc = trailer_source(inp.cfg, th["file"])
            if tsrc is None:
                sr.error(f"trailer {spec['slot']}: thumbnail {th['file']} missing")
            else:
                trules = rules_for(th)
                tdst = link_into(pkg, "trailer", tsrc)
                trec = recs.get(th["file"])
                for p in check_file(tdst, trules, trec["sha256"] if trec else None, trec["bytes"] if trec else None):
                    sr.error(f"trailer {spec['slot']} thumbnail: {p}")
                e["thumbnail"] = entry_for(pkg, tdst, trules, link_to=rel(tsrc))
        if "title_field" in spec:
            e["title_field"] = spec["title_field"]
            plat = store.get("text", {}).get("platform")
            titles = {}
            root = inp.export / plat if plat else None
            if root and root.exists():
                for loc in sorted(p.name for p in root.iterdir()):
                    lf = root / loc / "listing.json"
                    if not lf.exists():
                        continue
                    fields = json.loads(lf.read_text(encoding="utf-8"))["fields"]
                    hit = next((v for k, v in sorted(fields.items()) if k == spec["title_field"] or
                                re.fullmatch(re.escape(spec["title_field"]) + r"_\d+", k)), None)
                    if hit is None:
                        sr.error(f"{loc}: export has no {spec['title_field']} for the trailer title")
                    else:
                        titles[loc] = hit
            e["title"] = {"field": spec["title_field"], "by_locale": titles}
        if "with_asset" in spec:
            names = [a["slot"] for a in store.get("assets", [])]
            if spec["with_asset"] not in names:
                sr.error(f"trailer {spec['slot']}: companion asset slot {spec['with_asset']} is not packaged")
            e["with_asset"] = spec["with_asset"]
        if spec.get("note"):
            e["note"] = spec["note"]
        out.append(e)
    return out


# ---------------------------------------------------------------- desktop stores

def ms_captions(inp: Inputs, role: str, slot: int, sr: StoreReport) -> dict:
    order = inp.platforms["asset_text"]["desktop_gallery_order"]
    if role not in order:
        sr.error(f"role {role} is not in asset_text.desktop_gallery_order: no Microsoft caption field")
        return {}
    n = order.index(role) + 1
    field = f"desktop_screenshot_caption_{n}"
    if n != slot:
        MS_MISMATCH.append(f"slot {slot} {role} <- {field}")
    texts = {}
    root = inp.export / "microsoft"
    for loc in sorted(p.name for p in root.iterdir()):
        fields = json.loads((root / loc / "listing.json").read_text(encoding="utf-8"))["fields"]
        if field not in fields:
            sr.error(f"{loc}: export has no {field}")
            continue
        if len(fields[field]) > 200:
            sr.error(f"{loc}: {field} is {len(fields[field])} characters, over Microsoft's 200")
        texts[loc] = fields[field]
    return {"field": field, "source_field": f"shot_caption_{role}", "by_locale": texts}


def appstream_captions(inp: Inputs) -> dict:
    text = (inp.export / "appstream-fragment.xml").read_text(encoding="utf-8")
    caps: dict[str, dict[str, str]] = {}
    for m in re.finditer(r'<caption source_role="([^"]+)"(?: xml:lang="([^"]+)")?>(.*?)</caption>', text, re.S):
        caps.setdefault(m.group(1), {})[m.group(2) or ""] = m.group(3)
    return caps


def build_desktop(inp: Inputs, key: str, store: dict, pkg: Path, sr: StoreReport) -> dict:
    spec = store["screenshots"]
    row = inp.review["desktop"].get(store["review_row"])
    if row is None:
        sr.error(f"review has no desktop row {store['review_row']!r}")
        return {}
    tokens = row["tokens"]
    if not tokens:
        sr.error(f"review row {store['review_row']!r} lists no frames")
    lo, hi = spec["count"]
    if not lo <= len(tokens) <= hi:
        sr.error(f"{len(tokens)} screenshots; store takes {lo}-{hi}")
    as_caps = appstream_captions(inp) if spec.get("captions") == "appstream" else None
    rules = rules_for(spec)
    shots = []
    for i, tok in enumerate(tokens, 1):
        role, variant = inp.role_for(tok, sr)
        if role == "ai_coplay":
            on = inp.switch(store["switch"], "ai_coplay") if store.get("switch") is not None else \
                inp.switch(None, "ai_coplay")
            if not on:
                sr.error(f"frame `{tok}` is AI co-play but the ai_coplay switch is off for this store in platforms.json")
                continue
        capture = inp.capture_for(tok, spec["aspect"])
        if capture is None:
            sr.error(f"frame `{tok}`: no single {spec['aspect']} capture file in {rel(inp.captures)}")
            continue
        label = role.replace("_", "-") + (f"-{variant}" if variant else "")
        ext = "png" if spec["format"] == "PNG" else "jpg"
        w, h = spec["size"]
        name = f"{label}-{w}x{h}.{ext}" if spec.get("stable_names") else f"{i:02d}-{label}-{w}x{h}.{ext}"
        dst = pkg / "screenshots" / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        source = {"capture": rel(capture), "capture_sha256": sha256(capture), "frame": tok}
        if spec["source"] == "capture":
            if image_info(capture)["size"] != [w, h]:
                sr.error(f"{capture.name} is not {w}x{h}")
                continue
            shutil.copyfile(capture, dst)
            source["treatment"] = "copied unchanged (native game framebuffer pixels)"
        elif spec["source"] == "resize":
            buf = io.BytesIO()
            resized(capture, spec["size"]).save(buf, "PNG", optimize=True)
            save_bytes(dst, buf.getvalue())
            source["treatment"] = f"Lanczos reduction of the capture to {w}x{h}, PNG, no other change"
        else:  # web-1920 export if present and fit, else derived
            limit = spec.get("target_bytes", spec.get("max_bytes"))
            web = sorted(p for p in inp.web1920.glob(f"{tok}-*") if p.suffix.lower() in (".jpg", ".jpeg")) \
                if inp.web1920.exists() else []
            used = False
            if web:
                wi = image_info(web[0])
                if wi["size"] == [w, h] and wi["format"] == "JPEG" and not wi["alpha"] and \
                        (limit is None or web[0].stat().st_size <= limit):
                    shutil.copyfile(web[0], dst)
                    source.update({"export": rel(web[0]), "treatment": "web-1920 JPEG export copied unchanged"})
                    used = True
                else:
                    sr.note(f"{web[0].name} does not fit ({wi['size']}, {web[0].stat().st_size:,} bytes); derived instead")
            if not used:
                data, q = encode_jpeg(resized(capture, spec["size"]), inp.cfg, limit)
                save_bytes(dst, data)
                source["treatment"] = (f"Lanczos reduction of the capture to {w}x{h}, JPEG quality {q}, 4:4:4"
                                       + ("" if web else " (no web-1920 export present yet)"))
        e = entry_for(pkg, dst, rules, upload_order=i, role=role, source=source)
        if variant:
            e["variant"] = variant
        kind = inp.desktop_manifest.get(capture.name, {}).get("kind") or \
            inp.desktop_manifest.get(inp.capture_for(tok, "16:9").name, {}).get("kind")
        if kind:
            e["capture_kind"] = kind
        if spec.get("captions") == "microsoft":
            e["caption"] = ms_captions(inp, role, i, sr)
        if as_caps is not None:
            c = as_caps.get(role, {})
            if not c:
                sr.error(f"appstream fragment has no caption for role {role}")
            e["caption"] = {"field": f"shot_caption_{role}", "en": c.get("", ""), "languages": len(c)}
            e["intended_url"] = inp.cfg["appstream"]["url_base"] + inp.cfg["appstream"]["repo_dir"] + "/" + name
            e["repo_path"] = inp.cfg["appstream"]["repo_dir"] + "/" + name
        for p in check_file(dst, rules):
            sr.error(p)
        shots.append(e)
    if as_caps is not None:
        write_appstream_xml(pkg, shots, as_caps, inp.trailer_entries)
    if MS_MISMATCH:
        sr.pend("asset_text.desktop_gallery_order in translations/platforms.json is not the reviewed gallery order, so the "
                "numbered desktop_screenshot_caption_N fields (and a microsoft_import.py workbook) do not line up with the "
                f"upload slots ({'; '.join(MS_MISMATCH)}). This manifest gives each image its correct caption by role; "
                "either type them per image, or have the copy owner change desktop_gallery_order and re-run")
        MS_MISMATCH.clear()
    # the reviewed reference order must match selection.json once M5 is applied
    ref = inp.review["desktop"].get(inp.cfg["desktop"].get("selection_matches_row", "Microsoft Store"), {}).get("tokens")
    if key == "microsoft" and ref and ref != inp.selection_tokens():
        sr.pend(f"captures/desktop/selection.json order {inp.selection_tokens()} differs from the review's {ref} "
                f"(review fix M5 not applied yet); the package follows the review")
    return {"review_row": store["review_row"], "review_frames": tokens, "screenshots": shots}


def write_appstream_xml(pkg: Path, shots: list[dict], caps: dict, videos: list[dict] | None = None) -> None:
    lines = ["<screenshots>"]
    for i, e in enumerate(shots):
        w, h = e["pixels"].split("x")
        lines.append('  <screenshot type="default">' if i == 0 else "  <screenshot>")
        lines.append(f'    <image type="source" width="{w}" height="{h}">{escape(e["intended_url"])}</image>')
        for lang, text in sorted(caps.get(e["role"], {}).items(), key=lambda kv: kv[0] != ""):  # untranslated first
            attr = f' xml:lang="{lang}"' if lang else ""
            lines.append(f"    <caption{attr}>{text}</caption>")
        lines.append("  </screenshot>")
    for v in videos or []:  # a video is never the default screenshot (AppStream spec)
        if not v.get("intended_url"):
            continue
        w, h = v["pixels"].split("x")
        container = {"webm": "webm", "mkv": "matroska"}[Path(v["file"]).suffix.lstrip(".").lower()]
        lines.append("  <screenshot>")
        lines.append(f'    <video container="{container}" codec="{v["codec"]}" width="{w}" height="{h}">'
                     f'{escape(v["intended_url"])}</video>')
        lines.append("  </screenshot>")
    lines.append("</screenshots>")
    (pkg / "screenshots.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- mobile stores

def tool_hashes(inp: Inputs) -> dict:
    t = inp.cfg["mobile_tools"]
    d = rp(t["dir"])
    return {f: sha256(d / f) for f in t["files"]}


def build_mobile(inp: Inputs, key: str, store: dict, pkg: Path, sr: StoreReport) -> dict:
    plat = inp.platforms["platforms"][store["platform"]]
    locales = plat["locales"]
    current_tools = tool_hashes(inp)
    sel = rp(inp.cfg["mobile_tools"]["selection"])
    sel_sha = sha256(sel) if sel.exists() else None
    stale: dict[str, set] = {}
    out_locales = []
    set_orders = {}
    for s in store["sets"]:
        row = inp.review["mobile"].get(s["render_set"])
        set_orders[s["slot"]] = row["roles"] if row else None
        if s.get("blocked"):
            sr.block(f"{s['slot']} screenshots: {s['blocked']}")
        elif row is None or row["roles"] is None:
            sr.error(f"review has no slide list for {s['render_set']}")
    for canon, code in locales.items():
        folder = re.sub(r"[^A-Za-z0-9-]+", "-", code).strip("-") if store["platform"] == "amazon" else code
        lroot = pkg / folder
        lroot.mkdir(parents=True, exist_ok=True)
        rec = {"locale": canon, "store_locale": code, "folder": folder, "sets": {}, "captions": {}}
        lst = inp.export_listing(store["text"]["platform"], code)
        if lst.exists():
            shutil.copyfile(lst, lroot / "listing.json")
            rec["listing"] = {"file": f"{folder}/listing.json", "sha256": sha256(lst)}
        else:
            sr.error(f"{canon}: no export listing at {rel(lst)}")
        cat = rp(inp.cfg["translations"]) / f"{canon}.md"
        cat_sha = sha256(cat)
        for s in store["sets"]:
            if s.get("blocked"):
                rec["sets"][s["slot"]] = {"blocked": True}
                continue
            roles = set_orders[s["slot"]] or []
            mdir = inp.renders / s["render_set"] / canon
            mfile = mdir / "manifest.json"
            if not mfile.exists():
                sr.pend(f"{canon}/{s['slot']}: no render manifest at {rel(mfile)}")
                continue
            m = json.loads(mfile.read_text(encoding="utf-8"))
            if m.get("partial"):
                stale.setdefault("partial render", set()).add(f"{s['render_set']}/{canon}")
            if m["catalog"]["sha256"] != cat_sha:
                stale.setdefault("caption catalog changed since render", set()).add(f"{s['render_set']}/{canon}")
            if any(m["tool"].get(f) != h for f, h in current_tools.items()):
                stale.setdefault("rendered by an older screenshots.py/caption.html/gallery.json/fonts.json", set()).add(
                    f"{s['render_set']}/{canon}")
            if sel_sha and m.get("gallery", {}).get("sha256") != sel_sha:
                stale.setdefault("rendered from an older captures/mobile/selection.json", set()).add(
                    f"{s['render_set']}/{canon}")
            by_role = {img["role"]: img for img in m["images"]}
            extra = [r for r in by_role if r not in roles]
            if extra:
                stale.setdefault(f"render has slides the review dropped ({', '.join(sorted(extra))}); left out", set()).add(
                    f"{s['render_set']}/{canon}")
            entries = []
            for i, role in enumerate(roles, 1):
                img = by_role.get(role)
                if img is None:
                    stale.setdefault(f"render lacks the review's '{role}' slide", set()).add(f"{s['render_set']}/{canon}")
                    continue
                target = mdir / img["file"]
                w, h = s["size"]
                dst = lroot / s["slot"] / f"{len(entries) + 1:02d}-{role}-{w}x{h}.png"
                dst.parent.mkdir(parents=True, exist_ok=True)
                if dst.is_symlink() or dst.exists():
                    dst.unlink()
                os.symlink(target, dst)
                rec["captions"][role] = {"field": img["caption"]["field"], "text": img["caption"]["text"]}
                entries.append({"upload_order": len(entries) + 1, "role": role,
                                "file": dst.relative_to(pkg).as_posix(),
                                "link_to": rel(target), "sha256": img["sha256"], "bytes": img["bytes"]})
            lo, hi = s["count"]
            if not lo <= len(entries) <= hi:
                sr.error(f"{canon}/{s['slot']}: {len(entries)} screenshots, store takes {lo}-{hi}")
            rec["sets"][s["slot"]] = {"render_set": s["render_set"], "render_manifest_sha256": sha256(mfile),
                                      "screenshots": entries}
        out_locales.append(rec)
    for why, where in stale.items():
        sets = sorted({w.split("/")[0] for w in where})
        sr.pend(f"{why}: {len(where)} locale sets ({', '.join(sets)})")
    for b in store.get("blocked", []):
        sr.block(f"{b['slot']}: {b['why']}")
    assets = package_assets(inp, store, pkg, sr, subdir="_store-wide")
    set_rules = {s["slot"]: {"render_set": s["render_set"], "order": set_orders[s["slot"]],
                             "blocked": s.get("blocked"), "rules": rules_for(s) | {"count": s["count"]}}
                 for s in store["sets"]}
    return {"sets": set_rules, "locales": out_locales, "assets": assets}


# ---------------------------------------------------------------- per store

def dump_manifest(man: dict) -> str:
    """Indented JSON, with each mobile screenshot entry kept on one line so the big manifests stay readable."""
    raws: list[str] = []

    def walk(o):
        if isinstance(o, dict):
            if "upload_order" in o and "link_to" in o:
                raws.append(json.dumps(o, ensure_ascii=False))
                return f"@@RAW{len(raws) - 1}@@"
            return {k: walk(v) for k, v in o.items()}
        if isinstance(o, list):
            return [walk(v) for v in o]
        return o

    text = json.dumps(walk(man), ensure_ascii=False, indent=1)
    text = re.sub(r'"@@RAW(\d+)@@"', lambda m: raws[int(m.group(1))], text)
    return text + "\n"


def build_store(inp: Inputs, key: str, store: dict, report: Report) -> dict:
    sr = report.store(key)
    pkg = inp.out / key
    if pkg.exists():
        shutil.rmtree(pkg)
    pkg.mkdir(parents=True)
    man = {"store": key, "title": store["title"], "package_dir": rel(pkg),
           "generated_by": "assets/storefront-v2/store-packages/build.py",
           "inputs": {"stores.json": sha256(CONFIG), "review": {"file": inp.cfg["review"], "sha256": inp.review["sha256"]},
                      "platforms.json": sha256(rp(inp.cfg["platforms"])),
                      "desktop_selection": sha256(inp.selection_path),
                      "export": "fresh storefront.py export --require-review (upload_eligible false: preparation only)"}}
    man["inputs"]["trailer_manifest"] = sha256(rp(inp.cfg["trailer"]["manifest"]))
    if store["kind"] == "desktop":
        for b in store.get("lead_blocked", []):
            sr.block(f"{b['slot']}: {b['why']}")
        inp.trailer_entries = package_trailer(inp, key, store, pkg, sr)
        body = build_desktop(inp, key, store, pkg, sr)
        man.update(body)
        if store.get("lead_blocked"):
            man["carousel_lead"] = store["lead_blocked"]
        man["assets"] = package_assets(inp, store, pkg, sr)
        t = store["text"]
        if t.get("platform"):
            src = inp.export / t["platform"]
            shutil.copytree(src, pkg / "text")
            man["text"] = {"dir": "text", "locales": sorted(p.name for p in src.iterdir())}
        for f in t.get("files", []):
            shutil.copyfile(inp.export / f, pkg / f)
        if t.get("files"):
            man["text"] = {"files": t["files"]}
        for b in store.get("blocked", []):
            sr.block(f"{b['slot']}: {b['why']}")
    else:
        man.update(build_mobile(inp, key, store, pkg, sr))
        inp.trailer_entries = package_trailer(inp, key, store, pkg, sr)
    if inp.trailer_entries:
        man["trailer"] = inp.trailer_entries
        lead = [e["slot"] for e in inp.trailer_entries if e.get("carousel_position") == 1]
        if lead:
            man["carousel_lead"] = lead
    inp.trailer_entries = []
    man["blocked"] = sr.blocked
    man["pending"] = sr.pending
    man["errors"] = sr.errors
    man["not_packaged"] = store.get("not_packaged", [])
    man["unverified"] = store.get("unverified", [])
    man["notes"] = sr.notes
    data = dump_manifest(man)
    (pkg / "package.json").write_text(data, encoding="utf-8")
    MANIFESTS.mkdir(exist_ok=True)
    (MANIFESTS / f"{key}.json").write_text(data, encoding="utf-8")
    return man


# ---------------------------------------------------------------- verify

def iter_files(man: dict):
    for e in man.get("screenshots", []):
        yield e, e["rules"]
    for e in man.get("assets", []):
        yield e, e["rules"]
    for loc in man.get("locales", []):
        for slot, s in loc["sets"].items():
            for e in s.get("screenshots", []):
                yield e, man["sets"][slot]["rules"]


def verify(out: Path, keys: list[str], report: Report, carry: bool = False) -> dict:
    """Re-check every packaged file against its manifest and rules. With carry, also report the
    pending, blocked and error items the build recorded (verify run on its own)."""
    summary = {}
    for key in keys:
        sr = report.store(f"verify {key}")
        mf = out / key / "package.json"
        if not mf.exists():
            sr.error("no package.json; build first")
            continue
        man = json.loads(mf.read_text(encoding="utf-8"))
        if carry:
            for kind in ("errors", "pending", "blocked"):
                for item in man.get(kind, []):
                    getattr(report, kind).append(f"{key}: {item}")
        repo_m = MANIFESTS / f"{key}.json"
        if not repo_m.exists() or repo_m.read_bytes() != mf.read_bytes():
            sr.error(f"repository manifest manifests/{key}.json differs from the package's package.json")
        pkg = out / key
        listed = set()
        n_files = own = linked = 0
        for e, rules in iter_files(man):
            path = pkg / e["file"]
            listed.add(path)
            for p in check_file(path, rules, e["sha256"], e["bytes"]):
                sr.error(p)
            n_files += 1
            if path.is_symlink():
                linked += e["bytes"]
            elif path.exists():
                own += path.stat().st_size
        for loc in man.get("locales", []):
            for slot, s in loc["sets"].items():
                if "screenshots" not in s:
                    continue
                lo, hi = man["sets"][slot]["rules"]["count"]
                if not lo <= len(s["screenshots"]) <= hi:
                    sr.error(f"{loc['locale']}/{slot}: {len(s['screenshots'])} screenshots, store takes {lo}-{hi}")
        recs = trailer_records(CFG)
        for e in man.get("trailer", []):
            path = pkg / e["file"]
            listed.add(path)
            for p in check_video(path, recs.get(Path(e["file"]).name), e["rules"], e["sha256"], e["bytes"]):
                sr.error(p)
            n_files += 1
            linked += e["bytes"] or 0
            th = e.get("thumbnail")
            if th:
                tp = pkg / th["file"]
                listed.add(tp)
                for p in check_file(tp, th["rules"], th["sha256"], th["bytes"]):
                    sr.error(p)
                n_files += 1
                linked += th["bytes"]
        images = {p for p in pkg.rglob("*") if p.suffix.lower() in (".png", ".jpg", ".jpeg") and "text" not in p.parts}
        for p in sorted(images - listed):
            sr.error(f"unlisted image in package: {p.relative_to(pkg)}")
        other = sum(p.stat().st_size for p in pkg.rglob("*") if p.is_file() and not p.is_symlink() and p not in listed)
        summary[key] = {"files": n_files, "bytes_on_disk": own + other, "bytes_linked": linked}
    return summary


# ---------------------------------------------------------------- main

def human(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024
    return str(n)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", nargs="?", default="build", choices=["build", "verify"])
    ap.add_argument("--store", default="all", help="comma-separated store keys from stores.json, or all")
    ap.add_argument("--out", help="output root (default: output_root in stores.json)")
    ap.add_argument("--stage-appstream", action="store_true",
                    help="also copy the AppStream PNGs into the repository folder their URLs point at (for the Git steward)")
    ap.add_argument("--allow-pending", action="store_true", help="exit 0 when only pending items remain")
    a = ap.parse_args()
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    CFG.update(cfg)
    out = Path(a.out).resolve() if a.out else rp(cfg["output_root"])
    ROOTS.update({"renders": rp(cfg["renders_root"]), "packages": out, "trailer": rp(cfg["trailer"]["outside_dir"])})
    try:
        out.relative_to(REPO)
        raise SystemExit("output_root must be outside the repository")
    except ValueError:
        pass
    keys = list(cfg["stores"]) if a.store == "all" else a.store.split(",")
    for k in keys:
        if k not in cfg["stores"]:
            raise SystemExit(f"unknown store {k!r}; known: {', '.join(cfg['stores'])}")
    report = Report()
    out.mkdir(parents=True, exist_ok=True)
    if a.command == "build":
        inp = Inputs(cfg, out, report)
        inp.run_export()
        for k in keys:
            build_store(inp, k, cfg["stores"][k], report)
        if a.stage_appstream and "appstream" in keys:
            dst = rp(cfg["appstream"]["repo_dir"])
            if dst.exists():
                for p in dst.glob("*.png"):
                    p.unlink()
            dst.mkdir(parents=True, exist_ok=True)
            for p in sorted((out / "appstream" / "screenshots").glob("*.png")):
                shutil.copyfile(p, dst / p.name)
            print(f"staged AppStream screenshots in {rel(dst)}")
    summary = verify(out, keys, report, carry=a.command == "verify")
    total_disk = sum(v["bytes_on_disk"] for v in summary.values())
    total_link = sum(v["bytes_linked"] for v in summary.values())
    summary_out = {"stores": summary, "bytes_on_disk": total_disk, "bytes_linked": total_link,
                   "pending": report.pending, "blocked": report.blocked, "errors": report.errors}
    if a.command == "build" and a.store == "all":
        (out / "summary.json").write_text(json.dumps(summary_out, indent=1, ensure_ascii=False) + "\n")
    print(f"\n{'store':<12} {'files':>6} {'on disk':>10} {'linked':>10}")
    for k, v in summary.items():
        print(f"{k:<12} {v['files']:>6} {human(v['bytes_on_disk']):>10} {human(v['bytes_linked']):>10}")
    print(f"{'total':<12} {sum(v['files'] for v in summary.values()):>6} {human(total_disk):>10} {human(total_link):>10}")
    for title, items in (("BLOCKED (expected, not a failure)", report.blocked), ("PENDING", report.pending),
                         ("NOTES", report.notes), ("ERRORS", report.errors)):
        if items:
            print(f"\n{title}:")
            for i in items:
                print(f"  - {i}")
    if report.errors:
        return 1
    if report.pending and not a.allow_pending:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
