import os
import torch
import soundfile as sf
from encodec import EncodecModel
from encodec.utils import convert_audio

def compress_neural_sweep(input_wav, track_name, bandwidths=[1.5, 3.0, 6.0, 12.0, 24.0]):
    """
    Compresses and reconstructs audio using Meta's EnCodec model
    across 5 supported ultra-low bandwidths.
    """
    print("--- Processing Neural Codec ---")

    device = torch.device("cpu")

    # Initialize the pre-trained 24kHz model on CPU
    model = EncodecModel.encodec_model_24khz().to(device)
    model.eval()

    # Ensure output directory exists (per-track subdirectory)
    track_dir = f"export-output/neural-coding/{track_name}_neural"
    os.makedirs(track_dir, exist_ok=True)

    # Load audio with soundfile (avoids torchaudio/torchcodec)
    wav_np, sr = sf.read(input_wav, always_2d=True)

    # Convert to torch tensor: [channels, time]
    wav = torch.from_numpy(wav_np.T).float().to(device)

    # Resample / convert to model format
    wav = convert_audio(wav, sr, model.sample_rate, model.channels)
    wav = wav.unsqueeze(0)  # [batch, channels, time]

    recon_files = {"neural": {}}

    for bw in bandwidths:
        print(f"Encoding at {bw} kbps...")
        model.set_target_bandwidth(bw)

        with torch.no_grad():
            encoded_frames = model.encode(wav)

        with torch.no_grad():
            reconstructed_wav = model.decode(encoded_frames)

        # Convert back to [time, channels] for soundfile
        reconstructed_wav = reconstructed_wav.squeeze(0).cpu().numpy().T

        neural_recon_path = f"{track_dir}/recon_{track_name}_neural_{bw}k.wav"
        sf.write(neural_recon_path, reconstructed_wav, model.sample_rate)

        recon_files["neural"][f"{int(bw)}k"] = neural_recon_path

    print("Neural compression sweep complete.\n")
    return recon_files


neural_files = compress_neural_sweep("source-audio/27.flac", "track-27")
print(neural_files)

neural_files = compress_neural_sweep("source-audio/49.flac", "track-49")
print(neural_files)

neural_files = compress_neural_sweep("source-audio/69.flac", "track-69")
print(neural_files)