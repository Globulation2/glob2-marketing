#!/usr/bin/env bash
# Stop the stream, the stream game, Xvfb and the audio sink. Processes are stopped by
# recorded PID or exact command line, never by a loose pattern that could match a shell.
source "$(dirname "$(readlink -f "$0")")/lib.sh"
for f in stream game; do
  [[ -s "$LOG_DIR/$f.pid" ]] && kill "$(cat "$LOG_DIR/$f.pid")" 2>/dev/null && echo "stopped $f"
  rm -f "$LOG_DIR/$f.pid"
done
pkill -x -f "Xvfb $STREAM_DISPLAY .*" && echo "stopped Xvfb"
id=$(pactl list short modules | awk -v s="sink_name=$STREAM_SINK" '$0 ~ s {print $1}')
[[ -n "$id" ]] && pactl unload-module "$id" && echo "removed sink $STREAM_SINK"
true
