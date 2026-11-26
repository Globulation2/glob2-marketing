# GameDistribution listing comparison

Observed 2026-11-26. GameDistribution (Azerion) is a distribution catalogue: publishers, meaning other game sites, pick games from it to embed. It is not a site players browse. "Top" therefore means what GameDistribution promotes to publishers.

Sources:

- **The public catalogue GraphQL API** that gamedistribution.com uses (`https://gd-website-api.gamedistribution.com/graphql`):
  - `collections`: Hot (320 games, ordered by `featuredGameOrder`), Exclusive (1,760), Best New (434), plus seasonal collections;
  - `gamesSearched` with `UIfilter: {genres: ["Strategy"]}`: 448 strategy games in total; the 9 Strategy games in Hot and the first 12 in Best New were read with their full metadata.
- **The public RSS/JSON catalogue feed** (`catalog.api.gamedistribution.com/api/v2.0/rss/All/?categories=Strategy…&format=json`), newest first.
- **SDK rules:** the [GD-HTML5 SDK Implementation wiki](https://github.com/GameDistribution/GD-HTML5/wiki/SDK-Implementation). The [quality guidelines page](https://gamedistribution.com/developers/quality-guidelines/) renders client-side and could not be read.

Our state: developer application submitted and awaiting approval; nothing listed. The plan packages the standard build ([web portal rollout](../planning/web-portal-rollout.md#gamedistribution-azerion)).

## What the promoted strategy games carry

Sample: 21 games (9 from Hot, 12 from Best New).

| Field | Promoted strategy games | Globulation 2 |
|---|---|---|
| Categories | 1–2 (Strategy alone, or with Puzzle or Battle) | to choose |
| Tags | median 5 (0–12), lowercase; common: `arcade`, `logic`, `1player`, `singleplayer`, `defence`, `tower`, `building`, `war`, `multiplayer` | to choose |
| Description | median 356 characters (131–615) | to write |
| Instructions | median 123 characters (13–409) | to write |
| Languages field | most list 0–2; one lists 15 | standard build: 45 |
| Mobile | 16 of 21 flag Android, 13 flag iOS; `mobileMode` portrait or landscape | to test |
| Audience fields | `ageGroup` (Kids, Teens, YoungAdults, Adults, Seniors) and `gender` set on most | to set |
| Assets | 2–5 images per game, from the standard set 512×512, 512×384, 200×120, 1280×720, 1280×550 | the key-art derivatives need these sizes |
| Frame size | 800×600 is the most common; also 1280×720, 1920×1080 and portrait sizes | 16:9 |

The publisher-facing catalogue filters on exactly these fields: `genres`, `languages`, `mobile_ready`, `players`, `IAPs`, `no_blood`, `no_cruelty`, `kids_friendly`, `developers`. The newest RSS entry, "Front Line", also tags itself "Kids Friendly" and "No Blood".

No real-time strategy game close to Glob2 was in Hot or Best New. Ant Colony (Hot; tags: `farm`) and Kingdoms Wars (Hot; tags: `1player`, `2players`, `3players`, `multiplayer`, `singleplayer`) are the nearest. A recent "Ant Empire: Colony Clash" shows colony themes are being added.

## How GameDistribution works

- **Ads are the product.** The SDK guide asks developers to make sure the game "includes a pre-roll and mid-rolls" before submitting. Pre-rolls go on start, play or continue buttons; mid-rolls go on game-over or win buttons such as Replay, Next or Menu.
  - Activation requires viewing the in-game pre-roll once.
  - Pause and mute on `SDK_GAME_PAUSE` and resume on `SDK_GAME_START`; audio during ads is forbidden.
  - Ads show only on user input and outside gameplay. The SDK sets the interval.
- **Review** "can currently take up to two weeks".
- **Exclusive collection.** It holds 1,760 games, an exclusivity deal; GPL Glob2 is free elsewhere.

## Inferences (not validated)

- **Publishers search with filters**, so filled metadata fields probably matter more than prose. A 45-language standard build is unusual in the sample, where most list one or two languages. It would show up in every language filter, but only if the languages field is filled in and the package is the standard build.
- **The ads conflict is sharper than on any other portal.** The SDK guide expects a pre-roll and mid-rolls, and GameDistribution earns only through them. A Glob2 build without ad calls may not be accepted, and would give publishers nothing to earn.
- **The standard build's 126 MB is a risk.** GameDistribution's size limit was not found. Publishers favour light games, and 800×600 frames are common.

## Limits

Collection order is editorial. The sample measures what GameDistribution promotes, not what publishers pick or players play. The quality guidelines could not be read. The `pageView` counts in the API are small (132–2,942) and of unclear meaning.

## Action list for our listing

To apply after the account is approved, and only after the ads decision below.

| # | Change | Evidence | Effort |
|---|---|---|---|
| 1 | **Fill every filter field accurately:** Category Strategy (alone); languages 45 (standard build) or English (lite); mobile flags only after a real-device test; players: 1 player (local); IAPs: none; age group Teens and up. Set `no_blood` / `no_cruelty` only after checking combat in-game. | Publisher filters in the catalogue API; most promoted games fill them. | Low |
| 2 | **Tags (about 5):** `real-time-strategy`, `singleplayer`, `building`, `war`, `strategy`. Gold Tower Defense uses `real-time-strategy`. Not `multiplayer` if the build is lite, or if portal mode hides online play. | Tag habits in Hot and Best New. | Low |
| 3 | **Description of about 350 characters and instructions of about 120**, from approved claims, adjusted for the build: standard can mention the 23 maps and the map editor; lite cannot. Leave out "No ads" (GameDistribution builds carry SDK ads), MCP and LAN. | Median lengths in the sample; [storefront claims](../facts/storefront-claims.md). | Low |
| 4 | **Export the five asset sizes** (512×512, 512×384, 200×120, 1280×720, 1280×550) from the key-art build script, using real game art. Check legibility at 200×120. | Asset set on every promoted game. | Low–medium |
| 5 | **Choose the build by size and features:** standard for the 45 languages, or lite (17.7 MB zip) for publishers' load times. Both need a tag with portal mode (#1927) and the Quit fix (#1938). | Language filter; frame sizes; rollout caveats. | Decision |

**Decisions for the user**

- **Ads (blocking):** the SDK guide expects a pre-roll and mid-rolls. Either add SDK ad calls to the GameDistribution build only (start button and end-of-match buttons) and drop "No ads" there, or withdraw from GameDistribution.
- **Standard or lite build** for GameDistribution (see action 5).
- **Exclusivity:** not recommended. It is not compatible with free distribution elsewhere.
