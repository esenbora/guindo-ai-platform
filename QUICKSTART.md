# ⚡ Quick Start - 5 Dakikada Başla

## 1️⃣ Kurulum (2 dakika)

```bash
# Setup scriptini çalıştır
./setup.sh
```

Bu script:
- Virtual environment oluşturur
- Tüm bağımlılıkları yükler
- .env dosyası şablonu oluşturur

## 2️⃣ API Anahtarlarını Al (2 dakika)

### Groq API (Ücretsiz) 🔑

1. https://console.groq.com/ adresine git
2. Üye ol (Google hesabınla giriş yapabilirsin)
3. "API Keys" bölümüne git
4. "Create API Key" butonuna tıkla
5. Anahtarı kopyala (gsk_... ile başlar)

### Serper API (İlk 2500 arama ücretsiz) 🔍

1. https://serper.dev/ adresine git
2. "Get API Key" butonuna tıkla
3. Google ile giriş yap
4. Dashboard'dan API anahtarını kopyala

## 3️⃣ API Anahtarlarını Ekle (1 dakika)

`.env` dosyasını düzenle:

```bash
# Editör ile aç (VSCode, nano, vim, vb.)
code .env
# veya
nano .env
```

Şunu göreceksin:
```bash
GROQ_API_KEY=your_groq_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

Anahtarları yapıştır:
```bash
GROQ_API_KEY=gsk_abc123...
SERPER_API_KEY=xyz789...
```

Kaydet ve çık.

## 4️⃣ Test Et (30 saniye)

```bash
# Virtual environment'ı aktifleştir
source venv/bin/activate

# Test scriptini çalıştır
python test_setup.py
```

Şunu göreceksin:
```
✅ PASS - Package Imports
✅ PASS - Environment File
✅ PASS - Directory Structure
✅ PASS - Configuration Files
✅ PASS - Groq API Connection

🎉 All tests passed! You're ready to run the workflow.
```

## 5️⃣ İlk Çalıştırma! 🚀

```bash
python main.py
```

İşte bu kadar! 🎉

---

## ⏱️ Ne Kadar Sürer?

İlk çalıştırma **10-15 dakika** sürebilir çünkü:
- 4 ajan sırayla çalışıyor
- LinkedIn araması yapılıyor
- ROI hesaplamaları yapılıyor
- FIRE planı oluşturuluyor
- Mikro-iş fırsatları araştırılıyor

---

## 📊 Çıktılar Nerede?

`outputs/` klasörüne bak:

```
outputs/
├── career_paths_20250119_143022.csv
├── education_vs_work_20250119_143522.xlsx
├── retirement_plan_20250119_144022.md
└── microbusiness_report_20250119_144522.md
```

---

## ❓ Sorun mu Var?

### "Module not found" hatası

```bash
# Virtual environment aktif mi kontrol et
which python
# /Users/.../crewai_orchestration/venv/bin/python olmalı

# Değilse aktifleştir
source venv/bin/activate
```

### "API key not found" hatası

```bash
# .env dosyasını kontrol et
cat .env

# Anahtarlar doğru mu?
```

### "Rate limit exceeded" hatası

- Groq free tier limiti: Dakikada 30 istek
- 1-2 dakika bekle ve tekrar dene

---

## 🎯 Sonraki Adımlar

1. ✅ Çıktıları incele
2. 📝 Kendi hedeflerine göre özelleştir (USAGE_GUIDE.md'ye bak)
3. 📅 Aylık raporlar için cron job kur
4. 💪 Erken emeklilik yolunda ilerle!

---

**İyi şanslar! 🚀**
