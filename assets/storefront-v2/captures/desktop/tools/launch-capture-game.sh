#!/bin/sh
# Launch the released game off-screen for captures.
#
#   * SDL dummy video driver: no window appears, and the drawable can be larger
#     than any attached display (a real macOS window is clamped to its screen).
#   * --renderer portable-sdl: the shipped SDL renderer backend. Unlike
#     --renderer software it has texture filtering, so it draws the HD artwork
#     layers (checked against the default GPU renderer at the same density).
#   * --ui-scale 2: the raster scale of a 2x (HiDPI/Retina) display. 3840x2160
#     at scale 2 is pixel-for-pixel a 1920x1080-point HiDPI window; 2880x1800 at
#     scale 2 is a 1440x900-point Retina window. At this density the HD sprite
#     policy draws HD frames at 100% zoom (64 px per tile).
#   * preferences: Artwork is set to High resolution explicitly. On Automatic
#     the game turns HD artwork off for the session as soon as frames hitch,
#     which this off-screen software rasteriser always does, and every later
#     frame would be magnified 32-pixel art. The saved game speed is reset to
#     normal. (capture.py turns clouds and cloud shadows off through Settings.)
#   * fresh profile directory and the embedded MCP UI server on its own port.
#
# usage: launch-capture-game.sh PROFILE_DIR [WIDTHxHEIGHT] [UI_SCALE] [MCP_PORT]
set -eu
GLOB2="${GLOB2:-/Applications/Glob2.app/Contents/MacOS/glob2}"
profile="$1"; size="${2:-3840x2160}"; scale="${3:-2}"; port="${4:-47811}"
mkdir -p "$profile"
cd "$profile"
prefs="$profile/preferences.txt"
touch "$prefs"
for setting in highResolutionArtworkChoice=on highResolutionArtwork=1 gameSpeed=0; do
  key="${setting%%=*}"
  grep -v "^$key=" "$prefs" > "$prefs.tmp" || true
  echo "$setting" >> "$prefs.tmp"
  mv "$prefs.tmp" "$prefs"
done
SDL_VIDEO_DRIVER=dummy SDL_AUDIO_DRIVER=dummy \
GLOB2_USER_DATA_DIR="$profile" GLOB2_USER_DIR="$profile" \
exec "$GLOB2" play --renderer portable-sdl --window-size "$size" --no-fullscreen \
  --ui-scale "$scale" --interface desktop --mute --mcp-port "$port"
