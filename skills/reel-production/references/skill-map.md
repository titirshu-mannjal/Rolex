# Skill map: one winner per job

Consult this at decision points only (choosing a branch, a tool for a stage, a sound or caption tool). **Winner** is the default; switch only for the stated reason and write it in `TOOLS.md`.

## Routing table

| Job | Winner | Switch to (when) |
|---|---|---|
| Client profile, brand, voice, audience | `client-studio` | `brand-intake` (to fill brand.md/MOTION.md inside the client folder), `edit-kit:theme` (reads the same brand.json) |
| Expand a short request | `brief-amplifier` | - |
| Idea and visualization | `creative-visualization` | `creative-director` (only as a second opinion when the idea scores < 18/25) |
| Script | `reel-writer` agent | `screenwriting:*` (dialogue, series) |
| Voiceover | `voiceover-direction` (Kokoro) | `voicestudio` (designed/cloned voice, dubbing), Chatterbox (GPU, consenting voice) |
| Product demo / promo / SaaS / app / launch | `ui-promo-film` → build with `edit-kit:saas` | `edit-kit:product-launch-video` (from a URL); `launch-video`, `apple-launch-film`, `ad-creative-video` only as reading |
| Premium physical product, explode/assemble | `premium-product-film` | `product-check-reel` (everyday checklist ad), `edit-kit:blender-product-film` (bottles/cans/jars from a photo), `3d-animator` (no Blender) |
| Brand / logo reveal, teaser | `brand-reveal-film` | `logo-animation` (flat lockup only) |
| Footage edit (talking head, podcast, phone clips) | `edit-kit:director` | `edit-kit:reels` / `edit-kit:youtube` per format |
| Place / map story | `satellite-map-story` | `remotion-maps` (Mapbox token), `threejs-earth-render` |
| Heritage / history | `archival-collage-story` | `edit-kit:vox-director` (topic explainer in Vox collage) |
| Explainer | `explainer-studio` | `manim-skill` (math), `edit-kit:faceless-explainer` (from text), `edit-kit:pr-to-video` (code change) |
| Music-driven | `edit-kit:music-to-video` | `beat-sync-editing` |
| Special look / copy a reference on request | `edit-kit:video-clone` | the look skills it routes to |
| Motion graphics build | `hyperframes` + registry blocks (`creative-visualization/references/registry-index.md`) + `gsap-*` | `remotion` (React projects) |
| Multi-scene continuity | `edit-kit:motion-doctrine` | `edit-kit:cut-the-curve`, `edit-kit:seam-craft` |
| Captions | `edit-kit:fx` kinetic captions | `depth-captions` (word behind a talking head), `edit-kit:embedded-captions` (plain subtitles) |
| Sound design | `real-sfx` | `real-sound` (whole licensed soundtrack), `openverse-sounds` (a missing real sound) |
| Judge audio | `earshot` (critique, rank, ab, timeline) | `voiceover-direction/prosody.py` (voice delivery) |
| Study a reference | `scripts/teardown.sh` → `teardowns.md` | `learn` (a tutorial video → a skill) |
| QA | `scripts/gate.py` + `edit-kit:qa` + `reel-editor-qa` agent | `shotkit:visual-asset-critic` (independent frame critique) |
| Free route for a paid capability | `references/free-routes.md` (`scripts/hf_space.py`) | - |
| Export and packaging | `reel-export`, `loop-cover` | `instagram-skills:*`, `youtube-export` |

## NOT FOR video work (do not load)

- `poppify:*`: paid ("seeds") and triggers on "reel"; only with the user's explicit OK.
- `teardown` (a machine-simulator builder, not reference teardowns), `it-reelsmaker` (overlaps branch A, unmapped).
- `genre-*`, `*-worlds`, `godot/unity/unreal-export` (game design).
- Business packs: `sales:*`, `finance:*`, `human-resources:*`, `legal:*` (except `legal:compliance-check` for claims), `operations:*`, `apollo:*`, `small-business:*` (except `brand-style` as reading), `mannjal-program-builder`.
- Duplicates: prefer the `edit-kit:` copy inside an Edit Kit build and the standalone copy elsewhere (`video-shotcraft`, `painted-animation`, `figma`, `threejs-animation`, `particle-system`, `shader-glsl`); `remotion:*` and unprefixed `remotion-*` are the same skills.

# Stage detail

## 0 Research
- **`anthropic-skills:deep-research`** (multi-source research), **WebSearch** for single facts; `yt-dlp` + `ffmpeg` frame sheets to study reference reels; `learn` to turn a tutorial video into a reusable skill.
- Reference teardown: frames at 2 fps → contact sheets; cut detection (`select=gt(scene,0.25)`); voice via Demucs → `voiceover-direction/prosody.py`; SFX map method in `productions/_research/reel-refs/SFX-MAP.md`.
- `social-media-skills:viral-reverse-engineering`, `social-media-skills:competitor-analysis` - why a reel works / what the category does.
- Real assets: Wikimedia Commons API (check each licence), `openverse-sounds`, NASA GIBS / Natural Earth (`satellite-map-story`), the brand's own photos.

## 1 Idea and brief
- **`brief-amplifier`** → **`creative-visualization`** (the idea); `creative-director` only as a second opinion.
- `papercut-strategy`, `brand-intake`, `small-business:brand-style` (brand rules), `manjuforge` (series memory), `social-media-skills:hook-writer`, `instagram-skills:ig-hook-extractor`.

## 2 Script and voice
- **`reel-writer` agent** for the script; **`voiceover-direction`** for the read (Kokoro `hm_omega` male default, `hf_alpha` female; one continuous read; polish; measure).
- `screenwriting:*` (dialogue, structure), `social-media-skills:reels-script`, `papercut-script`, `papercut-voice`, `voice-and-audio`.
- Not for this: edge-tts for anything published (licence grey; internal drafts only), Chatterbox on CPU (too slow; GPU only, consenting voices).

## 3 Look
- **`reel-art-director` agent**, **`visual-style-direction`**.
- Light and set: `lighting-direction`, `production-design-direction`, `lookdev`, `materials`, `lighting`.
- Style presets (pick at most one): `minimalist-style`, `realistic-style`, `noir-style`, `painterly-style`, `vector-style`, `isometric-style`, `anime-style`, `manga-style`, `comic-book-style`, `hand-painted-style`, `lowpoly-style`, `stylized-style`, `cartoon-style`, mood packs (`dark-gritty-mood`, `cozy-wholesome-mood`, `brutalist-mood`, `dream-surreal-mood`, `neon-retrofuturism`, `frutiger-aero-style`, `visual-console-eras`, horror styles).
- `design-taste-frontend`, `impeccable`, `ui-ux-pro-max:*` - for UI screens shown in the film.
- Not for: `genre-*` (game design), `*-worlds` (worldbuilding for games), `godot-export`, `unity-export`, `unreal-export`.

## 4 Direction and storyboard
- **`reel-storyboard-artist` agent**; **`cinematic-director`** for shot logic.
- `cinematic-shot-direction`, `camera-cinematography`, `shot-composition`, `editing-montage`, `storyboard-previsualization`, `shotkit:*`, `visual-skills:video`, `video-shotcraft`, `motion-brief-writer`, `motion-art-direction`.

## 5 Build (format recipes)
- Product / 3D: **`premium-product-film`** (premium) · `product-check-reel` (everyday checklist, Blender headless) · **`3d-animator`** (three.js, no Blender) · Blender pack (`blender-agent-skills:*`, `blender-director`, `blender-modeler`, `hard-surface`, `cloth-sim`, `materials`, `rendering`, `compositing`, `geometry-nodes`, `particle-system`, `physics-sim`) · `threejs-*` · `title-sequence-3d`, `archviz`, `light-spotlight-render`.
- Places: **`satellite-map-story`** · `remotion-maps` (Mapbox token) · `threejs-earth-render` · `animation-skills:map-route`.
- History / collage: **`archival-collage-story`** · `colorize`, `object-separation`, `perspective-illusion`, DepthFlow, `pixel2motion`.
- Motion graphics: **`hyperframes`** (+ `hyperframes-registry` blocks first) · **`motion-graphics-starter`** prompts · `gsap-*` · `kinetic-typography`, `kinetic-reel:*`, `bang-motion`, `motionmaxxing`, `hyperframes-motion-reel`, `motion-design`, `motion-effects`, `motion-overlays`, `lower-thirds`, `logo-animation`, `milestone-reveal`, `countdown-video`, `svg-animation`, `lottie-animation`, `color-motion`, `motion-background`.
- Remotion route: `remotion:*` / `remotion-best-practices` when the project is React or needs Remotion components (`remotion-3d-ticker`, `remotion-candlestick`, `remotion-vinyl-player`).
- Data: `animated-chart`, `chart-animation`, `animated-infographic`, `diagram-animation`, `data:create-viz`.
- Explainers: `explainer-studio:*`, `manim-skill`, `manim-video`, `motion-canvas`, `papercut-*`, `animation-skills:kurzgesagt`, `vox-explainer`, `whiteboard-animation`.
- Characters: Rev2D MCP, `what-if-animation`, `character-design-continuity`, `line-art-animation`, `rive-mcp:*`, `anime-animation-production`, `vocaloid-style-mv`.
- Motion quality (apply to everything): **`animation-principles`**, `disney-animation-rule-skill`, `animation-basics`.
- Talking head: **`depth-captions`**, `talking-head-b-roll`, `caption-animation`, `remotion-captions`, `captions`.
- Ads and launches: used at stage 1 (Idea), not as build afterthoughts: `ad-creative-video`, `apple-launch-film`, `launch-video`, `brand-launch-video-star`, `business-motion-film`, `testimonial-video`.

## 6 Sound
- **`real-sfx`** (first pass on every film, not optional) - real sounds from the SOUNDE library (indexed), frame-exact, critique. **`earshot`** - judge everything you cannot hear (its critique compares against 7 launch films; also compare density and music gap against the user's own references) (`realness`, `rank`, `compare`, `ab`, `timeline`, `critique`).
- `real-sound` (whole soundtrack with licence audit), `openverse-sounds` (missing real sounds), `sound-effects` (CC0 pack + measured mix), `beat-sync-editing` (cuts on the beat), `music-and-sound`, `music-video-production`, `library/music/` (Mixkit tracks).
- Not for: synthesized SFX where a recording exists; `earshot make` only when nothing recorded fits.

## 7 Edit and QA
- **`hyperframes`** assembly + `npx hyperframes check` / `snapshot`; **`reel-editor-qa` agent**; `qa-review`, `papercut-qa`.
- `video-use`, `ffmpeg-skill`, `edit-video`, `rough-cut`, `reels-editor`, `vlog-pacing`, `effects`, `vfx-fx`, `hyperframes-to-after-effects` (hand-off).

## 8 Deliver
- **`reel-export`**, **`loop-cover`**, `instagram-skills:ig-caption-writer`, `instagram-skills:ig-hashtag-strategist`, `social-media-skills:thumbnail-design`, `export-pipeline`, `youtube-export`.

## Unique strengths: what only this tool does

Pick by the job it uniquely owns. If two tools fit, use the one whose unique job it is, and write the other in the ledger as "considered".

| Tool | The one thing it is uniquely best at |
|---|---|
| `earshot` | Hearing for an AI: realness, ranking candidates, A/B, mix scorecard against 7 pro launch films, sync to picture. Run it on every mix. |
| `real-sfx` | Placing real sounds from the user's own indexed library on exact frames at matched levels, with a self-critique. |
| `real-sound` | A whole licensed soundtrack: music edit at bar lines, licence audit, credits, mastering. |
| `openverse-sounds` | One specific real recording the libraries lack, commercial-safe, with its credit line. |
| `sound-effects` | A measured mix pass with a CC0 pack and loudness proof. |
| `voiceover-direction` | A VO that sounds alive: continuous read, stress, pause shaping, prosody measured against a reference. |
| `creative-visualization` | Inventing the idea and choosing the motion: eight lenses, animation atlas, domain guide with clichés to avoid, push-further checks. |
| `ui-promo-film` | Directing product demos and promos at the ElevenLabs standard: real UI in motion, voice-led story, word-fill type, 90% of events on sound. |
| `brand-reveal-film` | Logo reveals and launch teasers: fragments in darkness, build, resolve, 3D-to-2D handoff, drone-and-riser sound. |
| `premium-product-film` | Reference-level luxury product CG for any category: asset detail inventory, low-key edge lighting, assembly choreography, measurable look via `lookmeter.py`. |
| `product-check-reel` | Blender product films: macro detail, exploded view with tracked labels, checklist format. |
| `3d-animator` | Cinematic 3D in pure three.js with sub-frame motion blur, DOF and soft shadows; scenes and rooms without Blender. |
| `satellite-map-story` | Map shots on real imagery with India's official boundary, pins on spoken names. |
| `archival-collage-story` | Heritage montage: cut-outs, archive stacks, giant counters, era colour switch. |
| `depth-captions` | Text behind a person (BiRefNet masks) with onset-snapped word timing. |
| `motion-graphics-starter` | Tested prompts for four motion styles and ad formats; fastest path to a proven look. |
| `hyperframes` | Deterministic HTML/GSAP compositing over any plates; checks for safe zones, holds, type floor. |
| `hyperframes-to-after-effects` | Hand-off of a finished HyperFrames film to an editor as live AE layers. |
| `remotion` | React-based video when components, data or Remotion-only packages are needed. |
| `kinetic-typography`, `kinetic-reel` | Type as the main actor. |
| `animation-principles`, `disney-animation-rule-skill` | Motion with weight: anticipation, overshoot, follow-through. Apply to every tween. |
| `creative-director` | Finding the one idea when the brief is vague. |
| `reel-writer`, `reel-storyboard-artist`, `reel-art-director`, `reel-editor-qa` | Independent crew passes that catch what the lead misses (use for films over ~15 s or with several scenes). |
| `learn` | Turning a tutorial video into a new reusable skill. |
| `blender-agent-skills:*` | Specific Blender jobs (cloth, rigging, hard surface, PBR, lighting) when the recipe needs more than the product rig. |
| `threejs-*` | three.js reference for anything custom in a code-rendered scene. |
| `gsap-*` | Timeline and easing reference for every overlay. |
| `colorize`, `object-separation`, DepthFlow, Real-ESRGAN, rembg | Asset repair: colour, video cut-outs, photo parallax, upscaling, still cut-outs. |

Genuinely not for short-form video work: `genre-*` (game design), `*-worlds` (game worldbuilding), `godot/unity/unreal-export`, `mannjal-program-builder` (Mannjal lending programs).

## Edit Kit (`edit-kit:*`) and VoiceStudio: what each uniquely owns

| Tool | Unique job |
|---|---|
| `edit-kit:director` / `edit-kit:edit` | Editing raw footage end to end in 11 named styles (Creator Explainer, SaaS, Motion Graphics, Vox, Ali Abdaal, Real Estate, Construction, Gadzhi, Bold Impact, Podcast, Finance). |
| `edit-kit:fx` | The MotionKit/CreatorFX effects engine: kinetic captions, glass cards, checklist chips, text behind subject, smooth zooms, counters, cursor clicks, 3D tilted dashboards, logo orbits, Premiere-safe export. |
| `edit-kit:motion-doctrine` | The law of continuity across scenes (vector ledger, stamped seams, seam gate). Gateway for every multi-scene film. |
| `edit-kit:cut-the-curve`, `edit-kit:seam-craft` | Velocity-matched seams (zoom-through, waterfall cut, rack-focus blur-cut) and seam render correctness. |
| `edit-kit:theme` | Colours/fonts from a client brand kit (`~/.claude/motion-kit/brands/<client>/brand.json`) or designed from the footage. |
| `edit-kit:camera-arc` | A real-feeling 3D orbit on an already-shot flat clip (per-frame depth). |
| `edit-kit:video-clone` | Reverse a reference video's cut and style and route to the right look skill. |
| `edit-kit:blender-product-film` | Dark-studio liquid, glass, condensation product films in Blender. |
| `edit-kit:vox-director` | Vox paper-collage explainers from one topic, end to end. |
| `edit-kit:music-to-video` | Music-first edits on the beat grid (lyric, montage, kinetic promo). |
| `edit-kit:product-launch-video`, `edit-kit:pr-to-video` | Launch film from a website URL; code-change explainer from a PR. |
| `edit-kit:embedded-captions`, `edit-kit:talking-head-recut` | Captions and overlay cards on an untouched talking head. |
| `edit-kit:sound` | Its own SFX/music pass; prefer `real-sfx` for real recordings and use edit-kit's mix numbers. |
| `edit-kit:qa` | Delivery gate: format, loudness, SFX sync, safe zone, face clear, nothing mid-animation. |
| `voicestudio` | Local voice studio: design a voice from a description, clone a consented voice, dub into 646 languages, clean and normalize audio, transcribe; CLI `voicestudio speak/voices/dub/audio`. Needs one first-run setup in its app. |
