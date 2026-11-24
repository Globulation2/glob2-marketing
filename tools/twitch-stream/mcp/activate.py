#!/usr/bin/env python3
"""Activate a control on the stream game by its key, e.g. menu/1 or tutorial/lesson/0.

Usage: activate.py [--acquire] KEY
       activate.py --acquire          only acquire control and save the token
The control token is kept in $GLOB2_STREAM_HOME/logs/token (default ~/glob2-stream).
"""
import json
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mcp_call import call  # noqa: E402

HOME = pathlib.Path(os.environ.get("GLOB2_STREAM_HOME", pathlib.Path.home() / "glob2-stream"))
TOKEN = HOME / "logs" / "token"


def result(tool, args):
    out = call(tool, args)
    if "error" in out:
        sys.exit(f"{tool} failed: {json.dumps(out['error'])}")
    return json.loads(out["result"]["content"][0]["text"])


def acquire():
    tok = result("ui_acquire_control", {})["token"]
    TOKEN.parent.mkdir(parents=True, exist_ok=True)
    TOKEN.write_text(tok)
    TOKEN.chmod(0o600)
    return tok


def walk(controls):
    for c in controls:
        yield c
        yield from walk(c.get("children", []))


def main():
    args = sys.argv[1:]
    fresh = "--acquire" in args
    args = [a for a in args if a != "--acquire"]
    if fresh or not TOKEN.exists():
        acquire()
        if not args:
            print("control acquired; token saved to", TOKEN)
            return
    if not args:
        sys.exit(__doc__)
    key, tok = args[0], TOKEN.read_text().strip()
    d = result("ui_inspect", {"compact": True})["inspection"]
    for s in d["surfaces"]:
        for c in walk(s["controls"]):
            if c.get("key") == key:
                r = result("ui_act", {"token": tok, "surface": s["instance"], "key": key,
                                      "revision": c["revision"], "action": "activate"})
                print("dispatched", r.get("dispatched"), "screen", r.get("inspection", {}).get("screen"))
                return
    keys = [c.get("key") for s in d["surfaces"] for c in walk(s["controls"]) if c.get("key")]
    sys.exit(f"{key} not found on {d['screen']}: {keys}")


if __name__ == "__main__":
    main()
