---
name: poppify-troubleshoot
description: Diagnose a Poppify reel that came out wrong. Use when the user says: "the reel came out wrong", "render failed", "no audio in the video", "no music", "captions are missing", "wrong color text", "text is green/blue/etc instead of white", "video URL doesn't open", "video URL expired", "seeds were charged but no video", "render is stuck", "render still loading after 5 minutes", "duration is wrong", "video too short / too long", "image has text baked in", "library search returned nothing", or any deviation from what they asked for. Walks the symptom → root cause → action decision tree.
---

# Poppify render troubleshooting

Find the symptom that matches, then take the suggested action. Most root causes here trace to schema drift, library-asset state, or text/duration mismatches — not random renderer failures.

## Symptom → Root cause → Action

### "The live-motion slide has no sound"

**Most likely**: the clip genuinely has no audio stream. Veo 3.1 always generates audio, but **Seedance and Kling are video-only** — check which provider rendered it (`account {default_provider}` / `get_capabilities.pricing.live_motion.availableModels`). A video-only provider falls back to the ElevenLabs path, so that slide is silent unless you attach narration.

**Also check**: in a same-image run, several slides share one clip at different offsets and the audio is taken **once**, from the slide that starts the run. Later slides in that run are silent by design.

**Not the cause any more**: the composer used to strip the track with `-an`. It no longer does — `VideoGenerator` extracts the clip's audio and mixes it through the voiceover path.

### "Two voices are talking over each other on one slide"

**Root cause**: a live clip's audio now REPLACES a generated voiceover on the same slide, so this shouldn't happen — if it does, the voiceover was attached to a *different* slide number than the live clip.

**Action**: `get_session view:"plan"` and confirm the `voiceoverSlides` index matches the slide carrying `motionMode:"live"`. Never budget `generate {narration}` for a live slide; its audio is already there.

### "No audio in the finished video"

**Most likely**: library audio asset was attached but `resolvedUrl` ended up empty (renderer can only download URLs, not asset IDs).

**Action**: `get_session` does NOT return a session object — it returns `status, videoUrl, signedVideoUrl, price, voiceover, slideCount, errorMessage`. For audio state call `get_session({sessionId, view:"plan"})` and check the resolved soundtrack. If null/empty:
```
search({apiKey, music:{}})                      // get fresh assetIds
edit_session({sessionId, commands:[{patch:{audio: { source: "library", assetId: <new id> }}}]})
render({ sessionId, apiKey })                     // re-render (seeds re-charged)
```

If `resolvedUrl` is populated but audio still missing in the MP4: open `poppify-render-debug` and ffprobe the file — confirm the audio stream is actually absent, not just inaudible.

### "Caption text is the wrong color"

**Most likely**: `textColor` parameter was dropped because the deployed `edit_session {patch}` schema doesn't expose it (schema/code drift bug).

**Action**: invoke the `poppify-schema-introspect` skill to verify. If `textColor` is in the schema but the render still ignored it, check the session via `get_session view:"plan"` (NOT `get_session`, which returns no session object). If the field is missing there, your `edit_session {patch}` call dropped it client-side; re-call with the correct field name and re-`render`.

### "Captions don't appear on some slides"

**Three possibilities**:

1. **Intentional** — `edit_session({commands:[{slide:{action:"set_text", slideIndex, newText:""}}]})` was called on those slides (empty string = composer skips drawtext). Check the slide's text via `get_session({sessionId, view:"plan"})` — if empty, this is the user's earlier patch landing.

2. **Photo-led copywriter trip** — `start_session {photos}` ran but the inline copywriter failed silently and slides[] is empty. Falls back to concept hook + emotionalBeats (single-word labels). **Action**: call `edit_session({sessionId, commands:[{concept:{conceptIndex, feedback}}]})` to retry, then re-render.

3. **The copywriter's own line was echoed back** — `set_text` with exactly the line the session already had keeps it as the script but does NOT draw it (the response says `captionNotDrawn`). Captions are opt-in; a default re-sent is not a request. **Action**: show the user the lines; after their yes, re-send with `force:true` — or send the words they want instead.

### "Caption position is wrong"

**Most likely**: the caption STYLE decides the position — there are three, and position is baked into each. An older style name (typewriter / bold_captions / phrase_reveal) is no longer accepted.

**Action**: pick the style for the look you want:
- bottom serif lockup, quiet / premium → `textAnimation: "editorial"`
- broadcast plate bottom-left, ads / explainers → `textAnimation: "lower_third"`
- centred block, energetic (the TikTok standard) → `textAnimation: "karaoke"`

If the wrong LINE came out large (editorial / lower_third), set `heroLine` on that slide with `edit_session({sessionId, commands:[{patch:{slides:[{index, heroLine}]}}]})`; the deck view shows which line renders large (`large:Ln/m`).

### "A paid call came back `spend_not_consented`"

**Root cause**: the server holds every seed-spending call (`generate {image}`, `generate {music}`, `generate {narration}`, `generate {clip}`, `generate {text_card}` with `backgroundPrompt`) until the user's approval is on record. On third-party clients that record is `spendApproved: true` on the call; nothing was charged.

**Action**: tell the user what you want to make and what it costs, wait for their yes, then re-call with `spendApproved: true`. Do not set it to get past the refusal without asking — it states that they agreed. A plan recorded with `edit_session({commands:[{patch:{plan:{approvedSeeds, steps}}}]})` also counts, within its total.

### "publish doesn't list the channel I want" / "render asks which brand"

A reel belongs to ONE brand (portfolio): the one named at `start_session` (`portfolioId`), or the wallet's active one if none was named. `publish` lists only that brand's channels and refuses others.

- **The channel is on another brand** → a finished reel cannot change brand (its logo is on it). Make it again under that brand: `start_session` with that `portfolioId` (one render; reuse the same assets by id). Do not `account({portfolio:{action:"switch"}})` to fix one reel — it changes the default for every new session.
- **`publish` returned `no_channels` but they have channels** → none are on this reel's brand. Connect one with the reel's id — `account({channels:{action:"connect", platform, postId}})` — and it joins this brand.
- **`render` returned `portfolio_mismatch`** → the session inherited a brand that is no longer the active one. Ask the USER which brand, then `render({sessionId, portfolioId})` (before the first render, this works). Nothing was charged. Naming `portfolioId` at `start_session` avoids the question.

### "Render failed / seeds charged but no video"

**Action**:
```
get_session({ sessionId, apiKey })
```

If `status === "failed"`: the render error is in `errorMessage` (get_session returns no session object). A failed render is not refunded: its charge pays for the next `confirm` of the same session, so the retry costs nothing (the response says what it charged). If a retry is charged again, file via `submit_feedback`.

If `status === "rendering"` for > 5 minutes: the render is genuinely stuck (rare). File via `submit_feedback({ apiKey, sessionId, frictionPoints: ["render stuck in status=rendering for >5 minutes"] })`.

### "I got the video URL but it doesn't open"

**Most likely**: the signed GCS URL expired. TTL is ~7 days (`get_session` returns `videoUrlExpiresAtIso` with the exact time).

**Action**:
```
get_session({ sessionId, apiKey })
```

If `videoUrl` returned but the URL doesn't open: the URL has expired and Poppify doesn't persist videos beyond the ~7-day TTL (cost-control). Re-`render` charges seeds again. Tell the user to save the file within the window next time (shell clients: `curl` a local copy right after render).

### "Video duration is wrong"

**Most likely**: slide length is driven by text length OR an explicit per-slide duration. A reel shorter than expected means the slides have too little text and no explicit duration.

**Action**: two levers — write more text on the short slides (`edit_session({commands:[{slide:{action:"set_text", newText:"longer text"}}]})`), OR set an explicit hold with `edit_session({commands:[{slide:{action:"set_duration", slideIndex, duration:N}}]})` (2–15s captioned, 0.5–15s uncaptioned; works on ANY slide, overrides the text-length formula). There's no session-level duration knob. Note: **voiceover audio is an unconditional floor** and is never scaled down; a live clip plays in full BY DEFAULT but an explicit `set_duration` deliberately trims it. And a still cannot simply be held: past ~6s `render` refuses with `still_held_too_long` — add shots rather than stretching one picture.

### "The live-motion / morph clip is cut short" (e.g. an 8s Veo clip only plays ~2s)

**Most likely**: on older builds the live slide followed the caption's text-length instead of the clip length, truncating the Veo clip. The duration resolver now treats a rendered live clip as a **media floor** (always plays in full), so this is fixed on current builds.

**Action**: if a live clip is still cut short, set an explicit floor with `edit_session({commands:[{slide:{action:"set_duration", slideIndex, duration:8}}]})` on that live slide, then re-render. Do NOT try to fix it by padding the caption — the clip length binds on its own now.

### "The image in slide N looks wrong / has text baked in"

**Most likely**: `generate {image}` was called for a text-heavy concept and Gemini Imagen garbled the literal text into the image, AND composer drew drawtext on top — so the slide has double text.

**Action**:
- For text-heavy slides (terminal frames, install commands, stat callouts, end cards): render text-on-bg locally via HTML/CSS screencap + `add_media {upload}`, uploading with `add_media({sessionId, upload:{...}})` so it is registered in the session with an id, then attach it with `edit_session({commands:[{slide:{action:"set_image", slideIndex, asset:"P7"}}]})` and record `edit_session({commands:[{asset:{action:"set", asset:"P7", attrs:{caption:"none"}}}]})` so no caption is ever drawn over the baked-in text. The free `generate {text_card}` does all of this server-side when the slide is just typography.
- For non-text-heavy slides where AI image is fine: just re-generate with a sharper prompt — workshop it with `suggest({image:{}})` first (free).

### "Library search returned nothing relevant"

**Action**: refine the query. Library scoring weights **Visual Hint Match (tag/keyword)** at 50/100 points — generic queries score low. Use specific keywords from the slide's `copy` or concept hook.

If still nothing > score 40: fall through to `generate {image}` (5 seeds). Workshop the prompt with `suggest({image:{}})` for free before generating.

### "Single-image reel has jerky / resetting motion at each cut"

**Most likely**: different `videoEffect` values were set per slide on a same-image run, which disables continuous-curve smoothing. Each slide then gets its own independent camera move, so the motion visibly resets at every cut instead of flowing as one continuous shot.

**Action**: for a reel where one image carries all slides, use ONE session-wide `videoEffect` (e.g. `push_in`) and set `continuousEffect: true` (default `false` — you must set it) — the renderer then makes a single continuous camera move across the whole reel via a global frame offset. Variety comes from the changing captions, not from per-slide motion. Only assign per-slide effects when slides have *different* images.

### "render() refuses: slides_missing_images / asset_rules_violated / deck_half_written / still_held_too_long / motion_decision_unrecorded"

These refusals happen BEFORE any seed is charged, and each names the shots involved.

- **`still_held_too_long`** — a still is held past ~6s (a still may run as long as its caption needs to be read, plus at most 6s beyond; live clips are exempt). Split the time across more shots instead of stretching one picture. Only if the user actually asked for a long hold: `render({ longHoldsIntended: true })`.
- **`motion_decision_unrecorded`** — a reel that sells something is about to ship as stills with nothing moving, and nothing on record says the USER chose that. Its `question` is keyed `1` (stills, 1 seed) / `2` (live take, +10 seeds) and sets `noDefault`, so a bare "yes" is not an answer. Put both options and both prices to them; third-party clients record a decline as `render({ liveMotionDeclined: true })`, never in the same turn they ask.

- **`slides_missing_images`** — the named shots have no visual of their own. Remove the extra beats (`edit_session({commands:[{slide:{action:"remove"}}]})`), or place one of their photos / a library image by id (`edit_session({commands:[{slide:{action:"set_image", slideIndex, asset:"P2"}}]})`). Generating is one option, not the first.
- **`asset_rules_violated`** — the deck breaks something the user already decided (a pinned cover moved, text on a `caption:none` shot, a reference-only or rejected asset placed). The message says which; fix the deck, don't loosen the decision without asking them.
- **`deck_half_written`** — some shots have a caption and others have nothing decided. For a shot that should stay blank on purpose, `set_text` with `newText:""` (or `edit_session {asset}` `caption:"none"`) records the decision; never put placeholder text on it.

### "Live motion didn't apply / subject isn't moving"

**FIRST, check whose footage it is.** If the shot plays a video the USER uploaded, it is already moving and there is nothing to animate — `generate {clip}` refuses with `already_their_footage` rather than spend 10 seeds replacing their own footage. `get_session` reports `slidesPlayingTheirOwnFootage` separately from `slidesAnimated`, and `get_session view:"plan"` gives `clipSource` per shot. **Never describe a user's own clip as Live Motion** — a user who declined the upgrade was once told her reel contained "2 plans animés en Live Motion".

**Otherwise most likely**: `generate {clip}` was never called, or the slide's `motionMode` wasn't set to `live` first.

**Action**: `edit_session({commands:[{slide:{action:"set_motion_mode", slideIndex, motionMode:"live", liveAction:"<verb>"}}]})` THEN `generate({sessionId, clip:{slideIndex}})` (10 seeds, or free on a `search {clips}` cache hit ≥ 60). On a selling reel this is the RECOMMENDATION and comes before the stills render, not after a baseline — see `poppify-build-reel` Step 6.

## When to file feedback

If the symptom doesn't match any of the above, OR you've followed the action and the issue persists, call:

```
submit_feedback({
  apiKey,
  sessionId,                          // optional but include when you have one
  frictionPoints: ["<the symptom + what you tried, specific>"],
  suggestedImprovements: ["<concrete tool/doc/flow change>"],   // optional
  notes: "..."                        // optional free-text context
})
```

(There is no `kind`/`description` field — describe bugs in `frictionPoints`, improvement ideas in `suggestedImprovements`.)

Don't re-file known-resolved issues — check the "Recently addressed" block in the MCP server instructions before filing.
