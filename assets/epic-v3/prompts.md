# Role-specific character study prompt

Built-in `image_gen.imagegen` identity-preserve edit on **2026-10-26**. No CLI fallback. One model edit was run. An earlier validation-only attempt rejected seven input paths before generation; the built-in accepts at most five.

## Ordered inputs

1. `assets/epic-v2/character-correction-study.png` — edit target; prior scene, not a character identity reference.
2. `assets/epic-v2/unit-references/worker-warrior-comparison.png` — nearest-neighbor comparison of unmodified real game worker and warrior renders; workers above, warriors below.
3. `assets/epic-v2/unit-references/worker-direction-0-pose-0.png` — actual worker identity.
4. `assets/epic-v2/unit-references/worker-direction-1-pose-0.png` — actual worker identity, alternate direction.
5. `assets/epic-v2/unit-references/warrior-direction-0-pose-0.png` — actual warrior identity.

`transparent_background: false`. The mascot icon was not supplied. The copied output is byte-for-byte the native generated result `exec-61c4163a-9665-48ba-9c98-9e68e51b0b22.png`.

## Exact prompt

```text
Use case: identity-preserve.
EDIT TARGET: Image 1 is an existing landscape colony illustration. Change ONLY the glob creatures, including all prominent foreground gatherers and the smaller colony traffic. Keep the existing environment, buildings, food patches, crystal groves, water, shore, camera, framing, lighting and color palette.
AUTHORITATIVE REAL GAME REFERENCES: Image 2 is a comparison of unmodified actual game renders: top row WORKERS, bottom row WARRIORS, at identical source canvas size. Images 3 and 4 are actual WORKERS in two viewing directions. Image 5 is an actual WARRIOR. The comparison board shows three viewing directions for each role. Match these real creatures' actual shapes, proportions, surfaces and pose-dependent silhouettes. These are not inspiration for a new character design. Do not use the previous artwork's four-ball starfish/jacks anatomy as a reference.
WORKERS: All three large foreground food-gatherers are WORKERS. Give them the source worker's distinctly long, slender, narrow connected body, thin tapered limb connections, modest rounded terminals, and the more extended, asymmetric silhouette visible in the source orientations. Their body should look stretched and lean rather than a round central ball with four giant spherical extremities. Follow the references' attached continuous organic anatomy and source surface character; no human neck/head/face, chest/shoulders, arms/fists, hands/fingers, muscular thighs or conventional feet. Let pose and perspective vary naturally as in the real renders; do not force all limbs into a symmetrical X. Match the literal source shape even where unusual. Keep purple team coloration rather than the references' green tint, but do not change proportions because of this recoloring.
WARRIORS: Only a few creatures at the existing colony perimeter may be warriors. Match the warrior source's visibly broader/heavier central mass and bulkier connected limbs and terminal lobes, distinguishable from slender workers at the same scale. They are not humanoid bodybuilders. Most visible creatures remain workers.
REJECTED LOOKS: identical shiny purple four-ball jacks, plastic molecule toys, smooth spherical central balls, chunky round worker bodies, overlarge ball terminals, invented cartoon humanoids or faces, icon-derived anatomy. The game renders—not any mascot icon—are the identity.
Maintain natural scene contact and food gathering without inventing hands. Preserve the productive economy-led scene. No text, logos, HUD, border or additional scene changes. This is promotional illustration, not a gameplay screenshot.
```
