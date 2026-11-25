"""Smooth camera drift: between explicit camera moves, pan the view slowly toward the action.

The player, the chat host and the director cut the camera with game_view (instant jumps). In
between, this loop (no model calls) keeps the picture alive: every CAMERA_DRIFT_POLL seconds it
reads the colony with game_world (read-only, follows fog of war) and picks a target, and every
CAMERA_DRIFT_STEP seconds it nudges the view toward it with a tiny middle-button drag on the map.

Measured on the game (2026-11-24): middle-button drags pan the view one pixel per pixel, can't
select units or place buildings (left drags could), and with the game's map-scroll momentum a
chain of 12 px / 120 ms drags moves the view steadily at ~2 tiles/s at zoom 0.7. Holding arrow
keys was too fast (~38 tiles/s) to drift with. Each drag holds the game's MCP queue for its
duration, so drags stay short (other calls waited ~0.2 s).

Targets, in order: fresh alerts (fights, losses, sightings); visible enemy units near Claude's;
Claude's units that are moving (largest moving group); otherwise a slow circle around the last
explicit camera target. Drift never zooms, pauses for CAMERA_DRIFT_PAUSE seconds after any
explicit move, stays near a viewer-request hold's target, and only chases targets within
CAMERA_DRIFT_RANGE tiles of the view centre (farther action is for explicit cuts). It uses the
player's control token (published by game_proxy to STATE_DIR/control-token) and never shows it.
"""
import json
import math
import threading
import time

import camera

ALERT_FRESH_TICKS = 300      # ~10 s of game time
MOVE_MIN = 2                 # tiles a unit must move between polls to count as moving
CELL = 12                    # grouping cell for moving units, in tiles
ORBIT_RADIUS = 4             # tiles around the last explicit target
ORBIT_PERIOD = 40.0          # seconds per circle
DEADZONE = 2.0               # tiles: close enough
TARGET_BLEND = 0.35          # how far a new target of the same kind moves the old one per poll
CENTRE = (960, 520)          # screen point drags are made around (logical pixels, over the map)


def _f(name, default):
    try:
        return float(camera.env(name, str(default)))
    except ValueError:
        return float(default)


class Drift:
    def __init__(self):
        # Continuous glide: hold the middle button and move the pointer a little ~30 times a second
        # (2026-11-24: 120 ms drags every 0.2 s read as stop-start). Speed is in pixels per second.
        self.step_s = _f("CAMERA_DRIFT_STEP", 0.033)
        self.px_per_s = _f("CAMERA_DRIFT_PX_PER_S", 60)
        self.ptr = None           # pointer position while the middle button is held
        self.held_at = 0.0
        self.poll_s = _f("CAMERA_DRIFT_POLL", 3.0)
        self.pause_s = _f("CAMERA_DRIFT_PAUSE", 2.0)
        self.range = _f("CAMERA_DRIFT_RANGE", 40)
        self.px_per_step = _f("CAMERA_DRIFT_SPEED", 12)    # pixels per step (~60 px/s at 0.2 s steps)
        self.view = None          # {"x","y","width","height"} in tiles, top-left based
        self.map = (256, 256)
        self.tile_px = 22.4
        self.target = None
        self.reason = ""
        self.prev_units = {}
        self.last_poll = 0.0
        self.anchor = None        # last explicit target (tile) and when
        self.anchor_at = 0.0
        self.holding = False
        self.stop = threading.Event()

    # -- game ------------------------------------------------------------------
    def _world(self) -> dict:
        out = camera._rpc("game_world", {"detail": "full", "include": ["view", "map", "alerts", "colony", "others"]})
        res = out.get("result") or {}
        text = "".join(c.get("text", "") for c in res.get("content", []))
        if not text or res.get("isError"):
            return {}
        try:
            return json.loads(text)
        except ValueError:
            return {}

    def _wrap(self, d, size):
        return (d + size / 2) % size - size / 2

    def centre(self):
        v = self.view
        return (v["x"] + v["width"] / 2, v["y"] + v["height"] / 2)

    def poll(self) -> None:
        w = self._world()
        if not w or "view" not in w:
            self.view = None
            return
        self.view = w["view"]
        m = w.get("map") or {}
        self.map = (m.get("width", 256), m.get("height", 256))
        # tile size on screen: the screen is ~1716 px of map across the view's width
        self.tile_px = max(4.0, 1716.0 / max(1, self.view["width"]))
        cx, cy = self.centre()
        last = camera.last_move()
        if last.get("x") is not None and last.get("at", 0) > self.anchor_at:
            self.anchor, self.anchor_at = (last["x"], last["y"]), last["at"]
        elif last.get("at", 0) > self.anchor_at:
            self.anchor, self.anchor_at = (cx, cy), last["at"]
        target, reason = self.pick(w, cx, cy)
        # Glide between targets instead of jumping: blend a new target of the same kind into the old
        # one, so the camera doesn't wander back and forth between nearby groups of units.
        if target and self.target and reason == self.reason and reason in ("movers", "enemies"):
            k = TARGET_BLEND
            target = (self.target[0] + k * self._wrap(target[0] - self.target[0], self.map[0]),
                      self.target[1] + k * self._wrap(target[1] - self.target[1], self.map[1]))
        self.target, self.reason = target, reason

    def pick(self, w, cx, cy):
        def near(x, y):
            return (abs(self._wrap(x - cx, self.map[0])) <= self.range
                    and abs(self._wrap(y - cy, self.map[1])) <= self.range)
        # A viewer request holds the camera on its target: only circle that.
        if camera.hold_remaining() > 0 and self.anchor:
            return self._orbit(), "hold"
        # 1. fresh alerts
        for a in w.get("alerts") or []:
            if not isinstance(a, dict) or int(a.get("ticks_ago", 9999) or 9999) > ALERT_FRESH_TICKS:
                continue
            area = a.get("area")
            if isinstance(area, dict) and area.get("width", 99) <= 40 and area.get("height", 99) <= 40:
                x, y = area["x"] + area["width"] / 2, area["y"] + area["height"] / 2
            elif isinstance(a.get("x"), int):
                x, y = a["x"], a["y"]
            else:
                continue
            if near(x, y):
                return (x, y), "alert"
        # 2. visible enemy units close to the view
        enemies = [(u["x"], u["y"]) for u in (w.get("others") or {}).get("unit_list") or []
                   if isinstance(u, dict) and isinstance(u.get("x"), int) and near(u["x"], u["y"])]
        if enemies:
            return self._mean(enemies), "enemies"
        # 3. Claude's units on the move: the busiest group of movers
        units = {u["id"]: (u["x"], u["y"]) for u in (w.get("colony") or {}).get("unit_list") or []
                 if isinstance(u, dict) and isinstance(u.get("x"), int)}
        movers = [p for i, p in units.items() if i in self.prev_units
                  and math.dist(p, self.prev_units[i]) >= MOVE_MIN and near(*p)]
        self.prev_units = units
        if movers:
            cells = {}
            for p in movers:
                cells.setdefault((int(p[0] // CELL), int(p[1] // CELL)), []).append(p)
            group = max(cells.values(), key=len)
            if len(group) >= 2:
                return self._mean(group), "movers"
        # 4. a slow circle around the last explicit target
        if self.anchor:
            return self._orbit(), "orbit"
        return None, ""

    def _orbit(self):
        a = 2 * math.pi * (time.time() % ORBIT_PERIOD) / ORBIT_PERIOD
        return (self.anchor[0] + ORBIT_RADIUS * math.cos(a), self.anchor[1] + ORBIT_RADIUS * math.sin(a))

    @staticmethod
    def _mean(pts):
        return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))

    # -- motion ----------------------------------------------------------------
    def _press(self, token) -> bool:
        """(Re)start a hold at the screen centre: button up, pointer to centre, middle button down."""
        if self.ptr is not None:
            camera._rpc("ui_mouse_button", {"token": token, "action": "up", "button": "middle", "space": "logical",
                                            "x": round(self.ptr[0]), "y": round(self.ptr[1])})
        camera._rpc("ui_move", {"token": token, "space": "logical", "x": CENTRE[0], "y": CENTRE[1]})
        out = camera._rpc("ui_mouse_button", {"token": token, "action": "down", "button": "middle", "space": "logical",
                                             "x": CENTRE[0], "y": CENTRE[1]})
        if (out.get("result") or {}).get("isError"):
            self.ptr = None
            return False
        self.ptr = [float(CENTRE[0]), float(CENTRE[1])]
        self.held_at = time.time()
        return True

    def _lift(self, token=None) -> None:
        token = token or camera.read_token()
        if self.ptr is not None and token:
            try:
                camera._rpc("ui_mouse_button", {"token": token, "action": "up", "button": "middle", "space": "logical",
                                                "x": round(self.ptr[0]), "y": round(self.ptr[1])})
            except Exception:  # noqa: BLE001
                pass
        self.ptr = None

    def step(self) -> None:
        if not self.view or not self.target:
            return
        token = camera.read_token()
        if not token:
            return
        cx, cy = self.centre()
        dx = self._wrap(self.target[0] - cx, self.map[0])
        dy = self._wrap(self.target[1] - cy, self.map[1])
        dist = math.hypot(dx, dy)
        if dist < DEADZONE:
            self._lift(token)       # arrived: let go, the picture rests until the next target
            return
        # ease: full speed far away, slower within 6 tiles
        px = self.px_per_s * self.step_s * min(1.0, 0.35 + dist / 6.0)
        ux, uy = dx / dist, dy / dist
        # holds expire after 5 s, and the pointer must stay over the map: re-anchor at the centre
        if (self.ptr is None or time.time() - self.held_at > 3.5
                or abs(self.ptr[0] - CENTRE[0]) > 200 or abs(self.ptr[1] - CENTRE[1]) > 150):
            if not self._press(token):
                return
        # a middle-button drag moves the view with the mouse: move the pointer the way to travel
        self.ptr = [self.ptr[0] + ux * px, self.ptr[1] + uy * px]
        out = camera._rpc("ui_move", {"token": token, "space": "logical",
                                     "x": round(self.ptr[0], 1), "y": round(self.ptr[1], 1)})
        if (out.get("result") or {}).get("isError"):
            self.ptr = None
            return
        moved = px / self.tile_px
        self.view = dict(self.view, x=self.view["x"] + ux * moved, y=self.view["y"] + uy * moved)

    def release(self) -> None:
        self._lift()
        token = camera.read_token()
        if token:
            try:
                camera._rpc("ui_release_inputs", {"token": token})
            except Exception:  # noqa: BLE001
                pass

    def paused(self) -> bool:
        last = camera.last_move()
        return time.time() - float(last.get("at", 0)) < self.pause_s

    def run(self) -> None:
        was_paused = True
        while not self.stop.is_set():
            try:
                if self.paused() or not camera.read_token():
                    if not was_paused:
                        self.release()
                    was_paused = True
                    self.stop.wait(0.5)
                    continue
                if was_paused or time.time() - self.last_poll >= self.poll_s:
                    self.poll()
                    self.last_poll = time.time()
                was_paused = False
                if self.reason in ("orbit", "hold") and self.anchor:
                    self.target = self._orbit()
                self.step()
            except Exception:  # noqa: BLE001 - the drift must never take the chat agent down
                self.view = None
                self.stop.wait(2)
            self.stop.wait(self.step_s)
        self.release()


def start() -> Drift:
    d = Drift()
    threading.Thread(target=d.run, daemon=True, name="camera-drift").start()
    return d
