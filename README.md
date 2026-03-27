# Psychoacoustic vs. Neural Audio Codecs

Comparative analysis of traditional psychoacoustic codecs (MP3, AAC) and neural audio codecs (Meta EnCodec) across multiple bitrates, evaluated using objective SNR metrics.

## Project Structure

```
├── source-audio/               # Original FLAC audio tracks (27, 49, 69)
├── scripts/
│   ├── traditional-coding-sweep.py   # MP3 & AAC encoding at 8/12/24/48/64 kbps
│   ├── neural-coding-sweep.py        # EnCodec encoding at 1.5/3/6/12/24 kbps
│   └── objective-evaluation.py       # SNR calculation & rate-distortion plots
├── export-output/
│   ├── traditional-coding/     # Reconstructed WAVs per track (MP3 & AAC)
│   ├── neural-coding/          # Reconstructed WAVs per track (EnCodec)
│   └── plots/                  # Rate-distortion curve PNGs
├── setup_and_run.sh            # One-command setup & execution
└── README.md
```

## Quick Start

### Linux (Ubuntu/Debian)

```bash
chmod +x setup_and_run.sh
./setup_and_run.sh
```

### macOS

```bash
chmod +x setup_and_run_mac.sh
./setup_and_run_mac.sh
```

### Windows (Command Prompt or PowerShell)

```bat
setup_and_run_windows.bat
```

Each script creates a local Python virtual environment, installs dependencies, runs all encoding sweeps, and generates rate-distortion plots in `export-output/plots/`.

## Dependencies

- **System**: ffmpeg (download from https://ffmpeg.org/download.html; package managers: `brew install ffmpeg` on macOS, `choco install ffmpeg` or `winget install --id Gyan.FFmpeg` on Windows)
- **Python**: torch, torchaudio, pydub, encodec, numpy, scipy, matplotlib, librosa, soundfile

## Scripts

### traditional-coding-sweep.py
Encodes source audio to MP3 and AAC at 5 bitrates (8k, 12k, 24k, 48k, 64k), then decodes back to WAV. Output: `export-output/traditional-coding/{track}_trad/`

### neural-coding-sweep.py
Encodes source audio using Meta's EnCodec model at 5 bandwidths (1.5, 3.0, 6.0, 12.0, 24.0 kbps). Output: `export-output/neural-coding/{track}_neural/`

### objective-evaluation.py
Computes SNR between original and reconstructed audio, then plots rate-distortion curves comparing all three codecs. Output: `export-output/plots/`
