#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Arrange a real game frame beside the transcript of the same MCP session.

usage: uv run --with pillow python coplay-side-by-side.py GAME.png TRANSCRIPT.jsonl OUT.png \
           [--width 3840 --height 2160] [--calls N]

GAME.png is a native frame from the game window of the session (its height must
equal the output height). TRANSCRIPT.jsonl is written by agent-session.py (or
coplay-session.py): one line per MCP tool call, request and response, in the
order they happened. The panel shows the last N calls (default 6), each as the
tool name with its key arguments and a one-line summary of the game's real
response. With --all, it shows every call of the session in order, and a run
of consecutive `hive_program inspect` calls between the first and the last is
collapsed into one dimmed line that says how many calls it stands for and what
they returned ("... 3 more inspect calls: holding, moved ..."), so nothing is
reordered or hidden without saying so. Nothing is invented: every line is
derived from a transcript entry, and the token is never shown. Labelled in the
manifest as "game frame plus transcript of the same session, arranged side by
side".
"""
import argparse
import json
import textwrap

from PIL import Image, ImageDraw, ImageFont

BG = (16, 14, 40)        # close to the game's navy HUD
FG = (226, 228, 240)
DIM = (140, 146, 190)
ACCENT = (249, 232, 187)  # brand cream, for the prompt
OK = (150, 220, 150)


def summarise(entry):
    """The tool name with its key arguments and a short summary of the real response."""
    tool, a, r = entry["tool"], entry["arguments"], entry["result"]
    if tool == "hive_status":
        return "hive_status", [f"available: {str(r.get('available')).lower()}  programs: {r.get('programs')}",
                               f"tick {r.get('tick')}"]
    if tool == "game_world":
        st = r.get("status", {})
        return f"game_world detail={a.get('detail', 'summary')}", [
            f"workers {st.get('workers_free_total')}  warriors {st.get('warriors_free_total')}",
            f"{len(r.get('buildings', []))} buildings, {len(r.get('alerts', []))} alerts"]
    if tool == "hive_program":
        act = a.get("action")
        if act == "inspect":
            rec = r.get("recent") or {}
            return f"hive_program inspect {a.get('name', '')}", [
                f"revision {r.get('program', {}).get('revision')}  {'paused' if r.get('paused') else 'running'}"
                f"  tick {rec.get('observation_tick')}",
                "output " + json.dumps(rec.get("output"), separators=(",", ":")),
                f"orders sent: {rec.get('order_count')}"]
        head = f"hive_program {act} {a.get('name', '')}".rstrip()
        if act == "install":
            return head + f" every {a.get('interval_ticks')} ticks", [
                f'"{a.get("description", "")}"', f"status: {r.get('status')}"]
        if act == "list":
            p = (r.get("programs") or [{}])[0]
            return head, [f"{p.get('name')}  next tick {p.get('nextTick')}",
                          "output " + json.dumps((p.get("recent") or {}).get("output"), separators=(",", ":"))]
        return head, [str(r.get("status", ""))]
    if tool == "game_view":
        return f"game_view x={a.get('x')} y={a.get('y')} zoom={a.get('zoom')}", [
            f"camera on tiles {r.get('view', {}).get('x')},{r.get('view', {}).get('y')}"]
    return tool, [json.dumps(r)[:60]]


def inspect_word(e):
    out = ((e["result"].get("recent") or {}).get("output")) or {}
    word = next((k for k in ("placed", "moved", "holding", "waiting_for_flag") if k in out), None)
    return word or out.get("note") or "no output"


def collapse(entries, keep_first):
    """Every entry in order; inside each run of consecutive inspect calls, keep the
    first `keep_first` and the last in full and replace the middle with one line."""
    def is_inspect(e):
        return e["tool"] == "hive_program" and e["arguments"].get("action") == "inspect"
    out, i = [], 0
    while i < len(entries):
        if not is_inspect(entries[i]):
            out.append(entries[i]); i += 1; continue
        j = i
        while j < len(entries) and is_inspect(entries[j]):
            j += 1
        run = entries[i:j]
        if len(run) <= keep_first + 2:
            out += run
        else:
            middle = run[keep_first:-1]
            words = []
            for m in middle:
                w = inspect_word(m)
                if w not in words:
                    words.append(w)
            ticks = [(m["result"].get("recent") or {}).get("observation_tick") for m in middle]
            out += run[:keep_first]
            out.append({"elided": f"... {len(middle)} more hive_program inspect calls "
                                  f"(runs at ticks {ticks[0]}-{ticks[-1]}): {', '.join(words)} ..."})
            out.append(run[-1])
        i = j
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("game"); ap.add_argument("transcript"); ap.add_argument("out")
    ap.add_argument("--width", type=int, default=3840)
    ap.add_argument("--height", type=int, default=2160)
    ap.add_argument("--calls", type=int, default=6)
    ap.add_argument("--all", action="store_true", help="every call, collapsing middle inspect runs")
    ap.add_argument("--keep-inspects", type=int, default=1,
                    help="with --all: inspect calls shown in full at each end of a run (first N, last 1)")
    ap.add_argument("--font", default="/System/Library/Fonts/Menlo.ttc")
    args = ap.parse_args()
    game = Image.open(args.game).convert("RGB")
    if game.size[1] != args.height:
        raise SystemExit("the game frame must be as tall as the output")
    pw = args.width - game.size[0]
    canvas = Image.new("RGB", (args.width, args.height), BG)
    canvas.paste(game, (0, 0))
    d = ImageDraw.Draw(canvas)
    size = max(28, pw // 26)
    font = ImageFont.truetype(args.font, size)
    bold = ImageFont.truetype(args.font, size, index=1)
    x0, y = game.size[0] + size, size * 2
    d.line([(game.size[0], 0), (game.size[0], args.height)], fill=(60, 56, 100), width=4)
    d.text((x0, y), "MCP session (local)", font=bold, fill=DIM)
    y += int(size * 2.2)
    entries = [json.loads(l) for l in open(args.transcript) if l.strip()]
    cols = max(16, (pw - 2 * size) // int(size * 0.61))
    shown = entries[-args.calls:] if not args.all else collapse(entries, args.keep_inspects)
    for e in shown:
        if e.get("elided"):
            for part in textwrap.wrap(e["elided"], cols - 2):
                d.text((x0, y), "  " + part, font=font, fill=DIM)
                y += int(size * 1.3)
            y += int(size * 0.8)
            continue
        head, lines = summarise(e)
        for i, part in enumerate(textwrap.wrap(head, cols - 2) or [head]):
            d.text((x0, y), ("> " if i == 0 else "  ") + part, font=bold, fill=ACCENT)
            y += int(size * 1.3)
        for line in lines:
            for part in textwrap.wrap(line, cols - 2):
                d.text((x0, y), "  " + part, font=font, fill=OK if "error" not in part else (240, 120, 120))
                y += int(size * 1.3)
        y += int(size * 0.8)
    if y > args.height - size:
        raise SystemExit(f"panel overflows ({y} px of {args.height}); use fewer calls")
    canvas.save(args.out)


if __name__ == "__main__":
    main()
