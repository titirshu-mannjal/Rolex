#!/usr/bin/env python3
"""Delivery gate: fails (exit 1) instead of letting the agent grade itself.
Usage: python3 gate.py <production_dir> --video <final.mp4> [--vo-json whisper.json --script script.txt] [--cues cues.json]
                      [--pace 2.6,3.3] [--sfx-max-rate 1.3]
Checks (each prints PASS/FAIL with the number):
  files     brief.md script.md storyboard/ qa.md TOOLS.md sources.md research/facts.md exist; qa.md has no '- [ ]' open blockers
  pace      words per second over the spoken span (Whisper word timestamps) inside --pace
  words     every script word heard by Whisper (word error rate <= 8%)
  sfx       salient hits (gain > -22 dB) per s <= --sfx-max-rate, none < 0.25 s apart, no same file twice within 3 s
  loudness  -15.0..-13.0 LUFS integrated, true peak <= -1.0 dBTP
  delivery  1080x1920 (or 1920x1080), >= 25 fps, video bitrate >= 12 Mb/s, only one video + one audio stream
"""
import argparse, json, os, re, subprocess, sys

FILES = ["brief.md", "script.md", "storyboard", "qa.md", "TOOLS.md", "sources.md", "research/facts.md"]


def words(text):
    return re.findall(r"[a-z0-9']+", text.lower())


def wer(ref, hyp):
    r, h = words(ref), words(hyp)
    d = list(range(len(h) + 1))
    for i in range(1, len(r) + 1):
        prev, d[0] = d[0], i
        for j in range(1, len(h) + 1):
            cur = min(d[j] + 1, d[j - 1] + 1, prev + (r[i - 1] != h[j - 1]))
            prev, d[j] = d[j], cur
    return d[len(h)] / max(len(r), 1)


def sfx_check(cues, max_rate, salient_db=-22.0):
    # Only salient hits count against the budget: quiet micro-sounds (typing ticks, ratchets) may be denser.
    hits = sorted((c["t"], c["file"]) for c in cues if c.get("gain_db", 0) > salient_db)
    if not hits:
        return True, "no cues"
    span = max(hits[-1][0] - hits[0][0], 1.0)
    rate = len(hits) / span
    close = sum(1 for a, b in zip(hits, hits[1:]) if b[0] - a[0] < 0.25)
    repeat = sum(1 for i, (t, f) in enumerate(hits) for t2, f2 in hits[i + 1:] if f2 == f and t2 - t < 3.0)
    ok = rate <= max_rate and close == 0 and repeat == 0
    return ok, f"{rate:.2f} salient hits/s (max {max_rate}), {close} pairs <0.25 s apart, {repeat} same-file repeats within 3 s"


def probe(video):
    j = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", video],
                                  capture_output=True, text=True, check=True).stdout)
    return j


def loudness(video):
    out = subprocess.run(["ffmpeg", "-nostats", "-i", video, "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    summ = out[out.rfind("Summary:"):]
    i = float(re.search(r"I:\s+(-?[\d.]+) LUFS", summ).group(1))
    tp = float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", summ).group(1))
    return i, tp


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("prod"); ap.add_argument("--video", required=True)
    ap.add_argument("--vo-json"); ap.add_argument("--script"); ap.add_argument("--cues")
    ap.add_argument("--pace", default="2.6,3.3"); ap.add_argument("--sfx-max-rate", type=float, default=1.3)
    a = ap.parse_args(argv)
    res = []
    missing = [f for f in FILES if not os.path.exists(os.path.join(a.prod, f))]
    qa = os.path.join(a.prod, "qa.md")
    open_items = len(re.findall(r"^\s*- \[ \]", open(qa).read(), re.M)) if os.path.exists(qa) else 0
    res.append(("files", not missing and open_items == 0, f"missing {missing or 'none'}, {open_items} open QA blockers"))
    if a.vo_json:
        ws = [w for s in json.load(open(a.vo_json))["segments"] for w in s["words"]]
        lo, hi = map(float, a.pace.split(","))
        pace = len(ws) / max(ws[-1]["end"] - ws[0]["start"], 0.1)
        res.append(("pace", lo <= pace <= hi, f"{pace:.2f} words/s (target {lo}-{hi})"))
        if a.script:
            e = wer(open(a.script).read(), " ".join(w["word"] for w in ws))
            res.append(("words", e <= 0.08, f"word error rate {e:.1%} (max 8%)"))
    if a.cues:
        ok, msg = sfx_check(json.load(open(a.cues)), a.sfx_max_rate)
        res.append(("sfx", ok, msg))
    i, tp = loudness(a.video)
    res.append(("loudness", -15.0 <= i <= -13.0 and tp <= -1.0, f"{i} LUFS, {tp} dBTP"))
    p = probe(a.video)
    v = [s for s in p["streams"] if s["codec_type"] == "video"]
    au = [s for s in p["streams"] if s["codec_type"] == "audio"]
    other = len(p["streams"]) - len(v) - len(au)
    vb = int(v[0].get("bit_rate") or p["format"].get("bit_rate") or 0) / 1e6 if v else 0
    num, den = map(int, v[0]["r_frame_rate"].split("/")) if v else (0, 1)
    size_ok = v and (v[0]["width"], v[0]["height"]) in ((1080, 1920), (1920, 1080))
    res.append(("delivery", bool(size_ok and num / den >= 25 and vb >= 12 and len(v) == 1 and len(au) == 1 and other == 0),
                f"{v[0]['width']}x{v[0]['height']} {num/den:.0f} fps {vb:.1f} Mb/s, streams v{len(v)} a{len(au)} other{other}" if v else "no video"))
    for name, ok, msg in res:
        print(f"{'PASS' if ok else 'FAIL'}  {name:9} {msg}")
    failed = [n for n, ok, _ in res if not ok]
    print("GATE " + ("PASSED" if not failed else "FAILED: " + ", ".join(failed)))
    return 1 if failed else 0


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        assert wer("so it never scratches", "so it never scratches") == 0
        assert abs(wer("softer the more you wear it", "softer the more you weigh") - 2 / 6) < 1e-9
        assert sfx_check([{"t": 0, "file": "a"}, {"t": 0.1, "file": "b"}], 2)[0] is False      # too close
        assert sfx_check([{"t": 0, "file": "a"}, {"t": 1, "file": "a"}], 2)[0] is False        # repeat within 3 s
        assert sfx_check([{"t": 0, "file": "a"}, {"t": 1, "file": "b"}, {"t": 2, "file": "c"}], 1.6)[0] is True
        assert sfx_check([{"t": 0, "file": "a"}, {"t": 0.05, "file": "tick", "gain_db": -30}], 2)[0] is True  # quiet micro-sound ignored
        print("self-test ok"); sys.exit(0)
    sys.exit(main())
