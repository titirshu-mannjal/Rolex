---
name: brand-reveal-film
description: Direct a cinematic brand or logo reveal / launch teaser (the Farborn standard) - the logo is never shown whole until late: macro fragments of a 3D extruded mark emerge from darkness with edge glints, a radial or layered build, a pull-back to the full symmetric symbol on a reflective floor, then a hard handoff to the flat 2D wordmark and a date or CTA - with a drone-and-riser soundscape and one stop-down before the resolve. Use for "logo reveal", "brand reveal", "intro / outro sting", "launch teaser", "coming soon", "announce the brand", and for the brand moment at the end of any film.
---

# Brand reveal film

Built from a teardown of a Farborn launch teaser (29 s, 9:16; `productions/_research/logo-reveal/`, numbers in `reel-production/references/teardowns.md`).

## What it does, measured

- **Mystery first:** for 16 of 29 s the viewer sees only parts of the mark (extruded strips, steps, edges); the whole symbol appears at 16 s, the wordmark at 22 s, the date at 25.5 s.
- **Look:** emissive darkness (mean luminance 0.07, 72-75% near-black, contrast ~128) with ONE saturated brand colour (saturation 0.61) as the only light source: green glowing edges on dark glass/acrylic, small star glints where light hits corners, a mirror floor at the resolve.
- **Sound:** no voice; no beat grid; a continuous ambient pad with orchestral stabs and reverse-cymbal risers (salient hits only 0.14/s, onsets 6.6/s as texture); the strongest accents mark the first light (0.3 s) and the radial burst (8.5 s); a 0.35 s stop-down (silence) at 14 s just before the resolve; a riser and bell chime into the wordmark; very wide stereo; cuts 100% on sound.

## Structure (scale to 10-30 s)

| Beat | Share | Picture | Sound |
|---|---|---|---|
| Emerge | 0-14% | Extreme close-up of one fragment in darkness; light ramps up along its edges; glints | low drone, first stab as light hits |
| Multiply | 14-35% | Fragments repeat in a radial / kaleidoscopic or stepped arrangement; the camera dollies through | swell, risers |
| Travel | 35-55% | Layered strips slide in parallax; low angles along the structure; glow intensifies | stabs on the strongest moves |
| Stop-down | ~48% | A beat of near-silence and stillness | 0.3-0.5 s gap |
| Resolve | 55-75% | The full symbol forms, symmetric, on a reflective floor; the camera pulls back from big to small | the fullest chord |
| Handoff | 75-85% | Hard cut from the 3D symbol to the flat 2D wordmark in brand colour, which settles to white | riser into a bell or chime |
| Payload | 85-100% | Date, CTA or tagline in small mono type; fade to black | tail |

## Variants (pick by brand)

| Brand character | Material and light | Build |
|---|---|---|
| Tech, gaming, bold | emissive edges on dark glass (this reference) | fragments → radial → symbol |
| Luxury, heritage | polished metal, black stage, strip-light sweeps (`premium-product-film` lighting) | light sweep across a relief, never emissive |
| Friendly consumer, food, kids | soft clay or paper (`blender-claymation`, `edit-kit:paper-cutout`) | pieces bounce and snap together |
| Fintech, SaaS, editorial | flat vector on an off-white canvas (`ui-promo-film` look) | line-draw, mask reveals, letter build |
| Indian heritage, festive | gold foil, diya warm light, rangoli geometry | radial rangoli build → symbol |

## Build route

- 3D mark: extrude the logo SVG in Blender (curve → extrude + bevel, or Geometry Nodes for the strip/step repetition), emissive + glass materials, Cycles, a mirror floor, black world; or three.js via `3d-animator` when Blender is not wanted.
- 2D handoff and type: `hyperframes` + `gsap-*` (`logo-animation` for the flat lockup).
- Sound: drones and risers from the SOUNDE library (`real-sfx`), one stop-down, a chime into the wordmark; check with `earshot critique --video`.
- Logo rules: the real mark is only moved, scaled, masked or extruded from its own vector; never redrawn or recoloured beyond the brand palette.
- Also use the last 2-3 s of this recipe as the brand moment at the end of any other film.
