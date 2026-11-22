---
name: archival-collage-story
description: Build a premium documentary-style history Reel - archival photos scatter and stack, cut-out figures stand on a painted colour shape, huge condensed numbers count up ("300 YEARS AGO", "36", "45,000+"), old film frames with timecode, a newspaper prop slides in, year tickers flip from past to present, and modern product shots close with tag chips. Use for brand heritage, "the story of X", city/craft/industry origin stories, timelines, "how X became Y" and any narrated history montage.
---

# Archival collage story

A narrated history told as a magazine collage that moves. A 55 s reference had 42 cuts (average 1.3 s, as short as 0.1 s in the closing flurry) after a 10.7 s map opener: slow and grand to set up, fast and dense once the story turns modern.

## 1. Structure

| Act | Look | Moves |
|---|---|---|
| Hook | Map (use `satellite-map-story`) | One continuous push, pins on each name |
| Then | Black and white. Black ground with drifting cloud plates top and bottom | Archival photos fly in from off-screen, tilted 3-8 deg, and stack; a giant red number (Anton 300 px) + white small-caps line ("YEARS AGO") locks in the centre |
| The founder | Cut-out figure (rembg) standing on a torn red paint shape over a cut-out landmark and a stone parapet foreground | Layers parallax at different speeds; name card in mono small caps bottom-left; huge title behind the figure (figure overlaps the title) |
| Evidence | Old film plate in a rounded frame with VHS timecode, scan lines, gate weave and grain | Condensed white words stack line by line top-left ("TRADE / CRAFTSMANSHIP") |
| Scale | Craftsman cut-out on a red ellipse, giant number counts up (19 to 36) behind him, small archive photos orbit in | Counter rolls with `power3.out`, photos pop in staggered |
| Craft | Macro B&W hands at work (block print, setting stones) | Pill chip top-centre types on ("FLORAL BLOCK PRINTS ✓") |
| Turn | Colour returns on period paintings, slow Ken Burns | A newspaper headline prop ("X BANNED") slides up, slightly rotated, with a small mono caption ("THE CALICO ACT, 1720") |
| Now | Modern product macro shots, cut fast | Year ticker on a ruler line flips 1977 to 2026; big number "45,000+ ARTISANS" over an overhead shot |
| Close | Back to the map, all pins together, zoom out; final rapid cut flurry | Share-pill CTA |

Captions all the way through: one word or short phrase at a time, Instrument Serif Italic, low centre, synced to VO words.

## 2. Tools for each move

| Move | Tool |
|---|---|
| Cut out figures, landmarks, props | `rembg i -m birefnet-general in.jpg out.png` (portraits: `birefnet-portrait`; low RAM: `-m u2netp`); video: `object-separation` |
| Rescue low-res archive scans | `realesrgan-ncnn-vulkan -i in.jpg -o out.png -n realesrgan-x4plus -m ~/.local/share/realesrgan/models` |
| Restore colour to B&W, or colour on purpose | `colorize` |
| Parallax inside one photo (2.5D) | `depthflow`, `perspective-illusion`, `pixel2motion` |
| Layered collage, paint shapes, number counters, chips, year ticker | `hyperframes` + `gsap-timeline`, `kinetic-typography`, `animated-infographic`, `milestone-reveal`, `countdown-video` |
| Film grain, VHS timecode, gate weave, scan lines | `effects`, `motion-effects`, `ffmpeg-skill` (noise, `tblend`, `lenscorrection`), `shader-glsl` |
| Cloud / fog plates | free stock (Pexels, Pixabay) or `particle-system` |
| Editorial fonts | Anton, Bebas Neue, Oswald (headlines), Instrument Serif (captions), Space Mono (labels) - installed by Rolex |
| Pacing to beat | `beat-sync-editing`, `editing-montage`, `video-use` |
| Sound | `sound-effects` (paper slides, camera shutters, film projector, deep hits on numbers) |

## 3. Sourcing archival images

Use public-domain or licensed sources only: Wikimedia Commons (check each file's licence), Library of Congress, Rijksmuseum and The Met open-access collections, the brand's own archive. Record source and licence for every image in `productions/<slug>/sources.md`. Never lift frames from other creators' videos.

## 4. Direction rules

- Black, white and one accent colour (here red) until the story turns modern; then full colour. Colour is a story signal.
- Every still moves: scale 1.00 to 1.06, drift, or parallax. Nothing sits dead.
- Big numbers are the shot, not a label: 40-60% of frame width.
- The figure breaks the frame of the title (depth). Foreground elements (parapet, clouds) give layers.
- Speed up as you approach the present; the final flurry is 2-4 frames per cut.
