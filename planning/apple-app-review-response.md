# iOS App Review response draft

**Draft only, 2026-10-31.** The six sections below are prepared for the same review reply and App Review Notes. The user selected a short account/moderation supplement, primarily applicable Glob2 Online web flows, while retaining the existing core-gameplay clip. Supplement footage and updated final text remain pending. No reply, Notes update or resubmission is claimed.

## Reviewer response

1. Physical-device recording
Recording: Globulation 2 Preview.mp4, 1m49s, on a physical iPhone running iOS 15.8.8 (19H422), the latest supported public OS for this hardware. The recording uses the original submitted release binaries, version 0.11.400 (1002101), installed with a development profile without recompiling.

Timeline: 00:00–00:03 Home Screen and app launch; 00:05–00:23 Custom game/map/player setup; 00:24–01:24 colony gameplay, touch navigation, building/radial controls and flag/zone tools; 01:25–01:29 game menu; about 01:30 normal defeat/results; 01:38 guest connecting and 01:40–01:43 online guest hub; 01:44–01:49 main/More menu. This shows core gameplay and automatic guest access. Optional account registration/linking/login/deletion, player reporting/web handoff and applicable paid browser flows are not demonstrated in this recording.

2. Purpose and audience
Globulation 2 is a free, open-source real-time strategy game for players who enjoy colony building, economics and spatial strategy. Players balance food, construction and training while expanding and defending their colony. Autonomous creatures carry out assigned work, letting players guide the colony as a whole. iPhone and iPad use touch controls.

3. Setup and access
Offline single-player, campaigns and the map editor need no account or sample files. Choose Custom game, configure a map and players, then start; Campaign and Tutorial are also on the main menu. LAN is under More and needs no account.

Play online creates a guest account without email. Optional sign-in/linking opens the system browser from the online account menu or Settings > Online. Settings > Online > Download or delete my data > Open opens the account page. Guests must first link a sign-in method to use web deletion. No reviewer credentials are needed for offline or guest play.

Online content includes rooms/chat, community maps and music. Map details offer Report; music entries link to credits/downloads/reporting in the browser. Native AI Commander/paid-credit controls, AI-authoring links, community AI controllers and community map generators are disabled in this App Store build; built-in computer opponents remain available.

4. External services
Offline play uses local content/storage. Optional online play uses the project's account, room, matchmaking and shared-content service. Documented providers include Google Cloud hosting, optional Google browser sign-in and Gravatar images; the project also operates username/password authentication. Separate optional website tools use Stripe payments and OpenAI generation. They are not offline-game dependencies.

5. Regional behavior
This is the standard iOS build, not the separate China edition. Native feature configuration is shared across regions; relay regions select network servers. Online service/provider availability can vary, so we do not claim identical availability everywhere.

6. Third-party material
This strategy game is distributed under GPL-3.0-or-later, with separate font, codec, JavaScript, JSON, icon, MoltenVK and recording-component notices and soundtrack attribution. Woodland music credits JC Sounds under CC BY 4.0 and describes its adaptations. These notices identify the relevant third-party authors and licenses.

## Internal evidence and remaining gaps

Observed 2026-10-31: authenticated UI reports Guideline 2.1.0 Performance / App Completeness rejection requesting six information items. Apple's actual video wording specifies a physical device “running the latest operating system,” beginning with app launch and the typical flow, plus account registration/login/deletion, user-generated-content reporting/blocking and paid flows **if present**. “Latest supported for this hardware” is our evidence-backed device context, not a quoted Apple exception or an acceptance guarantee. No crash is alleged in the observed request. Related: [publishing ledger](approved-storefront-rollout.md).

The existing clip covers launch/core gameplay/automatic guest connection. Account signup/login/deletion and the player Report entry/web handoff remain unrecorded; reachable paid browser paths remain unverified. Backend moderation/service-ban handling belongs in the written explanation, not an administrator-ban demonstration. Save/load was part of our suggested script, **not a separately stated Apple video requirement**. Showing Save/Load menu buttons does not establish either action.

### Selected supplementary-footage route

The user chose **“Add a short account/moderation clip”** and clarified that these are mostly **Glob2 Online web flows**. Keep the existing **1m49s core-gameplay recording intact**; no core gameplay redo is selected. Live web inspection and read-only source mapping cover player-facing account signup/login/deletion and the Report entry/web handoff. Explain backend moderation/administrator ban handling in writing using only established facts. Do not film administrator bans, submit fake reports or require a new native feature. No supplemental recording or web-flow coverage is claimed yet. Update the unsent reviewer text only after the new footage is reviewed; Apple's acceptance is not assumed. No attachment upload, reviewer reply, App Review Notes save or resubmission has occurred.

### Player reporting versus service moderation

[Apple Guideline 1.2](https://developer.apple.com/app-store/review/guidelines/#user-generated-content), checked 2026-10-31, covers filtering, reporting, timely response, public contact and **“The ability to block abusive users from the service”**. It does not specify that an iPhone must expose administrator moderation controls or necessarily a personal native Block button. The player-facing recording scope is Report entry/web handoff plus account signup/login/deletion; describe evidenced backend moderation/administrator handling in writing.

The scoped inspection did not find an end-user Block control. That is a limited observation, **not an established policy failure** or a new native-feature prerequisite. No actual server ban/enforcement was verified or performed, and this document does not claim otherwise. Do not invent that coverage or fabricate a report to demonstrate it.

### Reply and Notes field readiness

The actual Apple review-reply and App Review Notes fields are editable and each has a **4,000-character cap**. The attachment UI supports multiple attachments; no file-type/size cap was visible in the inspected UI. Upload of the original **88 MB** recording is **untested**, so UI visibility does not guarantee acceptance. No field save or attachment upload has occurred.

### Exact candidate

[Upload 39651442049](https://github.com/genixpro/glob2-release/actions/runs/39651442049), referenced by [inspection 39743116258](https://github.com/genixpro/glob2-release/actions/runs/39743116258), binds 0.11.400 / 1002101 to `v0.11.4.0`, source `a766230578dede730be43919240c5c80fafb44fe`. The inspection's historical Waiting for Review state is superseded by the current UI rejection.

### Shipped mobile feature map

- [Tagged iOS workflow](https://github.com/Globulation2/glob2/blob/v0.11.4.0/.github/workflows/ios-testflight.yml) invokes `mobile/ios.py configure --environment device --release --unsigned --build-number`, without `--china` or feature overrides. [iOS packaging](https://github.com/Globulation2/glob2/blob/v0.11.4.0/mobile/ios.py) passes target ios/release to build identity. [Client feature resolution](https://github.com/Globulation2/glob2/blob/v0.11.4.0/scons/client_features.py) defaults release to free/app_store: commander, authoring_links, community_ai and community_generators false. This establishes the native build defaults; it does not remove every browser destination reachable from account/content pages.
- [Online account menu](https://github.com/Globulation2/glob2/blob/v0.11.4.0/src/online/screens/OnlineHubScreen.cpp) fetches authentication providers from the service and begins browser sign-in. [Online settings](https://github.com/Globulation2/glob2/blob/v0.11.4.0/src/ui/settings/SettingsScreenOnline.cpp) exposes linking, sign-out and `/account`; Commander account/credits controls return immediately when Commander is disabled. [Tagged policy](https://github.com/Globulation2/glob2/blob/v0.11.4.0/docs/mobile/privacy-policy.md) explains guest web-deletion limitations and provider purposes.
- [Maps UI](https://github.com/Globulation2/glob2/blob/v0.11.4.0/src/online/screens/OnlineMapsScreen.cpp) implements shared-map reporting. [Music UI](https://github.com/Globulation2/glob2/blob/v0.11.4.0/src/ui/screens/MusicLibraryScreen.cpp) exposes `/music/{id}` for credits/downloads/reporting; authoring actions are feature-gated. The scoped search did not establish an end-user Block control; this does not establish a service-level enforcement failure. Actual server-ban execution was not verified. The recorded guest connection verifies service access, but browser navigation and moderation behavior remain unrecorded.
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

The clip does not demonstrate account registration/linking/login/deletion, player Report entry/web handoff or a paid browser flow. No successful save/load, completed construction, online match or regional consistency is inferred from showing controls or reaching the guest hub. Keep footage, personal device names/IDs/serials, credentials, profile/certificate details and private paths outside this public repository. Provide the original and finished supplement privately to Apple with the updated written reply/Notes; the selected supplement remains unrecorded.
