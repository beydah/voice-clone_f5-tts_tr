#!/usr/bin/env python3
"""Audio cleaning and normalization utility for Turkish F5-TTS reference voices.

Converts any audio file to 48kHz mono WAV, applies a 75 Hz high-pass filter,
trims silence using energy-based Voice Activity Detection, adds soft fades,
and normalizes to -1.0 dBFS peak.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
from pydub import AudioSegment
from scipy import signal


def clean_reference_audio(
    input_path: str | Path,
    output_path: str | Path = "clean_reference.wav",
    target_sr: int = 48000,
    hp_cutoff: float = 75.0,
    peak_target: float = 0.89,  # ~ -1.0 dBFS
) -> Path:
    input_path = Path(input_path)
    output_path = Path(output_path)

    if not input_path.is_file():
        raise FileNotFoundError(f"Input audio not found: {input_path}")

    # 1. Convert to target_sr mono WAV using pydub
    seg = AudioSegment.from_file(str(input_path))
    seg = seg.set_channels(1).set_frame_rate(target_sr)
    temp_wav = output_path.with_name(f"temp_{input_path.stem}.wav")
    seg.export(str(temp_wav), format="wav")

    # 2. Read into numpy array
    data, sr = sf.read(str(temp_wav))
    if temp_wav.is_file():
        temp_wav.unlink(missing_ok=True)

    if len(data.shape) > 1:
        data = data.mean(axis=1)

    # 3. High-pass Butterworth filter
    sos = signal.butter(4, hp_cutoff, "hp", fs=sr, output="sos")
    filtered = signal.sosfilt(sos, data)

    # 4. Energy-based silence trimming (30ms windows)
    frame_len = int(sr * 0.03)
    energy = np.array([
        np.sum(filtered[i : i + frame_len] ** 2)
        for i in range(0, len(filtered) - frame_len, frame_len)
    ])
    thresh = np.percentile(energy, 65) * 0.08
    active_frames = np.where(energy > thresh)[0]

    if len(active_frames) > 0:
        start_idx = max(0, active_frames[0] * frame_len - int(sr * 0.08))
        end_idx = min(len(filtered), (active_frames[-1] + 1) * frame_len + int(sr * 0.12))
        trimmed = filtered[start_idx:end_idx]
    else:
        trimmed = filtered

    # 5. Soft edge fades (15ms in, 25ms out)
    fade_in = int(sr * 0.015)
    fade_out = int(sr * 0.025)
    if len(trimmed) > (fade_in + fade_out):
        trimmed[:fade_in] *= np.linspace(0, 1, fade_in)
        trimmed[-fade_out:] *= np.linspace(1, 0, fade_out)

    # 6. Peak normalization
    peak = np.max(np.abs(trimmed))
    if peak > 0:
        trimmed = trimmed / peak * peak_target

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(output_path), trimmed, sr)
    duration = len(trimmed) / sr
    print(f"Cleaned audio saved: {output_path} ({duration:.2f} s, {sr} Hz)")
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Input reference audio file")
    parser.add_argument("--output", "-o", type=Path, default=Path("clean_reference.wav"), help="Output WAV path")
    parser.add_argument("--sr", type=int, default=48000, help="Target sample rate (default: 48000)")
    args = parser.parse_args()

    try:
        clean_reference_audio(args.input, args.output, target_sr=args.sr)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
