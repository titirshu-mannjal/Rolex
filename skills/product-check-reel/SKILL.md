---
name: product-check-reel
description: Build a premium 3D product "checklist" Reel - a hero product rendered in 3D that orbits, rolls and floats, the camera pushes into macro details (stitches, knit, drawcord, pleats), x-ray highlights and callouts mark each feature, a five-item checklist card stack ticks off, A/B comparisons and a shape morph prove the claim, and a lookbook ends it. Use for apparel, watches, bags, shoes or any product where you show "5 things to look for", feature breakdowns, 360 product turntables, macro detail shots or "why this one" ads.
---

# Product check reel

The format: a buyer's checklist told through one hero product. A 33 s reference ran almost as one continuous camera move (only 6 hard cuts, average shot 4.5 s): the energy comes from the camera always moving and an overlay changing on every phrase, not from cutting.

## 1. Structure

| Beat | Shot | Overlay |
|---|---|---|
| Hook 0-2.5 s | Product turns in space, slow orbit + push | One italic serif line: the promise |
| Promise 2.5-4 s | Defocus the product (DOF to blur), it becomes the background | Checklist stack: 5 dark cards slide up one by one, each with a tiny image, number and condensed label |
| Check 1..5, 4-6 s each | Camera cuts or flies into the feature: macro push-in, focus pull, slow 15-30 deg orbit | Corner title `CHECK:0N` (mono 9 px) + feature name (Archivo Black 44 px) top-left; caption phrase by phrase low centre |
| Proof inside each check | Pick one: x-ray (feature tinted cool blue, wireframe bounding box draws on), line callouts drawing along seams/pleats, A/B side by side with ✕/✓ chips, morph from wrong shape to right shape, context light change (e.g. cool cabin blue to warm dinner amber) | Small pill chip bottom-right: red ✕ "JOGGER" / green ✓ "NO CREASES" |
| Payoff | Back to the blurred hero, checklist returns, all 5 tick green in a fast stagger | "that ticks all five." |
| Hero | Product walks/floats in an invisible-body cloth sim, full 360 roll | Brand line |
| CTA | Lookbook grid of styled outfits | "Follow X and comment WORD for the link" |

Framing marks: thin corner crop brackets in all four corners for the whole video (studio "viewfinder" feel). Background: soft grey seamless studio, colour shifts only to motivate a story point.

## 2. The 3D product (pick by what exists)

1. **Have the real product + time:** model it in Blender. Apparel: `blender-agent-skills:blender-clothing` + `cloth-sim` (pattern pieces, sew, simulate on a hidden mannequin; render the mannequin as holdout so the garment floats "invisible body"). Hard goods: `blender-agent-skills:blender-hardsurface-modeling`. Materials: `blender-agent-skills:blender-pbr-materials` (fabric: sheen 0.5, fuzz via noise bump, real thread normal map for macro).
2. **Only photos:** Blender MCP `generate_3d` from a clean cut-out (`rembg i -m birefnet-general`), then retopo/clean in Blender. It may cost a credit - ask first. Free online alternatives (TRELLIS / Hunyuan3D Hugging Face Spaces) upload the image to a third party - ask first. This machine (4 GB GPU) cannot run them locally.
3. **Only one photo and no 3D needed:** 2.5D parallax with `depthflow` / `perspective-illusion` - fine for push-ins, not for a 360 orbit.

## 3. Camera and motion (Blender)

- Orbit: camera on an empty with Track To; rotate the empty 360 deg over 6-8 s with Bezier ease; add 2-4 deg handheld noise at low frequency. Product can also spin on its own axis with a slight tilt so it "rolls".
- Macro: 85-135 mm lens, f/1.4-2.8 DOF, focus distance animated from background to the stitch (focus pull 0.6 s). Push 10-20% over the shot. This is what sells stitch and knit detail.
- Cloth: wind force field at low strength so fabric breathes in every shot; never let the garment freeze.
- Lighting: `blender-agent-skills:blender-lighting-lookdev` - large soft key, rim, grey seamless; motivated colour shifts per beat.
- Render: Cycles or EEVEE at 1080x1920, 30 fps, then `realesrgan-ncnn-vulkan` only if rendering at half res to save time.
- Use `camera-cinematography`, `blender-director` and `animation-principles` for the moves.

## 4. Overlays (HyperFrames or Remotion over the rendered plates)

- Type system: label `Space Mono` 9-11 px tracking 0.1em; feature title `Archivo Black` 40-48 px; captions `Instrument Serif Italic` 34-40 px white with 20% shadow; numbers condensed (`Bebas Neue`).
- Checklist cards: 300x62 px, 10 px radius, dark glass with a tiny photo bleed on the right, number in mono, empty ring at right that fills green on tick. Stack enters with 60 ms stagger, `expo.out`.
- Callout lines draw with stroke-dashoffset in 0.4 s; x-ray = blue tint + scanline + wireframe box with corner ticks; ✕/✓ chips pop with `back.out(2)`.
- Every overlay change lands on a VO word (whisper word timestamps, `beat-sync-editing`).
- Engines: `hyperframes`, `gsap-timeline`, `kinetic-typography`, `caption-animation`, `motion-overlays`, `lower-thirds`.

## 5. Sound and finish

Soft fabric whooshes on orbits, a click per checklist tick, low piano or ambient bed (`sound-effects`, `library/`). Export with `reel-export`. QA with `reel-editor-qa`: pull a frame at every overlay change and check type legibility on a phone-sized view.
