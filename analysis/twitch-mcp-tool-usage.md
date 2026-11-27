# How the stream player uses its MCP tools

[Analysis index](README.md) · [Stream rig](../tools/twitch-stream/README.md) · [Stream playbook](../tools/twitch-stream/stream-playbook.md) · [Glob2 MCP guide](https://github.com/Globulation2/glob2/blob/master/docs/development/mcp-ui-server.md)

Observed **2026-11-26**. This record measures how the Claude Plays Glob player (Sonnet 5.5 in `claude -p`, one session per match) spends its tool calls, tokens and errors, and ranks changes to the game's MCP server, the stream harness and the prompts. Re-run it with [`tools/twitch-stream/analysis/tool_usage.py`](../tools/twitch-stream/analysis/tool_usage.py) as more games accumulate.

## Data and limits

| Source | What was used |
| --- | --- |
| Player transcripts (`$LOG_DIR/player-archive`) | 99 transcript files: 87 sessions, of which 4 were recovery sessions, plus 12 resumed turns; matches 58 to 140, 2026-11-25 07:51 to 2026-11-26 21:25 (local time). Match 141 was still running and is left out (`--to 140`). |
| Match log (`games.jsonl`) | 83 results: 25 wins, 57 losses, 1 draw. |
| Supervisor log | Session starts, game timeouts, fast-forwards, quick-exit loops. |
| Chat agent log | 17 chat replies costing $0.41 and one `game_world` call in the window, plus 255 automatic camera-director moves. The chat side is negligible here and isn't analysed further. |
| Harness and server source | `game_proxy.py`, `stream_ctl.py`, `pacing.py`, `chat/camera.py`, the prompts, and the game's `src/mcp/` and `src/hive/LocalCommander.cpp` at the version the stream runs. |

Totals: 21,207 tool calls, 12,379 model calls and 37.0 hours of session wall time. That covers 35.7 hours of play (including fast-forward), and about $141 at API list prices ($3.82 an hour, $1.70 a match). The stream runs on a subscription, so these dollars measure rate-limit headroom, not a bill. They are the right yardstick for comparing designs.

How the numbers are measured, and the main limits:

- **Tokens per tool result.** The best measure is the cache write of the next model call (`cache_creation_input_tokens` plus uncached input). It counts the result plus the previous call's output and wrappers. It is measured only when the result was the only call in its message and no compaction came between. A linear fit over those calls gives about **0.47 tokens per character** for the JSON replies (2.1 characters per token), plus a fixed **~110–150 tokens per call**. A chars/4 estimate therefore undercounts JSON replies by about half. The tables show both measures.
- **Output and thinking tokens.** In stream-json, the `usage.output_tokens` on each assistant event is a snapshot taken when the message starts. Summed, the events give 0.32M output tokens against 2.49M in the `result` events. Output therefore comes from `result` events, per turn only. Compaction calls never appear as assistant events; their cost is the `result`'s `modelUsage` minus its `usage`.
- **Resumed sessions.** In a session resumed with `--resume`, `total_cost_usd` and `modelUsage` are cumulative over its turns, while `usage` covers one turn. The script takes the difference. The supervisor's "cost so far" and `cost_report.py` both just add the values up (see recommendation 13).
- **Unfinished turns.** The three turns the supervisor killed (match 95) have no `result` event. Their $6.23 is estimated from input usage plus 200 output tokens per call.
- **Phases.** *Setup* runs until `match_setup_done`, or until the first play call in a recovery session. *Fast-forward* starts at `match_fast_forward` or the supervisor's fast-forward note. *Wrap-up* starts after `match_result`. Wall minutes are gaps between tool calls, with gaps over 10 minutes dropped.
- **Which reply fields go unused.** The transcripts show only the arguments the model passes back. Whether a field shaped its thinking can't be seen. "Unused" here means repeated unchanged from the previous reply, or never passed back.
- **Outcomes.** These are 83 games against four AIs on varied maps, so the outcome comparison is descriptive only (see [Outcomes](#outcomes)).

## Summary

1. **About 60% of spend scales with the size of tool results.** Cache writes are 44% of cost and cache reads 24%. The other shares are output at 18% and compaction summaries at 15%. Tool results make up 11.3M of the 15.4M tokens written. Each result token costs about $7.9 per million over its life: $4.00 for the one-hour cache write, about $1.10 of re-reads before the next compaction, and about $2.80 of the compaction it brings closer.
2. **`match_wait` is the biggest stream.** It is 34% of calls and 36% of result characters. Each reply is about 600 tokens, and 57% of its field characters repeat the previous reply unchanged: losses, session, prestige, a duplicate `hud_sampled` block, and fixed notes. 75% of waits run their full 300 ticks with nothing happening, and 26% are followed straight by another wait.
3. **Compaction is constant.** It runs every 22 model calls (about 13.5 an hour, at a median 40.4k-token context) and costs 15% of spend in summaries. **Every fresh session compacts during setup** (79 once, 4 twice). That happens right after reading the 15–49 KB `strategy.md`, so the notes and the brief are summarized away before play starts.
4. **Setup is about 19% of spend in under 3% of the wall time.** It takes about 19 calls and 15.5 model calls per match, in 37 seconds. It also produces 138 of the 393 errors (35%), mostly stale or hidden `ui_act` controls in the landscape picker.
5. **Errors are few (1.85%), but the refusals are concentrated.** Narrations "not sent" (457, 16.6% of `narrate`) aren't flagged as errors, yet each one uses up a 6-second pacing slot. A further 39% of successful placements were moved away from the requested tile. 42 calls went to tools that don't exist, such as `Bash` to tail `games.md`, and stream-ctl tools called under the `glob2-stream` prefix.
6. **The player isn't slow; the loop is.** The model takes a median 1.3 s between calls, but calls are 11 s apart. 68% of play time is spent inside `match_wait`. It makes 1.5 decisions a minute (placements, building or zone changes), one every 40 s against the prompt's 20–30 s, at 3.25 model calls per decision.
7. **Screenshots aren't a problem.** There were 165 images at about 920 tokens each, roughly 1% of cache writes.
8. **One stalemate cost 14% of the window.** Match 95 ran for seven hours to tick 1.7M through five sessions and 3,932 calls, at $19.55, because the win chance hovered near 50% and fast-forward needs 10% or less.
9. **No link between tool use and results was found.** Wins and losses have near-identical call rates, error rates and tool mix, including in the first 10 minutes of play. The players' notes blame food: 52 of 57 losses mention starvation or food, and no tool raises an alert for it.

## Where calls and tokens go

### Calls per tool

| Tool | Calls | Share | Per match | Per play min | Setup | Playing | Fast-fwd | Wrap-up | Errors |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| match_wait | 7,286 | 34.4% | 87.8 | 3.39 | 0 | 7,106 | 174 | 6 | 8 |
| narrate | 2,754 | 13.0% | 33.2 | 1.26 | 0 | 2,609 | 97 | 48 | 8 (+457 "not sent") |
| game_world | 2,488 | 11.7% | 30.0 | 1.15 | 12 | 2,471 | 2 | 3 | 7 |
| camera_show | 2,259 | 10.7% | 27.2 | 1.05 | 1 | 2,233 | 25 | 0 | 65 |
| game_building | 2,015 | 9.5% | 24.3 | 0.94 | 6 | 2,007 | 2 | 0 | 34 |
| game_place | 1,346 | 6.3% | 16.2 | 0.63 | 0 | 1,345 | 1 | 0 | 81 |
| ui_act | 773 | 3.6% | 9.3 | – | 715 | 4 | 0 | 54 | 107 |
| ui_inspect | 490 | 2.3% | 5.9 | – | 417 | 5 | 5 | 63 | 1 |
| match_caption | 411 | 1.9% | 5.0 | 0.19 | 0 | 410 | 1 | 0 | 6 |
| Read | 317 | 1.5% | 3.8 | 0.04 | 114 | 47 | 46 | 110 | 15 |
| Edit | 175 | 0.8% | 2.1 | – | 0 | 13 | 12 | 150 | 0 |
| ui_screenshot | 162 | 0.8% | 2.0 | 0.08 | 1 | 161 | 0 | 0 | 0 |
| all others (21 tools) | 731 | 3.4% | 8.8 | – | | | | | 72 |

Other tools are rarely used. `game_time` had 89 calls (66 of them `speed 3`) and `match_fast_forward` 48 (13 refused). The Hive tools together had 69 calls, with 19 of 41 `hive_run` replies carrying a script error. `game_guide` had 36, `game_zone` 6 and `game_stats` 3. `game_alliance`, `ui_drag`, `ui_move`, `ui_mouse_button`, `ui_type_text` and `ui_release_inputs` were never called. No hidden tool (`game_view`, `game_wait`, `game_chat`) was called and there were no permission denials.

`game_building` is mostly flag handling: 938 `move` (47%), 490 `production`, 394 `workers`. Moving one war flag from one remembered enemy building to the next is the player's main attack technique.

### By phase

| Phase | Wall min | Tool calls | Model calls | Calls/min | Cache write tokens | Input-side cost |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Setup | 56 | 1,630 | 1,297 | 29.0 | 3.82M | $18.59 |
| Playing | 2,110 | 18,700 | 10,555 | 8.9 | 9.93M | $69.15 |
| Fast-forward | 34 | 428 | 210 | 12.5 | 0.34M | $1.91 |
| Wrap-up (notes) | 18 | 449 | 317 | 25.6 | 1.32M | $6.07 |

Input-side cost covers cache writes and reads only. Setup also carries 87 compactions (about $5.30 with rebuilds) and about $2.80 of output, so it costs about $27 in total, **19% of spend for 2.6% of wall time**. Roughly $8 of that is the unavoidable first prompt: 23.6k tokens written once per session.

### Spend

| Part | Cost | Share |
| --- | ---: | ---: |
| Cache writes (all one-hour TTL) | $61.6 | 43.6% |
| Cache reads | $34.0 | 24.1% |
| Output (including 0.37M thinking tokens, 15% of output) | $24.9 | 17.6% |
| Compaction summaries | $20.7 | 14.6% |
| Total | $141.3 | |

Every model call re-reads the whole context: 27.8k tokens on average during play. The 23.6k-token starting context is the system prompt and tool schemas (13.8k, cached across sessions) plus the brief (9.8k). Output averages 214 tokens per model call.

### Response sizes

| Tool | Median chars | p90 | Max | Share of all result chars | chars/4 est. (tokens, total) | Measured tokens, median (incl. ~110 overhead) | Measured / est. |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| match_wait | 1,022 | 1,317 | 1,777 | 36.2% | 1.97M | 601 | 2.2 |
| Read (notes) | 18,411 | 45,897 | 59,396 | 29.5% | 1.60M | 1,469 * | – |
| game_world | 869 | 1,928 | 8,259 | 11.3% | 0.62M | 616 | 2.7 |
| ui_inspect | 3,542 | 10,690 | 13,067 | 9.7% | 0.53M | 1,760 | 1.9 |
| ui_act | 524 | 3,898 | 9,025 | 4.3% | 0.23M | 368 | 2.8 |
| game_place | 445 | 534 | 686 | 2.7% | 0.15M | 407 | 3.4 |
| narrate | 133 | 170 | 222 | 1.7% | 0.09M | 145 | – |
| game_building | 134 | 147 | 260 | 1.3% | 0.07M | 230 | – |
| camera_show | 63 | 75 | 95 | 0.6% | 0.03M | 227 | – |
| ui_screenshot | 405 + image | | | image | | 922 (p90 1,586) | – |

\* Large note reads are mostly followed by a compaction, so few are measured. The measured median is for the smaller offset/limit reads. A full `strategy.md` read is now about 49 KB, roughly 12k tokens.

By tokens written after them, `match_wait` replies account for 30% of all writes, `game_world` 13%, and `narrate` and `camera_show` 9% and 7% (mostly the fixed per-call overhead). `ui_inspect` and `ui_act` together come to 11%.

### What the replies contain

`match_wait` (7,278 replies) breaks down as follows. 57% of its field characters equal the same field in the previous `match_wait` reply.

| Field or section | Share of reply | Unchanged from previous reply |
| --- | ---: | ---: |
| `status` (units_free, win_chance, prestige, hud_sampled) | 43% | `hud_sampled` restates units_free and win_chance as strings; `prestige` 99% unchanged |
| `losses` (six counters) | 22% | 92–99% per counter |
| `forces` | 11% | 17–68% |
| `note` ("The requested ticks passed…") | 7% | 81% |
| `alerts` | 7% | the actual news |
| `units` (repeats units_free totals) | 4% | 42% |
| `session`, `team` | 2.4% | 99% (never needed: the proxy and server already know the match) |

On top of the JSON, stream-ctl adds a "Game speed is …" line to every reply and a camera nudge to 906 of them: 0.5M characters in total.

`game_world` (2,488 replies) is used well. 87% of calls pass `include`, and 69% set `detail`, mostly `brief` with `include`. Only 8.7% of its content repeats. Building lists (38%) and resource fields (22%) dominate, then others' buildings (12%). The cheap path the prompt suggests (`detail: "alerts"` with `since_tick`) was used 13 times. 1,592 `game_world` calls (64%) come straight after a `match_wait`: the wait already returned status and alerts, and the player then asks for buildings, others or resources. `match_wait` can take `include` (stream-ctl passes it through), but it did so in 0.2% of waits.

The fixed `note` in action replies adds 254 characters to 501 `game_place` replies and 102 characters to 1,992 `game_building` replies. Together that is about 80k tokens.

## Errors and waste

393 errors in 21,207 calls (1.85%). After an error, the next call used the same tool 155 times, but with identical arguments only once: the player doesn't retry blindly. Getting the tool to work again took a median 2 calls (p90 5).

| Error class | Count | Example | Fix location |
| --- | ---: | --- | --- |
| UI control stale (revision changed) | 73 | `landscape/use` is at revision 128, not 90 (54 of 73) | Server (landscape picker) or harness setup |
| Placement: no room / unexplored | 55 | No room for Inn within 12 tiles: 625 spots tried… | Server (already explains; see placement below) |
| Camera rate limit | 51 | "the camera moved 8 s ago; wait 0 s" (rounding) | Harness `chat/camera.py` |
| Tool that doesn't exist | 42 | `Bash` ×14 (all to read the end of `games.md`), `mcp__glob2-stream__camera_show` ×12, `mcp__glob2-stream__match_wait` ×6, `*_placeholder` ×8 | Prompts, notes layout |
| UI control hidden/blocked | 32 | `landscape/38` scrolled out of view (25) | Prompt: select on `landscape/choice` |
| Stale or guessed building id | 21 | generation 0 "was not reported in this match" | Server (`LocalCommander::building`) |
| Invalid argument (schema range) | 19 | warflag `workers` 25 or 60 (max 20) ×9; `resource_radius` 80 (max 64) ×6 | Server: clamp and report |
| UI wait timed out | 17 | setup waits | Setup flow |
| Unknown building name | 16 | "exploration flag", "exploration_flag", "wheat" | Server: accept aliases |
| File too large to Read | 15 | `games.md` is 83 KB, over the 25k-token Read limit | Harness: notes layout |
| Action not valid for building | 13 | "Building does not produce units" (11): production sent to an Inn id | Server: name the type and the Swarm ids |
| Fast-forward refused | 13 | "not yet… now 36% at tick 26800" | Fine as is |
| Other (no match running, coordinates in caption, setup order, transport) | 26 | | |

Soft refusals, not flagged as errors:

- **`narrate` "not sent": 457 (16.6% of narrations).** They came a median 24 s after the previous message, against a 30 s limit. `stream_ctl.py` paces the call *before* checking the interval, so each refusal also uses a 6-second pacing slot: about 46 minutes in total.
- **`game_place` moved the building: 492 of 1,265 successful placements (39%).** `near` was used in 76% of calls. The move was a median 3 tiles (p90 8, max 23), 94% of the time because the ground wasn't clear and the rest because it wasn't explored. The player's notes come back to this repeatedly: "a near:true Inn landed across the water unreachable", "verify game_place 'moved' results", and an Inn or Swarm site "sat unbuilt… because canals made it unreachable".
- **Ignored wake-ups.** 1,085 waits woke for an attack (1,035 on units). In 48% of them the next call was simply another wait, against 22% after a plain timeout. The `attack` category also wakes on raids the player chooses not to answer.

## Pace and waiting

| Measure | Value |
| --- | --- |
| Tool calls per play minute | 8.9 (5.0 model calls) |
| Tools per model call | 1.73; 52% of messages carry several calls |
| Decisions (place, building, zone) per play minute | 1.51, at 3.25 model calls each |
| Model time between a result and the next call | median 1.3 s, p90 2.6 s (21% of play wall time) |
| Call to call | median 11.0 s, p90 21 s |
| Share of play wall time inside `match_wait` | 68% |
| Paced call latency (pacing wait), e.g. `game_place` / `game_building` | median 4.3 s |

The most common messages are a bare `match_wait` (25%), a bare `game_world` (16.5%), `narrate` + `match_wait` (14%) and `camera_show` + `match_wait` (10%). So the model already batches show calls with waits. The serial steps that remain are read, then act, then wait.

`match_wait`: the player asks for 300 ticks 95% of the time and gets a median 300. Wake reasons: ticks 75%, attack 15%, enemy sighted 3%, conversion lost 3%, enemy building gone 1.5%, match end 1.2%. 26% of waits come straight after another wait, though the brief says never to wait twice in a row. The rule survives compaction in only 149 of 559 summaries (27%).

## Setup, notes and compaction

**Setup** (83 fresh sessions) took a median 19 tool calls (15 of them UI), 15 model calls and 37 s. The landscape picker accounts for most of the errors: `landscape/use` stale 54, `landscape/N` hidden 25 or stale 19. The player clicked the generator cards (`landscape/N`, 108 times) more than it selected on `landscape/choice` by name (26 times), which the MCP guide recommends.

**Notes.** `strategy.md` read at setup grew from 15 KB (match 58) to 49 KB (match 140), about 400 characters a match, and `games.md` is 83 KB. Every session reads `strategy.md` first and compacts within a few calls. The lessons are therefore summarized away before the first placement. At wrap-up the player rereads both files (110 reads) and edits them (150 edits). The 14 `Bash` attempts and 15 Read errors all come from trying to read the end of `games.md`.

**Compaction.** There were 559 compactions, a median 5.5 per session and 13.5 per hour of play: 87 in setup, 400 playing, 58 at wrap-up and 14 in fast-forward. They trigger at a median 40.4k tokens and leave a 2.6k-token summary. With the 13.8k prefix and the rebuild (median 4.3k tokens written), each cycle buys about 22k tokens, roughly 22 model calls or 4.5 minutes of play. Each costs about $0.037 in summary plus $0.024 in rebuild. **Raising the threshold wouldn't help.** At 80k, the average context per call rises by about 20k tokens, which adds about $26 of reads over this window. Compactions would fall to about 200, saving about $22. The way to make cycles last longer is to make each call smaller.

The brief goes in as the first user message, so compaction replaces it with a summary within the first minute of every session. No session reread `session-brief.md` afterwards, as the brief asks. The summaries carry most rules (camera and narration in all 559), but "never wait twice in a row" in only 27%.

## Recovery sessions

Only match 95 needed recovery: four recovery sessions and 11 of the 12 resumed turns (the other was match 87's second turn). It was an island stalemate against Cabino. The win chance stayed around 40–60%, so neither the 10% fast-forward rule nor the player's own fast-forward attempt applied. The supervisor's two-hour game timeout ended three sessions. In another, the model ended its turn nine times in 23 minutes, and after three quick exits in a row the supervisor gave up on it. The match cost $19.55, $14.01 of it in recovery sessions, which is 14% of the window's spend, with 3,932 calls. Resuming worked: each resumed turn re-read its context from cache rather than rewriting it.

## Outcomes

These are medians over decided matches with at least 3 minutes of play.

| Group | n | Play min | Calls/min | Error % | Wait share | game_world share | Action share | Show share | Screenshots | Cost |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Wins | 25 | 20.3 | 9.4 | 2.4 | 31% | 19% | 23% | 21% | 1 | $1.37 |
| Losses | 57 | 17.2 | 8.9 | 2.0 | 34% | 17% | 23% | 23% | 2 | $1.35 |
| Wins, excl. Cortex | 13 | 22.5 | 8.4 | 2.0 | 37% | 16% | 22% | 22% | 1 | $1.45 |
| Losses, excl. Cortex | 49 | 17.2 | 8.9 | 1.9 | 34% | 17% | 23% | 23% | 2 | $1.35 |
| First 10 min only: wins / losses | 25 / 57 | – | 9.6 / 8.9 | 2.1 / 1.2 | 26% / 26% | 20% / 21% | 30% / 31% | | | |

There is no visible relationship between the player's tool use and the result. Several things limit what this can show:

- 12 of the 25 wins are against Cortex, which often quits early. With Cortex left out, only 13 wins remain.
- 56 matches were fast-forwarded, which shortens the wall time of lost games.
- Opponent and map vary from match to match.
- Tool behaviour is very uniform across matches, because pacing and the prompt fix most of the rhythm.

The notes point elsewhere: 52 of 57 losses cite food or starvation, and 14 matches say the enemy was found late or never. The tools report combat events well. None reports a weakening economy: no Inn running dry, no field running out, no site stalled with no builders, no flag that draws no units.

## Recommendations

Ranked by expected value. Savings are estimated over this window (83 matches, $141), using the $7.9-per-million marginal cost for result tokens and about $0.006 per avoided model call.

| # | Change | Where | Expected saving | Effort |
| ---: | --- | --- | --- | --- |
| 1 | Lean `match_wait` replies: news and changes only | Harness now, then server | ~2.6M tokens, ~$20 (14%), ~110 fewer compactions | Small |
| 2 | Five-minute cache TTL, if the CLI allows it | Harness (agent-run) | ~$23 (16%) of cache-write cost | Trivial if available |
| 3 | Notes digest instead of full notes; rotate `games.md` | Harness (supervisor), prompts | 1 compaction per session, ~$6–8; 29 errors and Bash attempts; lessons that survive into play | Small |
| 4 | One-call match setup, or a guided setup path | Harness (stream-ctl), prompts, server | ~$12–15 (9–10%), ~15 calls and ~1.5 errors per match | Medium |
| 5 | Stalemate rule | Harness (stream-ctl, supervisor) | ~$15 in this window (one match); caps the worst case | Small |
| 6 | Economy alerts: Inn low, field depleted, site stalled, flag unstaffed | Server | Targets the cause cited in 52 of 57 losses; fewer polling `game_world` calls | Medium |
| 7 | Let `match_wait` return what the next decision needs (`include`) | Prompts | Up to ~1,600 model calls, ~$5–7 | Trivial |
| 8 | Queue narrations instead of refusing them; check before pacing | Harness (stream-ctl) | 457 calls, ~46 min of pacing slots | Trivial |
| 9 | Argument tolerance and fix-it errors in game tools | Server | ~65 errors, fewer stranded sites | Small |
| 10 | Quieter attack wake-ups | Harness and server | ~500 ignored wakes, ~$4 | Small |
| 11 | Hide unused tools; give full tool names in prompts | Harness (proxy), prompts | ~2–3k prefix tokens, ~$7 (5%); 27 wrong-name calls | Trivial |
| 12 | Camera: wait out the 8 s gap instead of refusing; fix the "wait 0 s" rounding | Harness (`chat/camera.py`) | 51 errors | Trivial |
| 13 | Fix cost accounting for resumed sessions and output tokens | Harness (supervisor, `cost_report.py`) | Correct numbers | Trivial |
| 14 | A combined turn tool, and deltas in the server | Server and harness redesign | ~40% fewer model calls, ~$25–30 | Large |

### 1. Lean `match_wait` replies (harness now, server later)

**Evidence.** `match_wait` replies are 36% of result characters and about 600 tokens per call, 30% of all cache writes. 57% of their field characters repeat the previous reply. `session`, `team`, `prestige` and the fixed `note` almost never change, and `hud_sampled` and `units` restate `units_free`. The six `losses` counters are 92–99% unchanged. The speed line comes with every reply.

**Change.**

- *Harness, `stream_ctl.match_wait`.* Keep the previous reply per session and return `tick`, `reason`, `waited_ticks`, `trigger`, `alerts` and, from `status`, `losses` and `forces`, only the fields that changed. Report `win_chance` only when it moved by 2 points or more. Print the speed line only when the speed changed, and the camera nudge at most once a minute.
- *Server.* Add a compact option to `game_wait`/`game_world`, built by `LocalCommander::wait` and the status block in `LocalCommander::worldReply` (`src/hive/LocalCommander.cpp`). It would drop `session`/`team` when the caller doesn't need them, drop `hud_sampled` and `prestige`, report `losses` only when a counter changed (the server already tracks `units_converted_away_since_last_read`), and omit the note when the reason is `ticks`.

**Saving.** From about 505 to about 150 result tokens per wait: roughly 2.6M tokens, about $20 (14%), and about 110 fewer compactions over this window. The harness version needs no game release.

### 2. Five-minute cache TTL (harness)

**Evidence.** Every cache write was made with the one-hour TTL ($4.00 per million, against $2.50 for five minutes). Calls come every 11 s, and the longest gap in play was about a minute.

**Change.** If the Claude Code version the sandbox installs offers a choice of prompt-cache TTL, choose five minutes for the player in `agent-run`. Check the current docs; this analysis didn't verify that the setting exists.

**Saving.** 15.4M write tokens × $1.50 per million, about $23 (16%). On a subscription this shows up as rate-limit headroom.

### 3. Notes digest, rotated game log (harness, prompts)

**Evidence.** Every fresh session compacts during setup, right after reading `strategy.md` (now 49 KB, growing about 400 characters a match), so the lessons don't survive into play. `games.md` is too big to Read (15 errors), which led to 14 `Bash` attempts. Wrap-up rereads both files.

**Change.**

- *Supervisor.* Put the last three `games.md` entries and a capped digest of `strategy.md` into the brief.
- *Prompts.* Ask the player to keep a `## Current playbook` section of at most 4 KB at the top of `strategy.md`, append lessons below it, and move entries older than about 30 matches to `games-archive.md`.
- *`player.md`.* Say how to read the end of `games.md` (Read with `offset`), or drop the step once the brief includes it.

**Saving.** About 10k tokens and one compaction per session (about $6–8 over the window), 29 failed calls, and lessons that are still in context when play starts.

### 4. One-call match setup (harness, prompts, server)

**Evidence.** Setup costs about $27 (19%) in 37 s. It has 138 errors (35% of all): 106 from `ui_act`, nearly all in the landscape picker (`landscape/use` stale 54, `landscape/N` hidden 25 or stale 19), and 17 `ui_wait` timeouts.

**Change.**

- *Option A, harness.* Add a stream-ctl `match_setup(generator)` that drives the Custom game screens (opponent, generator, 256×256, start) through the game's `ui_inspect`/`ui_act` and calls `match_setup_done` itself, returning the screen it reached. Viewers still see the menus.
- *Option B, prompts.* Steps in `player.md`: select the generator with `ui_act` `select` on `landscape/choice` by name, act with `inspect: false` until the final screen, and use `wait_for: {"screen": "game_session"}` on `start`.
- *Server.* In `game/screens/LandscapePickerScreen.cpp`, stop `landscape/use` changing revision while previews load. `ui_act` (`src/mcp/Tools.cpp`, the stale-control check) could also accept `activate` on a stale revision when the label and actions are unchanged.

**Saving.** About 15 calls, 1.5 errors and one compaction per match: about $12–15 (9–10%) with option A, a third of that with option B.

### 5. Stalemate rule (harness)

**Evidence.** Match 95 ran seven hours (game tick 1.7M) at about 40–60% win chance, while the narration repeated "still holding" and "no enemy contact" for hours. It cost $19.55, 14% of the window.

**Change.**

- *`match_fast_forward`.* Also allow it when the match is past a long tick count (for example 300k), and there has been no building lost or destroyed on either side and less than a 15-point win-chance swing over the last 100k ticks. A `draw` result would also do.
- *Supervisor.* Use the same test before the game timeout ends a session and starts a recovery, so the stalemate doesn't keep running across sessions.

**Saving.** About $15 here, and a bound on the worst case.

### 6. Economy alerts (server)

**Evidence.** Most losses are food collapses (52 of 57 notes), but `game_wait` wakes only on combat, conversion, sightings, completions and Hive events (`waitCategories()` in `LocalCommander.cpp`). The player checks food by polling `game_world`: 2,488 calls, 22% with `resources`. The notes keep returning to Inn sites with 0 builders and flags that drew 0 warriors.

**Change.** Add own-colony alert kinds and `until` categories:

- `inn_low_food`: an Inn below a threshold with hungry units nearby;
- `resource_field_low`: a known field under, say, 25% of the amount first seen;
- `site_stalled`: no construction progress for N ticks, with the number of builders assigned;
- `flag_unstaffed`: a flag with 0 assigned after N ticks.

Expose them in `game_world` alerts and as `match_wait` `also_until` options. These read only the colony's own buildings and the fields it has seen, so fair play is unaffected.

**Saving.** Mainly play quality (the single biggest cause of losses), plus fewer polling calls.

### 7. Ask the wait for the next decision's data (prompts)

**Evidence.** 64% of `game_world` calls come straight after a `match_wait`, while `match_wait` `include` is used in 0.2% of waits.

**Change.** In `player.md`'s efficiency section: "When you plan to act after a wait, pass `include` (for example `["buildings"]` or `["others"]`) to `match_wait` instead of calling `game_world` next." Also correct the compaction note: it says compaction comes "about every 50k tokens", but it happens at about 40k.

**Saving.** Up to about 1,600 model and paced calls (about $5–7) and roughly 11 s off each read-then-act cycle.

### 8. Queue narrations (harness)

**Evidence.** 457 narrations (16.6%) were refused a median 24 s after the previous one. Each still went through `pacing.wait_turn()`, because `serve_mcp` paces before the handler runs.

**Change.** In `stream_ctl.narrate`, accept the message and send it when the 30 s window opens, replacing any queued one, and reply "queued, sends in 6 s". Or check the interval before pacing so a refusal costs no slot. Update the tool description to match.

**Saving.** 457 calls and about 46 minutes of pacing slots, with no extra viewer-visible chat.

### 9. Argument tolerance and fix-it errors (server)

**Evidence and change.** About 65 errors have causes the server can remove, all in the glob2 repository:

- *Unknown building name, 16* (`LocalCommander::placeByName` / `GameGUI::createDefaultsFromAutomation`). Accept case, space and underscore variants ("exploration flag", "war_flag"). For a resource name, say "wheat is a resource: place an inn beside it".
- *Out-of-range values, 15.* `game_place.workers` is capped at 20 in the schema, which rejects 25 or 60 for warflags, and `game_world.resource_radius` is capped at 64. Clamp and report under `settings`, as the guide promises ("capped, reported"), instead of failing schema validation (`src/mcp/Tools.cpp`).
- *Guessed generation, 21* (`LocalCommander::building`). The player passes generation 0. For an own building, say "building 4 is now generation 1 (an inn); pass generation 1". Or make generation optional for flags, where staleness matters less.
- *"Building does not produce units", 11* (`src/scripting/javascript/ScriptOrders.cpp`). Name the building's type and list the Swarm ids from the last `game_world`.
- *Placements moved, 39% of successful placements.* In `game_place`, report the requested-to-placed distance under `moved` (already done). Also add a `same_landmass` flag, computed only from explored terrain, saying whether the placed site connects by land to the colony's nearest Swarm or Inn, and an option to refuse rather than move across water. That addresses the player's recurring notes about sites placed out of reach.

**Saving.** About 65 errors and their recovery calls (a median 2 each), plus fewer stranded buildings. With recommendations 3, 4, 11 and 12, about 280 of the 393 errors (70%) have a named fix.

### 10. Quieter attack wake-ups (harness, server)

**Evidence.** Attacks wake 15% of waits, and 48% of those wakes are followed straight by another wait.

**Change.**

- *Harness (`WAIT_ALWAYS` in `stream_ctl.py`).* Wake on `attack_buildings`, conversions and building losses. Report other unit attacks in `alerts` without waking.
- *Server.* Group repeat attacks on the same area into one wake per skirmish over a longer window (the `ongoing` key in `LocalCommander::wait` is 8×8 tiles over 150 ticks).

**Saving.** About 500 model calls (about $4).

### 11. Hide unused tools, use full names (harness, prompts)

**Evidence.** Six listed game tools were never called (`game_alliance`, which the prompt forbids, `ui_drag`, `ui_move`, `ui_mouse_button`, `ui_type_text`, `ui_release_inputs`), and the Hive tools were used 69 times with frequent script errors. 27 calls used a wrong or invented name (`mcp__glob2-stream__camera_show`, `hive_run_placeholder` and similar).

**Change.**

- *Proxy.* Add these to `HIDDEN` in `game_proxy.py`, and consider `game_stats` and the Hive tools, whose light use the playbook allows; that is a product choice.
- *Prompts.* Name tools with their server in `player.md` and the playbook ("stream-ctl's `camera_show`" is already used in places; make it consistent), and never list `camera_show` or `match_wait` among the game tools.

**Saving.** An estimated 2–3k of the 13.8k prefix tokens on every call: about $3 of reads and about 10% longer compaction cycles (about $4).

### 12. Camera gate (harness)

**Evidence.** 51 `camera_show` refusals came while the director's own moves (255 in the window) held the 8 s gap. Two said "wait 0 s" because of rounding.

**Change.** In `chat/camera.py`, sleep out a remaining wait of up to 8 s, as `pacing.py` does, instead of refusing. Round the reported wait up.

**Saving.** 51 errors and the calls that followed them.

### 13. Cost accounting (harness)

**Evidence.**

- `supervisor.py` adds each resumed turn's `total_cost_usd`, which is cumulative over the session. It logged $7.93 for a session whose true cost was $1.39, and $6.23 against $3.75 for match 87.
- `cost_report.py` adds the same field per `result`, so it overcounts resumed sessions in the same way.
- `cost_report.py` also prices output from the per-event `usage.output_tokens` snapshots: 0.32M tokens against 2.49M actual, an $18 undercount in this window.

**Change.** Difference `total_cost_usd` and `modelUsage` across a session's turns. Take output from the `result` events. `tool_usage.py` (`cost_turns`) does both.

### 14. Larger redesigns

- **A combined turn tool.** `match_turn` in stream-ctl, or a `game_turn` in the server, taking `{orders: [...], camera, narrate, wait_ticks, include}`. It would apply the orders, move the camera, narrate (queued), wait, and return a lean delta. Messages already pair show calls with waits, so the gain is removing the serial read → act → wait round trips. Model calls per decision could fall from 3.25 to about 1.5, cutting about 40% of model calls (about $25–30) and freeing pacing for fewer, larger moves. Keep the 10-second wait cap and the camera rules in the tool, so the stream still looks active.
- **Delta replies throughout.** The server already keeps per-agent memory (remembered buildings, conversions since the last read). Extend it with `changes_since` for `game_world`: building lines whose stock, workers or hp changed, new and removed buildings, others' buildings first seen or gone, and resource fields whose amount moved more than 10%. On top of recommendation 1 this could save 30–40% of `game_world` tokens (about $3) and make long matches cheaper per minute.
- **Flag sweeps.** 47% of `game_building` calls move a flag, mostly war flags stepping from one remembered enemy building to the next after `enemy_building_gone`. A server or Hive helper ("move this flag to the nearest remembered enemy building when its target is gone") would use only what the colony has seen, so it stays within fair play. It would save hundreds of calls, but it automates the stream's most visible action. Weigh it against the playbook's rule to keep Hive light and the play visible, and if adopted, keep the camera and narration on each move.

## Re-running

```sh
cd tools/twitch-stream/analysis
./tool_usage.py --to 140                      # the tables in this record
./tool_usage.py --from 141 --json /tmp/new.json   # later games
./tool_usage.py --section errors              # one section: coverage, tools, phases, sizes, fields,
                                              # errors, refusals, efficiency, waits, screenshots, args,
                                              # setup, compaction, recovery, matches, outcomes
```

By default the script reads `$LOG_DIR/player-archive`, `$STATE_DIR/games.jsonl` and `$LOG_DIR/supervisor.log` through `rigconfig`, and needs only the standard library. It redacts long token-like strings in any text it prints.
