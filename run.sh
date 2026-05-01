#!/bin/bash
# Arbeitsverzeichnis = Ordner dieses Scripts
cd "$(dirname "$0")"

LOG="logs/monitor.log"
echo "──────────────────────────────────────" >> "$LOG"
echo "START: $(date '+%Y-%m-%d %H:%M:%S')"   >> "$LOG"

python3 monitor.py >> "$LOG" 2>&1
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  echo "ENDE:  $(date '+%Y-%m-%d %H:%M:%S') — OK" >> "$LOG"
else
  echo "ENDE:  $(date '+%Y-%m-%d %H:%M:%S') — FEHLER (Exit $EXIT_CODE)" >> "$LOG"
fi
