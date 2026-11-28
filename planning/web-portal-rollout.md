# Web game portal rollout

Started 2026-11-26. Covers getting the browser build of Globulation 2 onto Game Jolt, Newgrounds, CrazyGames, GameDistribution (Azerion), Yandex Games and Poki, plus a pitch to Armor Games. GamePix and itch.io are tracked separately in [GamePix listing](gamepix-launch.md) and [itch.io launch](itch-io-launch.md).

Evidence levels used below: **prepared** (drafted locally), **saved** (stored on the portal, not public), **submitted** (sent for review), **live** (publicly verified by loading the page).

## User decisions

- 2026-11-26: the user asked for "a game plan to get builds done, accounts registered and automated release pipelines implemented" for the six portals, with Poki to use the small download build from another thread, and to "pitch Armor Games just to see what they say".
- External links and online sign-in follow **per-portal rules** (user selection): each portal turns off only what it bans.
- Accounts: Claude fills in sign-up forms; passwords are saved in the user's password manager, never typed by Claude. Usernames are the user's own handle, not a Globulation-branded one (the user renamed the Game Jolt account to their handle).
- 2026-11-26: after the terrain defect was confirmed, the user chose "Unlist it for now" over cutting the patch release.
- 2026-11-26: after the gjpush token was rejected, the user said "lets get it on there manually for now too", then approved making the Game Jolt page public, then approved the four listing fixes in [Game Jolt listing comparison](../analysis/gamejolt-listing-comparison.md) ("Apply all four").

## Status

| Portal | State | Next step |
|---|---|---|
| Game Jolt | **Live** again 2026-11-26 with release 0.11.802 (textured terrain verified on gamejolt.net) | Launch devlog post (awaiting approval); next release brings the Quit fix |
| Newgrounds | Draft project 8315233 **saved** with 0.11.8.2; preview verified 2026-11-26 | Publish (awaiting the user's go-ahead) |
| CrazyGames | Developer portal set up; nothing submitted | Needs a build with portal mode and a first download under 50 MB |
| GameDistribution | Developer application submitted, awaiting approval | Game ID from the dashboard, then upload |
| Yandex Games | Parked | Not accepting new developer applications; the full build is also over its 100 MB limit |
| Poki | Not applied | Lite edition is ready (8 MB startup); needs a lite portal package, then apply |
| Armor Games | Pitch email **prepared** as a draft, not sent | The user checks the generative-AI disclosure line and sends it |

## Build and packaging (glob2 repository)

All three pieces are merged on glob2 master (2026-11-26):

- Per-portal packager (Globulation2/glob2#1926): `platforms/web/package-portal.py --portal <name>` repackages the verified `browser-release` artifact for gamepix, crazygames, newgrounds, gamejolt and gamedistribution. Each zip carries `window.GLOB2_PORTAL = {name, externalLinks, onlineSignIn}`.
- Portal mode in the game (Globulation2/glob2#1927): the game hides external links and online sign-in when the portal object says so.
- Game Jolt upload job (Globulation2/glob2#1928): `browser-release` can push the Game Jolt zip with gjpush. Release versions fold the fourth tag part into the patch: v0.11.8.1 becomes 0.11.801.

Release run 45873293249 on the release mirror (2026-11-26, tag v0.11.8.1, publish off) built all five portal zips. Package size: 126 MB zipped, about 219 MB unpacked, about 495 files.

**Caveat:** the game binary is built from the release tag, and v0.11.8.1 predates portal mode. Zips from that tag ignore the portal settings. That is harmless for Game Jolt and Newgrounds, which keep links and sign-in, but the CrazyGames and GameDistribution zips must wait for the first tag that contains #1927.

## Lite browser edition

Merged 2026-11-26 as Globulation2/glob2#1933. The user reported it finished that day, at the target of about 8 MB before the game starts. According to the PR, an English-speaking player downloads 8.07 MB (Brotli) before the game starts and 9.04 MB in total, against 21.93 MB and 106.62 MB for the standard build. It is published at `/play/lite/`.

The lite edition leaves out the map editor, online play, LAN, MCP, the JavaScript AIs, premade maps (random maps and campaigns remain), translations (English only), HD art and most music. Terrain looks simpler by design. Listing copy for a portal that uses lite must therefore drop the editor, online play, the 23 handmade maps and the 45 languages.

Not yet done: the portal packager still repackages the standard build only. Pointing the CrazyGames, Poki and Yandex profiles at the lite artifact is a change in the game repository.

## Local test of master before 0.11.8.2 (2026-11-26)

The release was going to take longer, so the user asked for a local build to test the browser packages sooner. Built on this machine from glob2 master at `8fb3c06aee` ("Prepare release 0.11.8.2", #1935). That commit includes the terrain fix #1932, portal mode #1927, the lite edition #1933 and the water fix #1929. Both editions were built with `release=1` (free client profile, as in CI) and packaged with `package-static.py` and `package-portal.py`, exactly as `browser-release.yml` does.

**Packages (version 0.11.8.2):**

| | Zip | Unpacked | Files |
|---|---|---|---|
| Standard | 132.1 MB | 219.3 MB | 494–495 |
| Lite | 17.7 MB | 45.8 MB | 32–33 |

Every portal profile packaged both editions, except Yandex standard, which the packager refused as over 100 MB unpacked. Yandex lite fits.

**How it was tested:** each zip was served the way a portal hosts it: an iframe on a different origin, plain static files, no COOP/COEP headers. This forces the single-threaded runtime that portal players get. Confirmed on the game page: `crossOriginIsolated` false, no `SharedArrayBuffer`.

**Results:**

| Package | Desktop Chrome | iPhone 17 Pro simulator (Safari, iOS 26.5) |
|---|---|---|
| Game Jolt (standard) | loads; textured terrain; Play online and Discord shown (policy keeps them) | not run |
| Newgrounds (standard) | loads; textured; links and online shown (policy keeps them) | not run |
| CrazyGames (standard) | loads; textured; links and online hidden; custom match plays | not run |
| GamePix (standard) | loads; textured; links and online hidden | not run |
| GameDistribution (standard) | loads; textured; links and online hidden | not run |
| Poki (lite) | menu in under 10 s; textured; links, online and editor hidden; custom match plays | not run |
| Yandex (lite) | loads; textured; links and online hidden | not run |
| CrazyGames (lite) | loads; textured; links and online hidden | loads; textured; sound prompt and handedness prompt work by touch; introduction match plays |

The terrain fix is confirmed: the console logs `DIRECT_TERRAIN_BASE` and no `ANIMATED_TERRAIN_FALLBACK`.

**Defect found:** every portal build still shows **Quit** on the main menu. Inside a portal iframe it leaves a blank dark screen that only a page reload recovers from. CrazyGames' rules ban exit buttons. Fix: Globulation2/glob2#1938 (opened 2026-11-26) hides Quit and makes Escape on the top-level menu do nothing in every portal. It was checked in the simulated portal: CrazyGames and Game Jolt menus show no Quit, and Escape keeps the menu. Upload packages only from a build that includes it.

**Phone layout depends on the portal page.** The first iPhone run drew the desktop layout with tiny controls. Cause: the test harness's host page had no `<meta name="viewport">`, so Safari laid it out 980 px wide and scaled it down, and the game's iframe took that width. The game's own page sets `width=device-width` and gets the phone layout, both standalone and inside a host page that sets the tag (re-checked the same day). On the real sites, check the mobile layout on a phone-sized screen. If a portal's page lacks the tag, its iframe will show the desktop layout.

**Not covered:** desktop Safari and Firefox; Android; audio pause and resume through each portal's SDK (the SDKs only respond on their own sites); the real portal sites. The real-site checks need uploads (Game Jolt unlisted release, GamePix Testing Toolkit, CrazyGames preview and QA tool, Newgrounds unpublished project, Poki Inspector).

## Release 0.11.8.2 packages (2026-11-26)

Tag v0.11.8.2 is commit `8fb3c06aee`, the same commit tested locally above. Release-mirror run 45902410410 published the standard and lite browser builds and produced the five standard portal zips (gamepix, crazygames, newgrounds, gamejolt, gamedistribution; 126 MB each). The workflow makes no lite portal zips, so those were packaged locally from the run's verified `browser-release-lite` artifact with `package-portal.py` for poki, crazygames, yandex, gamedistribution, gamepix, newgrounds and gamejolt (17.7 MB zip, 45.8 MB unpacked each). All are in `~/Downloads/glob2-0.11.8.2-portals/` on the build machine.

Smoke test in the simulated portal: the release CrazyGames zip and the lite Poki zip load with textured terrain and the expected menus. **The tag predates the Quit fix (#1938)**, so these packages still show Quit.

## Portal ads: build fit and SDK checks (2026-11-26)

Globulation2/glob2#1945 (portal ads at natural breaks, lite portal uploads, a 3-minute minimum gap between breaks) merged as `616d966` after the fast gate and sim-diff passed. Every portal package was rebuilt locally from that commit and fits its portal:

| Portal | Edition | Zip / unpacked | `ads` |
|---|---|---|---|
| Game Jolt, Newgrounds | standard | 132.1 / 219.5 MB | false |
| GamePix, GameDistribution | standard | 132.1 / 219.5 MB | true |
| CrazyGames, Poki, Yandex | lite | 17.9 / 46.2 MB | true |

**Poki, real SDK on localhost:** verified end to end. The first match started with `gameplayStart` and no ad. Leaving the match sent `gameplayStop`. Returning to the menu called `commercialBreak`, and Poki's local test ad (a promo video) played, then the game resumed. A second match within 3 minutes sent `gameplayStart` with no second break.

**CrazyGames, real SDK on localhost:** the SDK script loads, but `CrazyGames.SDK.init()` neither resolves nor rejects, and no network requests are made, so the adapter keeps running without the SDK. That is the designed fallback, so the game is unaffected. Ad behaviour can't be judged locally; CrazyGames' docs point to their **QA Tool** for that. Re-check that `init()` resolves there. If it hangs on CrazyGames too, the loading and gameplay events never reach the SDK.

**Still to check on each portal's own tool:** CrazyGames QA Tool, Poki Inspector, GamePix Testing Toolkit (interstitial), GameDistribution Upload-tab iframe (once the account is approved). Yandex SDK checks need Yandex's own domain.

**Noticed:** the lite in-game menu still lists "AI telemetry", a developer-facing item, for portal players.

## Release 0.11.9.1 packages (2026-11-28)

This is the patch the final submissions were held for. It carries the input-gated first match (glob2 #1983), Play online hidden in every portal (#1985), and the HD building art. Browser release run 46093648075 on genixpro/glob2-release passed every job, crash-symbol upload included, and all seven portal jobs met their limits.

| Package | Zip | Unpacked | Files | Policy (links, online, ads) |
| --- | --- | --- | --- | --- |
| poki-lite | 18.2 MB | 47.2 MB | 140 | no, no, yes (`awaitInput`) |
| crazygames-lite | 18.2 MB | 47.2 MB | 140 | no, no, yes |
| yandex-lite | 18.2 MB | 47.2 MB | 140 | no, no, yes |
| gamedistribution | 123.1 MB | 207.4 MB | 540 | no, no, yes (`awaitInput`) |
| gamepix | 123.1 MB | 207.4 MB | 540 | no, no, yes |
| newgrounds | 123.1 MB | 207.4 MB | 539 | yes, no, no |
| gamejolt | 123.1 MB | 207.4 MB | 539 | yes, no, no |

The full packages grew from about 132 MB to 207 MB unpacked with the HD art. That is still inside every limit: GamePix's 200 MB applies to the zip, Newgrounds allows about 250 MB, and the 100 MB Yandex and 50 MB CrazyGames first-download limits apply to the lite packages. Copies are in `~/Downloads/glob2-0.11.9.1-portals/`, and the unpacked CrazyGames upload is in `~/Downloads/glob2-0.11.9.1-crazygames/`.

Checks, 2026-11-28:
- **Poki Inspector:** returning player: SDK initialized, game loading finished, then Commercial break and Gameplay start at the lesson start, no warnings. A fresh visitor sits at the sound prompt and the menu with no gameplay event before input; initial download 19 MB.
- **Local portal frame:**
  - Newgrounds and Game Jolt show Discord community and no Play online.
  - GameDistribution, GamePix, CrazyGames and Yandex show no external links and no Play online.
  - Every package shows version 0.11.9.1 and the HD buildings.
  - The Newgrounds first-visit lesson starts, and leaving it returns to the menu.
- **CrazyGames QA Tool:** still to run on this build; the owner uploads it.

Nothing has been submitted.

**Submissions, 2026-11-28 (owner: "Do all of them").** The browser tool can attach at most 10 MB, so the owner uploaded the builds.
- **GamePix:** the owner uploaded the 0.11.9.1 zip, and the build processed. Claude **submitted the new release for review**, marking Description and Build as changed, with release notes covering HD art, crash reporting and hidden links/sign-in. GamePix showed "Game in review!".
- **CrazyGames:** Claude cleared the 0.11.8.4 files, and the owner uploaded the unpacked 0.11.9.1 folder (gameBuildId a6236c57-36b3-446f-9174-dcfa5d4ab1fc).
  - QA Tool, custom match: log sdkInit, sdkGameLoadingStart, gameLoaded, gameFinishedLoading, sdkGameLoadingStop, gameplayStart, gameplayStop (menu), gameplayStart (return), gameplayStop (quit). No warnings; 45 MB total, 8.7 MB load size, 28.8 s load time.
  - Claude pressed Continue. The QA Results checklist and its confirmation are the owner's declaration. Open item: the portal build has no Privacy policy button, while crash reporting (with consent) can send data.
- **Newgrounds:** the owner uploaded the 0.11.9.1 zip ("Ready to be Published"); its preview starts the introduction lesson. "Publish Project" opens a user agreement, left for the owner. Note: its Rights and Ownership section says the game must not be a modified version of someone else's work, which needs the owner's judgement for a long-running open-source project.
- **Poki:** Claude filled the "Submit your game" form for the owner's review:
  - studio GenixPro Technologies, registered company, Canada, just me;
  - lite link https://app.glob2.online/play/lite/;
  - three desktop screenshots.
  The guidelines box and Submit are the owner's.
- **Game Jolt:** browser-release run 46099064215 (v0.11.9.1, publish off, gamejolt on) waits for the owner's `gamejolt-release` approval.

**Follow-up, 2026-11-28.**
- **Newgrounds:** the owner accepted the agreement and published. The game is live at https://www.newgrounds.com/portal/view/1064794 (project 8315233).
- **CrazyGames:** the owner completed the QA Results checklist. Claude filled the Details step:
  - Strategy; tags War, Battle, Building, Management, Mouse (Mobile waits for a phone check);
  - the listing-copy description with "How to play" and "Features" headings, and the PC and mobile controls;
  - tools: Claude and Other ("Own open-source C++ engine (Globulation 2, developed since 2001), SDL, Emscripten");
  - Google Play and App Store links, and the three covers from `assets/portal-art/crazygames/`.
  The owner uploaded both preview videos. The Submit step's Terms & Conditions and PEGI 12 checkboxes and "Submit for approval" are the owner's.

## Game Jolt

- Page: https://gamejolt.com/games/globulation2/1122762, developer account `genixpro`. Game ID 1122762, package ID 1154961.
- Listing content (2026-11-26, saved then live): storefront-v2 description, header and thumbnail cropped from the Steam store package, seven 1920×1080 screenshots from the itch.io package, maturity All Ages with moderate cartoon violence, engine C/C++, website https://glob2.online.
- Release 0.11.801 (2026-11-26): browser build `glob2-0.11.8.1-gamejolt.zip` uploaded by hand by the user, fit-to-screen on, HTTPS on. Claude saved and published the release. Verified by opening the game from the page: it loaded to the Introduction screen.
- Page published (2026-11-26): status changed from Unlisted to Published after the user approved it.
- Listing optimisation (2026-11-26, saved and verified through the site API):
  - Added the gameplay trailer https://www.youtube.com/watch?v=t6Q3ZpY9aTM as the first media item (8 media items now).
  - Set the page colour theme to the brand accent `#e3c077` from glob2-design-system.
  - Added `#multiplayer` to the description hashtags, now `#strategy #rts #opensource #multiplayer`. Only `#strategy` and `#multiplayer` are on Game Jolt's official browse-tag list; the other two still help search.
  - Languages: no change was needed. Game Jolt has no languages field, and the description already says "45 languages".
- Not done yet: devlog posts (none so far; launch post 1 is [prepared for review](gamejolt-devlog.md)), development stage still "Early Access" (the user's call whether to switch to "Complete/Stable").

### Terrain defect in release 0.11.801

Reported by the user on 2026-11-26, after the page went public: the Game Jolt build has the flat-colour terrain flaw. Cause: Game Jolt sends no cross-origin isolation headers, so the game uses the single-threaded browser runtime. In v0.11.8.1 that runtime draws every terrain tile as flat colour. The fix, Globulation2/glob2#1932, merged after v0.11.8.1, so it reaches Game Jolt only with the next release tag. GamePix is waiting on the same release ([GamePix launch](gamepix-launch.md)). The user chose to **unlist** the page until then. It was unlisted on 2026-11-26 (dashboard badge "Unlisted", site API status 0), so it is still reachable by link but not in listings. Re-publish after the fixed release is uploaded and the terrain is checked visually, then post the [launch devlog](gamejolt-devlog.md). My earlier check, that the game "loaded to the Introduction screen", confirmed only that it loads, not that the terrain draws correctly.

### Release 0.11.802 and re-publication (2026-11-26)

The user approved uploading 0.11.8.2 to Game Jolt, Newgrounds and GamePix ("Yes, those three"). Release 0.11.802 was created with the release run's standard `glob2-0.11.8.2-gamejolt.zip`: the user uploaded it, and Claude set fit-to-screen and published the release. The page now serves only 0.11.802's build (overview API: one published release, one build). It was played on gamejolt.net and the terrain is textured, with blended shorelines. The page was then re-published (site API status 1), as planned when it was unlisted. Known issue: Quit is still shown until a release that includes glob2 #1938.

### Automated upload: blocked

gjpush rejected every token with "Authorization token is invalid" (three attempts on 2026-11-26, including a whitespace-stripped paste). gjpush's README says it needs a "service API authentication token" and that "only testers are given a token". The Game Token in the avatar menu is a different credential, for the in-game Game API. A request for a gjpush token, addressed to the gjpush maintainer listed in that README, is **prepared** as a Gmail draft and not yet sent.

Until a token arrives: dispatch `browser-release` with `gamejolt` off, download the `gamejolt-upload` artifact, and upload it by hand on the package page (New Release → set the version → upload the browser build → fit to screen → Save Build → Publish Release). The release cannot be saved as a draft until a build is attached.

### Claims note

Game Jolt shows its own site advertisements around the game page. "No ads" in the description refers to the game itself, which shows none.

## GamePix Testing Toolkit run of 0.11.8.2 (2026-11-26)

The user uploaded the release run's standard `glob2-0.11.8.2-gamepix.zip` to my.gamepix.com, SDK, Testing Toolkit ("upload my local build"). Its test URL loaded straight away, with no 403 this time. The game ran in the toolkit's 800×450 desktop frame. The Debug Console showed the GamePix SDK receiving LOADING 0–100, LOADED, GAME_START and FIRST_INTERACTION, and the toolkit's Pause and Resume reached the game. Audio was not checked by ear.

**Defect found:** in that 800×450 desktop frame the game shows the phone's "Left or right hand?" prompt. Choosing "Use desktop layout" and confirming brings the same prompt back, in a loop. A mouse player can only continue by picking a hand, which gives the touch layout.

Cause, from the glob2 code: `Application::mainMenu` asks whenever `Glob2UI::touchPresentation()` is true. That is `phonePresentationRequested()`, which equals `adaptedControls()` = touch input **or** the compact layout. Compact is chosen when the usable area is under 480 px tall, or narrower than 480 px plus the panel width. "Use desktop layout" turns touch off but cannot make the frame fit, so the layout stays compact and the prompt returns. Any portal that embeds the game below 480 px tall on desktop is affected. Fix: Globulation2/glob2#1941 (opened 2026-11-26) asks for the thumb side only on touch hosts. Verified in an 800×450 simulated-portal frame (mouse: straight to the compact main menu) and on the iPhone simulator (touch: still asked).

**Listing optimisation applied 2026-11-26** (entry BL8O73, from [portal listing copy](portal-listing-copy.md)):
- Orientation changed from All to Landscape (GP-4).
- New gameplay-led description, 443 characters (GP-3).
- "Game features" custom section added (GP-3).
- FAQs: "Do I control each unit?" and "How do I win?" (GP-2). The dashboard silently refused a third FAQ on every attempt, including after a save, so "Where should I start?" and "Does it cost anything?" are not on the listing.
- Video: initially left empty because the YouTube trailer's end card says "No ads". Then set to the unlisted gameplay cut https://www.youtube.com/watch?v=BJoMHyCxzkg (see "Gameplay video for ad-enabled portals" below), saved and re-read after a reload.

All changes were re-read after a reload. "Allow distribution" was already ticked and was not changed. Not submitted for review.

A dashboard notice asked the account owner to "Update Payment Settings" for future GamePix payouts. It was dismissed, not acted on; it is the user's to do.

## Gameplay video for ad-enabled portals (2026-11-26)

At the user's request ("Yes, cut it"), the existing textless 30-second trailer cut was used for listings on ad-enabled portals. The published trailer `t6Q3ZpY9aTM` ends on a "No ads" card and says "No ads" in its description.
- Source file: `storefront-v2-renders/trailer/glob2-trailer-30s-textless-1080p.mp4` (53 MB), from the same storefront trailer footage (manifest in `assets/storefront/trailer/manifest.json`). It has no text cards and no AI co-play beat.
- Check: the contact sheet `assets/storefront/trailer/contact-sheet-master-30s-textless.jpg` shows gameplay only. There is no text, MCP card, online screen or link. One beat shows the in-game build palette. This is standard-build footage with HD art, so it is not representative of the lite edition.
- YouTube: https://www.youtube.com/watch?v=BJoMHyCxzkg on the Globulation 2 Online channel, **Unlisted**, titled "Globulation 2 gameplay", not made for kids. The description has no ad claims and labels the footage as AI-versus-AI matches filmed from a player seat. The user uploaded the file; Claude set the details.
- Use: GamePix (standard build). Not for CrazyGames, Poki or Yandex, which use lite and need lite footage.

## Newgrounds

**Project 8315233 (draft, saved 2026-11-26)**, account username `Globulation2`:
- Title: Globulation 2.
- Short description: the storefront-v2 headline.
- Genre: Strategy - Real-time (RTS).
- Rating: T, with violence "Some" for cartoon combat. Everything else is None.
- Commentary: the browser-safe copy, the same claims as Game Jolt.
- AI disclosure added to the commentary 2026-11-27 (owner-approved; NG-9 in the [other portals audit](../analysis/other-portals-requirements-audit.md)). The commentary editor saves only after focus leaves it: click outside, wait, then reload to confirm.
- Tags: strategy, rts, colony, base-building, economy, multiplayer, open-source, map-editor.
- Icon: the itch.io cover, 630×500, from storefront-v2-renders.
- HTML5 file: the release run's standard `glob2-0.11.8.2-newgrounds.zip` (126 MB), uploaded by the user. Embed 1280×720, touchscreen friendly. "Uses SharedArrayBuffer/Cross Origin Isolation" is left off because the serial runtime is the verified path. Newgrounds offering cross-origin isolation means the threaded runtime could be tried there later.
- Allow Embedding: off.

Newgrounds' own preview loaded the game with textured terrain to the Introduction screen. Not published yet.

**Listing optimisation applied 2026-11-26** (from [portal listing copy](portal-listing-copy.md), after the user approved all recommendations):
- New short description (88 characters, NG-1).
- New author comments (about 230 words, NG-2 and NG-4).
- Tag `multiplayer` swapped for `real-time-strategy` (NG-7).

The first commentary typed when the draft was created had **not** been saved: the draft held an empty commentary until this pass. All three changes were re-read after a page reload. Touchscreen friendly stays ticked until the published page passes a phone test (NG-3). Not published.

Earlier notes:

Account signed in on 2026-11-26. No project page yet. The Newgrounds zip from run 45873293249 keeps links and sign-in, so it can be used as is. The upload limit was reported as about 250 MB but is not confirmed from Newgrounds documentation.

## CrazyGames

**QA Tool run, 2026-11-26** (not sent to QA, not submitted). The user ticked the six pre-submission declarations; Claude filled the upload form:
- Name: Globulation 2. Engine: HTML5. Save progress: "No, the game does not need progress save" (user choice; saves stay in browser storage, which CrazyGames' automatic LocalStorage backup doesn't cover).
- Options: mobile supported, CrazyGames SDK muting supported, not online multiplayer.
- Build: the lite package from glob2 master `616d966` plus PR #1947. The first upload attempts lost `core.<hash>.data`, because the uploader refused it as an archive; #1947 fixed that (see Lite browser edition notes).

QA results:
- SDK: `sdkInit`, then `sdkGameLoadingStart`, `gameLoaded` and `sdkGameLoadingStop`, about 3 s from init to loading finished.
- Load size 10.4 MB (limit 50 MB); total 44.1 MB.
- `gameplayStart` at match start and `gameplayStop` on leaving.
- No hand prompt in the desktop frame, no Quit, and no QA warnings.
- No `requestAd` appears in the QA log after leaving the match. Ads are disabled in Basic Launch, so this has to be re-checked for Full Launch.

**Resolution (2026-11-26):** CrazyGames' rules say the first gameplay start "excludes menus", and their 20-second time-to-gameplay rule applies only to externally hosted games ([technical requirements](https://docs.crazygames.com/requirements/technical/)). So match-based gameplay events stay. A first-screen gameplay change was tried in glob2 #1952 and removed. The QA load-time figure is informational for us; the binding limit is the ≤ 50 MB initial download (10.4 MB). The user decided to keep the current first-run flow: sound prompt, then the Introduction offer, which is one click into a skippable onboarding match. That already meets the quality guideline that new players "land directly" in a skippable onboarding. The in-game menu fit is fixed in glob2 #1952 (wheel scrolling, two columns in short frames, AI telemetry hidden in portals), and "Report a problem" is confirmed link-free there.

**QA Tool re-run, 2026-11-27**, with the lite package from glob2 master `8e03a98` (#1947 and #1952 merged): 18.0 MB zip, 46.8 MB unpacked, 138 files, because the game pack is now split into about 107 parts. The draft's old files were replaced and the saved answers kept, with mobile orientation set to Both. Results:
- `sdkInit` to `sdkGameLoadingStop` took about 8 s; load size 10.3 MB; total 44.6 MB.
- `gameplayStart` and `gameplayStop` arrive around the match.
- The in-game menu shows two columns at the ~910×470 frame, with every item including Quit the game visible.
- AI telemetry is hidden and there is no Quit on the main menu.
- No QA warnings.

Not sent to QA and not submitted: submission should use the next release tag, with the Details step filled from [portal listing copy](portal-listing-copy.md) and the art in `assets/portal-art/crazygames/`.

**To fix before submission (original findings):**
1. QA "Load time 61.9 s". CrazyGames measures it from Play Now to the first gameplay event, which the game sends only when a match starts, so it included the sound prompt, the introduction offer and slow manual clicks. Their bar is 20 s: send gameplay when the player is interacting with the main menu, or shorten the path to the first match.
2. The in-game menu doesn't fit the ~470 px tall frame: "Quit the game" is cut off and the mouse wheel doesn't scroll the list.
3. Check that the new "Report a problem" menu button doesn't open an external page when external links are off.


Art (2026-11-26, not uploaded): the three covers (1920×1080, 800×1200, 800×800) and both 18 s preview videos (1920×1080 and 1080×1620, one opening on a real fight) from lite-build footage, spectator view with areas hidden, in [portal art](../assets/portal-art/README.md). GameDistribution's five asset sizes are there too.

Developer portal set up on 2026-11-26. Target is Basic Launch. Two blockers:

- Portal mode: needs a tag that contains #1927 (see the caveat above).
- Size: CrazyGames allows a 50 MB first download. The full build loads about 54–75 MB uncompressed (25–32 MB gzip) before the main menu. The small download build may solve this.

## GameDistribution (Azerion)

Developer application submitted on 2026-11-26; awaiting approval. Once approved, the dashboard gives a Game ID, which goes into the glob2 repository variable `GLOB2_GAMEDISTRIBUTION_GAME_ID` (it still holds a placeholder). Also needs a tag that contains #1927.

## Yandex Games

Parked on 2026-11-26. The Yandex account was completed, but the Games console is not accepting new developer applications. The full build is also over Yandex's 100 MB unpacked limit, so it would need the small download build in any case.

## Poki

**Poki Inspector run, 2026-11-27** (https://inspector.poki.dev/). The lite package from glob2 master `8e03a98` (18.0 MB zip, `ads: true`) was served from the build machine at `http://localhost:8801/poki-master/index.html` and opened by URL, so no upload was needed. Event log:
- SDK initialized, then gameloadingstart, Game loading finished and gameloadingcomplete.
- Gameplay start when the introduction match began; Gameplay stop on leaving it.
- Commercial break straight after returning to the menu.
- No warnings.

The Inspector's "Initial download size 25 MB" and "loading 37 s" figures come from the local Python server, which sends files uncompressed. The lite build's compressed startup download is about 8 MB.

**Gap found:** opening the in-game menu or choosing Pause during a match sends no `gameplayStop`, and resuming sends no `gameplayStart`. Poki's checklist asks for stop and start "accurately fired when the game is paused". The Inspector's QA modules are a developer self-assessment (SDK Basics, Technical Stability, Mobile Optimization, Privacy & Security, Playground Integration, Ad Implementation); none have been ticked.

**Gap fixed** in glob2 #1955, merged 2026-11-27 as a592d8b. The in-game menu and Pause now send `gameplayStop`, and closing or resuming sends `gameplayStart` (Poki, CrazyGames, Yandex). Pause never triggers an ad.

**Inspector re-check, 2026-11-27, passed.** Lite Poki package built from the #1955 head (static hash 8e43749287e637f2), loaded by URL from localhost in Chrome. One custom match: open the menu, return, open the menu and pause, resume, quit, then leave the results. Event log: Gameplay start, stop (menu), start (return), stop (menu; the pause sent nothing extra), start (resume), stop (quit, once), Commercial break on leaving the results. No warnings. The Inspector needs Chrome: the desktop app's built-in browser shows a blank game frame for a localhost URL. Build note: `dev_build.py ... web-package` refreshes only the build directory; run `platforms/web/package-static.py --source build/emscripten/client/release/lite --output build/browser-static-lite` before `package-portal.py`, or the portal zip repackages the previous build.

**Requirements audits and fixes, 2026-11-27.** Line-by-line audits against each portal's published rules: [Yandex](../analysis/yandex-requirements-audit.md), [CrazyGames](../analysis/crazygames-requirements-audit.md), [Poki](../analysis/poki-requirements-audit.md), [GameDistribution, GamePix, Newgrounds, Game Jolt](../analysis/other-portals-requirements-audit.md). Fixes merged in glob2 #1956 (portal adapters: Poki commercialBreak before every gameplay start and resume with no own gap or menu break; Yandex window blur stops gameplay and mutes; GameDistribution waits for SDK_READY; GamePix pause holds the game and gameStart at the first match; CrazyGames device type picks touch layout; no text selection, page panning or pinch zoom on every portal page) and #1957 (no own fullscreen control in portals; in-game menu text legible in small frames; setup tabs fit at 640×360; a portal's first visit lands in the introduction lesson). Owner approved landing in the tutorial.

Checked on master f2b70e4 (lite static 2877a91ed764acfb), simulated portal frame 674×322 in the desktop app's browser: a fresh visit goes straight to the lesson briefing; the in-game menu text is legible; Settings > Display has no Window mode. Note for testing: a portal frame's storage is partitioned from the same origin opened top level, so clearing data at top level does not reset a first visit inside the frame. Poki Inspector in Chrome, same build, first visit (frame storage cleared by loading a clearing page through the Inspector): straight into the introduction lesson; log: SDK initialized, Game loading finished, Commercial break, Gameplay start (lesson), Gameplay stop (menu), Commercial break, Gameplay start (return), Gameplay stop (menu, then Pause: nothing extra), Commercial break, Gameplay start (resume). No warnings. In-game menu legible at the Inspector's desktop frame. The Inspector's Mobile mode needs a real phone (QR code) that can reach the game URL, so the Poki Pill position and mobile checks wait for a phone on the same network or an upload. Still to do: the CrazyGames QA Tool on this build. Small cosmetic item seen: the Interface scale dropdown value is clipped at 674×322.

Open, from the audits: GameDistribution mobile ads should start inside the player's tap (needs a game-side signal); phone players' first lesson is silent until the deferred sound question; the Yandex draft cannot be checked until Yandex accepts applications; ownership wording for Yandex 3.5 and Newgrounds (GPL project with many contributors) is the owner's call.

**Release 0.11.8.4 check, 2026-11-27.** Owner's instruction: no final portal submissions until the next patch release, but keep testing every portal against its standards. The release's browser run, genixpro/glob2-release run 46027109895 at af161e2, built all seven portal packages. Its crash-symbols upload failed, so its own GCS publish was skipped; that is a release-pipeline item, not a portal one. Sizes: CrazyGames, Poki and Yandex lite are 140 files and 45 MB unpacked (about 18 MB zipped). Newgrounds, Game Jolt, GameDistribution and GamePix full are 537 to 538 files and 198 MB unpacked (about 122 MB zipped).

Poki Inspector on the release package: SDK initialized, Game loading finished, then Commercial break and Gameplay start. A break runs before every return to play, and Pause sends nothing extra. Inspector warnings stayed empty.

The `gameplayStart()` checklist item showed a notice, "fired without a player interaction". On a first visit the lesson starts by itself, so the first start was reported before any input. Fixed in glob2 #1983 (merged 2026-11-27 as 792b3ba; owner approved merging despite the unrelated master-wide `contracts` failure, a NASM requirement on the CI runner): Poki and GameDistribution hold the first start and its break until the player's first key, click or tap, and begin them just after the press, so the click that closes the briefing still works. CrazyGames is unchanged, because its QA Tool times loading up to the first gameplayStart.

Re-checked with the fix swapped into the release package:
- nothing is reported until the first click;
- that one click closes the briefing, then a break and a start follow;
- the notice is gone;
- Force show ads plays an ad on return from the menu and holds the game, and Gameplay start follows when it ends.

The Inspector's Scaling Tests (640×360, and Galaxy S20 in portrait and landscape) show the layout adapting. In portrait the lesson title is shortened ("Scou…").

Simulated portal frame (Chrome, separate origin, no COOP/COEP): Newgrounds, Game Jolt, GameDistribution, GamePix and Yandex 0.11.8.4 all load to the main menu. Newgrounds and Game Jolt show Play online and Discord community. GameDistribution, GamePix and Yandex hide both, and Yandex (lite) also has no Editor.

The CrazyGames 0.11.8.4 package needs no #1983 change and is ready for the QA Tool. The upload is the owner's step.

**Play online hidden on Newgrounds and Game Jolt, 2026-11-27.** While resolving the listing decisions, a probe found that `https://app.glob2.online` sends no CORS headers: a preflight from a foreign origin returns 404. The Newgrounds and Game Jolt packages kept Play online, which therefore cannot connect from those sites. Game Jolt is live with the dead button. The owner chose to hide it ("Yes, hide it"): glob2 #1985 sets `onlineSignIn: false` for both and keeps their external links. Merged 2026-11-27 as b9ab96c; the owner approved merging despite the known master-wide `contracts` NASM failure. The live Game Jolt build changes only when the next release is pushed with `gamejolt-release`.

**CrazyGames QA Tool, 0.11.8.4, 2026-11-27, passed.** The owner uploaded the unpacked package (gameBuildId 8b23f07b-96c9-4e47-bcc5-9839942ddd75) and has not pressed Continue, so the build has not gone to QA. The Tool reports 44.5 MB total, 10.3 MB load size, and a 33.6 s load time that includes time spent in menus.

Log: sdkInit, sdkGameLoadingStart, gameLoaded, gameFinishedLoading, sdkGameLoadingStop when the menu is ready. Then, in a custom match:
- gameplayStart at the start;
- gameplayStop when the menu opens;
- gameplayStart on return;
- gameplayStop on the menu before quitting, with nothing extra on quit.

Leaving the results requested no ad, which is right for Basic Launch. The Warnings tab is empty. Settings > Display has no Window mode option, only the "Windowed" status text. The first-visit lesson wasn't seen, because this preview's storage already marks the introduction offered from earlier runs. Mobile checks need a phone; the Tool's QR code opens the preview.

Earlier notes:

Art (2026-11-26, not uploaded): text-free 1080×1080 thumbnail and 5.85 s 60 fps animated thumbnail from lite-build footage, in [portal art](../assets/portal-art/README.md).

Poki's sign-up is its game submission form. The application waits for the small download build from the "Small Download Browser Build" thread, which the user reported as merged on 2026-11-26 and about to be built. Check it with Poki's limits and the Poki Inspector before applying.

## Armor Games

A pitch email to Armor Games' game submission address is **prepared** as a Gmail draft and not sent. Armor Games asks submitters to disclose generative-AI use; the draft has a placeholder line for that which the user must check before sending.

## Open decisions

Listing research for every portal (2026-11-26, commit 1f95e7b): see the `analysis/<portal>-listing-comparison.md` files. Decisions it surfaced:

- **Ads are now blocking for three portals.** Poki requires its ad calls. GameDistribution's SDK expects a pre-roll and mid-rolls. Yandex rule 1.12 requires ads or in-app purchases. CrazyGames shows no ads in Basic Launch but needs SDK ads for Full Launch. This sharpens the "No ads" decision below.
- **Newgrounds content rating:** T, as currently set (recommended), or E.
- **Newgrounds build:** standard, as currently set (recommended), or lite.
- **GameDistribution build:** standard or lite (no size limit found).
- **Lite copy:** never claim campaigns (claims R5: none ship). Check whether "8 computer opponents" holds in lite, which drops the JavaScript AIs.

- **Ads:** storefront-v2 copy says "No ads". CrazyGames, GameDistribution, Yandex and Poki run their own ads around or inside games, so the claim needs scoping per portal before those listings go live. See [storefront v2 claims](../facts/storefront-claims.md).
- **Game Jolt development stage:** Early Access or Complete/Stable.
- **Game Jolt devlog:** whether to post a launch devlog. The comparison found devlog posting is the main gap against top games.
