# Canonical storefront localization rollout

[Planning index](README.md) · [Canonical catalogs](../translations/README.md) · [Approved English presentation](approved-storefront-rollout.md) · [Media audit](../translations/media-audit.md)

Observed **2026-10-31**. This ledger distinguishes reviewed source files, extracted forms, saved drafts, submitted updates and public availability. The original translation batch matched the game's then-current 32 non-English languages; the November 1 expansion below brings the current target to 44. English remains the source language. October 31 platform counts below remain historical observations, not counts for the expanded roster. Platform locale support is a separate constraint. No game-language declarations, prices, regions, ratings, builds or review responses are changed by this localization work.

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
| Steam / GOG / itch.io | Steam account sign-in succeeded, but its dashboard shows incomplete partner onboarding rather than a product list. GOG publisher/product access and itch account/project identity remain unresolved. | No controlled Glob2 editor verified on these destinations. Existing-product access must be established before applying; no new enrollment, agreements or fees inferred. |
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

A saved Steam login was found and directly autofilled into the Steamworks sign-in, using **Autofill only** without changing saved site associations. The submitted existing login reached an **email verification-code challenge**. The user completed email verification, and the actual signed-in Steamworks dashboard was then inspected. It offers **Continue the Onboarding Process**, says further steps are needed to finish onboarding, and separately requires signing an SDK Access Agreement for preliminary SDK access. No publisher product list or Glob2 editor was exposed to this account. Successful account authentication therefore does not establish Glob2 listing control. No onboarding continuation, agreement, fee or product creation was attempted; no code or password is recorded here.

The [November 17 Steam account/pipeline checkpoint](approved-storefront-rollout.md#steam-account-and-build-pipeline-checkpoint--2026-11-17) records the subsequent explicit setup request, restored authenticated access, the submitted corporate legal-entity correction request awaiting Valve, incomplete Payment & Tax Info and technical configuration gaps. The October 31 observations above remain historical.

These resumed checks supersede the earlier temporary deferral during GOG authentication. GOG's earlier application is known; publisher-role/product access remains unverified as recorded in [GOG readiness](gog-release-readiness.md). GOG tabs were preserved. No new account, reset, enrollment, fee, agreement, permission change or listing edit resulted from this audit.

## Game-language expansion — 2026-11-01

The current game roster adds **Hindi (`hi`), Urdu (`ur`), Swahili (`sw`), Bengali (`bn`), Norwegian Bokmål (`nb`), Malay (`ms`), Marathi (`mr`), Tamil (`ta`), Telugu (`te`), Filipino (`fil`), Bulgarian (`bg`) and Thai (`th`)**, bringing the canonical target to **44 non-English languages plus English**. Public source evidence is the game’s [locale map](https://github.com/Globulation2/glob2/blob/master/platform/packages/i18n/src/locales.ts) and [native text list](https://github.com/Globulation2/glob2/blob/master/data/texts.list.txt), with additions in commits [e67cba82e7](https://github.com/Globulation2/glob2/commit/e67cba82e7) (Hindi, Urdu and Swahili, October 31), [b9b1a4b7e1](https://github.com/Globulation2/glob2/commit/b9b1a4b7e1) (Norwegian Bokmål), [ffabe1b9ef](https://github.com/Globulation2/glob2/commit/ffabe1b9ef) (Malay), and [1bb5155e96](https://github.com/Globulation2/glob2/commit/1bb5155e96) (Bengali, November 1). Further November 1 additions are [a9db70d65c](https://github.com/Globulation2/glob2/commit/a9db70d65c) (Marathi), [0a5d4f68d9](https://github.com/Globulation2/glob2/commit/0a5d4f68d9) (Tamil), [f36de73aea](https://github.com/Globulation2/glob2/commit/f36de73aea) (Telugu), [0b6a9fe67b](https://github.com/Globulation2/glob2/commit/0b6a9fe67b) (Filipino), [0a38a29ed2](https://github.com/Globulation2/glob2/commit/0a38a29ed2) (Bulgarian), and [8d5293c436](https://github.com/Globulation2/glob2/commit/8d5293c436) (Thai). The observed game source at `8d5293c436` registers 45 total languages. Source support is separate from language availability in any submitted binary.

The twelve new catalogs use the unchanged 38-field [English master](../translations/en.md), approved colony/economy message, edition-specific qualifications, exact URLs and protected names. All twelve new catalogs have been translated and independently reviewed by separate agents against all 38 fields; current hash-bound review records determine readiness. Review corrections included natural campaign terminology, contested-territory wording and faithful short-field adaptations for character limits. No human or native-speaker validation is claimed. Existing English and the 32 prior translations are retained.

Canonical roster and upstream AppStream/desktop fragment mappings include all twelve additions. Store-specific console mappings and F-Droid locale directories for the twelve remain unverified and are intentionally absent; export gap reports must retain these gaps. No additional storefront save, review submission, public translation, source-repository merge or catalog publication is established by preparing the new catalogs. Existing October 31 rollout receipts and active reviews remain unchanged.

Validation on November 1: the strict review gate validates **45 canonical catalogs** (44 non-English plus English), all **20 tooling tests pass**, and whitespace checks pass. A fresh review-gated export succeeds with 45-language AppStream and desktop merge fragments. Existing store mappings prepare 192 listing payloads and retain 168 unsupported/unverified platform-locale gaps, including 96 gaps for all twelve new locales across the eight destination adapters. These are explicit preparation gaps, not translation omissions or platform rejections. Export artifacts remain outside the public repository; no live listing update resulted from this expansion.

## Canonical quality corrections — 2026-11-17

The [translation quality audit](storefront-translation-quality-audit.md#authorized-source-corrections--2026-11-17) identified and closed eight linguistic issues and a Vietnamese terminology follow-up. Eleven fields in nine source catalogs (`hu`, `it`, `pt-PT`, `ro`, `sl`, `ta`, `uk`, `vi`, `zh-Hans`) were corrected, independently reread against English/terminology, and bound to updated review hashes with prior provenance retained. Strict review validation and all 20 translation tests pass.

This establishes corrected reviewed canonical source, not changes to saved drafts, submissions or public listings. Existing payloads must be regenerated and compared before applying the affected fields through the platform's current editable state. Fresh public Apple/Microsoft samples and twelve-language source/mapping gaps are described in the audit; the October 31 console states remain historical until a new authenticated readback establishes their current state.

## Expanded locale mappings prepared — 2026-11-17

A current official-documentation check compared the complete 45-locale canonical roster with each destination's listing-language reference. The twelve expansion catalogs now have explicit preparation mappings wherever the reference establishes identifiers. This supersedes the earlier intentional omission, without establishing a saved listing or binary-language declaration.

| Destination | New canonical → destination mappings | Prepared total including English | Remaining canonical gaps |
| --- | --- | ---: | --- |
| Google Play | `hi`→`hi-IN`, `ur`→`ur`, `sw`→`sw`, `bn`→`bn-BD`, `nb`→`no-NO`, `ms`→`ms`, `mr`→`mr-IN`, `ta`→`ta-IN`, `te`→`te-IN`, `fil`→`fil`, `bg`→`bg`, `th`→`th` | 44 | `eo` |
| iOS / Mac | `hi`→`hi`, `ur`→`ur-PK`, `bn`→`bn-BD`, `nb`→`no`, `ms`→`ms`, `mr`→`mr-IN`, `ta`→`ta-IN`, `te`→`te-IN`, `th`→`th` | 38 each | `eo`, `eu`, `fa`, `sr-Cyrl`, `sw`, `fil`, `bg` |
| Microsoft | The twelve canonical codes map to identical generic codes, including `nb` | 44 | `eo` |
| Epic | `hi`→`hi`, `nb`→`no`, `ms`→`ms`, `fil`→`fil`, `bg`→`bg`, `th`→`th` | 31 | `ca`, `eo`, `eu`, `fa`, `el`, `sl`, `sk`, `sr-Cyrl`, `ur`, `sw`, `bn`, `mr`, `ta`, `te` |
| F-Droid source | The twelve canonical BCP 47 codes map to identical neutral directory names | 45 | None in source export |
| Amazon / Snap | No new mapping established | 11 / 1 | Existing matrix gaps remain |

Sources observed 2026-11-17: [Google's listing-language code table](https://support.google.com/googleplay/android-developer/answer/9844778?hl=en), [Apple's supported listing languages](https://developer.apple.com/help/app-store-connect/reference/app-information/app-store-localizations) and [metadata shortcodes](https://developer.apple.com/documentation/appstoreconnectapi/managing-metadata-in-your-app-by-using-locale-shortcodes), [Microsoft listing API language codes](https://learn.microsoft.com/en-us/windows/apps/publish/store-submission-api#languages), [Epic storefront codes](https://dev.epicgames.com/docs/epic-games-store/store-presence/localize/supported-languages?lang=en-US), and [F-Droid Fastlane directories](https://f-droid.org/en/docs/All_About_Descriptions_Graphics_and_Screenshots/#fastlane-structure) with [BCP 47 localized metadata keys](https://f-droid.org/en/docs/Build_Metadata_Reference/). [Amazon's international listing reference](https://www.developer.amazon.com/docs/app-submission/distribute-your-app-internationally.html) provides no added intersection. The old Microsoft `supported-languages` URL currently redirects to package requirements; it is retained as historical provenance, while the explicit listing API code table supports the new preparation mappings.

The authenticated Google language selector also confirmed all twelve exact identifiers on 2026-11-17: they were available and unchecked; 32 locales were selected. Neutral Malay `ms` and regional `ms-MY` are distinct choices, so canonical `ms` uses the neutral option. This establishes selectable locales, not application/save/readback. Apple, Microsoft and Epic additions remain preparation candidates requiring reconciliation with a fresh console/template before upload. Epic's formerly discarded six supported columns must now be retained when present in a fresh template; Greek and the other unmapped canonical languages remain absent from its documented table. No new language is inferred for Snap.

A fresh review-gated export at `/tmp/glob2-storefront-expanded-20261117` contains **252 mapped locale/destination payloads and 108 explicit gaps** across eight adapters, up from 192/168 before this change. F-Droid now exports all 45 source directories; incorporation in game master, release selection and downstream ingestion remain separate. No game source or public listing is changed merely by this matrix/export preparation.

## Maintained source expansion prepared, then merged — 2026-11-17

[Game PR #1825](https://github.com/Globulation2/glob2/pull/1825), source commit `16f8eda485`, prepares the reviewed translations in maintained game metadata: twelve new F-Droid directories with three fields each; corrected existing Hungarian, Slovenian, Vietnamese and Simplified Chinese Android descriptions; AppStream summary/description/captions for all 45 locales; and twelve new desktop comments. The release-maintenance guide now describes the 44 translated catalogs and source/console locale distinction. The PR changes 43 files.

Independent read-only review compared the prepared tree to the stable reviewed export: 135 exact F-Droid text files, 45 distinct AppStream summaries, 225 paragraphs, 180 captions across the existing four screenshots, and 45 desktop comments. Existing release history, screenshot URLs, launcher settings and Android changelogs remain unchanged. XML and whitespace checks pass. At that initial checkpoint the PR was open and awaiting its required fast CI gate. The confirmed merge below supersedes the open-PR state; it remains separate from a product release or downstream catalog publication.

## Google expanded import preview; save blocked — 2026-11-17

The authenticated Play editor showed the existing listing Live with 32 saved locales. The console accepted the reviewed sixteen-language import: twelve new locale additions plus corrected existing `hu`, `sl`, `zh-Hans` (Play `zh-CN`) and `vi` payloads. Its success banner stated **“Translated assets in 16 languages were successfully imported”**. This is an **unsaved editor import**, not sixteen saved/persisted localizations.

The imported payload file remained outside the public repository; its SHA-256 was `ac0e38d38098aa5afc21488a3139afb276cb2c90e4264419ae169d8f99d472dd`. Before computer access stopped, exact title/short/full preview values for English and Hindi matched the canonical triplet hashes. The other fifteen non-English previews were not fully verified. No Save action, fresh persisted-server readback or review submission occurred at this checkpoint.

The Mac subsequently locked and automatic unlock failed, blocking further computer interaction; the user was asked to unlock it. Preserve the existing Firefox draft page for continuation. The prior 32-locale saved listing and the new unsaved sixteen-language import are separate states. Do not count these twelve additions or four corrections as saved, submitted, approved or publicly displayed until those outcomes are independently verified.

## Google expansion saved, freshly verified and sent for review — 2026-11-17

After computer access resumed, all sixteen imported locale title/short/full triplets were compared with the reviewed canonical payload. The AI import had changed Tamil `வெவ்வேறு` to `வெவ்வேறான` in two occurrences; both were restored to the canonical wording before saving. **Save as draft** returned **“Your changes have been saved”**. A fresh server reload then verified all sixteen locale triplets plus unchanged English: **51 exact text values** by SHA-256. The corrected Tamil text persisted. This supersedes the unsaved-only checkpoint above.

The review-step Save succeeded. Publishing overview's entire pending set contained **exactly twelve Add language rows and four Change full description rows**, with no unrelated fields: additions `hi-IN`, `ur`, `sw`, `bn-BD`, `no-NO`, `ms`, `mr-IN`, `ta-IN`, `te-IN`, `fil`, `bg`, `th`; existing-description corrections Hungarian, Slovenian, Vietnamese and Simplified Chinese (`hu-HU`, `sl`, `vi`, `zh-CN`). Existing media, policy answers and the AI asset declaration were retained unchanged.

The actual send confirmation completed with **“16 changes sent for review”**. A fresh reload showed **Changes in review**, the same sixteen rows and Managed Publishing Off. Automated quick checks were still running, with up to fourteen minutes remaining. This is a **persisted queued-review request**, not completed checks, completed review, approval or public display of 44 localized listings. The submitted values come from the reviewed export snapshot `/tmp/glob2-storefront-expanded-20261117`; the external sixteen-language import file fingerprint remains `ac0e38d38098aa5afc21488a3139afb276cb2c90e4264419ae169d8f99d472dd`. Preserve a later check/approval/publication receipt separately.

## Apple current gates and candidate provenance; Microsoft access — 2026-11-17

Fresh authenticated Apple inspection shows **iOS 0.11.500 / build 1002301 Pending Developer Release**, older **0.11.400 Ready for Distribution**, and **Mac 0.11.2 Waiting for Review**. The current iOS product-page language selector, description and keywords are disabled. Shared App Information's language selector, Name and Subtitle are also disabled; the historical subtitle remains. No release, cancellation or Apple metadata edit occurred. Microsoft returned an account sign-in page rather than a product/editor, so its current saved submission/editability remains unknown. Native browser ownership was handed to the concurrent Steam work; further browser operations wait for handback.

The iOS candidate is traceable, rather than an unidentified replacement. Successful [trusted mirror upload run 43544438191](https://github.com/genixpro/glob2-release/actions/runs/43544438191) retains the small `ios-upload-provenance` artifact. Its exact record identifies **tag `v0.11.5.0`**, **source `11d46bdd48eff8d9233b2e66e7536726fc260d3f`**, **marketing version `0.11.500`**, **build `1002301`**, bundle `org.globulation2.glob2`, and `appStoreEligible: true`; archive binary SHA-256 is `9936ba601443f7c593adb3c55f16a7fefdaf0e6400e718154f25eb6fb91fe519`. The upload used the external audience. [Read-only inspect run 43611649089](https://github.com/genixpro/glob2-release/actions/runs/43611649089) subsequently reported that exact version/build attached with manual release and Waiting for Review. The fresh UI Pending Developer Release state is later evidence of the Apple approval/manual-publication gate, not proof that publication was requested.

The [maintained production guide](https://github.com/Globulation2/glob2/blob/master/docs/releases/ios-production.md) and driver provide a concrete guarded continuation: first inspect the same tag/upload-run provenance, then consider the separately authorized `publish` stage only after fresh API validation of the exact attached manual version, `PENDING_DEVELOPER_RELEASE`, processed/eligible build, `expired: false` and resolved encryption declaration. This audit dispatched neither stage. Historical physical-device video in this repository covers build 1002101, not 1002301; no current-build device gameplay qualification was found or inferred. Existing provenance and platform approval do not justify relabelling that old evidence.

[Apple's manual-release reference](https://developer.apple.com/help/app-store-connect/manage-your-apps-availability/select-an-app-store-version-release-option/) treats Pending Developer Release as an approved version awaiting a deliberate release, with public appearance potentially delayed. [Platform-version metadata](https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information) ties localization editability to app state. Publication is a product-release action, not a guaranteed way to unlock description/keyword edits on the same version. No cancellation, invented new version or blind release is performed solely to bypass the localization gate; an editable version and a truthful artifact check remain separate from prepared translations.

That same metadata reference states a **100-byte keywords limit**. A bounded follow-up check found twelve mapped Apple source keyword strings currently exceed 100 UTF-8 bytes despite passing the existing character-based gate: `ar`, `el`, `ru`, `uk`, `vi`, `ja`, `hi`, `bn`, `mr`, `ta`, `te`, `th`. This is an unresolved preparation/validation gap, not saved Apple data. The limit interpretation and affected adaptations require correction before those fields are applied.

## Apple keyword byte fit corrected in source — 2026-11-17

The [current Apple field reference](https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information) specifies 100 bytes for Keywords. The platform schema now supports explicit `length_unit: byte` (UTF-8) or `character` (backward-compatible default); only Apple keyword fields use byte counting. Both strict check and export enforce mapped destination fit. Other field limits retain character counting. Unknown length units fail explicitly, and values are never truncated.

The complete 44-translation audit found fifteen oversize `ios_keywords` fields: twelve currently mapped to Apple plus `fa`, `sr-Cyrl` and `bg`, whose Apple destinations remain unsupported/unverified. All fifteen were adapted by selecting whole existing localized concepts. Strategy, RTS and colony remain the first three terms; no new keyword concepts, partial words or broken UTF-8 sequences were introduced. Long lower-priority terms were omitted where necessary. English and every non-keyword catalog field remain unchanged in this pass.

| Locale | Previous UTF-8 bytes | Corrected UTF-8 bytes |
| --- | ---: | ---: |
| ar | 124 | 83 |
| bg | 132 | 99 |
| bn | 185 | 91 |
| el | 170 | 79 |
| fa | 118 | 92 |
| hi | 164 | 79 |
| ja | 112 | 87 |
| mr | 164 | 82 |
| ru | 123 | 97 |
| sr-Cyrl | 129 | 88 |
| ta | 218 | 100 |
| te | 185 | 91 |
| th | 187 | 94 |
| uk | 125 | 99 |
| vi | 118 | 85 |

`translation_quality` authored the adaptations; `language_coverage` independently checked the exact diffs against English and original concept lists, then renewed hashes with prior provenance retained in review history. This is AI review, not native-speaker validation. All 45 catalogs now pass strict review and mapped-field-fit checks. All 23 tests pass, including multibyte character-versus-byte behavior, exact byte boundary, unknown-unit rejection and check/export rejection before output. A fresh export at `/tmp/glob2-storefront-keyword-fit-20261117` succeeds with the same 252 mapped payloads and 108 gaps.

This closes the newly found keyword source/validation gap. No Apple field was applied because its observed edit controls remain disabled; no new Apple save or submission is inferred. Google Play payload values and the already submitted sixteen-change batch are unaffected because Apple keywords are not part of that adapter. Existing export snapshots remain historical; use the fresh byte-validated export for later Apple preparation.

## Maintained source expansion merged on current master — 2026-11-17

[Game PR #1825](https://github.com/Globulation2/glob2/pull/1825) **merged** as **`2c9d43da024d6cf88d7fa44f685fa8808d1a9361`**, recorded at 2026-11-18 02:24:39 UTC (2026-11-17 21:24:39 America/Toronto). The first tested head passed its gate, then required pre-merge fetch found newer master `1b60514218` with release 0.11.6.1/iOS changes. The worker rebased cleanly, preserved those changes, repeated focused checks and pushed tested head `c36f8f300e`. Its current-head fast gate passed: contracts 2m10s, Linux 17m15s and master-health 1m33s. Final pre-merge fetch found master unchanged; the post-merge tree equals the tested head and the source worktree was clean.

The final runtime, online and browser locale rosters each contain exactly 45 locales. Full source metadata/export and protected-field checks pass: F-Droid's 135 exact text files, AppStream's 45 summaries/225 paragraphs/180 captions, and 45 desktop comments preserve release history, images, launcher settings and changelogs. This **closes the twelve-language maintained-source gap on game master** and integrates the applicable corrected Android descriptions. It does not prove those sources are in a released artifact, selected by F-Droid ingestion or publicly displayed downstream.

The independent Apple keyword-only corrections live in marketing commit `2b14393`; they do not alter these game metadata payloads or the already submitted Play batch. The newer release/iOS source changes also mean the older Apple 0.11.500 candidate must not be presumed the current release choice. Microsoft currently requires an owner email code and Epic an owner authenticator challenge; no listing writes occurred at those gates. Public rollout, Apple editability and current artifact qualification remain separate from merged source.

## Owner MFA handoff for remaining storefronts — 2026-11-17

The final access checks reached genuine second-factor challenges after existing saved credentials: **Microsoft requires an email code**, **Epic requires an authenticator-app code**, and **Amazon requires an SMS code**. The owner was asked to enter these directly in the preserved Firefox tabs. Amazon's **“Don't require code”** option remains unchecked; no security setting was changed. Codes, email/phone details and credentials are excluded from this public record.

No product editor, listing write or unsaved metadata form was reached on these three stores. The concurrent Steam support submitted tab remains preserved. Further storefront application depends on the owner completing those challenges and a fresh product/editor preflight; this handoff is not evidence of saved translations, submission, approval or public display. Independent canonical-copy, tooling and merged-source work is complete as recorded above.

## Google automated checks complete; actual in-review state — 2026-11-17

A fresh Publishing overview now explicitly states **“Your changes are now in review”**. The automated quick-check message is gone and the same sixteen change rows remain. This supersedes the queued-checks qualification in the prior receipt: the twelve additions and four description corrections are now in review after checks. Platform approval, publication and public 44-locale display remain unverified.

## Epic current export structure and pre-application reconciliation — 2026-11-17

A current server export retains SHA-256 `d26e677cb3fb808a7d0a9930b61bec42d9fc306539f97e8f298743a2e0855bdc`. Precise CSV structure: **39 columns: seven identity/field columns plus 32 locale headers**. The historical **25 locales** count means populated saved locales (English plus 24 translations), not total exported header count. Seven additional headers are empty placeholders. Six (`bg`, `fil`, `hi`, `ms`, `no`, `th`) now have reviewed canonical mappings and can receive prepared translations; the unused `es` placeholder is empty and is removed only from the upload copy, preserving the original server export.

Reconciliation found exactly three differing nonempty canonical cells, each matching the prior reviewed source at marketing commit `6528f61`: Vietnamese `listing_intro` in two rows and Portuguese Portugal `epic_legal` in one. This ties the differing saved text to the previous approved catalog rather than authorizing a blind overwrite. Preparation includes 150 new canonical cells plus required invariant English fallbacks for the six added locales and those three reviewed corrections. No applied/save/readback outcome is claimed at this checkpoint.

The current Epic Stage state is **Issues found**, superseding the older In review observation. Its details are being inspected; no new Stage promotion, review submission or publication is inferred from template preparation.

## Epic Dev expansion applied and freshly verified — 2026-11-17

The owner completed Epic MFA. The independently verified localization candidate (SHA-256 `b810121833b7538079ac0bf8bb4dcfbf4ced340e87e703ab6364d0d13f6988e1`) was imported and the console returned **“Localized content has been applied”**. Fresh reload showed **31 saved locales on each of Offer, Product Home and Store Configs**. This supersedes the preparation-only checkpoint for those Dev localization fields.

A fresh server export at `/tmp/glob2-epic-saved-dev-20261117.csv` has SHA-256 `0ea4f9c18675a4efd693761a11f76d00a29a4fc6fd1891cba553d925407078a0`. Independent comparison verified **1,736 locale cells (31 × 56)** plus **392 identity/field cells (7 × 56)** exactly against the reviewed candidate. The 56 body rows comprise 53 entity rows, two separators and the footer. The server's sole structural addition was the unused `es` header, empty in all 56 rows. Saved text includes **750 canonical translated cells and 510 exact existing-English fallback cells**; technical/legal qualifications and URLs used as fallbacks remain explicit English, not invented translations.

Compared with the original server export (`d26e677cb3fb808a7d0a9930b61bec42d9fc306539f97e8f298743a2e0855bdc`), the saved data contains **exactly 255 intended cell changes**: 150 new canonical cells, 102 new English fallbacks and three reviewed corrections (Vietnamese introduction twice; Portuguese Portugal legal text once). No other existing values or row identities changed. This establishes applied, persisted Dev localization, not Stage promotion, new review submission or public availability.

Stage remains **Issues found**. Current reviewer feedback names EULA and Support Page links to GitHub as prohibited; these separate fields are not in the localization CSV. Exact URLs and truthful remedies are still being inspected. No legal text, link replacement or Stage promotion was performed by this localization import.

Microsoft's attempted owner verification returned a missing-session-context error; a fresh sign-in restart remains pending. The Gmail connector explicitly withheld the verification code; no code or authentication content is recorded here. The owner explicitly left Amazon pending, so no further Amazon code request was made. These access states do not establish product-editor changes or saved listings.

## Epic scoped Stage promotion and actual review submission — 2026-11-17

The authorized reviewer-link remedies were saved in Dev and freshly reloaded: the **optional EULA URL is blank** (previously GitHub `COPYING`) and **Support Page is `https://glob2.online/community/`** (previously GitHub issues). Exact comparison of all ten form text fields found only those two changes. GPL/source notices, online Terms, privacy/homepage links, product/studio identity and pitch remain unchanged. The first-party community page provides real help routes; the reviewer explicitly permits the optional blank EULA field. This creates no new EULA, licence waiver or replacement legal declaration.

The Dev-to-Stage promotion selected **only the three updated metadata entities: Product Configuration, Product Home and Offer** (including the required Offer dependency). Regions/ratings and the Windows artifact were unchecked and unchanged. Fresh Stage loads show **31 locales on each of the three entities**. Stage verification consists of those counts, representative exact hashes for the new Hindi introduction, corrected Vietnamese introduction and Portuguese legal text, plus the two English link fields. The exhaustive 1,736-cell localization/392-cell metadata export verification belongs to Dev; the download is Dev-only and there is no independently exported Stage CSV. Do not extend the representative Stage check into a full Stage-cell comparison.

**Submit for Review** operates on a nonselective platform review unit, with no entity selector. It included **all five Stage entities**, although only three were changed/promoted: the three metadata entities plus unchanged regions/ratings and Windows artifact. A fresh server reload confirms **Queued for review for all five**, with **Rescind** available, Dev Push disabled because the product is under review, and **Live 0**. This is an actual review submission, not approval or Live publication. No artifact/package or media edit was performed.

At this checkpoint Microsoft is still processing the reviewed CSV upload (38% observed), so no saved/readback outcome is claimed yet. Amazon remains explicitly deferred by the owner.

## Microsoft 44-locale drafts saved and freshly verified — 2026-11-17

The twelve added wire identifiers were established from the current console's expanded export rather than inferred. After the reviewed import completed, fresh reload showed **all 44 locales Complete**. This supersedes the prior processing-only checkpoint and establishes saved drafts, not submission or publication.

Reproducible export/candidate fingerprints:

| Input/outcome | SHA-256 |
| --- | --- |
| Original 32-locale workbook | `bb2ed2c0c50daa52e8e7ec973cd8ae0a14d6ed829afac18f51a1010b576fc004` |
| Expanded 44-locale workbook | `a1e23da12aa5b03dc490eb516913cb4841b616c23e56d7b14317cfdd5191cfb0` |
| Independently reviewed import CSV | `271b4eb3c98bba2daeee4197bc4ed0dc202e611fa236fef57a23fb98eba321c7` |
| Fresh saved server workbook | `bb85183cce96b0e6441c79ad9a5eb10bd559e83e7fb0d54e973e4c321e0424bd` |

Independent full comparison covered **21,744 cells**: **21,660 exact matches** and **84 new media references differing only in the `parentId` query value**. All other URL bytes/components, roles and order match the approved source references. All **516 non-English canonical cells** match the current reviewed catalogs. All 224 existing 32-locale media references, all 44 existing/server-created False flags and the four longer existing English screenshot-caption variants remain unchanged.

The saved scope changes exactly **242 coordinates** from the expanded source: 144 new canonical text cells, 96 approved English media/studio fills and two prior-reviewed Vietnamese corrections. Old unrelated listing fields, default/English values and row identities remain unchanged. Media comparison establishes exact source-reference identity apart from locale-parent routing, not downloaded image-byte hashing.

Fresh Hindi editor visual inspection confirms seven approved media roles: four gameplay images in the approved order, poster, box art and landscape promotional image. The compiled AppTile inherits unchanged; no explicit replacement icon was introduced. A brief Urdu editor check showed readable joined RTL text with the mixed-script brand. These are representative editor observations, not all-locale pixel checks or public-layout certification.

The current workflow is at Review and submit/pending-scope inspection. **No Microsoft review submission or publication is claimed at this checkpoint.** Epic's five-entity review unit remains queued; Amazon remains explicitly deferred.

## Microsoft actual 44-locale update submitted; Publishing — 2026-11-17

After the saved 44-locale and exact-server verification above, the review step selected only changed **Store listings** plus the mandatory, disabled **unchanged Age ratings** item. The unrelated incomplete package draft was disabled and unchecked; properties, pricing and gaming metadata were unchanged and unchecked. The existing published retail package was preserved.

**Publish** was accepted. A fresh console reload confirms **Retail Update — Publishing**, submitted **2026-11-18 03:18 UTC (2026-11-17 22:18 America/Toronto)**, with submitted changes exactly **“Age ratings, Store listings”**. **Cancel publish** is visible and was left untouched. This supersedes the saved-only checkpoint: the 44-locale update is actually submitted to the publishing pipeline. It does not establish public translated display, separate certification approval or a new package release.

Sign-in recovered through a fresh official dashboard without requesting a new OTP; the connector's withheld email code was not retrieved or bypassed. No private contact, code or credential content is retained. No unsaved browser edits remain, and the concurrent submitted Steam support tab is preserved.

Current bounded rollout summary: **Play's sixteen changes are explicitly In review; Epic's five-entity Stage review unit is Queued after three metadata promotions and two saved link fixes, with Live 0; Microsoft 44-locale Retail Update is Publishing; Apple localization remains version-state locked; Amazon remains explicitly owner-deferred.** Prepared canonical source, merged game metadata, saved console data, review/publishing states and public translated display remain distinct evidence levels.

## Latest Apple editable drafts and locale intersection — 2026-11-17

The [qualified latest Apple candidate receipt](approved-storefront-rollout.md#latest-apple-candidates-qualified-and-saved--2026-11-17) supersedes the prior version-state locks: **Mac 0.11.6/build2026111801** is saved Prepare for Submission with Add for Review enabled after qualification and removal of the old review item; **iOS 0.11.601/build1002501** is newly saved and bound to the processed exact tagged build with manual release. Both use `v0.11.6.1` source. No review submission or release occurred.

Mac's evidence-backed standard-encryption/no-France compliance answers were saved and freshly read back Ready to Submit. Existing territories, four screenshots, metadata/review notes and automatic-release setting remained unchanged. iOS's 335-character source-qualified What's New was freshly verified exactly, with inherited metadata/media preserved. Full source/upload/provenance distinctions are in the publishing receipt.

The fresh 50-choice Apple selector reconciles exactly to the existing **38 canonical locale mappings**: seven choices are non-game languages and five are additional regional English/French/Spanish variants. The nine expansion mappings already include `bn-BD`, `hi`, `mr-IN`, `ta-IN`, `te-IN`, `ur-PK`, `ms`, `no` and `th`; no new canonical match is missing. The seven canonical gaps remain `eo`, `eu`, `fa`, `sr-Cyrl`, `sw`, `fil`, `bg`. No locale field was written in this candidate-preparation unit.

All 45 Mac runtime catalogs are physically present and exact-tag-matching. The separate native Apple declaration has only six permission `.lproj` folders and lacks `CFBundleLocalizations`; this packaging gap needs follow-up/rebuild, not a claim that runtime translations are absent. Existing macOS 26/arm64 scope remains explicit. The optional priority question—finish translated listings before review or submit English first—awaits the user's response; do not infer either outcome from saved drafts.
