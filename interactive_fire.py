#!/usr/bin/env python3
"""
Interactive FIRE Workflow - Shows output directly in terminal
No file saving, just beautiful terminal output
"""

import os
from dotenv import load_dotenv
from groq import Groq
from datetime import datetime

load_dotenv()
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def print_section(title, emoji="🎯"):
    """Print formatted section header"""
    print("\n" + "="*70)
    print(f"{emoji} {title}")
    print("="*70 + "\n")

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

def get_user_input():
    """Get user profile interactively - DETAILED VERSION for undecided people"""
    print_section("KİŞİSEL PROFİL OLUŞTURMA", "👤")

    print("💭 Merhaba! Kariyer ve emeklilik planın konusunda kararsız mısın?")
    print("   Doğru kararları vermene yardımcı olmak için detaylı sorular soracağım.\n")

    profile = {}

    # ============ TEMEL BİLGİLER ============
    print("📝 Önce seninle tanışalım")
    print("-" * 70)
    profile['name'] = input("   Adın ne? ").strip() or "Kullanıcı"
    print(f"\n   Merhaba {profile['name']}! 👋")
    profile['age'] = input("   Kaç yaşındasın? ").strip() or "25"
    profile['university'] = input("   Hangi üniversitedesin (veya mezun oldun)? ").strip() or "ODTÜ"
    profile['major'] = input("   Bölümün ne? ").strip() or "İstatistik"
    profile['grad_year'] = input("   Ne zaman mezun oldun/olacaksın? ").strip() or "2024"
    profile['location'] = input("   Şu an nerede yaşıyorsun? ").strip() or "Türkiye"
    profile['relocation_ok'] = input("   Yurt dışına taşınma fikri nasıl geliyor? (evet/hayır/belki) ").strip() or "belki"

    # ============ MEVCUT DURUM - DETAYLI ============
    print(f"\n💼 Şimdi biraz {profile['name']}'in şu anki durumundan bahsedelim")
    print("-" * 70)
    profile['current_job'] = input("   Şu an ne iş yapıyorsun? (öğrenciysen 'öğrenci' yaz) ").strip() or "Yeni mezun"
    if profile['current_job'].lower() not in ['öğrenci', 'yok', 'işsiz']:
        profile['current_salary'] = input("   Net maaşın ne kadar? (USD olarak, yaklaşık) ").strip() or "0"
        profile['job_satisfaction'] = input("   İşinden ne kadar memnunsun? (1-10 arası) ").strip() or "5"
        profile['years_current_job'] = input("   Bu işte kaç yıldır çalışıyorsun? ").strip() or "0"
        profile['industry'] = input("   Hangi sektördesin? (tech, finans, eğitim...) ").strip() or "tech"
        profile['company_size'] = input("   Şirket büyüklüğü nasıl? (startup/orta/büyük) ").strip() or "orta"
    else:
        profile['current_salary'] = "0"
        profile['job_satisfaction'] = "0"
        profile['years_current_job'] = "0"
        profile['industry'] = "none"
        profile['company_size'] = "none"

    # ============ BECERİLER - ÇOK DETAYLI ============
    print("\n🛠️  Beceriler - Detaylı Envanter")
    print("-" * 70)
    profile['programming_langs'] = input("   Bildiğin programlama dilleri (virgülle ayır): ").strip() or "Python, R, SQL"
    profile['prog_level'] = input("   Programlama seviyeni nasıl değerlendirirsin (başlangıç/orta/ileri): ").strip() or "orta"
    profile['ml_exp'] = input("   ML/AI deneyimi (kaç yıl, eğer varsa): ").strip() or "1"
    profile['frameworks'] = input("   Bildiğin framework'ler (TensorFlow, PyTorch, vb.): ").strip() or "scikit-learn"
    profile['cloud_exp'] = input("   Cloud experience (AWS/Azure/GCP - hangileri): ").strip() or "yok"
    profile['data_tools'] = input("   Veri araçları (Tableau, PowerBI, Excel, vb.): ").strip() or "Excel, PowerBI"
    profile['github_projects'] = input("   GitHub'da kaç projen var: ").strip() or "0"
    profile['certifications'] = input("   Sertifikalarını yaz (varsa, virgülle ayır): ").strip() or "yok"

    # ============ EĞİTİM KARARLARI ============
    print("\n🎓 Eğitim Kararları")
    print("-" * 70)
    profile['considering_masters'] = input("   Master düşünüyor musun? (evet/hayır/kararsızım): ").strip() or "kararsızım"
    profile['masters_field'] = input("   Hangi alanda master yapacaksın (DS, CS, Stats, vb.): ").strip() or "Data Science"
    profile['masters_location'] = input("   Nerede yapacaksın (Türkiye/Yurt dışı/Online): ").strip() or "kararsızım"
    profile['can_afford_masters'] = input("   Master için maddi imkanın var mı? (evet/hayır/kısmen): ").strip() or "kısmen"
    profile['masters_timeline'] = input("   Ne zaman başlamayı planlıyorsun (bu yıl/gelecek yıl/2+ yıl): ").strip() or "bilmiyorum"

    # ============ KARİYER HEDEFLERİ - DETAYLI ============
    print("\n🎯 Kariyer Hedefleri - Sen Ne İstiyorsun Gerçekten?")
    print("-" * 70)
    profile['dream_job'] = input("   İdeal pozisyon (5 yıl sonra nerede olmak istersin): ").strip() or "Senior Data Scientist"
    profile['alternative_jobs'] = input("   Alternatif pozisyonlar (virgülle ayır): ").strip() or "ML Engineer, Data Engineer"
    profile['target_salary'] = input("   Hedef maaş - 5 yıl sonra (USD): ").strip() or "100000"
    profile['salary_vs_passion'] = input("   Maaş mı önemli yoksa tutku mu? (maaş/tutku/ikisi de): ").strip() or "ikisi de"
    profile['work_life_balance'] = input("   Work-life balance ne kadar önemli (1-10): ").strip() or "7"
    profile['career_speed'] = input("   Kariyerinde ne kadar hızlı ilerlemek istersin (yavaş/orta/hızlı): ").strip() or "hızlı"

    # ============ FİNANSAL DURUM ============
    print("\n💰 Finansal Durum - Açık Ol")
    print("-" * 70)
    profile['monthly_expenses'] = input("   Aylık harcaman ne kadar (USD): ").strip() or "1000"
    profile['savings'] = input("   Şu anki birikimlerin (USD): ").strip() or "0"
    profile['debt'] = input("   Borcun var mı, ne kadar (USD): ").strip() or "0"
    profile['family_support'] = input("   Aileden finansal destek alıyor musun? (evet/hayır/bazen): ").strip() or "hayır"
    profile['dependents'] = input("   Bakman gereken kimse var mı? (evet/hayır): ").strip() or "hayır"
    profile['risk_tolerance'] = input("   Risk alma toleransın (düşük/orta/yüksek): ").strip() or "orta"

    # ============ EMEKLİLİK VİZYONU ============
    print("\n🔥 Emeklilik Vizyonu - Gerçekten Erken Emekli Olmak İstiyor musun?")
    print("-" * 70)
    profile['retire_age'] = input("   Kaç yaşında emekli olmak istersin: ").strip() or "40"
    profile['why_fire'] = input("   Neden erken emekli olmak istiyorsun (kısaca): ").strip() or "özgürlük"
    profile['target_portfolio'] = input("   Emeklilik için hedef birikim (USD): ").strip() or "600000"
    profile['retirement_lifestyle'] = input("   Emeklilikte nasıl yaşamak istersin (sade/orta/lüks): ").strip() or "orta"
    profile['retirement_location'] = input("   Nerede emekli olmak istersin: ").strip() or "Türkiye"
    profile['passive_income_goal'] = input("   Aylık hedef pasif gelir (USD): ").strip() or "2000"

    # ============ YAN GELİR & GİRİŞİMCİLİK ============
    print("\n🚀 Yan Gelir & Girişimcilik")
    print("-" * 70)
    profile['side_hustle_interest'] = input("   Yan iş yapmak ister misin? (evet/hayır/belki): ").strip() or "evet"
    profile['interests'] = input("   İlgi alanların (SaaS, Kurs, Freelance, vb.): ").strip() or "SaaS, Kurs"
    profile['weekly_hours'] = input("   Yan işe haftada kaç saat ayırabilirsin: ").strip() or "10"
    profile['entrepreneurial'] = input("   Girişimci ruhun var mı? (1-10): ").strip() or "7"
    profile['startup_idea'] = input("   Aklında bir startup fikri var mı? (varsa yaz): ").strip() or "yok"
    profile['freelance_exp'] = input("   Freelance deneyimin var mı? (evet/hayır): ").strip() or "hayır"

    # ============ KİŞİLİK & ÇALIŞMA TARZI ============
    print("\n🧠 Kişilik & Çalışma Tarzı")
    print("-" * 70)
    profile['learning_style'] = input("   Nasıl öğrenirsin (okuyarak/yaparak/izleyerek): ").strip() or "yaparak"
    profile['team_vs_solo'] = input("   Takım mı yoksa solo çalışmayı mı seversin: ").strip() or "takım"
    profile['introvert_extrovert'] = input("   Introvert mi extrovert mi: ").strip() or "introvert"
    profile['decision_making'] = input("   Karar vermekte zorlanır mısın? (evet/hayır/bazen): ").strip() or "evet"
    profile['biggest_fear'] = input("   Kariyerle ilgili en büyük korku: ").strip() or "yanlış seçim yapmak"

    # ============ ZAMAN KISITLARI ============
    print("\n⏰ Zaman Kısıtları")
    print("-" * 70)
    profile['time_urgency'] = input("   Ne kadar acilen değişim istiyorsun (hemen/6ay/1yıl/acelem yok): ").strip() or "6ay"
    profile['daily_learning_hours'] = input("   Günde kaç saat öğrenmeye ayırabilirsin: ").strip() or "2"

    return profile

def show_career_analysis(profile):
    """Show career path analysis - PERSONALIZED"""
    print_section("KARİYER YOLU ANALİZİ", "🔍")
    print("⏳ Detaylı profiline göre kariyer yolu oluşturuluyor...\n")

    system = "Sen deneyimli bir kariyer koçusun. Kararsız insanlara NET ve UYGULANABILIR yol haritaları çıkarıyorsun."

    prompt = f"""ÇOK DETAYLI KİŞİSEL KARİYER ANALİZİ:

👤 KİŞİ:
- {profile['name']}, {profile['age']} yaş, {profile['university']} {profile['major']} ({profile['grad_year']})
- Lokasyon: {profile['location']}, Yurt dışı: {profile['relocation_ok']}
- Karar verme: {profile['decision_making']}, En büyük korku: {profile['biggest_fear']}

💼 MEVCUT DURUM:
- Pozisyon: {profile['current_job']} (${profile['current_salary']})
- Memnuniyet: {profile['job_satisfaction']}/10, Tecrübe: {profile['years_current_job']} yıl
- Sektör: {profile['industry']}, Şirket: {profile['company_size']}

🛠️ BECERİLER:
- Diller: {profile['programming_langs']} (Seviye: {profile['prog_level']})
- ML: {profile['ml_exp']} yıl, Framework: {profile['frameworks']}
- Cloud: {profile['cloud_exp']}, Tools: {profile['data_tools']}
- GitHub: {profile['github_projects']} proje, Sertifika: {profile['certifications']}

🎓 EĞİTİM:
- Master: {profile['considering_masters']} ({profile['masters_field']})
- Nerede: {profile['masters_location']}, Maddi: {profile['can_afford_masters']}
- Zaman: {profile['masters_timeline']}

🎯 HEDEF:
- Pozisyon: {profile['dream_job']} (Alternatif: {profile['alternative_jobs']})
- Maaş: ${profile['target_salary']} (Öncelik: {profile['salary_vs_passion']})
- Hız: {profile['career_speed']}, Work-life: {profile['work_life_balance']}/10

⏰ ZAMAN:
- Aciliyet: {profile['time_urgency']}
- Günlük öğrenme: {profile['daily_learning_hours']} saat

BU KİŞİ İÇİN DETAYLI KARİYER PLANI ÇıKAR:

1️⃣ ŞU ANKİ DURUMU ANALİZ:
   - Güçlü yönler (3 madde)
   - Eksikler/Riskler (3 madde)
   - Master yapmalı mı? (açık karar + sebep)

2️⃣ ADIM ADIM YOL HARİTASI:
   - İlk 3 ay: ne yapmalı (somut aksiyonlar)
   - 6 ay - 1 yıl: hangi beceriler/sertifikalar
   - 1-2 yıl: pozisyon değişiklikleri
   - 3-5 yıl: hedef pozisyona ulaşma

3️⃣ ÖNCELİKLİ BECERI LİSTESİ:
   - HEMEN öğrenmesi gerekenler (1-3 ay)
   - Orta vade (3-12 ay)
   - Uzun vade (1-2 yıl)

4️⃣ PROJE & SERTİFİKA:
   - Bu kişiye özel 3 proje önerisi
   - Alması gereken 2-3 sertifika (öncelik sırasıyla)

5️⃣ MAAŞ & ZAMAN PROJEKSİYONU:
   Yıl | Pozisyon | Maaş | Not
   0   | {profile['current_job']} | ${profile['current_salary']} | Şu an
   1   | ?
   2   | ?
   3   | ?
   5   | {profile['dream_job']} | ${profile['target_salary']} | Hedef

6️⃣ RİSKLER & UYARILAR:
   - Bu planda başarısız olma ihtimali nedir?
   - Nelere dikkat etmeli?
   - Plan B ne olmalı?

KISA, NET, UYGULANABILIR yaz. Max 40 satır."""

    result = call_ai(prompt, system)
    print(result)
    print("\n" + "─" * 70)

def show_roi_analysis(profile):
    """Show education ROI - PERSONALIZED"""
    print_section("EĞİTİM ROI ANALİZİ", "💰")
    print("⏳ Senin durumuna özel finansal analiz yapılıyor...\n")

    system = "Sen finansal analiz ve eğitim danışmanlığı uzmanısın. Kararsız insanlara NET KARAR vermelerine yardım ediyorsun."

    years_left = int(profile['retire_age']) - int(profile['age'])

    prompt = f"""KİŞİYE ÖZEL EĞİTİM ROI ANALİZİ:

👤 DURUM:
- {profile['name']}, {profile['age']} yaş, {profile['university']} {profile['major']}
- Master: {profile['considering_masters']}, Alan: {profile['masters_field']}
- Lokasyon: {profile['masters_location']}, Maddi durum: {profile['can_afford_masters']}
- Zaman planı: {profile['masters_timeline']}

💰 FİNANSAL:
- Şu anki maaş: ${profile['current_salary']}
- Hedef maaş: ${profile['target_salary']}
- Birikim: ${profile['savings']}, Borç: ${profile['debt']}
- Risk toleransı: {profile['risk_tolerance']}
- Aile desteği: {profile['family_support']}

🎯 HEDEFLERİ:
- Emeklilik: {profile['retire_age']} yaş ({years_left} yıl kaldı)
- Hedef birikim: ${profile['target_portfolio']}
- Öncelik: {profile['salary_vs_passion']}

3 SENARYO KARŞILAŞTIR (DETAYLI):

**Senaryo 1: Hemen İşe Başla (Master YOK)**
- Başlangıç maaş: $40K
- Yıllık artış: %10
- Pozisyon ilerlemesi: Data Analyst → Data Scientist → Senior (8-10 yıl)

**Senaryo 2: Türkiye'de Master (2 yıl)**
- Maliyet: $15K
- Başlangıç (sonrası): $50K
- Yıllık artış: %11
- Pozisyon ilerlemesi: Data Scientist → Senior (6-7 yıl)

**Senaryo 3: Yurt Dışı Master (2 yıl)**
- Maliyet: $60K
- Başlangıç (sonrası): $75K (yurt dışı)
- Yıllık artış: %12
- Pozisyon ilerlemesi: Data Scientist → Senior (5-6 yıl)

HER SENARYO İÇİN HESAPLA:

1️⃣ FİNANSAL ANALİZ:
   - {years_left} yıl sonunda TOPLAM KAZANÇ
   - TOPLAM MALİYET (master + fırsat maliyeti)
   - NET KAZANÇ (kazanç - maliyet)
   - NPV (discount rate %5)
   - ROI yüzdesi

2️⃣ KARİYER ETKİSİ:
   - {profile['dream_job']} pozisyonuna kaç yılda ulaşır?
   - Master olmadan bu pozisyona ulaşmak mümkün mü?
   - Hangi yolda daha hızlı ilerler?

3️⃣ FIRE HEDEFİNE KATKISI:
   - Hangi senaryoda ${profile['target_portfolio']} birikimine daha kolay ulaşır?
   - Tasarruf potansiyeli hangi senaryoda daha yüksek?

4️⃣ RİSK ANALİZİ:
   - Her senaryonun riskleri nedir?
   - Bu kişinin risk toleransı ({profile['risk_tolerance']}) göz önüne alındığında hangisi uygun?
   - Maddi durumu ({profile['can_afford_masters']}) hangi senaryoya izin veriyor?

5️⃣ NET TAVSİYE:
   - Bu kişi için BEST seçenek hangisi? (1/2/3)
   - NEDEN? (3-4 madde)
   - KARAR vermekte zorlanıyorsa ne yapmalı?
   - Eğer master yapacaksa, NASIL finanse etmeli?

TABLO + DETAYLI AÇIKLAMA. Max 50 satır."""

    result = call_ai(prompt, system)
    print(result)
    print("\n" + "─" * 70)

def show_fire_plan(profile):
    """Show FIRE plan - ULTRA PERSONALIZED"""
    print_section("FIRE PLANI", "🔥")
    print("⏳ Senin durumuna özel emeklilik stratejisi hazırlanıyor...\n")

    system = "Sen FIRE hareketi uzmanısın. Kararsız insanlara GERÇEKÇI ve UYGULANABILIR emeklilik planları yapıyorsun."

    current_age = int(profile['age'])
    retire_age = int(profile['retire_age'])
    years = retire_age - current_age
    target = profile['target_portfolio']

    prompt = f"""KİŞİYE ÖZEL FIRE PLANI:

👤 KİŞİ:
- {profile['name']}, {current_age} yaş → {retire_age} yaş emeklilik ({years} yıl)
- Neden FIRE: {profile['why_fire']}
- Emeklilik lokasyonu: {profile['retirement_location']}
- Yaşam tarzı: {profile['retirement_lifestyle']}

💰 FİNANSAL DURUM:
- Şu anki maaş: ${profile['current_salary']}
- Hedef maaş: ${profile['target_salary']}
- Birikim: ${profile['savings']}
- Borç: ${profile['debt']}
- Aylık harcama: ${profile['monthly_expenses']}
- Risk toleransı: {profile['risk_tolerance']}
- Aile desteği: {profile['family_support']}
- Bakılacak kişi: {profile['dependents']}

🎯 HEDEFLER:
- Hedef birikim: ${target}
- Aylık pasif gelir: ${profile['passive_income_goal']}
- Work-life balance: {profile['work_life_balance']}/10

🚀 YAN GELİR:
- İlgi: {profile['side_hustle_interest']}
- Haftalık: {profile['weekly_hours']} saat
- Girişimci ruhu: {profile['entrepreneurial']}/10

DETAYLI FIRE PLANI ÇıKAR:

1️⃣ GERÇEKÇİLİK TESTİ:
   - ${target} birikim hedefi {years} yılda GERÇEKÇİ mi?
   - ${profile['passive_income_goal']}/ay ile {profile['retirement_lifestyle']} yaşam tarzı mümkün mü?
   - {profile['retirement_location']}'da bu parayla yaşanır mı?
   - RİSKLER neler? (3-4 madde)

2️⃣ AYLIK BİRİKİM PLANI:
   - Mevcut maaşla aylık ne kadar biriktirmeli?
   - Hedef maaşa ulaşınca ne kadar biriktirmeli?
   - Tasarruf oranı hedefi: %?
   - {years} yıl boyunca ortalama aylık birikim: $?

3️⃣ YATIRIM STRATEJİSİ:
   Risk toleransı: {profile['risk_tolerance']}

   Önerilen portföy:
   - Hisse senedi/ETF: %?
   - Tahvil: %?
   - Emlak: %?
   - Kripto/Alternatif: %?
   - Nakit: %?

   Hangi platformlar/araçlar? (2-3 somut öneri)

4️⃣ YILLIK MİLESTONE'LAR:
   Yıl | Yaş | Birikim Hedefi | Nasıl Ulaşılır
   1   | {current_age + 1} | $? | ?
   3   | {current_age + 3} | $? | ?
   5   | {current_age + 5} | $? | ?
   10  | {current_age + 10} | $? | ?
   {years} | {retire_age} | ${target} | FIRE!

5️⃣ GELİR ARTIRMA:
   - Ana işten gelir projeksiyonu (yıl bazında)
   - Yan gelir hedefi (gerçekçi tahmin)
   - Toplam gelir projeksiyonu
   - Yan gelir olmadan FIRE mümkün mü?

6️⃣ HARCAMA OPTİMİZASYONU:
   - Şu anki aylık harcama: ${profile['monthly_expenses']}
   - Optimize edilmiş harcama: $?
   - En çok kesinti yapılabilecek alanlar (3 madde)
   - Yaşam kalitesinden ödün vermeden tasarruf: nasıl?

7️⃣ ACİL DURUM PLANLARI:
   - Bear market gelirse ne olur?
   - İşini kaybederse ne yapar?
   - Sağlık problemi olursa?
   - Borç varsa önce mi ödenmeli?

8️⃣ NET TAVSİYELER:
   - İLK 30 GÜN: ne yapmalı? (5 somut aksiyon)
   - İLK 1 YIL: neleri otomatikleştirmeli?
   - Bu kişi FIRE yapabilir mi? (evet/hayır/şartlı)
   - En büyük engeller ve çözümleri (3 madde)

9️⃣ BAŞARI OLASILIĞI:
   - Mevcut durumda başarı şansı: %?
   - Tüm önerileri uygularsa: %?
   - NEDEN bu oran? (2-3 satır açıklama)

Max 60 satır. TABLO + DETAYLI AÇIKLAMA."""

    result = call_ai(prompt, system)
    print(result)
    print("\n" + "─" * 70)

def show_side_hustles(profile):
    """Show side hustle ideas - PERSONALIZED"""
    print_section("YAN GELİR ÖNERİLERİ", "🚀")
    print("⏳ Senin beceri ve hedeflerine özel fırsatlar bulunuyor...\n")

    system = "Sen girişimcilik ve yan gelir danışmanısın. Kararsız insanlara SOMUT, UYGULANABILIR ve GERÇEKÇİ yan iş fikirleri veriyorsun."

    prompt = f"""KİŞİYE ÖZEL YAN GELİR ANALİZİ:

👤 KİŞİ:
- {profile['name']}, {profile['age']} yaş
- Ana iş: {profile['current_job']}, Memnuniyet: {profile['job_satisfaction']}/10

🛠️ BECERİLER:
- Programlama: {profile['programming_langs']} (Seviye: {profile['prog_level']})
- ML/AI: {profile['ml_exp']} yıl
- Framework: {profile['frameworks']}
- Cloud: {profile['cloud_exp']}
- GitHub: {profile['github_projects']} proje
- Sertifika: {profile['certifications']}

🎯 YAN GELİR HEDEFLERİ:
- İlgi: {profile['side_hustle_interest']}
- Alanlar: {profile['interests']}
- Haftalık zaman: {profile['weekly_hours']} saat
- Girişimci ruhu: {profile['entrepreneurial']}/10
- Freelance deneyim: {profile['freelance_exp']}
- Startup fikri: {profile['startup_idea']}

💰 FİNANSAL:
- FIRE hedefi: ${profile['target_portfolio']} (emeklilik: {profile['retire_age']} yaş)
- Risk toleransı: {profile['risk_tolerance']}
- Günlük öğrenme: {profile['daily_learning_hours']} saat

🧠 KİŞİLİK:
- Öğrenme: {profile['learning_style']}
- Çalışma: {profile['team_vs_solo']}
- Sosyallik: {profile['introvert_extrovert']}
- Aciliyet: {profile['time_urgency']}

BU KİŞİ İÇİN 5 YAN GELİR STRATEJİSİ ÖNER (KOLAY → ZOR SIRAYLA):

Her strateji için:

1️⃣ Strateji Adı & Özet (1 satır)

2️⃣ Ne Yapacak:
   - Somut iş tanımı
   - Hangi becerileri kullanacak
   - Kimler için/nerede satacak

3️⃣ Finansal Projeksiyon:
   - İlk ay: $?
   - 3. ay: $?
   - 6. ay: $?
   - 1 yıl: $?
   - FIRE hedefine katkısı: yılda $? tasarruf ekstra

4️⃣ Zaman & Çaba:
   - Başlamak için gereken süre: ? gün/hafta
   - Haftalık iş yükü: {profile['weekly_hours']} saat yeterli mi?
   - İlk gelir ne zaman gelir: ? ay
   - Ana işten ayrılma riski var mı?

5️⃣ Başlangıç Maliyeti:
   - Para: $?
   - Öğrenme: ? saat
   - Araç/platform: neler gerekli?

6️⃣ Bu Kişiye Uygunluk:
   - Beceri uyumu: ?/10
   - Kişilik uyumu: ?/10
   - Zaman uyumu: ?/10
   - Risk uyumu: ?/10
   - TOPLAM SKOR: ?/10

7️⃣ İlk 30 Gün Aksiyon Planı:
   Hafta 1: ?
   Hafta 2: ?
   Hafta 3: ?
   Hafta 4: ? (ilk deneme/launch)

8️⃣ Başarı Şansı:
   - Bu kişi için başarı olasılığı: %?
   - Neden bu oran?
   - En büyük engel ne?

9️⃣ Gerçek Örnek:
   - Kim yaptı?
   - Ne kadar kazandı?
   - Link/kaynak (eğer biliniyorsa)

──────────────────────────────────

5 STRATEJİ (Kolay → Zor):
1. Freelance/Konsültasyon (en hızlı)
2. Online Kurs/Eğitim
3. SaaS/Dijital Ürün
4. AI/ML Tooling/Otomasyon
5. Startup (en uzun vade)

Her strateji için yukarıdaki 9 maddeyi DETAYLI doldur.

SON OLARAK:

🎯 NET TAVSİYE:
   - Bu kişi HANGİ stratejiyle başlamalı? (1-5)
   - NEDEN?
   - İlk 7 gün MUTLAKA yapması gerekenler (5 madde)
   - 6 ay sonra yan gelir hedefi: $?
   - FIRE'a etki: emeklilik yaşını kaç yıl öne alabilir?

Max 80 satır. DETAYLI, SOMUT, UYGULANABILIR."""

    result = call_ai(prompt, system)
    print(result)
    print("\n" + "─" * 70)

def main():
    # Header
    print("\n" + "╔" + "═"*68 + "╗")
    print("║" + " "*12 + "🎯 KİŞİSEL FIRE PLANLAMA SİSTEMİ" + " "*24 + "║")
    print("║" + " "*68 + "║")
    print("║" + "  Kararsız mısın? Doğru kararları vermene yardımcı olacağız!  " + " "*4 + "║")
    print("║" + "  Gerçek AI ile DETAYLI, KİŞİSELLEŞTİRİLMİŞ analiz" + " "*16 + "║")
    print("╚" + "═"*68 + "╝")
    print("\n💡 Bu sistem kararsız insanlar için tasarlandı.")
    print("   Sana ÖZEL kariyer yolu, eğitim ROI, FIRE planı ve yan gelir fikirleri.")
    print("   Detaylı sorular soracağız - açık ol, bu senin geleceğin!\n")
    
    # Check API
    if not os.getenv('GROQ_API_KEY'):
        print("\n❌ GROQ_API_KEY bulunamadı!")
        return
    
    # Get profile
    profile = get_user_input()

    print_section("PROFİL ÖZETİ - Detaylı Snapshot", "✅")

    print("👤 KİŞİSEL BİLGİLER")
    print(f"   {profile['name']}, {profile['age']} yaş")
    print(f"   {profile['university']} {profile['major']} ({profile['grad_year']})")
    print(f"   📍 {profile['location']} | Yurt dışı: {profile['relocation_ok']}")

    print("\n💼 MEVCUT DURUM")
    print(f"   İş: {profile['current_job']}")
    print(f"   Maaş: ${profile['current_salary']} | Memnuniyet: {profile['job_satisfaction']}/10")
    print(f"   Sektör: {profile['industry']} | Şirket: {profile['company_size']}")

    print("\n🛠️  BECERİLER")
    print(f"   {profile['programming_langs']} ({profile['prog_level']})")
    print(f"   ML: {profile['ml_exp']} yıl | GitHub: {profile['github_projects']} proje")

    print("\n🎓 EĞİTİM PLANI")
    print(f"   Master: {profile['considering_masters']} ({profile['masters_field']})")
    print(f"   Lokasyon: {profile['masters_location']} | Maddi: {profile['can_afford_masters']}")

    print("\n🎯 KARİYER HEDEFLERİ")
    print(f"   Hedef: {profile['dream_job']} (${profile['target_salary']})")
    print(f"   Alternatif: {profile['alternative_jobs']}")
    print(f"   Öncelik: {profile['salary_vs_passion']} | Hız: {profile['career_speed']}")

    print("\n💰 FİNANSAL DURUM")
    print(f"   Birikim: ${profile['savings']} | Borç: ${profile['debt']}")
    print(f"   Aylık harcama: ${profile['monthly_expenses']}")
    print(f"   Risk: {profile['risk_tolerance']} | Aile desteği: {profile['family_support']}")

    print("\n🔥 FIRE VİZYONU")
    print(f"   Hedef yaş: {profile['retire_age']} | Birikim: ${profile['target_portfolio']}")
    print(f"   Lokasyon: {profile['retirement_location']} | Yaşam: {profile['retirement_lifestyle']}")
    print(f"   Sebep: {profile['why_fire']}")

    print("\n🚀 YAN GELİR")
    print(f"   İlgi: {profile['interests']}")
    print(f"   Haftalık: {profile['weekly_hours']} saat | Girişimci: {profile['entrepreneurial']}/10")

    print("\n🧠 KİŞİLİK")
    print(f"   {profile['introvert_extrovert']} | Öğrenme: {profile['learning_style']}")
    print(f"   Karar verme: {profile['decision_making']} | Korku: {profile['biggest_fear']}")

    print("\n⏰ ZAMAN")
    print(f"   Aciliyet: {profile['time_urgency']} | Günlük öğrenme: {profile['daily_learning_hours']} saat")

    print("\n" + "─" * 70)
    print("🤖 Bu detaylı profile göre 4 AI analizi hazırlanacak...")
    print("   1️⃣ Kariyer Yolu Haritası")
    print("   2️⃣ Eğitim ROI Analizi (Master vs İş)")
    print("   3️⃣ FIRE Emeklilik Planı")
    print("   4️⃣ Yan Gelir Stratejileri")

    input("\n⏎  Hazırsan ENTER'a bas ve analizleri gör...")
    
    # Run analyses
    show_career_analysis(profile)
    input("\n⏎  Sonraki analize geçmek için ENTER...")
    
    show_roi_analysis(profile)
    input("\n⏎  Sonraki analize geçmek için ENTER...")
    
    show_fire_plan(profile)
    input("\n⏎  Sonraki analize geçmek için ENTER...")
    
    show_side_hustles(profile)
    
    # Footer
    print_section("TAMAMLANDI!", "🎉")
    print(f"✅ {profile['name']} için kişisel plan hazır!")
    print("\n💡 İpucu: Tekrar çalıştırmak için: python interactive_fire.py\n")

if __name__ == "__main__":
    main()
