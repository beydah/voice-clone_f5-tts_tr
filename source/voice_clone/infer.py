"""Inference engine for F5-TTS Turkish zero-shot voice cloning."""

from __future__ import annotations

import os
import re
import time
from pathlib import Path
from typing import Any

import numpy as np

from .phonetics import GOLDEN_PANGRAM, apply_phonetics, split_sentences


def get_hf_token() -> str | None:
    """Retrieves HuggingFace token from environment or optional .env file."""
    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_TOKEN")
    if token:
        return token.strip()
    env_file = Path(".env")
    if env_file.is_file():
        try:
            for line in env_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line.startswith("HF_TOKEN=") or line.startswith("HUGGINGFACE_TOKEN="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
        except Exception:
            pass
    return None


def load_model(device: str = "auto") -> tuple[Any, str]:
    """Loads F5-TTS Turkish weights from Hugging Face repository."""
    import torch
    from huggingface_hub import hf_hub_download
    from f5_tts.api import F5TTS

    if device == "auto":
        dev = "cuda" if torch.cuda.is_available() else "cpu"
    else:
        dev = device

    print(f"Loading F5-TTS Turkish weights from Hugging Face on [{dev.upper()}]...")
    token = get_hf_token()

    ckpt_path = hf_hub_download(
        repo_id="marduk-ra/F5-TTS-Turkish",
        filename="f5_tts_turkish_1000000.safetensors",
        token=token,
    )
    vocab_path = hf_hub_download(
        repo_id="marduk-ra/F5-TTS-Turkish",
        filename="vocab.txt",
        token=token,
    )

    model = F5TTS(
        model="F5TTS_Base",
        ckpt_file=ckpt_path,
        vocab_file=vocab_path,
        device=dev,
    )
    print("Model initialized successfully.")
    return model, dev


def synthesize_text(
    model: Any,
    ref_audio: Path,
    ref_text: str,
    target_text: str,
    output_path: Path,
    speed: float = 1.0,
    cfg: float = 2.2,
    breath_pause_sec: float = 0.25,
) -> Path:
    """Synthesizes text in sentence batches and concatenates into final audio file."""
    import soundfile as sf
    import torch

    ref_audio = Path(ref_audio)
    output_path = Path(output_path)

    if not ref_audio.is_file():
        raise FileNotFoundError(f"Reference audio missing: {ref_audio}")

    sentences = split_sentences(target_text)
    print(f"Synthesizing {len(sentences)} sentence(s)...")
    t0 = time.time()
    audio_chunks: list[np.ndarray] = []
    sr_val = 24000

    pause_samples = int(sr_val * breath_pause_sec)
    pause_chunk = np.zeros(pause_samples, dtype=np.float32)

    with torch.inference_mode():
        for i, sentence in enumerate(sentences, start=1):
            s_t0 = time.time()
            wav, sr, _ = model.infer(
                ref_file=str(ref_audio),
                ref_text=ref_text,
                gen_text=sentence,
                speed=speed,
                cfg_strength=cfg,
            )
            sr_val = sr
            audio_chunks.append(wav)
            if i < len(sentences):
                audio_chunks.append(pause_chunk)

            s_dur = time.time() - s_t0
            print(f"  [{i}/{len(sentences)}] Synthesized in {s_dur:.1f}s -> {sentence[:45]}...")

    final_audio = np.concatenate(audio_chunks)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(output_path), final_audio, sr_val)

    total_time = time.time() - t0
    audio_dur = len(final_audio) / sr_val
    rtf = total_time / audio_dur if audio_dur > 0 else 0
    print(f"Done! Saved to: {output_path}")
    print(f"  Duration: {audio_dur:.1f}s | Elapsed: {total_time:.1f}s | RTF: {rtf:.2f}")

    return output_path
