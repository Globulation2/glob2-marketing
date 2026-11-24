"""The stream camera gate: the one path by which anything moves the stream camera.

Used by the player (stream_ctl.py's camera_show, run as the agent user), the chat host
(readonly_mcp.py's camera_show, run as the agent user) and the optional idle director
(director.py, off by default). It enforces, for every source: zoom 0..1 only (never past 100%,
and a framed area is widened to at least the 100% view), clean short labels, a minimum interval
between moves, and the viewer-request hold: when the chat host shows something a viewer asked
for, STATE_DIR/camera-hold.json holds the camera for CAMERA_HOLD_SECONDS, during which the
player's moves are refused (it keeps playing) while the chat host may still move it.

The player holds the game's single control lease. The supervisor publishes the player's current
control token to STATE_DIR/control-token (mode 0640, agent group) and deletes it when the session
ends, so camera moves ride on that lease. Only game_view is ever called with it. The token never
leaves this module: results and errors are rewritten without it.

Shared state, all in shared directories so either side can replace the files:
  STATE_DIR/camera.json      last move: time, source, tile, zoom, label and when the label expires
  STATE_DIR/camera-hold.json the viewer-request hold: until, label, by
  CAMERA_OVERLAY_FILE        the on-stream label ("Showing: ..."), empty when none
"""
import json
import math
import os
import pathlib
import re
import tempfile
import time
import urllib.error
import urllib.request

PROTOCOL = "2025-11-25"
LABEL_MAX = 60
# Labels go on screen: letters, digits, spaces and plain punctuation only; no links or mass mentions.
LABEL_DROP = re.compile(r"[^\w @'’,.!?:;()#&+\-/]", re.UNICODE)
URLISH = re.compile(r"(https?://|www\.|\b[\w-]+\.(?:com|net|org|io|gg|tv|ly|me|co|xyz|ru|cn)\b)", re.I)


def env(name: str, default: str) -> str:
    return os.environ.get(name) or default


def state_dir() -> pathlib.Path:
    return pathlib.Path(env("STATE_DIR", str(pathlib.Path.home() / "glob2-stream" / "state")))


def overlay_file() -> pathlib.Path:
    default = pathlib.Path(env("OVERLAY_FILE", str(state_dir().parent / "overlay" / "caption.txt"))).with_name("camera.txt")
    return pathlib.Path(env("CAMERA_OVERLAY_FILE", str(default)))


def min_interval() -> float:
    return float(env("CAMERA_MIN_INTERVAL", "8"))


def label_seconds() -> float:
    return float(env("CAMERA_LABEL_SECONDS", "12"))


def hold_seconds() -> float:
    return float(env("CAMERA_HOLD_SECONDS", "40"))


def hold_remaining() -> float:
    try:
        until = float(json.loads((state_dir() / "camera-hold.json").read_text()).get("until", 0))
    except (OSError, ValueError, TypeError):
        return 0.0
    return max(0.0, until - time.time())


def write_atomic(path: pathlib.Path, text: str, mode: int = 0o664) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=path.name + ".")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(text)
    os.chmod(tmp, mode)
    os.replace(tmp, path)


def read_token() -> str:
    try:
        tok = (state_dir() / "control-token").read_text().strip()
    except OSError:
        return ""
    return tok if re.fullmatch(r"[A-Za-z0-9+/]{20,}={0,2}", tok) else ""


def last_move() -> dict:
    try:
        return json.loads((state_dir() / "camera.json").read_text())
    except (OSError, ValueError):
        return {}


def seconds_since_move() -> float:
    return time.time() - float(last_move().get("at", 0))


# Tile coordinates and building ids mean nothing to viewers ("(48,45)", "at 138,147", "#16").
COORDS = re.compile(r"\(?\s*\b\d{1,3}\s*(?:[-–]\s*\d{1,3}\s*)?,\s*\d{1,3}(?:\s*[-–]\s*\d{1,3})?\b\s*\)?|#\d+")


def strip_coords(text: str) -> str:
    # Drop a preposition that only introduced the coordinates ("the tower at (48,45) now").
    text = re.sub(r"\s*\b(?:at|near|by|around|to)\s+(?=\(?\s*\d{1,3}\s*(?:[-–]\s*\d{1,3}\s*)?,\s*\d)", " ", text)
    text = COORDS.sub("", text)
    text = re.sub(r"\s+(?:at|near|by|around)\s*(?=[,.;:)]|$)", "", text)
    text = re.sub(r"\(\s*(?:at|near|by|around)?\s*\)?\s*$", "", text)     # a bracket left empty or open
    text = re.sub(r"\(\s*(?:at|near|by|around)?\s*\)", "", text)
    text = re.sub(r"\s+([.,;:!?])", r"\1", " ".join(text.split()))
    return text.strip(" ,;:-(")


def clean_label(label) -> str:
    if not isinstance(label, str):
        return ""
    text = " ".join(LABEL_DROP.sub("", strip_coords(label)).split())
    if URLISH.search(text) or "@everyone" in text.lower() or "@here" in text.lower():
        return ""
    return text[:LABEL_MAX].strip()


def set_label(text: str) -> None:
    write_atomic(overlay_file(), f"Showing: {text}" if text else "")


def clear_expired_label() -> None:
    """Called by the chat agent's loop: blank the label once its time is up."""
    mv = last_move()
    if mv.get("label") and time.time() >= float(mv.get("label_until", 0)):
        try:
            if overlay_file().read_text().strip():
                set_label("")
        except OSError:
            pass


def _rpc(name: str, arguments: dict, timeout: float = 15) -> dict:
    port = int(env("MCP_PORT", "27300"))
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                       "params": {"name": name, "arguments": arguments}}).encode()
    req = urllib.request.Request(f"http://127.0.0.1:{port}/mcp", body, {
        "Content-Type": "application/json", "Accept": "application/json, text/event-stream",
        "MCP-Protocol-Version": PROTOCOL, "Mcp-Method": "tools/call", "Mcp-Name": name})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.load(resp)


def show(x=None, y=None, zoom=None, width=None, height=None, label="", source="chat", by="") -> tuple:
    """Move the stream camera. source is "player", "chat" or "director"; by is the viewer a chat
    move answers. Returns (ok, message); the message never contains the token."""
    if source not in ("player", "chat", "director"):
        return False, "unknown camera source"
    try:
        if zoom is not None:
            zoom = float(zoom)
            if not math.isfinite(zoom):
                return False, "zoom must be a number between 0 and 1"
            if zoom > 1:
                return False, "zoom above 1 (100%) isn't allowed on stream: use 1 or lower (0 fits the whole map)"
            if zoom < 0:
                return False, "zoom must be between 0 and 1"
        args = {}
        for k, v in (("x", x), ("y", y), ("width", width), ("height", height)):
            if v is not None:
                v = int(v)
                if v < (1 if k in ("width", "height") else 0) or v > (256 if k in ("width", "height") else 4096):
                    return False, f"{k} out of range"
                args[k] = v
    except (TypeError, ValueError):
        return False, "x, y, width and height must be whole tile numbers and zoom a number"
    if zoom is None and "width" not in args and "height" not in args:
        zoom = 1.0                      # no zoom given: 100%, rather than whatever the last shot used
    if zoom is not None:
        args["zoom"] = zoom
    if "width" in args or "height" in args:
        # A frame smaller than the 100% view would zoom in past 100%: widen it to at least that view,
        # keeping its centre (about 54x34 tiles at 1080p beside the game's sidebar).
        mw, mh = (int(v) for v in env("CAMERA_MIN_FRAME", "56x36").split("x"))
        args["width"] = min(256, max(args.get("width", mw), mw))
        args["height"] = min(256, max(args.get("height", mh), mh))
        args.pop("zoom", None)          # the frame decides the zoom
    held = hold_remaining()
    if held > 0 and source != "chat":
        return False, (f"the camera is showing a viewer request for {held:.0f} more s; keep playing and "
                       "narrate instead")
    # Viewer requests win: a chat move is limited only by the previous chat move (and a 2 s floor),
    # so the player's frequent moves can't lock viewers out (seen at the 15:40 check-in).
    last = last_move()
    since = time.time() - float(last.get("at", 0))
    limit = min_interval() if (source != "chat" or last.get("source") == "chat") else 2.0
    wait = limit - since
    if wait > 0:
        return False, f"the camera moved {since:.0f} s ago; wait {wait:.0f} s before moving it again"
    token = read_token()
    if not token:
        return False, "camera unavailable right now (no match is being played)"
    try:
        out = _rpc("game_view", dict(args, token=token))
    except (urllib.error.URLError, OSError, ValueError) as e:
        return False, f"camera unavailable right now ({type(e).__name__})"
    err = (out.get("error") or {}).get("message") or ""
    res = out.get("result") or {}
    if not err and res.get("isError"):
        err = " ".join(c.get("text", "") for c in res.get("content", []))
    if err:
        err = err.replace(token, "<token>")
        if re.search(r"token|lease|control", err, re.I):
            return False, "camera unavailable right now (the player's control is changing hands)"
        return False, "camera move refused: " + err[:200]
    label = clean_label(label)
    viewer = clean_label(by).lstrip("@")[:25] if by else ""
    if label and viewer and f"@{viewer}".lower() not in label.lower():
        label = f"{label} · asked by @{viewer}"[:LABEL_MAX + 30]
    t = time.time()
    until = t + (hold_seconds() if source == "chat" else label_seconds())
    write_atomic(state_dir() / "camera.json", json.dumps({
        "at": t, "source": source, "x": args.get("x"), "y": args.get("y"), "zoom": args.get("zoom"),
        "width": args.get("width"), "height": args.get("height"),
        "label": label, "label_until": until if label else 0}))
    if source == "chat":
        write_atomic(state_dir() / "camera-hold.json", json.dumps({"until": until, "label": label, "by": viewer}))
    set_label(label)
    where = f"tile ({args['x']}, {args['y']})" if "x" in args else "the colony"
    return True, f"camera now on {where}" + (f" at zoom {args['zoom']:g}" if "zoom" in args else "") + \
        (f", labelled “{label}”" if label else "")
