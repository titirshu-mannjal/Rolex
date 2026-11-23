# Free routes for paid capabilities (legitimate only)

Free by default, never by breaking terms: no paywall bypass, no account farming, no scraped or shared keys, no
watermark removal. Every route below is a free tier, an open model or an open licence. Note each asset's licence in
`sources.md`. Tested 2026-11-24 unless marked.

| Paid tool people use | Free route here | Limits | Licence for commercial work | How |
|---|---|---|---|---|
| ElevenLabs voices | Kokoro (local), VoiceStudio (local: design, clone consented voices, dub), edge-tts (drafts only) | CPU/4 GB GPU speed | Kokoro Apache-2.0; VoiceStudio app AGPL (output is yours); check each VoiceStudio model's licence in its Model Manager | `voiceover-direction`, `voicestudio` |
| Midjourney / paid image gen | FLUX.1-schnell on a public Hugging Face Space (tested: 10 s, premium stills) | ~5 GPU-min/day with the user's free HF token, ~2 min as guest | FLUX.1-schnell Apache-2.0 (FLUX.1-dev is non-commercial: never for client work) | `scripts/hf_space.py image` |
| Paid image-to-3D (Meshy, Tripo, Rodin) | TRELLIS (MIT) or Hunyuan3D-2 Spaces | one generation ≈ 1-2 GPU-min; needs the free HF token; single mesh, not explodable | TRELLIS MIT; Hunyuan3D-2 has a regional community licence: check before client use | `scripts/hf_space.py to3d` (untested until the token is set) |
| Higgsfield / Runway / Kling video gen | Open video models on HF Spaces (Wan, LTX-Video) | 1-2 short clips/day on the free quota; quality below paid | per model (Wan Apache-2.0) | use only for B-roll texture, never for the product itself |
| Stock footage and photos | Pexels and Pixabay (free API keys from the user's free accounts), Openverse, Wikimedia Commons | API rate limits | Pexels/Pixabay licences allow commercial use without attribution (no trademarks/logos, no implied endorsement); Commons per file | `openverse-sounds` pattern; keep a source line per asset |
| Music libraries (Artlist, Epidemic) | Mixkit (local `library/music`), Pixabay Music, YouTube Audio Library (manual download), Free Music Archive (check each track's CC licence) | catalogue size | per track | pick with `earshot rank` |
| SFX libraries | SOUNDE pack + CC0 pack (local, indexed in `real-sfx`), Openverse/Freesound CC0, `earshot make` | - | per pack / CC0 | `real-sfx`, `openverse-sounds` |
| Adobe Podcast voice clean-up | DeepFilterNet (local), VoiceStudio `audio clean` | - | MIT/Apache | `voiceover-direction` |
| After Effects / Premiere | HyperFrames + GSAP (code), Blender, DaVinci Resolve free; hand-off with `hyperframes-to-after-effects` | - | - | |
| Premium 3D models | Poly Haven (CC0), Sketchfab CC models via Blender MCP (needs the user's free Sketchfab API key), procedural builds | - | CC0 / CC-BY (credit) | `premium-product-film` |
| Blender MCP Premium generators | not needed: TRELLIS/Hunyuan3D Spaces above | - | - | |

## One free account unlocks the most

A free Hugging Face account token (read scope, made by the user at huggingface.co/settings/tokens) gives:
faster VoiceStudio model downloads (pasted in VoiceStudio Settings → Credentials) and the ~5 GPU-min/day Space quota
(saved by the user with `huggingface-cli login` or as `HF_TOKEN`). Never print, store in files or commit the token.

## When a paid tool is genuinely better

Say so plainly, with the cost and what it would add (for example ElevenLabs for a hero voice in a paid campaign), and let
the user decide. Do not quietly downgrade a client deliverable to stay free.
