"""Build one sketch from registry blocks + a style JSON, proving the same blocks can be directed two different ways.
Usage: python3 make_sketch.py styles/a_editorial.json <out_dir>   (blocks are fetched into <out_dir>/../_blocks once)
Structure (16:9, 11 s): dot field + word-fill statement (0-5 s), own five-petal mark assembles with tagline (5-11 s)."""
import json, math, os, shutil, sys

style = json.load(open(sys.argv[1])); out = sys.argv[2]
SRC = os.path.join(os.path.dirname(os.path.abspath(out)) or ".", "_blocks")
if not os.path.exists(os.path.join(SRC, "compositions", "logo-outro.html")):  # bootstrap the registry blocks once
    import subprocess
    parent = os.path.dirname(SRC) or "."
    subprocess.run(["npx", "-y", "hyperframes", "init", os.path.basename(SRC), "--skip-skills", "--skill=hyperframes"], cwd=parent, check=True, capture_output=True)
    for b in ("halftone-field", "mk-callout-highlight", "logo-outro"):
        subprocess.run(["npx", "-y", "hyperframes", "add", b, "--json"], cwd=SRC, check=True, capture_output=True)
if os.path.exists(out): shutil.rmtree(out)
shutil.copytree(SRC, out, ignore=shutil.ignore_patterns("renders", ".hyperframes", "node_modules"))
comp = os.path.join(out, "compositions")


def petal(angle_deg, length=118, width=46, cx=80, cy=214):
    """A pointed petal from the base point, rotated around it; returns an SVG path in the 160x240 box."""
    a = math.radians(angle_deg)
    def rot(x, y):  # x across, y up from the base
        return cx + x * math.cos(a) + y * math.sin(a), cy - (-x * math.sin(a) + y * math.cos(a))
    p0, tip = rot(0, 0), rot(0, length)
    c1, c2 = rot(width, length * 0.38), rot(width * 0.55, length * 0.85)
    c3, c4 = rot(-width * 0.55, length * 0.85), rot(-width, length * 0.38)
    f = lambda p: f"{p[0]:.1f} {p[1]:.1f}"
    return f"M {f(p0)} C {f(c1)} {f(c2)} {f(tip)} C {f(c3)} {f(c4)} {f(p0)} Z"


# 1. word-fill statement
s = open(os.path.join(comp, "mk-callout-highlight.html")).read()
s = s.replace('scheme: "light"', f'scheme: "{style["scheme"]}"').replace('text: "Functionality was our goal from the very beginning"', f'text: {json.dumps(style["statement"])}')
s = s.replace("fontSize: 60,", f'fontSize: {style.get("fontSize", 72)},').replace("maxWidth: 700,", "maxWidth: 1500,").replace("x: 1030,", "x: null,").replace('align: "left"', 'align: "center"')
s = s.replace("sweep: { start: 1.2, end: 6.2 }", "sweep: { start: 0.9, end: 3.9 }").replace("var DUR = 8;", "var DUR = 5;")
s = s.replace('"#1d1d1f"', json.dumps(style["ink"])).replace('"#bcbcc2"', json.dumps(style["ink_faint"])).replace('"#f5f5f7"', json.dumps(style["ink"])).replace('"rgba(245,245,247,0.32)"', json.dumps(style["ink_faint"]))
open(os.path.join(comp, "mk-callout-highlight.html"), "w").write(s)

# 2. own five-petal mark replaces the vendor logo; brand colours, tagline, url, stage
s = open(os.path.join(comp, "logo-outro.html")).read()
start, end = s.index('<svg viewBox="0 0 160 240"'), s.index("</svg>") + len("</svg>")
names, angles = ["logo-tl", "logo-tr", "logo-ml", "logo-mr", "logo-bl"], [-56, 56, -28, 28, 0]
paths = "\n".join(f'            <path class="logo-piece {n}" d="{petal(a)}" fill="{c}" />' for n, a, c in zip(names, angles, style["mark_colours"]))
s = s[:start] + f'<svg viewBox="0 0 160 240" width="160" height="240" class="logo-svg">\n{paths}\n          </svg>' + s[end:]
s = s.replace("Nothing great is made alone.", style["tagline"]).replace("figma.com", style["url"])
for old, new in (("#0a0a0f", style["stage"]), ("#1a1a1f", style["stage_2"])):
    s = s.replace(old, new)
s = s.replace("color: white;", f'color: {style["ink"]};').replace("color: #666;", f'color: {style.get("url_ink", style["ink"])};')
s = s.replace("border: 1px solid #2c2c2c", f'border: 1px solid {style.get("pill_border", "#2c2c2c")}')
s = s.replace("rgba(162, 89, 255, 0.25)", style.get("glow", "rgba(162, 89, 255, 0.25)"))
open(os.path.join(comp, "logo-outro.html"), "w").write(s)

# 3. root: field + statement, then the mark
field_vars = json.dumps(style["field"]).replace("'", "&#39;")
html = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: {style["stage"]}; }}
      #root {{ position: relative; width: 100%; height: 100%; background: {style["stage"]}; }}
      #halftone-field {{ z-index: 1; opacity: {style.get("field_opacity", 1)}; }}
      #mk-callout-highlight {{ z-index: 2; }}
      #logo-outro {{ z-index: 3; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="11" data-width="1920" data-height="1080">
      <div id="halftone-field" data-composition-id="halftone-field" data-composition-src="compositions/halftone-field.html" data-start="0" data-duration="5.2" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080" data-variable-values='{field_vars}'></div>
      <div id="mk-callout-highlight" data-composition-id="mk-callout-highlight" data-composition-src="compositions/mk-callout-highlight.html" data-start="0" data-duration="5" data-track-index="2" data-track-kind="graphics" data-width="1920" data-height="1080"></div>
      <div id="logo-outro" data-composition-id="logo-outro" data-composition-src="compositions/logo-outro.html" data-start="5" data-duration="6" data-track-index="3" data-track-kind="graphics" data-width="1920" data-height="1080"></div>
    </div>
    <script>window.__timelines["main"] = gsap.timeline({{ paused: true }});</script>
  </body>
</html>
'''
open(os.path.join(out, "index.html"), "w").write(html)
print("built", out)
