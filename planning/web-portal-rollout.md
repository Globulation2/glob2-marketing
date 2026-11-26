# Web game portal rollout

Started 2026-11-26. Covers getting the browser build of Globulation 2 onto Game Jolt, Newgrounds, CrazyGames, GameDistribution (Azerion), Yandex Games and Poki, plus a pitch to Armor Games. GamePix and itch.io are tracked separately in [GamePix listing](gamepix-launch.md) and [itch.io launch](itch-io-launch.md).

Evidence levels used below: **prepared** (drafted locally), **saved** (stored on the portal, not public), **submitted** (sent for review), **live** (publicly verified by loading the page).

## User decisions

- 2026-11-26: the user asked for "a game plan to get builds done, accounts registered and automated release pipelines implemented" for the six portals, with Poki to use the small download build from another thread, and to "pitch Armor Games just to see what they say".
- External links and online sign-in follow **per-portal rules** (user selection): each portal turns off only what it bans.
- Accounts: Claude fills in sign-up forms; passwords are saved in the user's password manager, never typed by Claude. Usernames are the user's own handle, not a Globulation-branded one (the user renamed the Game Jolt account to their handle).
- 2026-11-26: after the gjpush token was rejected, the user said "lets get it on there manually for now too", then approved making the Game Jolt page public, then approved the four listing fixes in [Game Jolt listing comparison](../analysis/gamejolt-listing-comparison.md) ("Apply all four").

## Status

| Portal | State | Next step |
|---|---|---|
| Game Jolt | **Live** 2026-11-26, release 0.11.801 playable in the browser | Devlog posts; automated upload once a gjpush token arrives |
| Newgrounds | Account signed in; no project yet | Create the project page and upload the Newgrounds zip |
| CrazyGames | Developer portal set up; nothing submitted | Needs a build with portal mode and a first download under 50 MB |
| GameDistribution | Developer application submitted, awaiting approval | Game ID from the dashboard, then upload |
| Yandex Games | Parked | Not accepting new developer applications; the full build is also over its 100 MB limit |
| Poki | Not applied | Apply through the game submission form once the small download build exists |
| Armor Games | Pitch email **prepared** as a draft, not sent | The user checks the generative-AI disclosure line and sends it |

## Build and packaging (glob2 repository)

All three pieces are merged on glob2 master (2026-11-26):

- Per-portal packager (Globulation2/glob2#1926): `platforms/web/package-portal.py --portal <name>` repackages the verified `browser-release` artifact for gamepix, crazygames, newgrounds, gamejolt and gamedistribution. Each zip carries `window.GLOB2_PORTAL = {name, externalLinks, onlineSignIn}`.
- Portal mode in the game (Globulation2/glob2#1927): the game hides external links and online sign-in when the portal object says so.
- Game Jolt upload job (Globulation2/glob2#1928): `browser-release` can push the Game Jolt zip with gjpush. Release versions fold the fourth tag part into the patch: v0.11.8.1 becomes 0.11.801.

Release run 45873293249 on the release mirror (2026-11-26, tag v0.11.8.1, publish off) built all five portal zips. Package size: 126 MB zipped, about 219 MB unpacked, about 495 files.

**Caveat:** the game binary is built from the release tag, and v0.11.8.1 predates portal mode. Zips from that tag ignore the portal settings. That is harmless for Game Jolt and Newgrounds, which keep links and sign-in, but the CrazyGames and GameDistribution zips must wait for the first tag that contains #1927.

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

### Automated upload: blocked

gjpush rejected every token with "Authorization token is invalid" (three attempts on 2026-11-26, including a whitespace-stripped paste). gjpush's README says it needs a "service API authentication token" and that "only testers are given a token". The Game Token in the avatar menu is a different credential, for the in-game Game API. A request for a gjpush token, addressed to the gjpush maintainer listed in that README, is **prepared** as a Gmail draft and not yet sent.

Until a token arrives: dispatch `browser-release` with `gamejolt` off, download the `gamejolt-upload` artifact, and upload it by hand on the package page (New Release → set the version → upload the browser build → fit to screen → Save Build → Publish Release). The release cannot be saved as a draft until a build is attached.

### Claims note

Game Jolt shows its own site advertisements around the game page. "No ads" in the description refers to the game itself, which shows none.

## Newgrounds

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

- **Ads:** storefront-v2 copy says "No ads". CrazyGames, GameDistribution, Yandex and Poki run their own ads around or inside games, so the claim needs scoping per portal before those listings go live. See [storefront v2 claims](../facts/storefront-v2-claims.md).
- **Game Jolt development stage:** Early Access or Complete/Stable.
- **Game Jolt devlog:** whether to post a launch devlog. The comparison found devlog posting is the main gap against top games.
