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

SECTOR_ICONS = ["fuel", "food", "retail", "bank", "auto", "logistics", "mall", "hotel", "ev", "telecom", "edu", "factory"]

# ---------------------------------------------------------------- CONTENT
CONTENT = {
"tr": {
  "meta_suffix": " | BİGEL",
  "nav": {"solutions": "Çözümler", "sectors": "Sektörler", "tiers": "Abonelikler", "how": "Nasıl Çalışıyoruz", "about": "Hakkımızda", "cta": "Teklif Al", "menu": "Menü"},
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
    ("Restoran & Fast Food", "Cephe, cam, tabela, dış oturma ve arabaya servis alanı."),
    ("Perakende & Mağazacılık", "Vitrin, görsel alan, mobilya, giriş ve mağaza çevresi."),
    ("Bankacılık", "Şube girişi, ATM kabini, cam ve cephe, banko ve seperatörler."),
    ("Otomotiv", "Showroom camı, tabela, araç sergileme alanı ve otopark."),
    ("Lojistik & Depo", "Saha girişi, yükleme alanı, zemin çizgileri ve bariyerler."),
    ("AVM & Plaza", "Ortak dış alanlar, yönlendirme, kolon kaplamaları ve otopark."),
    ("Otel & Turizm", "Giriş, cephe, peyzaj elemanları ve havuz çevresi mobilyası."),
    ("EV Şarj İstasyonları", "Cihaz çevresi, kablo düzeni, park cebi ve yönlendirme. Audit30 ile skorlanır."),
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
        {"type": "cards3", "eyebrow": "Önleyici bakım programı", "h2": "Arızaya dönüşmeden tespit edin.", "items": [("Mart · İlkbahar kontrolü", "Kış hasarı, zemin, bordür ve dış alan elemanları."), ("Haziran · Yaz kontrolü", "Tente, şemsiye, dış oturma ve aydınlatma dış gövdesi."), ("Eylül · Sonbahar kontrolü", "Tabela, totem, cephe ve yönlendirme elemanları."), ("Aralık · Kış kontrolü", "Kaygan zemin riski, bariyer, kapı ve giriş elemanları."), ("Her ziyarette", "Standart kontrol listesi, fotoğraflı kayıt, risk ve öncelik sınıflandırması."), ("Sonuç", "Yerinde küçük müdahale, iş emri gerektiren bulguların raporu, aksiyon ve kapanış takibi.")]},
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
        {"type": "sub", "id": "ev", "logo": None, "eyebrow": "Şarj ağları için", "h2": "EV Audit30 — Şarj noktası saha kalite denetimi.",
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
  "thanks": {"title": "Teşekkürler", "h1": "Talebiniz alındı.", "p": "Ekibimiz aynı iş günü içinde sizinle iletişime geçecek. Bu arada çözümlerimizi inceleyebilirsiniz.", "b": "Ana sayfaya dön"},
},
"en": {
  "meta_suffix": " | BİGEL",
  "nav": {"solutions": "Solutions", "sectors": "Industries", "tiers": "Plans", "how": "How We Work", "about": "About", "cta": "Get a Quote", "menu": "Menu"},
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
    ("Restaurants & QSR", "Façade, glass, signage, outdoor seating and drive-thru."),
    ("Retail", "Shopfront, visual areas, furniture, entrance and store surroundings."),
    ("Banking", "Branch entrance, ATM cabin, glass and façade, counters and partitions."),
    ("Automotive", "Showroom glass, signage, display areas and car park."),
    ("Logistics & Warehousing", "Site entrance, loading areas, floor markings and barriers."),
    ("Shopping Malls & Plazas", "Common outdoor areas, wayfinding, column cladding and car park."),
    ("Hotels & Tourism", "Entrance, façade, landscape elements and poolside furniture."),
    ("EV Charging Stations", "Charger surroundings, cable management, bays and wayfinding. Scored with Audit30."),
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
        {"type": "cards3", "eyebrow": "Preventive maintenance", "h2": "Detect it before it becomes a fault.", "items": [("March · Spring check", "Winter damage, floors, kerbs and outdoor elements."), ("June · Summer check", "Awnings, umbrellas, outdoor seating and light fittings."), ("September · Autumn check", "Signage, totems, façade and wayfinding."), ("December · Winter check", "Slip risk, barriers, doors and entrance elements."), ("Every visit", "Standard checklist, photo record, risk and priority classification."), ("Outcome", "On-the-spot minor fixes, work orders for larger findings, action and closure tracking.")]},
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
        {"type": "sub", "id": "ev", "logo": None, "eyebrow": "For charging networks", "h2": "EV Audit30 — Charging point field quality audit.",
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
    return sec(f'<div class="cta-band"><div><h2>{esc(L["h2"])}</h2><p>{esc(L["p"])}</p></div><div class="btn-row"><a class="btn btn-primary" href="{href(lang,"contact")}">{esc(L["b1"])}</a><a class="btn btn-ghost" href="{href(lang,"contact")}">{esc(L["b2"])}</a></div></div>')

def scorecard(lang):
    c = CONTENT[lang]["home"]["card"]
    bars = "".join(f'<div class="bar"><span>{esc(n)}</span><span>{v}</span><i style="--w:{v}%;--c:{col}"></i></div>' for n, v, col in c["bars"])
    return (f'<div class="scorecard"><div class="top"><div class="loc">{esc(c["loc"])}<small>{esc(c["meta"])}</small></div>'
            f'<div><div class="score">87<small>/100</small></div><span class="pill amber">{esc(c["status"])}</span></div></div>'
            f'<div class="bars">{bars}</div><div class="foot"><span>{c["foot_l"]}</span><span>{esc(c["foot_r"])}</span></div></div>')

def turkey_map():
    # Temsili harita: ülke silüeti sadeleştirilmiş, noktalar örnek lokasyonlar.
    dots = [(120,120,"g"),(150,105,"g"),(175,140,"a"),(95,150,"g"),(215,95,"g"),(260,150,"a"),(300,120,"g"),(330,175,"r"),(360,100,"g"),(400,140,"g"),(430,95,"a"),(470,130,"g"),(500,165,"g"),(540,120,"r"),(230,200,"g"),(380,205,"a"),(140,190,"g"),(455,190,"g")]
    col = {"g": "#1F9D67", "a": "#D99A00", "r": "#D64545"}
    d = "".join(f'<circle cx="{x}" cy="{y}" r="7" fill="{col[c]}" stroke="#fff" stroke-width="2"/>' for x, y, c in dots)
    path = "M40 130 C60 85 120 70 180 78 C230 62 262 44 300 58 C342 46 400 42 452 62 C504 56 562 72 582 112 C592 152 562 192 520 202 C472 232 420 222 380 242 C332 252 282 232 240 237 C190 247 130 232 92 212 C52 192 30 152 40 130 Z"
    return f'<svg viewBox="0 0 620 280" role="img" aria-label="BİGEL Map"><path d="{path}" fill="#E8F1F5" stroke="#C9D6E0" stroke-width="2"/>{d}</svg>'

def sub_product(lang, s, accent):
    logo = f'<img src="{asset(lang,"logo/"+s["logo"])}" alt="AUDIT 100" loading="lazy">' if s["logo"] else f'<div class="score" style="color:{accent}">30<small>/100</small></div>'
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
           + a("sectors", N["sectors"]) + a("tiers", N["tiers"]) + a("how", N["how"]) + a("about", N["about"])
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
              f'<div><strong>{esc(F["company"])}</strong><a href="{href(lang,"about")}">{esc(N["about"])}</a><a href="{href(lang,"how")}">{esc(N["how"])}</a><a href="{href(lang,"sectors")}">{esc(N["sectors"])}</a><a href="{href(lang,"tiers")}">{esc(N["tiers"])}</a></div>'
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
        pages = {"home": page_home(lang), "sectors": page_sectors(lang), "tiers": page_tiers(lang), "how": page_how(lang), "about": page_about(lang), "contact": page_contact(lang), "thanks": page_thanks(lang)}
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
