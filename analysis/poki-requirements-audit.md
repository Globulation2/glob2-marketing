# Poki requirements audit (lite build)

[Analysis index](README.md) · [Poki listing comparison](poki-listing-comparison.md)

Observed 2026-11-27. Each published Poki requirement, checked against the
lite-edition upload built from glob2 `origin/master` at `e72a4ddc2a`. Read-only:
no code was changed and nothing was signed in to.

**Sources (official only):**
[requirements & quality](https://developers.poki.com/guide/requirements-quality),
[SDK overview & events](https://developers.poki.com/guide/sdk-overview),
[PokiSDK: HTML5](https://developers.poki.com/guide/sdk-html5),
[external resources policy](https://developers.poki.com/guide/external-resources-policy),
[content & player safety](https://developers.poki.com/guide/content-player-safety),
[easy access & onboarding](https://developers.poki.com/guide/easy-access),
[localization](https://developers.poki.com/guide/localization),
[game thumbnail](https://developers.poki.com/guide/game-thumbnail),
[user accounts](https://developers.poki.com/guide/accounts),
[Poki Inspector](https://developers.poki.com/guide/inspector),
[web fit test](https://developers.poki.com/guide/web-fit-test),
[final review](https://developers.poki.com/guide/final-review).

**Our build:** lite edition (English only, no editor, online or premade maps),
about 8 MB compressed startup download, 46.8 MB unpacked, about 140 files,
single-threaded. Policy `{externalLinks: false, onlineSignIn: false, ads: true}`;
Quit hidden. Poki SDK v2; `gameLoadingFinished()` at the interactive main menu;
`gameplayStart`/`Stop` on match play, in-game menu, pause and page visibility;
`commercialBreak()` at natural breaks after a match, never before the first match,
with our own 3-minute gap. Verified in the Poki Inspector with no warnings
(owner-reported). Code paths below are on glob2 `origin/master`.

**Size:** Poki publishes no file-size or initial-download limit. The only number is
that players leave when loading takes more than about 10 seconds; it asks for a
small build and progressive loading.

## Hard requirements

| # | Requirement (paraphrase) | Status | Evidence |
| --- | --- | --- | --- |
| H1 | Works on desktop, mobile and tablet; covers the full screen on mobile | Unknown | Touch layout exists (`platforms/web/tests/tutorial-phone.spec.js`, `responsive-presentation.spec.js`); confirm with the Inspector's mobile QR mode on a phone and a tablet |
| H2 | 16:9, scaled to fill 640×360, 836×470 and 1031×580 | Unknown | Layout is responsive to the frame; check legibility at 640×360 with Inspector Scaling Tests |
| H3 | Playable in incognito: storage failures must not break the game | Unknown | Saves use Emscripten IDBFS (IndexedDB), not localStorage (`platforms/web/shell.html` `FS.mount(IDBFS...)`); a failed restore is logged and play continues (`platforms/web/tests/storage.spec.js` fault tests). Check a private window in Safari and Firefox where IndexedDB may be missing or throw |
| H4 | No external requests; fonts, assets and libraries bundled | Met | `package-portal.py` bundles fonts and brand assets and fails on any external reference in `index.html`; online client and problem-report sending off in portals (`src/app/PortalPolicy.h`, `src/app/ProblemReport.cpp`); Inspector showed no External Resources warning |
| H5 | No splash screens, outgoing links or external ads; a logo on the loading screen is allowed | Met | Loading page shows only the wordmark; `externalLinks: false` hides every outgoing link (`src/app/PortalModeTest.cpp`); no other ad code |
| H6 | Playable with an ad blocker | Met | `poki.js` `connect()`: a rejected `init()` leaves the SDK unused and the game runs |

## SDK events

| # | Requirement (paraphrase) | Status | Evidence |
| --- | --- | --- | --- |
| E1 | Load the SDK in `<head>`; continue the game whether `init()` resolves or rejects | Met | Injected before the first script, which is in `<head>` (`package-portal.py` `first_script`; `shell.html` line 8); `poki.js` `connect()` |
| E2 | `gameLoadingFinished()` when loading completes | Met | `poki.js` `finish()` once the session is ready and `init()` resolved |
| E3 | `gameplayStart()` on the player's first input or level start, not on load | Met | Fires when a match the player chose starts (`portal-core.js` `matchBreak('start')`) |
| E4 | `gameplayStop()` on pause, menu, level end, quit to menu | Met | `end`, `leave`, `pause` points; `docs/releases/web-portals.md#ad-breaks` |
| E5 | Never the same event twice in a row | Met | `createSession` reports only changes; Inspector event log clean |
| E6 | No SDK events while a commercial or rewarded break plays | Met | The session is held for the whole break; visibility changes while held report nothing |
| E7 | `gameplayStop()` → `commercialBreak()` → `gameplayStart()`; mute audio and disable input during the break | Met | Hold reports stop before `show()`, audio silenced from the request, `glob2PortalHost.held` stops frames and input; start reported after release |
| E8 | `commercialBreak()` only when leaving a pause back into gameplay | Not met | `portal-core.js` also requests a break at `leave` (finished match back to the main menu), which returns to a menu, not gameplay |
| E9 | Call `commercialBreak()` before every `gameplayStart()` that follows a break, as many opportunities as possible | Not met | No break before the first match (`firstStart = false`), none on `resume` from the in-game menu or pause, and none within our own 3 minutes; Poki's pause/unpause sequence includes one |
| E10 | No internal ad timers; Poki manages frequency | Not met | `createBreaks` `minInterval = 180000` skips every request for 3 minutes after each break; `poki.js` does not override it |
| E11 | Rewarded-break rules | Not applicable | No rewarded ads |
| E12 | Keyboard games: Escape or Space pauses and resumes, with the matching events | Met | Escape opens and closes the in-game menu (`src/hud/draw/GameGUIDraw.cpp`, `src/hud/GameGUIDialog.cpp`), reported as `pause`/`resume` |
| E13 | Arrow keys, Space and wheel must not scroll the parent page | Unknown | `html,body{overflow:hidden}` in `shell.html`; no explicit `preventDefault` on `wheel` with `passive:false` or on ArrowUp/ArrowDown/Space keydown in the shell (SDL may do it on the canvas only). Check scrolling the Poki playground page over the loading screen and the game |

## Technical standards and UX

| # | Requirement (paraphrase) | Status | Evidence |
| --- | --- | --- | --- |
| U1 | Clean build: no development tools or debug code | Met | Lite: runtime assertions off, MCP and CLI tools off (`docs/browser/editions.md`); AI telemetry hidden in portals (`src/hud/GameGUIDialog.cpp`) |
| U2 | Save progress, or tell players it is not saved | Met | Saves, campaign progress and settings persist in IndexedDB (`docs/browser/storage.md`) |
| U3 | Fast loading (players leave after about 10 s); progressive loading | Unknown | About 8 MB compressed before the menu; optional packages load later (`platforms/web/asset-loader.js`). Read the Inspector's Game Details load time on a mid-range phone and slow network |
| U4 | Static and animated thumbnails | Unknown | Static: square, at least 628×628, full-bleed, no text, not close to `#83FFE7`. Animated: needed before Global Release. Portal submission |
| U5 | Force mobile controls on tablets; controls shown match the device | Unknown | Touch layout follows `maxTouchPoints > 0` or `(any-pointer: coarse)` (`shell.html` `publishPresentationMetrics`), which should cover tablets; confirm on an iPad and an Android tablet |
| U6 | Few screens and menus, ideally straight into gameplay | Not met | First-run questions and the main menu come before the first match (`docs/releases/crazygames.md` notes the same flow) |
| U7 | Cutscenes and intros skippable | Unknown | Check the first-run flow and tutorial intro |
| U8 | Visual rather than text-heavy tutorials | Unknown | Tutorial is text-led; subjective |
| U9 | Privacy policy in game when anything links out or analytics run | Not applicable | No external links or analytics in the portal build |
| U10 | Localization (recommended for text-heavy games); use `PokiSDK.getLanguage()` | Not applicable | English only by design; Poki makes it a recommendation, not a requirement |
| U11 | Cloud saves: synced from localStorage/IndexedDB for logged-in Poki users, at most 1 MB gzip | Unknown | IDBFS store under `/home/web_user` holds saves, maps, campaign and settings; its gzip size per player is unmeasured and nothing is prefixed `poki_ignore`. Over 1 MB disables cloud saves for that player |

## Ads, content and monetisation

| # | Requirement (paraphrase) | Status | Evidence |
| --- | --- | --- | --- |
| M1 | Implement `commercialBreak()`/`rewardedBreak()` as appropriate | Met | `poki.js` `createBreaks` `show` |
| M2 | Mute game audio during ads | Met | `portal-core.js` silences every AudioContext from the request until release |
| M3 | No custom "ad blocked" messages | Met | None |
| M4 | Only Poki's ad system | Met | No other ad code |
| M5 | No in-app purchases or ad-removal UI | Met | Nothing is sold (`docs/releases/web-portals.md`) |
| M6 | No chat; profanity filter for multiplayer usernames | Not applicable | Lite edition has no online play or chat |
| M7 | No external account systems or personal data | Met | `onlineSignIn: false` hides every sign-in |
| M8 | Family-friendly content, original, web-first | Unknown | Cartoon colony combat; Poki's content moderation decides |

## Poki Inspector QA modules

The guide says the QA modules sit in the Inspector's left panel but does not list
them or their checks, so the module names below come from the Inspector itself and
each is mapped to the rows above. The owner reports a run with no warnings; the
per-module checklists were not available to this audit.

| Module | Status | Rows |
| --- | --- | --- |
| SDK Basics | Met (Inspector) | E1–E7, E12 |
| Technical Stability | Unknown | H3, U3; no published checklist |
| Mobile Optimization | Unknown | H1, H2, U5 |
| Privacy & Security | Met (Inspector) | H4, H5, M7, U9 |
| Playground Integration | Unknown | E13 |
| Ad Implementation | Not met against the written guide | E8, E9, E10 (the Inspector raised no warning) |

## Not met, by priority

1. **E10 Internal ad timer.** Pass `minInterval: 0` to `core.createBreaks` in
   `platforms/web/poki.js` so every natural break reaches `commercialBreak()` and
   Poki's own timer decides. Keep the 3-minute gap for the other portals.
2. **E8 Break when returning to the menu.** For Poki, request a break only on the
   way into gameplay: skip `leave` (give `createBreaks` an option such as
   `points: ['start']`), so the break runs when the player starts the next match.
3. **E9 Break before every return to gameplay.** For Poki, also signal at
   `resume` from the in-game menu or a pause, and at the first match
   (`firstStart: true`); Poki will not show an ad until its own timer allows. Do
   E8 and E10 first, then decide on `resume` after a playtest, since a break on
   every unpause can feel heavy in a strategy game.
4. **U6 Straight into gameplay.** For a first visit in a portal, skip the first-run
   questions and main menu and open the first tutorial lesson or a quick match;
   this also helps the Web Fit Test's conversion-to-play metric.

Unknown items to check in the Inspector or on devices: H1 phone and tablet,
H2 16:9 scaling at 640×360, H3 private windows, E13 page scroll, U3 load time on
mobile, U4 thumbnails, U5 tablet controls, U7 skippable intro, U8 tutorial style,
U11 save size against the 1 MB cloud-save cap, M8 content review, and the
Technical Stability, Mobile Optimization and Playground Integration checklists.
