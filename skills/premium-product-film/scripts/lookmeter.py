#!/usr/bin/env python3
"""Measure the look of rendered frames against a reference (light, contrast, colour), so "premium" is a number.
Usage:
  lookmeter.py --ref ref.mp4 --ours ours.mp4 [--times 0.5,2,4]      sample frames from both videos
  lookmeter.py --ref-frames 'ref/*.png' --ours-frames 'ours/*.png'
Metrics per set: mean luminance, share of near-black (<6%), share of highlights (>85%), contrast p99/p5,
saturation of lit pixels, border luminance (the stage). Prints a PASS/FAIL per metric with tolerances.
Needs numpy and Pillow (any venv that has them, e.g. ~/.local/share/uv/tools/rembg/bin/python)."""
import argparse, glob, os, subprocess, sys, tempfile
import numpy as np
from PIL import Image

TOL = {"mean_lum": 0.35, "dark": 0.35, "highlights": 0.6, "contrast": 0.35, "sat": 0.06, "border": 0.5}  # relative, except sat (absolute)


def frames_from(video, times, out):
    paths = []
    for i, t in enumerate(times):
        p = os.path.join(out, f"f{i:03d}.png")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", video, "-frames:v", "1", "-vf", "scale=540:-2", p], check=True)
        paths.append(p)
    return paths


def measure(paths):
    rows = []
    for f in paths:
        a = np.asarray(Image.open(f).convert("RGB").resize((540, 960))).astype(np.float32) / 255
        lum = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
        mx, mn = a.max(-1), a.min(-1)
        sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
        border = np.concatenate([lum[:30].ravel(), lum[-30:].ravel(), lum[:, :20].ravel(), lum[:, -20:].ravel()])
        rows.append([lum.mean(), (lum < 0.06).mean(), (lum > 0.85).mean(),
                     np.percentile(lum, 99) / max(np.percentile(lum, 5), 0.005),
                     sat[lum > 0.1].mean() if (lum > 0.1).any() else 0.0, border.mean()])
    return dict(zip(["mean_lum", "dark", "highlights", "contrast", "sat", "border"], np.array(rows).mean(0)))


def compare(ref, ours):
    fails = 0
    for k, r in ref.items():
        o = ours[k]
        ok = abs(o - r) <= TOL[k] if k == "sat" else abs(o - r) <= TOL[k] * max(abs(r), 1e-3)
        fails += not ok
        print(f"{'PASS' if ok else 'FAIL'}  {k:10} ref {r:8.3f}  ours {o:8.3f}")
    print("LOOK " + ("MATCHES REFERENCE" if not fails else f"OFF on {fails} metric(s)"))
    return fails


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        d = tempfile.mkdtemp()
        dark = np.zeros((960, 540, 3), np.uint8); dark[400:560, 200:340] = 230
        bright = np.full((960, 540, 3), 180, np.uint8)
        Image.fromarray(dark).save(f"{d}/a.png"); Image.fromarray(bright).save(f"{d}/b.png")
        assert compare(measure([f"{d}/a.png"]), measure([f"{d}/a.png"])) == 0
        assert compare(measure([f"{d}/a.png"]), measure([f"{d}/b.png"])) > 0
        print("self-test ok"); sys.exit(0)
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref"); ap.add_argument("--ours"); ap.add_argument("--times", default="0.5,1.5,3,5,7,9")
    ap.add_argument("--ref-frames"); ap.add_argument("--ours-frames")
    a = ap.parse_args(); tmp = tempfile.mkdtemp(); times = [float(t) for t in a.times.split(",")]
    rp = sorted(glob.glob(a.ref_frames)) if a.ref_frames else frames_from(a.ref, times, tempfile.mkdtemp(dir=tmp))
    if not (a.ours or a.ours_frames):  # stats only: describe one film's look
        for k, v in measure(rp).items(): print(f"{k:10} {v:8.3f}")
        sys.exit(0)
    op = sorted(glob.glob(a.ours_frames)) if a.ours_frames else frames_from(a.ours, times, tempfile.mkdtemp(dir=tmp))
    sys.exit(1 if compare(measure(rp), measure(op)) else 0)
