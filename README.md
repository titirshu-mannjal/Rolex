<div align="center">

# Rolex

**A curated Claude Code toolkit for making Instagram Reels that look hand-made, not AI-made.**

Motion graphics · photo-to-video · captions · sound design · editing · scripting

`500+ skills` · `33 plugins` · `3 MCP servers` · one command

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
git clone --depth 1 https://github.com/titirshu-mannjal/Rolex.git && cd Rolex
bash install.sh --list                     # see the packs
bash install.sh                            # core video stack (default)
bash install.sh --packs core,blender       # add packs
bash install.sh --all --tools              # everything + CLI tools
```

Restart Claude Code afterwards.

| Flag | What it does |
|---|---|
| `--packs a,b` | Install these packs (default: `core`) |
| `--all` | Install every pack |
| `--tools` | Also install `yt-dlp`, `auto-editor`, `whisper-ctranslate2` (Whisper captions), `edge-tts` and `depthflow` (photo parallax) through `uv` |
| `--dry-run` | Show what would happen, change nothing |
| `--list` | List the packs |

**Safe to re-run.** Nothing is deleted: any skill or agent it replaces is moved to `~/.claude/rolex-backup/<timestamp>/`. Plugins update in place.

---

## Packs

Only `core` installs by default. The rest are opt-in so overlapping skills don't pull Claude away from the strongest ones.

| Pack | Contents | Install when |
|---|---|---|
| **core** | 110 skills, 11 plugins, 4 agents, papercut pipeline, Playwright MCP | Always. This is the Reels stack. |
| **ai** | Remotion Superpowers + VibeFrame MCP | You want AI voice, music and image-to-video. Paid APIs, billed per clip. |
| **blender** | 94 Blender skills + Blender MCP | You render 3D in Blender. |
| **resolve** | 12 DaVinci Resolve editing skills | You edit in Resolve Studio. Non-commercial licence. |
| **noncommercial** | `anything2explainer` | Personal projects only. |
| **social** | LinkedIn, TikTok, YouTube, X, Threads, Facebook plugins | You post beyond Instagram. |
| **work** | Anthropic document skills (docx/pdf/pptx/xlsx) + sales, finance, legal, data, ops, HR, PM plugins | General business work. |

---

## What `core` gives you, by job

### 1. Idea, script and hook
| Skill / plugin | Use it for |
|---|---|
| `papercut-*` (9 skills) | Full zero-to-reel pipeline: strategy → hook → script → storyboard → voice → build → QA, with 79 SFX and 8 music beds |
| `social-media-skills` (plugin) | Hooks, Reels scripts, storyboards, captions, hashtags, trend-jacking, Kling / Runway / Veo / Luma prompts |
| `instagram-skills` (plugin) | Instagram-specific growth, Reels and carousel writing |
| `motion-brief-writer`, `motion-prompt-writer` | Turn an idea into a shot-by-shot motion brief |
| `reference-to-motion`, `video-shotcraft` | Break down a reference video and rebuild its shots |
| `brand-intake`, `motion-art-direction` | Lock brand, palette, type and motion rules before animating |

### 2. Motion graphics that don't look AI
| Skill / plugin | Use it for |
|---|---|
| `animation-skills` (plugin) | 11 finished reel styles in code: stick-figure, 3D explainer, map route, low-poly, Kurzgesagt-style |
| `kinetic-reel`, `painted-animation` (plugins) | Kinetic-type reels and hand-painted watercolour reels, beat-cut to a generated score |
| `hyperframes-motion-reel` | Showreel-grade, beat-synced reel from a one-line theme |
| `remotion` (plugin), `remotion-video` | React-based video, frame-exact, renders to MP4 |
| `hyperframes` (plugin) | HTML/CSS/GSAP compositions rendered to video |
| `gsap-*` (8 skills) | Official GreenSock animation guidance |
| `bang-motion`, `motionmaxxing`, `motion-design`, `animate` | Full motion-graphics pipelines and styles |
| `animation-principles`, `disney-animation-rule-skill` | Easing, timing, overshoot: why motion feels premium |
| `kinetic-typography`, `caption-animation`, `lower-thirds`, `title-sequence-3d`, `logo-animation` | Type-driven story videos |
| `explainer-*`, `vox-explainer`, `whiteboard-animation`, `animated-infographic`, `chart-animation`, `diagram-animation` | One-story explainers |
| `launch-video`, `apple-launch-film`, `ad-creative-video`, `testimonial-video`, `wrapped-video`, `countdown-video` | Product, ad and announcement formats |
| `threejs-*`, `anatomy`, `isometric-animation` | 3D and isometric scenes in code |

### 3. One photo → short video
| Skill / plugin | Use it for |
|---|---|
| `perspective-illusion`, `pixel2motion`, `colorize`, `fisheye-motion` | Animate a still: parallax, pixel motion, colour, lens moves |
| `object-separation` | Cut the subject from the background for 2.5D moves |
| `poppify` (plugin) | Photos to a finished reel (Poppify account) |
| `social-media-skills` → kling / runway / veo-3 / luma | Prompting the big image-to-video models |
| [DepthFlow](https://github.com/BrokenSource/DepthFlow) (`--tools`) | Free, local 3D parallax from one photo; no AI look, no watermark |
| `ai` pack → VibeFrame | Seedance, Kling, Runway, Veo, Grok image-to-video with a hard spend cap |

### 4. Captions, voice and sound
| Skill | Use it for |
|---|---|
| `sound-effects` | Beat-synced SFX pass, mixed to -16 LUFS, CC0 library included |
| `beat-sync-editing` | Cut on the beat |
| `ffmpeg-skill`, `reels-editor`, `video-short` | Whisper transcription and burned-in captions |

### 5. Edit, polish and export
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

- **Update:** run the installer again. Old copies go to `~/.claude/rolex-backup/`.
- **Remove a skill:** delete its folder in `~/.claude/skills/`.
- **Remove a plugin:** `claude plugin uninstall <name>@<marketplace>`.

## Licences

Every skill belongs to its author. See [SOURCES.md](SOURCES.md) for credits and licences. Two packs (`resolve`, `noncommercial`) are **non-commercial only**: don't use them for paid or brand work without the author's permission. The 17 `vibe-motion` skills and all plugins are downloaded from their authors at install time, not stored here. The installer and docs are MIT ([LICENSE](LICENSE)).
