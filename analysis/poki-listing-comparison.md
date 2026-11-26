# Poki listing comparison

Observed 2026-11-26 from Poki's public pages, read signed-out with `curl`. Each page embeds its data as `window.INITIAL_STATE` JSON (`api.queries.getCategory` and `getGame`).

- **Category pages:** `https://poki.com/en/strategy` (98 games); `/en/rts`, which serves the Tower Defense category; `/en/war`.
- **Game pages** (`/en/g/<slug>`) for ten top strategy games:
  - the five games the category page itself names as "most popular … based on total plays": Master Chess, War Master, War of Sticks, Sort the Court!, and Pull the String (not read);
  - the closest RTS-like games: MicroWars, World Conquest, War Masters: Tactical Strategy, Era: Evolution;
  - two builders: Village Builder, The Final Earth 2.
- **Developer rules:** [requirements](https://developers.poki.com/guide/requirements-quality), [game thumbnail](https://developers.poki.com/guide/game-thumbnail), [Player Fit Test](https://developers.poki.com/guide/player-fit-test).

Our state: not applied. The plan is the lite build, about 8 MB before the game starts ([web portal rollout](../planning/web-portal-rollout.md#poki)).

## What the top strategy games do

| Feature | Top strategy games (10 read) | Globulation 2 (planned) |
|---|---|---|
| Animated thumbnail (hover video) | 10 of 10 | none made yet |
| Mobile available | 10 of 10 | lite works by touch in the iPhone simulator |
| Orientation | 4 landscape, 3 both, 3 portrait | landscape |
| Intro (page lead) | 29–43 words | n/a (Poki writes it) |
| Description | 109–238 words in Poki's house template: "How to play X?", "Who created X?", "How can I play X for free?", "Can I play X on mobile devices and desktop?" | n/a (Poki writes it) |
| Controls line | one sentence ("Mouse click or tap to send soldiers to build or attack.") | to supply |
| Categories | 2–12 per game; strategy games also sit in War, Brain, Mouse, Simulation, Tycoon, Tower Defense | to propose |
| Ad profile (desktop) | identical on all 10: `preroll: false`, first ad after 120,000 ms, then every 180,000 ms | see decisions |
| Store links | 3 of 10 (MicroWars, The Final Earth 2, War of Sticks) | none |

MicroWars is the nearest to Glob2 in theme: Poki's intro says "Command a colony of cells, expand your territory, and capture enemy nodes." It has 4.42 stars from about 230,000 votes. Poki's strategy page text names "real-time battles" and "help a small settlement grow into a city" as strategy sub-types. There is no RTS category: the `/en/rts` URL serves Tower Defense.

## How Poki works (from the docs)

- **Poki writes the page.** Every page uses the same template and voice. The developer supplies the game, the category, mobile orientations, thumbnails and a controls line.
- **Player Fit Test:** 500 players, usually about 5 hours, up to 2 tests a day. It "only measures playtime". **To pass:** average playtime over 3 minutes and at least 25% of plays over 3 minutes. Poki calls 3 minutes "the bar to advance". Stronger games average 5+ minutes, and **10+ for management and simulation games**. To unlock it: watch at least 10 playtest recordings and upload a thumbnail.
- **Thumbnail:**
  - square, at least 628×628, full-bleed, with no borders or letterboxing;
  - **no titles or other text**: Poki's tests found "visuals alone drive better performance";
  - "Visuals should closely match the actual game"; one clear foreground object; avoid Poki's background colour `#83FFE7`;
  - the animated thumbnail is added in Soft Release and is required before global release;
  - after the Web Fit Test passes, changes need Poki's sign-off, and after release only with a substantial content update.
- **Hard requirements:**
  - desktop, mobile and tablet support; 16:9 that scales to cover the canvas;
  - localStorage wrapped in try/catch; no external requests; no outgoing links except through `PokiSDK.openExternalLink`;
  - Esc or Space pauses keyboard games;
  - **no in-game purchases; Poki's SDK is the only ad system; implement `commercialBreak()` and/or `rewardedBreak()`**; playable with an ad blocker.
- **Size:** keep the download small; players tend to leave if loading takes more than 10 seconds. The page we read gives no hard limit. Poki's earlier requirements URL and the rollout record give about 8 MB initial download as the target.

## Inferences (not validated)

- **The Player Fit Test is the real gate, and it favours us on depth but not on the first minute.** A match runs long, so average playtime should be fine once a player is engaged. The risk is players who leave at the menu or in a slow early game before 3 minutes. Watching the 10 playtest recordings will show where they drop.
- **The thumbnail is the only marketing asset Poki lets us control**, and it must carry no text. Our key art leads with the wordmark, so Poki needs its own text-free image.
- **Glob2 sits between MicroWars-style capture games and builders like Village Builder.** Poki's 10-minute benchmark for management games suggests the colony-economy angle is the right lead.

## Limits

Ten games, one day. Poki's ranking of the category grid is not documented. The "most popular" list is Poki's own statement on the page. We cannot see Fit Test results for other games.

## Action list for our listing

Lite build only: no editor, online, LAN, 45 languages or 23 handmade maps, and no campaigns ([storefront claims](../facts/storefront-claims.md) R5). Poki writes the copy, so most of the work is assets and facts.

| # | Change | Evidence | Effort |
|---|---|---|---|
| 1 | **Make a text-free square thumbnail (at least 628×628) from a real in-engine capture**: a close crop on one clear subject, such as a busy inn or swarm with globs around it, on simple terrain. Check it at small tile size, keep it clear of `#83FFE7`, and make sure it matches what the lite build looks like (simpler terrain, no HD art). | Poki thumbnail rules; text-free tested better; our key art carries the wordmark. | Medium |
| 2 | **Make the animated thumbnail from lite-build footage** of a developed colony (footage rule), ready for Soft Release. | 10 of 10 top games have one; required for global release. | Medium |
| 3 | **Before applying, watch the first minutes as a new player would**: Poki shows recordings, and the pass bar is 3 minutes for 25% of plays. Make sure the first screen leads straight into the Tutorial or an introduction match. | Player Fit Test thresholds; "minimise menus" requirement. | Medium (may need a game change) |
| 4 | **Supply a one-line controls text and a fact sheet** for Poki's writers, using lite-safe approved lines: "Grow a colony and fight rivals for land: you set the priorities, your globs do the work." Controls: "Click or tap to place buildings and flags; drag to pan, wheel or pinch to zoom." | Poki's template and controls line on every page. | Low |
| 5 | **Category: Strategy; also suggest War and Simulation.** Set the mobile orientation to landscape unless portrait is tested. | Categories on MicroWars, War Masters and Village Builder; orientation mix in the sample. | Low |

**Decisions for the user**

- **Ads (blocking).** Poki's requirements say to implement `commercialBreak()` and/or `rewardedBreak()`, and every sampled game runs Poki's ad profile (first ad after 2 minutes, then every 3 on desktop). The game's "No ads" promise and Poki's model conflict. The options:
  1. accept Poki ads at natural pauses in the Poki build only, and never say "No ads" on Poki;
  2. ask Poki whether an ad-free game is acceptable (unlikely, as Poki is ad-funded);
  3. skip Poki.
- **Lite as the Poki edition**: forced by the size target in practice. The listing loses the editor, online and languages.
- **Tablet and mobile support is a hard requirement.** Lite worked by touch in the simulator, but no Android or real-device test has been done.
