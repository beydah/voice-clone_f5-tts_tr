<div align="center">

# 🎙️ Turkish Zero-Shot Voice Cloning (F5-TTS)

**Clone any Turkish voice in 10 seconds with Flow Matching neural synthesis.**  
*Zero training. Natural timbre. Studio fidelity.*

[![Open In Colab (TR)](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/beydah/voice-clone_f5-tts_tr/blob/main/colab/Voice_Cloning_Turkish_F5_TTS_TR.ipynb)
[![Open In Colab (EN)](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/beydah/voice-clone_f5-tts_tr/blob/main/colab/Voice_Cloning_Turkish_F5_TTS_EN.ipynb)
[![Website](https://img.shields.io/badge/Website-beydahsaglam.com-blue?style=flat&logo=googlechrome)](https://beydahsaglam.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-beydah-0A66C2?style=flat&logo=linkedin)](https://linkedin.com/in/beydah)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## ⚡ Highlights

- **Zero-Shot Transfer:** Learns your pitch, accent, and timbre from an **8-12 second** reference recording.
- **Flow Matching Architecture:** Replaces slow autoregressive sampling with non-autoregressive 32-step ODE solving.
- **Phonetically Balanced Pangram:** Uses a custom 29-letter Turkish pangram covering all consonants and vowels.
- **Natural Human Cadence:** Inserts calibrated 250ms breath pauses between sentences to eliminate robotic continuity.
- **Dual Runtime Support:** Run in interactive Google Colab (free GPU) or locally via Python CLI.

---

## 📁 Repository Structure

```
voice-clone_f5-tts_tr/
├── colab/
│   ├── Voice_Cloning_Turkish_F5_TTS_TR.ipynb  # Interactive Turkish Colab notebook
│   └── Voice_Cloning_Turkish_F5_TTS_EN.ipynb  # Interactive English Colab notebook
├── source/
│   ├── infer.py                               # Local CLI inference runner
│   ├── clean_audio.py                         # Audio filter, VAD, and normalizer
│   └── requirements.txt                       # Python dependencies
├── docs/
│   ├── ARCHITECTURE.md                        # Flow Matching & DiT specifications
│   ├── USAGE.md                               # Setup, Colab & CLI guide
│   └── AUDIO_GUIDELINES.md                    # Recording tips & 29-letter pangram
├── .agents/
│   └── AGENTS.md                              # Workspace contract
└── README.md
```

---

## 🚀 Quick Start (Google Colab)

1. Open either [Turkish Notebook](colab/Voice_Cloning_Turkish_F5_TTS_TR.ipynb) or [English Notebook](colab/Voice_Cloning_Turkish_F5_TTS_EN.ipynb) in Colab.
2. Run **Step 0** to install dependencies.
3. Record yourself reading the 29-letter golden pangram:
   > *"Çağdaş projelerde karmaşık sistemleri çözen; özgün, güçlü ve her zaman şeffaf bileşenleri, amaca uygun ve ciddi bir vizyonla tasarlamak gerekir."*
4. Upload the sample in **Step 2**, denoise in **Step 3**, and enter your text in **Step 4**.
5. Download your generated speech in **Step 5**!

---

## 💻 Local CLI Usage

```bash
# 1. Install dependencies
pip install -r source/requirements.txt

# 2. Denoise and prepare reference recording
python source/clean_audio.py sample.m4a --output clean_ref.wav

# 3. Synthesize Turkish speech
python source/infer.py \
  --ref-audio clean_ref.wav \
  --text "React ve yapay zeka entegrasyonunda bileşen sözleşmeleri kritik önem taşır." \
  --out speech.wav \
  --speed 1.05
```

For advanced CLI options and WebM Opus encoding, see [docs/USAGE.md](docs/USAGE.md).

---

## 📖 Technical Documentation

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md): Flow matching theory, Euler ODE, and Vocos integration.
- [docs/USAGE.md](docs/USAGE.md): Detailed local installation and deployment guide.
- [docs/AUDIO_GUIDELINES.md](docs/AUDIO_GUIDELINES.md): Acoustic conditions, microphone placement, and pangram details.

---

## 📜 License

MIT License. See [LICENSE](LICENSE) for details.
