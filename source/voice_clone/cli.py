"""Command-line interface for Turkish F5-TTS voice cloning.

Usage:
  python -m voice_clone.cli --text "Merhaba dünya" --ref sample.wav --out output.wav
  python -m voice_clone.cli --file input.txt --ref sample.wav --clean-ref
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .clean import clean_reference_audio
from .infer import load_model, synthesize_text
from .phonetics import GOLDEN_PANGRAM


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="voice_clone",
        description="Zero-shot Turkish voice cloning CLI powered by F5-TTS.",
    )
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--text", type=str, help="Direct text string to synthesize.")
    input_group.add_argument("--file", type=Path, help="Path to text or markdown file.")

    parser.add_argument(
        "--ref",
        type=Path,
        required=True,
        help="Path to speaker reference audio (WAV/MP3/M4A/OGG).",
    )
    parser.add_argument(
        "--ref-text",
        type=str,
        default=GOLDEN_PANGRAM,
        help="Transcript of reference audio (defaults to Golden Pangram).",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("output.wav"),
        help="Path for output audio file (default: output.wav).",
    )
    parser.add_argument(
        "--speed",
        type=float,
        default=1.0,
        help="Speech speed multiplier (0.8 - 1.5, default: 1.0).",
    )
    parser.add_argument(
        "--cfg",
        type=float,
        default=2.2,
        help="Classifier-Free Guidance strength (default: 2.2).",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="auto",
        choices=["auto", "cuda", "cpu", "mps"],
        help="Inference compute device (default: auto).",
    )
    parser.add_argument(
        "--clean-ref",
        action="store_true",
        help="Apply high-pass filtering and silence trimming to reference before inference.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.file:
        if not args.file.is_file():
            print(f"Error: Text file not found: {args.file}", file=sys.stderr)
            return 1
        text = args.file.read_text(encoding="utf-8")
    else:
        text = args.text

    ref_audio = args.ref
    if not ref_audio.is_file():
        print(f"Error: Reference audio file not found: {ref_audio}", file=sys.stderr)
        return 1

    if args.clean_ref:
        cleaned_path = ref_audio.with_name(f"cleaned_{ref_audio.stem}.wav")
        print(f"Cleaning reference audio -> {cleaned_path}...")
        ref_audio = clean_reference_audio(ref_audio, cleaned_path)

    try:
        model, dev = load_model(device=args.device)
        synthesize_text(
            model=model,
            ref_audio=ref_audio,
            ref_text=args.ref_text,
            target_text=text,
            output_path=args.out,
            speed=args.speed,
            cfg=args.cfg,
        )
        return 0
    except Exception as e:
        print(f"Synthesis failed: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
