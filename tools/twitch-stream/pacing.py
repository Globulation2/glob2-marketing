"""Shared call pacing for the player's game and stream-ctl tools.

The user (2026-11-24): about 5 calls a minute is enough to play. Measured before pacing: ~14 player
calls a minute, a tenth of them refused narrations or waits. Instead of refusing, each paced call
waits until PLAYER_CALLS_PER_MIN allows it, so no call is wasted; menus and bookkeeping aren't paced.
The last call's start time is shared through STATE_DIR/pace (both MCP servers are separate processes).
"""
import fcntl
import os
import pathlib
import time


def interval() -> float:
    try:
        per_min = float(os.environ.get("PLAYER_CALLS_PER_MIN") or 10)
    except ValueError:
        per_min = 10.0
    return 60.0 / per_min if per_min > 0 else 0.0


def wait_turn() -> float:
    """Block until this call may run; returns the seconds waited."""
    gap = interval()
    if gap <= 0:
        return 0.0
    path = pathlib.Path(os.environ.get("STATE_DIR", "/tmp")) / "pace"
    with open(path, "a+") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)          # one paced call at a time, across both servers
        fh.seek(0)
        try:
            last = float(fh.read().strip() or 0)
        except ValueError:
            last = 0.0
        delay = max(0.0, last + gap - time.time())
        if delay > gap:                          # clock jumped: don't wait longer than one interval
            delay = gap
        time.sleep(delay)
        fh.seek(0)
        fh.truncate()
        fh.write(f"{time.time():.3f}")
        fh.flush()
    try:
        os.chmod(path, 0o664)
    except OSError:
        pass
    return delay
