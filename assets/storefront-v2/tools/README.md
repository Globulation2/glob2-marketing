# Captioned store screenshots

[Raw mobile captures](../captures/mobile/README.md) · [English caption source](../../../translations/en.md) · [Store rules and comparables](../../../analysis/mobile-store-comparables.md) · [Footage rule](../../../planning/gameplay-video.md)

`screenshots.py` turns the raw gameplay captures into finished, captioned store screenshots for every language: one image per gallery slot, at the store's exact pixel size, with the caption in a brand-coloured band above the unretouched capture. It serves the stores that accept caption text inside screenshots: the App Store, Google Play, the Amazon Appstore and F-Droid. Microsoft, Steam and Epic take clean screenshots and are not handled here.

Output goes to [`../store-screenshots/`](../store-screenshots/) as `<store-set>/<locale>/<NN>-<role>-<WxH>.png`, with a `manifest.json` beside the images and a `contact-sheet-<locale>.jpg` per store set.

## Commands

Run from this directory. `uv` reads the pinned dependencies from the top of `screenshots.py`; nothing is installed into the system Python.

```sh
python3 fetch_fonts.py                              # once: download the caption fonts into .cache/fonts/

uv run screenshots.py check-config                  # print the gallery the tool will render
uv run screenshots.py fit --locale all              # preflight: fit every caption, write nothing
uv run screenshots.py fit --locale ja --min-scale 0.85   # caption editors' legibility gate
uv run screenshots.py render --locale en            # every store set, English
uv run screenshots.py render --locale de,fr,ja --set apple-iphone-6.9,google-play-phone
uv run screenshots.py verify --locale en
uv run screenshots.py contact-sheet --locale en
```

All locales, in one go (2,160 images with the round 2 gallery as revised after the final review: 45 locales × 48; allow roughly an hour and 7 GB, so point `--out` somewhere outside the repository unless the images are meant to be committed):

```sh
uv run screenshots.py render --locale all --out /path/outside/the/repo \
  && uv run screenshots.py verify --locale all --out /path/outside/the/repo \
  && uv run screenshots.py contact-sheet --locale all --out /path/outside/the/repo
```

| Option | Meaning |
| --- | --- |
| `--locale` | One locale, a comma-separated list, or `all` (the 45 codes in `translations/platforms.json`). Default `en`. |
| `--set` | One store set, a list, or `all` (default). |
| `--role` | Only these caption roles. Other files in the folder are left alone and the manifest is marked partial. |
| `--out` | Output root. Default `../store-screenshots`. |
| `--translations` | A directory of `<locale>.md` catalogs to read instead of `translations/`. For test strings only. |
| `--min-scale` | `fit` only. Exit non-zero if a caption on the phone sets is set below this share of full size, for example `0.85`. |
| `--jobs` | PNG encoder threads. |

`render`, `fit` and `verify` exit non-zero and list every problem by store set, locale and role. A locale with a caption that cannot be rendered gets no manifest, so `verify` fails for it until it is fixed.

### `fit`: the caption editor's check

`fit` writes nothing. For each requested locale it prints every caption as it would be set on the two phone-portrait sets, `apple-iphone-6.9` first because its type is largest and so its lines are shortest, then `google-play-phone`.

Every caption of one store set and locale is set at **one type size**: the largest at which all of that locale's captions fit the band in at most two lines. So one long caption makes every slide of its locale smaller, and shortening it makes every slide larger. The heading of each set gives that size:

```text
ru: caption type size as a share of full size, one size per store set (limit 36 characters, target 28)
  apple-iphone-6.9 (tightest): every caption at 77%
    hero        77%  SMALL  2 lines  28 chars  Стратегия в / реальном времени  (on its own 77%)
    build       77%         2 lines  23 chars  Вы решаете. / Они строят.
    ...
    territory   77%  SMALL  2 lines  27 chars  Выбирайте, / куда расширяться  (on its own 78%)
```

Each line gives the role, the set's type size as a share of the gallery's full size, `SMALL`, the number of lines, the caption's length in code points, and the caption with ` / ` where the line breaks. `SMALL` marks the captions that, even on their own, could not be set at 85% of full size: they are the ones holding the whole set below it, and the line ends with the size the caption would get on its own. Shorten those first. A caption the tool refuses is shown as `FAILED` with the reason. One more line per locale gives the smallest set size on the iPad and tablet sets, and the caption that sets it, for information (`fdroid-phone` is not listed because it is the same layout as `google-play-phone`). The limit and target in the heading come from `field_limits` in `translations/platforms.json`.

- Without `--min-scale`, `fit` exits non-zero only when a caption cannot be rendered at all (over the length limit, a banned word, a character no bundled font has, or no way to fit it).
- With `--min-scale 0.85`, it also exits non-zero when a phone set's size is below 85%, and lists the `SMALL` captions responsible. Tablet sets do not count towards the gate: their band is shallow and wide, so the size there is set by the longest caption on one line, and the one script that shrinks most there (Urdu's tall Nastaliq) is not something a caption edit can fix.
- Under "worth a look", `fit` and `render` list captions broken by a fallback rule, captions that could only be broken with a short word left at the end of the first line (`relaxed` or `loose`, see [How a caption is fitted](#how-a-caption-is-fitted)), and captions broken inside a clause because the break after their comma or full stop does not fit at the set's size ("No ads, no / in-app purchases"). Those read better shorter, or with a U+200B where the break should go.
- To move a line break, put a zero-width space (U+200B) where the break should go; see below. It counts as one character towards the limit.

Chromium comes from Playwright 1.63.0. If it is not installed yet: `uv run --with playwright==1.63.0 playwright install chromium`.

## Store sets

| Store set | Store | Captures from | Pixels |
| --- | --- | --- | --- |
| `apple-iphone-6.9` | App Store | `iphone-6.9` | 1320×2868 |
| `apple-ipad-13` | App Store | `ipad-13` | 2064×2752 |
| `google-play-phone` | Google Play | `android-phone` | 1080×1920 |
| `google-play-tablet-7` | Google Play | `android-tablet-7` | 1920×1200 |
| `google-play-tablet-10` | Google Play | `android-tablet-10` | 2560×1600 |
| `amazon-tablet` | Amazon Appstore | `android-tablet-10` | 2560×1600 |
| `fdroid-phone` | F-Droid | `android-phone` | 1080×1920 |

Orientations were fixed by the coordinator on 2026-11-24: phones and iPad portrait, Android tablets landscape. `amazon-tablet` uses the 10-inch captures because 2560×1600 is a size Amazon accepts and its 1280×800 dp layout is the one a Fire HD 10 shows. `fdroid-phone` has no captures of its own; it is the `android-phone` gallery checked against F-Droid's rules.

## Changing the gallery

The gallery is data. A slot is one line: a capture file and a caption role.

```json
{"capture": "01-hero-colony-1320x2868.png", "role": "hero"}
```

- **Final gallery:** when `../captures/mobile/selection.json` exists, the tool reads the slots from it and ignores `provisional_gallery`. Expected shape: `{"<device class>": [{"capture": "<file in captures/mobile/<device class>/>", "role": "<role>"}, ...]}` for `iphone-6.9`, `ipad-13`, `android-phone`, `android-tablet-7` and `android-tablet-10`. The reader also accepts the lists under a top-level `device_classes` key, a `slots` list per device class, `file` in place of `capture`, and `[file, role]` pairs. Anything else, a missing device class, an unknown role, a repeated role or a missing file stops the run with a message.
- **Order.** The store order of every mobile set is `asset_text.mobile_gallery_order` in `translations/platforms.json`: since the [round 2 final review](../review/round-2-final.md) (2026-11-24) **hero, battle, fair_deal, build, economy, territory, maps**, so a fight is in slot 2 and the fair-deal slide is still third (the App Store shows the first three portrait screenshots in search results). `selection.json` is rendered in its own order, but `check-config` and `render` refuse a class whose slots do not follow that list (a class may leave a role out: the iPhone has no territory slide), and refuse a role the list does not name.
- **Without `selection.json`:** `provisional_gallery` in [`gallery.json`](gallery.json), the first round's layout test material, sorted into the order above. To swap an image, change the file name. Then `render` and `verify` again; files for slots that no longer exist are removed from the output folders.
- Roles are the `screenshot_roles` in `translations/platforms.json`: `hero`, `build`, `economy`, `battle`, `territory`, `maps`, `opponents`, `fair_deal`. Only the roles in `mobile_gallery_order` are mobile slides: `opponents` was dropped from every mobile set by the round 2 review (M1; the picker menu failed the footage rule, and "8 computer opponents" stays in the description text), and `ai_coplay` is desktop-only.
- The pixel size is read from the capture itself. A size that is not listed for its device class in `device_classes` is refused: add it there with its `trim` and `band` first.
- `check-config` prints the gallery that will be rendered and where it came from, then dry-runs the system-bar trim of every slot of every device class (below) and exits non-zero if any slot would stop `render`. Each manifest records the same.

Since 2026-11-24 the gallery comes from the round 2 `selection.json`, revised the same day after the final review: the opponents slide is gone from every class, every class follows the order above, and the iPhone's `05-territory` capture (the best fight on any phone frame) is its `battle` slide, because no iPhone battle capture passed the clean-state protocol. That gives the iPhone 6 slides and every other set 7. The provisional gallery in `gallery.json` is the first round's and is used only if that file is removed.

### System-bar trim per capture

iPhone and iPad captures carry the iOS status bar at the top and the home-indicator band at the bottom. The size's `trim` in `device_classes` removes them (iPhone 184 px top and 104 px bottom, iPad 64 and 40). How a capture's strips are handled is decided per capture:

- **`flat-margins`** (the default for every capture): each strip is trimmed only if at least 90% of it is one flat colour, which holds for every gameplay frame, where the game letterboxes the system bars. Otherwise `render` refuses the capture before it sets any caption, because the strip holds game pixels.
- **`status-bar`**: for a capture that runs background art under the status bar, as the game's menu screens do. It trims exactly the size's top trim, without asking the strip to be flat, and trims nothing else: the bottom is left as captured and runs off the image edge like every other slide (the card already cuts more than the home-indicator band there, so the visible image is the same). Use it only after looking at the strip: it must hold nothing but the clock, signal, Wi-Fi and battery over background art, and the game's own interface must start at or below the trim line.

A non-default mode is set in `gallery.json` under `slot_trim`, by device class and capture file, with a `why` saying what the strip holds and the capture's `sha256`, so that a re-captured file under the same name is refused until someone looks at it again. (A `"trim"` and `"trim_why"` key on a slot in `selection.json` is read too, but `captures/mobile/tools/publish.py` rewrites that file, so `gallery.json` is where the decision is kept.) An entry naming a capture no longer in the gallery stops the run.

No capture uses `status-bar` now, and `slot_trim` is empty. The only two that did were the opponent picker menus `iphone-6.9/07-opponents` and `ipad-13/08-opponents`, dropped from the gallery on 2026-11-24. Every iPhone and iPad slot passes the strict check (top strips 95–97% flat, bottom strips 100%).

The Android captures are host renders with no system bars and are not trimmed. They carry a navy band along the top (rows 0–31 on the tablets, 0–41 on the phone), where the game reserves a 16 dp top inset and draws no map. It is not a flat margin and cannot be trimmed: the game's HUD is drawn over it (the stats panel from row 8 on tablets and row 10 on the phone, the tablet minimap from row 0), so the strip is only 71–88% one colour on the tablets and any trim deeper than the phone's 10 fully flat rows cuts into the HUD. It shows as a navy notch beside the stats panel at the card's top-left corner. The fix belongs at capture (render without the inset, or emulator or device captures); see the review's S2. Each image's manifest records `capture.trim_mode`, `capture.trim` (pixels per edge), `capture.trim_flat_share` (how flat each trimmed strip was), `capture.trim_why` for a non-default mode, and `capture.kind` (`gameplay` or `menu screen`) from the captures' own `manifest.json`.

## Layout

The layout is `framed`, revised on 2026-11-24 after the [round 1 layout review](../review/round-1-desktop-and-layout.md#part-3-captioned-layout):

- Night colony background (`#1b1229`, lifting to `#2b1c42` and `#34234f` at the top), from the design system's dark tokens.
- The capture as a card, fitted to the image **width** and running off the bottom edge: its flat system-bar margins are trimmed (iPhone status bar and home-indicator band, iPad status bar; menu screens lose the status bar only, see [System-bar trim per capture](#system-bar-trim-per-capture)), it is scaled down (never up) to the card width, it starts right under the caption band, and whatever does not fit is cut at the bottom edge of the image. Top corners are rounded (capped at 40 px so they never bite into a HUD element); the bottom corners are off the image. Nothing is drawn over the game image.
- A cream ring (`#f9e8bb` at 60% opacity, 0.4% of the image width) around the card, so its top edge reads against the game's own purple HUD, and a soft shadow.
- The caption in the band above the card, in bold (DejaVu Sans Bold for Latin, Greek and Cyrillic scripts; see below), cream `#f9e8bb`, centred, sentence case.
- The fair-deal slide has the same night background; its caption is in the action gold (`#e3c077`) and its card has a gold ring twice the normal width, so the listing's key promise stands out in the strip without looking like another product. It takes its capture from the gallery like every other slot (role `fair_deal`).

| Image size | Card width | Caption band | Full caption size | Gameplay share of the image |
| --- | --- | --- | --- | --- |
| iPhone 1320×2868 | 94.1% | 17% | 148 px | 78.1% |
| iPad 2064×2752 | 94.0% | 17% | 172 px | 78.0% |
| Android phone 1080×1920 | 94.1% | 17% | 118 px | 78.1% |
| Android 7-inch 1920×1200 | 93.0% | 16% | 112 px | 78.1% |
| Android 10-inch 2560×1600 | 93.0% | 16% | 150 px | 78.2% |

The card widths and bands are in `gallery.json` per image size (`card`, `band`, `caption_px`, `trim`); the gameplay share is recorded per image in the manifest (`capture.gameplay_share`). The review asked for 92% cards on iPad and tablets, but with a 16–17% band that leaves gameplay at 76–77% of the image, under its own 78% target; 93–94% meets it. With the 2026-11-24 captures, the cut on iPhone falls just under the bottom toolbar's icons, so its labels are off the image; on Android phones the whole bottom toolbar and a strip of map are; iPad and Android tablets have their toolbar at the side and lose only map. Full caption size on phones is about 11% of the width; the size actually used is the set's one size (see `fit`), which for English (2026-11-24 caption pass) is 95% of full on iPhone and 97% on Android phone.

Design constants are at the top of `screenshots.py` (`VARIANTS`, `LAYOUTS`). The `bleed` layout of the first round (capture at 1:1, flat band in the trimmed space) was removed; the framed card now gives the game more of the image than it did.

## How a caption is fitted

Headless Chromium lays out and draws the caption, so HarfBuzz does the shaping and ICU the bidirectional ordering. Pillow in this environment has no Raqm (`PIL.features.check('raqm')` is false), so it is used only for compositing. The capture never passes through the browser: Chromium draws the background, ring, shadow and caption; Pillow pastes the trimmed, Lanczos-scaled capture through an anti-aliased rounded mask.

Every caption of a store set and locale is set at one size. First the largest size each caption can take is measured; then every caption is set at the smallest of those. One exception keeps captions readable: if a caption has a clause break ("No ads, / no in-app purchases") that does not fit at that size, so it would be broken inside the clause, the set's size drops to the clause break's size when that costs at most 5% (`KEEP_CLAUSE`). Otherwise the caption is broken inside the clause and listed under "worth a look". A caption that fits on one line at that size is set on one line, the others on two balanced lines, so a set can mix one- and two-line captions but never type sizes. If a caption's measured ink then leaves the band (tall marks the font metrics did not promise, as with Arabic shadda over a descender on two lines), that caption's own size steps down by 3% and the set is set again at the new smallest size, so `fit` names the caption that really limits the set.

The largest size a caption can take is the larger of:

1. One line, from the full size down to 68% of it (60% for Thai and for landscape sets).
2. Two balanced lines, from the full size down to 62% of it (landscape: from 64% down to 48%, so a tablet caption is set on two lines only when one line would be smaller still). **If the caption contains a zero-width space (U+200B), the break goes there** and nowhere else, provided the caption fits that way. Otherwise the break is chosen in this order of preference:
   - **between clauses**: after a comma, full stop or their kin in any script ("23 maps, / or random ones");
   - **at a safe place**: a space or after CJK punctuation. A hyphenated compound stays whole ("in-app" is never split), a number stays with the word it counts ("67 map" never leaves "67" at the end of a line), and **a short word never ends the first line** (since 2026-11-24, round 2 review M3): a word of four letters or fewer ("se", "of", "ou", "и", "kaj", "atau", "wala") stays with the word after it, and a short last word stays with the word before it, so line 2 is never one short word. Letters are Unicode letters; marks and digits do not count, and a word that ends in punctuation ("reklám,") is a clause end, not a short word. If no break fits that way at any size, the rule is relaxed to three letters, then two, then one, and only then dropped (manifest `caption.fit` `relaxed` or `loose`, listed under "worth a look"); the strictest rule that fits at all is used, even when a looser one would set the caption larger. The rule and its exceptions are in [`fonts.json`](fonts.json) under `short_words`: Japanese, Chinese and Thai keep their own rules (no word spaces), Korean has none (its particles are attached, so a short Korean word is a whole phrase), Hindi, Marathi, Bengali, Tamil, Telugu, Persian and Urdu have none (their short words are mostly postpositions and case markers that belong at a line end with the noun before them, "कॉलोनी को", "کلونی را", and their scripts write few vowel letters, so content words count as short; a trial render with the rule moved their breaks the wrong way), and Vietnamese, where every syllable is a word, uses a list of its conjunctions and prepositions ("và", "hay", "hoặc", …) instead of a letter count. A rule break (below) that ends the first line with a short word does not compete with a safe break;
   - **by the script's own rule**: the browser's rules for most languages (a break after a hyphen or slash, Japanese phrase breaking with `word-break: auto-phrase`), dictionary words for Chinese. **Thai is never broken this way**, because the dictionary segmenter splits loanwords and compounds (it cuts "เรียลไทม์" and "อาณานิคม" in the wrong place).

   A less preferred break counts only when it sets the caption clearly larger: a safe break must beat a clause break by more than 15%, and a rule break must beat a safe break by more than 10%. At the set's size, the most preferred break that fits is used.
3. Only if neither fits: a rule break that leaves a number at the end of the first line, which step 2 otherwise refuses.
4. Otherwise the caption is refused.

Checks made on every caption before an image is written:

- every character is in one of the bundled fonts (read from the font files);
- Chromium drew every glyph with a bundled font and did not fall back to a system font (asked through the DevTools protocol);
- the laid-out lines reproduce the catalog text;
- two consecutive captures of the caption agree, so a frame Chromium had not finished drawing is never used;
- the measured ink stays inside the band with its margins. If tall marks push it out, that caption's size steps down by 3% and the set is set again at the smallest size; the locale is refused if that still fails at 40% of full size.

Only the ink's own rectangle is copied from the capture into the image; the rest of the band comes from one capture of the empty layout per image size. Chromium re-rasters only what changed, and after many captions a few anti-aliased pixels of the card's ring can drift by a few levels; taking the ink alone keeps every image byte-identical however many captions were rendered before it.

`render` and `fit` list the captions that needed a rule break, or were broken inside a clause, under "worth a look". Each manifest records how the caption was broken as `caption.fit` (`none` for one line, `hint`, `clause`, `safe`, `relaxed`, `loose`, `free` or `words`; for the three safe kinds, `caption.short_word_letters` gives the short-word length the break honoured, or `null` for none), its size as `caption.font_size` (the same for every image of the set and locale) and the size it could take on its own as `caption.own_size`.

A zero-width space is the way to place a break by hand in Thai, Japanese and Chinese, which have no word spaces. It has no width and draws nothing: a one-line caption with U+200B in it is byte-identical to the same caption without it, and a two-line caption broken at U+200B is byte-identical to the same caption with a space there (tested for `th`, `ja` and `zh-Hans` on both phone sets, 2026-11-24). When the caption fits on one line the hint is simply ignored.

## How long a caption can be

Measured on 2026-11-24 with the final catalogs, for the first round's regular-weight captions (bold type is about 12% wider, and the full sizes are larger, so these lengths now give about 78–80% of full size on phones): real phrases of each length, taken from every locale's own listing text, were fitted on the iPhone canvas, which is the tightest because its type is largest (the Android phone canvas takes about six more characters). Lengths are code points, as `storefront.py` counts them.

| Script | Reads well (at least 85% of full size for about 9 phrases in 10) | Ceiling (at least 70% of full size) |
| --- | --- | --- |
| Latin | 32 | 40 |
| Cyrillic, Greek | 28 | 36 |
| Chinese | 20 | 24 |
| Japanese | 18 | 20 |
| Korean | 22 | 32 |
| Devanagari (Hindi, Marathi) | 40 | 48 |
| Bengali | 36 | 46 |
| Telugu | 32 | 50 |
| Tamil | 24 | 32 |
| Arabic, Persian | 40 | 48 |
| Urdu (Nastaliq) | 28, on one line | 28 |
| Thai | 28 with a space or U+200B at a phrase boundary; about 20 without | 28 |

These are guides, not guarantees: one long unbreakable word (German, Dutch, Finnish compounds) can use a whole line. `fit` is the test: a single locale takes a few seconds, `--locale all` about three minutes. The limits the tool enforces are the per-script ones in `translations/platforms.json` (`field_limits`, `script_groups`), applied by `storefront.py`.

## Fonts and licences

`fetch_fonts.py` downloads the files below into `.cache/fonts/` with their licence texts, and refuses any file whose sha256 differs from [`fonts.json`](fonts.json). The cache is ignored by Git (`.gitignore` here) and must not be committed. Sources are pinned: `google/fonts` at commit `83c62e30d87daa70216dab6b984d00d20d96d585` (2026-11-24) and the DejaVu 2.37 release.

| Font | Used for | Source | Licence |
| --- | --- | --- | --- |
| DejaVu Sans 2.37 Bold (`DejaVuSans-Bold.ttf`, sha256 `e6476c1b…c27724`) | Latin, Greek, Cyrillic, Vietnamese and Romanian captions | [dejavu-fonts release 2.37](https://github.com/dejavu-fonts/dejavu-fonts/releases/tag/version_2_37), member `ttf/DejaVuSans-Bold.ttf` of `dejavu-fonts-ttf-2.37.zip` (archive sha256 `7576310b…908b0a`; the sans-only archive has no bold) | Bitstream Vera / DejaVu licence |
| Noto Sans Arabic | Arabic, Persian | [google/fonts `ofl/notosansarabic`](https://github.com/google/fonts/tree/83c62e30d87daa70216dab6b984d00d20d96d585/ofl/notosansarabic) | SIL OFL 1.1 |
| Noto Nastaliq Urdu | Urdu | [`ofl/notonastaliqurdu`](https://github.com/google/fonts/tree/83c62e30d87daa70216dab6b984d00d20d96d585/ofl/notonastaliqurdu) | SIL OFL 1.1 |
| Noto Sans Devanagari | Hindi, Marathi | [`ofl/notosansdevanagari`](https://github.com/google/fonts/tree/83c62e30d87daa70216dab6b984d00d20d96d585/ofl/notosansdevanagari) | SIL OFL 1.1 |
| Noto Sans Bengali | Bengali | [`ofl/notosansbengali`](https://github.com/google/fonts/tree/83c62e30d87daa70216dab6b984d00d20d96d585/ofl/notosansbengali) | SIL OFL 1.1 |
| Noto Sans Tamil | Tamil | [`ofl/notosanstamil`](https://github.com/google/fonts/tree/83c62e30d87daa70216dab6b984d00d20d96d585/ofl/notosanstamil) | SIL OFL 1.1 |
| Noto Sans Telugu | Telugu | [`ofl/notosanstelugu`](https://github.com/google/fonts/tree/83c62e30d87daa70216dab6b984d00d20d96d585/ofl/notosanstelugu) | SIL OFL 1.1 |
| Noto Sans Thai | Thai | [`ofl/notosansthai`](https://github.com/google/fonts/tree/83c62e30d87daa70216dab6b984d00d20d96d585/ofl/notosansthai) | SIL OFL 1.1 |
| Noto Sans SC | Simplified Chinese | [`ofl/notosanssc`](https://github.com/google/fonts/tree/83c62e30d87daa70216dab6b984d00d20d96d585/ofl/notosanssc) | SIL OFL 1.1 |
| Noto Sans TC | Traditional Chinese | [`ofl/notosanstc`](https://github.com/google/fonts/tree/83c62e30d87daa70216dab6b984d00d20d96d585/ofl/notosanstc) | SIL OFL 1.1 |
| Noto Sans JP | Japanese | [`ofl/notosansjp`](https://github.com/google/fonts/tree/83c62e30d87daa70216dab6b984d00d20d96d585/ofl/notosansjp) | SIL OFL 1.1 |
| Noto Sans KR | Korean | [`ofl/notosanskr`](https://github.com/google/fonts/tree/83c62e30d87daa70216dab6b984d00d20d96d585/ofl/notosanskr) | SIL OFL 1.1 |
| Noto Sans | Fallback behind each Noto script font (not needed by any caption so far) | [`ofl/notosans`](https://github.com/google/fonts/tree/83c62e30d87daa70216dab6b984d00d20d96d585/ofl/notosans) | SIL OFL 1.1 |

Both licences allow rendering text into images and distributing the images. The fonts themselves are not redistributed by this repository.

Matching across scripts:

- Captions are bold (since 2026-11-24, after the round 1 review: at weight 400 the strokes were about one pixel wide in search results). Glob2 Sans, the brand heading font, is a Latin subset of DejaVu Sans Book and has no bold, so Latin, Greek, Cyrillic, Vietnamese and Romanian captions are set in DejaVu Sans Bold: the same family, design and licence. Letter-spacing is −0.02 em.
- Weights were set by measurement: the mean stroke width (twice the median distance from the skeleton to the edge, over the en and each locale's own hero, build, battle and economy captions, rendered at 300 px) is 0.147 em for DejaVu Sans Bold. Each Noto family was measured from weight 700 to 900 and set where it comes closest, then checked by eye beside the English caption on the iPhone band: Arabic 850 (0.140 em, and it is set 4% larger), Thai 850 (0.147), Tamil 850 (0.145, set at 94%), Telugu 900 (0.138, the heaviest it goes), Chinese, Japanese and Korean 850 (0.119–0.133; heavier clogs dense characters at thumbnail size), Devanagari and Bengali 800 (0.135; their headline bar adds weight, and at 850 they looked heavier than the Latin). Noto Nastaliq Urdu stops at 700 (0.109) and is used at 700, its boldest.
- Sizes: CJK and Korean are set at 90–92% because their glyphs fill the em box; Arabic at 104%; Tamil at 94%; Nastaliq at 96% with a 1.75 line height. Scripts with marks above the headline are nudged down so they sit optically centred.
- Chinese, Japanese and Korean each use their own regional font, and the caption carries the locale as its `lang`, so `zh-Hans`, `zh-Hant` and `ja` get their own forms of shared characters (checked with 直, 骨, 令 and 返).
- Urdu is set in Nastaliq, the style Urdu readers expect and the one iOS and Android use for their own Urdu interface. Nastaliq is tall, so Urdu captions come out smaller in the shallow landscape band: the hero line's ink is about 2.9 em tall, which limits it to about 56 px on the 7-inch tablet (51% of the larger round 2 full size; about the pixel size of round 1) and are best kept on one line. To use the Naskh-style Noto Sans Arabic instead, point `ur` at the `arabic` profile in `fonts.json`.
- Direction is set per locale in `fonts.json` (`"dir": "rtl"` for Arabic, Persian and Urdu), never guessed from the text, so a caption that starts with a Western digit or a Latin term still lays out right to left.
- Digits are whatever the catalog uses (Western, Arabic-Indic, Persian, Bengali, Devanagari); each script font carries its own and the Western set.
- No-break spaces (U+00A0 and the narrow U+202F, as French uses before `:` `;` `!` `?`) are kept, are never a line-break point, and must have a glyph (DejaVu Sans Bold has both).
- Chromium reports DejaVu Sans Bold under its own family name, "DejaVu Sans"; the font check accepts a bundled font under the names its file gives itself, and still refuses any system font.

## What verify checks

For every expected image:

- it exists, and no image in the folder is missing from the gallery;
- its bytes are the ones the manifest recorded at render time (so the render-time checks above apply to this file);
- exact store pixel size; 24-bit RGB; no alpha channel, palette or transparency chunk; PNG (or JPEG where a set asks for it);
- file size under the store ceiling (8 MB for every store here; set `"format": "jpeg"` on a store set if a PNG ever exceeds it);
- the caption band is no more than 20% of the image, and the caption ink is inside the band. The band is everything above the card's top edge, so it already includes the ring and the shadow above the card (17% on phones and iPad, 16% on Android tablets); the check is unchanged;
- every caption of the store set and locale has the same type size;
- the caption text equals the catalog's current `shot_overlay_<role>` and is within the length limit in `translations/platforms.json` (`field_limits`, applied by `storefront.py`);
- no banned words for the destination store;
- the slot still maps to the same capture and role, the capture file is unchanged, and the gameplay pixels in the output equal the trimmed, scaled capture exactly (inside the card's rounded corners);
- it was rendered by the current `screenshots.py`, `caption.html`, `gallery.json` and `fonts.json`.

Banned-word lists are in `gallery.json` under `banned` and mirror `translations/tests/test_storefront.py`: currency signs and "#1" in every language; English price words (free, price, sale, discount, paid, buy) and banned claims (first, best, top-rated, download now, …); MCP, AI agent and JavaScript on every mobile set; Google Play's avoid list (best, top, new, free, …) for Play; names of other platforms and stores for Apple and Amazon. The English word lists apply to English only, because the same letters are ordinary words in other languages ("sale", "best"); translated price or ranking words are the translation review's job.

## Reproducibility

The same inputs give byte-identical PNGs on the same machine, whatever the order or number of locales and store sets in the run: no timestamps are written, Pillow's encoder is deterministic, and Chromium is pinned through Playwright 1.63.0 (Chromium 153) with `--force-color-profile=srgb` and whole-tile rastering; the tool checks at start-up that a flat brand colour comes back as exactly that colour. A different Chromium build or operating system may anti-alias text differently, so render a complete set on one machine. Each manifest records the hashes of the tool files, the gallery source, the catalog, the capture, the fonts used and each output.

## Files

| File | Purpose |
| --- | --- |
| [`screenshots.py`](screenshots.py) | The tool: `render`, `fit`, `verify`, `contact-sheet`, `check-config` |
| [`caption.html`](caption.html) | The page Chromium renders: background, card ring and shadow, caption measuring and setting |
| [`gallery.json`](gallery.json) | Store sets, per-size trim and band, per-capture trim decisions (`slot_trim`), provisional gallery, store limits and banned words |
| [`fonts.json`](fonts.json) | Font sources and hashes, and the font, weight and size for each locale |
| [`fetch_fonts.py`](fetch_fonts.py) | Downloads and verifies the fonts (standard library only) |

The catalog parser is `translations/tools/storefront.py` (`read_fields`), imported unchanged.
