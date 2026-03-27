#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "=== Checking ffmpeg ==="
if ! command -v ffmpeg >/dev/null 2>&1; then
  if command -v brew >/dev/null 2>&1; then
    echo "ffmpeg not found; installing via Homebrew..."
    brew install ffmpeg
  else
    echo "[ERROR] ffmpeg is required. Install Homebrew from https://brew.sh then run: brew install ffmpeg"
    exit 1
  fi
fi

echo "=== Creating virtual environment (if needed) ==="
if [ ! -x ".venv/bin/python" ]; then
  python3 -m venv .venv
fi
if [ ! -x ".venv/bin/python" ]; then
  echo "[ERROR] Failed to create .venv. Ensure Python 3 and the venv module are installed (e.g., reinstall Python via Homebrew)."
  exit 1
fi

echo "=== Activating virtual environment ==="
source .venv/bin/activate

echo "=== Installing Python dependencies ==="
python -m pip install --upgrade pip || { echo "[ERROR] Failed to upgrade pip"; exit 1; }
python -m pip install -r requirements.txt || { echo "[ERROR] Failed to install Python dependencies from requirements.txt"; exit 1; }

echo "=== Running traditional coding sweep ==="
python scripts/traditional-coding-sweep.py

echo "=== Running neural coding sweep ==="
python scripts/neural-coding-sweep.py

echo "=== Running objective evaluation ==="
python scripts/objective-evaluation.py

echo "=== All steps completed ==="
