#!/bin/bash
set -euo pipefail

INTERVAL=10
STATE="/home/roruck/iotcam/last_capture_time.txt"
DIR="/home/roruck/iotcam/motion_pics"
LOG="/home/roruck/iotcam/capture_event.log"
URL="http://192.168.18.24/capture"

exec 9>/tmp/iotcam_capture_event.lock
if ! flock -n 9; then
  exit 0
fi

NOW="$(date +%s)"
LAST="$(cat "$STATE" 2>/dev/null || echo 0)"

if (( NOW - LAST < INTERVAL )); then
  echo "$(date '+%F %T') SKIP cooldown" >> "$LOG"
  exit 0
fi

mkdir -p "$DIR"

DATE="$(date '+%Y%m%d_%H%M%S')"
TMP="${DIR}/tmp_${DATE}.jpg"
FILE="${DIR}/${DATE}.jpg"

curl -s --max-time 5 -o "$TMP" "$URL"

if [[ -s "$TMP" ]]; then
  mv "$TMP" "$FILE"
  echo "$NOW" > "$STATE"
  echo "$(date '+%F %T') SAVED ${FILE}" >> "$LOG"
else
  rm -f "$TMP"
  echo "$(date '+%F %T') ERROR empty capture" >> "$LOG"
fi
