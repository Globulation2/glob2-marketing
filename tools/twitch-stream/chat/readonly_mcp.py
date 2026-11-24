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
"""
import json
import os
import sys
import urllib.error
import urllib.request

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


def filtered_tools() -> list:
    tools = []
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
                          "instructions": "Read-only view of the Globulation 2 match being streamed. "
                                          "It follows fog of war. Use sparingly: at most a few calls per reply."}
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
