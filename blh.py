import os
import json
import sounddevice as sd
import numpy as np
import wave
import subprocess

from vosk import Model, KaldiRecognizer
from transformers import MarianMTModel, MarianTokenizer

# ================================================================
# 🧠 OFFLINE ENGLISH ↔ HINDI VOICE TRANSLATOR
# ================================================================

# ---------- PATHS TO OFFLINE MODELS ----------
# NOTE: Ensure these paths are correct for your system!
vosk_model_en = r"C:\Users\PARVATHY S NAIR\OneDrive\Desktop\offline_translator\vosk-model-en-us"
vosk_model_hi = r"C:\Users\PARVATHY S NAIR\OneDrive\Desktop\offline_translator\vosk-model-small-hi"

en_to_hi_model_path = r"C:\Users\PARVATHY S NAIR\OneDrive\Desktop\offline_translator\opus-mt-en-hi"
hi_to_en_model_path = r"C:\Users\PARVATHY S NAIR\OneDrive\Desktop\offline_translator\opus-mt-hi-en"

# ---------- MODE SELECTION ----------
print("=======================================")
print("🈯 OFFLINE TRANSLATOR MODES")
print("1️⃣  English → Hindi")
print("2️⃣  Hindi → English")
print("=======================================")
mode = input("👉 Select mode (1 or 2): ").strip()

if mode == "1":
    trans_model_name = en_to_hi_model_path
    vosk_path = vosk_model_en
    lang_in, lang_out = "English", "Hindi"
    lang_code_out = "hi"
    print(f"\n🌐 Mode: {lang_in} → {lang_out}")
else:
    trans_model_name = hi_to_en_model_path
    vosk_path = vosk_model_hi
    lang_in, lang_out = "Hindi", "English"
    lang_code_out = "en"
    print(f"\n🌐 Mode: {lang_in} → {lang_out}")

# --- Ensure correct language code for eSpeak-NG ---
speech_rate = 150 if lang_code_out == "hi" else 160

# ---------- LOAD TRANSLATION MODEL ----------
print("🔄 Loading translation model (offline)...")
tokenizer = MarianTokenizer.from_pretrained(trans_model_name)
translator = MarianMTModel.from_pretrained(trans_model_name)
print("✅ Translation model loaded successfully.\n")

# ---------- LOAD VOSK SPEECH MODEL ----------
print(f"🔄 Loading Vosk speech model for {lang_in}...")
vosk_model = Model(vosk_path)
print("✅ Vosk model loaded successfully.\n")

# ---------- RECORD AUDIO ----------
print("🎙 Speak now (6 seconds)...")
fs = 16000
duration = 6  # seconds
audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
sd.wait()
print("✅ Audio recorded.\n")

# ---------- SPEECH RECOGNITION ----------
print("🎧 Recognizing speech...")
rec = KaldiRecognizer(vosk_model, fs)
rec.AcceptWaveform(audio.tobytes())
result = json.loads(rec.Result())
text_in = result.get("text", "")
print(f"📝 Detected Speech: {text_in}\n")

if not text_in.strip():
    print("⚠ No speech detected. Please try again.")
    exit()

# ---------- TRANSLATION ----------
inputs = tokenizer(text_in, return_tensors="pt", padding=True)
translated = translator.generate(**inputs)
text_out = tokenizer.decode(translated[0], skip_special_tokens=True)
print(f"🌐 Translated Text: {text_out}\n")

# ---
# ================================================================
# 🔊 OFFLINE SPEECH OUTPUT (eSpeak-NG) - REVISED FOR ROBUSTNESS
# ================================================================

wav_file = "temp_output.wav"
print("🔊 Speaking translation (offline) via WAV file...")

# Construct the eSpeak-NG command to write to a WAV file
espeak_command = [
    'espeak-ng',
    f'-v{lang_code_out}',
    f'-s{speech_rate}',
    f'-w{wav_file}',  # Output to WAV file
    text_out          # The text to speak
]

try:
    print(f"🗣 Generating audio file for {lang_out}...")
    
    # Run eSpeak-NG command (check=True raises error on failure)
    subprocess.run(espeak_command, check=True, capture_output=True, text=True, encoding='utf-8')
    
    print(f"✅ Audio file '{wav_file}' generated. Playing back via sounddevice...")
    
    # --- Play the generated WAV file using sounddevice ---
    if os.path.exists(wav_file):
        with wave.open(wav_file, 'rb') as wf:
            # Read all parameters and frames from the WAV file
            framerate = wf.getframerate()
            frames = wf.readframes(wf.getnframes())
            
            # Convert binary data to numpy array (required by sounddevice)
            # eSpeak-NG usually outputs 16-bit PCM, which is why dtype='int16' is used.
            audio_data = np.frombuffer(frames, dtype=np.int16)

            # Play the audio
            sd.play(audio_data, framerate)
            sd.wait()
            
        print("🗣 Spoken successfully.\n")
    else:
        print(f"⚠ Error: eSpeak-ng did not create the file '{wav_file}'. Check eSpeak-ng installation.")

except subprocess.CalledProcessError as e:
    # This catches failures where the espeak-ng command crashed internally
    print(f"⚠ eSpeak NG command failed with error code {e.returncode}.")
    print(f"Error Output (stderr):\n{e.stderr}")
    print("Ensure eSpeak-ng is correctly installed and accessible in your system's PATH.")
except FileNotFoundError:
    # This catches failures where the 'espeak-ng' command itself could not be found
    print("⚠ eSpeak NG executable not found. Please ensure it is installed and in your PATH.")
except Exception as e:
    # General exception during file reading or playback
    print(f"⚠ An unexpected error occurred during audio output: {e}")

# ---
# ---------- CLEANUP (Optional) ----------
if os.path.exists(wav_file):
    os.remove(wav_file)
# ---

print("✅ Done! Everything worked completely offline.")