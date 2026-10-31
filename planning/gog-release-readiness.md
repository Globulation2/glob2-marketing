# GOG release readiness

[Planning index](README.md) · [Publishing ledger](approved-storefront-rollout.md) · [Application evidence](../facts/distribution.md#gog-application-follow-up--2026-10-31)

## Current state — 2026-10-31

Approved English copy and core product art are prepared and locally reviewed. Released-payload package checks now pass for Windows, Mac arm64, Mac x86_64 and Linux, including native CI smoke/preservation checks; this is not full gameplay QA or GOG acceptance. Linux added-runtime source-delivery review remains open. See [actual outputs and limits](#linux-candidate-package-checks-completed--2026-10-31).

The September 30 application/detail correction remain recorded. The user subsequently clarified that **GOG approval is pending and no publisher/store account has been provided yet**; this is user-reported status, not independently verified rejection. Stop login attempts pending acceptance/invitation; no password-login workaround or new-account creation is needed. Product IDs, Staging/QA submission and Live remain unverified. Prepared copy/art/package outputs are retained; Linux dependency source delivery, Mac architecture delivery mapping and trailer/product fields remain independent follow-ups.

## Existing-account authentication checkpoint — 2026-10-31

The user authorized an alternate Google-account attempt and browser coordination. Google SSO automatically selected another current identity and routed to new-account registration; execution stopped before creating an account. Normal existing-account **GOG Log in** was handed to the user. No company/product access, accepted onboarding, account creation, signup or security-setting change was verified. The user subsequently completed manual authentication preparation and asked for a recheck. The chooser offered the authorized application identity; selection succeeded, but GOG returned **Complete Sign Up**, indicating no linked existing GOG account for that Google identity in this flow. Execution again stopped before account creation or legal changes. This does not establish that no password-based GOG account exists or that the application was rejected. Accepted onboarding/invitation and company/product access remain unverified; no new external contact or submission occurred. Personal addresses and private authentication URLs are excluded from this record.

The user then clarified that no publisher/store account exists yet because approval is pending. That clarification supersedes the earlier login handoff as the current action: **stop authentication attempts and await acceptance/invitation**. Do not interpret the registration screens as application rejection or pursue an account-creation/password workaround. No external contact/account action followed this clarification.

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

## Released-payload build-only checkpoint — 2026-10-31

[Game PR #1299](https://github.com/Globulation2/glob2/pull/1299) merged as `d2b20d330c86d031b717b5d72df5e30d84841b3c`, following 23 focused tests and Python/YAML/whitespace checks. The new credential-free reuse route pins released v0.11.4.0 source `a766230578dede730be43919240c5c80fafb44fe` and four original asset SHA-256s. Its intended packaging preserves Windows payload bytes and signed/notarized Mac apps, separates Mac architectures, and resolves Linux dependency/license provenance; actual output and native gates remain to verify. Reuse mode rejects Staging uploads.

The normal release-mirror merge `f72ceca5541b6ac79fa58f661528771985bf9d08` retains both histories and has the exact reviewed public tree `a54eb9698cff5b78150e455ec5c415b2d651e5c0`. [Run 41220221276](https://github.com/genixpro/glob2-release/actions/runs/41220221276) was dispatched with `tag=v0.11.4.0`, `mode=build`, `platforms=all`, `reuse_released_payload=true`. This records a dispatch, **not completed candidates, successful native qualification or an upload**. No GOG credentials/product IDs/builder hash are verified; no source rebuild or GOG submission is claimed.

## Partial candidate results and Linux retry — 2026-10-31

[Run 41220221276](https://github.com/genixpro/glob2-release/actions/runs/41220221276) completed with overall failure **only in Linux**, where the packaging environment lacked existing `libva.so.2` and `libva-drm.so.2` dependencies. Windows, Mac arm64 and Mac x86_64 jobs succeeded, including native payload preservation, archive roundtrip and smoke checks. Retained outputs:

| Depot | GitHub artifact ID | Bytes | GitHub API artifact SHA-256 |
| --- | --- | --- | --- |
| Windows | `13049293985` | 178,920,545 | `7bc8b68f34b762b345ddb2983e90f8d8648cba9d04e8c4fa738ff378aae703ca` |
| Mac arm64 | `13049837290` | 170,893,887 | `d942426cbbfe4e6f8668a3cefb1fd0b73c1631e67f15cef390d35309dd684f5d` |
| Mac x86_64 | `13049573136` | 173,102,350 | `d2e7fb07b0e14546a273d3970069ad28c75bbc15c2dd451bb0126872ab9948bc` |

All three artifact containers currently expire **2027-01-29 16:33:05 UTC**; none has been downloaded or published as a public release by this record. These are **GitHub API artifact digests**, not hashes of an inner depot archive. Native CI smoke/preservation checks do not establish GOG offline-installer delivery, full gameplay qualification, Staging or platform QA acceptance.

[PR #1300](https://github.com/Globulation2/glob2/pull/1300), the narrow packaging dependency-list fix, merged as `5793d3f242bc35fd67d0e9d2844e3a653b50a7c0`. Normal mirror merge `070f2d642fedef6535133a0fbdb2729b70defd95` matches reviewed public tree `62321cd9ef3a71e4f19528534ebf4162bab241ff`. Corrected **Linux-only build** [run 41220918563](https://github.com/genixpro/glob2-release/actions/runs/41220918563) had verified workflow head `070f2d642fedef6535133a0fbdb2729b70defd95` and passed preflight, then failed only while parsing the sentence period after an actual GPL-notice path. This attempt is superseded by the completed retry below. Released payload/source `a766230578dede730be43919240c5c80fafb44fe` is unchanged. No upload, GOG offline installer, QA submission or Live result is claimed.

## Linux candidate package checks completed — 2026-10-31

The notice-path parser correction [PR #1301](https://github.com/Globulation2/glob2/pull/1301) merged after **24 focused tests**, without changing the notices. Normal workflow-mirror merge `3e3c3546b2dfbace0dc2a3f2a5bbcb3d1002681b` matches public commit `0abe90bbb9d83e94841eb0202b1d83ebd0d66eee`, tree `ee398c007443b113bb1e148f6528cb8e6a8bd7d6`. Linux-only [run 41221438076](https://github.com/genixpro/glob2-release/actions/runs/41221438076) completed **Success**, including local depot assembly and a fresh pinned Ubuntu 22.04 desktop-baseline offline fixture of **10 ticks**. This is bounded CI evidence, not full gameplay QA.

- Retained GitHub artifact `13050027417`: **174,506,498 bytes**, API container SHA-256 `27596f0cf5179437cabd5e143fa771635541e79f899c909faedadb632eca4867`, expires **2027-01-29 16:48:23 UTC**.
- Independently read inner tar: **174,686,010 bytes**, SHA-256 `6e3c3af6bb494410c52d4a32546ff9dceed3be0379984b68fdc3ead200a7639a`. This is a distinct inner-archive hash, not the API digest.
- Original released asset SHA-256 `c5a7544ee2d818e4eac501875c64a4721bd9163e5bfdfa54fddcb93aae5fd0db` and source `a766230578dede730be43919240c5c80fafb44fe` remain unchanged. Provenance checks matched all **18 added Ubuntu runtime library hashes**, actual copyright files and common-license hashes; **22 libraries total: four original private runtimes plus 18 Ubuntu libraries**.

**Source-delivery follow-up remains open:** output explicitly records `runtime_licence_review_required=true`. `SOURCE.txt` links Glob2 source only; no corresponding-source archive or verified compliant source offer for the added Ubuntu runtime dependencies has been prepared. FriBidi's notice includes LGPL 2.1; mixed source-package notices do not establish blanket licensing of every shipped binary. Preserve exact provenance/notices and resolve applicable dependency source-delivery obligations before treating this depot as release-ready. These checks are not rights certification.

All platform package checks now have successful outputs, but accepted GOG access/IDs, Mac architecture-to-product delivery mapping, trailer/product declarations and the source-delivery follow-up remain unresolved. No GOG upload, offline installer, QA submission or Live release is claimed.

## Product declarations evidence — 2026-10-31

This matrix uses immutable **v0.11.4.0 source `a766230578dede730be43919240c5c80fafb44fe`** as evidence, not older store-build declarations. The separately owned GOG candidate must supply actual package identity and qualification before these become portal promises.

| Field | Evidence available | Ready statement / unresolved limit |
| --- | --- | --- |
| Version / platform scope | [Tagged release](https://github.com/Globulation2/glob2/releases/tag/v0.11.4.0), [tagged GOG workflow](https://github.com/Globulation2/glob2/blob/a766230578dede730be43919240c5c80fafb44fe/.github/workflows/gog-staging.yml) targets Windows, Linux and macOS depots. | Intended three-platform candidate scope, not proof all depots built or tested. Record each actual candidate's source/architecture/manifest before enabling its store platform. |
| System requirements | [Tagged release workflow](https://github.com/Globulation2/glob2/blob/a766230578dede730be43919240c5c80fafb44fe/.github/workflows/release.yml) specifies Windows x86_64, Ubuntu 22.04 x86_64 output and macOS arm64/x86_64 builds with deployment target 15.0. | Build targets are not measured minimum requirements. Do not infer Windows minimum OS from runner OS, support every Linux distribution, transfer the macOS floor to a different candidate, or invent CPU/RAM/GPU/disk figures. Obtain final GOG payload architecture/deployment/dependency evidence and observed install footprint. |
| Languages | [Tagged translation registry](https://github.com/Globulation2/glob2/blob/a766230578dede730be43919240c5c80fafb44fe/data/texts.list.txt) lists English and additional game-text resources. | Translation-file presence is not complete localization, verified font/rendering or tested runtime language support. Record the actual depot's bundled resources and language-menu checks before selecting supported languages. Store-copy translations are a separate catalog and do not establish game localization. |
| Price / release designation | [Tagged GOG guide](https://github.com/Globulation2/glob2/blob/a766230578dede730be43919240c5c80fafb44fe/docs/releases/gog-release.md) records the intended free, DRM-free initial listing and says to confirm whether GOG accepts Early Access/beta. | Free is the historical project request/intention, not an observed GOG price configuration or accepted designation. No discount, release date or Early Access selection invented. |
| Rights / legal lines | [GPLv3 license text](https://github.com/Globulation2/glob2/blob/a766230578dede730be43919240c5c80fafb44fe/COPYING), [image-codec notices](https://github.com/Globulation2/glob2/blob/a766230578dede730be43919240c5c80fafb44fe/data/image-codec-licenses.txt), [Woodland CC-BY attribution](https://github.com/Globulation2/glob2/blob/a766230578dede730be43919240c5c80fafb44fe/data/zik/woodland/LICENSE.txt) and approved-art provenance provide concrete notice sources. | Preserve exact candidate third-party notices and corresponding-source delivery. These examples are not a complete rights audit or authority to sign a publisher warranty. Developer/publisher legal identity and final legal line remain portal/account dependent. |
| Ratings / territory / Galaxy features | No current GOG rating record, approved territory configuration or product-specific feature declaration verified. | Do not transplant another storefront's ratings, country exclusions, multiplayer/cloud-save or achievement declarations. Use actual certificates/IARC acceptance, selected candidate and GOG fields; SDK presence is not a promise of an integrated feature. |

The public-trailer gap remains as recorded above. This evidence preparation changes no publisher declarations, prices, ratings, accounts or releases.

## Remaining work and ownership

| Work | Owner / next evidence | Status |
| --- | --- | --- |
| Onboarding/access | Await acceptance/invitation for the submitted application; user reports approval pending/no publisher account. Login attempts stopped; no workaround/account creation | Pending approval; no independent rejection finding |
| Copy | Transfer approved blocks into actual portal fields, inspect limits and save/reload | Prepared locally, not applied |
| Graphics | Official ZIP/artboards/embedded guides inspected; core approved-source derivatives and genuine layered PSDs prepared and visually reviewed | Complete locally; portal acceptance unverified |
| Layered art / trailer | Layered product/key art prepared with genuine raster layers and disclosed native origins; confirm actual delivery acceptance. Public trailer remains absent | Layered exports reviewed; trailer/portal gaps remain |
| Candidate and QA | Build worker qualifies immutable source, DRM-free platform payloads and depot IDs, then protected Staging upload when configured | [All platform package checks passed](#linux-candidate-package-checks-completed--2026-10-31); bounded CI smoke only. Mac delivery mapping/dependency source delivery remain open; no GOG upload/offline installer/QA |
| Product declarations / source delivery | Verify product fields and exact Linux dependency obligations; current SOURCE.txt covers Glob2 only, added-runtime source archive/offer not prepared | Unresolved; runtime_licence_review_required remains true |
| Release | GOG QA/approval and actual branch/publication outcome | Not submitted or live |

No contact, fees, agreements, legal/rating declarations or external listing edits were made by this preparation unit.
