"""Unit tests for voice_clone CLI and phonetics pipeline."""

import unittest
from pathlib import Path
import sys

# Add source directory to path
source_dir = Path(__file__).resolve().parent.parent / "source"
if str(source_dir) not in sys.path:
    sys.path.insert(0, str(source_dir))

from voice_clone.cli import build_parser
from voice_clone.phonetics import apply_phonetics, split_sentences, PHONETIC_DICTIONARY


class TestVoiceClone(unittest.TestCase):
    def test_cli_parser_required_args(self):
        parser = build_parser()
        # Missing ref should raise
        with self.assertRaises(SystemExit):
            parser.parse_args(["--text", "Deneme"])

        # Valid args parse cleanly
        args = parser.parse_args(["--text", "Deneme", "--ref", "sample.wav"])
        self.assertEqual(args.text, "Deneme")
        self.assertEqual(args.ref, Path("sample.wav"))
        self.assertEqual(args.speed, 1.0)
        self.assertEqual(args.cfg, 2.2)
        self.assertEqual(args.device, "auto")

    def test_phonetics_replacement(self):
        sample = "React ve Next.js bileşenleri API üzerinden JSON verisi çeker."
        phonetic = apply_phonetics(sample)
        self.assertIn("Riyekt", phonetic)
        self.assertIn("Nekst ceyes", phonetic)
        self.assertIn("Eypiyay", phonetic)
        self.assertIn("Ceysın", phonetic)

    def test_sentence_splitting(self):
        paragraph = "Birinci cümle burada bitti. İkinci cümle ise başladı! Son olarak soru var mı?"
        sentences = split_sentences(paragraph)
        self.assertEqual(len(sentences), 3)
        self.assertTrue(sentences[0].startswith("Birinci"))
        self.assertTrue(sentences[1].startswith("İkinci"))
        self.assertTrue(sentences[2].startswith("Son"))


if __name__ == "__main__":
    unittest.main()
