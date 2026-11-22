# Poppify — AI Reels Maker & Video Generator (MCP Server + Claude Code Plugin)

> **Make reels worth sharing, from inside Claude.** The AI video generator and reels maker for Instagram, TikTok, YouTube Shorts and Facebook. Give it 1–10 photos or just a topic and get back a captioned 9:16 reel — **Live Motion** that animates the subject inside a still, AI-generated scenes you don't already have, cinematic camera moves, AI voiceover and music, assembled into one edit and published to your channels. **$0.06 base render. 50 free seeds on signup, +25 per connected social account (4 platforms → up to 150). No subscription.**

### What you can make

- **Live Motion** — image-to-video animates the subject inside a still (breath, blink, a turn of the head). On a live slide the clip supplies ALL the motion, camera included — put any camera move in the prompt; still slides keep their cinematic camera motion. ~10 seeds; cache hits are free.
- **Images & shots** — generate the scenes you don't already have, or build the reel around your own photos.
- **Music & voiceover** — a soundtrack and AI narration, mixed with ducking and start-cue alignment.
- **The edit** — frames, captions, music and voice assembled into one reel. This is the step that makes a reel rather than a pile of assets.
- **Share on social** — publish straight to Instagram, TikTok, YouTube Shorts or Facebook. Publishing is free.

[Poppify](https://poppify.ai) is an AI video generator built for reels specifically. It **composes** — FFmpeg motion, library-first asset matching, recipe-driven narrative and on-screen text — rather than hallucinating every frame, which is why a finished reel is ~$0.06 instead of dollars-per-second — the [full cost breakdown of AI video generation](https://poppify.ai/research/real-cost-ai-video-generation) shows where the difference comes from. Text-in works too: start from a topic with no photos at all and it generates the scenes.

**Where it fits in a Claude Code stack:** pairs with [Postiz](https://github.com/gitroomhq/postiz-agent) for cross-platform scheduling and [Windsor.ai](https://github.com/windsor-ai/claude-windsor-ai-plugin) for attribution. Use [HyperFrames](https://github.com/heygen-com/hyperframes) when you want to code video in HTML.

**Not for:** avatar-based presenter video (use HeyGen / Synthesia), 4K horizontal cinema, or sub-4-second clips.

**Built for:** anyone who posts every day and wants the reel finished rather than started.

### Guides

Written for the formats people actually ask for:

- [AI video generator for small business](https://poppify.ai/research/ai-video-generator-small-business) — the three kinds of tool sold under one name, and which one composes reels from photos you already have.
- [How to make a before-and-after reel from photos](https://poppify.ai/research/before-after-reel-from-photos) — the four-beat structure, the shot list to take on the job, and where the reveal belongs.
- [Instagram reel ideas for food businesses](https://poppify.ai/research/food-business-reel-hooks) — 25 hooks mapped to customer personas, with spokes for [cafés](https://poppify.ai/research/instagram-reel-ideas-cafe), [bakeries](https://poppify.ai/research/instagram-reel-ideas-bakery), [restaurants](https://poppify.ai/research/instagram-reel-ideas-restaurant), [food trucks](https://poppify.ai/research/instagram-reel-ideas-food-truck) and [dessert shops](https://poppify.ai/research/instagram-reel-ideas-dessert).

## What's inside

| Component | Purpose |
|---|---|
| **MCP server** (`https://poppify.ai/mcp`, HTTP) | Twelve tools, one meaning each: `get_capabilities`, `start_session`, `get_session`, `search`, `suggest`, `generate`, `edit_session` (the ONE way to change a reel), `render`, `publish` (post now / schedule to connected channels), `account` (wallet, portfolio, channels, reels), `add_media`, `submit_feedback`. Most take exactly one branch key — `generate({image:{…}})`, `search({music:{…}})`. |
| **`/poppify:make-reel`** slash command | Guided session flow — photo-led or topic-led entry, free customization loop, paid confirm. |
| **`/poppify:troubleshoot`** slash command | Symptom triage when a render came out wrong. |
| **`/poppify:verify-render`** slash command | Optional (shell + ffmpeg): download + ffprobe + frame-extract verdict on a finished MP4. |
| **`poppify-build-reel`** skill | The canonical photo-led / topic-led flow — when to use which tool, where the free vs paid boundaries are. |
| **`poppify-text-card`** skill | Render a pixel-perfect text card (terminal frame, code, stat callout, headline) locally via HTML/CSS + a headless browser, cross-platform. Shell-capable clients only; shell-less clients let the composer draw the caption. |
| **`poppify-live-motion`** skill | Veo live-motion prompting playbook — plain subject animation AND first/last-frame transitions (composition-locked end frames, journey overridePrompt, failure modes). |
| **`poppify-render-debug`** skill | Optional (shell + ffmpeg): download the finished MP4, run ffprobe, extract frames, surface a verdict. |
| **`poppify-troubleshoot`** skill | Decision tree: symptom → root cause → action for missing audio, wrong colors, dropped captions, stuck renders. |
| **`poppify-schema-introspect`** skill | How to verify the deployed MCP schema when a parameter looks silently dropped. |
| **`poppify-schedule-optimizer`** skill | Engagement-optimized publishing — `recommendedSlots` (real engagement history vs platform norms), `scheduledAt:"best"`, slot assessment, multi-post spacing. |

## Install

In Claude Code:

```
/plugin marketplace add Poppify/poppify-claude-plugin
/plugin install poppify@poppify
```

That's it. After install:

1. `account({register:{}})` (optionally `{ label: "claude" }`) mints a wallet and returns an `apiKey` + a `signupBonusUrl` (50 free seeds, +25 per connected social account across 4 platforms → up to 150 — claim before paying).
2. Use the `poppify-build-reel` skill (Claude will auto-invoke when you ask it to "make a reel") to drive the rest.

## What does it cost?

- **MCP install**: free
- **All non-generation tools** (search, suggest, edit_session, get_session, account — register, wallet balance / top-up / link, portfolio list/switch — and publish + schedule): **free**
- **`render`**: 1 seed base
- **`generate {image}`** (Gemini): 5 seeds per image
- **`generate {music}`** (ElevenLabs Music): 5 seeds per track
- **`generate {narration}`** (ElevenLabs Voice): 5 seeds per batch
- **`generate {clip}`** (image-to-video): 10 seeds per live clip. Animates the subject *inside* a still (blink, breath, micro-gesture); on a live slide the clip supplies ALL the motion, camera included — no FFmpeg camera move is layered on it. On a **selling** reel (product, local business, app promo, brand identity) the moving treatment is the RECOMMENDATION, offered first with its price, and the 1-seed stills render is the cheaper alternative — `render` refuses with `motion_decision_unrecorded` until the choice is on record. On any other reel it stays an optional upgrade after the baseline. Cache hits via `search {clips}` are free.

Seeds are sold at $5.99 for 100 seeds (standard pack) or $0.50 for 5 seeds (mini trial pack). 50 seeds are granted free on signup, plus 25 for each connected social account across 4 platforms — 150 in total, not 150 for one account.

## Generation as a workflow step

Generation is never the destination — it fills in what the library can't, *inside* a reel session. Always search the library first (free); generate only when there's no good match:

- **`search {images}`** / **`search {music}`** — search the existing royalty-free library first. FREE. Matches at score ≥ 40 generally beat fresh AI generation.
- **`generate {image}`** — fill a slide with a Gemini Imagen still, 5 seeds. Workshop the prompt free via `suggest({image:{}})` first.
- **`generate {music}`** — add an ElevenLabs Music track to the reel, 5 seeds. Workshop via `suggest({music:{}})` (free) first.
- **`generate {narration}`** — narrate slides via ElevenLabs Voice, 5 seeds per batch. Pick a voice free via `search {voices}` first.

Generated assets persist to your asset library, so they're reusable across future reels and discoverable on later searches.

## Manual install (without the plugin)

If you only want the MCP and don't want the skills:

```
claude mcp add --transport http poppify https://poppify.ai/mcp
```

You'll get the same tool surface, but Claude won't have the pre-loaded knowledge about when to call which tool or how to verify the finished video.

## Updates

The plugin uses semantic versioning. To get updates:

```
/plugin marketplace update poppify
```

Skill content evolves as the MCP surface evolves — we publish new versions when a tool surface changes meaningfully.

## Support

- **Bug reports / feature requests**: file via `submit_feedback({ apiKey, ... })` from inside any Claude session — the feedback flows directly to the Poppify team's triage queue.
- **GitHub Issues**: https://github.com/Poppify/poppify-claude-plugin/issues
- **Web**: [poppify.ai](https://poppify.ai) — the AI reels maker and video generator
- **MCP setup**: [poppify.ai/mcp](https://poppify.ai/mcp) — install in Claude, ChatGPT, Cursor or any MCP client
- **Research**: [poppify.ai/research](https://poppify.ai/research) — cost analysis, platform benchmarks, reel formats

## License

MIT — see [LICENSE](./LICENSE).
