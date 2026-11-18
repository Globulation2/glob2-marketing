# Storefront translation quality audit

[Planning index](README.md) · [Canonical catalogs](../translations/README.md) · [Rollout ledger](storefront-localization-rollout.md) · [Terminology](../translations/glossary.md)

Observed **2026-11-17**. Scope: supported game languages, canonical listing coverage and linguistic quality, maintained source metadata, and the evidence needed to distinguish prepared translations from saved or public listings.

## Audit outcome

The canonical storefront catalogs cover **all 45 current game locales: English plus 44 translations**. Coverage agrees with the latest remote game `master` checked during this audit. This is not an all-language quality or public-listing signoff: independent rereading found eight field-level issues in eight languages, subsequently corrected and independently rechecked below, and initially found maintained source metadata omitted the twelve-language expansion. Destination mappings were subsequently expanded and game source integration merged as recorded below. Existing review hashes establish which text was reviewed, not that the translation is free of defects.

The initial audit changed no storefront copy. The authorized correction pass below updates canonical source catalogs; no live listing, binary declaration or release was changed by that pass. The prior platform saves and submissions retain their historical status; they are not fresh public verification.

## Source and language coverage

The remote game `master` was checked using `git ls-remote origin refs/heads/master` and fetched without checking out or resetting the working tree. Its observed tip was **`d0faaea4af903d125f23a46fdb0efd6d2e93b5df`**, committed 2026-11-17 at 19:08:24 America/Toronto. The local checkout remained `00ce510bba239e91be7d9749680e2c34df415fc6`; comparing the relevant paths to the remote tip found identical runtime roster, BCP 47 mappings and incomplete-language declarations. The source listing differences were an AppStream release-history addition and three English Android changelog files, not translated listing content. Marketing checkout and remote `main` both resolved to **`4eb7d0df287544eb02ec542cf38ea36ab8d95d9b`** before this audit record.

Authoritative runtime enumeration: [game texts.list.txt at checked master](https://github.com/Globulation2/glob2/blob/d0faaea4af903d125f23a46fdb0efd6d2e93b5df/content/data/texts.list.txt). The game loads that list in [GlobalContainer.cpp](https://github.com/Globulation2/glob2/blob/d0faaea4af903d125f23a46fdb0efd6d2e93b5df/src/app/GlobalContainer.cpp). The corresponding [online locale mapping](https://github.com/Globulation2/glob2/blob/d0faaea4af903d125f23a46fdb0efd6d2e93b5df/services/online/packages/i18n/src/locales.ts) supplies the canonical BCP 47 identifiers used by [platforms.json](../translations/platforms.json). All three sets match, with no missing or extra canonical catalog.

Current canonical set: `ar`, `pt-BR`, `ca`, `cs`, `de`, `da`, `en`, `es`, `eo`, `eu`, `fa`, `fr`, `el`, `hu`, `it`, `nl`, `pl`, `pt-PT`, `ro`, `ru`, `sl`, `sk`, `sr-Cyrl`, `fi`, `sv`, `tr`, `zh-Hant`, `zh-Hans`, `uk`, `id`, `vi`, `ja`, `ko`, `hi`, `ur`, `sw`, `bn`, `nb`, `ms`, `mr`, `ta`, `te`, `fil`, `bg`, `th`.

Non-identical game-code mappings are `br` → `pt-BR`, `cz` → `cs`, `dk` → `da`, `gr` → `el`, `pt` → `pt-PT`, `si` → `sl`, `sr` → `sr-Cyrl`, `zh-tw` → `zh-Hant`, and `zh-cn` → `zh-Hans`. These are locale equivalences, not additional languages. Brazilian/European Portuguese and Simplified/Traditional Chinese remain distinct.

The [runtime incomplete list](https://github.com/Globulation2/glob2/blob/d0faaea4af903d125f23a46fdb0efd6d2e93b5df/content/data/texts.incomplete.txt) marks every non-English language incomplete. This is a qualification on the game catalogs, separate from the 38-field storefront catalogs. Runtime availability does not establish full in-game translation or support in every submitted artifact.

## Linguistic findings and correction status

The fresh AI screening covered all **1,672 translated fields (38 × 44 catalogs)** against English and the glossary. Each issue was read against [the English master](../translations/en.md) and terminology constraints by an initial reviewer and a second agent. These are AI linguistic assessments, not native-speaker or human validation. The initial findings and correction directions below are preserved as audit history; the follow-up section records accepted replacements and renewed review evidence.

| Locale / field | Observed wording and issue | Required correction direction |
| --- | --- | --- |
| [Italian](../translations/it.md), `open_source_body` | `Un gioco di strategia da giocare, esplorare e contribuire a sviluppare.` The coordination makes `da contribuire a sviluppare` grammatically awkward. | Recast the sentence so playing, exploring and contributing to its development all have natural syntax. |
| [Portuguese Portugal](../translations/pt-PT.md), `epic_legal` | `software livre e de código aberto` states software freedom/source availability without explicitly preserving the zero-price claim. The glossary requires both meanings. | State `gratuito` explicitly alongside the freedom/open-source qualification. |
| [Romanian](../translations/ro.md), `amazon_tail` | `adversarilor de pe calculator` can mean opponents on the computer rather than computer-controlled opponents. | Name computer-controlled opponents explicitly. |
| [Tamil](../translations/ta.md), `short_pitch` | `குடியிருப்பை வளருங்கள்` pairs an accusative object with an intransitive grow verb. | Use a natural transitive expression for developing the colony and recheck the full short pitch. |
| [Hungarian](../translations/hu.md), `android_tail` | `klasszikus asztali játékot` reads as a classic tabletop game. | Express desktop/computer game, for example `klasszikus számítógépes játékot`. |
| [Slovenian](../translations/sl.md), `android_tail` | `klasično namizno igro` conventionally describes a tabletop/board game. | Express computer game, for example `klasično računalniško igro`. |
| [Simplified Chinese](../translations/zh-Hans.md), `android_tail` | `经典的桌面游戏` admits a tabletop-game reading. | Use an unambiguous computer-game expression such as `经典电脑游戏`. |
| [Ukrainian](../translations/uk.md), `amazon_feature_5` | `Грайте в карти` means play cards, changing the included-map claim. | Use playing on maps and completing campaigns, preserving that both are included. |

Vietnamese has an additional lower-severity terminology follow-up: workers varies among `nhân công`, `công nhân` and the formal `người lao động` in `amazon_feature_4`. Standardize the natural game term during the next editorial pass; this was not counted among the eight blocking field issues. This terminology follow-up was also corrected in the pass below.

The absence of an issue in another field is not proof of native fluency. Distinct translator/reviewer identities and current source/content hashes remain useful maintenance gates, but this rereading demonstrates that they cannot substitute for semantic review.

## Destination and maintained-source gaps

At initial audit, the [platform matrix](../translations/platforms.json) omitted `hi`, `ur`, `sw`, `bn`, `nb`, `ms`, `mr`, `ta`, `te`, `fil`, `bg` and `th` from every destination locale mapping. That initial omission was deliberate pending platform verification, not proof those destinations reject those languages; the follow-up below supersedes these initial export counts. Do not infer platform support or invent locale wire identifiers from catalog existence.

| Export destination | Mapped locales including English | Missing canonical locales |
| --- | ---: | --- |
| Google Play | 32 | The twelve above plus Esperanto |
| iOS / Mac App Store | 29 each | The twelve above plus Esperanto, Basque, Persian and Serbian Cyrillic |
| Microsoft | 32 | The twelve above plus Esperanto |
| Amazon | 11 | 34 locales; see matrix for the exact mapped intersection |
| Epic | 25 | 20 locales; see matrix for the exact mapped intersection |
| Snap | 1 | All 44 non-English locales; translated-field capability unverified |
| F-Droid fastlane | 33 | The twelve above |

At the checked game master, maintained Android `fastlane/metadata/android/` has 33 locale directories including English. AppStream summary/description translations and desktop comments also cover the original 32 non-English locales. All three lack the twelve added locales, although canonical source catalogs exist for them. Prepared AppStream/desktop export fragments and published downstream catalogs are different outcomes. Source changes in the game repository must follow that repository's PR/CI workflow.

## Fresh public observations

Read-only public checks on 2026-11-17 found live gaps despite the historical saved-draft evidence:

- The [US Apple page requested in French](https://apps.apple.com/us/app/globulation-2/id6817603328?l=fr-FR), [Korean](https://apps.apple.com/us/app/globulation-2/id6817603328?l=ko) and [Simplified Chinese](https://apps.apple.com/us/app/globulation-2/id6817603328?l=zh-Hans-CN) localize store interface labels but retain the English game description. The US English page also retains the historical subtitle `Strategy without busywork`. These sampled descriptions do not establish the state of every Apple territory or language, but prevent claiming the prepared translations are all live.
- The [French Microsoft page](https://apps.microsoft.com/detail/9PH4FCRMX19F?hl=fr-FR&gl=FR) now responds successfully; its pitch, screenshot captions, full description and features remain English. This supersedes the old inaccessible-page observation for this URL. The October 31 saved localization drafts do not establish public translation.
- The sampled French Google Play public package URL returned HTTP 404. This is a bounded read failure, not evidence of universal unavailability, rejection or absence of saved translations.

No authenticated console session was available for a fresh check of review locks, editable locales or saved payloads. Historical October 31 submission states in the [rollout ledger](storefront-localization-rollout.md) remain dated evidence, not present-day console claims. No listings were edited or submitted during this audit.

## Validation and follow-up

- `python3 translations/tools/storefront.py check --require-review`: passes for all 45 catalogs and their current review records.
- `python3 -m unittest discover -s translations/tests`: all 20 tests pass.
- A fresh export to `/tmp/glob2-storefront-audit-20261117` produced 192 mapped locale/destination payloads and 168 unsupported/unverified gaps across eight adapters. Counts match the destination table above. These are prepared payloads, not saved or published listings.
- The full AI text screening found no unchanged-English translation fields beyond the fixed product name; URL multisets and occurrences of the proper names River, Four Squares and Lava Shield matched the English source throughout. Those mechanical checks do not resolve the linguistic findings.
- Runtime/online/canonical locale-set comparison found 45 in each set and zero missing or extra locales; remote-master comparison confirmed the relevant language data is unchanged from the inspected checkout.

The eight field issues and Vietnamese terminology follow-up were corrected and independently rechecked in the pass below. Destination locale verification, maintained-source expansion, saved-console readback and public-display verification remain separate work. An all-language high-quality/live claim is not supported by the present evidence.

## Authorized source corrections — 2026-11-17

The correction pass changed eleven fields across nine canonical catalogs. `translation_quality` authored the replacements; `language_coverage` independently compared each exact diff to English and the glossary before accepting updated hashes. Italian now coordinates playing/exploring and contributing naturally; Portuguese legal text explicitly says `gratuito`; Romanian explicitly names computer-controlled opponents; Tamil uses transitive `வளர்க்கவும்`; Hungarian, Slovenian and Simplified Chinese explicitly say computer game; Ukrainian now says playing on maps and completing included campaigns. Vietnamese consistently uses `nhân công` in the three affected fields and retains autonomous workers guided by priorities.

The Tamil short pitch remains exactly 170 Unicode code points, meeting the existing Apple promotional-text limit without truncation. Product names, URLs, factual qualifications and untouched catalog fields remain unchanged. Updated review JSON preserves previous reviewer/translator provenance in `review_history` and records the exact changed field names; only accepted current text receives new hashes. This is independent AI review, with no human/native-speaker certification inferred.

Validation after correction: strict review-gated check passes for all 45 catalogs; all 20 unit tests pass; whitespace validation passes. The eight audited issues and lower-severity Vietnamese terminology follow-up are closed in canonical source. Historical exported files, maintained game metadata and saved/public store payloads do not update themselves; their propagation remains separately tracked in the rollout ledger. Full all-platform live signoff remains open.

## Mapping preparation follow-up — 2026-11-17

The [expanded mapping receipt](storefront-localization-rollout.md#expanded-locale-mappings-prepared--2026-11-17) documents current official sources and exact remaining gaps after checking the full roster against destination listing-language references. Preparation now covers Play 44, Apple 38 per platform, Microsoft 44, Epic 31, Amazon 11, Snap 1 and F-Droid 45 locales including English: 252 mapped payloads and 108 gaps. Play's twelve additions were also verified selectable in the authenticated console. Other hosted-store additions still require a fresh template/console check. This closes the blanket twelve-language export omission; maintained source integration and saved/public rollout remain distinct outcomes.

## Maintained source preparation and merge — 2026-11-17

The [source expansion receipt](storefront-localization-rollout.md#maintained-source-expansion-prepared-then-merged--2026-11-17) links [game PR #1825](https://github.com/Globulation2/glob2/pull/1825), preparing all 45 locales in F-Droid/AppStream/desktop metadata and the applicable corrected Android fields. Independent export comparison passes. At the initial preparation checkpoint it had not yet merged. The confirmed merge receipt below closes the source gap on master; a release and public catalog ingestion remain separate.

## Google rollout checkpoint — 2026-11-17

The [Play import checkpoint](storefront-localization-rollout.md#google-expanded-import-preview-save-blocked--2026-11-17) records successful import into an **unsaved** sixteen-language editor draft: twelve additions plus four corrected existing locales. Only English/Hindi preview triplets received exact hash comparison before the Mac locked. Save, persisted readback, review submission and public display remain unverified; the draft page is preserved pending resumed computer access.

## Google persisted correction and expansion request — 2026-11-17

The [fresh Google save/readback/submission receipt](storefront-localization-rollout.md#google-expansion-saved-freshly-verified-and-sent-for-review--2026-11-17) supersedes the unsaved checkpoint: all sixteen changed locale triplets plus English matched canonical hashes after fresh server reload (51 values). The full pending set was exactly twelve additions and four corrected full descriptions; the send confirmation and fresh Changes in review state persisted. Automated quick checks were still pending, so this is a queued-review request with no approval or public 44-locale claim. Media and policy/declaration fields remained unchanged.

## Current Apple qualification and access limits — 2026-11-17

The [current access/provenance receipt](storefront-localization-rollout.md#apple-current-gates-and-candidate-provenance-microsoft-access--2026-11-17) supersedes the October 31 Apple-state observations: iOS 0.11.500/build1002301 is Pending Developer Release, with disabled locale/description/keyword and shared-name/subtitle controls; Mac 0.11.2 remains Waiting for Review. Successful upload provenance identifies the exact tagged source and App Store eligibility. A guarded production workflow can freshly inspect/publish that exact candidate when its checks pass, but no release was dispatched or current-build gameplay qualification invented. Microsoft currently stops at sign-in, and browser ownership is with concurrent Steam work.

A fresh official Apple field-reference check also found a separate unresolved prep issue: the stated 100-byte keyword limit is not enforced by the current character-based gate, and twelve mapped locale keyword strings exceed 100 UTF-8 bytes. The rollout receipt names them. Source corrections closed the eight linguistic findings; they do not close this newly identified field-fit gap or prove Apple save/publication.

## Apple keyword fit follow-up — 2026-11-17

The [byte-limit correction receipt](storefront-localization-rollout.md#apple-keyword-byte-fit-corrected-in-source--2026-11-17) closes the newly found keyword preparation gap: fifteen oversize source fields (twelve mapped, three currently unmapped) now contain independently reviewed whole-concept adaptations within 100 UTF-8 bytes. The tooling/matrix enforce bytes only for Apple keywords and preserve character counting elsewhere. All 45 strict-reviewed catalogs, mapped-field-fit checks, 23 tests and a fresh export pass. No Apple field was applied and the existing Play submission remains unchanged.

## Final game master integration — 2026-11-17

[PR #1825](https://github.com/Globulation2/glob2/pull/1825) merged as `2c9d43da024d6cf88d7fa44f685fa8808d1a9361` after rebasing onto newer master, preserving release 0.11.6.1/iOS changes and passing the current-head fast gate. The [merge receipt](storefront-localization-rollout.md#maintained-source-expansion-merged-on-current-master--2026-11-17) records exact source/CI evidence. Runtime, online and browser rosters remain exactly 45 locales; full maintained-metadata/export comparison and protected-field checks pass, and the post-merge tree equals the tested head. The twelve-language maintained-source gap is closed on game master. This establishes merged source coverage, not released artifacts or downstream public translations.

## Final remaining-store access checkpoint — 2026-11-17

The [owner MFA handoff](storefront-localization-rollout.md#owner-mfa-handoff-for-remaining-storefronts--2026-11-17) records Microsoft email-code, Epic authenticator-app and Amazon SMS challenges in preserved Firefox tabs. The owner must complete them directly. No security settings, product editors or listing fields were changed, and no unsaved metadata form remains. This is the current access boundary for the remaining stores, separate from completed source corrections, validated exports, merged game metadata and the Play queued-review request.

## Play in-review confirmation and Epic export clarification — 2026-11-17

The [fresh Play checkpoint](storefront-localization-rollout.md#google-automated-checks-complete-actual-in-review-state--2026-11-17) now explicitly says the same sixteen changes are in review and no longer shows automated checks. This closes the queued-checks uncertainty, without approval or public-display evidence. The [Epic reconciliation receipt](storefront-localization-rollout.md#epic-current-export-structure-and-pre-application-reconciliation--2026-11-17) distinguishes its 32 locale headers from 25 populated saved locales, documents six empty expansion columns and three prior-source differences, and records current Stage Issues found. Epic preparation remains separate from an applied import or verified save.

## Epic Dev persistence confirmed — 2026-11-17

The [Epic saved/readback receipt](storefront-localization-rollout.md#epic-dev-expansion-applied-and-freshly-verified--2026-11-17) confirms 31 saved locales on all three Dev entities, with 1,736 locale cells and 392 identity/field cells exactly matching the reviewed import. The 255 intended changes contain six added languages and three prior-source corrections, with no unrelated changes. This closes Epic Dev application/readback for the prepared scope; Stage remains Issues found over separately configured EULA/Support links and no promotion or public availability is claimed. Microsoft verification requires a fresh session after an error, while Amazon remains explicitly pending at the owner's direction.

## Epic Stage review submission confirmed — 2026-11-17

The [Epic Stage/review receipt](storefront-localization-rollout.md#epic-scoped-stage-promotion-and-actual-review-submission--2026-11-17) records the two saved reviewer-link remedies and scoped promotion of three updated metadata entities. Stage has 31 locales per entity, checked by fresh counts and representative exact text/link comparisons; exhaustive CSV comparison applies to Dev only. The platform's nonselective review submission includes all five Stage entities, including unchanged regions/ratings and Windows artifact. Fresh reload confirms all five Queued for review and Live 0. No artifact/media change, approval or publication is claimed. Microsoft upload processing remains distinct from a saved/readback result; Amazon remains deferred.

## Microsoft saved localization confirmed — 2026-11-17

The [Microsoft saved-draft receipt](storefront-localization-rollout.md#microsoft-44-locale-drafts-saved-and-freshly-verified--2026-11-17) confirms all 44 locales Complete after fresh reload and exact reviewed text in all 516 non-English canonical cells. Full server comparison covered 21,744 cells; the only 84 candidate-to-server differences are new media `parentId` query values, with approved roles/order and every other URL component preserved. Existing media, flags, English caption variants and unrelated values remain unchanged. Representative Hindi media and Urdu RTL editor checks passed within their stated limits. This closes Microsoft saved-draft/readback scope; submission, publication and public layout remain unverified.

## Microsoft publishing request and final current scope — 2026-11-17

The [actual Microsoft publishing receipt](storefront-localization-rollout.md#microsoft-actual-44-locale-update-submitted-publishing--2026-11-17) supersedes the saved-only state: fresh reload shows the 44-locale Retail Update Publishing, submitted at 22:18 Toronto. Only Store listings plus mandatory unchanged Age ratings were included; the unrelated incomplete package draft and other unchanged modules were excluded. This is an actual publishing-pipeline request, without a separate approval or public-translation claim.

Current outcomes: all 45 canonical catalogs are covered; audited linguistic and Apple keyword-fit defects are corrected and independently AI-reviewed; mapped field validation, 23 tests and export pass; all 45 locales are integrated in maintained game source. Play is In review, Epic's five-entity unit is Queued (Live 0), and Microsoft is Publishing. Apple is version-state locked and Amazon explicitly deferred. No all-store public or native-speaker-quality certification is supported by these receipts. Browser work is saved with no unsaved edit outstanding; private authentication details remain excluded.

## Latest Apple preparation follow-up — 2026-11-17

The [latest Apple draft receipt](storefront-localization-rollout.md#latest-apple-editable-drafts-and-locale-intersection--2026-11-17) replaces the old locked-version checkpoint: Mac 0.11.6/build2026111801 and iOS 0.11.601/build1002501 are qualified, saved editable candidates from exact `v0.11.6.1` source, with no review submission or release yet. The fresh selector's 50 choices still intersect the game roster in exactly the existing 38 mapped locales; no configuration expansion is needed. Exact Mac runtime catalogs cover all 45 languages, while missing `CFBundleLocalizations` is a distinct Apple-facing packaging declaration gap requiring follow-up. Storefront locale application remains pending the user's review-priority choice; this receipt records no translated field writes.

## Version-specific iOS translation review — 2026-11-18

Following the user's translation-first decision, [the iOS 0.11.601 source/review receipt](storefront-localization-rollout.md#translation-first-apple-release-note-source-prepared--2026-11-18) covers the exact approved English and all 37 translated Apple locales. Independent AI review accepted every translated bullet, including numeric wall health/cost and prestige's display contribution; 38 hash-bound strings fit the field limit. This supplements the reusable listing catalogs without claiming native-speaker certification or completed store application/submission.

## French Mac saved pilot — 2026-11-18

The [fresh French Mac pilot receipt](storefront-localization-rollout.md#french-mac-pilot-saved-secure-bulk-preparation--2026-11-18) confirms canonical promotional text, description and 82-byte keywords saved by exact hashes, with existing build/media/URLs preserved. Shared English subtitle now matches the approved text; French shared/iOS work remains unfinished. Native bulk entry stopped at the actual computer-control rate limit, with a clean saved form. Reviewed 38-locale release-note source is ready, while the secure helper remains implementation work with no API write or new live workflow claimed. Neither latest Apple version has been submitted for review.

## Microsoft sampled public availability — 2026-11-18

[Fresh public French/France and Hindi/India checks](storefront-localization-rollout.md#microsoft-public-french-and-hindi-text-verified--2026-11-18) now match eleven canonical product-copy fields each, including full descriptions, features and ordered screenshot captions. This is public localized content and supersedes the prior French English-fallback finding. Coverage is bounded to those two locale/market samples; all-44 availability and visual-layout certification remain unclaimed.
