# Storefront-v2 mobile gameplay captures

Raw, uncaptioned screenshots of the touch interface at store pixel sizes, as inputs for the captioned store sets. Nothing here has been scaled, cropped, composited or retouched. Captured 2026-11-24 from Globulation 2 0.11.8.0 (`origin/master` commit `5e96273ff62f`) with the HD artwork forced on. This is the second capture round; it replaces the first after the [round 1 review](../../review/round-1-mobile.md).

[Footage rule](../../../../planning/gameplay-video.md) · [selection.json](selection.json) (the gallery per device class, read by the caption renderer) · [manifest.json](manifest.json) (provenance per file)

## What is here

| Directory | Pixels | Orientation | How it was captured |
| --- | --- | --- | --- |
| [`iphone-6.9/`](iphone-6.9/) | 1320×2868 | portrait | The iOS app in the iOS Simulator (iPhone 17 Pro Max, iOS 26.5), `simctl io screenshot` |
| [`ipad-13/`](ipad-13/) | 2064×2752 | portrait | The iOS app in the iOS Simulator (iPad Pro 13-inch M5, iOS 26.5), `simctl io screenshot` |
| [`android-phone/`](android-phone/) | 1080×1920 | portrait | **Interim host render** at density 2.625 (420 dpi, 411×731 dp); no longer in `selection.json` since 2026-11-25 |
| [`android-tablet-7/`](android-tablet-7/) | 1920×1200 | landscape | **Interim host render** at density 2.0 (960×600 dp); no longer in `selection.json` since 2026-11-25 |
| [`android-tablet-10/`](android-tablet-10/) | 2560×1600 | landscape | **Interim host render** at density 2.0 (1280×800 dp); no longer in `selection.json` since 2026-11-25 |
| [`android-phone-emulator/`](android-phone-emulator/) | 1080×1920 | portrait | The Android app in the Android emulator (Android 15), 420 dpi, `adb exec-out screencap -p`. See [Android emulator captures](#android-emulator-captures-2026-11-25) |
| [`android-tablet-7-emulator/`](android-tablet-7-emulator/) | 1920×1200 | landscape | The Android app in the Android emulator (Android 15), 280 dpi, `adb exec-out screencap -p` |
| [`android-tablet-10-emulator/`](android-tablet-10-emulator/) | 2560×1600 | landscape | The Android app in the Android emulator (Android 15), 320 dpi, `adb exec-out screencap -p` |
| [`saves/`](saves/) | | | The saved games the frames were loaded from, with each match's lobby setup and telemetry |

- **The galleries changed after the [round 2 final review](../../review/round-2-final.md) (2026-11-24).** `selection.json` now orders every class as `hero`, `battle`, `fair_deal`, `build`, `economy`, `territory`, `maps` (`asset_text.mobile_gallery_order` in `translations/platforms.json`), so a fight is in slot 2 (M2), and drops the `opponents` menu slide from every class (M1; "8 computer opponents" stays in the description text). The iPhone has no battle capture, so its `05-territory` frame, the best fight of any phone frame, is its `battle` slide and the iPhone has no territory slide: 6 slides on iPhone, 7 on every other class. The capture files keep their round 2 names (`NN-role-WxH.png`, numbered in the old slot order) and `manifest.json` still records the old slots and roles; `selection.json` is what the caption renderer reads. Running `tools/publish.py` again would renumber the files into the new order: `tools/picks.json` and `publish.py` already carry the new order and roles.
- `selection.json` lists the slots as `{"<device class>": [{"capture": "<file>", "role": "<role>"}, ...]}`, in store order.
- F-Droid phone screenshots use the `android-phone/` files. There is no `fdroid-phone/` folder; `manifest.json` maps `fdroid-phone` to `android-phone` under `aliases`.
- Only the selected frames are in the repository. Alternates stay in the capture scratch directory.
- Each directory has a `contact-sheet.jpg` for review (downscaled; not a store asset).
- The PNGs carry an alpha channel that is fully opaque. Flatten to RGB when rendering store images, because App Store Connect rejects alpha.

## Android emulator captures (2026-11-25)

The three `*-emulator` classes are screenshots of the real Android app running in the Android emulator. They replace the interim host renders for Google Play, F-Droid and Amazon (review M8). **Since 2026-11-25 `selection.json` uses them:** the `android-phone`, `android-tablet-7` and `android-tablet-10` classes list the seven files of `android-phone-emulator/`, `android-tablet-7-emulator/` and `android-tablet-10-emulator/` in file order (`01-hero` … `07-maps`, roles as in the file names), named with their folder; `amazon-tablet` takes the 2560×1600 set (no doubled Wi-Fi glyph to worry about, and the trim removes the status bar anyway), F-Droid the phone set. The caption renderer trims the status bar and gesture band (phone 62/65 px, 1920×1200 40/57, 2560×1600 48/64; [tool README](../../tools/README.md#system-bar-trim-per-capture)). `tools/publish.py` writes the whole of `selection.json` from `tools/picks.json`, which still names the host renders for the Android classes: running it again would switch them back, so restore the three Android classes afterwards.

### Build and devices

- **App.** Globulation 2 0.11.8.1, `origin/master` commit `a9f878b9ff61`, built with `platforms/mobile/android.py build --arch arm64-v8a --release` and signed with `android.py sign` (local developer key). That is the Google Play configuration (arm64-v8a, online play included), not the Amazon `--amazon-apk` edition; the two differ only outside a match (the Amazon edition has no online hub). The only change to the game is [`tools/capture-build.patch`](tools/capture-build.patch), applied at configure time with `GLOB2_CAPTURE_MCP=1` exactly as for the iOS Simulator: it compiles the loopback automation listener into the mobile core and changes no rendering, HUD or simulation code. APK SHA-256 `56a37485fa5da9785218742fa228d6398e48737e9aa5cb8317690bc3ebe42637`.
- **Emulator.** The game repository's pinned emulator 37.1.11 and system image `system-images;android-35;default;arm64-v8a` revision 2 (`platforms/mobile/emulator.json`; Android 15, API 35, build `AE3A.240806.019`, userdebug), run on an Apple-silicon Mac with host GPU rendering (`-gpu host`), each emulator registered with its own ADB server on port 15077. SDK packages installed for the build: `platforms;android-36`, `build-tools;35.0.0` and `platform-tools`, through `python3 tools/dev_environment.py sdkmanager`.
- **AVDs** ([`tools/android_avds.py`](tools/android_avds.py)):

| Class | AVD | Panel | Density | Screen in dp, as held |
| --- | --- | --- | --- | --- |
| `android-phone-emulator` | `glob2-store-phone` (`pixel_2` hardware profile) | 1080×1920 | 420 dpi (2.625) | 411×731 dp, portrait |
| `android-tablet-7-emulator` | `glob2-store-tablet7` (`Nexus 7 2013` hardware profile, density set to 280 dpi) | 1200×1920 | 280 dpi (1.75) | 1097×686 dp, landscape |
| `android-tablet-10-emulator` | `glob2-store-tablet10` (`Nexus 10` hardware profile) | 1600×2560 | 320 dpi (2.0) | 1280×800 dp, landscape |

- **Why 280 dpi for the 1920×1200 class.** At the Nexus 7's own 320 dpi the landscape app area after the status bar and navigation handle is 960×544 dp. That is under the touch HUD's 600 dp tablet threshold (`tabletShortestSide`), so the game uses its phone-style landscape layout: a bottom bar and a side panel that stays open over the right third of the map. One test frame was taken that way and not kept. A 1920×1200 panel at 280 dpi is an 8-inch-class tablet (about 283 ppi) and gets the tablet rail, as the interim host render did. This is a real product behaviour on 7-inch xhdpi tablets held in landscape, and is reported to the game's owner rather than worked around.
- **Landscape** is the tablet display held at 90 degrees (`user_rotation 1`, auto-rotate off), as a player turning the tablet would; the game follows the display orientation.
- **System bars are in the frames.** The app draws edge to edge, and the game paints the status-bar and navigation-handle insets navy. The status bar uses Android's System UI demo mode (the Android counterpart of `simctl status_bar override`): 9:41, full Wi-Fi, full battery, no notification icons, mobile signal hidden. Navigation is the gesture handle, not the three-button bar. On the 1920×1200 class the demo status bar shows two Wi-Fi glyphs (an emulator demo-mode quirk that a second demo command did not clear); together they are about 50 px wide in the top-right corner. These navy bands (about 40–65 px at the top and bottom of every class) replace the flat navy strip of the host renders (review S2); the caption renderer trims them (since 2026-11-25).
- **HD artwork forced on**, as in the other classes: the profile written into the app's internal storage sets `highResolutionArtworkChoice=on`, confirmed by reading the app's `preferences.txt` back from the device after a session.

### Protocol differences from the host renders

- The disposable profile (preferences and the one save) is written into the app's internal storage (`/data/data/org.globulation2.glob2/files/`, which is where the app's Load game dialog reads `games/`) with `adb root`, and the match is loaded through the game's own Load game screen. The listener's port is forwarded with `adb forward`.
- Frames are `adb exec-out screencap -p` at native resolution, byte for byte. The event list is read again the moment screencap starts writing its PNG (the display is captured before the PNG is encoded, which takes 1–3 s on these panels), so the "after" reading belongs to the frame rather than to a later moment.
- Everything else is the clean-state protocol above: zone erase before every frame and zero zone-outline pixels in the saved image, at most two event rows, a non-negative first stat, live play at 1x, the *Health and food bars* lens switched off, and *Continue playing* on the "You have won" dialog where it appeared. The per-file numbers and the emulator, Android version, density, build commit, save, tick, camera and player actions are in `manifest.json` (`"build": "android-emulator"`, `"emulator_capture": true`). The battle and territory frames are the best of four to seven runs per class at the same front as the host renders.

### The galleries, against the host renders

Fog is the share of the free map area drawn fog-dimmed; rows are the event rows in the frame.

| Slot | Phone | 7-inch class (1920×1200) | 10-inch (2560×1600) | Compared with the host render |
| --- | --- | --- | --- | --- |
| 1 hero | Meets: both pools and racetracks whole, lower third filled; one green row; fog 5% | Meets: one red row; fog 5% | Meets: no rows; fog 4% | Same framing (`--hero-fit`); real device pixels and system bars |
| 2 battle | Partly: about 30 red and 20 blue warriors face each other, two war flags, mostly lit centre; no enemy building in frame; one row; fog 31% | Meets the unit and building parts: about 30 blue and 20 red warriors in a line beside three blue buildings and a blue Swarm under construction, war flags; two rows; fog 30% | Meets the unit and building parts: about 40 red and 25 blue warriors beside a burning blue building and the blue Swarm, war flags; two rows; fog 39% | Better on both tablets: more units and less fog than the host frames (44% and 46%). The phone frame is about as busy as the host's (20% fog there, 31% here). Hit flashes are not distinguishable at this size; the star sprites are war flags |
| 3 fair_deal | Meets: inns, hospitals and a Swarm, no rows, fog 4% | Meets: lakeshore with globs swimming, wheat, inns, a Swarm; one row | Meets: lake, wheat fields, inns, a Swarm, globs swimming; one row | As the host frames |
| 4 build | Meets; unlabelled icons on the phone, as on every phone | Meets; named palette, no rows | Meets; named palette, one row | As the host frames |
| 5 economy | Meets: Inn with Food 47/50 and its fruit lines beside the algae lake and a wheat field; the Swarm is mostly behind the priority dial | Meets: Food 49/50, cherries, oranges and prunes in stock, a Swarm; no rows | Meets: Food 50/50 with fruit in stock, a Swarm; no rows | As the host frames; the phone's Swarm is less visible than in the host frame |
| 6 territory | Partly, as every class: palette open, flag just placed, a red line facing a blue line; no range circle; two rows; fog 29% | Partly: red and blue warriors fighting around the new flag; one row; fog 26% | Partly: as the 7-inch; two rows; fog 31% | Less fog on the 7-inch (35% on the host) and the 10-inch matches the host (31%); the phone has more fog than the host (17%) but shows both colours |
| 7 maps | Meets: FourSquares1 island, algae sea, sand, violet forest; two red rows | Meets; the sea shows only in the top-left corner, violet forest frames the colony; two rows | Meets: algae sea in both top corners, sand, violet forest; two rows | As the host frames |

**Selection** (applied 2026-11-25): for each `*-emulator` class, the seven files in file order, roles as in the file names (`hero`, `battle`, `fair_deal`, `build`, `economy`, `territory`, `maps`). Amazon (`amazon-tablet`) takes `android-tablet-10-emulator` (2560×1600); Google Play phone and F-Droid take `android-phone-emulator`.

### Reproduce

```sh
# Game worktree at the release commit (never the shared checkout), with the capture patch
git -C glob2 worktree add ../glob2-wt-android-capture -b android-store-capture origin/master
cd glob2-wt-android-capture && git apply /path/to/captures/mobile/tools/capture-build.patch
export PATH=<dir with python3 -> python3.13>:$PATH   # the asset encoder needs a Pillow wheel 3.15 lacks
python3 tools/dev_environment.py sdkmanager -- "platforms;android-36" "build-tools;35.0.0" platform-tools
python3 platforms/mobile/setup_ndk.py && python3 platforms/mobile/setup_tools.py --glslang
python3 platforms/mobile/dependencies.py --arch arm64-v8a --release
GLOB2_CAPTURE_MCP=1 python3 platforms/mobile/android.py build --arch arm64-v8a --release
python3 platforms/mobile/android.py sign --arch arm64-v8a --release

# AVDs, ADB server and emulators (serials emulator-5600, -5602, -5604)
export GLOB2_WT=$PWD GLOB2_SCRATCH=/path/to/scratch GLOB2_ADB_PORT=15077
T=/path/to/captures/mobile/tools
python3 $T/android_avds.py create
python3 $T/android_avds.py adb-server &
python3 $T/android_avds.py run glob2-store-phone 5600 &   # likewise glob2-store-tablet7 5602, glob2-store-tablet10 5604
adb -P 15077 -s emulator-5600 install -r build/android/device/arm64-v8a/24/client/release/android-project/app/build/outputs/apk/release/app-release-development.apk

# Candidates (one MCP port per emulator), then the chosen files
RUN="uv run --python 3.13 --with pillow --with numpy python $T/capture.py"
GLOB2_MCP_PORT=47960 $RUN android-phone-emulator --save bigpond-n-t45017 --slots hero --hero-fit --rows 1
GLOB2_MCP_PORT=47960 $RUN android-phone-emulator --save bigpond-n-t45017 --slots build,economy --rows 1
GLOB2_MCP_PORT=47960 $RUN android-phone-emulator --save bigpond-n-t45017 --slots fair_deal --rows 1 --fair-at 49,17
GLOB2_MCP_PORT=47960 $RUN android-phone-emulator --save bigpond-n-t27015 --slots battle --fight-at 39,60 --fight-rows 2
GLOB2_MCP_PORT=47960 $RUN android-phone-emulator --save bigpond-n-t27015 --slots territory --territory-at 40,60 --territory-max-dim 0.6 --wait 300
GLOB2_MCP_PORT=47960 $RUN android-phone-emulator --save foursquares-n-t33028 --slots maps --maps-at 7,118,19 --wait 1500
# tablets: the same, with --fair-at 45,21 and maps --hero-fit --wait 1500; the 10-inch battle used --fight-zoom fight
uv run --python 3.13 --with pillow python $T/publish_android.py   # reads tools/picks-android.json
```

`publish_android.py` copies the candidates named in [`tools/picks-android.json`](tools/picks-android.json) byte for byte, re-checks size, hash, HD artwork and the clean-state protocol, replaces only these classes' entries in `manifest.json` and writes their contact sheets; it does not touch `selection.json` or the other classes. Fight frames are slow to get: the event list carries three or more rows most of the time, and per run of `capture.py` the battle slot kept zero to three frames.

## The galleries

What each slot shows and how far it meets the shot definition and the review's acceptance test. "Meets" means every part of the test holds; anything short of that is said.

The table below is the capture round's record, in the round's original slot numbering. The `opponents` row is no longer in any gallery, and the iPhone `territory` frame is now its `battle` slide (row 6).

| Slot | Shot test | iPhone 6.9 | iPad 13 | Android phone | Android 7" | Android 10" |
| --- | --- | --- | --- | --- | --- | --- |
| 1 hero | Core buildings, both pools and racetracks whole in the free map band, dense units, lower third filled | Meets (one green row) | Meets (one green row) | Meets (one red row at the top edge, over inns) | Meets (one red row between buildings) | Meets (no rows) |
| 2 build | Build palette open over a live, busy colony | Meets; unlabelled icons on phones | Meets; named palette | Meets; unlabelled icons; the school at the right edge is cut | Meets; named palette | Meets; named palette, no rows |
| 3 fair_deal | Busy, clean colony frame clearly different from the hero | Meets: lakeshore inns and wheat below violet forest, one green row; a fog-dimmed patch in the wheat (11%) | Meets: Swarms and wheat by the algae lake; a racetrack is cut at the bottom-left corner | Meets: inns, hospitals and a Swarm, no rows, no pools | Meets: lakeshore inns and a Swarm | Meets: lake, wheat fields, inns, globs swimming, no rows |
| 4 battle | At least 12 units per colour, a hit effect, enemy buildings, lit ground | **Not filled**: no iPhone frame passed the two-row limit in five runs (see below); the iPhone gallery has seven slots | Partly: about 30 red and 15 blue warriors, hit effects, blue buildings; bands of fog-dimmed ground (41% of the map area) | Partly: about 30 red and 18 blue warriors, two hit effects, mostly lit (20% fog-dimmed); no whole enemy building in frame | Partly: about 20 red and 15 blue, a burning blue building, blue buildings at the left edge; 44% fog-dimmed | Partly: about 20 red and 14 blue, two hit effects, blue buildings and Swarm; 46% fog-dimmed |
| 5 economy | A non-upgrading Inn selected so its food lines show, a lit wheat field, workers and a Swarm | Meets | Meets; pool and racetrack cut at the bottom edge | Meets; the dial covers the lower half, as it does on every phone inspector | Meets | Meets |
| 6 territory | Flags palette open, a just-placed flag on the frontier, its range circle | Partly: palette, flag just placed, warriors streaming to it; no range circle (see below). **Used as the iPhone `battle` slide since 2026-11-24**: a blue line and a red line face each other across the centre, about 15 blue and 25 red warriors, two war flags, a lit field | Partly, as iPhone | Partly, as iPhone | Partly, as iPhone | Partly, as iPhone; the strongest: dozens of warriors, mostly lit |
| 7 maps | A visually distinct second map with an active, zone-free colony | Meets: FourSquares1, sea with algae, sand, violet forest; two red rows over water | Meets: the island ringed by sea; two rows over water | Meets; the racetrack is cut at the right edge; two rows | Meets, though the sea shows only in a corner; violet forest frames the colony | Meets; two rows touch a Swarm at the top |
| 8 opponents (dropped 2026-11-24) | Three or more enemy colours fighting in one view, from a many-opponent match | **Not met**: the computer opponent picker (menu) | **Not met**: picker | **Not met**: picker | **Not met**: picker | **Not met**: picker |

All gameplay frames have zero zone squares, at most two event rows, a non-negative first stat, and are live play at 1x. The per-file numbers (rows, stat, fog fraction, zone pixels, tick, camera) are in `manifest.json`.

## Clean-state protocol

Every gameplay frame was kept only if all of these held at the moment it was read. `tools/capture.py` checks them and otherwise waits and tries again, so each kept frame is an ordinary moment of the running match; `tools/publish.py` checks them again from the sidecar before copying.

- **No zone squares.** The zone tool erases the co-controlling AI's forbidden, guard and clearing zones over the whole map immediately before the frame, and the saved image is then searched for straight runs of the zone outline colours at least 0.7 of a tile long. Zero outline pixels are required (`zone_outline_pixels`).
- **At most two event rows**, counted from the game's own controls before and after the frame (`event_rows` holds the union of both readings).
- **A sane first stat.** Free workers is not negative, so the red outline never shows (`first_stat`).
- **Lit ground.** Colony frames need less than 15% of the free map area fog-dimmed (`fog_dimmed_fraction`, estimated from the pixels). Fights happen on rival ground, which the colony sees only around its own units; see the battle row above.
- **HD artwork forced on.** The capture profile sets `highResolutionArtworkChoice=on`, so the session step-down that turns Auto HD artwork off after frame hitches or memory pressure cannot apply. Every file records `hd_artwork` in the manifest.
- **Framing.** Hero frames are placed by `--hero-fit`, which zooms out (to 16-pt tiles at most) until every swimming pool and racetrack fits whole in the free map area and sets that cluster on the bottom of the band so the rest of the colony fills it. Other colony frames use a search that rewards whole core buildings and a filled lower third, or a camera tile given on the command line (`--fair-at`, `--maps-at`, `--fight-at`, `--territory-at`), recorded in each file's `camera`.

## How honest these are

- **iOS files are real app pixels.** The simulator runs the iOS app built from the release commit with `platforms/mobile/ios.py` (plus the capture-only patch below), and the simulator framebuffer is saved at the device's native resolution. They are simulator screenshots, not hardware screenshots: the simulator package draws with the portable SDL renderer, because the SDL GPU (Metal) renderer that devices use is not available in the Simulator.
- **Android files are an interim set, not device screenshots.** The local Android SDK lacks `platform-tools`, `build-tools` and `platforms;android-36` because their licences have not been accepted on this Mac, so no emulator build exists. The Android sets are the desktop build of the same commit drawing the same shared touch interface (`--interface touch`) into a surface of the Android pixel size at the Android density scale (`--ui-scale`), with the SDL dummy video driver and the game's software renderer. Layout, HUD, sprites and text are produced by the game at that size; nothing is upscaled. They cannot show Android system bars, display cutouts or any Android-only rendering difference. Every Android entry in `manifest.json` carries an `interim` note. Replace them with emulator or device captures when a toolchain is available; `tools/capture.py` only needs a new target class.
- **Every gameplay frame is live play at normal speed (1x).** The match is loaded through Load game and keeps running; nothing is paused or stepped. The manifest records the tick and `"paused": false`.
- **Player view, not spectator view.** The saves come from custom matches set up in the lobby with colony 1 (red) as **You + AI** (shared control with the Nicowar AI) against AI colonies, standard rules. The AI grew the colony; the HUD is the local human player's.
- **Player actions before a frame** are ordinary in-game controls and are listed per file (`player_actions_before_capture`): the *Health and food bars* lens switched off in the Tools strip; the zone erase described above; on the late save, *Continue playing* on the "You have won" dialog where it appeared; for the territory frames, a war flag placed at the front at the recorded tile.
- **Menu frames** (`"kind": "menu screen"`, the opponents slot, no longer in any gallery) are the custom game setup on a fresh profile, with the computer opponent picker open. No match is running.
- **The simulator's Dynamic Island is not in the frames.** The simulator intermittently paints the island into its framebuffer, which a device screenshot never contains; such frames were retaken, not edited.
- Status bar on iOS: 9:41, full signal, Wi-Fi, full battery (`simctl status_bar override`). The iPad status bar also shows the capture date, and iPadOS 26 draws its window resize handle in the bottom right corner.

## Not met, and why

- **Opponents as gameplay.** No frame shows three rival colours fighting in one view. Five eight-colony matches were played on Playground (free-for-all twice, you-versus-all, 2v2v2v2 and 4v4): in each the shared colony stayed tiny or was eliminated before tick 30,000. A random eight-colony map (Lava shield), Sand River (six colonies) and FourSquares1 (four) reached developed colonies, but scans of their saves found at most two rival colonies' warriors within one screen; the best Sand River fight has red, blue and a few lime units, which is two enemy colours. The `opponents` slot was therefore the computer opponent picker, which lists the eight AI opponents (Numbi, Castor, Econo, Warrush, Cortex, Nicowar, Cabino, Maxima). The round 2 final review dropped it from every gallery on 2026-11-24 (a menu screen fails the footage rule, and the panel showed AI ratings and a ninth "Inactive" entry); the files stay here as a record.
- **iPhone battle.** Five iPhone runs at the front (tick 27,000–36,000 of the battle save) found no moment with at most two event rows that still held after the slower simulator screenshot; the event list there carries three to eight rows almost continuously. The iPhone territory frame shows the same fight with the Flags palette open, and since 2026-11-24 it is the iPhone `battle` slide. Another run may succeed; the command is in Reproduce.
- **Lit ground in battle and territory frames.** The fights are on the blue colony's ground, which the red colony sees only around its own units; there is no fog toggle for a player (only replays and spectators have one). The frames were taken at the first contact after loading, centred on the lit front line, and the least dimmed were chosen, but 17–46% of each map area is still fog-dimmed (`fog_dimmed_fraction` per file). The one mostly lit battle frame (Android phone) has the blue buildings just out of frame. A late-game raid inside the red colony (which would be lit) was searched for and not found: by tick 42,000 no screen holds more than six rival warriors.
- **Range circle with the Flags palette open.** The game draws a flag's range circle only while the flag is selected or being placed, and both states replace the palette; the War Flag inspector is excluded by the brief. The territory frames show the palette open over warriors answering a flag that was just placed.
- **iPad landscape (2752×2064).** iPadOS ignores an app's orientation request, so the device itself has to be rotated; `simctl` has no rotate command, and a landscape-only copy of the app is letterboxed at reduced scale.
- **Android emulator or device captures,** for the reason above.
- Phone landscape, 10-inch portrait, the map peek and the War Flag inspector were dropped after the review.

## Reproduce

Everything runs from a game worktree at the release commit, never from the shared checkout.

```sh
# 1. Worktree and builds (full Xcode via DEVELOPER_DIR; put Python 3.13 first in PATH:
#    the build scripts need tarfile filters (3.12+) and a Pillow wheel that 3.15 lacks)
git -C glob2 worktree add ../glob2-wt-mobile-capture -b mobile-store-capture origin/master
cd glob2-wt-mobile-capture
git apply /path/to/captures/mobile/tools/capture-build.patch
export DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer
python3 buildsys/sdl3_dependencies.py --prefix build/sdl3/prefix --work build/sdl3/sources --jobs 5
GLOB2_SDL3_PREFIX=$PWD/build/sdl3/prefix PKG_CONFIG_PATH=$PWD/build/sdl3/prefix/lib/pkgconfig \
  python3 tools/dev_build.py release=1 glob2 \
  CXXFLAGS="-g -I$(brew --prefix openssl@3)/include" LINKFLAGS="-g -L$(brew --prefix openssl@3)/lib"
python3 platforms/mobile/dependencies.py --target ios --environment simulator --release --developer-dir $DEVELOPER_DIR
GLOB2_CAPTURE_MCP=1 python3 platforms/mobile/ios.py build --environment simulator --release --developer-dir $DEVELOPER_DIR

# 2. Isolated simulators; write their ids to $GLOB2_SCRATCH/sim.env as IPHONE=..., IPAD=...
export GLOB2_WT=$PWD GLOB2_SCRATCH=/path/to/scratch
SET=$PWD/build/mobile-tools/ios-simulators
xcrun simctl --set $SET create Glob2-Capture-iPhone-6.9 com.apple.CoreSimulator.SimDeviceType.iPhone-17-Pro-Max com.apple.CoreSimulator.SimRuntime.iOS-26-5
xcrun simctl --set $SET create Glob2-Capture-iPad-13 com.apple.CoreSimulator.SimDeviceType.iPad-Pro-13-inch-M5-12GB com.apple.CoreSimulator.SimRuntime.iOS-26-5

# 3. Saves: copy saves/*.game.gz to $GLOB2_SCRATCH/saves, or play new matches
python3 tools/make_saves.py bigpond-n --ticks 48000 --every 3000 --from 12000

# 4. Candidates per device class (the calls behind this set), then the chosen files and the indexes
RUN="uv run --with pillow --with numpy python"
$RUN tools/capture.py android-phone --save bigpond-n-t45017 --slots hero --hero-fit --rows 1
$RUN tools/capture.py android-phone --save bigpond-n-t45017 --slots build,economy,fair_deal --rows 1
$RUN tools/capture.py android-tablet-10 --save bigpond-n-t45017 --slots fair_deal --fair-at 45,21
$RUN tools/capture.py android-phone --save bigpond-n-t27015 --slots battle --fight-at 39,60 --fight-rows 2
$RUN tools/capture.py android-phone --save bigpond-n-t27015 --slots territory --territory-at 40,60 --territory-max-dim 0.6 --wait 240
$RUN tools/capture.py android-phone --save foursquares-n-t33028 --slots maps --maps-at 7,118,19 --wait 420
$RUN tools/capture.py android-tablet-10 --save foursquares-n-t33028 --slots maps --hero-fit --wait 600
$RUN tools/capture.py android-phone --menus
$RUN tools/publish.py        # reads tools/picks.json, writes manifest.json, selection.json and contact sheets
```

The iOS classes take the same arguments; for fight frames add `--rows-margin 1`, because a simulator screenshot is slow enough that a new event row often arrives while it is taken. They use MCP port 47912 unless `GLOB2_IOS_OWN_PORT=1` is set, which keeps `GLOB2_MCP_PORT` so the iPhone and iPad simulators can run at once. Host instances take `GLOB2_MCP_PORT` (47812 and up).

`capture-build.patch` is the only change to the game: three small edits that let a local iOS Simulator build compile in the desktop-only MCP automation listener (`GLOB2_CAPTURE_MCP=1`), so the scripts can tap the real touch controls and move the camera. It changes no rendering, HUD or simulation code and must never ship. The listener is switched on by the disposable profile the scripts write into the app container (`mcpEnabled=1`).

A loaded save does not replay identically: AI controllers plan asynchronously, so each run of `capture.py` sees a slightly different continuation, and candidates are chosen by eye. The event list is the usual bottleneck: a fight frame often waits minutes for a moment with two rows or fewer.

## Reusable saves

| Save | Use | State |
| --- | --- | --- |
| [`saves/bigpond-n-t45017.game.gz`](saves/) | hero, build, economy, fair_deal | A big pond, tick 45,017. The red colony has about 340 workers, 240 warriors and 70 buildings and has nearly won, so the event list is short and the whole colony is lit. The "You have won" dialog appears a minute or two after loading; the scripts press *Continue playing*. |
| [`saves/bigpond-n-t27015.game.gz`](saves/) | battle, territory | The same match at tick 27,015: the red army (about 180 warriors) is attacking the blue colony to the south-west. The front line is around tile 39,60 for the first 1,000 ticks after loading; that is when the fights are biggest and the event list is shortest. |
| [`saves/foursquares-n-t33028.game.gz`](saves/) | maps | FourSquares1 (islands), tick 33,028: the red colony on its island, at war with three AI colonies. Free workers hover near zero, so frames wait for the first stat to be non-negative. |

Things to know when making more:

- Fast-forward at 13x at most. At unlimited speed the simulation outruns the AIs' planning and colonies stay tiny.
- Use the game's software renderer with the SDL dummy driver. The portable SDL renderer crashed in `SDL_UpdateTexture` about 20 seconds into a match in that setup (0.11.8.0).
- Wait about 12 seconds after loading before the first frame; the loading fade leaves earlier frames washed out.
- Of the AIs tried as co-controller on A big pond and Playground, only Nicowar grew a large colony. Castor stalled at five workers and Numbi stayed under 50.
- Late in a won match is the only time the event list is short. In mid-game it held three to eight rows in every save sampled.

## Tools

| File | Purpose |
| --- | --- |
| [`tools/make_saves.py`](tools/make_saves.py) | Sets up a custom match in the lobby (You + AI versus AIs), fast-forwards and saves through the game menu, with telemetry for picking moments |
| [`tools/capture.py`](tools/capture.py) | Loads a save on one device class and captures clean-state candidates for each gallery slot, or the setup menus |
| [`tools/picks.json`](tools/picks.json) | The chosen candidate for each class and slot, with its description |
| [`tools/publish.py`](tools/publish.py) | Copies the candidates named in `tools/picks.json` byte for byte, checks pixel sizes, hashes, HD artwork and the clean-state protocol, and writes `manifest.json`, `selection.json` and the contact sheets |
| [`tools/g2.py`](tools/g2.py), [`tools/mcp.py`](tools/mcp.py) | Targets (host render, iOS Simulator, Android emulator) and the MCP client |
| [`tools/contact_sheet.py`](tools/contact_sheet.py) | Contact sheet for a directory |
| [`tools/capture-build.patch`](tools/capture-build.patch) | The capture-only game patch described above |
| [`tools/android_avds.py`](tools/android_avds.py) | Creates and runs the three store AVDs and their separate ADB server (Android emulator classes) |
| [`tools/picks-android.json`](tools/picks-android.json), [`tools/publish_android.py`](tools/publish_android.py) | The chosen emulator candidates, and the publisher that adds only the `*-emulator` classes to `manifest.json` |
