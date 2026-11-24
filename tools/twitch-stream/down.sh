#!/usr/bin/env bash
# Stop the supervisor, the stream, the stream game, Xvfb and the audio sink. Processes are stopped by
# recorded PID or exact command line, never by a loose pattern that could match a shell.
source "$(dirname "$(readlink -f "$0")")/lib.sh"
# The supervisor first, so it doesn't restart what is stopped below; it ends its own children.
if [[ -s "$LOG_DIR/supervisor.pid" ]] && kill "$(cat "$LOG_DIR/supervisor.pid")" 2>/dev/null; then
  for _ in $(seq 60); do kill -0 "$(cat "$LOG_DIR/supervisor.pid" 2>/dev/null)" 2>/dev/null || break; sleep 0.5; done
  echo "stopped supervisor"
fi
for f in stream game; do
  [[ -s "$LOG_DIR/$f.pid" ]] && kill "$(cat "$LOG_DIR/$f.pid")" 2>/dev/null && echo "stopped $f"
  rm -f "$LOG_DIR/$f.pid"
done
[[ "$STREAM_DISPLAY_BACKEND" == xorg ]] || { pkill -x -f "Xvfb $STREAM_DISPLAY .*" && echo "stopped Xvfb"; }   # the xorg backend is a system service
id=$(pactl list short modules | awk -v s="sink_name=$STREAM_SINK" '$0 ~ s {print $1}')
[[ -n "$id" ]] && pactl unload-module "$id" && echo "removed sink $STREAM_SINK"
true
