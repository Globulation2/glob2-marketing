# Canonical storefront translations

[Project index](../README.md) · [Storefront v2 field map](storefront-v2-field-map.md) · [Terminology](glossary.md) · [Storefront v2 claims](../facts/storefront-v2-claims.md) · [Positioning v2](../analysis/positioning-v2.md) · [Storefront v1 presentation](../planning/approved-storefront-rollout.md)

Version: `storefront-v2`. English master rewritten 2026-11-24: [en.md](en.md). `storefront-v1` was created 2026-10-31 and is recorded in the [approved storefront rollout](../planning/approved-storefront-rollout.md).

**Status on 2026-11-24:** all 45 catalogs are storefront-v2: the English master, the platform matrix and the 44 locale catalogs, with `source-hashes.json` and a hash-bound review record for each locale. `check --require-review` passes ("Validated 45 canonical locales with independent reviews") and `export` writes its payloads with no limit violations. The 44 translations are AI translation with independent AI linguistic review, not human or native-speaker validation; the reviewers' ratings, fixes and the points a native speaker should check are in the [storefront v2 translation review record](../planning/storefront-v2-translation-review.md). `check-source` validates the English master alone.

Each locale catalog uses `## field_id` headings followed by plain text. Headings are identifiers; translate bodies only. Preserve field order and all identifiers. Catalog preambles record provenance and draft/review status; do not put extra second-level headings in them. Locale identifiers use the game's BCP 47 mapping, while destination identifiers are explicit mappings in tooling. Keep UTF-8 text, normal punctuation and intentional paragraph breaks; do not truncate text to pass a store limit.

Storefront-v2 follows [positioning v2](../analysis/positioning-v2.md): every listing opens with real-time strategy in player terms (you command the colony, not every unit) and the fair deal on the second line; desktop listings add an optional section on playing alongside the player's own AI agent through the built-in MCP server; mobile listings never mention it. A claim may appear on a store only where [storefront v2 claims](../facts/storefront-v2-claims.md) marks it safe there. Preserve meaning, factual qualifications and the product name **Globulation 2**. Translations are drafts until another agent independently checks them against English and terminology. Review status and source/content fingerprints belong in the tooling manifests; changing a field invalidates its dependent review/export status.

Each store composes its own plain-text description from shared blocks, in this order: `headline` and `fair_deal_line` on the first two lines; `listing_intro`; the control, economy, map and defense heading-body pairs; `features_heading` with a bullet list of `feature_*` fields; the multiplayer block; on desktop stores the AI-agent block; `open_source_heading/body`; and a platform tail. Sections are separated by one blank line, a heading from its body by one newline, and sentences that share a line by a space. Bullets are lines starting with `• `, or `- ` on stores that render Markdown lists (Snap, Epic); the AppStream fragment uses `<ul>`/`<li>`. Short fields are independently adapted and reviewed when a faithful literal translation exceeds a destination limit. Keywords are localized only from the keyword concepts listed in the [field map](storefront-v2-field-map.md).

Each catalog has 78 fields; the [field map](storefront-v2-field-map.md) gives each one's status against storefront-v1, its limit and unit, where it appears and how to adapt the tight ones. `epic_tail` and `epic_legal` keep the account and legal text read from the Epic console on 2026-10-31. Microsoft's feature list and Amazon's bullets (five at most) are now composed from the shared `feature_*` fields. `shot_overlay_<role>` fields are the short captions drawn onto mobile-store screenshots; `shot_caption_<role>` fields are caption sentences for stores with a caption field; `trailer_line_*` fields are the trailer's on-screen text. None of them names a map. Edition tails carry platform-specific truths and must not leak into other listings. Pricing, policy declarations, reviews, release notes and unsupported claims are not translated into listing fields by inference.

Under storefront-v1, all 44 non-English game locales had translated catalogs and independent AI review records (45 catalogs including the English master); those records were bound to the v1 source hashes and were replaced on 2026-11-24 by records bound to the storefront-v2 source and translation hashes. The twelve-language November 1 expansion and its validation are recorded in the [November 1 expansion](../planning/storefront-localization-rollout.md#game-language-expansion--2026-11-01). This does not establish human or native-speaker validation. The hash-bound records, rather than the original drafting preamble, determine current review status. Platform rollout uses supported locale intersections and independently verified current console options; language files do not prove every submitted artifact supports that language. For storefront-v2 imagery the [real-game-art rule](../AGENTS.md#real-game-art-only) applies: captioned screenshot sets are rendered per locale from the `shot_overlay_<role>` fields over real captures, and native UI, icons and the wordmark are never redrawn or translated in the image.

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
| [hi](hi.md) | Hindi | [ur](ur.md) | Urdu |
| [sw](sw.md) | Swahili | [bn](bn.md) | Bengali |
| [nb](nb.md) | Norwegian Bokmål | [ms](ms.md) | Malay |
| [mr](mr.md) | Marathi | [ta](ta.md) | Tamil |
| [te](te.md) | Telugu | [fil](fil.md) | Filipino |
| [bg](bg.md) | Bulgarian | [th](th.md) | Thai |

## Validation and maintenance

Run from the marketing repository root:

```sh
python3 translations/tools/storefront.py check-source
python3 translations/tools/storefront.py check --require-review
python3 -m unittest discover -s translations/tests
python3 translations/tools/storefront.py export --out /tmp/glob2-storefront-export
```

`check-source` reads only `en.md` and the platform matrix. It confirms that the English master parses, that every destination field mapped for English composes within its limit, that the matrix references no missing field and that no English field is unused. It ignores locale catalogs, source hashes and reviews, so it is the check to run after an English edit and before translation. It is not a release gate: `check --require-review` and `export` still reject every locale whose fields, source hashes or review are stale. The test suite also holds policy guards on the English source (fair deal on line two, no MCP on mobile, no other platform in Apple copy, no online claims on Amazon, no price word in image or trailer text, held switches off).

In the [platform matrix](platforms.json) a destination field is a list of paragraphs. A paragraph is a list of lines, or an object with `lines`, `bullets` and an optional `when` or `unless` switch. A line or bullet is a field ID, a `{"field": ID, "when": switch}` reference, or a list of those joined into one line. A platform declares its switches (`ai_coplay`, `online_play`) under `switches` and may set `bullet_prefix`; a reference to an undeclared switch is an error, and a destination field whose every reference is switched off is not exported. Switch values follow [storefront v2 claims](../facts/storefront-v2-claims.md) and are listed with their reasons in the [field map](storefront-v2-field-map.md#per-store-switches). The matrix also holds `protected_terms` (names, abbreviations and verified numbers that must survive wherever the English field has them, with local numerals accepted), `field_limits` (limits that bind in every locale, for image, caption and trailer text), `asset_text` (the screenshot roles and trailer lines the image and video renderers read) and `appstream` (the summary, description, caption roles and switches for the AppStream and desktop-entry fragments). `itch`, `steam` and `gog` are English-only preparation entries: itch.io has a single-language page, and no Steam or GOG listing exists.

The [November 17 mapping receipt](../planning/storefront-localization-rollout.md#expanded-locale-mappings-prepared--2026-11-17) records current documented expansion mappings and exact remaining gaps, including all 45 F-Droid source locales. The [platform matrix](platforms.json) defines destination field compositions, locale codes and measured limits; each field may set `length_unit` to `byte` (UTF-8) or `character` (the backward-compatible default). Apple `keywords` uses 100 UTF-8 bytes per the [current platform-version reference](https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information); other fields retain their documented character limits. Both `check` and export reject oversized mapped destination fields without truncation. Unsupported or unverified locales are written to the export gap report. Exports are preparation inputs and remain in a temporary directory. The export destination must be new or empty; reusing a populated directory fails so obsolete locale mappings cannot survive. A console locale, current editability and exact affected fields must be checked before applying them. Native game language support must be established separately from metadata translation availability. The `fastlane/` export targets the maintained F-Droid source tree and deliberately uses its neutral locale directories. The separate `google-play/` export uses Play locale identifiers; do not upload the F-Droid tree as ready Play metadata. Amazon preparation labels describe languages, not verified API wire codes; reconcile them with the current console/template.

For an approved English change, edit [en.md](en.md), check its source evidence, then refresh the source fingerprints:

```sh
python3 translations/tools/storefront.py hashes
```

Update affected locale fields and obtain an independent review. The reviewer records the exact accepted source and translation hashes only after checking meaning, consistent terminology, claims, proper names, URLs and destination field fit. For example:

```sh
python3 translations/tools/storefront.py review-record --locale fr --translator TRANSLATOR --reviewer INDEPENDENT_REVIEWER
```

Distinct identities are required. An English edit stales dependent source hashes; a translation edit stales its reviewed translation hash. The strict check/export gate rejects missing or stale reviews. Do not regenerate review records merely to silence a failed check. Keep issues unresolved until corrected and independently rechecked.

The game repository maintains `fastlane/metadata/android/`, `data/org.globulation2.Globulation2.metainfo.xml` and `data/glob2.desktop`. Merge exported localized text into those existing records, preserving English qualifications, release history, screenshot URLs and launcher settings. AppStream and desktop exports are merge fragments, not full replacement manifests. The AppStream fragment runs paragraph by paragraph with English first: a heading and its body share one `<p>` per locale, each bullet list is one `<ul>` holding an `<li>` per bullet per locale, and the desktop-entry `Comment` uses `appstream_summary`. The generated AppStream caption `source_role` attributes name the screenshot role (`hero`, `build`, `economy`, `battle`, `territory`, `maps`, `opponents`, `ai_coplay`); they are hints for matching screenshot nodes and must not appear in final AppStream metadata. Follow [the game maintenance guide](https://github.com/Globulation2/glob2/blob/master/docs/releases/store-setup.md#canonical-listing-translations).

## Version-specific release notes

[Localized release notes](releases/README.md) are reviewed separately from reusable storefront fields. Each release binds its exact approved English, game tag/source commit and translated content to an independent review manifest. A reviewed source file does not establish a saved or submitted store version.

## Artwork and rollout

The [artwork audit](media-audit.md) describes the storefront-v1 imagery: language-neutral key art, unchanged brand wordmark/native gameplay UI and the mobile gallery verification gaps of that time. Storefront-v2 replaces those galleries. Its only image text is the `shot_overlay_<role>` captions and the `trailer_line_*` lines from the reviewed catalogs; do not invent other slogans to create image variants.

The [localization rollout ledger](../planning/storefront-localization-rollout.md) records current per-platform editability, locale application and gaps. The [approved storefront ledger](../planning/approved-storefront-rollout.md) retains the underlying presentation/release evidence. Reviewed source catalogs, saved drafts, submitted updates and publicly displayed translations are separate outcomes.


## Epic template adapter

`tools/epic_template.py` maps the storefront-v2 Epic layout (updated 2026-11-24). It has been run only against synthetic templates so far: no storefront-v2 template has been downloaded, so the points under "Not yet checked against a real template" below remain open.

Use a fresh localization CSV downloaded from the authenticated Epic console. Keep that product-specific original and generated output outside this public repository:

```sh
python3 translations/tools/epic_template.py --template /path/to/downloaded-template.csv --out /tmp/glob2-epic-localized.csv
```

To replace the earlier translations in locale columns the template already has, add `--update-existing`:

```sh
python3 translations/tools/epic_template.py --template /path/to/downloaded-template.csv --out /tmp/glob2-epic-update.csv --update-existing
```

The mapping is data-driven. Canonical values are the payload keys under `platforms.epic.fields` in the [platform matrix](platforms.json), composed with that entry's `switches` and `bullet_prefix`; `FIELD_FAMILIES` at the top of `tools/epic_template.py` binds each key to its template rows:

| Payload key in `platforms.json` | Template rows (`Entity Type` / `Localization Field`) |
| --- | --- |
| `title` | `Offer` / `title`; `Store Configs` / `productDisplayName` |
| `short_description` | `Offer` / `description`; `Store Configs` / `shortDescription` |
| `legal` | `Store Configs` / `legalText` |
| `description` | `Offer` and `Product Home` / `aboutItem.N.textBlock.headline` and `.body`, `N` from 0 |

The composed `description` is split into About items by reading its paragraphs in order. A paragraph whose first line is a heading field (`headline` or `*_heading`) starts an item with that line as the heading; the rest of the paragraph and the paragraphs up to the next heading form the body, separated by a blank line, with bullets as a `- ` list. A switched-off paragraph is no item. With `ai_coplay` and `online_play` both off, as they are for Epic now, this gives the eight items of the [field map](storefront-v2-field-map.md#epic-about-items); turning `ai_coplay` on adds the AI-agent item as item 8 and moves the heritage item to 9. A payload key without a `FIELD_FAMILIES` line stops generation, so trailer or caption text added to the matrix later needs one line naming the row the current template actually exposes. The templates of 2026-10-31 and 2026-11-17 carried no carousel, caption or trailer rows; such a row in a later template stops generation as an unknown row until it is mapped or listed as preserved.

Before a storefront-v2 update, the About section on both the Offer and the Product Home must hold exactly as many items as the canonical layout, and the template must be downloaded after that. The adapter stops when an About entity has fewer item rows than the layout (it would otherwise leave a listing that mixes two layouts) or more (an extra item would keep its earlier text). It also stops when the English of a mapped row differs from canonical English, naming every such row. Either save the approved English in the console and download again, or add `--update-english` to replace exactly those English cells in the generated file.

The adapter requires current independent reviews: it refuses to write anything while any catalog, the source hashes or a review record is stale, and names the Epic locales that are not current. Until the locale catalogs were retranslated and reviewed on 2026-11-24 it therefore stopped for all 30 mapped non-English locales; since then `check --require-review` passes for all 45 catalogs. It then matches explicit template field keys, and fills only explicitly mapped locale columns that the actual template supports. Unknown rows, duplicate rows and unexpected field types stop generation. A saved translation that differs from the reviewed catalog stops generation unless `--update-existing` is given; then only those mapped cells are replaced. Identical saved translations, IDs, field definitions, separator and footer rows, and every unmapped cell are preserved. Required developer/publisher names, privacy/homepage URLs and technical requirements are copied exactly from the template’s existing English into the target locales as explicit English fallbacks, not claimed as translated technical prose. Empty invariant English values or conflicting saved fallback values stop generation with or without the update flags.

The command prints a JSON summary with one `changed_fields` line per locale column: the number of mapped cells replaced and filled and the canonical fields they belong to (`about_item_1-8` is a run of whole items; `already current` when nothing changed). `changed_cells` is the number of translated cells to expect as differences when comparing the fresh saved export with the downloaded template, `english` lists English rows replaced by `--update-english`, and `warnings` names canonical fields the template has no row for and list bodies that land in a row whose type is not `markdown`. The adjacent `.report.json` lists every changed row per column and counts fallback cells separately from canonical translated cells, without product IDs.

Not yet checked against a real template (2026-11-24): that items added in the console appear as further `aboutItem.N.textBlock` rows on both entities, including while their locale cells are empty; that About bodies are `markdown` rows and render `- ` lines as a list; whether the import writes the `en` column at all, which decides whether `--update-english` has any effect in the console; and any per-item length limit, since only the composed 10,000-character description limit is enforced. Check each with the first storefront-v2 template and a server readback.

Storefront-v1 history: the October 31 template batch used 24 canonical non-English locale columns; Greek is absent and the canonical Spanish mapping targets `es-ES`. Following [Epic’s localization instructions](https://dev.epicgames.com/docs/epic-games-store/store-presence/localize/localize-text?lang=en-US), the adapter removes unused locale columns from the upload copy so they do not create incomplete unintended localizations. For that historical batch the seven unused columns were `bg`, `es`, `fil`, `hi`, `ms`, `no` and `th`; any existing nonempty value in a column to be removed instead stops generation for reconciliation. The original downloaded template remains untouched. Hindi, Malay, Norwegian Bokmål, Filipino, Bulgarian and Thai were added to the game roster later; their current platform mappings require a fresh template check, including the distinction between canonical `nb` and the historical template’s `no`. That batch contained 600 canonical translated cells and 408 exact English fallback cells. Language-neutral wordmarks and technical text are not invented translations. The generated file is ready for import review; importing, saving, server readback and any review/publication step remain separately verified platform actions.

## Microsoft template adapter

Export the current Store listings workbook from the authenticated Microsoft console. Keep the original export and generated import outside this public repository:

```sh
python3 translations/tools/microsoft_import.py /path/to/current-console-export.xlsx --out /tmp/glob2-microsoft-localized.csv
```

The adapter reads a single unmodified XLSX sheet or a UTF-8 CSV and writes the UTF-8 CSV accepted by the console. It preserves template rows, field IDs/types, existing English values and approved asset URLs, then adds supported translated descriptions, short text, reserved product title, features, search term and desktop captions. Shared/inline strings, numeric field IDs and empty cells retain their original values; formulas, ambiguous sheets, unsupported cell types, missing expected fields, stale reviews, over-limit text and existing translated columns stop generation for reconciliation. English release notes, technical/legal fields and unrelated media are preserved rather than translated or changed.

To replace the copy in locale columns the export already has, add `--update-existing`:

```sh
python3 translations/tools/microsoft_import.py /path/to/current-console-export.xlsx --out /tmp/glob2-microsoft-update.csv --update-existing
```

Update mode overwrites only the mapped text rows of each existing locale column with the reviewed canonical values. Every other cell in those columns keeps its saved value, including screenshot, logo and trailer references, release notes and technical fields; locales missing from the export are still appended from English as before. The English column is not translated, so update mode first compares its mapped rows with canonical English and stops, naming the differing fields, when they differ. Either save the approved English in the console and export again, or add `--update-english` to replace exactly those English fields in the same import. The printed JSON lists, per locale column, the template fields whose saved value was replaced (`already current` when none), the appended locales, the English result and `changed_cells`, the number of overwritten cells to expect when comparing the fresh saved export.

`warnings` in that output need a decision before import. They name numbered text rows that hold text but have no canonical value (left unchanged, so earlier copy may survive there), captions or trailer titles whose own media row is empty in a column, and locale columns that no canonical locale maps to. Update mode never changes media: after new English screenshots are saved, each existing locale column still references its earlier images until those rows are updated separately. [Microsoft's import reference](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/import-and-export-store-listings) (observed 2026-11-24) states that a blank Text cell removes that entry or falls back to the `default` column, a blank image cell keeps the previous image, a blank trailer cell deletes the trailer, and saved asset URLs can be reused in other language columns.

The mapping is data-driven. Canonical values are the payload keys under `platforms.microsoft.fields` in the [platform matrix](platforms.json); `FIELD_FAMILIES` at the top of `tools/microsoft_import.py` binds each key to its template row:

| Payload key in `platforms.json` | Template row |
| --- | --- |
| `title`, `description`, `short_description` | `Title`, `Description`, `ShortDescription` |
| `feature_N` | `FeatureN` |
| `search_term` or `search_term_N` | `SearchTermN` |
| `desktop_screenshot_caption_N` | `DesktopScreenshotCaptionN` |
| `trailer_title_N` | `TrailerTitleN` |

Numbered families take as many rows as the matrix defines, so a listing with more than four desktop screenshots needs only further `desktop_screenshot_caption_N` entries composed from the relevant catalog fields, with their limits. Every defined key must land on exactly one row of the current export; a key without a row, or without a `FIELD_FAMILIES` line, stops generation. A new kind of translated text row needs one added line there. While the matrix defines no `desktop_screenshot_caption_N`, the adapter falls back to the four storefront-v1 catalog captions (`screenshot_caption_colony`, `_battle`, `_strategic`, `_terrain`) for the caption rows the export exposes. `TrailerTitleN` follows Microsoft's trailer title rows and has not yet been observed in a project export.

The actual 2026-10-31 template uses `Type (Type)` and `DesktopScreenshotCaption1` through `DesktopScreenshotCaption4`. It has 453 data rows and only `en-us`; 31 new locale columns are prepared. Indonesian `id` remains distinct from the reserved `ID` metadata column. Before applying a later export, inspect its current structure and submission state again. Import validation, fresh saved export comparison, screenshot checks and review/publication remain separate steps; a generated CSV does not establish any of them.
