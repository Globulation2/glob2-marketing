# CrazyGames listing comparison

Observed 2026-11-26 from CrazyGames' public pages, read signed-out with `curl`. Each page embeds its data as Next.js `__NEXT_DATA__` JSON.

- **Category page:** `https://www.crazygames.com/c/strategy` (`topGames`: 15 entries; `topMobileGames`: 10). The default sort is not described on the page.
- **Game pages** (`/game/<slug>`) for the top 8: Mage Castle Idle Defense, Tower Swap, Bloons Tower Defense 4, Hex Empire, State.io, THE KING, World Conquest, Kingdom Rush. Plus four RTS-like games: Age of War, Stick War, Battle for the Galaxy, and Territorial.io, which had no game record.
- **Tag list:** `https://www.crazygames.com/tags`, 201 tags.
- **Developer rules** at docs.crazygames.com: [requirements](https://docs.crazygames.com/requirements/intro/), [gameplay](https://docs.crazygames.com/requirements/gameplay/), [game covers](https://docs.crazygames.com/requirements/game-covers/), [Basic Launch metrics](https://docs.crazygames.com/resources/basic-launch-metrics/), [FAQ](https://docs.crazygames.com/faq/).

Our state: developer portal set up, nothing submitted; the target is Basic Launch with the lite build ([web portal rollout](../planning/web-portal-rollout.md#crazygames)).

## What the top strategy games do

| Feature | Top strategy games (12 read) | Globulation 2 (planned) |
|---|---|---|
| Preview video on the tile | 15 of 15 top games | none made yet |
| Covers | all have 16:9, 2:3 and 1:1 | Key art exists; the 2:3 and 1:1 CrazyGames sizes are not made |
| Mobile friendly (iOS and Android) | 13 of the top 15 | lite build works by touch in the iPhone simulator |
| Tags | 4–12, typically 5–6; `Mobile` and `Mouse` are common | not chosen |
| Description | a lead paragraph of 15–64 words, then 0–340 words with H3 sections such as "How to Play", "Features", "Release Date", "Developer", "Platform" | not written |
| Controls field | one or two sentences; World Conquest splits it by PC and mobile | not written |
| Cloud save | 7 of 8 top games (`userProgressionSaveMessage: cloud`) | no CrazyGames SDK in Basic Launch |
| Store links on the page | 4 of 8 (App Store, Play, Steam) | none planned (Basic Launch) |
| Orientation | landscape, portrait and both all appear | landscape |

The strategy category is mostly tower defence, idle and territory-capture games. The closest to Glob2 are Stick War (9.3, 144,375 upvotes; Strategy; tags Defense, Building, War, Stickman, Bloody, Sword, Flash) and Age of War (9.3; filed under Action). CrazyGames has no RTS, base-building or colony tag. The nearest tags are `war`, `army`, `battle`, `build`, `management`, `mouse`, `mobile`, `2d` and `top-down`.

## How CrazyGames Basic Launch works (from the docs)

- **The test:** at least 7 days and at least 500 plays, ending after 21 days if 500 plays are not reached. KPIs are tracked automatically, without the SDK. **CrazyGames ads are off during Basic Launch**, and external ads are not allowed.
- **Benchmarks that successful titles typically reach** (no hard thresholds are stated):
  - average play time of 10+ minutes;
  - day-1 retention of 10–15%;
  - 80%+ of visitors converting to a play of at least one minute, with loading under 10 seconds and a build under 20 MB;
  - from games starting Basic Launch on or after **23 November 2026**, **cover click-through rate** in the top 20% of the category.
- **Limits:** initial download ≤ 50 MB; total ≤ 250 MB (50 MB without the SDK); ≤ 1,500 files; PEGI 12 content; English required.
- **Covers:** three required: 1920×1080 (16:9), 800×1200 (2:3) and 800×800 (1:1). The only text allowed is the title. No "New", "Play now", icons, store logos or borders. CrazyGames advises "don't just screenshot the gameplay": use a character, a big title or an evocative graphic.
- **Preview videos:** landscape 1080p 16:9 and portrait 1080p 2:3 are both mandatory. At most 15–20 seconds and 50 MB, no sound, no cursor, no promotional text, no black bars, no fast-forwarding. Start on the static cover.
- **Experiments tab:** A/B tests of covers and videos, once all three covers and both videos are published. One test at a time, at most two a month, up to 14 days each.
- **Links:** community links such as Discord or the developer site are allowed in the menu if they are not the main call to action and do not lead to a playable web version. App store links are never allowed. In-game fullscreen buttons are banned (CrazyGames provides fullscreen).
- **Updates:** game and art updates go live instantly during Basic Launch.

## Inferences (not validated)

- **The cover now feeds the launch decision.** The new CTR metric makes the three covers and two videos part of the Basic Launch result, not decoration. Every top game has a preview video.
- **Lite fits the conversion benchmark**: a 17.7 MB zip, about 8 MB before the game starts, against "under 20 MB" and under 10 seconds. The standard build (126 MB zip, 219 MB unpacked) breaks the 50 MB limit without the SDK.
- **Play time suits an RTS**: 10+ minutes per play is natural for a match. The risk is the first minute. Players land on a menu, and the conversion metric counts plays that reach one minute.
- **The genre is crowded with simpler games.** Saying "real-time strategy" and "build a colony" plainly, and showing a busy colony, separates us from tower defence. Tags cannot do it, because there is no RTS tag.

## Limits

One day's snapshot of one category page. We could not see what players are shown in Basic Launch or how many impressions it buys. Tags and description fields may be edited by CrazyGames after submission: the docs do not say who writes the public page.

## Action list for our listing

Lite build only, so the copy must not claim the map editor, online play, LAN, 45 languages or 23 handmade maps. Campaigns stay out too ([storefront claims](../facts/storefront-claims.md) R5).

| # | Change | Evidence | Effort |
|---|---|---|---|
| 1 | **Make both preview videos (16:9 and 2:3, 15–20 s, silent, no cursor) from lite-build footage** of a developed colony, following the [footage rule](../planning/gameplay-video.md). The 2:3 cut needs a portrait capture or a careful crop. | 15 of 15 top games have one; videos are mandatory and count towards CTR. | Medium |
| 2 | **Make the three covers from the "Shoreline colony" key-art plate** (real game art plus the wordmark only): 1920×1080, 800×1200 and 800×800. Use no "Free" or "No ads" text, which the rules ban. Check them at tile size. | Cover rules; CTR metric from 2026-11-23. | Medium |
| 3 | **Submit with the lite build only**, after a tag that includes the Quit fix (#1938). Exit buttons break inside the iframe, and CrazyGames bans custom fullscreen and exit controls. | Size limits; conversion benchmark; rollout defect note. | Low (the packaging is done) |
| 4 | **Description:** a lead paragraph of about 50 words built from approved lite-safe lines ("Grow a colony of globs and fight rival colonies for land. You decide what to build and where to send workers and warriors; your globs gather, build, eat and fight on their own."), then H3 "How to play" (start with the 10-lesson Tutorial; keep inns full before training an army) and "Features" (random maps from 67 landscapes, computer opponents, up to 16 colonies, replays). Before using any count, check it in the lite build: lite drops the JavaScript AIs, so "8 computer opponents" may not hold, and the replay and colony counts were not checked in lite. Put the controls in the Controls field, split by PC and mobile. | Pattern in the top games; World Conquest's PC and mobile split. | Low |
| 5 | **Tags (if CrazyGames lets us choose):** War, Battle, Army, Management, Build, Mouse, Mobile (only after a phone check on the real site). Not `Multiplayer` (lite has no online), not `Offline` (unverified for a browser game). | CrazyGames tag list; no RTS tag exists. | Low |
| 6 | **Shorten the path from page to play:** for first-time portal players, start the introduction match or Tutorial lesson 1 straight away instead of the main menu. | The 80% one-minute conversion benchmark; Full Launch requires landing in gameplay. | High (game-repository change) |

**Decisions for the user**

- **Ads after Basic Launch.** Basic Launch runs with no CrazyGames ads, so "no ads in the game" holds there. Full Launch requires ads through the CrazyGames SDK. Decide before Full Launch whether to accept SDK ads in the CrazyGames build, or to stay in Basic Launch / reach-only. The listing should not say "No ads" either way: the site runs its own.
- **Lite as the CrazyGames edition**, given what it drops (editor, online, 44 languages). The decision is effectively forced by the 50 MB limit without the SDK.
- **Community link in the menu.** Allowed if it is not the main call to action and does not lead to a playable web version. Discord passes that test; glob2.online offers browser play, so it may not.
