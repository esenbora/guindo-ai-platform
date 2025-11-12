# 📘 Early Retirement Workflow - Kullanım Kılavuzu

## 🎯 Proje Amacı

Bu sistem, **35-40 yaş arası erken emeklilik (FIRE)** hedefine ulaşmak için yapay zeka ajanlarını kullanarak:

1. **Kariyer yolları araştırması** yapar
2. **Eğitim ROI analizi** hesaplar
3. **Finansal bağımsızlık planı** oluşturur
4. **Yan gelir fırsatları** keşfeder

---

## 🚀 Hızlı Başlangıç

### 1. Kurulum

```bash
# Depoyu klonla veya indir
cd crewai_orchestration

# Kurulum scriptini çalıştır
./setup.sh
```

### 2. API Anahtarlarını Ayarla

`.env` dosyasını düzenle:

```bash
# API Keys
GROQ_API_KEY=gsk_your_actual_key_here
SERPER_API_KEY=your_serper_key_here
```

**API anahtarları nasıl alınır:**

- **Groq API**: https://console.groq.com/keys (Ücretsiz)
- **Serper API**: https://serper.dev/api-key (İlk 2500 arama ücretsiz)

### 3. Çalıştır

```bash
# Virtual environment'ı aktifleştir
source venv/bin/activate

# Workflow'u başlat
python main.py
```

---

## 🤖 Ajanlar Nasıl Çalışır?

### Agent 1: Career Mapper 🔍
**Görevi**: LinkedIn'den ODTÜ/Boğaziçi/Bilkent İstatistik mezunlarının kariyer yollarını araştırır.

**Çıktı**: `outputs/career_paths_*.csv`

**Örnek veri:**
```csv
name,graduation_year,first_job,current_position,years_experience,education_level,estimated_salary_usd,notes
Ahmet Yılmaz,2015,Data Analyst,Senior Data Scientist,9,MSc,85000,FAANG company
```

### Agent 2: ROI Analyzer 📊
**Görevi**: Master/doktora yapmanın maliyeti ve faydalarını hesaplar.

**Çıktı**: `outputs/education_vs_work_*.xlsx`

**Karşılaştırılan senaryolar:**
- Direkt çalışmaya başla
- 2 yıl Master yap
- 5 yıl PhD yap

### Agent 3: FIRE Planner 💰
**Görevi**: 15 yılda $600,000 biriktirme planı oluşturur.

**Çıktı**: `outputs/retirement_plan_*.md`

**İçerik:**
- Aylık tasarruf hedefleri
- Yatırım portföy dağılımı
- 4% kuralı hesaplaması
- Risk senaryoları

### Agent 4: Market Watcher 🚀
**Görevi**: İkinci gelir kaynağı fırsatları araştırır.

**Çıktı**: `outputs/microbusiness_report_*.md`

**Araştırılan platformlar:**
- IndieHackers
- Product Hunt
- Reddit (r/SideProject)
- Twitter indie maker topluluğu

---

## 📊 Çıktıları Anlama

### Career Paths CSV

```csv
name,graduation_year,first_job,current_position,estimated_salary_usd
```

**Nasıl kullanılır:**
- Ortalama kariyer ilerleme süresini görürsün
- Hangi pozisyonların yüksek maaş getirdiğini öğrenirsin
- Master/PhD yapanların nasıl ilerlediğini karşılaştırırsın

### Education ROI Excel

**Üç senaryo karşılaştırması:**

| Senaryo | Eğitim Süresi | Toplam Kazanç (15 yıl) | NPV |
|---------|---------------|------------------------|-----|
| Direkt iş | 0 | $X | $Y |
| Master | 2 yıl | $X | $Y |
| PhD | 5 yıl | $X | $Y |

### Retirement Plan MD

**Yıllık birikim tablosu:**

| Yıl | Gelir | Tasarruf | Toplam Birikim | Hedef |
|-----|-------|----------|----------------|-------|
| 1   | $40K  | $12K     | $12.8K         | ✅    |
| 5   | $58K  | $20K     | $120K          | ✅    |
| 10  | $90K  | $35K     | $380K          | ✅    |
| 15  | $140K | $55K     | $625K          | ✅    |

### Microbusiness Report MD

**Fırsat örnekleri:**

```markdown
## SaaS Fikir: Email Automation Tool
- Aylık gelir: $2,000-$5,000
- Başlangıç maliyeti: $500
- Geliştirme süresi: 3 ay
- Teknik beceriler: Python, Flask, Stripe API
- Risk: Orta
```

---

## ⚙️ Özelleştirme

### LLM Modelini Değiştir

`.env` dosyasında:

```bash
LLM_MODEL=llama-3.3-70b-versatile  # Varsayılan
# veya
LLM_MODEL=mixtral-8x7b-32768       # Daha hızlı
```

### Ajanları Özelleştir

`config/agents.yaml` dosyasını düzenle:

```yaml
career_mapper:
  role: "Kariyer Yolu Araştırmacısı"
  goal: "..."  # Burayı düzenleyebilirsin
```

### Görevleri Özelleştir

`config/tasks.yaml` dosyasını düzenle:

```yaml
research_career_paths:
  description: >
    Kendi hedeflerine göre değiştirebilirsin...
```

---

## 🔧 Sorun Giderme

### Problem: "GROQ_API_KEY not found"

**Çözüm:**
```bash
# .env dosyasını kontrol et
cat .env

# API anahtarını ekle
echo "GROQ_API_KEY=gsk_your_key" >> .env
```

### Problem: "Module not found"

**Çözüm:**
```bash
# Virtual environment aktif mi?
source venv/bin/activate

# Bağımlılıkları tekrar yükle
pip install -r requirements.txt
```

### Problem: "Rate limit exceeded"

**Çözüm:**
- Groq free tier: Dakikada 30 istek limiti var
- Biraz bekle veya ücretli plana geç

---

## 📈 İleri Seviye Kullanım

### Aylık Otomatik Rapor

Cron job ekle (macOS/Linux):

```bash
# Crontab'ı düzenle
crontab -e

# Her ayın 1'inde çalıştır
0 9 1 * * cd /path/to/crewai_orchestration && ./venv/bin/python main.py
```

### Streamlit Dashboard Ekle

```bash
# Streamlit kur
pip install streamlit

# Dashboard oluştur (opsiyonel - ileride eklenecek)
streamlit run dashboard.py
```

---

## 🎯 Sonraki Adımlar

1. **API anahtarlarını al** (5 dakika)
2. **İlk çalıştırmayı yap** (10 dakika)
3. **Çıktıları incele** (30 dakika)
4. **Kendi hedeflerine göre özelleştir** (1 saat)

---

## 💡 İpuçları

1. **İlk çalıştırmada** ajanlar biraz yavaş olabilir (10-15 dakika)
2. **Serper API** limitini aşmamak için fazla sık çalıştırma
3. **Çıktıları Excel/Notion'a aktararak** daha detaylı analiz yapabilirsin
4. **Aylık güncellemeler** almak için workflow'u düzenli çalıştır

---

## 📞 Destek

Sorun yaşarsan:
1. README.md'yi tekrar oku
2. `.env` dosyasını kontrol et
3. `outputs/` klasöründeki hata loglarına bak

---

**Başarılar! 🚀 Erken emeklilik yolunda ilerlemene devam et!**
