# GOG release readiness

[Planning index](README.md) · [Publishing ledger](approved-storefront-rollout.md) · [Application evidence](../facts/distribution.md#gog-application-follow-up--2026-10-31)

## Current state — 2026-10-31

The user requested getting GOG ready for release. The September 30 application and subsequent detail correction are recorded; accepted partnership, publisher-portal access, product IDs, Staging upload, GOG QA submission and Live availability remain unverified. The current portal attempt remains at Login, with no publisher company reached. The scoped connected-mail check found no new late-October response; the separate publisher-contact inbox remains unverified. No new application or external message was sent.

Three-platform depot/pipeline tooling exists in the [public release guide](https://github.com/Globulation2/glob2/blob/6a16670c6daafa34f1f86a47014f23e0d05fd4e3/docs/releases/gog-release.md) and [workflow](https://github.com/Globulation2/glob2/blob/6a16670c6daafa34f1f86a47014f23e0d05fd4e3/.github/workflows/gog-staging.yml). Prepared tooling is not a qualified candidate, configured publisher account or completed submission. The build worker owns source/workflow improvements separately.

## English copy ready to transfer

The following reproduces the [approved presentation](approved-storefront-rollout.md#approved-copy). These are logical copy blocks, not claims about unverified GOG field limits. Product title: **Globulation 2**. Website: **https://glob2.online/**. Use the portal's actual taxonomy for Strategy / Real-Time Strategy and Colony building / Resource management.

### Headline

Build a thriving colony in contested territory.

### Short pitch

Build a thriving colony in contested territory. Balance food, workers and expansion, shape a sprawling base, and compete with rival colonies for land and resources.

### About

Food, workers and space shape your expansion. Grow a sprawling colony, balance its competing needs, and contend with rivals for land and resources. Your creatures act autonomously, letting you guide the colony as a whole.

**Grow an economy that can sustain your ambitions.**

Food, construction and training compete for your workforce. Decide where workers are needed and balance new ambitions with the needs of the colony you already have.

**Make the map part of your strategy.**

Different maps call for different strategies. Adapt your expansion to the terrain, choose what to defend, and find the routes and resources your colony needs.

**Defend what you've built.**

Your economy supports both growth and defense. Balance the needs of your colony while rivals compete for land and resources, and prepare for conflicts that can decide the match.

**Free and open source.**

A strategy game to play, explore and help shape.

“Free and open source” is approved descriptive copy, not a verified GOG price configuration or complete rights declaration. Do not invent publisher/legal lines, supported-language promises, release dates or ratings from marketing text.

## Approved asset handoff

| Slot / order | Source | Readiness and limits |
| --- | --- | --- |
| Key art | [Landscape 2560×1440](../assets/epic-v5/offer-landscape-2560x1440.png) | Approved promotional illustration, not gameplay. [Source provenance](../assets/epic-v5/README.md). |
| Logo | [Transparent wordmark 960×540](../assets/epic-v5/product-logo-960x540.png) | Approved original; preserve proportions. Smaller native dimensions must be disclosed if placed on a larger canvas. |
| Screenshot 1: colony | [1280×720 PNG](../assets/storefront-approved-v1/01-colony.png) | Approved actual Fingerprint replay; do not claim native 1920 capture. |
| Screenshot 2: battle | [2560×1440 PNG](../assets/storefront-approved-v1/02-river-battle.png) | Approved staged native River combat. |
| Screenshot 3: strategy | [2560×1440 PNG](../assets/storefront-approved-v1/03-four-squares-strategic.png) | Approved developed Four Squares AI match. |
| Screenshot 4: terrain | [2560×1440 PNG](../assets/storefront-approved-v1/04-lava-shield-terrain.png) | Approved staged Lava Shield terrain in use. |
| Layered delivery | [Existing compositing script and source family](../assets/epic-v5/build-assets.py) | [Reviewed GOG layered derivatives](../assets/storefront-approved-v1/gog/README.md) now separate background/shadow/original-wordmark raster layers. The colony composite remains flattened and resampling is disclosed; no editable original scene/vector claim. |
| Trailer | None prepared in the approved kit | Private Apple review clips are not an approved public GOG trailer. No new footage prepared or reused. |

See the [desktop source manifest](../assets/storefront-approved-v1/README.md) for capture provenance. Only approved images or direct technical derivatives may be introduced. Keep gameplay frames separate from key art. [Reviewed GOG product-format adapters](../assets/storefront-approved-v1/gog/README.md) now provide technical crops/layouts and layered delivery; no new imagery was created.

## Official requirements and their scope

Observed **2026-10-31**. The [GOG Essentials Checklist](https://docs.gog.com/basic-game-assets/) directs asset delivery through Assets Manager. Its unitalicized store-page checklist requests template/render-tool graphics, layered high-resolution key art/logo (minimum 1920×1080), description, requirements, languages, screenshots, a trailer with GOG end slate, tags, legal lines and applicable ratings/restrictions. These are documented delivery requests; exact portal enforcement and permitted exceptions are unverified without access.

DRM-free release candidates are requested for supported operating systems. Galaxy SDK is explicitly optional; achievement instructions and cloud-save paths are conditional on those features. Extras apply when relevant. Launch timing/pricing must be agreed/configured, not fabricated. Keep prior DevPortal builds. Postlaunch promotion guidance is not evidence of a pre-submission technical gate. [Official checklist](https://docs.gog.com/basic-game-assets/).

[Official graphics templates](https://items.gog.com/templates/gog_art_assets.zip) are inspected below; safe-area and file-delivery details still require guide/portal checks. Consumer Galaxy custom-library artwork sizes are not publisher-store specifications. [Early Access](https://docs.gog.com/games-in-development/) is a separate designation to resolve with GOG; a version number alone does not select it.

## Official template inspection — 2026-10-31

Downloaded the [official ZIP](https://items.gog.com/templates/gog_art_assets.zip) to temporary storage: **178,489,651 bytes**, SHA-256 `50222fd566382488f2b7888ece1c0ae5596bf84d73b86600be229a587c9a2468`. Read its instruction PDF and PSD metadata without executing content. The archive contains product, promotional, social and icon PSD sheets. The following dimensions come from **artboard descriptors**, not overall sheet canvases or painted-layer bounds.

| Product artboard | Width × height | Proposed treatment / qualification |
| --- | --- | --- |
| `prod_main_banner` | 1600×740 | Approved pre-title colony composite with separately positioned approved wordmark; guide fit still to inspect. |
| `prod_logo` | 1600×740 | Transparent canvas; preserve original wordmark proportions and disclose any resampling. |
| `prod_box` | 342×482 | Approved portrait composition adapted without losing title or colony; visual review required. |
| `prod_galaxy_background` | 2560×670 | Approved pre-title art crop; no new content. |
| `prod_bg` | 2560×655 | Distinct actual artboard height; not interchangeable with the 670-pixel background. |
| `prod_web_icon` | 98×98 | Existing compiled icon preserved; no replacement export currently assigned. |
| `prod_demo_box` | 342×482 | Demo-specific; no demo product selected, so not automatically needed. |

The instruction PDF identifies green boards as editable, requires transparent logos within the safe area, and says to hide crop/cover/safe-space guides before export. Mockup boards must not be exported. Embedded PSBs were subsequently inspected visually: main art and cover carry centered-title/corner-caution placeholders; the logo PSB is empty, with no numerical safe-margin specification. The prepared derivatives were reviewed against these guides.

The other sheets contain campaign/PR formats, not proof every slot is mandatory for this product: promotional Galaxy banner 1540×270, product card 1540×404, desktop 2560×423, mobile 767×472, spot 444×740, navbar 747×550/logo 285×170 and takeover desktop 2560×360/mobile 960×570/logo 454×200; social square 1200×1200, Twitter 1200×675, Facebook 1200×630 and news 1550×490. Request the actually applicable slots through the accepted product/Assets Manager rather than treating all campaign formats as launch blockers.

Icon-template names and some artboard bounds differ (for example, a board named `icon_128` measures 125×125); these are not grounds to modify the application icon or infer its required delivery sizes. Product/portal specifics remain unresolved. The inspected ZIP/templates are not redistributed in this public repository.

**Core asset unit complete locally:** [six PNGs, three genuine layered PSDs, reproducible script and manifest](../assets/storefront-approved-v1/gog/README.md). Coordinating visual review confirmed centered title fit, retained colony imagery and no guide/mockup leakage. PSDs reopen with three raster layers, correct dimensions and at most one RGB code-value recomposition difference from alpha rounding. Higher-resolution canvases resample the disclosed 1672×941 background and 900×131 wordmark; they do not create native detail. No icon replacement, demo/campaign export, public trailer, portal upload or acceptance is claimed.

## Remaining work and ownership

| Work | Owner / next evidence | Status |
| --- | --- | --- |
| Onboarding/access | Reconcile actual acceptance/invitation and controlled product identity; existing application only, no duplicate submission | Unresolved |
| Copy | Transfer approved blocks into actual portal fields, inspect limits and save/reload | Prepared locally, not applied |
| Graphics | Official ZIP/artboards/embedded guides inspected; core approved-source derivatives and genuine layered PSDs prepared and visually reviewed | Complete locally; portal acceptance unverified |
| Layered art / trailer | Layered product/key art prepared with genuine raster layers and disclosed native origins; confirm actual delivery acceptance. Public trailer remains absent | Layered exports reviewed; trailer/portal gaps remain |
| Candidate and QA | Build worker qualifies immutable source, DRM-free platform payloads and depot IDs, then protected Staging upload when configured | Tooling exists; no completed GOG candidate/upload claimed |
| Product declarations | Verify developer/publisher, requirements/languages, rights, ratings/territories and price from current artifact/account evidence | Not filled with assumptions |
| Release | GOG QA/approval and actual branch/publication outcome | Not submitted or live |

No contact, fees, agreements, legal/rating declarations or external listing edits were made by this preparation unit.
