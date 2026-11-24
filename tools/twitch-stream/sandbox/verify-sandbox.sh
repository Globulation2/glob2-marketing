#!/usr/bin/env bash
# Check the agent sandbox (README "Security and sandboxing"). Rerun after installing or updating.
#
#   sandbox/verify-sandbox.sh                 install checks; plus live model checks if the Claude token exists
#   sandbox/verify-sandbox.sh --dummy-token   without a real token: install a dummy one for the run, start
#                                             both roles and check their tools and MCP servers up to the
#                                             (expected) login failure, then remove it
#   sandbox/verify-sandbox.sh --no-model      install and permission checks only (no Claude calls)
#
# The live model checks start one cheap call per role (claude-haiku-5-5). Each asks Claude to read
# files it must not reach, then checks that the reads were refused and that the session's tools
# and MCP servers are exactly the expected ones. The direct file probes run commands as AGENT_USER
# with the operator's own sudo rights; without general sudo, they are skipped.
# shellcheck disable=SC2015,SC2016  # ok() always succeeds; the literal $(id) is a deliberate bad value
set -uo pipefail
here="$(dirname "$(readlink -f "$0")")"
# shellcheck source=../lib.sh
source "$here/../lib.sh"
operator="$(id -un)"
mode="${1:-}"
fails=0; passes=0
ok()   { echo "  ok    $*"; passes=$((passes + 1)); }
bad()  { echo "  FAIL  $*"; fails=$((fails + 1)); }
check() { local what="$1"; shift; if "$@" >/dev/null 2>&1; then ok "$what"; else bad "$what"; fi; }
refuse() { local what="$1"; shift; if "$@" >/dev/null 2>&1; then bad "$what"; else ok "$what"; fi; }
[[ -n "$AGENT_USER" ]] || { echo "AGENT_USER is empty: the sandbox is disabled"; exit 1; }
run="$AGENT_INSTALL_DIR/agent-run"
token="$AGENT_ETC_DIR/claude-oauth-token"

echo "agent user and files"
check "user $AGENT_USER exists" id "$AGENT_USER"
[[ "$(id -nG "$AGENT_USER" 2>/dev/null)" == "$AGENT_USER" ]] && ok "$AGENT_USER is in no other groups" || bad "$AGENT_USER groups: $(id -nG "$AGENT_USER" 2>/dev/null)"
shell="$(getent passwd "$AGENT_USER" | cut -d: -f7)"
[[ "$shell" == */nologin || "$shell" == /bin/false ]] && ok "no login shell ($shell)" || bad "login shell $shell"
[[ "$(stat -c %a "$HOME")" =~ 0$ ]] && ok "$HOME closed to other users ($(stat -c %a "$HOME"))" || bad "$HOME is mode $(stat -c %a "$HOME")"
[[ "$(stat -c %U "$AGENT_INSTALL_DIR")" == root ]] && ok "$AGENT_INSTALL_DIR owned by root" || bad "$AGENT_INSTALL_DIR owner"
writable="$(sudo -n find "$AGENT_INSTALL_DIR" \( ! -user root -o -perm /022 \) -print 2>/dev/null | head -3)"
[[ -z "$writable" ]] && ok "install dir: every file root-owned, not group/other writable" || bad "writable or foreign-owned: $writable"
refuse "agent-run has no unreplaced placeholders" grep -q '@AGENT_' "$run"
[[ "$(sudo -n stat -c '%U:%G %a' "$AGENT_ETC_DIR" 2>/dev/null)" == "root:$AGENT_USER 750" ]] && ok "$AGENT_ETC_DIR root:$AGENT_USER 750" || bad "$AGENT_ETC_DIR perms"
if sudo -n test -s "$token"; then
  [[ "$(sudo -n stat -c '%U:%G %a' "$token")" == "root:$AGENT_USER 640" ]] && ok "Claude token root:$AGENT_USER 640" || bad "token perms $(sudo -n stat -c '%U:%G %a' "$token")"
  have_token=1
else
  echo "  note  no Claude token at $token yet"; have_token=0
fi
for d in "$AGENT_SHARED_DIR" "$NOTES_DIR" "$STATE_DIR" "$(dirname "$OVERLAY_FILE")"; do
  want=2770; [[ "$d" == "$NOTES_DIR" ]] && want=3770   # notes: sticky, so the session brief stays read-only
  [[ "$(stat -c '%U:%G %a' "$d" 2>/dev/null)" == "$operator:$AGENT_USER $want" ]] && ok "shared $d" || bad "shared $d is $(stat -c '%U:%G %a' "$d" 2>/dev/null), want $want"
done
check "sudoers valid" sudo -n visudo -cq
rule="$(sudo -n grep -v '^#' "$AGENT_SUDOERS" 2>/dev/null | grep -v '^Defaults' | grep -v '^$')"
[[ "$rule" == "$operator ALL=($AGENT_USER) NOPASSWD: $run" ]] && ok "sudo rule allows only agent-run as $AGENT_USER" || bad "unexpected sudo rule: $rule"

echo "agent-run argument allowlist (through the sudo rule)"
reject() { local what="$1"; shift; local out; out="$(sudo -n -u "$AGENT_USER" "$run" "$@" </dev/null 2>&1)"; [[ $? -eq 64 && "$out" == agent-run:* ]] && ok "$what" || bad "$what: ${out:0:120}"; }
reject "rejects --tools Bash" chat --model claude-haiku-5-5 --tools Bash
reject "rejects --mcp-config" player --model claude-haiku-5-5 --mcp-config '{}'
reject "rejects --dangerously-skip-permissions" player --model claude-haiku-5-5 --dangerously-skip-permissions
reject "rejects an unknown role" shell --model claude-haiku-5-5
reject "rejects a bad model value" player --model '$(id)'
reject "rejects a bad --resume value" player --model claude-haiku-5-5 --resume ../../etc
reject "rejects chat-only options for the player" player --model claude-haiku-5-5 --no-game
# Run directly (not via sudo -u): refused either by the user check (77) or because the operator
# can't even read the agent config (78, permission denied).
out="$("$run" player --model claude-haiku-5-5 </dev/null 2>&1)"; rc=$?
{ [[ $rc -eq 77 ]] || { [[ $rc -eq 78 ]] && [[ "$out" == *"Permission denied"* ]]; }; } && ok "refuses to run as $operator directly" || bad "direct run: ${out:0:100}"

if [[ "$(sudo -n -l 2>/dev/null)" == *"(ALL : ALL) NOPASSWD: ALL"* || "$(sudo -n -l 2>/dev/null)" == *"(ALL) NOPASSWD: ALL"* ]]; then
  echo "direct probes as $AGENT_USER (using $operator's general sudo; the agents themselves have no shell)"
  as_agent() { sudo -n -u "$AGENT_USER" -- "$@"; }
  for f in "$HOME/.bashrc" "$HOME/.ssh" "$HOME/.config/glob2-stream" "$HOME/.config/twitch-cli" "$HOME/.config/gh" \
           "$HOME/.config/gcloud" "$HOME/.claude/.credentials.json" "$HOME/.claude.json" "$GLOB2_STREAM_HOME/stream.env" "$GLOB2_SRC"; do
    refuse "cannot read $f" as_agent test -r "$f"
  done
  refuse "cannot list $HOME" as_agent ls "$HOME"
  refuse "cannot write $AGENT_INSTALL_DIR" as_agent touch "$AGENT_INSTALL_DIR/probe"
  refuse "cannot write $AGENT_ETC_DIR" as_agent touch "$AGENT_ETC_DIR/probe"
  refuse "cannot use sudo itself" as_agent sudo -n true
  check "can write the overlay dir" as_agent test -w "$(dirname "$OVERLAY_FILE")"
  check "can write notes" as_agent test -w "$NOTES_DIR"
  check "can write state" as_agent test -w "$STATE_DIR"
  if [[ -f "$NOTES_DIR/session-brief.md" ]]; then
    refuse "cannot modify the session brief" as_agent sh -c ": >> '$NOTES_DIR/session-brief.md'"
    refuse "cannot delete or replace the session brief" as_agent mv "$NOTES_DIR/session-brief.md" "$NOTES_DIR/brief-probe"
  fi
else
  echo "  note  $operator has no general sudo: direct probes as $AGENT_USER skipped (the sudo rule allows only agent-run)"
fi

MODEL_CHECK_PY='
import json, sys
role, servers, builtins, live, home, token = sys.argv[1:7]
init = result = None
denied = []
for line in sys.stdin:
    try:
        ev = json.loads(line)
    except ValueError:
        continue
    if ev.get("type") == "system" and ev.get("subtype") == "init":
        init = ev
    if ev.get("type") == "result":
        result = ev
        denied = [str(d.get("tool_input", {})) for d in ev.get("permission_denials", [])]
fails = []
want = sorted(filter(None, servers.split(",")))
if not init:
    fails.append("no init event (claude did not start)")
else:
    names = sorted(s["name"] for s in init.get("mcp_servers", []))
    if names != want:
        fails.append(f"mcp servers {names}")
    tools = init.get("tools", [])
    plain = sorted(t for t in tools if not t.startswith("mcp__") and t != "StructuredOutput")
    if plain != sorted(filter(None, builtins.split(","))):
        fails.append(f"built-in tools {plain}")
    foreign = [t for t in tools if t.startswith("mcp__") and t.split("__")[1] not in want]
    if foreign:
        fails.append(f"foreign MCP tools {foreign[:3]}")
    if init.get("cwd", "").startswith(home + "/"):
        fails.append("runs inside the operator home")
if live == "1":
    if not result or result.get("is_error"):
        fails.append("live call failed: " + str((result or {}).get("result", "no result"))[:120])
    elif role == "player" and not (any(home in d for d in denied) and any(token in d for d in denied)):
        fails.append(f"reads were not refused (denials: {denied})")
elif result and not result.get("is_error"):
    fails.append("dummy token unexpectedly worked")
print("; ".join(fails) if fails else "ok")
'
model_check() {  # role, prompt, expected MCP servers, expected built-in tools, live (1) or dummy token (0)
  local role="$1" prompt="$2" servers="$3" builtins="$4" live="$5" extra=()
  [[ "$role" == chat ]] && extra=(--max-budget-usd 0.10 --max-game-calls 1)
  printf '%s' "$prompt" | timeout 180 sudo -n -u "$AGENT_USER" "$run" "$role" --model claude-haiku-5-5 "${extra[@]}" 2>&1 |
    python3 -c "$MODEL_CHECK_PY" "$role" "$servers" "$builtins" "$live" "$HOME" "$token"
}

if [[ "$mode" != --no-model ]]; then
  dummy=0
  if [[ $have_token == 0 && "$mode" == --dummy-token ]]; then
    printf 'sk-ant-oat01-verify-sandbox-dummy\n' | sudo -n install -o root -g "$AGENT_USER" -m 640 /dev/stdin "$token" && dummy=1
  fi
  if [[ $have_token == 1 || $dummy == 1 ]]; then
    live=$((1 - dummy))
    echo "model checks ($([[ $live == 1 ]] && echo "live, claude-haiku-5-5" || echo "dummy token: start-up only, login must fail"))"
    p_prompt="Permission test. Use the Read tool on $HOME/.bashrc, then on $token. Use no other tools. Then reply DONE."
    r="$(model_check player "$p_prompt" "glob2-stream,stream-ctl" "Edit,Read,Write" "$live")"
    [[ "$r" == ok ]] && ok "player: tools, MCP servers$([[ $live == 1 ]] && echo ', refused reads')" || bad "player: $r"
    r="$(model_check chat "Status check: reply with null and no suggestion." "glob2-readonly" "" "$live")"
    [[ "$r" == ok ]] && ok "chat: no built-in tools, only the read-only game proxy" || bad "chat: $r"
    [[ $dummy == 1 ]] && sudo -n rm -f "$token" && echo "  note  dummy token removed"
  else
    echo "  note  model checks skipped: install the Claude token, or use --dummy-token"
  fi
fi
echo "$passes passed, $fails failed"
[[ $fails == 0 ]]
