#!/usr/bin/env python3
"""Free cloud GPU routes through public Hugging Face Spaces (open models, legitimate free quota).
Run with: uv run -q --with gradio_client python hf_space.py <command> ...
  image "<prompt>" out.png [--w 1024 --h 1024 --seed 7]     FLUX.1-schnell (Apache-2.0, commercial use OK), ~10 s
  to3d in.png out.glb [--seed 7]                            TRELLIS (MIT), one textured mesh (not explodable), ~60-120 s of GPU
Quota: guests ~2 GPU-min/day (often refused for 3D); a free HF account token gives ~5 min/day. The token is read from
HF_TOKEN or ~/.cache/huggingface/token (the user's own; never print it). Prompts and images are sent to Hugging Face:
use only material the client has cleared for upload."""
import argparse, os, shutil, sys
from gradio_client import Client, handle_file


def token():
    t = os.environ.get("HF_TOKEN")
    p = os.path.expanduser("~/.cache/huggingface/token")
    if not t and os.path.exists(p):
        t = open(p).read().strip()
    return t or None


def client(space):
    t = token()
    for kw in ("token", "hf_token"):  # the argument name differs between gradio_client versions
        try:
            return Client(space, verbose=False, **({kw: t} if t else {}))
        except TypeError:
            continue
    return Client(space, verbose=False)


def image(a):
    c = client("black-forest-labs/FLUX.1-schnell")
    r = c.predict(prompt=a.prompt, seed=a.seed, randomize_seed=False, width=a.w, height=a.h, num_inference_steps=4, api_name="/infer")
    src = r[0] if isinstance(r, (list, tuple)) else r
    if a.out.endswith(".png"):
        os.system(f'magick "{src}" "{a.out}"')
    else:
        shutil.copy(src, a.out)
    print("saved", a.out)


def to3d(a):
    c = client("trellis-community/TRELLIS")
    c.predict(api_name="/start_session")
    pre = c.predict(image=handle_file(a.inp), api_name="/preprocess_image")
    r = c.predict(image=handle_file(pre), multiimages=[], seed=a.seed, ss_guidance_strength=7.5, ss_sampling_steps=12,
                  slat_guidance_strength=3.0, slat_sampling_steps=12, multiimage_algo="stochastic", mesh_simplify=0.95,
                  texture_size=1024, api_name="/generate_and_extract_glb")
    glb = next(x for x in r[::-1] if isinstance(x, str) and x.endswith(".glb"))
    shutil.copy(glb, a.out); print("saved", a.out)


ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest="cmd", required=True)
i = sp.add_parser("image"); i.add_argument("prompt"); i.add_argument("out"); i.add_argument("--w", type=int, default=1024); i.add_argument("--h", type=int, default=1024); i.add_argument("--seed", type=int, default=7)
t = sp.add_parser("to3d"); t.add_argument("inp"); t.add_argument("out"); t.add_argument("--seed", type=int, default=7)
a = ap.parse_args()
try:
    image(a) if a.cmd == "image" else to3d(a)
except Exception as e:
    msg = str(e)
    sys.exit("quota reached: add the user's free HF token (HF_TOKEN) or wait for the daily reset" if "quota" in msg.lower() else f"failed: {msg[:300]}")
