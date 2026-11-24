#!/usr/bin/env python3
"""Read-only MCP proxy to the stream game, for the Twitch chat host.

A stdio MCP server (newline-delimited JSON-RPC) that forwards a small allowlist of
read tools to the game's loopback HTTP endpoint (http://127.0.0.1:$MCP_PORT/mcp).
Nothing that sends input, takes control or changes the match can pass through:
tools outside the allowlist are hidden from tools/list and rejected on call, the
`token` argument and any argument outside each tool's allowlist are removed, and
screenshots are clamped small. Each proxy process (one per chat reply) also caps
the number of game calls (READONLY_MCP_MAX_CALLS, default 4) so the chat host
never competes with the player for the game's attention.

One exception to read-only: `camera_show` moves the stream camera through the shared
camera gate (camera.py: game_view on the player's lease). It never zooms in past 100%, is
rate limited across processes, holds the camera for the viewer briefly, counts toward
the call cap and never sees or returns the control token.
"""
import json
import os
import sys
import urllib.error
import urllib.request

import camera

PROTOCOL = "2025-11-25"
SHOT_MAX_W, SHOT_MAX_H = 960, 540

# tool -> allowed argument names (token is never allowed)
ALLOW = {
    "ui_status": set(),
    "ui_screenshot": {"max_width", "max_height"},
    "ui_inspect": {"compact", "subtree", "surface", "screenshot", "max_width", "max_height"},
    "game_world": {"area", "detail", "limit", "resource_radius"},
    "game_stats": {"list", "metrics", "points", "split"},
    "game_guide": {"topic"},
    "hive_status": set(),
    "hive_api": set(),
}


def game_url() -> str:
    return f"http://127.0.0.1:{int(os.environ.get('MCP_PORT', '27300'))}/mcp"


def game_rpc(method: str, params: dict, name: str = None) -> dict:
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream",
               "MCP-Protocol-Version": PROTOCOL, "Mcp-Method": method}
    if name:
        headers["Mcp-Name"] = name
    req = urllib.request.Request(game_url(), body, headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def sanitize(name: str, args) -> dict:
    """Keep only allowlisted arguments and clamp image sizes."""
    args = args if isinstance(args, dict) else {}
    clean = {k: v for k, v in args.items() if k in ALLOW[name]}
    if name == "ui_screenshot" or (name == "ui_inspect" and clean.get("screenshot")):
        clean["max_width"] = min(int(clean.get("max_width") or SHOT_MAX_W), SHOT_MAX_W)
        clean["max_height"] = min(int(clean.get("max_height") or SHOT_MAX_H), SHOT_MAX_H)
    return clean


CAMERA_TOOL = {
    "name": "camera_show",
    "description": ("Move the stream camera so viewers see something: centre on tile x/y, or frame a tile "
                    "rectangle with width/height, or leave x/y out to centre on Claude's colony. zoom 1 is 100% "
                    "(closest allowed, and the default), 0.7 and 0.5 zoom out, 0 fits the whole map; never above 1. label is a short "
                    "on-screen caption (max 60 chars) naming what's shown, e.g. \"Claude's main base\"; asked_by is the "
                    "viewer who asked (shown as \"asked by @name\"). The shot holds the camera for about 40 s so the "
                    "player doesn't move away. Fog of war still applies: hidden areas stay dark. One move per reply; "
                    "moves are rate limited."),
    "inputSchema": {"type": "object", "properties": {
        "x": {"type": "integer", "minimum": 0}, "y": {"type": "integer", "minimum": 0},
        "width": {"type": "integer", "minimum": 1, "maximum": 256},
        "height": {"type": "integer", "minimum": 1, "maximum": 256},
        "zoom": {"type": "number", "minimum": 0, "maximum": 1},
        "label": {"type": "string", "maxLength": 60},
        "asked_by": {"type": "string", "maxLength": 25, "description": "the viewer's name, without @"}}},
}
CAMERA_ARGS = {"x", "y", "width", "height", "zoom", "label", "asked_by"}


def filtered_tools() -> list:
    tools = [CAMERA_TOOL]
    for t in game_rpc("tools/list", {})["result"]["tools"]:
        if t["name"] not in ALLOW:
            continue
        schema = json.loads(json.dumps(t.get("inputSchema") or {"type": "object"}))
        props = schema.get("properties", {})
        for k in list(props):
            if k not in ALLOW[t["name"]]:
                del props[k]
        if "required" in schema:
            schema["required"] = [r for r in schema["required"] if r in props]
        tools.append({"name": t["name"], "description": "Read-only. " + t.get("description", ""),
                      "inputSchema": schema})
    return tools


def tool_error(text: str) -> dict:
    return {"content": [{"type": "text", "text": text}], "isError": True}


class Proxy:
    def __init__(self):
        self.calls = 0
        self.camera_moves = 0
        self.max_calls = int(os.environ.get("READONLY_MCP_MAX_CALLS", "4"))

    def handle(self, req: dict):
        method, rid, params = req.get("method"), req.get("id"), req.get("params") or {}
        if rid is None:                       # notification
            return None
        try:
            if method == "initialize":
                result = {"protocolVersion": params.get("protocolVersion", PROTOCOL),
                          "capabilities": {"tools": {"listChanged": False}},
                          "serverInfo": {"name": "glob2-readonly", "version": "1"},
                          "instructions": "Read-only view of the Globulation 2 match being streamed, plus camera_show "
                                          "to point the stream camera. It follows fog of war. Use sparingly: "
                                          "at most a few calls and one camera move per reply."}
            elif method == "ping":
                result = {}
            elif method == "tools/list":
                result = {"tools": filtered_tools()}
            elif method == "tools/call":
                result = self.call(params.get("name"), params.get("arguments"))
            else:
                return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": f"method not available: {method}"}}
        except (urllib.error.URLError, OSError, ValueError, KeyError) as e:
            return {"jsonrpc": "2.0", "id": rid, "result": tool_error(f"game unavailable: {type(e).__name__}")}
        return {"jsonrpc": "2.0", "id": rid, "result": result}

    def call(self, name, args) -> dict:
        if name == "camera_show":
            if self.calls >= self.max_calls:
                return tool_error(f"call limit reached ({self.max_calls} per reply); answer with what you have")
            if self.camera_moves >= 1:
                return tool_error("one camera move per reply")
            self.calls += 1
            args = {k: v for k, v in (args if isinstance(args, dict) else {}).items() if k in CAMERA_ARGS}
            by = args.pop("asked_by", "")
            ok, msg = camera.show(source="chat", by=by if isinstance(by, str) else "", **args)
            if ok:
                self.camera_moves += 1
                return {"content": [{"type": "text", "text": msg}]}
            return tool_error(msg)
        if name not in ALLOW:
            return tool_error(f"{name} is not available: this connection is read-only")
        if self.calls >= self.max_calls:
            return tool_error(f"call limit reached ({self.max_calls} per reply); answer with what you have")
        self.calls += 1
        out = game_rpc("tools/call", {"name": name, "arguments": sanitize(name, args)}, name)
        if "error" in out:
            return tool_error(str(out["error"].get("message", "error"))[:500])
        return out.get("result", tool_error("empty result"))


def main():
    proxy = Proxy()
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except ValueError:
            continue
        reqs = req if isinstance(req, list) else [req]
        for r in reqs:
            resp = proxy.handle(r)
            if resp is not None:
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()


if __name__ == "__main__":
    main()
