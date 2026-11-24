"""Rig settings for the Python tools, resolved exactly as the shell scripts do.

lib.sh is the single source of defaults; this sources it in bash and reads back
its settings (environment, then $GLOB2_STREAM_HOME/stream.env, then defaults).
"""
import os
import pathlib
import subprocess

RIG_DIR = pathlib.Path(__file__).resolve().parent


def load() -> dict:
    script = 'source "$1"; for v in GLOB2_STREAM_HOME RIG_DIR "${RIG_SETTINGS[@]}"; do printf "%s=%s\\0" "$v" "${!v}"; done'
    out = subprocess.run(["bash", "-c", script, "rigconfig", str(RIG_DIR / "lib.sh")],
                         check=True, capture_output=True, text=True, env=os.environ).stdout
    return dict(item.split("=", 1) for item in out.split("\0") if item)
