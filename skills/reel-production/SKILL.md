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
| 2 | **Script + voice** | `reel-writer` agent, then `voiceover-direction` | dialogue or characters: `screenwriting:*`; user records their own voice: `depth-captions` + DeepFilterNet | hook in 1-2 s; VO is one continuous read; pace 2.6-3.3 words/s; prosody measured against a reference; Whisper reads every word right |
| 3 | **Look** | `reel-art-director` agent | brand exists: `brand-intake`, `small-business:brand-style` | palette ≤ 4 colours, 2 type families, colour script per beat, engine chosen |
| 4 | **Storyboard** | `reel-storyboard-artist` agent | very short (<10 s) or a single continuous move: a shot table in `brief.md` is enough | every shot has framing, camera move, duration, the word it lands on, and its sound |
| 5 | **Build** | the format recipe (table below) | — | stills at 3-5 key times looked at before any long render; previews at 25% before full renders |
| 6 | **Sound** | `real-sfx` (your SOUNDE library, frame-exact) | full soundtrack with licence audit: `real-sound`; missing sound: `openverse-sounds`; nothing recorded exists: `earshot make` | `earshot` checks: candidates ranked (`earshot rank`), mix critiqued (`earshot critique` / `timeline`); -14 LUFS, true peak ≤ -1.5 dBTP |
| 7 | **Edit + QA** | `hyperframes` (or `remotion`) for overlays and assembly; `reel-editor-qa` agent | handing off to an editor: `hyperframes-to-after-effects` | `npx hyperframes check` clean; frames pulled at every cut and pop and looked at; captions in safe zones; QA blockers fixed and re-rendered |
| 8 | **Deliver** | `reel-export`, `loop-cover`, `instagram-skills:ig-caption-writer` | other platforms: `youtube-export`, `tiktok-skills:*` | 1080x1920 H.264, credits in caption for CC BY assets, `sources.md` complete |

## Format recipes (stage 5)

| The film is… | Recipe skill | Engine |
|---|---|---|
| Product checklist / feature ad, 360 turntable, macro details, exploded view | `product-check-reel` | Blender headless (EEVEE) + HyperFrames overlays; no Blender: `3d-animator` (three.js) |
| Cinematic 3D scene in code (desk, room, device, "no Blender") | `3d-animator` | three.js sub-frame renderer |
| Place story: map, region, pins, routes | `satellite-map-story` | HyperFrames |
| Heritage / history / "how X became Y" | `archival-collage-story` | HyperFrames + rembg + Real-ESRGAN |
| Talking head with premium captions | `depth-captions` | Remotion / Python compositing |
| Motion graphics, kinetic type, SaaS / app promo | `motion-graphics-starter` prompts + `hyperframes` | HyperFrames + `gsap-*` |
| Data, numbers, charts | `animated-chart`, `chart-animation`, `animated-infographic` | HyperFrames / Remotion |
| Explainer | `explainer-studio`, `manim-skill`, `papercut-*` | as the skill says |
| Anime / characters | `anime-animation-production`, Rev2D MCP, `what-if-animation` | as the skill says |
| One photo to motion | `perspective-illusion`, DepthFlow, `pixel2motion` | |

Combining recipes is normal (a heritage film that opens on a map; a product ad with depth captions). Each recipe still owns its stage.

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
