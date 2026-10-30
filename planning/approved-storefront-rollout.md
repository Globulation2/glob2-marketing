# Approved storefront presentation and rollout

[Planning index](README.md) · [Task ledger](tasks.md) · [Approved page](../assets/epic-page-preview/README.md) · [Positioning](../analysis/positioning-v1.md) · [Distribution evidence](../facts/distribution.md)

## Approval and scope

On **2026-10-30**, after the final River battle and developed Four Squares strategic replacements, the user approved the presentation for use and instructed: “lets commit this and then apply this to all of our various storefroents”. The approval applies to the final copy and media displayed in the [local page](../assets/epic-page-preview/index.html), recorded at source revision `baa3093` before this approval entry.

Apply this presentation to project-controlled storefront listings and their maintained metadata sources, with destination-specific field formatting and required asset exports. The instruction authorizes those listing updates. It does not establish account control, a successful upload, platform acceptance, a product release, or verified release metadata. Do not change game-build availability, price, account/privacy declarations, system requirements, release dates or ratings merely to make the profile look complete. No outreach or independent-catalog edits are included.

## Canonical domain update — 2026-10-30

The user subsequently requested migration to **`https://glob2.online/`** everywhere and redirects from the former domain. Use the new hostname for future listing edits; the [Snap upload fields](../assets/storefront-approved-v1/snap/listing-fields.json) have been updated. The old-domain URLs in the dated live-verification entries below preserve what was actually observed before migration. They are not the current paste source or evidence that a live listing has migrated. Track source changes, external listing saves and redirects separately in the [domain migration ledger](domain-migration.md).

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
| Maintained game-store metadata | Complete | [Game PR #1281](https://github.com/Globulation2/glob2/pull/1281) merged as `7038776f3fb84f43cacd51ff02e3c4d1aac4a331`. Snap, AppStream and maintained iOS/Windows/Amazon copy use the approved message; desktop/Mac guides link the canonical pack. [PR #1282](https://github.com/Globulation2/glob2/pull/1282), merged as `d3c99619f949b273302e4bf945f1977c4ddc808f`, aligns Android full text with the final Play revision. |
| Snap-specific exports | Complete | [Four sub-2 MB JPEGs, exact listing fields and a reviewed 3:1 banner](../assets/storefront-approved-v1/snap/README.md), committed as `f1d6af4`; all four gallery images and the banner uploaded and publicly verified. |
| Shared mobile-store promotional art | Complete | [1024×500 promotional PNG](../assets/storefront-approved-v1/mobile-promo/README.md), committed as `54bab83`, reviewed and uploaded to the Amazon promotional-image field. It is not a gameplay screenshot or app icon. |
| Exact storefront/account inventory | In progress | Snap, Google Play, Microsoft and Amazon authenticated access verified. Apple access is being rechecked; Epic sign-in remains incomplete; SourceForge recovery remains pending without credentials. |
| Snap listing application | Complete | Approved copy, homepage, Games category, four ordered screenshots and banner are live; independently verified on the public listing and API at 18:06 Toronto / 22:06 UTC on 2026-10-30. |
| Google Play text update | Submitted; review pending | Two en-US listing text changes submitted: 47-character short description and 1046-character full description. Console shows “Changes in review”; automatic checks/platform approval pending, not publicly live verified. |
| Amazon listing application | Applied to draft | US short/full copy, six economy/map feature bullets and the reviewed promotional image saved and verified on a fresh server reopen. Existing app remains an unsubmitted “Ready to Submit” draft, not live. |
| Cross-store application | In progress | Snap is complete; Google Play text is in review; Amazon metadata is saved in an unsubmitted draft. Other storefront outcomes remain pending. |

## Destination status

| Destination | Applied source changes | Live status / next action |
| --- | --- | --- |
| Snap (`globulation2`) | `snap/snapcraft.yaml`: approved short/full description and modern homepage; AppStream gallery refreshed. | Complete: public listing/API show the approved summary, full description, `https://glob2online.com/` homepage, Games category, Colony / River / Four Squares / Lava Shield gallery and banner. Verified 18:06 Toronto on 2026-10-30; stable 0.11.2 and app icon unchanged. |
| Desktop AppStream | Approved summary/description, modern homepage and four immutable hosted screenshots; local default PNG matches the hosted colony image. | Merged upstream metadata, for downstream packaging. No Flathub listing submission or independent package-catalog edit was performed. |
| Google Play / Android | English short text remains 47 characters. Full description now matches the approved marketing body plus the original Android touchscreen sentence, 1046 display characters; repository-only technical claims removed from listing text under PR #1282. | Controlled package `org.globulation2.glob2` is in closed testing. Exactly two en-US listing text changes submitted; console shows “Changes in review”. Quick checks/Google review pending; approval and public propagation unverified. No build, track, mobile visual, policy/privacy setting or managed publishing change. |
| Apple iPhone/iPad | Maintained iOS description, subtitle and promotional text adapted; actual-device screenshot requirement retained. | App Store Connect access is being rechecked after the user resolved the account-access prerequisite. No app-listing change verified yet; mobile gallery still requires actual device captures. |
| Mac App Store | Release guide points to the approved copy, desktop gallery and key-art sources. | App Store Connect access recheck is in progress; Mac listing availability and screenshot fit remain to verify. No external listing update, build selection or release recorded. |
| Microsoft Store (`9PH4FCRMX19F`) | Maintained short/full description and feature copy updated; Windows guide links the three 2560×1440 PNG captures and source limits. | Authenticated Partner Center product editor reached for `9PH4FCRMX19F`; saved listing-change outcome still pending. Do not enlarge the 1280×720 colony source to imply a new Windows capture. |
| Amazon Appstore | Maintained Fire listing description uses the approved message; Fire-device captures and qualification requirements retained. | Applied to the existing app draft and verified by fresh server reopen: US short 164 / full 1139 characters, six economy/map feature bullets and persisted 1024×500 promotional image. “Ready to Submit” remains unsubmitted and not live. Four existing Fire screenshot IDs, Free price, DRM, APK 9050003 and release state unchanged. |
| Epic | Shared desktop setup points to the canonical approved presentation and export pack; Epic remains the first selected store. | Epic sign-in has not completed; bounded access checks continue. No product ID/editor access or external listing update established. |
| Steam / GOG / itch.io | Shared desktop setup points to the canonical approved presentation and export pack. | Exact controlled listing/console identities and current fields still to verify; no upload or live save claimed. |
| SourceForge | No external edits. | [Public project](https://sourceforge.net/projects/globulation2/) shows Login; no authenticated editor session. Historical maintainer metadata includes `genixpro`, but current control is unverified. Existing publisher sign-in via [SourceForge authentication](https://sourceforge.net/auth/) needed. |
| Independent catalogs | No external edits. | Independent wrappers and distribution-maintained catalogs are not presumed controlled storefronts. |

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

## Google Play review submission — 2026-10-30

The authenticated publishing overview for package `org.globulation2.glob2` confirmed **“Changes in review”** for exactly **two en-US store-listing text changes**. The submitted short description has **47 characters**. The full description has **1046 characters**: the approved colony/economy marketing body followed by the original sentence, “This Android edition brings the classic desktop game to touchscreens.” Automatic quick checks and Google review remain pending. Submission is not approval or a verified live listing update.

The initially saved draft was corrected before submission to omit repository-only SDL, network/account and blanket no-ad/no-purchase/no-tracking claims. [Game PR #1282](https://github.com/Globulation2/glob2/pull/1282) updates the single maintained full-description file to the submitted text so future metadata uploads do not restore that tail. This is a listing-text change, not a change to privacy declarations, policies or application behavior.

No builds, testing tracks, mobile visual assets, policy/privacy settings or managed publishing settings changed. Authenticated console proof is retained outside the public repository; no private publisher-page screenshot is committed.

## Remaining publisher access — 2026-10-30

Initial read-only checks of Microsoft Partner Center, Epic Developer Portal, Apple App Store Connect, Amazon Appstore Developer Console and SourceForge reached sign-in gates without authenticated editor access; no external listing updates occurred in that initial pass. Subsequent publisher sign-ins enabled Microsoft and Amazon editors. Amazon draft changes are now saved and verified; Microsoft editing and Apple access recheck remain in progress. Epic sign-in has not completed; SourceForge remains pending recovery without credentials.

Continue approved presentation updates only for existing controlled listings after access is established. Skip destinations without an existing listing; do not create accounts, reset SourceForge credentials or create new listings. The cross-store rollout remains in progress, with per-destination outcomes in the table above.

## Amazon saved draft — 2026-10-30

The existing **Globulation 2** Amazon app draft was saved and reopened fresh from the server. The reopen confirmed the US listing's **164-character short description**, **1139-character full description**, **six economy/map feature bullets**, and persisted remote image for the approved [1024×500 promotional graphic](../assets/storefront-approved-v1/mobile-promo/README.md). The full copy uses the approved marketing body and retains the actual existing no-ad/in-app-purchase tail unchanged; no new policy claim was introduced.

The app remains **“Ready to Submit” and unsubmitted**. This is a saved metadata draft, not a submitted review, live listing or new app release. The four existing Fire-tablet screenshot references, Free price, DRM, APK **9050003** and release state are unchanged. The promotional graphic is key art in its dedicated field, not a replacement for mobile gameplay screenshots or application icons.

Private console proof is retained outside Git. No logged-in publisher-page screenshot or private account information is committed. Completing this draft update does not complete the cross-store rollout.

## Validation and limits

The game metadata work used an isolated worktree from `afab6e9b28`, leaving the existing game checkout and its concurrent branch untouched. XML and YAML parsed; the initial Android short/full adaptation was 47/1643 characters, and iOS subtitle/promotional text is 30/164. The subsequent Play-alignment check verified exact canonical body plus the preserved Android sentence at 1046 display characters (1047 including the repository terminal newline); the 47-character short text remained byte-identical. All four hosted screenshot URLs returned HTTP 200, and the AppStream default exactly matches the local PNG bytes. `tools/release/release.py check`, all 34 package-asset tests and whitespace checks passed. No engine build was needed for presentation-only metadata changes. No mobile screenshot, application icon, game build, price or account/privacy declaration was changed.
