#!/usr/bin/env python3
"""
Real AI version using Groq directly without CrewAI complications
"""

import os
from dotenv import load_dotenv
from groq import Groq
import pandas as pd
from datetime import datetime

# Load environment
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def call_ai(prompt: str, system: str = "You are a helpful AI assistant.") -> str:
    """Call Groq API directly"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4096
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


def research_career_paths():
    """Research career paths using AI"""
    print("\n🔍 Agent 1: Career Mapper - Researching career paths...")
    
    system = """Sen deneyimli bir kariyer danışmanı ve veri analistisin. 
    ODTÜ İstatistik mezunlarının kariyer yollarını araştırıyorsun."""
    
    prompt = """ODTÜ İstatistik bölümü mezunlarının gerçekçi kariyer yollarını araştır ve analiz et.

12 farklı profil oluştur. Her profil için:
- İsim (Türk ismi)
- Mezuniyet yılı (2014-2018 arası)
- İlk iş pozisyonu
- Şu anki pozisyon
- Deneyim yılı
- Eğitim seviyesi (BS, MS, veya PhD)
- Tahmini maaş (USD)
- Kariyer geçiş sayısı
- Kısa not

Gerçekçi veri kullan. Data science, machine learning, analytics rollerine odaklan.

Çıktıyı CSV formatında ver (header dahil):
name,graduation_year,first_job,current_position,years_experience,education_level,estimated_salary_usd,career_transitions,notes"""

    result = call_ai(prompt, system)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'outputs/career_paths_{timestamp}.csv'
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"✅ Created: {filename}")
    return filename, result


def analyze_roi():
    """Analyze education ROI using AI"""
    print("\n💰 Agent 2: ROI Analyzer - Analyzing education returns...")
    
    system = """Sen finansal planlama ve eğitim yatırımları konusunda uzman bir analistsin.
    NPV, opportunity cost ve IRR hesaplamalarında çok iyisin."""
    
    prompt = """15 yıllık perspektifte 3 senaryonun ROI analizini yap:

**Senaryo 1: Direkt Çalışmaya Başla**
- Başlangıç maaşı: $30,000
- Yıllık artış: %10
- Çalışma süresi: 15 yıl
- Eğitim maliyeti: $0

**Senaryo 2: Master Yap (2 yıl)**
- Eğitim maliyeti: $20,000
- Başlangıç maaşı (master sonrası): $45,000
- Yıllık artış: %12
- Çalışma süresi: 13 yıl

**Senaryo 3: PhD Yap (5 yıl)**
- Eğitim maliyeti: $0 (stipend)
- Başlangıç maaşı (PhD sonrası): $60,000
- Yıllık artış: %15
- Çalışma süresi: 10 yıl

Her senaryo için hesapla:
1. Toplam kazanç (15 yıl)
2. NPV (discount rate: 5%)
3. Son yıl maaşı

Sonucu tablo formatında ver. Hangisi en iyi ROI'yi veriyor açıkla."""

    result = call_ai(prompt, system)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'outputs/education_roi_{timestamp}.md'
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("# 📊 Education ROI Analysis\n\n")
        f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(result)
    
    print(f"✅ Created: {filename}")
    return filename, result


def create_fire_plan():
    """Create FIRE plan using AI"""
    print("\n🔥 Agent 3: FIRE Planner - Creating retirement plan...")
    
    system = """Sen FIRE (Financial Independence, Retire Early) hareketinin uzmanısın.
    4% kuralını, güvenli çekilme oranlarını ve pasif gelir kaynaklarını mükemmel biliyorsun."""
    
    prompt = """35-40 yaş arası erken emeklilik için detaylı FIRE planı oluştur:

**Hedef:**
- Yaş: 25 → 40 (15 yıl)
- Target portfolio: $600,000
- Pasif gelir (4% rule): $24,000/year

**Hesaplamalar:**
- Başlangıç maaşı: $40,000
- Yıllık maaş artışı: %10
- Tasarruf oranı: %30-50 (zamanla artan)
- Yatırım getirisi: %8 (ortalama)

Detaylı plan içermeli:
1. Yıl bazında birikim tablosu (1, 2, 3, 5, 8, 10, 12, 15)
2. Asset allocation stratejisi
3. Risk yönetimi (bear market, recession)
4. Yaşam giderleri optimizasyonu
5. Gelir artırma stratejileri
6. Milestone tracker
7. Aksiyon planı

Markdown formatında, tablolar ve emoji ile zenginleştir."""

    result = call_ai(prompt, system)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'outputs/fire_plan_{timestamp}.md'
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("# 🔥 FIRE Plan - Early Retirement Strategy\n\n")
        f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(result)
    
    print(f"✅ Created: {filename}")
    return filename, result


def discover_side_hustles():
    """Discover side income opportunities using AI"""
    print("\n🚀 Agent 4: Market Watcher - Finding side income opportunities...")
    
    system = """Sen girişimcilik ve pasif gelir konusunda uzman bir araştırmacısın.
    IndieHackers, Product Hunt ve startup topluluklarını çok iyi biliyorsun."""
    
    prompt = """Teknik becerilere sahip (Python, R, statistics, ML) biri için yan gelir fırsatlarını araştır.

8 farklı kategori:
1. SaaS ürünleri (2-3 örnek)
2. Mobil uygulamalar (2 örnek)
3. Template & Design satışları (1-2 örnek)
4. Online kurslar/eğitimler (1 örnek)
5. Newsletter/içerik (1 örnek)

Her fikir için:
- Tahmini aylık gelir ($)
- Başlangıç maliyeti
- Geliştirme süresi
- Gerekli teknik beceriler
- Risk seviyesi (Düşük/Orta/Yüksek)
- Gerçek örnek (ürün ismi ve başarı hikayesi)

Öncelik sıralaması ekle:
- Tier 1: Hızlı başlangıç (1-2 ay)
- Tier 2: Orta vade (2-3 ay)
- Tier 3: Uzun vade (3-6 ay)

Markdown formatında, emoji ve tablolar kullan.
Başarı ipuçları ekle."""

    result = call_ai(prompt, system)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'outputs/side_hustles_{timestamp}.md'
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("# 🚀 Side Income Opportunities Report\n\n")
        f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(result)
    
    print(f"✅ Created: {filename}")
    return filename, result


def main():
    print("\n" + "="*60)
    print("🤖 REAL AI WORKFLOW - Using Groq LLM")
    print("="*60)
    print("\n⚡ This will use REAL AI (not mock data)")
    print("⏱️  Estimated time: 2-3 minutes")
    print("\n" + "="*60 + "\n")
    
    # Check API key
    if not os.getenv('GROQ_API_KEY'):
        print("❌ Error: GROQ_API_KEY not found in .env file")
        return
    
    # Create outputs directory
    os.makedirs('outputs', exist_ok=True)
    
    # Run all agents sequentially
    files = []
    
    try:
        # Agent 1: Career Research
        file1, _ = research_career_paths()
        files.append(file1)
        
        # Agent 2: ROI Analysis
        file2, _ = analyze_roi()
        files.append(file2)
        
        # Agent 3: FIRE Planning
        file3, _ = create_fire_plan()
        files.append(file3)
        
        # Agent 4: Side Hustles
        file4, _ = discover_side_hustles()
        files.append(file4)
        
        print("\n" + "="*60)
        print("✅ WORKFLOW COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\n📁 Generated files:")
        for f in files:
            print(f"   ✅ {f}")
        
        print("\n💡 These are REAL AI-generated insights!")
        print("🔍 Open the files to see detailed analysis\n")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
