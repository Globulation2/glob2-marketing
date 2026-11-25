#!/usr/bin/env python3
"""Make each match easy to find and share on Twitch: per-game titles, stream markers and clips.

It runs as its own user service (glob2-stream-highlights, installed by autostart/install-autostart.sh
when the stream autostarts live), separate from the supervisor so it can be updated or restarted
without ending the broadcast. Every POLL seconds it reads the match state and, on match events:

  - match starts   -> sets the stream title ("Claude vs Cortex · Game 12 · Canals map") and adds
                      a stream marker, so the past broadcast can be cut into a Highlight per game;
  - momentum swing -> clips the last 60 s when the win chance moves HIGHLIGHT_SWING points within
                      three minutes (a battle won or lost), at most one clip per HIGHLIGHT_COOLDOWN;
  - match ends     -> adds a marker and clips the finish ("Claude beats Maxima · Game 12").

Clips are what Twitch shows on the channel page, in search and in shares, and they outlive
past broadcasts, which Twitch deletes after a few days. Every call runs on the supervisor's
side with the channel's token; agents never see it. Missing scopes, an offline stream or any
API error are logged once and skipped: highlights must never disturb the show.

  highlights.py run               poll forever (what the service runs)
  highlights.py status            show the token's scopes and what is enabled
  highlights.py marker TEXT       add a marker now (manual test)
  highlights.py clip TITLE        clip the last 60 s now (manual test)

Scopes: titles and markers need channel:manage:broadcast; clips need clips:edit. To add
clips:edit, log in again with the Twitch CLI (see README.md, "Clips and highlights").
"""
import collections
import json
import logging
import pathlib
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "chat"))
import rigconfig  # noqa: E402
import rigstate  # noqa: E402
import token_refresh  # noqa: E402

HELIX = "https://api.twitch.tv/helix"
POLL = 30   # seconds
log = logging.getLogger("highlights")

VERDICT = {"win": "Claude beats {opp}", "loss": "{opp} beats Claude", "draw": "Claude and {opp} draw"}


class TwitchAPI:
    def __init__(self, cfg: dict):
        self.refresher = token_refresh.from_config(cfg)
        self.client_id = token_refresh.read_env(self.refresher.cli_env).get("CLIENTID", "")
        self.info = {}

    def _token(self) -> str:
        self.info, _ = self.refresher.ensure()
        return self.refresher.current()

    def has(self, scope: str) -> bool:
        try:
            self._token()
        except Exception:  # noqa: BLE001
            return False
        return scope in self.info.get("scopes", [])

    def call(self, method: str, path: str, query: dict = None, body: dict = None):
        token = self._token()
        url = f"{HELIX}/{path}" + (f"?{urllib.parse.urlencode(query)}" if query else "")
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(url, data, method=method, headers={
            "Authorization": f"Bearer {token}", "Client-Id": self.client_id,
            **({"Content-Type": "application/json"} if data else {})})
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read()
        return json.loads(raw) if raw else {}

    @property
    def broadcaster(self) -> str:
        if not self.info:
            self._token()
        return self.info.get("user_id", "")

    def set_title(self, title: str):
        self.call("PATCH", "channels", {"broadcaster_id": self.broadcaster}, {"title": title[:140]})

    def marker(self, text: str) -> dict:
        out = self.call("POST", "streams/markers", body={"user_id": self.broadcaster, "description": text[:140]})
        return (out.get("data") or [{}])[0]

    def clip(self, title: str, duration: float = 60) -> dict:
        out = self.call("POST", "clips", {"broadcaster_id": self.broadcaster, "title": title[:100],
                                          "duration": duration})
        return (out.get("data") or [{}])[0]


class Highlights:
    SWING_WINDOW = 180   # seconds

    def __init__(self, cfg: dict, read_win_chance):
        self.cfg = cfg
        self.read_win_chance = read_win_chance
        self.enabled = str(cfg.get("HIGHLIGHTS", "1")) == "1"
        self.swing = int(cfg.get("HIGHLIGHT_SWING") or 25)
        self.cooldown = int(cfg.get("HIGHLIGHT_COOLDOWN") or 600)
        self.api = TwitchAPI(cfg)
        self.state_file = pathlib.Path(cfg["LOG_DIR"]) / "highlights-state.json"
        self.log_file = pathlib.Path(cfg["LOG_DIR"]) / "highlights.jsonl"   # clip edit links stay operator-side
        self.state = rigstate.read_json(self.state_file, {}) or {}
        self.wins = collections.deque()
        self.last_clip = 0.0
        self.warned = set()

    # --- bookkeeping --------------------------------------------------------------------------
    def _save(self):
        self.state_file.write_text(json.dumps(self.state))

    def _record(self, kind: str, **fields):
        with self.log_file.open("a") as fh:
            fh.write(json.dumps({"date": rigstate.now(), "kind": kind, **fields}) + "\n")

    def _warn_once(self, key: str, msg: str):
        if key not in self.warned:
            self.warned.add(key)
            log.warning(msg)

    def _try(self, what: str, fn, *args):
        try:
            return fn(*args)
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:200]
            self._warn_once(f"{what}{e.code}", f"{what} failed: HTTP {e.code} {detail}")
        except Exception as e:  # noqa: BLE001 - highlights never disturb the show
            self._warn_once(f"{what}{type(e).__name__}", f"{what} failed: {e}")
        return None

    def _clip(self, title: str, match: int, why: str):
        if not self.api.has("clips:edit"):
            self._warn_once("noclips", "clips need the clips:edit scope; see README.md, Clips and highlights")
            return
        got = self._try("clip", self.api.clip, title)
        if got:
            self.last_clip = time.time()
            log.info("clip %s: %s (%s)", got.get("id"), title, why)
            self._record("clip", match=match, title=title, why=why, id=got.get("id"), edit_url=got.get("edit_url"))

    # --- events -------------------------------------------------------------------------------
    def poll(self):
        if not self.enabled:
            return
        cur = rigstate.current(self.cfg)
        match, phase = cur.get("number"), cur.get("phase")
        if not match:
            return
        if self.state.get("match") != match:
            self.state = {"match": match}
            self.wins.clear()
        opp = cur.get("opponent", "?")
        if phase == "playing" and not self.state.get("started"):
            self.on_start(cur, opp)
        elif phase == "playing" and not cur.get("fast_forward"):
            self.watch_swing(cur, opp)
        if phase == "intermission" and self.state.get("started") and not self.state.get("ended"):
            self.on_end(cur, opp)

    def on_start(self, cur, opp):
        games = rigstate.games(self.cfg)
        number = rigstate.decided(games) + 1
        mapname = cur.get("generator") or "random"
        self.state.update(started=True, game=number)
        self._save()
        title = f"Claude Plays Glob · Claude vs {opp} · Game {number} on {mapname} · overall {rigstate.record(games)}"
        if self.api.has("channel:manage:broadcast"):
            self._try("title", self.api.set_title, title)
            got = self._try("marker", self.api.marker, f"Game {number} start: Claude vs {opp} on {mapname}")
            self._record("start", match=cur["number"], game=number, title=title,
                         position=(got or {}).get("position_seconds"))
        log.info("highlights: game %d (match %d) started", number, cur["number"])

    def watch_swing(self, cur, opp):
        try:
            win = int(self.read_win_chance())
        except Exception:  # noqa: BLE001 - no reading, no decision
            return
        now = time.time()
        self.wins.append((now, win))
        while self.wins and now - self.wins[0][0] > self.SWING_WINDOW:
            self.wins.popleft()
        lo = min(w for _, w in self.wins)
        hi = max(w for _, w in self.wins)
        if hi - lo < self.swing or now - self.last_clip < self.cooldown:
            return
        rising = win == hi
        if not rising and win != lo:
            return   # the swing has to end at the latest reading, or it's old news
        number = self.state.get("game", "?")
        what = f"the tide turns for Claude ({lo}% to {hi}%)" if rising else f"disaster strikes ({hi}% to {lo}%)"
        self._clip(f"Claude vs {opp} · Game {number}: {what}", cur["number"], f"win chance swing {lo}-{hi}")
        self.wins.clear()

    def on_end(self, cur, opp):
        self.state["ended"] = True
        self._save()
        result = cur.get("result")
        number = self.state.get("game", "?")
        if result not in VERDICT:
            return   # aborted: nothing worth a clip
        verdict = VERDICT[result].format(opp=opp)
        if self.api.has("channel:manage:broadcast"):
            got = self._try("marker", self.api.marker, f"Game {number} end: {verdict}")
            self._record("end", match=cur["number"], game=number, result=result,
                         position=(got or {}).get("position_seconds"))
        self._clip(f"{verdict} · Game {number} on {cur.get('generator') or 'a random map'}", cur["number"], "match end")


def win_chance_reader(cfg: dict):
    """Read the player's win chance from the game's MCP server (observation only, no control lease)."""
    def read() -> int:
        body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {
            "name": "game_world", "arguments": {"detail": "brief", "include": ["status"]}}}).encode()
        req = urllib.request.Request(f"http://127.0.0.1:{cfg['MCP_PORT']}/mcp", body, {
            "Content-Type": "application/json", "Accept": "application/json, text/event-stream",
            "MCP-Protocol-Version": "2025-11-25", "Mcp-Method": "tools/call", "Mcp-Name": "game_world"})
        out = json.load(urllib.request.urlopen(req, timeout=5))
        st = json.loads(out["result"]["content"][0]["text"])
        return int((st.get("status") or {}).get("win_chance"))
    return read


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    cfg = rigconfig.load()
    api = TwitchAPI(cfg)
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "run":
        hl = Highlights(cfg, win_chance_reader(cfg))
        log.info("highlights running (enabled=%s, swing %d points, cooldown %d s)", hl.enabled, hl.swing, hl.cooldown)
        while True:
            try:
                hl.poll()
            except Exception:  # noqa: BLE001 - keep polling
                log.exception("poll failed")
            time.sleep(POLL)
    elif cmd == "status":
        api.has("x")
        print(token_refresh.describe(api.info))
        print("titles/markers:", "yes" if "channel:manage:broadcast" in api.info.get("scopes", []) else "NO")
        print("clips:", "yes" if "clips:edit" in api.info.get("scopes", []) else "NO (needs clips:edit)")
        print("enabled:", str(cfg.get("HIGHLIGHTS", "1")) == "1")
    elif cmd == "marker":
        print(api.marker(" ".join(sys.argv[2:]) or "manual marker"))
    elif cmd == "clip":
        print(api.clip(" ".join(sys.argv[2:]) or "Claude Plays Glob"))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
