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
# files it must not reach (and the player to create ./CLAUDE.md), then checks that those calls
# were refused and that the session's tools, MCP servers, plugins, skills, subagents and slash
# commands are exactly the expected ones. The egress checks connect as AGENT_USER directly and
# through the allowlist proxy. The direct file probes run commands as AGENT_USER
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
echo "Claude Code policy and extension points"
for f in player chat chat-nogame; do
  pf="$AGENT_INSTALL_DIR/policy/$f.json"
  [[ "$(stat -c '%U %a' "$pf" 2>/dev/null)" == "root 644" ]] && python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "$pf" 2>/dev/null \
    && ok "policy $f.json root-owned, valid" || bad "policy $f.json missing, not root-owned or invalid"
done
check "agent-run passes the role policy with --settings" grep -q 'POLICY / "player.json"' "$run"
agent_home="$(getent passwd "$AGENT_USER" | cut -d: -f6)"
[[ "$(sudo -n stat -c '%U:%G %a' "$agent_home/.claude" 2>/dev/null)" == "root:$AGENT_USER 1770" ]] && ok "$agent_home/.claude root:$AGENT_USER 1770" || bad "$agent_home/.claude is $(sudo -n stat -c '%U:%G %a' "$agent_home/.claude" 2>/dev/null)"
for d in plugins skills agents commands; do
  [[ "$(sudo -n stat -c '%U %a' "$agent_home/.claude/$d" 2>/dev/null)" == "root 755" && -z "$(sudo -n ls -A "$agent_home/.claude/$d" 2>/dev/null)" ]] \
    && ok "$agent_home/.claude/$d root-owned and empty" || bad "$agent_home/.claude/$d not root-owned and empty"
done
[[ "$(sudo -n stat -c '%U %s' "$agent_home/.claude/CLAUDE.md" 2>/dev/null)" == "root 0" ]] && ok "$agent_home/.claude/CLAUDE.md root-owned and empty" || bad "$agent_home/.claude/CLAUDE.md not root-owned and empty"

if [[ "$AGENT_EGRESS" == 1 ]]; then
  echo "network egress"
  check "glob2-agent-egress.service active" systemctl is-active --quiet glob2-agent-egress.service
  check "glob2-agent-proxy.service active" systemctl is-active --quiet glob2-agent-proxy.service
  check "nftables table inet glob2_agent loaded" sudo -n nft list table inet glob2_agent
fi

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
  refuse "cannot open the stream X display" as_agent env -i PATH=/usr/bin:/bin DISPLAY="$STREAM_DISPLAY" xdpyinfo
  [[ "$STREAM_DISPLAY_BACKEND" != xorg ]] || refuse "cannot read the stream X auth cookie" as_agent test -r "$STREAM_XAUTHORITY"
  if [[ "$AGENT_EGRESS" == 1 ]]; then
    tcp() { as_agent /usr/bin/python3 -I -c 'import socket,sys; socket.create_connection((sys.argv[1], int(sys.argv[2])), timeout=5)' "$@"; }
    connect_via_proxy() {  # prints the proxy's status code for CONNECT host:443
      as_agent /usr/bin/python3 -I -c '
import socket, sys
s = socket.create_connection(("127.0.0.1", int(sys.argv[1])), timeout=10)
s.sendall(f"CONNECT {sys.argv[2]}:443 HTTP/1.1\r\nHost: {sys.argv[2]}:443\r\n\r\n".encode())
print(s.recv(64).split()[1].decode())' "$EGRESS_PROXY_PORT" "$1" 2>/dev/null
    }
    refuse "cannot connect directly to 1.1.1.1:443" tcp 1.1.1.1 443
    refuse "cannot connect directly to api.anthropic.com:443" tcp api.anthropic.com 443
    refuse "cannot reach DNS" tcp 127.0.0.53 53
    check "can reach the game MCP port" tcp 127.0.0.1 "$MCP_PORT"
    [[ "$(connect_via_proxy example.com)" == 403 ]] && ok "proxy refuses example.com" || bad "proxy did not refuse example.com"
    [[ "$(connect_via_proxy api.anthropic.com)" == 200 ]] && ok "proxy tunnels to api.anthropic.com" || bad "proxy did not tunnel to api.anthropic.com"
  fi
  if [[ -f "$NOTES_DIR/session-brief.md" ]]; then
    refuse "cannot modify the session brief" as_agent sh -c ": >> '$NOTES_DIR/session-brief.md'"
    refuse "cannot delete or replace the session brief" as_agent mv "$NOTES_DIR/session-brief.md" "$NOTES_DIR/brief-probe"
  fi
else
  echo "  note  $operator has no general sudo: direct probes as $AGENT_USER skipped (the sudo rule allows only agent-run)"
fi

echo "camera gate (installed player and chat paths; nothing is moved)"
proxy="$AGENT_INSTALL_DIR/chat/readonly_mcp.py"
if [[ -r "$proxy" ]]; then
  if [[ "$(declare -F as_agent)" ]]; then run_proxy() { as_agent env -i PATH=/usr/bin:/bin MCP_PORT="$MCP_PORT" STATE_DIR="$STATE_DIR" OVERLAY_FILE="$OVERLAY_FILE" /usr/bin/python3 -E -s "$proxy"; }
  else run_proxy() { env -i PATH=/usr/bin:/bin MCP_PORT="$MCP_PORT" STATE_DIR="$STATE_DIR" OVERLAY_FILE="$OVERLAY_FILE" /usr/bin/python3 -E -s "$proxy"; }; fi
  out="$(printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' \
    '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' \
    '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"game_place","arguments":{"building":"inn","x":1,"y":1}}}' \
    '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"game_view","arguments":{"x":1,"y":1}}}' \
    '{"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"camera_show","arguments":{"x":1,"y":1,"zoom":2}}}' | run_proxy 2>&1)"
  tools="$(printf '%s\n' "$out" | python3 -c 'import json,sys
for l in sys.stdin:
    d=json.loads(l)
    if d.get("id")==2: print(",".join(sorted(t["name"] for t in d["result"]["tools"])))' 2>/dev/null)"
  [[ "$tools" == "camera_show,game_guide,game_stats,game_world,hive_api,hive_status,ui_inspect,ui_screenshot,ui_status" ]] &&
    ok "proxy lists only the read tools plus camera_show" || bad "proxy tools: ${tools:-$out}"
  [[ "$out" == *"game_place is not available"* && "$out" == *"game_view is not available"* ]] &&
    ok "proxy refuses game_place and raw game_view" || bad "proxy write refusal: ${out:0:200}"
  [[ "$out" == *"zoom above 1"* ]] && ok "camera_show refuses zoom above 100%" || bad "zoom refusal missing"
  tok="$(cat "$STATE_DIR/control-token" 2>/dev/null)"
  [[ -z "$tok" || "$out" != *"$tok"* ]] && ok "proxy output never contains the control token" || bad "control token leaked in proxy output"
  # The viewer-request hold blocks the player's camera moves. Checked against a throwaway state
  # dir with a hold and no token, so nothing moves on stream.
  holddir="$(mktemp -d)"; chmod 755 "$holddir"
  printf '{"until": %s, "label": "verify", "by": "verify"}' "$(( $(date +%s) + 60 ))" > "$holddir/camera-hold.json"
  chmod 644 "$holddir/camera-hold.json"
  hold_out="$(printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' \
    '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"camera_show","arguments":{"x":1,"y":1,"zoom":0.5}}}' \
    '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"camera_show","arguments":{"x":1,"y":1,"zoom":3}}}' |
    env -i PATH=/usr/bin:/bin STATE_DIR="$holddir" OVERLAY_FILE="$holddir/caption.txt" MCP_PORT=1 \
      /usr/bin/python3 -E -s "$AGENT_INSTALL_DIR/stream_ctl.py" mcp 2>&1)"
  rm -rf "$holddir"
  [[ "$hold_out" == *"showing a viewer request"* ]] && ok "a viewer-request hold blocks the player's camera moves" ||
    bad "hold didn't block the player: ${hold_out:0:200}"
  [[ "$hold_out" == *"zoom above 1"* ]] && ok "player camera_show refuses zoom above 100%" || bad "player zoom refusal missing"
  if [[ -f "$STATE_DIR/control-token" ]]; then
    [[ "$(stat -c '%a %G' "$STATE_DIR/control-token")" == "640 $AGENT_USER" ]] && ok "control token file 640, group $AGENT_USER" ||
      bad "control token file is $(stat -c '%a %G' "$STATE_DIR/control-token")"
  fi
  if [[ "$(declare -F as_agent)" ]]; then
    grep -q '"mcp__glob2-stream__game_view"' "$AGENT_INSTALL_DIR/policy/player.json" && ok "player policy denies game_view" || bad "player policy lacks the game_view deny"
    grep -q '"mcp__glob2-stream__game_wait"' "$AGENT_INSTALL_DIR/policy/player.json" && ok "player policy denies raw game_wait (capped match_wait instead)" || bad "player policy lacks the game_wait deny"
  fi
else
  echo "  note  $proxy not installed yet: run install-agent-sandbox.sh"
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
    if role == "player" and "mcp__glob2-stream__game_view" in tools:
        fails.append("player can call game_view directly (bypassing the camera gate)")
    if role == "player" and "mcp__stream-ctl__camera_show" not in tools and tools:
        fails.append("player lacks stream-ctl camera_show")
    foreign = [t for t in tools if t.startswith("mcp__") and t.split("__")[1] not in want]
    if foreign:
        fails.append(f"foreign MCP tools {foreign[:3]}")
    if init.get("cwd", "").startswith(home + "/"):
        fails.append("runs inside the operator home")
    plugins = sorted(p.get("name") for p in init.get("plugins", []))
    if plugins != ["cc-plugin-privacy"]:
        fails.append(f"plugins {plugins}")
    for key in ("agents", "skills", "slash_commands"):
        if init.get(key):
            fails.append(f"{key} {init.get(key)[:3]}")
if live == "1":
    if not result or result.get("is_error"):
        fails.append("live call failed: " + str((result or {}).get("result", "no result"))[:120])
    elif role == "player" and not (any(home in d for d in denied) and any(token in d for d in denied)):
        fails.append(f"reads were not refused (denials: {denied})")
    elif role == "player" and not any("CLAUDE.md" in d for d in denied):
        fails.append(f"writing ./CLAUDE.md was not refused (denials: {denied})")
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
    p_prompt="Permission test. Use the Read tool on $HOME/.bashrc, then on $token, then use the Write tool to create ./CLAUDE.md containing x. Use no other tools. Then reply DONE."
    r="$(model_check player "$p_prompt" "glob2-stream,stream-ctl" "Edit,Read,Write" "$live")"
    [[ "$r" == ok ]] && ok "player: tools, MCP servers, plugins, no skills/agents/commands$([[ $live == 1 ]] && echo ', refused reads and ./CLAUDE.md')" || bad "player: $r"
    r="$(model_check chat "Status check: reply with null and no suggestion." "glob2-readonly" "" "$live")"
    [[ "$r" == ok ]] && ok "chat: no built-in tools, only the read-only game proxy" || bad "chat: $r"
    [[ $dummy == 1 ]] && sudo -n rm -f "$token" && echo "  note  dummy token removed"
  else
    echo "  note  model checks skipped: install the Claude token, or use --dummy-token"
  fi
fi
echo "$passes passed, $fails failed"
[[ $fails == 0 ]]
