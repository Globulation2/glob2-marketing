# Marketing asset ledger

[Fact index](README.md) · [Repositories](repositories.md) · [Product](product.md) · [Distribution](distribution.md)

Observed **26 October 2026** by inspecting repository files and image headers/hashes. This inventories existing families and points to their maintained manifests; it does not select launch assets or establish what every external listing currently displays. Media was not copied into this repository.

## Source identities

- **G**: game source at [`c9198b854a2ea6fc16cd5524913cf96c5a80c499`](https://github.com/Globulation2/glob2/tree/c9198b854a2ea6fc16cd5524913cf96c5a80c499).
- **W**: website at [`6e391ebe93b725747827a3ed7cea78f0d0d8f7e1`](https://github.com/Globulation2/glob2-online-website/tree/6e391ebe93b725747827a3ed7cea78f0d0d8f7e1).
- **D**: design system at [`acd277710acfebf528e1fc6f653d55fdf75de4b2`](https://github.com/Globulation2/glob2-design-system/tree/acd277710acfebf528e1fc6f653d55fdf75de4b2).

## Brand and reusable visual assets

| ID | Existing family / exact paths | Evidence and recorded use | Provenance / limit |
| --- | --- | --- | --- |
| A01 | D `assets/wordmark-letters.webp`, `wordmark-two.webp` | Two alpha-mask parts colored with shared `src/css/brand.css` | D [asset guide](https://github.com/Globulation2/glob2-design-system/blob/acd277710acfebf528e1fc6f653d55fdf75de4b2/docs/assets.md) says web wordmark stays adaptable to both themes and forced colors. Not a complete store capsule/logo export set. |
| A02 | D `assets/glob-64.png`, `favicon-32.png`, `apple-touch-icon.png`, `og-colony.jpg` | Glob icon, browser/application touch icons and social-preview image | D `assets/provenance.json` records hashes and upstream game revision; actual external social card display untested. |
| A03 | D `tokens/{foundation,web,light,dark}.json`, `src/css/`, `dist/css/` | Meadow/Night colony palette, gold actions, shapes, readable type and shared components | D README and `docs/design.md`; website and app consume a pinned build revision. A local source revision does not identify the deployed revision. |
| A04 | D `assets/glob2-sans.woff2`, `nunito.woff2` and license files | Glob2 Sans headings/numbers; Nunito reading/interface text | DejaVu-derived font notice and SIL OFL Nunito notice retained; these are separate from game-art license. |
| A05 | D `assets/` building/resource/flag/unit WebPs; `assets/icons/manifest.json` and SVGs | Reusable actual game sprites; Tabler interface icons | D provenance records original game revision `6ff1ebed476f2a055ccdbe16abd737f541ffcb44`; Tabler icons retain MIT notice. |
| A06 | G `data/icons/`, `mobile/ios/Assets.xcassets/AppIcon.appiconset/`, Android icon resource, fastlane icon | Native/mobile/platform icon families | Native icon variants exist independently of website favicons. Store publication and alignment were not established. |
| A07 | G `datasrc/gfx/`, `datasrc/gfx/production/`, `data/gfx/`, `data/highres/` | Preserved originals, reviewed production inputs, runtime sprites, high-resolution art | [Artwork workflow](https://github.com/Globulation2/glob2/blob/c9198b854a2ea6fc16cd5524913cf96c5a80c499/docs/assets/artwork-workflow.md), `datasrc/gfx/README.md`, generated `docs/assets/high-resolution/ASSET-PROVENANCE.md`. Originals, procedural assets, AI candidates and approved runtime art are distinct. |

## Screenshots, recordings and educational media

| ID | Existing family / path | Recorded dimensions or context | Status and evidence |
| --- | --- | --- | --- |
| A08 | G `data/screenshots/globulation2-gameplay.png`; W `public/images/globulation2-gameplay.png` | Both 1280 × 720; byte-identical SHA-256 `6430a4a8da5955525609096ade3fa269904aecb4558dafb4447048f3253f1312` | Confirmed duplicate by local hashing. G AppStream XML points at an older immutable game revision for this filename. This proves shared bytes across these local paths, not use across every store. |
| A09 | W `public/images/globulation2-match.png` and `.webp`; `globulation2-gameplay.webp` | Match PNG 1000 × 562; alternate web derivatives | Files exist; source/capture history for all older images was not established in this audit. |
| A10 | W `public/images/glob2-first-colony.webp`, `glob2-tutorial.webp`, `glob2-exploration-flag.webp` | First-colony WebP 1280 × 608; tutorial/HUD and exploration examples | W [content verification](https://github.com/Globulation2/glob2-online-website/blob/6e391ebe93b725747827a3ed7cea78f0d0d8f7e1/docs/website-content-verification.md) records public browser-game captures on 9 October, displayed version 0.11.0.0, exact counters and caption limits. |
| A11 | W `public/images/home-thriving-colony.webp`, `home-colony-defence.webp`, `home-rival-expansion.webp` | 1280 × 720 crops derived from 1408 × 792 captures; replay tick 41350 | Same verification doc records 11 October capture from four-colony Fingerprint/Quick clash replay with fog of war disabled and HUD cropped. They are replay views, not ordinary live-player visibility. |
| A12 | G `fastlane/metadata/android/en-US/images/phoneScreenshots/{1,2}.png` | Both 320 × 640 portrait; SHA-256 respectively `a53420ea3d5b2454222c0e80eb088b9ac1ae87b7601e69a628df348b59690e4e`, `9189b78d5f80cb786790334853fc9381aa0eba0a97db8de50342559e91d35915` | Distinct local assets from landscape website/AppStream images. Their physical-device provenance and currently displayed store versions are unverified. |
| A13 | D `assets/colony-loop.mp4`, `colony-960.webp`, `colony-1600.webp`, `colony.webp` | Silent actual main-menu colony simulation without UI; MP4 6,831,278 bytes | D asset guide, hash provenance and G `tools/record_menu_colony.py`. MP4 SHA-256 `f898edeb338efca294c1e12d1c7291c36c04f138906c5a123c2748751db28745`; static posters accompany the recording. |
| A14 | W `src/data/guide-media.json`; public `/guide-media/v1/<chapter>/` storage URLs | **237 manifest entries: 223 images, 14 videos across 26 chapters** | Counted from source JSON, not a fresh URL availability check. Entries retain URL/path, SHA-256, bytes, dimensions, caption/alt and video poster/rate metadata where applicable. Complete individual ledger already exists upstream. |
| A15 | W `scripts/capture-home-shots.mjs`, handbook scripts; G `tools/record_menu_colony.py`, `docs/features/gameplay-recording.md` | Capture/reproduction machinery, MP4 recording and chapter/event extraction | Source capability; no new capture or device qualification performed here. Ignored `artifacts/` and test-results directories are evidence workspaces, not approved published asset catalogs. |

A14 chapter coverage: getting-started 17; controls-and-hud 5; resources-and-hauling 9; jobs-and-flags 4; sustainable-food 8; population-and-production 8; buildings-and-services 7; training-and-upgrades 11; exploration-and-movement 5; reference-controls 2; recovering-your-colony 2; defending-your-colony 6; victory-and-rules 5; organizing-an-attack 14; browser-and-multiplayer 4; fruit-and-conversion 12; economy-and-expansion 10; choosing-an-ai 8; ai-numbi 8; ai-castor 13; ai-econo 11; ai-warrush 12; ai-cortex 13; ai-cabino 12; ai-nicowar 15; ai-maxima 16.

## Written assets and existing message variants

| ID | Source | Observed language / role |
| --- | --- | --- |
| A16 | W `src/data/marketing.ts` | Homepage: “Build a colony. Decide where the work goes.” Free, open-source RTS; buildings/flags, autonomous routes and needs; tutorial-first introduction. Game page explains indirect control, food/training and rival colonies. |
| A17 | W `src/data/site.ts` | Tagline: “A free, open-source real-time strategy game about managing the work of a colony.” |
| A18 | G `data/org.globulation2.Globulation2.metainfo.xml`, `snap/snapcraft.yaml`, Android `short_description.txt` | “Real time strategy with automatic unit task assignment”; AppStream/Snap homepage still points to globulation2.org. |
| A19 | G `fastlane/metadata/android/en-US/full_description.txt` | Colony/resources/AI/editor, cross-platform online play, guest start, campaign/LAN without account; ends with no ads, in-app purchases or analytics/tracking. This is stored copy, not a fresh verification of each claim. Optional web payment and app analytics source documented in [product](product.md) has a different scope requiring eventual reconciliation. |
| A20 | G `docs/releases/ios-app-store.md`, `mac-app-store.md`, `windows-store.md`, `gog-release.md` | Existing platform-specific listing/asset guidance and submission procedures. Microsoft guide names first-colony image as approved source; not proof uploaded assets match. |
| A21 | W `src/content/guides/`, history/news/archive, migration manifest | Existing tutorial, reference, AI-opponent, history and archive content; source/revision and article-media evidence are reusable knowledge assets, subject to rights and currency limits. |

The above documents concrete differences in wording, aspect ratios, capture contexts and source locations. It does **not** establish that every difference is erroneous or that a particular family should be selected.

## Sound, authored content and licensing

G `data/zik/` contains soundtrack sets; `docs/assets/source-attribution.md` identifies original music by Jacques-Paul Grivaz; externally licensed Woodland, Apple Cider and Curious Critters; original rendered sets; and disclosed AI-generated Orchestral Dawn. Exact source/credit/license notices remain per set. G `docs/assets/music-pipeline.md`, `music-packages.md` and `music-style-guide.md` document production and shareable community packages.

Game art is described as GPL-3.0-or-later by the shared design system; font, icon, third-party source and individual music notices remain authoritative. AI-generated artwork/audio exists and is disclosed in upstream provenance. A GPL game license does not establish permission to republish every legacy wiki article/image; W `content/migration-manifest.json` preserves unresolved rights and original history links. No separate press-kit archive, approved cross-store screenshot manifest, campaign trailer master, social-banner master set, or unified copy-by-platform ledger was identified in the inspected paths; absence here is a discovery gap, not proof none exists elsewhere.

## Unverified follow-up records

- Actual screenshots/capsules/icons and copy currently displayed on every store, directory and social profile.
- Account ownership, access, author approvals and rights for externally held assets.
- Capture game/build identity, renderer, device, rules, camera and disclosure metadata for older screenshots and Android portrait captures.
- Deployed design-system revision and whether every consumer/listing uses its current brand assets.
- Full raw-artifact archive and historic branding evolution; this ledger intentionally references maintained source catalogs instead of duplicating them.
