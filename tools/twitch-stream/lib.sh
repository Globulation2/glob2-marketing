# Shared configuration for the stream rig scripts. Source it; do not run it.
# Precedence: environment variables, then $GLOB2_STREAM_HOME/stream.env
# (default ~/glob2-stream), then the defaults below.
GLOB2_STREAM_HOME="${GLOB2_STREAM_HOME:-$HOME/glob2-stream}"
# shellcheck disable=SC2034  # used by the scripts that source this file
RIG_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
RIG_SETTINGS=(GLOB2_SRC GLOB2_BIN GAME_RENDERER STREAM_DISPLAY STREAM_SIZE STREAM_FPS STREAM_VBITRATE
  STREAM_ABITRATE STREAM_ENCODER STREAM_SINK MCP_PORT GAME_PROFILE TWITCH_INGEST TWITCH_KEY_FILE
  OVERLAY_FILE LOG_DIR BRAND BRAND_LOGO BRAND_TEXT BRAND_TEXT_SIZE BRAND_WIDTH BRAND_OPACITY
  BRAND_MARGIN_RIGHT BRAND_MARGIN_BOTTOM)
if [[ -f "$GLOB2_STREAM_HOME/stream.env" ]]; then
  declare -A rig_env=()
  for v in "${RIG_SETTINGS[@]}"; do [[ -n "${!v+x}" ]] && rig_env[$v]="${!v}"; done
  # shellcheck disable=SC1091
  source "$GLOB2_STREAM_HOME/stream.env"
  for v in "${!rig_env[@]}"; do printf -v "$v" '%s' "${rig_env[$v]}"; done
  unset rig_env v
fi
: "${GLOB2_SRC:=$GLOB2_STREAM_HOME/src}"
: "${GLOB2_BIN:=$GLOB2_SRC/build/linux/client/perf/src/glob2}"
: "${GAME_RENDERER:=sdl-gpu}"
: "${STREAM_DISPLAY:=:99}"
: "${STREAM_SIZE:=1920x1080}"
: "${STREAM_FPS:=30}"
: "${STREAM_VBITRATE:=4500k}"
: "${STREAM_ABITRATE:=160k}"
: "${STREAM_ENCODER:=}"
: "${STREAM_SINK:=glob2_stream}"
: "${MCP_PORT:=27300}"
: "${GAME_PROFILE:=$GLOB2_STREAM_HOME/profile}"
: "${TWITCH_INGEST:=rtmp://live.twitch.tv/app}"
: "${TWITCH_KEY_FILE:=$HOME/.config/glob2-stream/twitch.key}"
: "${OVERLAY_FILE:=$GLOB2_STREAM_HOME/overlay/caption.txt}"
: "${LOG_DIR:=$GLOB2_STREAM_HOME/logs}"
# Branding overlay (sizes in pixels at 1080p; scaled to STREAM_SIZE).
: "${BRAND:=1}"
: "${BRAND_LOGO:=$RIG_DIR/assets/glob2-wordmark.png}"
: "${BRAND_TEXT=glob2.online}"          # empty string = no text
: "${BRAND_TEXT_SIZE:=22}"
: "${BRAND_WIDTH:=200}"
: "${BRAND_OPACITY:=0.85}"
: "${BRAND_MARGIN_RIGHT:=224}"          # clears the ~200 px right sidebar and its zoom controls
: "${BRAND_MARGIN_BOTTOM:=16}"
export GLOB2_STREAM_HOME MCP_PORT LOG_DIR
