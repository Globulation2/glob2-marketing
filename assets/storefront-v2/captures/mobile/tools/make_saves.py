#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Play a real custom match to mid-game and keep saved games along the way.

    python3 make_saves.py SCENARIO [--ticks 45000] [--every 3000] [--from 9000] [--speed 8]

The match is set up through the ordinary Custom game screen of the desktop
build (driven over the embedded MCP UI server): colony 1 is "You + AI" (the
lobby's shared-control option, so the save has a human player whose colony an
AI co-manages) and every other colony is an AI. The match then runs at a fixed
fast-forward speed, and the in-game menu's "Save game" writes a save every
--every ticks. No cheats, no edited saves, standard rules.

Fast-forward is capped at 13x (speed 8): at unlimited speed the simulation
outruns the AI controllers' asynchronous planning and colonies stay tiny.

Scenarios are defined in SCENARIOS below. Output: SCRATCH/saves/<scenario>-tNNNNN.game.gz
and SCRATCH/saves/<scenario>.telemetry.jsonl (tick, unit counts, buildings,
win chance, alert groups with tiles - used to pick moments and battle tiles).
"""
import argparse
import json
import shutil
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import g2  # noqa: E402
import mcp  # noqa: E402

# map: ("premade", list label prefix) or ("random", landscape label, width, height, colonies)
# players: AI label per colony; colony 1 is always You + AI with players[0].
SCENARIOS = {
    "foursquares": {"map": ("premade", "FourSquares1  (content"), "players": ["Maxima", "Nicowar", "Cortex", "Cabino"]},
    "balanced": {"map": ("premade", "balanced  (content"), "players": ["Maxima", "Nicowar", "Cortex", "Cabino"]},
    "bigpond": {"map": ("premade", "A big pond  (content"), "players": ["Maxima", "Nicowar", "Cortex"]},
    "muka": {"map": ("premade", "Muka  (content"), "players": ["Maxima", "Nicowar"]},
    "dejans": {"map": ("premade", "Dejans  (content"), "players": ["Maxima", "Nicowar"]},
    # Nicowar paints no forbidden or clearing zones, so the shared colony reads cleanly.
    "foursquares-n": {"map": ("premade", "FourSquares1  (content"), "players": ["Nicowar", "Nicowar", "Cortex", "Cabino"]},
    "bigpond-n": {"map": ("premade", "A big pond  (content"), "players": ["Nicowar", "Cortex", "Cabino"]},
    "muka-n": {"map": ("premade", "Muka  (content"), "players": ["Nicowar", "Cabino"]},
    "triangle-n": {"map": ("premade", "Triangle  (content"), "players": ["Nicowar", "Cortex", "Cabino"]},
    "garden-n": {"map": ("premade", "Garden 3  (content"), "players": ["Nicowar", "Cortex", "Cabino", "Nicowar"]},
    # Round 2: co-controllers that paint no zones and build up before fighting
    # (Castor, Numbi), and an eight-colony match with every computer opponent.
    "bigpond-castor": {"map": ("premade", "A big pond  (content"), "players": ["Castor", "Numbi", "Econo"]},
    "bigpond-numbi": {"map": ("premade", "A big pond  (content"), "players": ["Numbi", "Castor", "Econo"]},
    "playground-ffa": {"map": ("premade", "Playground  (content"),
                       "players": ["Castor", "Numbi", "Econo", "Warrush", "Cortex", "Nicowar", "Cabino", "Maxima"]},
    "playground-ffa-n": {"map": ("premade", "Playground  (content"),
                         "players": ["Nicowar", "Numbi", "Econo", "Warrush", "Cortex", "Castor", "Cabino", "Maxima"]},
    "playground-2222": {"map": ("premade", "Playground  (content"), "teams": "2 vs 2 vs 2 vs 2",
                        "players": ["Nicowar", "Maxima", "Cabino", "Cortex", "Warrush", "Numbi", "Econo", "Castor"]},
    "playground-44": {"map": ("premade", "Playground  (content"), "teams": "4 vs 4",
                      "players": ["Nicowar", "Maxima", "Cabino", "Cortex", "Warrush", "Numbi", "Econo", "Castor"]},
    "sandriver-n": {"map": ("premade", "Sand River  (content"),
                    "players": ["Nicowar", "Numbi", "Econo", "Warrush", "Cortex", "Cabino"]},
    "random8-n": {"map": ("random", 8),
                  "players": ["Nicowar", "Numbi", "Econo", "Warrush", "Cortex", "Castor", "Cabino", "Maxima"]},
    "playground-vsall": {"map": ("premade", "Playground  (content"), "teams": "You vs all",
                         "players": ["Maxima", "Numbi", "Econo", "Warrush", "Cortex", "Nicowar", "Cabino", "Castor"]},
    "playground-4v4": {"map": ("premade", "Playground  (content"), "teams": "4 vs 4",
                       "players": ["Numbi", "Castor", "Econo", "Cabino", "Warrush", "Cortex", "Nicowar", "Maxima"]},
    "small2": {"map": ("premade", "SmallForTwo  (content"), "players": ["Maxima", "Cortex"]},
    "balanced2": {"map": ("premade", "balanced for 2  (content"), "players": ["Maxima", "Nicowar"]},
    "triangle": {"map": ("premade", "Triangle  (content"), "players": ["Maxima", "Nicowar", "Cortex"]},
    "easythree": {"map": ("premade", "Easy Three  (content"), "players": ["Maxima", "Nicowar", "Cortex"]},
}


def setup(scenario):
    g2.act("menu/3")
    g2.wait_screen("custom_game")
    time.sleep(1.5)
    kind = scenario["map"][0]
    if kind == "premade":
        g2.act("map/mode/0")
        time.sleep(0.8)
        g2.act("map/list/0", "select", scenario["map"][1])
        time.sleep(1.5)
    else:
        # Random map on the lobby's default landscape with the given number of colonies.
        g2.act("map/mode/1")
        time.sleep(0.8)
        g2.act("generator/colonies", "select", str(scenario["map"][1]))
        time.sleep(6)
    g2.act("tab/1")
    time.sleep(0.8)
    players = scenario["players"]
    g2.act("colony/0/controller", "select", "You + AI")
    time.sleep(0.4)
    for index, ai in enumerate(players):
        if index:
            g2.act(f"colony/{index}/controller", "select", "AI")
            time.sleep(0.2)
        g2.act(f"colony/{index}/ai", "select", ai)
        time.sleep(0.2)
    if scenario.get("teams"):
        g2.act("teams", "select", scenario["teams"])
        time.sleep(0.5)
    lobby = mcp.tree(g2.PORT)
    g2.act("start")
    g2.wait_screen("game_session", 90)
    return lobby


def save(name, profile):
    """Game menu -> Save game -> name -> Ok; retried until the file exists."""
    target = profile / "games" / f"{name}.game.gz"
    for attempt in range(4):
        try:
            if not any(c.get("key") == "game/menu" for _, c in g2.controls()):
                g2.tcall("ui_key", key="Escape")  # close whatever dialog is in the way
                time.sleep(0.6)
            g2.act("game/menu")
            time.sleep(0.6)
            g2.act("save")
            time.sleep(0.6)
            g2.act("name", "set_value", name)
            time.sleep(0.3)
            g2.act("ok")
        except RuntimeError as error:
            print("save retry:", error, flush=True)
        for _ in range(20):
            if target.exists() and target.stat().st_size > 0:
                time.sleep(0.3)
                return target
            time.sleep(0.25)
    raise RuntimeError(f"could not save {name}")


def scan_fights(map_w, map_h, width=28, height=18, stride=12):
    """Windows of the map where several other colonies' units are in sight together."""
    found = []
    for y in range(0, map_h - height + 1, stride):
        for x in range(0, map_w - width + 1, stride):
            area = {"x": x, "y": y, "width": width, "height": height}
            others = g2.call("game_world", area=area, include=["others"])["others"]
            teams = {}
            for key, count in (others.get("units_by_team_and_type") or {}).items():
                team, kind = key.split(":")
                if kind != "explorer":
                    teams[team] = teams.get(team, 0) + count
            strong = {t: n for t, n in teams.items() if n >= 4}
            if len(strong) >= 2:
                found.append({"x": x, "y": y, "teams": strong})
    found.sort(key=lambda f: (-len(f["teams"]), -sum(f["teams"].values())))
    return found[:4]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenario", choices=sorted(SCENARIOS))
    parser.add_argument("--ticks", type=int, default=45000)
    parser.add_argument("--every", type=int, default=3000)
    parser.add_argument("--from", dest="start", type=int, default=9000)
    parser.add_argument("--speed", type=int, default=8, help="top-bar speed level; 8 is 13x, 7 is 8x")
    parser.add_argument("--scan", action="store_true", help="log windows where several rival colonies meet")
    args = parser.parse_args()
    scenario = SCENARIOS[args.scenario]
    profile = g2.SCRATCH / "gen" / args.scenario
    if profile.exists():
        shutil.rmtree(profile)
    g2.write_profile(profile)
    g2.SAVES.mkdir(parents=True, exist_ok=True)
    host = g2.Host(1600, 1000, 1, "desktop", profile)
    host_args = " ".join(host.command[1:])
    try:
        lobby = setup(scenario)
        (g2.SAVES / f"{args.scenario}.lobby.txt").write_text(host_args + "\n\n" + lobby + "\n")
        telemetry = (g2.SAVES / f"{args.scenario}.telemetry.jsonl").open("w")
        next_tick = args.every
        g2.game_time("resume", speed=args.speed)
        while True:
            now = g2.tick()
            if now < next_tick:
                time.sleep(0.25 if next_tick - now > 200 else 0.02)
                continue
            event_rows = [c.get("label") for _, c in g2.controls() if str(c.get("key")).startswith("game/events/")]
            g2.game_time("pause")
            world = g2.call("game_world", detail="brief")
            row = {"tick": world["tick"], "units": world["units"], "buildings": len(world["buildings"]),
                   "win_chance": world["status"]["win_chance"],
                   "lost": world["losses"]["buildings_destroyed_total"],
                   "event_rows": event_rows, "hud_workers": world["status"]["hud_sampled"]["workers"],
                   "alerts": [{k: a.get(k) for k in ("kind", "n", "x", "y", "area", "team", "ticks_ago")}
                              for a in world.get("alerts", [])]}
            if args.scan:
                size = g2.call("game_world", include=["map"])["map"]
                row["meetings"] = scan_fights(size["width"], size["height"])
                print("   meetings", [(m["x"], m["y"], m["teams"]) for m in row["meetings"]], flush=True)
            telemetry.write(json.dumps(row) + "\n")
            telemetry.flush()
            fights = sum(a["n"] or 0 for a in row["alerts"] if "attacked" in (a["kind"] or ""))
            print(row["tick"], row["units"], "buildings", row["buildings"], "win", row["win_chance"],
                  "attack reports", fights, "rows", len(event_rows), "workers", row["hud_workers"], flush=True)
            if g2.screen() != "game_session" or not world["units"]:
                print("match over")
                break
            if world["tick"] >= args.start:
                name = f"{args.scenario}-t{world['tick']:05d}"
                shutil.copy2(save(name, profile), g2.SAVES / f"{name}.game.gz")
            if world["tick"] >= args.ticks:
                break
            next_tick += args.every
            g2.game_time("resume", speed=args.speed)
    finally:
        host.close()


if __name__ == "__main__":
    main()
