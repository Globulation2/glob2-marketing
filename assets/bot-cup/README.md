# Glob 2 Bot Cup demo

[Download the 90-second MP4](bot-cup-demo.mp4) · [Instructor brief](../../planning/bot-cup/instructor-brief.md)

The video is captioned and silent. It opens with a separate bot-versus-bot battle, shows one JavaScript edit, and compares the same match setup before and after the edit.

## What happens in the demo

| Time | On screen |
|---|---|
| 0:00 | Developed colonies compete in Four Squares. Every colony is AI-controlled. |
| 0:11 | A pair of students starts with a working bot and predicts the effect of a change. |
| 0:21 | The minimum inn target changes from 2 to 3. Inns feed globs. |
| 0:33 | The baseline bot runs against Numbi on SmallForTwo. |
| 0:45 | The same matchup runs with the edited bot. The red colony builds a third inn. |
| 0:57 | At the same cutoff, the baseline has 2 inns and 13 globs, with none seeking food. The edited colony has 3 inns and 14 globs, with one seeking food. Neither bot has won at that point. |
| 1:12 | Student teams test a second map, explain a result, and submit a bot for a private tournament. |
| 1:22 | The free pilot includes the JavaScript starter, instructor guide, and private tournament. |

## Capture and measurement

- Opening footage comes from the [Four Squares capture](../reddit-campaign/README.md#earlier-four-squares-take), with four Cortex opponents. It illustrates the game separately from the lesson experiment.
- Comparison footage is native macOS spectator gameplay captured in Globulation 2 version 0.11.7.0, revision `5bf966285aa8`, from tick 7,168 checkpoints. Both jobs used the bundled SmallForTwo map, game seed 19, the Bot Cup starter in seat 0, Numbi in seat 1, and a tick cap of 8,192. Both jobs reached the tick cap. The only source change was `MINIMUM_INNS` from 2 to 3.
- The results card uses the verified headless snapshots at tick 8,192. Their checksums are `3501970123` (baseline) and `3759927008` (edited). Food-seeking counts are a single snapshot and say nothing about how long individual globs were hungry.

The H.264 export has 2,700 frames at 30 fps and a resolution of 1280 × 720. SHA-256: `0ac942912907de0370e1e2bb3d036cbd8757700ff791f1aca9946d95e0bffd46`.
