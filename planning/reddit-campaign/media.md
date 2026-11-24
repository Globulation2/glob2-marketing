# Reddit campaign media

[Campaign index](README.md) · [Marketing gameplay video standards](../gameplay-video.md) · [Approved storefront imagery](../approved-storefront-rollout.md#approved-imagery-only--2026-10-30) · [Current desktop release](https://github.com/Globulation2/glob2/releases/tag/v0.11.7.0)

Updated on November 23, 2026. The lead video is a mid-game battle captured for the campaign. The approved storefront screenshot and earlier tutorial clips are documented below.

## Ready media and where to use it

| Use | Asset | Provenance and limits |
| --- | --- | --- |
| **r/Games Indie Sunday and r/StrategyGames** | [Four Squares mid-game AI battle](../../assets/reddit-campaign/four-squares-ai-midgame.mp4) | Four Cortex opponents on the native macOS build, shown at 68% zoom. The view holds on the red colony’s southern edge as green units attack. [Capture details](../../assets/reddit-campaign/README.md) |
| **r/IndieGaming** | [Approved Four Squares strategic-view PNG](../../assets/storefront-approved-v1/03-four-squares-strategic.png) | Native spectator capture from an earlier 0.11.4.0 build, with four Cortex-controlled colonies at 25,000 ticks. The 2560 × 1440 still shows the strategic layer and spectator HUD at 32% zoom, with two colonies centered, building-purpose icons, army markers and territory colors. Use it for a strategic-view post. Use the capture recipe below for the planned transition video. [Capture pack](../../assets/epic-gallery-v5/README.md) |
| **r/OpenSourceGames** | [Tagged original-art catalog](https://github.com/Globulation2/glob2/blob/v0.11.7.0/content-src/gfx/CATALOG.md) and [recovered-runtime recipes](https://github.com/Globulation2/glob2/blob/v0.11.7.0/content-src/gfx/recovered-runtime.md) | These show inspectable preservation work. Use them alongside the tagged graphics README and licenses. For a specific example, pair the worker walk rig with the rendering instructions. This is also usable in a text-only post. [Worker walk source](https://github.com/Globulation2/glob2/blob/v0.11.7.0/content-src/gfx/originals/units/glob-worker-walk.blend) · [Animation workflow](https://github.com/Globulation2/glob2/blob/v0.11.7.0/tools/unit-animation/README.md) |
| **r/linux_gaming** | [Approved Four Squares strategic-view PNG](../../assets/storefront-approved-v1/03-four-squares-strategic.png), optional illustration of the game | Caption as an earlier 0.11.4.0 desktop spectator capture if used. A text-only submission with verified Linux install context is viable while the current Linux comparison is pending. |
| **r/ObscureRTS** | [Original game archive](https://globulation2.org/wiki/News_Archive) and [tagged artwork provenance](https://github.com/Globulation2/glob2/blob/v0.11.7.0/content-src/gfx/README.md), for private preparation | Prepare an archival frame and an original-rig render as a credited pair if moderators clear the post. Confirm reuse rights for the specific archival image. Keep media and download links out of the submission until the applicable rules are clarified. |
| **r/FreeGames** | [Official desktop download landing page](https://glob2.online/downloads/) | The download page is the primary link. Media is optional. |

The repository download responds successfully, but GitHub serves it as a binary attachment. Before submitting to Indie Sunday, use a direct video link verified to play while logged out. For a subreddit that accepts video uploads, the checked-in MP4 is ready to attach.

## Tutorial footage for follow-up

The food supply and counterattack clips remain available for player guides and follow-up comments. Both files were verified on November 23, 2026. The campaign leads with a match battle.

| Lesson | Video | Capture details |
| --- | --- | --- |
| **Counterattack** | [Direct MP4 showing the counterattack lesson](https://storage.googleapis.com/glob2-website-public/guide-media/v3/organizing-an-attack/attack-counterattack-clip-v3.mp4) | 29 seconds, 1440 × 900. Actual prepared browser lesson, version shown in game 0.11.6.0, High artwork and WebGL2. The War Flag is already placed when the clip opens. The request and radius are visible, warriors attack the cyan practice Swarm, and the lesson completes. [Capture record](https://github.com/Globulation2/glob2-online-website/blob/main/docs/handbook-high-guard-motion-evidence.json) |
| **Food supply** | [Direct MP4 showing Inn food supply](https://storage.googleapis.com/glob2-website-public/guide-media/v3/sustainable-food/food-consumption-refill-clip-v3.mp4) | 34 seconds, 1440 × 900. An earlier browser lesson on 0.11.6.0. Inn Food falls from 10/10 to 9/10 with hauling stopped, then recovers after requesting two haulers at high priority. The clip illustrates the food-supply decision. [Capture record](https://github.com/Globulation2/glob2-online-website/blob/main/docs/handbook-high-food-evidence.json) |


| MP4 | SHA-256 |
| --- | --- |
| Counterattack lesson | `e6e4327eaade7e34ebbb40bf72bf2eac4ce2e4fed2bb4a8a7406dc33dcc5034f` |
| Food supply lesson | `5fb6b964546b5938d1a7359eb8bfa23cc210aa71cbf8d56da1d4f6b173ffda` |

## Optional native captures and the held preservation comparison

Use the public desktop package, verify the in-game version and record the package name, platform, game/map, graphics setting and any scenario or AI conditions. Capture actual game output with its normal interface and keep a master file. Use the approved family above for imagery already cleared. Review any fresh capture before using it, including what it visibly contains and any narration, account names or private notifications.

- **Linux classic/HD pair.** Install the [current official Linux build](https://glob2.online/downloads/#linux) on a Linux desktop. With a renderer that supports texture filtering, set Artwork to Original, load a local Four Squares save and pause. Capture a close enough view to show sprite and terrain detail. Switch to High resolution, then reload the same save since the setting takes effect on the next game or editor load. Match the camera, zoom, viewport and HUD. Verify the visual change and record the tested distro/version and package. The paired shots demonstrate art changes on that setup.
- **StrategyGames native consequence clip.** On a live local colony, frame an active construction job and an inn with a need for wheat. Record the existing worker numbers, raise the inn's hauling demand or priority, and keep both counters visible long enough to show the actual response. Reserve this mechanic-focused capture for a follow-up.
- **IndieGaming native readability clip.** On Four Squares, hold the local view for several seconds, transition through the adaptive strategic view, then pause long enough to make the building icons, resource fields and neighboring territory legible. Capture the full HUD and review the export at normal feed size. The approved Four Squares still can accompany a text post if no clip is prepared.
- **ObscureRTS preservation pair.** Once moderator guidance is available, choose a recovered original unit pose with clear archival credit and a matching frame from the tagged runtime render. Keep the direction and pose aligned, show both at comparable display scale, and caption which file and artist each image derives from. Link the public provenance if approved.

For each final video, export a normal-speed MP4, review the opening, action and ending, and verify the exact public playback link before submission. Add the captured game version to the caption whenever it differs from the desktop release being announced.
