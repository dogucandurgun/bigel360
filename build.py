#!/usr/bin/env python3
# BİGEL — bigel360.com static site generator.
# Run:  python3 build.py   → writes TR pages to ./ and EN pages to ./en/
# All copy lives in this file (CONTENT). Mock company facts are in SITE.
import os, html

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- MOCK DATA (düzeltilecek)
SITE = {
    "domain": "bigel360.com",
    "email": "info@bigelusta.com",
    "phone": "+90 216 000 00 00",
    "phone_href": "+902160000000",
    "address_tr": "Barbaros Mah. Ihlamur Sok. No:12 Kat:4, Ataşehir / İstanbul",
    "address_en": "Barbaros Mah. Ihlamur Sok. No:12 Floor 4, Ataşehir / Istanbul, Türkiye",
    "linkedin": "https://www.linkedin.com/company/bigel360",
    "founded": "2018",
    "regions": "7",
    "provinces": "81",
    "visits": "1.200+",
    "photo_rate": "%98",
    "photo_rate_en": "98%",
}

PAGES = {  # id: (tr file, en file)
    "home": ("index.html", "index.html"),
    "clean": ("clean.html", "clean.html"),
    "care": ("care.html", "care.html"),
    "audit": ("audit.html", "audit.html"),
    "field360": ("field360.html", "field360.html"),
    "sectors": ("sektorler.html", "sectors.html"),
    "tiers": ("abonelikler.html", "subscriptions.html"),
    "how": ("nasil-calisiyoruz.html", "how-we-work.html"),
    "about": ("hakkimizda.html", "about.html"),
    "contact": ("iletisim.html", "contact.html"),
    "pilot": ("pilot.html", "pilot.html"),
    "thanks": ("tesekkurler.html", "thank-you.html"),
}
PRODUCTS = ["clean", "care", "audit", "field360"]
ACCENT = {"clean": "var(--clean)", "care": "var(--care)", "audit": "var(--audit)", "field360": "var(--field)"}

def href(lang, pid, anchor=""):
    f = PAGES[pid][0 if lang == "tr" else 1]
    return f + (("#" + anchor) if anchor else "")

def asset(lang, path):
    return ("assets/" if lang == "tr" else "../assets/") + path

def switch_href(lang, pid):
    return ("en/" + PAGES[pid][1]) if lang == "tr" else ("../" + PAGES[pid][0])

def esc(s): return html.escape(s, quote=False)

# ---------------------------------------------------------------- ICONS (24px stroke)
def icon(name):
    P = {
        "fuel": '<path d="M5 21V5a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v16M3 21h12M15 9h2a2 2 0 0 1 2 2v5a1.5 1.5 0 0 0 3 0V9l-3-3M7 7h6v4H7z"/>',
        "food": '<path d="M4 3v8a3 3 0 0 0 3 3v7M7 3v8M10 3v8M17 3c-2 1-3 4-3 7v11M14 13h3"/>',
        "retail": '<path d="M3 9l1.5-5h15L21 9M3 9a3 3 0 0 0 6 0 3 3 0 0 0 6 0 3 3 0 0 0 6 0M5 12v8h14v-8M10 20v-5h4v5"/>',
        "bank": '<path d="M3 10h18L12 4zM5 10v7M9 10v7M15 10v7M19 10v7M3 20h18"/>',
        "auto": '<path d="M5 16l1.5-6h11L19 16M3 16h18v3H3zM7 19v1M17 19v1M7.5 13h9"/>',
        "logistics": '<path d="M3 7h11v9H3zM14 10h4l3 3v3h-7zM6 19a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3zM17 19a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3z"/>',
        "mall": '<path d="M4 21V9l8-5 8 5v12M4 21h16M9 21v-6h6v6M9 12h2M13 12h2"/>',
        "hotel": '<path d="M3 21V8l9-5 9 5v13M3 21h18M8 12h2M14 12h2M8 16h2M14 16h2"/>',
        "ev": '<path d="M6 21V5a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v16M4 21h12M11 7l-2 5h4l-2 5M16 9h2a2 2 0 0 1 2 2v6"/>',
        "telecom": '<path d="M12 21v-8M5 8a10 10 0 0 1 14 0M8 11a6 6 0 0 1 8 0M12 13a1 1 0 1 0 0-2 1 1 0 0 0 0 2z"/>',
        "edu": '<path d="M2 9l10-5 10 5-10 5zM6 11v5c0 1.5 3 3 6 3s6-1.5 6-3v-5M22 9v6"/>',
        "factory": '<path d="M3 21V10l5 3v-3l5 3v-3l5 3V4h3v17M3 21h18M7 17h2M12 17h2M16 17h2"/>',
        "check": '<path d="M20 6L9 17l-5-5"/>',
        "photo": '<path d="M4 8h3l2-3h6l2 3h3v11H4zM12 17a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7z"/>',
        "chart": '<path d="M4 20V10M10 20V4M16 20v-8M22 20H2"/>',
        "pin": '<path d="M12 21s7-6.2 7-11a7 7 0 1 0-14 0c0 4.8 7 11 7 11zM12 12a2 2 0 1 0 0-4 2 2 0 0 0 0 4z"/>',
        "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6zM9 12l2 2 4-4"/>',
        "hub": '<path d="M12 12m-3 0a3 3 0 1 0 6 0a3 3 0 1 0-6 0M12 3v6M12 15v6M3 12h6M15 12h6"/>',
        "clock": '<path d="M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zM12 7v5l3 2"/>',
        "flag": '<path d="M5 21V4M5 4h12l-2 4 2 4H5"/>',
    }
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{P[name]}</svg>'

SECTOR_ICONS = ["fuel", "ev", "food", "retail", "bank", "auto", "logistics", "mall", "hotel", "telecom", "edu", "factory"]

# ---------------------------------------------------------------- CONTENT
CONTENT = {
"tr": {
  "meta_suffix": " | BİGEL",
  "nav": {"solutions": "Çözümler", "sectors": "Sektörler", "tiers": "Abonelikler", "how": "Nasıl Çalışıyoruz", "pilot": "Pilot", "about": "Hakkımızda", "cta": "Teklif Al", "menu": "Menü"},
  "products": {
    "clean":    {"name": "BİGEL CLEAN", "cat": "Temizlik Operasyonları", "tag": "Standart her noktada aynı.", "short": "Kanopi, tabela, totem, cephe ve otopark için planlı dış alan temizliği. Öncesi ve sonrası fotoğrafla doğrulanır."},
    "care":     {"name": "BİGEL CARE", "cat": "Bakım Operasyonları", "tag": "Arızayı beklemeden, sahayı koruyun.", "short": "Küçük bakım, onarım ve saha müdahalesi. Tespitten fotoğraflı kapanışa tek iş emri akışı."},
    "audit":    {"name": "BİGEL AUDIT", "cat": "Denetim & Kalite", "tag": "Sahadaki standardınızı görün.", "short": "Marka, görsel, temizlik, fiziksel durum ve müşteri deneyimi denetimi. AUDIT 100 ve EV Audit30 ile skorlanır."},
    "field360": {"name": "BİGEL FIELD360", "cat": "Saha Yönetim Platformu", "tag": "Sahanın tamamı tek merkezde.", "short": "Temizlik, bakım, denetim ve aksiyonu tek sözleşme, tek standart ve tek raporlamada birleştirir."},
  },
  "more": "Çözümü Gör",
  "footer": {"tagline": "Sahadaki Gücünüz.", "desc": "Kurumsal Saha Operasyonları ve Hizmet Platformu. Çok lokasyonlu markalar için Türkiye genelinde temizlik, bakım, denetim ve saha operasyon yönetimi.", "solutions": "Çözümler", "company": "Şirket", "contact": "İletişim", "ev": "EV Audit30", "rights": "Tüm hakları saklıdır.", "privacy": "KVKK ve Gizlilik"},
  "cta": {"h2": "Saha operasyonunuzu birlikte tasarlayalım.", "p": "Pilot kapsamını seçili lokasyonlarla başlatır, sonuçlara göre bölgesel ve Türkiye geneli operasyona ölçekleriz.", "b1": "Pilot Başlat", "b2": "İletişim"},
  "sectors_list": [
    ("Akaryakıt İstasyonları", "Kanopi, totem, pompa adası, otopark ve saha çevresi."),
    ("Ev Şarj İstasyonları", "Cihaz çevresi, kablo düzeni, park cebi ve yönlendirme. Audit30 ile skorlanır."),
    ("Restoran & Fast Food", "Cephe, cam, tabela, dış oturma ve arabaya servis alanı."),
    ("Perakende & Mağazacılık", "Vitrin, görsel alan, mobilya, giriş ve mağaza çevresi."),
    ("Bankacılık", "Şube girişi, ATM kabini, cam ve cephe, banko ve seperatörler."),
    ("Otomotiv", "Showroom camı, tabela, araç sergileme alanı ve otopark."),
    ("Lojistik & Depo", "Saha girişi, yükleme alanı, zemin çizgileri ve bariyerler."),
    ("AVM & Plaza", "Ortak dış alanlar, yönlendirme, kolon kaplamaları ve otopark."),
    ("Otel & Turizm", "Giriş, cephe, peyzaj elemanları ve havuz çevresi mobilyası."),
    ("Telekom", "Mağaza, bayi ve saha noktası tabela, vitrin ve giriş alanları."),
    ("Eğitim", "Kampüs dış alanı, bahçe mobilyası, yönlendirme ve korkuluklar."),
    ("Fabrika & Tesis", "Giriş, totem, yol çizgileri, bariyer ve güvenlik binası çevresi."),
  ],
  "tiers_list": [
    ("BİGEL BASIC", "Temel Kontrol", "Periyodik kontrol ve temel saha raporlama.", "Az sayıda lokasyonda düzenli göz olmak isteyen markalar için.",
     ["20–30 maddelik kontrol listesi", "Fotoğraflı lokasyon raporu", "Periyodik ziyaret takvimi", "Bulgu ve öncelik listesi"]),
    ("BİGEL PRO", "Kontrol + Bakım", "Kontrol, bakım ve küçük müdahaleleri kapsar.", "Kontrol sırasında tespit edilen işin yerinde çözülmesini isteyenler için.",
     ["BASIC'in tamamı", "Sıkıştırma, sabitleme, silikon", "Küçük boya ve montaj işleri", "İş emri ve fotoğraflı kapanış"]),
    ("BİGEL BUSINESS", "Operasyonel Yönetim", "Düzenli operasyon yönetimi, raporlama ve öncelikli destek.", "Bölgesel veya ulusal ağını tek muhataptan yönetmek isteyen markalar için.",
     ["PRO'nun tamamı", "Planlı CLEAN temizlik programı", "AUDIT 100 periyodik denetim", "Yönetim dashboardu ve KPI/SLA raporu", "Öncelikli destek hattı"]),
    ("BİGEL 360", "Tam Entegre Çözüm", "CLEAN, CARE, AUDIT ve saha yönetiminin uçtan uca çözümü.", "Tüm fiziksel alan yönetimini FIELD360 ile tek sözleşmeye almak isteyenler için.",
     ["BUSINESS'ın tamamı", "FIELD360 tek operasyon merkezi", "Görsel alan ve mobilya yönetimi", "Acil saha müdahalesi 7/24", "Atanmış operasyon yöneticisi"]),
  ],
  "home": {
    "title": "BİGEL | Sahadaki Gücünüz",
    "desc": "Çok lokasyonlu markalar için Türkiye genelinde temizlik, bakım, denetim ve saha operasyon yönetimi. Fotoğraflı kanıt, skor ve aksiyon takibi.",
    "eyebrow": "Kurumsal Saha Operasyonları",
    "h1": "Sahadaki Gücünüz.",
    "lead": "Çok lokasyonlu markaların temizlik, bakım ve denetim operasyonlarını Türkiye genelinde tek standartla planlıyor, uyguluyor ve fotoğraflı kanıtla raporluyoruz.",
    "b1": "Çözümleri İncele", "b2": "Teklif Al",
    "sub": [("81", "ile erişim"), ("4", "ürün, tek standart"), ("100", "kriterli dijital denetim")],
    "card": {"loc": "Örnek Lokasyon · Kadıköy / İstanbul", "meta": "Denetim 12.09.2026 · Ekip MAR-04", "status": "Aksiyon gerekli",
             "bars": [("Temizlik", 94, "var(--green)"), ("Marka standardı", 89, "var(--amber)"), ("Müşteri deneyimi", 91, "var(--green)"), ("Teknik durum", 72, "var(--red)"), ("İş güvenliği", 100, "var(--green)")],
             "foot_l": "3 açık bulgu · <b>1 kritik</b>", "foot_r": "İş emri oluşturuldu"},
    "trust_eyebrow": "Neden BİGEL", "trust_h2": "Yerel saha gücü. Merkezi operasyon. Ölçülebilir sonuç.",
    "stats": [(SITE["provinces"], "ilde erişilebilir yerel ekip ağı"), (SITE["regions"], "bölgesel operasyon ekibi"), (SITE["visits"], "aylık planlı saha ziyareti"), (SITE["photo_rate"], "zorunlu fotoğraf doğrulama oranı")],
    "sol_eyebrow": "Çözümler", "sol_h2": "Dört ürün. Tek BİGEL standardı.", "sol_lead": "Her ürün bağımsız kullanılabilir ya da aynı ziyaret planında birleşir. Hepsi aynı kontrol listesi, fotoğraf açısı ve kapanış kuralıyla çalışır.",
    "proof_eyebrow": "Kanıt", "proof_h2": "Sadece yapmıyoruz. Ölçüyoruz.",
    "proof_p": "Her ziyaret fotoğraf, kontrol listesi ve skor üretir. Bulgular iş emrine dönüşür, kapanışı sorumlu ve hedef tarihle takip edilir.",
    "proof_list": ["Öncesi ve sonrası fotoğraf, GPS ve zaman damgası", "Soru bazlı skor ve kırmızı-sarı-yeşil durum özeti", "Sorumlu, hedef tarih ve kapanış kanıtıyla aksiyon takibi", "Lokasyon, bölge ve dönem karşılaştırmaları"],
    "ba": [("01.02.2026", "Tabela — Hasarlı", "Öncelik: Yüksek · İş emri açıldı", "red", "Açık"), ("01.03.2026", "Tabela — Yenilendi", "Sonrası fotoğrafı eklendi · Yetkili teyidi alındı", "green", "Kapandı")],
    "flow_eyebrow": "Nasıl çalışıyoruz", "flow_h2": "Planlamadan kapanışa tek kayıt zinciri.",
    "flow": [("Planlama", "Lokasyon, görev, ekip ve SLA tanımı."), ("Uygulama", "Temizlik veya bakım, standart prosedürle."), ("Denetim", "Kontrol listesi, skor ve fotoğraf."), ("Raporlama", "KPI, SLA ve lokasyon skoru."), ("Aksiyon", "İş emri, sorumlu ve kapanış kanıtı.")],
    "flow_more": "Süreci detaylı görün",
    "sec_eyebrow": "Sektörler", "sec_h2": "Çok lokasyonlu her marka için.", "sec_more": "Tüm sektörler",
    "tier_eyebrow": "Abonelikler", "tier_h2": "İhtiyacınıza göre ölçeklenen paketler.", "tier_more": "Paketleri karşılaştır",
    "photo_tag": "Gerçek saha, gerçek ekip, fotoğraflı kanıt",
  },
  "product_pages": {
    "clean": {
      "title": "BİGEL CLEAN — Çok lokasyonlu dış alan temizliği",
      "desc": "Kanopi, tabela, totem, cephe ve otopark temizliğini Türkiye genelinde tek standartla yönetiyoruz. Öncesi ve sonrası fotoğrafla doğrulanır.",
      "lead": "Yaygın fiziksel noktalara sahip markaların dış alan temizlik operasyonlarını Türkiye genelinde tek standartla yönetiyoruz. Her lokasyon için tanımlı kapsam, her ziyaret için fotoğraflı kanıt.",
      "sections": [
        {"type": "split", "eyebrow": "Sorun", "h2": "Lokasyon sayısı artınca standart dağılır.", "p": "Farklı ekipler, değişen uygulama yöntemleri ve dağınık raporlama marka görünümünde sapmalara yol açar. BİGEL CLEAN bu yapıyı tek model altında toplar.",
         "list": ["Ortak hizmet tanımı ve uygulama standardı", "Merkezi görev ve ziyaret planlaması", "Bölgesel ekiplerle hızlı saha erişimi", "Öncesi ve sonrası fotoğraflı hizmet kanıtı", "Lokasyon ve bölge bazında performans görünürlüğü"], "img": "station.jpg", "tag": "Kanopi ve saha temizliği · Akaryakıt"},
        {"type": "modules", "eyebrow": "Hizmet modülleri", "h2": "Her alan için tanımlı yöntem, ekipman ve fotoğraf açısı.", "lead": "Modüller tek seferlik ya da periyodik programa dahil edilebilir.",
         "items": [("01", "Kanopi Clean", "Atmosferik kir, toz, egzoz izi, kurum ve biyolojik kirlerin periyodik temizliği."), ("02", "Tabela ve Totem Clean", "Marka görünürlüğünü etkileyen tabela, totem ve yönlendirme elemanlarının yüzeye uygun temizliği."), ("03", "Zemin ve Otopark Clean", "Beton, asfalt, parke, epoksi ve taş yüzeylerde kir, yağ lekesi ve çevre temizliği."), ("04", "Cam ve Cephe Clean", "Vitrin, giriş camı, cam cephe, kompozit, metal, taş ve boyalı yüzeyler."), ("05", "Event Clean", "Etkinlik öncesi hazırlık, etkinlik sırasında destek ve sonrası kapanış temizliği."), ("06", "Night Clean", "İşletmenin çalışma düzenini etkilemeden kapanış sonrası planlanan temizlik."), ("07", "Emergency Clean", "Ani kirlenme, dökülme, kötü hava, vandalizm veya denetim öncesi acil müdahale."), ("08", "Seasonal Clean", "Kış kiri, yosun, yaprak, çamur ve kaygan yüzey risklerine göre mevsimsel program.")]},
        {"type": "flow", "eyebrow": "Yıllık program", "h2": "Her ziyaret aynı dijital akışla yürütülür.", "steps": [("Görev kapsamı", "Lokasyon bilgisi ve tanımlı hizmet."), ("Öncesi fotoğraf", "Standart açılardan başlangıç kaydı."), ("Uygulama", "Yöntem, ekipman ve kimyasal standardı."), ("Sonrası fotoğraf", "Kontrol listesi ve kalite kriteri."), ("Tamamlanma", "Bulgu bildirimi ve kapanış kaydı.")]},
        {"type": "kpi", "eyebrow": "Ölçülebilir hizmet seviyesi", "h2": "Performans, birlikte belirlenen KPI ve SLA ile izlenir.", "items": ["Zamanında ziyaret ve tamamlanma oranı", "İlk uygulamada kalite başarısı", "Zorunlu fotoğraf doğrulama oranı", "Kontrol listesi tamamlama oranı", "Şikâyet ve tekrar müdahale oranı", "Aksiyon kapanış süresi"]},
        {"type": "cards3", "eyebrow": "Hizmet modelleri", "h2": "Tek uygulamadan yıllık sözleşmeye.", "items": [("Lokasyon bazlı hizmet", "Belirli bir lokasyon ve ziyaret kapsamı için planlanan tek uygulama."), ("Periyodik paket", "Aylık, iki aylık, üç aylık veya mevsimsel ziyaret programı. Modüller ihtiyaca göre birleştirilir."), ("Yıllık çok lokasyonlu sözleşme", "Tüm lokasyonlar için yıllık takvim, hizmet kapsamı, SLA hedefleri ve merkezi raporlama.")],
         "note": "Fiyatlandırma; lokasyon sayısı, alan ve yüzey türü, ziyaret sıklığı, ekipman ihtiyacı ve erişim koşullarına göre hazırlanır. Pilot uygulama nihai birim fiyatı netleştirir."},
        {"type": "split", "eyebrow": "Franchise ağları", "h2": "Merkez adına, tüm ağda ortak standart.", "p": "Franchise yapılarında her şubenin farklı temizlik uygulaması marka görünümünde tutarsızlık yaratır. BİGEL CLEAN, merkez marka ile tek sözleşme ve tek hizmet tanımıyla çalışır.",
         "list": ["Tüm lokasyonlar için ortak kontrol listesi", "Standart fotoğraf açıları ve kalite kriterleri", "Lokasyon bazında skor ve uygunsuzluk takibi", "Merkez yönetim için karşılaştırmalı dashboard"], "img": "exterior.jpg", "tag": "Cephe ve giriş alanı · Perakende", "reverse": True},
      ]},
    "care": {
      "title": "BİGEL CARE — Fiziksel alan bakımı ve saha müdahalesi",
      "desc": "Küçük bakım, onarım ve saha müdahale ihtiyaçlarını Türkiye genelinde tek merkezden yönetiyoruz. Tespit, iş emri, uygulama ve fotoğraflı kapanış.",
      "lead": "Markaların fiziksel noktalarındaki küçük bakım, onarım ve saha müdahale ihtiyaçlarını tek merkezden yönetiyoruz. Tespit, planlama, saha uygulaması, fotoğraflama ve kapanış takibi BİGEL'de.",
      "sections": [
        {"type": "split", "eyebrow": "Kapsam", "h2": "Küçük işler birikmeden çözülür.", "p": "Lokasyonlarda biriken küçük fiziksel problemler müşteri deneyimini ve marka görünümünü etkiler. BİGEL CARE bu işleri tek iş emri sistemiyle yönetir.",
         "list": ["Periyodik ve önleyici bakım", "Arıza ve fiziksel hasar müdahalesi", "Görsel alan ve marka unsurları bakımı", "Dış alan ve çevre bakımı", "Mobilya, ekipman ve küçük montaj işleri", "Acil saha müdahalesi"], "img": "retail.jpg", "tag": "Mobilya ve teşhir kontrolü · Mağaza",
         "note": "Yüksek uzmanlık ve yasal yetki gerektiren işler (elektrik, mekanik tesisat vb.) uygun uzmanlarla koordine edilir; BİGEL tespit, planlama ve kapanış takibini yönetir."},
        {"type": "modules", "eyebrow": "Hizmet modülleri", "h2": "On modül, sektöre göre birleştirilir.", "lead": "",
         "items": [("01", "Minor Works", "Vida sıkıştırma, sabitleme, kapı kolu ve aksesuar değişimi, silikon, noktasal boya."), ("02", "Sign Care", "Tabela, totem ve yönlendirme elemanlarının bakımı."), ("03", "Exterior Care", "Cephe, giriş ve dış alan bakımı."), ("04", "Visual Care", "Görsel alan ve marka unsurları."), ("05", "Furniture Care", "Mobilya ve teşhir elemanları."), ("06", "Pavement Care", "Zemin, bordür ve otopark bakımı."), ("07", "Site Care", "Lokasyon fiziksel durum yönetimi."), ("08", "Preventive Care", "Periyodik önleyici bakım."), ("09", "Emergency Care", "Acil saha müdahalesi."), ("10", "Field Audit", "Fotoğraflı kontrol ve aksiyon raporu.")]},
        {"type": "flow", "eyebrow": "İş akışı", "h2": "Talepten fotoğraflı kapanışa.", "steps": [("Talep", "Tek kanal: talep veya denetim bulgusu."), ("Fotoğraflı tespit", "Hasar türü, öncelik ve önerilen aksiyon."), ("Görev onayı", "Kapsam, sorumlu ve hedef tarih."), ("Saha müdahalesi", "Bölgesel ekiple standart uygulama."), ("Kapanış raporu", "Sonrası fotoğrafı ve kalite kontrolü.")]},
        {"type": "cards3", "eyebrow": "Sektör paketleri", "h2": "Her sektörün fiziksel alanına göre.", "items": [("Station Care", "Akaryakıt istasyonları: kanopi, tabela, pompa adası, bordür, bariyer ve istasyon çevresi."), ("EV Charge Care", "Şarj ünitesi dış gövdesi, zemin, yönlendirme ve aydınlatma dış gövdesi. Elektriksel bakım yetkili uzmanlarla."), ("Restaurant Care", "Dış cephe, tabela, dış oturma, arabaya servis alanı ve iç mekân küçük işler."), ("Auto & ATM Care", "Showroom cephe, sergileme platformu; ATM kabini, şube girişi ve banko."), ("Retail & AVM Care", "Raf, teşhir ünitesi, vitrin çerçevesi; AVM yönlendirme, oturma grupları ve sezonluk dekorasyon."), ("Logistics & Facility Care", "Depo cephe, zemin çizgileri, bariyer; otel, eğitim kurumu ve fabrika girişleri.")]},
      ]},
    "audit": {
      "title": "BİGEL AUDIT — Saha denetimi, AUDIT 100 ve EV Audit30",
      "desc": "Marka standardını, görsel uygulamaları, temizlik ve fiziksel durumu sahada ölçülebilir hale getiriyoruz. AUDIT 100 ve EV Audit30 ile fotoğraflı skor.",
      "lead": "Markaların fiziksel noktalarındaki marka standardını, görsel uygulamaları, temizlik durumunu, fiziksel ihtiyaçları ve müşteri deneyimini sahada ölçülebilir hale getiriyoruz. Bağımsız kullanılır ya da CLEAN ve CARE ile bütünleşir.",
      "sections": [
        {"type": "flow", "eyebrow": "Nasıl çalışır", "h2": "Denetimi gözlemle sınırlamayız; karar ve aksiyona dönüştürürüz.", "steps": [("Saha", "Eğitimli ekip, standart kontrol listesiyle inceler."), ("Veri", "Puan, fotoğraf, GPS, tarih ve bulgu kaydedilir."), ("Merkez", "Lokasyonlar tek dashboard'da karşılaştırılır."), ("Karar", "Bulgular öncelik ve sorumluluğa göre sınıflanır."), ("İş emri", "Aksiyon oluşturulur, uygulanır, fotoğrafla kapanır.")]},
        {"type": "modules", "eyebrow": "Denetim kategorileri", "h2": "Sektöre uyarlanan ortak denetim çatısı.", "lead": "Her madde Uygun, Uygun Değil veya Uygulanamaz olarak işaretlenir; fotoğraf, konum, tarih ve açıklamayla kanıtlanır.",
         "items": [("01", "Brand Audit", "Logo, kurumsal renk, güncel tabela, kampanya materyali ve fiyat iletişimi. BRAND SCORE."), ("02", "Visual Audit", "Tabela, totem, ışıklı harf, folyo, poster, vitrin, stand ve dijital ekran."), ("03", "Clean Audit", "Zemin, cam, cephe, otopark, çöp alanı ve ortak alanlar; renk kodlu özet."), ("04", "Physical Audit", "Duvar, kapı, mobilya, bariyer, korkuluk ve küçük hasarlar; bakım iş emrine dönüşür."), ("05", "Customer Experience Audit", "Fark edilirlik, giriş, yönlendirme, kasa ve bekleme alanı. CX SCORE.")]},
        {"type": "sub", "id": "audit100", "logo": "audit100.png", "eyebrow": "Dijital denetim ürünü", "h2": "AUDIT 100 — 100 kriter. Tek skor.",
         "p": "10 kategori, 100 kontrol noktası. Her madde Uygun 100, Kısmen Uygun 50, Uygun Değil 0 puan alır; kategori ağırlıklarıyla 100 üzerinden lokasyon skoru oluşur. Fotoğraf kuralı soru bazında tanımlıdır: şartlı, zorunlu veya öncesi-sonrası.",
         "weights": [("Dış Alan & Cephe", 10), ("Tabela / Totem / Görsel", 10), ("Temizlik & Hijyen", 10), ("Mobilya / Ekipman", 10), ("Teknik & Fiziksel Durum", 10), ("İş Güvenliği & Risk", 15), ("Marka / Görsel Standart", 15), ("Müşteri Deneyimi", 10), ("Operasyon & Uygulama", 5), ("Yönetim / Veri / Uygunluk", 5)],
         "thresholds": [("g", "90–100 · Standarda uygun"), ("a", "75–89 · İyileştirme gerekli"), ("r", "0–74 · Öncelikli aksiyon")],
         "badges": ["Zorunlu fotoğraf ve GPS", "Kritik bulguda anlık bildirim", "Lokasyon skor kartı", "JSON / PDF rapor"]},
        {"type": "sub", "id": "ev", "logo": None, "eyebrow": "Şarj ağları için", "h2": "Şarj noktası saha kalite denetimi.",
         "p": "Uzaktan izleme cihazın teknik durumunu gösterir; Audit30 müşterinin karşılaştığı fiziksel saha koşullarını görünür kılar. 30 standart kontrol, 6 ağırlıklı alan, 100 üzerinden saha skoru. Güvenlik maddelerindeki uygunsuzluk aynı gün bildirim üretir; majör bulgular 24 saat içinde aksiyona bağlanır.",
         "weights": [("Güvenlik · 5 kritik kontrol", 25), ("Cihaz bütünlüğü", 20), ("İşlev işaretleri", 20), ("Kullanıcı deneyimi", 15), ("Temizlik ve çevre", 10), ("Marka standardı", 10)],
         "thresholds": [("g", "≥ 90 · Uygun"), ("a", "75–89 · Takip"), ("r", "< 75 · Aksiyon")],
         "badges": ["Ön, sağ, sol, ekran, kablo, park alanı fotoğraf seti", "Kritik: anlık · Majör: 24 saat", "Pilot: 10 lokasyon, 2 hafta, 2 tur"]},
        {"type": "map", "eyebrow": "BİGEL Map", "h2": "Tüm lokasyonlar tek haritada.", "p": "Lokasyonlar Türkiye haritası üzerinde skor rengiyle gösterilir. Kullanıcı bölgeden şehre, şehirden lokasyona iner; skor kartını, fotoğrafları, bulguları ve aksiyon geçmişini görür.",
         "legend": [("var(--green)", "90–100 · Standarda uygun"), ("var(--amber)", "75–89 · İyileştirme gerekli"), ("var(--red)", "0–74 · Öncelikli aksiyon")],
         "kpis": [("Bölge ve şehir bazında lokasyon sayısı"), ("Ortalama denetim skoru ve kritik bulgu sayısı"), ("Tamamlanan, bekleyen ve açık aksiyonlar")]},
        {"type": "cards3", "eyebrow": "Hizmet modelleri", "h2": "Tek denetimden sürekli platforma.", "items": [("Lokasyon bazlı audit", "Belirli lokasyonlarda tek seferlik denetim."), ("Periyodik audit", "Aylık, üç aylık, altı aylık veya yıllık tekrar eden program."), ("Proje audit", "Kampanya, açılış, tabela değişimi sonrası toplu kontrol."), ("Franchise audit", "Franchise ağında standart uyumunun merkez adına ölçülmesi."), ("Yatırım ve devir", "Satın alma, kiralama veya devir öncesi fiziksel durum belgeleme."), ("Platform ve dashboard", "Skor, fotoğraf, bulgu, iş emri ve kapanışların sürekli izlenmesi.")],
         "note": "Teklif; lokasyon sayısı, soru adedi, fotoğraf gereksinimi, seyahat, denetim sıklığı, rapor formatı ve dashboard kapsamına göre hazırlanır."},
      ]},
    "field360": {
      "title": "BİGEL FIELD360 — Uçtan uca saha operasyon yönetimi",
      "desc": "Temizlik, bakım, denetim ve saha aksiyonlarını tek sözleşme, tek operasyon standardı ve tek raporlama akışında yönetiyoruz.",
      "lead": "Temizlik, bakım, denetim ve saha aksiyonlarını tek sözleşme, tek operasyon standardı ve tek raporlama akışında birleştiriyoruz. Dağınık tedarikçi yapısı yerine tek muhatap.",
      "sections": [
        {"type": "cards3", "eyebrow": "FIELD360 nedir", "h2": "Tek merkez. Tek standart. Tek görünüm.", "items": [("01 · Tek merkez", "Planlama, saha koordinasyonu ve müşteri iletişimi ortak yönetim altında yürür."), ("02 · Tek saha standardı", "Kontrol listeleri, fotoğraf açıları, kalite kriterleri ve kapanış kuralları tüm lokasyonlarda aynıdır."), ("03 · Tek yönetim görünümü", "Ziyaretler, skorlar, açık bulgular, iş emirleri ve kapanış kanıtları tek ekranda izlenir.")]},
        {"type": "table", "eyebrow": "Dört hizmet tek modelde", "h2": "Hizmetler bağımsız başlar ya da aynı ziyaret planında birleşir.",
         "head": ["Hizmet", "Sahadaki rol", "Temel çıktı", "FIELD360 içindeki yeri"],
         "rows": [["CLEAN", "Temizlik ve görünüm standardı", "Öncesi/sonrası fotoğraf, kalite kontrolü", "Planlı veya ihtiyaç bazlı uygulama"], ["CARE", "Küçük bakım ve fiziksel müdahale", "Tespit, iş emri, uygulama, kapanış", "Bulgunun sahada çözülmesi"], ["AUDIT", "Marka, fiziksel alan ve CX denetimi", "Skor, kanıt, öncelikli bulgu listesi", "Karar ve aksiyon kaynağı"], ["EV Audit30", "Şarj noktası fiziksel kalite denetimi", "Audit30 skoru, kritik bildirim", "EV ağına özel kontrol standardı"]]},
        {"type": "table", "eyebrow": "Müşteri ihtiyacı", "h2": "Dağınık saha operasyonu, ortak düzene dönüşür.",
         "head": ["Yaşanan durum", "FIELD360 yaklaşımı", "Görülen sonuç"],
         "rows": [["Bölgeden bölgeye değişen hizmet kalitesi", "Ortak SOP, kontrol listesi ve fotoğraf standardı", "Lokasyonlar arası karşılaştırılabilir kalite"], ["Çok sayıda tedarikçi ve iletişim kanalı", "Tek sözleşme, tek operasyon merkezi, bölgesel ekip ağı", "Sade koordinasyon, tek muhatap"], ["Sahada ne yapıldığının görülememesi", "Konum, tarih, ekip ve fotoğrafla doğrulanan ziyaret", "Şeffaf, denetlenebilir hizmet"], ["Bulguların açık kalması", "Sorumlu, hedef tarih, öncelik ve kapanış kanıtı", "İş emri bazında takip"], ["Dağınık yönetim raporları", "Lokasyon, bölge, hizmet ve dönem bazlı görünüm", "KPI, SLA ve skorlar tek raporda"]]},
        {"type": "flow", "eyebrow": "Uçtan uca iş akışı", "h2": "Her görev aynı kayıt zincirinde ilerler.", "steps": [("Planlama", "Lokasyon, kapsam, ekip, tarih ve SLA."), ("Görev atama", "Saha ekibi, rota, ekipman ve talimat."), ("Saha uygulaması", "CLEAN, CARE, AUDIT veya EV kapsamı."), ("Doğrulama", "Konum, zaman, kontrol listesi, fotoğraf."), ("Aksiyon ve kapanış", "İş emri, sonrası fotoğrafı, müşteri raporu.")]},
        {"type": "cards3", "eyebrow": "Yönetim çıktıları", "h2": "Merkez ekip ne görür?", "items": [("Ağ görünümü", "Türkiye, bölge, şehir ve lokasyon durumu. Kaynak ve ziyaret önceliği."), ("Hizmet performansı", "Planlanan, tamamlanan ve geciken ziyaretler. Kapasite ve SLA takibi."), ("Kalite skoru", "Kontrol listesi sonucu ve lokasyon skoru. Düşük performanslı noktalar."), ("Bulgu ve iş emri", "Açık kritikler, sorumlular ve hedef tarihler. Müdahale ve bütçe önceliği."), ("Kanıt geçmişi", "Öncesi, sonrası ve kapanış fotoğrafları. Yapılan işin doğrulanması."), ("Örnek pilot", "20–30 lokasyon, 4–6 hafta, CLEAN + CARE + AUDIT. Başlangıç skoru, açık bulgu, SLA ve ikinci ziyaret.")]},
      ]},
  },
  "sectors": {"title": "Sektörler — Çok lokasyonlu markalar için saha operasyonu", "desc": "Akaryakıt, restoran, perakende, bankacılık, otomotiv, lojistik, AVM, otel, EV şarj, telekom, eğitim ve tesisler için saha hizmetleri.",
              "eyebrow": "Sektörler", "h1": "Sahadaki standardın merkezden yönetilmesi gereken her sektör.", "lead": "Hizmet kapsamı, her sektörün yüzeyleri ve operasyon saatlerine göre uyarlanır. Aşağıda her sektör için öne çıkan alanları görebilirsiniz.",
              "fr_eyebrow": "Franchise ağları", "fr_h2": "Merkez adına tek sözleşme, tüm şubelerde ortak standart.", "fr_p": "Franchise sahiplerinin uygulamaları görünür, ölçülebilir ve merkezden yönetilebilir hale gelir.",
              "fr_list": ["Merkez ile tek sözleşme ve tek hizmet tanımı", "Tüm lokasyonlar için ortak kontrol listesi", "Bölgesel ekiplerle planlı saha ziyaretleri", "Lokasyon bazında skor ve uygunsuzluk takibi", "Merkez yönetim için karşılaştırmalı dashboard"],
              "fit_eyebrow": "İhtiyaca göre çözüm", "fit_h2": "Hangi durumda hangi ürün?",
              "fit": [("Çok lokasyonlu temizlik", "Periyodik CLEAN programı", "clean"), ("Küçük bakım ve onarım birikiyor", "CARE müdahale planı", "care"), ("Marka standardını ölçmek", "AUDIT ve AUDIT 100", "audit"), ("Şarj ağı saha kalitesi", "EV Audit30", "audit"), ("Dağınık tedarikçi yapısı", "FIELD360 ile tek merkez", "field360"), ("Fotoğraf ve kanıt ihtiyacı", "Dijital ziyaret raporu", "field360")]},
  "tiers": {"title": "Abonelik Paketleri — BASIC, PRO, BUSINESS, 360", "desc": "BİGEL abonelik paketleri: temel kontrolden tam entegre saha yönetimine. Fiyatlandırma lokasyon sayısı ve kapsama göre.",
            "eyebrow": "Abonelikler", "h1": "İhtiyacınıza göre ölçeklenen dört paket.", "lead": "Alt paket adı ikinci hiyerarşidedir; ana BİGEL standardı, fotoğraflı kanıt ve raporlama her pakette aynıdır. Fiyatlandırma lokasyon sayısı, bölgesel dağılım, hizmet sıklığı ve kapsama göre hazırlanır.",
            "badge": "En kapsamlı", "cta": "Teklif Al", "cmp_h2": "Paket karşılaştırması",
            "cmp_head": ["Kapsam", "BASIC", "PRO", "BUSINESS", "360"],
            "cmp_rows": [["Periyodik kontrol ziyareti", 1,1,1,1], ["Fotoğraflı lokasyon raporu", 1,1,1,1], ["Bulgu ve öncelik listesi", 1,1,1,1], ["Küçük bakım müdahalesi (CARE)", 0,1,1,1], ["İş emri ve fotoğraflı kapanış", 0,1,1,1], ["Planlı temizlik programı (CLEAN)", 0,0,1,1], ["AUDIT 100 periyodik denetim", 0,0,1,1], ["Yönetim dashboardu, KPI / SLA", 0,0,1,1], ["Öncelikli destek hattı", 0,0,1,1], ["FIELD360 tek operasyon merkezi", 0,0,0,1], ["Acil saha müdahalesi 7/24", 0,0,0,1], ["Atanmış operasyon yöneticisi", 0,0,0,1]],
            "note": "Tüm paketler pilot uygulamayla başlatılabilir. Pilot sonuçlarına göre hizmet sıklığı ve kapsam netleştirilir."},
  "how": {"title": "Nasıl Çalışıyoruz — Devreye alma, pilot ve yaygınlaştırma", "desc": "İhtiyaç analizinden düzenli raporlamaya BİGEL hizmet devreye alma modeli, kalite güvence ve dijital raporlama.",
          "eyebrow": "Nasıl çalışıyoruz", "h1": "Merkezde planlanan işin sahada doğru gerçekleşmesini sağlarız.", "lead": "İhtiyaç analiziyle başlar, seçili lokasyonlarda pilotla doğrular, bölgesel ve Türkiye geneli operasyona ölçekleriz.",
          "steps_eyebrow": "Hizmet devreye alma", "steps_h2": "Altı adımda düzenli operasyon.",
          "steps": [("İhtiyaç ve lokasyon analizi", "Saha ağı, hizmet ihtiyacı ve öncelikler."), ("Hizmet kapsamı ve SLA", "Kontrol listeleri, kanıt kuralı ve hedef süreler."), ("Pilot uygulama", "Seçilen lokasyonlarda gerçek saha testi."), ("Sonuç ve aksiyon planı", "Skor, iş yükü, ekip ve ziyaret sıklığı."), ("Yaygınlaştırma", "Bölgesel devreye alma ve düzenli takvim."), ("Düzenli raporlama", "Görev, rapor, aksiyon ve performans toplantıları.")],
          "tl_eyebrow": "Uygulama takvimi", "tl_h2": "Sekiz haftada pilottan yaygınlaştırmaya.",
          "timeline": [("1–2. Hafta", "Hazırlık", ["Lokasyon listesi ve hizmet kapsamı", "Kontrol listeleri ve fotoğraf standardı", "Ekip planı ve iletişim akışı", "SLA hedefleri"]), ("3–4. Hafta", "Pilot uygulama", ["Saha ziyaretleri ve fotoğraflı kayıt", "Lokasyon skorları", "Bulgu sınıflandırma ve aksiyon önerileri", "Pilot sonuç toplantısı"]), ("5–8. Hafta", "Yaygınlaştırma", ["Ekip kapasite planı", "Bölgesel devreye alma", "Düzenli hizmet takvimi", "Dashboard, KPI ve SLA takibi"])],
          "q_eyebrow": "Kalite güvence modeli", "q_h2": "Her uygulama doğrulanır.",
          "quality": ["Görev öncesi ekip ve kapsam kontrolü", "Standart operasyon prosedürüne uygun uygulama", "Zorunlu fotoğraf ve kontrol listesi doğrulaması", "Merkezi kalite kontrolü ve uygunsuzluk kaydı", "Düzeltici aksiyon, sorumlu kişi ve termin takibi", "Düzenli KPI ve SLA değerlendirmesi"],
          "r_eyebrow": "Dijital raporlama", "r_h2": "Yönetim ekipleri ne görür?",
          "report": ["Ziyaret tarihi, lokasyon ve ekip bilgisi", "Soru bazlı skorlar ve fotoğraflı kanıtlar", "Kırmızı, sarı ve yeşil durum özeti", "Öncelikli bulgular ve sorumlu aksiyonlar", "Lokasyon, bölge ve dönem karşılaştırmaları", "Yönetim özeti ve kapanış takibi"],
          "s_eyebrow": "Ölçeklenebilir yayılım", "s_h2": "Pilottan Türkiye geneline.",
          "scale": [("1 · Pilot", "Seçili lokasyonlarda standardı doğrulama: kapsam, başlangıç ölçümü, saha uygulaması, sonuç raporu."), ("2 · Bölgesel yayılım", "Modeli öncelikli bölgelere taşıma: ekip planlama, eğitim, SLA takibi, bölgesel performans."), ("3 · Türkiye geneli", "Tüm ağı tek modelle yönetme: merkezi koordinasyon, lokasyon skorları, iş emri, yönetim dashboardu.")]},
  "about": {"title": "Hakkımızda — BİGEL", "desc": "BİGEL, kurumsal markaların saha operasyonlarını yürüten, denetleyen ve raporlayan yeni nesil bir saha hizmetleri platformudur.",
            "eyebrow": "Hakkımızda", "h1": "Usta gönderen firma değil, saha operasyonunuzu emanet edebileceğiniz partner.",
            "lead": "BİGEL, kurumsal markaların saha operasyonlarını yürüten, denetleyen ve raporlayan yeni nesil bir saha hizmetleri platformudur. Yerel saha gücünü merkezi operasyon, denetim ve raporlamayla birleştirir.",
            "story_h2": "Sahadan doğdu, sistemle büyüdü.",
            "story": ["BİGEL'in yolculuğu 2018'de İstanbul'da, akaryakıt istasyonu ağlarına yönelik dış alan temizlik ve küçük bakım işleriyle başladı. Lokasyon sayısı arttıkça sorun da netleşti: işi yapmak yetmiyordu, her noktada aynı standardı tutmak ve bunu merkeze kanıtlamak gerekiyordu.", "Bugün BİGEL, bölgesel ekip ağını merkezi planlama, standart kontrol listeleri ve fotoğraflı dijital raporlamayla yönetiyor. CLEAN, CARE, AUDIT ve FIELD360 aynı çatı altında, aynı kayıt zinciriyle çalışıyor.", "Bigel Usta olarak tanınan hizmet geçmişimiz, saha bilgimizin kaynağı olmaya devam ediyor; markamız ise artık kurumsal saha operasyonları ve teknoloji eksenine odaklanıyor."],
            "facts": [(SITE["founded"], "kuruluş, İstanbul"), (SITE["regions"], "bölgesel operasyon ekibi"), (SITE["provinces"], "ile erişilebilir saha ağı"), ("4", "ürün, tek kayıt zinciri")],
            "v_eyebrow": "Marka tanımı", "v_h2": "Ne için varız?",
            "values": [("Purpose", "Markaların sahadaki işlerini daha düzenli, ölçülebilir ve güvenilir hale getirmek.", "flag"), ("Promise", "İşi sahada gerçekleştirmek, kontrol etmek ve görünür kılmak.", "shield"), ("Differentiator", "Yerel saha gücü + merkezi operasyon + denetim + raporlama.", "hub")],
            "c_eyebrow": "Karakter", "c_h2": "BİGEL nasıl konuşur, nasıl çalışır?",
            "character": [("Güvenilir", "Standart, kanıt ve rapor. Abartılı vaat yok."), ("Çevik", "Bölgesel ekiplerle daha kısa müdahale süresi."), ("Sistemli", "Planlama + uygulama + kontrol + raporlama."), ("Çözüm odaklı", "Bulgu iş emrine, iş emri kapanışa dönüşür."), ("Teknolojik", "Dijital kontrol listesi, skor ve dashboard."), ("Ölçülebilir", "100 kriter, fotoğraflı kanıt, tek skor.")],
            "reg_eyebrow": "Saha ağı", "reg_h2": "Yedi bölge, tek operasyon merkezi.",
            "regions": ["Marmara", "Ege", "Akdeniz", "İç Anadolu", "Karadeniz", "Doğu Anadolu", "Güneydoğu Anadolu"],
            "reg_p": "Merkezi planlama ve kalite kontrolü İstanbul'dan yürütülür; uygulama bölgesel ekiplerle yapılır. Ekipler ortak hizmet standardına göre eğitilir, kıyafet, kimlik, İSG ve dijital kayıt standardına göre değerlendirilir."},
  "contact": {"title": "İletişim — Teklif, pilot ve demo talebi", "desc": "Saha operasyonunuzu birlikte tasarlayalım. Teklif, pilot veya demo görüşmesi için talep bırakın.",
              "eyebrow": "İletişim", "h1": "Saha operasyonunuzu birlikte tasarlayalım.", "lead": "Teklif, pilot veya demo görüşmesi için formu doldurun. Aynı iş günü içinde dönüş yapıyoruz.",
              "f": {"name": "Ad Soyad", "company": "Şirket", "email": "E-posta", "phone": "Telefon", "count": "Lokasyon sayısı", "counts": ["1–10", "11–50", "51–250", "251–1.000", "1.000+"], "solution": "İlgilendiğiniz çözüm", "solutions": ["BİGEL CLEAN", "BİGEL CARE", "BİGEL AUDIT / AUDIT 100", "EV Audit30", "BİGEL FIELD360", "Abonelik paketleri", "Birden fazla"], "msg": "İhtiyacınız", "msg_ph": "Lokasyon yapınız, hizmet ihtiyacınız ve öncelikleriniz…", "consent": "Kişisel verilerimin talebimle ilgili iletişim amacıyla işlenmesini kabul ediyorum.", "send": "Talep Oluştur", "subject": "bigel360.com — Yeni talep"},
              "info": [("Merkez", SITE["address_tr"]), ("Telefon", SITE["phone"]), ("E-posta", SITE["email"]), ("LinkedIn", "linkedin.com/company/bigel360"), ("Çalışma saatleri", "Hafta içi 08:30–18:00 · Acil saha hattı 7/24")]},
  "pilot": {"title": "Pilot Uygulama — Küçük başlayın, ölçün, ölçekleyin", "desc": "20–30 lokasyonda 4–6 haftalık pilot: başlangıç ölçümü, fotoğraflı bulgular, lokasyon skorları ve yaygınlaştırma planı. Pilot başvurusu.",
            "eyebrow": "Pilot uygulama", "h1": "Küçük başlayın. Ölçün. Sonra ölçekleyin.",
            "lead": "Seçili lokasyonlarda kısa bir pilotla başlıyoruz. Pilot bitince elinizde başlangıç skorları, fotoğraflı bulgular ve gerçek saha verisine dayanan bir yaygınlaştırma planı oluyor.",
            "stats": [("20–30", "lokasyon ile temsil gücü yüksek örneklem"), ("4–6", "hafta uygulama dönemi"), ("2", "ziyaret turu: başlangıç ve doğrulama"), ("1", "rapor: skor, bulgu, iş yükü ve takvim")],
            "why_eyebrow": "Neden pilot", "why_h2": "Sözleşmeden önce sahada kanıt.",
            "why": [("Riski sınırlar", "Tüm ağ yerine seçili lokasyonlarla başlarsınız. Kapsam, sıklık ve bütçe gerçek veriyle netleşir."), ("Gerçek veri üretir", "Her lokasyon için başlangıç skoru, fotoğraflı bulgu listesi ve öncelikli aksiyonlar. Varsayım değil, ölçüm."), ("Yaygınlaştırmayı planlar", "Pilot sonuç toplantısında bölge, ziyaret sıklığı, ekip ve bütçe planı birlikte kararlaştırılır.")],
            "steps_eyebrow": "Pilot süreci", "steps_h2": "Altı adımda pilot.",
            "steps": [("Kapsam ve kriterler", "Lokasyon seti, kategori kapsamı, soru seti ve skor ağırlıkları onaylanır."), ("Başlangıç ölçümü", "Mevcut durum fotoğraf ve kontrol listeleriyle kayıt altına alınır."), ("Saha uygulaması", "CLEAN, CARE, AUDIT veya EV kapsamı bölgesel ekiplerle uygulanır."), ("Sonuç raporu", "Lokasyon skorları, kritik bulgular ve aksiyon önerileri raporlanır."), ("İkinci tur", "Aksiyonlar kapatılır, ikinci ziyarette skor ve açık bulgu gelişimi doğrulanır."), ("Yaygınlaştırma planı", "Marka standartları, SLA hedefleri, bölge ve takvim ile ölçekleme planı hazırlanır.")],
            "out_eyebrow": "Pilot çıktıları", "out_h2": "Pilot bitince elinizde ne olur?",
            "outputs": ["Denetim özeti ve kategori skorları", "Fotoğraflı bulgu listesi: kritik, yüksek, orta, düşük", "Lokasyon ve bölge karşılaştırması", "Öncesi ve sonrası fotoğraflarla kapanış kanıtı", "Tahmini iş yükü, ziyaret sıklığı ve uygulama takvimi", "Doğrulanmış birim süre ve teklif için netleşmiş kapsam"],
            "photo_tag": "Pilot ziyareti · fotoğraflı başlangıç kaydı",
            "prod_eyebrow": "Ürüne göre pilot", "prod_h2": "Hangi üründen başlayalım?",
            "prod": [("clean", "CLEAN pilotu", "Seçili lokasyonlarda bir dış alan temizlik turu. Öncesi ve sonrası fotoğraf, kontrol listesi ve kalite skoru."), ("care", "CARE pilotu", "Fotoğraflı fiziksel durum tespiti, yerinde küçük müdahaleler ve iş emri gerektiren bulguların listesi."), ("audit", "AUDIT 100 pilotu", "100 kriterli denetim, lokasyon skor kartı, kritik bulgular ve aksiyon öncelikleri. EV ağları için Audit30: 10 lokasyon, 2 hafta, 2 tur."), ("field360", "FIELD360 pilotu", "Temizlik, bakım ve denetimin aynı ziyaret planında birleştiği bütünleşik pilot; tek rapor, tek muhatap.")],
            "form_eyebrow": "Pilot başvurusu", "form_h2": "Pilot kapsamını birlikte belirleyelim.",
            "form_lead": "Formu doldurun; aynı iş günü içinde 90 dakikalık bir kapsam toplantısı için sizinle iletişime geçelim.",
            "f": {"name": "Ad Soyad", "company": "Şirket", "email": "E-posta", "phone": "Telefon",
                  "sector": "Sektör", "sectors": ["Akaryakıt", "Ev şarj istasyonları", "Restoran / Fast food", "Perakende", "Bankacılık", "Otomotiv", "Lojistik / Depo", "AVM / Plaza", "Otel / Turizm", "Telekom", "Eğitim", "Fabrika / Tesis", "Diğer"],
                  "count": "Toplam lokasyon sayısı", "counts": ["1–10", "11–50", "51–250", "251–1.000", "1.000+"],
                  "geo": "Şehir / bölge dağılımı", "geo_ph": "Örn. İstanbul 12, Ankara 6, İzmir 4…",
                  "product": "Başlangıç ürünü", "products": ["AUDIT 100", "EV Audit30", "CLEAN", "CARE", "FIELD360", "Henüz karar vermedim"],
                  "start": "Hedef başlangıç", "starts": ["2 hafta içinde", "1 ay içinde", "1–3 ay içinde", "Planlama aşamasındayız"],
                  "msg": "Notlar", "msg_ph": "Öncelikli lokasyonlar, mevcut tedarikçi yapısı, beklentiler…",
                  "consent": "Kişisel verilerimin talebimle ilgili iletişim amacıyla işlenmesini kabul ediyorum.", "send": "Pilot Başvurusu Gönder", "subject": "bigel360.com — Pilot başvurusu"},
            "after_h3": "Başvurudan sonra", "after": [("1", "Kapsam toplantısı", "90 dakika. Lokasyon yapısı, hizmet modülleri ve pilot başarı kriterleri."), ("2", "Pilot planı", "Lokasyon seti, soru seti, fotoğraf kuralı, SLA ve takvim tek dokümanda."), ("3", "Saha", "Ziyaretler başlar; kritik bulgular aynı gün bildirilir."), ("4", "Sonuç toplantısı", "Skorlar, bulgular ve yaygınlaştırma teklifi.")],
            "note": "Pilot kapsamı ve ücreti lokasyon sayısı, hizmet modülü ve coğrafi dağılıma göre teklif olarak sunulur. Pilot sonuçları nihai birim fiyatı netleştirir."},
  "thanks": {"title": "Teşekkürler", "h1": "Talebiniz alındı.", "p": "Ekibimiz aynı iş günü içinde sizinle iletişime geçecek. Bu arada çözümlerimizi inceleyebilirsiniz.", "b": "Ana sayfaya dön"},
},
"en": {
  "meta_suffix": " | BİGEL",
  "nav": {"solutions": "Solutions", "sectors": "Industries", "tiers": "Plans", "how": "How We Work", "pilot": "Pilot", "about": "About", "cta": "Get a Quote", "menu": "Menu"},
  "products": {
    "clean":    {"name": "BİGEL CLEAN", "cat": "Cleaning Operations", "tag": "The same standard at every site.", "short": "Planned exterior cleaning for canopies, signage, totems, façades and car parks. Verified with before and after photos."},
    "care":     {"name": "BİGEL CARE", "cat": "Maintenance Operations", "tag": "Protect the site before it breaks.", "short": "Minor maintenance, repairs and on-site response. One work-order flow from detection to photo-verified closure."},
    "audit":    {"name": "BİGEL AUDIT", "cat": "Audit & Quality", "tag": "See your standard in the field.", "short": "Brand, visual, cleanliness, physical condition and customer experience audits. Scored with AUDIT 100 and EV Audit30."},
    "field360": {"name": "BİGEL FIELD360", "cat": "Field Management Platform", "tag": "Your entire field, one control centre.", "short": "Cleaning, maintenance, audit and action under one contract, one standard and one reporting flow."},
  },
  "more": "View solution",
  "footer": {"tagline": "Your Strength in the Field.", "desc": "Corporate Field Operations and Service Platform. Cleaning, maintenance, audit and field operations management across Türkiye for multi-site brands.", "solutions": "Solutions", "company": "Company", "contact": "Contact", "ev": "EV Audit30", "rights": "All rights reserved.", "privacy": "Privacy & Data Protection"},
  "cta": {"h2": "Let's design your field operation together.", "p": "We start with a pilot on selected sites and scale to regional or nationwide operations based on the results.", "b1": "Start a Pilot", "b2": "Contact"},
  "sectors_list": [
    ("Fuel Stations", "Canopy, totem, pump islands, car park and site surroundings."),
    ("EV Charging Stations", "Charger surroundings, cable management, bays and wayfinding. Scored with Audit30."),
    ("Restaurants & QSR", "Façade, glass, signage, outdoor seating and drive-thru."),
    ("Retail", "Shopfront, visual areas, furniture, entrance and store surroundings."),
    ("Banking", "Branch entrance, ATM cabin, glass and façade, counters and partitions."),
    ("Automotive", "Showroom glass, signage, display areas and car park."),
    ("Logistics & Warehousing", "Site entrance, loading areas, floor markings and barriers."),
    ("Shopping Malls & Plazas", "Common outdoor areas, wayfinding, column cladding and car park."),
    ("Hotels & Tourism", "Entrance, façade, landscape elements and poolside furniture."),
    ("Telecom", "Store, dealer and field-point signage, shopfront and entrances."),
    ("Education", "Campus exteriors, garden furniture, wayfinding and railings."),
    ("Factories & Facilities", "Entrance, totem, road markings, barriers and gatehouse surroundings."),
  ],
  "tiers_list": [
    ("BİGEL BASIC", "Essential Control", "Periodic inspection and essential site reporting.", "For brands that want regular eyes on a small number of sites.",
     ["20–30 item checklist", "Photo-verified site report", "Periodic visit calendar", "Findings and priority list"]),
    ("BİGEL PRO", "Control + Maintenance", "Inspection, maintenance and minor interventions.", "For those who want issues found during inspection fixed on the spot.",
     ["Everything in BASIC", "Tightening, fixing, sealant", "Minor paint and assembly work", "Work orders and photo-verified closure"]),
    ("BİGEL BUSINESS", "Operational Management", "Regular operations management, reporting and priority support.", "For brands running a regional or national network through a single partner.",
     ["Everything in PRO", "Planned CLEAN cleaning programme", "Periodic AUDIT 100 audits", "Management dashboard, KPI / SLA reports", "Priority support line"]),
    ("BİGEL 360", "Fully Integrated", "End-to-end CLEAN, CARE, AUDIT and field management.", "For those who want all physical-site management under one FIELD360 contract.",
     ["Everything in BUSINESS", "FIELD360 single operations centre", "Visual area and furniture management", "24/7 emergency field response", "Dedicated operations manager"]),
  ],
  "home": {
    "title": "BİGEL | Your Strength in the Field",
    "desc": "Cleaning, maintenance, audit and field operations management across Türkiye for multi-site brands. Photo evidence, scores and action tracking.",
    "eyebrow": "Corporate Field Operations",
    "h1": "Your Strength in the Field.",
    "lead": "We plan, execute and report the cleaning, maintenance and audit operations of multi-site brands across Türkiye, to one standard and with photo evidence.",
    "b1": "Explore Solutions", "b2": "Get a Quote",
    "sub": [("81", "provinces covered"), ("4", "products, one standard"), ("100", "criteria digital audit")],
    "card": {"loc": "Sample Site · Kadıköy / Istanbul", "meta": "Audit 12 Sep 2026 · Team MAR-04", "status": "Action required",
             "bars": [("Cleanliness", 94, "var(--green)"), ("Brand standard", 89, "var(--amber)"), ("Customer experience", 91, "var(--green)"), ("Technical condition", 72, "var(--red)"), ("Safety", 100, "var(--green)")],
             "foot_l": "3 open findings · <b>1 critical</b>", "foot_r": "Work order created"},
    "trust_eyebrow": "Why BİGEL", "trust_h2": "Local field power. Central operations. Measurable results.",
    "stats": [(SITE["provinces"], "provinces with local team access"), (SITE["regions"], "regional operations teams"), (SITE["visits"], "planned site visits per month"), (SITE["photo_rate_en"], "mandatory photo verification rate")],
    "sol_eyebrow": "Solutions", "sol_h2": "Four products. One BİGEL standard.", "sol_lead": "Each product works on its own or combines in the same visit plan. All run on the same checklists, photo angles and closure rules.",
    "proof_eyebrow": "Proof", "proof_h2": "We don't just do the work. We measure it.",
    "proof_p": "Every visit produces photos, a checklist and a score. Findings become work orders, and closure is tracked with an owner and a due date.",
    "proof_list": ["Before and after photos with GPS and timestamp", "Question-level scores and red-amber-green status", "Action tracking with owner, due date and closure evidence", "Site, region and period comparisons"],
    "ba": [("01 Feb 2026", "Signage — Damaged", "Priority: High · Work order opened", "red", "Open"), ("01 Mar 2026", "Signage — Replaced", "After photo added · Confirmed by site manager", "green", "Closed")],
    "flow_eyebrow": "How we work", "flow_h2": "One chain of record from planning to closure.",
    "flow": [("Plan", "Site, task, team and SLA definition."), ("Execute", "Cleaning or maintenance to a standard procedure."), ("Audit", "Checklist, score and photos."), ("Report", "KPI, SLA and site score."), ("Act", "Work order, owner and closure evidence.")],
    "flow_more": "See the full process",
    "sec_eyebrow": "Industries", "sec_h2": "For every multi-site brand.", "sec_more": "All industries",
    "tier_eyebrow": "Plans", "tier_h2": "Plans that scale with your needs.", "tier_more": "Compare plans",
    "photo_tag": "Real sites, real teams, photo evidence",
  },
  "product_pages": {
    "clean": {
      "title": "BİGEL CLEAN — Multi-site exterior cleaning",
      "desc": "Canopy, signage, totem, façade and car park cleaning across Türkiye to one standard. Verified with before and after photos.",
      "lead": "We manage the exterior cleaning operations of brands with widespread physical sites across Türkiye, to one standard. A defined scope for every site, photo evidence for every visit.",
      "sections": [
        {"type": "split", "eyebrow": "The problem", "h2": "As sites multiply, the standard drifts.", "p": "Different crews, changing methods and scattered reporting cause deviations in brand appearance. BİGEL CLEAN brings it all under one model.",
         "list": ["Common service definition and application standard", "Central task and visit planning", "Fast site access through regional teams", "Before and after photo evidence", "Site and regional performance visibility"], "img": "station.jpg", "tag": "Canopy and forecourt cleaning · Fuel"},
        {"type": "modules", "eyebrow": "Service modules", "h2": "A defined method, equipment and photo angle for every area.", "lead": "Modules can be one-off or part of a periodic programme.",
         "items": [("01", "Canopy Clean", "Periodic removal of atmospheric dirt, dust, exhaust marks, soot and biological soiling."), ("02", "Signage & Totem Clean", "Surface-appropriate cleaning of signs, totems and wayfinding that affect brand visibility."), ("03", "Floor & Car Park Clean", "Dirt, oil stains and litter on concrete, asphalt, pavers, epoxy and stone."), ("04", "Glass & Façade Clean", "Shopfronts, entrance glass, curtain walls, composite, metal, stone and painted surfaces."), ("05", "Event Clean", "Pre-event preparation, support during the event and post-event closing clean."), ("06", "Night Clean", "Cleaning scheduled after closing hours without disrupting operations."), ("07", "Emergency Clean", "Sudden soiling, spills, bad weather, vandalism or pre-audit rapid response."), ("08", "Seasonal Clean", "Programmes built around winter grime, moss, leaves, mud and slip risks.")]},
        {"type": "flow", "eyebrow": "Annual programme", "h2": "Every visit runs on the same digital flow.", "steps": [("Task scope", "Site information and defined service."), ("Before photo", "Baseline record from standard angles."), ("Execution", "Method, equipment and chemical standard."), ("After photo", "Checklist and quality criteria."), ("Completion", "Findings reported, closure recorded.")]},
        {"type": "kpi", "eyebrow": "Measurable service level", "h2": "Performance is tracked with jointly defined KPIs and SLAs.", "items": ["On-time visit and completion rate", "First-time quality success", "Mandatory photo verification rate", "Checklist completion rate", "Complaint and re-visit rate", "Action closure time"]},
        {"type": "cards3", "eyebrow": "Service models", "h2": "From a single job to an annual contract.", "items": [("Site-based service", "A single planned application for a specific site and visit scope."), ("Periodic package", "Monthly, bi-monthly, quarterly or seasonal visit programme. Modules combined as needed."), ("Annual multi-site contract", "Annual calendar for all sites, service scope, SLA targets and central reporting.")],
         "note": "Pricing is based on number of sites, area and surface type, visit frequency, equipment needs and access conditions. A pilot confirms the final unit price."},
        {"type": "split", "eyebrow": "Franchise networks", "h2": "One standard across the network, on behalf of head office.", "p": "In franchise structures, every branch cleaning differently creates inconsistency in brand appearance. BİGEL CLEAN works with head office under one contract and one service definition.",
         "list": ["A common checklist for all sites", "Standard photo angles and quality criteria", "Site-level scores and non-conformity tracking", "Comparative dashboard for head office"], "img": "exterior.jpg", "tag": "Façade and entrance · Retail", "reverse": True},
      ]},
    "care": {
      "title": "BİGEL CARE — Physical site maintenance and field response",
      "desc": "Minor maintenance, repairs and field response managed from one centre across Türkiye. Detection, work order, execution and photo-verified closure.",
      "lead": "We manage the minor maintenance, repair and field response needs of brand sites from one centre. Detection, planning, on-site execution, photography and closure tracking are all handled by BİGEL.",
      "sections": [
        {"type": "split", "eyebrow": "Scope", "h2": "Small jobs get fixed before they pile up.", "p": "Small physical problems accumulating at sites hurt customer experience and brand appearance. BİGEL CARE manages them through a single work-order system.",
         "list": ["Periodic and preventive maintenance", "Fault and physical damage response", "Visual area and brand element care", "Exterior and surroundings care", "Furniture, equipment and minor assembly", "Emergency field response"], "img": "retail.jpg", "tag": "Furniture and display check · Retail",
         "note": "Work requiring specialist skills or legal certification (electrical, mechanical installations, etc.) is coordinated with qualified specialists; BİGEL manages detection, planning and closure tracking."},
        {"type": "modules", "eyebrow": "Service modules", "h2": "Ten modules, combined by industry.", "lead": "",
         "items": [("01", "Minor Works", "Tightening, fixing, handle and accessory replacement, sealant, spot painting."), ("02", "Sign Care", "Signage, totem and wayfinding maintenance."), ("03", "Exterior Care", "Façade, entrance and outdoor area maintenance."), ("04", "Visual Care", "Visual areas and brand elements."), ("05", "Furniture Care", "Furniture and display elements."), ("06", "Pavement Care", "Floors, kerbs and car park maintenance."), ("07", "Site Care", "Site physical condition management."), ("08", "Preventive Care", "Periodic preventive maintenance."), ("09", "Emergency Care", "Emergency field response."), ("10", "Field Audit", "Photo-verified inspection and action report.")]},
        {"type": "flow", "eyebrow": "Workflow", "h2": "From request to photo-verified closure.", "steps": [("Request", "One channel: request or audit finding."), ("Photo assessment", "Damage type, priority and proposed action."), ("Task approval", "Scope, owner and due date."), ("Field intervention", "Standard execution by the regional team."), ("Closure report", "After photo and quality check.")]},
        {"type": "cards3", "eyebrow": "Industry packages", "h2": "Built around each industry's physical spaces.", "items": [("Station Care", "Fuel stations: canopy, signage, pump islands, kerbs, barriers and surroundings."), ("EV Charge Care", "Charger housing, floor, wayfinding and light fittings. Electrical maintenance by certified specialists."), ("Restaurant Care", "Façade, signage, outdoor seating, drive-thru and minor interior works."), ("Auto & ATM Care", "Showroom façade and display platforms; ATM cabins, branch entrances and counters."), ("Retail & Mall Care", "Shelving, display units, shopfront frames; mall wayfinding, seating and seasonal décor."), ("Logistics & Facility Care", "Warehouse façade, floor markings, barriers; hotel, school and factory entrances.")]},
      ]},
    "audit": {
      "title": "BİGEL AUDIT — Field audits, AUDIT 100 and EV Audit30",
      "desc": "We make brand standard, visual execution, cleanliness and physical condition measurable in the field. Photo-verified scores with AUDIT 100 and EV Audit30.",
      "lead": "We make brand standard, visual execution, cleanliness, physical needs and customer experience measurable at every site. Use it standalone or integrated with CLEAN and CARE.",
      "sections": [
        {"type": "flow", "eyebrow": "How it works", "h2": "We don't stop at observation; we turn it into decisions and action.", "steps": [("Field", "Trained team inspects with a standard checklist."), ("Data", "Score, photo, GPS, date and findings recorded."), ("Centre", "Sites compared on a single dashboard."), ("Decision", "Findings classified by priority and owner."), ("Work order", "Action created, executed, closed with photo.")]},
        {"type": "modules", "eyebrow": "Audit categories", "h2": "A common audit framework adapted to each industry.", "lead": "Each item is marked Compliant, Non-compliant or Not applicable, and evidenced with photo, location, date and notes.",
         "items": [("01", "Brand Audit", "Logo, corporate colours, current signage, campaign material and price communication. BRAND SCORE."), ("02", "Visual Audit", "Signage, totems, illuminated letters, vinyl, posters, shopfronts, stands and digital screens."), ("03", "Clean Audit", "Floors, glass, façade, car park, waste areas and common areas; colour-coded summary."), ("04", "Physical Audit", "Walls, doors, furniture, barriers, railings and minor damage; converts to maintenance work orders."), ("05", "Customer Experience Audit", "Visibility, entrance, wayfinding, checkout and waiting areas. CX SCORE.")]},
        {"type": "sub", "id": "audit100", "logo": "audit100.png", "eyebrow": "Digital audit product", "h2": "AUDIT 100 — 100 criteria. One score.",
         "p": "10 categories, 100 checkpoints. Each item scores Compliant 100, Partial 50 or Non-compliant 0; category weights produce a site score out of 100. The photo rule is defined per question: conditional, mandatory or before-and-after.",
         "weights": [("Exterior & Façade", 10), ("Signage / Totem / Visual", 10), ("Cleanliness & Hygiene", 10), ("Furniture / Equipment", 10), ("Technical & Physical Condition", 10), ("Safety & Risk", 15), ("Brand / Visual Standard", 15), ("Customer Experience", 10), ("Operations & Execution", 5), ("Management / Data / Compliance", 5)],
         "thresholds": [("g", "90–100 · Meets standard"), ("a", "75–89 · Improvement needed"), ("r", "0–74 · Priority action")],
         "badges": ["Mandatory photo and GPS", "Instant alert on critical findings", "Site scorecard", "JSON / PDF report"]},
        {"type": "sub", "id": "ev", "logo": None, "eyebrow": "For charging networks", "h2": "Charging point field quality audit.",
         "p": "Remote monitoring shows the device's technical state; Audit30 makes the physical site conditions your customers actually meet visible. 30 standard checks, 6 weighted areas, a site score out of 100. Safety non-conformities trigger a same-day alert; major findings are actioned within 24 hours.",
         "weights": [("Safety · 5 critical checks", 25), ("Device integrity", 20), ("Function indicators", 20), ("User experience", 15), ("Cleanliness & surroundings", 10), ("Brand standard", 10)],
         "thresholds": [("g", "≥ 90 · Compliant"), ("a", "75–89 · Follow-up"), ("r", "< 75 · Action")],
         "badges": ["Photo set: front, right, left, screen, cable, bay", "Critical: instant · Major: 24 hours", "Pilot: 10 sites, 2 weeks, 2 rounds"]},
        {"type": "map", "eyebrow": "BİGEL Map", "h2": "All sites on one map.", "p": "Sites are shown on a map of Türkiye in their score colour. Users drill from region to city to site and see the scorecard, photos, findings and action history.",
         "legend": [("var(--green)", "90–100 · Meets standard"), ("var(--amber)", "75–89 · Improvement needed"), ("var(--red)", "0–74 · Priority action")],
         "kpis": [("Site count by region and city"), ("Average audit score and critical finding count"), ("Completed, pending and open actions")]},
        {"type": "cards3", "eyebrow": "Service models", "h2": "From a single audit to a continuous platform.", "items": [("Site-based audit", "One-off audit at selected sites."), ("Periodic audit", "Monthly, quarterly, semi-annual or annual recurring programme."), ("Project audit", "Bulk check after campaigns, openings or signage changes."), ("Franchise audit", "Measuring standard compliance across a franchise network on behalf of head office."), ("Investment & handover", "Documenting physical condition before purchase, lease or handover."), ("Platform & dashboard", "Continuous tracking of scores, photos, findings, work orders and closures.")],
         "note": "Quotes are based on number of sites, question count, photo requirements, travel, audit frequency, report format and dashboard scope."},
      ]},
    "field360": {
      "title": "BİGEL FIELD360 — End-to-end field operations management",
      "desc": "Cleaning, maintenance, audit and field actions managed under one contract, one operating standard and one reporting flow.",
      "lead": "We bring cleaning, maintenance, audit and field actions together under one contract, one operating standard and one reporting flow. One partner instead of a scattered supplier base.",
      "sections": [
        {"type": "cards3", "eyebrow": "What is FIELD360", "h2": "One centre. One standard. One view.", "items": [("01 · One centre", "Planning, field coordination and client communication run under shared management."), ("02 · One field standard", "Checklists, photo angles, quality criteria and closure rules are identical at every site."), ("03 · One management view", "Visits, scores, open findings, work orders and closure evidence tracked on one screen.")]},
        {"type": "table", "eyebrow": "Four services, one model", "h2": "Services start independently or combine in the same visit plan.",
         "head": ["Service", "Role in the field", "Core output", "Place in FIELD360"],
         "rows": [["CLEAN", "Cleanliness and appearance standard", "Before/after photos, quality control", "Planned or on-demand execution"], ["CARE", "Minor maintenance and physical response", "Detection, work order, execution, closure", "Resolving findings on site"], ["AUDIT", "Brand, physical and CX audit", "Score, evidence, prioritised findings", "Source of decisions and actions"], ["EV Audit30", "Charging point physical quality audit", "Audit30 score, critical alerts", "EV-specific control standard"]]},
        {"type": "table", "eyebrow": "Client need", "h2": "Scattered field operations become one orderly system.",
         "head": ["Current situation", "FIELD360 approach", "Visible result"],
         "rows": [["Service quality varies by region", "Common SOP, checklist and photo standard", "Comparable quality across sites"], ["Many suppliers and communication channels", "One contract, one operations centre, regional team network", "Simpler coordination, one partner"], ["No visibility of what was done on site", "Visits verified by location, date, team and photo", "Transparent, auditable service"], ["Findings left open", "Owner, due date, priority and closure evidence", "Tracking per work order"], ["Scattered management reports", "Site, region, service and period views", "KPI, SLA and scores in one report"]]},
        {"type": "flow", "eyebrow": "End-to-end workflow", "h2": "Every task moves along the same chain of record.", "steps": [("Planning", "Site, scope, team, date and SLA."), ("Task assignment", "Field team, route, equipment and brief."), ("Field execution", "CLEAN, CARE, AUDIT or EV scope."), ("Verification", "Location, time, checklist, photos."), ("Action & closure", "Work order, after photo, client report.")]},
        {"type": "cards3", "eyebrow": "Management outputs", "h2": "What does head office see?", "items": [("Network view", "Türkiye, region, city and site status. Resource and visit priority."), ("Service performance", "Planned, completed and delayed visits. Capacity and SLA tracking."), ("Quality score", "Checklist results and site score. Low-performing sites identified."), ("Findings & work orders", "Open criticals, owners and due dates. Intervention and budget priority."), ("Evidence history", "Before, after and closure photos. Verification of work done."), ("Sample pilot", "20–30 sites, 4–6 weeks, CLEAN + CARE + AUDIT. Baseline score, open findings, SLA and second visit.")]},
      ]},
  },
  "sectors": {"title": "Industries — Field operations for multi-site brands", "desc": "Field services for fuel, restaurants, retail, banking, automotive, logistics, malls, hotels, EV charging, telecom, education and facilities.",
              "eyebrow": "Industries", "h1": "Every industry where the field standard must be managed centrally.", "lead": "Service scope adapts to each industry's surfaces and operating hours. Below are the priority areas for each industry.",
              "fr_eyebrow": "Franchise networks", "fr_h2": "One contract with head office, one standard across every branch.", "fr_p": "Franchisee execution becomes visible, measurable and centrally manageable.",
              "fr_list": ["One contract and one service definition with head office", "A common checklist for all sites", "Planned site visits by regional teams", "Site-level scores and non-conformity tracking", "Comparative dashboard for head office"],
              "fit_eyebrow": "Solution by need", "fit_h2": "Which product for which situation?",
              "fit": [("Multi-site cleaning", "Periodic CLEAN programme", "clean"), ("Minor maintenance piling up", "CARE response plan", "care"), ("Measuring brand standard", "AUDIT and AUDIT 100", "audit"), ("Charging network site quality", "EV Audit30", "audit"), ("Scattered supplier base", "One centre with FIELD360", "field360"), ("Need for photo evidence", "Digital visit report", "field360")]},
  "tiers": {"title": "Plans — BASIC, PRO, BUSINESS, 360", "desc": "BİGEL subscription plans: from essential control to fully integrated field management. Pricing based on site count and scope.",
            "eyebrow": "Plans", "h1": "Four plans that scale with your needs.", "lead": "The plan name is the second tier; the BİGEL standard, photo evidence and reporting are the same in every plan. Pricing is based on site count, regional spread, service frequency and scope.",
            "badge": "Most complete", "cta": "Get a Quote", "cmp_h2": "Plan comparison",
            "cmp_head": ["Scope", "BASIC", "PRO", "BUSINESS", "360"],
            "cmp_rows": [["Periodic inspection visit", 1,1,1,1], ["Photo-verified site report", 1,1,1,1], ["Findings and priority list", 1,1,1,1], ["Minor maintenance response (CARE)", 0,1,1,1], ["Work orders and photo-verified closure", 0,1,1,1], ["Planned cleaning programme (CLEAN)", 0,0,1,1], ["Periodic AUDIT 100 audits", 0,0,1,1], ["Management dashboard, KPI / SLA", 0,0,1,1], ["Priority support line", 0,0,1,1], ["FIELD360 single operations centre", 0,0,0,1], ["24/7 emergency field response", 0,0,0,1], ["Dedicated operations manager", 0,0,0,1]],
            "note": "Every plan can start with a pilot. Service frequency and scope are finalised based on pilot results."},
  "how": {"title": "How We Work — Onboarding, pilot and roll-out", "desc": "BİGEL's service onboarding model from needs analysis to regular reporting, quality assurance and digital reporting.",
          "eyebrow": "How we work", "h1": "We make sure the work planned at the centre happens correctly in the field.", "lead": "We start with a needs analysis, validate with a pilot on selected sites, and scale to regional and nationwide operations.",
          "steps_eyebrow": "Service onboarding", "steps_h2": "Regular operations in six steps.",
          "steps": [("Needs and site analysis", "Site network, service needs and priorities."), ("Service scope and SLA", "Checklists, evidence rules and target times."), ("Pilot", "A real field test at selected sites."), ("Results and action plan", "Score, workload, team and visit frequency."), ("Roll-out", "Regional go-live and a regular calendar."), ("Regular reporting", "Task, report, action and performance reviews.")],
          "tl_eyebrow": "Implementation timeline", "tl_h2": "From pilot to roll-out in eight weeks.",
          "timeline": [("Weeks 1–2", "Preparation", ["Site list and service scope", "Checklists and photo standard", "Team plan and communication flow", "SLA targets"]), ("Weeks 3–4", "Pilot", ["Site visits and photo records", "Site scores", "Finding classification and action proposals", "Pilot review meeting"]), ("Weeks 5–8", "Roll-out", ["Team capacity plan", "Regional go-live", "Regular service calendar", "Dashboard, KPI and SLA tracking"])],
          "q_eyebrow": "Quality assurance model", "q_h2": "Every execution is verified.",
          "quality": ["Pre-task team and scope check", "Execution to the standard operating procedure", "Mandatory photo and checklist verification", "Central quality control and non-conformity record", "Corrective action, owner and deadline tracking", "Regular KPI and SLA review"],
          "r_eyebrow": "Digital reporting", "r_h2": "What do management teams see?",
          "report": ["Visit date, site and team information", "Question-level scores and photo evidence", "Red, amber and green status summary", "Priority findings and assigned actions", "Site, region and period comparisons", "Management summary and closure tracking"],
          "s_eyebrow": "Scalable roll-out", "s_h2": "From pilot to nationwide.",
          "scale": [("1 · Pilot", "Validating the standard at selected sites: scope, baseline measurement, field execution, results report."), ("2 · Regional roll-out", "Taking the model to priority regions: team planning, training, SLA tracking, regional performance."), ("3 · Nationwide", "Managing the whole network with one model: central coordination, site scores, work orders, management dashboard.")]},
  "about": {"title": "About — BİGEL", "desc": "BİGEL is a new-generation field services platform that runs, audits and reports the field operations of corporate brands.",
            "eyebrow": "About", "h1": "Not a company that sends a handyman. A partner you can trust with your field operation.",
            "lead": "BİGEL is a new-generation field services platform that runs, audits and reports the field operations of corporate brands. It combines local field power with central operations, audit and reporting.",
            "story_h2": "Born in the field, grown with a system.",
            "story": ["BİGEL's journey began in Istanbul in 2018 with exterior cleaning and minor maintenance for fuel station networks. As the number of sites grew, so did the problem: doing the work was not enough; every site had to hold the same standard, and head office needed proof.", "Today BİGEL manages its regional team network with central planning, standard checklists and photo-verified digital reporting. CLEAN, CARE, AUDIT and FIELD360 run under one roof, on one chain of record.", "Our service heritage, known as Bigel Usta, remains the source of our field knowledge; the brand now focuses on corporate field operations and technology."],
            "facts": [(SITE["founded"], "founded, Istanbul"), (SITE["regions"], "regional operations teams"), (SITE["provinces"], "provinces with field access"), ("4", "products, one chain of record")],
            "v_eyebrow": "Brand definition", "v_h2": "Why we exist",
            "values": [("Purpose", "To make brands' field work more orderly, measurable and reliable.", "flag"), ("Promise", "To do the work in the field, control it and make it visible.", "shield"), ("Differentiator", "Local field power + central operations + audit + reporting.", "hub")],
            "c_eyebrow": "Character", "c_h2": "How BİGEL speaks and works",
            "character": [("Reliable", "Standard, evidence and reports. No exaggerated promises."), ("Agile", "Shorter response times through regional teams."), ("Systematic", "Plan + execute + control + report."), ("Solution-driven", "Findings become work orders; work orders get closed."), ("Technological", "Digital checklists, scores and dashboards."), ("Measurable", "100 criteria, photo evidence, one score.")],
            "reg_eyebrow": "Field network", "reg_h2": "Seven regions, one operations centre.",
            "regions": ["Marmara", "Aegean", "Mediterranean", "Central Anatolia", "Black Sea", "Eastern Anatolia", "Southeastern Anatolia"],
            "reg_p": "Central planning and quality control run from Istanbul; execution is done by regional teams. Teams are trained to a common service standard and assessed on uniform, ID, safety and digital record standards."},
  "contact": {"title": "Contact — Quote, pilot and demo requests", "desc": "Let's design your field operation together. Leave a request for a quote, pilot or demo meeting.",
              "eyebrow": "Contact", "h1": "Let's design your field operation together.", "lead": "Fill in the form for a quote, pilot or demo meeting. We respond within the same business day.",
              "f": {"name": "Full name", "company": "Company", "email": "Email", "phone": "Phone", "count": "Number of sites", "counts": ["1–10", "11–50", "51–250", "251–1,000", "1,000+"], "solution": "Solution of interest", "solutions": ["BİGEL CLEAN", "BİGEL CARE", "BİGEL AUDIT / AUDIT 100", "EV Audit30", "BİGEL FIELD360", "Subscription plans", "More than one"], "msg": "Your needs", "msg_ph": "Your site structure, service needs and priorities…", "consent": "I agree to the processing of my personal data for the purpose of responding to my request.", "send": "Send Request", "subject": "bigel360.com — New request"},
              "info": [("Head office", SITE["address_en"]), ("Phone", SITE["phone"]), ("Email", SITE["email"]), ("LinkedIn", "linkedin.com/company/bigel360"), ("Working hours", "Weekdays 08:30–18:00 · Emergency field line 24/7")]},
  "pilot": {"title": "Pilot — Start small, measure, then scale", "desc": "A 4–6 week pilot on 20–30 sites: baseline measurement, photo-verified findings, site scores and a roll-out plan. Apply for a pilot.",
            "eyebrow": "Pilot programme", "h1": "Start small. Measure. Then scale.",
            "lead": "We begin with a short pilot on selected sites. When it ends you hold baseline scores, photo-verified findings and a roll-out plan built on real field data.",
            "stats": [("20–30", "sites for a representative sample"), ("4–6", "weeks of execution"), ("2", "visit rounds: baseline and verification"), ("1", "report: scores, findings, workload and calendar")],
            "why_eyebrow": "Why a pilot", "why_h2": "Proof in the field before the contract.",
            "why": [("Limits risk", "You start with selected sites instead of the whole network. Scope, frequency and budget are settled on real data."), ("Produces real data", "A baseline score, photo-verified finding list and prioritised actions for every site. Measurement, not assumptions."), ("Plans the roll-out", "In the pilot review meeting, regions, visit frequency, teams and budget are decided together.")],
            "steps_eyebrow": "Pilot process", "steps_h2": "A pilot in six steps.",
            "steps": [("Scope and criteria", "Site set, category scope, question set and score weights are approved."), ("Baseline measurement", "Current condition is recorded with photos and checklists."), ("Field execution", "CLEAN, CARE, AUDIT or EV scope delivered by regional teams."), ("Results report", "Site scores, critical findings and action proposals are reported."), ("Second round", "Actions are closed; the second visit verifies score and open-finding progress."), ("Roll-out plan", "A scaling plan with brand standards, SLA targets, regions and calendar.")],
            "out_eyebrow": "Pilot outputs", "out_h2": "What do you have when the pilot ends?",
            "outputs": ["Audit summary and category scores", "Photo-verified finding list: critical, high, medium, low", "Site and regional comparison", "Closure evidence with before and after photos", "Estimated workload, visit frequency and implementation calendar", "Verified unit times and a settled scope for the quote"],
            "photo_tag": "Pilot visit · photo-verified baseline",
            "prod_eyebrow": "Pilot by product", "prod_h2": "Which product should we start with?",
            "prod": [("clean", "CLEAN pilot", "One exterior cleaning round at selected sites. Before and after photos, checklist and quality score."), ("care", "CARE pilot", "Photo-verified physical assessment, minor fixes on the spot and a list of findings needing work orders."), ("audit", "AUDIT 100 pilot", "100-criteria audit, site scorecard, critical findings and action priorities. For EV networks, Audit30: 10 sites, 2 weeks, 2 rounds."), ("field360", "FIELD360 pilot", "An integrated pilot where cleaning, maintenance and audit share one visit plan; one report, one partner.")],
            "form_eyebrow": "Pilot application", "form_h2": "Let's define the pilot scope together.",
            "form_lead": "Fill in the form; we will contact you within the same business day to schedule a 90-minute scoping meeting.",
            "f": {"name": "Full name", "company": "Company", "email": "Email", "phone": "Phone",
                  "sector": "Industry", "sectors": ["Fuel", "EV charging stations", "Restaurants / QSR", "Retail", "Banking", "Automotive", "Logistics / Warehousing", "Malls / Plazas", "Hotels / Tourism", "Telecom", "Education", "Factories / Facilities", "Other"],
                  "count": "Total number of sites", "counts": ["1–10", "11–50", "51–250", "251–1,000", "1,000+"],
                  "geo": "City / regional spread", "geo_ph": "e.g. Istanbul 12, Ankara 6, Izmir 4…",
                  "product": "Starting product", "products": ["AUDIT 100", "EV Audit30", "CLEAN", "CARE", "FIELD360", "Not decided yet"],
                  "start": "Target start", "starts": ["Within 2 weeks", "Within 1 month", "Within 1–3 months", "Still planning"],
                  "msg": "Notes", "msg_ph": "Priority sites, current supplier setup, expectations…",
                  "consent": "I agree to the processing of my personal data for the purpose of responding to my request.", "send": "Send Pilot Application", "subject": "bigel360.com — Pilot application"},
            "after_h3": "After you apply", "after": [("1", "Scoping meeting", "90 minutes. Site structure, service modules and pilot success criteria."), ("2", "Pilot plan", "Site set, question set, photo rules, SLA and calendar in one document."), ("3", "Field", "Visits begin; critical findings are reported the same day."), ("4", "Review meeting", "Scores, findings and the roll-out proposal.")],
            "note": "Pilot scope and fee are quoted based on site count, service module and geographic spread. Pilot results settle the final unit price."},
  "thanks": {"title": "Thank you", "h1": "Your request has been received.", "p": "Our team will contact you within the same business day. In the meantime, feel free to explore our solutions.", "b": "Back to home"},
},
}

# ---------------------------------------------------------------- RENDER HELPERS
def sec(inner, cls="", id_=""):
    return f'<section class="section {cls}"{f" id={chr(34)}{id_}{chr(34)}" if id_ else ""}><div class="container">{inner}</div></section>'

def head(eyebrow, h2, lead="", center=False):
    return f'<div class="section-head{" center" if center else ""}">{f"<span class={chr(34)}eyebrow{chr(34)}>{esc(eyebrow)}</span>" if eyebrow else ""}<h2>{esc(h2)}</h2>{f"<p class={chr(34)}lead{chr(34)}>{esc(lead)}</p>" if lead else ""}</div>'

def ul(items, accent=None):
    style = f' style="--accent:{accent}"' if accent else ""
    return f'<ul class="list"{style}>' + "".join(f"<li>{esc(i)}</li>" for i in items) + "</ul>"

def tr_upper(s, lang):
    if lang == "tr": s = s.replace("i", "İ").replace("ı", "I")
    return s.upper()

def product_cards(lang):
    L = CONTENT[lang]
    out = ""
    for p in PRODUCTS:
        d = L["products"][p]
        out += (f'<a class="card accent product-card" style="--accent:{ACCENT[p]}" href="{href(lang,p)}">'
                f'<img src="{asset(lang,"logo/"+p+".png")}" alt="{esc(d["name"])}" loading="lazy">'
                f'<span class="kicker">{esc(tr_upper(d["cat"], lang))}</span><h3>{esc(d["tag"])}</h3><p>{esc(d["short"])}</p>'
                f'<span class="more">{esc(L["more"])} →</span></a>')
    return f'<div class="grid g4">{out}</div>'

def sector_cards(lang, n=None):
    L = CONTENT[lang]
    items = L["sectors_list"][:n] if n else L["sectors_list"]
    out = ""
    for (title, desc), ic in zip(items, SECTOR_ICONS):
        out += f'<div class="sector">{icon(ic)}<div><h3>{esc(title)}</h3><p>{esc(desc)}</p></div></div>'
    return f'<div class="sectors">{out}</div>'

def tier_cards(lang, compact=False):
    L = CONTENT[lang]
    imgs = ["tier-basic.jpg", "tier-pro.jpg", "tier-business.jpg", "tier-360.jpg"]
    out = ""
    for i, (name, sub, one, who, feats) in enumerate(L["tiers_list"]):
        feat = "" if compact else "<ul>" + "".join(f"<li>{esc(f)}</li>" for f in feats) + "</ul>"
        cta = "" if compact else f'<a class="btn btn-outline btn-sm" href="{href(lang,"contact")}">{esc(L["tiers"]["cta"])}</a>'
        featured = ' featured' if (i == 3 and not compact) else ""
        out += (f'<div class="card tier{featured}" data-badge="{esc(L["tiers"]["badge"])}"><img src="{asset(lang,"logo/"+imgs[i])}" alt="{esc(name)}" loading="lazy">'
                f'<span class="name">{esc(name)}</span><h3>{esc(sub)}</h3><p class="who">{esc(one if compact else who)}</p>{feat}{cta}</div>')
    return f'<div class="tiers">{out}</div>'

def flow(steps):
    return '<div class="flow">' + "".join(f'<div class="step"><b>{i+1:02d}</b><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for i, (t, d) in enumerate(steps)) + "</div>"

def cta_band(lang):
    L = CONTENT[lang]["cta"]
    return sec(f'<div class="cta-band"><div><h2>{esc(L["h2"])}</h2><p>{esc(L["p"])}</p></div><div class="btn-row"><a class="btn btn-primary" href="{href(lang,"pilot")}">{esc(L["b1"])}</a><a class="btn btn-ghost" href="{href(lang,"contact")}">{esc(L["b2"])}</a></div></div>')

def scorecard(lang):
    c = CONTENT[lang]["home"]["card"]
    bars = "".join(f'<div class="bar"><span>{esc(n)}</span><span>{v}</span><i style="--w:{v}%;--c:{col}"></i></div>' for n, v, col in c["bars"])
    return (f'<div class="scorecard"><div class="top"><div class="loc">{esc(c["loc"])}<small>{esc(c["meta"])}</small></div>'
            f'<div><div class="score">87<small>/100</small></div><span class="pill amber">{esc(c["status"])}</span></div></div>'
            f'<div class="bars">{bars}</div><div class="foot"><span>{c["foot_l"]}</span><span>{esc(c["foot_r"])}</span></div></div>')

TURKEY_PATH = 'M298.1 10.0 L295.8 10.3 L295.4 12.0 L292.3 15.2 L288.7 16.1 L283.6 15.8 L282.0 14.9 L279.5 15.1 L275.7 15.8 L272.9 15.4 L267.6 14.6 L260.4 14.8 L247.9 13.2 L244.3 13.4 L234.3 17.0 L233.5 18.3 L230.2 19.5 L224.4 20.4 L221.9 20.8 L218.0 21.9 L216.6 23.1 L213.5 24.7 L211.4 25.2 L209.1 27.1 L206.6 29.9 L203.1 31.7 L198.8 33.6 L194.5 36.2 L190.8 38.8 L186.9 40.2 L184.4 41.6 L183.0 42.3 L182.8 43.7 L183.0 45.9 L182.2 47.5 L180.3 49.7 L176.9 50.3 L171.1 51.7 L164.0 51.4 L160.5 49.7 L156.7 49.0 L151.8 47.7 L147.8 46.2 L146.2 47.1 L145.0 48.0 L143.5 49.1 L137.8 48.9 L134.1 49.1 L131.8 48.3 L128.8 47.9 L126.2 47.5 L124.9 47.8 L120.0 46.2 L118.6 46.2 L116.2 45.6 L113.7 45.6 L111.5 45.8 L110.8 44.9 L109.5 44.4 L107.4 44.6 L104.0 43.7 L98.2 40.8 L95.5 40.2 L82.7 33.1 L80.5 30.7 L78.9 28.7 L79.2 27.6 L77.5 25.8 L77.3 24.7 L74.9 20.7 L75.6 19.4 L77.0 19.7 L77.4 17.9 L77.1 16.3 L76.8 15.1 L75.6 15.3 L74.6 15.0 L72.5 15.4 L71.3 14.5 L69.7 15.0 L70.0 16.5 L68.4 16.3 L66.8 15.5 L65.3 15.7 L63.4 16.5 L62.0 17.3 L61.5 18.3 L59.7 16.2 L57.5 15.4 L56.1 14.1 L55.0 12.1 L53.0 10.6 L51.3 10.4 L50.1 11.2 L47.4 11.5 L45.9 10.8 L44.6 11.2 L43.7 12.9 L42.1 14.4 L40.3 14.9 L39.1 14.6 L38.7 15.5 L37.2 15.0 L35.8 15.8 L33.2 15.8 L31.6 15.4 L29.7 17.5 L30.3 18.2 L30.0 19.3 L28.9 21.6 L23.5 21.8 L22.1 24.9 L23.1 26.3 L24.6 27.3 L25.8 27.2 L26.7 28.0 L27.3 28.6 L28.7 30.0 L29.8 30.4 L30.8 31.6 L30.6 32.7 L31.0 34.9 L31.3 36.4 L31.2 38.0 L31.8 38.9 L31.9 40.2 L31.6 41.3 L30.4 42.4 L28.7 41.4 L27.9 41.9 L27.2 42.8 L26.3 43.8 L24.5 45.1 L22.6 44.9 L21.9 45.9 L22.0 47.7 L22.4 49.4 L21.6 50.7 L21.8 52.0 L22.4 53.6 L23.4 54.4 L22.9 55.8 L23.2 57.6 L21.4 58.3 L20.8 59.7 L20.1 58.9 L19.7 60.1 L18.9 60.8 L18.3 61.7 L17.7 62.7 L17.0 63.3 L16.2 64.1 L15.9 65.3 L14.6 66.2 L13.6 66.4 L12.4 66.7 L12.5 68.8 L13.2 71.1 L15.6 72.6 L19.1 72.8 L23.8 72.7 L27.4 72.9 L29.6 72.1 L32.8 71.3 L36.0 71.6 L37.1 70.7 L37.8 72.3 L35.2 73.0 L34.0 74.6 L31.5 74.8 L26.8 77.1 L23.5 79.6 L18.6 82.2 L18.1 83.1 L18.8 83.8 L20.0 85.8 L20.2 86.9 L19.1 89.7 L16.7 93.4 L16.9 94.7 L18.8 94.5 L20.5 93.4 L21.9 92.4 L22.9 91.5 L23.9 90.7 L23.8 89.0 L25.3 87.5 L27.1 86.4 L28.2 84.9 L30.2 83.8 L31.0 83.1 L32.0 81.7 L32.4 80.5 L33.1 80.0 L34.2 79.0 L36.5 77.0 L40.0 75.4 L43.6 74.0 L45.4 72.3 L48.1 71.6 L50.1 70.6 L52.6 69.0 L54.3 67.2 L54.7 65.4 L58.7 61.7 L58.9 60.1 L59.5 58.1 L60.7 57.0 L64.1 56.1 L67.1 55.5 L69.5 55.8 L70.5 57.0 L72.8 57.4 L74.2 57.4 L74.9 56.8 L75.4 55.4 L76.5 54.4 L79.4 53.4 L81.5 53.4 L84.6 53.4 L89.4 54.9 L92.0 56.5 L93.2 56.2 L94.4 57.2 L95.6 57.4 L97.8 57.4 L99.6 56.9 L101.4 57.8 L102.4 57.2 L104.5 56.4 L106.5 55.7 L107.3 56.6 L109.1 57.7 L110.2 58.3 L111.1 59.8 L109.7 59.3 L109.3 58.5 L108.1 58.5 L108.1 59.7 L110.0 61.3 L110.0 62.7 L111.3 62.5 L112.2 61.9 L112.3 60.7 L114.0 61.1 L114.6 62.2 L114.7 63.7 L115.7 64.0 L117.1 63.7 L117.5 64.9 L118.2 66.0 L120.0 65.7 L122.6 64.9 L123.7 65.3 L125.2 65.4 L127.3 65.3 L130.2 65.2 L130.7 66.3 L128.5 66.6 L124.7 67.3 L124.3 65.7 L122.3 65.9 L120.5 67.4 L119.9 66.8 L118.7 67.2 L116.6 68.1 L114.1 68.2 L110.9 68.7 L106.3 69.1 L104.9 70.9 L100.9 72.2 L99.6 73.6 L99.8 75.1 L101.7 76.0 L102.7 76.8 L105.8 78.0 L109.0 77.5 L110.4 78.5 L109.3 79.3 L108.6 80.7 L106.4 81.0 L104.8 80.7 L101.6 79.5 L97.7 79.7 L95.1 80.6 L91.6 79.5 L87.5 79.5 L82.8 79.5 L78.2 80.0 L74.1 81.1 L73.0 80.3 L75.2 79.2 L76.1 78.6 L76.7 77.7 L78.2 78.1 L78.9 76.9 L77.0 77.1 L76.4 75.9 L74.0 75.2 L71.4 74.7 L68.0 74.3 L65.9 74.5 L65.1 75.6 L65.2 76.9 L66.4 77.8 L67.0 79.0 L68.2 79.8 L68.2 81.1 L69.2 80.8 L70.7 80.8 L69.6 82.0 L68.1 83.2 L65.8 83.0 L65.0 83.4 L63.3 82.7 L62.2 83.1 L60.7 83.8 L58.4 83.2 L56.1 82.1 L53.6 80.5 L54.5 79.6 L54.0 78.1 L53.3 77.4 L52.5 76.6 L51.8 77.1 L51.0 77.6 L49.7 78.1 L48.7 77.5 L47.3 77.5 L46.4 77.9 L45.3 79.0 L44.6 79.8 L42.4 80.3 L41.4 79.8 L40.1 79.7 L38.2 79.9 L36.5 79.5 L34.6 80.1 L34.0 80.8 L33.5 81.5 L32.2 82.7 L31.5 83.7 L30.9 84.5 L29.3 85.1 L28.9 86.3 L27.7 87.5 L26.6 87.8 L25.2 87.9 L24.2 88.3 L24.5 89.8 L24.4 91.3 L23.5 91.7 L23.0 92.9 L22.1 94.8 L20.0 95.4 L17.1 95.5 L15.9 98.0 L15.9 100.9 L15.2 103.7 L14.7 102.3 L12.9 101.6 L10.6 101.9 L10.0 103.4 L11.0 104.8 L13.1 105.8 L15.2 105.1 L15.5 107.9 L15.5 110.7 L13.8 112.6 L13.5 116.4 L13.1 118.4 L15.2 119.4 L21.2 117.7 L23.3 117.9 L24.0 117.3 L26.2 116.3 L31.8 115.0 L33.6 114.7 L35.5 114.4 L36.9 114.2 L37.9 114.8 L39.3 114.5 L40.5 113.5 L41.5 114.2 L40.9 116.8 L40.1 117.3 L38.6 118.1 L38.4 119.1 L37.0 119.2 L37.1 120.8 L36.4 121.3 L35.7 122.1 L34.9 121.4 L34.7 120.1 L34.0 120.8 L33.7 121.8 L33.0 121.0 L31.5 120.8 L29.8 120.9 L30.1 121.9 L29.1 123.2 L28.4 124.1 L29.5 123.8 L31.4 123.9 L30.5 124.3 L29.9 125.7 L30.8 126.1 L31.9 126.5 L33.3 126.7 L34.5 127.2 L34.6 128.4 L35.8 130.4 L36.9 131.1 L38.5 132.5 L39.4 134.0 L37.6 134.8 L36.5 135.8 L36.4 137.6 L36.8 139.1 L37.0 140.4 L37.9 141.2 L39.8 140.9 L40.7 140.2 L41.8 140.4 L43.8 141.0 L44.0 142.1 L43.1 142.7 L42.4 143.3 L40.6 144.1 L39.8 144.7 L40.7 146.1 L39.9 147.5 L38.7 146.9 L37.9 146.5 L37.0 147.1 L35.2 147.4 L34.1 148.2 L33.8 149.1 L34.2 150.6 L34.7 151.6 L35.4 152.8 L37.2 154.0 L37.8 154.8 L37.4 155.7 L38.3 156.9 L39.3 157.5 L40.1 158.2 L40.2 159.3 L41.3 159.9 L41.8 160.7 L42.9 160.5 L44.0 159.9 L45.7 159.6 L46.6 160.0 L47.4 160.4 L46.5 161.5 L44.7 160.7 L43.0 161.3 L41.4 161.9 L39.9 162.1 L38.1 162.7 L37.4 161.7 L36.8 160.5 L36.4 159.3 L35.9 158.5 L35.5 156.9 L35.1 156.0 L34.2 155.3 L33.5 156.3 L33.6 157.6 L34.2 158.8 L34.0 160.0 L33.2 160.7 L33.1 161.8 L32.7 162.9 L32.2 162.1 L31.9 161.1 L31.2 160.5 L32.4 159.2 L32.1 156.2 L31.0 155.6 L30.2 154.4 L29.8 153.2 L29.1 152.1 L28.8 151.1 L27.7 150.6 L26.2 150.2 L25.1 149.9 L24.2 150.5 L22.9 150.9 L22.8 152.1 L22.7 154.2 L23.3 155.8 L23.9 157.3 L24.4 158.3 L23.9 159.1 L22.6 159.3 L21.7 160.2 L22.7 161.1 L24.3 161.1 L24.7 160.1 L25.4 159.0 L26.1 159.5 L27.6 160.4 L26.0 160.3 L25.7 161.5 L25.2 162.4 L24.6 163.7 L23.7 164.1 L22.4 163.5 L21.8 162.3 L20.7 162.0 L20.2 163.6 L20.4 164.7 L19.9 165.9 L18.8 166.1 L19.0 167.4 L20.8 167.8 L21.4 168.8 L23.9 169.0 L24.7 169.8 L25.5 170.8 L27.7 171.4 L28.3 173.0 L29.7 173.5 L31.0 174.2 L31.7 172.8 L32.2 172.1 L32.1 170.9 L32.4 170.0 L33.8 169.9 L35.7 169.4 L36.1 170.4 L36.6 171.9 L37.7 172.8 L38.4 173.6 L38.5 175.6 L38.9 176.6 L39.9 177.5 L40.1 176.0 L41.4 175.5 L42.8 175.3 L43.8 176.0 L45.1 176.4 L45.5 177.3 L46.7 178.0 L47.6 178.8 L48.6 179.1 L50.1 178.7 L51.2 179.1 L51.9 180.5 L51.6 182.1 L51.0 183.6 L51.0 185.3 L51.8 186.8 L50.9 188.9 L50.1 189.5 L48.5 190.1 L47.0 190.6 L45.2 190.6 L44.0 190.5 L43.5 191.4 L43.6 192.6 L45.3 193.0 L46.7 193.3 L47.5 194.1 L48.5 195.7 L49.1 197.4 L49.1 199.7 L50.2 199.3 L50.1 200.7 L50.2 202.0 L50.0 203.0 L49.4 204.0 L50.3 205.1 L51.3 205.4 L52.4 205.0 L53.6 205.4 L54.5 205.0 L54.9 204.2 L55.5 203.3 L55.5 205.2 L55.9 206.1 L57.4 206.9 L58.6 206.2 L57.7 208.2 L58.2 209.0 L59.6 208.4 L59.1 209.3 L60.5 209.8 L61.4 209.3 L61.7 208.1 L62.2 209.0 L61.5 209.9 L59.8 210.7 L60.4 211.6 L59.4 212.0 L58.7 213.3 L58.4 214.3 L59.3 213.5 L60.5 213.5 L58.9 214.6 L58.0 214.2 L57.0 213.3 L56.2 212.6 L55.4 211.6 L54.8 212.6 L54.0 212.2 L53.3 213.4 L52.4 212.8 L51.4 213.4 L51.7 214.5 L50.9 215.2 L50.6 216.3 L50.9 217.6 L51.5 218.5 L51.3 220.0 L52.0 220.7 L53.2 221.2 L53.9 220.3 L54.4 219.5 L55.8 219.7 L56.1 218.4 L57.2 218.6 L56.6 219.3 L57.9 220.6 L58.9 220.8 L59.9 219.9 L62.2 220.6 L63.2 220.1 L64.8 220.0 L66.8 219.5 L68.7 219.6 L69.8 219.0 L72.9 218.4 L74.4 218.4 L75.6 218.3 L77.8 218.7 L79.0 218.8 L79.6 218.1 L81.8 217.8 L84.4 217.3 L83.5 218.1 L82.1 218.6 L81.3 219.6 L80.6 220.7 L79.7 221.1 L78.0 220.9 L76.6 221.2 L75.5 222.4 L76.1 223.6 L75.4 224.2 L75.3 225.3 L76.0 226.3 L74.9 226.6 L72.9 226.6 L70.8 226.3 L68.5 226.6 L65.7 227.1 L64.6 226.4 L63.2 226.9 L62.9 228.2 L61.2 228.4 L59.6 228.7 L58.6 228.0 L57.9 228.6 L56.6 229.2 L56.3 230.6 L54.8 230.6 L54.9 232.1 L55.9 232.4 L57.0 232.9 L58.1 233.3 L59.4 233.4 L60.6 232.9 L61.6 232.6 L64.2 233.1 L65.4 233.3 L65.3 232.1 L66.1 230.7 L67.0 229.0 L68.0 229.4 L69.3 229.2 L70.3 229.7 L71.7 229.8 L73.5 229.7 L74.5 229.3 L76.8 228.9 L77.7 229.5 L76.3 229.7 L75.2 230.0 L74.5 230.8 L74.0 231.9 L74.9 232.6 L75.9 232.9 L76.8 233.7 L76.6 234.7 L75.2 234.5 L73.7 235.1 L74.3 236.8 L75.3 237.1 L76.5 237.4 L77.6 235.9 L78.9 235.8 L79.7 235.2 L80.3 233.7 L81.0 232.4 L82.7 231.9 L83.6 231.1 L84.7 230.6 L85.1 229.2 L84.2 228.5 L83.8 227.5 L84.9 227.7 L85.6 227.0 L86.5 227.4 L87.3 227.9 L88.6 227.6 L89.3 225.7 L89.9 226.8 L90.8 227.5 L92.3 228.0 L93.0 227.5 L93.8 226.9 L94.5 227.4 L94.7 229.1 L94.5 230.1 L95.0 231.4 L96.2 231.1 L97.1 231.8 L98.5 231.3 L100.1 232.0 L100.5 233.5 L101.5 233.9 L101.0 234.7 L101.8 235.5 L103.0 235.7 L103.5 234.9 L104.2 233.9 L104.9 233.0 L105.6 232.4 L105.7 230.6 L107.0 231.4 L107.9 232.1 L108.3 233.1 L109.2 234.1 L107.9 234.8 L107.4 235.7 L108.1 237.0 L107.0 237.5 L108.5 238.1 L109.6 237.4 L110.7 237.9 L110.4 239.6 L110.5 241.2 L110.9 242.0 L110.3 243.0 L110.0 243.9 L111.1 244.8 L112.0 245.7 L113.3 246.6 L114.3 246.8 L116.3 249.0 L116.9 249.9 L118.5 250.6 L119.2 249.9 L120.1 249.4 L120.2 250.8 L121.2 250.6 L120.9 251.7 L121.8 251.0 L123.2 251.4 L124.5 251.4 L125.5 251.7 L126.2 252.4 L126.9 251.9 L126.7 253.2 L127.4 253.9 L127.9 254.7 L129.5 254.3 L130.8 253.8 L130.3 254.8 L132.3 254.4 L133.6 253.4 L135.4 253.1 L136.3 252.3 L136.3 250.8 L137.6 251.2 L138.8 251.2 L140.4 249.9 L142.1 249.9 L143.2 249.5 L144.0 248.9 L144.7 247.4 L147.8 247.1 L149.5 248.5 L150.5 249.0 L151.4 249.8 L151.3 251.1 L151.6 252.6 L152.2 251.8 L153.1 250.4 L154.1 250.7 L154.0 249.4 L154.7 248.3 L154.9 247.0 L156.0 246.6 L155.4 245.2 L154.7 244.0 L154.8 242.9 L155.5 241.9 L156.0 241.2 L156.6 238.8 L157.4 238.3 L158.1 236.0 L157.5 235.1 L157.2 233.1 L157.5 231.0 L157.9 227.2 L158.9 225.7 L159.8 224.7 L160.7 223.9 L162.2 225.2 L163.2 225.6 L164.6 225.5 L170.0 225.1 L171.8 225.3 L174.0 225.9 L176.4 226.3 L181.2 227.1 L182.3 227.8 L183.0 228.9 L187.8 230.7 L189.3 231.8 L191.0 233.0 L191.6 233.7 L194.1 234.0 L194.7 234.9 L196.2 235.8 L198.7 236.5 L199.9 237.1 L201.6 237.6 L202.5 238.4 L205.5 240.3 L206.2 241.4 L206.8 242.1 L208.1 244.0 L209.4 246.5 L210.6 247.8 L211.0 248.7 L211.3 249.9 L212.1 250.6 L213.2 251.2 L214.6 253.2 L215.9 254.1 L218.0 255.5 L219.5 256.2 L222.6 257.6 L223.8 258.4 L227.1 258.9 L228.1 259.5 L228.6 258.7 L229.9 257.7 L231.0 256.8 L232.5 256.3 L235.1 256.3 L236.4 256.7 L237.7 256.1 L238.5 254.7 L240.6 254.8 L242.7 254.8 L244.1 254.6 L245.7 254.5 L246.8 255.0 L247.9 254.4 L248.9 253.7 L250.9 254.4 L252.1 255.0 L252.9 253.7 L253.5 252.7 L255.0 252.5 L255.4 253.9 L256.4 254.7 L256.8 253.6 L257.3 252.3 L258.3 251.6 L259.0 252.7 L259.4 251.6 L259.9 250.5 L261.4 248.8 L262.1 247.4 L264.1 248.8 L264.4 250.5 L265.5 249.4 L266.8 248.0 L268.3 247.7 L268.9 246.6 L268.9 245.2 L269.1 243.2 L270.1 242.5 L271.5 241.2 L272.3 239.9 L273.6 238.5 L274.5 236.9 L275.7 235.8 L276.6 235.3 L279.8 233.1 L281.3 231.4 L282.8 230.2 L283.7 229.8 L284.3 228.6 L285.8 227.9 L286.7 227.3 L288.3 227.1 L290.6 226.9 L293.8 228.6 L294.6 230.0 L296.1 230.4 L297.8 231.0 L308.1 237.2 L308.7 238.0 L309.8 237.5 L311.1 236.6 L313.4 236.1 L315.2 236.8 L316.5 236.0 L317.5 235.7 L318.4 234.7 L318.4 233.2 L320.7 231.2 L321.0 230.2 L319.8 230.6 L318.4 230.9 L318.6 229.4 L319.5 228.9 L321.8 228.8 L323.1 229.0 L323.9 228.3 L324.9 227.7 L326.3 226.3 L327.0 225.3 L327.9 224.9 L330.0 222.2 L331.1 222.6 L333.3 224.0 L334.4 225.3 L335.6 227.7 L335.5 229.9 L335.7 231.9 L336.3 233.3 L335.7 233.9 L335.8 235.2 L334.1 235.5 L330.8 237.6 L330.4 238.6 L328.8 240.1 L326.7 241.2 L326.1 242.5 L325.2 243.3 L325.0 244.4 L323.8 244.7 L322.8 246.1 L322.6 247.8 L324.8 251.4 L326.3 254.0 L327.3 255.7 L328.8 259.4 L328.1 260.3 L327.4 260.9 L327.1 262.6 L328.7 262.5 L329.7 262.2 L330.0 263.7 L331.6 264.8 L333.1 265.5 L334.3 267.4 L335.2 266.3 L335.3 264.1 L335.4 262.4 L336.6 261.7 L337.9 261.2 L338.7 262.1 L339.2 261.3 L338.9 260.4 L340.0 260.1 L341.8 259.3 L342.0 257.9 L341.7 256.8 L342.0 255.9 L341.5 255.0 L341.9 254.1 L341.4 253.3 L341.7 252.3 L342.3 251.7 L343.4 251.3 L344.5 251.7 L345.2 250.8 L345.6 249.9 L347.2 250.6 L348.6 250.6 L349.5 251.0 L349.8 250.0 L350.7 250.4 L351.8 249.8 L351.3 248.7 L351.8 247.7 L350.6 247.6 L350.8 246.5 L349.6 245.7 L349.0 246.3 L349.4 245.3 L348.7 244.5 L347.7 242.5 L347.4 240.9 L347.0 239.4 L347.8 238.2 L348.4 235.8 L348.0 234.5 L347.9 232.8 L349.1 231.9 L349.9 230.7 L349.1 229.4 L350.1 227.7 L351.1 226.8 L353.4 226.3 L354.7 227.0 L357.4 227.8 L358.5 228.1 L359.7 228.2 L360.9 228.7 L361.4 229.5 L362.9 229.8 L362.8 231.2 L362.1 232.6 L363.3 233.1 L364.3 233.9 L364.9 232.4 L365.9 232.1 L366.8 232.9 L368.2 232.2 L370.1 232.6 L374.3 233.4 L375.6 233.7 L376.6 234.0 L377.1 233.1 L380.5 230.7 L382.2 229.2 L383.7 228.8 L386.5 229.1 L390.4 227.5 L391.2 226.3 L393.4 225.8 L394.3 224.7 L395.4 224.3 L396.5 223.7 L398.5 223.0 L400.1 222.6 L401.2 222.0 L403.3 222.7 L405.0 223.1 L411.0 225.4 L411.6 226.1 L412.1 226.8 L416.6 230.8 L419.9 231.1 L424.0 230.9 L426.2 230.7 L431.8 232.5 L435.6 232.0 L437.4 231.5 L441.5 230.9 L444.7 230.3 L446.6 229.8 L447.9 229.0 L451.6 228.8 L452.6 228.0 L457.4 226.1 L458.4 225.7 L458.9 224.8 L462.6 224.0 L464.3 222.5 L467.3 220.9 L468.8 220.0 L469.8 218.2 L473.7 217.7 L475.7 216.4 L477.0 216.0 L478.9 214.8 L481.0 214.2 L482.6 213.9 L483.5 214.5 L485.6 213.6 L492.3 215.0 L494.9 215.4 L495.6 216.3 L498.8 215.7 L504.2 215.6 L505.9 215.4 L508.5 214.3 L510.4 214.0 L512.1 214.0 L515.9 213.1 L519.3 212.3 L521.6 211.3 L523.2 210.3 L524.6 208.6 L526.4 207.0 L526.9 206.1 L527.0 207.4 L528.7 207.8 L530.0 208.2 L531.5 209.4 L530.7 211.3 L531.4 213.1 L531.7 214.0 L532.8 214.4 L533.5 213.9 L534.5 213.5 L535.9 213.4 L536.9 213.0 L538.1 212.8 L539.2 211.9 L540.1 210.7 L541.3 208.8 L541.6 207.8 L542.6 206.9 L543.7 205.9 L545.4 203.5 L546.7 203.7 L547.5 204.8 L551.0 206.1 L551.8 205.6 L553.1 204.4 L554.8 203.9 L556.8 203.7 L557.6 204.3 L559.3 204.8 L560.4 205.5 L562.2 206.4 L562.8 205.6 L564.2 206.2 L567.4 208.2 L568.6 209.1 L570.3 208.4 L571.2 209.4 L572.2 210.0 L573.3 209.7 L574.6 209.4 L577.3 209.6 L578.7 210.9 L579.4 209.7 L580.7 209.9 L582.2 209.0 L582.7 207.6 L583.8 206.5 L584.6 205.5 L586.1 205.7 L587.9 205.9 L589.2 206.5 L590.4 207.0 L591.4 207.6 L592.1 208.7 L592.6 211.0 L592.9 212.1 L591.3 212.4 L589.9 214.7 L591.4 217.0 L592.2 219.6 L593.9 220.4 L594.5 219.3 L595.6 217.9 L596.3 216.6 L598.4 215.9 L600.5 214.7 L601.0 213.9 L602.1 212.4 L603.5 211.7 L605.7 211.9 L608.2 212.2 L609.0 213.0 L608.4 211.4 L608.1 209.5 L609.1 208.4 L610.0 207.4 L609.4 206.2 L608.4 205.4 L607.4 204.6 L607.0 203.5 L604.9 203.0 L604.1 201.2 L602.6 200.8 L602.7 199.5 L602.7 198.2 L603.5 196.6 L603.2 195.1 L602.3 192.8 L603.8 190.0 L602.8 187.6 L601.1 186.9 L599.0 187.7 L598.1 187.3 L598.3 186.0 L596.6 185.3 L596.8 184.1 L595.4 183.5 L594.4 183.1 L592.7 183.3 L591.1 182.7 L591.4 181.0 L592.1 180.3 L592.7 177.0 L593.8 176.4 L594.2 175.5 L594.6 174.0 L595.3 172.6 L596.6 172.0 L597.0 169.0 L598.7 166.2 L599.9 165.5 L600.4 164.1 L599.7 163.3 L598.3 162.3 L595.9 163.3 L594.4 162.8 L593.8 161.9 L593.8 159.7 L594.1 158.3 L593.9 156.6 L594.1 154.7 L594.2 152.4 L592.8 151.7 L593.0 150.6 L592.3 148.6 L592.9 147.9 L593.2 146.0 L594.0 145.0 L593.7 143.8 L592.8 143.2 L591.7 142.4 L590.8 141.4 L590.4 140.4 L590.4 139.2 L590.1 138.0 L589.7 136.7 L590.8 136.4 L590.2 135.3 L590.1 134.2 L591.3 133.3 L590.7 132.3 L589.6 129.9 L587.8 129.4 L587.2 128.7 L587.3 127.2 L587.5 125.6 L586.5 125.0 L586.4 123.4 L585.3 122.3 L585.8 121.3 L586.9 120.3 L588.1 120.6 L590.3 120.7 L591.1 120.0 L591.9 120.8 L593.1 121.7 L594.1 121.3 L596.2 120.3 L597.6 120.3 L597.9 119.2 L597.2 117.9 L598.0 116.5 L597.3 114.4 L599.4 112.2 L599.7 110.8 L599.3 110.0 L603.5 105.3 L604.6 107.3 L605.7 108.0 L608.1 109.6 L609.3 110.7 L609.7 111.5 L610.0 110.4 L609.5 109.7 L609.0 108.7 L608.4 107.9 L607.7 107.1 L606.9 106.6 L606.6 105.6 L605.3 104.6 L604.2 104.0 L603.5 103.4 L602.8 101.9 L601.8 101.1 L601.0 99.4 L600.1 98.6 L599.0 97.3 L597.4 96.2 L596.2 95.7 L595.2 95.2 L594.0 94.8 L593.0 94.3 L590.9 94.4 L589.8 94.8 L587.6 94.9 L586.3 94.8 L584.8 95.2 L583.0 95.5 L581.7 95.2 L579.8 94.7 L578.3 94.2 L576.7 92.7 L575.2 92.8 L574.2 92.3 L573.4 91.9 L573.0 91.0 L573.5 90.0 L575.0 89.7 L574.2 88.3 L573.2 87.1 L574.0 86.2 L573.5 85.2 L572.4 84.0 L571.6 82.8 L571.1 81.9 L571.4 80.9 L572.0 79.0 L571.2 78.0 L570.4 77.5 L570.3 76.0 L571.3 75.5 L572.5 74.9 L572.8 73.5 L574.9 70.4 L575.4 69.1 L575.9 67.5 L576.1 66.3 L574.7 62.4 L573.8 61.6 L573.9 59.5 L573.9 58.2 L571.1 55.8 L570.0 55.6 L568.9 54.7 L567.2 54.2 L567.3 52.8 L566.5 51.3 L567.3 50.3 L566.5 48.1 L565.4 47.8 L564.1 47.0 L562.7 47.3 L561.3 47.7 L559.6 48.3 L558.4 45.0 L557.0 45.3 L558.0 44.1 L559.0 43.5 L558.1 42.9 L557.3 42.4 L555.6 41.0 L554.4 40.4 L553.6 39.9 L552.3 38.8 L551.8 38.0 L551.3 36.9 L550.2 36.4 L549.0 35.6 L548.2 34.9 L547.7 36.1 L546.8 35.6 L545.9 34.9 L546.6 32.5 L547.3 31.3 L545.5 31.4 L543.8 31.0 L542.1 30.8 L539.7 31.4 L538.5 32.3 L538.9 33.3 L538.6 34.6 L537.5 35.3 L536.9 36.0 L537.0 37.5 L535.4 37.5 L533.9 36.9 L533.0 36.2 L531.1 36.2 L528.9 35.2 L527.0 35.2 L526.1 34.3 L525.0 34.7 L523.2 34.5 L521.9 35.2 L520.3 34.7 L519.3 33.9 L517.6 35.0 L517.1 35.7 L515.6 37.0 L514.8 37.7 L513.8 37.0 L512.5 36.1 L511.2 36.0 L510.0 35.6 L508.8 35.5 L507.2 34.6 L506.3 34.2 L504.3 35.5 L503.0 36.4 L501.9 38.4 L500.7 39.2 L498.0 40.1 L494.9 42.7 L492.9 43.7 L490.3 45.8 L486.0 47.4 L483.9 47.6 L480.9 49.1 L479.4 51.1 L477.0 52.1 L473.9 53.7 L473.0 53.2 L468.3 54.0 L466.4 56.1 L463.0 58.1 L459.9 58.4 L459.2 56.8 L457.2 55.7 L453.0 56.4 L451.6 55.3 L448.5 54.1 L446.7 54.7 L444.7 54.3 L442.6 52.5 L440.7 50.9 L438.4 50.3 L436.4 51.3 L433.6 52.5 L432.7 51.7 L430.7 51.6 L429.1 51.6 L426.9 53.1 L425.0 53.3 L422.4 53.0 L420.5 54.1 L418.8 54.2 L417.2 55.5 L415.3 56.6 L414.2 55.9 L412.5 56.2 L410.2 57.8 L407.1 58.0 L404.5 57.8 L403.0 57.1 L400.8 57.3 L398.5 56.9 L396.0 55.8 L390.3 55.3 L389.4 54.5 L387.8 53.7 L386.8 52.1 L387.5 50.0 L384.6 49.8 L382.8 49.3 L381.4 50.8 L379.9 53.6 L378.1 53.6 L377.2 52.3 L375.3 51.4 L374.2 50.3 L371.5 49.9 L370.9 48.9 L366.7 48.5 L363.2 47.4 L363.1 45.7 L362.4 43.5 L357.4 40.7 L351.1 39.1 L349.6 39.4 L348.1 41.6 L346.5 44.3 L343.2 44.8 L341.2 43.2 L340.3 41.7 L337.9 40.4 L335.6 37.2 L334.2 35.5 L334.6 33.1 L334.2 30.6 L332.8 27.4 L330.2 25.5 L327.9 24.8 L324.0 26.4 L319.8 28.3 L315.3 28.6 L312.2 27.7 L310.7 26.7 L307.5 25.2 L305.3 23.7 L304.2 21.4 L301.5 18.4 L301.5 16.5 L302.3 14.3 L305.0 14.5 L304.5 12.8 L303.3 12.2 L301.8 13.0 L300.3 12.7 L299.9 11.0 L298.1 10.0 Z'
TURKEY_VIEWBOX = "0 0 620 278"
TURKEY_DOTS = [(106.2, 55.0, 'g'), (229.6, 99.1, 'g'), (48.0, 160.9, 'a'), (109.1, 88.5, 'g'), (161.2, 223.0, 'g'), (308.1, 218.9, 'a'), (218.1, 183.3, 'g'), (373.6, 216.0, 'g'), (464.2, 181.7, 'r'), (448.0, 55.4, 'g'), (340.2, 43.5, 'a'), (497.3, 100.3, 'g'), (564.3, 157.6, 'r'), (313.5, 148.2, 'g'), (155.5, 105.2, 'g'), (110.0, 187.0, 'a'), (286.2, 227.1, 'g'), (136.4, 64.8, 'g'), (59.8, 56.2, 'g'), (86.8, 210.3, 'g'), (29.6, 27.6, 'g'), (403.2, 163.7, 'a'), (418.4, 212.4, 'g'), (362.1, 106.5, 'g')]

def turkey_map():
    # Gerçek Türkiye sınırı (Natural Earth tabanlı GeoJSON'dan üretildi); noktalar örnek lokasyonlar.
    col = {"g": "#1F9D67", "a": "#D99A00", "r": "#D64545"}
    d = "".join(f'<circle cx="{x}" cy="{y}" r="6.5" fill="{col[c]}" stroke="#fff" stroke-width="2"/>' for x, y, c in TURKEY_DOTS)
    return f'<svg viewBox="{TURKEY_VIEWBOX}" role="img" aria-label="BİGEL Map"><path d="{TURKEY_PATH}" fill="#E8F1F5" stroke="#B9C9D4" stroke-width="1.5" stroke-linejoin="round"/>{d}</svg>'

def sub_product(lang, s, accent):
    logo = f'<img src="{asset(lang,"logo/"+s["logo"])}" alt="AUDIT 100" loading="lazy">' if s["logo"] else f'<div class="score" style="color:{accent};font-size:40px">EV Audit30</div>'
    w = "".join(f'<div class="w"><b>%{v}</b><div>{esc(n)}<i style="--w:{v*100//25}%"></i></div></div>' for n, v in s["weights"])
    th = "".join(f'<span class="{c}">{esc(t)}</span>' for c, t in s["thresholds"])
    b = "".join(f'<span class="badge">{esc(x)}</span>' for x in s["badges"])
    return sec(f'<div class="sub-product" id="{s["id"]}" style="--accent:{accent}"><div>{logo}<span class="eyebrow" style="color:{accent};margin-top:16px">{esc(s["eyebrow"])}</span><h2 style="font-size:clamp(26px,3vw,36px)">{esc(s["h2"])}</h2><p class="muted">{esc(s["p"])}</p><div class="badge-row">{b}</div></div><div><div class="weights">{w}</div><div class="thresholds">{th}</div></div></div>', "alt" if s["id"] == "audit100" else "")

def render_product_section(lang, s, accent):
    t = s["type"]
    if t == "split":
        img = f'<div class="photo"><img src="{asset(lang,"img/"+s["img"])}" alt="" loading="lazy"><span class="tag">{esc(s["tag"])}</span></div>'
        note = f'<p class="note" style="margin-top:18px">{esc(s["note"])}</p>' if s.get("note") else ""
        txt = f'<div>{head(s["eyebrow"], s["h2"])}<p class="lead">{esc(s["p"])}</p>{ul(s["list"], accent)}{note}</div>'
        inner = (img + txt) if s.get("reverse") else (txt + img)
        return sec(f'<div class="split">{inner}</div>')
    if t == "modules":
        items = "".join(f'<div class="module"><b>{esc(c)}</b><div><h3>{esc(h)}</h3><p>{esc(d)}</p></div></div>' for c, h, d in s["items"])
        return sec(head(s["eyebrow"], s["h2"], s.get("lead", "")) + f'<div class="modules" style="--accent:{accent}">{items}</div>', "alt")
    if t == "flow":
        return sec(head(s["eyebrow"], s["h2"]) + flow(s["steps"]))
    if t == "kpi":
        items = "".join(f'<div class="card">{esc(i)}</div>' for i in s["items"])
        return sec(head(s["eyebrow"], s["h2"]) + f'<div class="kpi">{items}</div>', "alt")
    if t == "cards3":
        items = "".join(f'<div class="card"><h3>{esc(h)}</h3><p>{esc(d)}</p></div>' for h, d in s["items"])
        note = f'<p class="note" style="margin-top:22px">{esc(s["note"])}</p>' if s.get("note") else ""
        return sec(head(s["eyebrow"], s["h2"]) + f'<div class="grid g3">{items}</div>{note}')
    if t == "table":
        th = "".join(f"<th>{esc(h)}</th>" for h in s["head"])
        rows = "".join("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in r) + "</tr>" for r in s["rows"])
        return sec(head(s["eyebrow"], s["h2"]) + f'<div class="table-wrap"><table class="table"><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table></div>', "alt")
    if t == "sub":
        return sub_product(lang, s, accent)
    if t == "map":
        leg = "".join(f'<span><i style="background:{c}"></i>{esc(t)}</span>' for c, t in s["legend"])
        k = "".join(f"<li>{esc(x)}</li>" for x in s["kpis"])
        return sec(head(s["eyebrow"], s["h2"], s["p"]) + f'<div class="map">{turkey_map()}<div><div class="legend">{leg}</div><ul class="list" style="margin-top:20px;--accent:{accent}">{k}</ul></div></div>', "alt")
    raise ValueError(t)

# ---------------------------------------------------------------- LAYOUT
def layout(lang, pid, title, desc, body, active=None):
    L = CONTENT[lang]; N = L["nav"]; F = L["footer"]
    sub = "".join(f'<li><a href="{href(lang,p)}" style="--accent:{ACCENT[p]}"><span class="dot"></span><span>{esc(L["products"][p]["name"])}<small>{esc(L["products"][p]["cat"])}</small></span></a></li>' for p in PRODUCTS)
    def a(p, label): return f'<li><a href="{href(lang,p)}"{" class=active" if active == p else ""}>{esc(label)}</a></li>'
    nav = (f'<li class="has-sub"><a href="{href(lang,"home","cozumler" if lang=="tr" else "solutions")}"{" class=active" if active in PRODUCTS else ""}>{esc(N["solutions"])}</a><ul class="sub">{sub}</ul></li>'
           + a("sectors", N["sectors"]) + a("tiers", N["tiers"]) + a("how", N["how"]) + a("pilot", N["pilot"]) + a("about", N["about"])
           + f'<li class="menu-cta"><a class="btn btn-primary" href="{href(lang,"contact")}">{esc(N["cta"])}</a></li>')
    lang_sw = (f'<span class="lang"><a class="{"on" if lang=="tr" else ""}" href="{switch_href("en",pid) if lang=="en" else "#"}" {"aria-current=page" if lang=="tr" else ""}>TR</a>'
               f'<a class="{"on" if lang=="en" else ""}" href="{switch_href("tr",pid) if lang=="tr" else "#"}">EN</a></span>')
    # fix: TR page → EN link; EN page → TR link
    if lang == "tr":
        lang_sw = f'<span class="lang"><a class="on" href="#" aria-current="page">TR</a><a href="{switch_href("tr",pid)}" hreflang="en">EN</a></span>'
    else:
        lang_sw = f'<span class="lang"><a href="{switch_href("en",pid)}" hreflang="tr">TR</a><a class="on" href="#" aria-current="page">EN</a></span>'
    tr_url = f'https://{SITE["domain"]}/{PAGES[pid][0]}'.replace("/index.html", "/")
    en_url = f'https://{SITE["domain"]}/en/{PAGES[pid][1]}'.replace("/index.html", "/")
    canonical = tr_url if lang == "tr" else en_url
    year = "2026"
    footer = (f'<footer class="footer"><div class="container"><div class="footer-grid"><div><img src="{asset(lang,"logo/bigel-white.png")}" alt="BİGEL" loading="lazy"><p><strong style="display:inline;text-transform:none;letter-spacing:0;font-size:15px">{esc(F["tagline"])}</strong></p><p>{esc(F["desc"])}</p></div>'
              f'<div><strong>{esc(F["solutions"])}</strong>' + "".join(f'<a href="{href(lang,p)}">{esc(L["products"][p]["name"])}</a>' for p in PRODUCTS) + f'<a href="{href(lang,"audit","ev")}">{esc(F["ev"])}</a></div>'
              f'<div><strong>{esc(F["company"])}</strong><a href="{href(lang,"about")}">{esc(N["about"])}</a><a href="{href(lang,"how")}">{esc(N["how"])}</a><a href="{href(lang,"sectors")}">{esc(N["sectors"])}</a><a href="{href(lang,"tiers")}">{esc(N["tiers"])}</a><a href="{href(lang,"pilot")}">{esc(N["pilot"])}</a></div>'
              f'<div><strong>{esc(F["contact"])}</strong><a href="mailto:{SITE["email"]}">{SITE["email"]}</a><a href="tel:{SITE["phone_href"]}">{SITE["phone"]}</a><a href="{SITE["linkedin"]}" target="_blank" rel="noopener">LinkedIn</a><a href="{href(lang,"contact")}">{esc(N["cta"])}</a></div></div>'
              f'<div class="bottom"><span>© {year} BİGEL · {SITE["domain"]} · {esc(F["rights"])}</span><span><a href="#">{esc(F["privacy"])}</a></span></div></div></footer>')
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="tr" href="{tr_url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="x-default" href="{tr_url}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta name="theme-color" content="#102A43">
<link rel="icon" type="image/png" href="{asset(lang,"logo/mark.png")}">
<link rel="stylesheet" href="{asset(lang,"styles.css")}">
</head>
<body>
<header class="header"><div class="container nav">
<a class="brand" href="{href(lang,"home")}"><img src="{asset(lang,"logo/bigel.png")}" alt="BİGEL — {esc(F["tagline"])}"></a>
<ul class="menu" id="menu">{nav}</ul>
<div class="nav-actions">{lang_sw}<a class="btn btn-primary btn-sm" href="{href(lang,"contact")}">{esc(N["cta"])}</a></div>
<button class="burger" aria-label="{esc(N["menu"])}" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
</div></header>
<main>
{body}
</main>
{footer}
<script src="{asset(lang,"site.js")}"></script>
</body>
</html>
'''

# ---------------------------------------------------------------- PAGES
def page_home(lang):
    L = CONTENT[lang]; H = L["home"]
    sub = "".join(f"<span><b>{esc(n)}</b>{esc(t)}</span>" for n, t in H["sub"])
    hero = (f'<section class="hero"><div class="container"><div><span class="eyebrow">{esc(H["eyebrow"])}</span><h1>{esc(H["h1"])}</h1><p class="lead">{esc(H["lead"])}</p>'
            f'<div class="btn-row"><a class="btn btn-primary" href="#{"cozumler" if lang=="tr" else "solutions"}">{esc(H["b1"])}</a><a class="btn btn-ghost" href="{href(lang,"contact")}">{esc(H["b2"])}</a></div>'
            f'</div></div></section>')
    stats = "".join(f'<div class="card stat"><div class="n">{esc(n)}</div><p>{esc(t)}</p></div>' for n, t in H["stats"])
    trust = sec(head(H["trust_eyebrow"], H["trust_h2"]) + f'<div class="grid g4">{stats}</div>')
    sol = sec(head(H["sol_eyebrow"], H["sol_h2"], H["sol_lead"]) + product_cards(lang), "alt", "cozumler" if lang == "tr" else "solutions")
    ba = "".join(f'<div class="card"><span class="date">{esc(d)}</span><h4>{esc(t)}</h4><p style="font-size:13px">{esc(s)}</p><span class="pill {c}" style="margin-top:10px">{esc(st)}</span></div>' for d, t, s, c, st in H["ba"])
    proof = sec(f'<div class="split"><div>{head(H["proof_eyebrow"], H["proof_h2"])}<p class="lead" style="color:#C9D8E6">{esc(H["proof_p"])}</p>{ul(H["proof_list"])}</div><div><div class="photo" style="margin-bottom:14px"><img src="{asset(lang,"img/tablet.jpg")}" alt="" loading="lazy"><span class="tag">{esc(H["photo_tag"])}</span></div><div class="ba">{ba}</div></div></div>', "navy")
    fl = sec(head(H["flow_eyebrow"], H["flow_h2"]) + flow(H["flow"]) + f'<p style="margin-top:22px"><a class="link" href="{href(lang,"how")}">{esc(H["flow_more"])} →</a></p>')
    secs = sec(head(H["sec_eyebrow"], H["sec_h2"]) + sector_cards(lang, 8) + f'<p style="margin-top:22px"><a class="link" href="{href(lang,"sectors")}">{esc(H["sec_more"])} →</a></p>', "alt")
    tiers = sec(head(H["tier_eyebrow"], H["tier_h2"]) + tier_cards(lang, compact=True) + f'<p style="margin-top:22px"><a class="link" href="{href(lang,"tiers")}">{esc(H["tier_more"])} →</a></p>')
    return layout(lang, "home", H["title"], H["desc"], hero + trust + sol + proof + fl + secs + tiers + cta_band(lang), "home")

def page_product(lang, pid):
    L = CONTENT[lang]; P = L["product_pages"][pid]; d = L["products"][pid]; accent = ACCENT[pid]
    hero = (f'<section class="p-hero" style="--accent:{accent}"><div class="container"><div><span class="eyebrow">{esc(d["name"])} · {esc(d["cat"])}</span><h1>{esc(d["tag"])}</h1><p class="lead">{esc(P["lead"])}</p>'
            f'<div class="btn-row"><a class="btn btn-primary" href="{href(lang,"contact")}">{esc(L["nav"]["cta"])}</a><a class="btn btn-outline" href="{href(lang,"how")}">{esc(L["nav"]["how"])}</a></div></div>'
            f'<img class="logo" src="{asset(lang,"logo/"+pid+".png")}" alt="{esc(d["name"])}"></div></section>')
    body = hero + "".join(render_product_section(lang, s, accent) for s in P["sections"]) + cta_band(lang)
    return layout(lang, pid, P["title"] + L["meta_suffix"], P["desc"], body, pid)

def simple_hero(eyebrow, h1, lead):
    return f'<section class="p-hero"><div class="container" style="grid-template-columns:1fr"><div><span class="eyebrow">{esc(eyebrow)}</span><h1>{esc(h1)}</h1><p class="lead">{esc(lead)}</p></div></div></section>'

def page_sectors(lang):
    L = CONTENT[lang]; S = L["sectors"]
    fit = "".join(f'<a class="card accent" style="--accent:{ACCENT[p]};text-decoration:none;display:block" href="{href(lang,p)}"><p style="font-size:13px;font-weight:700;color:var(--muted);margin-bottom:6px">{esc(q)}</p><h3 style="color:{ACCENT[p]};margin:0">{esc(a)} →</h3></a>' for q, a, p in S["fit"])
    body = (simple_hero(S["eyebrow"], S["h1"], S["lead"]) + sec(sector_cards(lang))
            + sec(f'<div class="split"><div>{head(S["fr_eyebrow"], S["fr_h2"])}<p class="lead">{esc(S["fr_p"])}</p>{ul(S["fr_list"])}</div><div class="photo"><img src="{asset(lang,"img/exterior.jpg")}" alt="" loading="lazy"></div></div>', "alt")
            + sec(head(S["fit_eyebrow"], S["fit_h2"]) + f'<div class="grid g3">{fit}</div>') + cta_band(lang))
    return layout(lang, "sectors", S["title"] + L["meta_suffix"], S["desc"], body, "sectors")

def page_tiers(lang):
    L = CONTENT[lang]; T = L["tiers"]
    th = "".join(f'<th{" class=center" if i else ""}>{esc(h)}</th>' for i, h in enumerate(T["cmp_head"]))
    rows = "".join("<tr>" + f"<td>{esc(r[0])}</td>" + "".join(f'<td class="center">{"<span style=color:var(--teal);font-weight:800>✓</span>" if v else "<span style=color:#B7C7D6>—</span>"}</td>' for v in r[1:]) + "</tr>" for r in T["cmp_rows"])
    body = (simple_hero(T["eyebrow"], T["h1"], T["lead"]) + sec(tier_cards(lang))
            + sec(head("", T["cmp_h2"]) + f'<div class="table-wrap"><table class="table"><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table></div><p class="note" style="margin-top:22px">{esc(T["note"])}</p>', "alt")
            + cta_band(lang))
    return layout(lang, "tiers", T["title"] + L["meta_suffix"], T["desc"], body, "tiers")

def page_how(lang):
    L = CONTENT[lang]; H = L["how"]
    steps = "".join(f'<div class="card"><span class="eyebrow">{i+1:02d}</span><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for i, (t, d) in enumerate(H["steps"]))
    tl = "".join(f'<div class="card"><span class="when">{esc(w)}</span><h3>{esc(t)}</h3><ul>' + "".join(f"<li>{esc(x)}</li>" for x in items) + "</ul></div>" for w, t, items in H["timeline"])
    scale = "".join(f'<div class="card"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t, d in H["scale"])
    body = (simple_hero(H["eyebrow"], H["h1"], H["lead"])
            + sec(head(H["steps_eyebrow"], H["steps_h2"]) + f'<div class="grid g3">{steps}</div>')
            + sec(head(H["tl_eyebrow"], H["tl_h2"]) + f'<div class="timeline">{tl}</div>', "alt")
            + sec(f'<div class="split"><div>{head(H["q_eyebrow"], H["q_h2"])}{ul(H["quality"])}</div><div>{head(H["r_eyebrow"], H["r_h2"])}{ul(H["report"])}</div></div>')
            + sec(head(H["s_eyebrow"], H["s_h2"]) + f'<div class="grid g3">{scale}</div>', "alt") + cta_band(lang))
    return layout(lang, "how", H["title"] + L["meta_suffix"], H["desc"], body, "how")

def page_about(lang):
    L = CONTENT[lang]; A = L["about"]
    facts = "".join(f'<div class="card stat"><div class="n">{esc(n)}</div><p>{esc(t)}</p></div>' for n, t in A["facts"])
    story = "".join(f"<p>{esc(p)}</p>" for p in A["story"])
    values = "".join(f'<div class="value"><div class="ic">{icon(ic)}</div><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t, d, ic in A["values"])
    ch = "".join(f'<div class="card"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t, d in A["character"])
    regs = "".join(f'<span class="badge">{esc(r)}</span>' for r in A["regions"])
    body = (simple_hero(A["eyebrow"], A["h1"], A["lead"])
            + sec(f'<div class="split"><div><h2>{esc(A["story_h2"])}</h2>{story}</div><div class="photo"><img src="{asset(lang,"img/exterior.jpg")}" alt="" loading="lazy"></div></div><div class="grid g4" style="margin-top:48px">{facts}</div>')
            + sec(head(A["v_eyebrow"], A["v_h2"]) + f'<div class="value-grid">{values}</div>', "alt")
            + sec(head(A["c_eyebrow"], A["c_h2"]) + f'<div class="grid g3">{ch}</div>')
            + sec(f'<div class="split"><div>{head(A["reg_eyebrow"], A["reg_h2"])}<p class="lead">{esc(A["reg_p"])}</p><div class="badge-row">{regs}</div></div><div class="photo"><img src="{asset(lang,"img/station.jpg")}" alt="" loading="lazy"></div></div>', "alt")
            + cta_band(lang))
    return layout(lang, "about", A["title"], A["desc"], body, "about")

def page_contact(lang):
    L = CONTENT[lang]; C = L["contact"]; f = C["f"]
    next_url = f'https://{SITE["domain"]}/' + ("" if lang == "tr" else "en/") + PAGES["thanks"][0 if lang == "tr" else 1]
    counts = "".join(f"<option>{esc(c)}</option>" for c in f["counts"])
    sols = "".join(f"<option>{esc(c)}</option>" for c in f["solutions"])
    form = (f'<form class="form" action="https://formsubmit.co/{SITE["email"]}" method="POST">'
            f'<input type="hidden" name="_subject" value="{esc(f["subject"])}"><input type="hidden" name="_template" value="table"><input type="hidden" name="_captcha" value="false"><input type="hidden" name="_next" value="{next_url}"><input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">'
            f'<div class="row"><div><label for="name">{esc(f["name"])}</label><input id="name" name="{f["name"]}" required></div><div><label for="company">{esc(f["company"])}</label><input id="company" name="{f["company"]}" required></div></div>'
            f'<div class="row"><div><label for="email">{esc(f["email"])}</label><input id="email" type="email" name="{f["email"]}" required></div><div><label for="phone">{esc(f["phone"])}</label><input id="phone" type="tel" name="{f["phone"]}"></div></div>'
            f'<div class="row"><div><label for="count">{esc(f["count"])}</label><select id="count" name="{f["count"]}">{counts}</select></div><div><label for="sol">{esc(f["solution"])}</label><select id="sol" name="{f["solution"]}">{sols}</select></div></div>'
            f'<label for="msg">{esc(f["msg"])}</label><textarea id="msg" name="{f["msg"]}" placeholder="{esc(f["msg_ph"])}"></textarea>'
            f'<label class="consent"><input type="checkbox" required><span>{esc(f["consent"])}</span></label>'
            f'<button class="btn btn-primary" type="submit">{esc(f["send"])}</button></form>')
    info = "".join(f'<div class="card"><b>{esc(t)}</b><p>{esc(v)}</p></div>' for t, v in C["info"])
    body = simple_hero(C["eyebrow"], C["h1"], C["lead"]) + sec(f'<div class="split" style="align-items:start">{form}<div class="contact-info">{info}</div></div>', "alt")
    return layout(lang, "contact", C["title"] + L["meta_suffix"], C["desc"], body, "contact")

def page_pilot(lang):
    L = CONTENT[lang]; P = L["pilot"]; f = P["f"]
    stats = "".join(f'<div class="card stat"><div class="n">{esc(n)}</div><p>{esc(t)}</p></div>' for n, t in P["stats"])
    why = "".join(f'<div class="card"><h3>{esc(h)}</h3><p>{esc(d)}</p></div>' for h, d in P["why"])
    steps = "".join(f'<div class="card"><span class="eyebrow">{i+1:02d}</span><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for i, (t, d) in enumerate(P["steps"]))
    prod = "".join(f'<a class="card accent" style="--accent:{ACCENT[pid]};text-decoration:none;display:block" href="{href(lang,pid)}"><span class="kicker" style="font-size:12px;font-weight:800;letter-spacing:.1em;color:{ACCENT[pid]}">{esc(L["products"][pid]["name"])}</span><h3 style="margin-top:8px">{esc(t)}</h3><p>{esc(d)}</p></a>' for pid, t, d in P["prod"])
    next_url = f'https://{SITE["domain"]}/' + ("" if lang == "tr" else "en/") + PAGES["thanks"][0 if lang == "tr" else 1]
    opt = lambda xs: "".join(f"<option>{esc(x)}</option>" for x in xs)
    form = (f'<form class="form" action="https://formsubmit.co/{SITE["email"]}" method="POST">'
            f'<input type="hidden" name="_subject" value="{esc(f["subject"])}"><input type="hidden" name="_template" value="table"><input type="hidden" name="_captcha" value="false"><input type="hidden" name="_next" value="{next_url}"><input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">'
            f'<div class="row"><div><label for="name">{esc(f["name"])}</label><input id="name" name="{f["name"]}" required></div><div><label for="company">{esc(f["company"])}</label><input id="company" name="{f["company"]}" required></div></div>'
            f'<div class="row"><div><label for="email">{esc(f["email"])}</label><input id="email" type="email" name="{f["email"]}" required></div><div><label for="phone">{esc(f["phone"])}</label><input id="phone" type="tel" name="{f["phone"]}"></div></div>'
            f'<div class="row"><div><label for="sector">{esc(f["sector"])}</label><select id="sector" name="{f["sector"]}">{opt(f["sectors"])}</select></div><div><label for="count">{esc(f["count"])}</label><select id="count" name="{f["count"]}">{opt(f["counts"])}</select></div></div>'
            f'<label for="geo">{esc(f["geo"])}</label><input id="geo" name="{f["geo"]}" placeholder="{esc(f["geo_ph"])}">'
            f'<div class="row"><div><label for="product">{esc(f["product"])}</label><select id="product" name="{f["product"]}">{opt(f["products"])}</select></div><div><label for="start">{esc(f["start"])}</label><select id="start" name="{f["start"]}">{opt(f["starts"])}</select></div></div>'
            f'<label for="msg">{esc(f["msg"])}</label><textarea id="msg" name="{f["msg"]}" placeholder="{esc(f["msg_ph"])}"></textarea>'
            f'<label class="consent"><input type="checkbox" required><span>{esc(f["consent"])}</span></label>'
            f'<button class="btn btn-primary" type="submit">{esc(f["send"])}</button></form>')
    after = "".join(f'<div class="card" style="padding:18px 20px"><span class="eyebrow">{esc(n)}</span><h4 style="margin:2px 0 4px">{esc(t)}</h4><p style="font-size:14px">{esc(d)}</p></div>' for n, t, d in P["after"])
    body = (simple_hero(P["eyebrow"], P["h1"], P["lead"]) + sec(f'<div class="grid g4">{stats}</div>')
            + sec(head(P["why_eyebrow"], P["why_h2"]) + f'<div class="grid g3">{why}</div>', "alt")
            + sec(head(P["steps_eyebrow"], P["steps_h2"]) + f'<div class="grid g3">{steps}</div>')
            + sec(f'<div class="split"><div>{head(P["out_eyebrow"], P["out_h2"])}{ul(P["outputs"])}</div><div class="photo"><img src="{asset(lang,"img/tablet.jpg")}" alt="" loading="lazy"><span class="tag">{esc(P["photo_tag"])}</span></div></div>', "alt")
            + sec(head(P["prod_eyebrow"], P["prod_h2"]) + f'<div class="grid g4">{prod}</div>')
            + sec(head(P["form_eyebrow"], P["form_h2"], P["form_lead"]) + f'<div class="split" style="align-items:start">{form}<div class="contact-info"><h3 style="margin:0 0 4px">{esc(P["after_h3"])}</h3>{after}<p class="note">{esc(P["note"])}</p></div></div>', "alt", "basvuru" if lang == "tr" else "apply"))
    return layout(lang, "pilot", P["title"] + L["meta_suffix"], P["desc"], body, "pilot")

def page_thanks(lang):
    L = CONTENT[lang]; T = L["thanks"]
    body = sec(f'<div class="center" style="padding:40px 0"><span class="eyebrow">BİGEL</span><h1 style="font-size:clamp(32px,4vw,52px)">{esc(T["h1"])}</h1><p class="lead" style="margin-inline:auto">{esc(T["p"])}</p><div class="btn-row" style="justify-content:center"><a class="btn btn-primary" href="{href(lang,"home")}">{esc(T["b"])}</a></div></div>')
    return layout(lang, "thanks", T["title"] + L["meta_suffix"], T["p"], body)

# ---------------------------------------------------------------- BUILD
def build():
    js = """document.querySelector('.burger').addEventListener('click',function(){var m=document.getElementById('menu');var o=m.classList.toggle('open');this.setAttribute('aria-expanded',o);});
document.querySelectorAll('.has-sub>a').forEach(function(a){a.addEventListener('click',function(e){if(window.innerWidth<=840){/* mobile: let the link work, submenu is already expanded */}});});"""
    with open(os.path.join(ROOT, "assets", "site.js"), "w") as fh: fh.write(js)
    n = 0
    for lang in ("tr", "en"):
        outdir = ROOT if lang == "tr" else os.path.join(ROOT, "en")
        os.makedirs(outdir, exist_ok=True)
        pages = {"home": page_home(lang), "sectors": page_sectors(lang), "tiers": page_tiers(lang), "how": page_how(lang), "about": page_about(lang), "contact": page_contact(lang), "pilot": page_pilot(lang), "thanks": page_thanks(lang)}
        for p in PRODUCTS: pages[p] = page_product(lang, p)
        for pid, html_ in pages.items():
            with open(os.path.join(outdir, PAGES[pid][0 if lang == "tr" else 1]), "w", encoding="utf-8") as fh: fh.write(html_)
            n += 1
    # robots + sitemap
    urls = [f'https://{SITE["domain"]}/{PAGES[p][0]}' for p in PAGES if p != "thanks"] + [f'https://{SITE["domain"]}/en/{PAGES[p][1]}' for p in PAGES if p != "thanks"]
    urls = [u.replace("/index.html", "/") for u in urls]
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    with open(os.path.join(ROOT, "robots.txt"), "w") as fh:
        fh.write(f"User-agent: *\nAllow: /\nSitemap: https://{SITE['domain']}/sitemap.xml\n")
    print(f"built {n} pages")

if __name__ == "__main__":
    build()
