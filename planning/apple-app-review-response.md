# iOS App Review response draft

**Draft only, 2026-10-31.** The six sections below are the shared reply / App Review Notes text. Replace bracketed gaps before sending.

## Reviewer response

1. Physical-device recording
[RECORDING LINK OR ATTACHMENT; DEVICE MODEL; LATEST SUPPORTED PUBLIC OS VERSION/BUILD FOR THIS DEVICE; INSTALLATION ROUTE AND ANY SIGNING DIFFERENCE; TIMESTAMPS]. The recording must show Globulation 2 0.11.400 (1002101) launching, normal gameplay and applicable online flows. The installed test copy is a development-signed export of the exact original compiled archive, without rebuilding; it is not TestFlight/App Store signing.

2. Purpose and audience
Globulation 2 is a free, open-source real-time strategy game for players who enjoy colony building, economics and spatial strategy. Players balance food, construction and training while expanding and defending their colony. Autonomous creatures carry out assigned work so players can guide the colony as a whole. iPhone and iPad use touch controls.

3. Setup and main features
Single-player games, campaigns, the map editor and LAN play need no account or sample files. Launch the app, choose a single-player game or campaign, select an included scenario and begin. [CONFIRM BUTTON LABELS IN RECORDING.] Show colony construction, work assignment and save/load.

Optional online play creates a guest account without an email address. Sign in or link a sign-in method through the online account menu or Settings > Online; authentication opens the system browser. Settings > Online > Download or delete my data opens the account page. A guest must first link a sign-in method to use web deletion. [ADD RECORDED REGISTRATION, LOGIN AND DELETION TIMESTAMPS; PRIVATE DEMO CREDENTIALS ONLY IF REQUIRED.]

Online features include rooms/chat and community maps. Maps have reporting controls; music entries link to credits/downloads/reporting in the browser. [UGC TIMESTAMPS AND VERIFIED REPORTING/BLOCKING INSTRUCTIONS.]

This App Store release disables the native AI commander, AI-authoring links, community AI controllers and community map generators. It retains ordinary strategy gameplay and community maps/music. [CONFIRM ANY PAID FEATURES REACHABLE THROUGH BROWSER LINKS AND SHOW THEM IF APPLICABLE.]

4. External services
Offline gameplay uses local content/storage. Optional online play uses the project's online service for accounts, rooms, matches, ratings and shared content. Its documented providers include Google Cloud hosting, optional Google browser sign-in and Gravatar profile images. Username/password authentication is operated by the project. The wider optional website services document Stripe payments and OpenAI generation; these are not dependencies of offline gameplay. [CONFIRM WHICH OPTIONAL SERVICES ARE REACHABLE FROM THIS BUILD'S BROWSER LINKS.] No publisher credentials are needed to play offline.

5. Regional behavior
The submitted workflow builds the standard iOS edition, without the separate China-edition option. The tagged native feature configuration is common to this build; relay regions select network servers, not different game content. [CONFIRM CURRENT SERVICE/REGIONAL RESTRICTIONS BEFORE STATING THAT ALL FEATURES ARE IDENTICAL IN EVERY REGION.]

6. Third-party material and authorization
Globulation 2 is a strategy game distributed under GPL-3.0-or-later. It includes separately licensed dependencies/assets: font notices, image-codec/JavaScript/JSON/icon notices, per-soundtrack attribution, and packaged MoltenVK/recording notices. For example, Woodland music credits JC Sounds under CC BY 4.0 and records the adaptations. [RELEVANT AUTHORIZATION DOCUMENTS IF REQUESTED.]


## Internal evidence and remaining gaps

Observed 2026-10-31: authenticated UI reports Guideline 2.1.0 Performance / App Completeness rejection requesting six items, including a physical-device recording on the latest supported public OS for the hardware and the same information in App Review Notes. No crash is alleged in the observed request. No reply, Notes update, resubmission or recording has been performed. Related: [publishing ledger](approved-storefront-rollout.md).

### Exact candidate

[Upload 39651442049](https://github.com/genixpro/glob2-release/actions/runs/39651442049), referenced by [inspection 39743116258](https://github.com/genixpro/glob2-release/actions/runs/39743116258), binds 0.11.400 / 1002101 to `v0.11.4.0`, source `a766230578dede730be43919240c5c80fafb44fe`. The inspection's historical Waiting for Review state is superseded by the current UI rejection.

### Shipped mobile feature map

- [Tagged iOS workflow](https://github.com/Globulation2/glob2/blob/v0.11.4.0/.github/workflows/ios-testflight.yml) invokes `mobile/ios.py configure --environment device --release --unsigned --build-number`, without `--china` or feature overrides. [iOS packaging](https://github.com/Globulation2/glob2/blob/v0.11.4.0/mobile/ios.py) passes target ios/release to build identity. [Client feature resolution](https://github.com/Globulation2/glob2/blob/v0.11.4.0/scons/client_features.py) defaults release to free/app_store: commander, authoring_links, community_ai and community_generators false. This establishes the native build defaults; it does not remove every browser destination reachable from account/content pages.
- [Online account menu](https://github.com/Globulation2/glob2/blob/v0.11.4.0/src/online/screens/OnlineHubScreen.cpp) fetches authentication providers from the service and begins browser sign-in. [Online settings](https://github.com/Globulation2/glob2/blob/v0.11.4.0/src/ui/settings/SettingsScreenOnline.cpp) exposes linking, sign-out and `/account`; Commander account/credits controls return immediately when Commander is disabled. [Tagged policy](https://github.com/Globulation2/glob2/blob/v0.11.4.0/docs/mobile/privacy-policy.md) explains guest web-deletion limitations and provider purposes.
- [Maps UI](https://github.com/Globulation2/glob2/blob/v0.11.4.0/src/online/screens/OnlineMapsScreen.cpp) implements shared-map reporting. [Music UI](https://github.com/Globulation2/glob2/blob/v0.11.4.0/src/ui/screens/MusicLibraryScreen.cpp) exposes `/music/{id}` for credits/downloads/reporting; authoring actions are feature-gated. User blocking was not established by the scoped source inspection. Current browser navigation and moderation behavior require the physical walkthrough.
- The workflow does not select the China edition. No country-based native content switch was identified in this scoped path. Online relay geography is not evidence of content restrictions. Current service/provider restrictions remain a specific confirmation gap, not an established regional difference.

### Notices and rights evidence

[iOS packaging](https://github.com/Globulation2/glob2/blob/v0.11.4.0/mobile/ios.py) exports data/maps/campaigns/scripts and adds recording and MoltenVK license directories to app resources. [Asset export filtering](https://github.com/Globulation2/glob2/blob/v0.11.4.0/tools/package_assets.py) preserves the applicable data notices; these include font, image-codec, JavaScript, JSON and Tabler icon notices. [Woodland attribution](https://github.com/Globulation2/glob2/blob/v0.11.4.0/data/zik/woodland/LICENSE.txt) identifies JC Sounds, CC BY 4.0, source and adaptations. These are concrete licensing records, not a universal ownership statement or a completed legal audit. No regulated-service credential was identified or claimed.

### Current-build archive and installation provenance

The exact unsigned archive retained by [upload 39651442049](https://github.com/genixpro/glob2-release/actions/runs/39651442049) was retrieved and verified: **0.11.400 / 1002101**, bundle **org.globulation2.glob2**, minimum **iOS 15**, **arm64**, **iPhone + iPad**. Its pre-sign executable SHA-256 is `3884e536ee1429759ed0f0c85da49cce5501bdd11c46e86f8e9f38080e6ee22c`, matching the original upload’s compiled-source provenance `a766230578dede730be43919240c5c80fafb44fe`. No original TestFlight/App Store-signed IPA is retained; the development export is identified separately below.

The existing app-specific development profile was regenerated using the **existing certificate and already registered test phone**, with capabilities preserved. App/team/device/private-key matching and strict code-signature, signer, profile, entitlement, minimum-OS and version checks passed. The archive was manually exported with **development/debugging signing**, without a rebuild or managed version change; the compiled binary UUID was unchanged. No new certificate/key or device registration was created.

The actual development IPA is **168,168,948 bytes**, SHA-256 `52f2f5c5debafde36bede7f5ed50a364e3afcd475d05c7315897a47c8f9f1d65`. **ios-deploy exited 0 and reported completed installation** to the connected test phone. This is not a new TestFlight/App Store artifact, TestFlight installation or a bit-identical signed IPA. No launch/debugger, uninstall or data-deletion action was performed; app data was not independently audited. App opening/gameplay/footage remain unverified. Private device/account/profile/certificate identifiers, paths and logs remain outside Git.

### Physical recording dependency

The earlier read-only Xcode inventory found this Mac and simulators, with **no physical iPhone/iPad at that time**. On 2026-10-31, a physical test iPhone connected and its existing trust pairing validated. It runs **iOS 15.8.8 / build 19H422**, the latest supported public OS for this older hardware, checked against [Apple’s public software catalog](https://gdmf.apple.com/v2/pmv) and [Apple’s iOS 15.8.8 support record](https://support.apple.com/en-ca/127114). This does not impose the globally newest OS or a replacement-phone requirement.

The newer Xcode CoreDevice path does not support this device/OS combination; that is a tooling limit, not evidence that the app cannot run. QuickTime’s actual **screen and speaker source picker recognizes the phone**. No source preview or recording has started. The phone’s TestFlight currently offers only an older version, and the user explicitly requested installing the current build. The current **0.11.400 / 1002101** is now installed through the verified same-archive development export described above. The user should open the installed app from the Home Screen; an older TestFlight listing may remain. No app opening or source preview is verified yet. The installation route/signing difference must be disclosed; it is not TestFlight-installed or a bit-identical signed IPA. A simulator or newly compiled development binary cannot stand in for the requested submitted-build footage. Personal device names, identifiers, serial numbers and accounts remain outside Git.

Use the device's [built-in screen recording](https://support.apple.com/en-ie/guide/iphone/iph52f6e1987/ios), starting before tapping the app icon. Show the usual colony flow, save/load, then actual account and applicable UGC/paid flows. Confirm exact button labels, account deletion, blocking and browser destinations during that pass. Keep raw footage and any credentials outside this public repository; provide the finished video privately to Apple. Replace all bracketed text before posting the six sections to both the reply and Notes. Preserve the actual launch and interactions in the footage.
