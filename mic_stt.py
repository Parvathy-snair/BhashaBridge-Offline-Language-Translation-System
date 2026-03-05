import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer

# Path to your offline model
model_path = r"C:\Users\PARVATHY S NAIR\OneDrive\Desktop\offline_translator\vosk-model-en-us"
model = Model(model_path)
recognizer = KaldiRecognizer(model, 16000)

# Create an audio queue
q = queue.Queue()

def callback(indata, frames, time, status):
    q.put(bytes(indata))

print("🎤 Speak something... (Ctrl+C to stop)")

# Open microphone stream
with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                       channels=1, callback=callback):

    while True:
        data = q.get()
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            text = json.loads(result).get("text", "")
            if text.strip():
                print("🗣️ You said:", text)
        else:
            partial = json.loads(recognizer.PartialResult()).get("partial", "")
