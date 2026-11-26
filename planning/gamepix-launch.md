# GamePix launch

[Planning index](README.md) · [Storefront v2 rollout](storefront-v2-rollout.md) · [Game repo: GamePix release guide](https://github.com/Globulation2/glob2/blob/master/docs/releases/gamepix.md) · [Game repo: web portals](https://github.com/Globulation2/glob2/blob/master/docs/releases/web-portals.md)

[GamePix](https://www.gamepix.com/) is a web games platform owned by Xsolla. It hosts HTML5 games in an iframe on its own site.

## Status — 2026-11-26

| State | GamePix |
| --- | --- |
| Prepared | Release pipeline builds a verified GamePix upload; listing copy approved |
| Saved on GamePix | Draft game entry [BL8O73](https://my.gamepix.com/games/globulation-2) with the approved title, tags and description and the Info settings. No assets, no How to Play and no build attached |
| Submitted for review | No |
| Publicly live | No |

Done:
- Outreach answered.
- Developer account registered by the owner.
- Upload built in CI and verified in GamePix's Testing Toolkit.
- Terrain defect found and fixed in the game.
- Listing copy approved.
- Draft game entry created and its Info settings saved.

Blocked:
- **The next game release.** It carries the terrain fix ([#1932](https://github.com/Globulation2/glob2/pull/1932)). The owner is holding the patch release for other fixes.
- **GamePix's answers** on links and online play.
- **The owner's decision on ads on web portals.**
- **The owner's decision on Allow distribution**, which GamePix turned on by default.
- **The rest of the entry:** How to Play copy, icon, cover and a build.

## Game entry created — 2026-11-26

At the owner's instruction ("Yes, create it"), the coordinating agent created the draft entry on the dashboard. Nothing was submitted for review.

**Create New Game** saved:
- title "Globulation 2";
- main tag `strategy`, plus `war`, `city-building`, `management` and `simulation`;
- the approved 449-character description;
- Game Jam: None.

The dashboard reported "Game successfully created!". The entry is Game Id `BL8O73` at <https://my.gamepix.com/games/globulation-2>.

**Info tab**, saved and verified after a fresh reload:
- Orientation: All.
- Desktop friendly and Mobile friendly: on.
- Game engine: Other. The game is C++ compiled to WebAssembly, and none of the listed engines fit.
- SDK integration: on.
- Multiplayer SDK integration: off.
- Allow distribution: on. This was GamePix's default and was left unchanged. It lets GamePix syndicate the game to third-party sites, and is an open owner decision.

**The other tabs**, as observed and not yet filled:
- **Assets:**
  - Icon: 256×256, at most 1 MB, JPG or PNG.
  - Cover: 1360×850, at most 1.5 MB, JPG or PNG.
- **Editorial:**
  - Description: done.
  - How to Play – Instructions: required, up to 500 characters, controls first, organised by platform.
  - Custom Sections: optional, titles up to 35 characters, content up to 350.
  - Video: optional, a YouTube or Vimeo link to footage that belongs to us.
  - FAQs: optional, questions up to 80 characters, answers up to 150.
- **Build:**
  - Either upload a `.zip` or `.gpx` with `index.html` at the root, up to **2 GB**, or set a Game URL.
  - A preview link valid for 24 hours can be generated.
- **Submit for review:** not touched.

**Proposal, not decided.** The Build tab's Game URL option would let us host the GamePix package ourselves, next to the browser release, so each release updates GamePix automatically. That is the itch-style automation the owner asked for. It needs two things: a hosting location serving the GamePix package, and GamePix's confirmation that URL-hosted games are allowed under their relative-path rule.

## Defect found and fixed — 2026-11-26

In the Testing Toolkit, terrain drew as flat colour. The same happened on the live direct browser build at <https://storage.googleapis.com/glob2-browser/index.html>. Both use the single-threaded browser runtime, which runs on any host without cross-origin isolation headers. The HD terrain mask builder tried to start worker threads, which that runtime cannot create. The terrain then fell back to flat colour for every material.

[#1932](https://github.com/Globulation2/glob2/pull/1932) builds the masks on the main thread when threads are unavailable. It merged on 2026-11-26, and the master fast gate passed on the first commit that includes it. A local single-threaded web build showed textured grass, sand and water in the menu and the introduction map. The fix reaches players with the next release; no patch release has been cut.

## Testing Toolkit verification — 2026-11-26

The owner uploaded the CI-built `glob2-0.11.8.1-gamepix.zip` to the dashboard's SDK Testing Toolkit. That is a test harness only: no game entry is created and nothing is submitted.

- GamePix served the files from `test.builds.gamepix.com` (Amazon S3). They returned HTTP 403 for a few minutes after the upload, then loaded.
- The game reached the introduction map inside the toolkit's frame.
- The toolkit's debug console logged:
  - `LOADING` 1 to 100;
  - `LOADED` and `GAME_START`;
  - `FIRST_INTERACTION`, which the SDK sends itself;
  - `PAUSE` and `RESUME` from the toolkit's manual buttons.
- Not verified: that audio actually goes silent during pause. The game runs in a cross-origin frame, so this needs listening with the toolkit's audio-stop tab.
- The test host sends no COOP/COEP headers, so players on GamePix get the single-threaded runtime.

## Release pipeline — 2026-11-26

Work in the game repository. Every browser release now also produces the GamePix upload.

| Change | What it does |
| --- | --- |
| [#1924](https://github.com/Globulation2/glob2/pull/1924) | `gamepix` job in `browser-release.yml`; `package-gamepix.py` repackages the verified browser release; `gamepix.js` reports loading and silences audio on pause |
| [#1925](https://github.com/Globulation2/glob2/pull/1925) | Packages with the workflow's own script, so older tags work; a `publish` switch builds uploads without replacing the live browser game |
| [#1926](https://github.com/Globulation2/glob2/pull/1926) | Generalised into `package-portal.py` for every web portal; the GamePix profile enforces the 200 MB Testing Toolkit limit (the game Build tab accepts up to 2 GB) |
| [#1927](https://github.com/Globulation2/glob2/pull/1927) | Portal mode: GamePix builds run with external links and online sign-in turned off |
| [#1931](https://github.com/Globulation2/glob2/pull/1931) | Closed as superseded by #1926 |

Test run: [browser-release 45852515327](https://github.com/genixpro/glob2-release/actions/runs/45852515327), tag `v0.11.8.1`, `publish=false`. It built `glob2-0.11.8.1-gamepix.zip` (132 MB, 494 files), which passed the packager's verification. The live browser game was not touched.

GamePix documents no upload API, so each release's zip is uploaded on the dashboard by hand. A third-party tool that scripts the dashboard's private endpoints exists; it was not used.

## Developer account — 2026-11-26

The owner registered on [my.gamepix.com](https://my.gamepix.com/) on 2026-11-26. The dashboard asks for payment settings. Payment details and agreements are the owner's to complete, and no agent entered them.

The **Create New Game** form has these fields:
- Title.
- An optional Game Jam, which can't be changed after creation.
- A main tag, plus up to four more chosen from about 150 GamePix tags.
- A description of 100 to 500 characters that must explain the controls.

GamePix writes the public game page from these. Its [OpenTTD page](https://www.gamepix.com/play/openttd) shows the result: a GamePix-written description, features, "How to play", FAQs, five tags, platform and orientation.

## Platform terms and requirements

Read on 2026-11-26 from [developers](https://partners.gamepix.com/developers), [submission guidelines](https://partners.gamepix.com/guidelines/submission) and the [JavaScript SDK guide](https://partners.gamepix.com/sdk/doc/javascript).

**Terms**
- 50% revenue share on net revenues.
- Non-exclusive.
- Optional "Allow Distribution" to third-party sites.

**SDK**
- `GamePix.events.on('pause')` and `on('resume')` are required, and the pause handler must mute audio.
- `GamePix.lifecycle.loaded()` and `gameStart()` are required in manual lifecycle mode; `loading(percent)` is recommended.
- Only the GamePix and Xsolla SDKs are allowed.

**Content and packaging**
- Files load by relative path.
- Banned: external links (including privacy-policy links), external analytics, external ads and system popups.
- Complete games only.
- The game must fit an iframe of at least 640×480 and pause only on page visibility changes.

**Storage**
- Only `localStorage` is synced; IndexedDB is not.

**Ads**
- Interstitials only between levels, never on a timer or during play.
- Rewarded ads must say what they give.

**Observed in use, not in the docs**
- Testing Toolkit uploads must be a zip of up to 200 MB with `index.html` at the root. The game's Build tab, seen after the entry was created, accepts `.zip` or `.gpx` up to 2 GB.
- Test uploads stay up for 24 hours.

## Inbound outreach — 2026-11-26

GamePix invited the project to publish after seeing the [itch.io page](https://genixpro.itch.io/globulation-2). The owner chose to proceed. A reply sent the same day said the project is on board and building a release pipeline, and asked about seven topics:

1. External links: a privacy-policy link, the Discord community and the GPL source-code link.
2. Online play and accounts on our own servers, and whether Xsolla Login is required.
3. Upload format and size limits.
4. Whether GamePix can serve COOP/COEP headers for the multi-threaded runtime.
5. Save storage: synced `localStorage` limits against our IndexedDB saves.
6. An upload API for CI, and whether every update is reviewed again.
7. Languages beyond the ten `GamePix.lang()` lists.

No answer yet. A colleague copied on the thread is out of office until 2026-11-30. Record the answers here when they arrive. The dashboard has since answered most of question 3. The Testing Toolkit takes a zip of up to 200 MB with `index.html` at the root. The game's Build tab takes a `.zip` or `.gpx` of up to 2 GB, or a Game URL.

## Listing

Status: **approved by the user on 2026-11-26** ("Use draft A"). Nothing has been entered on the dashboard. The copy is built from the storefront-v2 [English source](../translations/en.md) and limited to the claims [storefront v2 claims](../facts/storefront-v2-claims.md) marks safe for browser play. It is narrowed further to what the GamePix build contains.

The form warns: "Do not copy from other websites. Original content helps your game get more traffic." The description is therefore new wording of approved claims, not storefront-v2 text pasted in.

### What the GamePix build contains

The GamePix package runs with portal mode `{externalLinks: false, onlineSignIn: false}`:

- **No online play.** Play online, Settings → Online and online map links are hidden, so ranked, casual, rooms and cross-play are not claimed.
- **No external links.** No website, Discord or source-code link is claimed.
- **No LAN and no MCP AI co-play:** neither is in any browser build.
- Single-player against the computer, tutorial, map editor, replays and JavaScript opponents are all present.

Revisit this section when GamePix answers the questions about links and online play.

### Approved copy

**Title:** Globulation 2

The title is unchanged: the storefront rules keep `product_name` on every store except Google Play and Amazon. A subtitle such as "Globulation 2: Colony RTS" was considered for search and not used.

**Main tag:** Strategy games

**More tags (max 4):** War games · City Building games · Management games · Simulation games

The tags follow the game's pillars: fighting rivals, building the colony, running its economy. Alternatives from GamePix's list are Building games, Battle games and Tycoon games. Not used:

- Multiplayer games: there is no online play in this build.
- Vibe Coded Games: misleading for a volunteer project started in 2001.

**Description (449 characters):**

> Grow a colony of globs and win the fight for land in this real-time strategy game. You decide what to build and where to send workers and warriors; your globs gather, build, eat and fight on their own. Keep the colony fed, train an army and take on 8 computer opponents across 23 maps and 67 random landscapes. Mouse: left-click to build and place flags, right-click to cancel, wheel to zoom, arrow keys to scroll. Touch: drag to pan, pinch to zoom.

The controls match the game's desktop and touch control documentation. An alternative leading with "Command a whole colony, not single units" was offered and not chosen.

### Claims left out, and why

| Claim | Reason |
| --- | --- |
| "No ads" | True of the game, but GamePix shows its own ads around the game and earns from them. Open decision: ads on web portals. |
| "No in-app purchases", "Free" | True, but GamePix already presents every game as free, and the characters are better spent on gameplay and controls. |
| Online play, ranked, rooms, cross-play | Hidden by portal mode on GamePix. |
| Open source, GPL, since 2001/2004 | True, but GamePix bans external links, so players can't follow it to the source. The GPL source offer goes in the in-game credits. |
| 45 languages | True, but GamePix's own language list has 10; the game picks the player's language itself. |
| Map editor, replays, tutorial, JavaScript opponents | True for this build; left out for length. Candidates if GamePix offers a longer field after the game is created. |

## Open decisions and next steps

1. **Ads on web portals.** The storefront copy says "No ads", but GamePix earns only from ads around and between plays. Either the portal copy stays silent on ads, as it does now, or the portals are reach-only. Showing GamePix ads between matches would also need a game hook. Owner decision.
2. **GamePix's answers.** Their answers on links and online play may change the portal-mode switches and the listing's claims.
3. **Next release.** Re-test its zip in the Testing Toolkit: textured terrain, and audio silence on pause, checked by ear.
4. **Allow distribution.** It is on by GamePix default and lets GamePix syndicate the game to third-party sites. Owner decision.
5. **How to Play copy.** A draft is needed, with controls grouped by platform (desktop, mobile). The description also carries the controls today; it could drop them once How to Play exists, freeing characters for gameplay. Owner decision.
6. **Icon and cover** at 256×256 and 1360×850, from storefront-v2 real game art.
7. **Build.** After the next release with #1932, either upload that release's zip or switch to a Game URL (see the proposal above). Re-test in the Testing Toolkit first.
8. **Submission.** Third-party notes say a submitted build is locked until GamePix QA responds; this is unverified. Submit only a build that has passed the Testing Toolkit and includes #1932.
