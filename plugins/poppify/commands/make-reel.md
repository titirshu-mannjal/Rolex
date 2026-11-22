---
description: Generate a cinematic vertical reel via the Poppify MCP — photo-led or topic-led. Uses the poppify-build-reel skill for the canonical flow.
argument-hint: [photos or topic description]
---

The user wants to create a Poppify reel. Args provided: $ARGUMENTS

Invoke the `poppify-build-reel` skill and follow its flow:

1. If the user has no `apiKey` yet, call `account({register:{}})` first (optionally `{ label: "claude" }` — there is no `source` param). Surface the `signupBonusUrl` so they can claim 50 free seeds (+25 per connected social account across 4 platforms, 150 in total) before paying.

2. Pick the entry based on what the user provided. **Multi-brand user** (`portfolio_required`): ask which brand and pass `portfolioId` on `start_session` — the reel keeps that brand through render and publish; never `portfolio:{action:"switch"}` for one reel.
   - Photos (data URLs or http URLs) → `start_session({apiKey, photos:{userWords, photos, goal, audience?, platform?}})` — `userWords` is REQUIRED and is their brief VERBATIM, never your paraphrase
   - Topic / brand intent (no photos) → `start_session({apiKey, topic:{userWords, topic, audience, goal}})` — `userWords` REQUIRED, verbatim (no `platform` — not in the topic schema, silently dropped) then `edit_session {concept}` to pick from the 5 returned concepts. **Topic-led sessions start with NO images** — every slide's `imageUrl` is empty. You must give at least one slide an image (search the library or `generate {image}`, then `edit_session({commands:[{slide:{action:"set_image", slideIndex, imageUrl}}]})`) before `render`, or it is refused BEFORE any charge — `slides_missing_images` naming the empty shots (`topic_led_no_images` only when the deck is wholly empty). One image can serve every beat — `set_image` the same URL on each slide; captions + motion carry the variety.

3. Review the returned slides + caption + hashtags + CTA with the user. Default to ONE bulk call to apply any edits:
   ```
   edit_session({
     sessionId,
     expectedVersion: N,           // the N in the "DECK vN" line every response ends with
     commands: [
       {slide: {action: "set_text", slideIndex: 0, newText: "..."}},   // setting text turns that caption ON (captions are opt-in)
       {patch: {
         textColor: "#FFFFFF",         // or any hex
         textAnimation: "editorial",   // editorial | lower_third | karaoke
         videoEffect: "push_in",       // canonical vocabulary: push_in, pull_out, lateral_pan, vertical_pan, focus_pull, epic_parallax, static
         audioMood: "uplifting",
         audio: { source: "library", assetId: "..." }
       }}
     ]
   })
   ```

4. Use `search {images}` and `search {music}` BEFORE recommending `generate {image}` / `generate {music}` — library matches are free; generation is 5 seeds each. Attach images per shot by asset id from the deck view: `edit_session({commands:[{slide:{action:"set_image", slideIndex, asset:"G1"}}]})`, several at once with `edit_session({commands:[{slide:{…}}, {slide:{…}}]}) (one {slide} command per op)` — **not** the legacy pool and not by re-pasting URLs. Move one shot with `edit_session({commands:[{slide:{action:"move", asset:"P4", to:"first"}}]})`. To swap music, `edit_session({commands:[{patch:{audio:{source:"library", assetId}}}]})` — or `assetId:"M2"` for a track already in the session. When the user says what an asset IS ("that's the cover", "only an example", "don't crop it"), record it with `edit_session({commands:[{asset:{action:"set", asset, attrs:{...}}}]})` so later edits can't undo it.

5. When the user asks for the render (or says yes to the price you quoted — never in reply to a correction or a complaint): call `get_session` to confirm seed cost — pre-confirm it returns the exact price breakdown — then `render({ sessionId, apiKey })`. Poll `get_session` every 20–30 seconds. When complete, hand the `videoUrl` to the user with the note that it's valid ~7 days.

6. **Single-image reels**: when one image carries the whole reel, keep ONE `videoEffect` and set `continuousEffect: true` (default is `false` — you must set it) so the camera makes one continuous move across the slides. Assigning a DIFFERENT effect per slide on a same-image run disables continuous smoothing and produces a visible reset at each cut.

7. **Live Motion.** On a reel that SELLS something (product, local business, app promo, brand identity) the moving treatment is the RECOMMENDATION — offer it first with its price, the 1-seed stills render second; `render` refuses with `motion_decision_unrecorded` until the choice is on record, and its question is keyed `1`/`2` with NO default, so a bare "yes" is not an answer. On any other reel it stays an upgrade offered after the baseline. To animate: `search {clips}` first (cache hits free), else `edit_session({commands:[{slide:{action:"set_motion_mode", slideIndex, motionMode:"live", liveAction}}]})` + `generate {clip}` (10 seeds/clip). If a response carries a `stitchOffer`, that is the offer — ONE take cut 2–5 ways for the same 10 seeds — quote it verbatim. Otherwise at most one live slide, usually the hook. For before/after transformations (`endFrameUri`), invoke the `poppify-live-motion` skill first — bridged renders need a composition-locked end frame and an authored journey `overridePrompt`.

8. **Reel length is per-slide — no global knob.** Two DRIVERS: text length, or an explicit `edit_session({commands:[{slide:{action:"set_duration", slideIndex, duration:N}}]})` (2–15s captioned, 0.5–15s uncaptioned; works on ANY slide, overrides the text-length formula). Voiceover audio is an UNCONDITIONAL floor. A live clip plays in full BY DEFAULT — so an **8s morph slide holds all 8s** and you never pad a caption to keep it on screen — but an explicit `set_duration` deliberately TRIMS it. A still held past ~6s is refused before charging (`still_held_too_long`): split the time across more shots instead of stretching one picture. Lengthen a slide by writing more text OR set_duration.

9. **Optional consistency / before-after** (5 seeds/frame, same as an image): for the SAME subject across slides, `generate({image:{referenceAssetId|referenceImageUrl, prompt:"same subject, <new pose/scene>"}})` (consistent-frames mode) → `set_image`, animate normally. For a before/after transformation in ONE slide, `generate {image}` the "after" from the same reference, then `edit_session({commands:[{slide:{action:"set_motion_mode", ..., endFrameUri:<after url>}}]})` so Veo interpolates start → end. Each frame is one intentional call — not a random batch. Send `endFrameUri` only for transitions, never for plain micro-motion.

For verification of the finished MP4, use `/poppify:verify-render`. For symptoms (wrong color, missing audio, etc.), use `/poppify:troubleshoot`.
