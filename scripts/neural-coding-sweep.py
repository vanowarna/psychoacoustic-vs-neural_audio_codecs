import torch
import torchaudio
from encodec import EncodecModel
from encodec.utils import convert_audio

def compress_neural_sweep(input_wav, track_name, bandwidths=[1.5, 3.0, 6.0, 12.0, 24.0]):
    """
    Compresses and reconstructs audio using Meta's EnCodec model
    across 5 supported ultra-low bandwidths.
    """
    print("--- Processing Neural Codec ---")
    # Initialize the pre-trained 24kHz model
    model = EncodecModel.encodec_model_24khz()
    
    # Load and resample audio to match the neural network's requirement
    wav, sr = torchaudio.load(input_wav)
    wav = convert_audio(wav, sr, model.sample_rate, model.channels)
    wav = wav.unsqueeze(0)  # Add batch dimension for PyTorch: [Batch, Channels, Time]
    
    recon_files = {"neural": {}}
    
    for bw in bandwidths:
        print(f"Encoding at {bw} kbps...")
        model.set_target_bandwidth(bw)
        
        # Encode (Waveform -> Discrete Latent Space Bottleneck)
        with torch.no_grad():
            encoded_frames = model.encode(wav)
            
        # Decode (Latent Space -> Generative Waveform Reconstruction)
        with torch.no_grad():
            reconstructed_wav = model.decode(encoded_frames)
            
        # Save output
        reconstructed_wav = reconstructed_wav.squeeze(0)
        neural_recon_path = f"export-output/neural-coding/recon_{track_name}_neural_{bw}k.wav"
        torchaudio.save(neural_recon_path, reconstructed_wav, model.sample_rate)
        
        recon_files["neural"][f"{int(bw)}k"] = neural_recon_path
        
    print("Neural compression sweep complete.\n")
    return recon_files


# Run the function on your chosen audio file
neural_files = compress_neural_sweep("source-audio/27.flac", "track-27")
print(neural_files)

neural_files = compress_neural_sweep("source-audio/49.flac", "track-49")
print(neural_files)

neural_files = compress_neural_sweep("source-audio/69.flac", "track-69")
print(neural_files)