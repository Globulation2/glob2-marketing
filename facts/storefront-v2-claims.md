# Storefront v2 claims: what is true today, per platform

[Fact index](README.md) · [Product ledger](product.md) · [Distribution](distribution.md) · [History](history.md) · [Positioning v2](../analysis/positioning-v2.md) · [Rollout ledger](../planning/storefront-v2-rollout.md) · [Working rules](../AGENTS.md#storefront-v2-revamp--2026-11-24)

Observed **2026-11-24** (public checks between 18:20 and 18:30 UTC). This record sets what storefront-v2 copy may say. A claim not listed here as safe for a store is not cleared for that store.

## How to read the evidence

- **Source** means the game repository at the public tag [`v0.11.7.0`](https://github.com/Globulation2/glob2/tree/v0.11.7.0) (commit `d6596e5f8b9d`, tagged 2026-11-21, published as the latest GitHub release on 2026-11-22). Paths in backticks are at that tag unless a row says otherwise. Source shows what a build contains. It does not show that a store accepted or shipped it.
- **Production** means a public, signed-out read of the official instance or a store's public page or API on the observation date.
- **Installed build** means `/Applications/Glob2.app` on the working machine. It reports version 0.11.7.0 but is **not the public release binary**: `glob2 info version` reports revision `5bf966285aa8`, 15 commits after the tag, built 2026-11-23. Maps, tutorial lessons, generators, AI roster and simulation revision are identical to the tag (`git diff v0.11.7.0 5bf966285aa8` shows no change in those paths). It carries newer MCP tools than the release.
- **0.11.8.0** was tagged on 2026-11-24 and was not a public release at observation. Differences are noted where they matter.
- No account was created and nothing was signed in to. Anything behind sign-in is marked unverified.

Verdicts: **safe**, **safe with caveat**, **not safe**.

## Contradictions and risks for the coordinator

These conflict with, or put at risk, the user's 2026-11-24 decisions. Raise them before copy is final.

| # | Finding | Why it matters | Evidence |
| --- | --- | --- | --- |
| R1 | **Production has the paid-feature services switched on.** `https://app.glob2.online/api/v1/instance` lists `commander`, `map-studio`, `music-studio`, `terrain-studio`, `ai-building-studio`, `ai-studio`, `generator-studio` and `skins.designer` in `features`. The hosting guide's own "free launch" configuration says to set all eight to `enabled: false`. | "Nothing is sold" is the user's statement. The game clients agree with it (see below). The official website does not look like it: signed-out visitors can open `https://app.glob2.online/commander` ("Sign in to view your commander and credits.") and `https://app.glob2.online/map-studio` ("Sign in to create"). Each service has its own credit wallet in source. | Instance API read 2026-11-24; pages read signed-out 2026-11-24; `docs/hosting/configuration.md` L54–61, "Disable unfinished paid features for a free launch"; `services/online/apps/api/src/publicFeatures.ts` L14–22 |
| R2 | **Credit-pack sales state is unverified for Hive Mind and the six Studios.** The pack lists are only returned to a signed-in account (`GET /api/v1/hive/account` and the studio equivalents return 401 signed-out). Colony-skin sales are verifiably **off**: `skins.sales` is absent from `features`, and `GET /api/v1/skins/products` returns all three products `available: false`, `testMode: true`. | If any `salesEnabled` flag is true in the private production `instance.yaml`, "nothing is sold" is false on the website, and "no in-app purchases" becomes arguable for browser play. Only the owner can confirm the six studio flags and the Hive flag. | `services/online/apps/api/src/hive/routes.ts` L31–41, L59–80; `…/skins/billing/routes.ts` L71–95 (origin/master); both endpoints read 2026-11-24 |
| R3 | **The published privacy policy says purchases exist.** It has a section "Optional purchases and AI features" ("When offered, optional website purchases use Stripe checkout") and lists Stripe as a service provider. | A store reviewer comparing "no in-app purchases" against the linked policy will find purchase language. The policy scopes it to the website and "when offered", which is consistent with a client that sells nothing, but the listing must not say "nothing is ever sold" or "no purchases anywhere". | `docs/mobile/privacy-policy.md` L244 onward, "Optional purchases and AI features"; `https://glob2.online/privacy/` returned 200 |
| R4 | **"No in-game currency" has an expiry date.** The public handbook describes Hive Mind as "coming soon" and says it uses credits during online matches. Released clients have it compiled out today. | The claim is true of every shipped client now. It stops being true for a client the day a build ships with Hive Mind enabled. | `https://glob2.online/learn/hive-mind/` read 2026-11-24; `buildsys/client_features.py` L9–20 |
| R5 | **No ready-made campaigns ship.** 0.11.7.0 packages zero campaign definition files. The Campaign menu lists `campaigns/*.txt`; none is in the release, and the old `Tutorial_Campaign` is explicitly hidden. What ships is a 10-lesson tutorial and a campaign editor. | Positioning v2 lists "campaigns" under ways to play. Current live copy says "Play included maps and campaigns" (Amazon bullets), the iOS version notes say "maps, campaigns, and a map editor", and the public website says "follow a campaign". All three overclaim. | `content/campaigns/` holds only 10 `.map.gz` lesson maps; `src/campaign/screens/CampaignSelectorScreen.cpp` L10–17; commit `e7613e93b0` (2026-10-31) "Replace legacy tutorial campaign with JavaScript training lessons"; installed build `Resources/campaigns/` lists the same 10 files |
| R6 | **Online play needs 0.11.7.0 or newer, and several stores are behind.** Production serves one simulation version (format 219, protocol 75). Microsoft Store's last recorded package is game 0.11.6.5 (format 218), which the server will refuse with "update required". The Amazon edition has no online play at all. Epic's artifact in review is 0.11.4.0. Google Play's closed test is 0.11.2.0. | "Online multiplayer" and "cross-platform play" are not true of the build a Microsoft Store or Amazon customer installs today. | Instance API `supportedSimVersions`; `src/app/FileFormatVersions.h` `VERSION_MINOR` 218 at `v0.11.6.5`, 219 at `v0.11.7.0`; release notes for 0.11.7.0 ("Online play requires 0.11.7.0"); [v1 rollout ledger](../planning/approved-storefront-rollout.md) store table; `docs/releases/amazon-appstore.md` L3, L24–25 |
| R7 | **MCP on the Mac App Store build is unverified.** The source compiles the server into every native macOS build and the sandbox entitlements include `com.apple.security.network.server`, so it should work. No record shows it tested in the sandboxed store package, and no native Mac listing was publicly visible. | Decision 3 puts the MCP pitch on desktop listings. For the Mac App Store, hold it until one sandboxed-build check passes. | `src/mcp/Availability.h` L6–10; `platforms/macos/AppStore.entitlements`; no MCP mention in `docs/releases/mac-app-store.md`; iTunes Search API `entity=macSoftware` returned 0 results for "globulation" |
| R8 | **Epic's build predates the useful MCP tools.** At 0.11.4.0 the server has 12 tools: screenshots, pointer and keyboard only. The colony tools arrived in 0.11.6.2. | "Play the same colony together" is thin on 0.11.4.0. Hold the MCP section on Epic until its artifact is 0.11.6.2 or newer. | Tool-name counts per tag from `src/mcp/Tools.cpp`: 12 at `v0.11.4.0`, 21 at `v0.11.6.1`, 27 at `v0.11.6.2` through `v0.11.7.0` |
| R9 | **The research notes on store status are stale in two places.** The iOS app is **live**, not waiting for review: the public lookup API reports version 0.11.700 with `currentVersionReleaseDate` 2026-11-23. Snap stable is **0.11.7.0** (released 2026-11-21), not 0.11.2. | Decision 5 defers Apple until review clears. For iOS it has cleared. | `https://itunes.apple.com/lookup?id=6817603328&country=us`; `https://api.snapcraft.io/v2/snaps/info/globulation2` |
| R10 | **The iOS listing is visible in very few countries.** The lookup API returned the app for US, CA and MX and returned nothing for GB, FR, DE, AU, JP, IN and BR. | 44-language Apple copy has little reach until availability is widened. Ten storefronts were sampled; this is not a full territory list. | Lookup API per `country` code, 2026-11-24 |
| R11 | **The App Store shows six languages.** Its Languages row reads "English, Bulgarian, Marathi, Tamil, Telugu, Thai". The game has 45. | A "45 languages" line on the App Store sits next to Apple's own "6". The v1 ledger already records this as a packaging gap (only six `.lproj` folders). | `https://apps.apple.com/us/app/globulation-2/id6817603328`; `platforms/macos/*.lproj`; [v1 ledger](../planning/approved-storefront-rollout.md) L739 |
| R12 | **The online service is nearly empty.** The official instance home page showed "0 players online", "0 matches on now", "2 matches today", and one rated player on the Ranked 1v1 leaderboard. | Do not imply a busy ladder or quick human opponents. The true and useful line is that quick match fills empty seats with an AI opponent after a short wait. | `https://app.glob2.online/` read signed-out 2026-11-24; instance API `aiBackfillSeconds` 90 (ranked) and 45 (casual) |
| R13 | **Captures from the installed build are not "release 0.11.7.0".** | The footage rule requires recording the build. Manifests should say "0.11.7.0 + 15 commits, revision 5bf966285aa8". | `glob2 info version` on the installed build |

## 1. Monetisation: free, no ads, no in-app purchases, no lootboxes, no in-game currency

### What the shipped clients contain

| Check | Result | Evidence |
| --- | --- | --- |
| Ad SDKs, store billing, analytics or crash SDKs in the client | None found | `git grep` at `v0.11.7.0` over `src libs platforms cmake snap fastlane buildsys vcpkg.json` for StoreKit, `SKPayment`, Play Billing, `com.android.vending.BILLING`, AdMob, Unity Ads, AppLovin, ironSource, Facebook ads, Firebase, Crashlytics, AppsFlyer and similar: no matches |
| Android permissions | `INTERNET` only. No billing permission, no advertising ID permission | `platforms/mobile/android/app/src/main/AndroidManifest.xml` L2 |
| Android dependencies | No Gradle dependencies block at all; the app is the native library plus assets | `platforms/mobile/android/app/build.gradle` |
| iOS entitlements | Multicast networking and associated domains only. No in-app purchase capability | `platforms/mobile/ios/Glob2.entitlements` |
| Release client profile | Every release build is the **free** profile: Commander (Hive Mind) UI, its start-up calls, credit links and paid authoring links are compiled out | `buildsys/client_features.py` L9–20; `docs/development/build-options.md` § "Free launch profiles"; `.github/workflows/release.yml` L223, L365, L463, L621; `browser-release.yml` L84; `mac-app-store.yml` L96; `epic-windows-release.yml` L129; `steam-windows-package.yml` L145 |
| Purchase or credit UI reachable in a free-profile client | None. The only purchase-related button in source, "Commander account and credits" in Settings → Hive Mind, is inside the compiled-out block. The string is absent from the installed build's binary; so are the `/commander`, `/music/new` and `/ais/new` links | `src/ui/settings/SettingsScreenOnline.cpp` L102–115; `src/hive/HiveClient.cpp` L624–628; `strings` on the installed build |
| What a player does see that could be misread | A **Credits** entry in the main menu. It is the contributor credits screen, not a currency. A **Show colony skins** display toggle in Settings. Settings → Online → "Download or delete my data" opens the account page in the browser | `src/ui/screens/MainMenuScreen.cpp` L185, L244; `src/ui/settings/SettingsScreenGeneral.cpp` L184; `src/ui/settings/SettingsScreenOnline.cpp` L329 |
| Lootboxes or random paid rewards | No such mechanic in source | Search for loot, gacha and currency terms in `src` and `content/data/texts.en.txt`: none |
| In-game currency | None. Wheat, wood, stone, algae and fruit are gathered on the map. Prestige is a score. Nothing in the game is bought | [Product ledger](product.md) P02; `src/resource/` |

### What the stores show

| Store | Price and purchase flags observed | Evidence |
| --- | --- | --- |
| iOS App Store | Free. No in-app purchase row on the public page | Lookup API `formattedPrice: Free`; public page text has no "In-App Purchases" entry |
| Microsoft Store | Free (`ListPrice` 0.0). `HasAddOns: false` | `https://displaycatalog.mp.microsoft.com/v7.0/products/9PH4FCRMX19F?market=US&languages=en-US` |
| Snap Store | Free listing, licence GPL-3.0-or-later, stable 0.11.7.0 | Snap info API |
| itch.io | Free; payments disabled | [itch.io launch](../planning/itch-io-launch.md); public page read 2026-11-24 |
| Amazon Appstore | Free, per the release guide. Not publicly verifiable (submitted, not live) | `docs/releases/amazon-appstore.md` L73 |
| Epic | Free base offer, per the v1 ledger. Not live | [v1 ledger](../planning/approved-storefront-rollout.md) |
| Google Play | Not publicly visible (closed test). Price and declarations live only in Play Console | See [store declarations](#6-store-declarations) |

### Verdict on the five claims

"Shipped app" means the store or direct-download binary. "Browser" means play at `app.glob2.online/play/`, including the itch.io launcher, where the game runs inside the official website.

| Claim | Windows, macOS, Linux (all desktop stores and downloads) | iOS / iPadOS | Android (Play, direct APK, F-Droid) | Amazon Fire | Browser and itch.io browser play | Safe wording |
| --- | --- | --- | --- | --- | --- | --- |
| Free | safe | safe | safe | safe | safe | "Free." or "Free and open source." Keep the word out of graphics and out of Google Play and Apple short fields; see [per-store wording](#7-allowed-and-banned-wording-per-store) |
| No ads | safe | safe | safe | safe | safe | "No ads." The public website `glob2.online` runs opt-in Google Analytics with ad features off; that is the website, not the game, so do not stretch the line to "no analytics" or "no tracking" |
| No in-app purchases | safe | safe | safe | safe | **safe with caveat** (R1, R2) | "No in-app purchases." It is a statement about the game. Do not write "nothing is sold", "no purchases anywhere" or "never" until the owner confirms R2 |
| No lootboxes | safe | safe | safe | safe | safe | "No lootboxes." |
| No in-game currency | safe with caveat (R4) | safe with caveat (R4) | safe with caveat (R4) | safe | **safe with caveat** (R1, R4) | "No in-game currency." True of every released client. Recheck before any build that enables Hive Mind |
| No premium currency (wording recorded 2026-11-24 by the independent copy and policy review) | safe with caveat (R4) | safe with caveat (R4) | safe with caveat (R4) | safe | **safe with caveat** (R1, R4) | "No premium currency." The listing's `fair_deal_line` uses this in place of "No in-game currency", which a reader could take to deny the wheat, wood and stone gathered in play. It claims less than the row above (no currency bought with real money) and rests on the same evidence: no currency of any kind and no billing code in the client, and nothing in the game is bought. Same caveats and the same recheck before any build that enables Hive Mind credits |

Wording caveats that apply everywhere:

- Say what the game does. "Free, no ads, no in-app purchases, no lootboxes, no in-game currency" is supported for the game on every platform.
- Do not add "forever", "ever", "never" or "nothing to buy, anywhere". The website carries optional paid machinery (R1 to R3).
- Do not add privacy promises to the fair-deal line. The App Store label is "Data Linked to You" (see [store declarations](#6-store-declarations)).
- Do not mention Hive Mind, colony skins, Studios or credits in any listing.

## 2. MCP co-play

### What it is

| Fact | Detail | Evidence |
| --- | --- | --- |
| Built in | An MCP (Model Context Protocol) server inside the desktop game. No plug-in or separate download | `src/mcp/`; `docs/development/mcp-ui-server.md` |
| Off by default | The player turns it on in **Settings → MCP server → Enable MCP server**, then uses **Copy endpoint**. Default endpoint `http://127.0.0.1:27202/mcp`. Or for one run: `glob2 play --mcp-port 27202` | `mcp-ui-server.md` L3–9; `src/ui/settings/SettingsScreenMCP.cpp` L12–25; `glob2 --help` on the installed build |
| Local only | Listens on IPv4 loopback only. No token, no remote binding | `mcp-ui-server.md` L14–17 |
| Human input stays active | "Human input stays active." Human events are processed first. The player can press **Revoke control** | `mcp-ui-server.md` L17, L133; `SettingsScreenMCP.cpp` L75 |
| What an agent can do in 0.11.7.0 | **27 tools.** See and operate the game window (`ui_status`, `ui_screenshot`, `ui_inspect`, `ui_act`, `ui_wait`, pointer, keyboard and text input, and a control lease: 16 `ui_*` tools). Read the game's own guide (`game_guide`). In a local match: read the colony in map tiles and place buildings and flags, change a building, paint zones and move the camera (`game_world`, `game_place`, `game_building`, `game_zone`, `game_view`), and run JavaScript standing orders (`hive_status`, `hive_api`, `hive_run`, `hive_result`, `hive_program`) | `src/mcp/MCPTest.cpp` L59 (`tools.size() == 27`); tool table in `mcp-ui-server.md` |
| Limits | The `game_*` and `hive_*` tools work in local matches against the computer. The `ui_*` tools operate whatever screen is showing. Agents see only what the player's colony sees (fog of war). The player supplies the agent and model | `mcp-ui-server.md` tool notes; [MCP outreach evidence](../planning/mcp-outreach/product-and-prior-art.md) |
| 0.11.8.0 | **32 tools**: adds `game_chat`, `game_time`, `game_wait`, `game_alliance`, `game_stats`. Clients with MCP enabled quick-match only against each other, in separate "MCP Ranked 1v1" and "MCP Casual 1v1" queues. Those queues are already listed by production; 0.11.7.0 clients do not use them | `src/mcp/MCPTest.cpp` L63 at `v0.11.8.0`; `docs/multiplayer/ratings-and-matchmaking.md` § "Assisted queues" at `v0.11.8.0`; instance API `queues` |
| Public docs | All returned HTTP 200 on 2026-11-24: `https://glob2.online/learn/mcp-server/`, `https://glob2.online/learn/mcp-agent-tools/`, `https://glob2.online/learn/automation-overview/`, `https://glob2.online/learn/javascript-ai/`. The setup guide says it describes the 0.11.6.2 desktop release | `curl` status checks |

### Which builds include it

The compile gate is one line: every native build that is not browser, Android, iOS or the relay server (`src/mcp/Availability.h` L6–10). Distribution (Steam, Epic, Microsoft, App Store) does not change it.

| Build | MCP server | Version a customer gets today | Verdict for an MCP section in that listing |
| --- | --- | --- | --- |
| Windows direct download (installer, ZIP) | Yes | 0.11.7.0 | safe |
| macOS direct download (DMG, Apple Silicon and Intel) | Yes | 0.11.7.0 | safe |
| Linux direct (Flatpak bundle, tarball, RPM, Snap file) | Yes | 0.11.7.0 | safe |
| Snap Store | Yes. The snap declares the `network-bind` plug it needs to listen | 0.11.7.0 stable | safe with caveat: not exercised inside the snap in this pass |
| itch.io desktop downloads | Yes. They are the GitHub release packages | 0.11.7.0 | safe. Scope it to the desktop downloads; the page also offers browser play |
| Microsoft Store | Yes | Last recorded package is game 0.11.6.5 (27 tools) | safe with caveat: not exercised in the Store package. The package is full-trust (`runFullTrust`), which is what a loopback listener needs |
| Epic Games Store | Yes in source | Artifact in review is 0.11.4.0 (12 tools). Not live | **not safe yet** (R8). Hold until the artifact is 0.11.6.2 or newer |
| Mac App Store (sandboxed) | Yes in source; entitlement present | Not publicly live | **not safe yet** (R7). Hold until one sandboxed-build check passes |
| Steam, GOG | Yes in source | Prepared only | Prepare the copy; nothing to verify yet |
| Browser (including itch.io browser play) | **No** | n/a | not safe |
| iOS / iPadOS | **No** | 0.11.700 | not safe |
| Android (Play, APK, F-Droid, Amazon) | **No** | n/a | not safe |

Evidence for the "no" rows: `mcp-ui-server.md` L11 ("Browser, Android, iOS and relay builds do not expose this category or listener"); public guide: "The server exists only in the desktop builds for Windows, macOS and Linux."

### Safe public wording

- "Play alongside your own AI agent. Turn on the game's built-in MCP server and an AI agent on your computer can see the game and play the same colony with you. Your mouse and keyboard keep working the whole time."
- "Off by default. Runs on your own computer."
- "Bring your own AI agent" or "your own AI agent". Never imply the game includes, sells or needs a model.
- Do not write "first". Do not promise how well an agent plays. Do not say it works in ranked or online play. Do not mention it on mobile or browser listings.
- A tool count ("27 tools") is true of 0.11.6.2 to 0.11.7.0 only and changes to 32 in 0.11.8.0. Prefer no number.

## 3. Gameplay facts usable as feature bullets

Counted from the `v0.11.7.0` tree and cross-checked against the installed build. All counts are unchanged in 0.11.8.0.

| Claim | Verdict | Evidence | Safe wording |
| --- | --- | --- | --- |
| Included hand-made maps: **23** | safe | `content/maps/` has 23 `.map.gz` files; the installed build's `Resources/maps/` has 23 | "23 hand-made maps" |
| Random map generators: **67** landscapes | safe | `glob2 map generators` lists 68 entries, one of them (`uniform`) editor-only; generator sources identical at tag and installed build | "67 random map landscapes" or "Dozens of random landscapes". Not "infinite" |
| Campaigns: **0 included** | **not safe** to claim included campaigns (R5) | `content/campaigns/` has no campaign definition file | Do not write "campaigns" as content. "Build your own campaigns in the editor" is supportable: `src/map/editor/screens/EditorMainMenu.cpp` L34 |
| Tutorial: **10 guided lessons** | safe | `content/scripts/tutorials/catalog.json` has 10 entries: introduction, food supply, healing, walking training, swimming, schools, upgrades, warrior training, fortifications, defensive tactics | "A 10-lesson tutorial" |
| Computer opponents: **8** | safe | `src/ai/AINames.cpp` L35–46 and `glob2 info catalog`: Numbi, Castor, Econo, Warrush (Easy); Cortex, Nicowar, Cabino (Medium); Maxima (Hard) | "8 computer opponents, from easy to hard". The tiers are the game's own labels from its AI tournament; do not quote the ratings |
| Players per match: up to **16** colonies | safe | `src/team/TeamCapacity.h` L7; `docs/features/custom-game-setup/README.md` L15 ("up to 16 colonies and 16 controllers"); Microsoft Store declares online multiplayer 2–16 | "Up to 16 colonies in one match". Some landscapes allow fewer |
| Map editor | safe on every platform | Main menu Editor entry on desktop and under More on touch; no platform exclusion (`src/ui/screens/MainMenuScreen.cpp` L184, L243); `docs/mobile/editor-interface.md` | "Built-in map editor" |
| Offline single-player without an account | safe on every platform | Privacy policy: "Single-player games, the campaign, the map editor and LAN games work without an account and send nothing to us" | "Play offline. No account needed for single-player." |
| Online quick match: Ranked 1v1 and Casual 1v1 | safe with caveat (R6, R12) | Instance API `queues`: `ranked-1v1`, `casual-1v1`, each over 30 maps; plus the two MCP queues | "Ranked and casual 1v1 quick match." No promise about opponents or wait times. Not on Amazon |
| AI fills in when nobody is queueing | safe | Instance API `aiBackfillSeconds`: 90 ranked, 45 casual; `docs/multiplayer/ratings-and-matchmaking.md` L184 | "If no player is waiting, an AI opponent steps in." |
| Online rooms with invite codes | safe with caveat (R6) | `docs/multiplayer/rooms-and-matches.md` § Rooms; official home page: "Got an invite code?" | "Host a room and invite friends with a code." Not on Amazon |
| LAN play | safe on desktop, iOS, Android and Amazon. **Not in the browser** | `MainMenuScreen.cpp` L181–182, L239–240 (`#ifndef __EMSCRIPTEN__`); iOS `NSLocalNetworkUsageDescription` | "Local network play" |
| Online play as a guest | safe with caveat | Instance API `guestsAllowed: true`; ranked queues refuse guests (`ratings-and-matchmaking.md` L183). Opening online play creates a guest account automatically (privacy policy) | "Play online as a guest; sign in to play ranked." Not "no account" for online play |
| Cross-platform online play | safe with caveat (R6) | One simulation version for every client; "Browser and native clients in one match must have the same sim version" (`docs/browser/implementation.md` L129); CI requires Linux, Windows, macOS and browsers to verify the same match identically (`AGENTS.md` § Compatibility reminders); the service records device kind desktop, Android, iOS or browser. No live cross-device match was observed in this pass | "Desktop, browser and mobile players share the same online games, on the same game version." Do not name other platforms in Apple copy |
| In-game languages: **45** | safe with caveat (R11) | `content/data/texts.list.txt` lists 45 catalogues (English plus 44). All 44 non-English catalogues are flagged incomplete in `texts.incomplete.txt`, so newer strings can fall back to English | "Available in 45 languages." Omit on the App Store while Apple shows 6 |
| Replays | safe | End-of-game "Save Replay" (`src/game/screens/EndGameScreen.cpp` L735); Load game → Replays; online match replays download from match pages | "Save and watch replays" |
| JavaScript AI scripting | safe on Windows, macOS direct, Linux, browser, Android. **Not on iOS or the Mac App Store** | Settings → Custom AIs → Import JavaScript AI (`src/ui/settings/SettingsScreenCustomAIs.cpp` L127–149). App Store builds hide it: `buildsys/client_features.py` L19–20 (`v0.11.7.0`). Local games only | "Write your own computer opponent in JavaScript" (desktop listings other than the Mac App Store). Linking a development file is desktop-only |

## 4. Heritage and social proof

| Claim | Verdict | Evidence | Safe wording |
| --- | --- | --- | --- |
| First public alpha in 2004 | safe | [History](history.md): archived news dates the first alpha to 2004-02-01; the public site says "Growing since 2004" | "Growing since 2004" |
| In development since 2001 | safe with caveat | First commit in the repository is dated 2001-11-19. Commit activity is heavy in 2002–2010 and 2026 and sparse between (fewer than 60 commits a year from 2011 to 2025) | "Started in 2001." Not "25 years of continuous development" |
| Open source, GPL-3.0-or-later | safe | `COPYING` (GPL version 3); SPDX headers; Snap Store licence field | "Free and open source (GPLv3)" |
| Contributor count | **not safe** as a number | 78 distinct author names and 58 distinct e-mail addresses in `git log` at the tag, with obvious duplicates of the same people. `AUTHORS` names 8 core authors | "Built by volunteers over two decades." No count |
| Commit count | safe but weak | 6,456 commits at `v0.11.7.0` | Avoid; it is not a player benefit |
| Packaged by Linux distributions | safe with caveat | Debian, Fedora, Arch, FreeBSD ports and SlackBuilds carry the **legacy 0.9.x** game ([distribution](distribution.md), [platform audit](platform-audit.md)), not the current release | Do not use in store copy; a reader who installs the distro package gets a different game |
| Player counts, ratings, awards, press quotes | **not safe** | No ratings on the App Store (`userRatingCount: 0`); official instance nearly empty (R12) | None |

## 5. Platform specifics the copy must respect

| Platform | Fact | Evidence |
| --- | --- | --- |
| iOS / iPadOS | Universal app for iPhone and iPad. Requires iOS / iPadOS **15.0**. 303 MB. All four orientations declared, so portrait and landscape both work. Age rating shown as 13+ on the public page (12+ in the lookup API) | Lookup API; public page; `platforms/mobile/ios/Info.plist.in` (`UISupportedInterfaceOrientations`); `platforms/mobile/toolchain.json` |
| iOS / iPadOS | The page also reads "Designed for iPad. Not verified for macOS." That is the iPad app offered on Apple-silicon Macs, not the native Mac build | Public page |
| iOS / iPadOS | One iPhone screenshot and one iPad screenshot are live | Lookup API `screenshotUrls`, `ipadScreenshotUrls` |
| Android | Requires Android **7.0 (API 24)** and OpenGL ES 2.0. ARM64, ARMv7 and x86-64 builds. Orientation is not locked | Release `package-inventory.json`; `AndroidManifest.xml` L3, L6 |
| Phones | Source has a dedicated Phone layout (compact touch interface) for portrait and landscape, a Tablet layout, and a setting to choose between them. The repositories record no physical-phone qualification, and Google Play is still a closed test | `docs/mobile/interface.md`; 0.11.7.0 release notes; [v1 ledger](../planning/approved-storefront-rollout.md) |
| Phones | Wording: "Play on phone or tablet, portrait or landscape." Do not write "optimised for every phone" | |
| Amazon Fire | Fire tablets only (Fire OS 7 and 8). **No online play, no accounts, no invite links.** LAN and offline only | `docs/releases/amazon-appstore.md` L3, L7–9, L24–25; privacy policy § "Fire tablet edition" |
| Mac App Store | Native build is Apple Silicon only, requires **macOS 26.0**, United States and Canada only per the v1 ledger. Not publicly visible at observation. Hides community JavaScript AI and community generators | `docs/releases/mac-app-store.md` L92–94; [v1 ledger](../planning/approved-storefront-rollout.md) L733; `client_features.py` L19–20 |
| macOS direct download | Requires macOS **15.0**; Apple Silicon and Intel | `package-inventory.json` |
| Windows | Windows 10 64-bit or later | `package-inventory.json` |
| Linux | Flatpak bundle (GNOME 51 runtime), Snap, Ubuntu 22.04 tarball, Fedora 43 RPM; x86-64 only | `package-inventory.json` |
| Browser | "Early access" on the public site. No LAN, no MCP | `https://glob2.online/`; `MainMenuScreen.cpp` |
| Accounts | Single-player, editor and LAN need no account. Online play creates a guest account with a generated name. Ranked needs a registered account: Google sign-in, or a username and password | Privacy policy; instance API `authProviders` |

## 6. Store declarations

| Store | What is recorded or publicly shown | Gap |
| --- | --- | --- |
| Google Play | The release guide says what the Data safety form must declare: account and display name, optional e-mail, user IDs, chat, uploaded maps, match and connection data, IP addresses, first-party activity markers; "nothing is used for advertising or tracking". Single-player, editor and LAN collect nothing | **The Ads ("contains ads") and in-app purchase answers are not recorded in either repository.** The listing is not public. Read them in Play Console before publishing a no-ads line. Nothing in the binary would justify "contains ads" |
| iOS App Store | Public privacy label, read 2026-11-24: **Data Linked to You** only; no "Data Used to Track You". Purpose *App Functionality*: Contact Info (e-mail address, name), User Content (e-mails or text messages, photos or videos, gameplay content, other user content), Identifiers (user ID, device ID), Usage Data (product interaction), Diagnostics (other diagnostic data), Other Data. Purpose *Analytics*: User Content (gameplay content), Identifiers (user ID), Usage Data (product interaction). No Purchases category. Age rating content: cartoon or fantasy violence; messaging and chat, user-generated content | The label has an Analytics purpose, so "no analytics" is not safe on Apple |
| iOS App Store: what drives "Linked to You" | Optional online accounts: sign-in provider e-mail and name; uploaded profile photo; room and in-game chat; uploaded maps; match records; user and device credentials; one activity marker per account per day (the Analytics purpose). Offline play sends nothing | `docs/mobile/privacy-policy.md` § "What we collect and why" and § "Online activity and operational reporting" |
| Microsoft Store | Free; `HasAddOns: false`; ESRB E (Mild Fantasy Violence, Users Interact), PEGI 3, IARC 3, USK 6; declares single-player and online multiplayer 2–16; capabilities `internetClient`, `runFullTrust` | Package version is not in the public catalogue response |
| Amazon Appstore | Guide: price Free, DRM off, privacy questionnaire "based on the actual network and account behavior". Policy for this edition: "It has no ads, analytics, or in-app purchases" | Submitted answers are not recorded in the repositories |
| Snap / AppStream | Licence GPL-3.0-or-later. AppStream `content_rating` is an empty OARS 1.1 element, which declares "none" for every category, including in-app purchases, but also for cartoon violence and online chat | The empty OARS element understates combat and chat. Outside this revamp |
| Epic | Free base offer; IARC ratings present; Saudi Arabia and Taiwan excluded | Not live |

## 7. Allowed and banned wording per store

Policy sources were read on 2026-11-24: Google Play [Metadata policy](https://support.google.com/googleplay/android-developer/answer/9898842) and [preview asset rules](https://support.google.com/googleplay/android-developer/answer/9866151); Apple [App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/) 2.3.1, 2.3.3, 2.3.7, 2.3.10; Microsoft [screenshots and images](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/screenshots-and-images); Steam [asset rules](https://partner.steamgames.com/doc/store/assets/rules) and [store assets](https://partner.steamgames.com/doc/store/assets/standard). Amazon and Epic text policies were not confirmed in this pass.

| Store | Allowed | Banned or held, with reason |
| --- | --- | --- |
| Google Play | Full description: "Free and open source", "No ads", "No in-app purchases", "No lootboxes", "No in-game currency", 23 maps, 67 landscapes, 8 computer opponents, 10-lesson tutorial, editor, offline single-player, guest online play, replays, 45 languages. Captions on screenshots up to 20% of the image | **"Free" in the icon, feature graphic, screenshots and video** (asset rules name "Free" for the feature graphic and bar "price and promotional information" in the others). **Price or promotional wording in the short description.** Rankings and performance words anywhere: "Best", "#1", "Top", "New". Calls to action: "Download now", "Play now". ALL CAPS, emoji, unattributed testimonials. MCP (not in the Android build). Campaigns (R5). Confirm the Ads declaration in Play Console first |
| iOS App Store | Description: "Free", "No ads", "No in-app purchases", "No lootboxes", "No in-game currency", maps, landscapes, opponents, tutorial, editor, offline single-player, LAN, guest online play, replays. Text overlays on screenshots (2.3.3) | **Names of other platforms or stores** ("Android", "Windows", "Google Play", "Steam") in any metadata (2.3.10); say "other devices" at most. **Prices, including "Free", in the name, subtitle, screenshots and previews** (2.3.7). Unverifiable claims in the subtitle (2.3.7). MCP. JavaScript AI scripting (hidden in App Store builds). Campaigns (R5). "45 languages" while the store shows 6 (R11). "No tracking", "no data collected", "no analytics" (label is Data Linked to You) |
| Mac App Store | As iOS, for desktop play | As iOS. **MCP held** until a sandboxed-build check passes (R7). JavaScript AI scripting (hidden). "Intel", older macOS: the build is Apple Silicon, macOS 26 |
| Amazon Appstore | "Free", "No ads", "No in-app purchases" (the edition's own policy says so), maps, landscapes, opponents, tutorial, editor, offline play, local network play | **Online multiplayer, ranked, rooms, invites, cross-platform play, accounts** (the edition has none). MCP. Campaigns (R5). Phones (Fire tablets only) |
| Microsoft Store | Description and feature bullets: the fair deal, gameplay counts, MCP co-play section, JavaScript AI. Captions go in the caption field (200 characters), outside the image | **Marketing messages, extra logos or icons inside screenshots.** Text in the bottom third of logo art. Online-play claims are at risk until the Store package is 0.11.7.0 or newer (R6) |
| Snap Store, AppStream, F-Droid metadata | The fair deal, gameplay counts, MCP co-play section (Snap, AppStream), JavaScript AI | MCP in F-Droid text (Android). Campaigns (R5). F-Droid is preparation only |
| itch.io | The fair deal, gameplay counts; MCP and JavaScript AI scoped to "the desktop downloads" | MCP for browser play. "Nothing is sold" (R2). LAN for browser play |
| Epic Games Store | The fair deal, gameplay counts | **MCP held** until the artifact is 0.11.6.2 or newer (R8). Online-play claims at risk on a 0.11.4.0 artifact (R6). Policy text not confirmed here |
| Steam (prepared only) | The fair deal and gameplay counts in the description; MCP co-play section | **Screenshots must "exclusively show the gameplay"**: no marketing copy, awards or written descriptions in them, so captioned sets cannot be used. Capsules: no review scores, awards, discount text, calls to action or other miscellaneous text |
| GOG (prepared only) | As Steam description | Policy not confirmed here |
| Every store | | "First" about MCP or AI (user decision). "Nothing is sold", "never", "forever". Hive Mind, skins, Studios, credits. Player counts, ratings, awards. "Included campaigns". A busy online community. Contributor counts |

## Checks run

- `curl https://app.glob2.online/api/v1/instance` (200, 2026-11-24 18:20 UTC): `features`, `queues`, `guestsAllowed`, `authProviders`, `supportedSimVersions`.
- `curl https://app.glob2.online/api/v1/skins/products` (200); `…/hive/account`, `…/map-studio/account`, `…/music-studio/account`, `…/ai-studio/account` (401 signed-out).
- Signed-out page reads of `app.glob2.online/`, `/skins`, `/commander`, `/map-studio`.
- `git grep` and `git show` at `v0.11.7.0`, `v0.11.8.0` and `origin/master` in the game repository; no branch was switched and no file changed there.
- `strings`, `glob2 info version`, `glob2 info catalog --format json`, `glob2 map generators`, `glob2 --help` on the installed build, with a temporary home directory. The game window was not launched.
- `gh release view v0.11.7.0` and its `package-inventory.json`.
- Public store reads: iTunes lookup and search APIs, the App Store page, the Microsoft display catalogue API, the Snap info API, the itch.io page.
- HTTP status checks of the public handbook, downloads and privacy URLs.

Not done: no sign-in, so credit-pack sales (R2) and Play Console, App Store Connect, Partner Center, Amazon and Epic console answers were not read. No store binary was downloaded or run, so MCP inside the Snap, Microsoft Store and Mac App Store packages is established from source only. No live online or cross-device match was played.
