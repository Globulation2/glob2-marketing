# iOS App Review response draft

**Prepared final packet, 2026-10-31; outbound receipts pending.** Coordinating review approved the exact 3,547-character six-part text below for both the reply and App Review Notes, with both actual clips. The user authorized proceeding. The desktop companion is explicitly distinct from phone footage/native guest linking; no sent reply, Notes update or resubmission is claimed.

## Reviewer response

1. Recordings
Globulation 2 Preview.mp4 (1m49s) shows a physical iPhone on iOS 15.8.8 (19H422), the latest supported public OS for this hardware. It uses the original submitted release binaries, 0.11.400 (1002101), installed with a development profile without recompiling.
Phone timeline: 00:00–00:03 Home Screen/launch; 00:05–00:23 Custom game setup; 00:24–01:24 colony gameplay/touch controls; 01:25–01:30 menu/results; 01:38–01:43 automatic guest connection/online hub; 01:44–01:49 menus.

glob2-desktop-web-review-supplement.mp4 (1m44.2s) is a chronological desktop-browser companion, not iPhone footage: 00:00–00:18 signup; 00:18–00:38 new account; 00:38–00:51 sign-out/sign-in; 00:51–01:24 Maps/CrystalBasin/Report; 01:24–01:30 report reason/details controls, then Back without submitting; 01:30–01:44.2 account deletion and success confirmation. Only the newly created disposable web account was deleted. This web account was separate from the native guest; native guest linking, paid checkout and administrator ban execution are not filmed.

2. Purpose and audience
Globulation 2 is a free, open-source real-time strategy game for players who enjoy colony building, economics and spatial strategy. Balance food, construction and training while expanding and defending a colony. Autonomous creatures carry out assigned work so players guide the colony as a whole, using touch controls on iPhone/iPad.

3. Setup and access
Offline single-player, campaigns, the editor and LAN need no account or sample files. Choose Custom game, configure map/players and start. Campaign, Tutorial and Load game are on the main menu; LAN is under More.
Play online creates a guest without email. Optional sign-in/linking opens the browser from the online account menu or Settings > Online. Settings > Online > Download or delete my data > Open reaches the account page. Guests first need a linked sign-in method for web deletion. Offline/guest play needs no reviewer credentials; web /signin supports username/password registration.
Map details offer Report; music entries link to credits/downloads/reporting. Reports go to a server-side queue. Authorized web moderators can resolve/dismiss reports and hide content. Administrators can ban accounts; the server implementation ends their sessions. These are web/server capabilities, not an iPhone administration screen.
Native AI Commander/paid-credit controls, AI-authoring links, community AI controllers and community generators are disabled in this App Store build. Built-in computer opponents remain available.

4. External services
Offline play uses local content/storage. Optional Glob2 Online service at https://app.glob2.online handles accounts, rooms, matchmaking and shared content. Documented providers include Google Cloud hosting, optional Google sign-in and Gravatar images; the project also operates username/password authentication. Separate optional website tools use Stripe payments and OpenAI generation, not required for offline gameplay.

5. Regional behavior
This is the standard iOS build, not the separate China edition. Native feature configuration is shared across regions; relay regions select network servers. Online service/provider availability can vary.

6. Third-party material
The game is distributed under GPL-3.0-or-later, with separate font, codec, JavaScript, JSON, icon, MoltenVK, recording-component and soundtrack notices. Woodland music credits JC Sounds under CC BY 4.0 and describes its adaptations. Applicable notices identify the third-party authors and licenses.

## Internal evidence and remaining gaps

Observed 2026-10-31: authenticated UI reports Guideline 2.1.0 Performance / App Completeness rejection requesting six information items. Apple's actual video wording specifies a physical device “running the latest operating system,” beginning with app launch and the typical flow, plus account registration/login/deletion, user-generated-content reporting/blocking and paid flows **if present**. “Latest supported for this hardware” is our evidence-backed device context, not a quoted Apple exception or an acceptance guarantee. No crash is alleged in the observed request. Related: [publishing ledger](approved-storefront-rollout.md).

The physical clip covers launch/core gameplay/automatic guest connection. The desktop companion demonstrates a separate disposable web account signup, sign-out/sign-in, actual Maps navigation to Report controls without submitting, and deletion success. Native guest linking, paid browser checkout and administrator ban execution were not filmed. Backend moderation/service-ban handling is explained from source evidence, without claiming exercised enforcement or a response-time commitment. Save/load was part of our suggested script, **not a separately stated Apple video requirement**. Showing Save/Load menu buttons does not establish either action.

### Completed desktop web companion

The user authorized the account/moderation supplement and clarified that the flows are primarily Glob2 Online web features. The dedicated recording worker used a fresh isolated **desktop browser** and only a new disposable account. Registration, sign-out, sign-in, actual Maps UI navigation to **CrystalBasin**, Report form inspection, and account deletion success were observed. The form was left using Back without submitting a report; no fake report, purchase, administrator ban or existing-account deletion occurred. The new demonstration account was deleted last, with the UI confirming **Your account was deleted** and sign-out everywhere. This does not establish native guest linking or a personal user-blocking feature.

Final file: **glob2-desktop-web-review-supplement.mp4**, **104.200 seconds**, **5,313,512 bytes**, **H.264 / 1280 × 720 / 25 fps / no audio**. SHA-256 **`fe01515973771c237f9ffbda8e76fe7f7ff3a394108a83209c72bb61fe6ed072`**. It is a chronological derivative removing only a mistaken manually entered map URL and selector/idle waits; the actual successful workflow actions remain. The **208.2-second raw recording is preserved privately**. Root visually reviewed the contact sheet and signup sequence. Personal browser/session details, credentials, raw video and private evidence paths remain outside Git.

| Desktop companion time | Observed action |
| --- | --- |
| 00:00–00:18 | Disposable account registration and success |
| 00:18–00:38 | New account shown |
| 00:38–00:51 | Sign-out and subsequent sign-in |
| 00:51–01:24 | Actual Maps UI, CrystalBasin listing and Report entry |
| 01:24–01:30 | Reason/details and Send report button; Back without report submission |
| 01:30–01:39 | Deletion explanation and confirmation field |
| 01:39–01:44.2 | Current display-name confirmation, permanent deletion and success/sign-out |

The working map link is [CrystalBasin](https://app.glob2.online/maps/b5cdf9ff-0316-49e0-891a-14611c0ec192). The former manually guessed map URL was incorrect and was removed from the chronological derivative; reviewer instructions must use the observed link above. The physical clip is unchanged. The two clips and exact same written six-part response form the reviewed final packet. The original clip is already accepted in the unsent server draft; final companion attachment/text/Notes saves and sent reply/resubmission have no verified receipts yet.

### Player reporting versus service moderation

[Apple Guideline 1.2](https://developer.apple.com/app-store/review/guidelines/#user-generated-content), checked 2026-10-31, covers filtering, reporting, timely response, public contact and **“The ability to block abusive users from the service”**. It does not specify that an iPhone must expose administrator moderation controls or necessarily a personal native Block button. The desktop companion covers player-facing web account signup/login/deletion and Report controls. Describe the evidenced backend moderation/administrator handling in writing, without presenting desktop footage as a native phone demonstration.

The scoped inspection did not find an end-user Block control. That is a limited observation, **not an established policy failure** or a new native-feature prerequisite. Current source implements player reports stored in `map_reports`, moderator-only resolve/dismiss/hide routes and web controls, and an administrator-only ban route calling `setBanned`, which invokes `endSessions`. Sources: [map report routes](https://github.com/Globulation2/glob2/blob/master/platform/apps/api/src/maps/routes.ts), [web moderation controls](https://github.com/Globulation2/glob2/blob/master/platform/apps/web/src/admin/Moderation.tsx), [administrator routes](https://github.com/Globulation2/glob2/blob/master/platform/apps/api/src/routes/admin.ts), and [ban implementation](https://github.com/Globulation2/glob2/blob/master/platform/apps/api/src/auth/admin.ts). This establishes implemented capability; no live ban/enforcement test, fixed response SLA or actual report submission is claimed.

### Reply and Notes field readiness

The actual Apple review-reply and App Review Notes fields are editable and each has a **4,000-character cap**. The attachment UI supports multiple attachments; no file-type/size cap was visible in the inspected UI. The original **88 MB** recording was accepted in an unsent draft, with filename/Download/Continue Draft verified on reload. That earlier reply draft had 3,615 characters; the newly approved exact final text is 3,547 characters. Final companion attachment acceptance, replacement text, Notes save, sent reply and resubmission remain unconfirmed.

### Exact candidate

[Upload 39651442049](https://github.com/genixpro/glob2-release/actions/runs/39651442049), referenced by [inspection 39743116258](https://github.com/genixpro/glob2-release/actions/runs/39743116258), binds 0.11.400 / 1002101 to `v0.11.4.0`, source `a766230578dede730be43919240c5c80fafb44fe`. The inspection's historical Waiting for Review state is superseded by the current UI rejection.

### Shipped mobile feature map

- [Tagged iOS workflow](https://github.com/Globulation2/glob2/blob/v0.11.4.0/.github/workflows/ios-testflight.yml) invokes `mobile/ios.py configure --environment device --release --unsigned --build-number`, without `--china` or feature overrides. [iOS packaging](https://github.com/Globulation2/glob2/blob/v0.11.4.0/mobile/ios.py) passes target ios/release to build identity. [Client feature resolution](https://github.com/Globulation2/glob2/blob/v0.11.4.0/scons/client_features.py) defaults release to free/app_store: commander, authoring_links, community_ai and community_generators false. This establishes the native build defaults; it does not remove every browser destination reachable from account/content pages.
- [Online account menu](https://github.com/Globulation2/glob2/blob/v0.11.4.0/src/online/screens/OnlineHubScreen.cpp) fetches authentication providers from the service and begins browser sign-in. [Online settings](https://github.com/Globulation2/glob2/blob/v0.11.4.0/src/ui/settings/SettingsScreenOnline.cpp) exposes linking, sign-out and `/account`; Commander account/credits controls return immediately when Commander is disabled. [Tagged policy](https://github.com/Globulation2/glob2/blob/v0.11.4.0/docs/mobile/privacy-policy.md) explains guest web-deletion limitations and provider purposes.
- [Maps UI](https://github.com/Globulation2/glob2/blob/v0.11.4.0/src/online/screens/OnlineMapsScreen.cpp) implements shared-map reporting. [Music UI](https://github.com/Globulation2/glob2/blob/v0.11.4.0/src/ui/screens/MusicLibraryScreen.cpp) exposes `/music/{id}` for credits/downloads/reporting; authoring actions are feature-gated. The scoped search did not establish an end-user Block control; this does not establish a service-level enforcement failure. Actual server-ban execution was not verified. The physical recording verifies guest access; the separate desktop companion demonstrates web signup/login/deletion and Report controls without exercising server report submission or moderation enforcement.
- The workflow does not select the China edition. No country-based native content switch was identified in this scoped path. Online relay geography is not evidence of content restrictions; do not extrapolate identical provider/service availability in every region.

### Notices and rights evidence

[iOS packaging](https://github.com/Globulation2/glob2/blob/v0.11.4.0/mobile/ios.py) exports data/maps/campaigns/scripts and adds recording and MoltenVK license directories to app resources. [Asset export filtering](https://github.com/Globulation2/glob2/blob/v0.11.4.0/tools/package_assets.py) preserves the applicable data notices; these include font, image-codec, JavaScript, JSON and Tabler icon notices. [Woodland attribution](https://github.com/Globulation2/glob2/blob/v0.11.4.0/data/zik/woodland/LICENSE.txt) identifies JC Sounds, CC BY 4.0, source and adaptations. These are concrete licensing records, not a universal ownership statement or a completed legal audit. No regulated-service credential was identified or claimed.

### Current-build archive and installation provenance

The exact unsigned archive retained by [upload 39651442049](https://github.com/genixpro/glob2-release/actions/runs/39651442049) was retrieved and verified: **0.11.400 / 1002101**, bundle **org.globulation2.glob2**, minimum **iOS 15**, **arm64**, **iPhone + iPad**. Its pre-sign executable SHA-256 is `3884e536ee1429759ed0f0c85da49cce5501bdd11c46e86f8e9f38080e6ee22c`, matching the original upload’s compiled-source provenance `a766230578dede730be43919240c5c80fafb44fe`. No original TestFlight/App Store-signed IPA is retained; the development export is identified separately below.

The existing app-specific development profile was regenerated using the **existing certificate and already registered test phone**, with capabilities preserved. App/team/device/private-key matching and strict code-signature, signer, profile, entitlement, minimum-OS and version checks passed. The archive was manually exported with **development/debugging signing**, without a rebuild or managed version change; the compiled binary UUID was unchanged. No new certificate/key or device registration was created.

The actual development IPA is **168,168,948 bytes**, SHA-256 `52f2f5c5debafde36bede7f5ed50a364e3afcd475d05c7315897a47c8f9f1d65`. **ios-deploy exited 0 and reported completed installation** to the connected test phone. This is not a new TestFlight/App Store artifact, TestFlight installation or a bit-identical signed IPA. At the installation step, no launch/debugger, uninstall or data-deletion action was performed; app data was not independently audited. The later physical walkthrough below establishes app opening/gameplay; it does not demonstrate account deletion. Private device/account/profile/certificate identifiers, paths and logs remain outside Git.

### Physical device and recorded evidence

The earlier absence of a connected device is historical. On 2026-10-31, the physical test iPhone connected and its existing trust pairing validated. It runs **iOS 15.8.8 / build 19H422**, the latest supported public OS for this older hardware, checked against [Apple's public software catalog](https://gdmf.apple.com/v2/pmv) and [Apple's iOS 15.8.8 support record](https://support.apple.com/en-ca/127114). No globally newest-OS or replacement-phone requirement is inferred. Newer CoreDevice tooling's unsupported status did not prevent physical capture.

The user recorded **Globulation 2 Preview.mp4** on October 31. Original size **88,033,423 bytes**, duration **109.092317 seconds**, SHA-256 **`61d6c23e09bba2469f41100fd2269722d6423d225d5b92b3f07a259dc16afa29`**. Its MP4 container has a **1280 × 720 H.264** video stream with the portrait phone centered between black side areas, **48 kHz stereo AAC** audio, and an attached MJPEG thumbnail. No rotation metadata is present. Full video/audio decoding completed with exit 0 and no errors; audible content was not separately assessed. The original was not edited, deleted, copied or re-encoded. Only small private review frames/contact sheets were made and visually inspected outside Git.

Reviewed timestamps:

| Time | Actual observed coverage |
| --- | --- |
| 00:00–00:03 | Phone Home Screen, then app main menu after launch |
| 00:05–00:23 | Custom game map/player setup |
| 00:24–01:24 | Rendered colony, touch navigation, building/radial controls, flags and zone tools |
| 01:25–01:29 | In-game menu; Save/Load buttons visible but neither action demonstrated |
| About 01:30 | Normal defeat/results screen, not an observed crash |
| 01:38–01:43 | Guest connecting, then online hub at the original service host |
| 01:44–01:49 | Main/More menu |

The native version is **not legible in the reviewed launch/main-menu frames**. Build identity is supported by the separate archive/export/installation provenance above, not by a visible video label. The recording must be described as the original compiled archive with **development signing**, not a TestFlight installation, newly compiled development binary or bit-identical App Store-signed IPA.

The physical clip does not demonstrate account registration/linking/login/deletion, player Report entry/web handoff or a paid browser flow. The reviewed desktop companion demonstrates separate web signup/login/deletion and Report controls, without submitting a report, linking the native guest, executing a ban or making a purchase. No successful save/load, completed construction, online match or regional consistency is inferred from showing controls or reaching the guest hub. Keep footage, personal device names/IDs/serials, credentials, profile/certificate details and private paths outside this public repository. The user approved actual player-flow evidence plus the written web/server moderation explanation. Coordinating review approved this final packet and the user authorized proceeding. The designated UI owner is authorized to save both clips/exact text in the reply draft, save the same text in Notes, send the reply and inspect/perform same-build resubmission if available; actual final-action receipts remain unconfirmed. This document does not claim submission or that Apple accepted the evidence.
