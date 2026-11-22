#!/usr/bin/env bash
# Rolex installer: copies skills/agents into ~/.claude and installs Claude Code plugins + MCP servers.
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

# Piped from curl: fetch the repo first, then run the real copy.
SRC="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || true)"
if [ ! -d "$SRC/packs" ]; then
  command -v git >/dev/null || { echo "git is required" >&2; exit 1; }
  TMP_REPO="$(mktemp -d)"; trap 'rm -rf "$TMP_REPO"' EXIT
  git clone --depth 1 -q "$REPO_URL" "$TMP_REPO"
  SRC="$TMP_REPO"
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
WORK="$(mktemp -d)"; DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/rolex"; ADDED_MKT=" "   # bash 3.2 (macOS) has no associative arrays

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
        [ "$a" = "@rolex" ] && a="${ROLEX_MARKETPLACE:-titirshu-mannjal/Rolex}"   # this repo is the marketplace
        case "$ADDED_MKT" in *" $mkt "*) ;; *)
          run claude plugin marketplace add "$a" </dev/null >/dev/null 2>&1 || true   # already added is fine
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
    for t in yt-dlp auto-editor whisper-ctranslate2 edge-tts depthflow; do
      run uv tool install -q "$t" </dev/null >/dev/null 2>&1 && echo "  + $t" || echo "  ! $t failed (install it by hand)"
    done
  else
    echo "  ! uv not found. Install it (https://docs.astral.sh/uv/) and re-run with --tools."
  fi
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
