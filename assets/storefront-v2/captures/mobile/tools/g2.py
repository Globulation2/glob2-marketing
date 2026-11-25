#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Shared helpers for the storefront-v2 mobile captures.

Two capture targets share one driver (the game's embedded MCP UI server on
127.0.0.1:47812):

* ``host``  - the desktop build of the same commit, started with the SDL dummy
  video driver so the window can be any device pixel size, rendering the real
  touch presentation (``--interface phone|tablet``) at a device density scale
  (``--ui-scale``). Frames are read with ``ui_screenshot`` at native pixels.
* ``ios``   - the real iOS app in the iOS Simulator. Frames are read with
  ``simctl io screenshot`` (the simulator framebuffer, exact Apple pixel sizes).

Environment (see ../README.md):
  GLOB2_WT        game worktree (default ~/glob2/glob2-wt-mobile-capture)
  GLOB2_SCRATCH   scratch directory for saves, profiles, logs and candidates
                  (default $TMPDIR/glob2-mobile-capture)
  DEVELOPER_DIR   full Xcode (simctl); defaults to /Applications/Xcode.app/...
"""
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mcp  # noqa: E402

# 47812 is this task's desktop-instance port; the simulator app shares the Mac's
# loopback, so it takes its own port to let both run at once.
PORT = int(os.environ.get("GLOB2_MCP_PORT", "47812"))
IOS_PORT = 47912
mcp.PORT = PORT
WT = Path(os.environ.get("GLOB2_WT", Path.home() / "glob2/glob2-wt-mobile-capture"))
SCRATCH = Path(os.environ.get("GLOB2_SCRATCH", Path(tempfile.gettempdir()) / "glob2-mobile-capture"))
DEVELOPER_DIR = os.environ.get("DEVELOPER_DIR", "/Applications/Xcode.app/Contents/Developer")
HOST_BINARY = WT / "build/darwin/client/release/src/glob2"
SDL_PREFIX = WT / "build/sdl3/prefix"
SIMSET = WT / "build/mobile-tools/ios-simulators"
IOS_APP = WT / "build/ios/simulator/arm64/15.0/client/release/xcode-project/build/Release-iphonesimulator/Glob2.app"
BUNDLE_ID = "org.globulation2.glob2"
SAVES = SCRATCH / "saves"

os.environ.setdefault("GLOB2_MCP_TOKEN_FILE", str(SCRATCH / f"mcp-token-{PORT}"))

# First-launch choices are answered in the profile so every run starts at the
# main menu: silence, right thumb, introduction already offered.
PREFERENCES = {
    "username": "Player",
    "mute": "1",
    "introductionOffered": "1",
    "audioPreferenceChosen": "1",
    "thumbSide": "0",
    "thumbSideChosen": "1",
    "autosaveGames": "0",
    "language": "en",
    # Auto HD artwork steps down for the session after frame hitches or memory
    # pressure; store captures force it on so every frame uses the HD sprites.
    "highResolutionArtworkChoice": "on",
    "highResolutionArtwork": "1",
}
HD_ARTWORK = "on (highResolutionArtworkChoice=on in the capture profile; Auto step-down cannot apply)"


def write_profile(profile: Path, saves=(), extra=None):
    """Create a disposable profile holding only the capture saves."""
    (profile / "games").mkdir(parents=True, exist_ok=True)
    prefs = dict(PREFERENCES)
    prefs.update(extra or {})
    (profile / "preferences.txt").write_text("".join(f"{k}={v}\n" for k, v in prefs.items()))
    for save in saves:
        shutil.copy2(save, profile / "games" / Path(save).name)


# ---------------------------------------------------------------- MCP sugar

def call(tool, **args):
    data, images, err = mcp.call(tool, args, PORT, 60)
    if err:
        raise RuntimeError(f"{tool} failed: {data}")
    return data


def tcall(tool, **args):
    args["token"] = mcp.token(PORT)
    return call(tool, **args)


def wait_mcp(timeout=90):
    end = time.time() + timeout
    while time.time() < end:
        try:
            status, _, err = mcp.call("ui_status", {}, PORT, 5)
            if not err and status.get("available"):
                return status
        except Exception:
            pass
        time.sleep(1)
    raise RuntimeError("MCP listener did not come up")


def screen():
    return mcp.inspect(PORT).get("screen")


def wait_screen(name, timeout=60):
    end = time.time() + timeout
    while time.time() < end:
        try:
            if screen() == name:
                return
        except Exception:
            pass
        time.sleep(0.5)
    raise RuntimeError(f"screen {name!r} did not appear (now {screen()!r})")


def act(key, action="activate", value=None, **extra):
    data, _, err = mcp.act(key, action, value, PORT, **extra)
    if err:
        raise RuntimeError(f"ui_act {key} {action} {value!r} failed: {data}")
    return data


def controls():
    return list(mcp.walk(mcp.inspect(PORT)))


def find(text):
    return mcp.find(text, PORT)


def click(x, y, space="native"):
    return tcall("ui_click", x=x, y=y, space=space)


def drag(points, duration_ms=400, space="native"):
    return tcall("ui_drag", points=points, duration_ms=duration_ms, space=space)


def view(x=None, y=None, zoom=None, **extra):
    args = dict(extra)
    if x is not None:
        args.update(x=x, y=y)
    if zoom is not None:
        args["zoom"] = zoom
    return tcall("game_view", **args)


def game_time(action="status", **extra):
    if action == "status":
        return call("game_time", action="status")
    return tcall("game_time", action=action, **extra)


def tick():
    return game_time()["tick"]


def run_to(target, speed=10, poll=2.0, timeout=3600):
    """Run the match at `speed` until tick >= target, then return to 1x."""
    game_time("resume", speed=speed)
    end = time.time() + timeout
    while time.time() < end:
        t = tick()
        if t >= target:
            break
        time.sleep(poll if target - t > 400 else 0.05)
    game_time("status" if False else "resume", speed=0)
    return tick()


def host_shot(path):
    meta = mcp.screenshot(str(path), 16384, PORT)
    return {k: v for k, v in meta.items() if k in ("width", "height", "frame_id")}


# ---------------------------------------------------------------- host target

class Host:
    """Desktop build, dummy video driver, touch presentation at device pixels.

    The game's own software renderer is used: with the dummy video driver the
    portable SDL renderer falls back to SDL's software render driver, which
    crashed in SDL_UpdateTexture about 20 seconds into a match (0.11.8.0).
    """

    def __init__(self, width, height, scale, interface, profile, log=None, binary=HOST_BINARY):
        self.args = dict(width=width, height=height, scale=scale, interface=interface)
        env = dict(os.environ)
        env.update(GLOB2_USER_DATA_DIR=str(profile), SDL_VIDEODRIVER="dummy", SDL_AUDIODRIVER="dummy",
                   DYLD_LIBRARY_PATH=str(SDL_PREFIX / "lib"))
        command = [str(binary), "play", "--interface", interface, "--ui-scale", str(scale),
                   "--window-size", f"{width}x{height}", "--no-fullscreen", "--mute",
                   "--renderer", "software", "--mcp-port", str(PORT)]
        self.command = command
        self.log = open(log or (Path(profile) / "game.log"), "w")
        token = Path(os.environ["GLOB2_MCP_TOKEN_FILE"])
        if token.exists():
            token.unlink()
        self.process = subprocess.Popen(command, env=env, cwd=str(WT), stdout=self.log, stderr=subprocess.STDOUT)
        wait_mcp()

    def shot(self, path):
        return host_shot(path)

    def close(self):
        if self.process.poll() is None:
            self.process.send_signal(signal.SIGTERM)
            try:
                self.process.wait(10)
            except subprocess.TimeoutExpired:
                self.process.kill()
        self.log.close()


# ---------------------------------------------------------------- iOS target

def simctl(*args, check=True, capture=True):
    env = dict(os.environ, DEVELOPER_DIR=DEVELOPER_DIR)
    return subprocess.run(["xcrun", "simctl", "--set", str(SIMSET), *args], env=env, check=check,
                          text=True, capture_output=capture).stdout


class IOS:
    """The real iOS app in an isolated Simulator device."""

    def __init__(self, device, orientation="portrait"):
        self.device = device
        self.orientation = orientation

    def boot(self):
        simctl("boot", self.device, check=False)
        simctl("bootstatus", self.device)
        simctl("status_bar", self.device, "override", "--time", "9:41", "--batteryState", "discharging",
               "--batteryLevel", "100", "--wifiBars", "3", "--cellularBars", "4",
               "--dataNetwork", "wifi", "--wifiMode", "active", "--cellularMode", "active")

    def install(self):
        simctl("install", self.device, str(IOS_APP))

    def profile(self) -> Path:
        container = Path(simctl("get_app_container", self.device, BUNDLE_ID, "data").strip())
        return container / "Library/Application Support/Globulation2/glob2"

    def launch(self, saves=(), extra=None):
        simctl("terminate", self.device, BUNDLE_ID, check=False)
        profile = self.profile()
        if (profile / "games").exists():
            shutil.rmtree(profile / "games")
        write_profile(profile, saves, dict({"mcpEnabled": "1", "mcpPort": str(PORT)}, **(extra or {})))
        token = Path(os.environ["GLOB2_MCP_TOKEN_FILE"])
        if token.exists():
            token.unlink()
        env = dict(os.environ, DEVELOPER_DIR=DEVELOPER_DIR)
        # SDL reads its orientation hint from the environment with override
        # priority, so one unmodified app can be held in either orientation.
        env["SIMCTL_CHILD_SDL_ORIENTATIONS"] = (
            "LandscapeRight" if self.orientation == "landscape" else "Portrait")
        subprocess.run(["xcrun", "simctl", "--set", str(SIMSET), "launch", self.device, BUNDLE_ID],
                       env=env, check=True, capture_output=True)
        wait_mcp()

    def shot(self, path):
        simctl("io", self.device, "screenshot", "--type=png", str(path))
        return {}

    def close(self):
        simctl("terminate", self.device, BUNDLE_ID, check=False)


if __name__ == "__main__":
    print(json.dumps({"worktree": str(WT), "scratch": str(SCRATCH), "port": PORT}, indent=1))
