# Glob 2 Bot Cup facilitator checklist

## Before the sessions

- Name the instructor, cohort, and two dates. Check that participants recognize a JavaScript condition and function.
- Rehearse on a managed device with the same student permissions as the group. An approved desktop build can import the standalone [starter bot](starter.js). Try the browser only after confirming that the exact deployment can import, edit, playtest, and export on the host's devices. The browser AI Studio is opt-in. Record the build or deployment tested, device class, and any sign-in or permission barrier.
- In desktop Glob 2, open **Settings → Custom AIs**, import the starter and choose it for a computer-controlled seat in a local game. Arrange an AI-only spectator game if the available build supports it. Confirm that the instructor can import a second file or update the first bot, run another game, and hand off a source file. The starter file is also the known-good reset. Give pairs a separate copy to edit.
- Set one display name per pair and use filenames such as `team-maple.js`. The instructor handles submissions. Collect source and team aliases for scoring. Keep feedback, standings, and any match file private to the host.
- Rehearse the demo and reserve the same starting configuration for both runs. Use **Small For Two**, starter in the first seat, Numbi in the second, and game seed 19 for the reference test. If the host interface cannot set a seed, the facilitator should use the organizer's paired runs for scoring the experiment and students can still use local play for iteration. Use **balanced for 2** for the second exercise and for tied placings.
- Confirm the intended time per match and the second map with a dry run before the event. Arrange submissions by minute 25 of Session 2. For bigger classes, run several matches in parallel where available and show a small playoff or selected replay at the end; send complete standings through the instructor when ready.

## Session 1 — Compare a baseline and an edit

| Minutes | Work |
|---|---|
| 0–10 | Show the baseline match and explain that inns supply food while construction needs workers and time. |
| 10–20 | Pairs locate `MINIMUM_INNS`, predict one effect of changing it from `2` to `3`, and save a copy. |
| 20–40 | Start the modified simulation and compare it with the baseline using the same setup and observation point. Record how many inns are complete or under construction and one other observation, such as population or progress on another building. If a bot fails, restore the starter, read the message, and try one edit again. |
| 40–55 | Discuss why an extra inn may provide more capacity and may use workers and construction time that could have gone to another building. Use the results to check which of those things actually happened. |
| 55–60 | Capture the count of pairs that ran an edited bot within 20 minutes of starting the edit exercise. Record device failures and support interventions. |

### Example result

On macOS Glob2 0.11.7.0 (revision `5bf966285aa8`), the sample matchup ran to tick 8,192. The bot in the first seat had two completed inns and 13 globs at the baseline and three completed inns and 14 globs after the edit. The engine reported one glob needing food in the edited run at that tick, compared with zero in the baseline. Neither run produced a winner by the tick cap. These are observations from one matchup at one point in time.

| Minimum inn target | Completed inns | Globs | Globs needing food |
|---|---:|---:|---:|
| 2 | 2 | 13 | 0 |
| 3 | 3 | 14 | 1 |

Both bots passed startup validation and played to the tick cap without being disabled or reporting a rejected decision.

## Session 2 — Check a second map and run the cup

| Minutes | Work |
|---|---|
| 0–15 | Try the rule on the second map. Check whether the first result still holds. |
| 15–25 | Each pair finishes a three-sentence explanation and gives its final `.js` file to the instructor. |
| 25–45 | The organizer runs the paired matches while teams compare their evidence. Give teams a short correction window for a failed validation. |
| 45–60 | Show the result, discuss a close match or an instructive trade-off, and recognize the best explanation as well as the winner. |

Award one point for a win and half a point for a draw across paired games, with starting seats swapped. Use a second-map paired rematch for tied placings, and share a placing if it remains tied. Use the same pinned engine, maps, seeds, and tick cap for all teams. Set a learning expectation that a stalled or drawn match is still useful evidence. The organizer validates and executes submitted code in isolation using the [headless tools](https://github.com/Globulation2/glob2/blob/master/docs/tools/tournaments.md).

A dry run on macOS Glob2 0.11.7.0 used the two inn-target versions on both maps with starting seats swapped. All four matches reached the cap of 8,192 ticks without controller errors or a declared winner. These matches took about 40–45 seconds apiece in a four-job headless batch on the test machine. Rehearse the cap with the host before scheduling the cup, and expect ties if playing two closely related bots. The teaching example uses the fixed tick to compare strategies.

## Evidence and debrief

Score an explanation as meeting the rubric if it states **what changed**, names **one observed difference or explicitly reports no difference at the chosen tick**, and supports that observation with **a fair comparison or an acknowledged setup difference**. Record aggregate pass counts and total pairs. The pilot targets are at least 80% of pairs running a modified bot within the exercise's first 20 minutes and at least 70% meeting the explanation rubric.

Record rehearsal time, instructor prep, support interventions, and the top blocker. Ask the instructor what they would change, whether they could run the exercise again, and which cohort and date they would choose.

## Starter provenance

The single-file starter contains the readable bundled JavaScript from Globulation 2's Readable Colony example, adapted to expose the minimum-inn rule and use the workshop name. The upstream source is pinned at [b542af9](https://github.com/Globulation2/glob2-javascript-ai-starter-exampler/tree/b542af9f774c0664b70b045dcd95dffae12dc188). The included [license](LICENSE) covers redistribution of the starter.
