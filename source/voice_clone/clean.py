"""Audio cleaning and normalization for Turkish F5-TTS reference voices."""

from __future__ import annotations

from pathlib import Path
import numpy as np


def clean_reference_audio(
    input_path: str | Path,
    output_path: str | Path = "clean_reference.wav",
    target_sr: int = 48000,
    hp_cutoff: float = 75.0,
    peak_target: float = 0.89,  # ~ -1.0 dBFS
) -> Path:
    """Preprocesses a reference voice recording into clean mono 48kHz WAV."""
    from pydub import AudioSegment
    from scipy import signal
    import soundfile as sf

    input_path = Path(input_path)
    output_path = Path(output_path)

    if not input_path.is_file():
        raise FileNotFoundError(f"Input audio not found: {input_path}")

    # 1. Convert to mono WAV at target sample rate
    seg = AudioSegment.from_file(str(input_path))
    seg = seg.set_channels(1).set_frame_rate(target_sr)
    temp_wav = output_path.with_name(f"temp_{input_path.stem}.wav")
    seg.export(str(temp_wav), format="wav")

    # 2. Read into float array
    data, sr = sf.read(str(temp_wav))
    if temp_wav.is_file():
        temp_wav.unlink(missing_ok=True)

    if len(data.shape) > 1:
        data = data.mean(axis=1)

    # 3. High-pass filter
    sos = signal.butter(4, hp_cutoff, "hp", fs=sr, output="sos")
    filtered = signal.sosfilt(sos, data)

    # 4. Energy-based silence trimming
    frame_len = int(sr * 0.02)
    hop = int(sr * 0.01)
    frames = [
        filtered[i : i + frame_len]
        for i in range(0, len(filtered) - frame_len, hop)
    ]
    energies = [np.mean(f**2) for f in frames]
    threshold = np.percentile(energies, 30)

    voiced_idx = [i for i, e in enumerate(energies) if e > threshold]
    if voiced_idx:
        start_sample = max(0, voiced_idx[0] * hop - int(sr * 0.05))
        end_sample = min(len(filtered), voiced_idx[-1] * hop + int(sr * 0.1))
        trimmed = filtered[start_sample:end_sample]
    else:
        trimmed = filtered

    # 5. Peak normalization
    max_val = np.max(np.abs(trimmed))
    if max_val > 0:
        normed = (trimmed / max_val) * peak_target
    else:
        normed = trimmed

    # 6. Smooth head/tail fades
    fade_len = int(sr * 0.02)
    if len(normed) > 2 * fade_len:
        fade_in = np.linspace(0, 1, fade_len)
        fade_out = np.linspace(1, 0, fade_len)
        normed[:fade_len] *= fade_in
        normed[-fade_len:] *= fade_out

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(output_path), normed, sr, subtype="PCM_16")
    return output_path
