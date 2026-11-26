# Yandex Games listing notes

Short record only. Yandex Games is **parked**: the console is not accepting new developer applications ([web portal rollout](../planning/web-portal-rollout.md#yandex-games)). No top-game sample was taken. Rules were read on 2026-11-26 from Yandex's [game requirements](https://yandex.com/dev/games/doc/en/concepts/requirements); the numbers in brackets are Yandex's requirement IDs.

## Listing-relevant rules (observed)

- **Required fields** (5.2): icon, cover, screenshots, title, description, How to play and categories.
  - Screenshots may not be used as the icon or cover (5.6).
  - Screenshots must show real gameplay filling at least 70% of the image (5.1.1.2).
  - No borders, rounded corners, ratings or game UI on icons and covers (8.3.3, 8.3.4).
- **Video:** at least 70% real gameplay (5.1.1.3). YouTube integration is prohibited; host the video ourselves or include it in the archive (3.9).
- **Text:**
  - The title must be identical in the game and the draft for every selected language (5.1.3), and unique across languages (5.12).
  - No duplicate text across fields and no filler (5.11).
  - Controls must be described in the game or in How to play (2.2).
- **Localisation:** the game must detect the language automatically through the SDK (2.14).
- **Content:** the declared age rating must match the content (2.7). Realistic violence is prohibited (3.4); Glob2's combat is cartoon-like, so this should pass, but the reviewer decides.
- **Size:** at most 100 MB uncompressed (1.21). Only the lite build fits (45.8 MB unpacked); the packager refused standard.
- **Monetisation must be enabled (1.12):** the game must have ads or in-app purchases. Ads only through the Yandex SDK (4.1) and only at logical pauses (4.4).
- **Links:** no external links at all (8.4.2), including our website. Social community links are allowed under conditions (8.4.3).

## Inference

Rule 1.12 means a Yandex build cannot be fully ad-free and purchase-free: the fair deal and Yandex conflict at the rules level, not only in the copy. The lite build's English-only text is also weak for Yandex's mainly Russian-speaking audience. This is an inference from the platform's origin, not measured.

## Action list for our listing

1. **Keep it parked** until applications reopen **and** the user has decided whether the game will show SDK ads on portals (1.12).
2. If it goes ahead: use the lite build. Prepare screenshots and a self-hosted video from lite footage (≥70% gameplay, no YouTube), write separate Description and How to play texts, and add Russian translations from the reviewed storefront catalogue. The lite game itself is English-only, so check with Yandex whether listing-only localisation is acceptable under 8.2.3.

**Decision for the user:** whether Yandex is worth an ad-enabled build at all.
