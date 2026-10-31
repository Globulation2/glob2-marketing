# Canonical storefront translations

[Project index](../README.md) · [Approved English presentation](../planning/approved-storefront-rollout.md) · [Terminology](glossary.md)

Version: `storefront-v1`. Created 2026-10-31. English master: [en.md](en.md).

Each locale catalog uses `## field_id` headings followed by plain text. Headings are identifiers; translate bodies only. Preserve field order and all identifiers. Catalog preambles record provenance and draft/review status; do not put extra second-level headings in them. Locale identifiers use the game's BCP 47 mapping, while destination identifiers are explicit mappings in tooling. Keep UTF-8 text, normal punctuation and intentional paragraph breaks; do not truncate text to pass a store limit.

The approved core keeps colony building and economics first, with map strategy and rival pressure supporting. Preserve meaning, factual qualifications and the product name **Globulation 2**. Translations are drafts until another agent independently checks them against English and terminology. Review status and source/content fingerprints belong in the tooling manifests; changing a field invalidates its dependent review/export status.

The core plain-text description joins `headline`, `listing_intro`, the economy/map/defense heading-body pairs, and `listing_open_source`. Separate sections with one blank line and each heading from its body with one newline. Edition-specific tails are appended after a blank line. The page-specific `about_intro` and `open_source_heading/body` preserve the approved presentation variant. Short fields are independently adapted and reviewed when a faithful literal translation exceeds a destination limit. Keywords are localized only from the existing evidenced keyword concepts.

The portable core and exact edition tails are represented by 38 fields in each catalog. Epic account/legal text, Amazon's existing no-ad/in-app-purchase qualification and six bullets, and Windows' four saved bullets were read from current consoles on 2026-10-31. The Amazon qualification is edition-specific and must not leak into other listings. Preserve all existing factual tails. Pricing, policy declarations, reviews, release notes and unsupported claims are not translated into listing fields by inference.

All 32 non-English game locales have translated catalogs and independent AI review records; this does not establish human or native-speaker validation. The hash-bound records, rather than the original drafting preamble, determine current review status. Platform rollout uses supported locale intersections and independently verified current console options; language files do not prove every submitted artifact supports that language. Reuse approved artwork unchanged where it contains only the product wordmark or native gameplay UI. Audit existing mobile galleries for marketing overlays; translate only actual overlays using approved sources/direct derivatives, preserving native UI, icons and wordmark. The HTML headings in the approved preview are text rather than baked image content.

Record prepared, reviewed, saved, submitted and publicly verified separately. Preserve existing review submissions and wait for a platform's editable state where needed. After upload, wait for completion, save, fresh-reload from the server and compare persisted text/media. Unverified control or unsupported localization is an explicit gap, not completed rollout.


## Locale catalogs

| Locale | Language | Locale | Language |
| --- | --- | --- | --- |
| [ar](ar.md) | Arabic | [pt-BR](pt-BR.md) | Portuguese — Brazil |
| [ca](ca.md) | Catalan | [cs](cs.md) | Czech |
| [de](de.md) | German | [da](da.md) | Danish |
| [es](es.md) | Spanish | [eo](eo.md) | Esperanto |
| [eu](eu.md) | Basque | [fa](fa.md) | Persian |
| [fr](fr.md) | French | [el](el.md) | Greek |
| [hu](hu.md) | Hungarian | [it](it.md) | Italian |
| [nl](nl.md) | Dutch | [pl](pl.md) | Polish |
| [pt-PT](pt-PT.md) | Portuguese — Portugal | [ro](ro.md) | Romanian |
| [ru](ru.md) | Russian | [sl](sl.md) | Slovenian |
| [sk](sk.md) | Slovak | [sr-Cyrl](sr-Cyrl.md) | Serbian — Cyrillic |
| [fi](fi.md) | Finnish | [sv](sv.md) | Swedish |
| [tr](tr.md) | Turkish | [zh-Hant](zh-Hant.md) | Chinese — Traditional |
| [zh-Hans](zh-Hans.md) | Chinese — Simplified | [uk](uk.md) | Ukrainian |
| [id](id.md) | Indonesian | [vi](vi.md) | Vietnamese |
| [ja](ja.md) | Japanese | [ko](ko.md) | Korean |

## Validation and maintenance

Run from the marketing repository root:

```sh
python3 translations/tools/storefront.py check --require-review
python3 -m unittest discover -s translations/tests
python3 translations/tools/storefront.py export --out /tmp/glob2-storefront-export
```

The [platform matrix](platforms.json) defines destination field compositions, locale codes and measured limits; unsupported or unverified locales are written to the export gap report. Exports are preparation inputs and remain in a temporary directory. The export destination must be new or empty; reusing a populated directory fails so obsolete locale mappings cannot survive. A console locale, current editability and exact affected fields must be checked before applying them. Native game language support must be established separately from metadata translation availability. The `fastlane/` export targets the maintained F-Droid source tree and deliberately uses its neutral locale directories. The separate `google-play/` export uses Play locale identifiers; do not upload the F-Droid tree as ready Play metadata. Amazon preparation labels describe languages, not verified API wire codes; reconcile them with the current console/template.

For an approved English change, edit [en.md](en.md), check its source evidence, then refresh the source fingerprints:

```sh
python3 translations/tools/storefront.py hashes
```

Update affected locale fields and obtain an independent review. The reviewer records the exact accepted source and translation hashes only after checking meaning, consistent terminology, claims, proper names, URLs and destination field fit. For example:

```sh
python3 translations/tools/storefront.py review-record --locale fr --translator TRANSLATOR --reviewer INDEPENDENT_REVIEWER
```

Distinct identities are required. An English edit stales dependent source hashes; a translation edit stales its reviewed translation hash. The strict check/export gate rejects missing or stale reviews. Do not regenerate review records merely to silence a failed check. Keep issues unresolved until corrected and independently rechecked.

The game repository maintains `fastlane/metadata/android/`, `data/org.globulation2.Globulation2.metainfo.xml` and `data/glob2.desktop`. Merge exported localized text into those existing records, preserving English qualifications, release history, screenshot URLs and launcher settings. AppStream and desktop exports are merge fragments, not full replacement manifests. The generated AppStream caption `source_role` attributes are hints for matching existing screenshot nodes and must not appear in final AppStream metadata. Follow [the game maintenance guide](https://github.com/Globulation2/glob2/blob/master/docs/releases/store-setup.md#canonical-listing-translations).

## Artwork and rollout

The [artwork audit](media-audit.md) distinguishes language-neutral approved key art, unchanged brand wordmark/native gameplay UI and existing mobile gallery verification gaps. Reuse language-neutral approved files. Translate only actual marketing overlays discovered in the audit, using approved source images or direct derivatives; do not invent slogans to create image variants.

The [localization rollout ledger](../planning/storefront-localization-rollout.md) records current per-platform editability, locale application and gaps. The [approved storefront ledger](../planning/approved-storefront-rollout.md) retains the underlying presentation/release evidence. Reviewed source catalogs, saved drafts, submitted updates and publicly displayed translations are separate outcomes.


## Epic template adapter

Use a fresh localization CSV downloaded from the authenticated Epic console. Keep that product-specific original and generated output outside this public repository:

```sh
python3 translations/tools/epic_template.py --template /path/to/downloaded-template.csv --out /tmp/glob2-epic-localized.csv
```

The adapter requires current independent reviews, matches explicit template field keys and exact canonical English, and fills only explicitly mapped locale columns that the actual template supports. Unknown rows, changed English in translated fields or conflicting nonempty translated cells stop generation. Identical existing translations are preserved; reconcile differing saved translations before import. Existing IDs, English values, technical specifications, developer/publisher identity, unsupported locale cells and footer rows are preserved. The adjacent JSON report records the actual locale intersection without product IDs.

The inspected template exposes 24 canonical non-English locale columns; Greek is absent and generic Spanish is preserved because the canonical Spanish mapping targets `es-ES`. Language-neutral wordmarks and technical text are not invented translations. The generated file is ready for import review; importing, saving, server readback and any review/publication step remain separately verified platform actions.
