# Actual worker and warrior references

[Artwork study](../README.md) · [Comparison sheet](worker-warrior-comparison.png) · [Frame provenance](provenance.json)

Collected **2026-10-26** after the user clarified that workers are longer and more slender, while warriors are bulkier. These are actual game renders, not generated character interpretations. Use the role-specific images to preserve proportions; the project icon is not the anatomy reference.

The six role-named PNG files are unchanged 128×128 RGBA copies from the game's `datasrc/gfx/production/original-derived/` directory. They preserve the original recolorable body/team layer, including alpha. They do not include the separately rendered ground/shadow layer or represent an assembled gameplay screenshot. The comparison sheet enlarges each complete source canvas by the same **3× nearest-neighbor** factor against a dark inspection background. It does not normalize body width, alter anatomy, smooth texture or depict a newly rendered character.

| Role | Copied image | Original frame | Manifest identity |
| --- | --- | --- | --- |
| Worker | [Direction 0](worker-direction-0-pose-0.png) | `unit256r.png` | `worker-walk`, direction 0, pose 0 |
| Worker | [Direction 1](worker-direction-1-pose-0.png) | `unit288r.png` | `worker-walk`, direction 1, pose 0 |
| Worker | [Direction 3](worker-direction-3-pose-0.png) | `unit352r.png` | `worker-walk`, direction 3, pose 0 |
| Warrior | [Direction 0](warrior-direction-0-pose-0.png) | `unit1024r.png` | `warrior-walk`, direction 0, pose 0 |
| Warrior | [Direction 1](warrior-direction-1-pose-0.png) | `unit1056r.png` | `warrior-walk`, direction 1, pose 0 |
| Warrior | [Direction 3](warrior-direction-3-pose-0.png) | `unit1120r.png` | `warrior-walk`, direction 3, pose 0 |

Direction numbers follow the source manifest; no unverified compass labels are assigned. All poses are zero for a matched comparison. The original render cameras/proportions remain intact.

## Source and validation

Source repository: [Globulation2/glob2 at 7ebec312](https://github.com/Globulation2/glob2/tree/7ebec312cd2bdcb6b6f685e141726b8caaca9ef7). The [production manifest](https://github.com/Globulation2/glob2/blob/7ebec312cd2bdcb6b6f685e141726b8caaca9ef7/datasrc/gfx/production/pack-metadata/manifest.json) supplies the animation, direction, pose, Blender-source identities and render hashes. [Original-derived files](https://github.com/Globulation2/glob2/tree/7ebec312cd2bdcb6b6f685e141726b8caaca9ef7/datasrc/gfx/production/original-derived) are preserved artist exports and source-model renders, as described in the [production guide](https://github.com/Globulation2/glob2/blob/7ebec312cd2bdcb6b6f685e141726b8caaca9ef7/datasrc/gfx/production/README.md) and [unit-rendering guide](https://github.com/Globulation2/glob2/blob/7ebec312cd2bdcb6b6f685e141726b8caaca9ef7/tools/unit-animation/README.md).

Each copied file was decoded, checked as 128×128 RGBA, matched to the manifest's role/direction/pose, and compared byte-for-byte with its source via SHA-256. [provenance.json](provenance.json) records the exact paths, source-model hashes and copied-file hashes. No game or design-system source files were changed.

The source repository's [COPYING](COPYING) notice is retained unchanged. These references do not grant new rights or replace release-specific attribution review; preserve original artist credits and any applicable individual notices when preparing final marketing artwork.
