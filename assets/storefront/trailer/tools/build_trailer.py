#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Cut the store trailer from the filmed shots, as described by trailer.json.

usage: build_trailer.py CUT[,CUT] --raw DIR --work DIR --out DIR
                        [--locale en] [--cards DIR] [--only timeline|clean|text|poster] [--no-4k]

For each cut in trailer.json ("cuts"):

  timeline  WORK/<cut>-timeline-<W>x<H>.mkv, one per output size: the shots' frames
            (RAW/<shot>/f%04d.png, cropped to the segment's rectangle or the frame
            named in trailer.json), trimmed and joined with hard cuts, lossless. Each
            size is scaled straight from the native crop, so a punch-in ("upscale":
            true) is upscaled only where the output is larger than the crop, and the
            1080p files never pass through an upscaled 2160p picture. A segment with an
            "inset" also shows a crop of the game's own Hive card from the same frame
            (see prepare_inset). One frame is one game tick and the cut plays at 30
            frames a second, the game's normal speed; nothing is retimed or blended.
  clean     the text-free masters: OUT/<name>-textless-2160p.mp4 and -1080p.mp4
            (portrait cuts: one 1080x1920 file), with the music.
  text      the same picture with the text cards of --locale laid over it
            (render_cards.py output in --cards, rendered at each output size):
            OUT/<name>-2160p.mp4 and -1080p.mp4, or OUT/<name>-<locale>-1080p.mp4 for a
            locale other than en; plus the cut's "extra_outputs" for en (WebM, preview).
  poster    (trailer.json "poster") the poster PNGs, scaled straight from the raw frame.

Text cues, the wordmark's start, shot order and the music plan are all data in
trailer.json; another language is `render_cards.py --locale xx` and then
`build_trailer.py CUT --only text --locale xx`.

Needs ffmpeg with libx264, libvpx-vp9, libopus and AAC (brew install ffmpeg), and Pillow
and numpy for inset segments and posters (uv run --with pillow --with numpy python ...).
No drawtext is used.
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
GAME = Path(os.environ.get("GLOB2_GAME") or HERE.parents[4] / "glob2")
COLOR = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]


def run(cmd):
    print("+ " + " ".join(str(c) if " " not in str(c) else repr(str(c)) for c in cmd[:14]) + (" ..." if len(cmd) > 14 else ""),
          flush=True)
    subprocess.run([str(c) for c in cmd], check=True)


def canvas(cut, data):
    w, h = cut.get("size") or data["frame"]["size"]
    return w, h


def sizes_for(cut, data, no_4k, locales):
    """Output picture sizes the cut needs: portrait one size; landscape 2160p (en and
    text-free only, unless --no-4k) and 1080p, plus the sizes of extra outputs."""
    w, h = canvas(cut, data)
    if h > w:
        return [(w, h)]
    out = []
    if not no_4k and cut.get("uhd", True) and any(loc in (None, "en") for loc in locales):
        out.append((w, h))
    out.append((1920, 1080))
    return out


def seg_crop(seg, cut, data):
    return seg.get("crop") or cut.get("crop") or data["frame"]["crop"]


def check_scale(name, seg, crop, size):
    cw, ch = crop[0], crop[1]
    if abs(cw / ch - size[0] / size[1]) > 0.01:
        raise SystemExit(f"{name}: crop {cw}x{ch} of {seg['shot']} is not the shape of {size[0]}x{size[1]}")
    if (cw < size[0] or ch < size[1]) and not seg.get("upscale"):
        raise SystemExit(f"{name}: crop {cw}x{ch} of {seg['shot']} would be scaled up to {size[0]}x{size[1]}")


def card_top(a, ins):
    """Top edge of the Hive card in one raw frame (the card grows upwards as its output
    gets longer): walk up column top_probe_x from just above the card's bottom edge
    while the pixels are the card's own fill colour."""
    import numpy as np
    rgb = np.array(ins["card_rgb"])
    tol = np.array(ins["tolerance"])
    x, y = ins["top_probe_x"], ins["bottom"] - 12
    if not (abs(a[y, x].astype(int) - rgb) <= tol).all():
        raise SystemExit(f"inset: no card fill at ({x},{y})")
    while y > 0 and (abs(a[y - 1, x].astype(int) - rgb) <= tol).all():
        y -= 1
    return y


def prepare_inset(name, i, seg, raw, work, sizes):
    """Frames of an inset segment at each output size, as PNGs: the main window scaled
    to the canvas, and the game's own Hive card cropped from the same frame (from its
    top edge, found per frame, to its bottom edge, so the buttons stacked above the
    card stay outside the crop) and laid over the bottom-left corner with a soft
    shadow. Nothing inside either crop is altered."""
    import numpy as np
    from PIL import Image, ImageFilter
    ins = seg["inset"]
    cw, ch, cx, cy = seg["crop"]
    x0, x1 = ins["region_x"]
    dirs, tops = {}, []
    for (w, h) in sizes:
        d = work / f"{name}-seg{i}-{w}x{h}"
        d.mkdir(parents=True, exist_ok=True)
        dirs[(w, h)] = d
    for k in range(seg["frames"]):
        f = seg["in"] + k
        src = Image.open(raw / seg["shot"] / f"f{f:04d}.png").convert("RGB")
        a = np.asarray(src)
        top = card_top(a, ins)
        tops.append({"frame": f, "card_top": int(top)})
        card = src.crop((x0, top, x1, ins["bottom"]))
        main = src.crop((cx, cy, cx + cw, cy + ch))
        for (w, h), d in dirs.items():
            frame = main.resize((w, h), Image.LANCZOS)
            s = ins["scale_at_3840"] * w / 3840
            c = card if s == 1 else card.resize((round(card.width * s), round(card.height * s)), Image.LANCZOS)
            px, py = round(ins["margin"][0] * w), h - round(ins["margin"][1] * h) - c.height
            blur = max(2, round(0.012 * h))
            sh = Image.new("L", (c.width + 4 * blur, c.height + 4 * blur), 0)
            sh.paste(round(255 * ins["shadow"]), (2 * blur, 2 * blur, 2 * blur + c.width, 2 * blur + c.height))
            sh = sh.filter(ImageFilter.GaussianBlur(blur))
            frame.paste((12, 8, 20), (px - 2 * blur, py - 2 * blur + blur // 2), sh)
            frame.paste(c, (px, py))
            frame.save(d / f"f{k:04d}.png", compress_level=1)
    (work / f"{name}-seg{i}-inset.json").write_text(json.dumps({"shot": seg["shot"], "card_tops": tops}, indent=0))
    return dirs


def build_timeline(name, cut, data, raw, work, sizes):
    """Lossless join of the trimmed shots, one file per output size, each size scaled
    straight from the segment's native crop."""
    fps = data["fps"]
    outs = {sz: work / f"{name}-timeline-{sz[0]}x{sz[1]}.mkv" for sz in sizes}
    cmd = ["ffmpeg", "-v", "error", "-stats", "-y"]
    parts = []
    n_in = 0
    labels = {sz: [] for sz in sizes}
    for i, seg in enumerate(cut["timeline"]):
        d = raw / seg["shot"]
        n = len(list(d.glob("f*.png")))
        if seg["in"] + seg["frames"] > n:
            raise SystemExit(f"{name}: shot {seg['shot']} has {n} frames, needs {seg['in'] + seg['frames']}")
        crop = seg_crop(seg, cut, data)
        for sz in sizes:
            check_scale(name, seg, crop, sz)
        if seg.get("inset"):
            dirs = prepare_inset(name, i, seg, raw, work, sizes)
            for sz in sizes:
                cmd += ["-framerate", fps, "-start_number", 0, "-i", dirs[sz] / "f%04d.png"]
                parts.append(f"[{n_in}:v]trim=end_frame={seg['frames']},setpts=PTS-STARTPTS,setsar=1[s{i}_{sz[0]}]")
                labels[sz].append(f"[s{i}_{sz[0]}]")
                n_in += 1
            continue
        cmd += ["-framerate", fps, "-start_number", seg["in"], "-i", d / "f%04d.png"]
        cw, ch, cx, cy = crop
        chain = f"[{n_in}:v]trim=end_frame={seg['frames']},setpts=PTS-STARTPTS,crop={cw}:{ch}:{cx}:{cy}"
        chain += f",split={len(sizes)}" + "".join(f"[c{i}_{sz[0]}]" for sz in sizes)
        parts.append(chain)
        for sz in sizes:
            sc = "" if (cw, ch) == sz else f"scale={sz[0]}:{sz[1]}:flags=lanczos,"
            parts.append(f"[c{i}_{sz[0]}]{sc}setsar=1[s{i}_{sz[0]}]")
            labels[sz].append(f"[s{i}_{sz[0]}]")
        n_in += 1
    n = len(cut["timeline"])
    maps = []
    for sz in sizes:
        parts.append("".join(labels[sz]) + f"concat=n={n}:v=1:a=0,"
                     "scale=in_range=full:out_range=tv:out_color_matrix=bt709:flags=lanczos+accurate_rnd+full_chroma_int,"
                     f"format=yuv420p[v{sz[0]}]")
        maps += ["-map", f"[v{sz[0]}]", "-r", fps, "-c:v", "libx264", "-qp", 0, "-preset", "veryfast"] + COLOR + [outs[sz]]
    cmd += ["-filter_complex", ";".join(parts)] + maps
    run(cmd)
    return outs


def music_filter(cut, data, first_input):
    """Mood stems of one soundtrack set, cross-faded as the game does, tail faded out.

    mood_gain_db lifts one mood against the other (the combat mood is mixed quieter
    than the building mood in the game's files); the limiter keeps the true peak of
    the encoded file at or below -1 dBTP (checked with ebur128 after encoding)."""
    m = cut["music"]
    dur = cut["duration"]
    xf = m.get("crossfade", 0.8)
    moods = sorted({s["mood"] for s in m["segments"]})
    parts, labels = [], []
    for k, mood in enumerate(moods):
        # gain(t): 1 inside this mood's segments, linear ramps of `xf` centred on each boundary
        terms = []
        for s in m["segments"]:
            if s["mood"] != mood:
                continue
            a, b = s["from"], s["to"]
            up = "1" if a <= 0 else f"clip((t-{a - xf / 2})/{xf},0,1)"
            down = "1" if b >= dur else f"clip(({b + xf / 2}-t)/{xf},0,1)"
            terms.append(f"min({up},{down})")
        expr = "+".join(terms)
        gain = 10 ** (m.get("mood_gain_db", {}).get(mood, 0) / 20)
        expr = f"{gain:.6f}*({expr})"
        parts.append(f"[{first_input + k}:a]atrim=start={m.get('offset', 0)},asetpts=PTS-STARTPTS,"
                     f"atrim=end={dur},aresample=48000,volume='{expr}':eval=frame[m{k}]")
        labels.append(f"[m{k}]")
    tail = m.get("tail_fade", 2.0)
    lim = m.get("limiter", {"limit": 0.89, "attack_ms": 5, "release_ms": 50})
    parts.append("".join(labels) + f"amix=inputs={len(moods)}:normalize=0,volume={m.get('gain_db', 0)}dB,"
                 f"afade=t=in:st=0:d=0.04,afade=t=out:st={dur - tail}:d={tail},"
                 f"aresample=192000,alimiter=limit={lim['limit']}:attack={lim['attack_ms']}:release={lim['release_ms']}:level=disabled,"
                 f"aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[a]")
    inputs = []
    for mood in moods:
        inputs += ["-i", GAME / "content" / "data" / "zik" / m["set"] / f"{mood}.opus"]
    return inputs, ";".join(parts)


def encode_args(height, fps, codec="h264"):
    if codec == "vp9":
        return ["-c:v", "libvpx-vp9", "-crf", 30, "-b:v", 0, "-pix_fmt", "yuv420p", "-row-mt", 1, "-tile-columns", 2,
                "-deadline", "good", "-cpu-used", 2, "-g", fps * 4, "-r", fps] + COLOR + [
                "-c:a", "libopus", "-b:a", "160k", "-ar", 48000, "-ac", 2]
    if codec == "h264-preview":
        return ["-c:v", "libx264", "-profile:v", "high", "-level", "4.0", "-pix_fmt", "yuv420p", "-preset", "slow",
                "-crf", 23, "-maxrate", "6M", "-bufsize", "12M", "-g", fps * 2, "-bf", 2, "-r", fps] + COLOR + [
                "-c:a", "aac", "-b:a", "160k", "-ar", 48000, "-ac", 2, "-movflags", "+faststart"]
    crf = {2160: 18, 1920: 17, 1080: 17}.get(height, 17)
    level = "5.1" if height >= 2160 else "4.2"
    return ["-c:v", "libx264", "-profile:v", "high", "-level", level, "-pix_fmt", "yuv420p", "-preset", os.environ.get("X264_PRESET", "medium"),
            "-crf", crf, "-g", fps * 2, "-bf", 2, "-r", fps] + COLOR + [
            "-c:a", "aac", "-b:a", "256k", "-ar", 48000, "-ac", 2, "-movflags", "+faststart"]


def outputs(name, cut, data, text_locale, no_4k):
    """[(file, picture size the file is composed at, final size, codec)]."""
    w, h = canvas(cut, data)
    stem = cut["file"]
    tag = "" if text_locale == "en" else f"-{text_locale}"
    if text_locale is None:
        tag = "-textless"
    if h > w:   # portrait: one size
        return [(f"{stem}{tag}-{w}x{h}.mp4", (w, h), (w, h), "h264")]
    outs = []
    if not no_4k and cut.get("uhd", True) and (text_locale in (None, "en")):
        outs.append((f"{stem}{tag}-2160p.mp4", (w, h), (w, h), "h264"))
    outs.append((f"{stem}{tag}-1080p.mp4", (1920, 1080), (1920, 1080), "h264"))
    if text_locale == "en":
        for x in cut.get("extra_outputs", []):
            outs.append((x["file"], (1920, 1080), tuple(x["size"]), x["codec"]))
    return outs


def render(name, cut, data, work, out, locale, cards, no_4k):
    """locale None: text-free. Otherwise lay the locale's cards and the wordmark over the picture.

    One ffmpeg run per picture size, from that size's timeline. Each card is a
    full-frame transparent PNG rendered at that size, decoded once and held with the
    loop filter, faded in and out on its alpha, and laid over the picture only
    between its cue times."""
    fps = data["fps"]
    dur = cut["duration"]
    nfr = round(dur * fps)
    by_size = {}
    for fname, compose, final, codec in outputs(name, cut, data, locale, no_4k):
        by_size.setdefault(compose, []).append((fname, final, codec))
    done = []
    for (w, h), outs in by_size.items():
        timeline = work / f"{name}-timeline-{w}x{h}.mkv"
        cmd = ["ffmpeg", "-v", "error", "-stats", "-y", "-i", timeline]
        graph = []
        last = "[0:v]"
        n_in = 1
        if locale is not None:
            fade = data["text"].get("fade", 0.25)
            layers = [(cards / locale / f"{w}x{h}" / f"{c['field']}.png", c["start"], c["end"], fade) for c in cut.get("text", [])]
            if cut.get("wordmark"):
                wm = cut["wordmark"]
                layers.append((cards / f"wordmark-{w}x{h}.png", wm["start"], dur + 1, wm.get("fade", 0.5)))
            for path, start, end, fd in layers:
                if not path.exists():
                    raise SystemExit(f"missing card {path}: run render_cards.py --locale {locale} --size {w}x{h}")
                cmd += ["-i", path]
                fo = f",fade=t=out:st={end - fd}:d={fd}:alpha=1" if end < dur else ""
                graph.append(f"[{n_in}:v]format=rgba,loop=loop={nfr}:size=1:start=0,setpts=N/{fps}/TB,"
                             f"fade=t=in:st={start}:d={fd}:alpha=1{fo}[c{n_in}]")
                graph.append(f"{last}[c{n_in}]overlay=0:0:format=auto:eof_action=pass:enable='between(t,{start},{end})'[v{n_in}]")
                last = f"[v{n_in}]"
                n_in += 1
        m_inputs, m_graph = music_filter(cut, data, n_in)
        cmd += m_inputs
        k = len(outs)
        graph.append(f"{last}format=yuv420p,split={k}" + "".join(f"[o{i}]" for i in range(k)))
        graph.append(m_graph + f";[a]asplit={k}" + "".join(f"[a{i}]" for i in range(k)))
        maps = []
        for i, (fname, final, codec) in enumerate(outs):
            label = f"[o{i}]"
            if final != (w, h):
                graph.append(f"[o{i}]scale={final[0]}:{final[1]}:flags=lanczos+accurate_rnd[p{i}]")
                label = f"[p{i}]"
            maps += ["-map", label, "-map", f"[a{i}]", "-t", dur] + encode_args(final[1], fps, codec) + [out / fname]
            done.append(out / fname)
        cmd += ["-filter_complex", ";".join(graph)] + maps
        run(cmd)
    return done


def poster(data, raw, out):
    """Poster PNGs scaled (Lanczos) straight from the native crop of one raw frame."""
    from PIL import Image
    p = data["poster"]
    cw, ch, cx, cy = p["crop"]
    src = Image.open(raw / p["shot"] / f"f{p['frame']:04d}.png").convert("RGB").crop((cx, cy, cx + cw, cy + ch))
    for fname, (w, h) in p["files"].items():
        (src if (w, h) == (cw, ch) else src.resize((w, h), Image.LANCZOS)).save(out / fname, optimize=True)
        print(f"{out / fname}: {p['shot']} frame {p['frame']}, crop {cw}x{ch}+{cx}+{cy} -> {w}x{h}")


def expand(data, name):
    """A cut may borrow another cut's timeline, text and music ("timeline_from") and
    reframe it: "reframe" gives one entry per segment, either a crop x for a window of
    the reframe width and the full map-rectangle height, or [x, y, width] for a smaller
    window of the cut's shape whose top is y pixels below the map rectangle's top
    (native pixels of the captured frame). A portrait cut is thus cut out of the same
    frames and never scaled up; the source cut's own segment crops, punch-ins and
    insets do not carry over."""
    cut = dict(data["cuts"][name])
    src = cut.get("timeline_from")
    if src:
        base = data["cuts"][src]
        for key in ("timeline", "text", "wordmark", "music", "duration"):
            cut.setdefault(key, base.get(key))
        rf = cut.get("reframe")
        if rf:
            _, ch, _, cy = data["frame"]["crop"]
            w, h = canvas(cut, data)
            segs = []
            for seg, x in zip(cut["timeline"], rf["x"]):
                if isinstance(x, list):
                    x, dy, ww = x
                    crop = [ww, round(ww * h / w), x, cy + dy]
                else:
                    crop = [rf["width"], ch, x, cy]
                segs.append({"shot": seg["shot"], "in": seg["in"], "frames": seg["frames"], "crop": crop})
            if len(segs) != len(cut["timeline"]):
                raise SystemExit(f"{name}: reframe has {len(rf['x'])} entries for {len(cut['timeline'])} segments")
            cut["timeline"] = segs
    return cut


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cuts")
    ap.add_argument("--raw", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--locale", default="en")
    ap.add_argument("--cards")
    ap.add_argument("--data", default=str(HERE / "trailer.json"))
    ap.add_argument("--only", help="timeline, clean, text or poster (default: timeline, clean, text)")
    ap.add_argument("--no-4k", action="store_true")
    args = ap.parse_args()
    data = json.loads(Path(args.data).read_text())
    raw, work, out = Path(args.raw), Path(args.work), Path(args.out)
    work.mkdir(parents=True, exist_ok=True)
    out.mkdir(parents=True, exist_ok=True)
    cards = Path(args.cards) if args.cards else work / "cards"
    steps = [args.only] if args.only else ["timeline", "clean", "text"]
    if "poster" in steps:
        poster(data, raw, out)
    for name in ([] if steps == ["poster"] else args.cuts.split(",")):
        cut = expand(data, name)
        total = sum(s["frames"] for s in cut["timeline"])
        if total != round(cut["duration"] * data["fps"]):
            raise SystemExit(f"{name}: timeline has {total} frames, duration {cut['duration']} s needs "
                             f"{round(cut['duration'] * data['fps'])}")
        locales = ([None] if cut.get("textless", True) else []) + args.locale.split(",")
        if "timeline" in steps:
            build_timeline(name, cut, data, raw, work, sizes_for(cut, data, args.no_4k, locales))
        if "clean" in steps and cut.get("textless", True):
            render(name, cut, data, work, out, None, cards, args.no_4k)
        if "text" in steps:
            for locale in args.locale.split(","):
                render(name, cut, data, work, out, locale, cards, args.no_4k)
    return 0


if __name__ == "__main__":
    sys.exit(main())
