# Portal requirements audit: GameDistribution, GamePix, Newgrounds, Game Jolt

Observed **2026-11-27**. This audit checks the builds against each portal's published developer requirements, one requirement at a time. It covers code on `origin/master` of Globulation2/glob2 as of 2026-11-27 (head `e72a4ddc2a`, tags up to `v0.11.8.3`). Nothing was signed in to, uploaded, committed or changed. Requirements are paraphrased.

**Build under audit.** All four portals get the standard edition: a 132 MB zip that unpacks to 219 MB, about 495 files, with `index.html` at the root. Portal pages send no COOP/COEP headers, so the game runs single-threaded. Packaging is `platforms/web/package-portal.py`, the shared runtime is `platforms/web/portal-core.js`, and the adapters are `gamedistribution.js` and `gamepix.js`. The game-side policy is in `src/app/PortalPolicy.h`.

**Status key.** **Met**: the code or assets satisfy it. **Not met**: they do not. **Unknown**: not confirmed, either because the source is unclear or because it needs a run or a dashboard check. **N/A**: does not apply to this build.

**How sources were read.** Pages were read without signing in. The GameDistribution site and Newgrounds wiki pages were rendered in a browser because they are client-rendered or bot-guarded. No cookie banner was accepted.

---

## 1. GameDistribution (Azerion)

**Sources** (read 2026-11-27):
- SDK implementation wiki: https://github.com/GameDistribution/GD-HTML5/wiki/SDK-Implementation
- Wiki F.A.Q.: https://github.com/GameDistribution/GD-HTML5/wiki/F.A.Q.
- Quality guidelines, with tabs Quality Standards, SDK, Device Compatibility, Prohibited Practices and Promo Materials: https://gamedistribution.com/developers/quality-guidelines/
- Getting Started (HTML5/JS): https://gamedistribution.com/developers/faq/gd's-sdk-integration/getting-started-(html5js)/
- Interstitial Ads (HTML5/JS): https://gamedistribution.com/developers/faq/gd's-sdk-integration/interstitial-ads-(html5js)/
- Submitting your game: https://gamedistribution.com/developers/faq/getting-started/submitting-your-game/
- Developers page: https://gamedistribution.com/developers/ (requirement to implement the SDK, review up to 3 weeks)
- Developer terms and conditions, §2.4 and §2.6.x: https://static.gamedistribution.com/terms/developer.html

| # | Requirement (paraphrase) | Status | Evidence |
| --- | --- | --- | --- |
| GD-1 | The SDK is mandatory; the game is refused without it (terms §2.6.3, developers FAQ). | Met | `package-portal.py` profile loads `html5.api.gamedistribution.com/main.min.js` |
| GD-2 | Set the registered `gameId` in `GD_OPTIONS`. | **Not met** | The ID comes from `--game-id` or `GLOB2_GAMEDISTRIBUTION_GAME_ID`, otherwise the placeholder `000…0`. The game is not registered yet (`docs/releases/gamedistribution.md`, Open items). |
| GD-3 | Load the SDK only once, in the page head or during loading, never on a click. | Met | It is injected once, before the game scripts, after `GD_OPTIONS` is set. |
| GD-4 | Do not modify or interfere with the SDK (terms §2.4). | Met | It is loaded unmodified from GD's CDN. `onEvent` wraps any existing handler and does not replace it. |
| GD-5 | Wait for `SDK_READY` before the first ad request. | **Not met** | `gamedistribution.js` only handles `SDK_GAME_PAUSE` and `SDK_GAME_START`, and has no readiness gate. In practice the first `showAd` comes after a 54 MB load and some menu clicks, so the SDK is very likely ready, but the code does not check. |
| GD-6 | Pause the game and mute all audio on `SDK_GAME_PAUSE`. | Met | Calls `audio.pause()` (every `AudioContext` suspended), `session.hold(true)` (no frames, so no simulation or input) and `breaks.started()`. |
| GD-7 | Resume the game and unmute on `SDK_GAME_START`. | Met | Calls `audio.resume()`, `session.hold(false)` and `breaks.finished()`. |
| GD-8 | Show a pre-roll as early as possible, ideally on the Start/Play button of the splash or loading screen. | Met (later than ideal) | `firstStart: true`: the pre-roll runs at the first match `start`, after the player chooses to play. That is a play action, but it comes after menu navigation, not on a splash Play button. |
| GD-9 | Show mid-rolls only on non-gameplay buttons between sessions (Next, Replay, Menu on Game Over/Win). | Met | Breaks run only at `start` and `leave` (`portal-core.js` `createBreaks`); `pause`, `resume` and `end` never request one. |
| GD-10 | Ads only in response to user input, never during gameplay. | Met | Both break points follow a player choice, and gameplay is held during the break. |
| GD-11 | Call `showAd()` from inside a touchUp/mouseUp event so it works on mobile. | **Not met** | `matchBreak` is reached from the game loop through `ApplicationHost::matchBreak` (`GameSessionScreen.cpp:92`), not synchronously inside a DOM input handler. It relies on the browser's transient user activation surviving until the next frame. Untested on iOS. |
| GD-12 | Check that `gdsdk` and `showAd` exist before calling, so a blocked script is harmless. | Met | `typeof win.gdsdk?.showAd === 'function'`. A missing SDK releases the break. |
| GD-13 | Disable ad-trigger buttons while an ad shows. | Met | While `held` is true the game runs no screen frames. |
| GD-14 | `showAd` may be called freely; the SDK throttles. If the game has its own timer, match the SDK's. | Unknown | Our gap is 3 minutes after every break, including the pre-roll. GD does not publish its interval, so we cannot tell whether they match. |
| GD-15 | Leave `debug` off in uploads. | Met | The packager never sets `debug`. |
| GD-16 | Activation: open the uploaded game in the dashboard iframe and watch the pre-roll to the end (`CONTENT_RESUME_REQUESTED`). Then complete the Checklist tab and Request Activation. | **Not met** (pending) | Blocked by GD-2: there is no registered game yet. |
| GD-17 | No ads other than GD's (Prohibited Practices; terms §2.6.8). | Met | No other ad code. Ads are on only for this policy. |
| GD-18 | No collection of users' personal data and no third-party tracking or analytics (Prohibited Practices; terms §2.6.8). | Met (by code) | `onlineSignIn: false` hides online play and sign-in. `ProblemReport::sendPolicy` returns `Portal`, so reports can only be saved to a file. No analytics SDK is present. |
| GD-19 | No outgoing requests or links at all (links, redirects, analytics, social; terms §2.6.7). | Met for links; **Unknown** for network | `externalLinks: false` hides every link button, and `ApplicationHost::openUrl` refuses links. `package-portal.py` fails on external references in `index.html`. No network capture was made of a portal package, so it is unconfirmed that zero cross-origin requests happen at runtime (for example from the online client constructed with `signIn=false`). |
| GD-20 | No contact details or website URLs shown in the game. | Met | `texts.en.txt` has no URLs. `CreditScreen` strips the one e-mail address in `authors.txt`. Third-party licence files that contain URLs are not shown by any screen. |
| GD-21 | Moderate branding only: logo on credits, loading screen and main menu. | Met | The wordmark appears only on the loading screen and main menu. |
| GD-22 | Own the IP, with proof available (terms §2.6.2). | Met | GPL project, our own art. Music provenance is in `platforms/web/assets/music/24k/sources.json`. |
| GD-23 | No explicit alcohol, drugs, sex, politics or offensive religious content. | Met | RTS with cartoon violence only. |
| GD-24 | At least English (terms §2.6.5). | Met | English is the default, chosen from the browser's languages. |
| GD-25 | The GD version must match the latest version published elsewhere (terms §2.6.4). | Met (process) | The portals job builds the GD zip from the same release as every other channel. Each new tag needs a re-upload. |
| GD-26 | Scale to full screen in the iframe on desktop Chrome and Safari, with no cuts. Mobile support preferred. | Unknown | The canvas follows `innerWidth`/`innerHeight` and `visualViewport` (`shell.html`). The single-threaded runtime in Safari inside a GD iframe has not been tested. |
| GD-27 | Keyboard and mouse controls. | Met | Native RTS controls. |
| GD-28 | Thumbnails in JPG: 512×384, 512×512 and 200×120 required; 1280×720 and 1280×550 recommended. | Met (made, not uploaded) | `glob2-marketing/assets/portal-art/gamedistribution/`, all five sizes. |
| GD-29 | No identical game already in the catalogue (developers page). | Unknown | Not checked against GD's catalogue. |
| GD-30 | Upload size or file-count limit. | N/A | GD publishes none. The build is 132 MB and 495 files. |

**Prioritized Not met items and fixes (GameDistribution)**
1. **GD-2 / GD-16, no game ID.** Register the game in the GD dashboard and set the `GLOB2_GAMEDISTRIBUTION_GAME_ID` repository variable on the release mirror. Rebuild the upload, upload it, watch the pre-roll in the dashboard iframe, then complete the Checklist and Request Activation.
2. **GD-11, `showAd` not called inside an input handler.** Remember the last `pointerup`/`touchend`/`mouseup` time in `gamedistribution.js` and call `showAd()` from that handler when a break is pending. Alternatively, make `matchBreak('start')` for the pre-roll fire from the Play click's DOM event. At minimum, test the pre-roll on iOS Safari inside an iframe before submitting.
3. **GD-5, no `SDK_READY` gate.** Track `SDK_READY` in `onEvent`. If the pre-roll is due before it arrives, either wait for it (within the existing 10 s start timeout) or skip the break without starting the 3 minutes.
4. Before submitting, turn the Unknowns GD-19 and GD-26 into checks. Run the GD zip unpacked in headless Chromium and confirm there are no cross-origin requests. Run it in Safari in an iframe.

---

## 2. GamePix

**Sources** (read 2026-11-27):
- Submission guidelines: https://partners.gamepix.com/guidelines/submission
- JavaScript SDK documentation: https://partners.gamepix.com/sdk/doc/javascript

| # | Requirement (paraphrase) | Status | Evidence |
| --- | --- | --- | --- |
| GP-1 | Only the GamePix SDK (or Xsolla); no other third-party SDKs and no external ads. | Met | The profile loads only `gamepix.sdk.js` v3. |
| GP-2 | Set `GamePixConfig = {lifecycle:'manual'}` before the SDK script. | Met | Injected in the same inline script, before the SDK. |
| GP-3 | Load the SDK before any script uses `localStorage`. | Met | The SDK is the first injected script, before any game script. |
| GP-4 | Report `lifecycle.loading(n)` as whole numbers from 0 to 100 that never decrease. | Met | `session.progress` floors the value, clamps it and drops non-increasing values. The 2026-11-26 Testing Toolkit run showed LOADING 0–100. |
| GP-5 | Call `lifecycle.loaded()` when assets are ready. | Met | Called when the body gets the `ready` class. LOADED was seen in the Toolkit. |
| GP-6 | Call `lifecycle.gameStart()` when real gameplay starts (the first level or active loop), not at load. | **Not met** | `gamepix.js` calls `gameStart()` right after `loaded()`, at the main menu. GAME_START appeared at load in the Toolkit run. |
| GP-7 | Register both `pause` and `resume` handlers. | Met | `GamePix.events.on('pause'/'resume', …)` in `attach()`. The Toolkit's Pause and Resume reached the game. |
| GP-8 | `pause` must stop gameplay, timers, physics and input as well as audio. | **Not met** | `adapter.pause` is `audio.pause` only, which mutes. It does not call `session.hold`, so the simulation keeps running during a GamePix-initiated pause. The GameDistribution adapter does hold the game. Our own ad breaks still hold through `createBreaks`. |
| GP-9 | `resume` restores audio only if the game's own mute setting allows it. | Unknown | `audio.resume` resumes every suspended context. The game's volume settings act inside those contexts, so this should hold, but it has not been checked by ear. The 2026-11-26 Toolkit run did not check audio. |
| GP-10 | Handlers must be idempotent. | Met | Pause state is a flag set (`portal-core.js` `createAudio`). |
| GP-11 | Ad calls only after `loaded()` has completed. | Met | No break before the first match, which comes after `loaded()`. |
| GP-12 | Interstitials only at natural breaks (level end, game over, back to menu, between sessions); never during play, never on a timer. | Met | Breaks run at `leave` and at later `start`s only. |
| GP-13 | Don't trigger several ads at once or too often; wait for each interstitial to resolve. | Met | One break at a time, held until the promise settles, then a 3-minute gap. |
| GP-14 | Rewarded ads rules. | N/A | No rewarded ads. |
| GP-15 | No external links of any kind (More Games, social, privacy policy, Rate Us, readable URLs). | Met | `externalLinks: false` (see GD-19, GD-20). |
| GP-16 | Load resources by relative path. | Met | The packager fails on root-absolute and external references. |
| GP-17 | No external analytics. | Met | None present. Problem reports are file-only on portals. |
| GP-18 | Works in an iframe of at least 640×480. | Unknown | The Toolkit ran at 800×450 desktop. 640×480 itself was not tested. |
| GP-19 | Include a loading screen. | Met | The shell's download bar and loading note. |
| GP-20 | Remove any main-menu quit button. | Met in `v0.11.8.3`+; **Not met** in the 0.11.8.2 Toolkit upload | Hide Quit in portal mode (#1938) is in `v0.11.8.3`. Earlier uploads still show Quit. |
| GP-21 | Viewport meta with `user-scalable=no`. | **Not met** | `shell.html:5` sets `width=device-width,initial-scale=1,viewport-fit=cover,interactive-widget=resizes-visual`, with no `user-scalable=no`. |
| GP-22 | `touch-action:none` on the body. | **Not met** | Only the canvas has `touch-action:none` (`shell.html:22`). |
| GP-23 | Read screen size from `innerWidth`/`innerHeight`, and detect rotation with resize events. | Met | `shell.html` (pending viewport from `innerWidth`/`innerHeight`, `visualViewport` resize). |
| GP-24 | No "rotate device" prompts; support both orientations with the canvas centred. | Unknown | Not verified on a phone inside a GamePix frame. |
| GP-25 | Pause when page visibility changes, but not on clicks outside the iframe. | Met | The game stops frames and audio while hidden (`portal-core.js` `watchShell`, the shell's visibility handler). Focus loss does not pause. |
| GP-26 | Stop audio on incoming calls or when the browser pauses. | Unknown | Covered only as far as the browser hides the page. Not tested. |
| GP-27 | No system popups. | Unknown | No `alert`/`confirm`/`beforeunload` in `shell.html`. Game code paths were not exhaustively checked. |
| GP-28 | Support several languages, pick the system language, fall back to English. | Met | `shell.html:530` uses the saved preference, then `navigator.languages`, then `en`, with about 30 translations. |
| GP-29 | Multiplayer games must use `updateRoom`/`leftRoom`, invite links and guests. | N/A | Online play is hidden on GamePix (`onlineSignIn: false`). Whether online play can be enabled later is an open question to GamePix. |
| GP-30 | Light saves in `localStorage`; GamePix syncs only `localStorage`. | N/A (guidance) | Saves are in IndexedDB and stay on the device. This is allowed, but they do not sync across devices. |
| GP-31 | No malicious, explicit or religious content; complete games only; licensed templates; no duplicates. | Met | Complete original game, no template. |
| GP-32 | Game name matches in namespace and display; icon and cover show the matching title. | Met (made) | Icon and cover made 2026-11-26 (`glob2-marketing/assets/portal-art/README.md`). Not verified on the dashboard. |
| GP-33 | Upload size or file-count limit. | Unknown | No figure is published ("no file size limit specified"). Our 200 MB cap is from the Toolkit's observed behaviour. File count is unanswered (`docs/releases/gamepix.md`, Open items). |

**Prioritized Not met items and fixes (GamePix)**
1. **GP-8, `pause` does not stop gameplay.** In `gamepix.js`, make the `pause` handler call `session.hold(true)` and the `resume` handler call `session.hold(false)`, as `gamedistribution.js` does, keeping both idempotent. Without this, a GamePix overlay pause leaves the simulation running.
2. **GP-20, Quit visible in the uploaded 0.11.8.2.** Upload `v0.11.8.3` or later, which includes #1938, before submitting.
3. **GP-6, `gameStart()` called at the main menu.** Call it on the first `matchBreak('start')` (first real gameplay) instead of in `loaded`. `loaded()` stays at the main menu.
4. **GP-21 / GP-22, viewport and touch.** In the GamePix package only, add `user-scalable=no` (with `maximum-scale=1`) to the viewport meta and set `touch-action:none` on `body`. The packager's inline injection is the natural place, so the shared shell is unchanged.
5. Close the Unknowns GP-18 and GP-24: run the Toolkit at 640×480, and on a phone in both orientations.

---

## 3. Newgrounds

**Sources** (read 2026-11-27, public pages, not signed in):
- Games and Movies: https://www.newgrounds.com/wiki/help-information/content-submission/games-and-movies
- Game Guidelines (Terms of Use for games): https://www.newgrounds.com/wiki/help-information/terms-of-use/game-guidelines
- Project System: https://www.newgrounds.com/wiki/help-information/content-submission/project-system
- FAQ: https://www.newgrounds.com/wiki/frequently-asked-questions (no file-size figure found)

| # | Requirement (paraphrase) | Status | Evidence |
| --- | --- | --- | --- |
| NG-1 | HTML5 games upload as a ZIP with `index.html` at the root, loaded in an iframe. | Met | The packager writes `index.html` at the zip root and verifies it. |
| NG-2 | Zero body margins recommended. | Met | `shell.html:18`, `html,body{margin:0}`. |
| NG-3 | Tick the project form's details, such as "touchscreen friendly". | Unknown | This is a form setting, chosen at upload. |
| NG-4 | File size limit. The wiki gives no figure and says to request a raise if the limit is too small, so the limit is per account. | Unknown | `package-portal.py` caps uploads at 250 MB, a commonly cited figure that is not confirmed. Our 132 MB fits only if the account limit is at least that. Check the upload form. |
| NG-5 | File-count limit. | Unknown | None published. The build has 494 files. |
| NG-6 | At most two game or movie submissions per day. | N/A (process) | One project. |
| NG-7 | You must be the creator and owner, and it must not be a modified version of someone else's work. | Unknown | Globulation 2 is a GPL project with many historical authors. We publish as the maintainers. Newgrounds also asks that real contributors be credited on the project. Moderator interpretation is unknown, so credit the project and name the original team in the author comments. |
| NG-8 | You hold rights to all music, sprites and footage. | Met | Own art. Music provenance is in `platforms/web/assets/music/24k/sources.json`. |
| NG-9 | Disclose any use of AI in the author commentary. Prompt-generated games are not allowed. | **Not met** | Development is AI-assisted (commits co-authored by Claude), and the itch.io listing already carries a generative-AI disclosure for artwork and translations. `planning/portal-listing-copy.md` has no AI disclosure for Newgrounds. |
| NG-10 | Thumbnail represents the work: no AI-generated or bait-and-switch thumbnail. | Unknown | No dedicated Newgrounds thumbnail was found in `assets/portal-art/`. The rule must be met when one is chosen. |
| NG-11 | Proper content rating. | Unknown | A draft rating exists (`analysis/newgrounds-listing-comparison.md` discusses T versus E). It is set on the form at upload. |
| NG-12 | No auto-redirects and no pop-ups. | Met | Links open only from a player's click (`ApplicationHost::openUrl`). There is no automatic navigation. |
| NG-13 | Must play in the browser on Newgrounds, with no download or install. | Met | Browser build, single-threaded runtime without COOP/COEP. |
| NG-14 | Best not to rely on third-party servers. If the game calls any third-party API or anything that can track, notify the player at the start and offer an opt-out that is respected. | Unknown | The Newgrounds package keeps `onlineSignIn: true`, so online play and sign-in reach `app.glob2.online`, and problem reports can be sent (age-gated). Online play is opt-in, because the player has to choose Play online. There is no start-of-game notice, and no capture has confirmed that nothing contacts our servers before the player opts in. |
| NG-15 | Not shovelware made to serve ads or promote a site. | Met | No ads. A full game. |
| NG-16 | No hate speech, no prohibited adult content. | Met | |
| NG-17 | Not a pointless demo or preview. | Met | Complete game. |
| NG-18 | Newgrounds.io API (medals, scoreboards). | N/A (optional) | Not integrated. Listed as an open item. |

**Prioritized Not met items and fixes (Newgrounds)**
1. **NG-9, AI disclosure.** Add a short, accurate disclosure to the Newgrounds author commentary in `planning/portal-listing-copy.md`, saying what AI was used for (code assistance, any artwork or translations, matching the itch.io wording), and have the owner approve it before publishing.
2. Close NG-14 before publishing. Capture the network traffic of the Newgrounds package from load to the main menu. If anything reaches our servers before the player chooses online play, gate it behind that choice. Otherwise, consider a one-line note on the online hub that it connects to Globulation 2's own servers.
3. Confirm NG-4 (account file-size limit) on the project form, and request a raise if it is below 132 MB.

---

## 4. Game Jolt

**Sources** (read 2026-11-27):
- https://gamejolt.com/help/web-builds, cited in our docs and in the `package-portal.py` profile, **no longer exists**: it redirects to the Help Docs index (https://gamejolt.com/help-docs), which has no browser-build article.
- Site guidelines: https://gamejolt.com/help-docs/general/guidelines
- gjpush CLI README: https://github.com/gamejolt/cli
- Game Jolt publishes no current help page with browser-build limits.

| # | Requirement (paraphrase) | Status | Evidence |
| --- | --- | --- | --- |
| GJ-1 | HTML builds are a ZIP with `index.html` at the root. | Met | The packager verifies this. Game Jolt's own upload error states it, as reported in third-party forums, not an official help page. The 0.11.802 build was accepted and played on 2026-11-26. |
| GJ-2 | Browser-build size or file-count limit. | Unknown | The help article is gone and no figure is published. The profile enforces none. 132 MB and 494 files were accepted on 2026-11-26, which shows they currently fit. |
| GJ-3 | Release versions are semver (gjpush). | Met | The tag's fourth part is folded into the patch number (`docs/releases/gamejolt.md`). |
| GJ-4 | Don't upload a game you did not create. | Met | Maintainers of the project, game page 1122762 already live. Same note as NG-7 on crediting. |
| GJ-5 | No pornographic, sexually explicit or realistic gore content. | Met | |
| GJ-6 | No malware or phishing. | Met | |
| GJ-7 | No links to off-topic or monetized external sites in posts. | Met | This rule is about posts. The in-game links go to our own free site and Discord (`externalLinks: true`). |
| GJ-8 | No in-game ad or SDK requirement. | N/A | No SDK, no ads. Game Jolt runs its own site ads around the page. |
| GJ-9 | Game API (trophies, scores). | N/A (optional) | Not integrated. Listed as an open item. |

**Prioritized Not met items and fixes (Game Jolt)**
- None are Not met against a published rule.
- Housekeeping: replace the dead `https://gamejolt.com/help/web-builds` citation in `docs/releases/gamejolt.md` and in the `gamejolt` profile of `platforms/web/package-portal.py`. State instead that Game Jolt publishes no browser-build limits, and that 132 MB and 494 files were accepted on 2026-11-26.

---

## Cross-portal notes

- The Newgrounds doc (`docs/releases/newgrounds.md`) says the Newgrounds wiki was not readable without signing in. It is readable publicly once the bot guard passes in a real browser. The page states no size figure, only that limits can be raised on request.
- The gap between "Met by code" and "verified at runtime" is the same for every portal: there is no network capture of the portal packages yet (GD-19, NG-14). One headless Chromium run per package that logs cross-origin requests from load to the main menu and through one match would close it.
