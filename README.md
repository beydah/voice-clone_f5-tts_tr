# 🎙️ Ses-Klonlama_Turkce_F5-TTS: 10 Saniyede Sıfır Örnekli (Zero-Shot) Türkçe Ses Klonlama

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/beydah/ses-klonlama-turkce-f5-tts/blob/main/Ses-Klonlama_Turkce_F5-TTS.ipynb)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Website](https://img.shields.io/badge/Website-beydahsaglam.com-blue?style=flat&logo=googlechrome)](https://beydahsaglam.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-beydah-0A66C2?style=flat&logo=linkedin)](https://linkedin.com/in/beydah)
[![GitHub](https://img.shields.io/badge/GitHub-beydah-181717?style=flat&logo=github)](https://github.com/beydah)

Yalnızca **10 saniyelik tek bir referans ses kaydıyla** kendi sesinizi birebir klonlayın! Model eğitimi, günlerce bekleme veya pahalı GPU kiralama maliyetleri olmadan; stüdyo netliğinde, doğal tonlamalı ve akıcı Türkçe ses üretimi.

---

## 🧠 Algoritmanın Kısa Tarihçesi ve Çalışma Mantığı

Yapay zekâ ile ses üretimi (Text-to-Speech) son birkaç yılda üç büyük evrim aşamasından geçti:

```
[1. Kuşak: 2017-2020]            [2. Kuşak: 2021-2023]             [3. Kuşak: 2024 ve Günümüz]
Tacotron 2 & WaveNet     ──►     VITS & Difüzyon Modelleri   ──►   Akış Eşleme (Flow Matching)
• Sıralı/yavaş üretim            • Rastgele gürültü giderme        • F5-TTS Mimarisi
• Saatlerce stüdyo kaydı         • Uzun hesaplama süresi           • 10 sn sesle Zero-Shot klonlama
• Günlerce model eğitimi         • Türkçe harf yutma & fısıltı     • Doğrusal, hızlı ve kristal netlik
```

### 1. Kuşak: Otoregresif Modeller (Tacotron 2, WaveNet, FastSpeech)
İlk modern derin öğrenme sistemleri kelimeleri veya ses dalgalarını sırayla (adım adım) üretiyordu. Bir kişinin sesini klonlayabilmek için profesyonel stüdyoda 10–20 saatlik ses kaydı alınıyor, bu veriler üzerinde günler boyunca model eğitiliyordu. Sonuçlar anlaşılır olsa da robotik kalıntılar ve duygusuz bir ton taşıyordu.

### 2. Kuşak: Standart Difüzyon ve VITS Modelleri
Görsel üretiminde çığır açan difüzyon mantığı (Stable Diffusion) ses alanına taşındı. Rastgele gürültüden başlayıp onlarca adımda gürültüyü temizleyerek ses spektrogramı oluşturuldu. Ses doğallığı artsa da işlem adımları çok fazlaydı ve özellikle Türkçe gibi zengin eklemeli dillerde kelime sonlarındaki harfleri yutma veya fısıltılı konuşma gibi problemler yaşanıyordu.

### 3. Kuşak: Akış Eşleme (Flow Matching) ve F5-TTS
2024 sonlarında duyurulan **F5-TTS (Flow Matching TTS)**, difüzyonun karmaşık ve dolambaçlı gürültü giderme sürecini ortadan kaldırır. 
* **Doğrusal Vektör Alanı (Continuous Normalizing Flow - CNF):** Rastgele gürültüden hedef insan sesine giden yolu en kısa ve en pürüzsüz doğru üzerinden hesaplar. Bu sayede yalnızca 32 adımda (`nfe_step=32`) stüdyo kalitesinde ses oluşturur.
* **Bağlamsal Şartlandırma (In-Context Conditioning):** Model eğitimi (fine-tuning) gerektirmez. Verdiğiniz 10 saniyelik referans ses kaydını ve onun metnini bir "bağlam kılavuzu" olarak alır. Tıpkı modern bir büyük dil modelinin (LLM) bir cümlenin devamını tahmin etmesi gibi, sesinizin rezonansını ve konuşma temposunu hedef metnin üzerine eksiksiz aktarır.
* **Vocos Nöral Çözücü:** Üretilen Mel-spektrogramını saniyeler içinde doğal insan kulağının duyduğu yüksek çözünürlüklü ses dalgasına dönüştürür.

---

## 🛠️ 5 Adımlı Kullanım Rehberi

Google Colab üzerinde tek tıkla çalıştırabileceğiniz 5 adımlı iş akışı:

### 1. Adım: Referans Sesi Hazırlayın
Modelin sesinizin tüm harf tınılarını tek seferde öğrenebilmesi için, Türk alfabesindeki 29 harfin tamamını barındıran altın cümleyi okuyun:

> **"Çağdaş projelerde karmaşık sistemleri çözen; özgün, güçlü ve her zaman şeffaf bileşenleri, amaca uygun ve ciddi bir vizyonla tasarlamak gerekir."**

* **Kayıt İpucu:** 8–12 saniye arasında, mikrofona 15–20 cm mesafeden, enerjik ve net bir diksiyonla okuyun. WhatsApp ses kaydı veya telefon kaydedicisi yeterlidir.

### 2. Adım: Sesi Yükleyin
Colab hücresini çalıştırın ve `Dosyaları Seç` butonuna basarak kaydettiğiniz ses dosyasını (.wav, .mp3, .ogg, .m4a) yükleyin.

### 3. Adım: Sesi Otomatik Temizleyin ve İyileştirin
Kod hücresi sesinizi otomatik olarak işler:
* Baş ve sondaki sessizlikleri kırpar (VAD).
* 75 Hz altı dip uğultularını ve nefes patlamalarını temizler (High-pass Butterworth filtresi).
* Mikrosaniyelik tıkırtıları yumuşatır (Fade-in / Fade-out).
* Stüdyo standardı olan `-1.0 dBFS` seviyesine normalize eder.

### 4. Adım: Metni Girin ve Sesi Klonlayın
Seslendirmek istediğiniz hedef metni forma yapıştırın.
* **Sıfır Halüsinasyon Mimarisi:** Model, metni bağımsız cümlelere ayırarak işler ve cümleler arasına **250 milisaniyelik doğal insan nefesi** koyar. Böylece uzun paragraflarda kelime uydurma veya harf yutma yaşanmaz.

### 5. Adım: Sesi Dinleyin ve İndirin
Üretilen yüksek kaliteli Türkçe ses kaydını tarayıcınızda dinleyin ve otomatik olarak bilgisayarınıza indirin!

---

## 💻 Yerel Bilgisayarda Çalıştırma (Offline / CPU & GPU)

Bu projeyi internet bağlantısı olmadan kendi bilgisayarınızda (Windows, macOS, Linux) çalıştırmak isterseniz:

```bash
# 1. Gerekli kütüphaneleri kurun
pip install f5-tts pydub soundfile scipy torch

# 2. Python kodunuzda çalıştırın
python -c "
import soundfile as sf
from f5_tts.model import DiT
from f5_tts.infer.utils_infer import load_model, load_vocoder, infer_process
from huggingface_hub import hf_hub_download

ckpt = hf_hub_download(repo_id='marduk-ra/F5-TTS-Turkish', filename='f5_tts_turkish_1000000.safetensors')
vocab = hf_hub_download(repo_id='marduk-ra/F5-TTS-Turkish', filename='vocab.txt')

model = load_model(DiT, dict(dim=1024, depth=22, heads=16, ff_mult=2, text_dim=512, conv_layers=4), ckpt, vocab_file=vocab, device='cpu')
vocoder = load_vocoder('vocos', device='cpu')

audio, sr, _ = infer_process('temiz_referans.wav', 'Çağdaş projelerde...', 'Klonlanacak hedef metin...', model, vocoder, device='cpu')
sf.write('cikti.wav', audio, sr)
print('Tamamlandı!')
"
```

---

## ⚙️ Tavsiye Edilen Ayarlar

| Parametre | Değer | Açıklama |
| :--- | :--- | :--- |
| `cfg_strength` | **2.2** | Ses benzerliği ve diksiyon netliği katsayısı (1.8 - 2.4 ideal aralıktır). |
| `nfe_step` | **32** | Nöral akış adım sayısı (32 adım hız ve stüdyo kalitesi arasındaki altın dengedir). |
| `speed` | **1.0** | Konuşma hızı çarpanı (1.0 doğal ritimdir). |
| `pause` | **250ms** | Cümle sonlarındaki doğal insan nefesi payı. |

---

## 👤 Geliştirici & Bağlantılar

* **Geliştirici:** Beydah Sağlam
* 🌐 **Kişisel Web Sitesi & Blog:** [beydahsaglam.com](https://beydahsaglam.com)
* 💼 **LinkedIn:** [linkedin.com/in/beydah](https://linkedin.com/in/beydah)
* 🐙 **GitHub:** [github.com/beydah](https://github.com/beydah)

---

## 📜 Teşekkür & Lisans

* Türkçe model ağırlıkları için [marduk-ra/F5-TTS-Turkish](https://huggingface.co/marduk-ra/F5-TTS-Turkish) topluluk çalışmasına teşekkür ederiz.
* Temel mimari: [F5-TTS: A Fairytaler that Fakes Fluent and Faithful Speech with Flow Matching](https://arxiv.org/abs/2410.06885)
* Bu proje **MIT Lisansı** ile lisanslanmıştır. Özgürce kullanabilir, geliştirebilir ve paylaşabilirsiniz.
