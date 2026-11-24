# Linux, open-source, and preservation submissions

[Campaign overview](README.md)

Working material for the desktop release. Nothing on this page has been posted or sent. The baseline is the 0.11.7.0 release published November 22, 2026. Describe the larger remaster separately from the changes in this specific build. [Release notes](https://github.com/Globulation2/glob2/releases/tag/v0.11.7.0) · [Official downloads](https://glob2.online/downloads/)

## r/linux_gaming

**Format.** Maintainer-written text post. The community bars LLM-generated posts, so this is an internal checklist. The maintainer writes their own title, body, and replies. The subreddit welcomes developers to share Linux games when they engage, asks for transparency about AI assistance, and expects substantially assisted projects to have at least two months of development history. Have the public development history handy. One personal observation and one genuine game capture give readers something to discuss. [Community rules](https://www.reddit.com/r/linux_gaming/) · [Native game developer precedent](https://www.reddit.com/r/linux_gaming/comments/1vefysn/i_released_a_native_linux_build_of_my_game_on/) · [Repository history](https://github.com/Globulation2/glob2/commits/v0.11.7.0/)

**What to cover in the maintainer’s own words**

- Introduce your actual role and identify Globulation 2 as a free, open-source RTS with a native Linux build. Lead with the modern native Linux release. Give HD graphics and the rebuilt online platform as examples of the broader remaster, then describe one specific Linux improvement you worked on or tried.
- Show the same scene in classic and high-resolution mode, with capture version, platform, and any settings readers need to interpret the comparison. If only one genuine scene is available, use it on its own.
- Include one personally tested install and first-run route. Record the distro, version, architecture, package, and what you ran successfully. Link the route you verified. The official downloads page explains the x86-64 direct Flatpak bundle and its GNOME runtime. It also links to the Snap Store and provides the Ubuntu tarball and Fedora RPM.
- Describe AI assistance in your own words. Check the release for the scope of code assistance, generated terrain and sprite enhancement, and link the tagged provenance. Keep game opponent AI distinct from generative tools.
- Follow the thread. Useful first responses cover the package source, tested distro versions, classic/HD art selection, and the steps that would let you reproduce an install issue. [Linux downloads](https://glob2.online/downloads/#linux) · [Snap Store](https://snapcraft.io/globulation2) · [Tagged graphics sources](https://github.com/Globulation2/glob2/blob/v0.11.7.0/content-src/gfx/README.md) · [HD pack notes](https://github.com/Globulation2/glob2/blob/v0.11.7.0/content-src/gfx/production/pack-metadata/README.md)

**Ready when** a maintainer has written the post, tested a native package, checked the post’s AI disclosure against the exact build, and can answer replies. The desktop first-run play check and comparison capture are still open.

**Package preflight on November 23.** The published Ubuntu 22.04 x86-64 tarball matched the official SHA-256. In an emulated x86-64 Ubuntu 22.04 container, its executable reported version 0.11.7.0, revision `d6596e5f8b9d` and SDL 3.4.16 with `glob2 info version`. This verifies the archive and executable identity. A maintainer should still check first-run gameplay and capture the comparison in a Linux desktop session. [Download and checksum](https://glob2.online/downloads/#linux)

## r/OpenSourceGames

**Format.** English text post with a tagged source link, license and content notices, and one illustrative image if cleared for public use. The community requires OSI-licensed content. Verify the license and attribution for the specific example you show. [Community rules](https://www.reddit.com/r/OpenSourceGames/) · [Comparable developer release](https://www.reddit.com/r/opensourcegames/comments/1xsshqh/grandleon_tactical_rpg_engine_05_release_major/)

**Working title**

Globulation 2 remastered — the free, open-source RTS returns with HD graphics and online play

**Working body**

I help maintain Globulation 2, a free, open-source RTS that first appeared in 2004. The globs choose their own jobs and routes based on the priorities and flags you set.

We’ve modernized the game across the board. It has native builds for current Linux, Windows and macOS, HD artwork and a redesigned interface. The rebuilt multiplayer platform has guest rooms for casual games, ranked matches, leaderboards and match records. We’ve also expanded the procedural map generators. The desktop release is free, and browser play is in early access.

Part of the HD work came from an archive of original artwork recovered by Stéphane Magnenat. The remaster includes 1,792 unit poses rendered from those Blender rigs. The tagged source includes the worker’s walk rig and the steps used to turn it into game frames.

The code is GPLv3, with component-specific notices in the licensing index. The remaster includes AI-assisted code contributions, some AI-generated terrain and some AI-enhanced sprites. The art notes record the provenance of those assets.

Start a match from the desktop release, try the new generators in a custom game, or open the built-in map editor. [Hedgerow Country gameplay clip](https://storage.googleapis.com/glob2-website-public/campaign-media/reddit/v1/hedgerow-country-battle-d8838a88.mp4)

[Desktop downloads](https://glob2.online/downloads/) · [Online play](https://app.glob2.online/) · [Tagged source](https://github.com/Globulation2/glob2/tree/v0.11.7.0) · [Licensing and notices](https://github.com/Globulation2/glob2/blob/v0.11.7.0/docs/development/licensing.md) · [Graphics provenance](https://github.com/Globulation2/glob2/blob/v0.11.7.0/content-src/gfx/README.md) · [HD pack notes](https://github.com/Globulation2/glob2/blob/v0.11.7.0/content-src/gfx/production/pack-metadata/README.md) · [Worker walk rig](https://github.com/Globulation2/glob2/blob/v0.11.7.0/content-src/gfx/originals/units/glob-worker-walk.blend) · [Rendering steps](https://github.com/Globulation2/glob2/blob/v0.11.7.0/tools/unit-animation/README.md)

**Before approval.** Adapt the opening to the poster’s actual role, credit Stéphane Magnenat and the original artists as appropriate, confirm scope of AI use, and check the links and any attached image. Use the approved Hedgerow Country gameplay clip if adding a visual of the remaster. Credit the original-rig material if including it as a second example. [Project history](https://glob2.online/history/project-history/)

## r/ObscureRTS

**Hold for an explicit moderator response.** Rule 4 conditionally allows improvements of older titles. Rule 7’s anti-piracy language includes an abandonware-only download line, and Rule 9 refers to AI-generated content. Clarify how those apply to this active, free project and to a comparison made with original-derived artwork. The draft below is for review only. [Community rules](https://www.reddit.com/r/ObscureRTS/) · [Remaster flair precedent](https://www.reddit.com/r/ObscureRTS/comments/1xavn2r/im_remaking_project_y_an_old_rts_where_robo/)

**Unsent modmail draft**

Subject — Would a Globulation 2 restoration post fit r/ObscureRTS?

Hi moderators, I help maintain Globulation 2, an open-source RTS whose first alpha appeared in 2004. I’d like to share a one-off post under Remaster/Remake showing a credited archival image alongside a modern render from an original Blender rig.

The release also includes AI-assisted code, some AI-generated terrain and some AI-enhanced sprites. The proposed comparison would show only the original rig’s artwork. Would the remaster and comparison be eligible under your rules? If so, may I include the official page for the free desktop release?

Thanks for helping me make sure the post fits the community.

**Submission brief if cleared.** Name the game, approximate year, and verified original developer credit in the title. Use `Remaster/Remake`, label the original and modern images, credit each image source, and describe what was recovered and what players will recognize. Use only links and media the moderators have cleared. If they decline or give no clear answer, leave this subreddit out of the campaign.

## Communities to omit

- **r/RealTimeStrategy.** The November 3 update directs AI-assisted game projects elsewhere and removed the old megathread route. Leave this release out while that policy applies. [Moderator update](https://www.reddit.com/r/RealTimeStrategy/comments/1xmkiuj/rrealtimestrategy_announcement_mobile_games_ai/)
- **r/opensource.** The current project-promotion policy restricts AI-made projects and adds participation and maintenance eligibility requirements. Use r/OpenSourceGames for this release. [Moderator policy](https://www.reddit.com/r/opensource/comments/1xelcuf/your_tokens_arent_valuable_no_more_ai/)
