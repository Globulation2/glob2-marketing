# Storefront v2: what changed, expected effect and traffic options

[Analysis index](README.md) · [Rollout ledger](../planning/storefront-rollout.md) · [Current store status](../planning/storefront-rollout.md#current-status-and-open-follow-ups) · [Positioning v2](positioning.md) · [Mobile store comparables](mobile-store-comparables.md) · [Player priorities](player-priorities.md) · [Task ledger](../planning/tasks.md)

Written **2026-11-26** from the rollout ledger, the analysis records linked below and the summary the coordinating agent gave the user that day. It summarises; the linked records hold the evidence. Store states change, so check the [rollout ledger](../planning/storefront-rollout.md) for anything current.

Labels used below:

- **[Evidence]**: observed and recorded elsewhere in this repository, with the date of observation.
- **[Inference]**: the analyst's or coordinator's reasoning from that evidence. Not tested.
- **[Option]**: a possible next step. **The user has not chosen any channel, order or budget.** Nothing here authorizes outreach, posting or spending.

## 1. What changed from v1 to v2

Storefront-v1 was approved by the user on 2026-10-30 ([v1 ledger](../planning/approved-storefront-rollout.md)). Storefront-v2 replaced it from 2026-11-24 under the user's decisions in [AGENTS.md](../AGENTS.md#storefront-v2-revamp--2026-11-24).

| Area | Storefront v1 [Evidence] | Storefront v2 [Evidence] |
| --- | --- | --- |
| Key art | AI-painted landscape that does not look like the top-down game, natively 1672×941 and upscaled ([key-art README](../assets/storefront/key-art/README.md)) | Built from a real in-game scene with the game wordmark, native 4K, cropped per store ([key art](../assets/storefront/key-art/README.md)) |
| Desktop screenshots | Raw captures showing the replay spectator panel, no captions or set order; one upscaled from 720p | Seven per device, in story order, under the busy mid-game [footage rule](../planning/gameplay-video.md) ([desktop captures](../assets/storefront/captures/desktop/README.md)) |
| Mobile screenshots | Legacy menu captures: one iPhone and one iPad image on the App Store (observed 2026-11-24, [comparables §2](mobile-store-comparables.md#2-where-the-current-globulation-2-listing-stands)); F-Droid images at 320×640 | Seven per device; Android sets taken from the real app in the Android emulator ([mobile captures](../assets/storefront/captures/mobile/README.md)) |
| Captions | None | Captions in 45 languages, 2,160 rendered images, plus caption-free sets ([store screenshots](../assets/storefront/store-screenshots/README.md)) |
| Icon | 1024 px store icon was an 8× upscale of a 128 px source ([icon README](../assets/storefront/icon/README.md#provenance)) | Faithful vector redraw of the same blue glob |
| Video | No trailer on any store (observed 2026-11-24) | 30 s trailer on YouTube plus per-store cuts and a vertical cut ([trailer](../assets/storefront/trailer/README.md)); frame-stepped iPhone and iPad app previews ([app previews](../assets/storefront/app-previews/README.md)) |
| Copy | The fair deal (no ads, no purchases) was stated only on Amazon; no MCP; multiplayer only implied; no iOS subtitle search terms; Play short description used 47 of 80 characters | Hook, fair deal, indirect control in player terms, features, heritage and open source. Mobile leads with RTS gameplay; desktop adds AI co-play through MCP, never "first" ([positioning v2](positioning.md), [English source](../translations/en.md)) |
| Search fields | Name and subtitle carried no genre term ([comparables gap 4](mobile-store-comparables.md#gap-4--name-and-subtitle-carry-no-genre-term)) | Search fields filled; Android title "Globulation 2 - Offline RTS" on Google Play and Amazon (user request, 2026-11-26) |
| Translations | Storefront-v1 catalogs ([translation quality audit](../planning/storefront-translation-quality-audit.md)) | 44 translations, each AI-translated and independently AI-reviewed; no native-speaker validation ([translation review](../planning/storefront-translation-review.md)) |
| Copyright | Microsoft's copyright field was empty in all 44 listings (observed 2026-11-26, [ledger](../planning/storefront-rollout.md#log)) | Owner-decided copyright line (decision 11 in the [ledger](../planning/storefront-rollout.md#decisions)) |

v1 details without a link come from the coordinator's 2026-11-26 summary to the user.

Every claim in the copy was checked against the game source, production and each store's declarations in [storefront v2 claims](../facts/storefront-claims.md). Where a store's build does not support a claim, the claim is dropped or scoped for that store.

## 2. Why the new listing should convert better

Supporting research: [mobile store comparables](mobile-store-comparables.md) (store pages observed 2026-11-24), [player priorities](player-priorities.md) (surveys and press, gathered 2026-11-24) and the earlier mechanics-focused [comparable games](comparables.md).

1. **The first screenshots now do the selling job.** [Evidence] Comparable listings spend screenshot one on a genre or value caption over gameplay, or on gameplay that reads at a glance; peers show 5–10 gameplay images per device, and Apple's guideline 2.3.3 says screenshots should not be only title art ([comparables patterns](mobile-store-comparables.md#patterns-across-the-table), [gap 1](mobile-store-comparables.md#gap-1--screenshots-one-menu-image-where-peers-show-510-gameplay-images)). [Inference] First screenshots do most of the selling on a store page, so this is likely the largest change.
2. **The images match the game.** [Evidence] The v1 key art did not look like the game. [Inference] Art that matches what players then see removes an expectation gap that can cost installs and ratings.
3. **The fair deal is a differentiator.** [Evidence] 64% of players surveyed say ads interrupt play (Bain 2025), and pay-to-win is the top stated reason for abandoning mobile games in a vendor survey (Mistplay 2023) ([player priorities](player-priorities.md#summary-table)); the listings with nothing to sell state it early and bluntly ([comparables pattern 5](mobile-store-comparables.md#patterns-across-the-table)). [Inference] It matters most on mobile, where players expect ads and purchases in free strategy games.
4. **The trailer answers "how does it play".** [Evidence] All four re-verified Play peers have a trailer, and Play, Steam and Epic say video affects placement or purchase ([gap 3](mobile-store-comparables.md#gap-3--no-trailer)).
5. **Better search reach.** [Evidence] Most peers put the genre in the name or subtitle; the v1 Play title used 13 of 30 characters ([gap 4](mobile-store-comparables.md#gap-4--name-and-subtitle-carry-no-genre-term)). [Inference] "Offline RTS" and filled keyword fields should match more searches.
6. **Localized captions.** [Evidence] Captions are rendered in 45 languages; 41 pass the 85% legibility gate ([ledger V2-11](../planning/storefront-rollout.md#work-units)).

None of this has been tested with players. Positioning v2 is a user decision, not player validation.

## 3. Honest conversion expectations

[Inference, coordinator's assessment of 2026-11-26] The change should be directionally better, but no number can be promised:

- **Little measurable traffic.** Google Play is a closed test with no public listing; the iOS listing carries only the v2 promotional text until a new build ships; traffic elsewhere is small ([current status](../planning/storefront-rollout.md#current-status-and-open-follow-ups)).
- **Published uplift figures vary too widely** between games and stores to transfer to this listing.
- [Evidence] The comparables record had no conversion data for any listing, so it cannot show that a treatment causes installs ([comparables limits](mobile-store-comparables.md#evidence-labels-and-limits)).

### How it could be measured [Option]

1. **Record a baseline now**, before each store's v2 goes live or as soon as possible after: App Store Connect conversion rate; Microsoft Partner Center page views against acquisitions; Amazon and itch.io views against downloads. No baseline has been recorded yet (2026-11-26).
2. **Compare 2–4 weeks after each store goes live**, using the same metric and window length, and note anything else that changed traffic in that window (press, posts, releases, featuring).
3. **A/B test where the store allows it:** Google Play store listing experiments (after production access) and Apple product page optimization.
4. Website visits from store links can be read in the [website analytics](../planning/website-analytics.md) set up on 2026-11-20; that record explains why it has no earlier baseline.

## 4. Traffic routes

[Inference, coordinator's assessment of 2026-11-26] Conversion is not the bottleneck; reach is. The routes below are options with existing plans. **No decision has been made.** The coordinator suggested, as an order for the user to consider: Play tester push, press follow-up with the new assets, then the MCP launch.

### Open the stores

- **Google Play production.** Needs 12 opted-in testers for 14 days; the count is 0. Plan: [Android closed-test recruitment](../planning/android-closed-test-recruitment.md).
- **iOS 0.11.8.2.** A new build would carry the staged v2 listing and the new icon; owner decision ([current status](../planning/storefront-rollout.md#current-status-and-open-follow-ups)).
- **Apple featuring nomination.** Not yet submitted.

### Referrals

- **Mobile press follow-up.** 29 publications had a pitch attempt on 2026-11-23 ([mobile press outreach](../planning/mobile-press-outreach.md); contacts in [mobile games press](mobile-games-press.md)). A follow-up could carry the new trailer and art.
- **MCP launch** to AI and developer media and creators: research and drafts in [MCP outreach](../planning/mcp-outreach/README.md).
- **Reddit:** community drafts in the [Reddit campaign kit](../planning/reddit-campaign/README.md).
- **Open-source catalogs:** F-Droid, Flathub and distribution packages ([Linux distro rollout](../planning/linux-distro-rollout.md)).

### Video and social

- **YouTube trailer** on the Globulation 2 Online channel, and the **vertical 30 s cut** for Shorts, TikTok and Reels ([trailer files](../assets/storefront/trailer/README.md#files)).
- **Claude Plays Glob stream:** [Twitch streaming](../planning/twitch-streaming.md). It now runs from another machine; its live status is unknown (2026-11-26).
- **Discord and Bluesky** per the [social media strategy](../planning/social-media-strategy.md); account state in [social media accounts](../facts/social-media-accounts.md).
- **Paid ads** only as a small conversion test, since nothing is sold. See the [channel and model map](channels-and-business-models.md) for tradeoffs.
