"""Idle camera director: keeps the stream camera moving when nobody in chat is steering it.

Run from chat_agent.py's loop (no model calls). When the camera hasn't moved for
CAMERA_IDLE_SECONDS, it reads the colony with game_world (read-only, follows fog of war) and
picks the next shot deterministically: new alert tiles first (fights are the best TV), then a
rotation of the colony overview, one of Claude's buildings, a resource field, the frontier,
enemy buildings Claude has seen and, now and then, the whole map. Zoom varies between 1, 0.7,
0.5 and 0, never above 1. Moves go through camera.show(), with its rate limit and labels.
"""
import json
import math

import camera

ROTATION = ("colony", "building", "resource", "frontier", "enemy", "building", "colony", "map")
INTERESTING = ("barracks", "defensetower", "stonewall", "hospital", "school", "racetrack", "swimmingpool",
               "market", "inn", "swarm", "exploration", "warflag", "clearingflag")
ALERT_FRESH_TICKS = 900   # 30 s of game time: older alerts are history, not live action
# Checked in order against an alert's kind (substring).
ALERT_LABELS = {"building_lost": "Live: a building lost", "attack": "Live: fight", "conversion": "Live: globs leaving",
                "enemy_building_sighted": "Live: enemy building spotted", "enemy_sighted": "Live: enemy spotted",
                "building_completed": "Live: new building finished", "hive": None}
PRETTY = {"defensetower": "defence tower", "stonewall": "stone wall", "swimmingpool": "swimming pool",
          "warflag": "war flag", "explorationflag": "exploration flag", "clearingflag": "clearing flag"}


def world() -> dict:
    out = camera._rpc("game_world", {"detail": "summary", "limit": 40, "resource_radius": 40})
    res = out.get("result") or {}
    text = "".join(c.get("text", "") for c in res.get("content", []))
    return json.loads(text) if text and not res.get("isError") else {}


def _xy(d: dict):
    if isinstance(d, dict):
        if isinstance(d.get("x"), int) and isinstance(d.get("y"), int):
            return d["x"] + int(d.get("width", 1)) // 2, d["y"] + int(d.get("height", 1)) // 2
        for k in ("tile", "at", "position", "nearest"):
            if isinstance(d.get(k), dict):
                return _xy(d[k])
    return None


def pretty(kind: str) -> str:
    kind = str(kind or "building")
    return PRETTY.get(kind, kind.replace("_", " "))


class Director:
    def __init__(self):
        self.turn = 0
        self.building_turn = 0
        self.seen_alerts = set()

    def next_shot(self, w: dict):
        """Return camera.show() keyword arguments, or None when there's nothing to show."""
        colony = (w.get("colony") or {}).get("buildings") or []
        mw, mh = (w.get("map") or {}).get("width", 256), (w.get("map") or {}).get("height", 256)
        for a in w.get("alerts") or []:
            pos = _xy(a)
            key = f"{a.get('kind')}@{a.get('x')},{a.get('y')}#{a.get('last_tick')}"
            fresh = int(a.get("ticks_ago", 0) or 0) <= ALERT_FRESH_TICKS
            if pos and fresh and key not in self.seen_alerts:
                self.seen_alerts.add(key)
                kind = str(a.get("kind") or "")
                label = next((v for k, v in ALERT_LABELS.items() if k in kind), None) or \
                    str(a.get("event") or kind or "Action").replace("_", " ")
                return dict(x=pos[0], y=pos[1], zoom=0.7, label=label)
        if len(self.seen_alerts) > 500:
            self.seen_alerts.clear()
        for _ in range(len(ROTATION)):
            kind = ROTATION[self.turn % len(ROTATION)]
            self.turn += 1
            shot = getattr(self, "_" + kind)(w, colony, mw, mh)
            if shot:
                return shot
        return None

    def _colony(self, w, colony, mw, mh):
        pts = [_xy(b) for b in colony if _xy(b)]
        if not pts:
            return None
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        width, height = max(xs) - min(xs) + 16, max(ys) - min(ys) + 12
        if width > 120 or height > 120:  # spread out (or across the map wrap): centre on the swarm instead
            return dict(x=pts[0][0], y=pts[0][1], zoom=0.5, label="Claude's colony")
        return dict(x=(min(xs) + max(xs)) // 2, y=(min(ys) + max(ys)) // 2,
                    width=min(width, 256), height=min(height, 256), label="Claude's colony")

    def _building(self, w, colony, mw, mh):
        picks = [b for b in colony if any(str(b.get("type", "")).startswith(t) for t in INTERESTING) and _xy(b)]
        if not picks:
            return None
        b = picks[self.building_turn % len(picks)]
        self.building_turn += 1
        x, y = _xy(b)
        return dict(x=x, y=y, zoom=1, label=f"Claude's {pretty(b.get('type'))}")

    def _resource(self, w, colony, mw, mh):
        res = w.get("resources") or {}
        for name in ("wheat", "wood", "stone", "algae", "cherries", "oranges", "prunes"):
            field = (res.get(name) or {}).get("fields") or []
            if field and _xy(field[0]):
                x, y = _xy(field[0])
                return dict(x=x, y=y, zoom=0.7, label=f"{name.capitalize()} near the colony")
        return None

    def _frontier(self, w, colony, mw, mh):
        pts = [(_xy(b), b) for b in colony if _xy(b)]
        if len(pts) < 2:
            return None
        (sx, sy), _ = pts[0]

        def dist(p):  # the map wraps
            dx, dy = abs(p[0] - sx), abs(p[1] - sy)
            return math.hypot(min(dx, mw - dx), min(dy, mh - dy))
        (x, y), b = max(pts, key=lambda pb: dist(pb[0]))
        return dict(x=x, y=y, zoom=0.7, label="The frontier") if dist((x, y)) > 12 else None

    def _enemy(self, w, colony, mw, mh):
        others = w.get("others") or {}
        seen = [b for b in (others.get("buildings") or []) + (others.get("remembered_buildings") or []) if _xy(b)]
        if not seen:
            return None
        b = seen[0]
        x, y = _xy(b)
        return dict(x=x, y=y, zoom=0.7, label=f"Enemy {pretty(b.get('type'))} (last seen)")

    def _map(self, w, colony, mw, mh):
        return dict(zoom=0, label="The whole map")

    def step(self) -> tuple:
        """Choose and make one shot. Returns (ok, message, shot)."""
        try:
            w = world()
        except Exception as e:  # game busy or between matches: try again next time
            return False, f"no game view ({type(e).__name__})", None
        if not w:
            return False, "no game view", None
        shot = self.next_shot(w)
        if not shot:
            return False, "nothing to show", None
        ok, msg = camera.show(source="director", **shot)
        return ok, msg, shot
