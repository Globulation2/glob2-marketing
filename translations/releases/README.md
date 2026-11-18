# Localized release notes

[Storefront translation contract](../README.md)

Release notes are version-specific. Their English source is approved separately
from the long-lived listing catalogs. Keep each release's platform version, game
tag, exact source commit and public evidence together with its translations.

- [iOS 0.11.601](ios-0.11.601.json): game `v0.11.6.1`, relative to live
  `v0.11.5.0`; English plus the 37 non-English canonical Apple locales.
  [Independent AI review records](reviews/ios-0.11.601.json) bind the accepted
  text. AI review does not establish native-speaker validation.

Each JSON translation is plain UTF-8 text with five hyphen-prefixed bullets and a
final newline. Preserve meaning, version scope, gameplay numbers and product
names. All values must fit Apple's 4,000-character release-note field. The
`englishSource` and `translations.en` values must match exactly. Review records
must bind accepted source and translated content; a draft file or successful
upload does not establish saved, submitted or publicly displayed release notes.
