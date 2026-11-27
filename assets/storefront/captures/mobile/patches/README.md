# Capture harness patches

Uncommitted game-repo changes used to take the storefront-v2 mobile captures, saved here when the capture worktrees were removed on 2026-11-27.

| Patch | Base commit (Globulation2/glob2) | Used for |
|---|---|---|
| `mobile-store-capture.patch` | 5e96273ff6 (Prepare release 0.11.8.0, #1913) | iPhone 6.9", iPad 13" and Android phone/tablet captures: capture clock, MCP capture tools, HUD/event-feed and render tweaks, mobile build settings |
| `android-store-capture.patch` | a9f878b9ff (#1922) | Android emulator captures: mobile build settings and MCP availability |

These are capture-only changes, not meant for release builds. To reuse one: `git worktree add <dir> <base commit>`, then `git -C <dir> apply <patch>`.
