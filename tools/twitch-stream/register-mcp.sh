#!/usr/bin/env bash
# Register the stream game as Claude Code's user-scope MCP server "glob2-stream".
# The server reuses a game already listening on MCP_PORT (game-up.sh), or starts one
# on the stream display with the same audio and profile settings.
set -euo pipefail
source "$(dirname "$(readlink -f "$0")")/lib.sh"
name="${1:-glob2-stream}"
[[ -f "$GLOB2_SRC/tools/mcp_stdio.py" ]] || { echo "No glob2 checkout at $GLOB2_SRC" >&2; exit 1; }
claude mcp remove --scope user "$name" >/dev/null 2>&1 || true
claude mcp add --scope user "$name" \
  -e DISPLAY="$STREAM_DISPLAY" -e SDL_AUDIO_DRIVER=pulseaudio -e PULSE_SINK="$STREAM_SINK" -e GLOB2_USER_DIR="$GAME_PROFILE" \
  -- python3 "$GLOB2_SRC/tools/mcp_stdio.py" --executable "$GLOB2_BIN" --cwd "$GLOB2_SRC" \
  --url "http://127.0.0.1:$MCP_PORT/mcp" -- play --renderer "$GAME_RENDERER" --window-size "$STREAM_SIZE"
echo "registered $name; start a new Claude Code session to load its tools"
