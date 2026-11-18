# Player handbook refresh inventory

[Website execution record](website-refresh-execution.md) · [Planning index](README.md)

Observed **18 November 2026**. This records the remaining instructional refresh, separately from the completed marketing-media preparation. Source completion, object upload and production publication are different states; use the execution record above for the latest publication receipt.

## Inventory and current status

The pre-refresh website contained **29 current handbook chapters**, **26 capture families** and **237 media assets: 223 images and 14 videos**. All manifest assets were used, including video posters. Three reference chapters reuse other families, so chapter and family counts differ. These were active instructional images, not historical archive material merely because their original provenance was retained.

Sources: the [237-asset manifest](https://github.com/Globulation2/glob2-online-website/blob/bf24997cd73b303d68b407e69349ab74c8c0f800/src/data/guide-media.json), [chapter directory](https://github.com/Globulation2/glob2-online-website/tree/bf24997cd73b303d68b407e69349ab74c8c0f800/src/content/guides), and [capture baseline](https://github.com/Globulation2/glob2-online-website/blob/bf24997cd73b303d68b407e69349ab74c8c0f800/src/data/guide-baseline.json), inspected on the observation date.

| Work unit | Status and scope |
| --- | --- |
| Marketing homepage, game page, social image and hero | Current native 0.11.6.1 captures prepared and reviewed. Separate from handbook lessons; see the website execution record. |
| Current first-session entry and scouting task | Bounded source unit complete in [website commit f7a625b](https://github.com/Globulation2/glob2-online-website/commit/f7a625bae9758e8e14ff7a157718d41636286d29), within [PR #62](https://github.com/Globulation2/glob2-online-website/pull/62). Four genuine current-browser images, including a readable sidebar detail, uploaded under immutable v2 paths and publicly hash-verified. Guide mechanics and two rendered rounds reviewed. Production publication remains a separate receipt. |
| Earlier first-session walkthrough | Its 17 original assets and original provenance retained in a collapsed, explicitly earlier-version reference, excluded from search indexing. It describes the retired lesson, not the current task order. |
| Other 28 active chapters | **220 older assets across 25 families remain to assess and refresh.** Their flows, mechanics and counters were not reverified by this audit. Do not infer that every instruction is wrong, or that these chapters have become historical material. |

The updated manifest contains 241 assets: the original 237 plus four current first-session images. The original first-session family is not referenced by other chapters. The remaining 220 includes 13 videos and their supporting imagery; the four-image repair is not a complete five-task Introduction walkthrough.

## Family ledger

Counts below describe the original 237-asset inventory and include posters/detail crops. “Pending” means current-game reproduction and editorial assessment remain open, not a verified defect in every asset.

| Capture family | Assets | Refresh state |
| --- | ---: | --- |
| getting-started | 17 | Earlier lesson retained; four current images added separately. |
| controls-and-hud | 5 | Pending |
| resources-and-hauling | 9 | Pending |
| jobs-and-flags | 4 | Pending |
| sustainable-food | 8 | Pending |
| population-and-production | 8 | Pending |
| buildings-and-services | 7 | Pending |
| training-and-upgrades | 11 | Pending |
| exploration-and-movement | 5 | Pending |
| reference-controls | 2 | Pending |
| recovering-your-colony | 2 | Pending |
| defending-your-colony | 6 | Pending |
| victory-and-rules | 5 | Pending |
| organizing-an-attack | 14 | Pending |
| browser-and-multiplayer | 4 | Pending |
| fruit-and-conversion | 12 | Pending |
| economy-and-expansion | 10 | Pending |
| choosing-an-ai | 8 | Pending |
| ai-numbi | 8 | Pending |
| ai-castor | 13 | Pending |
| ai-econo | 11 | Pending |
| ai-warrush | 12 | Pending |
| ai-cortex | 13 | Pending |
| ai-cabino | 12 | Pending |
| ai-nicowar | 15 | Pending |
| ai-maxima | 16 | Pending |

## Verified version and workflow differences

- The public browser game visibly reported **0.11.6.0** on 18 November. Current menu, lesson catalog, briefing, flag placement and explorer arrival were captured through real visible controls. The exact deployed source revision remains unverified; the displayed version alone does not establish it. [First-session evidence](https://github.com/Globulation2/glob2-online-website/blob/f7a625bae9758e8e14ff7a157718d41636286d29/docs/first-session-current-evidence.json) records public package hashes and the bounded observations.
- The new marketing family uses the public **native 0.11.6.1** Mac release, source `1b60514218218c89516b6c6f26f2fcefc9c8f974`. It does not establish the browser deployment identity or validate browser lessons. [Marketing capture provenance](https://github.com/Globulation2/glob2-online-website/blob/f7a625bae9758e8e14ff7a157718d41636286d29/docs/website-media-v0.11.6.1.json).
- The existing capture baseline specifies **0.11.0.0**, older JavaScript/WASM hashes and the former application hostname. Both current package hashes differ. The [capture helper](https://github.com/Globulation2/glob2-online-website/blob/f7a625bae9758e8e14ff7a157718d41636286d29/scripts/capture-guide.mjs) intentionally refuses changed packages; its baseline cannot simply be relabelled current. Its first-menu wait also needs to handle the current first-use Introduction offer.
- No original scenario modules were found in the retained handbook capture artifacts during this audit; only the media cache was present. The helper exists, but the 26 lesson scenarios are not available as a repeatable batch. This is a local retention finding, not proof that no copies exist elsewhere.
- The old first-colony instructions named Tutorial Campaign and Introduction and Basics. The current game instead exposes a ten-lesson Tutorial lessons catalog. Actual Introduction starts by scouting a stone landmark with an Exploration Flag. [Game PR #1297](https://github.com/Globulation2/glob2/pull/1297) provides source context for replacing the legacy campaign with JavaScript training lessons. Merely swapping images would have preserved a broken entry flow; that bounded flow is now corrected in source.

## Next capture requirements

1. Establish the actual deployed browser source and package identity, then reconcile the capture baseline without asserting that native and browser versions match.
2. Reconstruct and retain reproducible scenario modules by family. Record real menu/control actions, map/save or seed, rules, AI, renderer, viewport and observed ticks; handle first-use screens and asynchronous readiness.
3. Reproduce each lesson against the current game before changing its text or imagery. Check labels, actions, costs, requested versus attached units, outcomes and failure recovery. Preserve uncertainty where a behavior has not been tested.
4. Capture authentic full scenes, readable control details and short explanatory clips. Match captions to observed counters; keep originals and full action logs out of public Git. New imagery must come from the game and respect the approved imagery/provenance restrictions.
5. Follow the [maintained handbook production workflow](https://github.com/Globulation2/glob2-online-website/blob/f7a625bae9758e8e14ff7a157718d41636286d29/docs/handbook-production.md): independent content/visual review, immutable versioned objects, public byte/hash readback, manifest checks, two rendered rounds, then the website’s normal PR and publication gates.

No outreach, storefront-gallery replacement, all-chapter revalidation or further publication is recorded by this inventory. Link subsequent completed families here and retain the dated baseline rather than silently rewriting its historical evidence.
