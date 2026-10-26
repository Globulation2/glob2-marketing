# Product, creator and commercial-capability ledger

[Fact index](README.md) · [Repositories](repositories.md) · [Assets](assets.md) · [Distribution](distribution.md) · [History](history.md)

Observed **26 October 2026**. Unless a row says otherwise, these are **documented source capabilities**, read at game revision [`c9198b854a2ea6fc16cd5524913cf96c5a80c499`](https://github.com/Globulation2/glob2/tree/c9198b854a2ea6fc16cd5524913cf96c5a80c499). They are not claims of launch readiness, enabled production features, live revenue, audience demand or physical-device qualification. Website evidence is at [`6e391ebe93b725747827a3ed7cea78f0d0d8f7e1`](https://github.com/Globulation2/glob2-online-website/tree/6e391ebe93b725747827a3ed7cea78f0d0d8f7e1).

## Gameplay and player surfaces

| ID | Capability | Source / factual scope | Verification boundary |
| --- | --- | --- | --- |
| P01 | Indirect colony control | `README.md`; `src/hud/input/GameGUIInputMenuClickBuilding.cpp`; `src/unit/UnitActivity.cpp`; `src/unit/UnitMovement.cpp` | Players set building worker demand and place work/exploration/war flags; globs route and meet needs autonomously. Not a promise that every task succeeds immediately. |
| P02 | Interdependent economy and population | `src/building/IntBuildingType.cpp`, `src/building/Misc.cpp`; website `src/data/marketing.ts` | Inns/food, swarm births, hauling, construction, healing and training compete for time and workers. Workers, explorers and warriors have distinct roles. |
| P03 | Rival play and objectives | `src/game/WinningConditions.cpp`, `docs/features/custom-game-setup/README.md` | Conquest, prestige and scenario objectives; rulesets/custom parameters influence pacing, hunger, training and regrowth. No single universal match length established. |
| P04 | Learn and play solo | `campaigns/Tutorial_Campaign.txt`, `docs/ai/README.md`; website `docs/website-content-verification.md` | Tutorial, campaigns, custom games, multiple computer opponents and editor. Prior website observer saw tutorial/custom-game menus and played portions on 9 October; this audit did not complete campaigns. |
| P05 | Offline/LAN and online modes | `docs/multiplayer/lan.md`, `rooms-and-matches.md`, `client.md`, `identity.md` | Source supports rooms/invites, public rooms, casual/quick matches and account-ranked play. Website prior observation states guests can use rooms/casual while ranked requires sign-in. Fresh anonymous play and matchmaking liquidity not measured. |
| P06 | Multiplayer records and competition infrastructure | `docs/multiplayer/ratings-and-matchmaking.md`, `history-and-web.md`, `turn-verification.md` | OpenSkill-based ratings, provisional status, player records, match history, AI rating entities, verification and sim-version grouping. Neither user counts nor tournament demand follows from this infrastructure. |
| P07 | Browser/native/mobile clients | `browser/README.md`, `docs/browser/`, `docs/mobile/`, `docs/releases/` | Source/build coverage includes browser, Windows/macOS/Linux, Android and iOS. Store acceptance, release availability and real-device controls remain separate checks. Website prior evidence specifically avoids a blanket phone-support claim. |
| P08 | Replays and gameplay recording | `docs/features/gameplay-recording.md`, `src/replay/`, website capture verification | Source describes MP4 recording, game audio, semantic chapters/events and extraction; website used replay views for captured colony imagery. Public replay/download journeys not freshly tested. |
| P09 | Optional experimental rules and content | `docs/features/experimental-features.md`, `farm-areas.md`, `guard-area-balancing.md`, `markets-v2.md`, terrain/resource catalogs | Experiments can change balance/pacing and are preserved in match/save/replay context. They are not all default gameplay; tutorial/campaign local experiment behavior differs. |

For the gameplay claims already used by the public introduction, the website's [verification record](https://github.com/Globulation2/glob2-online-website/blob/6e391ebe93b725747827a3ed7cea78f0d0d8f7e1/docs/website-content-verification.md) preserves an older checked engine revision, public observation dates, menu labels, screenshot counters and limitations. It is prior evidence, not a fresh 26 October device qualification.

## Creator and community-content estate

| ID | Existing source system | Evidence paths under game repository | What exists / limits |
| --- | --- | --- | --- |
| P10 | Map authoring and sharing | `docs/map-generators/README.md`, `docs/multiplayer/client-content.md`, `map-studio.md` | Native editor, generated maps, catalog versions, previews and private/unlisted/public sharing contracts. AI Map Studio adds private conversations, generated revisions, validation, downloads and explicit publication. Opening checks do not prove competitive balance or enjoyment. |
| P11 | JavaScript AI library and coding | `docs/multiplayer/ai-library.md`, `coding-studios.md`, `docs/scripting/javascript.md` | Authored AI source, isolated validation and immutable releases; AI Studio editing/check/playtest/publish workflow. Local test results do not authorize publication. |
| P12 | Generator code library and Studio | `docs/multiplayer/content-libraries.md`, `coding-studios.md`, `docs/map-generators/javascript.md` | Versioned generator packages and validation, bounded local runs, previews and publication; distinct opt-in coding Studio. No adoption/creator volume measured. |
| P13 | Terrain and resource sets | `docs/multiplayer/content-libraries.md`, `docs/features/terrain-resource-sets.md`, `docs/hosting/art-studios.md` | PNG/package drafts, properties, credits, previews, immutable releases, likes/download/report contracts; optional generation. Engine validation capabilities are gated and publication may be disabled. |
| P14 | Building families | `docs/multiplayer/building-library.md`, `docs/features/building-authoring.md`, `building-family-packages.md` | Portable building catalogs/families, authored services/effects and library validation; optional building Studio. Gameplay-changing content differs from cosmetic content. |
| P15 | Community soundtracks and Music Studio | `docs/multiplayer/music-library.md`, `docs/assets/music-packages.md`, `music-pipeline.md` | Three-mood arrangements, technical validation, preview mixing, licenses/credits/AI disclosure and portable downloads. Optional symbolic generation needs listening and cost qualification; automated checks alone do not establish musical quality. |
| P16 | Colony appearance designer and presets | `docs/multiplayer/colony-skins.md` | Custom paint/material maps, versioned publication, equipment and frozen match appearances, preset entitlements. Source includes purchase paths; live prices/sales not established. |

The [feature index](https://github.com/Globulation2/glob2/blob/c9198b854a2ea6fc16cd5524913cf96c5a80c499/docs/features/README.md) and [multiplayer index](https://github.com/Globulation2/glob2/blob/c9198b854a2ea6fc16cd5524913cf96c5a80c499/docs/multiplayer/README.md) are maintained entrypoints. The table inventories systems rather than claiming that each is available on the currently deployed instance.

## Existing commercial machinery

| ID | Mechanism already in source | Evidence | Status / boundary |
| --- | --- | --- | --- |
| B01 | One-time colony skin/designer entitlement purchases | `docs/multiplayer/colony-skins.md:211`; products `designer`, `stripes`, `spots`; hosted Stripe checkout, reconciliation/refunds/disputes | Configuration missing means purchases unavailable; test mode default, live mode explicit. No verified prices, successful live purchase, revenue or payer count collected. |
| B02 | Hive Mind commander usage credits | `docs/multiplayer/hive-mind.md` | Natural-language commands, reports and standing orders alongside manual controls, including ranked where instance permits. Feature/sales flags default off. Docs describe prepaid packs and no subscriptions/automatic top-ups/expiry. Live-model, payment and playtesting gates precede enablement. |
| B03 | AI Map Studio generation credits | `docs/multiplayer/map-studio.md`, `docs/hosting/map-studio.md` | Separate wallet/purchases; generation reserves one map credit, validated delivery consumes it, failures return it. Conversation and publication are distinct. Demand, generation quality and actual sales unmeasured. |
| B04 | Domain-specific Studio usage accounting | `platform/packages/billing/src/credits.ts:44`; `docs/multiplayer/coding-studios.md`, `docs/hosting/art-studios.md`, `docs/hosting/music.md` | Registry includes buildings, hive, maps, terrain, music, generatorStudio, aiStudio. Separate namespaces/balances; opt-in services, caps and provider configuration. No shared subscription or creator marketplace revenue share established. |
| B05 | Shared payment/credit/reporting implementation | `platform/packages/billing/src/{checkout,credits,reporting,usage}.ts` | Reservation/settlement, retries/reconciliation and financial reporting exist. Infrastructure does not establish product-market fit, margins or commercial viability. |

[Assets](assets.md#written-assets-and-existing-message-variants) records Android listing copy saying no in-app purchases/analytics. That scoped platform copy and optional account/web payment/reporting systems coexist in source. This audit documents the difference; it has not established a policy contradiction, verified live configuration or chosen future claims. New business-model possibilities belong in analysis, not in this factual ledger.

## Measurement and account infrastructure

- Game `docs/hosting/admin-reporting.md:26` documents independently configurable activity collection and administrator display, default true in source configuration. It records authenticated guest/registered account-day activity, excludes anonymous visitors/service requests and distinguishes gaps from zero. It is **not** a public-site acquisition funnel or an independently verified live DAU report.
- The same document describes 7/30/90-day comparisons, library download counts, CSVs, per-product credit flows, actual payment/refund/dispute reporting and provider usage/cost estimates when rates are supplied. Currency/mode distinctions, incomplete usage and unknown historical amounts are explicit. Fees, hosting bills, exchange rates and profit are outside that report.
- `docs/multiplayer/identity.md` and `account-management.md` document guest/registered identities, configured sign-in providers, profiles, account export/deletion and retention. A provider implementation does not establish that provider is enabled in production.
- Website README says public pages use no analytics/account cookies; rankings use a sanitized public feed. A functional shared theme preference is documented separately. No mailing-list/CRM, ad conversion pixel, campaign attribution system, or marketing email automation was identified in the inspected website paths. This is a search boundary, not proof none exists elsewhere.

The local website snapshot has null curated release metadata, whereas the independent public-estate inspection found a deployed experimental native release. See [distribution](distribution.md) for live download observations; a local snapshot is not the current deployed release catalog.

## Explicit unknowns

Live feature flags and paid-service availability; real checkout prices/conversion; retention/acquisition cohorts; operating cost; physical-device qualification; store acceptance; matchmaking wait times; active player/creator counts; accessibility testing across devices; asset-review completion for all submissions; and qualitative player motivations. No private analytics, account tables or store dashboards were accessed. These unknowns limit claims and remain inputs for later research, without selecting a marketing direction.
