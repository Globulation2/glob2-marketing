#!/usr/bin/env bash
# Start Claude Plays Glob automatically at boot, without anyone logged in.
#
#   autostart/install-autostart.sh              install or update the user service (idempotent)
#   autostart/install-autostart.sh --uninstall  disable and remove it
#
# Installs the systemd *user* service glob2-stream.service for the operator, which runs
# supervisor.py (game, stream, player, chat) and restarts it if it exits. Lingering is enabled
# so the operator's user manager, PipeWire and this service start at boot. The system services
# it relies on (glob2-stream-xorg, glob2-agent-egress, glob2-agent-proxy) come from
# display/install-xorg-display.sh and sandbox/install-agent-sandbox.sh and are enabled there.
# Settings: AUTOSTART_STREAM (live, none or file:PATH; default live) and AUTOSTART_CHAT (1/0).
# Going live at every boot is a standing decision: install with AUTOSTART_STREAM=live only when
# the channel owner wants an always-on stream.
set -euo pipefail
here="$(dirname "$(readlink -f "$0")")"
# shellcheck source=../lib.sh
source "$here/../lib.sh"
unit=glob2-stream.service
hl_unit=glob2-stream-highlights.service   # per-game titles, markers and clips (highlights.py)
ar_unit=glob2-stream-archive               # .service + .timer: keep every player transcript (archive-transcripts.sh)
unit_dir="$HOME/.config/systemd/user"

if [[ "${1:-}" == --uninstall ]]; then
  systemctl --user disable --now "$unit" "$hl_unit" "$ar_unit.timer" 2>/dev/null || true
  rm -f "$unit_dir/$unit" "$unit_dir/$hl_unit" "$unit_dir/$ar_unit.service" "$unit_dir/$ar_unit.timer"; systemctl --user daemon-reload
  echo "removed $unit and $hl_unit (lingering left as it was)"; exit 0
fi
[[ -z "${1:-}" ]] || { sed -n 2,5p "$0"; exit 2; }

if [[ "$(loginctl show-user "$(id -un)" -p Linger --value 2>/dev/null)" != yes ]]; then
  sudo -n loginctl enable-linger "$(id -un)" && echo "enabled lingering for $(id -un)"
fi
args=(run --stream "$AUTOSTART_STREAM")
[[ "$AUTOSTART_STREAM" == live ]] && args+=(--i-mean-it)
[[ "$AUTOSTART_CHAT" == 1 ]] && args+=(--chat)
mkdir -p "$unit_dir" "$LOG_DIR"
cat > "$unit_dir/$unit" <<UNIT
# Written by autostart/install-autostart.sh.
[Unit]
Description=Claude Plays Glob: supervisor (game, stream, player and chat agents)
After=pipewire.service pipewire-pulse.service wireplumber.service
Wants=pipewire-pulse.socket

[Service]
Type=simple
WorkingDirectory=$RIG_DIR
Environment=PATH=$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin
ExecStartPre=$RIG_DIR/autostart/wait-ready.sh
ExecStart=/usr/bin/python3 $RIG_DIR/supervisor.py ${args[*]}
Restart=always
RestartSec=20
# Only the supervisor gets the stop signal; it ends the stream, chat and player itself and leaves
# the game running, so a service restart doesn't throw away the match.
KillMode=process
TimeoutStopSec=90
StandardOutput=append:$LOG_DIR/supervisor-console.log
StandardError=append:$LOG_DIR/supervisor-console.log

[Install]
WantedBy=default.target
UNIT
if [[ "$AUTOSTART_STREAM" == live && "$HIGHLIGHTS" == 1 ]]; then
  # Separate from the supervisor so it can be updated without ending the broadcast.
  cat > "$unit_dir/$hl_unit" <<UNIT
# Written by autostart/install-autostart.sh.
[Unit]
Description=Claude Plays Glob: per-game Twitch titles, markers and clips
After=$unit

[Service]
Type=simple
WorkingDirectory=$RIG_DIR
ExecStart=/usr/bin/python3 $RIG_DIR/highlights.py run
Restart=always
RestartSec=30
StandardOutput=append:$LOG_DIR/highlights-console.log
StandardError=append:$LOG_DIR/highlights-console.log

[Install]
WantedBy=default.target
UNIT
else
  systemctl --user disable --now "$hl_unit" 2>/dev/null || true
  rm -f "$unit_dir/$hl_unit"
fi
# Transcript archive for analysis/: hard links past the supervisor's 100-transcript rotation.
cat > "$unit_dir/$ar_unit.service" <<UNIT
# Written by autostart/install-autostart.sh.
[Unit]
Description=Claude Plays Glob: archive player transcripts for analysis

[Service]
Type=oneshot
ExecStart=$RIG_DIR/autostart/archive-transcripts.sh
UNIT
cat > "$unit_dir/$ar_unit.timer" <<UNIT
# Written by autostart/install-autostart.sh.
[Unit]
Description=Claude Plays Glob: archive player transcripts every 10 minutes

[Timer]
OnBootSec=2min
OnUnitActiveSec=10min

[Install]
WantedBy=timers.target
UNIT
systemctl --user daemon-reload
systemctl --user enable "$unit" >/dev/null 2>&1
systemctl --user enable --now "$ar_unit.timer" >/dev/null 2>&1 && echo "installed $ar_unit.timer"
[[ -f "$unit_dir/$hl_unit" ]] && systemctl --user enable --now "$hl_unit" >/dev/null 2>&1 && echo "installed $hl_unit (running)"
echo "installed $unit: supervisor.py ${args[*]}"
echo "start now with: systemctl --user restart $unit  (stop any hand-started supervisor first)"
