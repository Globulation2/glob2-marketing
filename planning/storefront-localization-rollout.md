# Canonical storefront localization rollout

[Planning index](README.md) · [Canonical catalogs](../translations/README.md) · [Approved English presentation](approved-storefront-rollout.md) · [Media audit](../translations/media-audit.md)

Observed **2026-10-31**. This ledger distinguishes reviewed source files, extracted forms, saved drafts, submitted updates and public availability. Translation targets match the game's 32 non-English languages; English remains the source language. Platform locale support is a separate constraint. No game-language declarations, prices, regions, ratings, builds or review responses are changed by this localization work.

## Current platform evidence

| Destination | Actual observed state | Localization action / gate |
| --- | --- | --- |
| Google Play | Initial audit found the existing default listing Live in console and English U.S. only; 31 locale additions are now saved and in review. Language manager exposes target locale choices except Esperanto. Title/short/full limits 30/80/4000. Current closed-test production eligibility remains separate. | 31 non-English locale additions saved and submitted. Fresh-server readback verified all 32 locale field triplets (English plus 31 translations) against canonical SHA-256 values. Final fresh overview confirms “Your changes are now in review”; automated quick checks have finished. No approval/public-display claim. |
| Snap | Authenticated editor shows one Title/Summary/Description, approved English text and website; Save disabled. No localized-field controls observed. | Retain approved English; native translated-listing capability unverified. Canonical catalogs remain usable for AppStream/downstream sources. Do not concatenate languages into a single listing. |
| iOS App Store | 0.11.400 Waiting for Review. Product-page locale selector explicitly disabled; existing English text fields remain editable. | New locales blocked by the current UI state. Do not cancel review to add them. |
| Mac App Store | 0.11.2 Waiting for Review. Product-page locale selector explicitly disabled. | New locales blocked by current UI state. Preserve automatic release after approval. |
| Shared Apple App Information | Locale selector disabled; changes released with next version. Existing subtitle is historical `Strategy without busywork`, distinct from the approved-source subtitle being localized. | Coordinate iOS/Mac shared name/subtitle changes as one unit when editable; adding a locale can affect both platforms. |
| Microsoft Store | Retail Publishing continues. Initially English U.S. only; 31 translated listings plus English now persist as 32 Complete locales. | Exact saved export verified 31 × 12 canonical text fields, unchanged English/identifiers/unrelated values, and identical source media references apart from per-locale parent IDs. Publish disabled until in-progress submission publishes; no cancellation. |
| Amazon Appstore | Initially SUBMITTED, subsequently observed Under Review; English U.S. only. All listing text and Add localization explicitly disabled. Observed title/short/full limits 200/1200/4000; up to 10 feature bullets. | Wait for current review to finish, then submit metadata-only localized update. Do not cancel submission. |
| Epic Games Store | Existing Stage entities advanced from Queued to In review; Dev Push to Stage remains disabled because product is under review; Live 0. All three Dev entities now have English plus 24 intended locales. | Corrected CSV applied successfully in Dev; fresh server export exactly matched all 1,400 locale cells and all 56 row identities. No Stage promotion or cancellation. Existing review must finish before localized Dev changes can be promoted/submitted. |
| SourceForge | Earlier access recovery gap remains unresolved; no new editor-access evidence. | Access-dependent handoff; no live edit claim. |
| Steam / GOG / itch.io | Controlled listing identity and editor access remain unresolved in the rollout source record. | Verify existing product/account before applying; no new enrollment, agreements or fees inferred. |
| AppStream / F-Droid / downstream catalogs | [Upstream PR #1296](https://github.com/Globulation2/glob2/pull/1296) merged as `f5272df9776818fd1798d5369f5139c383333242`: 99 source files / 32 locales. Downstream ownership and acceptance differ by ecosystem. | Record upstream source changes separately from catalog publication. Flathub's documented human-authored first-submission condition remains unchanged. |

## Platform references

- [Google locale choices](https://support.google.com/googleplay/android-developer/answer/9844778?hl=en), [field limits and shared-track listing](https://support.google.com/googleplay/android-developer/answer/9859152?hl=en). Text translations can inherit default graphics.
- [Apple localization workflow](https://developer.apple.com/help/app-store-connect/manage-app-information/localize-app-information), [supported locales](https://developer.apple.com/help/app-store-connect/reference/app-information/app-store-localizations), [review-state editing rules](https://developer.apple.com/help/app-store-connect/reference/app-information/app-and-submission-statuses/). Store languages differ from binary languages.
- [Microsoft localized listings](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/add-and-edit-store-listing-info). The current gaming product's actual console/template governs its fields.
- [Amazon locale support](https://www.developer.amazon.com/docs/app-submission/distribute-your-app-internationally.html), [review locks and metadata-only updates](https://www.developer.amazon.com/docs/app-submission/update-published-app.html). The prose locale list and embedded console screenshot differ for some regional English/Spanish variants; inspect the live enabled selector before adding those variants.
- [Epic locale identifiers](https://dev.epicgames.com/docs/epic-games-store/store-presence/localize/supported-languages), [template/review workflow](https://dev.epicgames.com/docs/epic-games-store/store-presence/localize/localize-text?lang=en-US).
- [Snap listing documentation](https://forum.snapcraft.io/t/store-listing-and-branding/16397) documents default fields; native multilingual publishing is not established by that page.

## Access and verification boundaries

Existing gcloud CLI authentication and a configured project were available; Cloud Translation API was already enabled. No API, billing, identity or access setting was changed. The team used existing Google Cloud Translation for initial drafting of 16 catalogs, followed by independent review; this does not assert a zero charge. The existing gcloud OAuth token lacks Android Publisher scope, so it was not repurposed for Play listing writes or expanded silently. No credentials or private console identifiers are stored here.

For each editable platform, compare exact reviewed payloads with current fields, apply only intended locales/fields, save, reload from the server and compare again. Before submission, inspect the complete pending-change set to exclude unrelated concurrent work. Record review/approval/public-display receipts separately. Active platform reviews are preserved.

## Google saved localization batch — 2026-10-31

The console's **Import translations with AI** flow accepted the existing reviewed translations as a 31-language JSON file. It detected exactly the intended 31 supported non-English languages; Esperanto is unsupported. Every preview's name, short description and full description was compared with the reviewed payload by SHA-256 over the three exact UTF-8 values. Thirty matched; the French preview had introduced `bâtiti` in place of canonical `bâti`. The full French description was corrected in the unsaved editor, then all three French field values matched the canonical hash. The canonical catalog was not changed to match the extraction.

The mandatory new **AI asset declaration** was answered from the existing [approved artwork provenance](../assets/storefront-approved-v1/mobile-promo/README.md). **Only `feature-graphic-1024x500.png`** was selected as created/edited using AI. The existing app icon and four native phone screenshots were unselected. This is an evidence-backed required declaration for the existing illustrated promotional derivative, not an image replacement or an assertion that native gameplay captures were generated. [Google's declaration guidance](https://support.google.com/googleplay/android-developer/answer/17262077?hl=en) was checked the same day.

**Save** completed and the console displayed **Change saved. Send for review in Publishing overview.** The entire pending-change table contains **exactly 31 Add language entries** under Default store listing, with no English-default, package, track or tester changes. Managed Publishing remains Off. Automated checks were running with up to 14 minutes remaining. This establishes a saved localization batch, **not a submitted review, approval or public localization**. Fresh-server exact-field readback is still required before the intended review submission.

## Google fresh readback and actual review request — 2026-10-31

A new server load of the listing editor was used to traverse **all 32 stored locales**: unchanged English U.S. plus the 31 new translations. For each locale, the actual name, short description and full description values matched the exact reviewed payload SHA-256, including the corrected French field. Thus **96 stored text values** were verified; the original English source remained unchanged.

Publishing overview was rechecked with **exactly 31 Add language rows**, Managed Publishing Off, and no unrelated package/track/tester/default-English changes. The **Send changes for review** confirmation was completed. A fresh server reload verifies **Changes in review** and **Remove changes**. The console says automated quick checks are running and changes will be sent for review when checks succeed. This is a persisted review request/queued-checks state, **not completed platform review, approval, production-track access or public localization**. The earlier attempt without a persisted state was inspected and did not establish a submission; only the fresh confirmed state is counted.

## Microsoft saved locale drafts; existing publish lock — 2026-10-31

The actual current Microsoft spreadsheet template was exported and used to build a locale-only import. The server finished processing it. Fresh reload plus a fresh server export verified **31 translated listings plus unchanged English, all 32 Complete**. All **31 × 12 canonical text fields** matched reviewed source values; IDs, type rows, English and unrelated values remained unchanged.

The 217 localized media references (seven roles × 31) retain the same source asset type, host/path, remaining query values and order; only their locale-specific parent IDs differ. This verifies retained source references, not independent image-byte downloads. The saved Arabic listing was also visually checked in the actual editor: four approved gameplay placements plus poster, box art and 16:9 promotional image match the approved family. This representative seven-role comparison does not claim separate pixel checks for all 31 languages.

The actual Review and publish screen explicitly disables Publish with **“You have an in-progress submission. You can't publish until the in-progress submission has been published.”** No existing submission was cancelled, withdrawn or modified to bypass this gate. This establishes **saved and verified localization drafts**, not a second submission or public translated listings. After the existing Retail Publishing unit completes, these drafts require their own allowed review/publish action.

## Epic first template validation — 2026-10-31

The existing Dev upload accepted the first UTF-8 CSV for processing, then reported **142 issues** and no successful import/save. The inspected Arabic Store Configuration preview explicitly marked developer name, publisher name and technical-requirement values as required but absent; the translated marketing body rendered correctly. The upload summary also included unused locale columns. [Epic's template instructions](https://dev.epicgames.com/docs/epic-games-store/store-presence/localize/localize-text?lang=en-US) explicitly require removing unused locale columns before upload.

A corrected template preserves all 56 rows, English content and metadata identities, removes seven unused columns, supplies exact existing English names/URLs/technical values in the 24 intended locales, and retains all 600 reviewed marketing-cell translations. Technical prose is retained from the approved existing English source, not represented as newly translated or newly qualified requirements. This preparation was followed by the successful applied/readback result below. Stage review was not rescinded or replaced.

## Epic corrected import applied and freshly verified — 2026-10-31

The reviewed second CSV completed processing with **“Localized content has been applied.”** The console applies this import directly to Dev; no further Save action was offered. A fresh server reload showed **25 locales on each of the three entities**: unchanged English plus exactly the 24 intended supported translations, with none of the seven removed unused locale columns added.

A new all-three-entity template was downloaded from the server and compared with the reviewed import: **56 rows, unchanged seven-column row identities, 25 locale columns and 1,400 exact cell comparisons; zero differences**. This includes all 600 reviewed marketing translations and 408 invariant existing-English fallback values. Developer/publisher names, URLs and technical requirement prose remain exact existing source values; the fallback technical prose is not represented as translated. The fresh export SHA-256 is `d26e677cb3fb808a7d0a9930b61bec42d9fc306539f97e8f298743a2e0855bdc`.

The current Stage entities advanced independently to **In review**. **Push to Stage remains disabled** with “This product is under review and cannot be pushed to Stage”; Live remains 0. No Stage promotion, review withdrawal, binary change or public localization is claimed. After the existing review unlocks promotion, the exact saved Dev translations still require their own Stage/review/publication progression.

## Final Google review checkpoint — 2026-10-31

The final publishing overview now explicitly states **“Your changes are now in review. We may find additional issues when reviewing your app.”** The automated quick-check message is gone; the same **31 Add language** rows remain under Changes in review, with Managed Publishing Off. This supersedes the earlier queued-checks checkpoint. Platform approval, public translated display and production-track eligibility remain unverified.

## Existing-account authentication check — 2026-10-31

Snap already has authenticated listing access; its multilingual-field capability is the unresolved question. SourceForge's observed login page offers username/password, with no Google SSO shown. After the earlier matching-site menu check, the actual Bitwarden vault loaded without an unlock challenge. Full-vault searches for **sourceforge** and **sf.net** each returned **No items match your search**. An existing SourceForge credential still needs to be located or entered by the owner; no reset or new account was attempted.

The itch.io dashboard redirected to login, offering username/password or **Log in with GitHub**, with no Google SSO shown. The loaded vault's exact **itch.io** search found no matching item. Existing itch account identity/project control remains unverified; no GitHub account linking or signup was attempted.

A saved Steam login was found and directly autofilled into the Steamworks sign-in, using **Autofill only** without changing saved site associations. The submitted existing login reached an **email verification-code challenge**. Email verification remains pending before publisher-role or Glob2 project-edit access can be checked. No code or password is recorded here; reaching this challenge does not establish Steamworks product control.

These resumed checks supersede the earlier temporary deferral during GOG authentication. GOG's earlier application is known; publisher-role/product access remains unverified as recorded in [GOG readiness](gog-release-readiness.md). GOG tabs were preserved. No new account, reset, enrollment, fee, agreement, permission change or listing edit resulted from this audit.
