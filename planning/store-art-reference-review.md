# Store artwork reference review

[Planning index](README.md) · [Epic profile](epic-store-profile-v1.md) · [First artwork pack](../assets/epic-v1/README.md) · [Positioning](../analysis/positioning-v1.md)

Observed **2026-10-26**, following the user's rejection of the first artwork pack as resembling a presentation slide. This pass visually inspected the current publisher-provided Steam header and small capsule images for six strategy/colony games. The Steam app-details API supplied the actual image URLs; the images were downloaded to a temporary inspection directory and viewed together. This is visual analysis, not evidence of conversion performance. No third-party game artwork is included in Glob2's exported or committed assets.

## Observed examples

| Official store reference | What is visible in the inspected header | Useful composition lesson |
| --- | --- | --- |
| [Against the Storm](https://store.steampowered.com/app/1336490/Against_the_Storm/) | Painted character group in the foreground, threatening creature and atmospheric world behind; ornate title integrated at lower right. The scene fills the frame. | Foreground identity, depth and atmosphere make the world inviting before explaining its systems. |
| [Timberborn](https://store.steampowered.com/app/1062090/Timberborn/) | Two beaver characters overlook a busy settlement, with architecture and machinery extending into depth. Large white title occupies the sky above. | Colony/economy can be communicated through character activity and an expansive inhabited world rather than text. |
| [Northgard: Definitive Edition](https://store.steampowered.com/app/466560/Northgard/) | Armed foreground figures face a settlement under an atmospheric sky; centered title. The current header also carries a temporary Battlegrounds demo-promotion strip. | A readable foreground silhouette and settlement create a journey into the scene. The temporary promo strip is a current observation, not a model for the Glob2 master. |
| [They Are Billions](https://store.steampowered.com/app/644930/They_Are_Billions/) | Nighttime city in the distance, surrounding threatening silhouettes, luminous central emblem and large title. | A focused emotional conflict and strong light/dark hierarchy survive at thumbnail size. Its combat/horror emphasis does not match Glob2's economy-first positioning. |
| [Factorio](https://store.steampowered.com/app/427520/Factorio/) | Dense factory machinery occupies the entire frame; orange industrial title is large and centered. | Authentic game-world systems can become the cover's visual texture without an inset screenshot or separate explanation panel. |
| [Mindustry](https://store.steampowered.com/app/1127400/Mindustry/) | Full-frame machinery/production imagery behind a very large, angular central title. | Even a systems-heavy, visually small-unit game can make a bold cover by simplifying title hierarchy and filling the frame with its world. |

The small capsules were also inspected: title readability and the dominant color/composition persist while fine details recede. These examples do not all use the same art treatment; the common pattern is a coherent image with a strong title, rather than a slide containing a screenshot.

## Implications for the next Glob2 draft

These are proposed design changes derived from the observations, not assertions that another game's style would perform better for Glob2.

1. **Make the game world the whole image.** Remove the purple presentation panel, inset screenshot, explanatory headline and tiny genre footer. Build a full-bleed colony scene and integrate the Globulation 2 title into a deliberately quieter part of it.
2. **Give the colony a focal point and depth.** Distinctive globs doing economic work can anchor the foreground; food, workers and buildings establish a productive colony in the middle distance; terrain and a subtle rival presence supply scale and contested space. Use actual Glob2 creature/building references so the result belongs to this game.
3. **Separate key art from gameplay proof.** A promotional illustration may dramatize the world, but must be identified as illustrated key art rather than a gameplay screenshot. The carousel still needs genuine current-build gameplay images. Test title legibility at small size and compose portrait separately rather than squeezing a landscape slide into a tall canvas.

The selected message remains **“Build a thriving colony in contested territory.”** That guides the subject of the art; it does not need to be printed across the store cover. Preserve the existing title identity where it remains readable.

## Character-reference correction

A subsequent character-source review on **2026-10-26** found that the enlarged-sprite interpretation used for the first generated illustration was wrong. The user rejected its globs. A humanoid body with a separate head, hands or muscular anatomy is not an approved Glob2 identity; corrected art remains in progress.

The game repository at revision `7ebec312cd2bdcb6b6f685e141726b8caaca9ef7` retains [original Blender unit sources](https://github.com/Globulation2/glob2/tree/7ebec312cd2bdcb6b6f685e141726b8caaca9ef7/datasrc/gfx/originals/units) (`glob-worker-walk.blend`, `glob-warrior-walk.blend`, `explorer.blend`) and [original-derived renders](https://github.com/Globulation2/glob2/tree/7ebec312cd2bdcb6b6f685e141726b8caaca9ef7/datasrc/gfx/production/original-derived) (`unit256r.png` worker, `unit1024r.png` warrior, `unit0r.png` explorer; each 128×128 RGBA). These are stronger form references than guessing anatomy from tiny gameplay sprites.

Source review describes workers and warriors as a connected core with tapered branching extensions ending in four rounded terminal lobes. The [retained surface definitions](https://github.com/Globulation2/glob2/blob/7ebec312cd2bdcb6b6f685e141726b8caaca9ef7/datasrc/gfx/authored/skins/limb-surfaces.json) explicitly contain four paths for each; the [animation documentation](https://github.com/Globulation2/glob2/blob/7ebec312cd2bdcb6b6f685e141726b8caaca9ef7/tools/unit-animation/README.md) explains connected surfaces, rounded bulbs and legacy metaballs. Avoid separately recognizable heads/faces, fingers, toes, armor or human musculature. The explorer has a distinct low, horizontal paired-lobe form and flying behavior; do not turn all unit types into the same upright creature.

The correction is a source-fidelity requirement, not a final illustration approval. Review the original forms at useful scale before generating another colony scene. A source-reference board used for inspection remains temporary and is not a new marketing export.

## Evidence and rights boundary

The reference stores and their publisher-provided images are external visual references only. Temporary inspection files are outside the repository and must not be reused in Glob2 exports. Reference observation does not authorize use of another game's characters, logo, scenery or artwork. Any new Glob2 illustration needs its own source/provenance record and must not imply unverified gameplay features or a new in-game rendering style.
