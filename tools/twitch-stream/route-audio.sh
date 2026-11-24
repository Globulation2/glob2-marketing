#!/usr/bin/env bash
# Move audio from every process running on the stream display onto the stream sink.
# PipeWire remembers per-application routing ("glob2" -> speakers), so a new game
# stream can land on the speakers even with PULSE_SINK set. Other displays are untouched.
source "$(dirname "$(readlink -f "$0")")/lib.sh"
pactl list sink-inputs | awk '/^Sink Input #/{id=substr($3,2)} /application.process.id/{gsub(/"/,"",$3); print id, $3}' |
while read -r id pid; do
  tr '\0' '\n' < "/proc/$pid/environ" 2>/dev/null | grep -qx "DISPLAY=$STREAM_DISPLAY" || continue
  pactl move-sink-input "$id" "$STREAM_SINK" && echo "routed audio of pid $pid to $STREAM_SINK"
done
true
