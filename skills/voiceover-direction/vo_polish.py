"""Polish a TTS or recorded voiceover like a VO editor would.
Usage: python vo_polish.py in.wav out.wav [--max-gap 0.19]
1. Tighten pauses: any silence longer than max-gap is cut down to it (with 15 ms fades), so lines flow.
2. Broadcast chain: rumble cut, de-mud, presence and air lift, gentle compression, light de-ess.
Prints the old and new durations and the gap map (old start -> new start) so the edit can be re-timed."""
import sys, json, subprocess, numpy as np, soundfile as sf

args = sys.argv[1:]
src, dst = args[0], args[1]
max_gap = float(args[args.index("--max-gap") + 1]) if "--max-gap" in args else 0.19

x, sr = sf.read(src, always_2d=True); x = x.mean(1)
hop = int(0.01 * sr)
db = 20 * np.log10(np.array([np.sqrt(np.mean(x[i:i + hop] ** 2)) + 1e-9 for i in range(0, len(x), hop)]))
speech = db > db.max() - 38
# silence runs
keep, i, n = [], 0, len(speech)
segs = []
while i < n:
    j = i
    while j < n and speech[j] == speech[i]: j += 1
    segs.append((speech[i], i * hop, min(j * hop, len(x))))
    i = j
out, tmap, t_new = [], [], 0.0
fade = int(0.015 * sr)
for k, (is_sp, a, b) in enumerate(segs):
    seg = x[a:b]
    if not is_sp and 0 < k < len(segs) - 1 and (b - a) / sr > max_gap:
        m = int(max_gap * sr); half = m // 2
        seg = np.concatenate([seg[:half], seg[-(m - half):]])
    elif not is_sp and (k == 0 or k == len(segs) - 1):
        seg = seg[: int(0.08 * sr)]
    if is_sp:
        tmap.append([round(a / sr, 3), round(t_new, 3)])
    out.append(seg); t_new += len(seg) / sr
y = np.concatenate(out)
tmp = dst + ".tight.wav"
sf.write(tmp, y, sr)
chain = ("highpass=f=80,equalizer=f=250:t=q:w=1.2:g=-2.5,equalizer=f=3400:t=q:w=1.0:g=3,"
         "highshelf=f=9500:g=2,acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=3,"
         "deesser=i=0.4,alimiter=limit=0.89")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", chain, "-ar", "48000", dst], check=True)
subprocess.run(["rm", "-f", tmp])
print(json.dumps({"in_s": round(len(x) / sr, 2), "out_s": round(len(y) / sr, 2), "speech_starts_old_to_new": tmap}))
