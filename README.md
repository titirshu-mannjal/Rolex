<div align="center">

# Rolex

**A studio-grade Claude Code toolkit for premium Instagram Reels: from idea to finished MP4, the way film and anime studios work.**

Concept · script · storyboard · art direction · animation · sound · edit · QA

`800+ skills` · `41 plugins` · `8 agents` · one command · free tools only by default

</div>

---

## Install

**Easiest: ask Claude.** Open Claude Code and paste:

```text
Install https://github.com/titirshu-mannjal/Rolex
```

Claude reads [`CLAUDE.md`](CLAUDE.md), runs the installer and reports what it set up.

**Or from a terminal:**

```bash
curl -fsSL https://raw.githubusercontent.com/titirshu-mannjal/Rolex/main/install.sh | bash
```

**Or clone first, then choose packs:**

```bash
git clone --depth 1 https://github.com/titirshu-mannjal/Rolex.git ~/.local/share/rolex/repo
cd ~/.local/share/rolex/repo
bash install.sh --list                     # see the packs
bash install.sh                            # core video stack (default)
bash install.sh --packs core,blender       # add packs
bash install.sh --all --tools              # everything + CLI tools
```

Restart Claude Code afterwards.

> **Keep the repo folder.** The download is about 1.5 GB. Plugins are installed from that local copy (`~/.local/share/rolex/repo` by default), so don't delete it. To update, run the installer again.

| Flag | What it does |
|---|---|
| `--packs a,b` | Install these packs (default: `core`) |
| `--all` | Install every pack |
| `--tools` | Also install `yt-dlp`, `auto-editor`, `whisper-ctranslate2` (Whisper captions), `edge-tts`, `depthflow` (photo parallax) and `rembg` (cut-outs) through `uv`; the Real-ESRGAN upscaler; the Kokoro (Indian English voices) and Chatterbox (voice cloning) engines in `~/.local/share/rolex/tts`; and the editorial fonts in `assets/fonts` |
| `--dry-run` | Show what would happen, change nothing |
| `--list` | List the packs |

**Safe to re-run.** Nothing is deleted: any skill or agent it replaces is moved to `~/.claude/rolex-backup/<timestamp>/`. Plugins you already have from their original marketplace are kept as they are.

---

## Start a video

After installing, tell Claude:

```text
Use reel-production to make a 30-second Reel about <your idea>.
```

The `reel-production` skill runs it like a studio and stops for your OK after each stage:

| Stage | Who | Output |
|---|---|---|
| 1. Brief | Showrunner (main Claude) | `brief.md` |
| 2. Script | `reel-writer` agent | Beat sheet, hook options, VO and on-screen text |
| 3. Look | `reel-art-director` agent | Visual bible, palette, type, colour script, engine choice |
| 4. Storyboard | `reel-storyboard-artist` agent | `shots.json` + HTML board: framing, camera, timing, transitions |
| 5. Build | Showrunner | Animation in the chosen engine |
| 6. Sound | Showrunner | SFX, music, voice, beat sync |
| 7. Edit + QA | `reel-editor-qa` agent | Frame-checked fixes until it passes |
| 8. Deliver | Showrunner | 1080×1920 MP4, cover, caption |

Everything lands in `production/<slug>/`, and the series bible in `bible/` keeps characters and style consistent across episodes.

---

## Packs

Only `core` installs by default. The rest are opt-in so overlapping skills don't pull Claude away from the strongest ones.

| Pack | Contents | Install when |
|---|---|---|
| **core** | 135 skills, 16 plugins, 8 agents, papercut pipeline, Rev2D puppet MCP, Playwright MCP | Always. This is the studio. |
| **genai** | ComfyUI (local WAN/LTX image-to-video, lip-sync, interpolation) + claude-code-video-toolkit (open models on Modal's free monthly credit) | Free AI video. ComfyUI needs an NVIDIA GPU with 12 GB+ VRAM. |
| **ai** | Poppify, Remotion Superpowers, VibeFrame | **Paid** APIs, billed per clip. |
| **blender** | 95 Blender skills (incl. claymation), Blender agent skills plugin + Blender MCP | You render 3D in Blender. |
| **resolve** | 12 DaVinci Resolve editing skills | You edit in Resolve Studio. Non-commercial licence. |
| **noncommercial** | `anything2explainer` | Personal projects only. |
| **social** | LinkedIn, TikTok, YouTube, X, Threads, Facebook plugins | You post beyond Instagram. |
| **work** | Anthropic document skills (docx/pdf/pptx/xlsx) + sales, finance, legal, data, ops, HR, PM plugins | General business work. |

---

## What `core` gives you, by job

### 1. Idea, script and hook
| Skill / plugin | Use it for |
|---|---|
| `creative-director` | Concept and big idea before any script |
| `screenwriting` (plugin, 26 skills) | Story structure, scene craft, series engine and bible, episode arcs |
| `social-short-production` | Short-form structure grounded in real platform metrics |
| `manjuforge` | Series memory: story bible, foreshadowing, 22 consistency checks across episodes |
| `papercut-*` (9 skills) | Full zero-to-reel pipeline: strategy → hook → script → storyboard → voice → build → QA, with 79 SFX and 8 music beds |
| `social-media-skills` (plugin) | Hooks, Reels scripts, storyboards, captions, hashtags, trend-jacking, Kling / Runway / Veo / Luma prompts |
| `instagram-skills` (plugin) | Instagram-specific growth, Reels and carousel writing |
| `motion-brief-writer`, `motion-prompt-writer` | Turn an idea into a shot-by-shot motion brief |
| `reference-to-motion`, `video-shotcraft` | Break down a reference video and rebuild its shots |
| `brand-intake`, `motion-art-direction` | Lock brand, palette, type and motion rules before animating |

### 2. Storyboard, direction and art direction
| Skill / plugin | Use it for |
|---|---|
| `visual-skills` (plugin) | Direction-first storyboards: Rule of Six, 14-field shot cards, rhythm, animatic keyframes |
| `cinematic-director` | Director's book, blocking, coverage, continuity bible, match cuts, lenses of 20 directors |
| `shotkit` (plugin) | shots.json storyboard, brand lock, visual critic, HTML board |
| `storyboard-previsualization`, `cinematic-shot-direction`, `editing-montage` | Shot lists, camera language, cutting rhythm |
| `lighting-direction`, `visual-style-direction`, `production-design-direction`, `character-design-continuity` | Lighting, style, sets and on-model characters |
| `anime-mv-art-direction`, `anime-animation-production`, `music-video-production` | Anime and MV art direction: colour scripts, motif systems, beat-matched shot lists |

### 3. Motion graphics that don't look AI
| Skill / plugin | Use it for |
|---|---|
| `animation-skills` (plugin) | 11 finished reel styles in code: stick-figure, 3D explainer, map route, low-poly, Kurzgesagt-style |
| `kinetic-reel` (plugin: kinetic-reel + painted-animation skills) | Kinetic-type reels and hand-painted watercolour reels, beat-cut to a generated score |
| `hyperframes-motion-reel` | Showreel-grade, beat-synced reel from a one-line theme |
| `remotion` (plugin), `remotion-video` | React-based video, frame-exact, renders to MP4 |
| `hyperframes` (plugin) | HTML/CSS/GSAP compositions rendered to video |
| `gsap-*` (8 skills) | Official GreenSock animation guidance |
| `bang-motion`, `motionmaxxing`, `motion-design`, `animate` | Full motion-graphics pipelines and styles |
| `animation-principles`, `disney-animation-rule-skill` | Easing, timing, overshoot: why motion feels premium |
| `kinetic-typography`, `caption-animation`, `lower-thirds`, `title-sequence-3d`, `logo-animation` | Type-driven story videos |
| `explainer-*`, `vox-explainer`, `whiteboard-animation`, `animated-infographic`, `chart-animation`, `diagram-animation` | One-story explainers |
| `launch-video`, `apple-launch-film`, `ad-creative-video`, `testimonial-video`, `wrapped-video`, `countdown-video` | Product, ad and announcement formats |
| `threejs-*`, `anatomy`, `isometric-animation`, `shader-glsl`, `particle-system` | 3D, shaders, particles, isometric scenes in code |
| `animation-styles` | 39 hand-made looks in code: cel, paper, ink, and more |
| `what-if-animation`, Rev2D (MCP), `line-art-animation` | Character stories: rigged cast, 2D puppets with bones and lip-flap, ink walk cycles |
| `vocaloid-style-mv` | Anime lyric MVs, beat-locked, 9:16 |
| `manim-skill` (plugin), `motion-canvas`, `explainer-studio` (plugin) | 3b1b-style math, Motion Canvas, 8 hand-drawn explainer styles |
| `lottie-animation`, `svg-animation`, `rive-mcp` (plugin), `pixelfx` (plugin) | Lottie, SVG, Rive state machines, 244 pixel-art effects |

### 4. One photo → short video
| Skill / plugin | Use it for |
|---|---|
| `perspective-illusion`, `pixel2motion`, `colorize`, `fisheye-motion` | Animate a still: parallax, pixel motion, colour, lens moves |
| `object-separation` | Cut the subject from the background for 2.5D moves |
| `poppify` (plugin) | Photos to a finished reel (Poppify account) |
| `social-media-skills` → kling / runway / veo-3 / luma | Prompting the big image-to-video models |
| [DepthFlow](https://github.com/BrokenSource/DepthFlow) (`--tools`) | Free, local 3D parallax from one photo; no AI look, no watermark |
| [rembg](https://github.com/danielgatis/rembg) (`--tools`) | Free, local background removal for collage cut-outs and product isolation |
| [Real-ESRGAN ncnn](https://github.com/xinntao/Real-ESRGAN) (`--tools`) | Free 4x upscaler on any GPU through Vulkan; rescues archive scans and half-res renders |
| `ai` pack → VibeFrame | Seedance, Kling, Runway, Veo, Grok image-to-video with a hard spend cap |

### 5. Captions, voice and sound
| Skill | Use it for |
|---|---|
| `sound-effects` | Beat-synced SFX pass, mixed to -16 LUFS, CC0 library included |
| `beat-sync-editing` | Cut on the beat |
| `ffmpeg-skill`, `reels-editor`, `video-short` | Whisper transcription and burned-in captions |

### 6. Edit, polish and export
| Skill / plugin | Use it for |
|---|---|
| `video-use`, `it-reelsmaker` (plugin) | Edit raw footage into a reel |
| `effects`, `motion-effects`, `motion-broll`, `talking-head-b-roll` | Talking-head effects and B-roll |
| `reel-export`, `short-form-video`, `loop-cover` | 9:16 export, platform specs, covers |
| `qa-review`, `shot-composition` | Check frames before posting |
| `impeccable`, `design-taste-frontend`, `hallmark`, `ui-ux-pro-max`, `frontend-design` | Design quality for every frame |

---

## Optional: connect AI generators

Not installed automatically because they need your own API key or account. Run the line once you have the key.

| Tool | What it adds | Set up |
|---|---|---|
| [MiniMax MCP](https://github.com/MiniMax-AI/MiniMax-MCP) | Hailuo image-to-video from one photo, TTS, voice clone | `claude mcp add minimax -e MINIMAX_API_KEY=<key> -e MINIMAX_API_HOST=https://api.minimax.io -- uvx minimax-mcp -y` |
| [Google GenMedia MCP](https://github.com/GoogleCloudPlatform/genmedia-creative-studio/tree/main/experiments/mcp-genmedia) | Veo image-to-video, Lyria music, Chirp voice | Follow its `install.sh`, then `claude mcp add veo -e GOOGLE_CLOUD_PROJECT=<id> -- mcp-veo-go` |
| [Postiz](https://github.com/gitroomhq/postiz-app) | Schedule and publish Reels with an approval step | `claude mcp add --transport http postiz https://mcp.postiz.com/mcp --header "Authorization: Bearer <key>"` (or self-host free) |
| [Herk Edit Kit](https://github.com/nateherkai/herk-edit-kit) | Talking-head editing kit: word-precise captions, silence cuts, 406 motion cards | Clone it and open Claude Code **inside that folder**. Its skill names clash with core, so keep it separate. |

## Requirements

| Tool | Needed for | Install |
|---|---|---|
| [Claude Code](https://claude.com/claude-code) | Plugins and MCP servers | `npm i -g @anthropic-ai/claude-code` |
| git, bash | The installer | Built in on macOS/Linux; Git Bash or WSL on Windows |
| ffmpeg | Almost every video skill | `brew install ffmpeg` · `sudo apt install ffmpeg` · `winget install ffmpeg` |
| Node.js 18+ | Remotion, HyperFrames, Playwright | [nodejs.org](https://nodejs.org) |
| Python 3.10+ and [uv](https://docs.astral.sh/uv/) | Whisper, TTS, `--tools` | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Blender 4+ | blender pack only | [blender.org](https://www.blender.org) |

Some plugins call paid services (Poppify, ElevenLabs, Kling, Runway). They ask for keys when used; nothing is charged at install.

---

## Update and uninstall

- **Update:** run the installer again: it pulls the latest repo and refreshes plugins. Old skill copies go to `~/.claude/rolex-backup/`.
- **Remove a skill:** delete its folder in `~/.claude/skills/`.
- **Remove a plugin:** `claude plugin uninstall <name>@<marketplace>`.

## Licences

Every skill belongs to its author. See [SOURCES.md](SOURCES.md) for credits and licences. Two packs (`resolve`, `noncommercial`) are **non-commercial only**: don't use them for paid or brand work without the author's permission. Everything (skills, plugins, the papercut pipeline) is stored in this repo, so installs keep working even if an author deletes their repo. The installer and docs are MIT ([LICENSE](LICENSE)).
