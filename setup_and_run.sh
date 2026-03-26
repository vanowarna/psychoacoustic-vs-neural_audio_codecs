#!/bin/bash
set +e  # Continue running even if a command fails

echo "=== Step 1: System packages ==="
sudo apt update
sudo apt install -y ffmpeg

echo "=== Step 2: Python dependencies ==="
pip install torch torchaudio pydub encodec numpy scipy matplotlib librosa soundfile

echo "=== Step 3: Traditional coding sweep ==="
python scripts/traditional-coding-sweep.py

echo "=== Step 4: Neural coding sweep ==="
python scripts/neural-coding-sweep.py

echo "=== Step 5: Objective evaluation ==="
python scripts/objective-evaluation.py

echo "=== All steps completed ==="
