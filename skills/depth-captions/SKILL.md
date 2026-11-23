---
name: depth-captions
description: Captions with depth for a talking-head Reel - one big word sits behind the speaker's head (person cut out on every frame), the rest of the words pop up as small captions in front, each landing on the exact frame it is spoken, with a light sound on every move. Use when someone wants a word behind their head, 3D or layered captions, captions that feel premium, or to build their own caption style from reels they like.
---

# Depth captions

Method credit: Shaan Johari (@viashaan), "How I edited my captions reel with AI" (Notion, 2026). Written here in our own words.

## The layer stack (back to front)

1. The original frame (or a replaced background).
2. The big word: Anton capitals, white, ~85% of frame width, never wider than the frame.
3. The person, cut out with a soft alpha edge so hair does not look chopped.
4. Small captions in front: Inter Bold, ~7% of frame width, soft dark shadow, up to 3 words per group, split at natural breaks.

Optionally move a virtual camera slightly through the stack so the text reads as 3D, not stuck to the screen.

## Steps

1. Ask for the clip (5-10 s talking to camera, space above the head works best), the word that goes behind the head (or pick the strongest: a number or the subject), and any brand names to spell right.
2. Set up inside the project folder only: ffmpeg, a venv with faster-whisper (small) or `whisper-ctranslate2`, `rembg` with `birefnet-portrait`, Pillow, numpy, and the fonts in Rolex `assets/fonts`. Model downloads: ~1 GB cut-out, ~0.5 GB speech; warn before they start.
3. Words and timing: extract audio (16 kHz mono), transcribe with word timestamps and no initial prompt. Show the words in one line, flag anything that looks wrong, wait for OK. A corrected word keeps the replaced word's time. Then snap each word start to the nearest audio onset: Whisper often starts words ~0.1 s early, and 3 frames late or early is felt.
4. Cut out the person with `rembg i -m birefnet-portrait` (frames from the big word to the end). Keep the soft alpha.
5. Place the big word: find the top of the head from the mask on the frame the word is spoken, looking only at the middle 40% of the frame width (ignore raised hands). The head should overlap ~60% of the letter height and cover at least 15% of the letters; lower the word until it does. It pops in on its word: 80% to 100% scale over 6 frames with ~5% overshoot, then holds still.
6. Captions: each word appears on its own start time; each group holds until the next starts; keep them between 15% and 65% of frame height (Instagram covers the bottom third and the right rail); never on top of the big word; do not caption the big word twice.
7. Export H.264 at the source size and frame rate, keeping the source colour settings; save one PNG with the big word showing. Then change only what is asked.

## Building your own style

- Start from 3-5 reels you love: screen-record, break down fonts, sizes, entrances, exits, placement and motion, then combine the parts you like.
- Two fonts, not ten: a clean one for most words, a bold one for the word that matters.
- One accent colour, for the one word per line that must be remembered.
- Every move gets a sound: a light tick or whoosh, kept under the voice (`sound-effects`).
- Give notes on the exact frame like you would to an editor ("this word is late", "bigger and behind my head").
- When a note lands, save it as a rule in the project's style file so the style builds up across videos.

## Related

Voice clean-up for a real recording: DeepFilterNet in `~/.local/share/rolex/tts/.venv` (`deepFilter in.wav -o outdir`), the free local stand-in for Adobe Podcast. Background replacement (Beeble in the original) is a paid service: ask first.
