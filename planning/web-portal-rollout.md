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

A dashboard notice asked the account owner to "Update Payment Settings" for future GamePix payouts. It was dismissed, not acted on; it is the user's to do.

## Newgrounds

**Project 8315233 (draft, saved 2026-11-26)**, account username `Globulation2`:
- Title: Globulation 2.
- Short description: the storefront-v2 headline.
- Genre: Strategy - Real-time (RTS).
- Rating: T, with violence "Some" for cartoon combat. Everything else is None.
- Commentary: the browser-safe copy, the same claims as Game Jolt.
- Tags: strategy, rts, colony, base-building, economy, multiplayer, open-source, map-editor.
- Icon: the itch.io cover, 630×500, from storefront-v2-renders.
- HTML5 file: the release run's standard `glob2-0.11.8.2-newgrounds.zip` (126 MB), uploaded by the user. Embed 1280×720, touchscreen friendly. "Uses SharedArrayBuffer/Cross Origin Isolation" is left off because the serial runtime is the verified path. Newgrounds offering cross-origin isolation means the threaded runtime could be tried there later.
- Allow Embedding: off.

Newgrounds' own preview loaded the game with textured terrain to the Introduction screen. Not published yet.

Earlier notes:

Account signed in on 2026-11-26. No project page yet. The Newgrounds zip from run 45873293249 keeps links and sign-in, so it can be used as is. The upload limit was reported as about 250 MB but is not confirmed from Newgrounds documentation.

## CrazyGames

Developer portal set up on 2026-11-26. Target is Basic Launch. Two blockers:

- Portal mode: needs a tag that contains #1927 (see the caveat above).
- Size: CrazyGames allows a 50 MB first download. The full build loads about 54–75 MB uncompressed (25–32 MB gzip) before the main menu. The small download build may solve this.

## GameDistribution (Azerion)

Developer application submitted on 2026-11-26; awaiting approval. Once approved, the dashboard gives a Game ID, which goes into the glob2 repository variable `GLOB2_GAMEDISTRIBUTION_GAME_ID` (it still holds a placeholder). Also needs a tag that contains #1927.

## Yandex Games

Parked on 2026-11-26. The Yandex account was completed, but the Games console is not accepting new developer applications. The full build is also over Yandex's 100 MB unpacked limit, so it would need the small download build in any case.

## Poki

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
