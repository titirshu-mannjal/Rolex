---
name: voiceover-direction
description: Direct and produce a voiceover that sounds alive, premium and relatable (Indian English by default) instead of flat TTS - script for the ear, generate one continuous read with stress marks, tighten pauses, broadcast-polish, measure against reference reels, then time the edit to the voice. Use whenever a Reel needs narration, when a VO "sounds flat, robotic or boring", or when matching the delivery of a reference video.
---

# Voiceover direction

Communication carries the video. A flat read kills good frames.

## Why TTS sounds flat (measured, not guessed)

Measured on two reference reels (voices separated with Demucs) against our first TTS reads:

| | Ref 1 (product ad) | Ref 2 (history) | Line-by-line TTS |
|---|---|---|---|
| Pace (words/s over the spoken span) | 3.1 | 2.6 | ~2.0 |
| Pauses ≥150 ms per 10 s | 3.4 (avg 290 ms) | 0.4 (avg 160 ms) | 3.4-3.9 |
| Pitch range | 12.7 st | 10.2 st | 13-17 st |

The TTS did not lack pitch range. It was flat because each line was generated on its own: every sentence restarted and fell to the same full-stop melody, and it was slow. Repetition of the same contour reads as robotic.

## Method

1. **Write for the ear.** Short lines, one idea each, the selling word late in the line. Hook as a question or a promise. Use contrast ("so it never scratches"). Keep the brand's register: polished, relatable Indian English, polite and warm, not foreign-accented.
2. **Generate one continuous read** of the whole script (never line by line), so phrases link and the intonation builds.
   - Kokoro (`~/.local/share/rolex/tts/.venv`, Apache-2.0): `KPipeline(lang_code='b', device='cpu')`, voices `hm_omega` (male, user's default) or `hf_alpha` (female, clearest), speed ~0.97 for calm, 1.05-1.1 for energy.
   - Stress the words that sell with misaki markup: `[five](+2)`, `[never](+2)`, `[dark](+1)`.
   - Chatterbox (MIT) adds an `exaggeration` control (0.5-0.8) and can clone a voice from a 10 s clip: clone only a synthetic voice or a consenting actor. It needs the GPU; on CPU it is impractically slow. Do not run it while Blender holds the GPU.
3. **Polish:** `python vo_polish.py in.wav out.wav --max-gap 0.28` tightens long pauses (0.19 for punchy ads, 0.28 for calm) and applies the broadcast chain (80 Hz high-pass, -2.5 dB at 250 Hz, +3 dB at 3.4 kHz, +2 dB air shelf, 3:1 compression, de-ess, limiter).
4. **Measure:** `python prosody.py ref_vocals.wav ours.wav`. Target pace 2.6-3.3 words/s total, pauses near the reference, then run Whisper to check every word is intelligible (fix spellings the model mangles with phonetic respelling).
5. **Time the edit to the voice:** take Whisper word timestamps of the final VO and cut, pop and caption on those words. Open gaps in the VO (split and delay) for big visual moments, and land the next line on the payoff (e.g. a reassembly snap).
6. **Mix:** VO on top, music ducked under it with sidechain compression, SFX tucked under consonants, -14 LUFS integrated, true peak ≤ -1.5 dBTP.

## References in this folder

- `prosody.py` - pitch range, movement, loudness contrast, pauses (YIN pitch on voiced frames).
- `vo_polish.py` - pause tightening + broadcast chain; prints a speech-start map for re-timing.
- Separate a reference reel's voice: `python -m demucs --two-stems=vocals -n htdemucs -d cpu ref.wav` (same venv).
- Clean a real recording (free Adobe Podcast stand-in): `deepFilter in.wav -o outdir` (same venv).
