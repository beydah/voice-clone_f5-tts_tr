# AGENTS.md — voice-clone_f5-tts_tr

Turkish zero-shot voice cloning toolkit powered by F5-TTS Flow Matching architecture.

## Directory Structure
- `colab/`: Interactive Google Colab notebooks (`Voice_Cloning_Turkish_F5_TTS_TR.ipynb`, `Voice_Cloning_Turkish_F5_TTS_EN.ipynb`).
- `source/`: Local CLI utilities (`infer.py`, `clean_audio.py`, `requirements.txt`).
- `docs/`: Technical and operational English documentation (`ARCHITECTURE.md`, `USAGE.md`, `AUDIO_GUIDELINES.md`).
- `.agents/`: Agent guidelines and repo contracts.

## Contracts & Standards
- Keep notebooks self-contained and reproducible on free Colab T4 instances.
- Documentation and code comments must be written in English.
- No heavy binaries or cloned model weights stored in Git (use Hugging Face Hub cache).
