# Audio Recording & Quality Guidelines

Zero-shot voice cloning quality depends heavily on the quality, acoustics, and phonetic balance of the 8-12 second reference audio sample.

---

## 1. The 29-Letter Turkish Golden Pangram

To allow the F5-TTS model to learn your full vocal timbre, vocal cord vibrations, and resonance across every Turkish consonant and vowel, read this exact sentence:

> **"Çağdaş projelerde karmaşık sistemleri çözen; özgün, güçlü ve her zaman şeffaf bileşenleri, amaca uygun ve ciddi bir vizyonla tasarlamak gerekir."**

### Phonetic Coverage:
This single sentence contains all 29 characters of the Turkish alphabet:
`a, b, c, ç, d, e, f, g, ğ, h, ı, i, j, k, l, m, n, o, ö, p, r, s, ş, t, u, ü, v, y, z`.

---

## 2. Acoustic Best Practices

| Factor | Recommended | Avoid |
| :--- | :--- | :--- |
| **Duration** | 8 – 12 seconds | Under 5s (insufficient context) or over 25s (causes drift) |
| **Microphone Distance** | 15 – 20 cm at a 30° off-axis angle | Speaking directly into capsule (causes plosive pops) |
| **Room Acoustics** | Dry room with curtains/carpets | Empty tiled room with echo or flutter reflections |
| **Vocal Tone** | Energetic, articulate, steady cadence | Whispering, monotone mumbling, or exaggerated acting |
| **Background** | < 30 dB ambient room noise | Fans, AC hum, computer coil whine, traffic |

---

## 3. Automated Post-Processing

The bundled `clean_audio.py` script automatically standardizes any raw recording:
1. **75 Hz Butterworth Filter:** Removes sub-bass desk thumps, AC hum, and proximity effect plosives.
2. **Dynamic Energy VAD:** Trims silence at start and end while preserving initial consonant attacks.
3. **Micro-Fade Curves:** Applies 15ms linear fade-in and 25ms fade-out to prevent digital clipping ticks.
4. **-1.0 dBFS Peak Normalization:** Maximizes dynamic range without clipping distortion.
