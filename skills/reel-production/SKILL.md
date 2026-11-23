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
| 0 | **Research** | `anthropic-skills:deep-research` or WebSearch; every reference video through `scripts/teardown.sh` (frames, cuts, transcript, earshot critique and timeline, look numbers), then a row in `references/teardowns.md` | the product is the user's own: ask for photos/specs, research category and competitors instead | facts verified with sources in `research/facts.md`; reference reels broken down (shot list, timings, type, sound map, VO prosody) |
| 1 | **Brief + idea** | **`brief-amplifier`** first (turns a short request into the full super-brief: brand-derived idea + through-line device, look in numbers, beat sheet on a music grid, voice lines timed, music, sound, brand rules), with `creative-director` for the 3 routes | a series: `manjuforge` + bible | one idea in one line; format, length, audience, CTA written in `brief.md` |
| 2 | **Script + voice** | `reel-writer` agent, then `voiceover-direction` | dialogue or characters: `screenwriting:*`; designed/cloned voice or dubbing: `voicestudio`; user records their own voice: DeepFilterNet or `voicestudio audio clean` | hook in 1-2 s; VO is one continuous read; pace 2.6-3.3 words/s; prosody measured against a reference; Whisper reads every word right |
| 3 | **Look** | `reel-art-director` agent | brand exists: `brand-intake`, `small-business:brand-style` | palette ≤ 4 colours, 2 type families, colour script per beat, engine chosen |
| 4 | **Storyboard** | `reel-storyboard-artist` agent (required for any brand film) | none for brand work; a <10 s internal test may use a shot table | every shot has framing, camera move, duration, the word it lands on, and its sound |
| 5 | **Build** | the format recipe (table below) | — | stills at 3-5 key times looked at before any long render; previews at 25% before full renders |
| 6 | **Sound** | `real-sfx` (your SOUNDE library, frame-exact) | full soundtrack with licence audit: `real-sound`; missing sound: `openverse-sounds`; nothing recorded exists: `earshot make` | `earshot` checks: candidates ranked (`earshot rank`), mix critiqued (`earshot critique` / `timeline`); -14 LUFS, true peak ≤ -1.5 dBTP |
| 7 | **Edit + QA** | the branch core (below) on `hyperframes`; `edit-kit:motion-doctrine` seams; `edit-kit:qa` + `reel-editor-qa` agent | handing off to an editor: `hyperframes-to-after-effects` | `npx hyperframes check` clean; frames pulled at every cut and pop and looked at; captions in safe zones; QA blockers fixed and re-rendered |
| 8 | **Deliver** | `reel-export`, `loop-cover`, `instagram-skills:ig-caption-writer` | other platforms: `youtube-export`, `tiktok-skills:*` | 1080x1920 H.264, credits in caption for CC BY assets, `sources.md` complete |

## Non-negotiable gates (added after an adversarial review; `scripts/gate.py` enforces the measurable ones)

1. **Three concept routes + a mood board.** `creative-director` writes 3 different routes; build a mood board of 6-10 frames from the product's own category (watch films for watches, not apparel reels). Pick one route on purpose and write why.
2. **Look by category.** Premium watches, jewellery, perfume, tech: dark stage, low-key grazing light, light sweeps (`edit-kit:blender-product-film`, `apple-launch-film` grammar). Apparel, food, everyday goods: bright studio (`product-check-reel`). Never default.
3. **Hero-asset lookdev gate.** Before animating anything: 100% stills of the product beside 2 real category references. It must read as a real product (bevels, real materials, micro-detail, correct scale). Cycles for glass and polished metal; HDRI from Poly Haven via Blender MCP `search_assets`. Fails if any part reads as a primitive.
4. **Proof per claim.** Every feature gets a demonstration (stress test, comparison ✗/✓, in-use context with its own colour), never a chip alone.
5. **Claims gate.** Every on-screen and VO claim has a qualifier and a source in `research/facts.md`; run `legal:compliance-check` (ASCI for India). No absolutes ("never scratches").
6. **Hook pack + retention map.** 3 openings (`social-media-skills:hook-writer`, `instagram-skills:ig-hook-extractor`), situational and India-specific; something moves in frame 0; a re-hook every 3-5 s.
7. **Ending standard.** Product in use (a wrist, a hand, a person) + one CTA (comment keyword or follow) + last frame loops to frame 0 + a cover frame (`loop-cover`).
8. **Music stage.** Choose music by brief and reference (tempo, era, instrumentation) with `earshot rank`; no generic stock by default.
9. **Grade pass.** One grade per beat (`compositing`, `lookdev`), checked on the frame sheet.
10. **Localisation.** Indian settings, occasions, casting (hands, skin tone), ₹ price card when relevant; VO checked by Whisper for meaning.
11. **Sound budget.** About 1 salient hit per second on average (measured in the user's references), never two within 0.25 s, no same sample within 3 s, no trailer impacts on calm premium products, one signature motif. Music about 20-24 dB under the voice.
12. **Independent critique.** `shotkit:visual-asset-critic` or the `impeccable-finish-reviewer` agent on the frame sheet, plus `edit-kit:qa` and `reel-editor-qa`; `qa.md` lists every blocker as `- [ ]` until fixed.
13. **Delivery.** `python3 scripts/gate.py <prod> --video final.mp4 --vo-json ... --script ... --cues ...` must print GATE PASSED: files present, pace in range, word error ≤ 8%, SFX budget, -15..-13 LUFS and ≤ -1 dBTP, ≥ 12 Mb/s, no stray streams. Export 15-20 Mb/s.

## Branches: one core tool each, then its sub-tools

`reel-production` is the spine and always the entry point. Pick ONE branch by what the user has and wants; the branch's core tool owns stages 4-7 for that film and its sub-tools are called only through it. Combining branches is normal (a heritage film that opens on a map), but each part keeps its own core.

| Branch | Pick it when | Core | Sub-tools (in the order they are used) |
|---|---|---|---|
| **A. Footage edit** | the user gives raw footage: talking head, podcast, interview, phone clips, real estate, construction | `edit-kit:director` (via `edit-kit:edit`) | `edit-kit:reels` (9:16) or `edit-kit:youtube` (16:9), `edit-kit:theme`, `edit-kit:fx`, `depth-captions` or `edit-kit:embedded-captions`, `edit-kit:talking-head-recut`, `edit-kit:camera-arc` (2.5D orbit on a flat clip) |
| **B. Product demo / promo** | no footage: app, SaaS, AI tool, product launch, feature demo, motion-graphics ad | **`ui-promo-film`** directs (ElevenLabs standard); `edit-kit:saas` or `edit-kit:product-launch-video` (from a URL) builds | `motion-graphics-starter` prompts, `edit-kit:fx`, `hyperframes` + `gsap-*`, `edit-kit:oversized-cursor`, `kinetic-typography` |
| **C. 3D product** | a physical product as the hero: turntable, macro, exploded view, checklist | premium/luxury: **`premium-product-film`** (reference-level recipe + lookmeter); everyday checklist ads: look by category (gate 2): dark stage `edit-kit:blender-product-film` for premium, bright `product-check-reel` for everyday; Cycles | hero asset first: Blender MCP `search_assets`/`import_asset` (CC0/CC-BY models, Poly Haven HDRIs) or detailed modelling with `blender-agent-skills:blender-hardsurface-modeling`, `blender-pbr-materials`, `blender-lighting-lookdev`, `geometry-nodes`; `3d-animator` when no Blender |
| **D. Story, place, history** | a narrated story of a place, brand heritage, a topic explainer | `satellite-map-story` + `archival-collage-story` | `edit-kit:vox-director` (Vox paper-collage topic explainer), `edit-kit:faceless-explainer` (text to explainer), `colorize`, `object-separation` |
| **E. Special look / copy a reference** | "make it like this video", or a named look | `edit-kit:video-clone` | `edit-kit:anime-cel`, `edit-kit:pixel-art`, `edit-kit:whiteboard`, `edit-kit:paper-cutout`, `edit-kit:crayon-storybook`, `edit-kit:painted-animation`, `anime-animation-production`, `animation-styles` |
| **F. Music-driven** | the track drives everything: lyric video, beat montage, slideshow | `edit-kit:music-to-video` | `beat-sync-editing`, `music-video-production` |
| **H. Brand / logo reveal, teaser** | a logo reveal, intro/outro sting, launch teaser, "coming soon", or the brand moment closing any film | **`brand-reveal-film`** (Farborn standard) | Blender extrude or `3d-animator`, `logo-animation`, `premium-product-film` lighting for luxury brands |
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
- Every overlay change lands on a spoken word (Whisper timestamps, snapped to onsets). Sound follows the budget in gate 11: the moves that matter get a sound, not every move.
- Type: one bold display face, one clean face, one italic serif for captions; one accent colour; labels tracked at most 0.06em (edit-kit:qa); safe zone x 150-930, y 210-1530 on 1080x1920; reading text ≥ 34 px.
- Proof beats claims: show the stitch, the scratch test, the dimension, the glow; a chip or callout confirms it.
- The ending pays off or loops; the brand lands on the final beat with a sub drop.

## Known failure modes (check before calling a stage done)

Blender macro shots empty (camera clip start), soft focus at macro (f-stop too open), boolean materials grey, EEVEE glass blob, EOX tile seams, washed archive grades, failed cut-outs on close crops, captions running ahead of the voice, VO generated line by line (flat), long renders lost on session restart (run detached and resumable). Fixes live in the recipe skills.
