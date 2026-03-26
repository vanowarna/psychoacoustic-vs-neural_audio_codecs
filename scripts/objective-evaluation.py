from pathlib import Path
import re
from math import gcd

import numpy as np
import soundfile as sf
from scipy.signal import resample_poly
import matplotlib.pyplot as plt


def _to_mono(audio: np.ndarray) -> np.ndarray:
    if audio.ndim > 1:
        audio = audio.mean(axis=1)
    return audio.astype(np.float32)


def _resample_audio(audio: np.ndarray, src_sr: int, target_sr: int) -> np.ndarray:
    if src_sr == target_sr:
        return audio.astype(np.float32)

    factor = gcd(src_sr, target_sr)
    up = target_sr // factor
    down = src_sr // factor
    return resample_poly(audio.astype(np.float32), up, down)


def calculate_snr(original_file, recon_file):
    """Calculates SNR between original and reconstructed audio in dB."""
    orig_audio, sr_orig = sf.read(str(original_file))
    recon_audio, sr_recon = sf.read(str(recon_file))

    orig_audio = _to_mono(orig_audio)
    recon_audio = _to_mono(recon_audio)

    # Match sample rates before comparing
    if sr_recon != sr_orig:
        recon_audio = _resample_audio(recon_audio, sr_recon, sr_orig)

    # Align lengths
    min_len = min(len(orig_audio), len(recon_audio))
    orig_audio = orig_audio[:min_len]
    recon_audio = recon_audio[:min_len]

    signal_power = np.sum(orig_audio ** 2)
    noise_power = np.sum((orig_audio - recon_audio) ** 2)

    if noise_power == 0:
        return float("inf")

    return 10 * np.log10(signal_power / noise_power)


def _get_track_id(original_wav):
    name = Path(original_wav).stem
    m = re.search(r"(\d+)", name)
    if not m:
        raise ValueError(f"Cannot extract track id from: {original_wav}")
    return m.group(1)


def _first_existing_path(paths):
    for p in paths:
        if p.exists():
            return p
    return None


def _traditional_candidates(base_dir, track_id, codec, bitrate):
    return [
        base_dir / f"recon_track-{track_id}_{codec}_{bitrate}k.wav",
        base_dir / f"recon_track-{track_id}_{codec}_{float(bitrate):.1f}k.wav",
        base_dir / f"recon_track-{track_id}_{codec}_{float(bitrate):g}k.wav",
    ]


def _neural_candidates(base_dir, track_id, bitrate):
    b = float(bitrate)
    variants = []

    if b.is_integer():
        variants.extend([f"{int(b)}k", f"{b:.1f}k", f"{b:g}k"])
    else:
        variants.extend([f"{b:.1f}k", f"{b:g}k"])

    variants = list(dict.fromkeys(variants))
    return [base_dir / f"recon_track-{track_id}_neural_{v}.wav" for v in variants]


def _build_file_lists(original_wav):
    track_id = _get_track_id(original_wav)

    trad_base = Path("export-output/traditional-coding") / f"track-{track_id}_trad"
    neural_base = Path("export-output/neural-coding") / f"track-{track_id}_neural"

    trad_bitrates = [8, 12, 24, 48, 64]
    neural_bitrates = [1.5, 3, 6, 12, 24]

    mp3_files = []
    aac_files = []
    neural_files = []

    for b in trad_bitrates:
        mp3_path = _first_existing_path(_traditional_candidates(trad_base, track_id, "mp3", b))
        aac_path = _first_existing_path(_traditional_candidates(trad_base, track_id, "aac", b))

        if mp3_path is None:
            raise FileNotFoundError(f"Missing MP3 file for {b} kbps in: {trad_base}")
        if aac_path is None:
            raise FileNotFoundError(f"Missing AAC file for {b} kbps in: {trad_base}")

        mp3_files.append(mp3_path)
        aac_files.append(aac_path)

    for b in neural_bitrates:
        neural_path = _first_existing_path(_neural_candidates(neural_base, track_id, b))
        if neural_path is None:
            raise FileNotFoundError(f"Missing neural file for {b} kbps in: {neural_base}")
        neural_files.append(neural_path)

    return trad_bitrates, neural_bitrates, {"mp3": mp3_files, "aac": aac_files}, {"neural": neural_files}


def plot_rd_curve(original_wav):
    """Plots the Rate-Distortion (SNR) curve for MP3, AAC, and neural codec."""
    trad_x, neural_x, trad_files, neural_files = _build_file_lists(original_wav)

    mp3_y = [calculate_snr(original_wav, path) for path in trad_files["mp3"]]
    aac_y = [calculate_snr(original_wav, path) for path in trad_files["aac"]]
    neural_y = [calculate_snr(original_wav, path) for path in neural_files["neural"]]

    plt.figure(figsize=(10, 6))
    plt.plot(trad_x, mp3_y, marker="o", linestyle="-", label="MP3 (MPEG-1 Layer 3)")
    plt.plot(trad_x, aac_y, marker="s", linestyle="--", label="AAC (MPEG-2/4)")
    plt.plot(neural_x, neural_y, marker="^", linestyle="-.", label="Neural (Meta EnCodec)")

    track_id = _get_track_id(original_wav)
    plt.title(f"Rate-Distortion Curve: Objective SNR vs. Bitrate | Track-{track_id}")
    plt.xlabel("Bitrate (kbps)")
    plt.ylabel("Signal-to-Noise Ratio (dB)")
    plt.grid(True)
    plt.legend(loc="upper left", frameon=True)
    plt.xlim(0, 66)
    plt.ylim(-5, 17.5)
    plot_dir = Path("export-output/plots")
    plot_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(plot_dir / f"rd_curve_track_{track_id}.png", dpi=300, bbox_inches="tight")
    # plt.show()

# Plotting
plot_rd_curve("source-audio/27.flac")
plot_rd_curve("source-audio/49.flac")
plot_rd_curve("source-audio/69.flac")