#!/usr/bin/env python3
"""
Personalized FIRE Workflow - Takes user input and creates custom analysis
"""

import os
from dotenv import load_dotenv
from groq import Groq
from datetime import datetime
import json

load_dotenv()
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def call_ai(prompt: str, system: str) -> str:
    """Call Groq API"""
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


def get_user_profile():
    """Interactive user profiling"""
    print("\n" + "="*60)
    print("👤 KİŞİSEL PROFİL OLUŞTURMA")
    print("="*60 + "\n")
    
    profile = {}
    
    # Basic Info
    profile['name'] = input("📝 İsminiz: ").strip() or "Kullanıcı"
    profile['age'] = int(input("🎂 Yaşınız: ").strip() or "25")
    profile['university'] = input("🎓 Üniversite: ").strip() or "ODTÜ"
    profile['major'] = input("📚 Bölüm: ").strip() or "İstatistik"
    profile['graduation_year'] = int(input("🎯 Mezuniyet Yılı: ").strip() or "2024")
    
    # Current Status
    print("\n📊 Mevcut Durum")
    profile['current_job'] = input("💼 Şu anki işiniz (boş bırak yoksa): ").strip() or "Henüz çalışmıyor"
    profile['current_salary'] = input("💰 Şu anki maaşınız (USD, boş bırak yoksa): ").strip() or "0"
    
    # Skills
    print("\n🛠️  Teknik Beceriler")
    profile['programming'] = input("💻 Programlama dilleri (ör: Python, R): ").strip() or "Python, R"
    profile['ml_experience'] = input("🤖 ML/AI deneyimi (0-5 yıl): ").strip() or "1"
    profile['other_skills'] = input("🔧 Diğer beceriler: ").strip() or "Statistics, Data Analysis"
    
    # Education Plans
    print("\n🎓 Eğitim Planları")
    profile['education_plan'] = input("📖 Master/PhD planın var mı? (evet/hayır): ").strip().lower() or "hayır"
    if profile['education_plan'] == "evet":
        profile['education_type'] = input("   Hangisi? (master/phd): ").strip().lower() or "master"
        profile['education_field'] = input("   Hangi alan?: ").strip() or "Data Science"
    
    # Career Goals
    print("\n🎯 Kariyer Hedefleri")
    profile['dream_job'] = input("💫 Hedef pozisyon: ").strip() or "Senior Data Scientist"
    profile['target_salary'] = int(input("💵 Hedef maaş (USD): ").strip() or "100000")
    
    # FIRE Goals
    print("\n🔥 Erken Emeklilik Hedefi")
    profile['target_retirement_age'] = int(input("🎂 Kaç yaşında emekli olmak istiyorsun?: ").strip() or "40")
    profile['target_portfolio'] = int(input("💰 Hedef birikim (USD): ").strip() or "600000")
    profile['risk_tolerance'] = input("📊 Risk toleransın (düşük/orta/yüksek): ").strip().lower() or "orta"
    
    # Side Hustle Interests
    print("\n🚀 Yan Gelir İlgi Alanları")
    profile['side_interests'] = input("💡 İlgilendiğin alanlar (ör: SaaS, App, Course): ").strip() or "SaaS, Course"
    profile['available_time'] = input("⏰ Haftada kaç saat ayırabilirsin?: ").strip() or "10"
    
    print("\n✅ Profil oluşturuldu!\n")
    return profile


def analyze_career_path(profile):
    """Personalized career path analysis"""
    print("🔍 1/4 - Kişiselleştirilmiş kariyer yolu analizi...")
    
    system = "Sen deneyimli bir kariyer danışmanısın. Kişiye özel, gerçekçi ve ulaşılabilir kariyer tavsiyeleri veriyorsun."
    
    prompt = f"""Aşağıdaki profil için KİŞİSELLEŞTİRİLMİŞ kariyer yolu analizi yap:

**Profil:**
- İsim: {profile['name']}
- Yaş: {profile['age']}
- Eğitim: {profile['university']} - {profile['major']} ({profile['graduation_year']})
- Şu anki durum: {profile['current_job']}
- Mevcut maaş: ${profile['current_salary']}
- Beceriler: {profile['programming']}, {profile['other_skills']}
- ML deneyimi: {profile['ml_experience']} yıl
- Eğitim planı: {profile.get('education_plan', 'hayır')}
- Hedef pozisyon: {profile['dream_job']}
- Hedef maaş: ${profile['target_salary']}

BU KİŞİYE ÖZEL:
1. Şu andan hedef pozisyona nasıl ulaşır? (Adım adım plan)
2. Hangi becerileri geliştirmeli?
3. Hangi sertifikalar/projeler işine yarar?
4. Gerçekçi timeline (kaç yılda hedefine ulaşır?)
5. Maaş artışı projeksiyonu (yıl bazında)
6. Bu profille benzer başarılı örnekler var mı?

Markdown formatında, tablolar ve emoji kullan."""

    result = call_ai(prompt, system)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'outputs/personal_career_plan_{profile["name"]}_{timestamp}.md'
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# 🎯 Kişisel Kariyer Planı - {profile['name']}\n\n")
        f.write(f"**Oluşturulma**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(result)
    
    print(f"   ✅ {filename}")
    return result


def create_personalized_roi(profile):
    """Personalized education ROI"""
    print("💰 2/4 - Senin için eğitim ROI analizi...")
    
    system = "Sen finansal analiz uzmanısın. Gerçek verilerle, kişiye özel ROI hesaplamaları yaparsın."
    
    current_age = profile['age']
    target_age = profile['target_retirement_age']
    years_left = target_age - current_age
    
    prompt = f"""BU KİŞİ İÇİN eğitim ROI analizi:

**Profil:**
- Yaş: {current_age}
- Hedef emeklilik yaşı: {target_age} ({years_left} yıl var)
- Şu anki maaş: ${profile['current_salary']}
- Hedef maaş: ${profile['target_portfolio']}
- Eğitim planı: {profile.get('education_plan', 'hayır')}

3 SENARYO KARŞILAŞTIR:
1. Şimdi işe başla (eğitim yok)
2. Master yap (2 yıl) - {profile.get('education_field', 'Data Science')} alanında
3. PhD yap (5 yıl) - Akademik kariyer seçeneği

Her senaryo için:
- {years_left} yıl içinde toplam kazanç
- NPV hesabı (discount rate 5%)
- Hangi yaşta ne kadar birikmiş olur
- Hangi senaryo bu kişi için EN UYGUN?

ÖNEMLİ: Bu kişinin {target_age} yaşında ${profile['target_portfolio']} biriktirme hedefine hangisi daha iyi ulaştırır?

Markdown, tablolar, emoji kullan."""

    result = call_ai(prompt, system)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'outputs/personal_roi_{profile["name"]}_{timestamp}.md'
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# 💰 Kişisel ROI Analizi - {profile['name']}\n\n")
        f.write(f"**Oluşturulma**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(result)
    
    print(f"   ✅ {filename}")
    return result


def create_personalized_fire(profile):
    """Personalized FIRE plan"""
    print("🔥 3/4 - Senin için FIRE planı...")
    
    system = "Sen FIRE (Financial Independence Retire Early) uzmanısın. Kişiye özel, gerçekçi erken emeklilik planları oluşturursun."
    
    current_age = profile['age']
    target_age = profile['target_retirement_age']
    years = target_age - current_age
    current_salary = int(profile['current_salary']) if profile['current_salary'].isdigit() else 40000
    target = profile['target_portfolio']
    
    prompt = f"""BU KİŞİ İÇİN özel FIRE planı oluştur:

**Profil:**
- İsim: {profile['name']}
- Şu anki yaş: {current_age}
- Hedef emeklilik yaşı: {target_age}
- Süre: {years} yıl
- Şu anki maaş: ${current_salary}
- Hedef birikim: ${target}
- Risk toleransı: {profile['risk_tolerance']}

DETAYLI PLAN:
1. Yıl bazında birikim tablosu (her yıl için: yaş, maaş, tasarruf, toplam birikim)
2. Aylık ne kadar biriktirmeli?
3. Hangi yatırım araçları? (risk toleransına göre)
4. Asset allocation önerisi
5. Alternatif senaryolar (bear market, iş kaybı, vs.)
6. Bu sürede yan gelir önemli mi? Ne kadar katkı sağlar?
7. Milestone'lar (1 yıl: $X, 5 yıl: $Y, vb.)

ÖNEMLİ: {years} yılda ${target} biriktirmek GERÇEKÇİ mi? Değilse ne kadar gerçekçi?

Markdown, detaylı tablolar, emoji kullan."""

    result = call_ai(prompt, system)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'outputs/personal_fire_{profile["name"]}_{timestamp}.md'
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# 🔥 Kişisel FIRE Planı - {profile['name']}\n\n")
        f.write(f"**Oluşturulma**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(result)
    
    print(f"   ✅ {filename}")
    return result


def suggest_side_hustles(profile):
    """Personalized side hustle suggestions"""
    print("🚀 4/4 - Senin için yan gelir önerileri...")
    
    system = "Sen girişimcilik danışmanısın. Kişinin becerilerine, zamanına ve ilgi alanlarına göre yan gelir önerileri veriyorsun."
    
    prompt = f"""BU KİŞİ İÇİN kişiselleştirilmiş yan gelir önerileri:

**Profil:**
- İsim: {profile['name']}
- Beceriler: {profile['programming']}, {profile['other_skills']}
- ML deneyimi: {profile['ml_experience']} yıl
- İlgi alanları: {profile['side_interests']}
- Haftada ayırabileceği zaman: {profile['available_time']} saat
- Risk toleransı: {profile['risk_tolerance']}

BU KİŞİYE ÖZEL 5-6 FİKİR:
1. Bu becerilere uygun fikirler
2. Haftada {profile['available_time']} saatte yapılabilir projeler
3. Risk toleransına uygun seçenekler

Her fikir için:
- Tahmini aylık gelir
- Başlangıç maliyeti
- Geliştirme süresi
- Hangi becerileri kullanacak?
- Gerçek başarı örnekleri
- İlk adımlar (ne yapmalı?)

Öncelik sıralaması: HEMEN başlayabileceklerden başla!

Markdown, tablolar, emoji, actionable advice kullan."""

    result = call_ai(prompt, system)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'outputs/personal_sidehustle_{profile["name"]}_{timestamp}.md'
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# 🚀 Kişisel Yan Gelir Önerileri - {profile['name']}\n\n")
        f.write(f"**Oluşturulma**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(result)
    
    print(f"   ✅ {filename}")
    return result


def main():
    print("\n" + "="*60)
    print("🎯 KİŞİSELLEŞTİRİLMİŞ FIRE WORKFLOW")
    print("="*60)
    print("\n💡 Bu versiyon SENIN profilini alacak ve")
    print("   SANA ÖZEL analiz yapacak!\n")
    print("="*60 + "\n")
    
    # Check API key
    if not os.getenv('GROQ_API_KEY'):
        print("❌ Error: GROQ_API_KEY not found")
        return
    
    os.makedirs('outputs', exist_ok=True)
    
    # Get user profile
    profile = get_user_profile()
    
    # Save profile
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    profile_file = f'outputs/user_profile_{profile["name"]}_{timestamp}.json'
    with open(profile_file, 'w', encoding='utf-8') as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)
    
    print(f"📝 Profil kaydedildi: {profile_file}\n")
    
    print("="*60)
    print("🤖 AI AJANLAR ÇALIŞIYOR...")
    print("="*60 + "\n")
    
    # Run personalized analysis
    files = []
    
    try:
        # Career path analysis
        analyze_career_path(profile)
        
        # ROI analysis
        create_personalized_roi(profile)
        
        # FIRE plan
        create_personalized_fire(profile)
        
        # Side hustles
        suggest_side_hustles(profile)
        
        print("\n" + "="*60)
        print(f"✅ {profile['name']} İÇİN KİŞİSEL PLAN HAZIR!")
        print("="*60)
        print(f"\n📁 Dosyalar outputs/ klasöründe:")
        print(f"   - Kişisel kariyer planı")
        print(f"   - ROI analizi")
        print(f"   - FIRE planı")
        print(f"   - Yan gelir önerileri")
        print(f"   - Profil bilgileri (JSON)\n")
        
    except Exception as e:
        print(f"\n❌ Hata: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
