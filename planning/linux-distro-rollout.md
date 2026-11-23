# Linux distro rollout

Baseline on 2026-11-23 is [Globulation 2 0.11.7.0](https://github.com/Globulation2/glob2/releases/tag/v0.11.7.0). The [engineering tracker](https://github.com/Globulation2/glob2/issues/1311) records native packaging work and downstream submissions. The [0.11.4.0 handoff](https://gist.github.com/genixpro/3970738a7a839b32b83db671db20545f) is prior evidence for recipe structure and upgrade tests. Current candidates need fresh evidence from the published source tarball after the [CMake migration](https://github.com/Globulation2/glob2/pull/1645).

## First wave

Start the Tumbleweed, Arch, and Debian candidates in parallel. Use the Debian source package for Ubuntu compatibility builds while the Debian upload is pending. Fedora starts in Rawhide. Gentoo needs a CMake ebuild and a willing reviewer or proxy maintainer.

| Distro and target | Observed downstream baseline | Step toward publication | 0.11.7.0 status |
| --- | --- | --- | --- |
| openSUSE Tumbleweed | `games/globulation2` at `0.9.4.4`. [Games repository](https://ftp2.gwdg.de/pub/opensuse/repositories/games/openSUSE_Tumbleweed/src/) | Build in OBS, submit to Games, and track forwarding to Factory. The engineering tracker records the existing reviewer offer. | Candidate planned |
| openSUSE Leap | Repository coverage still to verify | Check current Leap dependencies and packaging policy after qualifying the Tumbleweed build. | Compatibility check planned |
| Arch Extra | `0.9.4.4-56`. [Package](https://archlinux.org/packages/extra/x86_64/glob2/) | Update the maintained PKGBUILD, verify a clean chroot build and upgrade, and propose the change to the Extra maintainer. | Candidate planned |
| Debian sid and testing | sid source series `0.9.4.4-11`. [Package](https://packages.debian.org/sid/glob2) | Preserve the executable/data split, run sbuild and Lintian, seek Games Team review and sponsorship on Salsa, then track testing migration. | Candidate planned |
| Debian 13 | `0.9.4.4-8`. [Source index](https://packages.debian.org/stable/source/allpackages) | Check build and upgrade compatibility. Assess backport eligibility after the unstable upload. | Compatibility check planned |
| Ubuntu development series | `0.9.4.4` series. [Launchpad publishing history](https://launchpad.net/ubuntu/+source/glob2/+publishinghistory) | Sync from Debian when eligible or prepare a merge when an Ubuntu delta is required. | Depends on Debian upload |
| Ubuntu 26.10 and 26.04 LTS | `0.9.4.4-11`. [Launchpad publishing history](https://launchpad.net/ubuntu/+source/glob2/+publishinghistory) | Rebuild the Debian candidate on both releases and assess released-series backports separately. | Compatibility checks planned |
| Fedora Rawhide | `0.9.4.4` series. [Package overview](https://packages.fedoraproject.org/pkgs/glob2/glob2/) | Use the maintained dist-git spec, qualify in mock, and work with maintainers on Koji and Bodhi. | Candidate planned |
| Fedora 45 | `0.9.4.4-75.fc45`. [Package overview](https://packages.fedoraproject.org/pkgs/glob2/glob2/) | Check the Rawhide candidate on Fedora 45 and confirm released-branch update eligibility. | Compatibility check planned |
| Gentoo | Former `games-strategy/glob2` removed. [Removal record](https://github.com/gentoo/gentoo/commit/3e8ec1262d16c7ce12b1dfb785e0339602a6f5f8) | Test a CMake ebuild with pkgcheck and a clean emerge, then seek Games or proxy-maintainer review. | Candidate planned, review path open |

The first milestone is a reviewable OBS request and Arch packaging change, with the Debian sid source package ready for Games Team review. While those requests are in review, inventory NixOS, Mageia, Alpine, and Void for package presence, dependencies, and contribution routes.

## Evidence and rollout

- **Glob2 engineering** owns source identity, shared CMake fixes, and the evidence for each candidate. Record clean build and package-manager installation, upgrade from the distro package where available, gameplay smoke, save/resume and replay checks, and removal with the user profile retained. Record architectures and exact package revisions. Keep the licensing and dependency decisions keyed to the source release.
- **Downstream maintainers** own acceptance and publishing. For each release, record candidate built, submitted, accepted, published, and installed from the official repository as distinct milestones. Link public build and review evidence as it becomes available.
- **Marketing** owns this ledger and launch copy. For each active target, update the version, latest verified milestone, public evidence, blocker, and next follow-up date when known. Use the [approved rollout](approved-storefront-rollout.md) for copy and imagery.
- **Website** adds a distro-specific install command and version after a clean machine can install and launch the published repository package. The [upstream release](https://github.com/Globulation2/glob2/releases/tag/v0.11.7.0) already provides direct-download Linux artifacts, including its Fedora 43 RPM, Ubuntu 22.04 tarball, Flatpak bundle, and Snap file. Link those artifacts under direct downloads.
