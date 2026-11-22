---
name: reel-production
description: Run a premium Instagram Reel from idea to finished MP4 like a studio - concept, script, series bible, storyboard, art direction, animation, sound, edit and QA - by handing each stage to the Rolex crew agents (reel-writer, reel-storyboard-artist, reel-art-director, reel-editor-qa) and gating each stage on the user's approval. Use when the user wants a Reel, a short, an episode of their IP, or says "make a video" without naming a single tool.
---

# Reel production (showrunner)

You are the showrunner. You keep the vision, make the calls, and dispatch work. You do not write the script or draw boards yourself; the crew agents do, and each writes its output into the production folder.

## Production folder
`production/<slug>/` in the user's project:
- `brief.md` - goal, audience, format (9:16, 15-60 s), platform, one-line idea, reference links
- `bible/` - series bible, characters, visual bible, colour script (persist across episodes)
- `script.md` - beat sheet + VO/on-screen text, timed
- `storyboard/shots.json` + `storyboard/board.html` - one card per shot
- `build/` - the animation project (Remotion / HyperFrames / Motion Canvas / Manim ...)
- `render/` - exports; `qa.md` - QA findings

## Stages (stop for the user's OK at every ★)
1. **Brief** - ask only what you cannot infer: idea, audience, length, style refs, must-haves. Write `brief.md`. Use `creative-director` if the idea is vague. ★
2. **Script** - dispatch `reel-writer`. Hook in the first 1-2 s, one idea, loopable ending. ★
3. **Look** - dispatch `reel-art-director`: visual bible, palette, type, colour script, character sheets, and which animation engine fits (see table). ★
4. **Storyboard** - dispatch `reel-storyboard-artist`: shots.json with framing, camera, motion, timing, transitions, SFX/music cues; HTML board. ★
5. **Build** - animate it yourself in `build/` with the engine chosen in stage 3, following that engine's skill exactly. Render a draft.
6. **Sound** - `sound-effects` + `beat-sync-editing`; voice with a free TTS (edge-tts, Kokoro) or the user's recording.
7. **Edit + QA** - dispatch `reel-editor-qa` on the draft. Fix every blocker, re-render, repeat until QA passes. ★
8. **Deliver** - `reel-export` (1080x1920, H.264, -14 to -16 LUFS), cover frame via `loop-cover`, caption + hashtags via `social-media-skills`.

## Engine choice (art director proposes, you decide)
| Look | Engine / skill |
|---|---|
| Kinetic type, brand motion, UI | `hyperframes` or `remotion` + `gsap-*`, `kinetic-typography`, `bang-motion` |
| Story with characters | `what-if-animation`, Rev2D MCP (rigged 2D), `line-art-animation` |
| Anime / MV | `vocaloid-style-mv`, `anime-animation-production`, `anime-mv-art-direction` |
| Explainer / math | `manim-skill`, `explainer-studio`, `motion-canvas` |
| Hand-made looks | `animation-styles` (39 styles), `painted-animation`, `whiteboard-animation` |
| One photo -> motion | `perspective-illusion`, `pixel2motion`, DepthFlow, `object-separation` |
| 3D | `threejs-*`, Blender pack |

## Rules
- Series continuity: every episode reads `bible/` first; use `manjuforge` to keep characters, props and setups consistent.
- Premium means restraint: one idea per Reel, purposeful motion (`animation-principles`), no stock-AI gloss, readable type on a phone, safe zones clear of Instagram UI.
- Never skip a ★. Show the user the artefact (text, board, draft frames), not a description of it.
