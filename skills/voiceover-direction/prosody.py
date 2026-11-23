"""Measure how 'alive' a voice read is. Usage: python prosody.py file.wav [...]
Metrics (voiced frames only):
  f0_med   median pitch (Hz)
  range_st pitch range 5th-95th percentile, semitones   (flat reads ~4-6, lively ~9-14)
  sd_st    pitch standard deviation, semitones
  move     mean |pitch change| per 50 ms, semitones     (melodic movement)
  dyn_db   loudness contrast: std of frame level, dB    (emphasis)
  pauses   pauses >=150 ms per 10 s of speech; mean pause ms
"""
import sys, numpy as np, soundfile as sf

def load(p, sr=16000):
    x, s = sf.read(p, always_2d=True); x = x.mean(1)
    if s != sr:
        n = int(len(x) * sr / s); x = np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x)
    return x.astype(np.float32), sr

def yin(x, sr, hop=0.01, fmin=70, fmax=400, th=0.15):
    w = int(0.04 * sr); h = int(hop * sr); tmin, tmax = int(sr / fmax), int(sr / fmin)
    f0, rms = [], []
    for i in range(0, len(x) - w - tmax, h):
        fr = x[i:i + w + tmax]; rms.append(np.sqrt(np.mean(fr[:w] ** 2)) + 1e-9)
        d = np.array([np.sum((fr[:w] - fr[t:t + w]) ** 2) for t in range(tmax + 1)])
        c = d.copy(); c[1:] = d[1:] * np.arange(1, tmax + 1) / np.maximum(np.cumsum(d[1:]), 1e-9); c[0] = 1
        idx = np.where(c[tmin:tmax] < th)[0]
        if len(idx):
            t = idx[0] + tmin
            while t + 1 < tmax and c[t + 1] < c[t]: t += 1
            f0.append(sr / t)
        else:
            f0.append(0.0)
    return np.array(f0), 20 * np.log10(np.array(rms))

def measure(p):
    x, sr = load(p)
    f0, db = yin(x, sr)
    speech = db > (np.max(db) - 35)
    v = (f0 > 0) & speech
    st = 12 * np.log2(f0[v] / np.median(f0[v]))
    # median-filter octave errors
    st = st[np.abs(st) < 12]
    move = np.abs(np.diff(st[::5])).mean()
    # pauses: runs of non-speech >= 150 ms inside the spoken span
    idx = np.where(speech)[0]; sp = speech[idx[0]:idx[-1] + 1]
    runs, cur = [], 0
    for s in sp:
        if not s: cur += 1
        elif cur: runs.append(cur); cur = 0
    pauses = [r * 10 for r in runs if r >= 15]
    dur = len(sp) * 0.01
    return dict(file=p.split("/")[-1][:28], f0_med=round(float(np.median(f0[v])), 1), range_st=round(float(np.percentile(st, 95) - np.percentile(st, 5)), 1),
                sd_st=round(float(st.std()), 2), move=round(float(move), 2), dyn_db=round(float(db[speech].std()), 1),
                pauses_per10s=round(len(pauses) / dur * 10, 1), pause_ms=int(np.mean(pauses)) if pauses else 0)

if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(measure(p))
