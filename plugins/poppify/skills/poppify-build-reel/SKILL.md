---
name: poppify-build-reel
description: Canonical photo-led / topic-led flow for the Poppify MCP. Use whenever the user wants: a reel, short video, vertical video, Instagram reel, TikTok video, TikTok, YouTube Short, YouTube Shorts, Facebook reel, FB reel, 15-second video, 30-second video, 60-second video, photo slideshow, photo to video, animate photos, photo animation, slideshow video, social media video, content for social, brand video, product reel, ad creative for social, before/after reel, transformation video, story reel, hook video, or any vertical short-form video for IG/TikTok/YT/FB. Covers the free customization loop and the single paid confirm step. Base render = 1 seed (~$0.06). 50 free seeds on signup, +25 per connected social account across 4 platforms (up to 150). Use poppify-troubleshoot if the render comes out wrong; poppify-render-debug to verify the finished MP4.
---

# Building a Poppify reel — the canonical flow

Poppify is FREE for everything except `render` (1 seed base render) and `generate` (5 seeds each for AI image / music / voiceover; `generate {clip}` is 10 seeds per clip). You can iterate the configuration **infinitely** before render and not spend anything.

> **Tier awareness — check what's doable first.** Not every Poppify connector exposes AI generation. Before using `generate {image}`, `generate {clip}`, `generate {music}`, `generate {narration}`, or `account {voice_clone}`, confirm they exist — call `get_capabilities` (it reports only what *this* tier can do) or check the tool list. If they're absent (the **composer tier**), build entirely from the user's own photos + `search {images}` / `search {clips}` / `search {music}`; never assume a generator exists.

> **Work from the DECK VIEW, by asset id — never by URL.** Every session response ends with a deck view: the shot list in order, each shot's asset id and filename, its flags, the music, what is *not* in the reel, and a version. Every piece of media the session has seen has a short, stable id — `P` photo, `V` uploaded video, `L` live clip, `G` generated image, `T` text card, `M` music, `N` narration. A deck view looks like this (abridged):
>
> ```
> DECK v7 — 4 shots, ~39.3s. #n = slideIndex. Edit by asset id; pass expectedVersion:7.
> #0 P4 reels1.jpg [cover · pin:first · no-caption · whole] 3.0s
> #1 P1 IMG_1001.jpg "Autumn in the garden" 3.5s
> #2 P3 IMG_1003.jpg large:L2/2 "Book a consultation" 4.5s
> music: M2 «Quiet Luxury» rendered v5
> not in reel: P5 example.png reference_only; M1 auto-picked
> ```
>
> - **Address media and shots by id** (`asset:"P4"`, `audio:{source:"library", assetId:"M2"}`), not by signed URL — URLs rotate on every read and re-pasting them is how shots get swapped by accident.
> - **Pass `expectedVersion`** (the N in "DECK vN") on every edit. If the deck changed since you read it, the edit is refused with `deck_stale` and nothing is applied — you get the current deck back to re-decide against. Your own earlier edits in the same turn never make the next one stale. Omitting it still works, with a warning.
> - **Send only what changes.** A music-only turn sends `audio`, never `slides[]`; moving one shot is `edit_session({commands:[{slide:{action:"move", asset:"P4", to:"first"}}]})`, not a re-sent deck. Several edits → `edit_session({commands:[{slide:{…}}, {slide:{…}}]}) (one {slide} command per op)` in one call.

## Step 1 — Mint a wallet (one-time, free)

If the user hasn't registered yet:

```
account({register:{}})                       // optional: { label: "claude" } for provenance
```

Returns `apiKey` and `signupBonusUrl`. **Surface the signupBonusUrl** — opening it and signing in with Google grants 50 free seeds — and connecting social accounts earns +25 each across 4 platforms, 150 in total (≈ 50 base renders, or ~3 fully-loaded reels WITH AI image + AI music + AI voiceover at ~16 seeds each). Don't ask the user to pay before they've claimed this.

Store the `apiKey` — every subsequent call needs it.

## Step 2 — Start a session

> **Follow `playbook` when a response carries it.** Session start, `get_session view:"plan"` and
> `edit_session {concept}` may return `playbook: {domain, version, text}`: the approach that got reels
> of this kind (a product ad, a property tour, …) downloaded and posted, measured on real
> outcomes and updated server-side. Plan by it. The user's explicit instructions still win.
> Domain advice lives there rather than in this skill, so it never goes stale here.

**Photo-led** (user has photos already):
```
start_session({photos:{
  apiKey,
  userWords: "...",         // REQUIRED — their brief VERBATIM, never re-worded. See below.
  photos: [...],            // data: URLs or http(s) URLs, 1–10
  goal: "educate" | "sell" | "connect" | "prove" | "entertain",
  audience: "...",          // optional but biases narrative meaningfully
  theme: "...",             // optional free-text intent
  platform: "instagram" | "tiktok" | "youtube_shorts" | "facebook",
  aspectRatio: "9:16" | "16:9",  // OPTIONAL — otherwise the photos decide. See below.
  aspectRatioFromUser: true,     // ONLY when THEY asked for it. Never a default.
  motionDecision: "live" | "cinematic",    // ONLY when their words say
  narrationDecision: "spoken" | "silent"   // ONLY when their words say
}})
```

Returns: slides[] (each with `copy` — the shot's ONE committed line), caption, hashtags, callToAction, picked recipe, and `runtimeNote` (the runtime to quote).

> **One line per shot.** The copywriter writes a short and a full version of every line; the session commits each shot to ONE of them at creation — the full line for few shots, the short one for many, a mix in between, aiming at a 20–30s reel. `slides[].copy` is that line, and it is everything at once: it sets the shot's length whether or not it is drawn, it is the caption when captions go on, and it is what `generate {narration}` speaks. Present `copy` to the user (never `voiceoverShort`), and quote `runtimeNote` — it is computed from the same line, so it is the length that renders. Rewriting a line with `set_text` changes that shot's length; say the new runtime when you do.

> **Which brand — name it once, at the start.** A linked wallet with 2+ portfolios gets
> `portfolio_required` from `start_session`: ASK THE USER which brand (from
> `account({portfolio:{action:"list"}})`), then pass `portfolioId` to `start_session`. That brand
> sticks to the reel — its logo watermark, the post it files, and the channels `publish` offers.
> `render` does not ask again. Do NOT `portfolio:{action:"switch"}` to make a reel for another
> brand: switching changes their wallet-wide default. A `portfolio_mismatch` from `render` only
> happens when the session inherited a brand silently; it is a question for the user, not an error.

**Topic-led** (no photos, brand or topic input):
```
start_session({apiKey, portfolioId, topic:{userWords, topic, audience, goal, aspectRatio}})
// `userWords` is REQUIRED here too — see below. `portfolioId` only for a multi-brand user (above).
// NOTE: no `platform` here — the topic schema does not declare it, so it is
// silently dropped. Only start_session {photos} accepts it.
```

> **`userWords` is REQUIRED on both entry calls, and it is their message verbatim.**
> `topic` / `theme` is your paraphrase, and the paraphrase is where constraints die. The
> server reads `userWords` — not the paraphrase — for the stated runtime, for whether this
> reel sells something, and for a claimed attachment. Omitting it fails schema validation;
> re-wording it loses the brief to every step after it. Paste what they wrote.
>
> If their brief says images were supplied and none arrived, the session is refused with
> `attachment_claimed_but_missing` BEFORE it exists. Ask for the image — do not generate a
> stand-in from the text, and do not strip the claim out of `userWords` without telling them
> the visuals will be approximations.

**Aspect ratio is a SESSION property.** Photo-led sessions take it from the photos
(landscape photos → 16:9) unless you pass `aspectRatio`; topic-led sessions default to
`9:16`. Everything downstream inherits it: `generate {image}` stills, live-motion clips,
library search/match, and the render canvas. If the user later asks to change it ("make it
vertical for mobile"), **change it** with `edit_session({sessionId, commands:[{patch:{aspectRatio:"9:16"}}]})`
— the response echoes the stored value and the crop it costs (`orientation.note`); relay that
before they pay. Never tell the user it changed without that call. Don't mix orientations: a
16:9 still in a 9:16 session gets cropped/letterboxed, and `generate {image}` will warn.

Returns 5 concept options. Pick one with `edit_session {concept}`. **A topic-led session starts with NO images** — every slide's `imageUrl` is empty. Every shot needs its own visual before `render` — otherwise confirm refuses BEFORE charging (`slides_missing_images`, naming the empty shots). The free fixes come first: remove the extra beats, or place one of their photos / a library image. The `recipeDistribution` field shows which recipes the 5 concepts span; if they collapsed off-brief (e.g. you wanted a tribute/hype angle but got all confessional), call `start_session {topic}` again with an explicit `recipe` parameter (`get_capabilities({recipes:{}})` for IDs).

### Decide FIRST: one image, or one per beat?

Before generating anything, ask whether **one image can carry the whole reel**. For a single-subject / hero / cinematic reel (recipe `visualType: "hero_image"`), it usually can — the camera motion and the changing captions ARE the variety; the image stays the star. Generating four images for four beats is the wrong default — it costs 4× the seeds AND drifts the subject's identity across slides.

- **One image across all beats** — the 1-seed ALTERNATIVE, not the recommendation: `generate {image}` once, then `set_image` the SAME asset id on every slide. Keep ONE `videoEffect` + `continuousEffect` on so the camera makes one continuous move (see Gotchas). 5 seeds total for imagery. When every shot is the same upload the server offers a take generated FROM that photo, cut 2–5 ways, for 10 seeds — on a selling reel lead with that and keep the continuous camera move as the cheaper option. Measured: single-photo reels were downloaded 35% of the time against 62% for two or more.
- **One image per beat** (only when beats are genuinely distinct scenes — before/after, multi-step, comparison): generate/search per slide. N × 5 seeds.

## Step 3 — Refine (FREE, unlimited iteration)

The single most efficient call here is **one `edit_session` with several commands** — per-slide text as `{slide}` commands, then ONE `{patch}` with music + production knobs + textColor + per-slide motion, in ONE round-trip:

```
edit_session({
  sessionId,
  expectedVersion: 7,                      // the N in "DECK vN" — see the deck-view note above
  commands: [
  // Per-slide caption text. Setting text is what turns a slide's caption ON
  // (captions are opt-in); empty string = a shot left blank ON PURPOSE.
  { slide: { action: "set_text", slideIndex: 0, newText: "Your literal slide 1 caption" } },
  { slide: { action: "set_text", slideIndex: 1, newText: "" } },   // deliberately no caption (e.g. text baked into the image)
  { slide: { action: "set_text", slideIndex: 2, newText: "Book a consultation\nexample.com" } },
  { patch: {
  slides: [{ index: 2, heroLine: 1 }],     // patch.slides carries ONLY language + heroLine (which line renders LARGE, 1-based)
  // Production knobs
  aspectRatio: "9:16",                     // change orientation mid-session (response states the crop)
  textColor: "#FFFFFF",                    // hex; overrides recipe palette
  accentColor: "#88beb4",                  // second brand colour: the rule / highlighted word
  textAnimation: "editorial",              // editorial | lower_third | karaoke (position is baked in)
  font: "Georgia",                         // a font the USER named → nearest caption style; relay font.note
  videoEffect: "push_in",                  // session-wide motion (canonical: push_in, pull_out, lateral_pan, vertical_pan, focus_pull, epic_parallax, static)
  audioMood: "uplifting",
  // NOTE: no SESSION-level `duration` knob. Per-slide length is resolved as:
  // voiceover audio ALWAYS plays in full; a live clip plays in full BY DEFAULT
  // but an explicit set_duration deliberately trims it. Then set_duration (any
  // slide, capped 2–15s captioned / 0.5–15s uncaptioned) or the length
  // of the shot's committed line (slides[].copy, drawn or not) drive the rest;
  // 4s for a deliberately wordless shot. To change runtime: rewrite lines, use
  // set_duration on any slide, or add/remove slides.
  // Per-slide motion overrides (takes precedence over session-wide — but is IGNORED entirely while `continuousEffect:true`, which drives one curve across the whole run)
  slideEffects: [
    { slideIndex: 3, videoEffect: "focus_pull" }  // end card → minimal motion
  ],
  // Music attach (free — library audio is resolved to a playable URL here)
  audio: { source: "library", assetId: "..." }
  } }
  ]
})
```

If you'd rather iterate one edit at a time, send one command per call (pass `expectedVersion` on each):
- `edit_session({commands:[{slide:{action: "set_text", asset: "P1", newText}}]})` — literal caption on the shot showing P1 (or `slideIndex`)
- `edit_session({commands:[{slide:{action: "set_image", slideIndex, asset: "P4"}}]})` — put a registered asset on a shot
- `edit_session({commands:[{slide:{action: "move", asset: "P4", to: "first"}}]})` — move ONE shot; everything else keeps its order
- `edit_session({commands:[{slide:{…}}, {slide:{…}}]})` — consecutive slide commands apply all-or-nothing (indexes = the deck as it is now)
- `edit_session({commands:[{patch:{audio: { source: "library", assetId: "M2" }}}]})` — music by id (library ids work too)
- `edit_session({commands:[{patch:{...}}]})` — production knobs (one knob per call works fine)
- `edit_session({commands:[{slide:{action:"add", slideIndex, imageUrl, newText}}]})` — insert a slide (`remove` takes one out)

**Search the library FIRST** before generating:
- `search({apiKey, mine:{limit}})` FIRST — the user's own library: every image, text card and Live Motion clip they already paid for. Reusing one is free. `visualType:"live_motion"` narrows to clips; `cursor`/`nextCursor` page through a big library. Spending 5 seeds to regenerate something they already own is the most common avoidable cost in the product.
- `search({apiKey, images:{keywords, limit}})` for images (keywords = string or array: subject + mood + scene) — score ≥ 40 should beat AI gen
- `search({apiKey, music:{mood, genre}})` for music

### Record what the user says about their assets (FREE) — the server holds you to it

When the user says what something IS or how it must be treated, write it down with
`edit_session({commands:[{asset:{action:"set"}}]})` the moment they say it. The server then enforces it on every later
edit and before `render` — so a later turn cannot quietly undo it:

```
edit_session({sessionId, expectedVersion, commands:[{asset:{action: "set", asset: "P4", attrs: { role: "cover" }}}]})
//   "reels1.jpg is the cover" → pinned first, no caption, and no edit may move it or add text
edit_session({sessionId, commands:[{asset:{action: "set", asset: "P5", attrs: { role: "reference_only" }}}]})
//   "that screenshot is only an example" → it can never be placed as a shot
edit_session({sessionId, commands:[{asset:{action: "set", asset: "P4", attrs: { fit: "whole" }}}]})
//   "don't crop it / show the whole image" → rendered uncropped (banded), not cover-cropped
edit_session({sessionId, commands:[{asset:{action: "reject", asset: "M3"}}]})
//   "not that track" → it cannot come back until she asks for it
edit_session({sessionId, commands:[{asset:{action: "set", asset: "M2", attrs: { label: "first track" }}}]})
//   your note in her words, so "that one" can be found again
```

- **Tightening is yours to record** (pin, reject, cover, reference_only, `caption:none`, `fit:whole`). **Loosening is hers** (unpin, restore, text back on a no-caption shot, `fit` away from whole): the refusal carries a `question` to put to the user; third-party clients pass `userAsked:true` only when the user asked for it in their own words.
- **"The first music / the original photo"** is the one with the EARLIEST render (`rendered vN` in the deck view), not the lowest id — an `auto-picked` asset that was replaced before anything rendered was never heard by the user.
- **Her logo** goes to her brand profile with `account({sessionId, portfolio:{action:"set_logo", asset:"P9"}})`. It changes her account, so it asks her first. The renderer stamps it on every reel as a **small round badge in the bottom-right corner** (a wide logo is cropped to its centre) — tell her exactly that; it is not a shot and cannot be moved or resized. Don't rebuild it as a text card.
- **A font she names** → `edit_session({commands:[{patch:{font:"Georgia"}}]})`. Custom fonts aren't supported: it maps to the nearest caption style and `font.note` says which — relay it plainly, never as "Georgia (or close to it)".
- **A copy question** (`copy_replacement_needs_confirmation`): the rest of the patch applies and only the shot texts wait (`partiallyApplied`, `pending.lines`). Tell her both halves — never describe the pending lines as already on the reel.

## Step 4 — Generate AI assets only when needed

These cost 5 seeds each. Always workshop the prompt for free first.

**Every call that charges takes `spendApproved: true` — and is refused without it.** Tell the user what you will make and what it costs ("one hero image, 5 seeds"), wait for their yes, then make the call with `spendApproved: true`. It is your on-the-record statement that they agreed to THIS spend; never set it pre-emptively. Without it the call returns `status: "spend_not_consented"` before any seed moves. (On the Poppify web chat the flag is ignored — the user's own reply is recorded server-side and decides.) `suggest({live_prompt:{dryRun:true}})` is free and needs no flag.

```
suggest({apiKey, sessionId, image:{slideIndex}})  // FREE — pass sessionId+slideIndex
                                                 //   for the slide's composer plan (or subjectDescription when no session)
generate({apiKey, sessionId, spendApproved: true, image:{prompt, visualStyle}})  // 5 seeds — after their yes

// PHOTO-LED SESSIONS GATE THIS. If the session has uploaded photos, a
// reference-free call is refused BEFORE charging, with `reference_required`.
// Pass one of:
//   referenceAssetIds: [...]     // up to 8 (compose: 2-3; collage: all of them), from search {mine} / the session
//   referenceImageUrls: [...]    // up to 8
//   referenceSlide: <index>      // reuse a slide's existing image as reference
//   ignoreSessionPhotos: true    // deliberately generate unrelated to their photos
// so the generated scene matches the user's own shots instead of drifting.
// allowTextInImage: true only when you genuinely want baked-in typography —
// otherwise use generate {text_card}, which is exact and free.
//   Pass sessionId so the still inherits the session's aspect ratio (vertical by
//   default). The render canvas is fixed to the session aspect, so a still that
//   doesn't match it is cropped — passing sessionId keeps them aligned.
// The new image is registered in the session with an id (G1, G2 … — see the deck view).
// Attach via edit_session({commands:[{slide:{action:"set_image", slideIndex, asset:"G1"}}]})
//   — several at once: one {slide} command each, in the same edit_session call for several beats.
//   For a single-image reel, set_image the SAME id on every slide.

suggest({apiKey, music:{userInput}})     // FREE — userInput = natural-language music description
generate({apiKey, spendApproved: true, music:{prompt, durationSeconds}}) // 5 seeds, returns URL (default 30s, max 300s)
// Then attach via edit_session({commands:[{patch:{audio:{source:"user_url", url}}}]})

search({apiKey, voices:{}})                          // FREE voice catalog
generate({apiKey, sessionId, spendApproved: true, narration:{voiceId}}) // 5 seeds per batch — speaks each shot's committed line
// With sessionId, omit `scripts`: narration says what the shot says. Passing different
// words is refused before any charge (narration_text_mismatch) — set_text the shot first.
```

## Step 5 — Verify, then confirm

> **Read the render manifest's `contradictions` before you quote a price.** `blocking` ones
> refuse the render and name the fix. `notice` ones do not block but require you to SAY
> something first — in particular **`fewer_shots_than_scenes`**: they described N scenes and
> the deck has fewer. Condensing is often right (their photos ran out, two scenes are one
> shot), but say so and say why in one line BEFORE rendering, and if it is short of their own
> media ask for the missing photos by number. A reel that quietly drops a third of someone's
> storyboard reads as the product ignoring them. The other codes: `script_reaches_nobody`,
> `slide_has_no_image`, `requested_runtime_ignored`, `caption_style_draws_nothing`,
> `stored_duration_stale` (quote the projection, never the stored value).

Use `get_session({ sessionId })` to see the seed total — pre-confirm it returns the exact price breakdown. **Render only when the user asked for it in this message, or said yes to the price you just quoted.** A correction, a question or a complaint is never a go-ahead: fix or answer it, say in one line what changed, and ask "Render now? (1 seed)". If they said "don't render", don't end your reply by inviting one either. Then:

```
render({ sessionId, apiKey, buyerEmail })
```

Charges seeds. Render typically completes in 30–120s. Poll:

```
get_session({ sessionId, apiKey })
```

When `status === "complete"`, you get a `videoUrl` (signed GCS URL, valid ~7 days — `videoUrlExpiresAtIso` in the response has the exact expiry). Hand it to the user right away and tell them to save it before it expires; on shell clients also `curl` a local copy as the durable backup. Don't tell the user "we emailed it" — Poppify does not email rendered reels; the URL is the only delivery surface.

## Step 6 — Live Motion (the RECOMMENDATION on a selling reel; an upgrade on everything else)

Live Motion animates the **subject inside a still** (blink, breath, micro-gesture, a small action) using image-to-video. On a live slide the clip supplies **ALL** the motion, camera included — the renderer applies no FFmpeg camera move to it, because zoompan over an already-moving clip over-zooms and discards its composition. Put any camera move in the prompt; still slides keep their cinematic motion.

**Which treatment you offer FIRST depends on the reel's job, and the server decides, not you.**

- **A reel that SELLS something** — a product, a local business, an app, a brand — leads with the MOVING treatment. Quote it first *with its price*, and offer the 1-seed stills render second, as the cheaper alternative. `render` **refuses before charging** with `motion_decision_unrecorded` until either a live clip is on the deck or the user has been offered live motion and said no. Do not plan to "render the baseline and offer live after" here: that is the refusal.
- **Any other reel** — explainer, personal, story — keeps the old shape: cinematic baseline first, user reviews, then offer the upgrade on the slides that earn it.

You do not have to classify this yourself. Read the `nextSteps` block on any session response: when the recommended tool is `generate {clip}` or `suggest {live_action}` and its `why` says the reel sells something, that is a selling reel and the order is already decided.

### Answering the refusal

`motion_decision_unrecorded` returns a `question` block whose options are keyed **`1`** (ship the stills, 1 seed) and **`2`** (make the live take, +10 seeds). It sets `noDefault`, so **a bare "yes" is not read as an answer** — the question is re-asked. Put both options and both prices to the user in one line and relay their key, or a phrase that names a side ("camera motion is fine", "do the live take"). On the Poppify chat their reply is read server-side. On a third-party client, record a decline as `render({ liveMotionDeclined: true })` — your statement, on the record, that they chose camera motion — and **never in the same turn you ask**.

> **For before/after transformations (`endFrameUri` first/last-frame interpolation), invoke the `poppify-live-motion` skill first** — bridged renders need a composition-locked end frame and an authored journey `overridePrompt`; the auto prompt is wrong for that mode.

When the user wants it (same order as the server instructions' lifecycle):
1. `suggest({sessionId, live_action:{slideIndex}})` (FREE) → pick a motion verb with the user.
2. `suggest({sessionId, live_prompt:{slideIndex, liveAction}})` (FREE) — preview the exact Veo prompt; iterate until it reads right.
3. `search({apiKey, clips:{imageHash?, actionKeywords:<finalized action>, durationSeconds}})` — cache hits (score ≥ 60) attach for **zero seeds**.
4. `edit_session({commands:[{slide:{action:"set_motion_mode", slideIndex, motionMode:"live", liveAction:"<verb>", liveDurationSeconds:<4|6|8>}}]})`.
5. `generate({sessionId, spendApproved: true, clip:{slideIndex}})` — **10 seeds** per clip, after they said yes to that price (capped 8s), or free on a cache hit. ~30–90s wall-clock.
6. `render` again to re-render with the live slide.

### One take cut N ways beats N clips

If a session response or `suggest {live_action}` carries a **`stitchTheirPhotos` / `stitchOffer`**, THAT is the offer: one continuous take of their subject cut 2–5 ways — real footage — for the same **10 seeds**, not one clip per shot at 10 seeds each. Quote its `headline` and `pitch` verbatim and do not shrink it to "+10 seeds on shot 1"; an offer you paraphrase is an offer the user never got. The single-hook upgrade is the fallback rung, not the headline.

Absent a stitch offer, recommend **at most one** live slide, usually the hook (slide 0) — a living subject in the first frame stops the scroll. Quote the planner's per-slide score to justify the pick.

### Close the turn on the render offer

After a paid clip lands, `generate {clip}`'s own `nextStep` says to end the turn on `render({sessionId})` **with the price in it** — 1 seed on top of the 10 the clip just cost. Do not end on "how does the movement feel?" or any other bare aesthetic question: the measured failure is 10 seeds spent and no reel.

## Step 7 — OPTIONAL: publish or schedule (linked accounts only)

Rendering and publishing are separate. `render` produces the MP4 and files a `ready` post in the user's Poppify portfolio; `publish` is what sends it to social channels. Both `publish` and `account {portfolio}` are FREE.

Preconditions, in order:
1. **Wallet linked** to the user's Poppify app account: `account({wallet:{action:"link"}})` (QR / code). Channels live on the app account.
2. **Channels connected** — `account({channels:{action:"list"}})`. To add one, `account({channels:{action:"connect", platform}})` returns a one-use sign-in link (15 min) to give the user; when they say done, `account({channels:{action:"status", requestId}})` → `connected`, or `selection_required` with the accounts to choose from → `account({channels:{action:"select", platform, accounts}})`. Removing a channel (`remove`) needs the user's yes (`confirmed:true`). `account({portfolio:{action:"list"}})` shows portfolios and their channels. **A reel posts only to the channels of the brand it was made for** — `publish` lists exactly those as `availableChannels` and refuses any other. If that brand has none, `publish` returns `no_channels` with the connect path — a channel connected with the reel's `postId` joins the reel's brand. A finished reel cannot change brand: to post to another brand's channels, make it again under that brand (`start_session` with that `portfolioId` — one render). `account({portfolioId, portfolio:{action:"switch"}})` changes only the wallet-wide default for NEW sessions.

Flow after `get_session` returns `complete`:

```
publish({ apiKey, postId })                                  // no channelIds → returns availableChannels + recommendedSlots
publish({ apiKey, postId, channelIds })                      // PREVIEW — returns status:"confirm_required", publishes nothing
publish({ apiKey, postId, channelIds, confirmed:true })      // post NOW (queued; worker publishes within minutes)
publish({ apiKey, postId, channelIds, scheduledAt, confirmed:true })  // schedule (ISO, future, before the ~7-day video expiry)
```

**`confirmed:true` is required or nothing is published.** A call without it
returns `status:"confirm_required"` and a preview of the caption, channels and
time — that is the design, not an error. Show the user that preview, get a
real yes, and only then repeat the SAME call with `confirmed:true`. Never send
both in one breath: a wasted seed can be refunded, a wrong caption in front of
an audience cannot. If you find yourself calling this repeatedly and getting
`confirm_required` each time, you are missing the flag — do not report success.

`postId` comes from the `render` response (preferred — survives session expiry); `sessionId` also works while the session is alive. **Always show `availableChannels` and let the USER pick** — never auto-select where their content goes. Re-calling reschedules: already-published channels are preserved, deselected unpublished ones are dropped. The user can move or cancel scheduled posts in the Poppify app calendar.

**Scheduling for engagement/reach:** the no-channelIds response also returns `recommendedSlots` — the account's best posting times from its real engagement history (platform norms for new accounts; hours are UTC). Pass a slot's `nextOccurrence` as `scheduledAt`, or `scheduledAt:"best"` to auto-pick the top slot; scheduling responses include a `slotAssessment` ranking the chosen time. For the full playbook (basis handling, sample-size honesty, multi-post spacing), invoke the **`poppify-schedule-optimizer`** skill.

## Gotchas worth knowing

- **Don't burn seeds on text-heavy slides.** Gemini Imagen garbles literal text (terminal frames, install commands, stat callouts). For those call `generate({apiKey, sessionId, text_card:{slideIndex, text}})` — server-side, ZERO seeds, works in every client including shell-less ones. Only when the design needs pixel control (terminal frame, multi-line code) fall back to the local render in the **`poppify-text-card`** skill.
- **Single-image reel → ONE continuous camera move.** When one image carries all slides, keep a SINGLE `videoEffect` and set `continuousEffect: true` (default `false` — you must set it). The renderer then makes one continuous move across the whole reel via a global frame offset. **Assigning a DIFFERENT effect per slide on a same-image run disables continuous smoothing** — each slide gets its own independent move and the motion visibly resets at every cut. Only use per-slide `slideEffects` when the slides have *different* images.
- **On-screen captions are OPT-IN.** Each shot's committed line (`slides[].copy`) times the shot and is what narration speaks; nothing is drawn on the picture until `edit_session({commands:[{slide:{action:"set_text", slideIndex, newText}}]})` sets it (one `{slide}` command per shot — caption text never goes inside `patch`). A deck with a script and no captions renders wordless — set the text you want shown. **Re-sending the copywriter's own line does not draw it**: it stays the script and the response carries `captionNotDrawn`. Show the user the lines; if they want them on screen as written, send the same `set_text` with `force:true`; if they want other words, send those (new words draw without `force`). Empty string = this shot left blank on purpose (allowed even when every other shot is captioned).
- **Slide duration: two DRIVERS + two MEDIA FLOORS, no global control.** (1) Attached **voiceover** audio is an UNCONDITIONAL floor — nothing truncates it. (2) A rendered **live-motion clip** plays in full *by default*, so an 8s morph slide holds all 8s under a short caption (you do NOT pad the caption) — **but an explicit `set_duration` deliberately TRIMS it**, so a short live clip can be an edit rather than a bug. Drivers: (3) **EXPLICIT** `edit_session({commands:[{slide:{action:"set_duration", slideIndex, duration:N}}]})` on ANY slide — overrides text-length, capped **2–15s on a captioned shot and 0.5–15s on an uncaptioned one** (a fast cut is a real ask); (4) **TEXT-LENGTH** `(words/2.6)*1.2` of the shot's committed line, whether or not it is drawn; 4s for a deliberately wordless shot. Lengthen a slide: write MORE text OR use set_duration. `edit_session({commands:[{patch:{duration}}]})` is silently STRIPPED (not in the schema, so no error comes back) — no session-level control. **Use text** for normal captioned slides; **use set_duration** for text-baked cards or any precise hold.
- **Voiceover auto-detaches when text changes.** The shot's line IS the voiceover script — generate {narration} speaks exactly `slides[].copy`. `edit_session({commands:[{slide:{action:"set_text"}}]})` on a slide with attached voiceover detaches it (old audio of wrong words). Call `generate {narration}` ONLY after text is finalized — otherwise you waste 5 seeds per text edit.
- **Images with text already baked in (her cover, terminal screencaps, end cards)**: place the image, then record `edit_session({commands:[{asset:{action:"set", asset, attrs:{caption:"none"}}}]})` (or `role:"cover"`, which implies it) — or at least `set_text` with `newText:""`. Never put placeholder text (a space, a dot, a slogan) on a shot the user said to leave blank. Hold it with `edit_session({commands:[{slide:{action:"set_duration", slideIndex, duration:N}}]})` — set_duration works on any slide, so you no longer have to blank the caption first just to control the hold. Blank slide with no explicit duration falls back to 4s. **But not as long as you want:** a still held past ~6s is refused before charging with `still_held_too_long` (a still may run as long as its caption needs to be read, plus at most 6s beyond that; live clips are exempt). The repair is to split the time across more shots rather than stretch one picture. If the user genuinely asked for a long hold, third-party clients record that as `render({ longHoldsIntended: true })`.
- **Sceneboard recipes auto-lock motion across all panels** — per-slide variation is ignored when visualType is sceneboard.
- **Library audio resolves URLs at attach time** — if `edit_session({commands:[{patch:{audio:{source:"library", assetId}}}]})` errors with "asset not found", pick a different `assetId` from `search {music}`. Once a track has been in the session it has an `M` id — put it back with `audio:{source:"library", assetId:"M2"}`.
- **Which caption line renders large** (editorial / lower_third): the renderer picks the hero line itself and never picks a URL, domain or @handle. When the user says which line should be big ("CTA large, site smaller"), set `heroLine` on that slide; the deck view shows `large:Ln/m`. Describe sizes only as the deck view shows them.

## When something looks wrong with the finished video

Invoke the `poppify-troubleshoot` skill. It has the decision tree for common symptoms (wrong colors, missing audio, caption drops, duration mismatch).
