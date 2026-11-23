#!/usr/bin/env python3
"""Search and fetch openly licensed sounds from Openverse (WordPress), with licence records.
  ov.py search "whoosh" [--n 10] [--cc0] [--max-s 6]      list results (commercial-use licences only)
  ov.py get <id> [--out library/openverse]                 download one, append its credit to CREDITS.md
No key needed (anonymous rate limits apply). Only cc0 / pdm / by / by-sa are allowed (all allow commercial use);
anything with 'nc' or 'nd' is refused."""
import argparse, json, os, re, sys, urllib.parse, urllib.request
API = "https://api.openverse.org/v1/audio/"
UA = {"User-Agent": "rolex-studio/1.0 (openverse-sounds skill)"}
OK = {"cc0", "pdm", "by", "by-sa"}

def call(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return json.load(r)

def search(q, n, cc0, max_s):
    p = {"q": q, "page_size": min(max(n * 2, 10), 50), "license": "cc0,pdm" if cc0 else "cc0,pdm,by,by-sa"}
    rows = [r for r in call(API + "?" + urllib.parse.urlencode(p))["results"]
            if r["license"] in OK and (not max_s or (r.get("duration") or 0) <= max_s * 1000)][:n]
    for r in rows:
        print(f'{r["id"]}  {(r.get("duration") or 0)/1000:5.1f}s  {r["license"]:5} {r["source"]:10} {r["title"][:50]}  by {r.get("creator") or "?"}')
    return rows

def get(i, out):
    r = call(API + i + "/")
    if r["license"] not in OK:
        sys.exit(f'refused: licence {r["license"]} does not allow commercial use')
    os.makedirs(out, exist_ok=True)
    ext = os.path.splitext(urllib.parse.urlparse(r["url"]).path)[1] or "." + (r.get("filetype") or "mp3")
    name = re.sub(r"[^a-z0-9]+", "-", r["title"].lower()).strip("-")[:50] + f"_{i[:8]}{ext}"
    with urllib.request.urlopen(urllib.request.Request(r["url"], headers=UA), timeout=60) as s, open(os.path.join(out, name), "wb") as f:
        f.write(s.read())
    lic = f'{r["license"].upper()} {r.get("license_version") or ""}'.strip()
    credit = f'- {name}: "{r["title"]}" by {r.get("creator") or "unknown"} ({r["source"]}), {lic}, {r.get("foreign_landing_url") or r["url"]}'
    with open(os.path.join(out, "CREDITS.md"), "a") as f:
        f.write(credit + "\n")
    print(os.path.join(out, name)); print(credit)
    if r["license"] in ("by", "by-sa"):
        print("ATTRIBUTION REQUIRED: put the credit line in the post caption or end card.")

ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest="cmd", required=True)
a = sp.add_parser("search"); a.add_argument("q"); a.add_argument("--n", type=int, default=10); a.add_argument("--cc0", action="store_true"); a.add_argument("--max-s", type=float, default=0)
b = sp.add_parser("get"); b.add_argument("id"); b.add_argument("--out", default="library/openverse")
x = ap.parse_args()
search(x.q, x.n, x.cc0, x.max_s) if x.cmd == "search" else get(x.id, x.out)
