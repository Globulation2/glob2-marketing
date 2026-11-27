#!/usr/bin/env python3
"""Build the web-portal art (Poki, CrazyGames, GameDistribution) from lite-build takes.

Every picture comes from takes of the Globulation 2 **lite** browser build
(0.11.8.2, package b3eb782b40c80032) recorded by record.js: the game's own canvas,
captured at real speed with canvas.captureStream + MediaRecorder in headless
Chromium. This script only crops (never scales up), cuts, downscales, and lays the
game's own wordmark over the opening frame of the CrazyGames and GameDistribution
art (the cover rule allows the title only). The Poki thumbnail and animated
thumbnail carry no text at all.

    uv run --with pillow python assets/portal-art/tools/build.py

Inputs:  ../storefront-v2-renders/portal-art/takes/*.webm (relative to the repo root)
Outputs: stills in assets/portal-art/<portal>/ (committed), MP4s in
         ../storefront-v2-renders/portal-art/<portal>/ (not committed, like the
         trailer MP4s), and assets/portal-art/manifest.json.
"""
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
ART = HERE.parent
MARKETING = ART.parents[1]
RENDERS = MARKETING.parent / "storefront-v2-renders/portal-art"
TAKES = RENDERS / "takes"
WORK = RENDERS / "work"
LANCZOS = Image.Resampling.LANCZOS

# The key-art script's wordmark (the game's menu-wordmark.png, cream and gold with a
# night outline), reused so every store shows the same title treatment.
_spec = importlib.util.spec_from_file_location("keyart", MARKETING / "assets/storefront/key-art/build-assets.py")
keyart = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(keyart)

# Crops of the game window that hold only the map view: below the top bar and the
# event list (up to five rows in spectator view), left of the 200-px right-hand panel. Map pixels are 1:1 with the canvas.
CROP = {
    "land": (0, 160, 1920, 1080),   # 2122x1260 window
    "port": (0, 160, 1080, 1620),   # 1282x1800 window
    "poki": (0, 160, 1080, 1080),   # 1282x1260 window
}
# (take, start s, length s) per cut, in order.
CUTS = {
    "crazygames-preview-landscape-1920x1080": ("land", 30, [("land-s1", 0.5, 7.0), ("land-s2", 1.0, 5.5), ("land-s3", 1.0, 5.5)]),
    "crazygames-preview-portrait-1080x1620": ("port", 30, [("port-s1", 0.5, 7.0), ("port-s2", 1.0, 5.5), ("port-s3", 1.0, 5.5)]),
    "poki-animated-thumbnail-1080x1080": ("poki", 60, [("poki-p1", 0.3, 1.95), ("poki-p2", 0.3, 1.95), ("poki-p3", 0.3, 1.95)]),
}
TITLE_HOLD, TITLE_FADE = 1.2, 0.6   # the cover's title stays 1.2 s on the live picture, then fades


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run(*cmd):
    subprocess.run([str(c) for c in cmd], check=True)


def frame(take, t, kind):
    """The first frame of a cut, cropped to the map view, as RGB."""
    out = WORK / f"{take}-{t:.2f}.png"
    if not out.exists():
        x, y, w, h = CROP[kind]
        run("ffmpeg", "-v", "error", "-y", "-ss", f"{t}", "-i", TAKES / f"{take}.webm", "-frames:v", "1",
            "-vf", f"crop={w}:{h}:{x}:{y}", out)
    return Image.open(out).convert("RGB")


def title_layer(size, width, cx, top):
    """Transparent layer with the wordmark: (cx, top) is the letters' top centre."""
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    wm, (dx, dy) = keyart.wordmark_layer(width, "outline")
    x = cx - width // 2 - dx
    layer.alpha_composite(wm, (max(0, x), max(0, top - dy)), (max(0, -x), max(0, dy - top)))
    return layer


def with_title(img, layer):
    base = img.convert("RGBA")
    base.alpha_composite(layer)
    return base.convert("RGB")


def save(img, path, quality=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".jpg":
        img.save(path, quality=quality or 92, subsampling=0, optimize=True)
    else:
        img.save(path, optimize=True)
    return path


def cut(name, layer_png=None):
    kind, fps, parts = CUTS[name]
    x, y, w, h = CROP[kind]
    portal = name.split("-")[0]
    out = RENDERS / portal / f"glob2-lite-{name}.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-v", "error", "-y"]
    for take, start, length in parts:
        cmd += ["-ss", f"{start}", "-t", f"{length}", "-i", TAKES / f"{take}.webm"]
    chains = [f"[{i}:v]crop={w}:{h}:{x}:{y},fps={fps},setpts=PTS-STARTPTS[v{i}]" for i in range(len(parts))]
    graph = ";".join(chains) + ";" + "".join(f"[v{i}]" for i in range(len(parts))) + f"concat=n={len(parts)}:v=1:a=0[cat]"
    if layer_png:
        cmd += ["-loop", "1", "-t", f"{TITLE_HOLD + TITLE_FADE}", "-i", layer_png]
        n = len(parts)
        graph += (f";[{n}:v]format=rgba,fade=t=out:st={TITLE_HOLD}:d={TITLE_FADE}:alpha=1[t]"
                  f";[cat][t]overlay=0:0:eof_action=pass:format=auto[out]")
    else:
        graph += ";[cat]null[out]"
    cmd += ["-filter_complex", graph, "-map", "[out]", "-an", "-c:v", "libx264", "-profile:v", "high",
            "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709",
            "-color_trc", "bt709", "-movflags", "+faststart", out]
    run(*cmd)
    return out


def probe(path):
    data = json.loads(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-show_entries",
                                      "stream=width,height,codec_name,avg_frame_rate,nb_read_frames:format=duration",
                                      "-of", "json", str(path)], capture_output=True, text=True, check=True).stdout)
    s = [x for x in data["streams"] if x.get("width")][0]
    return dict(width=s["width"], height=s["height"], codec=s["codec_name"], fps=s["avg_frame_rate"],
                frames=int(s["nb_read_frames"]), duration=float(data["format"]["duration"]),
                audio_streams=len([x for x in data["streams"] if not x.get("width")]))


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    outputs = []

    def record(path, kind, **extra):
        p = Path(path)
        entry = dict(file=str(p.relative_to(MARKETING) if MARKETING in p.parents else p.relative_to(MARKETING.parent)),
                     kind=kind, bytes=p.stat().st_size, sha256=sha256(p), **extra)
        if p.suffix == ".mp4":
            entry.update(probe(p))
        else:
            entry["size"] = list(Image.open(p).size)
        outputs.append(entry)

    # ---- Poki: text-free square thumbnail = the animated thumbnail's first frame.
    poki_first = frame("poki-p1", 0.3, "poki")
    thumb = save(poki_first, ART / "poki/poki-thumbnail-1080x1080.png")
    record(thumb, "Poki static thumbnail (no text)", source=("poki-p1", 0.3), crop=CROP["poki"])
    record(cut("poki-animated-thumbnail-1080x1080"), "Poki animated thumbnail (no text)",
           cuts=CUTS["poki-animated-thumbnail-1080x1080"][2])

    # ---- CrazyGames: covers are the previews' opening frames with the title.
    land = frame("land-s1", 0.5, "land")
    land_title = title_layer(land.size, 880, 960, 900)
    land_title.save(WORK / "title-land.png")
    cover169 = with_title(land, land_title)
    record(save(cover169, ART / "crazygames/crazygames-cover-landscape-1920x1080.jpg"),
           "CrazyGames cover 16:9 (title only)", source=("land-s1", 0.5), crop=CROP["land"])

    port = frame("port-s1", 0.5, "port")
    port_title = title_layer(port.size, 900, 540, 1420)
    port_title.save(WORK / "title-port.png")
    cover23 = with_title(port, port_title).resize((800, 1200), LANCZOS)
    record(save(cover23, ART / "crazygames/crazygames-cover-portrait-800x1200.jpg"),
           "CrazyGames cover 2:3 (title only)", source=("port-s1", 0.5), crop=CROP["port"], scale=round(800 / 1080, 4))

    square = land.crop((420, 0, 1500, 1080))
    sq_title = title_layer(square.size, 860, 540, 900)
    cover11 = with_title(square, sq_title).resize((800, 800), LANCZOS)
    record(save(cover11, ART / "crazygames/crazygames-cover-square-800x800.jpg"),
           "CrazyGames cover 1:1 (title only)", source=("land-s1", 0.5), crop=[420, 160, 1080, 1080], scale=round(800 / 1080, 4))

    record(cut("crazygames-preview-landscape-1920x1080", WORK / "title-land.png"),
           "CrazyGames preview 16:9 (opens on the cover, title fades by 1.8 s)", cuts=CUTS["crazygames-preview-landscape-1920x1080"][2])
    record(cut("crazygames-preview-portrait-1080x1620", WORK / "title-port.png"),
           "CrazyGames preview 2:3 at 1080x1620 (opens on the cover, title fades by 1.8 s)",
           cuts=CUTS["crazygames-preview-portrait-1080x1620"][2])

    # ---- GameDistribution: the five standard asset sizes, from the same lite frame.
    full = with_title(land, land_title)
    gd = {
        (1280, 720): (0, 0, 1920, 1080),
        (1280, 550): (0, 255, 1920, 825),
        (512, 384): (240, 0, 1440, 1080),
        (512, 512): (420, 0, 1080, 1080),
        (200, 120): (60, 0, 1800, 1080),
    }
    for (w, h), (x, y, cw, ch) in gd.items():
        if (w, h) == (512, 512):
            img = cover11.resize((512, 512), LANCZOS)
            box = "crazygames square cover"
        else:
            img = full.crop((x, y, x + cw, y + ch)).resize((w, h), LANCZOS)
            box = [x, y, cw, ch]
        record(save(img, ART / f"gamedistribution/gamedistribution-{w}x{h}.jpg"),
               f"GameDistribution {w}x{h}", source=("land-s1", 0.5), crop_of_cover=box)

    # Review sheet: every still at the size a portal tile shows it (Poki ~200 px,
    # CrazyGames cards ~300 px wide, GameDistribution's smallest at its own size).
    tiles = [(ART / "poki/poki-thumbnail-1080x1080.png", (200, 200)),
             (ART / "crazygames/crazygames-cover-landscape-1920x1080.jpg", (300, 169)),
             (ART / "crazygames/crazygames-cover-portrait-800x1200.jpg", (200, 300)),
             (ART / "crazygames/crazygames-cover-square-800x800.jpg", (300, 300)),
             (ART / "gamedistribution/gamedistribution-200x120.jpg", (200, 120))]
    sheet = Image.new("RGB", (sum(w for _, (w, _) in tiles) + 12 * (len(tiles) + 1), 324), (30, 30, 30))
    x = 12
    for path, (w, h) in tiles:
        sheet.paste(Image.open(path).convert("RGB").resize((w, h), LANCZOS), (x, 12))
        x += w + 12
    record(save(sheet, ART / "contact-sheet-tile-size.png"), "Review sheet: stills at portal tile size (not an upload)")

    takes = {}
    for f in sorted(TAKES.glob("*.json")):
        meta = json.loads(f.read_text())
        meta["save"] = "saves/" + Path(meta["save"]).name
        meta["webm_sha256"] = sha256(f.with_suffix(".webm"))
        takes[f.stem] = meta
    manifest = dict(
        build=dict(edition="lite", version="0.11.8.2", tag="v0.11.8.2", commit="8fb3c06aee",
                   package="browser-release-lite b3eb782b40c80032 (release-mirror run 45902410410)"),
        renders=str(RENDERS.relative_to(MARKETING.parent)),
        crops=CROP, title=dict(hold_s=TITLE_HOLD, fade_s=TITLE_FADE), takes=takes, outputs=outputs)
    (ART / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
    for o in outputs:
        print(o["file"], o.get("size") or (o["width"], o["height"], round(o["duration"], 2), o["fps"]), o["bytes"])


if __name__ == "__main__":
    sys.exit(main())
