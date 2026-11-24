#!/usr/bin/env bash
# Install, update or remove the sandbox the Claude agents run in (README "Security and sandboxing").
#
#   sandbox/install-agent-sandbox.sh              install, or resync after `git pull` (idempotent)
#   sandbox/install-agent-sandbox.sh --uninstall  remove the sudo rule, install dir, config, token and
#                                                 agent user; keeps the shared notes and state
#
# Run it as the operator: the account that runs the supervisor. It uses sudo for the system
# changes. Settings come from lib.sh and stream.env: AGENT_USER, AGENT_INSTALL_DIR, AGENT_ETC_DIR,
# AGENT_SHARED_DIR, AGENT_SUDOERS, plus STATE_DIR, NOTES_DIR, OVERLAY_FILE and MCP_PORT.
#
# It does the following:
#   - creates a system user AGENT_USER with its own home, no login shell and no extra groups;
#   - installs a root-owned, read-only copy of the agent-side code and of `claude` in AGENT_INSTALL_DIR;
#   - writes AGENT_ETC_DIR/agent.env;
#   - creates the shared notes, state and overlay dirs (operator:AGENT_USER, 2770), moving the
#     data from the old per-user locations if they exist;
#   - installs one sudoers rule: the operator may run AGENT_INSTALL_DIR/agent-run as AGENT_USER,
#     and nothing else.
#
# The Claude token is never handled here: the user installs it (see README).
set -euo pipefail
here="$(dirname "$(readlink -f "$0")")"
# shellcheck source=../lib.sh
source "$here/../lib.sh"
operator="$(id -un)"
[[ "$operator" != root ]] || { echo "run as the operator account, not root" >&2; exit 2; }
[[ -n "$AGENT_USER" ]] || { echo "AGENT_USER is empty: the sandbox is disabled in stream.env" >&2; exit 2; }
[[ "$AGENT_USER" != "$operator" ]] || { echo "AGENT_USER must differ from the operator" >&2; exit 2; }
S() { sudo -n "$@"; }
S true 2>/dev/null || { echo "needs sudo for system changes (run 'sudo -v' first)" >&2; exit 2; }
agent_home="/var/lib/$AGENT_USER"

if [[ "${1:-}" == --uninstall ]]; then
  if id "$AGENT_USER" >/dev/null 2>&1 && pgrep -u "$AGENT_USER" >/dev/null; then
    echo "stopping $AGENT_USER processes"; S pkill -u "$AGENT_USER" || true; sleep 2; S pkill -9 -u "$AGENT_USER" || true
  fi
  S rm -f "$AGENT_SUDOERS" && echo "removed $AGENT_SUDOERS"
  S rm -rf "$AGENT_INSTALL_DIR" && echo "removed $AGENT_INSTALL_DIR"
  S rm -rf "$AGENT_ETC_DIR" && echo "removed $AGENT_ETC_DIR (agent.env and the Claude token)"
  if id "$AGENT_USER" >/dev/null 2>&1; then S userdel -r "$AGENT_USER" 2>/dev/null || S userdel "$AGENT_USER"; echo "removed user $AGENT_USER"; fi
  echo "kept $AGENT_SHARED_DIR (notes, state, overlay); remove it with: sudo rm -rf '$AGENT_SHARED_DIR'"
  echo "set AGENT_USER=\"\" in stream.env to run the agents unsandboxed, or reinstall"
  exit 0
fi
[[ -z "${1:-}" ]] || { sed -n 2,8p "$0"; exit 2; }

# --- the agent user ------------------------------------------------------------------------
if ! id "$AGENT_USER" >/dev/null 2>&1; then
  S useradd --system --user-group --home-dir "$agent_home" --create-home --shell /usr/sbin/nologin \
    --comment "Claude Plays Glob agents" "$AGENT_USER"
  echo "created user $AGENT_USER"
fi
agent_home="$(getent passwd "$AGENT_USER" | cut -d: -f6)"
S install -d -o "$AGENT_USER" -g "$AGENT_USER" -m 700 "$agent_home"
extra="$(id -nG "$AGENT_USER" | tr ' ' '\n' | grep -vx "$AGENT_USER" || true)"
[[ -z "$extra" ]] || { echo "refusing: $AGENT_USER is in extra groups: $extra" >&2; exit 1; }
home_mode="$(stat -c %a "$HOME")"
[[ "${home_mode: -1}" == 0 ]] || echo "warning: $HOME is mode $home_mode; other users can enter it. Consider: chmod o-rwx $HOME" >&2

# --- root-owned agent code and claude --------------------------------------------------------
claude_src="${CLAUDE_BIN:-$(readlink -f "$(command -v claude)")}"
[[ -x "$claude_src" ]] || { echo "no claude binary found (set CLAUDE_BIN)" >&2; exit 1; }
S install -d -o root -g root -m 755 "$AGENT_INSTALL_DIR" "$AGENT_INSTALL_DIR/bin" "$AGENT_INSTALL_DIR/chat" "$AGENT_INSTALL_DIR/prompts"
manifest=(stream_ctl.py rigstate.py rigconfig.py lib.sh caption.sh chat/readonly_mcp.py chat/reply_schema.json prompts/chat.md)
for f in "${manifest[@]}"; do
  mode=644; [[ "$f" == *.sh || "$f" == stream_ctl.py ]] && mode=755
  S install -o root -g root -m "$mode" "$RIG_DIR/$f" "$AGENT_INSTALL_DIR/$f"
done
tmp="$(mktemp)"; trap 'rm -f "$tmp"' EXIT
sed -e "s|@AGENT_INSTALL_DIR@|$AGENT_INSTALL_DIR|" -e "s|@AGENT_ETC_DIR@|$AGENT_ETC_DIR|" "$here/agent-run" > "$tmp"
S install -o root -g root -m 755 "$tmp" "$AGENT_INSTALL_DIR/agent-run"
if ! S cmp -s "$claude_src" "$AGENT_INSTALL_DIR/bin/claude"; then
  S install -o root -g root -m 755 "$claude_src" "$AGENT_INSTALL_DIR/bin/claude"
  echo "installed claude $("$AGENT_INSTALL_DIR/bin/claude" --version 2>/dev/null | head -1)"
fi
# Drop files that are no longer part of the manifest.
keep="$(printf '%s\n' agent-run bin/claude "${manifest[@]}")"
S find "$AGENT_INSTALL_DIR" -type f | sed "s|^$AGENT_INSTALL_DIR/||" | while read -r f; do
  grep -qxF "$f" <<<"$keep" || { S rm -f "$AGENT_INSTALL_DIR/$f"; echo "removed stale $f"; }
done

# --- shared data (operator and agent) -----------------------------------------------------------
shared_dirs=("$AGENT_SHARED_DIR" "$NOTES_DIR" "$STATE_DIR" "$(dirname "$OVERLAY_FILE")")
for d in "${shared_dirs[@]}"; do
  S install -d -o "$operator" -g "$AGENT_USER" -m 2770 "$d"
done
# An empty chat-sandbox (created by an earlier run) doesn't count as data when migrating.
[[ -d "$STATE_DIR/chat-sandbox" && -z "$(ls -A "$STATE_DIR/chat-sandbox")" ]] && rmdir "$STATE_DIR/chat-sandbox"
migrate() {  # old dir -> new dir, once, if the new one is empty
  local old="$1" new="$2"
  [[ -d "$old" && "$(readlink -f "$old")" != "$(readlink -f "$new")" ]] || return 0
  if [[ -z "$(ls -A "$new")" && -n "$(ls -A "$old")" ]]; then
    cp -a "$old/." "$new/" && mv "$old" "$old.migrated-$(date +%Y%m%d)" && echo "moved $old to $new"
  fi
}
migrate "$GLOB2_STREAM_HOME/notes" "$NOTES_DIR"
migrate "$GLOB2_STREAM_HOME/state" "$STATE_DIR"
S install -d -o "$operator" -g "$AGENT_USER" -m 2770 "$STATE_DIR/chat-sandbox"   # after migrating state
shared_dirs+=("$STATE_DIR/chat-sandbox")
old_caption="$GLOB2_STREAM_HOME/overlay/caption.txt"
[[ -f "$old_caption" && ! -e "$OVERLAY_FILE" && "$old_caption" != "$OVERLAY_FILE" ]] && cp "$old_caption" "$OVERLAY_FILE"
for d in "${shared_dirs[@]}"; do  # both sides may read and replace everything here
  S chgrp -R "$AGENT_USER" "$d"
  S find "$d" -type d -exec chmod 2770 {} +
  S find "$d" -type f -exec chmod ug+rw,o=r {} +   # o=r: the 2770 dirs already keep other users out
done
# Notes: sticky bit, so the agent can't delete or replace operator-owned files there, and the
# session brief (the player's rules, written 0644 by the supervisor) stays read-only to it.
S chmod 3770 "$NOTES_DIR"
[[ -f "$NOTES_DIR/session-brief.md" ]] && S chown "$operator" "$NOTES_DIR/session-brief.md" && S chmod 644 "$NOTES_DIR/session-brief.md"
for v in STATE_DIR NOTES_DIR OVERLAY_FILE; do
  case "${!v}" in "$AGENT_SHARED_DIR"/*) ;; *) echo "warning: $v=${!v} is outside $AGENT_SHARED_DIR (check stream.env)" >&2 ;; esac
done

# --- agent config and token location ------------------------------------------------------------
S install -d -o root -g "$AGENT_USER" -m 750 "$AGENT_ETC_DIR"
cat > "$tmp" <<EOF
# Written by install-agent-sandbox.sh; rerun it after changing these settings.
AGENT_USER=$AGENT_USER
AGENT_SHARED_DIR=$AGENT_SHARED_DIR
STATE_DIR=$STATE_DIR
NOTES_DIR=$NOTES_DIR
OVERLAY_FILE=$OVERLAY_FILE
MCP_PORT=$MCP_PORT
EOF
S install -o root -g "$AGENT_USER" -m 640 "$tmp" "$AGENT_ETC_DIR/agent.env"
token="$AGENT_ETC_DIR/claude-oauth-token"
if S test -s "$token"; then
  S chown root:"$AGENT_USER" "$token"; S chmod 640 "$token"; token_state="installed"
else
  token_state="missing"
fi

# --- the sudo rule --------------------------------------------------------------------------------
cat > "$tmp" <<EOF
# Written by install-agent-sandbox.sh: $operator may start sandboxed agents as $AGENT_USER, nothing else.
Defaults!$AGENT_INSTALL_DIR/agent-run !use_pty, !requiretty, env_reset
$operator ALL=($AGENT_USER) NOPASSWD: $AGENT_INSTALL_DIR/agent-run
EOF
S visudo -cqf "$tmp" || { echo "generated sudoers rule failed visudo" >&2; exit 1; }
S install -o root -g root -m 440 "$tmp" "$AGENT_SUDOERS"
S visudo -cq

echo "sandbox ready: user $AGENT_USER, code $AGENT_INSTALL_DIR, shared $AGENT_SHARED_DIR, rule $AGENT_SUDOERS"
if [[ "$token_state" == missing ]]; then
  cat <<EOF
Claude token not installed yet. As $operator, run:
  claude setup-token
and copy the token it prints, then:
  sudo install -o root -g $AGENT_USER -m 640 /dev/stdin $token
paste the token, press Enter and Ctrl-D. Then check everything with sandbox/verify-sandbox.sh.
EOF
fi
