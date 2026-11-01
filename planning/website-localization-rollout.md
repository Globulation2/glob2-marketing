# Main marketing website localization

[Planning index](README.md) · [Repository and web-property facts](../facts/repositories.md) · [Storefront localization](storefront-localization-rollout.md)

Observed **2026-11-01**. The user scoped this work to the **main marketing pages** of [glob2.online](https://glob2.online/). The website has its own English editorial source; the canonical storefront translations supplied terminology references rather than replacing the website's copy.

## Scope and source

The homepage, game explanation, downloads and community pages have **45 locale variants: English plus the game's 44 non-English languages**, producing **180 static marketing routes**. English retains its existing paths; translated pages use `/<locale>/`, `/<locale>/game/`, `/<locale>/downloads/` and `/<locale>/community/`.

The [194-field website English master](https://github.com/Globulation2/glob2-online-website/blob/e6e7636fa10dbe8ea944affb7bf46d50527501cd/src/i18n/en.json) covers page copy, navigation, footer, screenshot captions and descriptions, download instructions, accessible labels, theme controls and animation controls. The [locale registry](https://github.com/Globulation2/glob2-online-website/blob/e6e7636fa10dbe8ea944affb7bf46d50527501cd/src/i18n/locales.ts) matches the game roster observed at `8d5293c436`. Existing artwork, wordmark orientation, release metadata, download URLs, package checksums and executable commands are retained.

The language menu preserves the current marketing page. Pages declare their language, Arabic/Persian/Urdu text direction, canonical URL and same-page language alternatives. Guides, history, news, competition, archive, search, credits and legal pages remain English; links from translated pages visibly label those English destinations. Existing legal-source synchronization remains authoritative.

## Translation and validation

Machine-translation drafts received agent corrections and separate independent AI review against all 194 fields. The [review records](https://github.com/Globulation2/glob2-online-website/tree/e6e7636fa10dbe8ea944affb7bf46d50527501cd/src/i18n/reviews) bind the English and translated files by SHA-256. Targeted supplementary reviews aligned Tutorial instructions with the game's actual localized menu names while preserving the original full-reviewer provenance. **Human or native-speaker validation is not claimed.**

The strict gate validates all 45 catalogs, complete keys, placeholders, protected commands and screenshot counters, source drift, and current independent review fingerprints. The built-site gate checks all 180 marketing routes for language/direction, exact canonical and same-page alternate URLs, localized navigation and unresolved placeholders. Check, build and internal-link validation passed.

The pull-request browser suite recorded **325 passed and two skipped**. Two rendered review rounds each covered **20 cases**: English, German, Arabic, Japanese and Tamil home/download pages at 360px and 1440px. Those representative checks covered accessibility, overflow, keyboard language switching, page preservation, RTL command isolation and retained download URLs/checksums. Their results do not establish a separate visual inspection of every language. Screenshots and detailed reports remain in ignored website artifacts; the [website maintenance guide](https://github.com/Globulation2/glob2-online-website/blob/e6e7636fa10dbe8ea944affb7bf46d50527501cd/docs/localization.md) records reproducible commands.

## Publication receipts

| Stage | Actual evidence |
| --- | --- |
| Reviewed source and merge | [Website PR #59](https://github.com/Globulation2/glob2-online-website/pull/59) merged into website `main` as [`e6e7636fa10dbe8ea944affb7bf46d50527501cd`](https://github.com/Globulation2/glob2-online-website/commit/e6e7636fa10dbe8ea944affb7bf46d50527501cd). The website's own pull-request workflow was followed. |
| Production deployment | [Main workflow 41352253657](https://github.com/Globulation2/glob2-online-website/actions/runs/41352253657) completed successfully for that source, with verification and publishing jobs passing. Preview upload, preview smoke test and promotion of the tested version each succeeded. Both release and promotion receipts identify immutable Hosting version `cf412bd22a6c195d`. |
| Independent public readback | On **2026-11-01, 16:48:38–16:48:52 America/Toronto / 21:48:38–21:48:52 UTC**, all **180 public URLs across 45 locales and four pages** passed, with HTTP 200 and zero gaps. Fresh responses matched native headings, language/direction, canonical URLs, all 46 same-page alternate links, local marketing navigation, English-only guide/legal labels, retained media URLs and source-package URL/checksum for `v0.11.4.0`. The expected English catalog SHA-256 was `69c3109f676976b1c91341050cd45528546af26f35ca5a8a0f289b5c666f401b`. Public examples include the [French homepage](https://glob2.online/fr/), [Arabic game explanation](https://glob2.online/ar/game/), [Japanese downloads](https://glob2.online/ja/downloads/) and [Tamil community page](https://glob2.online/ta/community/). |

This record concerns website localization. Existing storefront saves, reviews, release states and platform-language gaps remain in the separate [storefront ledger](storefront-localization-rollout.md); website publication does not update those listings.
