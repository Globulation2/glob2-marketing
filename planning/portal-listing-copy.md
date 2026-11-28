# Web portal listing copy

[Planning index](README.md) · [Web portal rollout](web-portal-rollout.md) · [GamePix launch](gamepix-launch.md) · [Storefront claims](../facts/storefront-claims.md) · [English source](../translations/en.md) · [Working rules](../AGENTS.md#web-portal-ads--2026-11-26)

Prepared 2026-11-26. This is paste-ready copy for every field each web portal asks for. **Evidence level: prepared.** Nothing here has been entered on any portal, and no live listing was changed while writing it. Game Jolt is live and out of scope here; its listing is covered in the [Game Jolt listing comparison](../analysis/gamejolt-listing-comparison.md).

## Authority and rules applied

- The user authorized the per-portal recommendations on 2026-11-26 ([Web portal ads](../AGENTS.md#web-portal-ads--2026-11-26)). They are the "Action list" sections of the six comparisons: [Newgrounds](../analysis/newgrounds-listing-comparison.md), [GamePix](../analysis/gamepix-listing-comparison.md), [CrazyGames](../analysis/crazygames-listing-comparison.md), [Poki](../analysis/poki-listing-comparison.md), [GameDistribution](../analysis/gamedistribution-listing-comparison.md) and [Yandex Games](../analysis/yandex-games-listing-comparison.md).
- **Ads.** The Poki, GameDistribution, Yandex, CrazyGames and GamePix packages will carry portal ads, so their copy never says "No ads" or "ad-free" in any form. It may say "No in-app purchases" and "No loot boxes". Newgrounds stays ad-free in the game, so "no ads" is used there, scoped to the game itself because Newgrounds shows its own site ads (NG-4).
- **Claims rows used** from [storefront claims](../facts/storefront-claims.md): §1 monetisation, §3 gameplay facts, R5 (no campaigns: never claimed), R12 (nearly empty online service: no quick online opponents, no busy-community wording), §2 (MCP is not in any browser build: never mentioned), §5 (browser: no LAN). "First" is not written anywhere. Images and video are out of scope here; any listed for a field must follow the real-game-art and footage rules.
- **Evidence notes** under each field cite the recommendation as portal code plus action number (NG, GP, CG, PK, GD, YA; for example NG-1 is Newgrounds action 1) and the claims row or section.

## What each build can claim

| Claim | Standard, ad-free (Newgrounds) | Standard, ads, portal mode (GamePix, GameDistribution) | Lite, ads (CrazyGames, Poki, Yandex) |
|---|---|---|---|
| No ads (in the game) | yes, scoped to the game | **no** | **no** |
| No in-app purchases, no loot boxes | yes | yes | yes |
| 23 handmade maps | yes | yes | **no** (premade maps removed) |
| Random maps from 67 landscapes | yes | yes | yes |
| Computer opponents | 8, easy to hard | 8, easy to hard | **7** (see below) |
| Up to 16 colonies | yes | yes | yes |
| 10-lesson tutorial | yes | yes | yes |
| Replays | yes | yes | yes |
| Map editor | yes | yes | **no** |
| Online room with an invite code | **no** (decided 2026-11-27: the online service refuses cross-site requests, so portal pages cannot connect) | **no** (portal mode hides online) | **no** (online removed) |
| 45 languages | yes | yes | **no** (English only) |
| LAN, MCP | no | no | no |
| Campaigns | never (R5) | never | never |

## Lite facts verified in the game source

Read on 2026-11-26 in the glob2 repository at master `6260faaaa1`. None of the files below changed between tag `v0.11.8.2` (the packaged release) and that commit.

- **Lite turns every feature switch off.** `buildsys/edition.py`: `PRESETS['lite']` sets every entry of `FEATURES` to False, including `editor`, `online`, `lan`, `mcp`, `ai_maxima`, `js_toolkit`, `translations` and `premade_maps`. `.github/workflows/browser-release.yml` builds lite with plain `edition=lite` and no overrides.
- **7 computer opponents, Easy and Medium only.** `src/ai/AIRegistry.cpp` `available()`: Maxima returns `GLOB2_HAS_AI_MAXIMA`, the JavaScript AI returns `GLOB2_HAS_JS_TOOLKIT`, and both are 0 in lite. Castor, Cortex and Cabino depend only on the compile profile, and `buildsys/dev_build.py` makes web builds use the full profile. `src/ai/AINames.cpp` `selectionOrder()` therefore offers Numbi, Castor, Econo and Warrush (Easy) and Cortex, Nicowar and Cabino (Medium). The only Hard opponent, Maxima, is missing, so "from easy to hard" is not true of lite. `docs/browser/editions.md` agrees: "no Maxima AI", "no JavaScript AIs".
- **Random landscapes: 67, with no edition gate.** `src/map/generator/core/GeneratorRegistry.cpp` includes 68 generators, one of them the editor-only `uniform` (claims §3), and contains no edition switch. The only JavaScript-toolkit gates in the generators remove script blueprints in `EvenGroundGenerator.cpp` and `FortsGenerator.cpp`, not generators. `buildsys/web_assets.py` `edition_export` removes only `maps/` for `premade_maps` ("random maps and campaign missions remain").
- **10 tutorial lessons.** `content/scripts/tutorials/catalog.json` has 10 entries. Tutorial scripts keep QuickJS (`docs/browser/editions.md`, `js_toolkit` row).
- **16 colonies.** `src/team/TeamCapacity.h`: `TEAM_MAX_COUNT = 16`, with no edition gate.
- **Replays.** `src/game/screens/EndGameScreen.cpp` offers "save replay" with no edition gate. The `recording` switch removes only gameplay video recording (`SettingsScreen.cpp`, `Application.cpp`).
- **Menus.** `src/ui/screens/MainMenuScreen.cpp` gates only Online (and the portal's sign-in policy), LAN and Editor.
- **Checked in source only.** These counts were not exercised in a running lite build. The rollout's simulator runs confirm only that lite loads and plays a match.

## Shared controls (all builds)

The desktop controls come from the approved GamePix How to Play ([GamePix launch](gamepix-launch.md#how-to-play-and-art-2026-11-26)), which is based on the website's controls guides. Middle-drag panning comes from `docs/features/torus-experiment.md` in the game repository ("Middle-drag follows the ordinary map panning path"). The touch controls come from the game's touch-controls documentation and were observed in the web build on 2026-11-26. The UI is the same in lite, apart from the hidden menu entries.

---

## Newgrounds

Project 8315233, a draft saved with 0.11.8.2. **Standard build, no ads in the game.** External links and online sign-in are kept.

**Title:** Globulation 2
- Evidence: unchanged `product_name` ([en.md](../translations/en.md)).

**Short description (88 characters):**

> Grow a colony and fight rivals for land: you set the priorities, your globs do the work.

- Evidence: NG-1 (a concrete, verb-first line under about 90 characters), word for word. Built from `short_pitch` and `headline` claims.

**Genre:** Strategy - Real-time (RTS)
- Evidence: Newgrounds comparison, "Genre field". Unchanged from the draft.

**Author comments (about 230 words):**

> Not a demo: this is the free browser version of Globulation 2, a real-time strategy game about a colony of globs. New here? Start with the 10-lesson Tutorial from the main menu.
>
> You don't control units one by one. Choose what to build and how many globs should work on it; they gather the materials, build it, and eat when they are hungry. To explore or attack, place a flag and set how many globs should go. Inns feed the colony, swarms grow it, and schools, barracks and hospitals train and heal it. Every new project takes workers from another, so a bigger army is no use if nobody is left to harvest the wheat.
>
> Features:
> - 23 handmade maps, plus new maps from 67 random landscapes
> - 8 computer opponents, from easy to hard
> - Up to 16 colonies in one match
> - A 10-lesson tutorial
> - Built-in map editor
> - Save and watch replays
> - Available in 45 languages
>
> The game itself has no ads, no in-app purchases and no loot boxes. Globulation 2 is free and open source (GPLv3). It was started in 2001 and has been built by volunteers over two decades.
>
> AI disclosure: this remaster includes AI-assisted code contributions, some AI-generated terrain and some AI-enhanced sprites.
>
> Desktop versions for Windows, macOS and Linux: https://glob2.online/

- Evidence: NG-2 (open with what the game is and where to start, avoid "complete", a "Features" list, 150–250 words). NG-4: "no ads" scoped to the game. Feature lines from claims §3. The online rooms line was cut on 2026-11-27 (owner decision 4): `https://app.glob2.online` sends no cross-origin headers and answers CORS preflight with 404, so a Newgrounds-hosted page cannot reach it. Heritage from claims §4. The link is allowed because the Newgrounds package keeps external links (rollout).
- No MCP (claims §2: not in browser builds), no LAN (§5), no campaigns (R5), no quick-match line (R12).
- AI disclosure (added 2026-11-27, approved by the owner and entered on the Newgrounds draft the same day, verified after a reload): Newgrounds requires disclosing any AI use in the author commentary ([other portals audit](../analysis/other-portals-requirements-audit.md), NG-9). Wording matches the maintainer-reviewed line in [the Linux and preservation Reddit draft](reddit-campaign/linux-and-preservation.md).

**Tags (8):** strategy, rts, real-time-strategy, colony, base-building, economy, open-source, map-editor
- Evidence: NG-7, taking its optional swap of `multiplayer` for `real-time-strategy`, because online play does not work from the portal (owner decision 5, accepted 2026-11-27).

**Content rating:** T. Violence: "Some" (cartoon combat). Everything else: None.
- Evidence: the draft as saved. Newgrounds comparison, "Decisions for the user" (T is the safe choice). Owner decision 6: T, accepted 2026-11-27.

**Touchscreen friendly:** tick it only if a phone-sized test of the published page shows the phone layout. Otherwise untick it.
- Evidence: NG-3 (the page has two viewport tags). Rollout, "Phone layout depends on the portal page".

**Uses SharedArrayBuffer/Cross Origin Isolation:** off. **Allow Embedding:** off. **Embed size:** 1280×720.
- Evidence: Newgrounds comparison decisions. Both switches are kept as saved until the owner decides otherwise.

**Medals and scoreboards:** none.
- Evidence: NG-6 is a game-repository change (Newgrounds.io integration), not a listing field.

**Languages:** Newgrounds has no language field in the draft form as recorded. The 45 languages are stated in the author comments instead.

**Publish timing:** publish when someone can answer the first comments during judgment (NG-5). Publishing waits for the owner's go-ahead.

---

## GamePix

Draft entry BL8O73. **Standard build, portal mode, with ads.** Online play and external links are hidden. Field limits come from the [GamePix launch](gamepix-launch.md) record.

**Title:** Globulation 2
- Evidence: the approved title (GamePix launch, "Approved copy").

**Main tag:** Strategy. **More tags:** War, City Building, Management, Simulation
- Evidence: GP-5 (keep the five). No Multiplayer tag: online is hidden in this build.

**Description (443 of 100–500 characters), replacing the approved 449-character text (owner decision 7, accepted 2026-11-27):**

> Grow a colony of globs and fight rival colonies for land in this real-time strategy game. You never steer single units: choose what to build and how many globs work on it, then place flags to explore or attack. Your globs gather, build, eat and fight on their own. Keep the inns full, train warriors and defend your borders before rivals take the best ground. Click or tap to build and place flags; drag or use the arrow keys to move the view.

- Evidence: GP-3 (move the controls to How to Play and free the space for gameplay). GamePix's form requires the description to explain the controls, so one short controls sentence stays. Claims from `control_body`, `economy_body` and `defense_body`. The wording is new, as GamePix asks for original text.

**How to Play – Instructions (497 of 500 characters):** keep the saved text unchanged. It is in [GamePix launch](gamepix-launch.md#how-to-play-and-art-2026-11-26).
- Evidence: saved and verified on 2026-11-26. It contains no ads, online or MCP claims.

**Custom Section.** Title (13 of 35 characters):

> Game features

Body (239 of 350 characters):

> 23 handmade maps, plus new maps from 67 random landscapes. 8 computer opponents, from easy to hard. Up to 16 colonies in one match. A 10-lesson tutorial. A built-in map editor. Save and watch replays. No in-app purchases and no loot boxes.

- Evidence: GP-3 (a "Game features" section, as on OpenTTD). Claims §3 for every count. The editor and replays are in the GamePix build (GamePix launch, "What the GamePix build contains"). Monetisation wording follows the ads rule.

**FAQs** (questions at most 80 characters, answers at most 150):

| Question | Characters | Answer | Characters |
|---|---|---|---|
| Do I control each unit? | 23 | No. You choose what to build and where to send workers and warriors; your globs do the work on their own. | 105 |
| How do I win? | 13 | Defeat the rival colonies. Depending on the match rules, a prestige goal or a time limit can also end the game. | 111 |
| Where should I start? | 21 | Play the 10-lesson Tutorial from the main menu. It covers food, healing, training, upgrades and defense. | 104 |
| Does it cost anything? | 22 | No. The game is free, with no in-app purchases and no loot boxes. | 65 |

- Evidence: GP-2. The victory wording was checked against `docs/features/custom-game-setup/README.md` in the game repository, which lists win reasons: opponents defeated, prestige, time limit, and others. The lesson topics come from claims §3 (tutorial catalogue). The fourth FAQ is monetisation (claims §1) without "No ads".

**Video:** https://www.youtube.com/watch?v=BJoMHyCxzkg, the unlisted textless gameplay cut (owner decision 2). Replacement from the V2 re-record: https://www.youtube.com/watch?v=O2chQJ8nTkU (unlisted, 2026-11-28), to set once GamePix's current review clears.
- History: GP-1 recommends the YouTube trailer `t6Q3ZpY9aTM`. That cut shows the end card "No ads. No in-app purchases." ([trailer manifest](../assets/storefront/trailer/manifest.json), `text_cards`), and its YouTube description carries `fair_deal_line` ("No ads."). Both break the ads rule on an ad-enabled package. A textless 30 s cut exists (`glob2-trailer-30s-textless-1080p.mp4`, not committed). It would need its own YouTube upload, and its footage would need checking for online, link and MCP screens. See owner decision 2.

**Orientation:** Landscape (change from All). **Desktop friendly / Mobile friendly:** on.
- Evidence: GP-4 (63 of 96 strategy games are landscape). Return to All only if a portrait phone test passes.

**Allow distribution:** not changed here. This is an open owner decision (GamePix launch, decision 4).

**Languages:** no listing field. The game picks the player's language itself.

---

## CrazyGames

Not submitted. **Lite build. Ads are off in Basic Launch and come through the CrazyGames SDK at Full Launch**, so the copy never claims no ads. The field names come from CrazyGames' documentation and the public game pages. The submission form itself has not been observed.

**Title:** Globulation 2
- Evidence: `product_name`. CrazyGames covers allow only the title as text (CG-2).

**Category:** Strategy
- Evidence: the CrazyGames comparison. Strategy is the only fitting category, and there is no RTS category.

**Description, lead paragraph (285 characters, 51 words):**

> Grow a colony of globs and fight rival colonies for land in this real-time strategy game. You decide what to build and where to send workers and warriors; your globs gather, build, eat and fight on their own. Keep them fed, train an army and take the best ground before your rivals do.

- Evidence: CG-4 (a lead of about 50 words built from lite-safe lines, close to its own example). `control_body` and `defense_body` claims.

**Description, H3 "How to play":**

> Start with the 10-lesson Tutorial from the main menu: it teaches food, healing, training, upgrades and defense one step at a time. In a match, build inns early and keep them full, because an attack lasts only as long as the food that supports it. Then train warriors and place a war flag where your army should attack.

- Evidence: CG-4 ("start with the 10-lesson Tutorial; keep inns full before training an army"). `defense_body` (war flags, food supports attacks). Claims §3 (tutorial).

**Description, H3 "Features":**

> - Command the colony, not every unit
> - New random maps from 67 landscapes
> - 7 computer opponents
> - Up to 16 colonies in one match
> - A 10-lesson tutorial
> - Save and watch replays
> - No in-app purchases and no loot boxes

- Evidence: CG-4, with every count checked in the lite source (see "Lite facts verified" above). The count is 7, not 8, and the line does not say "easy to hard". There is no editor, no handmade maps, no online play and no 45 languages. Monetisation follows the ads rule.

**Controls (276 characters):**

> PC: left-click to select, or to place the chosen building or flag; right-click to cancel; arrow keys, middle-drag or the minimap move the view; mouse wheel zooms. Mobile: tap to select or place; drag to pan; pinch to zoom; the Build, Flags and Tools buttons are at the bottom.

- Evidence: CG-4 (put the controls in the Controls field, split by PC and mobile, as World Conquest does). Shared controls source above.

**Tags:** War, Battle, Army, Management, Build, Mouse, and Mobile only after a real-device phone check on the CrazyGames preview.
- Evidence: CG-5. All are on CrazyGames' tag list. No Multiplayer (lite has no online) and no Offline (unverified for a browser game).

**Orientation:** landscape. **Mobile (iOS and Android):** declare it only after a real-device test. Lite has played by touch only in the iPhone simulator.
- Evidence: CrazyGames comparison table. Rollout results table.

**Content rating:** within CrazyGames' PEGI 12 limit. Declare mild cartoon or fantasy violence, and no user interaction (lite has no online or chat).
- Evidence: the CrazyGames rule "PEGI 12 content". Claims §6: the Microsoft Store IARC rating is PEGI 3, ESRB E for mild fantasy violence. "Users Interact" in that rating comes from online play, which lite does not have.

**Languages:** English.
- Evidence: CrazyGames requires English. Lite is English only (`translations` switch).

**Community link in the menu:** none. Portal mode hides links, and the owner decision is still open (CrazyGames comparison).

**Not filled:** the three covers and two preview videos (CG-1, CG-2) are assets, not copy. CG-3 and CG-6 are build and game changes.

---

## Poki

Not applied. **Lite build, Poki SDK ads.** Poki writes the public page itself (intro, description and FAQ template). We supply the controls line, a category, the orientation and facts for Poki's writers. The form fields are taken from Poki's developer guide. The submission form has not been observed.

**Game name:** Globulation 2

**Controls line (103 characters):**

> Click or tap to place buildings and flags; arrow keys or drag to move the view, wheel or pinch to zoom.

- Evidence: PK-4. Its suggested line was corrected for desktop, where the view moves with the arrow keys or middle-drag, not a left-drag. Shared controls source above.

**Category:** Strategy. Also suggest War and Simulation.
- Evidence: PK-5 (categories used by MicroWars, War Masters and Village Builder).

**Mobile orientation:** landscape. **Desktop, mobile and tablet:** required by Poki. This is unverified on a real device (see owner decisions).
- Evidence: PK-5. Poki's hard requirements. Rollout results table.

**Fact sheet for Poki's writers** (paste as notes):

> - One line: Grow a colony and fight rivals for land: you set the priorities, your globs do the work.
> - What it is: a real-time strategy game about a colony of globs, small creatures that work, eat, train and fight. You choose what to build and how many globs work on it, and place flags to explore or attack; the globs do the work on their own.
> - Content: new random maps from 67 landscapes, 7 computer opponents, up to 16 colonies in one match, a 10-lesson tutorial, replays.
> - Where to start: the Tutorial from the main menu.
> - Monetisation: free; no in-app purchases and no loot boxes. Poki's ads only.
> - Who made it: an open-source game (GPLv3) started in 2001 and built by volunteers over two decades.
> - Please do not mention: a map editor, online or multiplayer play, handmade maps, other languages or campaigns. This edition has none of them.

- Evidence: PK-4 (fact sheet built from lite-safe approved lines). Lite facts verified above. Claims §1 and §4. R5. The ads rule. The last line exists because Poki's writers might otherwise draw on our other pages.

**Thumbnail and animated thumbnail:** not filled. They are assets (PK-1, PK-2). Poki bans any text on them.

**Age rating, languages:** Poki's guide asks for neither. Lite is English only.

---

## GameDistribution

Developer application awaiting approval. **Standard build (per the brief), portal mode, GameDistribution SDK pre-roll and mid-rolls.** Online play and external links are hidden.

**Title:** Globulation 2

**Description (351 characters):**

> Grow a colony of globs and fight rival colonies for land. You choose what to build and where to send workers and warriors; your globs gather, build, eat and fight on their own. Play 23 handmade maps or new maps from 67 random landscapes against 8 computer opponents, with up to 16 colonies in one match. Includes a 10-lesson tutorial and a map editor.

- Evidence: GD-3 (about 350 characters; standard may mention the 23 maps and the editor; no "No ads", MCP or LAN). Claims §3.

**Instructions (140 characters):**

> Click or tap to build and place flags. Right-click cancels. Arrow keys or drag move the view; wheel or pinch zooms. Start with the Tutorial.

- Evidence: GD-3 (about 120 characters; the sample median is 123). Shared controls source.

**Category:** Strategy (alone).
- Evidence: GD-1.

**Tags:** real-time-strategy, strategy, singleplayer, building, war
- Evidence: GD-2. No `multiplayer`, because portal mode hides online play.

**Languages:** all 45 in-game catalogues: English, Arabic, Basque, Bengali, Bulgarian, Catalan, Chinese (Simplified), Chinese (Traditional), Czech, Danish, Dutch, Esperanto, Filipino, Finnish, French, German, Greek, Hindi, Hungarian, Indonesian, Italian, Japanese, Korean, Malay, Marathi, Norwegian Bokmål, Persian, Polish, Portuguese, Portuguese (Brazil), Romanian, Russian, Serbian, Slovak, Slovenian, Spanish, Swahili, Swedish, Tamil, Telugu, Thai, Turkish, Ukrainian, Urdu, Vietnamese.
- Evidence: GD-1. Claims §3 "45 languages", with the caveat that all 44 non-English catalogues are flagged incomplete. The list was read from `content/data/texts.list.txt` in the game repository. Pick only the entries GameDistribution's own list offers. That list has not been seen.

**Players:** 1 player. **IAPs:** none. **Mobile (Android, iOS):** off until a real-device test passes. **Mobile mode:** landscape.
- Evidence: GD-1. Claims §1 (no in-app purchases).

**Age group:** Teens, YoungAdults, Adults, Seniors. **Gender:** leave unset, or all.
- Evidence: GD-1 ("Teens and up"). No evidence supports targeting a gender.

**`no_blood`:** on. **`no_cruelty`:** on. **`kids_friendly`:** off.
- Evidence: combat checked 2026-11-27 (owner decision 8). The game shows no blood: a unit's death is a green sparkle that fades (`content/data/gfx/death0r.png` to `death9r.png`, 32×32), and warriors fight without wounds or gore. Nothing tortures or mistreats creatures. `kids_friendly` stays off because the age group is Teens and up (GD-1) and the game has real combat and starvation ("dying hungry"). One ruleset is named "Bloodbath" ("Fragile, fearless armies"), but that is only a name; nothing bloody is drawn.

**Frame size:** 1280×720 (16:9).
- Evidence: GameDistribution comparison table.

**Assets:** not filled. The five image sizes are GD-4, an asset task.

---

## Yandex Games

**Parked.** The console is not accepting new developer applications (YA-1). The copy is prepared for when it reopens. **Lite build, Yandex SDK ads** (rule 1.12 requires monetisation). Yandex requires separate Description and How to play texts that do not duplicate each other (5.11).

**Title:** Globulation 2, identical in the game and the draft (5.1.3).

**Description, English (388 characters):**

> Globulation 2 is a real-time strategy game about a colony of globs: small, busy creatures that work, eat, train and fight. You choose what to build and how many globs should work on it, and place flags to explore or attack. Grow the colony, keep it fed and take land from rival colonies on random maps from 67 landscapes, against 7 computer opponents, with up to 16 colonies in one match.

- Evidence: YA-2. `listing_intro` and `control_body` claims. Lite counts verified above. It makes no claim about ads, as required by the ads rule and Yandex 1.12.

**How to play, English (345 characters):**

> Start with the 10-lesson Tutorial in the main menu. Mouse: left-click to select or place a building or flag, right-click to cancel, arrow keys or middle-drag to move the view, wheel to zoom. Touch: tap to select or place, drag to pan, pinch to zoom. Build inns early and keep them full: an attack lasts only as long as the food that supports it.

- Evidence: YA-2. Yandex 2.2 (describe the controls). Shared controls source. This text has no sentences in common with the Description.

**Description, Russian** (assembled word for word from the reviewed storefront catalogue [ru.md](../translations/ru.md), fields `listing_intro` and `control_body`):

> Globulation 2 — стратегия в реальном времени о колонии глобул: маленьких деловитых существ, которые работают, едят, тренируются и сражаются. Вы развиваете колонию, следите, чтобы она была сыта, и боретесь с колониями-соперниками, которым нужна та же земля.
>
> Выбирайте, что строить и сколько глобул будет над этим работать. Они сами находят дорогу, собирают материалы и строят, а когда проголодаются — едят. Чтобы разведать новые земли или напасть на соперника, поставьте флаг и укажите, сколько глобул должно туда отправиться. Здесь нет юнитов, которых нужно выделять по одному: вы строите планы для всей колонии.

- Evidence: YA-2 (Russian from the reviewed catalogue). The review was AI only, with no native speaker ([translation review](storefront-translation-review.md)). It contains no counts that differ in lite.
- **How to play in Russian: not filled.** The catalogue has no controls text, and new Russian copy would need its own review.

**Categories:** Strategy. Yandex's category list was not observed, so choose the nearest match there.

**Age rating:** 12+, the conservative choice for cartoon combat (owner decision 9, accepted 2026-11-27).
- Evidence: Yandex 2.7 (the rating must match the content). Claims §5: the iOS listing shows 12+/13+, and Microsoft's IARC rating is PEGI 3. See owner decision 9.

**Languages:** English (the game). Russian for the listing only, if Yandex accepts listing-only localisation (8.2.3). Ask Yandex first (YA-2).

**Video, screenshots, icon, cover:** not filled. They are assets. Video must be self-hosted, with no YouTube (3.9).

---

## Fields not filled, and why

| Portal | Field | Why |
|---|---|---|
| GamePix | Video | The only trailer on YouTube shows a "No ads" card. A textless cut needs uploading and checking (owner decision 2) |
| GameDistribution | Exact language entries | GameDistribution's picklist has not been seen |
| Yandex | How to play (Russian), categories | No reviewed Russian controls text. The category list has not been observed |
| CrazyGames, Poki, Yandex, GameDistribution | Mobile flags | Real-device test not done (simulator only) |
| Newgrounds | Touchscreen friendly | Depends on a phone-sized test of the published page (NG-3) |
| All | Covers, thumbnails, preview videos, asset sizes | Asset work under the real-game-art and footage rules, not copy |
| Poki, CrazyGames | Exact form field names | Submission forms not yet seen. The fields follow each portal's developer documentation |

## Owner decisions

All nine were resolved on 2026-11-27, when the owner accepted every recommendation ("I accept your recommendations on all of these issues").

1. **Lite opponents:** "7 computer opponents", with no "easy to hard". Already used in the CrazyGames, Poki and Yandex copy.
2. **GamePix video:** the textless 30 s cut. Already done on 2026-11-26: it is the unlisted YouTube video https://www.youtube.com/watch?v=BJoMHyCxzkg ("Globulation 2 gameplay"), set on the GamePix draft ([rollout](web-portal-rollout.md#gameplay-video-for-ad-enabled-portals-2026-11-26)). Re-checked 2026-11-27: still in the GamePix Video field.
3. **Trailer `t6Q3ZpY9aTM`:** never embedded on an ad-enabled portal (unchanged).
4. **Newgrounds online rooms line:** cut. `https://app.glob2.online` answers a CORS preflight with 404 and sends no `Access-Control-Allow-Origin`, so the game on a Newgrounds (or Game Jolt) page cannot sign in or join rooms.
5. **Newgrounds tags:** `real-time-strategy` replaces `multiplayer`. The draft already had the swap when checked on 2026-11-27. The online-rooms bullet was removed from the draft's author comments the same day and verified after a reload.
6. **Newgrounds rating:** T.
7. **GamePix description:** the gameplay-led 443-character text. Already saved on the GamePix draft on 2026-11-26 and re-read on 2026-11-27. The GamePix changes are in an unsubmitted new release, which waits for the next patch.
8. **GameDistribution content flags:** `no_blood` and `no_cruelty` on, `kids_friendly` off, after the combat check recorded under GameDistribution.
9. **Yandex age rating:** 12+.
