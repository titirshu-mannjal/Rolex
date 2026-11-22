"""Refresh plugins/ from each upstream repo named in packs/*.txt and rewrite .claude-plugin/marketplace.json.
Usage: python3 -I scripts/refresh-plugins.py .  (maintainers only; installs do not need this)"""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path

root = Path(sys.argv[1]).resolve()
work = Path(tempfile.mkdtemp())
clones, entries = {}, []

def clone(src):
    if src not in clones:
        d = work / str(len(clones))
        subprocess.run(["git", "clone", "-q", "--depth", "1", src, str(d)], check=True)
        clones[src] = d
    return clones[src]

for pack in sorted((root / "packs").glob("*.txt")):
    for line in pack.read_text().splitlines():
        parts = line.split()
        if len(parts) < 4 or parts[0] != "plugin":
            continue
        repo, name = parts[3], parts[2].split("@")[0]   # plugin @rolex <name>@rolex <upstream owner/repo>
        d = clone(f"https://github.com/{repo}.git")
        mkt = json.loads((d / ".claude-plugin/marketplace.json").read_text())
        e = next(p for p in mkt["plugins"] if p["name"] == name)
        src = e["source"]
        if isinstance(src, dict):  # plugin lives in another repo
            url = src.get("url") or f"https://github.com/{src['repo']}.git"
            base = clone(url) / src.get("path", "")
        else:
            base = (d / src).resolve()
        dest = root / "plugins" / name
        shutil.rmtree(dest, ignore_errors=True)
        shutil.copytree(base, dest, symlinks=True, ignore=shutil.ignore_patterns(".git", "node_modules", ".venv", "__pycache__", ".env"))
        e = dict(e, source=f"./plugins/{name}")
        entries.append(e)
        print(f"{pack.stem:8} {name:28} <- {repo}")

out = {"name": "rolex", "owner": {"name": "titirshu-mannjal"},
       "metadata": {"description": "Rolex: curated Claude Code toolkit for Instagram Reels (stored copies of every plugin)."},
       "plugins": entries}
(root / ".claude-plugin").mkdir(exist_ok=True)
(root / ".claude-plugin/marketplace.json").write_text(json.dumps(out, indent=2) + "\n")
assert len({e["name"] for e in entries}) == len(entries), "duplicate plugin names"
shutil.rmtree(work)
print(len(entries), "plugins stored")
