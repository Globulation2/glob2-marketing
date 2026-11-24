#!/usr/bin/env bash
# Set the on-stream caption; ffmpeg's drawtext reloads it within a second. Usage: caption.sh "text"
source "$(dirname "$(readlink -f "$0")")/lib.sh"
mkdir -p "$(dirname "$OVERLAY_FILE")"
tmp="$OVERLAY_FILE.tmp"; printf '%s' "$*" > "$tmp" && mv "$tmp" "$OVERLAY_FILE"
