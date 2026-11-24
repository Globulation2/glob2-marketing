#!/usr/bin/env bash
# Start the virtual display, the game-audio sink and (unless --no-game) the game with MCP enabled.
set -euo pipefail
source "$(dirname "$(readlink -f "$0")")/lib.sh"
mkdir -p "$LOG_DIR" "$GAME_PROFILE"
if ! xdpyinfo -display "$STREAM_DISPLAY" >/dev/null 2>&1; then
  setsid Xvfb "$STREAM_DISPLAY" -screen 0 "${STREAM_SIZE}x24" -nolisten tcp >"$LOG_DIR/xvfb.log" 2>&1 < /dev/null &
  for _ in $(seq 50); do xdpyinfo -display "$STREAM_DISPLAY" >/dev/null 2>&1 && break; sleep 0.1; done
  echo "Xvfb $STREAM_DISPLAY up"
fi
if ! pactl list short sinks | awk '{print $2}' | grep -qx "$STREAM_SINK"; then
  pactl load-module module-null-sink sink_name="$STREAM_SINK" sink_properties=device.description=Glob2Stream >/dev/null
  echo "audio sink $STREAM_SINK created"
fi
[[ "${1:-}" == "--no-game" ]] && exit 0
if curl -s -o /dev/null --max-time 1 "http://127.0.0.1:$MCP_PORT/mcp"; then
  echo "game already listening on MCP port $MCP_PORT"; exit 0
fi
[[ -x "$GLOB2_BIN" ]] || { echo "No game binary at $GLOB2_BIN (see setup.sh --with-game)" >&2; exit 1; }
cd "$GLOB2_SRC"
# SDL3 ignores PULSE_SINK on its PipeWire backend; the Pulse backend honours it, and
# route-audio.sh catches PipeWire's remembered per-application routing.
DISPLAY="$STREAM_DISPLAY" SDL_AUDIO_DRIVER=pulseaudio PULSE_SINK="$STREAM_SINK" GLOB2_USER_DIR="$GAME_PROFILE" \
  setsid "$GLOB2_BIN" play --mcp-port "$MCP_PORT" --renderer "$GAME_RENDERER" --window-size "$STREAM_SIZE" \
  >"$LOG_DIR/game.log" 2>&1 < /dev/null &
echo $! > "$LOG_DIR/game.pid"
for _ in $(seq 60); do
  if curl -s -o /dev/null --max-time 1 "http://127.0.0.1:$MCP_PORT/mcp"; then
    sleep 2; "$RIG_DIR/route-audio.sh"
    echo "game up (pid $(cat "$LOG_DIR/game.pid")), MCP on $MCP_PORT"; exit 0
  fi
  sleep 0.5
done
echo "game did not open MCP port; see $LOG_DIR/game.log" >&2; exit 1
