#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Shared setup for the App Store app-preview recordings.

Reuses the mobile capture driver (../../captures/mobile/tools/g2.py, mcp.py): the
real iOS app (capture build with the loopback MCP listener) in the isolated
simulator set of the capture worktree. Each device class gets its own MCP port so
the iPhone and iPad simulators never share one.

Environment: GLOB2_WT (game worktree, default ~/glob2/glob2-wt-mobile-capture),
GLOB2_SCRATCH (saves/, sim.env, raw recordings).
"""
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CAPTURE_TOOLS = HERE.parents[1] / "captures" / "mobile" / "tools"

DEVICES = {
    "iphone-6.9": {"sim": "IPHONE", "port": 47930, "points": 3, "native": (1320, 2868), "preview": (886, 1920),
                   "model": "iPhone 17 Pro Max simulator, iOS 26.5"},
    "ipad-13": {"sim": "IPAD", "port": 47931, "points": 2, "native": (2064, 2752), "preview": (1200, 1600),
                "model": "iPad Pro 13-inch (M5) simulator, iOS 26.5"},
}


def setup(device):
    d = DEVICES[device]
    os.environ["GLOB2_MCP_PORT"] = str(d["port"])
    os.environ.setdefault("GLOB2_SCRATCH", str(Path(os.environ.get("TMPDIR", "/tmp")) / "glob2-app-previews"))
    os.environ["GLOB2_MCP_TOKEN_FILE"] = str(Path(os.environ["GLOB2_SCRATCH"]) / f"mcp-token-{d['port']}")
    sys.path.insert(0, str(CAPTURE_TOOLS))
    import g2  # noqa: E402
    import mcp  # noqa: E402
    mcp.PORT = g2.PORT = d["port"]
    ids = dict(line.split("=", 1) for line in (g2.SCRATCH / "sim.env").read_text().split())
    return g2, mcp, ids[d["sim"]]
