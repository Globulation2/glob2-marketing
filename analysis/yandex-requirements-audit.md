# Yandex Games requirements audit (lite upload)

Observed 2026-11-27. This audit checks the Yandex Games upload of Globulation 2 against each numbered item in Yandex's published requirements. Code evidence is from glob2 `origin/master` at `e72a4ddc2a`. Nothing was signed in to, so every item that depends on the Developer Console draft or on moderation is marked Unknown. "Check on draft" means: open the draft with `&debug-mode=16` and look at the debug panel, or look at the draft's fields.

**Build audited:** the lite edition, packaged by `platforms/web/package-portal.py --portal yandex`. It is English only, with no editor, no online play and no premade maps. It downloads about 8 MB before the menu, unpacks to 46.8 MB in 138 files (figures supplied by the caller) and runs single-threaded. Its policy is `{externalLinks:false, onlineSignIn:false, ads:true}`. The earlier local package of 0.11.8.2 measured 45.8 MB unpacked ([web portal rollout](../planning/web-portal-rollout.md)).

**Sources (official only):**

- Requirements: https://yandex.com/dev/games/doc/en/concepts/requirements
- Detail pages: https://yandex.com/dev/games/doc/en/requirements/1/19, https://yandex.com/dev/games/doc/en/requirements/2/14, https://yandex.com/dev/games/doc/en/requirements/8/2/3
- SDK: https://yandex.com/dev/games/doc/en/sdk/sdk-about (connection), https://yandex.com/dev/games/doc/en/sdk/sdk-game-events (LoadingAPI, GameplayAPI), https://yandex.com/dev/games/doc/en/sdk/sdk-events (game_api_pause/resume), https://yandex.com/dev/games/doc/en/sdk/sdk-adv (showFullscreenAdv), https://yandex.com/dev/games/doc/en/sdk/sdk-environment (i18n)
- Languages: https://yandex.com/dev/games/doc/en/concepts/languages-and-domains

## Language rules (what the docs say)

- **English only is not forbidden.** No page read states a minimum number of languages, and none makes Russian mandatory. Russian appears only in the recommended language set for reach ("languages and domains") and in the example list for 6.9.
- **Automatic detection is still required (2.14).** The 2.14 detail page says the rule also covers single-language games. The game must read `ysdk.environment.i18n.lang` at launch, not during play. On the debug panel the 文 indicator must turn green at startup. A short delay during loading is acceptable, but green only after "Play" fails.
- **Moderation checks only the declared languages.** It tests every language in the draft's "Game translated into" field (2.14 detail page). 8.2.3 requires gameplay text to be in the selected language, with no mixing of two languages. An English-only game should therefore declare English only.
- **Domains:** yandex.ru (Russia), yandex.com.tr (Türkiye) and yandex.com (multilingual) are listed. The pages read do not say whether an English-only game is offered to players on yandex.ru, or how declared languages map to domains: Unknown.
- **Listing text versus game text:** AI descriptions translate only the game card. The game's own interface must be localised separately (languages and domains page). Translating the listing into Russian therefore does not make the game Russian.

## 1. Technical requirements

| # | Requirement (paraphrase) | Status | Evidence |
| --- | --- | --- | --- |
| 1.1 | Yandex Games SDK installed | Met | `platforms/web/package-portal.py:145-146` injects `/sdk.js` before `portal-core.js` and `yandex.js`. `verify()` at `package-portal.py:293` onward enforces that order. |
| 1.2 | Playable with no third-party registration; only Yandex ID login via the SDK | Met | The policy has `onlineSignIn:false` (`package-portal.py:147`, `src/app/PortalPolicy.cpp:19`). The lite edition has no online client (`docs/browser/editions.md:28`). The game has no login at all. |
| 1.2.1 | Login only on a deliberate action, with its benefits explained | Not applicable | No login. |
| 1.2.2 | Guest play available and progress saved | Met | No account is needed. Saves are kept in IndexedDB on the device (`docs/releases/web-portals.md:146-147`). |
| 1.3 | Sound stops when the game loses focus | Not met (focus case); Met (hidden tab) | Audio is suspended when the page is hidden (`platforms/web/audio.js:156-168`) and on `game_api_pause` (`platforms/web/yandex.js:64`). Nothing handles window `blur`, so sound keeps playing when focus moves to another window that leaves the tab visible. The platform's pause events cover tab switches and minimising, not plain focus loss (sdk-events). Check on draft: click into another window and listen. |
| 1.4 | Payments only through the SDK | Not applicable | Nothing is sold (`docs/releases/web-portals.md:27-28`). |
| 1.6 | Meets the rules for each device type selected in the draft | Unknown | Depends on which device types the draft selects. |
| 1.6.1.1 | Mobile: full screen at launch and in play | Unknown | Page and canvas fill 100% (`platforms/web/shell.html:18-21`). Not tested on Yandex's mobile page. Phone layout depends on the host page's viewport tag ([rollout notes](../planning/web-portal-rollout.md)). |
| 1.6.1.2 | Mobile: keyboard opens when a text field is tapped | Unknown | The shell creates real input elements for text fields (`shell.html:711-718`). Not tested on a phone through Yandex. |
| 1.6.1.5 | Mobile: fully gesture-controlled | Unknown | Touch input exists (the CrazyGames lite run in the iPhone simulator worked by touch, per the rollout notes). Not tested on Yandex. |
| 1.6.1.6 | Mobile: no system player opens | Met | The lite edition has no video assets (`editions.md:33`). |
| 1.6.1.7 | Mobile: no WebGL notification on open | Unknown | Check on draft on a phone. A software renderer fallback exists (`shell.html:331`). |
| 1.6.1.8 | Mobile: long tap does not select or open a context menu | Unknown | The canvas cancels `contextmenu` and sets `touch-action:none` (`shell.html:22`, `:78`). No `user-select` or `-webkit-touch-callout` rule exists for the loading page text. Check on iOS and Android. |
| 1.6.2.1 | Desktop: fills the available space, excluding sticky banners | Unknown | Fills its iframe (`shell.html:18-21`). Check on draft. |
| 1.6.2.2 | Desktop: long side at most twice the short side | Unknown | The canvas follows the iframe. Yandex sets the frame, so check on draft. |
| 1.6.2.4 | Desktop: keyboard or mouse by default, independent of keyboard layout | Unknown | The game can be played fully with the mouse. Whether letter shortcuts still work on a Russian layout is not verified. |
| 1.6.2.5 | Desktop: no system player | Met | No video in lite (`editions.md:33`). |
| 1.6.2.6 | Desktop: no shortcuts reserved by the OS or other apps | Unknown | Ctrl/Cmd+R and +L pass to the browser (`shell.html:839-847` (`preserveBrowserShortcut` at :842)). The game's full shortcut list was not audited. |
| 1.6.2.7 | Desktop: interacting with the field does not highlight it or open a context menu | Met | `oncontextmenu="event.preventDefault()"` and `outline:none` on the canvas (`shell.html:22`, `:78`). |
| 1.6.3.x | TV: full screen, remote arrows, Back/OK, no purchases, no links to other games | Unknown / likely not applicable | The adapter does not handle `HISTORY_BACK` (`yandex.js` has no handler). The game cannot be played with arrow keys alone. Do not select TV in the draft. |
| 1.7 | No absolute URLs to Yandex S3 | Met (index.html) | The SDK loads by the relative path `/sdk.js` (`package-portal.py:145`). `verify()` rejects any external reference in `index.html` (`package-portal.py:39`, `:326` onward). Game JS and data files are not scanned. |
| 1.8 | Interactive elements fit the screen and are easy to use | Unknown | Check on draft on desktop and phone. |
| 1.9 | Progress saved on action or via a save button, and kept after refresh or rotation | Unknown | The in-game save goes to IndexedDB (`web-portals.md:146-147`). Whether moderators accept manual saves for an RTS match is not stated. Check that campaign progress survives a refresh in the Yandex iframe. |
| 1.10.1-1.10.4 | Correct rendering on resize and rotation; no browser scroll or swipe-to-refresh; no overlap; one-handed play | Unknown | Page scrolling is blocked by `overflow:hidden` (`shell.html:18`) and `touch-action:none` on the canvas (`:22`). No `overscroll-behavior` is set. Check rotation and resizing on draft. |
| 1.11 | Cloud-save option enabled if cloud saves are used | Not applicable | No cloud saves. Leave the option off. |
| 1.12 | Monetised by ads or in-app purchases | Met (code); Unknown (console) | `ads:true` (`package-portal.py:147`). Fullscreen ads run (`yandex.js:46-57`). Check that ads are enabled in the console. |
| 1.13.x | In-app purchase rules | Not applicable | No purchases. |
| 1.14 | No errors, freezes or crashes, including on rotation, ads, minimising or history navigation | Unknown | Needs a test pass on draft. Not run on the Yandex page yet (the rollout notes record only a local simulated-portal load). |
| 1.15 | Finished game with all elements implemented | Met | Lite keeps the campaigns, tutorial and random maps (`editions.md:44`). Features that are off are left out of the menus, not shown disabled (`editions.md:53-55`). |
| 1.16 | Ad units unaltered; no fake ads | Met | Only `ysdk.adv.showFullscreenAdv` is called, with no custom UI (`yandex.js:48-55`). |
| 1.18 | Not restricted by the URL it opens on | Met | No domain lock in the shell. The only origin check is a replay-URL migration for `app.glob2.online` (`shell.html:262-263`). |
| 1.19.1 | SDK initialised exactly as documented, with the current loader | Unknown | A plain `<script src="/sdk.js">` then `YaGames.init()` (`yandex.js:60-62`), as on sdk-about. Check the panel shows `IT` (current loader). |
| 1.19.2 | `LoadingAPI.ready()` called when the player can start | Met (code); Unknown (timing) | Called once, when the body gains `ready` (interactive main menu), or right after `init()` if the menu was ready first (`portal-core.js:95-101`, `:239-246`; `yandex.js:38`, `:67`). If `init()` is slow the call comes after the menu is already usable, which the detail page calls "too late". The indicator must turn green within 90 s. Check on draft. |
| 1.19.3 | `GameplayAPI.start()`/`stop()` at the documented moments | Partly met | Calls happen for match start and end, the in-game menu, pause, ads and hidden tabs (`portal-core.js:71-126`, `:203-216`, `:252`; `yandex.js:39-43`). The main menu does not count as gameplay. Not handled: focus moving to another window while the tab stays visible. The detail page names "stays green when focus moves to another window" as a violation. Check on draft. |
| 1.19.4 | `game_api_pause`/`game_api_resume` handled as documented | Met | Pause suspends audio and holds the game; resume restores both (`yandex.js:64-65`; hold path `portal-core.js:107-111`; the frame loop stops while held, `web-portals.md:125-129`). The platform's own `GameplayAPI` calls on these events do not conflict with ours. Startup ad: handlers are registered after `init()` resolves, so check on draft that menu music does not play under a launch ad. |
| 1.20.1 | Runs on Yandex Browser, Chrome, Firefox, Opera, Safari and the Yandex app | Unknown | Tested only in desktop Chrome and the iPhone simulator (rollout notes). Desktop Safari, Firefox and Android are untested. |
| 1.20.2 | Desktop OS: Windows Vista and later, Mac OS X 10.6 and later | Not met (oldest listed versions) | The runtime is WebAssembly (`web-portals.md:158-159`). The last browsers for Vista and OS X 10.6 predate WebAssembly. It is Unknown whether moderation tests these versions. |
| 1.20.3 | Mobile OS: Android 5.0 and later, iOS 9.0 and later | Not met (oldest listed versions) | Same reason: iOS 9 Safari has no WebAssembly. It is Unknown whether moderation tests these versions. |
| 1.20.4 | Android TV | Unknown / not applicable | Only if TV is selected. Do not select it. |
| 1.21 | At most 100 MB uncompressed | Met | Limit enforced on unpacked size (`package-portal.py:150`). The package is 46.8 MB. |
| 1.22 | `index.html` at the root; no spaces or Cyrillic in names | Met | `file_name=r"[A-Za-z0-9._/-]+"` (`package-portal.py:151`) is checked for every entry (`:301`). `index.html` is read from the root (`:305`). |
| 1.23 | No interactive AI (pre-generated AI material allowed) | Met | Opponents are scripted game AIs. The lite edition removes the JavaScript AIs and the generator toolkit (`editions.md:36`). |
| 1.24 | Updates keep the core concept | Not applicable | First upload. |
| 1.5, 1.6.1.3, 1.6.1.4, 1.6.2.3, 1.17 | Deprecated | Not applicable | |

## 2. UX requirements

| # | Requirement (paraphrase) | Status | Evidence |
| --- | --- | --- | --- |
| 2.1 | Quality design; may be refused below platform standard | Unknown | Moderator's judgement. Lite terrain is simplified by design (rollout notes). |
| 2.2 | Controls explained in game or in "How to play" | Unknown | The tutorial exists. The "How to play" field is in the draft. |
| 2.3 | Matches the selected genre | Unknown | Draft field. |
| 2.4 | Meets at least one mechanics criterion | Met | Real-time strategy with a campaign and random maps. |
| 2.7 | Content matches the age rating | Unknown | Draft field. |
| 2.8 | Gradual difficulty; clear setting | Unknown | The tutorial and campaign ramp up. The moderator decides. |
| 2.9 | Over 10 minutes of content, or a reason to replay | Met | Multi-mission campaign and random maps. |
| 2.13 | Rating above 30, or the game is unpublished after 3 weeks | Not applicable yet | Applies after publication. |
| 2.14 | Language detected automatically through the SDK | Met (code); Unknown (indicator) | `ysdk.environment.i18n.lang` is read right after `init()` and passed to `Glob2I18n.setLocale` (`yandex.js:21-32`, `:66`). Lite is English only (`editions.md:43`), so the game does not change. The 文 indicator should still turn green. Known open item: a slow `init()` applies the language late (`docs/releases/yandex.md:42-44`). That is harmless for English-only lite, but would fail 2.14 for a multi-language build. Check on draft after clearing the cache. |
| 2.5, 2.6, 2.10, 2.11, 2.12 | Deprecated | Not applicable | |

## 3. Content requirements

| # | Requirement (paraphrase) | Status | Evidence |
| --- | --- | --- | --- |
| 3.4.2 | No black magic; no purchases in fortune-telling games | Unknown (low risk) | Assets not audited. No known such content. |
| 3.4.3 | No realistic violence or cruelty to animals, children or the elderly | Unknown (low risk) | Combat is cartoon-like. The moderator decides ([listing comparison](yandex-games-listing-comparison.md)). |
| 3.4.4 | No politics, political figures, conflicts or wars | Unknown | Fictional colony combat between globs. Whether moderators treat battles between fictional tribes as "war" is not stated. |
| 3.4.5 | No religious figures, symbols or references | Unknown (low risk) | Assets not audited. |
| 3.4.6 | No predictions about health or death | Met | None in the game. |
| 3.5 | Creator holds all copyright, or the submitter is authorised | Unknown | Globulation 2 is a GPL project with many past contributors and third-party assets (`licenses/` in the package). Whether Yandex accepts GPL redistribution as "authorised" is not stated. Owner decision, or ask Yandex. |
| 3.6 | Not a copy of a catalog game | Unknown | Search the catalog for an existing Globulation 2 upload. |
| 3.7 | No real-money or prize winnings | Met | None. |
| 3.9 | Video embedded, never YouTube | Not applicable (game); Unknown (listing) | The game has no video. Any promo video must be self-hosted. |
| 3.1-3.3, 3.4.1, 3.8 | Deprecated | Not applicable | |

## 4. Ad requirements

| # | Requirement (paraphrase) | Status | Evidence |
| --- | --- | --- | --- |
| 4.1 | Ads only through the SDK; no third-party ads | Met | Only `ysdk.adv.showFullscreenAdv` (`yandex.js:48-55`). |
| 4.2 | Progress kept after an ad click and return | Met | Ads run only between matches. The page and game state stay in place while an ad's link opens elsewhere. Check on draft. |
| 4.3 | Ad orientation matches the game | Unknown | Yandex renders the ad. Check on a phone. |
| 4.4 | Ads only at logical pauses, never during play | Met | Ads run only at `start` (after the player chose to play, never before the first match) and `leave`. `pause` and `resume` never ask for an ad. There is a 3-minute gap after every break (`portal-core.js:151-216`). The docs warn against timer-driven ads during play; ours are event-driven at breaks. |
| 4.5 | Rewarded ads optional, labelled and a bonus only | Not applicable | No rewarded ads (`web-portals.md:27-28`). |
| 4.6.1-4.6.2 | Only sticky banners as extra placements; no custom RTB | Met (code); Unknown (console) | The code shows no banners. If sticky banners are enabled in the console, they show for the whole session by default (sdk-adv), and the layout must leave room for them (1.6.2.1). |
| 4.7 | Sound and gameplay paused during fullscreen ads | Met | The game is held and audio silenced before `showFullscreenAdv`, and released on `onClose`/`onError` or after a timeout (`portal-core.js:159-197`; `yandex.js:51-55`). |

## 5. Descriptions and promotional materials

All items depend on the draft listing, which was not opened.

| # | Requirement (paraphrase) | Status | Evidence |
| --- | --- | --- | --- |
| 5.1.1.1-5.1.1.3 | Own gameplay only; screenshots at least 70% gameplay; videos at least 70% gameplay | Unknown | Prepare from lite footage. |
| 5.1.2 | Materials show what the game is and why it is unique | Unknown | Draft. |
| 5.1.3 | Name identical in game and materials for each language | Unknown | The in-game name is "Globulation 2" (`shell.html:64`, `:78`). The draft title must match. |
| 5.2 | All required fields filled, plus screenshots | Unknown | Draft. |
| 5.3 | Text and files meet draft limits | Unknown | Draft. |
| 5.4 | Tags match the content | Unknown | Draft. |
| 5.6 | No screenshots as icon or cover | Unknown | Draft. |
| 5.9 | Black bars only when part of the game | Unknown | Check on draft (1.6.2.2). |
| 5.11 | No padding characters; no duplicate text across fields | Unknown | Draft. |
| 5.12 | Unique catalog name across selected languages | Unknown | Draft. |
| 5.5, 5.7, 5.8, 5.10 | Deprecated | Not applicable | |

## 6. Recommendations (not checked by moderation)

| # | Recommendation | Status | Evidence |
| --- | --- | --- | --- |
| 6.1 | Developer email | Unknown | Draft. |
| 6.2 | Sound can be turned off | Unknown | The game's audio settings were not checked in lite. |
| 6.3 | Gameplay can be paused | Met | The in-game pause exists (`web-portals.md:80-83`). |
| 6.4 | No DevTools console errors | Unknown | Check on draft. |
| 6.5-6.6 | Avoid "game" in the name; keep it short | Met | "Globulation 2". |
| 6.7 | No useless buttons such as Exit | Met | Quit is hidden in portals (`web-portals.md:65-66`; `src/ui/screens/MainMenuScreen.cpp:26`, `:214`, `:272`). |
| 6.8 | Tutorial for complex mechanics | Met | The tutorial campaign exists. |
| 6.9 | Language switch uses universal icons and native names | Not applicable | Lite hides the language picker (`shell.html:118-135`). |

## 8. Text and media content

| # | Requirement (paraphrase) | Status | Evidence |
| --- | --- | --- | --- |
| 8.2.1 | Correct grammar and punctuation | Unknown | English source strings. Not proofread for this audit. |
| 8.2.2 | Text reflects real mechanics and does not mislead | Unknown | Listing copy must drop the editor, online play, premade maps and the 45 languages (rollout notes). |
| 8.2.3 | Gameplay text translated into the selected language; no mixed languages | Met if the draft declares English only; Unknown otherwise | Lite ships only the English catalog (`editions.md:43`; `shell.html:117-118`). Declaring Russian in "Game translated into" would fail, because the game would stay English. |
| 8.2.4-8.2.5 | No profanity or prohibited text | Unknown (low risk) | Not audited. |
| 8.3.1-8.3.7 | Media quality; no borders or Yandex UI; no prohibited or unsafe media | Unknown | Depends on the draft icon, cover and screenshots. |
| 8.4.1 | SDK links only to own catalog games | Not applicable | None. |
| 8.4.2 | No links to external resources | Met (code) | `externalLinks:false` (`package-portal.py:147`). `openUrl` refuses links when it is off (`platforms/web/ApplicationHost.cpp:399-405`). Discord and privacy buttons are gated (`MainMenuScreen.cpp:201-205`, `:276-286`). Report a Problem opens no page in ad portals (`src/app/PortalModeTest.cpp:290-294`). The Credits screen was not checked for a printed web address. |
| 8.4.3 | Community links only under three conditions | Not applicable | Discord is hidden. |
| 8.4.4 | No automatic or suggested redirects | Met (code) | Same gating as 8.4.2. |

## Not met, by priority

1. **1.19.3 and 1.3: focus loss to another window.** Gameplay stays reported active and sound keeps playing when the player focuses another window while the tab stays visible. The 1.19 detail page names this exact case as a violation. Fix: in `portal-core.js`, extend `watchShell` (lines 239-256) to treat window `blur`/`focus` as not visible/visible for Yandex. A Yandex-only option avoids changing CrazyGames, which turns visibility handling off. Also silence audio on blur (a `'blur'` reason through `createAudio().set`). Confirm first on the draft's debug panel that Yandex does not already send `game_api_pause` on blur.
2. **1.20.2 and 1.20.3: oldest listed OS versions.** Windows Vista, Mac OS X 10.6, iOS 9 and Android 5 era browsers cannot run a WebAssembly build. No code change can fix this. Fix: select only the platforms and browsers the draft lets you narrow, and ask Yandex support whether moderation tests the oldest listed versions.

## Unknown items that most need checking

- **Draft languages and domains (2.14, 8.2.3):** declare English only, and confirm the 文 indicator turns green at startup. The docs do not say whether an English-only game reaches yandex.ru players.
- **1.19.1 and 1.19.2:** loader shows `IT`; Game Ready turns green when the menu is usable, not seconds later when `init()` is slow.
- **1.19.4:** no menu music under the platform's launch ad.
- **3.5 copyright:** whether GPL redistribution of a multi-contributor game meets "creator holds the copyright or is authorised". Owner decision, or ask Yandex.
- **1.6.x, 1.8, 1.10, 1.14, 1.20.1:** a test pass on the draft on desktop (Chrome, Firefox, Safari, Yandex Browser) and on a phone (iOS and Android). Cover rotation, long tap, swipe, ads and minimising.
- **1.6.2.4:** keyboard shortcuts on a Russian layout.
- **4.6:** whether sticky banners are enabled in the console, and if so whether the game area still fits.
- **Section 5 and 8.3:** every listing field and media item.

Small documentation note: `docs/releases/yandex.md:31` and `package-portal.py:154` cite `sdk-gameready`. The current page for LoadingAPI and GameplayAPI is `sdk-game-events`.
