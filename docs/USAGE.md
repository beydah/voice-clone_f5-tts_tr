# Usage Guide: Colab & Local Execution

This repository supports two execution modes:
1. **Cloud Execution:** Zero-setup interactive Google Colab notebooks (free T4 GPU).
2. **Local Execution:** Python CLI scripts on CUDA or Apple Silicon / CPU.

---

## 1. Google Colab (Recommended for Fast Inference)

Launch either the Turkish or English notebook directly with one click:

| Language | Notebook Path | Colab Link |
| :--- | :--- | :--- |
| **Turkish** | `colab/Voice_Cloning_Turkish_F5_TTS_TR.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/beydah/voice-clone_f5-tts_tr/blob/main/colab/Voice_Cloning_Turkish_F5_TTS_TR.ipynb) |
| **English** | `colab/Voice_Cloning_Turkish_F5_TTS_EN.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/beydah/voice-clone_f5-tts_tr/blob/main/colab/Voice_Cloning_Turkish_F5_TTS_EN.ipynb) |

### Steps in Colab:
1. Run Step 0 to install dependencies (~40 seconds).
2. Upload your 8-12 second reference audio in Step 2.
3. Run Step 3 to clean, filter, and normalize the audio.
4. Paste your target script in Step 4 and click Run.
5. In Step 5, listen to the generated speech and download the output `.wav`.

---

## 2. Local Environment Setup

### Prerequisites
- Python 3.10+
- PyTorch 2.2+ with CUDA (optional for CPU mode)
- `ffmpeg` (installed on system path for audio format conversions)

### Installation
```bash
git clone https://github.com/beydah/voice-clone_f5-tts_tr.git
cd voice-clone_f5-tts_tr
pip install -r source/requirements.txt
```

---

## 3. Local CLI Usage

### A. Clean a Reference Audio File
```bash
python source/clean_audio.py my_voice.m4a --output clean_ref.wav
```

### B. Synthesize Voice from Text String
```bash
python source/infer.py \
  --ref-audio clean_ref.wav \
  --text "Çağdaş projelerde karmaşık sistemleri çözen bileşenler tasarlıyoruz." \
  --out studio_voice.wav \
  --speed 1.0 \
  --cfg 2.2
```

### C. Synthesize Voice from a Long File to WebM Opus
```bash
python source/infer.py \
  --ref-audio clean_ref.wav \
  --file article.txt \
  --out article-tr.webm \
  --speed 1.05
```
