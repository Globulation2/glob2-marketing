#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Cut, caption, score and encode the App Store app previews from the raw simulator takes.

    uv run --with pillow --with numpy python build_previews.py --raw RAW --cards CARDS --out OUT \
        [--device iphone-6.9,ipad-13] [--locale en] [--textless] [--poster]

RAW holds <device>/<take>.mov from record.py; CARDS holds the text cards from the
trailer's render_cards.py run with --data previews.json at each preview size
(CARDS/<locale>/<WxH>/<field>.png and CARDS/wordmark-<WxH>.png). Everything the
edit does is data in previews.json: per device, the timeline (take, in point,
length), the text cues (catalog field, start, end), the wordmark start and the
music plan. A localized preview is the same command with another --locale once its
cards are rendered.

Picture path per segment: the take's own frames from `in` for `seconds`, put on a
constant 30 fps grid (each output frame shows the take's frame on screen at that
moment, so the game plays at its real speed), then one Lanczos downscale from the
simulator's native pixels to Apple's preview size (iPhone 1320x2868 -> 886x1925,
then the 5 bottom rows of the empty home-indicator band are cropped to 886x1920;
iPad 2064x2752 -> 1200x1600 exactly). On iPhone, `simctl io recordVideo` draws the
simulator's Dynamic Island cut-out into the status bar, which no device screen
recording or `simctl io screenshot` contains: that pill is filled with the flat
status-bar colour around it (`island` in previews.json; check_previews.py verifies
the fill matches the bar). Nothing else in the picture is touched.

Encode: H.264 High profile, level 4.0, yuv420p, BT.709, progressive, constant
30 fps, about 11 Mbps (Apple: target 10-12 Mbps, up to High 4.0), AAC-LC 256 kbps
stereo 48 kHz, MP4 with faststart.
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TRAILER_TOOLS = HERE.parents[1] / "trailer" / "tools"
GAME = Path(os.environ.get("GLOB2_GAME") or HERE.parents[4] / "glob2")
FPS = 30
COLOR = ["-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv"]


def run(cmd):
    cmd = [str(c) for c in cmd]
    print("+", " ".join(cmd[:6]), "...", flush=True)
    subprocess.run(cmd, check=True)


def music_filter(cut, first_input):
    """The trailer's music plan: the game's soundtrack moods cross-faded on one timeline."""
    sys.path.insert(0, str(TRAILER_TOOLS))
    m = cut["music"]
    dur = cut["duration"]
    xf = m.get("crossfade", 0.8)
    moods = sorted({s["mood"] for s in m["segments"]})
    parts, labels = [], []
    for k, mood in enumerate(moods):
        terms = []
        for s in m["segments"]:
            if s["mood"] != mood:
                continue
            a, b = s["from"], s["to"]
            up = "1" if a <= 0 else f"clip((t-{a - xf / 2})/{xf},0,1)"
            down = "1" if b >= dur else f"clip(({b + xf / 2}-t)/{xf},0,1)"
            terms.append(f"min({up},{down})")
        gain = 10 ** (m.get("mood_gain_db", {}).get(mood, 0) / 20)
        expr = f"{gain:.6f}*({'+'.join(terms)})"
        parts.append(f"[{first_input + k}:a]atrim=start={m.get('offset', 0)},asetpts=PTS-STARTPTS,"
                     f"atrim=end={dur},aresample=48000,volume='{expr}':eval=frame[m{k}]")
        labels.append(f"[m{k}]")
    tail = m.get("tail_fade", 2.0)
    lim = m["limiter"]
    parts.append("".join(labels) + f"amix=inputs={len(moods)}:normalize=0,volume={m.get('gain_db', 0)}dB,"
                 f"afade=t=in:st=0:d=0.04,afade=t=out:st={dur - tail}:d={tail},"
                 f"aresample=192000,alimiter=limit={lim['limit']}:attack={lim['attack_ms']}:"
                 f"release={lim['release_ms']}:level=disabled,"
                 f"aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[a]")
    inputs = []
    for mood in moods:
        inputs += ["-i", GAME / "content" / "data" / "zik" / m["set"] / f"{mood}.opus"]
    return inputs, ";".join(parts)


def picture_chain(dev, seg_label, out_label, start, seconds):
    """Trim one take onto the 30 fps grid, fill the simulator's island, scale to the preview size."""
    w, h = dev["size"]
    nw, nh = dev["native"]
    chain = [f"trim=start={start}:duration={seconds + 0.2}", "setpts=PTS-STARTPTS", f"fps={FPS}:round=near",
             f"trim=end_frame={round(seconds * FPS)}", "setpts=N/(FR*TB)"]
    if dev.get("island"):
        i = dev["island"]
        chain.append(f"drawbox=x={i['x']}:y={i['y']}:w={i['w']}:h={i['h']}:color={i['color']}:t=fill")
    # The simulator recording is Display P3 (smpte432 primaries, sRGB curve; the status bar's
    # sRGB 0,0,32 arrives as 0,0,30). Convert the primaries to BT.709, keeping the sRGB curve,
    # so the pixels match the simulator's own screenshots and the store screenshots.
    chain += ["colorspace=iall=bt709:iprimaries=smpte432:itrc=srgb:irange=tv:"
              "space=bt709:primaries=bt709:trc=srgb:range=tv:format=yuv420p"]
    sh = round(nh * w / nw)
    chain += ["format=gbrp", f"scale={w}:{sh}:flags=lanczos+accurate_rnd+full_chroma_int"]
    if sh != h:
        chain.append(f"crop={w}:{h}:0:0")  # the empty home-indicator band at the bottom
    return f"[{seg_label}]" + ",".join(chain) + f"[{out_label}]"


def build(device, cfg, args, locale, textless):
    dev = cfg["devices"][device]
    cut = cfg["cuts"][device]
    w, h = dev["size"]
    raw = Path(args.raw) / device
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    name = cut["file"] + ("-textless" if textless else ("" if locale == "en" else f"-{locale}")) + ".mp4"
    total = sum(s["seconds"] for s in cut["timeline"])
    assert abs(total - cut["duration"]) < 1e-6, (total, cut["duration"])
    inputs, graph = [], []
    takes = []
    for s in cut["timeline"]:
        if s["take"] not in takes:
            takes.append(s["take"])
            inputs += ["-i", raw / f"{s['take']}.mov"]
    for k, s in enumerate(cut["timeline"]):
        ti = takes.index(s["take"])
        graph.append(f"[{ti}:v]null[src{k}]")
        graph.append(picture_chain(dev, f"src{k}", f"v{k}", s["in"], s["seconds"]))
    graph.append("".join(f"[v{k}]" for k in range(len(cut["timeline"]))) +
                 f"concat=n={len(cut['timeline'])}:v=1:a=0,format=gbrp[base]")
    last = "base"
    n_in = len(takes)
    fade = cfg["text"]["fade"]
    overlays = []
    if not textless:
        for cue in cut["text"]:
            overlays.append((Path(args.cards) / locale / f"{w}x{h}" / f"{cue['field']}.png", cue["start"], cue["end"]))
    if cut.get("wordmark") and not textless:
        overlays.append((Path(args.cards) / f"wordmark-{w}x{h}.png", cut["wordmark"]["start"], cut["duration"] + 1))
    for k, (png, a, b) in enumerate(overlays):
        inputs += ["-loop", "1", "-framerate", FPS, "-t", cut["duration"], "-i", png]
        fo = f",fade=t=out:st={b - fade}:d={fade}:alpha=1" if b < cut["duration"] else ""
        graph.append(f"[{n_in}:v]format=rgba,fade=t=in:st={a}:d={fade}:alpha=1{fo}[c{k}]")
        graph.append(f"[{last}][c{k}]overlay=0:0:format=gbrp:enable='between(t,{a},{b})'[o{k}]")
        last = f"o{k}"
        n_in += 1
    graph.append(f"[{last}]scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,"
                 f"setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv[vout]")
    m_inputs, m_graph = music_filter(cut, n_in)
    inputs += m_inputs
    graph.append(m_graph)
    kbps = cfg["encode"]["video_kbps"]
    cmd = ["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(graph), "-map", "[vout]", "-map", "[a]",
           "-c:v", "libx264", "-profile:v", "high", "-level", "4.0", "-pix_fmt", "yuv420p", "-preset", "slow",
           "-b:v", f"{kbps}k", "-maxrate", f"{cfg['encode']['max_kbps']}k", "-bufsize", f"{cfg['encode']['buf_kbps']}k",
           "-x264-params", "nal-hrd=vbr", "-g", FPS * 2, "-bf", 2, "-r", FPS, "-fps_mode", "cfr", *COLOR,
           "-c:a", "aac", "-b:a", "256k", "-ar", 48000, "-ac", 2,
           "-t", cut["duration"], "-movflags", "+faststart", out_dir / name]
    # Two-pass for an even ~11 Mbps.
    passlog = out_dir / f".{name}.x264"
    first = cmd[:]
    i = first.index("-c:a")
    first = first[:i] + ["-an", "-pass", 1, "-passlogfile", passlog, "-f", "mp4", "/dev/null"]
    run(first)
    second = cmd[:]
    j = second.index("-c:a")
    second = second[:j] + ["-pass", 2, "-passlogfile", passlog] + second[j:]
    run(second)
    for p in out_dir.glob(f".{name}.x264*"):
        p.unlink()
    return out_dir / name


def poster(device, cfg, args, mp4):
    t = cfg["cuts"][device]["poster"]["time"]
    w, h = cfg["devices"][device]["size"]
    png = Path(args.out) / f"poster-{device}-{w}x{h}.png"
    run(["ffmpeg", "-y", "-v", "error", "-ss", t, "-i", mp4, "-frames:v", 1, png])
    return png


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", default=str(HERE / "previews.json"))
    ap.add_argument("--raw", required=True)
    ap.add_argument("--cards", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--device", default="iphone-6.9,ipad-13")
    ap.add_argument("--locale", default="en")
    ap.add_argument("--textless", action="store_true")
    ap.add_argument("--poster", action="store_true")
    args = ap.parse_args()
    cfg = json.loads(Path(args.data).read_text())
    for device in args.device.split(","):
        for locale in args.locale.split(","):
            mp4 = build(device, cfg, args, locale, args.textless)
            print(mp4)
            if args.poster and locale == "en" and not args.textless:
                print(poster(device, cfg, args, mp4))


if __name__ == "__main__":
    main()
