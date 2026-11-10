"""Phonetic normalizations and pangram definitions for Turkish F5-TTS."""

from __future__ import annotations

import re

GOLDEN_PANGRAM = (
    "Çağdaş projelerde karmaşık sistemleri çözen; özgün, güçlü ve her zaman şeffaf "
    "bileşenleri, amaca uygun ve ciddi bir vizyonla tasarlamak gerekir."
)

PHONETIC_DICTIONARY: dict[str, str] = {
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
    "N8N": "En-sekiz-en",
    "SQL": "Es-Kü-El",
    "UI": "Yu-Ay",
    "UX": "Yu-Eks",
    "SEO": "Se-O",
    "GitHub": "Githap",
}


def apply_phonetics(text: str) -> str:
    """Replaces foreign technical abbreviations with Turkish phonetic approximations."""
    for term, rep in PHONETIC_DICTIONARY.items():
        text = re.sub(rf"\b{re.escape(term)}\b", rep, text, flags=re.IGNORECASE)
    return text


def split_sentences(text: str) -> list[str]:
    """Splits body text into natural sentence chunks for synthesis."""
    clean = apply_phonetics(text)
    sentences = [
        c.strip()
        for c in re.split(r"(?<=[.!?])\s+", clean.replace("\n", " "))
        if len(c.strip()) > 3
    ]
    return sentences if sentences else [clean.strip()]
