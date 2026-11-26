# GamePix listing comparison

Observed 2026-11-26. Rankings come from GamePix's public JSON feed: `https://feeds.gamepix.com/v2/json?order=quality&sid=1&pagination=96&page=1&category=strategy`, plus the same feed without a category. It returns title, description, category, orientation and GamePix's `quality_score`. Game pages were read with a page-reader fetch, because `curl` is blocked by Cloudflare: Defend the Castle, Perimeter - Legate Edition, Transport Tycoon Deluxe - Open TTD and the `/t/strategy` tag page. Platform rules are in the [GamePix launch](../planning/gamepix-launch.md) record, read on 2026-11-26 from GamePix's developer pages. That record also holds our draft entry BL8O73.

Sample: the top 25 of the 96 strategy games in the quality-ranked feed, plus the 96 top games overall, for orientation and description patterns. Three of those pages were read in full.

## What the top strategy games do

| Feature | Top strategy (feed and sampled pages) | Globulation 2 draft (BL8O73) |
|---|---|---|
| Feed description length | median 316 characters (top 30) | 449 characters |
| Orientation | 63 of 96 landscape, 26 portrait, 7 "all" | All |
| Tags on page | 4–5 (OpenTTD: Strategy, Money, City Building, Tycoon, Simulation; Perimeter: Strategy, War, Retro, Classics, Mobile) | 5 (Strategy, War, City Building, Management, Simulation) |
| How to Play | Present on all three pages; Defend the Castle and OpenTTD give real controls, Perimeter's is empty | 497 characters, desktop and mobile controls |
| Custom sections | OpenTTD: "Strategic Infrastructure and Logistical Success" and "Game Features" | none |
| FAQs | Defend the Castle adds its own ("How do I lose?", "How do I win?") before GamePix's generic "best strategy games" links | none |
| Gameplay video | Defend the Castle shows a "Gameplay footage" slot | none |
| Screenshots | none shown on any page; only the cover | n/a (GamePix takes only an icon and a cover) |
| Rating | 8.0–9.6 out of 10 from 237–632 votes | not live |

Two classic PC strategy ports sit high in GamePix's strategy ranking. Perimeter - Legate Edition, a real-time strategy game, is second of 96 (8.8 from 237 votes). OpenTTD is 18th (8.0 from 632 votes). Most of the rest are tower defence, idle and stickman war games.

## How GamePix discovery works (observed)

- GamePix writes the public page from the developer's fields: title, main tag and up to four more tags, a 100–500-character description, How to Play (up to 500 characters), optional Custom Sections (title up to 35 characters, body up to 350), optional FAQs (question up to 80 characters, answer up to 150) and an optional YouTube or Vimeo video.
- The feed's `quality_score` orders the lists. GamePix does not publish how it is computed.
- The `/t/strategy` tag page has no sort control. Its SEO text describes strategy games as conquest, tower defence and tycoon games.
- The site header shows "Recently played", "Most played", "Discovery", "New", "Trending" and "Specials".

## Inferences (not validated)

- Perimeter and OpenTTD ranking high suggests GamePix players accept a deeper PC-style strategy game in the browser. Glob2 is the same kind of product, so there is a fit.
- The page has no screenshots, so the cover and, if supplied, the video are the only pictures a player sees before pressing play. The video slot is the only place to show the colony at work.
- Custom Sections and FAQs are extra indexed text on the page. OpenTTD uses them for features. They may help search, but that is not measured.
- Our orientation "All" is uncommon (7 of 96). If the game is poor in portrait on a phone, players who open it that way meet a bad first screen.

## Limits

One day's feed snapshot. The quality score's inputs are unknown. Only three game pages were read in full because of the Cloudflare block. The vote counts are small, so the ratings are noisy.

## Action list for our listing

The draft is saved and has no build; it waits on the next release ([GamePix launch](../planning/gamepix-launch.md)). These are field changes on the existing draft, ranked by impact against effort.

| # | Change | Evidence | Effort |
|---|---|---|---|
| 1 | **Add the gameplay trailer** (https://www.youtube.com/watch?v=t6Q3ZpY9aTM, already on Game Jolt) in the Editorial video field. First check that it shows nothing the GamePix build lacks: no online lobby, Discord or website links, and no MCP. | The page shows only a cover; the video slot is the only moving picture. Defend the Castle uses it. | Low |
| 2 | **Add two or three FAQs** answered from approved claims, for example "Do I control each unit?" (No: you choose what to build and where to send workers and warriors; your globs do the work), "How do I win?" (defeat the rival colonies; check the exact wording against the game's victory conditions before saving), "Where do I start?" (the 10-lesson Tutorial). | Defend the Castle's own FAQs; the field limits are 80 and 150 characters. | Low |
| 3 | **Add one Custom Section, "Game features"** (up to 350 characters), with the approved feature lines the build supports: 23 maps and 67 random landscapes, 8 computer opponents, up to 16 colonies, the map editor, replays. Then **drop the controls from the description** to leave room for gameplay, since How to Play already carries them (open decision 5 in the GamePix record). | OpenTTD's "Game Features" section. GamePix asks for controls in How to Play. | Low |
| 4 | **Set orientation to Landscape** unless a phone test in portrait shows a usable layout. | 63 of 96 strategy games are landscape; "All" is rare. | Low (needs one phone check) |
| 5 | **Keep the five tags**, which match OpenTTD's pattern. `Retro`/`Classics`, as on Perimeter, would be arguable for a game started in 2001 but could suggest old graphics; not recommended. Do not add `Multiplayer`: online play is hidden in this build. | Perimeter and OpenTTD tag sets; portal mode turns online off. | None |

Claims still out of the GamePix copy: online play, external links, MCP, LAN and "No ads" (GamePix earns from ads around the game). Campaigns stay out too: [storefront claims](../facts/storefront-claims.md) R5 found no ready-made campaigns shipped.

**Decisions for the user** (already open in the GamePix record): ads on web portals, Allow distribution, and whether the description should keep the controls.
