---
name: reel-production
description: The director's playbook for any premium Reel, ad or short - research, idea, script and voice, look, storyboard, build (3D, motion graphics, maps, collage), sound, edit, QA and delivery - with one default tool per stage, explicit rules for when to switch, hard quality gates and a tool ledger so nothing installed is ignored. Use whenever the user wants a video, Reel, ad, product film, episode or "make it like this reference", without naming a single tool. Start here before any other video skill.
---

# Reel production: the director's playbook

Hundreds of skills are installed. Overlap is the enemy: two half-used tools make a worse film than one tool used fully. This playbook picks **one default per stage**, names the **switch conditions**, and enforces **gates**. Every production keeps a ledger (`TOOLS.md`) so the choice of each tool, and each skipped alternative, is written down.

The full stage-by-stage map of skills is in `references/skill-map.md`. Read it at the start of every production and again before each stage.

## Autonomy

The user wants one prompt in, a finished film out. Work end to end without stopping for approval, except for decisions that are genuinely theirs: spending money (paid APIs, paid models), publishing, licences that need attribution they must accept, consent (cloning a real voice), or a brief so vague two different films would both fit. Show artefacts as you go (script, board, frames) without waiting.

## Production folder `productions/<slug>/`

`brief.md` · `research/` · `script.md` · `vo/` · `bible/` (look, colour script) · `storyboard/` · `blender/` or `build/` or `edit/` · `sound/` · `renders/` · `qa.md` · `sources.md` (every asset and licence) · `TOOLS.md` (ledger) · `NOTES.md` (what changed per version and why).

## Stages

| # | Stage | Default | Switch when | Gate (must pass to continue) |
|---|---|---|---|---|
| 0 | **Research** | `anthropic-skills:deep-research` or WebSearch; `yt-dlp` + frame sheets for reference reels | the product is the user's own: ask for photos/specs, research category and competitors instead | facts verified with sources in `research/facts.md`; reference reels broken down (shot list, timings, type, sound map, VO prosody) |
| 1 | **Brief + idea** | `creative-director` | a series: `manjuforge` + bible | one idea in one line; format, length, audience, CTA written in `brief.md` |
| 2 | **Script + voice** | `reel-writer` agent, then `voiceover-direction` | dialogue or characters: `screenwriting:*`; designed/cloned voice or dubbing: `voicestudio`; user records their own voice: DeepFilterNet or `voicestudio audio clean` | hook in 1-2 s; VO is one continuous read; pace 2.6-3.3 words/s; prosody measured against a reference; Whisper reads every word right |
| 3 | **Look** | `reel-art-director` agent | brand exists: `brand-intake`, `small-business:brand-style` | palette ≤ 4 colours, 2 type families, colour script per beat, engine chosen |
| 4 | **Storyboard** | `reel-storyboard-artist` agent | very short (<10 s) or a single continuous move: a shot table in `brief.md` is enough | every shot has framing, camera move, duration, the word it lands on, and its sound |
| 5 | **Build** | the format recipe (table below) | — | stills at 3-5 key times looked at before any long render; previews at 25% before full renders |
| 6 | **Sound** | `real-sfx` (your SOUNDE library, frame-exact) | full soundtrack with licence audit: `real-sound`; missing sound: `openverse-sounds`; nothing recorded exists: `earshot make` | `earshot` checks: candidates ranked (`earshot rank`), mix critiqued (`earshot critique` / `timeline`); -14 LUFS, true peak ≤ -1.5 dBTP |
| 7 | **Edit + QA** | the branch core (below) on `hyperframes`; `edit-kit:motion-doctrine` seams; `edit-kit:qa` + `reel-editor-qa` agent | handing off to an editor: `hyperframes-to-after-effects` | `npx hyperframes check` clean; frames pulled at every cut and pop and looked at; captions in safe zones; QA blockers fixed and re-rendered |
| 8 | **Deliver** | `reel-export`, `loop-cover`, `instagram-skills:ig-caption-writer` | other platforms: `youtube-export`, `tiktok-skills:*` | 1080x1920 H.264, credits in caption for CC BY assets, `sources.md` complete |

## Branches: one core tool each, then its sub-tools

`reel-production` is the spine and always the entry point. Pick ONE branch by what the user has and wants; the branch's core tool owns stages 4-7 for that film and its sub-tools are called only through it. Combining branches is normal (a heritage film that opens on a map), but each part keeps its own core.

| Branch | Pick it when | Core | Sub-tools (in the order they are used) |
|---|---|---|---|
| **A. Footage edit** | the user gives raw footage: talking head, podcast, interview, phone clips, real estate, construction | `edit-kit:director` (via `edit-kit:edit`) | `edit-kit:reels` (9:16) or `edit-kit:youtube` (16:9), `edit-kit:theme`, `edit-kit:fx`, `depth-captions` or `edit-kit:embedded-captions`, `edit-kit:talking-head-recut`, `edit-kit:camera-arc` (2.5D orbit on a flat clip) |
| **B. Code-built promo** | no footage: app, SaaS, agency, brand, motion-graphics ad | `edit-kit:saas` or `edit-kit:product-launch-video` (from a URL) | `motion-graphics-starter` prompts, `edit-kit:fx`, `hyperframes` + `gsap-*`, `edit-kit:oversized-cursor`, `kinetic-typography` |
| **C. 3D product** | a physical product as the hero: turntable, macro, exploded view, checklist | `product-check-reel` (Blender headless, bright studio) | `edit-kit:blender-product-film` (dark studio, glass, liquid, condensation), `3d-animator` (three.js, no Blender), `blender-agent-skills:*`, `threejs-*` |
| **D. Story, place, history** | a narrated story of a place, brand heritage, a topic explainer | `satellite-map-story` + `archival-collage-story` | `edit-kit:vox-director` (Vox paper-collage topic explainer), `edit-kit:faceless-explainer` (text to explainer), `colorize`, `object-separation` |
| **E. Special look / copy a reference** | "make it like this video", or a named look | `edit-kit:video-clone` | `edit-kit:anime-cel`, `edit-kit:pixel-art`, `edit-kit:whiteboard`, `edit-kit:paper-cutout`, `edit-kit:crayon-storybook`, `edit-kit:painted-animation`, `anime-animation-production`, `animation-styles` |
| **F. Music-driven** | the track drives everything: lyric video, beat montage, slideshow | `edit-kit:music-to-video` | `beat-sync-editing`, `music-video-production` |
| **G. Explainer / data** | teaching, numbers, charts, math | `explainer-studio` / `manim-skill` | `animated-chart`, `animated-infographic`, `papercut-*`, `edit-kit:pr-to-video` (code changes) |

**Cross-cutting gateways, every branch:**
- **Motion:** `edit-kit:motion-doctrine` before composing any multi-scene film (one continuous camera move: exit vector sets entry vector, stamped seams, `seam-gate`), with `edit-kit:cut-the-curve` (seam catalogue) and `edit-kit:seam-craft` (no white flashes). `animation-principles` for weight in every tween.
- **Voice:** `voiceover-direction` (Kokoro default, measured). When the user wants a designed or cloned voice, or dubbing: `voicestudio` (local app: voice design from a description, cloning of consented voices, dubbing in 646 languages, clean-up). A/B the candidates with `earshot ab` and the prosody meter.
- **Sound:** `real-sfx` places real recordings from the indexed libraries; `earshot critique --video` judges the mix (target: launch-grade). Default mix numbers (Edit Kit house): voice -14 LUFS and loudest, each SFX peak -17 dBFS at most one per 0.25 s, music about 24 dB under the voice and ducked; no voice: music -20 LUFS.
- **QA:** `npx hyperframes check` + frames at every cut and pop + `edit-kit:qa` + `reel-editor-qa` + `earshot critique`.

**Duplicates: which copy to use.** Edit Kit ships its own `threejs-animation`, `particle-system`, `shader-glsl`, `video-shotcraft`, `painted-animation`, `ffmpeg`, `slideshow`, `figma`, `remotion-to-hyperframes`, `frontend-design`. Inside a branch-A/B/E build use the `edit-kit:` copy (its links point to `edit-kit:fx`); everywhere else use the standalone skill. Never load both copies for one job.

## The ledger (`TOOLS.md`)

One row per stage: stage · tool used · why · alternatives considered and why skipped · gate result with numbers. Write it as you go, not at the end. Before delivery, read `references/skill-map.md` once more and add any skill that would have improved the film to `NOTES.md` as a next-version idea.

## Quality bar (from the user's reference reels)

- The camera moves every frame; energy comes from motion and overlay changes on every phrase, not only from cutting. Cut rhythm: 1-1.5 s average for montage, 3-5 s for a continuous product move.
- Every overlay change lands on a spoken word (Whisper timestamps, snapped to onsets). Every move gets a sound, quiet and under the voice.
- Type: one bold display face, one clean face, one italic serif for captions; one accent colour; corner brackets or another framing device held through the film.
- Proof beats claims: show the stitch, the scratch test, the dimension, the glow; a chip or callout confirms it.
- The ending pays off or loops; the brand lands on the final beat with a sub drop.

## Known failure modes (check before calling a stage done)

Blender macro shots empty (camera clip start), soft focus at macro (f-stop too open), boolean materials grey, EEVEE glass blob, EOX tile seams, washed archive grades, failed cut-outs on close crops, captions running ahead of the voice, VO generated line by line (flat), long renders lost on session restart (run detached and resumable). Fixes live in the recipe skills.
