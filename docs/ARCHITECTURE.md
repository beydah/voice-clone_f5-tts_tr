# Architecture & Model Specifications

`voice-clone_f5-tts_tr` provides zero-shot voice cloning for the Turkish language using the **F5-TTS (Flow Matching)** non-autoregressive text-to-speech architecture.

---

## 1. Flow Matching vs. Autoregressive TTS

Traditional neural TTS architectures often suffer from specific trade-offs:
- **Autoregressive models (e.g. XTTS, Bark, Tortoise):** Token-by-token generation is slow, prone to compounding phoneme skips, hallucinated repetitions, and high latency.
- **Diffusion models:** Require dozens of denoising steps and often suffer from whispery high-frequency noise.
- **Flow Matching (F5-TTS):** Learns continuous probability flows between standard Gaussian noise and mel-spectrogram trajectories using an Ordinary Differential Equation (ODE). It allows fast, deterministic generation in 32 Euler steps with superior vocal timbre fidelity.

---

## 2. Model Pipeline

```
[Target Text] ──> [Phonetic Normalizer] ──> [Sentence Chunker]
                                                   │
[Reference Audio] ──> [75Hz Filter + VAD] ──> [Vocos / Mel Extract]
                                                   │
                                                   ▼
                                       [F5-TTS DiT Transformer]
                                          (Euler ODE: 32 Steps)
                                                   │
                                                   ▼
                                           [Vocos Vocoder]
                                                   │
                                                   ▼
                                         [Paced Audio Output]
```

1. **Phonetic Preprocessing:** Technical terms (React, HTML, CSS, API) are converted into phonetically matched Turkish syllables before model input.
2. **Audio Conditioning:** The 8-12 second reference audio is high-pass filtered (75 Hz Butterworth) and trimmed with Voice Activity Detection (VAD).
3. **Diffusion Transformer (DiT):** In conditioned generation, the model matches the acoustic flow vector field conditioned on both the text embedding and reference mel-spectrogram.
4. **Vocoder:** Vocos reconstructs high-fidelity 24 kHz / 48 kHz time-domain waveforms.
5. **Breath Pacing:** A calibrated 250 ms silence buffer is inserted between sentence boundaries to recreate natural human respiratory cadences.

---

## 3. Pretrained Weights

- **Backbone Architecture:** F5-TTS Base (Diffusion Transformer with ConvNeXt mel front-end).
- **Turkish Checkpoint:** `marduk-ra/F5-TTS-Turkish` (1,000,000 step checkpoint trained on Turkish speech corpora).
- **Vocab File:** `vocab.txt` covering Turkish phonemes and accented characters (ç, ğ, ı, ö, ş, ü).
