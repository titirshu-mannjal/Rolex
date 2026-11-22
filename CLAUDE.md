# Rolex studio

You are working in **Rolex**, a studio for premium short-form video: anime-style series, cinematic shorts, motion-graphics films and Instagram Reels that look like a real studio made them, never like AI slop.

The skills, plugins and agents below are installed user-wide by `install.sh`. If one is missing, run `bash install.sh` from this folder (see "Installing" at the end).

## How to start any video

Use the `reel-production` skill. It runs the job like a studio and stops for the user's OK at each stage: brief → script (`reel-writer`) → look (`reel-art-director`) → storyboard (`reel-storyboard-artist`) → build → sound → edit and QA (`reel-editor-qa`) → deliver.
Work goes in `productions/<slug>/`. A series keeps its bible in `productions/<series>/bible/` and every episode reads it first.

Before building, look at `references/` if it exists: two finished videos Claude made in this workflow, with their full source, treatment, storyboards and sound scripts. Match or beat that bar.

## The bar

- One idea per video. The hook lands in the first 1-2 s. The ending loops or pays off.
- Direct it like film or anime: motivated camera, shot sizes that vary with purpose, cuts on action or beat, colour script per beat, consistent characters on model.
- Motion has weight: eased, with anticipation and follow-through (`animation-principles`, `animation-basics`, `disney-animation-rule-skill`). No linear slides, no default fades.
- Restraint reads as premium: limited palette, big readable type (phone first), safe zones clear of Instagram UI, sound designed rather than stacked.
- Render, look at the frames, fix, re-render. Never call a cut done without looking.

## Which tool for which job

| Goal | First choice | Also |
|---|---|---|
| Concept, big idea | `creative-director` | `papercut-strategy` |
| Script, hook, series arcs | `reel-writer` agent, `screenwriting:*` | `social-short-production`, `instagram-skills:*`, `papercut-hook`, `manjuforge` (series memory) |
| Direction, shot list, blocking | `cinematic-director` | `visual-skills:video`, `cinematic-shot-direction`, `editing-montage` |
| Storyboard / animatic | `reel-storyboard-artist` agent, `shotkit:*` | `storyboard-previsualization`, `papercut-storyboard` |
| Art direction, colour script, style bible | `reel-art-director` agent, `visual-style-direction` | `anime-mv-art-direction`, `lighting-direction`, `production-design-direction`, `character-design-continuity` |
| **Frames / keyframes / stills** | Draw them in code: HyperFrames or Remotion stills, `animation-styles`, `shader-glsl` | Blender (`blender-agent-skills:*`, `blender-stylized-npr`), Rive (`rive-mcp:rive-designer`), ComfyUI (`comfy:*`, needs a GPU) |
| Anime / MV look | `vocaloid-style-mv`, `anime-animation-production` | `kinetic-reel:painted-animation`, `animation-styles` (cel anime, ukiyo-e…), `blender-stylized-npr` (toon 3D) |
| Characters that act | Rev2D MCP (rigged 2D puppets, lip-flap), `what-if-animation` | `line-art-animation`, `animation-skills:stick-figure`, `animation-skills:zach-3d-films`, Blender rigging |
| Motion graphics, kinetic type | `hyperframes` / `remotion` + `gsap-*` | `kinetic-reel:kinetic-reel`, `bang-motion`, `hyperframes-motion-reel`, `kinetic-typography` |
| Cinematic 3D | `threejs-*`, Blender pack | `title-sequence-3d`, `particle-system`, `blender-claymation` |
| Explainers | `manim-skill:manim-skill`, `explainer-studio:*` | `motion-canvas`, `animation-skills:kurzgesagt`, `papercut-*` |
| One photo → motion | `perspective-illusion`, `pixel2motion`, DepthFlow CLI | `object-separation`, `colorize`, `fisheye-motion` |
| Sound | `sound-effects`, `beat-sync-editing` | `library/` (local SFX and music), edge-tts / whisper-ctranslate2 CLIs |
| Edit, captions, export | `video-use`, `ffmpeg-skill`, `reel-export` | `caption-animation`, `reels-editor`, `loop-cover` |
| Instagram packaging | `instagram-skills:*` | `social-media-skills:*` |

Free tools only by default. Paid APIs (the `ai` pack) need the user's explicit OK.

## Local-only folders (never commit or push)

- `references/` - Claude-built reference videos and their source (confidential).
- `library/` - sound effects, music, style references.
- `productions/` - all new work.

## Installing (when asked to "install this repo")

1. Clone to the permanent location if it is not already there (plugins are installed from this folder, so it must stay):
   `git clone --depth 1 https://github.com/titirshu-mannjal/Rolex.git ~/.local/share/rolex/repo && cd ~/.local/share/rolex/repo`
   If it exists, update it: `git -C ~/.local/share/rolex/repo pull --ff-only`. The repo is about 1.5 GB; run the clone in the background and wait.
2. Show the packs (`bash install.sh --list`) and say that `core` is the default studio stack.
3. Run `bash install.sh` for core, or `bash install.sh --packs core,blender,...` / `bash install.sh --all` if the user asked for more. Add `--tools` for yt-dlp, auto-editor, whisper-ctranslate2, edge-tts and DepthFlow.
4. Report the summary line, any failures, and any MISSING system tools with the install command for the user's OS.
5. Tell the user to restart Claude Code.

Never delete existing skills: the installer moves replaced folders to `~/.claude/rolex-backup/<timestamp>/`. On Windows, run the installer from Git Bash or WSL.
