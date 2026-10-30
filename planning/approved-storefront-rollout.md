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
| Exact storefront/account inventory | In progress | [Public audit](../facts/platform-audit.md) supplies known identities; authenticated consoles and unpublished listings remain to verify. |
| Live storefront application | Access pending | Snap's editor requires publisher sign-in; no listing save was possible. Access to the other store consoles has not yet been verified in this run. Repository metadata changes are not a live-console publication. |

## Destination status

| Destination | Applied source changes | Live status / next action |
| --- | --- | --- |
| Snap (`globulation2`) | `snap/snapcraft.yaml`: approved short/full description and modern homepage; AppStream gallery refreshed. | Known public listing. Publisher authentication required to change current Store copy/images; not saved live. Do not publish a new binary just to update presentation. |
| Desktop AppStream | Approved summary/description, modern homepage and four immutable hosted screenshots; local default PNG matches the hosted colony image. | Merged upstream metadata, for downstream packaging. No Flathub listing submission or independent package-catalog edit was performed. |
| Google Play / Android | `fastlane/metadata/android/en-US/short_description.txt` and `full_description.txt` updated. Existing account/network/privacy/IAP paragraphs retained byte-for-byte. | Console/listing identity and access not verified here. Existing mobile screenshot directories remain unchanged; desktop frames are not phone captures. |
| Apple iPhone/iPad | Maintained iOS description, subtitle and promotional text adapted; actual-device screenshot requirement retained. | Console/listing identity and access not verified. Mobile gallery still requires actual release-candidate device captures. |
| Mac App Store | Release guide points to the approved copy, desktop gallery and key-art sources. | Console/listing access and candidate screenshot fit remain to verify. No build selected or released. |
| Microsoft Store (`9PH4FCRMX19F`) | Maintained short/full description and feature copy updated; Windows guide links the three 2560×1440 PNG captures and source limits. | Known product identity; public listing was unavailable in the prior audit. Partner Center access/save/publication not verified. Do not enlarge the 1280×720 colony source to imply a new Windows capture. |
| Amazon Appstore | Maintained Fire listing description uses the approved message; Fire-device captures and qualification requirements retained. | Exact live listing and console access not verified. Desktop gallery not substituted for Fire screenshots. |
| Epic / Steam / GOG / itch.io | Shared desktop setup points to the canonical approved presentation and export pack; Epic remains the first selected store. | Exact controlled listing/console identities and current fields still to verify. No upload or live save claimed. |
| SourceForge / independent catalogs | No external edits. | SourceForge is a historical public project; current maintainer access must be verified. Independent wrappers and distribution-maintained catalogs are not presumed controlled storefronts. |

## Validation and limits

The game metadata work used an isolated worktree from `afab6e9b28`, leaving the existing game checkout and its concurrent branch untouched. XML and YAML parsed; Android short/full text is 47/1643 characters, iOS subtitle/promotional text is 30/164. All four hosted screenshot URLs returned HTTP 200, and the AppStream default exactly matches the local PNG bytes. `tools/release/release.py check`, all 34 package-asset tests and whitespace checks passed. No engine build was needed for presentation-only metadata changes. No mobile screenshot, application icon, game build, price or account/privacy declaration was changed.
