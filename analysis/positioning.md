# Storefront positioning

[Analysis index](README.md) · [Working rules](../AGENTS.md#storefront-v2-revamp--2026-11-24) · [Rollout ledger](../planning/storefront-rollout.md) · [Positioning v1](https://github.com/Globulation2/glob2-marketing/blob/4e62f805935fa57724d66338071ee8553f059f18/analysis/positioning-v1.md) · [Product facts](../facts/product.md)

Decided by the user on **2026-11-24**. This supersedes [positioning v1](https://github.com/Globulation2/glob2-marketing/blob/4e62f805935fa57724d66338071ee8553f059f18/analysis/positioning-v1.md) as the message reference for store listings. It is a user decision, not a player-research finding: no wording here has been tested with players, and nothing here shows that a listing has changed.

This file sets what each listing leads with, what supports it, and what may not be said. It does not hold listing copy. The exact wording is written as `storefront-v2` in the [canonical English source](../translations/en.md), which still held `storefront-v1` when this record was written.

## The decision

The user's instruction on the message:

> make sure we are mentioning some of our biggest advantages like being 100% ad-free while also free to play and also no annoying lootboxes or in-game currencies. For desktop users, being the first game you can play in tandem with AI through MCP is a selling point. For mobile users, its just great RTS gameplay.

Two points were then settled with the user:

- **"First" is dropped.** After being shown the [prior-art research](../planning/mcp-outreach/product-and-prior-art.md), which lists earlier and overlapping games playable through MCP, the user chose not to claim "first".
- **Nothing is sold.** Asked what is sold to players, the user answered: "Nothing is sold".

The platform split below was selected by the user from options presented by the coordinating agent.

## Platform split

| Listing class | Stores | Leads with | Adds |
| --- | --- | --- | --- |
| Mobile | Google Play, iOS App Store, Amazon Appstore, F-Droid metadata | Great real-time-strategy gameplay, plus the fair deal | Touch play |
| Desktop | Microsoft Store, Epic Games Store, Snap, itch.io, Mac App Store, AppStream metadata; Steam and GOG prepared only | The same gameplay and fair deal | AI co-play through the built-in MCP server |

MCP is a native desktop feature (Windows, macOS, Linux). It is not part of browser play, so on itch.io it describes the desktop downloads only. It goes into a desktop listing only where [the claims record](../facts/storefront-claims.md) confirms it for that store's build; the sandboxed Mac App Store build is the open case.

## Key messages in priority order

### Mobile

1. **Great real-time strategy.** Grow a colony, fight rival colonies for land and resources. This is the opening promise.
2. **The fair deal.** Free, no ads, no in-app purchases, no lootboxes, no in-game currency. Stated flatly, near the top.
3. **What you actually do.** You set priorities and place flags; your globs do the work. Indirect control, in player terms.
4. **Ways to play.** Skirmish against computer opponents, campaigns, map editor, online multiplayer, offline play. Each only as verified for that platform.
5. **Heritage and open source.** A long-running open-source game, as social proof rather than the pitch.
6. **Built for touch.** In the platform tail.

### Desktop

1. **Great real-time strategy.** As mobile.
2. **The fair deal.** As mobile.
3. **Play alongside your own AI agent.** Connect your own AI agent through the game's built-in MCP server and play the same colony together. Its own section, in desktop listings only.
4. **What you actually do.** As mobile.
5. **Ways to play.** As mobile.
6. **Heritage and open source.** As mobile.

The user fixed that desktop adds AI co-play as a selling point, not its exact position. Placing it third, after the fair deal, is this record's working order; the composition in `translations/platforms.json` is the final word.

## Proof points

A proof point may be used in copy only as far as [the claims record](../facts/storefront-claims.md) confirms it for the store in question.

| Message | Support | Limit |
| --- | --- | --- |
| Real-time strategy with indirect control | [Product ledger](../facts/product.md#gameplay-and-player-surfaces) P01–P03: players set worker demand and place flags; globs route and meet needs on their own; rival play with conquest and other objectives | No claim that every task succeeds at once, and no fixed match length |
| Fair deal | The user's statement that nothing is sold; stores configured as Free in the [v1 rollout ledger](../planning/approved-storefront-rollout.md) | The source contains payment and credit machinery ([B01–B05](../facts/product.md#existing-commercial-machinery)). Production flags and each store's ads and purchase declarations are checked in the claims record |
| Ways to play | Product ledger P04–P07: tutorial, campaigns, custom games, computer opponents, editor; rooms, LAN, casual and ranked play; browser, desktop and mobile clients | Counts of maps or campaigns, and per-platform availability, come only from the claims record |
| AI co-play on desktop | [MCP evidence](../planning/mcp-outreach/product-and-prior-art.md#glob2-capabilities-and-availability): opt-in local MCP server in the native desktop builds since public release 0.11.4.0; human input stays active | The player supplies the AI agent and model, which may have their own requirements. No claim about how well an agent plays |
| Heritage and open source | [History](../facts/history.md): first alpha in 2004; GPL-3.0-or-later per [assets](../facts/assets.md) | Dates as recorded there; no player or download counts |

Supporting research for what store visitors look for: [mobile store comparables](mobile-store-comparables.md) and [player priorities](player-priorities.md).

## Banned and cautioned claims

Banned:

- **"First".** Not "the first game", "the first RTS" or "the first MCP-playable" anything, in any language, in copy, captions, images or video.
- **Rankings and superlatives.** No "best", "#1", "top-rated", awards, or comparisons with named games.
- **Invented numbers.** No player counts, download counts, ratings, or counts of maps, campaigns or languages that the claims record does not confirm.
- **Hive Mind, colony skins, credit packs and the Studios.** Not promoted, not mentioned as available, not teased as coming.
- **MCP on mobile or in the browser.** It is desktop-only.
- **AI-generated or stock imagery.** See [real game art only](../AGENTS.md#real-game-art-only).

Cautioned:

- **Fair deal wording.** Say what is true of the product on that store. It is a statement about ads and purchases, not about privacy or data collection; do not add "no tracking" or "no data collected". The App Store privacy label is [flagged in the ledger](../planning/storefront-rollout.md#flagged-outside-this-plan).
- **Accounts and offline play.** Scope "no account" and "offline" to what the claims record confirms, such as single-player. Avoid "free forever" and "no account ever".
- **AI co-play.** Say "your own AI agent". Do not imply the game includes, sells or requires an AI model.
- **Multiplayer.** Name the modes that exist; make no promise about opponents being available or wait times.
- **Captions and footage.** Describe only what the frame shows. Label AI-versus-AI footage as a spectator view, per [gameplay video](../planning/gameplay-video.md).
- **Store policy.** No price or "free" inside images or the Google Play feature graphic; no all-caps, calls to action or rankings in Google Play text; no mention of other platforms in Apple copy; no marketing text inside Microsoft or Steam screenshots. These guards come from the approved plan and are confirmed per store by the independent policy reviewer.
- **Earlier cautions still apply.** Do not imply a cozy, combat-free, persistent or short-session game ([positioning options](positioning-options.md)).

## How v2 differs from v1

| Topic | v1 (2026-10-26) | v2 (2026-11-24) |
| --- | --- | --- |
| Lead | Colony building and economics; battles "part of the game rather than the whole promise" | Great real-time-strategy gameplay. The colony and economy remain the substance of what the player does; the user did not ask to remove them |
| Monetisation | "Free and open source" only; earlier drafts warned against blanket no-purchase claims | The fair deal is stated flatly: free, no ads, no in-app purchases, no lootboxes, no in-game currency |
| AI | "Control innovation, Hive Mind and JavaScript tooling are not the launch's lead promise" | Desktop listings add AI co-play through MCP as a selling point. Hive Mind is still not promoted, and JavaScript tooling is still not a lead message |
| Platforms | One message everywhere, with short platform tails | Mobile and desktop listings differ in what they add |
| Imagery | The approved v1 source family, including an illustrated cover | Real game art only, bound by the footage rule |
| Validation | User decision, not player-validated | The same |

## Evidence

- [Mobile store comparables](mobile-store-comparables.md): how comparable strategy listings present themselves.
- [Player priorities](player-priorities.md): what players say they want from a strategy listing and its monetisation.
- [Storefront v2 claims](../facts/storefront-claims.md): per-store allowed and banned wording, with the checks behind it.

These three records were being written by other agents when this file was created. If one of them contradicts a message above, the claim is dropped or scoped, and the difference is reported to the user and logged in the [rollout ledger](../planning/storefront-rollout.md).
