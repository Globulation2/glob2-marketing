# Game Jolt listing comparison

Observed 2026-11-26 through Game Jolt's public site API (`/site-api/web/discover/games?tag=strategy`, the per-game and overview endpoints). Sample: the first 14 games in "best" and the first 8 in "hot" for the strategy tag, 22 entries in total (21 games: XANNIBAN appears in both lists). Execution is recorded in the [web portal rollout](../planning/web-portal-rollout.md#game-jolt).

## What the top strategy games do

| Feature | Top 22 | Globulation 2 before | After 2026-11-26 changes |
|---|---|---|---|
| Trailer or gameplay video | 16 of 22 | none | gameplay trailer added |
| Custom page colour theme | 18 of 22 | none | brand accent `#e3c077` |
| Screenshots | median 8 | 7 | 7 (unchanged) |
| Description hashtags | median 7 | 3 | 4 |
| Devlog posts | median 32 | 0 | 0 |
| Browser-playable build | 1 of 22 | yes | yes |

Most common hashtags in the sample: `#strategy` (22), `#action` and `#adventure` (10 each), `#horror` (9), `#other` (9), then `#retro`, `#rpg`, `#arcade` and `#puzzle` (8 each). `#multiplayer` appeared on 2. Most of the sample are not real-time strategy games: Game Jolt's strategy tag is broad, and its top games are mostly horror, fan games and action games that also tag themselves strategy.

## How Game Jolt discovery works (observed)

- **Tags come from description hashtags.** There is no tag field. The description editor lists about 24 official tags (for example strategy, multiplayer, retro, rpg, puzzle, survival); each has browse pages at `/games/best/tag-<name>`, `/games/hot/tag-<name>` and `/games/new/tag-<name>`. Other hashtags are allowed but get no browse page.
- **No genre or language fields.** The Details page has development stage, title, URL path, website and engine only.
- **Devlog posts feed discovery.** Posts appear in followers' feeds and on Discover. Even the "hot" entries with few followers post regularly (45 and 69 posts for two of them).
- **Development stage:** Devlog-Only, Early Access or Complete/Stable. 12 of the 22 used Complete/Stable.

## Inferences (not validated)

- Browser play is rare among top strategy listings (1 of 22), so it may stand out. The description already says "Play it right here in your browser"; moving that to the first line was considered and not applied.
- Devlog posting is the largest remaining gap and probably the largest lever, but it is an ongoing commitment, and each post is public.
- Adding tags that do not fit (horror, action) would match the sample's habits but would mislead players, so they were not used.

## Limits

One day's snapshot; rankings move. The sample measures what top listings have, not what made them top: their follower counts mostly come from franchise fan games and long histories, not from listing fields.
