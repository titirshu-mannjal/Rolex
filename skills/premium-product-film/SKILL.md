---
name: premium-product-film
description: Reference-level luxury product CG film (the Hublot / Apple / perfume-ad grade) for ANY product - hero asset detail, low-key black-on-black lighting with edge lines, path-traced materials, the assembly/explode choreography, macro crawl, reverse-side reveal, hero light-up, restrained typography and music-led sound - with a category table that adapts the recipe to watches, perfume, phones, shoes, jewellery, skincare, headphones, cars and food, and a lookmeter that turns "premium" into numbers. Use whenever a product must look expensive, for "explode/assemble animation", "like this luxury ad", 3D product commercials, launch hero films, or when a 3D product render looks flat, cheap, plastic or AI-made.
---

# Premium product film

> A vocabulary, not a template: use the parts that serve this film's script, brand and audience, adapt them, and record what you used and rejected under REFERENCE FIT in `brief.md` (see `reel-production/references/craft-nuances.md`). Reproduce the reference closely only when the user asks for that explicitly.

Built from a frame-by-frame teardown of a Hublot Big Bang Unico film (15 s, `productions/_research/watch-explode-ref/`) against our own first watch ad, which looked flat. Everything below is what separated them. Measure every film against a reference with `scripts/lookmeter.py` before calling the look done.

## Why the reference looks expensive and ours did not (measured)

| | Reference | Our flat attempt | Lesson |
|---|---|---|---|
| Mean luminance | 0.13 | 0.59 | low-key: the frame is mostly dark |
| Near-black pixels | 33% | 0% | darkness is a material, not an absence |
| Highlights >85% | 0.9% | 2.0% | light is precise lines and points, never wash |
| Contrast p99/p5 | 83 | 4 | deep blacks against crisp speculars |
| Saturation | 0.02 | 0.08 | near-monochrome, one tiny accent (red) |
| Stage (border) | 0.08 | 0.61 | a dark stage with a soft pool of light behind the product |
| Asset | hundreds of parts: skeleton dial, movement, screws with slots, engraved caseback text, ribbed strap | ~10 primitives | detail is what the camera sells |
| Explode | parts fly in from every axis, spinning, and assemble on the product's own axes | slabs slid vertically | assembly is choreography |
| Film | assembly → macro crawl → reverse side → hero lights up → ~40% of runtime on quiet type | busy chips, captions and cards | restraint reads as luxury |

## The six pillars

### 1. Hero asset (gate before anything moves)
- **Detail inventory first.** List every part a buyer would know (for a watch: case, bezel, screws, crown, guards, pushers, crystal, dial layers, applied indices, numerals, hands, subdials, movement plate, bridges, wheels, jewels, balance, hairspring, rotor, caseback, engraving, strap ribs, buckle). If a part is missing, the camera will find the gap.
- **Micro-detail that sells scale:** chamfered (bevelled) edges on everything, screw slots, engraved micro-text, knurling, perlage/Côtes de Genève, brushed vs polished zones on the same part, real thickness (no zero-thickness planes), contact shadows.
- **Separate objects per part,** grouped by assembly layer, with true pivots: the explode depends on it.
- **Source, in order:** the client's CAD or photos (model to them) → `blender-agent-skills:blender-hardsurface-modeling` + `geometry-nodes` procedural build (unbranded, fully explodable) → Blender MCP `search_assets` Sketchfab (needs the user's own API key in Blender; check licence, remove real brand marks) → `generate_3d` only for props (single mesh, cannot explode; may cost credits). Round products (bottles, cans, jars): `edit-kit:blender-product-film` builds from a photo.
- **Lookdev gate:** 3 stills at 100% (hero 3/4, macro, reverse) beside 2 reference frames; `lookmeter.py` within tolerance; no part may read as a primitive. Only then animate.

### 2. Materials (Cycles, physically based)
- Black ceramic / lacquer: base ~0.012, roughness 0.04-0.08, clear coat 1.0. It is invisible except for reflections: that is the point.
- Polished metal: roughness 0.05-0.1. Brushed: roughness 0.2-0.3 with anisotropy along the brush direction (radial for dials and bezels). Never one roughness for a whole part.
- Glass/sapphire/crystal: transmission 1, IOR 1.5-1.77, thin geometry with real edges; a faint blue coat for AR coating; edge glints come from the strip lights.
- Rubber/leather/fabric: roughness 0.55-0.75, fine noise bump, low sheen; ribs and grooves as geometry, not texture.
- Gems/jewels: transmission + colour + dispersion (or a high IOR) so they spark.
- Finishes as bump: perlage (Voronoi), Côtes de Genève (wave bands), guilloché, knurl.

### 3. Light (low-key, black-on-black)
- **Stage:** black world for camera rays (Light Path → Is Camera Ray), an HDRI only for reflections (Poly Haven `studio_small_03`, CC0, in `library/hdri/`), and a dim radial pool on the backdrop behind the product (border luminance ~0.08).
- **Strip lights** (long thin area lights, 0.02 × 0.4-0.5 m) at grazing angles left and right: they draw the edge lines that define a black object.
- **Large soft overhead** for the long gradient reflection across glossy faces.
- **Rim/back light** to separate the silhouette from the stage; a **small kicker** for the specular points on screws and numerals (the brightest 1% of the frame).
- **Light as animation:** sweep a strip across the product, fade the key up from black for the hero reveal, never cut light on/off.
- Target numbers (lookmeter): mean luminance 0.10-0.18, highlights 0.5-1.5%, saturation < 0.05 plus one accent.

### 4. Render
- Cycles + OptiX, adaptive sampling 64-128 samples + OptiX denoiser, motion blur ON (shutter 0.5) for the explode, true DOF (f/2.8-5.6 hero, f/8-16 macro: depth of field is millimetres at macro).
- Camera clip start 2 mm. Persistent data on for animations. 4 GB laptop GPU: 1080x1920 runs about 10-30 s/frame, so render detached and resumable (`setsid nohup`, `use_overwrite = False`), stills first, then a 25% preview, then the final.
- AgX view transform, High Contrast look; grade in compositing toward near-monochrome with the accent preserved.

### 5. Camera and choreography
- **Assembly (the opener, 3-4 s):** frame 0 is already exploded and moving. Parts converge along the product's own axes (layers stack on the main axis; screws, crown, pushers, side parts fly in laterally), each with a small spin that stops as it seats; stagger outer-to-inner or bottom-to-top 2-3 frames apart; expo-out ease with a 2-4% overshoot and settle; motion blur on. The camera orbits slowly (10-25°) on a low 3/4 angle with slight dutch.
- **Macro crawl (2-3 s):** f/8-16, a slow lateral slide or rotation across the most detailed surface, rack focus once.
- **Reverse side (2 s):** the side nobody sees (caseback, internals, sole, inner box), with its engraving.
- **Hero light-up (2-3 s):** frontal, centred, the product rises out of black as the key fades up; a slow push-in.
- **Type (~40% of runtime):** small, centred, white tracked caps on black (product name, then the brand mark, then the URL or CTA), each a gentle fade with no slam.
- Disassembly is the reverse: the same choreography played backwards also works as a loop.

### 6. Sound and edit
- Music-led, no voiceover by default for luxury: a minimal, dark bed with a clear pulse; the assembly lands on a downbeat.
- Mechanical foley from real recordings (`real-sfx`, `openverse-sounds`): metal clicks as parts seat (not every part: about 1 per beat), a deep lock thump when the product closes, a tick motif under the macro, air under the light sweep. Check with `earshot critique` and the `reel-production` sound budget.
- 3-4 hard cuts plus fades only into and out of black; no wipes, no chips, no captions over the product.

## Category adaptation

| Category | Assembly / explode | Hero light | Signature macro | Signature sound |
|---|---|---|---|---|
| Watch | layers on the case axis, screws spin in | strips + overhead on black | dial, hands, movement | tick, metal seat clicks |
| Perfume / glass bottle | cap lifts and spins, liquid rises, label wraps | backlight through glass, caustics, coloured liquid glow | glass edge, liquid surface, atomiser | glass ring, liquid pour, spray |
| Phone / laptop / tech | internals stack: board, battery, camera module, glass back | edge strips tracing the frame, screen glow as key | camera lenses, port chamfer, buttons | soft UI ticks, magnetic snaps |
| Sneaker / shoe | sole, midsole, upper, laces, insole separate and assemble | rim light + top soft, fabric texture grazing | knit, stitching, sole tread | fabric swishes, rubber squeak, lace pull |
| Jewellery | stones set into the setting, prongs close | small hard points for sparkle (dispersion), black velvet | stone facets, engraving | crystal shimmer, soft chime |
| Skincare / cosmetics jar | lid unscrews, product swirl | soft wraparound, glossy highlights, pastel stage (bright variant) | cream texture, embossing | lid twist, soft pop |
| Headphones / audio | cups, drivers, cushions, band | rim + strips on matte black | mesh, drivers, stitching | bass hit, driver thump |
| Car / vehicle | panels and wheels assemble | long strip reflections along the body | badge, headlights, rims | engine note, door thunk |
| Food / drink | ingredients fly in and layer | backlit splash, warm key | droplets, texture | crunch, fizz, pour |

Bright variants (apparel, skincare, food for everyday brands) keep pillars 1, 2, 5 and 6 and replace pillar 3 with a soft high-key studio; set the lookmeter reference to a bright film of that category.

## Workflow

1. Find a category reference (Pinterest, brand channels); download with `yt-dlp`; frame sheet; run `lookmeter.py` on it to get its numbers.
2. Write the detail inventory and shot list (assembly → macro → reverse → hero → type) in `brief.md`.
3. Build the asset (pillar 1), materials (2), light (3). Lookdev stills; lookmeter against the reference; fix until it matches.
4. Animate the assembly with per-part keyframes from an exploded state (vectors from the product axes, spins, stagger, overshoot); preview at 25%.
5. Render final (pillar 4), edit and type in HyperFrames, sound per pillar 6, then `reel-production` gates (`gate.py`).

## Pitfalls already paid for

Primitive geometry reads as AI; a bright grey studio flattens black and metal products; EEVEE glass reads as a grey blob; boolean-cut objects keep an empty material slot; camera clip start 100 mm empties macro shots; macro f/4 gives no focus; sliding slabs is not an explode; chips and captions over a luxury product cheapen it; 70 sound cues in 24 s is noise.
