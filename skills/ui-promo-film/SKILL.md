---
name: ui-promo-film
description: Direct a product demo, promo, launch or SaaS/app film at the ElevenLabs-Architect standard - a narrated story where the real product UI is recreated crisp and shown in motion (macro zooms into the input, typing, cursor clicks, cards lifting into 3D), brand textures and type carry the identity, kinetic text fills word by word with the voice, dark/light beats give rhythm, people add warmth, and every visual event gets a sound within 100 ms. Use for any "product demo video", "promo", "feature launch", "app/SaaS/AI tool video", "explain my product" or "make it like the ElevenLabs video" request; it directs, while edit-kit:saas / product-launch-video / edit-kit:fx / hyperframes build.
---

# UI promo film

Built from a teardown of ElevenLabs' "Eleven Agents Architect" launch film (67 s, 16:9; `productions/_research/elevenlabs-promo/`, numbers in `reel-production/references/teardowns.md`). It is the reference for every product demo and promo. Make ours at least this good.

## What it does, measured

- **Voice-led story, one calm narrator:** about 2.2 words/s with natural pauses, one continuous read. A second voice performs the product inside the demo (the user dictating "I need an agent that…"), which turns a feature into a scene.
- **Sound on the picture:** 42 visual events, 88% get a sound within ±100 ms; about 0.9 salient hits/s over a dense micro-bed of 5-8 onsets/s (UI pops, keys, swishes, ticks); sub-bass drops on section changes; a sonic logo (a single bell/glockenspiel ding) at frame 1; music changes texture with the story (intro, feature section, quiet piano under the end lockup); wide stereo; voice always on top.
- **Look:** high-key editorial (mean luminance 0.76, low contrast 4.8, near-neutral colour 0.09): off-white canvas, black type, brand mesh-gradient textures with grain as the only colour, generous whitespace. "Premium" here is consistency, not darkness.

## Structure (scale to 30-70 s; 9:16 is a re-layout)

| Beat | Share | What happens | Device |
|---|---|---|---|
| Hook | 0-6% | The promise in 5-7 words, type assembling on the canvas, brand textures blooming around it with tiny spec-sheet labels; sonic logo | kinetic type + texture swatches |
| Name | 6-11% | Product lockup builds from the brand mark (mark splits, letters arrive), brand shape-language pattern in the background | logo build |
| Feature 1: ask | 11-27% | Macro zoom into the real input; text types itself live; the cursor clicks send; the camera pushes through into the working state (panels, tools, reasoning, a proposed fix); the cursor approves | UI macro, typing, cursor, 3D tilted panels |
| Proof of scale | 27-35% | A real person (photo/footage) using it, then the frame explodes into a field of floating cards; cut to dark | people + card field |
| Feature 2: proactive | 35-50% | Dark beat: "scanning…" particles converge; diff of settings with highlighted changes; a proposals table | dark/light alternation |
| Pressure test | 45-48% | Fast mosaic of gradient tiles and code panels | montage on the beat |
| Feature 3: build | 50-72% | An orb/avatar morphs from a gradient; the input pill; second voice dictates; file icons fly in; config screens fill | morph, dictation, flying assets |
| Values line | 72-76% | One sentence on dark, words fill grey→white with the voice | word-fill kinetic type |
| Customers | 76-80% | Real people grid, one word per photo ("For / Real / Customers") | photo grid typography |
| Integrations | 80-86% | "Connect [product] to — X" with X swapping on the beat over a background that changes to each partner's colour | word swap |
| Close | 86-95% | Orb + "Improve / your agents", then the tagline filling word by word over a particle field | |
| Lockup | 95-100% | The opening lockup returns (loop) over a quiet piano tail | loop |

## The craft rules

1. **Recreate the real UI crisply** (vector/HTML rebuild, never blurry screenshots): real copy, real states, real data. Placeholder bars read as fake instantly.
2. **The camera lives inside the UI:** macro zoom to the element being used, push through it into the next state; 3D tilt for depth; never a static full-screen screenshot.
3. **The cursor is an actor:** big, enters from off-screen, clicks ignite the next beat (`edit-kit:oversized-cursor`).
4. **Type is choreography:** word-by-word reveal or grey→black/white fill locked to the voice (Whisper timestamps snapped to onsets); light weight, large tracking for statements; one accent at most.
5. **Brand textures as transitions:** mesh gradients and the brand's shape language (rounded rects, grids) carry the cut from one scene to the next (zoom into a card, morph a blob into an orb).
6. **Rhythm by contrast:** alternate light and dark beats about every 10-15 s; insert one fast montage; let one line sit on near-empty space.
7. **People for warmth:** at least one human moment (photo or footage) after the first feature.
8. **One continuous motion logic:** `edit-kit:motion-doctrine` (exit vector sets entry vector), seams from `edit-kit:cut-the-curve`.
9. **Sound map before the build:** list every visual event with its sound; 90% of events within 100 ms (`earshot critique --video` measures it); salient hits about 1/s; micro-sounds quiet; sub drop on section changes; sonic logo at the start and the end.
10. **Loop:** the last frame returns to the opening lockup.

## Build route

`brief-amplifier` → this skill's structure in `brief.md` → voice first (`voiceover-direction`, Kokoro or VoiceStudio; second voice for the in-product demo) → build with `edit-kit:saas` (or `edit-kit:product-launch-video` from a URL) on `hyperframes` + `edit-kit:fx` + `gsap-*` → sound with `real-sfx` and the sound map → `earshot critique --video` (target: sync ≥ 85%, salient 0.8-1.3/s) → `lookmeter.py` against the brand's own reference → `gate.py`.
