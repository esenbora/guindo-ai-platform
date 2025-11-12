#!/usr/bin/env python3
"""
Demo/Test version without requiring API keys
Simulates the workflow with mock data
"""

import os
import pandas as pd
from datetime import datetime

# Create outputs directory
os.makedirs('outputs', exist_ok=True)

def generate_career_paths():
    """Generate mock career path data"""
    data = {
        'name': [
            'Ahmet Yılmaz', 'Ayşe Demir', 'Mehmet Kaya', 'Zeynep Şahin',
            'Can Öztürk', 'Elif Yıldız', 'Burak Arslan', 'Seda Çelik',
            'Cem Koç', 'Deniz Aydın', 'Emre Güneş', 'Fatma Kurt'
        ],
        'graduation_year': [
            2015, 2016, 2014, 2017, 2015, 2018, 2016, 2015,
            2017, 2014, 2016, 2018
        ],
        'first_job': [
            'Junior Data Analyst', 'Research Assistant', 'Business Analyst',
            'Data Analyst', 'Statistical Analyst', 'Junior Data Scientist',
            'Analytics Intern', 'Data Analyst', 'Research Scientist',
            'Data Engineer', 'Machine Learning Engineer', 'Data Analyst'
        ],
        'current_position': [
            'Senior Data Scientist', 'Data Science Manager', 'Lead Data Analyst',
            'Senior ML Engineer', 'Data Science Lead', 'Staff Data Scientist',
            'Principal Data Scientist', 'Senior Data Analyst', 'ML Research Lead',
            'Senior Data Engineer', 'ML Engineering Manager', 'Senior Data Scientist'
        ],
        'years_experience': [9, 8, 10, 7, 9, 6, 8, 9, 7, 10, 8, 6],
        'education_level': [
            'BS', 'MS', 'BS', 'MS', 'PhD', 'MS',
            'BS', 'BS', 'PhD', 'MS', 'MS', 'BS'
        ],
        'estimated_salary_usd': [
            85000, 95000, 78000, 92000, 110000, 88000,
            105000, 72000, 115000, 90000, 100000, 75000
        ],
        'career_transitions': [3, 4, 2, 3, 2, 3, 4, 2, 2, 3, 4, 2],
        'notes': [
            'FAANG company, remote work',
            'Tech lead role, startup experience',
            'Finance sector, stable growth',
            'AI/ML specialist',
            'Research to industry transition',
            'Product-focused data science',
            'Multiple startups, high growth',
            'Traditional corporate path',
            'Academic to industry, PhD advantage',
            'Data infrastructure specialist',
            'Team management focus',
            'Early career, fast progression'
        ]
    }
    
    df = pd.DataFrame(data)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'outputs/career_paths_{timestamp}.csv'
    df.to_csv(filename, index=False)
    print(f"\n✅ Career paths data generated: {filename}")
    return filename

def generate_roi_analysis():
    """Generate ROI analysis"""
    scenarios = {
        'Scenario': [
            'Direct Work (No Master)',
            'Master\'s Degree (2 years)',
            'PhD Degree (5 years)'
        ],
        'Education_Years': [0, 2, 5],
        'Education_Cost_USD': [0, 20000, 0],
        'Starting_Salary_USD': [30000, 45000, 60000],
        'Annual_Raise': ['10%', '12%', '15%'],
        'Working_Years': [15, 13, 10],
        'Total_Earnings_15yr_USD': [726984, 813916, 809747],
        'NPV_USD': [589243, 612407, 556194],
        'Final_Year_Salary_USD': [114523, 158094, 243588]
    }
    
    df = pd.DataFrame(scenarios)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'outputs/education_vs_work_{timestamp}.xlsx'
    df.to_excel(filename, index=False, engine='openpyxl')
    print(f"✅ ROI analysis generated: {filename}")
    return filename

def generate_fire_plan():
    """Generate FIRE plan"""
    report = f"""# 🔥 FIRE Plan - Erken Emeklilik Stratejisi

**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 📊 Executive Summary

- **Current Age**: 25
- **Target Retirement Age**: 40
- **Time Horizon**: 15 years
- **Target Portfolio**: $600,000
- **Annual Passive Income** (4% rule): $24,000/year

---

## 💰 Financial Projections

### Yıllık Birikim Hedefleri

| Year | Age | Salary | Savings Rate | Annual Savings | Total Portfolio | Status |
|------|-----|--------|--------------|----------------|-----------------|--------|
| 1    | 25  | $40,000 | 30% | $12,000 | $12,800 | ✅ On Track |
| 2    | 26  | $44,000 | 35% | $15,400 | $29,168 | ✅ On Track |
| 3    | 27  | $48,400 | 35% | $16,940 | $49,279 | ✅ On Track |
| 4    | 28  | $53,240 | 40% | $21,296 | $74,625 | ✅ On Track |
| 5    | 29  | $58,564 | 40% | $23,426 | $105,524 | ✅ On Track |
| 8    | 32  | $77,136 | 45% | $34,711 | $231,849 | ✅ On Track |
| 10   | 35  | $92,973 | 45% | $41,838 | $351,487 | ✅ On Track |
| 12   | 37  | $112,106 | 50% | $56,053 | $507,293 | ✅ On Track |
| 15   | 40  | $149,474 | 50% | $74,737 | $625,194 | 🎯 Target Reached! |

---

## 🎯 Investment Strategy

### Asset Allocation

- **US Stock Market ETFs** (60%): $360K
  - VTI, VOO, QQQ
- **International ETFs** (20%): $120K
  - VXUS, VEA
- **Bonds** (10%): $60K
  - BND, AGG
- **Alternative/Crypto** (10%): $60K
  - Bitcoin, Ethereum

### Expected Returns
- Average annual return: 8%
- Conservative estimate: 7%
- Aggressive estimate: 10%

---

## 📉 Risk Management

### Bear Market Scenario
- Portfolio drop: -30% ($420K → $294K)
- Recovery time: 2-3 years
- **Mitigation**: Keep 2 years expenses in cash ($48K)

### Recession Protection
- Emergency fund: 6 months expenses ($12K)
- Diversified income streams
- Side hustles as buffer

---

## 💡 Optimization Strategies

### Yaşam Giderleri
1. **Housing**: Roommate veya ebeveynlerle kalma (5 yıl)
2. **Transportation**: Toplu taşıma kullanımı
3. **Food**: Evde yemek, meal prep
4. **Entertainment**: Ücretsiz/düşük maliyetli aktiviteler

### Gelir Artırma
1. **Salary negotiation**: Yıllık %10-15 artış hedefle
2. **Side hustles**: $500-2000/ay ek gelir
3. **Freelancing**: Data analysis, ML consulting
4. **Passive income**: Blog, YouTube, courses

---

## 📅 Milestone Tracker

- ✅ **$50K** (Year 3): İlk büyük baraj
- ✅ **$100K** (Year 5): Momentum kazanma
- 🎯 **$250K** (Year 8): Yarı yol
- 🎯 **$400K** (Year 11): Home stretch
- 🎯 **$600K** (Year 15): Financial Independence! 🎉

---

## 🚀 Action Plan

### Immediate (Next 30 days)
1. ✅ Open Vanguard/Fidelity account
2. ✅ Set up automatic transfers ($1000/month)
3. ✅ Start side hustle research
4. ✅ Create detailed budget tracker

### Short-term (6 months)
1. Launch first side hustle
2. Reach $5K invested
3. Optimize monthly expenses by 20%
4. Build emergency fund ($5K)

### Long-term (2+ years)
1. Launch second income stream
2. Hit $50K net worth
3. Consider real estate investment
4. Reassess and adjust strategy

---

**Remember**: FIRE is a marathon, not a sprint. Stay consistent, track progress, and adjust as needed! 💪
"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'outputs/retirement_plan_{timestamp}.md'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"✅ FIRE plan generated: {filename}")
    return filename

def generate_microbusiness_report():
    """Generate microbusiness opportunities report"""
    report = f"""# 🚀 Mikro İş Fırsatları Raporu

**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 💼 SaaS Ürün Fırsatları

### 1. Email Automation Tool for Researchers
**Tahmini Aylık Gelir**: $2,000-$5,000  
**Başlangıç Maliyeti**: $500  
**Geliştirme Süresi**: 3 ay  
**Teknik Beceriler**: Python, Flask/FastAPI, Stripe API  
**Risk Seviyesi**: Orta  

**Açıklama**: Akademisyenler ve araştırmacılar için otomatik email takibi, hatırlatma ve collaboration tool.

**Örnek**: SimpleResearchCRM - $3K/month MRR ile çalışıyor

---

### 2. LinkedIn Profile Analyzer
**Tahmini Aylık Gelir**: $1,500-$3,000  
**Başlangıç Maliyeti**: $300  
**Geliştirme Süresi**: 2 ay  
**Teknik Beceriler**: Python, Web scraping, NLP  
**Risk Seviyesi**: Düşük  

**Açıklama**: Kullanıcıların LinkedIn profilini analiz edip kariyer tavsiyeleri veren AI tool.

---

## 📱 Mobil Uygulama Fırsatları

### 3. FIRE Progress Tracker App
**Tahmini Aylık Gelir**: $1,000-$2,500  
**Başlangıç Maliyeti**: $0 (tek kişi geliştirme)  
**Geliştirme Süresi**: 2-3 ay  
**Teknik Beceriler**: React Native / Flutter  
**Risk Seviyesi**: Düşük  

**Açıklama**: Erken emeklilik hedefi olanlar için net worth tracker, investment calculator, milestone tracker.

**Monetization**: Freemium ($4.99/month premium)

---

### 4. Statistics Problem Solver
**Tahmini Aylık Gelir**: $800-$2,000  
**Başlangıç Maliyeti**: $200  
**Geliştirme Süresi**: 2 ay  
**Teknik Beceriler**: R, Python, Mobile development  
**Risk Seviyesi**: Orta  

**Açıklama**: Öğrenciler için istatistik problemlerini AI ile çözen, adım adım açıklama veren uygulama.

---

## 🎨 Template & Design Fırsatları

### 5. Notion Finance Templates
**Tahmini Aylık Gelir**: $500-$1,500  
**Başlangıç Maliyeti**: $0  
**Geliştirme Süresi**: 1 ay  
**Teknik Beceriler**: Notion, Design, Marketing  
**Risk Seviyesi**: Çok Düşük  

**Açıklama**: FIRE planlama, budget tracking, investment tracker Notion şablonları.

**Satış Platformu**: Gumroad, Etsy, kendi website

---

### 6. Data Visualization Templates (Tableau/Power BI)
**Tahmini Aylık Gelir**: $600-$1,800  
**Başlangıç Maliyeti**: $100  
**Geliştirme Süresi**: 1-2 ay  
**Teknik Beceriler**: Tableau, Power BI, Data viz  
**Risk Seviyesi**: Düşük  

---

## 📚 İçerik & Eğitim

### 7. "Statistics to Data Science" Online Course
**Tahmini Aylık Gelir**: $1,000-$4,000  
**Başlangıç Maliyeti**: $200 (hosting, equipment)  
**Geliştirme Süresi**: 3-4 ay  
**Teknik Beceriler**: Video editing, İçerik oluşturma  
**Risk Seviyesi**: Orta  

**Platform**: Udemy, Teachable, kendi site

---

### 8. FIRE Türkiye Newsletter
**Tahmini Aylık Gelir**: $300-$1,200  
**Başlangıç Maliyeti**: $50  
**Geliştirme Süresi**: 1 ay (başlangıç)  
**Teknik Beceriler**: Writing, Marketing, Substack  
**Risk Seviyesi**: Çok Düşük  

**Monetization**: Sponsorships, premium subscriptions

---

## 🏆 Öncelik Sıralaması

### Tier 1: Hızlı Başlangıç (1-2 ay)
1. **Notion Finance Templates** - En düşük risk, hızlı gelir
2. **FIRE Türkiye Newsletter** - Community building

### Tier 2: Orta Vade (2-3 ay)
3. **LinkedIn Profile Analyzer** - Good market fit
4. **FIRE Progress Tracker App** - Solves own problem

### Tier 3: Uzun Vade (3-6 ay)
5. **Email Automation for Researchers** - High potential
6. **Statistics to Data Science Course** - Passive income

---

## 💡 Başarı İpuçları

1. **Start Small**: İlk ürünü mükemmel yapmaya çalışma, MVP yap
2. **Solve Your Own Problem**: Kendi kullandığın bir şey yap
3. **Build in Public**: Twitter/X'te progress paylaş
4. **Talk to Users**: İlk 10 kullanıcıyla konuş
5. **Iterate Fast**: Haftada bir güncelleme yap

---

## 📊 Gerçekçi Beklentiler

**İlk 3 Ay**: $0-$200/month (normal!)  
**6 Ay**: $200-$1000/month  
**1 Yıl**: $1000-$3000/month  
**2 Yıl**: $2000-$10K/month (eğer başarılıysa)

---

**Remember**: %90'ı başarısız olur, ama denemezsen %100 başarısız olursun! 💪
"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'outputs/microbusiness_report_{timestamp}.md'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"✅ Microbusiness report generated: {filename}")
    return filename

def main():
    print("\n" + "="*60)
    print("🚀 Early Retirement Workflow - DEMO MODE")
    print("="*60)
    print("\nGenerating mock data for demonstration...\n")
    
    # Generate all outputs
    career_file = generate_career_paths()
    roi_file = generate_roi_analysis()
    fire_file = generate_fire_plan()
    micro_file = generate_microbusiness_report()
    
    print("\n" + "="*60)
    print("✅ Demo completed successfully!")
    print("="*60)
    print("\n📁 Generated files:")
    print(f"   - {career_file}")
    print(f"   - {roi_file}")
    print(f"   - {fire_file}")
    print(f"   - {micro_file}")
    print("\n💡 This is demo data. For real analysis, add API keys to .env")
    print("   and run: python main.py\n")

if __name__ == "__main__":
    main()
