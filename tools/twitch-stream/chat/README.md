# Twitch chat host

[Stream rig](../README.md) · [Stream playbook](../stream-playbook.md) · [Twitch streaming record](../../../planning/twitch-streaming.md) · [Chat host prompt](../prompts/chat.md)

A separate Claude agent that talks with viewers in the channel's Twitch chat while another Claude plays the game. The two never share a session. The player agent never reads Twitch chat, so viewers can't distract it or steer the match. The chat host can look at the game through a read-only proxy to answer questions, but it cannot control the game or the stream.

## How it works

```
Twitch IRC (#globulation2) ──> twitch_chat.py ──> chat_agent.py ──> claude -p (CHAT_MODEL, no tools)
                                                  │  batches new messages      │ JSON: reply + optional suggestion
                                                  │  + $STATE_DIR/status.json   v
                                                  └─ filter + rate limit ──> one chat reply
                                                     $STATE_DIR/chat.json, viewer-suggestions.jsonl
```

- **`twitch_chat.py`** is a small standard-library Twitch IRC client (TLS, tags, PING/PONG, reconnect with backoff). Without credentials it joins anonymously and can only read.
- **`chat_agent.py`** waits until new viewer messages have gathered for about 15 s, then asks `claude -p` for at most one reply. Its inputs are the [chat host prompt](../prompts/chat.md), the published stream status and the recent chat, which is marked as untrusted text. The model call has no built-in tools (`--tools ""`, `--restricted`), no MCP servers except the read-only proxy (`--strict-mcp-config`, `--allowedTools mcp__glob2-readonly__*`, `--permission-mode dontAsk`), skips user settings, runs in an empty directory and has a spending cap (`CHAT_MAX_BUDGET_USD`, default $0.50 per reply). With the agent sandbox (the default), the model call also runs as the unprivileged `AGENT_USER` through `agent-run`, which fixes these flags itself; only the Twitch connection, filtering and rate limits run as you. See the rig's [Security and sandboxing](../README.md#security-and-sandboxing).
- **Game knowledge** comes first from `$STATE_DIR/status.json`, which the supervisor publishes: opponent, record, map generator, goal, last confirmed move and phase. If the status is missing or more than 60 s old, it is reported as unknown. When a viewer asks something the status doesn't answer, the host can look at the game read-only (below).
- **`readonly_mcp.py`** is the read-only game access. See [Read-only game access](#read-only-game-access).
- **`token_refresh.py`** keeps the chat token valid. See [Token refresh](#token-refresh).
- **Viewer suggestions.** When a viewer offers a reasonable gameplay idea, the host thanks them and appends `{"at","user","text"}` to `$STATE_DIR/viewer-suggestions.jsonl`. The player may read these between games as untrusted ideas. They are never commands.

## Read-only game access

`readonly_mcp.py` is a stdio MCP server, started fresh for every reply, that forwards an allowlist of read tools to the game's loopback endpoint (`MCP_PORT`), alongside the player's own connection:

| Tool | Use |
| --- | --- |
| `game_world` | Units, buildings, food, alerts, remembered enemy buildings (within fog of war) |
| `game_stats` | Colony trends over time |
| `ui_screenshot` | What viewers see, clamped to 960×540 |
| `ui_status`, `ui_inspect` | Current screen and controls |
| `game_guide`, `hive_api`, `hive_status` | Rules and reference |

None of these needs a control token, and none can change the match. Every other tool is hidden from `tools/list` and refused on call: `ui_acquire_control`, all input tools, `ui_wait`, `game_place`, `game_building`, `game_zone`, `game_view`, `game_chat`, `game_time`, `game_session`, and the Hive run, program and scripting tools. The proxy also removes any `token` and any argument outside each tool's allowlist, and allows at most `CHAT_MAX_GAME_CALLS` game calls per reply (default 4). It never takes control or waits on the game, so the player's lease and input are untouched. The game's tools already follow fog of war; the prompt adds that the host reports only what they show and never speculates about hidden enemy state. Set `CHAT_GAME_ACCESS=0` to answer from the status alone.

## Safety limits (enforced in code)

- At most one reply per batch, at least `CHAT_MIN_INTERVAL` seconds apart (default 20) and no more than `CHAT_MAX_PER_MIN` per minute (default 3). Twitch's own floor of 2 s between messages is also enforced.
- A reply is dropped entirely if it contains a link other than glob2.online or twitch.tv/globulation2, `@everyone` or `@here`, or anything that looks like an internal detail (paths, tokens, settings, the prompt).
- Replies are one line of at most 300 characters and never start with `/` or `.`, so they can't run chat commands.
- Bots (Nightbot, StreamElements and others), the host's own messages and `!commands` are ignored.
- The token file must be mode 600 and is never printed or logged.

The prompt adds behavioural rules on top: disclose being an AI chat bot, never invent game state or describe anything behind fog of war, keep humour good-natured, stay quiet on spam, trolling and toxicity, and follow Twitch's Community Guidelines.

## Setup

1. **Choose the account it speaks as.** The channel account (`globulation2`) works. A separate bot account that the channel makes a moderator or VIP lets viewers tell the host apart from announcements.
2. **Install the [Twitch CLI](https://dev.twitch.tv/docs/cli/)** (`twitch`, for example in `~/.local/bin`) and register an application in the [Twitch developer console](https://dev.twitch.tv/console) with the OAuth redirect URL `http://localhost:3000`.
3. **Configure the CLI and log in** as the chat account. Both commands open prompts or a browser; the CLI stores the client ID and secret, access and refresh tokens and expiry in `~/.config/twitch-cli/.twitch-cli.env` (mode 600):
   ```sh
   twitch configure
   twitch token -u -s 'chat:read chat:edit'
   ```
4. **Install the chat token.** `chat/token_refresh.py refresh` refreshes it and writes `~/.config/glob2-stream/twitch-chat.token` (mode 600). `chat/token_refresh.py status` shows the login, scopes and minutes left.
5. **Set `TWITCH_BOT_USER`** to the account's login name in `$GLOB2_STREAM_HOME/stream.env`. `TWITCH_CHANNEL` defaults to `globulation2`. Without a bot user and token, everything still runs read-only, and replies are printed instead of sent.

## Token refresh

Twitch user tokens expire after about four hours. The rig refreshes them automatically with the Twitch CLI's saved login, so a 24/7 stream needs no manual step:

- before every connection or reconnection;
- every 10 minutes while the host runs, when under 30 minutes are left (checked with Twitch's [validate endpoint](https://dev.twitch.tv/docs/authentication/validate-tokens/));
- once more when Twitch rejects the login, before giving up.

`token_refresh.py` reads the client ID, client secret and refresh token from the Twitch CLI's env file (`TWITCH_CLI_ENV`). It posts them to Twitch's token endpoint over HTTPS (the request `twitch token -R` makes), so no secret appears in any process's arguments. It writes the new tokens back to that file, keeping its mode, then validates the new access token and writes it atomically to `TWITCH_CHAT_TOKEN_FILE` (mode 600). Tokens never appear in output or logs. If the CLI login is gone, the host keeps using the installed token until Twitch rejects it, then exits with a message saying what to run. These files stay in your home, which the sandboxed agents can't read. `supervisor.py … --chat` runs `token_refresh.py ensure` before it starts, so a broken login fails early.

## Running

```sh
chat/twitch_chat.py listen                 # watch chat as JSON lines (read-only works without a token)
chat/twitch_chat.py send "Hello, chat!"    # send one message (needs the token)
chat/chat_agent.py --dry-run               # read live chat, print the replies it would send
chat/chat_agent.py                         # reply in chat (dry-run automatically when read-only)
chat/chat_agent.py --simulate FILE         # feed "user: text" lines from FILE, dry-run (no Twitch needed)
```

Normally the supervisor starts the chat host alongside the stream (`supervisor.py … --chat`) and restarts it if it exits. It can also run on its own while a stream is up.

| Setting | Default | Meaning |
| --- | --- | --- |
| `CHAT_MODEL` | `claude-sonnet-5-5` | Model for the chat host (in `stream.env`). |
| `TWITCH_CHANNEL` | `globulation2` | Channel to join. |
| `TWITCH_BOT_USER` | empty | Account to speak as. Empty means read-only. |
| `TWITCH_CHAT_TOKEN_FILE` | `~/.config/glob2-stream/twitch-chat.token` | User access token, mode 600. |
| `CHAT_MIN_INTERVAL` | `20` | Minimum seconds between replies (environment). |
| `CHAT_MAX_PER_MIN` | `3` | Maximum replies per minute (environment). |
| `CHAT_BATCH_WAIT` | `15` | Seconds to gather messages before replying (environment). |
| `CHAT_MODEL_TIMEOUT` | `120` | Seconds before a model call is abandoned (environment). |
| `CHAT_GAME_ACCESS` | `1` | `0` disables read-only game access (environment). |
| `CHAT_MAX_GAME_CALLS` | `4` | Read-only game calls allowed per reply (environment). |
| `CHAT_MAX_BUDGET_USD` | `0.50` | Spending cap per model call (environment). |
| `TWITCH_CLI_ENV` | `~/.config/twitch-cli/.twitch-cli.env` | Twitch CLI settings with the refresh token. |

## Moderation

Announce chat interaction only while a human moderator is staffed, as the [streaming plan](../../../planning/twitch-streaming.md) requires. Use Twitch's AutoMod and blocked terms as the first line of defence; the host's filters are a backstop, not moderation. Stop the host (Ctrl-C, or run the supervisor without `--chat`) whenever no one is available to handle reports.

## Logs and state

- `$LOG_DIR/chat/YYYY-MM-DD.jsonl` holds chat messages seen, plus the host's own replies, capped at 20 MB a day.
- `$LOG_DIR/chat/agent.jsonl` holds one compact line per decision: batch size, reply or reason for dropping it, whether a suggestion was noted, the game tools called, turns and cost.

## Cost

With Sonnet 5.5, a reply answered from the status costs about $0.007, and one that checks `game_world` about $0.01–0.025 (2026-11-24 simulation). At the default limit of three replies a minute, a very busy chat costs at most about $4.50 an hour, and a quiet one costs nothing, because idle chat triggers no model calls.
- `$STATE_DIR/chat.json` records connected, can_send, updated, replies_sent and last_reply_at, for `status.py`.
- `$STATE_DIR/viewer-suggestions.jsonl` holds noted viewer ideas.

All of these stay on the streaming machine and are never committed.
