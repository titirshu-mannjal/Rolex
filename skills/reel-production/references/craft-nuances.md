# Craft nuances: the small details that make a film feel made

A vocabulary gathered from the user's references (joggers, Jaipur, Hublot, Amazon prompt, ElevenLabs, Farborn). None of these is mandatory. Each one is a tool with a job; use it only when the script needs that job done, and say in `brief.md` (REFERENCE FIT) why it is in or out.

## How to choose

For every nuance below, ask four questions before using it:
1. **Job:** what does it do for THIS film (depth, rhythm, brand identity, clarity, mood, continuity)?
2. **Fit:** does it suit the brand, the audience and the tone of the script (calm, energetic, luxurious, playful, serious)?
3. **Cost to clarity:** does it compete with the product, the words or the face? Anything that steals attention from the message is out.
4. **Restraint:** is something else already doing that job? Two nuances doing the same job make noise.

If the answer to 1 is vague, leave it out.

## Background and space

| Nuance | Seen in | Job | Helps when | Hurts when | Build |
|---|---|---|---|---|---|
| Dot grid / dot field (tiny dots, sometimes drifting or converging) | ElevenLabs (behind "Scanning", the orb, the tagline) | gives empty space depth and quiet life; implies data, intelligence, a system | tech, AI, data, minimal canvases with a lot of empty space; a "thinking" or "scanning" moment | the frame is already busy, footage behind it, warm or organic brands, luxury black stage | HyperFrames canvas or SVG; drift 2-6 px/s, dots 1.5-3 px, 6-15% opacity; converge to a point on a cue |
| Brand shape-language pattern (rounded-rect tiles, outlines at low contrast) | ElevenLabs title and end lockup | makes the brand's geometry the wallpaper; ties scenes to the identity | the brand has a clear shape language | the brand has none (inventing one looks generic) | SVG tile, 4-8% contrast, slow parallax |
| Mesh gradient textures with grain | ElevenLabs swatches, backgrounds | colour and softness without clutter; transitions (zoom into a swatch) | modern tech/creative brands, light editorial looks | heritage, rugged, luxury-dark looks | shader or pre-rendered gradient video with 3-5% grain |
| Soft light pool on a dark stage | Hublot, Amazon (amber glow) | separates the hero from the void; mood | dark premium looks | bright looks | radial gradient behind the hero, border luminance ~0.05-0.1 |
| Particle field / floating dust | ElevenLabs closing, Farborn glints | atmosphere, scale, magic | reveals, closings, abstract ideas | product demos that need clarity | particles at low density, depth of field, slow |
| Film grain | Amazon, Jaipur archive | removes the CG sheen, unifies footage and graphics | mixed media, cinematic, archive | crisp UI shots meant to look like software | 2-4% grain overlay or media-treatment |
| Corner brackets / viewfinder frame | joggers checklist | "inspection" framing, holds a format across shots | checklist, review, spec formats | lifestyle, emotional, luxury | 4 L-shapes, safe zone |

## Type

| Nuance | Seen in | Job | Helps when | Hurts when |
|---|---|---|---|---|
| Word-by-word fill (grey → white/black) locked to the voice | ElevenLabs, Jaipur captions | the viewer reads at the speaker's pace; statements feel spoken | narrated statements, taglines | dense information, fast cuts |
| Word swap on the beat ("Connect X to — Claude / Cursor / ChatGPT") | ElevenLabs integrations | shows breadth fast without a list | integrations, cities, use cases, audiences | fewer than 3 items |
| Letter build / logo split into a lockup | ElevenLabs title, Amazon logo | the name arrives as an event | product names, launches | the logo must stay pixel-exact at rest (then animate only around it) |
| Tiny spec-sheet labels in mono around a hero | ElevenLabs swatches | precision, "engineered" feel | tech, product details | storytelling, emotional pieces, phone-size text below 28 px |
| Giant numbers as the shot | Jaipur ("300", "36", "45,000+") | facts with impact | data, heritage, scale | when the number is not verified or not meaningful |
| Small centred tracked caps end cards | Hublot, Farborn | luxury restraint | premium, reveal, teaser | energetic social ads that need a CTA |

## Camera and motion

| Nuance | Seen in | Job | Helps when | Hurts when |
|---|---|---|---|---|
| Frame 0 already moving | all | the first second hooks | always for social; skip only for deliberate stillness | - |
| Macro zoom into a UI element, push through into the next state | ElevenLabs | the product is the set; continuity | software, apps | physical products (use real macro instead) |
| Oversized cursor as an actor | ElevenLabs | shows intent and causality (click → next beat) | UI demos | non-UI films |
| 3D tilted cards / floating card field | ElevenLabs, Amazon | depth and scale from flat UI | many items, scale of use | when one thing matters |
| Assembly / explode with spin and overshoot | Hublot | engineering, value | premium physical products | soft goods, services |
| Fragments before the whole (mystery) | Farborn | anticipation | reveals, teasers | explainers that need clarity fast |
| Dark/light beat alternation | ElevenLabs | rhythm and chapter feeling in longer films | 30 s+ narrated films | short 10-15 s pieces |
| One continuous shot with a through-line device | Amazon | the film feels like one idea | a strong brand device exists | forced devices that do not mean anything |
| Mirror floor, glints on edges | Farborn, Hublot | value, polish | 3D heroes on dark | flat editorial looks |

## Sound

| Nuance | Seen in | Job | Helps when | Hurts when |
|---|---|---|---|---|
| Sonic logo (one bell/ding at frame 1 and at the end) | ElevenLabs | brand recall, bookends | brands with an audio identity or a clean opening | busy openings |
| Micro-UI bed (keys, pops, ticks, 5-8 onsets/s, quiet) | ElevenLabs, Amazon | the interface feels alive | UI demos | cinematic or emotional pieces |
| Sub drop on section changes | ElevenLabs | chapter breaks felt in the body | narrated multi-section films | luxury calm pieces (use a soft swell) |
| Stop-down: 0.3-0.5 s of near-silence before the resolve | Farborn, Amazon (breath before the hero) | makes the payoff land | any reveal or hero moment | never skip it before a hero hit |
| No voice in the reveal | Farborn, Hublot | lets image and music carry emotion | reveals, luxury, teasers | when the script needs explanation: then keep the voice and let the reveal be its pause |
| Second voice performing the product | ElevenLabs dictation | a feature becomes a scene | voice or input products | products with no input moment |
| Real mechanical foley motif (tick, seat clicks) | Hublot, watch tests | tactility | physical products | software |

## Decision example

Brief: "a 30 s promo for an Indian fintech app, warm and trustworthy".
- In: word-by-word fill (narrated statements), macro UI zoom + cursor (it is an app), micro-UI bed (alive), one human moment (trust), sonic logo (brand recall), stop-down before the logo.
- Out: dot field (would feel cold and techy against "warm"), mesh gradients (replace with the brand's own warm palette), spec-sheet labels (reads technical, not trustworthy), dark/light alternation (30 s is short; one tone holds better), explode (not a physical product).
