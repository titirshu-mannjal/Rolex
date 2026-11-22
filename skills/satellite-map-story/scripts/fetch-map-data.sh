#!/usr/bin/env bash
# Fetch base imagery and borders for satellite map shots.
# Usage: fetch-map-data.sh [out_dir] [bbox lonW,latS,lonE,latN] [width_px]
#   default: library/maps  60,5,100,40 (South Asia)  4096
# Imagery: NASA Blue Marble Next Generation via NASA GIBS (public domain, credit "NASA").
# Optional: SOURCE=eox uses EOX Sentinel-2 cloudless 2016 (CC BY 4.0, credit required:
#   "Sentinel-2 cloudless - https://s2maps.eu by EOX IT Services GmbH (Contains modified Copernicus Sentinel data 2016)").
#   EOX layers from 2018 onward are CC BY-NC-SA: never use them for brand work.
# Borders: Natural Earth 10m (public domain). countries_india_pov = India's official-boundary view.
set -euo pipefail
OUT="${1:-library/maps}"; BBOX="${2:-60,5,100,40}"; W="${3:-4096}"
IFS=, read -r x0 y0 x1 y1 <<<"$BBOX"
H=$(python3 -c "print(round($W*($y1-$y0)/($x1-$x0)))")
mkdir -p "$OUT"; cd "$OUT"
get() { [ -s "$2" ] && echo "= $2" || { curl -fsSL --retry 3 -m 600 -o "$2.part" "$1" && mv "$2.part" "$2" && echo "+ $2"; }; }
if [ "${SOURCE:-nasa}" = eox ]; then
  URL="https://tiles.maps.eox.at/wms?SERVICE=WMS&REQUEST=GetMap&VERSION=1.1.1&LAYERS=s2cloudless&SRS=EPSG:4326&BBOX=$BBOX&WIDTH=$W&HEIGHT=$H&FORMAT=image/jpeg"
else
  URL="https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?SERVICE=WMS&REQUEST=GetMap&VERSION=1.1.1&LAYERS=BlueMarble_NextGeneration&SRS=EPSG:4326&BBOX=$BBOX&WIDTH=$W&HEIGHT=$H&FORMAT=image/jpeg"
fi
get "$URL" "sat_${SOURCE:-nasa}_${BBOX//,/_}_${W}.jpg"
NE=https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson
get "$NE/ne_10m_admin_0_countries_ind.geojson" countries_india_pov.geojson
get "$NE/ne_10m_admin_1_states_provinces.geojson" states_world.geojson
get "$NE/ne_10m_populated_places_simple.geojson" places.geojson
echo "Done: $(pwd)  (image is plate carree: x=lon, y=lat linear over the bbox)"
