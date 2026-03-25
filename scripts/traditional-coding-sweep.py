import os
from pydub import AudioSegment
def compress_traditional_sweep(input_wav, track_name, bitrates=["8k", "12k", "24k", "48k", "64k"]):
    """
    Compresses a WAV file to MP3 and AAC across 5 bitrates,
    then decodes them back to WAV for mathematical analysis.
    """
    print("--- Processing Traditional Codecs ---")
    audio = AudioSegment.from_file(input_wav)
    recon_files = {"mp3": {}, "aac": {}}
    
    for br in bitrates:
        print(f"Encoding at {br}bps...")
        
        # MP3 Processing
        mp3_path = f"export-output/traditional-coding/temp_{br}.mp3"
        mp3_recon = f"export-output/traditional-coding/recon_{track_name}_mp3_{br}.wav"
        audio.export(mp3_path, format="mp3", bitrate=br)
        AudioSegment.from_mp3(mp3_path).export(mp3_recon, format="wav")
        recon_files["mp3"][br] = mp3_recon
        
        # AAC Processing (requires ffmpeg installed on OS)
        aac_path = f"export-output/traditional-coding/temp_{br}.aac"
        aac_recon = f"export-output/traditional-coding/recon_{track_name}_aac_{br}.wav"
        audio.export(aac_path, format="adts", bitrate=br)
        AudioSegment.from_file(aac_path, format="aac").export(aac_recon, format="wav")
        recon_files["aac"][br] = aac_recon
        
        # Clean up the compressed files to save disk space
        os.remove(mp3_path)
        os.remove(aac_path)
        
    print("Traditional compression sweep complete.\n")
    return recon_files

# Run the function on your chosen audio file
trad_files = compress_traditional_sweep("source-audio/27.flac", "track-27")
print(trad_files)
trad_files = compress_traditional_sweep("source-audio/49.flac", "track-49")
print(trad_files)
trad_files = compress_traditional_sweep("source-audio/69.flac", "track-69")
print(trad_files)