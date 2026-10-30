# Approved storefront presentation and rollout

[Planning index](README.md) · [Task ledger](tasks.md) · [Approved page](../assets/epic-page-preview/README.md) · [Positioning](../analysis/positioning-v1.md) · [Distribution evidence](../facts/distribution.md)

## Approval and scope

On **2026-10-30**, after the final River battle and developed Four Squares strategic replacements, the user approved the presentation for use and instructed: “lets commit this and then apply this to all of our various storefroents”. The approval applies to the final copy and media displayed in the [local page](../assets/epic-page-preview/index.html), recorded at source revision `baa3093` before this approval entry.

Apply this presentation to project-controlled storefront listings and their maintained metadata sources, with destination-specific field formatting and required asset exports. The instruction authorizes those listing updates. It does not establish account control, a successful upload, platform acceptance, a product release, or verified release metadata. Do not change game-build availability, price, account/privacy declarations, system requirements, release dates or ratings merely to make the profile look complete. No outreach or independent-catalog edits are included.

## Approved copy

### Headline

Build a thriving colony in contested territory.

### Short pitch

Build a thriving colony in contested territory. Balance food, workers and expansion, shape a sprawling base, and compete with rival colonies for land and resources.

### About introduction

Food, workers and space shape your expansion. Grow a sprawling colony, balance its competing needs, and contend with rivals for land and resources. Your creatures act autonomously, letting you guide the colony as a whole.

### Grow an economy that can sustain your ambitions.

Food, construction and training compete for your workforce. Decide where workers are needed and balance new ambitions with the needs of the colony you already have.

### Make the map part of your strategy.

Different maps call for different strategies. Adapt your expansion to the terrain, choose what to defend, and find the routes and resources your colony needs.

### Defend what you've built.

Your economy supports both growth and defense. Balance the needs of your colony while rivals compete for land and resources, and prepare for conflicts that can decide the match.

### Free and open source.

A strategy game to play, explore and help shape.

The product title is **Globulation 2**. Descriptive terms are **Strategy / Real-Time Strategy**, **Colony building / Resource management**; use a destination's actual taxonomy. Preserve the colony/economy lead. The local page's proposed Free/Windows offer is not a verified universal platform declaration.

## Approved media and order

| Role | Exact source | Treatment and provenance |
| --- | --- | --- |
| Cover | [Illustrated landscape](../assets/epic-v5/offer-landscape-2560x1440.png) | Promotional illustration, existing title and real source-unit silhouettes; not gameplay. [Artwork provenance](../assets/epic-v5/README.md). Use its existing JPEG delivery export where required. |
| Colony | [Colony replay](../assets/epic-page-preview/media/colony.webp) | Actual Fingerprint replay, tick 41350, fog disabled and outer HUD cropped. [Page provenance](../assets/epic-page-preview/README.md). |
| Battle | [River, blue and gold armies](../assets/epic-gallery-v4/river-battle.jpg) | Staged native scenario with actual combat; [capture pack](../assets/epic-gallery-v4/README.md). |
| Strategic view | [Developed Four Squares match](../assets/epic-gallery-v5/four-squares-midgame-strategic.jpg) | Genuine Cortex AI match at 25,000 ticks; [capture pack](../assets/epic-gallery-v5/README.md). |
| Terrain | [Lava Shield in use](../assets/epic-gallery-v3/lava-shield-terrain-in-use.jpg) | Closer native staged-scene capture; [capture pack](../assets/epic-gallery-v3/README.md). |
| Product logo | [Transparent logo](../assets/epic-v5/product-logo-960x540.png) | Existing wordmark; preserve proportions. |

The cover belongs in key-art/cover slots. Keep the four gameplay images separate where a store permits screenshots only. The preview uses colony, strategic and battle images with their corresponding About sections. Preserve full HUDs in the native captures; do not retouch game content or recolour units. Keep the rejected fog image, older repetitive crops and superseded whole-map view out of new listing uploads. Additional platform crops or device-specific screenshots require their own fit check; desktop images do not demonstrate phone/tablet compatibility.

## Execution ledger

| Work unit | Status on 2026-10-30 | Evidence / next action |
| --- | --- | --- |
| Approved source copy/media | Complete | Final source already committed through `baa3093`; this record saves the user's approval and rollout authorization. |
| Desktop PNG exports | Complete | [Four screenshots and source manifest](../assets/storefront-approved-v1/README.md), committed as `a968359`; decoded RGB preserved exactly. Existing key-art/logo sources linked. |
| Maintained game-store metadata | Complete | [Game PR #1281](https://github.com/Globulation2/glob2/pull/1281) merged as `7038776f3fb84f43cacd51ff02e3c4d1aac4a331`. Snap, AppStream, Android English metadata and maintained iOS/Windows/Amazon copy now use the approved message. Desktop/Mac guides link the canonical pack. |
| Snap-specific exports | Complete | [Four sub-2 MB JPEGs, exact listing fields and a reviewed 3:1 banner](../assets/storefront-approved-v1/snap/README.md), committed as `f1d6af4`; all four gallery images and the banner uploaded and publicly verified. |
| Exact storefront/account inventory | In progress | Snap publisher access verified; Google Play package `org.globulation2.glob2` found in authenticated closed testing. Epic and Microsoft still require sign-in; other consoles and unpublished listings remain to verify. |
| Snap listing application | Complete | Approved copy, homepage, Games category, four ordered screenshots and banner are live; independently verified on the public listing and API at 18:06 Toronto / 22:06 UTC on 2026-10-30. |
| Cross-store application | In progress | Snap is complete; Google Play copy work continues and remaining store consoles still need verified access/application. |

## Destination status

| Destination | Applied source changes | Live status / next action |
| --- | --- | --- |
| Snap (`globulation2`) | `snap/snapcraft.yaml`: approved short/full description and modern homepage; AppStream gallery refreshed. | Complete: public listing/API show the approved summary, full description, `https://glob2online.com/` homepage, Games category, Colony / River / Four Squares / Lava Shield gallery and banner. Verified 18:06 Toronto on 2026-10-30; stable 0.11.2 and app icon unchanged. |
| Desktop AppStream | Approved summary/description, modern homepage and four immutable hosted screenshots; local default PNG matches the hosted colony image. | Merged upstream metadata, for downstream packaging. No Flathub listing submission or independent package-catalog edit was performed. |
| Google Play / Android | `fastlane/metadata/android/en-US/short_description.txt` and `full_description.txt` updated. Existing account/network/privacy/IAP paragraphs retained byte-for-byte. | Authenticated console identified controlled package `org.globulation2.glob2` in closed testing. Listing-copy work continues; no completed live save is recorded yet. Existing mobile screenshot directories remain unchanged; desktop frames are not phone captures. |
| Apple iPhone/iPad | Maintained iOS description, subtitle and promotional text adapted; actual-device screenshot requirement retained. | Console/listing identity and access not verified. Mobile gallery still requires actual release-candidate device captures. |
| Mac App Store | Release guide points to the approved copy, desktop gallery and key-art sources. | Console/listing access and candidate screenshot fit remain to verify. No build selected or released. |
| Microsoft Store (`9PH4FCRMX19F`) | Maintained short/full description and feature copy updated; Windows guide links the three 2560×1440 PNG captures and source limits. | Known product identity; public listing was unavailable in the prior audit. Partner Center requires sign-in; no save/publication verified. Do not enlarge the 1280×720 colony source to imply a new Windows capture. |
| Amazon Appstore | Maintained Fire listing description uses the approved message; Fire-device captures and qualification requirements retained. | Exact live listing and console access not verified. Desktop gallery not substituted for Fire screenshots. |
| Epic | Shared desktop setup points to the canonical approved presentation and export pack; Epic remains the first selected store. | Developer Portal requires sign-in. Exact controlled product and current fields still to verify; no upload or live save claimed. |
| Steam / GOG / itch.io | Shared desktop setup points to the canonical approved presentation and export pack. | Exact controlled listing/console identities and current fields still to verify; no upload or live save claimed. |
| SourceForge / independent catalogs | No external edits. | SourceForge remains unchecked in this authenticated pass; current maintainer control is unverified. Independent wrappers and distribution-maintained catalogs are not presumed controlled storefronts. |

## Snap live verification — 2026-10-30

The [public Snap listing](https://snapcraft.io/globulation2) and [public information API](https://api.snapcraft.io/v2/snaps/info/globulation2) were independently checked at **18:06 America/Toronto / 22:06 UTC**. They show the exact approved summary and full description, `https://glob2online.com/` homepage and Games category. The app icon and **stable 0.11.2** release remain unchanged. The authenticated save was also explicitly confirmed; no private publisher-page proof is committed.

All four gameplay images appear in the approved order, and the 3:1 illustration banner is live. Each public media URL returned HTTP 200, decoded successfully and remained below 2,000,000 bytes:

| Role / order | Public media |
| --- | --- |
| Banner | [1440×480 illustrated banner](https://dashboard.snapcraft.io/site_media/appmedia/2026/10/banner-1440x480.jpg) |
| 1 — Colony | [Colony screenshot](https://dashboard.snapcraft.io/site_media/appmedia/2026/10/01-colony-1793397810.jpg) |
| 2 — River battle | [Blue/gold battle screenshot](https://dashboard.snapcraft.io/site_media/appmedia/2026/10/02-river-battle-1793397810.jpg) |
| 3 — Four Squares strategic view | [Developed AI match screenshot](https://dashboard.snapcraft.io/site_media/appmedia/2026/10/03-four-squares-strategic-1793397810.jpg) |
| 4 — Lava Shield terrain | [Terrain-in-use screenshot](https://dashboard.snapcraft.io/site_media/appmedia/2026/10/04-lava-shield-terrain-1793397810.jpg) |

The [Snap export pack](../assets/storefront-approved-v1/snap/README.md) retains source provenance and file validation. No binary, price, icon or release state was changed. Google Play and other storefront work remain in progress; completing Snap does not complete the cross-store rollout.

## Validation and limits

The game metadata work used an isolated worktree from `afab6e9b28`, leaving the existing game checkout and its concurrent branch untouched. XML and YAML parsed; Android short/full text is 47/1643 characters, iOS subtitle/promotional text is 30/164. All four hosted screenshot URLs returned HTTP 200, and the AppStream default exactly matches the local PNG bytes. `tools/release/release.py check`, all 34 package-asset tests and whitespace checks passed. No engine build was needed for presentation-only metadata changes. No mobile screenshot, application icon, game build, price or account/privacy declaration was changed.
