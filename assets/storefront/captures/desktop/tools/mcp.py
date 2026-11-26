#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Minimal client for the Globulation 2 embedded MCP UI server (stdlib only).

Usage:
  mcp.py [--port N] list
  mcp.py [--port N] call TOOL '{"json":"args"}'
  mcp.py [--port N] tcall TOOL '{"json":"args"}'      (adds a control token)
  mcp.py [--port N] tree                              (outline of the screen)
  mcp.py [--port N] find TEXT                         (controls matching text)
  mcp.py [--port N] act KEY [ACTION [VALUE]]          (ui_act by key)
  mcp.py [--port N] shot OUTPUT.png [max_width]

`call` prints the tool's structured result as JSON. `shot` saves the next
complete game frame at native pixels (no scaling) and prints its metadata.
"""
import base64
import json
import sys
import urllib.request

import os as _os
PORT = int(_os.environ.get("GLOB2_MCP_PORT", "47811"))
PROTOCOL = "2025-11-25"


def rpc(method, params=None, port=None, timeout=45):
    body = {"jsonrpc": "2.0", "id": 1, "method": method}
    if params is not None:
        body["params"] = params
    req = urllib.request.Request(
        f"http://127.0.0.1:{port or PORT}/mcp",
        data=json.dumps(body).encode(),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "MCP-Protocol-Version": PROTOCOL,
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def call(tool, args=None, port=None, timeout=45):
    """Return (structured_or_text, images, is_error)."""
    reply = rpc("tools/call", {"name": tool, "arguments": args or {}}, port, timeout)
    if "error" in reply:
        return reply["error"], [], True
    result = reply["result"]
    images = [base64.b64decode(c["data"]) for c in result.get("content", []) if c.get("type") == "image"]
    data = result.get("structuredContent")
    if data is None:
        texts = [c["text"] for c in result.get("content", []) if c.get("type") == "text"]
        data = "\n".join(texts)
        try:
            data = json.loads(data)
        except (ValueError, TypeError):
            pass
    return data, images, bool(result.get("isError"))


def screenshot(path, max_width=8192, port=None):
    data, images, err = call("ui_screenshot", {"max_width": max_width, "max_height": max_width}, port, 60)
    if err or not images:
        raise RuntimeError(f"screenshot failed: {data}")
    with open(path, "wb") as fh:
        fh.write(images[0])
    return data


TOKEN_FILE = None


def token(port=None):
    """Acquire (or reuse a cached) control token. Cached in GLOB2_MCP_TOKEN_FILE."""
    import os
    import tempfile
    path = TOKEN_FILE or os.environ.get(
        "GLOB2_MCP_TOKEN_FILE", os.path.join(tempfile.gettempdir(), f"glob2-mcp-token-{port or PORT}"))
    if os.path.exists(path):
        tok = open(path).read().strip()
        data, _, err = call("ui_renew_control", {"token": tok}, port)
        if not err:
            return tok
    data, _, err = call("ui_acquire_control", {}, port)
    if err:
        raise RuntimeError(f"cannot acquire control: {data}")
    tok = data["token"]
    with open(path, "w") as fh:
        fh.write(tok)
    return tok


def inspect(port=None, **args):
    data, _, err = call("ui_inspect", args, port)
    if err:
        raise RuntimeError(f"inspect failed: {data}")
    return data["inspection"]


def walk(inspection):
    """Yield (surface_instance, control) for every control on the screen."""
    def rec(surface, ctl):
        yield surface, ctl
        for child in ctl.get("children", []):
            yield from rec(surface, child)
    for surface in inspection.get("surfaces", []):
        for ctl in surface.get("controls", []):
            yield from rec(surface["instance"], ctl)


def find(text, port=None):
    """Controls whose key or label contains text (case-insensitive)."""
    text = text.lower()
    out = []
    for surface, ctl in walk(inspect(port)):
        if text in str(ctl.get("key", "")).lower() or text in str(ctl.get("label", "")).lower():
            out.append(dict({k: v for k, v in ctl.items() if k != "children"}, surface=surface))
    return out


def act(key, action="activate", value=None, port=None, **extra):
    """Operate an inspected control by key, looking up its surface and revision."""
    matches = [(s, c) for s, c in walk(inspect(port)) if c.get("key") == key]
    if not matches:
        raise RuntimeError(f"no control with key {key!r}")
    surface, ctl = matches[-1]
    args = {"token": token(port), "surface": surface, "key": key,
            "revision": ctl["revision"], "action": action}
    if value is not None:
        args["value"] = value
    args.update(extra)
    data, images, err = call("ui_act", args, port)
    if isinstance(data, dict) and "inspection" in data:
        data = dict(data, inspection={"screen": data["inspection"].get("screen")})
    return data, images, err


def tree(port=None):
    """Compact text outline of the current screen."""
    insp = inspect(port)
    lines = ["screen: " + str(insp.get("screen"))]
    def rec(ctl, depth):
        bits = [ctl.get("role", "?")]
        for k in ("key", "label", "value", "value_label", "selected", "enabled", "actions"):
            if k in ctl:
                bits.append(f"{k}={ctl[k]!r}"[:110])
        lines.append("  " * depth + " ".join(bits))
        for child in ctl.get("children", []):
            rec(child, depth + 1)
    for surface in insp.get("surfaces", []):
        lines.append(f"surface {surface['instance']}")
        for ctl in surface.get("controls", []):
            rec(ctl, 1)
    return "\n".join(lines)


def main(argv):
    global PORT
    if len(argv) > 1 and argv[0] == "--port":
        PORT = int(argv[1])
        argv = argv[2:]
    if not argv:
        print(__doc__)
        return 2
    if argv[0] == "list":
        for tool in rpc("tools/list")["result"]["tools"]:
            print(tool["name"], "-", tool.get("description", "")[:100].replace("\n", " "))
    elif argv[0] == "schema":
        for tool in rpc("tools/list")["result"]["tools"]:
            if tool["name"] == argv[1]:
                print(json.dumps(tool, indent=1))
    elif argv[0] == "call":
        data, images, err = call(argv[1], json.loads(argv[2]) if len(argv) > 2 else {})
        print(json.dumps(data, indent=1) if not isinstance(data, str) else data)
        if images:
            print(f"[{len(images)} image(s) omitted]", file=sys.stderr)
        return 1 if err else 0
    elif argv[0] == "tcall":
        args = json.loads(argv[2]) if len(argv) > 2 else {}
        args["token"] = token()
        data, images, err = call(argv[1], args)
        print(json.dumps(data, indent=1) if not isinstance(data, str) else data)
        return 1 if err else 0
    elif argv[0] == "tree":
        print(tree())
    elif argv[0] == "find":
        print(json.dumps(find(argv[1]), indent=1))
    elif argv[0] == "act":
        value = None
        if len(argv) > 3:
            try:
                value = json.loads(argv[3])
            except ValueError:
                value = argv[3]
        data, _, err = act(argv[1], argv[2] if len(argv) > 2 else "activate", value)
        print(json.dumps(data, indent=1) if not isinstance(data, str) else data)
        return 1 if err else 0
    elif argv[0] == "shot":
        meta = screenshot(argv[1], int(argv[2]) if len(argv) > 2 else 8192)
        if isinstance(meta, dict):
            meta = {k: v for k, v in meta.items() if k != "data"}
        print(json.dumps(meta))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
