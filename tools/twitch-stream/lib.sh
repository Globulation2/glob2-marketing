# shellcheck shell=bash
# Shared configuration for the stream rig scripts. Source it; do not run it.
# Precedence: environment variables, then $GLOB2_STREAM_HOME/stream.env
# (default ~/glob2-stream), then the defaults below.
GLOB2_STREAM_HOME="${GLOB2_STREAM_HOME:-$HOME/glob2-stream}"
# shellcheck disable=SC2034  # used by the scripts that source this file
RIG_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
RIG_SETTINGS=(GLOB2_SRC GLOB2_BIN GAME_RENDERER GAME_USERNAME STREAM_DISPLAY STREAM_DISPLAY_BACKEND STREAM_XAUTHORITY STREAM_SIZE STREAM_FPS STREAM_VBITRATE
  STREAM_ABITRATE STREAM_ENCODER STREAM_SINK MCP_PORT GAME_PROFILE TWITCH_INGEST TWITCH_KEY_FILE
  OVERLAY_FILE LOG_DIR BRAND BRAND_LOGO BRAND_TEXT BRAND_TEXT_SIZE BRAND_WIDTH BRAND_OPACITY
  BRAND_MARGIN_RIGHT BRAND_MARGIN_BOTTOM STATE_DIR NOTES_DIR PLAYER_MODEL CHAT_MODEL
  TWITCH_CHANNEL TWITCH_BOT_USER TWITCH_CHAT_TOKEN_FILE TWITCH_CLI_ENV HIGHLIGHTS HIGHLIGHT_SWING HIGHLIGHT_COOLDOWN LIVE_WATCH
  AGENT_USER AGENT_SHARED_DIR AGENT_INSTALL_DIR AGENT_ETC_DIR AGENT_SUDOERS AGENT_EGRESS EGRESS_PROXY_PORT EGRESS_ALLOW
  AUTOSTART_STREAM AUTOSTART_CHAT CAMERA_OVERLAY_FILE CAMERA_DIRECTOR CAMERA_IDLE_SECONDS CAMERA_LABEL_SECONDS
  CAMERA_MIN_INTERVAL CAMERA_HOLD_SECONDS STREAM_GAME_PREFS GAME_AGE_BAND AGENT_COMPACT_WINDOW AGENT_COMPACT_PCT PLAYER_CALLS_PER_MIN
  CAMERA_DRIFT CAMERA_DRIFT_PX_PER_S CAMERA_DRIFT_MAX_PX_PER_S CAMERA_DRIFT_DEADZONE CAMERA_DRIFT_RANGE)
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
: "${GAME_USERNAME:=Claude}"                    # player name shown in game chat and the score screen
: "${STREAM_DISPLAY:=:99}"
: "${STREAM_DISPLAY_BACKEND:=xvfb}"   # xvfb (anywhere, ~12 fps game) or xorg (headless NVIDIA X, 60 fps; display/install-xorg-display.sh)
: "${STREAM_XAUTHORITY:=$GLOB2_STREAM_HOME/display/Xauthority}"
: "${STREAM_SIZE:=1920x1080}"
: "${STREAM_FPS:=60}"
: "${STREAM_VBITRATE:=6000k}"
: "${STREAM_ABITRATE:=160k}"
: "${STREAM_ENCODER:=}"
: "${STREAM_SINK:=glob2_stream}"
: "${MCP_PORT:=27300}"
: "${GAME_PROFILE:=$GLOB2_STREAM_HOME/profile}"
: "${TWITCH_INGEST:=rtmp://live.twitch.tv/app}"
: "${TWITCH_KEY_FILE:=$HOME/.config/glob2-stream/twitch.key}"
# Agent sandbox (sandbox/README.md): the Claude agents run as AGENT_USER from AGENT_INSTALL_DIR and
# share notes, state and the caption with the rig through AGENT_SHARED_DIR. AGENT_USER="" runs them
# as the current user instead, which is less isolated.
: "${AGENT_USER=glob2agent}"
: "${AGENT_INSTALL_DIR:=/opt/glob2-stream-agent}"   # root-owned copy of the agent-side code and claude
: "${AGENT_ETC_DIR:=/etc/glob2-stream}"              # agent.env and the Claude token (claude-oauth-token)
: "${AGENT_SUDOERS:=/etc/sudoers.d/glob2-stream}"    # the one sudo rule: operator may run agent-run as AGENT_USER
: "${AGENT_EGRESS:=1}"                               # 1: firewall the agent user to loopback; it reaches the
                                                    # Anthropic API only through the allowlist egress proxy
: "${EGRESS_PROXY_PORT:=3129}"                      # egress_proxy.py on 127.0.0.1 (systemd: glob2-agent-proxy)
: "${EGRESS_ALLOW:=api.anthropic.com}"              # hosts the proxy tunnels to (port 443 only), space-separated
if [[ -n "$AGENT_USER" ]]; then : "${AGENT_SHARED_DIR:=/var/lib/glob2-stream}"; else : "${AGENT_SHARED_DIR:=$GLOB2_STREAM_HOME}"; fi
: "${OVERLAY_FILE:=$AGENT_SHARED_DIR/overlay/caption.txt}"
# Stream camera (player, chat host and optional director, all through the gate in chat/camera.py).
: "${CAMERA_OVERLAY_FILE:=${OVERLAY_FILE%/*}/camera.txt}"   # "Showing: ..." label, empty when none
: "${CAMERA_DIRECTOR:=1}"            # fallback: an automatic director shows the action when the camera has been idle
: "${CAMERA_IDLE_SECONDS:=90}"
: "${CAMERA_DRIFT:=1}"               # pan slowly toward the action between explicit camera moves
: "${CAMERA_DRIFT_PX_PER_S:=60}"     # glide speed near the target: ~2.7 tiles/s at zoom 0.7
: "${CAMERA_DRIFT_MAX_PX_PER_S:=240}" # up to this when the action is far (~25+ tiles)
: "${CAMERA_DRIFT_DEADZONE:=4}"     # tiles: the drift rests once this close to its target
: "${CAMERA_DRIFT_RANGE:=40}"        # only chase action within this many tiles of the view centre
: "${CAMERA_LABEL_SECONDS:=12}"       # how long a player's camera label stays up
: "${CAMERA_HOLD_SECONDS:=40}"        # a viewer request holds the camera this long (sandboxed agents use the default)
: "${CAMERA_MIN_INTERVAL:=8}"        # seconds between camera moves, from any source
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
# Agents and Twitch chat.
: "${STATE_DIR:=$AGENT_SHARED_DIR/state}"         # status.json, games.jsonl, chat.json, viewer-relay.jsonl
: "${NOTES_DIR:=$AGENT_SHARED_DIR/notes}"         # the player agent's strategy notes and game log
: "${PLAYER_MODEL:=claude-sonnet-5-5}"          # the agent playing the game
: "${CHAT_MODEL:=claude-sonnet-5-5}"            # the agent answering Twitch chat
: "${TWITCH_CHANNEL:=globulation2}"
: "${TWITCH_BOT_USER:=}"                        # account the chat agent speaks as; empty = read-only
: "${TWITCH_CHAT_TOKEN_FILE:=$HOME/.config/glob2-stream/twitch-chat.token}"
: "${TWITCH_CLI_ENV:=$HOME/.config/twitch-cli/.twitch-cli.env}"   # Twitch CLI credentials used to refresh the chat token
: "${HIGHLIGHTS:=1}"                            # per-game stream titles, markers and clips (highlights.py)
: "${HIGHLIGHT_SWING:=25}"                      # clip when the win chance moves this many points in 3 min
: "${HIGHLIGHT_COOLDOWN:=600}"                  # seconds between swing clips
: "${LIVE_WATCH:=1}"                            # restart the encoder when Twitch shows the channel offline (highlights.py)
# Context compaction for the agents (env-vars docs: CLAUDE_CODE_AUTO_COMPACT_WINDOW, CLAUDE_AUTOCOMPACT_PCT_OVERRIDE).
# Aggressive by default: the smallest window and compaction at half of it (~50k tokens).
: "${AGENT_COMPACT_WINDOW:=100000}"
: "${AGENT_COMPACT_PCT:=50}"
: "${PLAYER_CALLS_PER_MIN:=10}"          # paced game calls per minute for the player (menus unpaced)
# Game settings forced in the stream profile at each launch (space-separated key=value, preferences.txt keys).
# glob2 #1919 turns chat off for a profile that has not declared an age (or is under 13), which
# silenced the player's narration on the first build from master (2026-11-27). The stream's profile is
# run by the channel owner, an adult, who approved declaring 13_plus (source self) on 2026-11-27.
# game-up.sh applies it with STREAM_GAME_PREFS; empty leaves the profile's own answer.
: "${GAME_AGE_BAND:=13_plus}"
: "${STREAM_GAME_PREFS:=clouds=0 cloudShadows=0}"
# Autostart at boot (autostart/install-autostart.sh).
: "${AUTOSTART_STREAM:=live}"          # live, none or file:PATH
: "${AUTOSTART_CHAT:=1}"
export GLOB2_STREAM_HOME MCP_PORT LOG_DIR
if [[ "$STREAM_DISPLAY_BACKEND" == xorg ]]; then export XAUTHORITY="$STREAM_XAUTHORITY"; fi
