# CrazyGames requirements audit (lite build)

[Analysis index](README.md) · [CrazyGames listing comparison](crazygames-listing-comparison.md)

Observed 2026-11-27. Each published CrazyGames requirement, checked against the
lite-edition upload built from glob2 `origin/master` at `e72a4ddc2a`. Read-only:
no code was changed and nothing was signed in to.

**Sources (official only):**
[intro](https://docs.crazygames.com/requirements/intro/),
[technical](https://docs.crazygames.com/requirements/technical/),
[gameplay](https://docs.crazygames.com/requirements/gameplay/),
[ads](https://docs.crazygames.com/requirements/ads/),
[account integration](https://docs.crazygames.com/requirements/account-integration/),
[multiplayer](https://docs.crazygames.com/requirements/multiplayer/),
[game covers](https://docs.crazygames.com/requirements/game-covers/),
[quality guidelines](https://docs.crazygames.com/requirements/quality/),
[SDK game module](https://docs.crazygames.com/sdk/game/),
[SDK data module](https://docs.crazygames.com/sdk/data/).

**Our build:** lite edition (English only, no editor, online or premade maps),
about 8 MB compressed startup download (QA Tool load 10.3 MB), 46.8 MB unpacked,
about 140 files, single-threaded. Policy `{externalLinks: false, onlineSignIn:
false, ads: true}`; Quit hidden. CrazyGames SDK v3 with `gameplayStart`/`Stop` on
match play, in-game menu and pause; `requestAd('midgame')` at natural breaks after
a match, never before the first match, with our own 3-minute gap. The QA Tool
passed with no warnings (owner-reported).

Code paths below are on glob2 `origin/master`. "Basic" and "Full" are the
CrazyGames launch stages: Full Launch requirements apply only once CrazyGames
selects the game after Basic Launch.

## Technical

| # | Requirement (paraphrase) | Stage | Status | Evidence |
| --- | --- | --- | --- | --- |
| T1 | Total size at most 250 MB | Basic | Met | 46.8 MB unpacked; `platforms/web/package-portal.py` profile `max_bytes=250 MB, size_basis="unpacked"` fails the build above it |
| T2 | At most 1,500 files | Basic | Met | about 140 files; profile `max_files=1500` |
| T3 | Initial download (start of load to first gameplay start) at most 50 MB | Basic | Met | QA Tool reported 10.3 MB |
| T4 | Initial download at most 20 MB for the mobile homepage | Mobile | Met | 10.3 MB QA Tool figure. `docs/releases/crazygames.md` still lists this as an open item; it can be closed |
| T5 | Relative paths only | Basic | Met | `package-portal.py` bundles root-absolute assets under relative paths and fails on any other root-absolute or external reference in `index.html` |
| T6 | Externally hosted files: time to gameplay 20 s or less | Basic | Not applicable | Everything is in the upload |
| T7 | Works on Chrome and Edge | Basic | Unknown | QA Tool pass was in one browser; check Edge on the live preview |
| T8 | Works well on Safari, or it is disabled there | Basic | Unknown | Check macOS and iOS Safari on the preview |
| T9 | Runs smoothly on a 4 GB RAM Chromebook | Basic | Unknown | Needs a low-memory ChromeOS device test |
| T10 | Mouse and keyboard; touch too if mobile is supported | Basic | Met | Desktop controls; touch layout exists (`platforms/web/tests/tutorial-phone.spec.js`) |
| T11 | Desktop playable in landscape | Basic | Met | Responsive presentation (`platforms/web/tests/responsive-presentation.spec.js`) |
| T12 | Use the SDK's system info for device-specific experiences, not touch detection | Mobile | Not met | `platforms/web/shell.html` `publishPresentationMetrics()` sets `touch: navigator.maxTouchPoints>0 \|\| (any-pointer: coarse)`, the detection CrazyGames names; `crazygames.js` never reads `SDK.user.systemInfo` |
| T13 | Supported orientations set in the submission | Mobile | Unknown | Portal submission field; not visible from code |
| T14 | `body` has `user-select: none` (with -webkit-, -moz-, -ms- prefixes) | Mobile | Not met | `shell.html` `html,body{...}` rules have no `user-select`; `package-portal.py` injects scripts only, no CSS |
| T15 | Works fullscreen in the CrazyGames app with safe-area padding | Mobile | Met (verify) | `shell.html` measures `env(safe-area-inset-*)` and passes it to the layout; confirm in the app |
| T16 | iOS audio: resume the AudioContext inside a user gesture | Mobile | Unknown | `shell.html` `focusGame()`/`activateAudio()` resume on `pointerdown` and `keydown`; CrazyGames names `touchend`/`click`. Check on an iPhone that sound starts after the first tap |
| T17 | Unity-specific rules (DPR, iOS disable) | — | Not applicable | Not a Unity game |
| T18 | Sitelock, if any, whitelists CrazyGames domains | — | Not applicable | No sitelock |
| T19 | Privacy/terms notice if personal data beyond SDK events is collected | Basic | Not applicable | Online sign-in, problem-report sending (`src/app/ProblemReport.cpp` `SendPolicy::Portal`) and external links are off in portals; nothing leaves the device |

## SDK (Full Launch unless noted)

| # | Requirement (paraphrase) | Stage | Status | Evidence |
| --- | --- | --- | --- | --- |
| S1 | Gameplay start when play begins or resumes; it also measures initial download | Basic if SDK used; Full | Met | `platforms/web/crazygames.js` `session` gameplay handler; `portal-core.js` `createSession`; QA Tool pass |
| S2 | Gameplay stop at every break (menu, level end, pause) | Full | Met | `portal-core.js` `matchBreak` `end`/`leave`/`pause`; `docs/releases/web-portals.md#ad-breaks` |
| S3 | Do not report gameplay stop on tab or focus changes | Full | Met | `crazygames.js` passes `{visibility: false}` to `createSession` |
| S4 | Loading start/stop (optional) | Full | Met | `connect()` calls `loadingStart()`, then `loadingStop()` at the interactive main menu |
| S5 | Respect the `muteAudio` setting, above in-game audio settings | Full | Met | `applySettings` and `addSettingsChangeListener`; `portal-core.js` `createAudio` re-suspends any context the game resumes while a reason holds it |
| S6 | `happytime()` only for special moments (optional) | — | Not applicable | Not used |
| S7 | `disableChat` honoured if the game has chat | — | Not applicable | Lite edition has no online play or chat |

## Gameplay

| # | Requirement (paraphrase) | Stage | Status | Evidence |
| --- | --- | --- | --- | --- |
| G1 | Text and images readable at DPR 1, in 16:9 iframes from 800×450 to 1920×1080 and on mobile | Basic | Unknown | Check the ten listed iframe sizes in the QA Tool / preview at DPR 1 |
| G2 | Physics the same at any refresh rate (144, 165 Hz) | Basic | Met | Fixed-tick deterministic simulation (`platforms/web/tests/determinism.spec.js`, `pacing.spec.js`) |
| G3 | English localisation; any translations accurate | Basic | Met | Lite edition is English only (`docs/browser/editions.md`, `translations` switch) |
| G4 | Use the SDK `locale`, falling back to English | Basic | Not applicable | Only English ships, which is the fallback |
| G5 | Intuitive controls on all devices | Basic | Unknown | Subjective; QA visual check |
| G6 | Loads quickly and plays without errors or crashes | Basic | Met (QA Tool) | QA Tool passed with no warnings |
| G7 | Original names, assets and content | Basic | Met | Our own game and assets |
| G8 | No custom in-game fullscreen button | Basic | Not met | Settings > Display offers "Window mode: Windowed / Fullscreen" on web desktop (`src/ui/settings/SettingsScreenGeneral.cpp` `display.mode`, not gated by `PortalPolicy`); F11 also toggles it (`libs/gag/src/GraphicContext.cpp`) |
| G9 | No cross-promotion of other games or platforms | Basic | Met | `externalLinks: false` hides Discord, privacy, guide and page links (`src/app/PortalPolicy.h`; `src/app/PortalModeTest.cpp`) |
| G10 | Suitable for 13+, PEGI 12 compliant | Basic | Unknown | Cartoon colony combat; no rating obtained. QA decides |
| G11 | New players land in gameplay, or at most one click away | Full | Not met | `docs/releases/crazygames.md`: load time "includes the first-run questions and menus"; the player passes first-run questions and the main menu before a match |

## Ads

| # | Requirement (paraphrase) | Stage | Status | Evidence |
| --- | --- | --- | --- | --- |
| A1 | Basic Launch: no ads; with the SDK, the game must not freeze when ads are disabled | Basic | Met | `adsDisabled` arrives as `adError`, which ends the break; `createBreaks` also releases after 10 s if no ad starts |
| A2 | Only ads requested through the CrazyGames SDK | Basic | Met | Only `SDK.ad.requestAd`; no other ad code |
| A3 | Ads not before a reasonable amount of gameplay | Full | Met | No break before the first match (`portal-core.js` `request`, `firstStart = false`) |
| A4 | Midgame ads only at logical points, never in active play | Full | Met | Only at `start` and `leave`; `pause`/`resume` never ask |
| A5 | No midgame ad on navigation buttons (main menu, settings, shop) | Full | Unknown | The `start` break runs after the player picks a match from the main menu. It is the start of a level, but it follows a main-menu button; ask CrazyGames QA whether that counts, or ask only at `leave` and tutorial-lesson transitions |
| A6 | No chained ads | Full | Met | One break at a time and a 3-minute gap after every break, so `leave` and the next `start` are one break |
| A7 | Game paused and progress blocked from the request until `adFinished`/`adError` | Full | Met | Session held from the request; `glob2PortalHost.held` stops screen frames, simulation and input |
| A8 | Unfilled or failed request: game continues normally | Full | Met | Every `adError` resolves the break |
| A9 | Mute only when the ad starts, unmute when it ends | Full | Met | `muteOnStart: true`; muted at `adStarted` |
| A10 | Respect the SDK's 3-minute midgame limit | Full | Met | SDK enforces `adCooldown`; ours adds a 3-minute gap |
| A11 | Rewarded and banner ad rules | — | Not applicable | Neither is used |
| A12 | Playable with an ad blocker, no penalty, no popups | Full | Met | A rejected `init()` leaves the game running without the SDK (`crazygames.js` `connect()`) |

## Account integration and saving

| # | Requirement (paraphrase) | Stage | Status | Evidence |
| --- | --- | --- | --- | --- |
| C1 | No external login options; guests can play | Basic | Met | `onlineSignIn: false` hides every sign-in (`src/app/PortalPolicy.h`) |
| C2 | No required in-game username or avatar | Basic | Met | No account in the portal build |
| C3 | Progress saved through the Data module, own back end, or Automatic Progress Save, where progress applies | Full | Not met | Saves, campaign progress and settings live only in IndexedDB on the device (`docs/browser/storage.md`, `platforms/web/shell.html` IDBFS mount); no Data module calls. The Data module page caps data at 1 MB and speaks only of localStorage; whether Automatic Progress Save covers IndexedDB is not documented |
| C4 | Use the CrazyGames username/avatar, automatic login | Full | Not applicable | The game has no accounts in the portal build |

## Multiplayer

| # | Requirement (paraphrase) | Status | Evidence |
| --- | --- | --- | --- |
| M1 | Room sharing, invites, instant multiplayer, chat controls | Not applicable | Lite edition has no online or LAN play |

## Submission materials

| # | Requirement (paraphrase) | Status | Evidence |
| --- | --- | --- | --- |
| P1 | Covers: 1920×1080, 800×1200 and 800×800, title-only text, no borders/icons | Unknown | Portal submission; see [listing comparison](crazygames-listing-comparison.md) |
| P2 | Preview videos: 15–20 s, at most 50 MB, landscape and portrait 1080p, silent, no cursor or promo text, open on the cover | Unknown | Portal submission |
| P3 | Description and controls metadata | Unknown | Portal submission |

## Quality guidelines (recommended, not mandatory)

| # | Guideline (paraphrase) | Status | Evidence |
| --- | --- | --- | --- |
| Q1 | Onboarding inside gameplay, skippable, visual | Unknown | Tutorial exists; first-run questions come first |
| Q2 | Avoid keys with browser behaviour such as Escape | Not met (guideline) | Escape opens and closes the in-game menu (`src/hud/draw/GameGUIDraw.cpp`, `src/hud/GameGUIDialog.cpp`); in fullscreen Escape also leaves fullscreen |
| Q3 | Adapt key bindings to the keyboard layout (AZERTY) | Unknown | Not checked |
| Q4 | Clear goals, easy to learn, consistent controls, good aesthetics | Unknown | Subjective |

## Not met, by priority

1. **G8 Custom fullscreen control (Basic, blocks review).** Hide the Settings > Display
   "Window mode" choice and ignore F11 when `PortalPolicy::current().portal` is true
   (`src/ui/settings/SettingsScreenGeneral.cpp`, `libs/gag/src/GraphicContext.cpp`
   key handler). CrazyGames, and every portal, provides fullscreen itself.
2. **T14 `user-select: none` on `body` (mobile).** Add
   `-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none`
   to the `body` rule in `platforms/web/shell.html` (harmless everywhere), or have
   `package-portal.py` inject it for portal uploads.
3. **T12 Device detection from the SDK (mobile).** In `crazygames.js`, after
   `init()`, read `SDK.user.systemInfo.device.type` and hand it to the shell's
   presentation metrics (for example a `Module.portalDevice` override that
   `publishPresentationMetrics()` prefers over `maxTouchPoints`).
4. **G11 Land in gameplay (Full Launch only).** For a first visit in a portal, skip
   the first-run questions and main menu and start the first tutorial lesson or a
   quick random match directly, with the menu reachable afterwards.
5. **C3 Progress saving (Full Launch only).** Mirror the save directory into the
   Data module (`SDK.data.setItem`/`getItem`) for portal builds, within its 1 MB
   cap, or ask CrazyGames whether Automatic Progress Save covers IndexedDB.
6. **Q2 Escape key (guideline only).** Optional: also accept another key (for
   example P or F10) for the in-game menu so players in fullscreen do not lose it
   on Escape.

Unknown items to check on the live preview or a device: T7 Edge, T8 Safari,
T9 4 GB Chromebook, T13 orientation setting, T16 iOS audio after first tap,
G1 readability at the ten iframe sizes, G5 controls, G10 PEGI 12, A5 ad after a
main-menu Play click, P1–P3 submission materials, Q1, Q3, Q4.
