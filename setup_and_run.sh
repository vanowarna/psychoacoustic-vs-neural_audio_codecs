#!/usr/bin/env bash

# =========================
# Safe Bash Settings
# =========================
set -o pipefail
set -o nounset

echo "=============================="
echo " Setup + Run Pipeline Started "
echo "=============================="

# =========================
# Helper: retry function
# =========================
retry() {
    local n=0
    local max=3
    local delay=3

    until "$@"; do
        ((n++))
        if ((n >= max)); then
            echo "❌ Command failed after $n attempts: $*"
            return 1
        fi
        echo "⚠️ Retry $n/$max: $*"
        sleep $delay
    done
}

# =========================
# System Dependencies
# =========================
echo "🔄 Updating system..."
retry sudo apt-get update || echo "⚠️ apt update failed"

echo "📦 Installing system dependencies..."
retry sudo apt-get install -y ffmpeg libsndfile1 || echo "⚠️ system install failed"

# =========================
# Python Dependencies
# =========================
echo "⬆️ Upgrading pip..."
retry python3 -m pip install --upgrade pip || echo "⚠️ pip upgrade failed"

echo "📦 Installing Python packages..."
retry pip install \
    torch \
    torchaudio \
    pydub \
    encodec \
    numpy \
    scipy \
    matplotlib \
    librosa \
    soundfile \
    || echo "⚠️ some pip installs failed"

# =========================
# Create Output Folders
# =========================
echo "📁 Ensuring output directories exist..."

create_dir_if_missing() {
    if [ ! -d "$1" ]; then
        mkdir -p "$1"
        echo "✅ Created: $1"
    else
        echo "✔️ Exists: $1"
    fi
}

create_dir_if_missing "export-output/traditional-coding"
create_dir_if_missing "export-output/neural-coding"
# # =========================
# # Run Scripts
# # =========================
# echo "🚀 Running Traditional Codec Sweep..."
# if python scripts/traditional-coding-sweep.py; then
#     echo "✅ Traditional sweep completed"
# else
#     echo "⚠️ Traditional sweep failed, continuing..."
# fi

# echo "🚀 Running Neural Codec Sweep..."
# if python scripts/neural-coding-sweep.py; then
#     echo "✅ Neural sweep completed"
# else
#     echo "⚠️ Neural sweep failed, continuing..."
# fi

# # =========================
# # Done
# # =========================
# echo "=============================="
# echo " ✅ Pipeline Finished "
# echo "📁 Outputs available in: export-output/"
# echo "=============================="