# Quick Guide: Running on Google Colab

## 1. Upload Files to Colab

After opening `scripts/colab_pipeline.ipynb` in Google Colab:

1. Click the **folder icon** on the left sidebar to open the file browser
2. Create a folder called `source-audio/`
3. Upload your source FLAC files into it:
   ```
   source-audio/27.flac
   source-audio/49.flac
   source-audio/69.flac
   ```

## 2. Run the Notebook

Run each cell **top to bottom** in order:

| Cell | What it does |
|------|-------------|
| Setup | Installs ffmpeg and Python libraries |
| Upload check | Creates directories, verifies your audio files are in place |
| Step 1 | Traditional codec sweep (MP3 & AAC at 5 bitrates) |
| Step 2 | Neural codec sweep (EnCodec at 5 bandwidths) |
| Step 3 | Computes SNR and displays rate-distortion plots inline |
| Download | Zips all outputs for easy download |

## 3. Collect Outputs

After all cells complete, the output structure will be:

```
export-output/
├── traditional-coding/
│   ├── track-27_trad/
│   │   ├── recon_track-27_mp3_8k.wav
│   │   ├── recon_track-27_aac_8k.wav
│   │   └── ... (10 files per track)
│   ├── track-49_trad/
│   └── track-69_trad/
├── neural-coding/
│   ├── track-27_neural/
│   │   ├── recon_track-27_neural_1.5k.wav
│   │   └── ... (5 files per track)
│   ├── track-49_neural/
│   └── track-69_neural/
└── plots/
    ├── rd_curve_track_27.png
    ├── rd_curve_track_49.png
    └── rd_curve_track_69.png
```

Run the **last cell** to create `export-output.zip`, then download it from the Colab file browser.

## Running Locally Instead

```bash
chmod +x setup_and_run.sh
./setup_and_run.sh
```

This runs the same pipeline without needing Colab.
