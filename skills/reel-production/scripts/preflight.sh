#!/usr/bin/env bash
# Preflight: is every tool the pipeline relies on actually working? Run at the start of a rendering session.
# Prints OK / MISSING / WARN per item with the fix; exits 1 if a required item is missing.
fail=0
ok()   { printf "OK      %-22s %s\n" "$1" "$2"; }
miss() { printf "MISSING %-22s fix: %s\n" "$1" "$2"; fail=1; }
warn() { printf "WARN    %-22s %s\n" "$1" "$2"; }
have() { command -v "$1" >/dev/null 2>&1; }
for t in ffmpeg ffprobe node npx python3 uv magick; do have $t && ok "$t" "" || miss "$t" "install with the OS package manager"; done
have blender && ok blender "$(blender --version 2>/dev/null | head -1)" || miss blender "install Blender 4.2+"
have nvidia-smi && ok gpu "$(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>/dev/null)" || warn gpu "no NVIDIA GPU: Cycles/EEVEE on CPU, slow"
for t in yt-dlp whisper-ctranslate2 rembg realesrgan-ncnn-vulkan depthflow earshot; do have $t && ok "$t" "" || miss "$t" "bash install.sh --tools"; done
V="$HOME/.local/share/rolex/tts/.venv/bin/python"
[ -x "$V" ] && "$V" -c "import kokoro" 2>/dev/null && ok kokoro "voice engine venv" || miss kokoro "bash install.sh --tools"
python3 -c "import PIL, numpy" 2>/dev/null && ok "python pillow+numpy" "" || miss "python pillow+numpy" "sudo pacman -S python-pillow python-numpy (or your OS equivalent)"
[ -f "$HOME/.claude/skills/real-sfx/library_index.json" ] && ok real-sfx "library indexed" || warn real-sfx "run: python3 ~/.claude/skills/real-sfx/scripts/setup.py check"
fc-list | grep -qi "Instrument Serif" && ok fonts "editorial fonts" || warn fonts "bash install.sh --tools (fonts)"
if have voicestudio; then s=$(timeout 20 voicestudio status 2>&1 | tail -1); case "$s" in *"not finished setup"*|*"setup"*) warn voicestudio "installed; finish first-run setup in its window";; *) ok voicestudio "$s";; esac; else warn voicestudio "optional: designed/cloned voices"; fi
[ -n "${HF_TOKEN:-}" ] || [ -s "$HOME/.cache/huggingface/token" ] && ok "hf token" "present (free GPU quota)" || warn "hf token" "optional: free HF token raises Space quota to ~5 GPU-min/day"
[ -d "$HOME/.claude/motion-kit/brands" ] && ok "client profiles" "$(ls "$HOME/.claude/motion-kit/brands" | grep -v '^_template$' | grep -v README | tr '\n' ' ')" || warn "client profiles" "none yet: client-studio/scripts/new_client.sh <name>"
exit $fail
