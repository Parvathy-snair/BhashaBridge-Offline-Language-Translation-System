# 🌐 BhashaBridge – Offline Language Translation System

**BhashaBridge** is an efficient offline language translation system that converts spoken language into another language without requiring internet connectivity.
The system integrates **speech recognition, machine translation, and text-to-speech technologies** to enable real-time voice translation.

This project demonstrates how multiple AI components can be combined to build a **fully offline multilingual communication system**.

---

# 🧾 Project Overview

BhashaBridge is an **offline voice translator** that listens to spoken input, converts the speech into text, translates it into another language, and speaks the translated output.

The system works completely offline using pre-downloaded models for:

* Speech recognition
* Language translation
* Speech synthesis

Currently, the system supports translation between:

* **English**
* **Hindi**
* **Malayalam**

---

## ✨ Features

* 🎤 **Speech Recognition** using Vosk offline models
* 🌐 **Language Translation** using MarianMT models
* 🔊 **Text-to-Speech Output** using pyttsx3 / eSpeak
* 💻 **Fully Offline Operation** – No internet required
* ⚡ **Real-time voice processing**
* 🌏 **Multilingual Support (English, Hindi, Malayalam)**

---

## ⚙️ Technologies Used

* **Python**
* **Vosk Speech Recognition**
* **HuggingFace MarianMT Translation Models**
* **Transformers Library**
* **SoundDevice**
* **pyttsx3 Text-to-Speech**
* **eSpeak-NG (for Hindi & Malayalam speech)**

---

# 🧠 System Workflow

The translation system follows this pipeline:

Speech Input
↓
Speech Recognition (Vosk)
↓
Text Conversion
↓
Language Translation (MarianMT)
↓
Text-to-Speech Output

---

# 📁 Repository Structure

```id="os0v9z"
bhashabridge/
│
├── main.py              # Main voice translation program
├── mic_stt.py           # Speech-to-text microphone test
├── tts_test.py          # Text-to-speech test script
├── blh.py               # Helper functions / translation logic
├── download_models.py   # Script to download required models
├── requirements.txt     # Python dependencies
└── README.md
```

---

# ▶️ How to Run

### 1️⃣ Install dependencies

```id="k00z3n"
pip install -r requirements.txt
```

### 2️⃣ Run the translator

```id="t9c6wt"
python main.py
```

Speak into the microphone when prompted and the system will translate the speech.

---

# 📦 Required Offline Models

The large AI models used for speech recognition and translation are **not included in this repository** because of their size.

You must download the following models before running the program.

### Speech Recognition Models (Vosk)

* `vosk-model-en-us`
* `vosk-model-small-hi`
* `vosk-model-ml`

### Translation Models (MarianMT)

* `opus-mt-en-hi`
* `opus-mt-hi-en`
* `opus-mt-en-ml`
* `opus-mt-ml-en`

---

# 📄 Requirements

The required Python libraries are listed in `requirements.txt`.

```id="q4jrrm"
vosk
transformers
torch
sounddevice
pyttsx3
sentencepiece
```

---

# 📊 Project Summary

BhashaBridge demonstrates how speech recognition, machine translation, and speech synthesis can be integrated into a **fully offline multilingual voice translation system**.

The project highlights the potential of AI-powered tools for **multilingual communication in low-connectivity environments**.
