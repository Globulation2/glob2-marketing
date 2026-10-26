# Distribution platforms and listing ledger

[Fact index](README.md) · [Channels](channels.md) · [Assets](assets.md) · [History](history.md) · [Product](product.md)

Checked **2026-10-26**. Listing existence, download availability, successful installation, current multiplayer compatibility, submission state and publisher account control are separate facts. No binaries were downloaded or installed. Version fields below are observations of each surface, not a single project-wide latest-version assertion.

## Publicly observed distribution

| ID | Surface | Observed public state | Evidence / limits |
| --- | --- | --- | --- |
| DS-01 | [Current downloads](https://glob2online.com/downloads/) | HTTP 200; explicitly labels **0.11.4.0 experimental** for early testing. Windows x64 installer/portable ZIP; macOS15 Apple Silicon/Intel DMGs; Linux x64 Flatpak bundle, Snap file, tarball, RPM; Android API24+ ARM64/ARM32/x64 APKs; source archive. Provides hashes. | Page describes platform/online testing as in progress. No verified production iPhone/iPad App Store release listed. Direct Flatpak bundle is distinct from Flathub publication; direct Snap file distinct from Snap Store channel. |
| DS-02 | [Browser game](https://app.glob2online.com/play/) | Current homepage links browser early access; app root serves HTTP 200 shell. | Gameplay/runtime/version not exercised. |
| DS-03 | [GitHub release 0.11.4.0](https://github.com/Globulation2/glob2/releases/tag/v 0.11.4.0) | Public API reports published 2026-10-22T08:29:36Z, `draft=false`, `prerelease=false`. | API release flag differs from website’s experimental wording; neither establishes qualification success. [API](https://api.github.com/repos/Globulation2/glob2/releases?per_page=5) also exposes prerelease/evidence records. |
| DS-04 | [Snap Store](https://snapcraft.io/globulation2) | Direct HTML200: publisher Bradley Arsenault (`genixpro`), stable **0.11.2.0**, updated **2026-10-11**, GPL-3.0-or-later; links old domain and current GitHub. | Store version differs from current website release. Publisher display name is public evidence, not an account access audit. No install performed. |
| DS-05 | [Legacy download wiki](https://globulation2.org/wiki/Download_and_Install) | Page last edited 2018-06-03 offers Beta 4 **0.9.4.4** source/Windows/Mac via Savannah, with an old OS X warning and distro links. | Historical catalog still live; commands and compatibility not treated as current instructions. |
| DS-06 | [SourceForge](https://sourceforge.net/projects/globulation2/) | Profile calls project Beta, Linux/Windows, GPLv2; registered 2007-06-05, update field 2013-04-03. Search exposes alpha23 and 0.9.2/0.9.4 Windows files. | GPLv2 metadata differs from wiki/current GPLv3 notices. Download execution, complete file inventory and account access not tested. |
| DS-07 | [Debian trixie](https://packages.debian.org/trixie/glob2) | HTTP 200, **0.9.4.4-8**, paired `glob2-data`, multiple architectures; legacy YOG description and old homepage. | Distribution-maintained package, not evidence of upstream marketing control. |
| DS-08 | [Fedora](https://packages.fedoraproject.org/pkgs/glob2/glob2/) | Public package record exposes 0.9.4.4 builds, e.g. 0.9.4.4-71.fc43, and old homepage/YOG description. | Distro package catalog; not the current native release. |
| DS-09 | [FreeBSD ports](https://www.freshports.org/games/glob2) | Public port record lists **0.9.5.0.g 20240607_8**, including 2026 maintenance, with upstream GitHub snapshot. | Port-maintained packaging. Successful installation not checked. |

## Prepared or unresolved distribution estate

Source evidence: game repository [`docs/releases/`](https://github.com/Globulation2/glob2/tree/c9198b854a2ea6fc16cd5524913cf96c5a80c499/docs/releases), [`docs/releases/store-setup.md`](https://github.com/Globulation2/glob2/blob/c9198b854a2ea6fc16cd5524913cf96c5a80c499/docs/releases/store-setup.md). These are preparation/workflow records, not proof of approved releases.

| Platform | Existing evidence | Public verification status |
| --- | --- | --- |
| Microsoft Store | `docs/releases/windows-store.md` names product ID **9PH4FCRMX19F** and submission assets. | Candidate [public URL](https://apps.microsoft.com/detail/9PH4FCRMX19F) returned HTTP 410. Availability/submission state unresolved. |
| Google Play | `google-play.md` and Android fastlane metadata/assets. | No public Globulation 2 store listing found with targeted search. No authenticated console inspected. |
| Apple iOS/iPadOS / TestFlight | `ios-app-store.md`, `ios-production.md`, `testflight.md`; website states no verified production listing. | Public production App Store URL not verified. TestFlight access not checked. |
| Mac App Store | `mac-app-store.md` release preparation. | No public listing verified. Native DMG availability does not imply App Store publication. |
| Amazon Appstore | `amazon-appstore.md` specifies Fire tablet release workflow. | No live listing URL established. Separate offline flavor described in source. |
| F-Droid | `fdroid.md` and build metadata. | Repository presence/approval and live package catalog not verified. |
| Flathub | Flatpak preparation; direct bundle on current downloads page. | No Flathub listing verified; runtime use is not game listing proof. |
| Steam / itch.io | `store-setup.md` preparation and release workflow references. | Targeted title/domain searches did not identify exact public listing URLs. Absence from search does not establish absence of drafts/submissions. |
| GOG | `gog-release.md` submission and packaging preparation. | Public listing/acceptance not verified. |
| China channels | `china-release.md` planning and separate edition constraints. | No distribution approval, publisher partnership or live store listing established. |
| Ubuntu | Legacy upstream link and package ecosystem references. | Direct noble package fetch returned500; current package version not verified. |
| Arch/AUR, Gentoo, openSUSE/Packman, Slackware, Mageia, MacPorts | Legacy wiki/Libregamewiki references; wiki itself marks MacPorts unmaintained. | Historical leads only until individual present catalogs are checked. |

## Presentation observations and missing comparison work

The inspected surfaces disagree in **version and description context**: modern website experimental 0.11.4.0; Snap stable 0.11.2.0; legacy wiki 0.9.4.4; Debian/Fedora 0.9.4.4; Libregamewiki 0.9.4.1. The current website explains colony work and browser play; older surfaces retain YOG and older platform descriptions.

The [legacy screenshot page](https://globulation2.org/wiki/Screenshots) explicitly labels Beta 2/0.9.2 captures and WinterDryad’s Beta 4 artwork. The live new homepage names three replay image files. SourceForge has a 2007 screenshot-update announcement. These establish different dated asset sets; no claim is made that every submitted platform currently uses a particular image. A complete console-to-source screenshot matrix, image hashes, publication dates, locales, dimensions and account owners remain missing. See [assets](assets.md) and [task ledger](../planning/tasks.md).
