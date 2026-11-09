#!/usr/bin/env python3
"""Local CLI inference tool for zero-shot Turkish voice cloning using F5-TTS.

Loads weights from `marduk-ra/F5-TTS-Turkish`, applies phonetic corrections,
chunks text into natural sentences, synthesizes audio chunks, and outputs
the final merged speech file.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import soundfile as sf
import torch
from huggingface_hub import hf_hub_download

GOLDEN_PANGRAM = (
    "Çağdaş projelerde karmaşık sistemleri çözen; özgün, güçlü ve her zaman şeffaf "
    "bileşenleri, amaca uygun ve ciddi bir vizyonla tasarlamak gerekir."
)

PHONETIC_DICTIONARY = {
    "React": "Riyekt",
    "HTML": "He-Te-Me-Le",
    "JavaScript": "Cavasikript",
    "DOM": "Dom",
    "CSS": "Si-Es-Es",
    "Next.js": "Nekst ceyes",
    "API": "Eypiyay",
    "JSON": "Ceysın",
    "Suspense": "Saspens",
    "fallback": "folbek",
    "transition": "trenzışın",
    "effect": "efekt",
    "render": "rendır",
    "URL": "Yu-Ar-El",
    "AI": "Ey-Ay",
    "LLM": "El-El-Em",
    "TTS": "Ti-Ti-Es",
}


def apply_phonetics(text: str) -> str:
    for term, rep in PHONETIC_DICTIONARY.items():
        text = re.sub(rf"\b{re.escape(term)}\b", rep, text, flags=re.IGNORECASE)
    return text


def load_model(device: str = "auto") -> tuple[Any, str]:
    from f5_tts.api import F5TTS

    if device == "auto":
        dev = "cuda" if torch.cuda.is_available() else "cpu"
    else:
        dev = device

    print(f"Loading F5-TTS Turkish weights from Hugging Face on [{dev.upper()}]...")
    ckpt_path = hf_hub_download(repo_id="marduk-ra/F5-TTS-Turkish", filename="f5_tts_turkish_1000000.safetensors")
    vocab_path = hf_hub_download(repo_id="marduk-ra/F5-TTS-Turkish", filename="vocab.txt")

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
    if not ref_audio.is_file():
        raise FileNotFoundError(f"Reference audio missing: {ref_audio}")

    clean_text = apply_phonetics(target_text)
    sentences = [c.strip() for c in re.split(r"(?<=[.!?])\s+", clean_text.replace("\n", " ")) if len(c.strip()) > 3]

    if not sentences:
        sentences = [clean_text.strip()]

    print(f"Synthesizing {len(sentences)} sentence(s)...")
    t0 = time.time()
    audio_chunks: list[np.ndarray] = []
    sr_val = 24000

    for idx, s in enumerate(sentences, 1):
        print(f"  [{idx}/{len(sentences)}] {s[:50]}...")
        wav, sr, _ = model.infer(
            ref_file=str(ref_audio),
            ref_text=ref_text,
            gen_text=s,
            nfe_step=32,
            cfg_strength=cfg,
            speed=speed,
            seed=42,
            remove_silence=False,
        )
        sr_val = sr
        audio_chunks.append(wav)
        if idx < len(sentences):
            audio_chunks.append(np.zeros(int(breath_pause_sec * sr)))

    final_wav = np.concatenate(audio_chunks)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save initial wav
    wav_path = output_path.with_suffix(".wav")
    sf.write(str(wav_path), final_wav, sr_val)
    duration = len(final_wav) / sr_val
    elapsed = time.time() - t0
    print(f"Rendered {duration:.1f}s audio in {elapsed:.1f}s wall time.")

    # Convert format if target is webm or mp3
    ext = output_path.suffix.lower()
    if ext in (".webm", ".opus"):
        try:
            cmd = ["ffmpeg", "-y", "-i", str(wav_path), "-c:a", "libopus", "-b:a", "32k", "-vbr", "on", str(output_path)]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if output_path != wav_path and output_path.is_file():
                wav_path.unlink(missing_ok=True)
            print(f"Encoded to WebM Opus: {output_path}")
            return output_path
        except Exception:
            print("ffmpeg not available or failed; kept WAV output.")
            return wav_path
    elif ext == ".mp3":
        try:
            cmd = ["ffmpeg", "-y", "-i", str(wav_path), "-c:a", "libmp3lame", "-b:a", "128k", str(output_path)]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if output_path != wav_path and output_path.is_file():
                wav_path.unlink(missing_ok=True)
            print(f"Encoded to MP3: {output_path}")
            return output_path
        except Exception:
            print("ffmpeg not available or failed; kept WAV output.")
            return wav_path

    return wav_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref-audio", required=True, type=Path, help="Reference voice recording (8-12 seconds)")
    parser.add_argument("--ref-text", default=GOLDEN_PANGRAM, help="Transcript of reference audio (default: 29-letter pangram)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", type=str, help="Direct text string to synthesize")
    group.add_argument("--file", type=Path, help="Text file containing speech script")
    parser.add_argument("--out", type=Path, default=Path("output.wav"), help="Output audio path (.wav, .webm, .mp3)")
    parser.add_argument("--speed", type=float, default=1.0, help="Speech rate multiplier (0.8 - 1.3)")
    parser.add_argument("--cfg", type=float, default=2.2, help="CFG fidelity guidance strength (1.5 - 3.0)")
    parser.add_argument("--device", choices=["auto", "cuda", "cpu"], default="auto", help="Execution device")
    args = parser.parse_args()

    if args.file:
        target_text = args.file.read_text(encoding="utf-8")
    else:
        target_text = args.text

    model, _ = load_model(args.device)
    synthesize_text(
        model=model,
        ref_audio=args.ref_audio,
        ref_text=args.ref_text,
        target_text=target_text,
        output_path=args.out,
        speed=args.speed,
        cfg=args.cfg,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
