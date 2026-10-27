# Store assets v1

[Planning index](README.md) · [Store profile draft](store-profile-v1.md) · [Agreed positioning](../analysis/positioning-v1.md) · [Asset ledger](../facts/assets.md) · [Public image audit](../facts/platform-audit.md)

**Current preparation, 2026-10-26:** Epic Games Store is first. Use the [Epic profile](epic-store-profile-v1.md), [verified requirements](epic-store-requirements.md) and [current illustrated artwork](../assets/epic-v5/README.md). The working covers combine a generated environment with actual source units and the existing title. The genuine gameplay gallery remains separate. The first artwork pack and subsequent character/screenshot studies remain historical; no artwork is user-approved or uploaded. This reusable brief remains source material for later stores.

Prepared **2026-10-26** for the working launch positioning: **“Build a thriving colony in contested territory.”** This is an asset selection and capture brief, not a finished export pack. Existing candidates below were documented in the dated asset inventory/public audit; no new captures, rights clearance, platform uploads or live changes were performed here.

## Small first pack

Prepare one wordmark, one square icon, one cover composition and five gameplay images. Lead with a functioning colony and its economy; show spatial decisions next, with combat supplying pressure rather than dominating the gallery. Use the same named launch build and visual treatment for fresh captures. Platform-specific dimensions, device families and upload formats follow once the first storefront is identified; the measurements below describe existing files, not store requirements.

## Existing source candidates

Paths beginning W refer to the website repository, D to the design-system repository, and G to the game repository. Their immutable revisions and provenance are recorded in the [asset ledger](../facts/assets.md#source-identities).

| Role | Exact candidate | Why it fits / preparation remaining |
| --- | --- | --- |
| Wordmark | D `assets/wordmark-letters.webp` + `assets/wordmark-two.webp` ([A01](../facts/assets.md#brand-and-reusable-visual-assets)) | Existing brand components. Assemble using the maintained brand styling; these alpha-mask parts are not already a complete store logo export. Check legibility at the actual placement size. |
| Square icon | D `assets/glob-64.png`; G `data/icons/` and native app icon families ([A02/A06](../facts/assets.md#brand-and-reusable-visual-assets)) | Use the glob identity already associated with the project. Select an original with enough resolution from the native family; do not enlarge the 64px web file into a store master. Exact platform variant remains to be chosen. |
| Cover composition | W `public/images/home-thriving-colony.webp` + assembled wordmark ([A11](../facts/assets.md#screenshots-recordings-and-educational-media), public image W-01 in the [audit](../facts/platform-audit.md#exact-inspected-image-register)) | Strong provisional colony scene: 1280×720, food fields, buildings and many units. It is a replay view with fog disabled and HUD cropped. Check the selected store permits this presentation; prefer a matched fresh capture for the final pack. No capsule/cover master exists in this brief. |
| Genuine interface/control example | W `public/images/glob2-first-colony.webp`, `glob2-tutorial.webp`, `glob2-exploration-flag.webp` ([A10](../facts/assets.md#screenshots-recordings-and-educational-media)) | Browser captures documented on 2026-10-09, displayed version 0.11.0.0. First-colony image is 1280×608. Inspect the original HUD/crop against the intended launch edition; useful reference for fresh controls/economy shots. |
| Territory and rival-pressure references | W `public/images/home-rival-expansion.webp`, `home-colony-defence.webp` ([A11](../facts/assets.md#screenshots-recordings-and-educational-media), audit W-03/W-02) | Existing 1280×720 replay crops show adjacent colonies/flags and a defended colony. Capture record: 2026-10-11, four-colony Fingerprint/Quick clash replay, tick 41350, fog disabled and outer HUD cropped. Keep that disclosure when reused. |
| Optional motion/background | D `assets/colony-loop.mp4`, with `colony-1600.webp` poster ([A13](../facts/assets.md#screenshots-recordings-and-educational-media)) | Actual main-menu colony simulation, not a recorded player match. Suitable only where that context is clear; it does not demonstrate combat, player decisions or gameplay controls. Defer a trailer until the still-image pack is coherent. |

## Five-image story and draft captions

These are proposed shot objectives and captions, not claims that all five final images already exist. Caption only what the selected frame actually demonstrates. Preserve clean originals; add captions through the storefront when available rather than baking promotional text into gameplay screenshots.

| Order | What the image should show | Draft caption | Source / work needed |
| --- | --- | --- | --- |
| 1 — Colony | A substantial, readable colony with food, buildings and active workers in one view. | “Grow a thriving colony.” | Existing W `home-thriving-colony.webp` is a provisional composition/reference. Fresh launch-build player-view capture preferred; retain replay disclosure if using the existing file. |
| 2 — Economy | Food supply and competing work needs, with enough HUD context to make the player's economic decisions legible. | “Balance food, workers and the needs of a growing colony.” | **Fresh capture needed.** A10 tutorial images and [guide-media chapters](../facts/assets.md#screenshots-recordings-and-educational-media) on sustainable food, resources/hauling and population/production provide references, not a selected finished shot. |
| 3 — Space | A base edge or expansion route where terrain, resources and a rival's presence make location meaningful. | “Choose where to build and where to expand.” | Existing W `home-rival-expansion.webp` is a replay reference. Fresh player-view capture needed to show a clear spatial decision without implying the player sees through fog. |
| 4 — Colony control | A selected building's worker demand or a flag, with autonomous creatures visible in the surrounding colony. | “Guide the colony as a whole.” | A10 tutorial/exploration captures are candidates to inspect. **Fresh capture needed** if their build, interface or crop does not match the launch edition. A still should not claim to prove a before/after worker response. |
| 5 — Rival pressure | A defended colony or contested edge with both the settlement and threat readable. | “Defend what you've built.” | Existing W `home-colony-defence.webp` is a replay reference. Fresh matching capture preferred. Keep economy/base context in frame rather than ending with an unrelated wall of combat. |

The first pack needs these five roles, not five separate scenarios or a cinematic production. One well-chosen match may supply several shots. Do not manufacture a scene or hide a material experimental/debug setting to imply ordinary gameplay.

## Capture and provenance handoff

For each final image retain: original file, source repository/revision or capture build, edition/device, scenario/map and rules, player/replay/menu context, fog/HUD settings, capture date, crop/export details and rights/credit source. Keep any private accounts, names or notifications out of frame. The [website capture verification](https://github.com/Globulation2/glob2-online-website/blob/6e391ebe93b725747827a3ed7cea78f0d0d8f7e1/docs/website-content-verification.md) is the existing provenance reference; [A15](../facts/assets.md#screenshots-recordings-and-educational-media) records capture machinery.

The design system's `assets/provenance.json`, artwork workflow and individual notices remain authoritative. Game art is described as GPL-3.0-or-later in the inventory; fonts, icons, music and third-party sources carry separate notices. Asset existence or public display is not a completed usage-rights review. Preserve font notices when exporting with the existing brand typography. Do not pull legacy wiki/catalog imagery into the new pack merely because it is publicly downloadable; its rights and capture currency are less established.

## First completion boundary

- **Must have:** chosen storefront/edition, final wordmark/icon source, cover composition, five coherent gameplay images, and a small provenance/export manifest. Confirm that each asset satisfies that storefront's current rules before producing final dimensions.
- **Later:** trailer, motion/social variants, translated image text and extra device-specific galleries when the selected stores require them. Hive Mind and coding-tool imagery should not displace the core colony/economy story in this first profile.

The [distribution ledger](../facts/distribution.md) and [candidate-store audit](../facts/platform-audit.md#candidate-stores-and-prepared-submission-materials) distinguish published surfaces from prepared submissions. This brief does not select a store or establish account access. The next asset task is selecting the first storefront and launch build, then checking the existing candidates against it and filling the economy/spatial capture gaps.
