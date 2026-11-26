# Storefront v2 application icon

Store-upload copies of the Globulation 2 application icon, redrawn sharp for
storefront v2. The icon is the same blue glob the game has always used: same
silhouette, pose, proportions, colours, gloss and outline. It is not a redesign.

| File | Use |
| --- | --- |
| `icon-1024.png` | Apple App Store icon. 1024x1024, opaque, full-bleed purple `#4C3676`, square corners. Identical to the iOS app's compiled `icon-1024.png`. |
| `icon-512.png` | Google Play store icon. 512x512, 32-bit PNG, full-bleed purple `#2B1C42`, square corners. Matches the Android launcher icon, whose background is that colour. |
| `gamepix-icon-256.png` | GamePix icon. 256x256 PNG, the Google Play icon (purple `#2B1C42`) downscaled with Lanczos. GamePix takes 256x256, JPG or PNG, at most 1 MB. |
| `glob-1024.png` | The glob alone on a transparent background, 1024x1024, for compositions. |
| `glob2-icon.svg` | The vector master (viewBox 0 0 128 128, transparent). Render it for any other size. |
| `manifest.json` | SHA-256, size and source path of each file. |

The two store icons use different purples on purpose: each matches the icon
the installed app shows on that platform. The glob fills 82% of both, as it
does in the apps' launcher icons. Neither has rounded corners baked in; the
stores apply their own masks.

## Provenance

Observed 2026-11-24.

- **Source art.** The game's application icon existed only as PNG files of at
  most 128 pixels (`content/data/icons/` in the
  [game repository](https://github.com/Globulation2/glob2)). No vector or
  larger original was found in that repository, its history or its recovered
  artwork. Larger icons, including the 1024-pixel iOS icon, were enlargements
  of the 128-pixel file and were visibly blurry.
- **How it was made.** The icon was redrawn as vector shapes traced over the
  128-pixel file: the silhouette from its alpha edge, the fill, shading and
  gloss gradients from fits to its pixel values, and the shadow crescents and
  specular streaks from profiles across each edge. No image generator and no
  stock imagery was used. This satisfies the storefront v2 rule of real game
  art only.
- **Fidelity.** The silhouette is crisp and the shading inside it is blurred
  to about the softness the old file's pixels gave it, so the icon reads as
  the old one, no longer blurry. The rim is the one deliberate departure: the
  old file ends in a neutral grey fringe about 1.1 units wide (of 128), which
  enlarges into a border like a sticker's; the vector has a dark navy rim
  (`#141d4a`) half that wide, checked on the iOS purple, the Android purple,
  white and black. Rendered at 128 pixels over the iOS purple, the vector
  differs from the old file by a mean of 5 of 255 levels across the icon's
  pixels and 2 of 255 away from its edges. Because of the thinner rim the
  silhouette is about half a unit smaller all round; the silhouettes overlap
  by 96%.
- **Where it lives.** The vector and its 1024-pixel render are in the game
  repository under `content-src/icons/app/`, added by
  [pull request 1915](https://github.com/Globulation2/glob2/pull/1915), which
  also regenerates the app, launcher and desktop icons from them. That pull
  request was open, not merged, when these files were exported, and had two
  commits: the redraw and a refinement after review. `manifest.json` records
  the commit these files were exported from, the second.

## Regenerating

In a checkout of the game repository at or after that commit:

```sh
uv run --with pillow==11.3.0 --with resvg-py==0.5.0 python platforms/mobile/icons.py --render-master
```

`icon-1024.png` is then
`platforms/mobile/ios/Assets.xcassets/AppIcon.appiconset/icon-1024.png` and
`glob-1024.png` is `content-src/icons/app/glob2-icon-1024.png`. `icon-512.png`
is that render reduced to 420 pixels with premultiplied alpha and centred on a
512-pixel `#2B1C42` square.
