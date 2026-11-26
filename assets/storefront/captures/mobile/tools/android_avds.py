#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Create and run the three store-capture AVDs (in the game worktree's build/mobile-tools/).

Mirrors platforms/mobile/emulator.py configure: the pinned emulator and the API 35
arm64-v8a default image (platforms/mobile/emulator.json), avdmanager run against a
task-local SDK view, then config.ini set to the store device's pixels and density.
Every emulator registers with its own ADB server on port 15077, never the user's.

    GLOB2_WT=<game worktree> python3 android_avds.py create
    python3 android_avds.py adb-server &                  # ADB server on 15077
    python3 android_avds.py run glob2-store-phone 5600 &  # serial emulator-5600
    python3 android_avds.py run glob2-store-tablet7 5602 &
    python3 android_avds.py run glob2-store-tablet10 5604 &
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

WT = Path(os.environ.get("GLOB2_WT", Path.home() / "glob2/glob2-wt-android-capture"))
sys.path[:0] = [str(WT / "platforms/mobile"), str(WT / "buildsys")]
from developer_apk import java_environment  # noqa: E402
from dev_paths import android_sdk  # noqa: E402
from dev_store import android_java_command  # noqa: E402

TOOLS = WT / "build/mobile-tools"
SDK = android_sdk(WT)
LOCK = json.loads((WT / "platforms/mobile/emulator.json").read_text())
IMAGE_REL = f"system-images/android-{LOCK['api']}/{LOCK['tag']}/arm64-v8a"
PACKAGE = f"system-images;android-{LOCK['api']};{LOCK['tag']};arm64-v8a"

# name: (device profile, width, height, density, orientation, ram MB)
AVDS = {
    "glob2-store-phone": ("pixel_2", 1080, 1920, 420, "portrait", 4096),
    "glob2-store-tablet7": ("Nexus 7 2013", 1200, 1920, 280, "landscape", 4096),
    "glob2-store-tablet10": ("Nexus 10", 1600, 2560, 320, "landscape", 4096),
}


def environment(adb_port=15077):
    env = java_environment(WT)
    env.pop("ADB_SERVER_SOCKET", None)
    env.pop("ANDROID_SERIAL", None)
    env.update(ANDROID_USER_HOME=str(TOOLS / "android-user"), ANDROID_EMULATOR_HOME=str(TOOLS / "android-user"),
               ANDROID_AVD_HOME=str(TOOLS / "avd"), ANDROID_HOME=str(SDK), ANDROID_SDK_ROOT=str(SDK),
               ANDROID_ADB_SERVER_PORT=str(adb_port),
               ANDROID_EMU_CRASH_REPORTING_DATABASE=str(TOOLS / "emulator-crash.db"),
               ANDROID_EMULATOR_DISCOVERY_DIR=str(TOOLS / "emulator-discovery"),
               ADB_MDNS_AUTO_CONNECT="", ADB_LOCAL_TRANSPORT_MAX_PORT="0", TMPDIR=str(TOOLS / "tmp"))
    for d in ("android-user", "avd", "tmp", "emulator-discovery"):
        (TOOLS / d).mkdir(parents=True, exist_ok=True)
    return env


def props(path):
    return dict(l.split("=", 1) for l in path.read_text().splitlines() if "=" in l and not l.startswith("#"))


def create():
    env = environment()
    view = TOOLS / "sdk-view"
    if view.exists():
        shutil.rmtree(view)
    for rel in ("cmdline-tools/19.0", "emulator", IMAGE_REL):
        (view / rel).mkdir(parents=True)
        for entry in (SDK / rel).iterdir():
            (view / rel / entry.name).symlink_to(entry)
    (view / "licenses").symlink_to(SDK / "licenses")
    view_env = dict(env, ANDROID_HOME=str(view), ANDROID_SDK_ROOT=str(view))
    for name, (device, w, h, dpi, orientation, ram) in AVDS.items():
        avd = TOOLS / "avd" / (name + ".avd")
        if not (avd / "config.ini").exists():
            subprocess.run(android_java_command(view, "avdmanager", view_env) +
                           ["create", "avd", "--name", name, "--package", PACKAGE, "--device", device,
                            "--path", str(avd)], input="no\n", text=True, env=view_env, check=True)
        config = avd / "config.ini"
        s = props(config)
        s.update({"image.sysdir.1": IMAGE_REL + "/", "hw.lcd.width": str(w), "hw.lcd.height": str(h),
                  "hw.lcd.density": str(dpi), "hw.initialOrientation": orientation, "hw.ramSize": str(ram),
                  "hw.keyboard": "yes", "hw.gpu.enabled": "yes", "hw.gpu.mode": "host",
                  "disk.dataPartition.size": "8G", "skin.dynamic": "yes", "showDeviceFrame": "no"})
        s.pop("skin.name", None)
        s.pop("skin.path", None)
        config.write_text("".join(f"{k}={v}\n" for k, v in s.items()))
        print(name, "->", config)
    shutil.rmtree(view)


def run(name, port, gpu="host", window=False):
    env = environment()
    avd = TOOLS / "avd" / (name + ".avd")
    emulator = str(SDK / "emulator/emulator")
    cmd = [emulator, "-avd", name, "-port", str(port), "-no-audio", "-no-boot-anim", "-no-snapshot",
           "-no-metrics", "-crash-report-mode", "disabled", "-datadir", str(avd), "-data",
           str(avd / "userdata-qemu.img"), "-gpu", gpu, "-cores", "4"]
    if not window:
        cmd.append("-no-window")
    os.execvpe(emulator, cmd, env)


if __name__ == "__main__":
    what = sys.argv[1]
    if what == "create":
        create()
    elif what == "run":
        run(sys.argv[2], int(sys.argv[3]), *(sys.argv[4:5] or ["host"]))
    elif what == "list":
        print("\n".join(AVDS))
    elif what == "env":
        e = environment()
        print(json.dumps({k: e[k] for k in e if k.startswith(("ANDROID", "JAVA", "ADB"))}, indent=1))
        print("SDK", SDK)
    elif what == "adb-server":
        env = environment()
        adb = [str(SDK / "platform-tools/adb"), "-P", "15077"]
        os.execvpe(adb[0], adb + ["--one-device", "glob2-store-no-usb", "server", "nodaemon"], env)
