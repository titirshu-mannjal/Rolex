#!/usr/bin/env bash
# Create (or open) a client profile: new_client.sh <client-slug>
# Lives in ~/.claude/motion-kit/brands/<slug>/ (Edit-Kit reads brand.json there); productions go in productions/<slug>/.
set -euo pipefail
SLUG="$(echo "${1:?usage: new_client.sh <client-slug>}" | tr 'A-Z ' 'a-z-')"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DST="$HOME/.claude/motion-kit/brands/$SLUG"
if [ -d "$DST" ]; then echo "exists: $DST"; else mkdir -p "$(dirname "$DST")"; cp -R "$HERE/../template" "$DST"; sed -i "s/\"Client name\"/\"$SLUG\"/" "$DST/brand.json"; echo "created: $DST"; fi
ROLEX="${ROLEX_DIR:-$HOME/Desktop/Rolex}"
if [ -d "$ROLEX" ]; then mkdir -p "$ROLEX/productions/$SLUG"; echo "productions: $ROLEX/productions/$SLUG"; fi
