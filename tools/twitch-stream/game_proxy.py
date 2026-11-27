#!/usr/bin/env python3
"""The player agent's connection to the stream game: a stdio MCP proxy that owns game control.

A stdio MCP server (newline-delimited JSON-RPC) named `glob2-stream` that forwards the game's
own tools (game_*, ui_*, hive_*) to http://127.0.0.1:$MCP_PORT/mcp, with one difference that
matters: the control token never reaches the model.

Why: the player used to take control itself and carry the token in its context. A compaction,
resume or recovery session lost it, the lease stayed held under the lost token, and the colony
ran on autopilot while the player told viewers it was locked out (2026-11-24). Now this proxy:

  - takes control itself (adopting the token in STATE_DIR/control-token if it still renews,
    otherwise acquiring; it retries while another holder's lease is active);
  - removes `token` from every tool schema it lists and from every call it receives, and adds
    its own token to the calls whose game schema takes one;
  - renews the lease in the background well before it expires, and on a "token does not match"
    or "not controlled" reply takes control again once and retries the call once;
  - hides ui_acquire_control, ui_renew_control and ui_release_control, and also game_view,
    game_wait and game_chat (the player moves the camera, waits and narrates through stream-ctl);
  - publishes the token to STATE_DIR/control-token (0644 inside the 2770 operator:agent state
    dir) for stream-ctl, the camera gate and the supervisor, and releases control and removes the
    file when it exits;
  - never writes the token to stdout, logs or error text (it is replaced with "<token>").
"""
import json

import pacing  # noqa: E402  shared call pacing (same directory)
import os
import pathlib
import signal
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request

PROTOCOL = "2025-11-25"
HIDDEN = {"ui_acquire_control", "ui_renew_control", "ui_release_control",   # control is managed here
          "game_view", "game_wait", "game_chat",                               # stream-ctl owns these
          # Never used in 84 matches (analysis rec. 11): their schemas cost ~2-3k tokens on every call.
          # game_alliance is forbidden anyway (1v1); the camera drift drives the pointer itself.
          "game_alliance", "ui_drag", "ui_move", "ui_mouse_button", "ui_type_text", "ui_release_inputs"}
LEASE_ERRORS = ("does not match", "not controlled", "no control", "controls the game", "control lease",
                "lease lost", "holds control", "acquire_control", "stale token")
ACQUIRE_TRIES = int(os.environ.get("GAME_PROXY_ACQUIRE_TRIES", "40"))         # x5 s while another lease holds


def game_url() -> str:
    return f"http://127.0.0.1:{int(os.environ.get('MCP_PORT', '27300'))}/mcp"


def token_file() -> pathlib.Path:
    return pathlib.Path(os.environ.get("STATE_DIR", "/var/lib/glob2-stream/state")) / "control-token"


def rpc(method: str, params: dict, name: str = None, timeout: float = 60) -> dict:
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream",
               "MCP-Protocol-Version": PROTOCOL, "Mcp-Method": method}
    if name:
        headers["Mcp-Name"] = name
    with urllib.request.urlopen(urllib.request.Request(game_url(), body, headers), timeout=timeout) as resp:
        return json.load(resp)


def call_text(name: str, args: dict, timeout: float = 60) -> str:
    """tools/call and return the first text content ('' if none)."""
    out = rpc("tools/call", {"name": name, "arguments": args}, name, timeout)
    if "error" in out:
        return json.dumps({"error": out["error"].get("message", "error")})
    content = out.get("result", {}).get("content") or [{}]
    return content[0].get("text", "")


def parse(text: str) -> dict:
    try:
        value = json.loads(text)
        return value if isinstance(value, dict) else {}
    except ValueError:
        return {}


class Lease:
    """The control lease this proxy holds on the player's behalf."""

    def __init__(self):
        self.token = None
        self.seconds = 300.0
        self.lock = threading.RLock()
        self.stop = threading.Event()

    def _publish(self):
        path = token_file()
        try:
            if self.token:
                fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".control-token.")
                with os.fdopen(fd, "w") as fh:
                    fh.write(self.token + "\n")
                os.chmod(tmp, 0o644)
                os.replace(tmp, path)
            elif path.exists():
                path.unlink()
        except OSError:
            pass

    def _try_renew(self, token: str) -> bool:
        reply = parse(call_text("ui_renew_control", {"token": token}))
        if "error" in reply or not reply.get("controlled", True):
            return False
        self.seconds = float(reply.get("lease_seconds") or self.seconds)
        return True

    def ensure(self) -> bool:
        """Hold control: keep the current token, adopt the published one, or acquire."""
        with self.lock:
            if self.token and self._try_renew(self.token):
                return True
            self.token = None
            try:
                published = token_file().read_text().strip()
            except OSError:
                published = ""
            if published and self._try_renew(published):
                self.token = published
                return True
            for attempt in range(ACQUIRE_TRIES):
                reply = parse(call_text("ui_acquire_control", {}))
                if reply.get("token"):
                    self.token = reply["token"]
                    self.seconds = float(reply.get("lease_seconds") or 300)
                    self._publish()
                    return True
                if self.stop.is_set() or attempt == ACQUIRE_TRIES - 1:
                    break
                self.stop.wait(5)          # another holder's lease: it lapses within its lease time
            self._publish()
            return False

    def renew_loop(self):
        while not self.stop.wait(max(20.0, self.seconds / 3)):
            try:
                with self.lock:
                    if self.token and not self._try_renew(self.token):
                        self.ensure()
            except (urllib.error.URLError, OSError, ValueError):
                pass

    def release(self):
        self.stop.set()
        with self.lock:
            token, self.token = self.token, None
            if token:
                try:
                    call_text("ui_release_control", {"token": token}, timeout=10)
                except (urllib.error.URLError, OSError, ValueError):
                    pass
            try:
                if token and token_file().read_text().strip() == token:
                    token_file().unlink()
            except OSError:
                pass


class Proxy:
    def __init__(self, lease: Lease):
        self.lease = lease
        self.takes_token = set()        # tools whose game schema has a token parameter

    def redact(self, text: str) -> str:
        token = self.lease.token
        return text.replace(token, "<token>") if token and isinstance(text, str) else text

    def tools(self) -> list:
        listed = []
        for t in rpc("tools/list", {})["result"]["tools"]:
            schema = json.loads(json.dumps(t.get("inputSchema") or {"type": "object"}))
            props = schema.get("properties", {})
            if "token" in props:
                self.takes_token.add(t["name"])
                del props["token"]
            if "required" in schema:
                schema["required"] = [r for r in schema["required"] if r != "token"]
            if t["name"] in HIDDEN:
                continue
            desc = t.get("description", "").replace("Needs token.", "").replace("No token.", "")
            listed.append({"name": t["name"], "description": desc.strip() + " (Game control is handled for you.)"
                           if t["name"] in self.takes_token else desc.strip(), "inputSchema": schema})
        return listed

    @staticmethod
    def lease_lost(out: dict) -> bool:
        """The game refused the call because this proxy's lease is gone (expired or taken)."""
        if "error" in out:
            message = str(out["error"].get("message", ""))
        else:
            content = out.get("result", {}).get("content") or [{}]
            reply = parse(content[0].get("text", ""))
            if reply.get("error") and reply.get("controlled") is False:
                return True             # an error while nobody holds control: our lease is gone
            message = str(reply.get("error", ""))
        return any(e in message.lower() for e in LEASE_ERRORS)

    def call(self, name, args) -> dict:
        if name in HIDDEN:
            return {"content": [{"type": "text", "text": f"{name} isn't available here: game control is "
                                 "handled for you, and the camera, waiting and chat go through stream-ctl"}],
                    "isError": True}
        if not self.takes_token:
            self.tools()                 # learn which tools take a token
        args = {k: v for k, v in (args if isinstance(args, dict) else {}).items() if k != "token"}
        if not name.startswith("ui_"):   # menus and setup stay quick; game calls are paced
            pacing.wait_turn()
        for attempt in (1, 2):
            if name in self.takes_token:
                if not self.lease.token and not self.lease.ensure():
                    return {"content": [{"type": "text", "text": "the game is controlled by someone else right "
                                         "now; keep narrating and try again shortly"}], "isError": True}
                args["token"] = self.lease.token
            out = rpc("tools/call", {"name": name, "arguments": args}, name)
            if name in self.takes_token and attempt == 1 and self.lease_lost(out):
                self.lease.token = None
                self.lease.ensure()
                continue
            break
        if "error" in out:
            return {"content": [{"type": "text", "text": self.redact(str(out["error"].get("message", "error")))}],
                    "isError": True}
        result = out.get("result", {})
        for item in result.get("content") or []:
            if item.get("type") == "text":
                item["text"] = self.redact(item["text"])
        return result

    def handle(self, req: dict):
        method, rid, params = req.get("method"), req.get("id"), req.get("params") or {}
        if rid is None:
            return None
        try:
            if method == "initialize":
                result = {"protocolVersion": params.get("protocolVersion", PROTOCOL),
                          "capabilities": {"tools": {"listChanged": False}},
                          "serverInfo": {"name": "glob2-stream", "version": "1"},
                          "instructions": "The Globulation 2 match being streamed. Game control is handled for "
                                          "you: call tools without any token."}
            elif method == "ping":
                result = {}
            elif method == "tools/list":
                result = {"tools": self.tools()}
            elif method == "tools/call":
                result = self.call(params.get("name"), params.get("arguments"))
            else:
                return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": f"not available: {method}"}}
        except (urllib.error.URLError, OSError, ValueError, KeyError) as e:
            result = {"content": [{"type": "text", "text": f"game unavailable: {type(e).__name__}"}], "isError": True}
        return {"jsonrpc": "2.0", "id": rid, "result": result}


def main():
    lease = Lease()
    signal.signal(signal.SIGTERM, lambda *_: (lease.release(), sys.exit(0)))
    if os.environ.get("GAME_PROXY_NO_CONTROL") == "1":     # list-only (verify-sandbox): never touch the lease
        lease.ensure = lambda: False
        lease.release = lambda: None
    def take_control():               # in the background: MCP startup must answer at once
        try:
            lease.ensure()
        except (urllib.error.URLError, OSError, ValueError):
            pass                        # the game may still be starting; calls retry
        lease.renew_loop()
    threading.Thread(target=take_control, daemon=True).start()
    proxy = Proxy(lease)
    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                req = json.loads(line)
            except ValueError:
                continue
            for r in (req if isinstance(req, list) else [req]):
                resp = proxy.handle(r)
                if resp is not None:
                    sys.stdout.write(json.dumps(resp) + "\n")
                    sys.stdout.flush()
    finally:
        lease.release()


if __name__ == "__main__":
    main()
