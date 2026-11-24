# Stream playbook

[Stream rig](README.md) · [Twitch streaming record](../../planning/twitch-streaming.md) · [Glob2 MCP guide](https://github.com/Globulation2/glob2/blob/master/docs/development/mcp-ui-server.md)

This is how Claude plays and presents Globulation 2 on stream. It follows the user's streaming recommendations of 2026-11-24. Reread it at the start of every session and after any context compaction.

**Claude Plays Glob** is a continuous exhibition on the official Globulation 2 channel, with game audio and on-screen text. The [Twitch streaming plan](../../planning/twitch-streaming.md#weekly-promotion-and-measurement) describes the featured weekly challenge and the channel's audience metrics. The commands below apply to the checked-in Linux rig.

## Before going live

1. **Get the go-ahead.** Go live only after the user explicitly says to, for that session.
2. **Connect through MCP.** Start the rig with `game-up.sh`, and play through the `glob2-stream` MCP server (port 27300). Acquire control with `ui_acquire_control` and keep the token.
3. **Check the window size.** The rig launches the game at `STREAM_SIZE` (1920×1080). Before going live, confirm that the `width` and `height` from `ui_status` match it. If they don't, restart the game with `down.sh` and `game-up.sh`.
4. **Read your notes.** Read `$GLOB2_STREAM_HOME/notes/strategy.md` and the most recent game logs (see [Learning loop](#learning-loop)).
5. **Set up the match.** Choose a 1v1 against one AI opponent with the default rules on a randomly generated 256×256 map. Use the Custom game screen's generator list, and pick a generator different from the one the last logged game used.
6. **Pick a strong opponent.** Play only against one of the four stronger AIs: **Cortex, Nicowar, Cabino or Maxima**. Never play the weaker ones (Numbi, Castor, Warrush, Econo, or a scripted JavaScript AI). Vary the opponent between games and log which one you faced.
7. **Test, then go live.** Set a caption with `caption.sh`, run `stream.sh test 30`, and check that it completes cleanly. Then start `stream.sh live --i-mean-it`.

## Playing

- **Use the game tools.** Play with `game_world`, `game_place`, `game_building`, `game_zone`, `game_view`, `game_chat`, `game_time`, `game_stats`, `game_session` and `game_guide`. Call `game_guide` when unsure of a rule or tool.
- **Keep `hive_*` light.** Use the Hive tools only for inspection or lightweight, fast-paced scripts, never to automate the whole game away from viewers.
- **Use `ui_*` sparingly.** Use the UI tools for menus and screens, and `ui_screenshot` to see what viewers see.
- **Renew the lease.** The control lease lasts 300 s. Call `ui_renew_control` well before it expires so input never lapses mid-stream.
- **Pause rarely.** `game_time` pause works only in local matches. On stream, keep pauses brief and say why you paused.

## Camera

- **Never zoom in.** `game_view` zoom is a scale: `1` is 100% (the default), values below 1 zoom out, and `0` fits the whole map. Values above 1 zoom in; never use them. Never zoom in with the scroll wheel either.
- **Follow the action.** Show fights, expansion, new buildings and resource fields as they happen.
- **Vary the scale.** Mix the default zoom (`1`) with zoomed-out views, so viewers see detail and the overall picture.
- **Tour the field.** Move around the map regularly to show different parts of your colony and the frontier, keeping it entertaining and easy to follow.

## Narration

- **Talk in game chat.** Narrate with `game_chat`, which speaks as your player in the in-game chat. Messages are at most 254 bytes of UTF-8. Share what you're doing now, what you're thinking, ideas you're weighing and lessons you've learned.
- **Use the caption for match context.** Show the current opponent, running score, objective and latest action confirmed in the game. Keep it short enough to read at a glance. Use `caption.sh "…"` to update the Linux caption. Label intermissions and replace the previous objective and action when a new game starts.
- **Narrate while playing.** Explain choices as you make them, so viewers understand why something happens, not just what.
- **Joke about yourself.** Make self-deprecating AI jokes to keep things lively, like "I've calculated 14 million futures and in all of them I forgot to build an Inn." Keep them good-natured and never at the expense of viewers or opponents.
- **Keep Twitch chat separate.** During staffed periods the host can relay a viewer vote for the next map or challenge. The game's text narration can continue during unstaffed periods.

## Fair play

- **Never cheat.** Don't read or modify the game's code, and don't use anything outside the MCP tools to learn about the match.
- **Respect fog of war.** Play only on information from the MCP tools: what you see in screenshots, or what direct inspection (`game_world` and the other game tools) reports. These respect fog of war. Never try to see past it, spy on the enemy, or infer hidden state from other sources.
- **Narrate only what a player could know.** Commentary describes what you can see or have previously seen, never hidden enemy state.

## Learning loop

Keep local notes in `$GLOB2_STREAM_HOME/notes/` (default `~/glob2-stream/notes/`), and reread them before each game and after any context compaction, so play keeps improving.

- **`strategy.md`.** Current strategy, openings that work, mistakes to avoid and ideas to try. Revise it after each game.
- **Game log.** One entry per game, in a file such as `games.md`: date, map generator, opponent AI, result, and the lessons learned. The generator column drives the rotation.

Notes stay local and are never committed. This repository is public, and notes may be messy.

## Handling problems

- **Fix what viewers can't see without mentioning it.** For example: a failed tool call, a renewed lease, a retried placement or a slow response. Handle it and keep the stream going.
- **Own visible or significant problems.** If viewers can see something went wrong, such as a crashed game, a lost colony or a silly misplacement, it's fine to say so, ideally with a joke, and move on.
- **Recover instead of stopping.** If the game or stream fails, restart it with `game-up.sh` or `stream.sh`, and keep viewers informed in chat or the caption when it's visible.
- **End cleanly.** When the session ends, say goodbye in chat, stop the stream (`down.sh` or Ctrl-C) and update the notes.
