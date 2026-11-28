#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-or-later
# Launch the released game off-screen for trailer footage.
#
# Same conditions as ../../captures/desktop/tools/launch-capture-game.sh (SDL
# dummy video driver, --renderer portable-sdl, --ui-scale 2, HD artwork forced
# on, fresh profile, embedded MCP UI server), plus:
#   * clouds and cloud shadows off and game speed normal, written to the
#     profile before the start;
#   * optional RECORD argument: the game's own gameplay recorder
#     (--record FILE --record-fps FPS). Not used for the trailer: with the dummy
#     video driver the recorder gets no framebuffer, so capture_shot.py saves
#     every tick's frame through the MCP UI server instead. The trailer ran
#     launch-record-game.sh PROFILE 4256x2800 2 47814.
#
# usage: launch-record-game.sh PROFILE_DIR [WIDTHxHEIGHT] [UI_SCALE] [MCP_PORT] [RECORD.mp4] [FPS]
set -eu
GLOB2="${GLOB2:-/Applications/Glob2.app/Contents/MacOS/glob2}"
profile="$1"; size="${2:-3840x2160}"; scale="${3:-2}"; port="${4:-47814}"
record="${5:-}"; fps="${6:-60}"
mkdir -p "$profile"
cd "$profile"
prefs="$profile/preferences.txt"
touch "$prefs"
for setting in highResolutionArtworkChoice=on highResolutionArtwork=1 gameSpeed=0 \
               clouds=0 cloudShadows=0 graphicsDetailAdaptive=0 introductionOffered=1 \
               audioPreferenceChosen=1 ${GLOB2_EXTRA_PREFS:-}; do
  key="${setting%%=*}"
  grep -v "^$key=" "$prefs" > "$prefs.tmp" || true
  echo "$setting" >> "$prefs.tmp"
  mv "$prefs.tmp" "$prefs"
done
set -- play --renderer "${GLOB2_RENDERER:-portable-sdl}" --window-size "$size" --no-fullscreen \
  --ui-scale "$scale" --interface desktop ${GLOB2_MUTE:---mute} --mcp-port "$port"
if [ -n "$record" ]; then
  set -- "$@" --record "$record" --record-fps "$fps" --record-encoder "${GLOB2_RECORD_ENCODER:-auto}" \
    --record-crf "${GLOB2_RECORD_CRF:-12}"
  # Short chapters give the recording a tick-to-time map (capture_realtime.py).
  if [ -n "${GLOB2_RECORD_CHAPTER_TICKS:-}" ]; then
    set -- "$@" --record-chapter-ticks "$GLOB2_RECORD_CHAPTER_TICKS"
  fi
fi
export SDL_AUDIO_DRIVER=dummy GLOB2_USER_DATA_DIR="$profile" GLOB2_USER_DIR="$profile"
if [ "${GLOB2_WINDOW:-offscreen}" = "offscreen" ]; then
  export SDL_VIDEO_DRIVER=dummy
fi
exec "$GLOB2" "$@"
