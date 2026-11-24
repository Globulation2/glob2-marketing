#!/usr/bin/env python3
"""Call one tool on the stream game's MCP server over loopback HTTP.

Usage: mcp_call.py TOOL ['{"json": "arguments"}']
The port comes from MCP_PORT (default 27300). Prints each text content block.
"""
import json
import os
import sys
import urllib.request


def call(tool, args=None, port=None):
    port = port or int(os.environ.get("MCP_PORT", "27300"))
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                       "params": {"name": tool, "arguments": args or {}}}).encode()
    req = urllib.request.Request(f"http://127.0.0.1:{port}/mcp", body, {
        "Content-Type": "application/json", "Accept": "application/json, text/event-stream",
        "MCP-Protocol-Version": "2025-11-25", "Mcp-Method": "tools/call", "Mcp-Name": tool})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    out = call(sys.argv[1], json.loads(sys.argv[2]) if len(sys.argv) > 2 else {})
    for c in out.get("result", {}).get("content", []):
        print(c.get("text", f"<{c.get('type')}>"))
    if "error" in out:
        print(json.dumps(out["error"]))
        sys.exit(1)


if __name__ == "__main__":
    main()
