import numpy as np
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt
def calculate_snr(original_file, recon_file):
    """Calculates SNR between original and reconstructed audio in Decibels (dB)."""
    sr_orig, orig_audio = wavfile.read(original_file)
    sr_recon, recon_audio = wavfile.read(recon_file)
    
    # Convert to float for accurate math
    orig_audio = orig_audio.astype(np.float32)
    recon_audio = recon_audio.astype(np.float32)
    
    # Mix down to mono for simplicity
    if len(orig_audio.shape) > 1: orig_audio = orig_audio.mean(axis=1)
    if len(recon_audio.shape) > 1: recon_audio = recon_audio.mean(axis=1)
        
    # Align lengths (Naive truncation to handle encoder padding)
    min_len = min(len(orig_audio), len(recon_audio))
    orig_audio, recon_audio = orig_audio[:min_len], recon_audio[:min_len]
    
    # Calculate Power
    signal_power = np.sum(orig_audio ** 2)
    noise_power = np.sum((orig_audio - recon_audio) ** 2)
    
    if noise_power == 0: return float('inf')
    
    return 10 * np.log10(signal_power / noise_power)

def plot_rd_curve(original_wav, trad_files, neural_files):
    """Plots the Rate-Distortion (SNR) curve for all 3 codecs."""
    
    # X-axis Data: Bitrates
    trad_x = [8, 12, 24, 48, 64] 
    neural_x = [1.5, 3, 6, 12, 24]
    
    # Y-axis Data: Calculated SNR
    mp3_y = [calculate_snr(original_wav, path) for path in trad_files["mp3"].values()]
    aac_y = [calculate_snr(original_wav, path) for path in trad_files["aac"].values()]
    neural_y = [calculate_snr(original_wav, path) for path in neural_files["neural"].values()]
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(trad_x, mp3_y, marker='o', linestyle='-', label='MP3 (MPEG-1 Layer 3)')
    plt.plot(trad_x, aac_y, marker='s', linestyle='--', label='AAC (MPEG-2/4)')
    plt.plot(neural_x, neural_y, marker='^', linestyle='-.', label='Neural (Meta EnCodec)')
    
    plt.title("Rate-Distortion Curve: Objective SNR vs. Bitrate")
    plt.xlabel("Bitrate (kbps)")
    plt.ylabel("Signal-to-Noise Ratio (dB)")
    plt.grid(True)
    plt.legend()
    plt.show()
    
# Run the graphing function
# plot_rd_curve("test_audio.wav", trad_files, neural_files)
