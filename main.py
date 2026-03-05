import os
import json
import tempfile
import subprocess
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from transformers import MarianMTModel, MarianTokenizer
import pyttsx3

# ================================================================
# 🧠 OFFLINE MULTILINGUAL VOICE TRANSLATOR (EN ↔ HI ↔ ML)
# ================================================================

# ---------- PATHS TO OFFLINE MODELS ----------
vosk_en_path = r"C:\Users\PARVATHY S NAIR\OneDrive\Desktop\offline_translator\vosk-model-en-us"
vosk_hi_path = r"C:\Users\PARVATHY S NAIR\OneDrive\Desktop\offline_translator\vosk-model-small-hi"
vosk_ml_path = r"C:\Users\PARVATHY S NAIR\OneDrive\Desktop\offline_translator\vosk-model-ml"

en_to_hi_model_path = r"C:\Users\PARVATHY S NAIR\OneDrive\Desktop\offline_translator\opus-mt-en-hi"
hi_to_en_model_path = r"C:\Users\PARVATHY S NAIR\OneDrive\Desktop\offline_translator\opus-mt-hi-en"

en_to_ml_model_path = r"C:\Users\PARVATHY S NAIR\OneDrive\Desktop\offline_translator\opus-mt-en-ml"
ml_to_en_model_path = r"C:\Users\PARVATHY S NAIR\OneDrive\Desktop\offline_translator\opus-mt-ml-en"

# ---------- MODE SELECTION ----------
print("=======================================")
print("🈯 OFFLINE TRANSLATOR MODES")
print("1️⃣  English → Hindi")
print("2️⃣  Hindi → English")
print("3️⃣  English → Malayalam")
print("4️⃣  Malayalam → English")
print("=======================================")

mode = input("👉 Select mode (1-4): ").strip()

if mode == "1":
    trans_model_path = en_to_hi_model_path
    vosk_path = vosk_en_path
    target_lang = "hi"
    print("\n🌐 Mode: English → Hindi")

elif mode == "2":
    trans_model_path = hi_to_en_model_path
    vosk_path = vosk_hi_path
    target_lang = "en"
    print("\n🌐 Mode: Hindi → English")

elif mode == "3":
    trans_model_path = en_to_ml_model_path
    vosk_path = vosk_en_path
    target_lang = "ml"
    print("\n🌐 Mode: English → Malayalam")

elif mode == "4":
    trans_model_path = ml_to_en_model_path
    vosk_path = vosk_ml_path
    target_lang = "en"
    print("\n🌐 Mode: Malayalam → English")

else:
    print("⚠ Invalid selection! Please choose 1-4.")
    exit()

# ---------- LOAD TRANSLATION MODEL ----------
print("🔄 Loading translation model (offline)...")
tokenizer = MarianTokenizer.from_pretrained(trans_model_path)
translator = MarianMTModel.from_pretrained(trans_model_path)
print("✅ Translation model loaded successfully.\n")

# ---------- LOAD VOSK SPEECH MODEL ----------
print("🔄 Loading Vosk speech model...")

if not os.path.exists(vosk_path):
    print(f"❌ Vosk model not found at: {vosk_path}")
    exit()

vosk_model = Model(vosk_path)

print("✅ Vosk model loaded successfully.\n")

# ---------- RECORD AUDIO ----------
print("🎙 Speak now (6 seconds)...")

fs = 16000
duration = 6

audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
sd.wait()

print("✅ Audio recorded.\n")

# ---------- SPEECH RECOGNITION ----------
print("🎧 Recognizing speech...")

rec = KaldiRecognizer(vosk_model, fs)
rec.AcceptWaveform(audio.tobytes())

result = json.loads(rec.Result())
text_in = result.get("text", "").strip()

print(f"📝 Detected Speech: {text_in}\n")

if not text_in:
    print("⚠ No speech detected. Please try again.")
    exit()

# ---------- TRANSLATION ----------
print("🌐 Translating text...")

inputs = tokenizer(text_in, return_tensors="pt", padding=True)
translated = translator.generate(**inputs)

text_out = tokenizer.decode(translated[0], skip_special_tokens=True)

print(f"💬 Translated Text: {text_out}\n")

# ================================================================
# 🔊 OFFLINE SPEECH OUTPUT
# ================================================================

def speak_text(text, lang):

    # Hindi Speech
    if lang == "hi":
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                temp_path = tmp.name

            subprocess.run(
                ["espeak-ng", "-v", "hi", "-s", "150", text, "-w", temp_path],
                check=True
            )

            subprocess.run(
                ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", temp_path],
                check=True
            )

            os.remove(temp_path)

            print("🗣 Spoken using Hindi voice.\n")

        except Exception as e:
            print("⚠ Hindi TTS failed:", e)

    # Malayalam Speech
    elif lang == "ml":
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                temp_path = tmp.name

            subprocess.run(
                ["espeak-ng", "-v", "ml", "-s", "150", text, "-w", temp_path],
                check=True
            )

            subprocess.run(
                ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", temp_path],
                check=True
            )

            os.remove(temp_path)

            print("🗣 Spoken using Malayalam voice.\n")

        except Exception as e:
            print("⚠ Malayalam TTS failed:", e)

    # English Speech
    else:
        engine = pyttsx3.init()
        engine.setProperty("rate", 160)
        engine.say(text)
        engine.runAndWait()

        print("🗣 Spoken using English voice.\n")

# ---------- PLAY TRANSLATED OUTPUT ----------
print("🔊 Speaking translation (offline)...")

speak_text(text_out, target_lang)

print("✅ Done! Everything worked completely offline.")