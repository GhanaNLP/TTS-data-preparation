import os
from pydub import AudioSegment

input_folder = "/media/owusus/Godstestimo/NLP-Projects/asr-datasets/data/youversion/data/mp3"
output_folder = "/media/owusus/Godstestimo/NLP-Projects/asr-datasets/data/youversion/data/wav"

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.lower().endswith(".mp3"):
        mp3_path = os.path.join(input_folder, filename)
        wav_filename = os.path.splitext(filename)[0] + ".wav"
        wav_path = os.path.join(output_folder, wav_filename)

        # Skip if wav already exists
        if os.path.exists(wav_path):
            print(f"⏭️ Skipping {filename} (already converted)")
            continue

        audio = AudioSegment.from_mp3(mp3_path)
        audio = audio.set_frame_rate(16000).set_channels(1)  # 16kHz, mono

        audio.export(wav_path, format="wav")
        print(f"✅ Converted {filename} → {wav_filename}")

