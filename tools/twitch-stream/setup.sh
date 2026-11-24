#!/usr/bin/env bash
# Prepare a Linux (Debian/Ubuntu) machine for the stream rig. Safe to re-run.
#   setup.sh              install missing packages, create $GLOB2_STREAM_HOME, report GPU support
#   setup.sh --with-game  also fetch a glob2 checkout at GLOB2_SRC and print its build command
set -euo pipefail
source "$(dirname "$(readlink -f "$0")")/lib.sh"

pkgs=(xvfb ffmpeg pulseaudio-utils x11-utils xdotool mesa-utils vulkan-tools curl git fonts-dejavu-core)
missing=()
for p in "${pkgs[@]}"; do dpkg -s "$p" >/dev/null 2>&1 || missing+=("$p"); done
if ((${#missing[@]})); then
  echo "installing: ${missing[*]}"
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -q "${missing[@]}"
else
  echo "packages: all present"
fi

mkdir -p "$GLOB2_STREAM_HOME"/{logs,profile,overlay,notes}
if [[ ! -f "$GLOB2_STREAM_HOME/stream.env" ]]; then
  cp "$RIG_DIR/stream.env.example" "$GLOB2_STREAM_HOME/stream.env"
  echo "created $GLOB2_STREAM_HOME/stream.env (edit to taste)"
fi
key_dir="$(dirname "$TWITCH_KEY_FILE")"
mkdir -p "$key_dir" && chmod 700 "$key_dir"
if [[ -s "$TWITCH_KEY_FILE" ]]; then
  echo "stream key: present ($(stat -c %A "$TWITCH_KEY_FILE"))"
else
  echo "stream key: missing. Copy it from the Twitch dashboard (Settings > Stream), then run"
  echo "  install -m 600 /dev/stdin $TWITCH_KEY_FILE"
  echo "paste the key and press Ctrl-D."
fi

if ffmpeg -hide_banner -loglevel error -f lavfi -i color=size=1280x720:rate=30 -frames:v 1 -c:v h264_nvenc -f null - >/dev/null 2>&1; then
  echo "encoder: h264_nvenc works (GPU encoding)"
else
  echo "encoder: h264_nvenc unavailable; stream.sh will use libx264 on the CPU"
fi
gpus=$(vulkaninfo --summary 2>/dev/null | awk -F= '/deviceName/{gsub(/^ +/,"",$2); print $2}' | grep -v llvmpipe || true)
if [[ -n "$gpus" ]]; then
  echo "vulkan GPUs: $(echo "$gpus" | paste -sd, -)"
else
  echo "vulkan: no hardware device; set GAME_RENDERER=software (slow) or use a GPU machine"
fi

if [[ "${1:-}" == "--with-game" ]]; then
  if [[ -e "$GLOB2_SRC/.git" ]]; then
    echo "game checkout: $GLOB2_SRC already exists ($(git -C "$GLOB2_SRC" log -1 --oneline))"
  else
    git clone --depth 50 https://github.com/Globulation2/glob2 "$GLOB2_SRC"
  fi
  cat <<MSG
Build the game (perf tier) with:
  cd "$GLOB2_SRC" && python3 tools/dev_build.py perf=1
If the build reports "Missing SDL3", point GLOB2_SDL3_PREFIX at a native SDL3 prefix, for example
  python3 scons/sdl3_dependencies.py --prefix ~/.local/share/glob2/native-sdl3/prefix --work ~/.local/share/glob2/native-sdl3/sources
  GLOB2_SDL3_PREFIX=~/.local/share/glob2/native-sdl3/prefix python3 tools/dev_build.py perf=1
The binary lands at $GLOB2_BIN.
MSG
fi
