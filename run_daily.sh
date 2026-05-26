#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="$SCRIPT_DIR/logs"
mkdir -p "$LOG_DIR"

LOG="$LOG_DIR/$(date +%Y-%m-%d).log"

echo "=== $(date) ===" >> "$LOG"

# Activate venv if it exists
if [ -f "$SCRIPT_DIR/.venv/bin/activate" ]; then
  source "$SCRIPT_DIR/.venv/bin/activate"
fi

cd "$SCRIPT_DIR"
python3 -m pip install -q --user -r "$SCRIPT_DIR/requirements.txt" >> "$LOG" 2>&1
python3 daily_email_agent.py "$@" >> "$LOG" 2>&1

echo "Done." >> "$LOG"
