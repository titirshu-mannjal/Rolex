---
name: creative-visualization
description: The creative engine - turn any subject, product, service or abstract idea into original visual ideas and the right animation for them. A method that generates visual metaphors through eight lenses, an atlas of animation techniques (what each one makes the viewer feel and how to build it in HyperFrames/GSAP, Blender, three.js or Remotion), a domain guide (fintech, lending, health, food, travel, fashion, real estate, education, SaaS/AI, beauty, auto, heritage) with metaphors, clichés to avoid and motion/sound temperament, and push-further checks. Use at the idea stage of every film (from brief-amplifier), whenever a concept feels generic, "how do I visualise X", or a subject has no obvious picture (services, data, software, abstract benefits).
---

# Creative visualization

References teach what great looks like. This skill is how to invent the next one: a subject goes in, a fitting visual idea and its motion come out. Nothing here is a template; it is a way of thinking plus a vocabulary.

## 1. The idea method (15 minutes, written in `brief.md`)

1. **Find the truth.** One sentence: what changes for the viewer because this exists? ("Loans approved in minutes, not weeks." "This watch keeps its accuracy for 70 years.") Visuals that do not express this truth are decoration.
2. **Run the eight lenses.** For each lens write one visual idea in a sentence:

| Lens | Question | Example (a lending platform) |
|---|---|---|
| Transformation | what becomes what? | a stack of paper forms folds itself into a single glowing card |
| Scale | what is small that is big, or big that is small? | one tap ripples out into a map of 600 cities lighting up |
| Journey | what travels from A to B? | an application moves like a parcel through stations, never stopping |
| Contrast | before vs after, slow vs fast, old vs new | split screen: a queue of files vs a single line of light |
| Inside view | what is hidden that we can open up? | x-ray into the app: rules, checks and partners clicking into place |
| Brand device | what does the logo, name or colour already mean? | the brand's mark becomes the route the money takes |
| Personification | what if it behaved like a person/creature? | the paperwork "sighs" and dissolves; a quiet assistant hand completes it |
| Data as object | what number can become a physical thing? | approval time as a sand-timer that empties in one second |

3. **Pick one, then make it carry the film.** Choose the idea that (a) expresses the truth, (b) reads in one second without words, (c) can travel through every beat as a through-line device. Combine at most two lenses.
4. **Score it before building** (1-5 each): clarity in one second, ownability (could only this brand say it?), emotional pull, buildability with our tools in the time we have, fit with the audience. Under 18/25: run the lenses again.

## 2. Animation technique atlas

Choose motion by the feeling it creates, then by the engine that builds it best. Combine families deliberately (one primary, one secondary), never stack everything.

| Family | Techniques | It makes the viewer feel | Build with |
|---|---|---|---|
| Kinetic type | word fill, word swap, letter build, mask rise, scale slam, type on a 3D path | the message is spoken, confident | `hyperframes` + `gsap-*`, `kinetic-typography`, `edit-kit:fx` |
| Reveals | mask/clip reveal, light sweep, draw-on (stroke), fragment-to-whole, assembly, iris, curtain of type | anticipation, value | GSAP masks, SVG `stroke-dashoffset`, Blender light keys, `brand-reveal-film` |
| Camera | push-in, push-through (into a UI or object), orbit, parallax (2.5D), rack focus, crane, whip pan, dolly zoom | presence, discovery, drama | HyperFrames 3D transforms, DepthFlow / `edit-kit:camera-arc`, Blender, three.js |
| Transitions / seams | match cut by shape or colour, zoom-through, inverse zoom, waterfall cut, rack-focus blur cut, morph, wipe on motion | continuity, one-shot feeling | `edit-kit:cut-the-curve`, `edit-kit:seam-craft`, `edit-kit:motion-doctrine` |
| Shape and morph | blob/orb morph, shape-to-icon, line becomes route, card stack fan, liquid fill | intelligence, fluidity | SVG path morph (GSAP MorphSVG), shaders (`shader-glsl`), `svg-animation` |
| UI motion | macro zoom into an element, typing, oversized cursor clicks, card lift into 3D, notification pop, list cascade | "it really works", ease | `ui-promo-film`, `edit-kit:fx`, `edit-kit:oversized-cursor` |
| Data | count-up, bar/line grow, map routes and pins, network graph build, before/after split, unit visualisation (dots = people) | credibility, scale | `animated-chart`, `animated-infographic`, `satellite-map-story`, D3 in HyperFrames |
| Particles and fields | dot grid breathing, particles converging into a shape, flow fields, dust in light, confetti burst | system intelligence, magic, celebration | `particle-system`, canvas in HyperFrames, three.js Points |
| 3D product | turntable, explode/assemble, x-ray/cutaway, macro crawl, light sweep, material close-ups | engineering, desire | `premium-product-film`, `product-check-reel`, `3d-animator`, Blender pack |
| Physical character | squash and stretch, anticipation, overshoot, follow-through, secondary motion, bounce on landing | life, friendliness | `animation-principles`, `disney-animation-rule-skill`, GSAP elastic/back eases |
| Collage and mixed media | cut-outs, paper layers, archive stacks, torn edges, stop-motion stepping (12 fps) | craft, history, authenticity | `archival-collage-story`, `edit-kit:paper-cutout`, `edit-kit:vox-director` |
| Illustration looks | line draw, watercolour, cel anime, pixel art, whiteboard, crayon | warmth, story, nostalgia | `edit-kit:*` looks, `animation-styles`, `painted-animation` |
| Texture and film | grain, halation, chromatic aberration at cuts, light leaks, scanlines, VHS | cinema, era, rawness | `effects`, `motion-effects`, media treatments |
| Light as motion | light sweep, flicker to life, rim light rising, lume glow, god rays | reveal, premium, mood | Blender/three.js light keys, HyperFrames gradients |

Motion rules that apply to every family: frame 0 already moving; eased (never linear) with anticipation and settle; one hero motion per beat with quieter secondary motion; motion has a reason (it shows a cause, a change or a direction); exit direction sets the next entry direction.

## 3. Domain guide

| Domain | Strong visual metaphors | Clichés to avoid | Motion temperament | Sound temperament |
|---|---|---|---|---|
| Fintech, payments | money as light/flow, a line that becomes a route, cards stacking, instant ripple | coin rain, piggy banks, rocket to the moon | precise, quick, clean easing | crisp UI ticks, soft confirm chime |
| Lending, credit, B2B finance (e.g. Mannjal) | paperwork transforming into one clean flow, partners as connected nodes, a journey with no stops, a ledger drawing itself | handshakes on white, stacks of rupee notes, bank buildings | steady, trustworthy, no gimmicks, measured pace | warm low pad, paper and stamp foley turning into soft digital clicks |
| Health, wellness | breath, rhythm, cells, light through water, growth | pills raining, generic doctors, heart-rate line everywhere | slow, organic, breathing | soft air, heartbeat sub only if meaningful |
| Food, beverage | macro texture, steam, pour, slow-motion splash, ingredients assembling | stock "happy family at table" | sensual slow-mo then quick cuts on the beat | crunch, sizzle, pour, fizz (real foley) |
| Travel, places | maps and routes, a journey through a window, passport stamps, light changing through the day | spinning globe, airplane icon on a dotted line | flowing, continuous camera, parallax | ambience beds of place, music swell |
| Fashion, apparel | fabric in motion, cloth simulation, detail macro, silhouette, walk cycle | spinning mannequin, flat lay montage without motion | rhythmic, cuts on the beat, attitude | fabric swishes, beat-led music |
| Real estate | light moving through rooms, blueprint to built, a day in the life, aerial to doorstep | drone-only montage, keys in hand | slow glide, architectural lines | room tone, birds, warm music |
| Education, edtech | ideas as building blocks, a mind map growing, light switching on, a path of steps | lightbulb icon, graduation cap toss | playful precision, builds and reveals | soft plucks, chalk/pencil foley |
| SaaS, AI tools | the real UI in motion, an orb or system thinking, dots converging, cards assembling | glowing brains, robots, blue binary code | macro UI, smooth camera, kinetic type on voice | UI micro-bed, sonic logo |
| Beauty, skincare | texture macro, light on skin, droplets, product swirl, pastel stages | before/after face swaps, sparkles on everything | soft, slow, luxurious | soft whooshes, water, airy pads |
| Automotive | light lines along the body, assembly, speed through parallax, engine detail | burning tyres, generic highway | powerful camera moves, low angles | engine note, door thunk, sub hits |
| Heritage, culture, India | archive collage, maps, craft hands, textile patterns, festive light (diya, rangoli geometry) | stock Taj Mahal, sitar on everything | respectful pace, collage motion, warm light | real instruments, place ambience, restrained |

## 4. Push it further (before calling an idea or a shot done)

- **Detail:** what is the smallest real detail the camera could find (engraving, stitch, UI micro-copy, texture)? Add it.
- **Second layer:** is there quiet secondary motion (dust, dots, light drift, parallax background) supporting the hero motion without competing?
- **Transition:** is every cut designed (shape match, motion match, colour match), or just a cut?
- **Light:** is the light telling the story (rising on the reveal, falling on the pause)?
- **Sound:** does the most important visual event have its own sound, and the moment before it a breath?
- **Surprise:** is there one moment the viewer did not expect (a scale jump, an inside view, a reversal)?
- **Restraint:** what can be removed so the idea reads faster?
- **Phone test:** does it read at phone size, muted, in the first second?

## 5. Proven blocks and the restyle pattern

- **Search the registry before building anything:** 448 HyperFrames blocks, indexed by atlas family in `references/registry-index.md` (regenerate with `scripts/index_registry.py`). Install with `npx hyperframes add <name> --json`, then restyle through its variables (`data-variable-values`) or its CONFIG.
- **Restyle, do not copy:** `sketchbook/make_sketch.py <style.json> <out>` builds the same three blocks (halftone dot field, word-fill statement, mark assembly) into two different films from two style files: `a_editorial` (off-white, lavender dots, cool mark, tech line) and `b_warm_india` (near-black, saffron dots, gold lotus, trust line). Proven 2026-11-24: both pass `hyperframes check` with 0 errors and render at 11 s.
- **Lessons from that test:** registry blocks can ship other brands' marks (`logo-outro` contains the Figma logo): always replace with the client's own mark; unfilled words in a word-fill need ≥ 3:1 contrast; a strong dot field behind type hurts reading (keep it ~0.3 opacity on dark); widen lines so no single word is stranded.

## 6. Grow the range

Every new reference the user shares goes through `reel-production/scripts/teardown.sh`, a row in `references/teardowns.md`, and any new technique into the atlas above or `references/craft-nuances.md` with its job and when it hurts. Every finished film adds one line to `productions/<slug>/NOTES.md`: what worked, what did not, what to try next.
