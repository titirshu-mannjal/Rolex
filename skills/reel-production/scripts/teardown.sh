#!/usr/bin/env bash
# Tear down any reference video the user sends, the same way every time.
# Usage: teardown.sh <url-or-file> <out_dir>
# Writes: ref.mp4, probe.txt, f/ (2 fps frames with timestamps), sheet_N.jpg, cuts.txt, audio.wav,
#         transcript.txt (if speech), earshot_critique.txt, earshot_timeline.txt, look.txt
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$1"; [ -f "$SRC" ] && SRC="$(cd "$(dirname "$SRC")" && pwd)/$(basename "$SRC")"
OUT="$2"; mkdir -p "$OUT"; cd "$OUT"
PY="${LOOK_PY:-$HOME/.local/share/uv/tools/rembg/bin/python}"   # any python with numpy + Pillow
if [ -f "$SRC" ]; then cp "$SRC" ref.mp4; else yt-dlp -q --no-warnings -o "ref.%(ext)s" --remux-video mp4 "$SRC"; fi
ffprobe -v error -show_entries format=duration:stream=codec_type,width,height,r_frame_rate -of compact ref.mp4 | tee probe.txt
mkdir -p f; ffmpeg -v error -y -i ref.mp4 -vf "fps=2,scale=320:-1,drawtext=text='%{pts\:hms}':x=4:y=4:fontsize=14:fontcolor=yellow:box=1:boxcolor=black" f/%03d.jpg
ls f/*.jpg | split -l 40 - grp_; i=0; for g in grp_*; do magick montage $(cat "$g") -tile 8x -geometry +2+2 -background black "sheet_$i.jpg"; i=$((i+1)); done; rm -f grp_*
ffmpeg -v error -i ref.mp4 -vf "select='gt(scene,0.22)',metadata=print:file=-" -an -f null - 2>/dev/null | grep -o "pts_time:[0-9.]*" | cut -d: -f2 > cuts.txt || true
echo "cuts: $(wc -l < cuts.txt)"
ffmpeg -v error -y -i ref.mp4 -vn -ac 2 -ar 48000 audio.wav
whisper-ctranslate2 audio.wav --model small --device cpu --compute_type int8 --word_timestamps True --output_format json --output_dir . >/dev/null 2>&1 || true
python3 -c "
import json
d=json.load(open('audio.json')); open('transcript.txt','w').write('\n'.join(f\"{s['start']:6.2f}-{s['end']:6.2f}  {s['text'].strip()}\" for s in d['segments']))" 2>/dev/null || echo "(no speech)" > transcript.txt
earshot critique ref.mp4 --video ref.mp4 --threads 3 > earshot_critique.txt 2>&1 || true
earshot timeline audio.wav --threads 3 > earshot_timeline.txt 2>&1 || true
"$PY" "$HERE/../../premium-product-film/scripts/lookmeter.py" --ref ref.mp4 > look.txt 2>&1 || true
echo "done: read sheet_*.jpg, transcript.txt, earshot_*.txt, look.txt; write teardown.md"
