#!/usr/bin/env bash
# Rolex installer: copies skills/agents into ~/.claude and installs Claude Code plugins + MCP servers.
# Pack line types: skill | agent | setup | bundle | plugin | mcp | fetch <skill> <owner/repo> <path-in-repo>
# Usage: bash install.sh [--packs core,blender,...] [--all] [--tools] [--dry-run] [--list]
set -euo pipefail

REPO_URL="https://github.com/titirshu-mannjal/Rolex.git"
CLAUDE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
export ROLEX_SKILLS_DIR="$CLAUDE_DIR/skills"   # used by repo-line install commands in packs/
PACKS="core"; TOOLS=0; DRY=0; LIST=0

while [ $# -gt 0 ]; do
  case "$1" in
    --packs) PACKS="$2"; shift ;;
    --packs=*) PACKS="${1#*=}" ;;
    --all) PACKS="all" ;;
    --tools) TOOLS=1 ;;
    --dry-run) DRY=1 ;;
    --list) LIST=1 ;;
    -h|--help) sed -n '2,3p' "$0"; exit 0 ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
  shift
done

# The plugin marketplace is read from a local copy of this repo, so that copy must stay put.
# Piped from curl: keep a shallow clone at ~/.local/share/rolex/repo (updated on every run).
DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/rolex"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || true)"
if [ ! -d "$SRC/packs" ]; then
  command -v git >/dev/null || { echo "git is required" >&2; exit 1; }
  SRC="$DATA_DIR/repo"
  if [ -d "$SRC/.git" ]; then
    echo "Updating $SRC"; git -C "$SRC" fetch -q --depth 1 origin main && git -C "$SRC" reset -q --hard origin/main
  else
    echo "Downloading Rolex (about 1.5 GB) to $SRC"; mkdir -p "$DATA_DIR"; git clone --depth 1 -q "$REPO_URL" "$SRC"
  fi
fi

[ "$PACKS" = "all" ] && PACKS="$(ls "$SRC/packs" | sed 's/\.txt$//' | paste -sd, -)"

if [ $LIST -eq 1 ]; then
  for f in "$SRC"/packs/*.txt; do printf '%-14s %s\n' "$(basename "$f" .txt)" "$(head -1 "$f" | sed 's/^# //')"; done
  exit 0
fi

run() { if [ $DRY -eq 1 ]; then echo "  [dry-run] $*"; else "$@"; fi; }
STAMP="$(date +%Y%m%d-%H%M%S)"; BACKUP="$CLAUDE_DIR/rolex-backup/$STAMP"
ok=0; skipped=0; failed=()

# Replace a destination, keeping the old copy in a timestamped backup (never deletes user data).
place() {
  local from="$1" to="$2"
  if [ -e "$to" ]; then run mkdir -p "$BACKUP/$(basename "$(dirname "$to")")"; run mv "$to" "$BACKUP/$(basename "$(dirname "$to")")/"; fi
  run cp -R "$from" "$to"
}

HAVE_CLAUDE=0; command -v claude >/dev/null && HAVE_CLAUDE=1
[ $HAVE_CLAUDE -eq 0 ] && echo "! 'claude' CLI not found: skills will be copied, plugins and MCP servers skipped. Install Claude Code, then re-run."
HAVE_PLUGINS=" "; [ $HAVE_CLAUDE -eq 1 ] && HAVE_PLUGINS=" $(claude plugin list </dev/null 2>/dev/null | sed -n 's/^ *❯ *\([^ ]*@[^ ]*\).*/\1/p' | tr '\n' ' ')"
WORK="$(mktemp -d)"; ADDED_MKT=" "   # bash 3.2 (macOS) has no associative arrays

run mkdir -p "$CLAUDE_DIR/skills" "$CLAUDE_DIR/agents"
IFS=',' read -ra PACK_LIST <<< "$PACKS"
for pack in "${PACK_LIST[@]}"; do
  file="$SRC/packs/$pack.txt"
  [ -f "$file" ] || { echo "Unknown pack: $pack (try --list)" >&2; exit 1; }
  echo "== Pack: $pack"
  while read -r kind a b rest; do
    case "$kind" in
      ''|'#'*) continue ;;
      skill)
        place "$SRC/skills/$a" "$CLAUDE_DIR/skills/$a" && ok=$((ok+1)) || failed+=("skill $a") ;;
      agent)
        place "$SRC/agents/$a" "$CLAUDE_DIR/agents/$a" && ok=$((ok+1)) || failed+=("agent $a") ;;
      fetch)
        # A skill installed straight from its GitHub repo at install time (not redistributed here): fetch <skill> <owner/repo> <path>
        if [ $DRY -eq 1 ]; then echo "  [dry-run] fetch $a from $b/$rest"; ok=$((ok+1))
        elif git clone -q --depth 1 "https://github.com/$b" "$WORK/fetch-$a" </dev/null >/dev/null 2>&1 && place "$WORK/fetch-$a/$rest" "$CLAUDE_DIR/skills/$a"; then ok=$((ok+1))
        else failed+=("fetch $a"); fi ;;
      setup)
        # Run a one-time setup (e.g. npm install) inside an installed skill folder.
        if [ $DRY -eq 1 ]; then echo "  [dry-run] (cd skills/$a && $b $rest)"; ok=$((ok+1))
        elif (cd "$CLAUDE_DIR/skills/$a" && bash -c "$b $rest") </dev/null >"$WORK/setup-$a.log" 2>&1; then echo "  + setup $a"; ok=$((ok+1))
        else cp "$WORK/setup-$a.log" "$CLAUDE_DIR/rolex-setup-$a.log" 2>/dev/null; failed+=("setup $a (log: $CLAUDE_DIR/rolex-setup-$a.log)"); fi ;;
      bundle)
        # Tools that need their own folder (a library beside the skills): copy from tools/ and run their installer.
        dir="$DATA_DIR/$b"
        run rm -rf "$dir"; run mkdir -p "$DATA_DIR"; run cp -R "$SRC/tools/$a" "$dir"
        if [ $DRY -eq 1 ]; then echo "  [dry-run] (cd $dir && $rest)"; ok=$((ok+1))
        elif (cd "$dir" && bash -c "$rest") </dev/null >"$WORK/$b.log" 2>&1; then echo "  + $b"; ok=$((ok+1))
        else cp "$WORK/$b.log" "$CLAUDE_DIR/rolex-$b-install.log" 2>/dev/null; failed+=("$b (log: $CLAUDE_DIR/rolex-$b-install.log)"); fi ;;
      plugin)
        [ $HAVE_CLAUDE -eq 1 ] || { skipped=$((skipped+1)); continue; }
        mkt="${b#*@}"
        # Same plugin already installed from its original marketplace: keep it, so skills don't load twice.
        case "$HAVE_PLUGINS" in *" ${b%@*}@"*) case "$HAVE_PLUGINS" in *" $b "*) ;; *) echo "  = plugin ${b%@*} (already installed)"; continue ;; esac ;; esac
        [ "$a" = "@rolex" ] && a="${ROLEX_MARKETPLACE:-$SRC}"   # this repo (local copy) is the marketplace; avoids a second 1.5 GB download
        case "$ADDED_MKT" in *" $mkt "*) ;; *)
          run claude plugin marketplace add "$a" </dev/null >/dev/null 2>&1 || run claude plugin marketplace update "$mkt" </dev/null >/dev/null 2>&1 || true   # already added: refresh it
          ADDED_MKT="$ADDED_MKT$mkt " ;;
        esac
        if run claude plugin install "$b" </dev/null >/dev/null 2>&1; then echo "  + plugin $b"; ok=$((ok+1)); else failed+=("plugin $b"); fi ;;
      mcp)
        [ $HAVE_CLAUDE -eq 1 ] || { skipped=$((skipped+1)); continue; }
        if claude mcp get "$a" </dev/null >/dev/null 2>&1; then echo "  = mcp $a (already set)"; continue; fi
        # shellcheck disable=SC2086
        if run claude mcp add --scope user "$a" -- $rest </dev/null >/dev/null 2>&1; then echo "  + mcp $a"; ok=$((ok+1)); else failed+=("mcp $a"); fi ;;
      *) failed+=("bad line: $kind $a") ;;
    esac
  done < "$file"
done
rm -rf "$WORK"

if [ $TOOLS -eq 1 ]; then
  echo "== Command-line tools"
  if command -v uv >/dev/null; then
    for t in yt-dlp auto-editor whisper-ctranslate2 edge-tts depthflow "rembg[cpu,cli]" "earshot[listen,mcp,images] @ git+https://github.com/Leonxlnx/earshot"; do
      run uv tool install -q "$t" </dev/null >/dev/null 2>&1 && echo "  + $t" || echo "  ! $t failed (install it by hand)"
    done
  else
    echo "  ! uv not found. Install it (https://docs.astral.sh/uv/) and re-run with --tools."
  fi
  # Real-ESRGAN upscaler (GPU via Vulkan, no Python). Last prebuilt release upstream is v0.2.5.0.
  case "$(uname -s)" in
    Linux) RE=ubuntu ;; Darwin) RE=macos ;; *) RE=windows ;;
  esac
  RED="${XDG_DATA_HOME:-$HOME/.local/share}/realesrgan"
  if [ -x "$RED/realesrgan-ncnn-vulkan" ] || [ -f "$RED/realesrgan-ncnn-vulkan.exe" ]; then echo "  = realesrgan-ncnn-vulkan"
  elif run curl -fsSL -o "/tmp/realesrgan-$$.zip" "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-$RE.zip" \
    && run mkdir -p "$RED" && run python3 -c "import zipfile,sys;zipfile.ZipFile(sys.argv[1]).extractall(sys.argv[2])" "/tmp/realesrgan-$$.zip" "$RED"; then
    run chmod +x "$RED/realesrgan-ncnn-vulkan" 2>/dev/null || true
    run mkdir -p "$HOME/.local/bin"; run ln -sf "$RED/realesrgan-ncnn-vulkan" "$HOME/.local/bin/realesrgan-ncnn-vulkan"
    rm -f "/tmp/realesrgan-$$.zip"; echo "  + realesrgan-ncnn-vulkan (models in $RED/models)"
  else echo "  ! realesrgan-ncnn-vulkan failed (install it by hand)"; fi
  # Local voiceover engines (Apache-2.0 Kokoro with Indian voices hm_omega/hm_psi/hf_alpha/hf_beta; MIT Chatterbox for
  # consented voice cloning; Demucs to separate a reference voice; DeepFilterNet to clean real recordings). One venv; use it as: ~/.local/share/rolex/tts/.venv/bin/python
  TTS="${XDG_DATA_HOME:-$HOME/.local/share}/rolex/tts"
  if command -v uv >/dev/null; then
    run mkdir -p "$TTS" && run uv venv -q --allow-existing --python 3.11 "$TTS/.venv" </dev/null >/dev/null 2>&1 \
    && run uv pip install -q --python "$TTS/.venv/bin/python" "kokoro>=0.9" soundfile chatterbox-tts demucs deepfilternet \
       "en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl" </dev/null >/dev/null 2>&1 \
    && echo "  + voice engines (Kokoro, Chatterbox) -> $TTS/.venv" || echo "  ! voice engines failed (see README)"
  fi
  # Editorial fonts (SIL OFL, bundled in assets/fonts).
  case "$(uname -s)" in Darwin) FD="$HOME/Library/Fonts" ;; *) FD="$HOME/.local/share/fonts/rolex" ;; esac
  run mkdir -p "$FD" && run cp "$SRC"/assets/fonts/*.ttf "$FD"/ && { command -v fc-cache >/dev/null && run fc-cache -f >/dev/null 2>&1; echo "  + fonts -> $FD"; }
fi

echo "== Checking system tools"
for t in ffmpeg ffprobe node npx python3 git uv; do
  command -v "$t" >/dev/null && printf '  ok %s\n' "$t" || printf '  MISSING %s\n' "$t"
done

echo
echo "Done: $ok installed, $skipped skipped, ${#failed[@]} failed."
[ ${#failed[@]} -gt 0 ] && printf '  failed: %s\n' "${failed[@]}"
[ -d "$BACKUP" ] && echo "Replaced items were backed up to $BACKUP"
echo "Restart Claude Code so it loads the new skills and plugins."
