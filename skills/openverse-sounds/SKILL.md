---
name: openverse-sounds
description: Find and download openly licensed real sound effects and ambiences from Openverse (WordPress's open media search over Freesound, Jamendo, Wikimedia and more), keeping only licences that allow commercial use and writing a credit line for every file. Use when a video needs a specific real sound that the local libraries lack (a door, rain on a window, a crowd, a mechanical click, a temple bell), or the user asks for free, CC0 or royalty-free sound effects.
---

# Openverse sounds

Search first in the local libraries (`library/cinematic-sound-effects`, the `sound-effects` CC0 pack, `real-sfx`'s index). Go to Openverse only for what they lack.

```bash
python3 ~/.claude/skills/openverse-sounds/scripts/ov.py search "temple bell" --n 10 --max-s 6     # add --cc0 for no-attribution only
python3 ~/.claude/skills/openverse-sounds/scripts/ov.py get <id> --out library/openverse
```

- Only CC0, Public Domain Mark, CC BY and CC BY-SA are accepted (all allow commercial use). NC and ND are refused by the script.
- Every download appends a line to `library/openverse/CREDITS.md`. CC BY / BY-SA need that credit in the post caption or end card: copy it into the production's `sources.md`.
- Prefer CC0 for brand work. Results are previews (often 128-320 kbps mp3), fine for SFX, not for a music bed.
- You cannot hear: check candidates with `earshot` (`earshot realness`, `earshot rank`, `earshot compare`) before using them, and measure the trim you place.
- Anonymous API use is rate-limited; keep searches specific instead of paging through results.

Source: Openverse by WordPress (https://openverse.org), API https://api.openverse.org.
