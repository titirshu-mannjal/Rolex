---
name: satellite-map-story
description: Build a premium satellite-map sequence for a Reel - slow push from country to region, the region lifts out with a glow, photo pins drop in one by one on the beat, arcs radiate out, a condensed title slams in. Free, offline imagery (NASA Blue Marble, Sentinel-2 cloudless 2016) and public-domain borders (Natural Earth, India point of view). Use when a video needs "show it on the map", a brand/city/state origin story, a "where it comes from" beat, or a map with pins, arcs or highlighted regions.
---

# Satellite map story

A map shot that feels like a documentary title, not a Google Maps screen recording. Built as one continuous camera move with things arriving on it, never a static map with labels.

## 1. Data (free, offline)

```bash
bash ~/.local/share/rolex/repo/skills/satellite-map-story/scripts/fetch-map-data.sh library/maps            # South Asia, NASA, 4096 px
bash .../fetch-map-data.sh library/maps 68,22,79,31 4096                                                      # tighter bbox = sharper zoom
SOURCE=eox bash .../fetch-map-data.sh library/maps 68,22,79,31 4096                                           # Sentinel-2 2016, sharper, credit required
```

- Image is plate carree: `x = (lon - lonW) / (lonE - lonW) * W`, `y = (latN - lat) / (latN - latS) * H`. Project GeoJSON with the same formula (or `d3.geoEquirectangular().fitExtent`) so borders sit exactly on the imagery.
- Fetch two images: a wide one for the opening and a tight one for the region. Cross-dissolve between them during the push so the zoom never goes soft. Max useful zoom is about 1 source pixel per output pixel.
- **India maps must show India's official boundary.** Use `countries_india_pov.geojson` for the country outline. Never use the default world file for India, and never publish a map of India without checking Kashmir and Arunachal Pradesh.
- Credits: NASA imagery is public domain (credit "NASA" is courtesy). EOX 2016 needs its credit line in the caption or end card (see script header). EOX 2018+ is non-commercial: never use it for brand work.

## 2. The move (measured from a 55 s reference: map opener ran 10.7 s as one take, map return 8 s)

| Beat | What happens | Timing and easing |
|---|---|---|
| Establish | Whole country, very slow push-in (scale 1.00 to 1.08) | Starts at frame 0, `power1.inOut`, never stops moving |
| Region lift | Region polygon fills 15-20% white, 1.5 px white stroke, outer glow (blur 30 px, 40%), rest of map darkens 25% | 0.5 s, `expo.out` |
| Ping | Soft white ring or a fog ring sweeps around the region once | 0.8 s, then fades |
| Pins | Photo cards (polaroid: white 4 px frame, mono 7 px label under, small pointer) drop in **one per spoken name**, scale 0.6 to 1 with `back.out(2)`, 3 deg random tilt settling to 0 | Each pin lands on the word that names it (whisper word timestamps) |
| Crowd | When pins overlap, earlier pins shrink to 70% and nudge apart; do not let them collide | `power2.out`, 0.3 s |
| Arcs | Thin white great-circle arcs draw out from the region to the frame edges (stroke-dashoffset), 1 px, 60% opacity | 0.6 s each, staggered 0.08 s |
| Title | Condensed headline (Bebas Neue / Anton, 120-160 px, white) slams in at top third: scale 1.4 to 1 + blur 12 to 0 | 0.25 s `expo.out`, then holds while the camera keeps moving |
| Exit | Push through the region into the next shot (scale to 3x with motion blur), or fog/cloud wipe | 0.4 s |

Rules: the camera moves every frame. One new element per beat of VO. Pins carry real product photos (cut out with `rembg`, upscaled with `realesrgan-ncnn-vulkan`). Keep the top 220 px and bottom 400 px clear of Instagram UI except the title.

## 3. Engine

- **HyperFrames** (`hyperframes` skill) or **Remotion** (`remotion-best-practices`): one `<img>` for the satellite image inside a transformed container, one inline `<svg>` with the projected region path, arcs and pins in the same coordinate space, so a single transform drives the whole camera.
- Animate with GSAP (`gsap-timeline`, `gsap-core`). Use `remotion-maps` only if a Mapbox token is available; the static-image route needs none and renders deterministically.
- For a true 3D globe opener use `threejs-earth-render`.
- Caption: one word or short phrase at a time, Instrument Serif Italic 34-40 px, white, centred low (see `caption-animation`).

## 4. QA

Render, pull frames at every pin landing (`ffmpeg -ss T -frames:v 1`), check: border on imagery, no pin overlap, title inside safe zone, boundary correct, credit line present when EOX is used.
