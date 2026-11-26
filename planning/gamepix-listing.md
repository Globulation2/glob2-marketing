# GamePix listing draft

Status: **approved by the user on 2026-11-26** ("Use draft A"). Nothing has been entered on the GamePix dashboard yet. Built from the storefront-v2 [English source](../translations/en.md) and limited to the claims [storefront v2 claims](../facts/storefront-v2-claims.md) marks safe for browser play, narrowed further to what the GamePix build contains.

## What GamePix asks for

The dashboard's Create New Game form has four fields: **Title**, an optional **Game Jam**, one **Main tag**, and a **Description** of 100 to 500 characters that must explain the controls. Up to four more tags can be added. The form warns: "Do not copy from other websites. Original content helps your game get more traffic." The description below is therefore new wording of approved claims, not storefront-v2 text pasted in.

GamePix writes the public game page itself. Its [OpenTTD page](https://www.gamepix.com/play/openttd), another long-running open-source game, shows a GamePix-written description, features list, "How to play", FAQs, five tags, platform and orientation. Our description and tags are what that page is generated from.

## What the GamePix build contains

The GamePix package runs with portal mode `{externalLinks: false, onlineSignIn: false}` (glob2 `docs/releases/gamepix.md`):

- **No online play.** Play online, Settings → Online and online map links are hidden, so ranked, casual, rooms and cross-play are not claimed.
- **No external links.** No website, Discord or source-code link is claimed.
- **No LAN and no MCP AI co-play:** neither is in any browser build.
- Single-player against the computer, tutorial, map editor, replays and JavaScript opponents are all present.

Revisit this section when GamePix answers our questions about links and online play.

## Approved listing

**Title:** Globulation 2

Unchanged. The storefront rules keep `product_name` on every store except Google Play and Amazon. A subtitle such as "Globulation 2: Colony RTS" was considered for search and not used.

**Main tag:** Strategy games

**More tags (max 4):** War games · City Building games · Management games · Simulation games

The tags follow the game's pillars: fighting rivals, building the colony, running its economy. Alternatives from GamePix's list: Building games, Battle games, Tycoon games. Not used:

- Multiplayer games: no online play in this build.
- Vibe Coded Games: misleading for a volunteer project started in 2001.

**Description (449 characters):**

> Grow a colony of globs and win the fight for land in this real-time strategy game. You decide what to build and where to send workers and warriors; your globs gather, build, eat and fight on their own. Keep the colony fed, train an army and take on 8 computer opponents across 23 maps and 67 random landscapes. Mouse: left-click to build and place flags, right-click to cancel, wheel to zoom, arrow keys to scroll. Touch: drag to pan, pinch to zoom.

An alternative leading with "Command a whole colony, not single units" was offered and not chosen.

## Claims left out, and why

| Claim | Reason |
| --- | --- |
| "No ads" | True of the game, but GamePix shows its own ads around the game and earns from them. Open decision: ads on web portals. |
| "No in-app purchases", "Free" | True, but GamePix already presents every game as free, and the characters are better spent on gameplay and controls. |
| Online play, ranked, rooms, cross-play | Hidden by portal mode on GamePix. |
| Open source, GPL, since 2001/2004 | True, but GamePix bans external links, so players can't follow it to the source. The GPL source offer goes in the in-game credits. |
| 45 languages | True, but GamePix's own language list has 10; the game picks the player's language itself. |
| Map editor, replays, tutorial, JavaScript opponents | True for this build; left out for length. Candidates if GamePix offers a longer field after the game is created. |

## Still needed before submission

- Icon, cover and any banner GamePix asks for once the game exists, from the storefront-v2 key art and screenshots (real game art only).
- Platform and orientation: desktop and mobile, landscape and portrait.
- A release that includes the serial-runtime terrain fix (glob2 #1932). Until then the GamePix build draws flat terrain.

[Planning index](README.md)
