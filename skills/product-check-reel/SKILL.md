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

## 3b. Hard-won Blender rules (from the first watch build)

- **Camera clip start:** Blender's default near clip is 100 mm. Any macro closer than 10 cm renders empty. Set `cam.data.clip_start = 0.002`.
- **Aim in the product's own coordinates.** When the product is tilted, convert local points with `root.matrix_world @ Vector(local)`; world-space guesses miss.
- **Frame by field width, not distance:** portrait 9:16 with a 36 mm sensor (AUTO fit) has a 20.25 mm horizontal sensor, so `distance = field_width_mm * lens_mm / 20.25`. Pick the field (e.g. 26 mm for a crown, 50 mm for a 40 mm dial) and compute the camera.
- **Macro depth of field:** at ~0.8x magnification f/4 gives under 1 mm of focus, so everything goes soft. Use f/16-f/22 for macro shots, f/5.6-f/8 for hero shots (CG has no diffraction penalty).
- **Boolean-cut objects keep an empty first material slot** and render grey. Clear slots before assigning (`obj.data.materials.clear()`).
- **Glass in EEVEE:** a solid domed crystal refracts the background into a white blob. Use a thin, near-flat cap with Transparent + Glossy mixed by Fresnel x 0.45, render method Blended.
- **Metal needs something to reflect:** add emissive "softbox" planes invisible to camera (`visible_camera = False`) beside and above the product.
- **Render engine:** EEVEE at 48 samples is ~1-5 s a 1080x1920 frame on a 4 GB laptop GPU; Cycles is 5-10x slower. Make renders resumable (`use_overwrite = False`, `use_placeholder = True`) and launch them detached (`setsid nohup`).
- Preview every shot at 25% resolution with a frame step before the full render, and look at the sheet.

## 3c. Exploded view (the ad money shot)

1. Group parts under empties parented to the product (crystal, bezel, hands, dial, case, caseback, straps), keeping world transforms.
2. Lay the product flat and film from just above the horizon so the explode axis reads as screen-vertical; spin the product slowly (30-40 deg over the shot).
3. Timing over ~4.6 s: hold 0.5 s, lift parts 2 frames apart (bottom-up order so the top part travels furthest), hold exploded ~1.3 s, reassemble with a 4% overshoot past home, settle.
4. Export each part's screen position per frame (`world_to_camera_view`) to JSON; in the overlay, labels with leader lines read that track so they follow the parts while the product turns.
5. Sound: whoosh as parts lift, a small click per part, ticks on labels, a reverse riser into the reassembly and an impact + metal click on the snap. Land the next VO line on the snap.

## 4. Overlays (HyperFrames or Remotion over the rendered plates)

- Type system: label `Space Mono` 9-11 px tracking 0.1em; feature title `Archivo Black` 40-48 px; captions `Instrument Serif Italic` 34-40 px white with 20% shadow; numbers condensed (`Bebas Neue`).
- Checklist cards: 300x62 px, 10 px radius, dark glass with a tiny photo bleed on the right, number in mono, empty ring at right that fills green on tick. Stack enters with 60 ms stagger, `expo.out`.
- Callout lines draw with stroke-dashoffset in 0.4 s; x-ray = blue tint + scanline + wireframe box with corner ticks; ✕/✓ chips pop with `back.out(2)`.
- Every overlay change lands on a VO word (whisper word timestamps, `beat-sync-editing`).
- Engines: `hyperframes`, `gsap-timeline`, `kinetic-typography`, `caption-animation`, `motion-overlays`, `lower-thirds`.

## 5. Sound and finish

Soft fabric whooshes on orbits, a click per checklist tick, low piano or ambient bed (`sound-effects`, `library/`). Export with `reel-export`. QA with `reel-editor-qa`: pull a frame at every overlay change and check type legibility on a phone-sized view.
