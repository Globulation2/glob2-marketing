#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Round-3 AI co-play session: one recorded agent session, ending on the standing
order acting, with the game frame captured at that moment.

usage: uv run --with pillow --with numpy python coplay-session.py OUT_DIR X Y ZOOM
           [--match coral --tick 36000 --team 0] [--max-seconds 900]

Two clients talk to the same game:

* the "agent": a scripted MCP client (agent-session.py's call(), every call
  appended, request and response, to OUT_DIR/coplay-transcript.jsonl);
* the capture tooling (scene.py, session.py: load, bars off, zone erase,
  screenshot, ui_inspect reads, game_time polls). Its calls are not in the
  transcript; the sidecar lists them as player_actions_before_capture.

Agent calls, in order, all real and all recorded:
  1. hive_status                      (session id)
  2. game_world detail=brief          (the colony's status)
  3. hive_program install frontline-flag every 150 ticks (agent-session.FRONTLINE)
  4. game_view X Y ZOOM               (the camera on the front)
  5. hive_program inspect frontline-flag, once after each run of the standing
     order from its first run on (the first shows the flag being placed; the
     tooling waits on game_time for the next run, unrecorded), until
     one shows the order's latest run moving the flag ("moved") with orders
     sent >= 1.
Shortly before each run the tooling erases the view's zones and reads the HUD;
right after an inspect that shows a move it reads the in-game card and saves
the frame, then checks the HUD (top stat not negative, at most two event rows,
at the pre-run read and just before the frame), the zone outlines, that the in-game Hive card (read just
before the frame and again after it) shows the same output as the inspect, and that the moved flag
is in view.
If any check fails the frame is discarded and the agent keeps inspecting. The
session stops at the first kept frame, so the transcript ends on that inspect.
"""
import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import importlib.util  # noqa: E402

import mcp  # noqa: E402
import scene  # noqa: E402
import session  # noqa: E402

_spec = importlib.util.spec_from_file_location("agent_session", os.path.join(HERE, "agent-session.py"))
agent = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(agent)


def card_texts():
    """Labels and values of every control on screen that mentions the standing order
    or carries its JSON output (the in-game Hive card)."""
    out = []
    for _, ctl in mcp.walk(mcp.inspect(compact=False)):
        for k in ("label", "value", "value_label", "text"):
            v = ctl.get(k)
            if isinstance(v, str) and ("frontline" in v or v.startswith("{")):
                out.append({"key": ctl.get("key"), k: v})
    return out


def wait_tick(target, timeout=30):
    end = time.time() + timeout
    while time.time() < end:
        if session.gtime()["tick"] >= target:
            return
        time.sleep(0.05)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("x", type=int); ap.add_argument("y", type=int)
    ap.add_argument("zoom", type=float)
    ap.add_argument("--match", default="coral"); ap.add_argument("--tick", default="36000")
    ap.add_argument("--team", default="0"); ap.add_argument("--max-seconds", type=float, default=900)
    ap.add_argument("--prefix", default="ai-coplay-coral")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    tr = os.path.join(a.out, "coplay-transcript.jsonl")
    if os.path.exists(tr):
        raise SystemExit(f"{tr} exists: one transcript per session")

    scene.load(a.match, a.tick, a.team)                      # tooling: seat, bars off, clouds off
    st, _ = agent.call(tr, "hive_status", {})
    agent.call(tr, "game_world", {"detail": "brief"})
    inst, err = agent.call(tr, "hive_program", {
        "action": "install", "token": "", "session": st["session"],
        "operation_key": f"frontline-{int(time.time())}", "name": "frontline-flag",
        "description": "Keep one war flag on the enemy warrior nearest our buildings",
        "source": agent.FRONTLINE, "interval_ticks": 150})
    if err:
        raise SystemExit(f"install failed: {inst}")
    v, err = agent.call(tr, "game_view", {"token": "", "x": a.x, "y": a.y, "zoom": a.zoom})
    s = scene.state()
    s["camera"] = {"centre_tile": [a.x, a.y], "zoom": v["zoom"], "view_tiles": v["view"]}
    scene.save_state(s)
    vt = v["view"]
    world = session.world("summary")
    msize = (world["map"]["width"], world["map"]["height"])

    end = time.time() + a.max_seconds
    last_obs = None
    attempts = []
    while time.time() < end:
        # tooling: shortly before the order's next run, erase the view's zones and read the HUD,
        # so that little has to happen between the agent's inspect and the frame
        target = (last_obs + 150 + 18) if last_obs else session.gtime()["tick"] + 40
        wait_tick(target - 45)
        scene.erase(vt["x"] - 2, vt["y"] - 2, vt["width"] + 4, vt["height"] + 4)
        hud = scene.hud_state()
        wait_tick(target)
        ins, err = agent.call(tr, "hive_program", {"action": "inspect", "name": "frontline-flag"})
        rec = (ins or {}).get("recent") or {}
        if (ins or {}).get("paused") or rec.get("status") == "failed":
            print("standing order paused or failed:", str(rec.get("error"))[:160], flush=True)
            return 3
        if rec.get("observation_tick"):
            if rec["observation_tick"] == last_obs:  # the next run had not finished yet
                last_obs += 15
                continue
            last_obs = rec["observation_tick"]
        out = rec.get("output") or {}
        print("inspect", rec.get("observation_tick"), json.dumps(out), "orders", rec.get("order_count"), flush=True)
        if err or ins.get("paused") or "moved" not in out or (rec.get("order_count") or 0) < 1:
            continue
        # capture at this moment: read the card, then take the frame at once
        cards_before = card_texts()  # the card, HUD and flags as they are just before the frame is taken
        hud_now = scene.hud_state()
        flags_before = [b for b in session.world("summary")["colony"]["buildings"] if b["type"] == "warflag"]
        t = session.gtime()["tick"]
        path = os.path.join(a.out, f"{a.prefix}-{t}.png")
        try:
            side = scene.shot(path)
        except RuntimeError as exc:  # e.g. the PNG encoder missed its deadline on a busy machine
            print("shot failed", str(exc)[:120], flush=True)
            continue
        share = scene.zone_share(path)
        after = scene.hud_state()
        cards = card_texts()
        flags = [b for b in session.world("summary")["colony"]["buildings"] if b["type"] == "warflag"]
        mx, my = out["moved"]
        # A 3840x2160 PNG takes seconds to encode on a busy machine, long enough for the next run to
        # move the flag again, so the flag and the HUD are judged as read just before the frame.
        mine = [b for b in flags_before if abs(b["x"] - mx) + abs(b["y"] - my) <= 1]
        px = scene.tile_native(mx, my) if mine else None
        W, H = side["window"]
        in_view = bool(px) and 120 < px[0] < W - 520 and 260 < px[1] < H - 120 and not (px[0] < 700 and px[1] > H - 520)
        # ui_screenshot saves the next rendered frame and then encodes it (seconds at 3840x2160), so the card
        # is read just before the call and again after it: only if both show the inspected output can no
        # later run have changed it in between, so the frame shows it too (checked by eye as well)
        want = json.dumps(out, separators=(",", ":"))
        card_ok = all(any(want in (c.get("label") or c.get("value") or c.get("text") or "") for c in cs)
                      for cs in (cards_before, cards))
        hud_ok = all(h["free"] >= 0 and h["events"] <= 2 for h in (hud, hud_now))
        ok = hud_ok and share <= 1.0 and in_view and card_ok
        side.update({"zone_outline_share_per_10000": share,
                     "hud": {"before": hud, "just_before_frame": hud_now, "after": after},
                     "hive_card": cards_before, "hive_card_after_shot": cards, "agent_flag": {"tile": [mx, my], "native_px": px, "building": mine},
                     "other_warflags_in_colony": [b for b in flags_before if b not in mine],
                     "warflags_before_shot": flags_before, "warflags_after_shot": flags,
                     "transcript_calls": sum(1 for _ in open(tr)),
                     "inspect_observation_tick": rec.get("observation_tick"),
                     "checks": {"hud": hud_ok, "zones": share <= 1.0, "flag_in_view": in_view,
                                "card_matches_inspect": card_ok}})
        attempts.append({"tick": t, "checks": side["checks"]})
        print("attempt", t, side["checks"], flush=True)
        if ok:
            try:
                side["fog_of_war_in_view"] = scene.fog_share(vt)
            except Exception as exc:  # a read only; keep the frame
                side["fog_of_war_in_view"] = {"error": str(exc)[:100]}
            side["player_actions_before_capture"] = scene.state().get("actions", []) + [
                "agent (scripted MCP client, see transcript): hive_program install frontline-flag; game_view; "
                "the standing order then placed and moved its war flag by itself"]
            side["attempts"] = attempts
            json.dump(side, open(path[:-4] + ".json", "w"), indent=1)
            print("kept", path, flush=True)
            return 0
        os.rename(path, path[:-4] + "-discarded.png")
        if os.path.exists(path[:-4] + ".json"):
            os.remove(path[:-4] + ".json")
        json.dump(side, open(path[:-4] + "-discarded.json", "w"), indent=1)
    print("no frame kept", flush=True)
    return 1


if __name__ == "__main__":
    sys.exit(main())
