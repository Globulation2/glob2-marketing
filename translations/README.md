# Canonical storefront translations

[Project index](../README.md) · [Approved English presentation](../planning/approved-storefront-rollout.md) · [Terminology](glossary.md)

Version: `storefront-v1`. Created 2026-10-31. English master: [en.md](en.md).

Each locale catalog uses `## field_id` headings followed by plain text. Headings are identifiers; translate bodies only. Preserve field order and all identifiers. Catalog preambles record provenance and draft/review status; do not put extra second-level headings in them. Locale identifiers use the game's BCP 47 mapping, while destination identifiers are explicit mappings in tooling. Keep UTF-8 text, normal punctuation and intentional paragraph breaks; do not truncate text to pass a store limit.

The approved core keeps colony building and economics first, with map strategy and rival pressure supporting. Preserve meaning, factual qualifications and the product name **Globulation 2**. Translations are drafts until another agent independently checks them against English and terminology. Review status and source/content fingerprints belong in the tooling manifests; changing a field invalidates its dependent review/export status.

The core plain-text description joins `headline`, `listing_intro`, the economy/map/defense heading-body pairs, and `listing_open_source`. Separate sections with one blank line and each heading from its body with one newline. Edition-specific tails are appended after a blank line. The page-specific `about_intro` and `open_source_heading/body` preserve the approved presentation variant. Short fields are independently adapted and reviewed when a faithful literal translation exceeds a destination limit. Keywords are localized only from the existing evidenced keyword concepts.

The portable core and exact edition tails are ready for translation. Epic account/legal text, Amazon's existing no-ad/in-app-purchase qualification and six bullets, and Windows' four saved bullets were read from current consoles on 2026-10-31. The Amazon qualification is edition-specific and must not leak into other listings. Preserve all existing factual tails. Pricing, policy declarations, reviews, release notes and unsupported claims are not translated into listing fields by inference.

All 32 non-English game locales are translation targets. Platform rollout uses supported locale intersections and independently verified current console options; language files do not prove every submitted artifact supports that language. Reuse approved artwork unchanged where it contains only the product wordmark or native gameplay UI. Audit existing mobile galleries for marketing overlays; translate only actual overlays using approved sources/direct derivatives, preserving native UI, icons and wordmark. The HTML headings in the approved preview are text rather than baked image content.

Record prepared, reviewed, saved, submitted and publicly verified separately. Preserve existing review submissions and wait for a platform's editable state where needed. After upload, wait for completion, save, fresh-reload from the server and compare persisted text/media. Unverified control or unsupported localization is an explicit gap, not completed rollout.
