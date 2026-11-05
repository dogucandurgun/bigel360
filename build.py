#!/usr/bin/env python3
# BİGEL — bigel360.com static site generator.
# Run:  python3 build.py   → writes TR pages to ./ and EN pages to ./en/
# All copy lives in this file (CONTENT). Mock company facts are in SITE.
import os, html

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- SITE DATA
# E-posta, telefon ve adres doğrulandı (2026-10-19). Kuruluş yılı ve rakamlar (bölge, ziyaret, oran) henüz doğrulanmadı.
SITE = {
    "domain": "bigel360.com",
    "email": "info@bigel360.com",
    "phone": "+90 532 293 22 33",
    "phone_href": "+905322932233",
    # Address parts: the same text is used in the JSON-LD, the footer and the contact page (NAP consistency
    # with the Google Business Profile "BİGEL360"). address_tr is built from these parts below.
    "street": "Bağlarbaşı Mah. İncilik Sok. No:1 B Blok D:2",
    "postal_code": "34844",
    "locality": "Maltepe",
    "region": "İstanbul",
    "country": "TR",
    "linkedin": "https://www.linkedin.com/company/bigel360",
    "founded": "2018",
    "regions": "60",
    "provinces": "81",
    "visits": "1.200+",
    "photo_rate": "%98",
    "photo_rate_en": "98%",
    # BİGEL yazılımının giriş sayfası (Operasyon Merkezi + müşteri portalı). Şimdilik yerel geliştirme
    # adresi: canlıya geçince panelin gerçek adresiyle değiştirilmeli (ör. https://panel.<alan-adı>/giris).
    # BİGEL yazılımının giriş sayfası (Operasyon Merkezi + müşteri portalı). Alan adı bağlanınca
    # (ör. https://panel.bigel360.com/giris) burası güncellenecek. Boşken buton "Portal yakında" sayfasına gider.
    "portal_url": "https://panel.bigel360.com/giris",
    # Teklif ve pilot formları buraya gider; talepler panelde Merkez > Site Talepleri'nde görünür.
    "form_url": "https://panel.bigel360.com/api/site-talep",
}
SITE["address_tr"] = f'{SITE["street"]}, {SITE["postal_code"]} {SITE["locality"]} / {SITE["region"]}'
SITE["address_en"] = SITE["address_tr"]  # one address text on every page, identical to the JSON-LD
SHOW_PORTAL = True

def org_ld(lang):
    """The company entity, the same on every page: Organization + LocalBusiness (ProfessionalService) under
    one @id that WebSite, Service and Article nodes point to. Name, address and phone match the footer
    and the contact page character for character."""
    base = f'https://{SITE["domain"]}'
    return {"@type": ["Organization", "ProfessionalService"], "@id": base + "/#organization", "name": "BİGEL",
            "alternateName": ["BİGEL360", "BİGEL 360", "bigel360.com"], "url": base + "/",
            "logo": {"@type": "ImageObject", "@id": base + "/#logo", "url": base + "/assets/icons/icon-512.png", "width": 512, "height": 512, "caption": "BİGEL"},
            "image": base + "/assets/icons/og-image.jpg", "description": CONTENT[lang]["home"]["desc"],
            "email": SITE["email"], "telephone": SITE["phone"],
            "address": {"@type": "PostalAddress", "streetAddress": SITE["street"], "postalCode": SITE["postal_code"],
                        "addressLocality": SITE["locality"], "addressRegion": SITE["region"], "addressCountry": SITE["country"]},
            "areaServed": {"@type": "Country", "name": "Türkiye"},
            "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "18:00"}],
            "sameAs": [SITE["linkedin"]],
            "contactPoint": [{"@type": "ContactPoint", "contactType": "sales", "email": SITE["email"], "telephone": SITE["phone"], "areaServed": "TR", "availableLanguage": ["Turkish", "English"]}]}

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
    # Sector landing pages (fuel and EV charging stations); copy in CONTENT[lang]["landings"].
    "fuel_clean": ("akaryakit-istasyonu-temizligi.html", "fuel-station-cleaning.html"),
    "fuel_audit": ("akaryakit-istasyonu-denetimi.html", "fuel-station-audit.html"),
    "ev_care": ("sarj-istasyonu-bakimi.html", "ev-charging-station-maintenance.html"),
    "ev_audit": ("sarj-istasyonu-denetimi.html", "ev-charging-station-audit.html"),
    "retail": ("zincir-magaza-temizligi-bakimi.html", "retail-store-cleaning-maintenance.html"),
    "bank": ("banka-subesi-atm-temizligi.html", "bank-branch-atm-cleaning.html"),
    "restaurant": ("restoran-zinciri-dis-alan-temizligi.html", "restaurant-chain-exterior-cleaning.html"),
    # Guides (Rehber): index + articles; copy in CONTENT[lang]["guides"].
    "guides": ("rehber.html", "guides.html"),
    "g_canopy": ("rehber-kanopi-temizligi.html", "guide-fuel-station-canopy-cleaning.html"),
    "g_ev": ("rehber-sarj-istasyonu-kontrol-listesi.html", "guide-ev-charging-station-checklist.html"),
    "g_fuel_audit": ("rehber-akaryakit-istasyonu-denetim-kriterleri.html", "guide-fuel-station-audit-criteria.html"),
    "g_sign": ("rehber-totem-tabela-temizligi.html", "guide-pylon-sign-cleaning.html"),
    # KVKK notice: draft awaiting legal review, built with noindex and kept out of the sitemap.
    "kvkk": ("kvkk.html", "privacy.html"),
    "thanks": ("tesekkurler.html", "thank-you.html"),
    "portal": ("portal.html", "portal.html"),
    # Not-found page: GitHub Pages serves /404.html for any missing URL. Built in Turkish only (with an
    # English line); its EN counterpart is the EN home page. noindex, out of the sitemap.
    "notfound": ("404.html", "index.html"),
}
PRODUCTS = ["clean", "care", "audit", "field360"]
ACCENT = {"clean": "var(--clean)", "care": "var(--care)", "audit": "var(--audit)", "field360": "var(--field)",
          "fuel_clean": "var(--clean)", "fuel_audit": "var(--audit)", "ev_care": "var(--care)", "ev_audit": "var(--audit)",
          "retail": "var(--clean)", "bank": "var(--care)", "restaurant": "var(--clean)"}
LANDINGS = ["fuel_clean", "fuel_audit", "ev_care", "ev_audit", "retail", "bank", "restaurant"]
LANDING_ICON = {"fuel_clean": "fuel", "fuel_audit": "fuel", "ev_care": "ev", "ev_audit": "ev", "retail": "retail", "bank": "bank", "restaurant": "food"}
GUIDES = ["g_canopy", "g_fuel_audit", "g_ev", "g_sign"]
# Related pages shown at the bottom of each landing page (sibling sector pages first, then products).
LANDING_RELATED = {"fuel_clean": ["fuel_audit", "ev_care", "clean", "care"], "fuel_audit": ["fuel_clean", "ev_audit", "audit", "care"],
                   "ev_care": ["ev_audit", "fuel_clean", "care", "clean"], "ev_audit": ["ev_care", "fuel_audit", "audit", "field360"],
                   "retail": ["restaurant", "bank", "clean", "audit"], "bank": ["retail", "restaurant", "clean", "care"],
                   "restaurant": ["retail", "bank", "clean", "care"]}
# "Related guides" block on each landing page, and related pages at the bottom of each guide.
LANDING_GUIDES = {"fuel_clean": ["g_canopy", "g_sign", "g_fuel_audit"], "fuel_audit": ["g_fuel_audit", "g_canopy"], "ev_care": ["g_ev"], "ev_audit": ["g_ev"],
                  "retail": ["g_sign"], "bank": ["g_sign"], "restaurant": ["g_sign"]}
# In-copy link from each landing page to its main guide: (guide, TR anchor, EN anchor).
LANDING_GUIDE_LINK = {"fuel_clean": ("g_canopy", "Kanopi ne sıklıkla temizlenmeli?", "How often to clean a canopy"),
                      "fuel_audit": ("g_fuel_audit", "Denetim kriterleri ve kontrol listesi", "Audit criteria and checklist"),
                      "ev_care": ("g_ev", "Şarj istasyonu kontrol listesi", "EV charging station checklist"),
                      "ev_audit": ("g_ev", "Şarj istasyonu kontrol listesi", "EV charging station checklist"),
                      "retail": ("g_sign", "Totem ve tabela temizliği rehberi", "Pylon and sign cleaning guide"),
                      "bank": ("g_sign", "Totem ve tabela temizliği rehberi", "Pylon and sign cleaning guide"),
                      "restaurant": ("g_sign", "Totem ve tabela temizliği rehberi", "Pylon and sign cleaning guide")}
GUIDE_RELATED = {"g_canopy": ["fuel_clean", "fuel_audit", "g_fuel_audit", "g_sign"], "g_fuel_audit": ["fuel_audit", "fuel_clean", "g_canopy", "audit"],
                 "g_ev": ["ev_audit", "ev_care", "audit", "care"], "g_sign": ["fuel_clean", "retail", "restaurant", "bank"]}
# Sector cards that open a landing page: index in sectors_list -> (main page[, second link]).
SECTOR_LINKS = {0: ("fuel_clean", "fuel_audit"), 1: ("ev_care", "ev_audit"), 2: ("restaurant",), 3: ("retail",), 4: ("bank",)}

def href(lang, pid, anchor=""):
    f = PAGES[pid][0 if lang == "tr" else 1]
    return f + (("#" + anchor) if anchor else "")

def asset(lang, path):
    return ("assets/" if lang == "tr" else "../assets/") + path

def versioned(lang, path):
    """The asset's link with a fingerprint of its content, so browsers fetch a changed file at once
    instead of keeping an old copy from their cache."""
    import hashlib
    with open(os.path.join(ROOT, "assets", path), "rb") as fh:
        return asset(lang, path) + "?v=" + hashlib.md5(fh.read()).hexdigest()[:8]

# Intrinsic pixel sizes of the site images, written as width/height on <img> so the browser reserves the space
# before the file loads (no layout shift). CSS keeps height:auto, so the rendered size does not change.
IMG_SIZE = {"logo/audit.png": (520, 388), "logo/audit100.png": (520, 355), "logo/bigel-white.png": (520, 174), "logo/bigel.png": (520, 174),
            "logo/care.png": (520, 357), "logo/clean.png": (520, 345), "logo/field360.png": (520, 357),
            "logo/tier-basic.jpg": (600, 386), "logo/tier-pro.jpg": (600, 386), "logo/tier-business.jpg": (600, 386), "logo/tier-360.jpg": (600, 386),
            "img/exterior.jpg": (1400, 933), "img/hero.jpg": (1600, 900), "img/retail.jpg": (1400, 933), "img/station.jpg": (1400, 788), "img/tablet.jpg": (1400, 788)}

def img(lang, path, alt, cls="", lazy=True, priority=False):
    """<img> with its intrinsic size. lazy: below the fold (loading=lazy, decoding=async); priority: the
    above-the-fold logo/hero image (fetchpriority=high). When scripts/make_webp.py has written a smaller
    .webp copy, it is offered through <picture> and the PNG/JPG stays as the fallback (picture is
    display:contents in the CSS, so the layout is the same as a bare <img>)."""
    w, h = IMG_SIZE[path]
    tag = (f'<img{f" class={chr(34)}{cls}{chr(34)}" if cls else ""} src="{asset(lang, path)}" alt="{html.escape(alt)}" width="{w}" height="{h}"'
           + (' loading="lazy" decoding="async"' if lazy else "") + (' fetchpriority="high"' if priority else "") + ">")
    webp = os.path.splitext(path)[0] + ".webp"
    if os.path.exists(os.path.join(ROOT, "assets", webp)):
        return f'<picture><source type="image/webp" srcset="{asset(lang, webp)}">{tag}</picture>'
    return tag

def logo_alt(lang, name):
    return f"{name} logosu" if lang == "tr" else f"{name} logo"

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
  "nav": {"solutions": "Çözümler", "sectors": "Sektörler", "tiers": "Abonelikler", "how": "Nasıl Çalışıyoruz", "pilot": "Pilot Başvurusu", "about": "Hakkımızda", "cta": "Teklif Al", "menu": "Menü", "portal": "Portal Girişi"},
  "products": {
    "clean":    {"name": "BİGEL CLEAN", "cat": "Temizlik Operasyonları", "tag": "Standart her noktada aynı.", "short": "Kanopi, tabela, totem, cephe ve otopark için planlı dış alan temizliği. Öncesi ve sonrası fotoğrafla doğrulanır."},
    "care":     {"name": "BİGEL CARE", "cat": "Bakım Operasyonları", "tag": "Arızayı beklemeden, sahayı koruyun.", "short": "Küçük bakım, onarım ve saha müdahalesi. Tespitten fotoğraflı kapanışa tek iş emri akışı."},
    "audit":    {"name": "BİGEL AUDIT", "cat": "Denetim & Kalite", "tag": "Sahadaki standardınızı görün.", "short": "Marka, görsel, temizlik, fiziksel durum ve müşteri deneyimi denetimi. AUDIT 100 ve EV Audit30 ile skorlanır."},
    "field360": {"name": "BİGEL FIELD360", "cat": "Saha Yönetim Platformu", "tag": "Sahanın tamamı tek merkezde.", "short": "Temizlik, bakım, denetim ve aksiyonu tek sözleşme, tek standart ve tek raporlamada birleştirir."},
  },
  "more": "Çözümü Gör",
  "ui": {"home": "Ana Sayfa", "faq_eyebrow": "SSS", "faq_h2": "Sıkça sorulan sorular", "rel_eyebrow": "İlgili sayfalar", "rel_h2": "Konuyla ilgili diğer sayfalar", "crumb_label": "Sayfa konumu",
         "guides": "Rehber", "guides_eyebrow": "Rehber", "guides_h2": "İlgili rehberler", "published": "Yayın tarihi", "by": "Hazırlayan: BİGEL",
         "short": {"fuel_clean": "Temizlik ve bakım", "fuel_audit": "Denetim · AUDIT 100", "ev_care": "Bakım ve temizlik", "ev_audit": "Denetim · EV Audit30"},
         "footer": {"fuel_clean": "Akaryakıt istasyonu temizliği", "fuel_audit": "Akaryakıt istasyonu denetimi", "ev_care": "Şarj istasyonu bakımı", "ev_audit": "Şarj istasyonu denetimi"}},
  "footer": {"tagline": "Sahadaki Gücünüz.", "desc": "Kurumsal Saha Operasyonları ve Hizmet Platformu. Çok lokasyonlu markalar için Türkiye genelinde temizlik, bakım, denetim ve saha operasyon yönetimi.", "solutions": "Çözümler", "company": "Şirket", "contact": "İletişim", "ev": "EV Audit30", "rights": "Tüm hakları saklıdır.", "privacy": "KVKK ve Gizlilik"},
  "cta": {"h2": "Saha operasyonunuzu birlikte tasarlayalım.", "p": "Pilot kapsamını seçili lokasyonlarla başlatır, sonuçlara göre bölgesel ve Türkiye geneli operasyona ölçekleriz.", "b1": "Pilot Başlat", "b2": "İletişim"},
  "sectors_list": [
    ("Akaryakıt İstasyonları", "Kanopi, totem, pompa adası, otopark ve saha çevresi."),
    ("Elektrikli Araç (EV) Şarj İstasyonları", "Cihaz çevresi, kablo düzeni, park cebi ve yönlendirme. Audit30 ile skorlanır."),
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
     ["BUSINESS'ın tamamı", "FIELD360 tek operasyon merkezi", "Görsel alan ve mobilya yönetimi", "Atanmış operasyon yöneticisi"]),
  ],
  "home": {
    "title": "Akaryakıt, Şarj ve Zincir Markalar İçin Saha Operasyonu | BİGEL",
    "desc": "Akaryakıt ve elektrikli araç şarj istasyonu ağları ile çok lokasyonlu markalar için Türkiye genelinde temizlik, bakım ve denetim. Fotoğraflı kanıt ve skor.",
    "eyebrow": "Kurumsal Saha Operasyonları",
    "h1": "Sahadaki Gücünüz.",
    "lead": "Çok lokasyonlu markaların temizlik, bakım ve denetim operasyonlarını Türkiye genelinde tek standartla planlıyor, uyguluyor ve fotoğraflı kanıtla raporluyoruz.",
    "b1": "Çözümleri İncele", "b2": "Teklif Al",
    "sub": [("81", "ile erişim"), ("4", "ürün, tek standart"), ("100", "kriterli dijital denetim")],
    "card": {"loc": "Örnek Lokasyon · Kadıköy / İstanbul", "meta": "Denetim 12.09.2026 · Ekip MAR-04", "status": "Aksiyon gerekli",
             "bars": [("Temizlik", 94, "var(--green)"), ("Marka standardı", 89, "var(--amber)"), ("Müşteri deneyimi", 91, "var(--green)"), ("Teknik durum", 72, "var(--red)"), ("İş güvenliği", 100, "var(--green)")],
             "foot_l": "3 açık bulgu · <b>1 kritik</b>", "foot_r": "İş emri oluşturuldu"},
    "trust_eyebrow": "Neden BİGEL", "trust_h2": "Yerel saha gücü. Merkezi operasyon. Ölçülebilir sonuç.",
    "stats": [(SITE["provinces"], "ilde erişilebilir yerel ekip ağı"), (SITE["regions"], "saha ekibi"), (SITE["visits"], "aylık planlı saha ziyareti"), (SITE["photo_rate"], "zorunlu fotoğraf doğrulama oranı")],
    "sol_eyebrow": "Çözümler", "sol_h2": "Dört ürün. Tek BİGEL standardı.", "sol_lead": "Her ürün bağımsız kullanılabilir ya da aynı ziyaret planında birleşir. Hepsi aynı kontrol listesi, fotoğraf açısı ve kapanış kuralıyla çalışır.",
    "proof_eyebrow": "Kanıt", "proof_h2": "Sadece yapmıyoruz. Ölçüyoruz.",
    "proof_p": "Her ziyaret fotoğraf, kontrol listesi ve skor üretir. Bulgular iş emrine dönüşür, kapanışı sorumlu ve hedef tarihle takip edilir.",
    "proof_list": ["Öncesi ve sonrası fotoğraf, GPS ve zaman damgası", "Soru bazlı skor ve kırmızı-sarı-yeşil durum özeti", "Sorumlu, hedef tarih ve kapanış kanıtıyla aksiyon takibi", "Lokasyon, bölge ve dönem karşılaştırmaları"],
    "ba": [("01.02.2026", "Tabela — Hasarlı", "Öncelik: Yüksek · İş emri açıldı", "red", "Açık"), ("01.03.2026", "Tabela — Yenilendi", "Sonrası fotoğrafı eklendi · Yetkili teyidi alındı", "green", "Kapandı")],
    "flow_eyebrow": "Nasıl çalışıyoruz", "flow_h2": "Planlamadan kapanışa tek kayıt zinciri.",
    "flow": [("Planlama", "Lokasyon, görev, ekip ve SLA tanımı."), ("Uygulama", "Temizlik veya bakım, standart prosedürle."), ("Denetim", "Kontrol listesi, skor ve fotoğraf."), ("Raporlama", "KPI, SLA ve lokasyon skoru."), ("Aksiyon", "İş emri, sorumlu ve kapanış kanıtı.")],
    "flow_more": "Süreci detaylı görün",
    "sec_eyebrow": "Sektörler", "sec_h2": "Akaryakıt ve şarj istasyonlarından perakendeye, çok lokasyonlu her marka için.", "sec_more": "Tüm sektörler",
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
         "list": ["Ortak hizmet tanımı ve uygulama standardı", "Merkezi görev ve ziyaret planlaması", "Bölgesel ekiplerle hızlı saha erişimi", "Öncesi ve sonrası fotoğraflı hizmet kanıtı", "Lokasyon ve bölge bazında performans görünürlüğü"], "img": "station.jpg", "tag": "Kanopi ve saha temizliği · Akaryakıt", "link": "fuel_clean"},
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
      "desc": "Küçük bakım, onarım ve saha müdahalesini Türkiye genelinde tek merkezden yönetiyoruz. Tespit, iş emri, uygulama ve fotoğraflı kapanış.",
      "lead": "Markaların fiziksel noktalarındaki küçük bakım, onarım ve saha müdahale ihtiyaçlarını tek merkezden yönetiyoruz. Tespit, planlama, saha uygulaması, fotoğraflama ve kapanış takibi BİGEL'de.",
      "sections": [
        {"type": "split", "eyebrow": "Kapsam", "h2": "Küçük işler birikmeden çözülür.", "p": "Lokasyonlarda biriken küçük fiziksel problemler müşteri deneyimini ve marka görünümünü etkiler. BİGEL CARE bu işleri tek iş emri sistemiyle yönetir.",
         "list": ["Periyodik ve önleyici bakım", "Arıza ve fiziksel hasar müdahalesi", "Görsel alan ve marka unsurları bakımı", "Dış alan ve çevre bakımı", "Mobilya, ekipman ve küçük montaj işleri", "Acil saha müdahalesi"], "img": "retail.jpg", "tag": "Mobilya ve teşhir kontrolü · Mağaza",
         "note": "Yüksek uzmanlık ve yasal yetki gerektiren işler (elektrik, mekanik tesisat vb.) uygun uzmanlarla koordine edilir; BİGEL tespit, planlama ve kapanış takibini yönetir."},
        {"type": "modules", "eyebrow": "Hizmet modülleri", "h2": "On modül, sektöre göre birleştirilir.", "lead": "",
         "items": [("01", "Minor Works", "Vida sıkıştırma, sabitleme, kapı kolu ve aksesuar değişimi, silikon, noktasal boya."), ("02", "Sign Care", "Tabela, totem ve yönlendirme elemanlarının bakımı."), ("03", "Exterior Care", "Cephe, giriş ve dış alan bakımı."), ("04", "Visual Care", "Görsel alan ve marka unsurları."), ("05", "Furniture Care", "Mobilya ve teşhir elemanları."), ("06", "Pavement Care", "Zemin, bordür ve otopark bakımı."), ("07", "Site Care", "Lokasyon fiziksel durum yönetimi."), ("08", "Preventive Care", "Periyodik önleyici bakım."), ("09", "Emergency Care", "Acil saha müdahalesi."), ("10", "Field Audit", "Fotoğraflı kontrol ve aksiyon raporu.")]},
        {"type": "flow", "eyebrow": "İş akışı", "h2": "Talepten fotoğraflı kapanışa.", "steps": [("Talep", "Tek kanal: talep veya denetim bulgusu."), ("Fotoğraflı tespit", "Hasar türü, öncelik ve önerilen aksiyon."), ("Görev onayı", "Kapsam, sorumlu ve hedef tarih."), ("Saha müdahalesi", "Bölgesel ekiple standart uygulama."), ("Kapanış raporu", "Sonrası fotoğrafı ve kalite kontrolü.")]},
        {"type": "cards3", "eyebrow": "Sektör paketleri", "h2": "Her sektörün fiziksel alanına göre.", "items": [("Station Care", "Akaryakıt istasyonları: kanopi, tabela, pompa adası, bordür, bariyer ve istasyon çevresi.", "fuel_clean"), ("EV Charge Care", "Şarj ünitesi dış gövdesi, zemin, yönlendirme ve aydınlatma dış gövdesi. Elektriksel bakım yetkili uzmanlarla.", "ev_care"), ("Restaurant Care", "Dış cephe, tabela, dış oturma, arabaya servis alanı ve iç mekân küçük işler."), ("Auto & ATM Care", "Showroom cephe, sergileme platformu; ATM kabini, şube girişi ve banko."), ("Retail & AVM Care", "Raf, teşhir ünitesi, vitrin çerçevesi; AVM yönlendirme, oturma grupları ve sezonluk dekorasyon."), ("Logistics & Facility Care", "Depo cephe, zemin çizgileri, bariyer; otel, eğitim kurumu ve fabrika girişleri.")]},
      ]},
    "audit": {
      "title": "BİGEL AUDIT — Saha denetimi, AUDIT 100 ve EV Audit30",
      "desc": "Marka standardını, görsel uygulamaları, temizliği ve fiziksel durumu sahada ölçülebilir kılıyoruz. AUDIT 100 ve EV Audit30 ile fotoğraflı skor.",
      "lead": "Markaların fiziksel noktalarındaki marka standardını, görsel uygulamaları, temizlik durumunu, fiziksel ihtiyaçları ve müşteri deneyimini sahada ölçülebilir hale getiriyoruz. Bağımsız kullanılır ya da CLEAN ve CARE ile bütünleşir.",
      "sections": [
        {"type": "flow", "eyebrow": "Nasıl çalışır", "h2": "Denetimi gözlemle sınırlamayız; karar ve aksiyona dönüştürürüz.", "steps": [("Saha", "Eğitimli ekip, standart kontrol listesiyle inceler."), ("Veri", "Puan, fotoğraf, GPS, tarih ve bulgu kaydedilir."), ("Merkez", "Lokasyonlar tek dashboard'da karşılaştırılır."), ("Karar", "Bulgular öncelik ve sorumluluğa göre sınıflanır."), ("İş emri", "Aksiyon oluşturulur, uygulanır, fotoğrafla kapanır.")]},
        {"type": "modules", "eyebrow": "Denetim kategorileri", "h2": "Sektöre uyarlanan ortak denetim çatısı.", "lead": "Her madde Uygun, Uygun Değil veya Uygulanamaz olarak işaretlenir; fotoğraf, konum, tarih ve açıklamayla kanıtlanır.",
         "items": [("01", "Brand Audit", "Logo, kurumsal renk, güncel tabela, kampanya materyali ve fiyat iletişimi. BRAND SCORE."), ("02", "Visual Audit", "Tabela, totem, ışıklı harf, folyo, poster, vitrin, stand ve dijital ekran."), ("03", "Clean Audit", "Zemin, cam, cephe, otopark, çöp alanı ve ortak alanlar; renk kodlu özet."), ("04", "Physical Audit", "Duvar, kapı, mobilya, bariyer, korkuluk ve küçük hasarlar; bakım iş emrine dönüşür."), ("05", "Customer Experience Audit", "Fark edilirlik, giriş, yönlendirme, kasa ve bekleme alanı. CX SCORE.")]},
        {"type": "sub", "id": "audit100", "logo": "audit100.png", "eyebrow": "Dijital denetim ürünü", "h2": "AUDIT 100 — 100 kriter. Tek skor.",
         "p": "10 kategori, 100 kontrol noktası. Her madde Uygun 100, Kısmen Uygun 50, Uygun Değil 0 puan alır; kategori ağırlıklarıyla 100 üzerinden lokasyon skoru oluşur. Fotoğraf kuralı soru bazında tanımlıdır: şartlı, zorunlu veya öncesi-sonrası.",
         "weights": [("Dış Alan & Cephe", 10), ("Tabela / Totem / Görsel", 10), ("Temizlik & Hijyen", 10), ("Mobilya / Ekipman", 10), ("Teknik & Fiziksel Durum", 10), ("İş Güvenliği & Risk", 15), ("Marka / Görsel Standart", 15), ("Müşteri Deneyimi", 10), ("Operasyon & Uygulama", 5), ("Yönetim / Veri / Uygunluk", 5)],
         "thresholds": [("g", "90–100 · Standarda uygun"), ("a", "75–89 · İyileştirme gerekli"), ("r", "0–74 · Öncelikli aksiyon")],
         "badges": ["Zorunlu fotoğraf ve GPS", "Kritik bulguda anlık bildirim", "Lokasyon skor kartı", "JSON / PDF rapor"], "more": "fuel_audit"},
        {"type": "sub", "id": "ev", "logo": None, "eyebrow": "Şarj ağları için", "h2": "Şarj noktası saha kalite denetimi.",
         "p": "Uzaktan izleme cihazın teknik durumunu gösterir; Audit30 müşterinin karşılaştığı fiziksel saha koşullarını görünür kılar. 30 standart kontrol, 6 ağırlıklı alan, 100 üzerinden saha skoru. Güvenlik maddelerindeki uygunsuzluk aynı gün bildirim üretir; majör bulgular 24 saat içinde aksiyona bağlanır.",
         "weights": [("Güvenlik · 5 kritik kontrol", 25), ("Cihaz bütünlüğü", 20), ("İşlev işaretleri", 20), ("Kullanıcı deneyimi", 15), ("Temizlik ve çevre", 10), ("Marka standardı", 10)],
         "thresholds": [("g", "≥ 90 · Uygun"), ("a", "75–89 · Takip"), ("r", "< 75 · Aksiyon")],
         "badges": ["Ön, sağ, sol, ekran, kablo, park alanı fotoğraf seti", "Kritik: anlık · Majör: 24 saat", "Pilot: 10 lokasyon, 2 hafta, 2 tur"], "more": "ev_audit"},
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
  "sectors": {"title": "Sektörler — Akaryakıt, EV Şarj ve Zincir Markalar", "desc": "Akaryakıt, elektrikli araç şarj, restoran, perakende, bankacılık, otomotiv, lojistik, AVM, otel, telekom, eğitim ve tesisler için saha hizmetleri.",
              "eyebrow": "Sektörler", "h1": "Akaryakıt ve şarj istasyonlarından perakendeye, standardın merkezden yönetildiği her sektör.", "lead": "Hizmet kapsamı, her sektörün yüzeyleri ve operasyon saatlerine göre uyarlanır. Aşağıda her sektör için öne çıkan alanları görebilirsiniz.",
              "fr_eyebrow": "Franchise ağları", "fr_h2": "Merkez adına tek sözleşme, tüm şubelerde ortak standart.", "fr_p": "Franchise sahiplerinin uygulamaları görünür, ölçülebilir ve merkezden yönetilebilir hale gelir.",
              "fr_list": ["Merkez ile tek sözleşme ve tek hizmet tanımı", "Tüm lokasyonlar için ortak kontrol listesi", "Bölgesel ekiplerle planlı saha ziyaretleri", "Lokasyon bazında skor ve uygunsuzluk takibi", "Merkez yönetim için karşılaştırmalı dashboard"],
              "fit_eyebrow": "İhtiyaca göre çözüm", "fit_h2": "Hangi durumda hangi ürün?",
              "fit": [("Çok lokasyonlu temizlik", "Periyodik CLEAN programı", "clean"), ("Küçük bakım ve onarım birikiyor", "CARE müdahale planı", "care"), ("Marka standardını ölçmek", "AUDIT ve AUDIT 100", "audit"), ("Şarj ağı saha kalitesi", "EV Audit30", "ev_audit"), ("Dağınık tedarikçi yapısı", "FIELD360 ile tek merkez", "field360"), ("Fotoğraf ve kanıt ihtiyacı", "Dijital ziyaret raporu", "field360")]},
  "tiers": {"title": "Abonelik Paketleri — BASIC, PRO, BUSINESS, 360", "desc": "BİGEL abonelik paketleri: temel kontrolden tam entegre saha yönetimine. Fiyatlandırma lokasyon sayısı ve kapsama göre.",
            "eyebrow": "Abonelikler", "h1": "İhtiyacınıza göre ölçeklenen dört paket.", "lead": "Alt paket adı ikinci hiyerarşidedir; ana BİGEL standardı, fotoğraflı kanıt ve raporlama her pakette aynıdır. Fiyatlandırma lokasyon sayısı, bölgesel dağılım, hizmet sıklığı ve kapsama göre hazırlanır.",
            "badge": "En kapsamlı", "cta": "Teklif Al", "cmp_h2": "Paket karşılaştırması",
            "cmp_head": ["Kapsam", "BASIC", "PRO", "BUSINESS", "360"],
            "cmp_rows": [["Periyodik kontrol ziyareti", 1,1,1,1], ["Fotoğraflı lokasyon raporu", 1,1,1,1], ["Bulgu ve öncelik listesi", 1,1,1,1], ["Küçük bakım müdahalesi (CARE)", 0,1,1,1], ["İş emri ve fotoğraflı kapanış", 0,1,1,1], ["Planlı temizlik programı (CLEAN)", 0,0,1,1], ["AUDIT 100 periyodik denetim", 0,0,1,1], ["Yönetim dashboardu, KPI / SLA", 0,0,1,1], ["Öncelikli destek hattı", 0,0,1,1], ["FIELD360 tek operasyon merkezi", 0,0,0,1], ["Atanmış operasyon yöneticisi", 0,0,0,1]],
            "note": "Tüm paketler pilot uygulamayla başlatılabilir. Pilot sonuçlarına göre hizmet sıklığı ve kapsam netleştirilir."},
  "how": {"title": "Nasıl Çalışıyoruz — Pilot ve yaygınlaştırma", "desc": "İhtiyaç analizinden düzenli raporlamaya BİGEL hizmet devreye alma modeli, kalite güvence ve dijital raporlama.",
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
  "about": {"title": "Hakkımızda — Kurumsal saha operasyonları", "desc": "BİGEL, kurumsal markaların saha operasyonlarını yürüten, denetleyen ve raporlayan yeni nesil bir saha hizmetleri platformudur.",
            "eyebrow": "Hakkımızda", "h1": "Usta gönderen firma değil, saha operasyonunuzu emanet edebileceğiniz partner.",
            "lead": "BİGEL, kurumsal markaların saha operasyonlarını yürüten, denetleyen ve raporlayan yeni nesil bir saha hizmetleri platformudur. Yerel saha gücünü merkezi operasyon, denetim ve raporlamayla birleştirir.",
            "story_h2": "Sahadan doğdu, sistemle büyüdü.",
            "story": ["BİGEL'in yolculuğu 2018'de İstanbul'da, akaryakıt istasyonu ağlarına yönelik dış alan temizlik ve küçük bakım işleriyle başladı. Lokasyon sayısı arttıkça sorun da netleşti: işi yapmak yetmiyordu, her noktada aynı standardı tutmak ve bunu merkeze kanıtlamak gerekiyordu.", "Bugün BİGEL, bölgesel ekip ağını merkezi planlama, standart kontrol listeleri ve fotoğraflı dijital raporlamayla yönetiyor. CLEAN, CARE, AUDIT ve FIELD360 aynı çatı altında, aynı kayıt zinciriyle çalışıyor.", "Yıllara dayanan saha deneyimimiz bilgimizin kaynağı olmaya devam ediyor; BİGEL markası ise kurumsal saha operasyonları ve teknoloji eksenine odaklanıyor."],
            "facts": [("45", "il"), ("60", "ekip"), (SITE["provinces"], "ile erişim"), ("4", "ürün, tek kayıt zinciri")],
            "v_eyebrow": "Marka tanımı", "v_h2": "Ne için varız?",
            "values": [("Amacımız", "Markaların sahadaki işlerini daha düzenli, ölçülebilir ve güvenilir hale getirmek.", "flag"), ("Sözümüz", "İşi sahada gerçekleştirmek, kontrol etmek ve görünür kılmak.", "shield"), ("Farkımız", "Yerel saha gücü + merkezi operasyon + denetim + raporlama.", "hub")],
            "c_eyebrow": "Karakter", "c_h2": "BİGEL nasıl konuşur, nasıl çalışır?",
            "character": [("Güvenilir", "Standart, kanıt ve rapor. Abartılı vaat yok."), ("Çevik", "Bölgesel ekiplerle daha kısa müdahale süresi."), ("Sistemli", "Planlama + uygulama + kontrol + raporlama."), ("Çözüm odaklı", "Bulgu iş emrine, iş emri kapanışa dönüşür."), ("Teknolojik", "Dijital kontrol listesi, skor ve dashboard."), ("Ölçülebilir", "100 kriter, fotoğraflı kanıt, tek skor.")],
            "reg_eyebrow": "Saha ağı", "reg_h2": "Yedi bölge, tek operasyon merkezi.",
            "regions": ["Marmara", "Ege", "Akdeniz", "İç Anadolu", "Karadeniz", "Doğu Anadolu", "Güneydoğu Anadolu"],
            "reg_p": "Merkezi planlama ve kalite kontrolü İstanbul'dan yürütülür; uygulama bölgesel ekiplerle yapılır. Ekipler ortak hizmet standardına göre eğitilir, kıyafet, kimlik, İSG ve dijital kayıt standardına göre değerlendirilir."},
  "contact": {"title": "İletişim — Teklif, pilot ve demo talebi", "desc": "Saha operasyonunuzu birlikte tasarlayalım. Teklif, pilot veya demo görüşmesi için talep bırakın.",
              "eyebrow": "İletişim", "h1": "Saha operasyonunuzu birlikte tasarlayalım.", "lead": "Teklif, pilot veya demo görüşmesi için formu doldurun. Aynı iş günü içinde dönüş yapıyoruz.",
              "f": {"name": "Ad Soyad", "company": "Şirket", "email": "E-posta", "phone": "Telefon", "count": "Lokasyon sayısı", "counts": ["1–10", "11–50", "51–250", "251–1.000", "1.000+"], "solution": "İlgilendiğiniz çözüm", "solutions": ["BİGEL CLEAN", "BİGEL CARE", "BİGEL AUDIT / AUDIT 100", "EV Audit30", "BİGEL FIELD360", "Abonelik paketleri", "Birden fazla"], "msg": "İhtiyacınız", "msg_ph": "Lokasyon yapınız, hizmet ihtiyacınız ve öncelikleriniz…", "consent": "Kişisel verilerimin talebimle ilgili iletişim amacıyla işlenmesini kabul ediyorum.", "send": "Talep Oluştur", "subject": "bigel360.com — Yeni talep"},
              "info": [("Merkez", SITE["address_tr"]), ("Telefon", SITE["phone"]), ("E-posta", SITE["email"]), ("LinkedIn", "linkedin.com/company/bigel360"), ("Çalışma saatleri", "Hafta içi 09:00–18:00")]},
  "pilot": {"title": "Pilot Uygulama — 20–30 lokasyonda 4–6 hafta", "desc": "20–30 lokasyonda 4–6 haftalık pilot: başlangıç ölçümü, fotoğraflı bulgular, lokasyon skorları ve yaygınlaştırma planı. Pilot başvurusu.",
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
                  "sector": "Sektör", "sectors": ["Akaryakıt", "EV şarj istasyonları", "Restoran / Fast food", "Perakende", "Bankacılık", "Otomotiv", "Lojistik / Depo", "AVM / Plaza", "Otel / Turizm", "Telekom", "Eğitim", "Fabrika / Tesis", "Diğer"],
                  "count": "Toplam lokasyon sayısı", "counts": ["1–10", "11–50", "51–250", "251–1.000", "1.000+"],
                  "geo": "Şehir / bölge dağılımı", "geo_ph": "Örn. İstanbul 12, Ankara 6, İzmir 4…",
                  "product": "Başlangıç ürünü", "products": ["AUDIT 100", "EV Audit30", "CLEAN", "CARE", "FIELD360", "Henüz karar vermedim"],
                  "start": "Hedef başlangıç", "starts": ["2 hafta içinde", "1 ay içinde", "1–3 ay içinde", "Planlama aşamasındayız"],
                  "msg": "Notlar", "msg_ph": "Öncelikli lokasyonlar, mevcut tedarikçi yapısı, beklentiler…",
                  "consent": "Kişisel verilerimin talebimle ilgili iletişim amacıyla işlenmesini kabul ediyorum.", "send": "Pilot Başvurusu Gönder", "subject": "bigel360.com — Pilot başvurusu"},
            "after_h3": "Başvurudan sonra", "after": [("1", "Kapsam toplantısı", "90 dakika. Lokasyon yapısı, hizmet modülleri ve pilot başarı kriterleri."), ("2", "Pilot planı", "Lokasyon seti, soru seti, fotoğraf kuralı, SLA ve takvim tek dokümanda."), ("3", "Saha", "Ziyaretler başlar; kritik bulgular aynı gün bildirilir."), ("4", "Sonuç toplantısı", "Skorlar, bulgular ve yaygınlaştırma teklifi.")],
            "note": "Pilot kapsamı ve ücreti lokasyon sayısı, hizmet modülü ve coğrafi dağılıma göre teklif olarak sunulur. Pilot sonuçları nihai birim fiyatı netleştirir."},
  "portal": {"title": "Müşteri Portalı", "desc": "BİGEL müşteri portalı: taleplerinizi açın, saha işlerinizi ve fotoğraflı raporlarınızı takip edin. Erken erişim için bizimle iletişime geçin.", "h1": "Müşteri portalı çok yakında hizmetinizde.", "p": "BİGEL portalı üzerinden taleplerinizi açabilecek, saha işlerinizi ve fotoğraflı raporlarınızı anlık takip edebileceksiniz. Erken erişim için bizimle iletişime geçin.", "b1": "İletişime geçin", "b2": "Ana sayfaya dön"},
  "thanks": {"title": "Teşekkürler", "badge": "Talebiniz alındı", "h1": "Teşekkürler, sizi arayacağız.", "p": "Bilgileriniz operasyon ekibimize ulaştı. Aynı iş günü içinde sizinle iletişime geçiyoruz.",
             "steps_h": "Bundan sonra", "steps": [("Talebiniz bize ulaştı", "Formdaki bilgiler ekibimizin önünde."), ("Sizi arıyoruz", "Aynı iş günü içinde, hafta içi 09:00–18:00."), ("Kapsamı netleştiriyoruz", "Lokasyon yapınıza göre teklif ya da pilot planı hazırlıyoruz.")],
             "b": "Ana sayfaya dön", "b2": "Nasıl çalıştığımızı görün", "urgent": "Acil mi? Hemen ulaşın:"},
  "landings": {
    "fuel_clean": {'title': 'Akaryakıt İstasyonu Temizliği ve Bakımı',
       'desc': 'Kanopi, totem, pompa adası, pist ve otopark temizliği; bordür, bariyer ve küçük onarımlar. Türkiye genelinde tek standart ve fotoğraflı kanıt.',
       'crumb': 'Akaryakıt İstasyonu Temizliği ve Bakımı',
       'service': 'Akaryakıt istasyonu temizliği ve bakımı',
       'eyebrow': 'Akaryakıt İstasyonları · CLEAN + CARE',
       'h1': 'Akaryakıt istasyonu temizliği ve bakımı, her noktada aynı standartta.',
       'lead': 'Kanopi, totem, pompa adası, pist, otopark ve istasyon çevresinin temizliğini ve küçük bakımını Türkiye genelinde tek standartla planlıyoruz. Her ziyaret merkezi görev planından '
               'çıkar; öncesi ve sonrası fotoğraf, GPS ve zaman damgasıyla kapanır.',
       'b1': 'Pilot Başlat',
       'b2': 'Teklif Al',
       'sections': [{'eyebrow': 'Kapsam',
                     'h2': 'Akaryakıt istasyonu temizliği neleri kapsar?',
                     'lead': 'BİGEL CLEAN, istasyonun müşteriye görünen dış alanını tanımlı yöntem, ekipman ve fotoğraf açısıyla ele alır. Modüller tek seferlik uygulanabilir ya da periyodik '
                             'programa eklenir.',
                     'cards': [('Akaryakıt istasyonu kanopisi temizliği',
                                'Kanopi tavanı ve alın bandında biriken atmosferik kir, toz, egzoz izi, kurum ve biyolojik kirlerin periyodik temizliği.'),
                               ('Totem ve fiyat panosu temizliği', 'Totem, tabela ve yönlendirme elemanlarının yüzeye uygun yöntemle temizliği. Marka görünürlüğü yoldan bakıldığında da korunur.'),
                               ('Pompa adası ve pist temizliği',
                                'Pompa adası çevresi ve ön sahada beton ve asfalt zeminde kir, yağ lekesi ve çevre temizliği; hepsi aynı kontrol listesine bağlanır.'),
                               ('Cephe, cam ve otopark', 'İstasyon binası ve market cephesinde giriş camı, cam cephe, kompozit ve metal yüzeyler; otopark zemininde kir ve yağ lekesi temizliği.'),
                               ('Gece, acil ve sezonluk temizlik',
                                'Night Clean çalışma düzenini bozmadan kapanış sonrası planlanır. Emergency Clean dökülme, kötü hava, vandalizm ve denetim öncesi durumlar için; Seasonal Clean '
                                'kış kiri, yaprak, çamur ve kaygan yüzey riskine göre kurulur.')]},
                    {'eyebrow': 'İstasyon bakımı · Station Care',
                     'h2': 'Küçük arızalar birikmeden kapanır.',
                     'lead': "BİGEL CARE'in Station Care paketi; kanopi, tabela, pompa adası, bordür, bariyer ve istasyon çevresindeki küçük bakım ve onarım işlerini tek iş emri akışında toplar. "
                             'Ayrı ayrı usta aramak yerine tek kanaldan talep açılır.',
                     'steps': [('Tespit', 'Fotoğraflı tespit: hasar türü, öncelik ve önerilen aksiyon.'),
                               ('İş emri', 'Kapsam, sorumlu ve hedef tarih onaylanır.'),
                               ('Uygulama', 'Bölgesel ekiple standart uygulama.'),
                               ('Fotoğraflı kapanış', 'Sonrası fotoğrafı ve kalite kontrolü.')],
                     'list': ['Minor Works: vida sıkıştırma, sabitleme, silikon, noktasal boya ve aksesuar değişimi',
                              'Sign Care: tabela, totem ve yönlendirme elemanlarının bakımı',
                              'Pavement Care: zemin, bordür ve otopark bakımı',
                              'Preventive Care: arızayı beklemeden periyodik önleyici bakım',
                              'Emergency Care: acil saha müdahalesi'],
                     'note': 'Yüksek uzmanlık ve yasal yetki gerektiren işler (elektrik, mekanik tesisat vb.) uygun uzmanlarla koordine edilir; BİGEL tespit, planlama ve kapanış takibini '
                             'yönetir.'},
                    {'eyebrow': 'Saha güvenliği',
                     'h2': 'Akışı durmayan bir sahada düzenli ve güvenli çalışma.',
                     'lead': 'Akaryakıt istasyonunda temizlik ve bakım, müşteri trafiği sürerken yapılır. Bu yüzden ziyaret planı istasyonun çalışma düzenine göre kurulur ve güvenlik maddeleri '
                             'denetimde ayrıca puanlanır.',
                     'list': ['Ziyaret saatleri, erişim koşulları ve hedef süreler kapsam ve SLA aşamasında birlikte tanımlanır',
                              'Uygulama yöntemi, ekipman ve kimyasal kullanımı standart operasyon prosedürüne bağlıdır',
                              'Ekipler ortak hizmet standardına göre eğitilir; kıyafet, kimlik ve İSG standardına göre değerlendirilir',
                              'Dökülme ve ani kirlenmede Emergency Clean ile hızlı müdahale',
                              'Kış aylarında kaygan yüzey riskine karşı Seasonal Clean programı',
                              "AUDIT 100'de İş Güvenliği & Risk kategorisi %15 ağırlıkla puanlanır; kritik bulguda anlık bildirim üretilir"]},
                    {'eyebrow': 'Çok lokasyonlu ağlar',
                     'h2': 'İstasyon sayısı artsa da temizlik standardı aynı kalır.',
                     'lead': "BİGEL'in yolculuğu akaryakıt istasyonu ağlarına yönelik dış alan temizlik ve küçük bakım işleriyle başladı. Öğrendiğimiz şey netti: işi yapmak yetmez; her noktada "
                             'aynı standardı tutmak ve bunu merkeze kanıtlamak gerekir.',
                     'list': ['Tüm istasyonlar için ortak hizmet tanımı, kontrol listesi ve uygulama standardı',
                              'Merkezi görev ve ziyaret planlaması; aylık, iki aylık, üç aylık veya mevsimsel program',
                              'Standart fotoğraf açıları ve kalite kriterleri',
                              'Lokasyon, bölge ve dönem bazında performans görünürlüğü',
                              'Zamanında ziyaret, tamamlanma oranı ve aksiyon kapanış süresi KPI ve SLA ile izlenir']},
                    {'eyebrow': 'Kanıt ve raporlama · FIELD360',
                     'h2': 'Sahada yapılan iş, merkezde görünür.',
                     'lead': "Her ziyaret aynı dijital akışla yürütülür ve FIELD360'ta tek kayıt zincirine düşer.",
                     'steps': [('Görev kapsamı', 'Lokasyon bilgisi ve tanımlı hizmet.'),
                               ('Öncesi fotoğraf', 'Standart açılardan başlangıç kaydı.'),
                               ('Uygulama', 'Yöntem, ekipman ve kimyasal standardı.'),
                               ('Sonrası fotoğraf', 'Kontrol listesi ve kalite kriteri.'),
                               ('Tamamlanma', 'Bulgu bildirimi ve kapanış kaydı.')],
                     'list': ['Öncesi ve sonrası fotoğraf, GPS ve zaman damgası',
                              'Konum, tarih, ekip ve fotoğrafla doğrulanan ziyaret',
                              'Ziyaretler, skorlar, açık bulgular, iş emirleri ve kapanış kanıtları tek ekranda',
                              'Planlanan, tamamlanan ve geciken ziyaretlerle SLA takibi'],
                     'links': [('BİGEL FIELD360', 'field360', '')]},
                    {'eyebrow': 'Temizlik + bakım + denetim',
                     'h2': 'Temizlikten denetime tek döngü.',
                     'lead': 'AUDIT 100, istasyonu 10 kategoride 100 kontrol noktasıyla puanlar. Bu bir marka, görsel standart ve saha durumu denetimidir. Çıkan bulgu CARE iş emrine dönüşür, '
                             'kapanışı fotoğrafla doğrulanır.',
                     'steps': [('Saha', 'Eğitimli ekip, standart kontrol listesiyle inceler.'),
                               ('Veri', 'Puan, fotoğraf, GPS, tarih ve bulgu kaydedilir.'),
                               ('Merkez', "İstasyonlar tek dashboard'da karşılaştırılır."),
                               ('Karar', 'Bulgular öncelik ve sorumluluğa göre sınıflanır.'),
                               ('İş emri', 'Aksiyon oluşturulur, uygulanır, fotoğrafla kapanır.')],
                     'list': ['Her madde Uygun 100, Kısmen Uygun 50, Uygun Değil 0 puan alır',
                              'Kategori ağırlıklarıyla 100 üzerinden istasyon skoru oluşur',
                              '90–100 standarda uygun · 75–89 iyileştirme gerekli · 0–74 öncelikli aksiyon',
                              'BİGEL Map ile tüm istasyonlar Türkiye haritasında skor rengiyle görünür'],
                     'links': [('Akaryakıt istasyonu denetimi', 'fuel_audit', '')]},
                    {'eyebrow': 'Nasıl başlarız',
                     'h2': '20–30 istasyonla başlayın, sonuçla ölçekleyin.',
                     'lead': 'Pilot 4–6 hafta sürer ve iki ziyaret turundan oluşur. Sonunda elinizde başlangıç skorları, fotoğraflı bulgular ve gerçek saha verisine dayanan bir yaygınlaştırma '
                             'planı olur.',
                     'steps': [('Kapsam ve kriterler', 'İstasyon seti, soru seti ve skor ağırlıkları onaylanır.'),
                               ('Başlangıç ölçümü', 'Mevcut durum fotoğraf ve kontrol listesiyle kaydedilir.'),
                               ('Saha uygulaması', 'CLEAN, CARE veya AUDIT bölgesel ekiplerle uygulanır.'),
                               ('İkinci tur', 'Aksiyonlar kapatılır, skor gelişimi doğrulanır.'),
                               ('Yaygınlaştırma', 'SLA, bölge ve takvimle ölçekleme planı.')],
                     'list': ['BASIC: periyodik kontrol ve fotoğraflı lokasyon raporu',
                              'PRO: kontrole ek olarak küçük bakım, iş emri ve fotoğraflı kapanış',
                              'BUSINESS: planlı CLEAN programı, AUDIT 100 periyodik denetim, KPI/SLA raporu',
                              '360: FIELD360 tek operasyon merkezi ve atanmış operasyon yöneticisi'],
                     'note': 'Fiyatlandırma; lokasyon sayısı, alan ve yüzey türü, ziyaret sıklığı, ekipman ihtiyacı ve erişim koşullarına göre hazırlanır. Pilot uygulama nihai birim fiyatı '
                             'netleştirir.',
                     'links': [('Abonelik paketleri', 'tiers', '')]}],
       'faq': [('Akaryakıt istasyonu temizliği hangi alanları kapsar?',
                'Kanopi tavanı ve alın bandı, totem ve tabelalar, pompa adaları ve pist, istasyon binası cephesi ve camları, otopark ve istasyon çevresi. Kapsam her istasyon için kontrol '
                'listesiyle tanımlanır.'),
               ('Kanopi ve totem temizliği istasyon çalışırken yapılabilir mi?',
                'Ziyaret saatleri ve erişim koşulları kapsam aşamasında istasyonun çalışma düzenine göre belirlenir. Gerekirse Night Clean modeliyle işletmenin çalışma düzenini etkilemeden '
                'kapanış sonrası planlanır.'),
               ('Pist ve pompa adası temizliği ne sıklıkla yapılmalı?',
                'Sıklık istasyonun yoğunluğuna ve yüzey durumuna göre aylık, iki aylık, üç aylık veya mevsimsel programla belirlenir. Ani dökülme ve kirlenmelerde Emergency Clean devreye girer; '
                'kesin sıklık pilot verisiyle netleşir.'),
               ('Küçük onarımlar için ayrı ayrı usta çağırmak gerekir mi?',
                'Hayır. Station Care; kanopi, tabela, pompa adası, bordür ve bariyerdeki küçük işleri tek iş emri akışında toplar. Elektrik ve mekanik tesisat gibi yasal yetki gerektiren işler '
                "uygun uzmanlarla koordine edilir, takibi BİGEL'de kalır."),
               ('Temizlik ve bakım işinin yapıldığı nasıl doğrulanır?',
                "Her ziyaret öncesi ve sonrası fotoğraf, GPS ve zaman damgası ile kayda geçer; kontrol listesi ve zorunlu fotoğrafla doğrulanır. Tüm kayıtlar FIELD360'ta istasyon bazında "
                'izlenir.'),
               ('Çok sayıda istasyonda aynı temizlik standardı nasıl sağlanır?',
                'Tüm istasyonlar ortak hizmet tanımı, kontrol listesi ve fotoğraf açısıyla çalışır; ziyaretler merkezden planlanır, 81 ile erişen bölgesel ekiplerle uygulanır. Sonuçlar lokasyon '
                've bölge bazında karşılaştırılır.'),
               ('Denetimde çıkan bulgular nasıl kapanır?',
                'AUDIT 100 bulgusu öncelik, sorumlu ve hedef tarihle CARE iş emrine dönüşür. Uygulama sonrası fotoğrafla kapanır, ikinci ziyarette skor gelişimi doğrulanır.')],
       'cta': {'h2': 'İstasyon ağınız için pilot kapsamını birlikte belirleyelim.',
               'p': '20–30 istasyonla, 4–6 haftada başlangıç skorunu ve açık bulguları görün. Formu doldurun; aynı iş günü içinde dönüş yapalım.',
               'b1': 'Pilot Başlat',
               'b2': 'Teklif Al'}},
    "fuel_audit": {'title': 'Akaryakıt İstasyonu Denetimi — AUDIT 100',
       'desc': 'İstasyon ağınızda marka, görsel standart, temizlik, fiziksel durum ve müşteri deneyimi denetimi. 100 kriter, fotoğraflı kanıt, skor ve aksiyon takibi.',
       'crumb': 'Akaryakıt İstasyonu Denetimi',
       'service': 'Akaryakıt istasyonu marka ve saha standardı denetimi',
       'eyebrow': 'Akaryakıt İstasyonları · AUDIT 100',
       'h1': 'Akaryakıt istasyonu denetimi: 100 kriter, tek skor.',
       'lead': 'İstasyon ağınızdaki marka standardını, görsel uygulamaları, temizliği, fiziksel durumu ve müşteri deneyimini sahada ölçülebilir hale getiriyoruz. Her istasyon aynı kontrol '
               'listesiyle denetlenir, fotoğrafla kanıtlanır ve 100 üzerinden skorlanır.',
       'b1': 'AUDIT 100 Pilotu Başlat',
       'b2': 'Teklif Al',
       'sections': [{'eyebrow': 'Kapsam',
                     'h2': 'Resmi denetimden farkı',
                     'lead': 'Yakıt kalitesi, ölçü aletleri ve lisans uygunluğu denetimleri yetkili kurumların işidir; BİGEL bu denetimleri yapmaz. AUDIT 100, müşterinin istasyonda gördüğü ve '
                             'yaşadığı her şeye bakar. Resmi denetimlerin yerini almaz, onları tamamlar.',
                     'list': ['Marka ve görsel standart: logo, kurumsal renkler, güncel tabela, kampanya materyali ve fiyat iletişimi',
                              'Temizlik: pist, pompa adaları, cam ve cephe, otopark, çöp alanı ve ortak alanlar',
                              'Fiziksel durum: bariyer, bordür, korkuluk, kapı, mobilya ve küçük hasarlar',
                              'Müşteri deneyimi: fark edilirlik, giriş, yönlendirme, kasa ve bekleme alanı']},
                    {'eyebrow': 'Denetim kategorileri',
                     'h2': 'İstasyonda ne kontrol edilir?',
                     'lead': "BİGEL AUDIT'in beş modülü istasyonun fiziksel alanına uyarlanır. Soru seti ve skor ağırlıkları, pilot öncesinde sizinle birlikte onaylanır.",
                     'list': ['Brand Audit: kanopi ve totem üzerindeki marka unsurları, kurumsal renkler, kampanya materyali ve fiyat iletişimi (BRAND SCORE)',
                              'Visual Audit: tabela, totem ve fiyat panosu, ışıklı harf, folyo, poster, market vitrini ve dijital ekranlar',
                              'Clean Audit: pist zemini, pompa adaları, kanopi, cam ve cephe, otopark ve çöp alanı; renk kodlu özet',
                              'Physical Audit: bariyer, bordür, korkuluk, kapı ve mobilya hasarları; bulgular bakım iş emrine dönüşür',
                              'Customer Experience Audit: istasyonun yoldan fark edilirliği, giriş-çıkış yönlendirmesi, market girişi, kasa ve bekleme alanı (CX SCORE)']},
                    {'eyebrow': 'AUDIT 100 skor modeli',
                     'h2': 'Skor nasıl hesaplanır?',
                     'lead': '10 kategori, 100 kontrol noktası. Her madde Uygun (100), Kısmen Uygun (50) veya Uygun Değil (0) puan alır; kategori ağırlıklarıyla 100 üzerinden istasyon skoru '
                             'oluşur. Modeli açıkça yayımlıyoruz: skorun neye dayandığı her zaman görünür.',
                     'weights': 'audit100'},
                    {'eyebrow': 'İş güvenliği',
                     'h2': 'İstasyonda güvenlik önce gelir.',
                     'lead': "Akaryakıt istasyonu, risk toleransı düşük bir sahadır. Bu yüzden AUDIT 100'de en yüksek ağırlık İş Güvenliği & Risk kategorisine verilir ve kritik bulgular raporu "
                             'beklemez.',
                     'list': ["İş Güvenliği & Risk kategorisi skorun %15'ini oluşturur",
                              'Kritik bulguda rapor beklenmeden anlık bildirim',
                              'Bulgular kritik, yüksek, orta ve düşük olarak önceliklendirilir',
                              'Saha ekipleri kıyafet, kimlik, İSG ve dijital kayıt standardına göre değerlendirilir',
                              'Elektrik ve mekanik tesisat gibi yasal yetki gerektiren işler uygun uzmanlarla koordine edilir; BİGEL tespit, planlama ve kapanış takibini yönetir']},
                    {'eyebrow': 'Kanıt ve raporlama',
                     'h2': 'Her bulgu fotoğrafla, her ziyaret konumla kanıtlanır.',
                     'lead': 'Her madde fotoğraf, konum, tarih ve açıklamayla kayda geçer. Fotoğraf kuralı soru bazında tanımlıdır: şartlı, zorunlu veya öncesi-sonrası.',
                     'list': ['Zorunlu fotoğraf ve GPS ile doğrulanan ziyaret',
                              'İstasyon bazında skor kartı ve kırmızı-sarı-yeşil durum özeti',
                              'JSON / PDF rapor',
                              'BİGEL Map: tüm istasyonlar Türkiye haritasında skor rengiyle; bölgeden şehre, şehirden istasyona inilir',
                              'İstasyon, bölge ve dönem karşılaştırmaları']},
                    {'eyebrow': 'Aksiyon',
                     'h2': 'Bulgudan iş emrine',
                     'lead': 'Denetim raporla bitmez. Bulgu öncelik ve sorumluya göre sınıflanır; küçük bakım BİGEL CARE, temizlik ihtiyacı BİGEL CLEAN ile sahada çözülür ve kapanış fotoğrafla '
                             'doğrulanır.',
                     'steps': [('Saha', 'Eğitimli ekip istasyonu standart kontrol listesiyle inceler.'),
                               ('Veri', 'Puan, fotoğraf, GPS, tarih ve bulgu kaydedilir.'),
                               ('Merkez', "İstasyonlar tek dashboard'da karşılaştırılır."),
                               ('Karar', 'Bulgular öncelik ve sorumluluğa göre sınıflanır.'),
                               ('İş emri', 'Aksiyon oluşturulur, uygulanır, fotoğrafla kapanır.')],
                     'links': [('BİGEL CARE', 'care', ''), ('BİGEL CLEAN', 'clean', ''), ('Akaryakıt istasyonu temizliği', 'fuel_clean', '')]},
                    {'eyebrow': 'Hizmet modelleri',
                     'h2': 'Tek denetimden sürekli programa.',
                     'lead': 'Teklif; istasyon sayısı, soru adedi, fotoğraf gereksinimi, seyahat, denetim sıklığı, rapor formatı ve dashboard kapsamına göre hazırlanır.',
                     'list': ['Lokasyon bazlı audit: seçili istasyonlarda tek seferlik denetim',
                              'Periyodik audit: aylık, üç aylık, altı aylık veya yıllık program',
                              'Proje audit: kampanya, açılış veya tabela değişimi sonrası toplu kontrol',
                              'Franchise ve bayi audit: bayi ağında standart uyumunun merkez adına ölçülmesi',
                              'Yatırım ve devir: satın alma, kiralama veya devir öncesi fiziksel durumun belgelenmesi']},
                    {'eyebrow': 'Saha ağı',
                     'h2': 'Tüm istasyon ağı, tek standart.',
                     'lead': "BİGEL'in yolculuğu akaryakıt istasyonu ağlarına yönelik saha işleriyle başladı. Bugün merkezi planlama ve kalite kontrolü İstanbul'dan yürütülür; denetimler "
                             'bölgesel ekiplerle yapılır.',
                     'list': ['81 ilde erişilebilir yerel ekip ağı',
                              'Ortak kontrol listesi, fotoğraf açısı ve kapanış kuralı',
                              'FIELD360 ile denetim, temizlik ve bakım tek sözleşme, tek standart ve tek raporlamada']},
                    {'eyebrow': 'Pilot',
                     'h2': 'Önce seçili istasyonlarda ölçün.',
                     'lead': '20–30 lokasyon, 4–6 hafta, iki ziyaret turu: başlangıç ve doğrulama. Pilot sonunda istasyon skorları, fotoğraflı bulgu listesi ve yaygınlaştırma planı elinizde '
                             'olur.',
                     'list': ['Denetim özeti ve kategori skorları',
                              'Fotoğraflı bulgu listesi: kritik, yüksek, orta, düşük',
                              'Lokasyon ve bölge karşılaştırması',
                              'Tahmini iş yükü, ziyaret sıklığı ve uygulama takvimi']}],
       'faq': [('Bayi standart denetimi nedir, resmi denetimden farkı ne?',
                'Bayi standart denetimi, istasyonun marka, görsel standart, temizlik, fiziksel durum ve müşteri deneyimi açısından merkezin belirlediği standarda uyup uymadığını ölçer. Yakıt '
                'kalitesi, ölçü aletleri ve lisans denetimleri yetkili kurumların işidir; BİGEL bu denetimleri yapmaz, onları tamamlayan bir saha standardı denetimi sunar.'),
               ('Akaryakıt istasyonu denetiminde hangi maddeler kontrol edilir?',
                'Kanopi ve totemdeki marka unsurları, tabela ve fiyat panosu, pist ve pompa adalarının temizliği, bariyer, bordür ve korkuluk gibi fiziksel unsurlar, market girişi, kasa ve '
                'yönlendirme kontrol edilir. AUDIT 100 bunları 10 kategoride 100 kontrol noktasıyla ölçer; soru seti pilot öncesinde sizinle onaylanır.'),
               ('Denetim sonuçları nasıl skorlanır ve raporlanır?',
                'Her madde Uygun 100, Kısmen Uygun 50 veya Uygun Değil 0 puan alır; kategori ağırlıklarıyla 100 üzerinden istasyon skoru oluşur. 90–100 standarda uygun, 75–89 iyileştirme '
                'gerekli, 0–74 öncelikli aksiyon anlamına gelir. Sonuçlar istasyon skor kartı, JSON / PDF rapor ve BİGEL Map üzerinden izlenir.'),
               ('Denetimde çıkan bulgular nasıl aksiyona dönüşür?',
                'Bulgular öncelik ve sorumluya göre sınıflanır, iş emrine dönüşür ve hedef tarihle takip edilir. Küçük bakım BİGEL CARE, temizlik ihtiyacı BİGEL CLEAN ile sahada çözülür; kapanış '
                'fotoğrafla doğrulanır.'),
               ('Denetim ne sıklıkla yapılmalı?',
                'Periyodik programlar aylık, üç aylık, altı aylık veya yıllık kurulabilir. Kampanya, açılış veya tabela değişimi sonrasında ayrıca proje denetimi yapılabilir. Doğru sıklık, pilot '
                'sonuçlarına göre birlikte netleştirilir.'),
               ('Kritik bir güvenlik bulgusu çıkarsa ne olur?',
                "İş Güvenliği & Risk, AUDIT 100'de en yüksek ağırlığa (%15) sahip kategoridir. Kritik bulgu rapor beklenmeden anlık bildirilir ve öncelikli aksiyon olarak iş emrine bağlanır."),
               ('İstasyonlarımızda şarj noktaları da var. Onlar nasıl denetlenir?',
                'Şarj noktaları için EV Audit30 kullanılır: 30 standart kontrol, 6 ağırlıklı alan ve 100 üzerinden saha skoru. Akaryakıt alanı ve şarj noktaları aynı ziyaret planında birlikte '
                'denetlenebilir.')],
       'cta': {'h2': 'İstasyon ağınız için AUDIT 100 pilotu başlatın.',
               'p': 'Seçili istasyonlarda 4–6 haftalık bir pilotla başlangıç skorlarını ölçelim, sonuçlara göre bölgesel ve Türkiye geneli programı birlikte planlayalım.',
               'b1': 'AUDIT 100 Pilotu Başlat',
               'b2': 'İletişim'}},
    "ev_care": {'title': 'Şarj İstasyonu Bakımı ve Temizliği',
       'desc': 'Elektrikli araç şarj istasyonlarında ünite dış gövdesi, kablo düzeni, park cebi, zemin ve yönlendirme bakımı. Elektriksel bakım yetkili uzmanlarla.',
       'crumb': 'Şarj İstasyonu Bakımı ve Temizliği',
       'service': 'Elektrikli araç şarj istasyonu saha bakımı ve temizliği',
       'eyebrow': 'EV Şarj İstasyonları · CLEAN + CARE',
       'h1': 'Elektrikli araç şarj istasyonu saha bakımı ve temizliği.',
       'lead': 'Uzaktan izleme size cihazın teknik durumunu gösterir. Sürücünün istasyonda gördüğü saha koşullarını ise ancak sahadaki ekip korur. BİGEL, şarj ünitesinin dış gövdesini, kablo '
               'düzenini, park cebini, zemini ve yönlendirmeyi ağınızın tamamında aynı standartla bakımda tutar. Planlamayı, uygulamayı ve fotoğraflı raporlamayı tek merkezden yönetir.',
       'b1': 'Pilot Başvurusu',
       'b2': 'Teklif Al',
       'sections': [{'eyebrow': 'Kapsam',
                     'h2': 'Saha ve görsel bakım: sürücünün gördüğü her şey.',
                     'lead': 'Şarj noktasında deneyimi belirleyen tek şey cihazın çalışması değildir. Ünitenin temiz ve sağlam görünmesi, kablonun yerde kalmaması, park cebinin boş ve okunur '
                             "olması, yönlendirmenin araçtan fark edilmesi de aynı deneyimin parçasıdır. BİGEL CARE'in EV Charge Care paketi bu alanı kapsar.",
                     'list': ['Şarj ünitesi dış gövdesi ve ekran yüzeyi',
                              'Kablo düzeni: kablo ve konektörün yerde kalmaması',
                              'Park cebi, zemin, bordür ve otopark yüzeyi',
                              'Yönlendirme ve tabela elemanları',
                              'Aydınlatma armatürlerinin dış gövdesi',
                              'Cihaz çevresi ve istasyonun dış alanı']},
                    {'eyebrow': 'Kapsam dışı',
                     'h2': 'Elektriksel bakım yapmıyoruz. Bunu baştan açıkça söylüyoruz.',
                     'lead': 'Şarj ünitesinin elektriksel bakımı, periyodik muayenesi ve kalibrasyonu yasal yetki ve yüksek uzmanlık gerektirir. Bu işler yetkili uzmanlar tarafından yürütülür. '
                             'BİGEL bu işlerin yerine geçmez, onları tamamlar. Sahada fark edilen bulguyu kaydeder, uzmanlık gerektiren işi uygun uzmanla koordine eder, planlamayı ve kapanış '
                             'takibini yönetir.',
                     'list': ['Ünitenin içine ve elektriksel bileşenlere müdahale edilmez',
                              'Sahada görülen fiziksel bulgu fotoğrafla kayda geçer',
                              'Yetki gerektiren iş uygun uzmanla koordine edilir',
                              "Tespit, planlama ve kapanış takibi BİGEL'dedir"]},
                    {'eyebrow': 'BİGEL CLEAN',
                     'h2': 'Şarj istasyonu temizliği: ünite, ekran, zemin ve park cebi.',
                     'lead': 'Şarj alanı açık havadadır. Toz, yağmur, çamur ve kış kiri ünite gövdesinde ve zeminde hızla birikir. Temizlik, kapsam aşamasında onaylanan ortak kontrol listesi ve '
                             'standart prosedürle yapılır. Her yüzey kendi malzemesine uygun yöntemle temizlenir.',
                     'list': ['Ünite dış gövdesi ve ekran yüzeyinin temizliği',
                              'Tabela, totem ve yönlendirme elemanlarının yüzeye uygun temizliği',
                              'Zemin ve park cebinde kir, yağ lekesi ve çevre temizliği',
                              'Kablo ve konektörün kendi yerinde bırakılması',
                              'Kış kiri, yaprak ve çamura göre mevsimsel program',
                              'Ani kirlenme, vandalizm ya da kötü havadan sonra acil müdahale']},
                    {'eyebrow': 'BİGEL CARE iş akışı',
                     'h2': 'Tespit, iş emri, fotoğraflı kapanış.',
                     'lead': 'Sahada görülen her sorun tek iş emri akışında ilerler. Her şarj noktası aynı fotoğraf setiyle kayda geçer: ön, sağ, sol, ekran, kablo ve park alanı. Böylece '
                             'lokasyonlar ve dönemler aynı açıdan karşılaştırılabilir.',
                     'steps': [('Talep', 'Tek kanal: işletmeci talebi ya da denetim bulgusu.'),
                               ('Fotoğraflı tespit', 'Hasar türü, öncelik ve önerilen aksiyon.'),
                               ('Görev onayı', 'Kapsam, sorumlu ve hedef tarih.'),
                               ('Saha müdahalesi', 'Bölgesel ekiple standart uygulama.'),
                               ('Kapanış raporu', 'Sonrası fotoğrafı ve kalite kontrolü.')]},
                    {'eyebrow': 'EV Audit30',
                     'h2': 'Saha kalitesini ölçmek için EV Audit30.',
                     'lead': 'Bakımın etkisini görmek için ölçmek gerekir. EV Audit30, şarj noktasında 30 standart kontrol yapar. Bu kontroller 6 ağırlıklı alanda toplanır ve 100 üzerinden bir '
                             "saha skoru çıkar. 90 ve üzeri uygun, 75–89 takip, 75'in altı aksiyon anlamına gelir. Güvenlik maddelerinde uygunsuzluk çıkarsa aynı gün bildirim gider, majör "
                             'bulgular 24 saat içinde aksiyona bağlanır. Ayrıntılar şarj istasyonu denetimi sayfasındadır.',
                     'list': ['Güvenlik, 5 kritik kontrol: %25', 'Cihaz bütünlüğü: %20', 'İşlev işaretleri: %20', 'Kullanıcı deneyimi: %15', 'Temizlik ve çevre: %10', 'Marka standardı: %10'],
                     'links': [('Şarj istasyonu denetimini inceleyin', 'ev_audit', '')]},
                    {'eyebrow': 'FIELD360',
                     'h2': 'Ağın tamamında tek standart.',
                     'lead': 'Şarj ağları çoğu zaman şehirlere ve otoyollara dağılmış, az sayıda ünitesi olan çok sayıda noktadan oluşur. FIELD360 bu ağı tek merkezden yönetir. Kontrol '
                             'listeleri, fotoğraf açıları, kalite kriterleri ve kapanış kuralları her lokasyonda aynıdır.',
                     'list': ['Merkezi görev ve ziyaret planlaması',
                              '81 ile erişilebilir bölgesel ekip ağı',
                              'Konum, zaman, kontrol listesi ve fotoğrafla doğrulanan ziyaret',
                              'Aylık, iki aylık, üç aylık veya mevsimsel ziyaret programı',
                              'Birlikte belirlenen KPI ve SLA hedefleri',
                              'Lokasyon, bölge ve dönem bazında tek dashboard']}],
       'faq': [('Şarj istasyonu bakımı neleri kapsar, elektriksel bakım dahil mi?',
                "BİGEL'in kapsamı saha ve görsel bakımdır: ünite dış gövdesi, ekran yüzeyi, kablo düzeni, park cebi, zemin, yönlendirme ve aydınlatma dış gövdesi. Elektriksel bakım, periyodik "
                'muayene ve kalibrasyon bu kapsama girmez, yetkili uzmanlar tarafından yürütülür. BİGEL bu işlerde tespit, planlama ve kapanış takibini üstlenir.'),
               ('Şarj istasyonu nasıl temizlenir?',
                'Temizlik, kapsam aşamasında onaylanan kontrol listesine ve standart prosedüre göre yapılır. Ünite gövdesi, ekran, zemin ve park cebi her yüzeyin malzemesine uygun yöntemle '
                'temizlenir. Ünitenin içine ya da elektriksel bileşenlerine müdahale edilmez.'),
               ('Şarj kabloları yerde kalınca ne olur, kablo düzeni nasıl korunur?',
                'Yerde kalan kablo hem görüntüyü bozar hem de yürüyen ve manevra yapan araçlar için risk oluşturur. Bu yüzden kablo, her ziyaretin zorunlu fotoğraf setinde ayrı bir kare olarak '
                'kayda geçer. Uygunsuzluk görülürse bulgu olarak işaretlenir. Güvenlik maddelerindeki uygunsuzluklar aynı gün bildirilir.'),
               ('Şarj park yeri ve yönlendirme düzeni nasıl takip edilir?',
                "Park cebi ve yönlendirme her ziyarette fotoğrafla kaydedilir. EV Audit30'da bu alan kullanıcı deneyimi başlığı altında skorlanır. Silinmiş zemin işareti ya da hasarlı tabela "
                'gibi bulgular CARE iş emrine dönüşür ve fotoğraflı kapanışla takip edilir.'),
               ('Bakımın yapıldığı nasıl raporlanır?',
                'Her ziyaret GPS, zaman damgası, kontrol listesi ve fotoğrafla kayda geçer. İş emirleri sorumlu, hedef tarih ve kapanış kanıtıyla izlenir. Merkez ekip ise tüm lokasyonları '
                "lokasyon, bölge ve dönem bazında tek dashboard'da görür."),
               ('Ziyaret sıklığı nasıl belirlenir?',
                'Ziyaret sıklığı ağın ihtiyacına göre birlikte belirlenir. Aylık, iki aylık, üç aylık ya da mevsimsel bir program kurulabilir. Ani kirlenme, vandalizm veya kötü hava sonrası için '
                'ayrıca acil müdahale planlanabilir.'),
               ('Tüm ağa geçmeden önce deneyebilir miyiz?',
                'Evet. EV ağları için Audit30 pilotu 10 lokasyonda, 2 haftada ve 2 turda yapılır. Pilot sonunda başlangıç skorları, fotoğraflı bulgular ve aksiyon önerileri elinizde olur.')],
       'cta': {'h2': 'Şarj ağınızda pilotla başlayın.',
               'p': 'Audit30 pilotu 10 lokasyonda, 2 haftada ve 2 turda tamamlanır. Başlangıç skorları, fotoğraflı bulgular ve aksiyon önerileri tek raporda toplanır.',
               'b1': 'Pilot Başvurusu',
               'b2': 'Teklif Al'}},
    "ev_audit": {'title': 'Şarj İstasyonu Denetimi — EV Audit30',
       'desc': 'Şarj noktalarında kullanıcının gördüğü saha koşullarını ölçün: 30 kontrol, 6 ağırlıklı alan, 100 üzerinden skor. Kritik bulguda anlık bildirim.',
       'crumb': 'Şarj İstasyonu Denetimi',
       'service': 'Elektrikli araç şarj istasyonu saha denetimi',
       'eyebrow': 'EV Şarj İstasyonları · EV Audit30',
       'h1': 'Şarj istasyonu denetimi: EV Audit30 ile saha skoru.',
       'lead': 'Uzaktan izleme cihazın teknik durumunu gösterir; Audit30 müşterinin karşılaştığı fiziksel saha koşullarını görünür kılar. 30 standart kontrol, 6 ağırlıklı alan ve 100 üzerinden '
               'tek saha skoru. Her şarj noktası aynı fotoğraf setiyle kayda geçer, bulgular iş emrine dönüşür.',
       'b1': 'Audit30 Pilotu Başlat',
       'b2': 'Teklif Al',
       'sections': [{'eyebrow': 'Kapsam',
                     'h2': 'Neyi ölçer, neyi ölçmez?',
                     'lead': 'Bir şarj noktası izleme panelinde çevrimiçi görünebilir; sürücü ise sahada kirli bir ekranla, yere sarkmış bir kabloyla ya da başka bir aracın işgal ettiği park '
                             'cebiyle karşılaşabilir. EV Audit30 bu boşluğu kapatır: sürücünün gördüğü fiziksel saha kalitesini standart bir kontrol listesiyle ölçer.',
                     'list': ['Ölçer: cihaz çevresi, ünitenin dış gövdesi, ekran, kablo düzeni, park cebi, zemin, yönlendirme ve marka unsurları.',
                              'Ölçer: sahada gözle görülebilen işlev işaretleri ve kullanıcı deneyimini etkileyen koşullar.',
                              'Ölçmez: elektriksel muayene, ölçüm veya cihaz içi teknik test. Elektriksel işler yetkili uzmanlarla koordine edilir.',
                              'Resmi denetim değildir: EV Audit30, kurum denetimlerinin yerini tutmaz. Şarj ağınızın saha durumunu fotoğraflı ve tarihli kayıtla belgeleyerek iç hazırlığınızı '
                              'destekler.']},
                    {'eyebrow': 'Kontrol yapısı',
                     'h2': '30 kontrol, 6 ağırlıklı alan.',
                     'lead': 'Her lokasyon aynı 30 standart kontrolle incelenir. Alanlar sürücü ve marka açısından önemine göre ağırlıklandırılır; sonuç 100 üzerinden saha skorudur.',
                     'weights': 'ev'},
                    {'eyebrow': 'Sahada neye bakılır',
                     'h2': 'Şarj istasyonu kontrol listesinin saha alanları.',
                     'lead': 'Kontrol listesi, sürücünün araca yaklaştığı andan şarjı başlattığı ana kadar karşılaştığı fiziksel noktaları kapsar.',
                     'list': ['Şarj ünitesinin dış gövdesi ve ekranı',
                              'Kablo düzeni ve kablonun bırakıldığı konum',
                              'Park cebi, zemin ve çevre temizliği',
                              'Yönlendirme elemanları ve aydınlatma dış gövdesi',
                              'Marka unsurlarının görünürlüğü ve standarda uygunluğu',
                              'Kullanıcıyı etkileyen güvenlik riskleri']},
                    {'eyebrow': 'Skorlama',
                     'h2': 'Skor eşikleri ve yanıt süreleri.',
                     'lead': 'Skor, hangi lokasyona ne zaman müdahale edileceğini netleştirir. Bulgular önem derecesine göre farklı sürelerle bildirilir ve aksiyona bağlanır.',
                     'list': ['90 ve üzeri: Uygun.',
                              '75–89: Takip.',
                              "75'in altı: Aksiyon.",
                              'Kritik bulgu: anlık bildirim. Güvenlik maddelerindeki uygunsuzluk aynı gün bildirim üretir.',
                              'Majör bulgu: 24 saat içinde aksiyona bağlanır.']},
                    {'eyebrow': 'Kanıt',
                     'h2': 'Fotoğraf seti: her noktada aynı altı kare.',
                     'lead': 'Şarj noktaları birbiriyle ancak aynı açılardan kayıt altına alınırsa karşılaştırılabilir. Her Audit30 ziyaretinde standart fotoğraf seti çekilir; kayıt GPS ve zaman '
                             'damgasıyla doğrulanır.',
                     'list': ['Ön görünüm', 'Sağ görünüm', 'Sol görünüm', 'Ekran', 'Kablo', 'Park alanı']},
                    {'eyebrow': 'Aksiyon',
                     'h2': 'Bulgudan sahaya: tespit, iş emri, kapanış.',
                     'lead': 'Denetim gözlemle bitmez. Audit30 bulguları BİGEL CARE iş emri akışına aktarılır; uygulama bölgesel ekiplerle yapılır ve sonrası fotoğrafıyla kapanır. Şarj '
                             'ünitesinin dış gövdesi, zemin, yönlendirme ve aydınlatma dış gövdesi gibi fiziksel işler CARE kapsamındadır. Ayrıntılar için şarj istasyonu bakımı sayfamıza '
                             'bakabilirsiniz.',
                     'steps': [('Saha', 'Eğitimli ekip, standart kontrol listesiyle inceler.'),
                               ('Veri', 'Puan, fotoğraf, GPS, tarih ve bulgu kaydedilir.'),
                               ('Karar', 'Bulgular öncelik ve sorumluluğa göre sınıflanır.'),
                               ('İş emri', 'Kapsam, sorumlu ve hedef tarih belirlenir.'),
                               ('Kapanış', 'Müdahale sonrası fotoğraf ve kalite kontrolüyle kapanır.')],
                     'links': [('Şarj istasyonu bakımı', 'ev_care', ''), ('BİGEL CARE', 'care', '')]},
                    {'eyebrow': 'Ağ yönetimi',
                     'h2': 'Tüm şarj noktaları tek ekranda.',
                     'lead': 'Lokasyonlar Türkiye haritası üzerinde skor rengiyle gösterilir. Bölgeden şehre, şehirden tek bir şarj noktasına inilir; skor kartı, fotoğraflar, bulgular ve aksiyon '
                             'geçmişi aynı yerde görülür. Ziyaretler FIELD360 ile planlanır, SLA hedefleri merkezden izlenir.',
                     'list': ['81 ile erişim, bölgesel saha ekipleri',
                              'Ortak kontrol listesi, fotoğraf açısı ve kapanış kuralı',
                              'Ortalama skor, kritik bulgu sayısı ve açık aksiyonlar',
                              'Planlanan, tamamlanan ve geciken ziyaretlerin takibi',
                              'Saha ekipleri kıyafet, kimlik, İSG ve dijital kayıt standardına göre değerlendirilir']},
                    {'eyebrow': 'Pilot',
                     'h2': 'Audit30 pilotu: 10 lokasyon, 2 hafta, 2 tur.',
                     'lead': 'Ağın tamamına geçmeden önce seçili lokasyonlarda başlangıç skorunu ölçer, bulguları kapatır ve ikinci turda gelişimi doğrularız.',
                     'steps': [('Kapsam toplantısı', '90 dakika. Lokasyon yapısı ve pilot başarı kriterleri.'),
                               ('Pilot planı', 'Lokasyon seti, fotoğraf kuralı, SLA ve takvim tek dokümanda.'),
                               ('Birinci tur', 'Başlangıç ölçümü; kritik bulgular aynı gün bildirilir.'),
                               ('İkinci tur', 'Aksiyonlar kapatılır, skor ve açık bulgu gelişimi doğrulanır.'),
                               ('Sonuç toplantısı', 'Skorlar, bulgular ve yaygınlaştırma planı.')],
                     'links': [('Pilot başvurusu', 'pilot', 'basvuru')]}],
       'faq': [('Şarj istasyonu denetiminde neler kontrol edilir?',
                'EV Audit30, 30 standart kontrolü altı alanda toplar: güvenlik, cihaz bütünlüğü, işlev işaretleri, kullanıcı deneyimi, temizlik ve çevre, marka standardı. Sahada ünitenin dış '
                'gövdesi, ekran, kablo düzeni, park cebi, zemin ve yönlendirme incelenir.'),
               ('EV Audit30 resmi denetimin yerini tutar mı?',
                'Hayır. EV Audit30 resmi bir denetim ya da elektriksel muayene değildir. Şarj noktalarınızın saha durumunu fotoğraflı, GPS ve zaman damgalı kayıtla belgeler; bu kayıt iç '
                'hazırlığınızı destekler.'),
               ('Çalışmayan veya sorunlu şarj noktaları sahada nasıl tespit edilir?',
                'Uzaktan izleme cihazın teknik durumunu gösterir; saha ekibi ise sürücünün gördüğü işlev işaretlerini, ekranı, kabloyu ve park alanını yerinde kontrol eder ve fotoğraflar. '
                'Uygunsuzluklar bulgu olarak kaydedilir ve önem derecesine göre bildirilir.'),
               ('Şarj noktası saha kalitesi nasıl skorlanır?',
                "Altı alan ağırlıklandırılır ve sonuç 100 üzerinden saha skoru olarak hesaplanır. 90 ve üzeri Uygun, 75–89 Takip, 75'in altı Aksiyon olarak sınıflanır."),
               ('Kritik bir bulguda ne kadar sürede bildirim yapılır?',
                'Kritik bulgular anlık bildirilir; güvenlik maddelerindeki uygunsuzluk aynı gün bildirim üretir. Majör bulgular 24 saat içinde aksiyona bağlanır.'),
               ('Audit30 pilotu nasıl işler?',
                'Pilot 10 lokasyonda, 2 hafta içinde, 2 tur olarak yürütülür. İlk turda başlangıç skoru çıkarılır, ikinci turda aksiyonların kapanışı ve skor gelişimi doğrulanır.'),
               ('Denetimde çıkan bulgular kim tarafından giderilir?',
                'Fiziksel bulgular BİGEL CARE iş emri akışıyla bölgesel ekiplere atanır ve sonrası fotoğrafıyla kapanır. Elektriksel bakım gerektiren işler yetkili uzmanlarla koordine edilir; '
                'BİGEL tespit, planlama ve kapanış takibini yönetir.')],
       'cta': {'h2': 'Şarj ağınızın saha skorunu ölçelim.',
               'p': '10 lokasyonda, 2 haftada, 2 turla başlayın. Başlangıç skoru, fotoğraflı bulgular ve yaygınlaştırma planı pilotun sonunda elinizde.',
               'b1': 'Audit30 Pilotu Başlat',
               'b2': 'İletişim'}},
  },
},
"en": {
  "meta_suffix": " | BİGEL",
  "nav": {"solutions": "Solutions", "sectors": "Industries", "tiers": "Plans", "how": "How We Work", "pilot": "Pilot Application", "about": "About", "cta": "Get a Quote", "menu": "Menu", "portal": "Portal Login"},
  "products": {
    "clean":    {"name": "BİGEL CLEAN", "cat": "Cleaning Operations", "tag": "The same standard at every site.", "short": "Planned exterior cleaning for canopies, signage, totems, façades and car parks. Verified with before and after photos."},
    "care":     {"name": "BİGEL CARE", "cat": "Maintenance Operations", "tag": "Protect the site before it breaks.", "short": "Minor maintenance, repairs and on-site response. One work-order flow from detection to photo-verified closure."},
    "audit":    {"name": "BİGEL AUDIT", "cat": "Audit & Quality", "tag": "See your standard in the field.", "short": "Brand, visual, cleanliness, physical condition and customer experience audits. Scored with AUDIT 100 and EV Audit30."},
    "field360": {"name": "BİGEL FIELD360", "cat": "Field Management Platform", "tag": "Your entire field, one control centre.", "short": "Cleaning, maintenance, audit and action under one contract, one standard and one reporting flow."},
  },
  "more": "View solution",
  "ui": {"home": "Home", "faq_eyebrow": "FAQ", "faq_h2": "Frequently asked questions", "rel_eyebrow": "Related pages", "rel_h2": "Related reading", "crumb_label": "Breadcrumb",
         "guides": "Guides", "guides_eyebrow": "Guides", "guides_h2": "Related guides", "published": "Published", "by": "By BİGEL",
         "short": {"fuel_clean": "Cleaning and maintenance", "fuel_audit": "Audit · AUDIT 100", "ev_care": "Maintenance and cleaning", "ev_audit": "Audit · EV Audit30"},
         "footer": {"fuel_clean": "Fuel station cleaning", "fuel_audit": "Fuel station audit", "ev_care": "EV charging station maintenance", "ev_audit": "EV charging station audit"}},
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
     ["Everything in BUSINESS", "FIELD360 single operations centre", "Visual area and furniture management", "Dedicated operations manager"]),
  ],
  "home": {
    "title": "Field Operations for Fuel, EV Charging and Retail Chains | BİGEL",
    "desc": "Cleaning, maintenance and audits across Türkiye for fuel and EV charging station networks and multi-site brands. Photo evidence and scores.",
    "eyebrow": "Corporate Field Operations",
    "h1": "Your Strength in the Field.",
    "lead": "We plan, execute and report the cleaning, maintenance and audit operations of multi-site brands across Türkiye, to one standard and with photo evidence.",
    "b1": "Explore Solutions", "b2": "Get a Quote",
    "sub": [("81", "provinces covered"), ("4", "products, one standard"), ("100", "criteria digital audit")],
    "card": {"loc": "Sample Site · Kadıköy / Istanbul", "meta": "Audit 12 Sep 2026 · Team MAR-04", "status": "Action required",
             "bars": [("Cleanliness", 94, "var(--green)"), ("Brand standard", 89, "var(--amber)"), ("Customer experience", 91, "var(--green)"), ("Technical condition", 72, "var(--red)"), ("Safety", 100, "var(--green)")],
             "foot_l": "3 open findings · <b>1 critical</b>", "foot_r": "Work order created"},
    "trust_eyebrow": "Why BİGEL", "trust_h2": "Local field power. Central operations. Measurable results.",
    "stats": [(SITE["provinces"], "provinces with local team access"), (SITE["regions"], "field teams"), (SITE["visits"], "planned site visits per month"), (SITE["photo_rate_en"], "mandatory photo verification rate")],
    "sol_eyebrow": "Solutions", "sol_h2": "Four products. One BİGEL standard.", "sol_lead": "Each product works on its own or combines in the same visit plan. All run on the same checklists, photo angles and closure rules.",
    "proof_eyebrow": "Proof", "proof_h2": "We don't just do the work. We measure it.",
    "proof_p": "Every visit produces photos, a checklist and a score. Findings become work orders, and closure is tracked with an owner and a due date.",
    "proof_list": ["Before and after photos with GPS and timestamp", "Question-level scores and red-amber-green status", "Action tracking with owner, due date and closure evidence", "Site, region and period comparisons"],
    "ba": [("01 Feb 2026", "Signage — Damaged", "Priority: High · Work order opened", "red", "Open"), ("01 Mar 2026", "Signage — Replaced", "After photo added · Confirmed by site manager", "green", "Closed")],
    "flow_eyebrow": "How we work", "flow_h2": "One chain of record from planning to closure.",
    "flow": [("Plan", "Site, task, team and SLA definition."), ("Execute", "Cleaning or maintenance to a standard procedure."), ("Audit", "Checklist, score and photos."), ("Report", "KPI, SLA and site score."), ("Act", "Work order, owner and closure evidence.")],
    "flow_more": "See the full process",
    "sec_eyebrow": "Industries", "sec_h2": "From fuel and EV charging stations to retail, for every multi-site brand.", "sec_more": "All industries",
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
         "list": ["Common service definition and application standard", "Central task and visit planning", "Fast site access through regional teams", "Before and after photo evidence", "Site and regional performance visibility"], "img": "station.jpg", "tag": "Canopy and forecourt cleaning · Fuel", "link": "fuel_clean"},
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
      "title": "BİGEL CARE — Site maintenance and field response",
      "desc": "Minor maintenance, repairs and field response managed from one centre across Türkiye. Detection, work order, execution and photo-verified closure.",
      "lead": "We manage the minor maintenance, repair and field response needs of brand sites from one centre. Detection, planning, on-site execution, photography and closure tracking are all handled by BİGEL.",
      "sections": [
        {"type": "split", "eyebrow": "Scope", "h2": "Small jobs get fixed before they pile up.", "p": "Small physical problems accumulating at sites hurt customer experience and brand appearance. BİGEL CARE manages them through a single work-order system.",
         "list": ["Periodic and preventive maintenance", "Fault and physical damage response", "Visual area and brand element care", "Exterior and surroundings care", "Furniture, equipment and minor assembly", "Emergency field response"], "img": "retail.jpg", "tag": "Furniture and display check · Retail",
         "note": "Work requiring specialist skills or legal certification (electrical, mechanical installations, etc.) is coordinated with qualified specialists; BİGEL manages detection, planning and closure tracking."},
        {"type": "modules", "eyebrow": "Service modules", "h2": "Ten modules, combined by industry.", "lead": "",
         "items": [("01", "Minor Works", "Tightening, fixing, handle and accessory replacement, sealant, spot painting."), ("02", "Sign Care", "Signage, totem and wayfinding maintenance."), ("03", "Exterior Care", "Façade, entrance and outdoor area maintenance."), ("04", "Visual Care", "Visual areas and brand elements."), ("05", "Furniture Care", "Furniture and display elements."), ("06", "Pavement Care", "Floors, kerbs and car park maintenance."), ("07", "Site Care", "Site physical condition management."), ("08", "Preventive Care", "Periodic preventive maintenance."), ("09", "Emergency Care", "Emergency field response."), ("10", "Field Audit", "Photo-verified inspection and action report.")]},
        {"type": "flow", "eyebrow": "Workflow", "h2": "From request to photo-verified closure.", "steps": [("Request", "One channel: request or audit finding."), ("Photo assessment", "Damage type, priority and proposed action."), ("Task approval", "Scope, owner and due date."), ("Field intervention", "Standard execution by the regional team."), ("Closure report", "After photo and quality check.")]},
        {"type": "cards3", "eyebrow": "Industry packages", "h2": "Built around each industry's physical spaces.", "items": [("Station Care", "Fuel stations: canopy, signage, pump islands, kerbs, barriers and surroundings.", "fuel_clean"), ("EV Charge Care", "Charger housing, floor, wayfinding and light fittings. Electrical maintenance by certified specialists.", "ev_care"), ("Restaurant Care", "Façade, signage, outdoor seating, drive-thru and minor interior works."), ("Auto & ATM Care", "Showroom façade and display platforms; ATM cabins, branch entrances and counters."), ("Retail & Mall Care", "Shelving, display units, shopfront frames; mall wayfinding, seating and seasonal décor."), ("Logistics & Facility Care", "Warehouse façade, floor markings, barriers; hotel, school and factory entrances.")]},
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
         "badges": ["Mandatory photo and GPS", "Instant alert on critical findings", "Site scorecard", "JSON / PDF report"], "more": "fuel_audit"},
        {"type": "sub", "id": "ev", "logo": None, "eyebrow": "For charging networks", "h2": "Charging point field quality audit.",
         "p": "Remote monitoring shows the device's technical state; Audit30 makes the physical site conditions your customers actually meet visible. 30 standard checks, 6 weighted areas, a site score out of 100. Safety non-conformities trigger a same-day alert; major findings are actioned within 24 hours.",
         "weights": [("Safety · 5 critical checks", 25), ("Device integrity", 20), ("Function indicators", 20), ("User experience", 15), ("Cleanliness & surroundings", 10), ("Brand standard", 10)],
         "thresholds": [("g", "≥ 90 · Compliant"), ("a", "75–89 · Follow-up"), ("r", "< 75 · Action")],
         "badges": ["Photo set: front, right, left, screen, cable, bay", "Critical: instant · Major: 24 hours", "Pilot: 10 sites, 2 weeks, 2 rounds"], "more": "ev_audit"},
        {"type": "map", "eyebrow": "BİGEL Map", "h2": "All sites on one map.", "p": "Sites are shown on a map of Türkiye in their score colour. Users drill from region to city to site and see the scorecard, photos, findings and action history.",
         "legend": [("var(--green)", "90–100 · Meets standard"), ("var(--amber)", "75–89 · Improvement needed"), ("var(--red)", "0–74 · Priority action")],
         "kpis": [("Site count by region and city"), ("Average audit score and critical finding count"), ("Completed, pending and open actions")]},
        {"type": "cards3", "eyebrow": "Service models", "h2": "From a single audit to a continuous platform.", "items": [("Site-based audit", "One-off audit at selected sites."), ("Periodic audit", "Monthly, quarterly, semi-annual or annual recurring programme."), ("Project audit", "Bulk check after campaigns, openings or signage changes."), ("Franchise audit", "Measuring standard compliance across a franchise network on behalf of head office."), ("Investment & handover", "Documenting physical condition before purchase, lease or handover."), ("Platform & dashboard", "Continuous tracking of scores, photos, findings, work orders and closures.")],
         "note": "Quotes are based on number of sites, question count, photo requirements, travel, audit frequency, report format and dashboard scope."},
      ]},
    "field360": {
      "title": "BİGEL FIELD360 — End-to-end field operations",
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
  "sectors": {"title": "Industries — Fuel, EV Charging and Multi-site Brands", "desc": "Field services for fuel and EV charging stations, restaurants, retail, banking, automotive, logistics, malls, hotels, telecom, education and facilities.",
              "eyebrow": "Industries", "h1": "From fuel and EV charging stations to retail, every industry where the field standard is managed centrally.", "lead": "Service scope adapts to each industry's surfaces and operating hours. Below are the priority areas for each industry.",
              "fr_eyebrow": "Franchise networks", "fr_h2": "One contract with head office, one standard across every branch.", "fr_p": "Franchisee execution becomes visible, measurable and centrally manageable.",
              "fr_list": ["One contract and one service definition with head office", "A common checklist for all sites", "Planned site visits by regional teams", "Site-level scores and non-conformity tracking", "Comparative dashboard for head office"],
              "fit_eyebrow": "Solution by need", "fit_h2": "Which product for which situation?",
              "fit": [("Multi-site cleaning", "Periodic CLEAN programme", "clean"), ("Minor maintenance piling up", "CARE response plan", "care"), ("Measuring brand standard", "AUDIT and AUDIT 100", "audit"), ("Charging network site quality", "EV Audit30", "ev_audit"), ("Scattered supplier base", "One centre with FIELD360", "field360"), ("Need for photo evidence", "Digital visit report", "field360")]},
  "tiers": {"title": "Plans — BASIC, PRO, BUSINESS, 360", "desc": "BİGEL subscription plans: from essential control to fully integrated field management. Pricing based on site count and scope.",
            "eyebrow": "Plans", "h1": "Four plans that scale with your needs.", "lead": "The plan name is the second tier; the BİGEL standard, photo evidence and reporting are the same in every plan. Pricing is based on site count, regional spread, service frequency and scope.",
            "badge": "Most complete", "cta": "Get a Quote", "cmp_h2": "Plan comparison",
            "cmp_head": ["Scope", "BASIC", "PRO", "BUSINESS", "360"],
            "cmp_rows": [["Periodic inspection visit", 1,1,1,1], ["Photo-verified site report", 1,1,1,1], ["Findings and priority list", 1,1,1,1], ["Minor maintenance response (CARE)", 0,1,1,1], ["Work orders and photo-verified closure", 0,1,1,1], ["Planned cleaning programme (CLEAN)", 0,0,1,1], ["Periodic AUDIT 100 audits", 0,0,1,1], ["Management dashboard, KPI / SLA", 0,0,1,1], ["Priority support line", 0,0,1,1], ["FIELD360 single operations centre", 0,0,0,1], ["Dedicated operations manager", 0,0,0,1]],
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
  "about": {"title": "About — Corporate field operations", "desc": "BİGEL is a new-generation field services platform that runs, audits and reports the field operations of corporate brands.",
            "eyebrow": "About", "h1": "Not a company that sends a handyman. A partner you can trust with your field operation.",
            "lead": "BİGEL is a new-generation field services platform that runs, audits and reports the field operations of corporate brands. It combines local field power with central operations, audit and reporting.",
            "story_h2": "Born in the field, grown with a system.",
            "story": ["BİGEL's journey began in Istanbul in 2018 with exterior cleaning and minor maintenance for fuel station networks. As the number of sites grew, so did the problem: doing the work was not enough; every site had to hold the same standard, and head office needed proof.", "Today BİGEL manages its regional team network with central planning, standard checklists and photo-verified digital reporting. CLEAN, CARE, AUDIT and FIELD360 run under one roof, on one chain of record.", "Years of field experience remain the source of our know-how; the BİGEL brand focuses on corporate field operations and technology."],
            "facts": [("45", "provinces"), ("60", "teams"), (SITE["provinces"], "provinces within reach"), ("4", "products, one chain of record")],
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
              "info": [("Head office", SITE["address_en"]), ("Phone", SITE["phone"]), ("Email", SITE["email"]), ("LinkedIn", "linkedin.com/company/bigel360"), ("Working hours", "Weekdays 09:00–18:00")]},
  "pilot": {"title": "Pilot Programme — 20–30 sites in 4–6 weeks", "desc": "A 4–6 week pilot on 20–30 sites: baseline measurement, photo-verified findings, site scores and a roll-out plan. Apply for a pilot.",
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
  "portal": {"title": "Customer Portal", "desc": "BİGEL customer portal: open requests and follow your field work and photo-verified reports. Contact us for early access.", "h1": "The customer portal is coming soon.", "p": "Through the BİGEL portal you will be able to open requests and follow your field work and photo-verified reports in real time. Contact us for early access.", "b1": "Contact us", "b2": "Back to home"},
  "thanks": {"title": "Thank you", "badge": "Request received", "h1": "Thank you, we'll be in touch.", "p": "Your details have reached our operations team. We will contact you within the same business day.",
             "steps_h": "What happens next", "steps": [("We have your request", "Your details are in front of our team."), ("We call you", "Within the same business day, weekdays 09:00–18:00."), ("We define the scope", "A quote or pilot plan shaped around your sites.")],
             "b": "Back to home", "b2": "See how we work", "urgent": "Urgent? Reach us now:"},
  "landings": {
    "fuel_clean": {'title': 'Fuel Station Cleaning and Maintenance',
       'desc': 'Canopy, totem, pump island, forecourt and car park cleaning plus kerb, barrier and minor repairs. One standard across Türkiye, photo-verified.',
       'crumb': 'Fuel Station Cleaning and Maintenance',
       'service': 'Fuel station cleaning and maintenance',
       'eyebrow': 'Fuel Stations · CLEAN + CARE',
       'h1': 'Fuel station cleaning and maintenance, to the same standard at every site.',
       'lead': 'We plan cleaning and minor maintenance for canopies, totems, pump islands, forecourts, car parks and station surroundings across Türkiye to one standard. Every visit comes from a '
               'central task plan and closes with before and after photos, GPS and a timestamp.',
       'b1': 'Start a Pilot',
       'b2': 'Get a Quote',
       'sections': [{'eyebrow': 'Scope',
                     'h2': 'What does fuel station cleaning cover?',
                     'lead': 'BİGEL CLEAN covers the customer-facing exterior of the station with a defined method, equipment and photo angle for each area. Modules can be one-off or part of a '
                             'periodic programme.',
                     'cards': [('Fuel station canopy cleaning', 'Periodic removal of atmospheric dirt, dust, exhaust marks, soot and biological soiling from the canopy ceiling and fascia.'),
                               ('Totem and price sign cleaning', 'Surface-appropriate cleaning of totems, signage and wayfinding, so the brand stays visible from the road.'),
                               ('Pump island and forecourt cleaning',
                                'Dirt, oil stains and litter on concrete and asphalt around pump islands and across the forecourt, all tied to one checklist.'),
                               ('Façade, glass and car park',
                                'Entrance glass, curtain walls, composite and metal surfaces on the station building and shop front; dirt and oil stains on car park surfaces.'),
                               ('Night, emergency and seasonal cleaning',
                                'Night Clean is scheduled after closing without disrupting operations. Emergency Clean handles spills, bad weather, vandalism and pre-audit needs; Seasonal Clean '
                                'targets winter grime, leaves, mud and slip risks.')]},
                    {'eyebrow': 'Station maintenance · Station Care',
                     'h2': 'Small defects are closed before they pile up.',
                     'lead': 'The Station Care package of BİGEL CARE brings minor maintenance and repairs on canopies, signage, pump islands, kerbs, barriers and station surroundings into one '
                             'work-order flow. One channel replaces calling separate tradespeople.',
                     'steps': [('Detection', 'Photo-verified assessment: damage type, priority and proposed action.'),
                               ('Work order', 'Scope, owner and due date approved.'),
                               ('Execution', 'Standard execution by a regional team.'),
                               ('Photo-verified closure', 'After photo and quality check.')],
                     'list': ['Minor Works: tightening, fixing, sealant, spot painting and accessory replacement',
                              'Sign Care: signage, totem and wayfinding maintenance',
                              'Pavement Care: floors, kerbs and car park maintenance',
                              'Preventive Care: periodic maintenance before things break',
                              'Emergency Care: emergency field response'],
                     'note': 'Work requiring specialist skills or legal certification (electrical, mechanical installations, etc.) is coordinated with qualified specialists; BİGEL manages '
                             'detection, planning and closure tracking.'},
                    {'eyebrow': 'Site safety',
                     'h2': 'Orderly, safe work on a site that never stops.',
                     'lead': "At a fuel station, cleaning and maintenance happen while customers keep coming. Visit plans are built around the station's operating pattern, and safety items are "
                             'scored separately in the audit.',
                     'list': ['Visit hours, access conditions and target times are agreed during scope and SLA definition',
                              'Method, equipment and chemical use follow the standard operating procedure',
                              'Teams are trained to a common service standard and assessed on uniform, ID and safety standards',
                              'Rapid response to spills and sudden soiling with Emergency Clean',
                              'Seasonal Clean programme against slip risk in winter',
                              'In AUDIT 100, Safety & Risk carries a 15% weight; critical findings trigger an instant alert']},
                    {'eyebrow': 'Multi-site networks',
                     'h2': 'More stations, the same cleaning standard.',
                     'lead': "BİGEL's journey began with exterior cleaning and minor maintenance for fuel station networks. The lesson was clear: doing the work is not enough; every site has to "
                             'hold the same standard, and head office needs proof.',
                     'list': ['One service definition, checklist and execution standard for every station',
                              'Central task and visit planning; monthly, bi-monthly, quarterly or seasonal programmes',
                              'Standard photo angles and quality criteria',
                              'Performance visibility by site, region and period',
                              'On-time visits, completion rate and action closure time tracked through KPIs and SLAs']},
                    {'eyebrow': 'Evidence and reporting · FIELD360',
                     'h2': 'Work done in the field, visible at head office.',
                     'lead': 'Every visit follows the same digital flow and lands in one chain of record in FIELD360.',
                     'steps': [('Task scope', 'Site details and defined service.'),
                               ('Before photo', 'Baseline record from standard angles.'),
                               ('Execution', 'Method, equipment and chemical standard.'),
                               ('After photo', 'Checklist and quality criteria.'),
                               ('Completion', 'Finding report and closure record.')],
                     'list': ['Before and after photos, GPS and timestamp',
                              'Visits verified by location, date, team and photo',
                              'Visits, scores, open findings, work orders and closure evidence on one screen',
                              'SLA tracking of planned, completed and delayed visits'],
                     'links': [('BİGEL FIELD360', 'field360', '')]},
                    {'eyebrow': 'Cleaning + maintenance + audit',
                     'h2': 'One loop from cleaning to audit.',
                     'lead': 'AUDIT 100 scores the station across 10 categories and 100 checkpoints. It is a brand, visual standard and site condition audit. Each finding becomes a CARE work '
                             'order, and its closure is verified with a photo.',
                     'steps': [('Field', 'Trained team inspects with a standard checklist.'),
                               ('Data', 'Score, photo, GPS, date and finding recorded.'),
                               ('Centre', 'Stations compared on one dashboard.'),
                               ('Decision', 'Findings classified by priority and owner.'),
                               ('Work order', 'Action created, executed and closed with a photo.')],
                     'list': ['Each item scores Compliant 100, Partial 50 or Non-compliant 0',
                              'Category weights produce a station score out of 100',
                              '90–100 compliant · 75–89 improvement needed · 0–74 priority action',
                              'BİGEL Map shows every station on a map of Türkiye in its score colour'],
                     'links': [('Fuel station audit', 'fuel_audit', '')]},
                    {'eyebrow': 'How to start',
                     'h2': 'Start with 20–30 stations, scale on results.',
                     'lead': 'The pilot runs for 4–6 weeks over two visit rounds. At the end you hold baseline scores, photo-verified findings and a roll-out plan built on real field data.',
                     'steps': [('Scope and criteria', 'Station set, question set and score weights approved.'),
                               ('Baseline', 'Current condition recorded with photos and checklists.'),
                               ('Field execution', 'CLEAN, CARE or AUDIT delivered by regional teams.'),
                               ('Second round', 'Actions closed, score progress verified.'),
                               ('Roll-out', 'Scaling plan with SLAs, regions and calendar.')],
                     'list': ['BASIC: periodic checks and a photo-verified site report',
                              'PRO: checks plus minor maintenance, work orders and photo-verified closure',
                              'BUSINESS: planned CLEAN programme, periodic AUDIT 100, KPI/SLA reporting',
                              '360: FIELD360 single operations centre and a dedicated operations manager'],
                     'note': 'Pricing depends on site count, area and surface type, visit frequency, equipment needs and access conditions. The pilot finalises the unit price.',
                     'links': [('Subscription plans', 'tiers', '')]}],
       'faq': [('What does fuel station cleaning cover?',
                'Canopy ceiling and fascia, totems and signage, pump islands and forecourt, building façade and glass, car park and station surroundings. Scope is defined per station with a '
                'checklist.'),
               ('Can canopy and totem cleaning be done while the station is open?',
                "Visit hours and access conditions are set around the station's operating pattern during scoping. Where needed, Night Clean is scheduled after closing without disrupting "
                'operations.'),
               ('How often should forecourts and pump islands be cleaned?',
                'Frequency is set as a monthly, bi-monthly, quarterly or seasonal programme based on traffic and surface condition. Emergency Clean covers sudden spills and soiling; the final '
                'frequency is confirmed with pilot data.'),
               ('Do we need to call separate tradespeople for minor repairs?',
                'No. Station Care brings minor work on canopies, signage, pump islands, kerbs and barriers into one work-order flow. Work requiring legal certification, such as electrical or '
                'mechanical installations, is coordinated with qualified specialists while BİGEL keeps tracking it.'),
               ('How is completed cleaning and maintenance verified?',
                'Every visit is recorded with before and after photos, GPS and a timestamp and verified against the checklist and mandatory photos. All records are tracked per station in '
                'FIELD360.'),
               ('How do you keep one cleaning standard across many stations?',
                'Every station works to the same service definition, checklist and photo angles; visits are planned centrally and delivered by regional teams reaching all 81 provinces. Results '
                'are compared by site and region.'),
               ('How are audit findings closed?',
                'An AUDIT 100 finding becomes a CARE work order with a priority, owner and due date. It closes with an after photo, and the second visit verifies score progress.')],
       'cta': {'h2': "Let's define a pilot scope for your station network.",
               'p': 'See baseline scores and open findings on 20–30 stations in 4–6 weeks. Fill in the form and we will respond within the same business day.',
               'b1': 'Start a Pilot',
               'b2': 'Get a Quote'}},
    "fuel_audit": {'title': 'Fuel Station Brand Standards Audit — AUDIT 100',
       'desc': 'Brand standards audit for fuel station networks: visual, cleanliness, physical condition and customer experience. 100 criteria, photo evidence, one score.',
       'crumb': 'Fuel Station Audit',
       'service': 'Fuel station brand and site standard audit',
       'eyebrow': 'Fuel Stations · AUDIT 100',
       'h1': 'Fuel station audit: 100 criteria, one score.',
       'lead': 'We make brand standard, visual execution, cleanliness, physical condition and customer experience measurable at every station in your network. Each station is audited with the '
               'same checklist, verified with photos and scored out of 100.',
       'b1': 'Start an AUDIT 100 Pilot',
       'b2': 'Get a Quote',
       'sections': [{'eyebrow': 'Scope',
                     'h2': 'How it differs from regulatory inspections',
                     'lead': 'Fuel quality, measuring instruments and licence compliance are inspected by the competent authorities; BİGEL does not carry out those inspections. AUDIT 100 looks '
                             'at everything a customer sees and experiences at the station. It does not replace official inspections; it complements them.',
                     'list': ['Brand and visual standard: logo, corporate colours, current signage, campaign material and price communication',
                              'Cleanliness: forecourt, pump islands, glass and façade, car park, waste area and common areas',
                              'Physical condition: barriers, kerbs, railings, doors, furniture and minor damage',
                              'Customer experience: visibility, entrance, wayfinding, checkout and waiting area']},
                    {'eyebrow': 'Audit categories',
                     'h2': 'What is checked at the station?',
                     'lead': "The five BİGEL AUDIT modules are adapted to the station's physical layout. The question set and score weights are approved with you before the pilot.",
                     'list': ['Brand Audit: brand elements on the canopy and totem, corporate colours, campaign material and price communication (BRAND SCORE)',
                              'Visual Audit: signage, totem and price board, illuminated letters, vinyl, posters, shop window and digital screens',
                              'Clean Audit: forecourt surface, pump islands, canopy, glass and façade, car park and waste area; colour-coded summary',
                              'Physical Audit: damage to barriers, kerbs, railings, doors and furniture; findings become maintenance work orders',
                              'Customer Experience Audit: visibility from the road, entry and exit wayfinding, shop entrance, checkout and waiting area (CX SCORE)']},
                    {'eyebrow': 'AUDIT 100 scoring model',
                     'h2': 'How is the score calculated?',
                     'lead': '10 categories, 100 checkpoints. Each item scores Compliant (100), Partial (50) or Non-compliant (0); category weights produce a station score out of 100. We publish '
                             'the model openly, so it is always clear what the score is based on.',
                     'weights': 'audit100'},
                    {'eyebrow': 'Safety',
                     'h2': 'At a fuel station, safety comes first.',
                     'lead': 'A fuel station leaves little room for risk. That is why Safety & Risk carries the highest weight in AUDIT 100, and critical findings do not wait for the report.',
                     'list': ['Safety & Risk makes up 15% of the score',
                              'Instant alert on critical findings, without waiting for the report',
                              'Findings are prioritised as critical, high, medium or low',
                              'Field teams are assessed against uniform, ID, occupational health and safety and digital record standards',
                              'Work requiring legal authorisation, such as electrical or mechanical installations, is coordinated with qualified specialists; BİGEL manages detection, planning '
                              'and closure tracking']},
                    {'eyebrow': 'Evidence and reporting',
                     'h2': 'Every finding is backed by a photo, every visit by a location.',
                     'lead': 'Each item is recorded with a photo, location, date and note. The photo rule is defined per question: conditional, mandatory or before-and-after.',
                     'list': ['Visits verified with mandatory photos and GPS',
                              'Station scorecard with a red-amber-green status summary',
                              'JSON / PDF report',
                              'BİGEL Map: every station on a map of Türkiye in its score colour; drill down from region to city to station',
                              'Station, region and period comparisons']},
                    {'eyebrow': 'Action',
                     'h2': 'From finding to work order',
                     'lead': "An audit doesn't end with a report. Findings are classified by priority and owner; minor maintenance is resolved on site with BİGEL CARE, cleaning needs with BİGEL "
                             'CLEAN, and closure is verified with a photo.',
                     'steps': [('Field', 'A trained team inspects the station with a standard checklist.'),
                               ('Data', 'Score, photo, GPS, date and findings recorded.'),
                               ('Centre', 'Stations compared on a single dashboard.'),
                               ('Decision', 'Findings classified by priority and owner.'),
                               ('Work order', 'Action created, executed, closed with photo.')],
                     'links': [('BİGEL CARE', 'care', ''), ('BİGEL CLEAN', 'clean', '')]},
                    {'eyebrow': 'Service models',
                     'h2': 'From a single audit to a continuous programme.',
                     'lead': 'Quotes are based on the number of stations, question count, photo requirements, travel, audit frequency, report format and dashboard scope.',
                     'list': ['Site-based audit: one-off audit at selected stations',
                              'Periodic audit: monthly, quarterly, semi-annual or annual programme',
                              'Project audit: bulk check after campaigns, openings or signage changes',
                              'Franchise and dealer audit: measuring standard compliance across the dealer network on behalf of head office',
                              'Investment and handover: documenting physical condition before purchase, lease or handover']},
                    {'eyebrow': 'Field network',
                     'h2': 'Your whole station network, one standard.',
                     'lead': 'BİGEL started with field work for fuel station networks. Today central planning and quality control run from Istanbul, while audits are carried out by regional '
                             'teams.',
                     'list': ['Local team network reaching all 81 provinces',
                              'Shared checklist, photo angles and closure rules',
                              'Audit, cleaning and maintenance under one contract, one standard and one report with FIELD360']},
                    {'eyebrow': 'Pilot',
                     'h2': 'Measure selected stations first.',
                     'lead': '20–30 sites, 4–6 weeks, two visit rounds: baseline and verification. At the end of the pilot you have station scores, a photo-backed findings list and a roll-out '
                             'plan.',
                     'list': ['Audit summary and category scores',
                              'Photo-backed findings list: critical, high, medium, low',
                              'Site and region comparison',
                              'Estimated workload, visit frequency and implementation calendar']}],
       'faq': [('What is a dealer standards audit, and how does it differ from a regulatory inspection?',
                "A dealer standards audit measures whether a station meets head office's standard for brand, visual execution, cleanliness, physical condition and customer experience. Fuel "
                'quality, measuring instruments and licensing are inspected by the competent authorities; BİGEL does not do those inspections and instead provides a complementary site standards '
                'audit.'),
               ('What is checked in a fuel station audit?',
                'Brand elements on the canopy and totem, signage and price board, cleanliness of the forecourt and pump islands, physical elements such as barriers, kerbs and railings, plus the '
                'shop entrance, checkout and wayfinding. AUDIT 100 measures these across 10 categories and 100 checkpoints; the question set is approved with you before the pilot.'),
               ('How are audit results scored and reported?',
                'Each item scores Compliant 100, Partial 50 or Non-compliant 0, and category weights produce a station score out of 100. 90–100 means the station meets standard, 75–89 needs '
                'improvement and 0–74 requires priority action. Results are tracked through the station scorecard, JSON / PDF reports and BİGEL Map.'),
               ('How do audit findings turn into action?',
                'Findings are classified by priority and owner, turned into work orders and tracked against a target date. Minor maintenance is resolved with BİGEL CARE and cleaning needs with '
                'BİGEL CLEAN; closure is verified with a photo.'),
               ('How often should stations be audited?',
                'Periodic programmes can be monthly, quarterly, semi-annual or annual. A project audit can also be run after a campaign, opening or signage change. The right frequency is agreed '
                'with you based on pilot results.'),
               ('What happens if a critical safety finding is found?',
                'Safety & Risk is the highest-weighted category in AUDIT 100 (15%). A critical finding triggers an instant alert without waiting for the report and is linked to a work order as a '
                'priority action.'),
               ('Our stations also have EV chargers. How are they audited?',
                'Charging points are audited with EV Audit30: 30 standard checks, 6 weighted areas and a site score out of 100. The fuel forecourt and the chargers can be audited together in the '
                'same visit plan.')],
       'cta': {'h2': 'Start an AUDIT 100 pilot for your station network.',
               'p': "Let's measure baseline scores at selected stations in a 4–6 week pilot, then plan a regional or nationwide programme together based on the results.",
               'b1': 'Start an AUDIT 100 Pilot',
               'b2': 'Contact'}},
    "ev_care": {'title': 'EV Charging Station Site Maintenance and Cleaning',
       'desc': 'Site upkeep for EV charging stations: charger housing, cable management, bays, floor and wayfinding. Electrical maintenance by certified specialists.',
       'crumb': 'EV Charging Station Maintenance',
       'service': 'EV charging station site maintenance and cleaning',
       'eyebrow': 'EV Charging Stations · CLEAN + CARE',
       'h1': 'EV charging station site maintenance and cleaning.',
       'lead': "Remote monitoring shows you the device's technical state. Only a team on site can keep up the conditions drivers actually see. BİGEL maintains charger housings, cable management, "
               'bays, floors and wayfinding to one standard across your entire network, with planning, execution and photo-verified reporting run from a single centre.',
       'b1': 'Apply for a Pilot',
       'b2': 'Get a Quote',
       'sections': [{'eyebrow': 'Scope',
                     'h2': 'Site and visual upkeep: everything the driver sees.',
                     'lead': 'A charge point experience depends on more than whether the device works. A clean, intact unit, a cable that is not left on the ground, a bay that is clear and easy '
                             'to read and wayfinding that is visible from the car all shape the same experience. The EV Charge Care package of BİGEL CARE covers this area.',
                     'list': ['Charger housing and screen surface',
                              'Cable management: cable and connector kept off the ground',
                              'Bay, floor, kerbs and car park surface',
                              'Wayfinding and signage elements',
                              'Light fitting housings',
                              'Charger surroundings and site exterior']},
                    {'eyebrow': 'Out of scope',
                     'h2': "We don't do electrical maintenance, and we say so up front.",
                     'lead': 'Electrical maintenance, periodic inspection and calibration of chargers require legal authorisation and specialist expertise, so certified specialists carry them '
                             'out. BİGEL does not replace that work. It complements it: we record what we see on site, coordinate specialist work with the right specialists, and manage the '
                             'planning and closure tracking.',
                     'list': ['No work inside the unit or on electrical components',
                              'Physical findings on site are recorded with photos',
                              'Work that needs authorisation is coordinated with the right specialists',
                              'Detection, planning and closure tracking are handled by BİGEL']},
                    {'eyebrow': 'BİGEL CLEAN',
                     'h2': 'EV charger cleaning: unit, screen, floor and bay.',
                     'lead': 'Charging sites are outdoors, so dust, rain, mud and winter grime quickly build up on housings and floors. Cleaning follows a common checklist and standard procedure '
                             'approved at the scoping stage, with methods suited to each surface.',
                     'list': ['Cleaning of charger housings and screen surfaces',
                              'Surface-appropriate cleaning of signs, totems and wayfinding',
                              'Dirt, oil stains and litter removed from floors and bays',
                              'Cables and connectors left in their proper place',
                              'Seasonal programme for winter grime, leaves and mud',
                              'Rapid response after sudden soiling, vandalism or bad weather']},
                    {'eyebrow': 'BİGEL CARE workflow',
                     'h2': 'Detection, work order, photo-verified closure.',
                     'lead': 'Every issue found on site follows a single work order flow. Each charge point is recorded with the same photo set: front, right, left, screen, cable and bay. That '
                             'keeps sites and periods comparable from the same angles.',
                     'steps': [('Request', 'One channel: operator request or audit finding.'),
                               ('Photo assessment', 'Damage type, priority and recommended action.'),
                               ('Task approval', 'Scope, owner and due date.'),
                               ('Field response', 'Standard execution by a regional team.'),
                               ('Closure report', 'After photo and quality check.')]},
                    {'eyebrow': 'EV Audit30',
                     'h2': 'Measure site quality with EV Audit30.',
                     'lead': 'You have to measure upkeep to see its effect. EV Audit30 runs 30 standard checks at the charge point, grouped into 6 weighted areas, and produces a site score out '
                             'of 100. A score of 90 or above is compliant, 75–89 needs follow-up and below 75 needs action. Safety non-conformities trigger a same-day alert, and major findings '
                             'are actioned within 24 hours. See the charging station audit page for details.',
                     'list': ['Safety, 5 critical checks: 25%',
                              'Device integrity: 20%',
                              'Function indicators: 20%',
                              'User experience: 15%',
                              'Cleanliness & surroundings: 10%',
                              'Brand standard: 10%'],
                     'links': [('Explore the charging station audit', 'ev_audit', '')]},
                    {'eyebrow': 'FIELD360',
                     'h2': 'One standard across the whole network.',
                     'lead': 'Charging networks are often many small sites spread across cities and highways. FIELD360 runs the network from one centre, with the same checklists, photo angles, '
                             'quality criteria and closure rules at every site.',
                     'list': ['Central task and visit planning',
                              'Regional team network reaching all 81 provinces',
                              'Visits verified by location, time, checklist and photos',
                              'Monthly, bi-monthly, quarterly or seasonal visit programme',
                              'Jointly defined KPI and SLA targets',
                              'One dashboard by site, region and period']}],
       'faq': [('What does EV charging station maintenance cover? Is electrical maintenance included?',
                'BİGEL covers site and visual upkeep: charger housing, screen surface, cable management, bays, floor, wayfinding and light fitting housings. Electrical maintenance, periodic '
                'inspection and calibration are not included and are carried out by certified specialists. BİGEL handles detection, planning and closure tracking for that work.'),
               ('How is an EV charging station cleaned?',
                'Cleaning follows the checklist and standard procedure approved at the scoping stage. Housings, screens, floors and bays are cleaned with methods suited to each surface. No work '
                'is done inside the unit or on its electrical components.'),
               ('What happens when charging cables are left on the ground, and how is cable management kept up?',
                'A cable left on the ground looks poor and is a hazard for people walking and cars manoeuvring. That is why the cable has its own shot in the mandatory photo set on every visit. '
                'Non-conformities are flagged as findings, and safety non-conformities trigger a same-day alert.'),
               ('How are charging bays and wayfinding monitored?',
                'Bays and wayfinding are photographed on every visit, and EV Audit30 scores them under user experience. Findings such as worn floor markings or damaged signs become CARE work '
                'orders tracked to a photo-verified closure.'),
               ('How is the maintenance work reported?',
                'Every visit is recorded with GPS, a timestamp, a checklist and photos. Work orders are tracked with an owner, due date and closure evidence. Head office sees all sites on one '
                'dashboard by site, region and period.'),
               ('How is visit frequency decided?',
                'Visit frequency is agreed with you based on what the network needs. It can be a monthly, bi-monthly, quarterly or seasonal programme. Rapid response can also be scheduled after '
                'sudden soiling, vandalism or bad weather.'),
               ('Can we try it before rolling out to the whole network?',
                'Yes. The Audit30 pilot for EV networks covers 10 sites over 2 weeks in 2 rounds. At the end you have baseline scores, photo-verified findings and action proposals.')],
       'cta': {'h2': 'Start with a pilot on your charging network.',
               'p': 'The Audit30 pilot covers 10 sites over 2 weeks in 2 rounds. Baseline scores, photo-verified findings and action proposals come together in one report.',
               'b1': 'Apply for a Pilot',
               'b2': 'Get a Quote'}},
    "ev_audit": {'title': 'EV Charging Station Audit — EV Audit30',
       'desc': 'Measure the site conditions EV drivers actually meet: 30 checks, 6 weighted areas, a score out of 100. Instant alerts on critical findings.',
       'crumb': 'EV Charging Station Audit',
       'service': 'EV charging station field audit',
       'eyebrow': 'EV Charging Stations · EV Audit30',
       'h1': 'EV charging station audit: a site score with EV Audit30.',
       'lead': "Remote monitoring shows the device's technical state; Audit30 makes the physical site conditions your customers actually meet visible. 30 standard checks, 6 weighted areas and "
               'one site score out of 100. Every charging point is recorded with the same photo set, and findings become work orders.',
       'b1': 'Start an Audit30 Pilot',
       'b2': 'Get a Quote',
       'sections': [{'eyebrow': 'Scope',
                     'h2': 'What it measures, and what it does not.',
                     'lead': 'A charger can look online in the monitoring dashboard while the driver on site faces a dirty screen, a cable lying on the ground or a bay blocked by another car. EV '
                             'Audit30 closes that gap by measuring the physical site quality drivers see, with a standard checklist.',
                     'list': ['Measures: charger surroundings, unit housing, screen, cable management, parking bay, floor, wayfinding and brand elements.',
                              'Measures: function indicators visible on site and conditions that affect the user experience.',
                              'Does not measure: electrical inspection, testing or internal diagnostics. Electrical work is coordinated with certified specialists.',
                              "Not a regulatory audit: EV Audit30 does not replace official inspections. It documents your network's site condition with photo-verified, time-stamped records that "
                              'support your internal preparation.']},
                    {'eyebrow': 'Check structure',
                     'h2': '30 checks, 6 weighted areas.',
                     'lead': 'Every site is inspected against the same 30 standard checks. Areas are weighted by their importance to drivers and to the brand; the result is a site score out of '
                             '100.',
                     'weights': 'ev'},
                    {'eyebrow': 'On site',
                     'h2': 'What the charging station checklist covers.',
                     'lead': 'The checklist follows the physical touchpoints a driver meets, from pulling into the bay to starting a charge.',
                     'list': ['Charger housing and screen',
                              'Cable management and where the cable is left',
                              'Parking bay, floor and surrounding cleanliness',
                              'Wayfinding and light fittings',
                              'Visibility and compliance of brand elements',
                              'Safety risks that affect users']},
                    {'eyebrow': 'Scoring',
                     'h2': 'Score thresholds and response times.',
                     'lead': 'The score tells you which site needs attention and when. Findings are reported and actioned on different timelines depending on severity.',
                     'list': ['90 and above: Compliant.',
                              '75–89: Follow-up.',
                              'Below 75: Action.',
                              'Critical findings: instant alert. Safety non-conformities trigger a same-day alert.',
                              'Major findings: actioned within 24 hours.']},
                    {'eyebrow': 'Evidence',
                     'h2': 'The photo set: the same six shots at every site.',
                     'lead': 'Charging points can only be compared if they are recorded from the same angles. Every Audit30 visit captures the standard photo set, verified with GPS and a time '
                             'stamp.',
                     'list': ['Front', 'Right side', 'Left side', 'Screen', 'Cable', 'Parking bay']},
                    {'eyebrow': 'Action',
                     'h2': 'From finding to fix: detection, work order, closure.',
                     'lead': 'An audit does not end at observation. Audit30 findings flow into the BİGEL CARE work-order process; regional teams carry out the work and close it with an after '
                             'photo. Physical work such as charger housing, floor, wayfinding and light fittings falls under CARE. See our EV charging station maintenance page for details.',
                     'steps': [('Field', 'A trained team inspects against the standard checklist.'),
                               ('Data', 'Score, photo, GPS, date and finding are recorded.'),
                               ('Decision', 'Findings are classified by priority and owner.'),
                               ('Work order', 'Scope, owner and due date are set.'),
                               ('Closure', 'Closed with an after photo and quality check.')],
                     'links': [('EV charging station maintenance', 'ev_care', ''), ('BİGEL CARE', 'care', '')]},
                    {'eyebrow': 'Network management',
                     'h2': 'Every charging point on one screen.',
                     'lead': 'Sites are shown on a map of Türkiye in their score colour. Drill down from region to city to a single charging point and see the scorecard, photos, findings and '
                             'action history in one place. Visits are planned in FIELD360 and SLA targets are tracked centrally.',
                     'list': ['Reach across 81 provinces with regional field teams',
                              'Shared checklist, photo angles and closure rules',
                              'Average score, critical finding count and open actions',
                              'Tracking of planned, completed and delayed visits',
                              'Field teams are assessed against uniform, ID, occupational health and safety and digital record standards']},
                    {'eyebrow': 'Pilot',
                     'h2': 'Audit30 pilot: 10 sites, 2 weeks, 2 rounds.',
                     'lead': 'Before rolling out across the network, we measure a baseline score at selected sites, close the findings and verify progress in a second round.',
                     'steps': [('Scoping meeting', '90 minutes. Site structure and pilot success criteria.'),
                               ('Pilot plan', 'Site set, photo rules, SLA and calendar in one document.'),
                               ('First round', 'Baseline measurement; critical findings reported the same day.'),
                               ('Second round', 'Actions are closed; score and open-finding progress verified.'),
                               ('Review meeting', 'Scores, findings and the roll-out plan.')],
                     'links': [('Pilot application', 'pilot', 'apply')]}],
       'faq': [('What is checked in an EV charging station audit?',
                'EV Audit30 groups 30 standard checks into six areas: safety, device integrity, function indicators, user experience, cleanliness and surroundings, and brand standard. On site, '
                'the team inspects the charger housing, screen, cable management, parking bay, floor and wayfinding.'),
               ('Does EV Audit30 replace an official inspection?',
                "No. EV Audit30 is neither an official inspection nor an electrical test. It documents your charging points' site condition with photo, GPS and time-stamped records that support "
                'your internal preparation.'),
               ('How are faulty or problematic charging points identified on site?',
                "Remote monitoring shows the device's technical state, while the field team checks and photographs the function indicators, screen, cable and bay that drivers see. "
                'Non-conformities are logged as findings and reported according to severity.'),
               ('How is charging point site quality scored?',
                'The six areas are weighted and combined into a site score out of 100. 90 and above is Compliant, 75–89 is Follow-up and below 75 is Action.'),
               ('How quickly are critical findings reported?',
                'Critical findings are alerted instantly; safety non-conformities trigger a same-day alert. Major findings are actioned within 24 hours.'),
               ('How does the Audit30 pilot work?',
                'The pilot runs on 10 sites over 2 weeks in 2 rounds. The first round sets the baseline score; the second verifies action closure and score progress.'),
               ('Who fixes the findings from the audit?',
                'Physical findings are assigned to regional teams through the BİGEL CARE work-order process and closed with an after photo. Electrical work is coordinated with certified '
                'specialists; BİGEL manages detection, planning and closure tracking.')],
       'cta': {'h2': "Let's measure your charging network's site score.",
               'p': 'Start with 10 sites, 2 weeks and 2 rounds. At the end of the pilot you hold baseline scores, photo-verified findings and a roll-out plan.',
               'b1': 'Start an Audit30 Pilot',
               'b2': 'Contact'}},
  },
},
}

# ---------------------------------------------------------------- MORE SECTOR LANDING PAGES
# Retail chains, bank branches / ATMs and restaurant chains. Same shape as CONTENT[lang]["landings"]; copy uses only
# facts already on the site (sector lines, CLEAN/CARE/AUDIT modules, pilot and plan facts). No customer names.
CONTENT["tr"]["landings"].update({
    "retail": {
        "title": "Zincir Mağaza Temizliği ve Bakımı — Vitrin, Tabela",
        "desc": "Zincir mağaza temizliği: vitrin, cam, cephe ve tabela tüm şubelerde tek standartta. Öncesi ve sonrası fotoğraf, şube skoru ve iş emri takibi.",
        "crumb": "Zincir Mağaza Temizliği ve Bakımı",
        "service": "Zincir mağaza dış alan temizliği ve bakımı",
        "eyebrow": "Perakende & Mağazacılık · CLEAN + CARE + AUDIT",
        "h1": "Zincir mağazalarda vitrin, cephe ve tabela her şubede aynı standartta.",
        "lead": "Zincir perakendede müşteri markayı önce vitrinden, girişten ve tabeladan tanır. Şubeden şubeye değişen bir mağaza önü marka algısını aşındırır. BİGEL işi merkezden planlar, "
                "bölgesel saha ekipleri uygular, sonuç her ziyarette öncesi ve sonrası fotoğrafla raporlanır.",
        "b1": "Pilot Başvurusu", "b2": "Teklif Al",
        "sections": [
            {"eyebrow": "Kapsam", "h2": "Zincir mağaza temizliği ne kapsar?",
             "lead": "BİGEL CLEAN, mağazanın dışarıdan görünen yüzlerine odaklanır: vitrin, giriş, cephe, tabela ve mağaza çevresi. Her alan için tanımlı yöntem, ekipman ve fotoğraf açısı vardır; "
                     "modüller tek seferlik uygulamaya ya da periyodik programa dahil edilebilir.",
             "cards": [("Vitrin ve giriş camı temizliği", "Cam ve Cephe Clean modülüyle vitrin ve giriş camları planlı ziyaret takviminde temizlenir. Mağaza cam temizliği her şubede aynı kontrol listesi ve aynı fotoğraf açısıyla kayda geçer."),
                       ("Dış cephe ve kompozit yüzeyler", "Cam cephe, kompozit, metal, taş ve boyalı yüzeylerde mağaza dış cephe temizliği, yüzey türüne uygun yöntemle yapılır."),
                       ("Tabela, ışıklı harf ve yönlendirme", "Tabela ve Totem Clean, marka görünürlüğünü etkileyen tabela, totem ve yönlendirme elemanlarını yüzeye uygun şekilde temizler."),
                       ("Giriş ve mağaza çevresi zemini", "Mağaza girişinin ve çevresinin dış zemini, Zemin ve Otopark Clean kapsamında kir ve leke açısından ele alınır."),
                       ("Kapanış sonrası ve acil müdahale", "Night Clean, mağazanın çalışma düzenini etkilemeden kapanış sonrasına planlanır. Ani kirlenme, kötü hava, vandalizm veya denetim öncesi durumlarda Emergency Clean devreye girer.")],
             "note": "Hizmet kapsamı, mağazanın yüzeylerine ve çalışma saatlerine göre uyarlanır. Bu sayfa dış alan ve mağaza önü hizmetlerini anlatır.",
             "links": [("BİGEL CLEAN", "clean", "")]},
            {"eyebrow": "Mağaza bakımı", "h2": "Perakende mağaza bakımı: Retail Care.",
             "lead": "Mağazada biriken küçük fiziksel sorunlar, temizlik kadar marka görünümünü etkiler. BİGEL CARE'in Retail & AVM Care paketi raf, teşhir ünitesi ve vitrin çerçevesi gibi elemanları "
                     "kapsar; işler tek iş emri akışıyla yönetilir.",
             "steps": [("Tespit", "Hasar türü, öncelik ve önerilen aksiyon fotoğrafla kaydedilir."), ("İş emri", "Kapsam, sorumlu ve hedef tarih netleşir."),
                       ("Uygulama", "Bölgesel ekip standart yöntemle sahada müdahale eder."), ("Fotoğraflı kapanış", "Sonrası fotoğrafı ve kalite kontrolüyle iş kapanır.")],
             "list": ["Minor Works: vida sıkıştırma, sabitleme, kapı kolu ve aksesuar değişimi, silikon, noktasal boya", "Sign Care: tabela, totem ve yönlendirme elemanlarının bakımı",
                      "Visual Care: görsel alan ve marka unsurları", "Furniture Care: mobilya ve teşhir elemanları"],
             "note": "Yüksek uzmanlık ve yasal yetki gerektiren işler (elektrik, mekanik tesisat vb.) uygun uzmanlarla koordine edilir; BİGEL tespit, planlama ve kapanış takibini yönetir.",
             "links": [("BİGEL CARE", "care", "")]},
            {"eyebrow": "Denetim", "h2": "Mağaza görsel standart denetimi.",
             "lead": "Merkezde onaylanan görsel standardın sahada nasıl uygulandığını görmek için BİGEL AUDIT kullanılır. Her madde Uygun, Uygun Değil veya Uygulanamaz olarak işaretlenir; fotoğraf, konum, "
                     "tarih ve açıklamayla kanıtlanır.",
             "steps": [("Saha", "Eğitimli ekip, standart kontrol listesiyle mağazayı inceler."), ("Veri", "Puan, fotoğraf, GPS, tarih ve bulgu kaydedilir."),
                       ("Merkez", "Şubeler tek dashboard'da karşılaştırılır."), ("İş emri", "Bulgu aksiyona dönüşür, uygulanır ve fotoğrafla kapanır.")],
             "list": ["Brand Audit: logo, kurumsal renk, güncel tabela, kampanya materyali ve fiyat iletişimi", "Visual Audit: tabela, ışıklı harf, folyo, poster, vitrin, stand ve dijital ekran",
                      "Clean Audit: cam, cephe, zemin ve ortak alanlar için renk kodlu özet", "Proje audit: kampanya, açılış veya tabela değişimi sonrasında tüm şubelerin toplu kontrolü"],
             "links": [("BİGEL AUDIT", "audit", "")]},
            {"eyebrow": "Franchise ve çok şubeli ağlar", "h2": "Franchise mağaza standart kontrolü, merkez adına.",
             "lead": "Franchise yapılarında her şubenin farklı temizlik uygulaması marka görünümünde tutarsızlık yaratır. BİGEL merkez marka ile tek sözleşme ve tek hizmet tanımıyla çalışır; franchise "
                     "sahiplerinin uygulamaları görünür, ölçülebilir ve merkezden yönetilebilir hale gelir.",
             "list": ["Merkez ile tek sözleşme ve tek hizmet tanımı", "Tüm şubeler için ortak kontrol listesi", "Standart fotoğraf açıları ve kalite kriterleri",
                      "Şube bazında skor ve uygunsuzluk takibi", "Merkez yönetim için karşılaştırmalı dashboard"],
             "p": "FIELD360, temizlik, bakım ve denetimi tek sözleşme, tek operasyon standardı ve tek raporlama akışında birleştirir. Ziyaretler, skorlar, açık bulgular ve kapanış kanıtları tek ekranda izlenir.",
             "links": [("BİGEL FIELD360", "field360", "")]},
            {"eyebrow": "Başlangıç", "h2": "Nasıl başlarız?",
             "lead": "Tüm ağa geçmeden önce seçili mağazalarda bir pilotla başlıyoruz. Pilot bitince elinizde başlangıç skorları, fotoğraflı bulgular ve gerçek saha verisine dayanan bir yaygınlaştırma planı oluyor.",
             "steps": [("Kapsam toplantısı", "90 dakika. Şube yapısı, hizmet modülleri ve pilot başarı kriterleri."), ("Pilot planı", "Lokasyon seti, soru seti, fotoğraf kuralı, SLA ve takvim tek dokümanda."),
                       ("Saha", "Ziyaretler başlar; kritik bulgular aynı gün bildirilir."), ("Sonuç toplantısı", "Skorlar, bulgular ve yaygınlaştırma teklifi.")],
             "p": "Pilotun ardından ihtiyaca göre BASIC, PRO, BUSINESS veya 360 paketinden biriyle devam edilir. Fiyatlandırma şube sayısı, bölgesel dağılım, hizmet sıklığı ve kapsama göre hazırlanır.",
             "links": [("Pilot başvurusu", "pilot", "basvuru"), ("Abonelik paketleri", "tiers", "")]},
        ],
        "faq": [("Zincir mağaza temizliği hangi alanları kapsar?", "Vitrin ve giriş camı, cam cephe, kompozit, metal, taş ve boyalı cephe yüzeyleri, tabela, totem ve yönlendirme elemanları ile mağaza girişi ve çevresinin dış zemini. Kapanış sonrası temizlik (Night Clean) ve acil müdahale (Emergency Clean) de programa eklenebilir."),
                ("Vitrin ve cephe temizliği mağaza açıkken yapılabilir mi?", "Ziyaret zamanı her mağazanın çalışma saatlerine göre planlanır. Müşteri trafiğinin yoğun olduğu şubelerde Night Clean modülüyle temizlik, mağazanın çalışma düzenini etkilemeden kapanış sonrasına alınabilir."),
                ("Kampanya veya tabela değişiminden sonra tüm şubeler nasıl kontrol edilir?", "Proje audit ile kampanya, açılış veya tabela değişimi sonrasında şubeler toplu olarak denetlenir. Brand ve Visual Audit maddeleri kampanya materyalini, fiyat iletişimini, tabelayı, vitrini ve dijital ekranı kapsar; her madde fotoğrafla kanıtlanır."),
                ("Franchise mağazalarda aynı görsel standart nasıl sağlanır?", "BİGEL merkez marka ile tek sözleşme ve tek hizmet tanımıyla çalışır. Tüm şubelerde ortak kontrol listesi, standart fotoğraf açıları ve kalite kriterleri kullanılır; şube bazında skor ve uygunsuzluklar merkez için karşılaştırmalı dashboard'da izlenir."),
                ("Temizliğin yapıldığı nasıl doğrulanır?", "Her ziyarette standart açılardan öncesi ve sonrası fotoğraf çekilir; kayıt GPS ve zaman damgası taşır. Kontrol listesi, sonrası fotoğrafı ve bulgu bildirimiyle tamamlanma kaydı oluşur."),
                ("Mağazadaki küçük hasarlar da giderilebilir mi?", "Evet. BİGEL CARE'in Retail & AVM Care paketi raf, teşhir ünitesi ve vitrin çerçevesi gibi elemanları kapsar. Tespit, iş emri, uygulama ve fotoğraflı kapanış tek akışta yürür; elektrik gibi yetki gerektiren işler uygun uzmanlarla koordine edilir."),
                ("Hangi illerde hizmet veriyorsunuz?", "BİGEL Türkiye genelinde bölgesel saha ekip ağıyla çalışır. Merkezi planlama ve kalite kontrolü İstanbul'dan yürütülür, uygulama bölgesel ekiplerle yapılır.")],
        "cta": {"h2": "Şubelerinizin mağaza önünü tek standarda taşıyalım.", "p": "Seçili mağazalarda pilotla başlayın. Başlangıç skorları, fotoğraflı bulgular ve yaygınlaştırma planı pilotun sonunda elinizde.",
                "b1": "Pilot Başvurusu", "b2": "Teklif Al"}},
    "bank": {
        "title": "Banka Şubesi ve ATM Kabini Temizliği ve Bakımı",
        "desc": "Banka şubesi temizliği ve ATM kabini bakımı: giriş, cam, cephe, tabela ve banko tek standartla, mesai dışında planlanır ve fotoğrafla doğrulanır.",
        "crumb": "Banka Şubesi ve ATM Kabini Temizliği",
        "service": "Banka şubesi ve ATM kabini temizliği ve bakımı",
        "eyebrow": "Bankacılık · CLEAN + CARE",
        "h1": "Banka şubesi ve ATM kabini temizliği, tüm ağda tek standartla.",
        "lead": "Şubede ya da şube dışındaki bir ATM noktasında müşterinin ilk gördüğü şey giriş, cam ve ATM kabinidir. BİGEL, banka şubesi temizliğini ve ATM kabini bakımını merkezden planlar, "
                "bölgesel ekiplerle uygular ve her ziyareti öncesi ve sonrası fotoğrafla kayda geçirir.",
        "b1": "Pilot Başlat", "b2": "Teklif Al",
        "sections": [
            {"eyebrow": "Kapsam", "h2": "Banka şubesi ve ATM kabini temizliği ne kapsar?",
             "lead": "Bankacılıkta saha işi şube girişi, ATM kabini, cam ve cephe, banko ve seperatörlerde yoğunlaşır. Her alan için yöntem, kontrol maddesi ve fotoğraf açısı önceden tanımlanır; böylece "
                     "İstanbul'daki bir şube ile Anadolu'daki bir ATM noktası aynı ölçüyle değerlendirilir.",
             "list": ["ATM kabini ve çevresi: kabin camı, kabin içi yüzeyler, giriş ve çevre temizliği; kabinin görünür fiziksel durumunun kontrolü (Auto & ATM Care kapsamında)",
                      "Şube girişi, cam ve cephe: Cam ve Cephe Clean ile vitrin, giriş camı, cam cephe, kompozit, metal, taş ve boyalı yüzeyler",
                      "Tabela ve ışıklı harf: Tabela ve Totem Clean ile yüzeye uygun temizlik, Sign Care ile tabela ve yönlendirme elemanlarının bakımı; ışıklı harf ve tabelanın görünümü Visual Audit maddeleriyle izlenir",
                      "Banko ve seperatörler: müşteri alanındaki banko ve seperatörlerin temizliği ile sabitleme, sıkıştırma gibi küçük fiziksel müdahaleler",
                      "Vandalizm ve ani kirlenmede acil müdahale: Emergency Clean; ani kirlenme, dökülme, kötü hava, vandalizm veya denetim öncesi hızlı müdahale için planlanır"],
             "links": [("BİGEL CLEAN", "clean", "")]},
            {"eyebrow": "Night Clean", "h2": "Mesai dışı planlama",
             "lead": "Şube içinde ve girişinde yapılan iş, müşteri trafiğini ve şube operasyonunu aksatmamalıdır. Night Clean, işletmenin çalışma düzenini etkilemeden kapanış sonrasına planlanan temizliktir.",
             "list": ["Ziyaret takvimi şube çalışma saatlerine göre merkezde hazırlanır", "Kapanış sonrası yapılan iş de aynı kontrol listesi ve fotoğraf kuralına bağlıdır",
                      "Modüller tek seferlik ya da periyodik programa dahil edilebilir", "Mevsimsel ihtiyaçlar (kış kiri, çamur, yaprak ve kaygan yüzey riski) Seasonal Clean ile programa eklenebilir"]},
            {"eyebrow": "CARE + AUDIT", "h2": "Küçük onarım ve fiziksel durum",
             "lead": "Kabin kapısındaki gevşek bir kol, yerinden oynamış bir seperatör ya da solmuş bir yönlendirme etiketi tek başına küçük görünür; ağ genelinde biriktiğinde marka algısını etkiler. "
                     "Auto & ATM Care, ATM kabini, şube girişi ve bankoya odaklanan CARE paketidir.",
             "steps": [("Tespit", "Talep ya da Physical Audit bulgusu tek kanaldan gelir: duvar, kapı, mobilya, bariyer, korkuluk ve küçük hasarlar fotoğrafla kaydedilir."),
                       ("İş emri", "Hasar türü, öncelik, kapsam, sorumlu ve hedef tarih belirlenir."),
                       ("Saha müdahalesi", "Minor Works ile vida sıkıştırma, sabitleme, kapı kolu ve aksesuar değişimi, silikon ve noktasal boya bölgesel ekiple yapılır."),
                       ("Kapanış", "Sonrası fotoğrafı ve kalite kontrolüyle iş emri kapanır.")],
             "list": ["Kapsam sınırı: BİGEL'in işi ATM kabininin ve çevresinin temizliği ile görünür fiziksel durumudur. Nakit işlemleri, ATM cihazının teknik bakımı ve güvenlik hizmeti kapsam dışındadır",
                      "Elektrik ve mekanik tesisat gibi uzmanlık ve yasal yetki gerektiren işler uygun uzmanlarla koordine edilir; BİGEL tespit, planlama ve kapanış takibini yönetir"],
             "links": [("BİGEL CARE", "care", "")]},
            {"eyebrow": "Görünürlük", "h2": "Şube ağında görünürlük",
             "lead": "Genel müdürlük ya da bölge yönetimi, sahada ne yapıldığını raporla değil kanıtla görmek ister. Her ziyaret fotoğraf, kontrol listesi ve skor üretir; bulgular iş emrine dönüşür.",
             "list": ["Öncesi ve sonrası fotoğraf, GPS ve zaman damgası", "Lokasyon, bölge ve dönem karşılaştırmaları; düşük performanslı şubeler ve ATM noktaları tek listede",
                      "Brand Audit ve Visual Audit ile logo, kurumsal renk, güncel tabela, kampanya materyali ve ışıklı harf; Customer Experience Audit ile giriş, yönlendirme ve bekleme alanı ölçülür",
                      "FIELD360 ile tek sözleşme, tek operasyon merkezi ve bölgesel ekip ağı; ziyaretler, skorlar, açık bulgular ve kapanış kanıtları tek ekranda"],
             "links": [("BİGEL AUDIT", "audit", ""), ("BİGEL FIELD360", "field360", "")]},
        ],
        "faq": [("ATM kabini temizliği neleri kapsar?", "Kabin camı, kabin içi yüzeyler, giriş ve kabin çevresinin temizliği ile kabinin görünür fiziksel durumunun kontrolünü kapsar. Her ziyaret öncesi ve sonrası fotoğrafla kaydedilir. Gevşek kapı kolu, sabitleme veya noktasal boya gibi küçük ihtiyaçlar Auto & ATM Care kapsamında iş emrine bağlanır."),
                ("Şube temizliği mesai dışında yapılabilir mi?", "Evet. Night Clean, işletmenin çalışma düzenini etkilemeden kapanış sonrasına planlanan temizliktir. Şube saatleri ziyaret takvimine işlenir; mesai dışında yapılan iş de aynı kontrol listesi ve fotoğraf kuralıyla doğrulanır."),
                ("Şube dışındaki ATM'ler için de hizmet veriliyor mu?", "Kapsam lokasyon listesine göre tanımlanır; şube dışındaki ATM noktaları da bu listeye ayrı lokasyon olarak eklenebilir. Ziyaretler merkezde planlanır ve bölgesel ekiplerle yapılır. Her nokta aynı kontrol listesi ve fotoğraf standardıyla kayda geçer, böylece şube ve şube dışı ATM'ler aynı raporda karşılaştırılır."),
                ("Vandalizm veya ani kirlenmede ne kadar hızlı müdahale edilir?", "Emergency Clean; ani kirlenme, dökülme, kötü hava ve vandalizm gibi durumlar için tanımlı acil müdahale modülüdür. Hedef müdahale süreleri sözleşme başında lokasyon yapınıza göre SLA olarak birlikte belirlenir ve raporda takip edilir."),
                ("ATM cihazının teknik bakımı kapsama dahil mi?", "Hayır. BİGEL'in kapsamı ATM kabininin ve çevresinin temizliği ile görünür fiziksel durumudur. Cihazın teknik bakımı, nakit işlemleri ve güvenlik hizmeti kapsam dışındadır. Elektrik gibi yasal yetki gerektiren işler uygun uzmanlarla koordine edilir."),
                ("Hizmete nasıl başlanır?", "Seçili şube ve ATM noktalarıyla bir pilotla başlanabilir. Pilot sonunda başlangıç skorları, fotoğraflı bulgular ve gerçek saha verisine dayanan bir yaygınlaştırma planı elinizde olur. Teklif; lokasyon sayısı, bölgesel dağılım, hizmet sıklığı ve kapsama göre hazırlanır.")],
        "cta": {"h2": "Şube ve ATM ağınızı tek standartla yönetelim.", "p": "Seçili şube ve ATM noktalarında pilotla başlayın: başlangıç ölçümü, fotoğraflı bulgular ve lokasyon skorları. Sonuçlara göre bölgesel ve Türkiye geneli operasyona ölçekleriz.",
                "b1": "Pilot Başlat", "b2": "Teklif Al"}},
    "restaurant": {
        "title": "Restoran Zinciri Dış Cephe ve Tabela Temizliği",
        "desc": "Restoran zincirlerinde dış cephe, cam, tabela, dış oturma ve drive-thru temizliği. Kapanış sonrası uygulama, fotoğraflı kanıt, tüm şubelerde tek standart.",
        "crumb": "Restoran Zinciri Dış Alan Temizliği",
        "service": "Restoran zinciri dış alan temizliği ve bakımı",
        "eyebrow": "Restoran & Fast Food · CLEAN + CARE",
        "h1": "Restoran zincirlerinde dış cephe, tabela ve arabaya servis alanı, her şubede aynı görünümde.",
        "lead": "Misafir restoranınızı önce sokaktan ve yoldan görür: cephe, cam, tabela ve arabaya servis şeridi markanın ilk izlenimidir. BİGEL, restoran zincirlerinin dış alan temizliğini ve küçük "
                "bakımını tüm şubelerde tek standartla yönetir. Uygulama, işletmenin çalışma düzenini bozmadan kapanış sonrasına planlanabilir; her ziyaret öncesi ve sonrası fotoğraf, GPS ve zaman "
                "damgasıyla kapanır.",
        "b1": "Pilot Başlat", "b2": "Teklif Al",
        "sections": [
            {"eyebrow": "Kapsam", "h2": "Restoran dış cephe temizliği neleri kapsar?",
             "lead": "BİGEL CLEAN, şubenin misafire görünen dış alanını tanımlı yöntem, ekipman ve fotoğraf açısıyla ele alır. Modüller tek seferlik uygulanabilir ya da periyodik programa eklenir.",
             "cards": [("Dış cephe ve cam", "Vitrin, giriş camı ve cam cephe; kompozit, metal, taş ve boyalı yüzeyler. Cam ve Cephe Clean modülü her yüzeye uygun yöntemle uygulanır."),
                       ("Tabela, totem ve yönlendirme", "Restoran tabela temizliği marka görünürlüğünü doğrudan etkiler. Tabela, totem ve yönlendirme elemanları yüzeye uygun yöntemle temizlenir; şube yoldan bakıldığında da net okunur."),
                       ("Arabaya servis (drive-thru) şeridi ve otopark", "Drive-thru şeridi, otopark ve giriş çevresinde beton, asfalt, parke, epoksi ve taş yüzeylerde kir, yağ lekesi ve çevre temizliği. Zemin ve Otopark Clean modülüyle yürütülür."),
                       ("Dış oturma alanı mobilyası", "Dış oturma alanının ve mobilyasının düzenli temizliği. Gevşeyen, hasar gören ya da eksilen parçalar Furniture Care kapsamında CARE iş emrine bağlanır."),
                       ("Sezonluk program: yaprak, çamur, kış kiri", "Seasonal Clean; kış kiri, yosun, yaprak, çamur ve kaygan yüzey risklerine göre mevsimsel program kurar. Ani kirlenme, dökülme, kötü hava veya vandalizmde Emergency Clean devreye girer.")],
             "links": [("BİGEL CLEAN", "clean", "")]},
            {"eyebrow": "Restoran bakımı · Restaurant Care", "h2": "Restaurant Care: küçük işler birikmeden kapanır.",
             "lead": "BİGEL CARE'in Restaurant Care paketi; dış cephe, tabela, dış oturma, arabaya servis alanı ve iç mekândaki küçük işleri tek iş emri akışında toplar. Her arıza için ayrı usta aramak "
                     "yerine şube ya da merkez tek kanaldan talep açar.",
             "steps": [("Talep", "Tek kanal: şube talebi veya denetim bulgusu."), ("Fotoğraflı tespit", "Hasar türü, öncelik ve önerilen aksiyon."), ("Görev onayı", "Kapsam, sorumlu ve hedef tarih."),
                       ("Saha müdahalesi", "Bölgesel ekiple standart uygulama."), ("Kapanış raporu", "Sonrası fotoğrafı ve kalite kontrolü.")],
             "list": ["Minor Works: vida sıkıştırma, sabitleme, kapı kolu ve aksesuar değişimi, silikon, noktasal boya", "Sign Care: tabela, totem ve yönlendirme elemanlarının bakımı",
                      "Exterior Care: cephe, giriş ve dış alan bakımı", "Furniture Care: mobilya ve teşhir elemanları", "Pavement Care: zemin, bordür ve otopark bakımı",
                      "Preventive Care ve Emergency Care: periyodik önleyici bakım ve acil saha müdahalesi"],
             "note": "Yüksek uzmanlık ve yasal yetki gerektiren işler (elektrik, mekanik tesisat vb.) uygun uzmanlarla koordine edilir; BİGEL tespit, planlama ve kapanış takibini yönetir. Mutfak, davlumbaz "
                     "ve gıda hijyeni hizmetleri bu kapsamın dışındadır.",
             "links": [("BİGEL CARE", "care", "")]},
            {"eyebrow": "Franchise ağları", "h2": "Franchise ağında tek standart.",
             "lead": "Franchise yapılarında her şubenin farklı temizlik uygulaması marka görünümünde tutarsızlık yaratır. BİGEL merkez marka ile tek sözleşme ve tek hizmet tanımıyla çalışır; franchise "
                     "sahiplerinin uygulamaları görünür, ölçülebilir ve merkezden yönetilebilir hale gelir.",
             "list": ["Tüm şubeler için ortak kontrol listesi", "Standart fotoğraf açıları ve kalite kriterleri", "Bölgesel ekiplerle planlı saha ziyaretleri",
                      "Lokasyon bazında skor ve uygunsuzluk takibi", "Merkez yönetim için karşılaştırmalı dashboard"]},
            {"eyebrow": "Franchise audit · BİGEL AUDIT", "h2": "Franchise restoran standart denetimi: ölçün, sonra kapatın.",
             "lead": "Franchise audit, ağdaki standart uyumunu merkez adına ölçer. Customer Experience Audit fark edilirlik, giriş, yönlendirme, kasa ve bekleme alanına bakar ve CX SCORE üretir. Visual Audit "
                     "tabela, ışıklı harf, folyo, poster ve vitrini kontrol eder. Çıkan bulgu CARE iş emrine dönüşür, kapanışı fotoğrafla doğrulanır.",
             "steps": [("Saha", "Eğitimli ekip, standart kontrol listesiyle inceler."), ("Veri", "Puan, fotoğraf, GPS, tarih ve bulgu kaydedilir."), ("Merkez", "Şubeler tek dashboard'da karşılaştırılır."),
                       ("Karar", "Bulgular öncelik ve sorumluluğa göre sınıflanır."), ("İş emri", "Aksiyon oluşturulur, uygulanır, fotoğrafla kapanır.")],
             "list": ["AUDIT 100: 10 kategori, 100 kontrol noktası; kategori ağırlıklarıyla 100 üzerinden lokasyon skoru", "Her madde Uygun 100, Kısmen Uygun 50, Uygun Değil 0 puan alır",
                      "Proje audit: kampanya, açılış veya tabela değişimi sonrası toplu kontrol", "Periyodik audit: aylık, üç aylık, altı aylık veya yıllık tekrar eden program"],
             "links": [("BİGEL AUDIT", "audit", "")]},
            {"eyebrow": "Kanıt ve raporlama · FIELD360", "h2": "Şubede yapılan iş, merkezde görünür.",
             "lead": "Her ziyaret aynı dijital akışla yürütülür ve FIELD360'ta tek kayıt zincirine düşer. Merkez ekip ziyaretleri, skorları, açık bulguları, iş emirlerini ve kapanış kanıtlarını tek ekranda izler.",
             "steps": [("Görev kapsamı", "Lokasyon bilgisi ve tanımlı hizmet."), ("Öncesi fotoğraf", "Standart açılardan başlangıç kaydı."), ("Uygulama", "Yöntem, ekipman ve kimyasal standardı."),
                       ("Sonrası fotoğraf", "Kontrol listesi ve kalite kriteri."), ("Tamamlanma", "Bulgu bildirimi ve kapanış kaydı.")],
             "list": ["Öncesi ve sonrası fotoğraf, GPS ve zaman damgası", "Planlanan, tamamlanan ve geciken ziyaretlerle SLA takibi", "Lokasyon, bölge ve dönem karşılaştırmaları",
                      "Zamanında ziyaret, aksiyon kapanış süresi ve tekrar müdahale oranı KPI olarak izlenir"],
             "links": [("BİGEL FIELD360", "field360", "")]},
        ],
        "faq": [("Restoran dış cephe ve tabela temizliği hangi alanları kapsar?", "Dış cephe ve camlar, vitrin ve giriş camı, tabela, totem ve yönlendirme elemanları, dış oturma alanı, arabaya servis (drive-thru) şeridi, otopark ve giriş çevresi. Kapsam her şube için kontrol listesiyle tanımlanır; modüller tek seferlik ya da periyodik programla uygulanır."),
                ("Drive-thru şeridi ve otopark temizliği servis saatlerini etkiler mi?", "Etkiyi en aza indirecek şekilde planlanır. Ziyaret saatleri, erişim koşulları ve hedef süreler kapsam ve SLA aşamasında birlikte tanımlanır. Night Clean, işletmenin çalışma düzenini etkilemeden kapanış sonrasına planlanan temizliktir; geç saate kadar açık şubelerde uygulama zamanı şube ile birlikte belirlenir."),
                ("Franchise şubelerin dış görünümü merkezden nasıl takip edilir?", "Tüm şubeler aynı kontrol listesi ve standart fotoğraf açılarıyla ziyaret edilir. Her ziyaret öncesi ve sonrası fotoğraf, GPS ve zaman damgasıyla kaydedilir. Lokasyon skorları, uygunsuzluklar ve açık iş emirleri merkez yönetim için karşılaştırmalı dashboard'da izlenir. Franchise audit ile standart uyumu merkez adına ölçülür."),
                ("Mevsime göre temizlik programı değişir mi?", "Evet. Seasonal Clean; kış kiri, yosun, yaprak, çamur ve kaygan yüzey risklerine göre mevsimsel program kurar. Ani kirlenme, dökülme, kötü hava veya vandalizm gibi durumlar için Emergency Clean ile planın dışında müdahale edilir."),
                ("Mutfak veya davlumbaz temizliği kapsama dahil mi?", "Hayır. BİGEL'in restoranlardaki kapsamı dış cephe, cam, tabela, dış oturma ve arabaya servis alanı ile iç mekândaki küçük bakım işleridir. Mutfak, davlumbaz ve gıda hijyeni hizmetleri kapsam dışındadır."),
                ("Restoran zinciri için pilot nasıl başlar?", "Pilot genellikle 20–30 lokasyonla ve 4–6 haftalık bir uygulama dönemiyle yürütülür. Kapsam ve kriterler onaylanır, başlangıç ölçümü yapılır, ikinci turda aksiyonların kapanışı ve skor gelişimi doğrulanır. Sonunda başlangıç skorları, fotoğraflı bulgular ve yaygınlaştırma planı elinizde olur.")],
        "cta": {"h2": "Şube ağınız için pilot kapsamını birlikte belirleyelim.", "p": "Seçili şubelerde başlayın; başlangıç skorlarını, fotoğraflı bulguları ve gerçek saha verisine dayanan yaygınlaştırma planını pilotun sonunda görün.",
                "b1": "Pilot Başlat", "b2": "Teklif Al"}},
})
CONTENT["en"]["landings"].update({
    "retail": {
        "title": "Retail Store Cleaning & Maintenance for Chains",
        "desc": "Retail store cleaning for chains: shopfronts, glass, façades and signage to one standard in every branch. Before/after photos, scores, work orders.",
        "crumb": "Retail Store Cleaning & Maintenance",
        "service": "Retail chain store exterior cleaning and maintenance",
        "eyebrow": "Retail · CLEAN + CARE + AUDIT",
        "h1": "Shopfronts, façades and signage to the same standard in every store.",
        "lead": "In chain retail, customers meet the brand at the shopfront, the entrance and the sign. A store front that varies from branch to branch erodes brand perception. BİGEL plans the work "
                "centrally, regional field teams carry it out, and every visit is reported with before and after photos.",
        "b1": "Apply for a Pilot", "b2": "Get a Quote",
        "sections": [
            {"eyebrow": "Scope", "h2": "What does retail chain cleaning cover?",
             "lead": "BİGEL CLEAN focuses on what customers see from outside: shopfront, entrance, façade, signage and surroundings. Each area has a defined method, equipment and photo angle; modules run "
                     "one-off or as a periodic programme.",
             "cards": [("Shopfront and entrance glass", "Glass & Façade Clean covers shopfront and entrance glass on a planned visit calendar, recorded with the same checklist and photo angles in every store."),
                       ("Façade and composite surfaces", "Curtain walls, composite, metal, stone and painted surfaces are cleaned with methods suited to each surface type."),
                       ("Signage, illuminated letters and wayfinding", "Signage & Totem Clean covers signs, totems and wayfinding that affect brand visibility, with surface-appropriate cleaning."),
                       ("Entrance and store surroundings", "Outdoor flooring at the entrance and around the store is handled for dirt and stains under Floor & Car Park Clean."),
                       ("After closing and emergency response", "Night Clean is scheduled after closing hours without disrupting operations. Emergency Clean responds to sudden soiling, bad weather, vandalism or pre-inspection needs.")],
             "note": "Scope is adapted to each store's surfaces and operating hours. This page covers exterior and shopfront services.",
             "links": [("BİGEL CLEAN", "clean", "")]},
            {"eyebrow": "Store maintenance", "h2": "Retail store maintenance: Retail Care.",
             "lead": "Small physical issues affect brand appearance as much as cleanliness. BİGEL CARE's Retail & Mall Care package covers shelving, display units and shopfront frames through a single work-order flow.",
             "steps": [("Detection", "Damage type, priority and recommended action recorded with photos."), ("Work order", "Scope, owner and due date confirmed."),
                       ("Execution", "A regional team carries out the work to a standard method."), ("Photo-verified closure", "The job closes with an after photo and quality check.")],
             "list": ["Minor Works: tightening, fixing, handle and accessory replacement, sealant, spot painting", "Sign Care: signage, totem and wayfinding maintenance",
                      "Visual Care: visual areas and brand elements", "Furniture Care: furniture and display elements"],
             "note": "Work that requires specialist expertise or legal authorisation (electrical, mechanical installations etc.) is coordinated with qualified specialists; BİGEL manages detection, planning and closure tracking.",
             "links": [("BİGEL CARE", "care", "")]},
            {"eyebrow": "Audit", "h2": "Store visual standards audit.",
             "lead": "BİGEL AUDIT shows how the visual standard approved at head office is applied in each store. Every item is marked Compliant, Non-compliant or Not applicable and evidenced with photo, location, date and notes.",
             "steps": [("Field", "Trained teams inspect the store with a standard checklist."), ("Data", "Score, photos, GPS, date and findings are recorded."),
                       ("Head office", "Stores are compared on one dashboard."), ("Work order", "Findings become actions, are executed and closed with photos.")],
             "list": ["Brand Audit: logo, corporate colours, current signage, campaign material and price communication", "Visual Audit: signage, illuminated letters, vinyl, posters, shopfronts, stands and digital screens",
                      "Clean Audit: glass, façade, floors and common areas with a colour-coded summary", "Project audit: a bulk check of all stores after campaigns, openings or signage changes"],
             "links": [("BİGEL AUDIT", "audit", "")]},
            {"eyebrow": "Franchise and multi-branch networks", "h2": "Franchise store standards, checked on behalf of head office.",
             "lead": "In franchise structures, every branch cleaning differently creates inconsistent brand appearance. BİGEL works with head office under one contract and one service definition.",
             "list": ["One contract and one service definition with head office", "A shared checklist for every store", "Standard photo angles and quality criteria",
                      "Store-level scores and non-conformity tracking", "A comparative dashboard for head office"],
             "p": "FIELD360 combines cleaning, maintenance and audits in one contract, one operating standard and one reporting flow, tracked on one screen.",
             "links": [("BİGEL FIELD360", "field360", "")]},
            {"eyebrow": "Getting started", "h2": "How do we start?",
             "lead": "We start with a pilot in selected stores. At the end you hold baseline scores, photo-verified findings and a roll-out plan based on real field data.",
             "steps": [("Scoping meeting", "90 minutes. Store structure, service modules and pilot success criteria."), ("Pilot plan", "Site set, question set, photo rules, SLA and schedule in one document."),
                       ("Field", "Visits begin; critical findings are reported the same day."), ("Results meeting", "Scores, findings and a roll-out proposal.")],
             "p": "After the pilot you continue with the BASIC, PRO, BUSINESS or 360 plan that fits. Pricing is based on number of stores, regional spread, service frequency and scope.",
             "links": [("Pilot application", "pilot", "apply"), ("Plans", "tiers", "")]},
        ],
        "faq": [("What does retail chain store cleaning cover?", "Shopfront and entrance glass, façade surfaces (curtain wall, composite, metal, stone, painted), signs, totems and wayfinding, and outdoor flooring at the entrance and around the store. Night Clean and Emergency Clean can be added."),
                ("Can shopfront and façade cleaning be done while the store is open?", "Visit times are planned around each store's operating hours. For busy stores, Night Clean moves the work to after closing so it does not disrupt operations."),
                ("How are all stores checked after a campaign or signage change?", "A project audit checks stores in bulk after a campaign, opening or signage change. Brand and Visual Audit items cover campaign material, price communication, signage, shopfronts and digital screens, and every item is evidenced with photos."),
                ("How do you keep the same visual standard across franchise stores?", "BİGEL works with head office under one contract and one service definition. Every store uses a shared checklist, standard photo angles and quality criteria; store scores and non-conformities are tracked on a comparative dashboard for head office."),
                ("How do you verify that the cleaning was done?", "Each visit includes before and after photos from standard angles, with GPS and a time stamp. The checklist, after photo and any reported findings form the completion record."),
                ("Can minor damage in the store be fixed too?", "Yes. BİGEL CARE's Retail & Mall Care package covers shelving, display units and shopfront frames, from detection to photo-verified closure. Work requiring authorisation, such as electrical, is coordinated with qualified specialists."),
                ("Where in Türkiye do you operate?", "BİGEL works across Türkiye with a regional field team network. Central planning and quality control are run from Istanbul; execution is carried out by regional teams.")],
        "cta": {"h2": "Let's bring every store front to one standard.", "p": "Start with a pilot in selected stores. At the end you hold baseline scores, photo-verified findings and a roll-out plan.",
                "b1": "Apply for a Pilot", "b2": "Get a Quote"}},
    "bank": {
        "title": "Bank Branch and ATM Cabin Cleaning & Maintenance",
        "desc": "Bank branch and ATM cabin cleaning and maintenance: entrance, glass, façade, signage and counters to one standard, after hours, photo-verified.",
        "crumb": "Bank Branch and ATM Cabin Cleaning",
        "service": "Bank branch and ATM cabin cleaning and maintenance",
        "eyebrow": "Banking · CLEAN + CARE",
        "h1": "Bank branch and ATM cabin cleaning, one standard across the network.",
        "lead": "Whether at a branch or an off-site ATM, the first thing a customer sees is the entrance, the glass and the ATM cabin. BİGEL plans branch and ATM cabin cleaning and maintenance centrally, "
                "delivers it with regional teams and records every visit with before and after photos.",
        "b1": "Start a Pilot", "b2": "Get a Quote",
        "sections": [
            {"eyebrow": "Scope", "h2": "What does bank branch and ATM cabin cleaning cover?",
             "lead": "In banking, field work concentrates on branch entrances, ATM cabins, glass and façade, counters and partitions. Each area has a defined method, checklist items and photo angles, so a "
                     "branch in one city and an ATM point in another are measured the same way.",
             "list": ["ATM cabin and surroundings: cabin glass, interior surfaces, entrance and surrounding area cleaning, plus a check of the cabin's visible physical condition (within Auto & ATM Care)",
                      "Branch entrance, glass and façade: Glass & Façade Clean for shopfronts, entrance glass, curtain walls, composite, metal, stone and painted surfaces",
                      "Signage and illuminated letters: Signage & Totem Clean for surface-appropriate cleaning, Sign Care for signage and wayfinding maintenance; illuminated letters and signage appearance are tracked through Visual Audit items",
                      "Counters and partitions: cleaning of counters and partitions in customer areas, plus minor physical fixes such as tightening and fixing",
                      "Emergency response to vandalism and sudden soiling: Emergency Clean covers sudden soiling, spills, bad weather, vandalism or pre-audit rapid response"],
             "links": [("BİGEL CLEAN", "clean", "")]},
            {"eyebrow": "Night Clean", "h2": "After-hours scheduling",
             "lead": "Work at the branch entrance and inside the branch must not disrupt customers or branch operations. Night Clean is cleaning scheduled after closing hours without disrupting operations.",
             "list": ["The visit calendar is built centrally around branch opening hours", "After-hours work follows the same checklist and photo rule",
                      "Modules can be one-off or part of a periodic programme", "Seasonal needs (winter grime, mud, leaves and slip risks) can be added through Seasonal Clean"]},
            {"eyebrow": "CARE + AUDIT", "h2": "Minor repairs and physical condition",
             "lead": "A loose handle on a cabin door, a shifted partition or a faded wayfinding label looks minor on its own; repeated across a network, it shapes how the brand is seen. Auto & ATM Care is "
                     "the CARE package focused on ATM cabins, branch entrances and counters.",
             "steps": [("Detection", "A request or a Physical Audit finding arrives through one channel: walls, doors, furniture, barriers, railings and minor damage are recorded with photos."),
                       ("Work order", "Damage type, priority, scope, owner and target date are set."),
                       ("On-site fix", "Minor Works such as tightening, fixing, handle and accessory replacement, sealant and spot painting by a regional team."),
                       ("Closure", "The work order closes with an after photo and a quality check.")],
             "list": ["Scope boundary: BİGEL's work is the cleaning and visible physical condition of the ATM cabin and its surroundings. Cash handling, technical maintenance of the ATM device and security services are out of scope",
                      "Work requiring specialist skills or legal certification, such as electrical or mechanical installations, is coordinated with qualified specialists; BİGEL manages detection, planning and closure tracking"],
             "links": [("BİGEL CARE", "care", "")]},
            {"eyebrow": "Visibility", "h2": "Visibility across the branch network",
             "lead": "Head office and regional management want to see what happened in the field as evidence, not just as a report. Every visit produces photos, a checklist and a score; findings become work orders.",
             "list": ["Before and after photos, GPS and timestamp", "Site, region and period comparisons; underperforming branches and ATM points in one list",
                      "Brand Audit and Visual Audit cover logo, corporate colours, current signage, campaign material and illuminated letters; Customer Experience Audit covers entrance, wayfinding and waiting areas",
                      "With FIELD360: one contract, one operations centre and a regional team network; visits, scores, open findings and closure evidence on one screen"],
             "links": [("BİGEL AUDIT", "audit", ""), ("BİGEL FIELD360", "field360", "")]},
        ],
        "faq": [("What does ATM cabin cleaning cover?", "Cleaning of the cabin glass, interior surfaces, entrance and surroundings, plus a check of the cabin's visible physical condition. Every visit is recorded with before and after photos. Minor needs such as a loose door handle, fixing or spot painting are tied to a work order under Auto & ATM Care."),
                ("Can branch cleaning be done outside business hours?", "Yes. Night Clean is cleaning scheduled after closing hours without disrupting operations. Branch hours go into the visit calendar, and after-hours work is verified with the same checklist and photo rule."),
                ("Do you also serve off-site ATMs?", "Scope is defined by your site list, and off-site ATM points can be added to it as separate sites. Visits are planned centrally and carried out by regional teams. Every point is recorded to the same checklist and photo standard, so branches and off-site ATMs are compared in the same report."),
                ("How fast is the response to vandalism or sudden soiling?", "Emergency Clean is the defined rapid-response module for sudden soiling, spills, bad weather and vandalism. Target response times are agreed as SLAs at the start, based on your site structure, and tracked in reporting."),
                ("Is technical maintenance of the ATM device included?", "No. BİGEL's scope is the cleaning and visible physical condition of the ATM cabin and its surroundings. Technical maintenance of the device, cash handling and security services are out of scope. Work requiring legal certification, such as electrical work, is coordinated with qualified specialists."),
                ("How do we get started?", "You can start with a pilot at selected branches and ATM points. At the end you have baseline scores, photo-verified findings and a rollout plan based on real field data. Quotes are prepared based on number of sites, regional spread, service frequency and scope.")],
        "cta": {"h2": "Let's run your branch and ATM network to one standard.", "p": "Start with a pilot at selected branches and ATM points: baseline measurement, photo-verified findings and site scores. Then scale regionally and nationwide based on the results.",
                "b1": "Start a Pilot", "b2": "Get a Quote"}},
    "restaurant": {
        "title": "Restaurant Chain Exterior & Drive-Thru Cleaning",
        "desc": "Façade, glass, signage, outdoor seating and drive-thru cleaning for restaurant chains. After-hours work, photo evidence, one standard at every branch.",
        "crumb": "Restaurant Chain Exterior Cleaning",
        "service": "Restaurant chain exterior cleaning and maintenance",
        "eyebrow": "Restaurants & QSR · CLEAN + CARE",
        "h1": "Façade, signage and drive-thru that look the same at every branch of your restaurant chain.",
        "lead": "Guests see your restaurant from the street and the road first: the façade, glass, signage and drive-thru lane are the brand's first impression. BİGEL manages exterior cleaning and minor "
                "maintenance for restaurant chains to one standard across every branch. Work can be scheduled after closing without disrupting operations, and every visit closes with before and after "
                "photos, GPS and a timestamp.",
        "b1": "Start a Pilot", "b2": "Get a Quote",
        "sections": [
            {"eyebrow": "Scope", "h2": "What does restaurant exterior cleaning cover?",
             "lead": "BİGEL CLEAN handles the guest-facing exterior of each branch with a defined method, equipment and photo angle. Modules can be applied once or added to a periodic programme.",
             "cards": [("Façade and glass", "Shopfronts, entrance glass and curtain walls; composite, metal, stone and painted surfaces. The Glass & Façade Clean module uses a method suited to each surface."),
                       ("Signage, totems and wayfinding", "Restaurant sign cleaning directly affects brand visibility. Signs, totems and wayfinding are cleaned with surface-appropriate methods, so the branch stays legible from the road."),
                       ("Drive-thru lane and car park", "Dirt, oil stains and litter on concrete, asphalt, pavers, epoxy and stone across the drive-thru lane, car park and entrance. Delivered through the Floor & Car Park Clean module."),
                       ("Outdoor seating furniture", "Regular cleaning of the outdoor seating area and its furniture. Loose, damaged or missing parts are routed to a CARE work order under Furniture Care."),
                       ("Seasonal programme: leaves, mud, winter grime", "Seasonal Clean builds a programme around winter grime, moss, leaves, mud and slip risks. Emergency Clean covers sudden soiling, spills, bad weather or vandalism.")],
             "links": [("BİGEL CLEAN", "clean", "")]},
            {"eyebrow": "Restaurant maintenance · Restaurant Care", "h2": "Restaurant Care: small jobs closed before they pile up.",
             "lead": "BİGEL CARE's Restaurant Care package brings small jobs on the façade, signage, outdoor seating, drive-thru and interior into one work-order flow. Instead of finding a different contractor "
                     "for every fault, the branch or head office raises a request through one channel.",
             "steps": [("Request", "One channel: branch request or audit finding."), ("Photo assessment", "Damage type, priority and proposed action."), ("Task approval", "Scope, owner and due date."),
                       ("Field intervention", "Standard execution by the regional team."), ("Closure report", "After photo and quality check.")],
             "list": ["Minor Works: tightening, fixing, handle and accessory replacement, sealant, spot painting", "Sign Care: signage, totem and wayfinding maintenance",
                      "Exterior Care: façade, entrance and outdoor area maintenance", "Furniture Care: furniture and display elements", "Pavement Care: floors, kerbs and car park maintenance",
                      "Preventive Care and Emergency Care: periodic preventive maintenance and emergency field response"],
             "note": "Work requiring specialist expertise or legal authorisation (electrical, mechanical installations, etc.) is coordinated with qualified specialists; BİGEL manages detection, planning and "
                     "closure tracking. Kitchen, hood and food-hygiene services are outside this scope.",
             "links": [("BİGEL CARE", "care", "")]},
            {"eyebrow": "Franchise networks", "h2": "One standard across the franchise network.",
             "lead": "In franchise structures, every branch cleaning differently creates inconsistency in brand appearance. BİGEL works with head office under one contract and one service definition, so "
                     "franchisee execution becomes visible, measurable and centrally manageable.",
             "list": ["A common checklist for all branches", "Standard photo angles and quality criteria", "Planned site visits by regional teams", "Site-level scores and non-conformity tracking",
                      "Comparative dashboard for head office"]},
            {"eyebrow": "Franchise audit · BİGEL AUDIT", "h2": "Franchise restaurant standards audit: measure, then close.",
             "lead": "Franchise audit measures standard compliance across the network on behalf of head office. Customer Experience Audit looks at visibility, entrance, wayfinding, checkout and waiting areas "
                     "and produces a CX SCORE. Visual Audit checks signage, illuminated letters, vinyl, posters and shopfronts. Every finding becomes a CARE work order, and closure is verified with a photo.",
             "steps": [("Field", "Trained team inspects with a standard checklist."), ("Data", "Score, photo, GPS, date and findings recorded."), ("Centre", "Branches compared on a single dashboard."),
                       ("Decision", "Findings classified by priority and owner."), ("Work order", "Action created, executed, closed with photo.")],
             "list": ["AUDIT 100: 10 categories, 100 checkpoints; category weights produce a site score out of 100", "Each item scores Compliant 100, Partially Compliant 50, Non-compliant 0",
                      "Project audit: bulk check after campaigns, openings or signage changes", "Periodic audit: monthly, quarterly, semi-annual or annual recurring programme"],
             "links": [("BİGEL AUDIT", "audit", "")]},
            {"eyebrow": "Evidence and reporting · FIELD360", "h2": "Work done at the branch, visible at head office.",
             "lead": "Every visit runs on the same digital flow and lands in a single record chain in FIELD360. Head office tracks visits, scores, open findings, work orders and closure evidence on one screen.",
             "steps": [("Task scope", "Site information and defined service."), ("Before photo", "Baseline record from standard angles."), ("Execution", "Method, equipment and chemical standard."),
                       ("After photo", "Checklist and quality criteria."), ("Completion", "Findings reported, closure recorded.")],
             "list": ["Before and after photos with GPS and timestamp", "SLA tracking of planned, completed and delayed visits", "Site, region and period comparisons",
                      "On-time visits, action closure time and repeat-intervention rate tracked as KPIs"],
             "links": [("BİGEL FIELD360", "field360", "")]},
        ],
        "faq": [("What does restaurant façade and sign cleaning cover?", "The façade and glass, shopfront and entrance glass, signs, totems and wayfinding, the outdoor seating area, the drive-thru lane, the car park and the entrance surroundings. Scope is defined for each branch with a checklist; modules run once or as a periodic programme."),
                ("Does drive-thru lane and car park cleaning disrupt service hours?", "It is planned to keep disruption to a minimum. Visit times, access conditions and target durations are agreed at the scope and SLA stage. Night Clean is cleaning scheduled after closing without disrupting operations; for branches open late, timing is set together with the branch."),
                ("How does head office track the exterior of franchise branches?", "Every branch is visited with the same checklist and standard photo angles. Each visit is recorded with before and after photos, GPS and a timestamp. Site scores, non-conformities and open work orders are tracked on a comparative dashboard for head office, and franchise audit measures standard compliance on its behalf."),
                ("Does the cleaning programme change with the seasons?", "Yes. Seasonal Clean builds a programme around winter grime, moss, leaves, mud and slip risks. Sudden soiling, spills, bad weather or vandalism are handled outside the plan with Emergency Clean."),
                ("Is kitchen or hood cleaning included?", "No. BİGEL's restaurant scope covers the façade, glass, signage, outdoor seating and drive-thru, plus minor interior maintenance jobs. Kitchen, hood and food-hygiene services are out of scope."),
                ("How does a pilot start for a restaurant chain?", "A pilot typically runs on 20–30 sites over a 4–6 week period. Scope and criteria are approved, a baseline measurement is taken, and a second round verifies action closure and score progress. You end with baseline scores, photo-backed findings and a roll-out plan.")],
        "cta": {"h2": "Let's define a pilot scope for your branch network.", "p": "Start with selected branches and see baseline scores, photo-backed findings and a roll-out plan based on real field data at the end of the pilot.",
                "b1": "Start a Pilot", "b2": "Get a Quote"}},
})
CONTENT["tr"]["ui"]["short"].update({"retail": "Mağaza temizliği ve bakımı", "bank": "Şube ve ATM temizliği", "restaurant": "Dış cephe ve tabela temizliği"})
CONTENT["en"]["ui"]["short"].update({"retail": "Store cleaning and maintenance", "bank": "Branch and ATM cleaning", "restaurant": "Exterior and sign cleaning"})
CONTENT["tr"]["ui"]["footer"].update({"retail": "Zincir mağaza temizliği", "bank": "Banka şubesi ve ATM temizliği", "restaurant": "Restoran dış alan temizliği"})
CONTENT["en"]["ui"]["footer"].update({"retail": "Retail store cleaning", "bank": "Bank branch and ATM cleaning", "restaurant": "Restaurant exterior cleaning"})

# ---------------------------------------------------------------- GUIDES (Rehber)
# Guide articles: CONTENT[lang]["guides"][gid]. Section shape: h2, paragraphs, list, after (paragraph after the list),
# links [(text, page id, anchor)]. "how" is the closing "How BİGEL does it" block. Author is the organisation BİGEL.
GUIDE_DATE = "2026-11-05"
CONTENT["tr"]["guides_index"] = {
    "title": "Rehber: İstasyon ve Zincir Saha Operasyonu",
    "desc": "Akaryakıt ve şarj istasyonları, zincir mağaza ve restoranlar için saha rehberleri: kanopi ve tabela temizliği, denetim kriterleri ve kontrol listeleri.",
    "eyebrow": "Rehber",
    "h1": "Saha operasyonu rehberleri",
    "lead": "Çok lokasyonlu ağlarda temizlik, bakım ve denetimi planlayanlar için pratik rehberler: neye bakılır, ne sıklıkla yapılır, sahada yapılan iş nasıl kanıtlanır.",
    "read": "Rehberi oku",
}
CONTENT["en"]["guides_index"] = {
    "title": "Guides: Field Operations for Stations and Chains",
    "desc": "Field guides for fuel and EV charging stations, retail and restaurant chains: canopy and sign cleaning, audit criteria and site checklists.",
    "eyebrow": "Guides",
    "h1": "Field operations guides",
    "lead": "Practical guides for teams planning cleaning, maintenance and audits across multi-site networks: what to check, how often, and how to prove the work was done.",
    "read": "Read the guide",
}
CONTENT["tr"]["guides"] = {
    "g_canopy": {
        "title": "Akaryakıt Kanopisi Ne Sıklıkla Temizlenmeli?",
        "desc": "Akaryakıt istasyonu kanopisi için tek bir temizlik aralığı yoktur. Trafik, konum, mevsim ve marka standardına göre doğru sıklığı belirleme rehberi.",
        "crumb": "Kanopi temizliği",
        "h1": "Akaryakıt istasyonu kanopisi ne sıklıkla temizlenmeli?",
        "lead": "Kısa cevap: Akaryakıt istasyonu kanopisi için herkese uyan tek bir temizlik aralığı yoktur. Doğru sıklık; istasyonun trafiğine, konumuna (otoyol, şehir içi, sanayi bölgesi), mevsime ve "
                "marka standardına göre değişir. En sağlıklı aralık, periyodik saha kontrollerinde kaydedilen bulgulara bakılarak belirlenir ve gerektikçe güncellenir.",
        "intro": "Bu rehberde kanopi derken mağaza tentesi ya da sundurma değil, akaryakıt istasyonunda pompa adalarının üzerini örten, marka kimliğini taşıyan büyük tavan yapısını kastediyoruz. Akaryakıt "
                 "istasyonu kanopisi istasyonun uzaktan görünen yüzüdür; alın bandındaki renkler soluk görünüyorsa, tavanda kurum lekeleri birikmişse sürücü bunu daha istasyona girmeden fark eder. "
                 "Aşağıda kanopide hangi kirlerin biriktiğini, temizlik sıklığını hangi etkenlerin belirlediğini, istasyon çalışırken işin nasıl planlanacağını ve yapılan temizliğin nasıl kanıtlanacağını "
                 "adım adım ele alıyoruz.",
        "sections": [
            {"h2": "Kanopide hangi kirler birikir?",
             "paragraphs": ["Kanopi yüzeyleri açık havada, araç trafiğinin hemen üzerinde durur. Bu yüzden kir tek tip değildir ve her biri farklı hızla birikir. Sahada en sık karşılaşılan kir türleri şunlardır:"],
             "list": ["Atmosferik kir: havadaki partiküllerin yüzeye yapışmasıyla oluşan, zamanla grileşen tabaka.",
                      "Toz: özellikle kuru dönemlerde ve yol çalışması, inşaat ya da açık arazi yakınında hızla artar.",
                      "Egzoz izi: rölantide bekleyen ve manevra yapan araçların bıraktığı koyu iz, genellikle pompa adalarının hemen üzerinde yoğunlaşır.",
                      "Kurum: ağır vasıta trafiğinin yoğun olduğu istasyonlarda tavanda ve alın bandının alt kenarında belirginleşir.",
                      "Biyolojik kirler: kuş pisliği, yosun ve nemli dönemlerde oluşan lekeler; yüzeye zarar vermeden zamanında alınmaları gerekir."]},
            {"h2": "Sıklığı belirleyen etkenler",
             "paragraphs": ["Kanopi temizliğinin sıklığı bir takvim kararından çok bir saha kararıdır. Aynı markanın iki istasyonu bile çok farklı hızda kirlenebilir. Planlama yaparken şu etkenleri birlikte değerlendirin:"],
             "list": ["Trafik ve konum: Ağır vasıta trafiği yüksek bir otoyol istasyonunda egzoz izi ve kurum, şehir içindeki bir istasyona göre çok daha hızlı birikir. Sanayi bölgesindeki istasyonlarda toz ve atmosferik kir öne çıkar.",
                      "Mevsim: Kış kiri, çamur, yaprak ve yosun mevsime bağlı olarak artar. Mevsimsel bir program bu dönemleri önceden takvime koyar.",
                      "Kampanya ve marka değişimi: Yeni bir kampanya giydirmesi, logo yenilemesi ya da marka değişimi öncesinde kanopinin temiz olması gerekir; aksi halde yeni görseller eski kirin yanında sönük kalır.",
                      "Denetim bulgusu: Periyodik saha denetimlerinde kanopi ile ilgili tekrar eden bulgular, mevcut aralığın yetersiz kaldığını gösterir. Bulgu çıkmıyorsa aralık korunabilir; sürekli çıkıyorsa sıklık artırılmalıdır.",
                      "Marka standardı: Bazı ağlar görünüm için kendi iç standartlarını belirler. Temizlik planı bu standartla uyumlu olmalıdır."],
             "after": "Pratik bir yöntem: Ağdaki istasyonları trafik ve konuma göre birkaç gruba ayırın, her gruba bir başlangıç aralığı verin ve ilk birkaç ziyaretin öncesi fotoğraflarını karşılaştırarak aralığı daraltın ya da genişletin."},
            {"h2": "İstasyon çalışırken temizlik nasıl planlanır?",
             "paragraphs": ["Akaryakıt istasyonları çoğu zaman kesintisiz çalışır. Kanopi temizliği pompa adalarının hemen üzerinde yapıldığı için müşteri trafiğiyle çakışmaması gerekir. En uygun zaman, kapanış sonrası ya da trafiğin en düşük olduğu saatlerdir. Gece planlanan temizlik, işletmenin çalışma düzenini etkilemeden yapılır.",
                            "Uygulama öncesinde çalışma alanı belirlenmeli ve işaretlenmeli, pompa adalarına araç girişi gerektiği kadar sınırlandırılmalı, istasyon sorumlusuyla hangi adaların ne zaman kapatılacağı netleştirilmelidir. Kimyasal seçimi ve yüksekte çalışma güvenliği ilgili mevzuat ve marka standartlarına göre yapılmalıdır.",
                            "Planlı programın dışında da ihtiyaç doğabilir: ani kirlenme, kötü hava sonrası oluşan birikinti, vandalizm ya da yaklaşan bir denetim. Bu durumlar için acil temizlik müdahalesinin nasıl talep edileceği önceden tanımlanmalıdır."]},
            {"h2": "Alın bandı, tavan ve aydınlatma çevresi",
             "paragraphs": ["Kanopi temizliği tek bir yüzeyden ibaret değildir. Kapsamı baştan yazılı hale getirmek, hem ekip hem de istasyon yönetimi için belirsizliği ortadan kaldırır. Tipik kapsam şu bölümleri içerir:"],
             "list": ["Alın bandı: marka renklerinin ve logonun bulunduğu, en çok görünen yüzey.", "Tavan yüzeyi: egzoz izi ve kurumun en çok biriktiği alan.",
                      "Kolonlar: araç ve insan temasına en açık bölüm.", "Aydınlatma çevresi: armatürlerin çevresindeki yüzeyler."],
             "after": "Önemli bir sınır: Aydınlatma armatürleri üzerindeki elektrik işleri temizlik kapsamına girmez. Elektriksel müdahale gerektiren bir durum fark edilirse bulgu olarak kaydedilir ve yetkili uzmanlara yönlendirilir."},
            {"h2": "Temizliğin yapıldığı nasıl kanıtlanır?",
             "paragraphs": ["Çok lokasyonlu ağlarda merkez ekip her istasyona gidemez. Bu yüzden temizliğin yapıldığını gösteren kayıt, temizliğin kendisi kadar önemlidir. Her ziyarette şunların kaydedilmesini öneririz:"],
             "list": ["Aynı açılardan çekilmiş öncesi ve sonrası fotoğrafları", "Ziyaret tarihi ve lokasyon bilgisi", "Uygulanan kapsam: alın bandı, tavan, kolonlar, aydınlatma çevresi",
                      "Uygulama sırasında fark edilen hasar ya da bakım ihtiyacı", "Kontrol listesi üzerinden kalite kontrolü"],
             "after": "Standart açılardan çekilen fotoğraflar zaman içinde karşılaştırılabilir hale gelir; böylece hangi istasyonun daha sık kirlendiği veriyle görülür. Periyodik saha denetimlerinde temizlik ve görsel standart maddeleri de kanopinin durumunu bağımsız biçimde gösterir.",
             "links": [("Akaryakıt istasyonu denetim kriterleri", "g_fuel_audit", "")]},
            {"h2": "Birden çok istasyonda planlama",
             "paragraphs": ["Tek bir istasyon için temizlik planı yapmak kolaydır; zorluk, onlarca ya da yüzlerce istasyonda aynı standardı tutmaktır. Çok lokasyonlu bir ağda planlama için şu yaklaşım işe yarar:"],
             "list": ["Merkezi plan: Tüm istasyonlar için ortak hizmet tanımı ve yıllık takvim oluşturun.", "Gruplama: İstasyonları trafik, konum ve bölgeye göre gruplayın; her gruba ayrı aralık tanımlayın.",
                      "Bölgesel ekipler: Uygulamayı bölgedeki ekiplerle yaptırarak ulaşım süresini kısaltın.", "Ortak kontrol listesi: Her istasyonda aynı kapsam, aynı fotoğraf açıları ve aynı kalite kriteri kullanılsın.",
                      "Geri besleme: Denetim bulgularına göre aralıkları dönemsel olarak gözden geçirin."]},
        ],
        "how": {"h2": "BİGEL nasıl yapar?",
                "paragraphs": ["BİGEL CLEAN, kanopi, tabela, totem, cephe ve otopark temizliğini Türkiye genelinde tek standartla yönetir. Kanopi Clean; atmosferik kir, toz, egzoz izi, kurum ve biyolojik kirlerin periyodik temizliğini kapsar. Night Clean kapanış sonrası, Emergency Clean ani kirlenme ya da denetim öncesi, Seasonal Clean ise kış kiri, yosun, yaprak ve çamura göre planlanır. Her ziyaret öncesi ve sonrası fotoğrafla doğrulanır.",
                               "Periyodik paket aylık, iki aylık, üç aylık veya mevsimsel olarak kurulabilir; doğru seçeneği istasyonunuzun koşullarına göre birlikte belirleriz. Kanopinin durumunu bağımsız ölçmek isterseniz AUDIT 100 ile fotoğraflı saha denetimi yapılır. Planlama merkezden yapılır, uygulama Türkiye genelinde bölgesel ekiplerle yürütülür."],
                "links": [("Akaryakıt istasyonu temizliği", "fuel_clean", ""), ("Akaryakıt istasyonu denetimi", "fuel_audit", ""), ("BİGEL CLEAN", "clean", ""), ("Pilot başlatın", "pilot", "basvuru")]},
        "faq": [("Akaryakıt istasyonu kanopisi ne sıklıkla temizlenmeli?", "Herkese uyan tek bir aralık yoktur. Sıklık; trafik, konum, mevsim ve marka standardına göre belirlenir. En doğru yöntem, bir başlangıç aralığıyla başlayıp periyodik saha kontrollerindeki bulgulara göre aralığı güncellemektir."),
                ("Kanopi temizliği istasyon açıkken yapılabilir mi?", "Yapılabilir, ancak müşteri trafiğiyle çakışmaması için kapanış sonrası ya da trafiğin en düşük olduğu saatler tercih edilir. Çalışma alanı işaretlenir ve hangi pompa adalarının ne zaman kapatılacağı istasyon sorumlusuyla önceden netleştirilir."),
                ("Kanopi temizliğine aydınlatma armatürleri dahil mi?", "Armatürlerin çevresindeki yüzeyler temizlik kapsamındadır. Armatürler üzerindeki elektrik işleri kapsam dışıdır; elektriksel bir sorun fark edilirse bulgu olarak kaydedilir ve yetkili uzmanlara yönlendirilir."),
                ("Temizliğin yapıldığını merkezden nasıl takip edebilirim?", "Her ziyarette aynı açılardan çekilen öncesi ve sonrası fotoğrafları, tarih ve lokasyon bilgisi ile kontrol listesi kaydedilmelidir. Bu kayıtlar istasyonları birbiriyle ve zaman içinde karşılaştırmayı mümkün kılar.")]},
    "g_ev": {
        "title": "Şarj İstasyonu Kontrol Listesi: Neye Bakılır?",
        "desc": "Şarj istasyonunda sahada neye bakılır? Güvenlikten marka standardına 6 alanlı kontrol listesi, fotoğraf seti, skor eşikleri ve bulgudan iş emrine akış.",
        "crumb": "Şarj istasyonu kontrol listesi",
        "h1": "Şarj istasyonu kontrol listesi: sahada neye bakılır?",
        "lead": "Şarj istasyonu kontrolü iki katmandan oluşur: yetkili uzmanların yaptığı elektriksel periyodik muayene ve testler ile kullanıcının sahada karşılaştığı fiziksel koşullar. Bu rehber ikinci "
                "katmana odaklanır ve 6 alanda neye bakılacağını, neyin kaydedileceğini anlatır.",
        "intro": "Şarj istasyonu kontrolü denince çoğu kaynak elektriksel testleri ve mevzuatı anlatır. Bu işler yetkili uzmanların sorumluluğundadır ve ilgili mevzuat ve marka standartlarına göre "
                 "yürütülür; bu rehberin konusu değildir. Ancak bir sürücünün şarj noktasında yaşadığı deneyimi belirleyen pek çok şey elektrikle ilgili değildir: yerde kalan bir kablo, okunmayan bir "
                 "ekran, başka bir aracın işgal ettiği park cebi ya da karanlıkta görünmeyen bir yönlendirme tabelası. Aşağıdaki kontrol listesi, bu saha koşullarını düzenli ve karşılaştırılabilir "
                 "biçimde kaydetmek için hazırlanmıştır.",
        "sections": [
            {"h2": "6 alanlı saha kontrol listesi",
             "paragraphs": ["Liste, EV Audit30'un altı ağırlıklı alanını temel alır. Parantez içindeki sayılar alanın 100 üzerinden skordaki ağırlığıdır. Maddeler teknik test değil, sahada gözle bakılacak ve fotoğrafla kaydedilecek noktalardır.",
                            "1. Güvenlik (25, 5 kritik kontrol): Kablo ve konektör yerde ya da yürüme yolunda kalmış mı? Konektör yuvasına düzgün yerleştirilmiş mi? Ünitenin çevresinde takılıp düşmeye yol açacak bir engel var mı? Gövdede açıkta kalmış, kırık ya da sarkan bir parça göze çarpıyor mu? Zeminde kaygan bir yüzey var mı? Bu alandaki uygunsuzluklar aynı gün bildirilmelidir.",
                            "2. Cihaz bütünlüğü (20): Gövdede çarpma, çatlak, kırık kapak ya da eksik parça var mı? Kablo kılıfında görünür hasar var mı? Etiketler ve bilgilendirme yüzeyleri yerinde mi?",
                            "3. İşlev işaretleri (20): Ekran açık ve okunabilir mi? Durum ışıkları görünüyor mu? Ekranda kullanıcıyı yönlendiren bilgi mi, hata mesajı mı var? Bu maddeler cihazın içine bakmadan, yalnızca kullanıcının gördüğü işaretler üzerinden değerlendirilir.",
                            "4. Kullanıcı deneyimi (15): Park cebi boş ve kullanılabilir mi, başka bir araç tarafından işgal edilmiş mi? Yönlendirme tabelası istasyona girişten görülebiliyor mu? Aydınlatma dış gövdesi sağlam mı, alan karanlıkta görünür mü? Kablo araca rahatça ulaşıyor mu?",
                            "5. Temizlik ve çevre (10): Zemin temiz mi, yağ lekesi, çöp ya da yaprak birikmiş mi? Ünite gövdesi ve ekran yüzeyi temiz mi? Çevrede bakımsız görünen bir alan var mı?",
                            "6. Marka standardı (10): Logo, renk ve giydirme marka standardına uygun mu? Soyulmuş folyo, solmuş renk ya da güncel olmayan bir bilgilendirme var mı?"]},
            {"h2": "Fotoğraf seti: her ziyarette aynı altı kare",
             "paragraphs": ["Kontrol listesinin değeri, kayıtların karşılaştırılabilir olmasından gelir. Bunun için her ziyarette aynı fotoğraf seti çekilmelidir:"],
             "list": ["Ön", "Sağ", "Sol", "Ekran", "Kablo", "Park alanı"],
             "after": "Fotoğraflar tarih, saat ve konum bilgisiyle saklanmalıdır. Bir bulgu varsa yakın plan bir fotoğraf ve kısa bir açıklama eklenmelidir. Aynı açılardan çekilen kareler, aynı noktanın zaman içindeki değişimini ve farklı noktalar arasındaki farkları görmeyi kolaylaştırır."},
            {"h2": "Skor ve aksiyon eşikleri",
             "paragraphs": ["Her alanın ağırlığıyla hesaplanan skor 100 üzerinden çıkar ve bir sonraki adımı belirler:"],
             "list": ["90 ve üzeri, Uygun: Nokta standarda uygundur; periyodik kontrol sürer.", "75–89, Takip: İyileştirme gerekir; bulgular takip listesine alınır.", "75'in altı, Aksiyon: Öncelikli müdahale planlanır."],
             "after": "Skordan bağımsız olarak bulgunun önemi de ayrıca değerlendirilir. Kritik bulgu anlık bildirilir, majör bulgu 24 saat içinde aksiyona bağlanır. Böylece genel skoru yüksek bir noktada bile güvenlikle ilgili tek bir sorun beklemeden ele alınır."},
            {"h2": "Uzaktan izleme ile saha kontrolü arasındaki fark",
             "paragraphs": ["Pek çok şarj ağı cihazlarını uzaktan izler. Uzaktan izleme cihazın teknik durumunu gösterir; saha kontrolü ise sürücünün karşılaştığı fiziksel koşulları görünür kılar. Bir ünite yazılım tarafında çalışır görünürken park cebi işgal edilmiş, kablo yerde kalmış ya da yönlendirme tabelası devrilmiş olabilir. İki yöntem birbirinin yerine geçmez, birbirini tamamlar."]},
            {"h2": "Bulgudan iş emrine",
             "paragraphs": ["Kontrol listesi bulguyu kaydetmekle biter; asıl değer, bulgunun kapatılmasıdır. Sağlıklı bir akış şöyle işler:"],
             "list": ["Bulgu fotoğrafla kaydedilir, önceliği belirlenir.", "Fiziksel bulgular (gövde temizliği, zemin, yönlendirme, aydınlatma dış gövdesi) iş emrine dönüşür ve sorumlu ile hedef tarih atanır.",
                      "Elektriksel müdahale gerektiren bulgular yetkili uzmanlara yönlendirilir.", "İş tamamlanınca sonrası fotoğrafıyla kapanış kaydı oluşturulur.", "Bir sonraki kontrolde aynı madde yeniden değerlendirilir."]},
            {"h2": "Yazdırılabilir kısa liste",
             "paragraphs": ["Sahada hızlı kullanım için özet liste:"],
             "list": ["Kablo ve konektör yerde değil, yuvasında", "Gövdede hasar, kırık ya da eksik parça yok", "Ekran açık ve okunabilir, durum ışıkları görünür", "Park cebi boş ve kullanılabilir",
                      "Yönlendirme tabelası görünür ve sağlam", "Aydınlatma dış gövdesi sağlam", "Zemin ve ünite gövdesi temiz", "Logo, renk ve giydirme marka standardına uygun",
                      "Altı fotoğraf çekildi: ön, sağ, sol, ekran, kablo, park alanı"]},
        ],
        "how": {"h2": "BİGEL nasıl yapar?",
                "paragraphs": ["EV Audit30, şarj noktaları için 30 standart kontrol ve 6 ağırlıklı alanla 100 üzerinden saha skoru üretir. Her ziyarette ön, sağ, sol, ekran, kablo ve park alanı fotoğraf seti çekilir; güvenlik maddelerindeki uygunsuzluk aynı gün bildirim üretir, majör bulgular 24 saat içinde aksiyona bağlanır.",
                               "Fiziksel bulgular EV Charge Care kapsamında iş emrine dönüşür: şarj ünitesi dış gövdesi, zemin, yönlendirme ve aydınlatma dış gövdesi bölgesel ekiplerle ele alınır ve sonrası fotoğrafıyla kapanır. Elektriksel bakım yetkili uzmanlarla koordine edilir. Pilot; 10 lokasyon, 2 hafta ve 2 turla başlar."],
                "links": [("Şarj istasyonu denetimi", "ev_audit", ""), ("Şarj istasyonu bakımı", "ev_care", ""), ("BİGEL AUDIT", "audit", ""), ("BİGEL CARE", "care", ""), ("Pilot başlatın", "pilot", "basvuru")]},
        "faq": [("Bu liste resmi denetimin yerini tutar mı?", "Hayır. Bu liste resmi bir denetim ya da elektriksel muayene değildir. Şarj noktalarının saha durumunu fotoğraflı olarak belgeleyen bir kayıttır ve resmi denetimlere hazırlığı destekler. Elektriksel muayene ve testler ilgili mevzuat ve marka standartlarına göre yetkili uzmanlarca yapılır."),
                ("Şarj istasyonu saha kontrolü ne sıklıkla yapılmalı?", "Tek bir doğru aralık yoktur. Kullanım yoğunluğu, konum ve önceki kontrollerin bulguları birlikte değerlendirilmelidir. Bulgu çıkan noktalarda kontrol sıklaştırılabilir; skoru sürekli yüksek olan noktalarda aralık korunabilir."),
                ("Uzaktan izleme varken saha kontrolüne neden ihtiyaç var?", "Uzaktan izleme cihazın teknik durumunu gösterir. Park cebinin işgal edilmesi, kablonun yerde kalması, kirli bir ekran ya da görünmeyen bir yönlendirme tabelası gibi kullanıcı deneyimini etkileyen koşullar ancak sahada görülür."),
                ("Kontrolde hangi fotoğraflar çekilmeli?", "Her ziyarette aynı altı kare çekilmelidir: ön, sağ, sol, ekran, kablo ve park alanı. Bulgu varsa yakın plan bir fotoğraf ve kısa açıklama eklenir.")]},
    "g_fuel_audit": {
        "title": "Akaryakıt Bayi Denetim Kriterleri ve Kontrol Listesi",
        "desc": "Bayi standart denetiminde kanopi, totem, pompa adası ve market girişinde neye bakılır? Denetim alanları, skorlama, kanıt kuralı ve sıklık.",
        "crumb": "Denetim kriterleri",
        "h1": "Akaryakıt istasyonu denetim kriterleri: bayi standart denetiminde neye bakılır?",
        "lead": "Bir istasyonun marka standardına ne kadar uyduğu, kanopiden market girişine kadar sahada görülen ayrıntılarla ölçülür. Bu rehber; bayi standart denetiminde hangi alanlara bakıldığını, "
                "bulguların nasıl puanlandığını, kanıtın nasıl kayda alındığını ve bulguların nasıl kapatıldığını anlatıyor.",
        "intro": "Akaryakıt istasyonlarında iki ayrı denetim türünden söz edilir. Birincisi resmî denetimlerdir: yakıt kalitesi, ölçü aletleri, lisans ve güvenlik yükümlülükleri, ilgili mevzuat çerçevesinde "
                 "yetkili kurum ve kuruluşlar tarafından kontrol edilir. BİGEL bu denetimleri yapmaz. İkincisi marka standart denetimidir: dağıtım şirketi veya ağ sahibi, bayilerinin kurumsal kimliğini, "
                 "görsel uygulamalarını, temizliğini, fiziksel durumunu ve müşteri deneyimini kendi standartlarına göre ölçer ya da bu ölçümü kendi adına bir hizmet sağlayıcıya yaptırır. Bu rehber ikinci "
                 "türü, yani bayi standart denetimini ele alıyor. Amaç, yüzlerce istasyonu aynı ölçütle karşılaştırabilmek ve sorunlu noktaları kanıtıyla birlikte görmektir.",
        "sections": [
            {"h2": "Beş denetim alanı",
             "paragraphs": ["Marka standart denetimi tek bir uzun kontrol listesinden çok, birbirini tamamlayan beş alandan oluşur. BİGEL AUDIT bu alanları Marka (Brand), Görsel (Visual), Temizlik (Clean), Fiziksel Durum (Physical) ve Müşteri Deneyimi (Customer Experience) olarak ayırır. İstasyonda her alan belirli noktalara karşılık gelir.",
                            "Alanları ayırmak raporu okunur kılar. Düşük bir genel skorun kirli bir kanopiden mi, hasarlı bir fiyat panosundan mı yoksa eksik bir yönlendirmeden mi kaynaklandığı ilk bakışta anlaşılır; böylece doğru ekip doğru işe yönlendirilir."],
             "list": ["Marka: kanopi ve totemdeki logo ile kurumsal renklerin doğruluğu, tabelanın güncelliği, fiyat iletişimi ve kampanya materyalinin güncel olması.",
                      "Görsel: totem ve fiyat panosu, ışıklı harfler, folyolar, posterler, market vitrini, stantlar ve varsa dijital ekranların eksiksiz ve okunur olması.",
                      "Temizlik: kanopi yüzeyleri, pompa adası, zemin ve otopark, market giriş camları, çöp alanı ve ortak alanlar.",
                      "Fiziksel durum: duvar, kapı, bariyer, korkuluk, mobilya, ada bordürleri ve zemindeki küçük hasarlar.",
                      "Müşteri deneyimi: istasyonun yoldan fark edilirliği, giriş ve çıkış yönlendirmesi, market girişi, kasa ve bekleme alanı."]},
            {"h2": "Sahada nokta nokta kontrol listesi",
             "paragraphs": ["Beş alan, istasyonun fiziksel bölümleri üzerinden kontrol edildiğinde denetçi sahada daha az şey kaçırır. Aşağıdaki liste tipik bir istasyon turunun iskeletidir; maddelerin ayrıntısı ve ağırlığı her markanın kendi standart kitabına göre belirlenir."],
             "list": ["Kanopi: alın bandında logo ve renklerin bütünlüğü, yüzeyde kir, egzoz izi veya leke, aydınlatmada sönük ya da eksik bölüm, alt yüzeyde görünür hasar.",
                      "Totem ve fiyat panosu: fiyatların okunurluğu ve güncelliği, eksik veya solmuş rakam, kırık panel, ışıklı bölümlerin çalışması, gövde ve kaidede kir veya hasar.",
                      "Pompa adası: ada yüzeyinin ve bordürün temizliği, ada üzerindeki marka ve bilgilendirme materyalleri, çöp kutuları, kaygan zemine yol açabilecek döküntü ve lekeler.",
                      "Market girişi: cam ve kapı temizliği, giriş yönlendirmeleri, vitrin uygulamaları, kampanya posterlerinin güncel kampanyayla uyumu.",
                      "Otopark ve saha çevresi: zemin temizliği, yağ lekeleri, çizgi ve yön işaretlerinin görünürlüğü, çevre düzeni.",
                      "Yönlendirme: giriş-çıkış, hizmet alanları ve market için yön gösteren elemanların yerinde, sağlam ve okunur olması.",
                      "Kampanya materyali: süresi dolmuş materyalin kaldırılması, güncel materyalin doğru yerde ve hasarsız olması."],
             "links": [("Kanopi temizliği rehberi", "g_canopy", ""), ("Totem ve tabela temizliği rehberi", "g_sign", "")]},
            {"h2": "Skorlama nasıl yapılır?",
             "paragraphs": ["BİGEL'in dijital denetim ürünü AUDIT 100; 10 kategori ve 100 kontrol noktasından oluşur. Her madde Uygun (100 puan), Kısmen Uygun (50 puan) veya Uygun Değil (0 puan) olarak değerlendirilir. İstasyonda karşılığı olmayan maddeler, örneğin o lokasyonda bulunmayan bir alanla ilgili kontrol, Uygulanamaz olarak işaretlenir.",
                            "Madde puanları kategori ağırlıklarıyla birleştirilerek 100 üzerinden tek bir lokasyon skoru oluşur. Varsayılan ağırlıklarda İş Güvenliği & Risk ile Marka / Görsel Standart en yüksek paya sahiptir; pilot aşamasında kategori kapsamı, soru seti ve skor ağırlıkları müşteriyle birlikte onaylanır.",
                            "Skor üç renkle okunur: 90–100 standarda uygun (yeşil), 75–89 iyileştirme gerekli (sarı), 0–74 öncelikli aksiyon (kırmızı). Böylece merkez ekip yüzlerce istasyon arasından hangisine önce gidilmesi gerektiğini tek bakışta görür. Varsayılan kategori ağırlıkları şöyledir:"],
             "list": ["Dış Alan & Cephe: 10", "Tabela / Totem / Görsel: 10", "Temizlik & Hijyen: 10", "Mobilya / Ekipman: 10", "Teknik & Fiziksel Durum: 10", "İş Güvenliği & Risk: 15",
                      "Marka / Görsel Standart: 15", "Müşteri Deneyimi: 10", "Operasyon & Uygulama: 5", "Yönetim / Veri / Uygunluk: 5"]},
            {"h2": "Kanıt kuralı: neler kayda alınmalı?",
             "paragraphs": ["Kanıtı olmayan bulgu tartışmaya açıktır. Bu nedenle BİGEL denetiminde her madde fotoğraf, konum, tarih ve açıklamayla kanıtlanır. Fotoğraf kuralı soru bazında tanımlanır: bazı maddelerde fotoğraf yalnızca uygunsuzluk varsa istenir (şartlı), bazılarında her durumda zorunludur, bazılarında ise öncesi ve sonrası fotoğraf gerekir.",
                            "Fotoğrafların karşılaştırılabilir olması için aynı noktanın her ziyarette aynı açıdan çekilmesi önemlidir. Totemin tam cepheden, kanopinin aynı köşeden, pompa adasının aynı yönden çekilmesi; dönemler ve istasyonlar arasında gerçek bir kıyas yapılmasını sağlar."],
             "list": ["Ziyaret tarihi, saati, lokasyon ve denetimi yapan ekip", "Her madde için sonuç: Uygun, Kısmen Uygun, Uygun Değil veya Uygulanamaz",
                      "Uygunsuzluklar için standart açıdan çekilmiş fotoğraf ve kısa açıklama", "Bulgunun önceliği (kritik, yüksek, orta, düşük)", "Önerilen aksiyon ve aksiyonun hangi ekibe ait olduğu"]},
            {"h2": "Denetim ne sıklıkla yapılmalı?",
             "paragraphs": ["Her ağ için geçerli tek bir denetim sıklığı yoktur. Doğru sıklık; istasyon sayısına, bölgesel dağılıma, önceki skorlara, trafik yoğunluğuna, kampanya takvimine ve markanın kendi standart kitabına göre belirlenir. Düşük skor alan istasyonların daha sık ziyaret edilmesi, istikrarlı biçimde yüksek skor alanların ise daha seyrek takvime alınması yaygın bir yaklaşımdır.",
                            "BİGEL AUDIT farklı ihtiyaçlar için farklı hizmet modelleri sunar ve bunlar birlikte kullanılabilir."],
             "list": ["Lokasyon bazlı audit: belirli istasyonlarda tek seferlik denetim.", "Periyodik audit: aylık, üç aylık, altı aylık veya yıllık tekrar eden program.",
                      "Proje audit: kampanya, açılış veya tabela değişimi sonrasında toplu kontrol.", "Franchise audit: bayi ağında standart uyumunun merkez adına ölçülmesi."]},
            {"h2": "Bulgudan iş emrine",
             "paragraphs": ["Denetimin değeri, bulguların kapanmasıyla ortaya çıkar. Skor raporu bir sonraki denetime kadar rafta bekliyorsa aynı bulgular tekrar eder. Bu nedenle her bulgu bir sorumluya, bir hedef tarihe ve bir kapanış kanıtına bağlanmalıdır.",
                            "Temizlik kaynaklı bulgular CLEAN programına, fiziksel hasar ve sabitleme gerektiren bulgular CARE iş emrine dönüşür. İş güvenliği ve risk içeren bulgular ilk sıraya alınır. Elektrik ve mekanik tesisat gibi yasal yetki gerektiren işler uygun uzmanlarla koordine edilir; kapanış, sonrası fotoğrafıyla doğrulanır."],
             "list": ["Bulguyu önceliklendirin: önce güvenlik, sonra marka görünürlüğü, sonra diğerleri.", "Her bulgu için sorumlu ve hedef tarih belirleyin.", "Kapanışı sonrası fotoğrafla kanıtlayın.",
                      "Bir sonraki denetimde kapanan bulguyu yeniden kontrol edin."]},
        ],
        "how": {"h2": "BİGEL nasıl yapar?",
                "paragraphs": ["BİGEL, akaryakıt istasyonu ağları için marka standart denetimini AUDIT 100 ile fotoğraflı ve skorlu olarak yürütür; bulguları CLEAN ve CARE ile sahada kapatır. Denetim çatısı ve AUDIT 100 ayrıntıları BİGEL AUDIT sayfasında yer alır. Sözleşmeden önce seçili istasyonlarda sonucu görmek isterseniz pilot uygulama talep edebilirsiniz."],
                "links": [("Akaryakıt istasyonu denetimi", "fuel_audit", ""), ("Akaryakıt istasyonu temizliği", "fuel_clean", ""), ("BİGEL AUDIT", "audit", ""), ("Pilot başvurusu", "pilot", "basvuru")]},
        "faq": [("Bayi standart denetimi ile resmî denetim arasındaki fark nedir?", "Resmî denetimler yakıt kalitesi, ölçü aletleri, lisans ve güvenlik yükümlülükleri gibi konuları kapsar ve ilgili mevzuat çerçevesinde yetkili kurumlarca yapılır. Bayi standart denetimi ise markanın kurumsal kimlik, görsel uygulama, temizlik, fiziksel durum ve müşteri deneyimi standartlarını ölçer. BİGEL yalnızca ikinci türü yapar."),
                ("AUDIT 100 skoru nasıl hesaplanır?", "10 kategorideki 100 kontrol noktasının her biri Uygun 100, Kısmen Uygun 50 veya Uygun Değil 0 puan alır; karşılığı olmayan maddeler Uygulanamaz işaretlenir. Puanlar kategori ağırlıklarıyla birleştirilerek 100 üzerinden lokasyon skoru oluşur."),
                ("Hangi skor aralığı ne anlama gelir?", "90–100 standarda uygun, 75–89 iyileştirme gerekli, 0–74 öncelikli aksiyon anlamına gelir. Renk kodu sayesinde merkez ekip öncelikli istasyonları hızlıca ayırır."),
                ("Denetim sıklığını nasıl belirlemeliyiz?", "Tek bir doğru sıklık yoktur. İstasyon sayısı, önceki skorlar, kampanya takvimi ve marka standartlarına göre aylık, üç aylık, altı aylık veya yıllık periyodik program kurulabilir; kampanya ya da tabela değişikliği sonrası proje audit eklenebilir."),
                ("Denetimde bulunan sorunlar nasıl kapatılır?", "Temizlik bulguları CLEAN programına, fiziksel bulgular CARE iş emrine dönüşür. Her bulguya sorumlu ve hedef tarih atanır, kapanış sonrası fotoğrafla kanıtlanır.")]},
    "g_sign": {
        "title": "Totem ve Tabela Temizliği: Sıklık ve Planlama",
        "desc": "Totem, fiyat panosu ve ışıklı tabela temizliği nasıl planlanır? Sıklığı belirleyen etkenler, yüzeye uygun temizlik ve temizlik-bakım ayrımı.",
        "crumb": "Totem ve tabela temizliği",
        "h1": "Totem ve tabela temizliği nasıl yapılır, ne sıklıkla planlanır?",
        "lead": "Tabela ve totem, markanın sahadaki ilk temas noktasıdır; kirli bir pano ya da sönük bir harf, müşteri daha içeri girmeden standardın bozulduğunu gösterir. Bu rehber, tabela temizliğini "
                "çok şubeli bir ağda nasıl planlayacağınızı adım adım anlatıyor.",
        "intro": "Kısa cevap: Tüm tabelalar için geçerli tek bir temizlik aralığı yoktur. Sıklık; lokasyonun konumuna, hava koşullarına ve markanın görsel standardına göre planlanmalıdır. Temizlik, "
                 "tabelanın yüzeyine uygun yöntemle yapılmalı; sabitleme, onarım ve elektrik işleri gibi bakım konuları temizlikten ayrı ele alınmalıdır. Aşağıda tabela türlerini, sıklığı belirleyen "
                 "etkenleri, temizlik ile bakım arasındaki farkı ve çok şubeli yapılarda standardı korumanın yollarını bulacaksınız.",
        "sections": [
            {"h2": "Hangi tabela türleri var?",
             "paragraphs": ["Temizlik planı yapmadan önce ağdaki tabela envanterini çıkarmak gerekir. Her tür farklı yükseklikte, farklı malzemeden ve farklı erişim koşullarında olabilir; bu da ekip, ekipman ve süre planını doğrudan etkiler.",
                            "Envanter çıkarılırken her lokasyon için tabelanın türü, yaklaşık konumu, erişim şekli ve ışıklı olup olmadığı kayda alınmalıdır. Bu kayıt hem temizlik planının hem de sonraki denetimlerin temelidir."],
             "list": ["Totem ve fiyat panosu: akaryakıt istasyonlarında yoldan görünen, fiyat ve marka bilgisini taşıyan yüksek yapılar.", "Işıklı harf ve kutu harf: mağaza, restoran ve banka şubelerinin cephesindeki marka yazıları.",
                      "Folyo ve vitrin uygulamaları: cam yüzeylere uygulanan kurumsal ve kampanya grafikleri.", "Yönlendirme elemanları: giriş, çıkış, otopark ve hizmet alanlarını gösteren tabelalar.",
                      "Poster, stant ve dijital ekranlar: kampanya iletişimi taşıyan, daha sık değişen görsel elemanlar."]},
            {"h2": "Yüzeye uygun temizlik",
             "paragraphs": ["Tabela temizliğinin temel ilkesi yüzeye uygun yöntemdir. Kompozit, metal, boyalı yüzey, cam, akrilik ve folyo aynı yöntemle temizlenmez; yanlış yöntem yüzeyi matlaştırabilir, folyoyu kaldırabilir ya da renkleri soldurabilir. Bu nedenle her tabela türü için yöntem, ekipman ve kimyasal standardı önceden belirlenmeli ve ekiplerin tamamı aynı standardı uygulamalıdır. Kullanılacak ürünler için tabela üreticisinin önerileri ve marka standartları esas alınmalıdır.",
                            "Işıklı tabelalarda dikkat gerekir. Temizlik sırasında elektrikli bileşenlere, bağlantı noktalarına ve kablolara müdahale edilmemelidir. Sönük harf, arızalı aydınlatma veya hasarlı kablo gibi elektrik konuları yetkili uzmanlara bırakılır; temizlik ekibi bunları fotoğraflayıp bildirir.",
                            "Yüksekte çalışma gerektiren totem ve cephe tabelalarında güvenli erişim planı, işe başlamadan önce yapılmalıdır. Ekipman, çalışma alanının çevrilmesi ve trafiğin güvenli yönetimi, ilgili mevzuat ve marka standartları doğrultusunda planlanmalıdır."],
             "list": ["Her tabela türü için yöntem ve ekipman standardı tanımlayın.", "Işıklı tabelalarda elektrikli bileşenlerden uzak durun; arızayı bildirin, müdahale etmeyin.",
                      "Yüksekte çalışmayı önceden planlayın, çalışma alanını güvenli hale getirin.", "İşlem öncesinde ve sonrasında aynı açıdan fotoğraf çekin."]},
            {"h2": "Temizlik mi, bakım mı?",
             "paragraphs": ["Tabela sahada iki farklı ihtiyaç doğurur ve bu ikisini karıştırmak plan ile bütçeyi bulandırır. Temizlik; toz, egzoz izi, kir ve lekenin giderilerek tabelanın görünürlüğünün geri kazanılmasıdır. BİGEL'de bu iş CLEAN altındaki Tabela ve Totem Clean modülüyle yapılır.",
                            "Bakım ise tabelanın fiziksel durumuyla ilgilidir: gevşemiş bağlantının sabitlenmesi, küçük onarımlar, hasarlı parçaların düzeltilmesi. BİGEL'de bu iş CARE altındaki Sign Care modülüyle yürütülür. Temizlik sırasında fark edilen bakım ihtiyacı fotoğrafla kaydedilir ve ayrı bir iş emrine dönüşür; böylece temizlik ekibi kendi kapsamı dışındaki işi yapmaz, bulgu da kaybolmaz."]},
            {"h2": "Sıklığı belirleyen etkenler",
             "paragraphs": ["Temizlik sıklığını tek bir takvim yerine etkenlere göre belirlemek, hem kaynakları doğru kullanmayı hem de görünürlüğü korumayı sağlar. Aynı ağ içinde bile lokasyonlar farklı sıklıkta ziyaret edilebilir.",
                            "Pratikte lokasyonları gruplara ayırmak işe yarar: yoğun yol kenarındaki noktalar daha sık, korunaklı noktalar daha seyrek takvime alınır. Periyodik program aylık, iki aylık, üç aylık veya mevsimsel olarak kurulabilir; ani kirlenme ya da denetim öncesi ihtiyaçlarda acil müdahale eklenir."],
             "list": ["Yol kenarı tozu ve egzoz: yoğun trafiğe bakan totem ve tabelalar daha hızlı kirlenir.", "Mevsim: kış kiri, çamur ve yaprak dönemi; bazı bölgelerde sezona göre ek ziyaret gerekir.",
                      "Kampanya değişimi: yeni kampanya materyali uygulanmadan önce ve sonra tabelanın temiz olması beklenir.", "Denetim bulgusu: denetimde tabela temizliği uygunsuz bulunan lokasyonlar programa öncelikli alınır.",
                      "Marka standardı: bazı markalar görünürlük için daha sık temizlik talep eder."]},
            {"h2": "Çok şubede tabela standardı",
             "paragraphs": ["Tek bir lokasyonda tabela temizliği basit bir iştir. Yüzlerce şubede ise asıl sorun, her noktada aynı sonucu almak ve bunu merkezden görebilmektir. Farklı şehirlerde farklı tedarikçilerle çalışmak; farklı kalite, farklı raporlama ve karşılaştırılamayan sonuçlar demektir.",
                            "Standardı korumanın yolu, uygulamayı ve kanıtı ortaklaştırmaktır. Tabela değişimi veya yeni kampanya sonrasında tüm ağda toplu kontrol yapmak da uygulamanın eksiksiz olduğunu teyit eder."],
             "list": ["Tek hizmet sağlayıcı ve tek muhatap ile tüm ağı yönetin.", "Ortak kontrol listesi: tabelanın temizliği, okunurluğu, aydınlatması ve hasar durumu.",
                      "Standart fotoğraf açıları: her tabelayı her ziyarette aynı açıdan kaydedin.", "Kayıt: tarih, lokasyon, ekip, öncesi ve sonrası fotoğraf, tespit edilen bakım ihtiyacı.",
                      "Tabela değişimi veya kampanya sonrası proje audit ile toplu kontrol."]},
            {"h2": "Sektöre göre tabela temizliği",
             "paragraphs": ["Tabela temizliğinin kapsamı sektöre göre değişir. Akaryakıt istasyonlarında totem ve fiyat panosu öne çıkarken zincir mağazalarda cephe tabelası ve vitrin, restoranlarda cephe, tabela ve arabaya servis alanı, banka şubelerinde ise cephe tabelası ile ATM çevresi ön plandadır. Sektörünüze özel kapsam için ilgili sayfalara göz atabilirsiniz."],
             "links": [("Akaryakıt istasyonu temizliği", "fuel_clean", ""), ("Zincir mağaza temizliği", "retail", ""), ("Restoran dış alan temizliği", "restaurant", ""), ("Banka şubesi ve ATM temizliği", "bank", "")]},
        ],
        "how": {"h2": "BİGEL nasıl yapar?",
                "paragraphs": ["BİGEL, tabela ve totem temizliğini CLEAN programı içinde Tabela ve Totem Clean modülüyle planlar; her ziyaret görev kapsamı, standart açılardan öncesi fotoğrafı, uygulama, sonrası fotoğrafı ve kapanış kaydıyla yürür. Temizlikte fark edilen bakım ihtiyaçları CARE altında Sign Care iş emrine dönüşür."],
                "links": [("BİGEL CLEAN", "clean", ""), ("BİGEL CARE", "care", ""), ("Pilot başvurusu", "pilot", "basvuru")]},
        "faq": [("Totem ve tabela ne sıklıkla temizlenmeli?", "Tek bir doğru aralık yoktur. Lokasyonun yola yakınlığı, toz ve egzoz yükü, mevsim, kampanya takvimi ve marka standardına göre aylık, iki aylık, üç aylık veya mevsimsel bir program kurulabilir; denetim bulgusu olan noktalar öncelikli alınır."),
                ("Işıklı tabela temizliğinde nelere dikkat edilmeli?", "Temizlik yüzeye uygun yöntemle yapılmalı, elektrikli bileşenlere ve bağlantılara müdahale edilmemelidir. Sönük harf veya arızalı aydınlatma gibi elektrik konuları fotoğrafla bildirilir ve yetkili uzmanlara bırakılır."),
                ("Tabela temizliği ile tabela bakımı arasındaki fark nedir?", "Temizlik kir, toz ve lekeyi gidererek görünürlüğü geri kazandırır. Bakım ise sabitleme, küçük onarım ve hasarlı parçaların düzeltilmesi gibi fiziksel müdahaleleri kapsar. BİGEL'de temizlik CLEAN, bakım CARE altında yürür."),
                ("Çok şubeli bir ağda tabela standardı nasıl korunur?", "Tek hizmet sağlayıcı, ortak kontrol listesi, standart fotoğraf açıları ve merkezi raporlama ile. Tabela değişimi veya kampanya sonrasında yapılan toplu kontrol, uygulamanın tüm şubelerde eksiksiz olduğunu teyit eder.")]},
}
CONTENT["en"]["guides"] = {
    "g_canopy": {
        "title": "How Often Should a Fuel Station Canopy Be Cleaned?",
        "desc": "There is no single cleaning interval for a fuel station canopy. Learn how traffic, location, season and brand standards set the right frequency.",
        "crumb": "Canopy cleaning",
        "h1": "How often should a fuel station canopy be cleaned?",
        "lead": "Short answer: there is no single cleaning interval that suits every fuel station canopy. The right frequency depends on the station's traffic, its location (motorway, city or industrial "
                "area), the season and the brand standard. The most reliable interval is set from the findings of periodic site checks and adjusted as they change.",
        "intro": "In this guide, canopy means the large roof structure over the pump islands of a fuel station that carries the brand identity, not a shop awning or porch roof. The fuel station canopy is the "
                 "face of the station seen from the road: if the fascia colours look faded or soot has built up on the ceiling, drivers notice before they even pull in. Below we cover what kinds of dirt "
                 "build up on a canopy, which factors set the cleaning frequency, how to plan the work while the station is open and how to prove the cleaning was done.",
        "sections": [
            {"h2": "What builds up on a canopy?",
             "paragraphs": ["Canopy surfaces sit outdoors, directly above vehicle traffic. The dirt is not one type, and each type builds up at a different rate. The most common in the field are:"],
             "list": ["Atmospheric dirt: airborne particles that stick to the surface and turn it grey over time.", "Dust: rises quickly in dry periods and near roadworks, construction or open land.",
                      "Exhaust marks: dark traces left by idling and manoeuvring vehicles, usually concentrated right above the pump islands.",
                      "Soot: most visible on the ceiling and lower fascia edge at stations with heavy goods traffic.",
                      "Biological soiling: bird droppings, moss and stains from damp periods, which should be removed in time to avoid surface damage."]},
            {"h2": "Factors that set the frequency",
             "paragraphs": ["Canopy cleaning frequency is a site decision more than a calendar decision. Two stations of the same brand can soil at very different rates. Weigh these factors together when planning:"],
             "list": ["Traffic and location: exhaust marks and soot build up much faster at a motorway station with heavy goods traffic than at a city station. Dust and atmospheric dirt dominate in industrial areas.",
                      "Season: winter grime, mud, leaves and moss rise with the seasons. A seasonal programme puts these periods in the calendar in advance.",
                      "Campaigns and rebranding: before new campaign graphics, a logo refresh or a brand change, the canopy needs to be clean, otherwise new visuals look dull next to old grime.",
                      "Audit findings: recurring canopy findings in periodic site audits show the current interval is not enough. If no findings appear, the interval can stay; if they keep appearing, frequency should go up.",
                      "Brand standard: some networks set their own internal appearance standards. The cleaning plan should align with them."],
             "after": "A practical method: group the network's stations by traffic and location, give each group a starting interval, then compare the before photos of the first few visits to tighten or relax it."},
            {"h2": "Cleaning while the station is open",
             "paragraphs": ["Fuel stations often run without a break. Because canopy cleaning happens right above the pump islands, it must not clash with customer traffic. The best time is after closing or during the quietest hours. Night cleaning is done without disrupting the station's operations.",
                            "Before work starts, the work area should be defined and marked, access to pump islands restricted only as much as needed, and the station manager should agree which islands close and when. Chemical selection and working-at-height safety should follow the applicable regulations and brand standards.",
                            "Needs also arise outside the plan: sudden soiling, build-up after bad weather, vandalism or an upcoming audit. How to request an emergency clean for these cases should be defined in advance."]},
            {"h2": "Fascia, ceiling and around the lighting",
             "paragraphs": ["Canopy cleaning is more than one surface. Writing the scope down from the start removes ambiguity for both the crew and station management. A typical scope includes:"],
             "list": ["Fascia: the most visible surface, carrying the brand colours and logo.", "Ceiling: where exhaust marks and soot gather most.", "Columns: the part most exposed to vehicle and human contact.",
                      "Around the lighting: the surfaces surrounding the light fittings."],
             "after": "An important boundary: electrical work on light fittings is not part of cleaning. If an electrical issue is noticed, it is recorded as a finding and passed to authorised specialists."},
            {"h2": "How do you prove the cleaning was done?",
             "paragraphs": ["In a multi-site network the central team cannot visit every station. The record that shows cleaning took place matters as much as the cleaning itself. We recommend recording the following at every visit:"],
             "list": ["Before and after photos taken from the same angles", "Visit date and site details", "Scope delivered: fascia, ceiling, columns, around the lighting",
                      "Any damage or maintenance need noticed during the work", "Quality check against a checklist"],
             "after": "Photos from standard angles become comparable over time, so you can see with data which stations soil faster. In periodic site audits, the cleanliness and visual standard items also show the canopy's condition independently.",
             "links": [("Fuel station audit criteria", "g_fuel_audit", "")]},
            {"h2": "Planning across many stations",
             "paragraphs": ["Planning cleaning for one station is easy; the challenge is holding the same standard across dozens or hundreds. This approach works for a multi-site network:"],
             "list": ["Central plan: one service definition and an annual calendar for all stations.", "Grouping: group stations by traffic, location and region, and set an interval per group.",
                      "Regional teams: deliver the work with crews in the region to cut travel time.", "Shared checklist: the same scope, photo angles and quality criteria at every station.",
                      "Feedback loop: review intervals periodically against audit findings."]},
        ],
        "how": {"h2": "How BİGEL does it",
                "paragraphs": ["BİGEL CLEAN manages canopy, signage, totem, façade and car park cleaning across Türkiye to one standard. Canopy Clean covers the periodic removal of atmospheric dirt, dust, exhaust marks, soot and biological soiling. Night Clean is scheduled after closing hours, Emergency Clean responds to sudden soiling or pre-audit needs, and Seasonal Clean is built around winter grime, moss, leaves and mud. Every visit is verified with before and after photos.",
                               "A periodic package can be monthly, bi-monthly, quarterly or seasonal; we set the right option together based on your stations' conditions. To measure canopy condition independently, AUDIT 100 provides photo-verified site audits. Planning is central and delivery runs through regional teams across Türkiye."],
                "links": [("Fuel station cleaning", "fuel_clean", ""), ("Fuel station audit", "fuel_audit", ""), ("BİGEL CLEAN", "clean", ""), ("Start a pilot", "pilot", "apply")]},
        "faq": [("How often should a fuel station canopy be cleaned?", "There is no one-size-fits-all interval. Frequency depends on traffic, location, season and brand standard. The most reliable approach is to start with an initial interval and adjust it based on findings from periodic site checks."),
                ("Can the canopy be cleaned while the station is open?", "Yes, but after closing or the quietest hours are preferred so the work does not clash with customer traffic. The work area is marked and the station manager agrees in advance which pump islands close and when."),
                ("Does canopy cleaning include the light fittings?", "The surfaces around the fittings are in scope. Electrical work on the fittings is not; if an electrical issue is noticed, it is recorded as a finding and passed to authorised specialists."),
                ("How can I track from head office that cleaning was done?", "Each visit should record before and after photos from the same angles, the date and site details, and a completed checklist. These records let you compare stations with each other and over time.")]},
    "g_ev": {
        "title": "EV Charging Station Checklist: 6 Areas to Check",
        "desc": "What should you check on site at an EV charging station? A 6-area checklist from safety to brand standard, photo set, score thresholds and work orders.",
        "crumb": "EV charging station checklist",
        "h1": "EV charging station checklist: what to check on site",
        "lead": "Checking an EV charging station has two layers: electrical periodic inspection and testing carried out by authorised specialists, and the physical conditions drivers meet on site. This "
                "guide focuses on the second layer and explains what to check in 6 areas and what to record.",
        "intro": "Most sources on charging station checks cover electrical tests and regulation. That work is the responsibility of authorised specialists and follows the applicable regulations and brand "
                 "standards; it is not the subject of this guide. Yet much of what shapes a driver's experience at a charging point has nothing to do with electricity: a cable left on the ground, an "
                 "unreadable screen, a bay occupied by another vehicle or a wayfinding sign that cannot be seen at night. The checklist below is designed to record these site conditions regularly and comparably.",
        "sections": [
            {"h2": "The 6-area site checklist",
             "paragraphs": ["The list follows the six weighted areas of EV Audit30. The numbers in brackets are each area's weight in the score out of 100. The items are not technical tests; they are points to look at on site and record with photos.",
                            "1. Safety (25, 5 critical checks): Is the cable or connector lying on the ground or across a walkway? Is the connector seated properly in its holder? Is there any obstacle around the unit that could cause a trip? Is any part of the housing exposed, broken or hanging loose? Is the floor slippery? Non-conformities in this area should be reported the same day.",
                            "2. Device integrity (20): Is there impact damage, a crack, a broken cover or a missing part on the housing? Is there visible damage to the cable sheath? Are labels and information panels in place?",
                            "3. Function indicators (20): Is the screen on and readable? Are status lights visible? Does the screen show guidance for the user or an error message? These items are judged only from what the user sees, without looking inside the device.",
                            "4. User experience (15): Is the bay free and usable, or occupied by another vehicle? Can the wayfinding sign be seen from the station entrance? Is the light fitting housing intact and is the area visible after dark? Does the cable reach the vehicle comfortably?",
                            "5. Cleanliness and surroundings (10): Is the floor clean, or are there oil stains, litter or leaves? Are the unit housing and screen surface clean? Does any part of the surroundings look neglected?",
                            "6. Brand standard (10): Do the logo, colours and graphics meet the brand standard? Is there peeling vinyl, faded colour or out-of-date information?"]},
            {"h2": "Photo set: the same six shots every visit",
             "paragraphs": ["A checklist is only as useful as its records are comparable. Take the same photo set at every visit:"],
             "list": ["Front", "Right", "Left", "Screen", "Cable", "Bay"],
             "after": "Store photos with date, time and location. If there is a finding, add a close-up and a short note. Shots from the same angles make it easy to see how one point changes over time and how points differ from each other."},
            {"h2": "Score and action thresholds",
             "paragraphs": ["The score, calculated with each area's weight, comes out of 100 and sets the next step:"],
             "list": ["90 and above, Compliant: the point meets the standard; periodic checks continue.", "75–89, Follow-up: improvement is needed; findings go on a follow-up list.", "Below 75, Action: priority intervention is planned."],
             "after": "Independently of the score, each finding's severity is assessed. Critical findings are reported instantly; major findings are actioned within 24 hours. This way a single safety issue is handled without delay, even at a point with a high overall score."},
            {"h2": "Remote monitoring versus site checks",
             "paragraphs": ["Many charging networks monitor their devices remotely. Remote monitoring shows the device's technical state; a site check makes the physical conditions drivers actually meet visible. A unit can look healthy in software while its bay is occupied, its cable is on the ground or its wayfinding sign has fallen over. The two methods do not replace each other; they complement each other."]},
            {"h2": "From finding to work order",
             "paragraphs": ["A checklist ends with recording the finding; the real value is closing it. A healthy flow works like this:"],
             "list": ["The finding is recorded with a photo and given a priority.", "Physical findings (housing cleanliness, floor, wayfinding, light fitting housing) become work orders with an owner and due date.",
                      "Findings needing electrical intervention are passed to authorised specialists.", "When the work is done, a closure record is created with an after photo.", "The same item is reassessed at the next check."]},
            {"h2": "Printable short list",
             "paragraphs": ["A summary list for quick use on site:"],
             "list": ["Cable and connector off the ground, in the holder", "No damage, cracks or missing parts on the housing", "Screen on and readable, status lights visible", "Bay free and usable",
                      "Wayfinding sign visible and intact", "Light fitting housing intact", "Floor and unit housing clean", "Logo, colours and graphics meet the brand standard",
                      "Six photos taken: front, right, left, screen, cable, bay"]},
        ],
        "how": {"h2": "How BİGEL does it",
                "paragraphs": ["EV Audit30 produces a site score out of 100 for charging points, with 30 standard checks and 6 weighted areas. Each visit takes the photo set of front, right, left, screen, cable and bay; safety non-conformities trigger a same-day alert and major findings are actioned within 24 hours.",
                               "Physical findings become work orders under EV Charge Care: charger housing, floor, wayfinding and light fittings are handled by regional teams and closed with an after photo. Electrical maintenance is coordinated with certified specialists. A pilot starts with 10 sites, 2 weeks and 2 rounds."],
                "links": [("EV charging station audit", "ev_audit", ""), ("EV charging station maintenance", "ev_care", ""), ("BİGEL AUDIT", "audit", ""), ("BİGEL CARE", "care", ""), ("Start a pilot", "pilot", "apply")]},
        "faq": [("Does this checklist replace an official regulatory inspection?", "No. This list is not an official inspection or an electrical test. It is a photo-based record of the site condition of your charging points that supports preparation for official inspections. Electrical inspection and testing is carried out by authorised specialists under the applicable regulations and brand standards."),
                ("How often should site checks be done at a charging station?", "There is no single right interval. Usage, location and findings from earlier checks should be weighed together. Checks can be made more frequent at points with findings; the interval can stay where scores are consistently high."),
                ("Why do I need site checks if I have remote monitoring?", "Remote monitoring shows the device's technical state. Conditions that affect the driver, such as an occupied bay, a cable on the ground, a dirty screen or a sign that cannot be seen, are only visible on site."),
                ("Which photos should be taken during a check?", "The same six shots at every visit: front, right, left, screen, cable and bay. If there is a finding, add a close-up and a short note.")]},
    "g_fuel_audit": {
        "title": "Fuel Station Audit Checklist: Brand Standards",
        "desc": "What does a fuel station brand standard audit check? Canopy, pylon, pump island and shop entrance criteria, scoring, evidence rules and frequency.",
        "crumb": "Audit criteria",
        "h1": "Fuel station audit criteria: what does a brand standard audit check?",
        "lead": "How closely a station meets its brand standard is measured by details you can see on site, from the canopy to the shop entrance. This guide explains which areas a brand standard audit "
                "covers, how findings are scored, how evidence is recorded and how findings get closed.",
        "intro": "Two different kinds of inspection apply to fuel stations. The first is official inspection: fuel quality, measuring instruments, licensing and safety obligations are checked by authorised "
                 "bodies under the relevant regulations. BİGEL does not carry out these inspections. The second is the brand standard audit: the fuel distributor or network owner measures its dealers' "
                 "corporate identity, visual execution, cleanliness, physical condition and customer experience against its own standards, or has a service provider do this on its behalf. This guide "
                 "covers the second kind. The goal is to compare hundreds of stations against the same yardstick and see problem sites together with their evidence.",
        "sections": [
            {"h2": "Five audit areas",
             "paragraphs": ["A brand standard audit is less one long checklist than five complementary areas. BİGEL AUDIT separates them into Brand, Visual, Clean, Physical and Customer Experience. At a station, each area maps to specific points on the forecourt.",
                            "Separating the areas makes the report readable. You can see at a glance whether a low overall score comes from a dirty canopy, a damaged price board or missing wayfinding, so the right team is sent to the right job."],
             "list": ["Brand: correct logo and corporate colours on the canopy and pylon, current signage, price communication and up-to-date campaign material.",
                      "Visual: pylon and price board, illuminated letters, vinyl, posters, shopfront, stands and any digital screens complete and legible.",
                      "Clean: canopy surfaces, pump islands, forecourt and car park, shop entrance glass, waste area and common areas.",
                      "Physical: walls, doors, barriers, railings, furniture, island kerbs and minor surface damage.",
                      "Customer Experience: visibility from the road, entry and exit wayfinding, shop entrance, checkout and waiting area."]},
            {"h2": "An on-site checklist, point by point",
             "paragraphs": ["When the five areas are checked by walking the station's physical zones, auditors miss less. The list below is the skeleton of a typical station walk; the detail and weight of each item follow each brand's own standards manual."],
             "list": ["Canopy: integrity of logo and colours on the fascia, dirt, exhaust marks or stains, dim or missing lighting sections, visible damage underneath.",
                      "Pylon and price board: legible, current prices, missing or faded digits, broken panels, working illuminated sections, dirt or damage on the body and base.",
                      "Pump island: clean island surface and kerb, brand and information material on the island, bins, spills or stains that could make the surface slippery.",
                      "Shop entrance: clean glass and doors, entrance wayfinding, shopfront graphics, campaign posters matching the current campaign.",
                      "Car park and surroundings: clean surfaces, oil stains, visible line and direction markings, general tidiness.",
                      "Wayfinding: entry, exit, service area and shop signs in place, secure and legible.",
                      "Campaign material: expired material removed, current material in the right place and undamaged."],
             "links": [("Canopy cleaning guide", "g_canopy", ""), ("Pylon and sign cleaning guide", "g_sign", "")]},
            {"h2": "How is scoring done?",
             "paragraphs": ["BİGEL's digital audit product, AUDIT 100, consists of 10 categories and 100 checkpoints. Each item is rated Compliant (100 points), Partial (50 points) or Non-compliant (0 points). Items that do not apply at a given station, for example a check for an area the site does not have, are marked Not applicable.",
                            "Item scores are combined with category weights into a single site score out of 100. In the default weighting, Safety & Risk and Brand / Visual Standard carry the largest share; during a pilot, the category scope, question set and score weights are agreed with the client.",
                            "The score reads in three colours: 90–100 meets standard (green), 75–89 improvement needed (amber), 0–74 priority action (red). Head office can see at a glance which of hundreds of stations to visit first. The default category weights are:"],
             "list": ["Exterior & Façade: 10", "Signage / Totem / Visual: 10", "Cleanliness & Hygiene: 10", "Furniture / Equipment: 10", "Technical & Physical Condition: 10", "Safety & Risk: 15",
                      "Brand / Visual Standard: 15", "Customer Experience: 10", "Operations & Execution: 5", "Management / Data / Compliance: 5"]},
            {"h2": "The evidence rule: what to record",
             "paragraphs": ["A finding without evidence invites argument. That is why every item in a BİGEL audit is evidenced with a photo, location, date and description. The photo rule is defined per question: some items need a photo only when there is a non-compliance (conditional), some always require one (mandatory), and some need before-and-after photos.",
                            "For photos to be comparable, the same point should be shot from the same angle on every visit. Shooting the pylon straight on, the canopy from the same corner and the pump island from the same direction makes real comparison between periods and stations possible."],
             "list": ["Visit date, time, site and the team carrying out the audit", "Result for each item: Compliant, Partial, Non-compliant or Not applicable", "A photo from the standard angle and a short note for each non-compliance",
                      "Priority of the finding (critical, high, medium, low)", "Recommended action and which team owns it"]},
            {"h2": "How often should stations be audited?",
             "paragraphs": ["There is no single audit frequency that suits every network. The right cadence depends on the number of stations, regional spread, previous scores, traffic, the campaign calendar and the brand's own standards manual. A common approach is to visit low-scoring stations more often and move consistently high-scoring ones to a lighter schedule.",
                            "BİGEL AUDIT offers service models for different needs, and they can be combined."],
             "list": ["Site-based audit: a one-off audit at selected stations.", "Periodic audit: a monthly, quarterly, semi-annual or annual recurring programme.",
                      "Project audit: a bulk check after campaigns, openings or signage changes.", "Franchise audit: measuring standard compliance across a dealer network on behalf of head office."]},
            {"h2": "From finding to work order",
             "paragraphs": ["An audit pays off when findings are closed. If the score report sits on a shelf until the next audit, the same findings come back. Every finding should therefore be tied to an owner, a target date and closure evidence.",
                            "Cleaning findings feed into the CLEAN programme; physical damage and anything that needs fixing becomes a CARE work order. Safety and risk findings go first. Work that requires legal authorisation, such as electrical or mechanical installations, is coordinated with qualified specialists, and closure is verified with an after photo."],
             "list": ["Prioritise: safety first, then brand visibility, then the rest.", "Assign an owner and target date to each finding.", "Prove closure with an after photo.", "Recheck closed findings at the next audit."]},
        ],
        "how": {"h2": "How BİGEL does it",
                "paragraphs": ["BİGEL runs brand standard audits for fuel station networks with AUDIT 100, photo-verified and scored, and closes findings on site with CLEAN and CARE. The audit framework and AUDIT 100 details are on the BİGEL AUDIT page. To see results at selected stations before signing a contract, request a pilot."],
                "links": [("Fuel station audit", "fuel_audit", ""), ("Fuel station cleaning", "fuel_clean", ""), ("BİGEL AUDIT", "audit", ""), ("Pilot application", "pilot", "apply")]},
        "faq": [("What is the difference between a brand standard audit and an official inspection?", "Official inspections cover topics such as fuel quality, measuring instruments, licensing and safety obligations and are carried out by authorised bodies under the relevant regulations. A brand standard audit measures the brand's corporate identity, visual execution, cleanliness, physical condition and customer experience standards. BİGEL only does the second."),
                ("How is the AUDIT 100 score calculated?", "Each of the 100 checkpoints across 10 categories scores Compliant 100, Partial 50 or Non-compliant 0; items that do not apply are marked Not applicable. Scores are combined with category weights into a site score out of 100."),
                ("What do the score bands mean?", "90–100 means meets standard, 75–89 improvement needed and 0–74 priority action. The colour code lets head office quickly pick out priority stations."),
                ("How should we set audit frequency?", "There is no single right frequency. Depending on station count, previous scores, campaign calendar and brand standards, you can run a monthly, quarterly, semi-annual or annual periodic programme and add project audits after campaigns or signage changes."),
                ("How are audit findings closed?", "Cleaning findings go into the CLEAN programme and physical findings become CARE work orders. Each finding gets an owner and target date, and closure is proven with an after photo.")]},
    "g_sign": {
        "title": "Pylon and Sign Cleaning: Frequency and Planning",
        "desc": "How to plan cleaning for pylons, price boards and illuminated signs: what drives frequency, surface-appropriate cleaning and cleaning vs maintenance.",
        "crumb": "Pylon and sign cleaning",
        "h1": "How should pylons and signs be cleaned, and how often?",
        "lead": "Signs and pylons are a brand's first point of contact in the field; a dirty board or an unlit letter shows the standard has slipped before a customer even walks in. This guide explains "
                "step by step how to plan sign cleaning across a multi-site network.",
        "intro": "The short answer: there is no single cleaning interval that fits every sign. Frequency should be planned around location, weather and the brand's visual standard. Cleaning should use a "
                 "method suited to the sign's surface, and maintenance topics such as fixing, repairs and electrical work should be handled separately from cleaning. Below you will find the types of "
                 "signage, the factors that drive frequency, the difference between cleaning and maintenance, and how to hold the standard across many branches.",
        "sections": [
            {"h2": "What types of signage are there?",
             "paragraphs": ["Before planning cleaning, build a signage inventory for the network. Each type can sit at a different height, be made of different materials and have different access conditions, which directly affects team, equipment and time planning.",
                            "For each site, record the sign type, its approximate position, how it is accessed and whether it is illuminated. This record is the basis of both the cleaning plan and later audits."],
             "list": ["Pylons and price boards: tall structures at fuel stations carrying price and brand information visible from the road.", "Illuminated and box letters: brand lettering on the façades of shops, restaurants and bank branches.",
                      "Vinyl and shopfront graphics: corporate and campaign graphics applied to glass.", "Wayfinding: signs for entry, exit, car park and service areas.",
                      "Posters, stands and digital screens: visual elements carrying campaign messages that change more often."]},
            {"h2": "Surface-appropriate cleaning",
             "paragraphs": ["The core principle of sign cleaning is a method suited to the surface. Composite, metal, painted surfaces, glass, acrylic and vinyl are not cleaned the same way; the wrong method can dull a surface, lift vinyl or fade colours. Method, equipment and chemical standards should therefore be set in advance for each sign type, and every team should apply the same standard. The sign manufacturer's recommendations and brand standards should guide product choice.",
                            "Illuminated signs need care. Electrical components, connection points and cables must not be touched during cleaning. Electrical issues such as unlit letters, faulty lighting or damaged cables are left to authorised specialists; the cleaning team photographs and reports them.",
                            "For pylons and façade signs that require work at height, a safe access plan should be in place before work starts. Equipment, cordoning off the work area and safe traffic management should be planned in line with the relevant regulations and brand standards."],
             "list": ["Define a method and equipment standard for each sign type.", "Keep away from electrical components on illuminated signs; report faults, do not fix them.",
                      "Plan work at height in advance and secure the work area.", "Take before and after photos from the same angle."]},
            {"h2": "Cleaning or maintenance?",
             "paragraphs": ["Signage creates two different needs on site, and mixing them up blurs both the plan and the budget. Cleaning removes dust, exhaust marks, dirt and stains to restore visibility. At BİGEL this is done with the Signage & Totem Clean module under CLEAN.",
                            "Maintenance concerns the sign's physical condition: securing loose fixings, minor repairs and correcting damaged parts. At BİGEL this runs under the Sign Care module of CARE. Any maintenance need spotted during cleaning is photographed and turned into a separate work order, so the cleaning team does not work outside its scope and the finding is not lost."]},
            {"h2": "What drives cleaning frequency?",
             "paragraphs": ["Setting frequency by factors rather than a single calendar uses resources well and protects visibility. Even within one network, sites can be visited at different intervals.",
                            "In practice, grouping sites helps: roadside locations with heavy traffic go on a tighter schedule, sheltered ones on a lighter one. A periodic programme can be monthly, bi-monthly, quarterly or seasonal, with emergency visits added for sudden soiling or before an audit."],
             "list": ["Roadside dust and exhaust: pylons and signs facing heavy traffic get dirty faster.", "Season: winter grime, mud and leaf fall; some regions need extra seasonal visits.",
                      "Campaign changes: signs are expected to be clean before and after new campaign material goes up.", "Audit findings: sites where sign cleanliness failed an audit are prioritised.",
                      "Brand standard: some brands require more frequent cleaning for visibility."]},
            {"h2": "Holding the signage standard across many branches",
             "paragraphs": ["Cleaning a sign at one site is simple. Across hundreds of branches, the real challenge is getting the same result everywhere and being able to see it from head office. Working with different suppliers in different cities means different quality, different reporting and results you cannot compare.",
                            "The way to hold the standard is to share both the execution and the evidence. A network-wide check after a signage change or a new campaign also confirms that the rollout is complete."],
             "list": ["Manage the whole network with one provider and one point of contact.", "A shared checklist: cleanliness, legibility, lighting and damage.",
                      "Standard photo angles: record each sign from the same angle on every visit.", "Records: date, site, team, before and after photos, maintenance needs identified.",
                      "A project audit after signage changes or campaigns for a bulk check."]},
            {"h2": "Sign cleaning by sector",
             "paragraphs": ["The scope of sign cleaning varies by sector. At fuel stations the pylon and price board come first; in chain retail it is the façade sign and shopfront; at restaurants the façade, signage and drive-thru area; at bank branches the façade sign and the ATM surroundings. See the sector pages for scope."],
             "links": [("Fuel station cleaning", "fuel_clean", ""), ("Retail store cleaning", "retail", ""), ("Restaurant exterior cleaning", "restaurant", ""), ("Bank branch and ATM cleaning", "bank", "")]},
        ],
        "how": {"h2": "How BİGEL does it",
                "paragraphs": ["BİGEL plans sign and pylon cleaning within the CLEAN programme using the Signage & Totem Clean module; every visit runs through task scope, a before photo from standard angles, execution, an after photo and a closure record. Maintenance needs found during cleaning become Sign Care work orders under CARE."],
                "links": [("BİGEL CLEAN", "clean", ""), ("BİGEL CARE", "care", ""), ("Pilot application", "pilot", "apply")]},
        "faq": [("How often should pylons and signs be cleaned?", "There is no single right interval. Depending on proximity to the road, dust and exhaust load, season, campaign calendar and brand standard, a monthly, bi-monthly, quarterly or seasonal programme can be set up, with sites flagged in audits prioritised."),
                ("What should be considered when cleaning illuminated signs?", "Use a surface-appropriate method and do not touch electrical components or connections. Electrical issues such as unlit letters or faulty lighting are photographed, reported and left to authorised specialists."),
                ("What is the difference between sign cleaning and sign maintenance?", "Cleaning removes dirt, dust and stains to restore visibility. Maintenance covers physical work such as securing fixings, minor repairs and correcting damaged parts. At BİGEL, cleaning runs under CLEAN and maintenance under CARE."),
                ("How do you keep a signage standard across a multi-site network?", "With one provider, a shared checklist, standard photo angles and central reporting. A bulk check after signage changes or campaigns confirms the rollout is complete at every branch.")]},
}

# ---------------------------------------------------------------- KVKK / PRIVACY NOTICE
# DRAFT awaiting legal review: placeholders in [brackets] must be filled in before this page is indexed.
# Until then the page is built with <meta name="robots" content="noindex,follow"> and kept out of the sitemap.
# Sections: (h2, paragraphs, bullets).
CONTENT["tr"]["kvkk"] = {
    "title": "KVKK Aydınlatma Metni ve Gizlilik Politikası",
    "desc": "BİGEL'in bigel360.com teklif ve pilot formlarında topladığı kişisel verileri nasıl işlediğini ve KVKK kapsamındaki haklarınızı açıklayan aydınlatma metni.",
    "crumb": "KVKK ve Gizlilik",
    "eyebrow": "KVKK ve Gizlilik",
    "h1": "KVKK Aydınlatma Metni ve Gizlilik Politikası",
    "consent_link": "KVKK Aydınlatma Metni",
    "sections": [
        ("Bu metnin kapsamı", ["Bu metin, 6698 sayılı Kişisel Verilerin Korunması Kanunu (\"KVKK\") uyarınca, bigel360.com internet sitesini ziyaret eden ve site üzerindeki teklif ya da pilot başvuru formlarını dolduran kişilerin kişisel verilerinin nasıl işlendiğini açıklar.",
                               "BİGEL'in müşterileriyle yaptığı sözleşmeler kapsamında sahada yürütülen hizmetlerde işlenen veriler bu metnin konusu değildir. Bu veriler ilgili sözleşme ve ayrı aydınlatma metinleriyle yönetilir."], []),
        ("Veri sorumlusu", ["Kişisel verileriniz, veri sorumlusu sıfatıyla [ŞİRKET UNVANI] (\"BİGEL\") tarafından işlenir."],
         ["Unvan: [ŞİRKET UNVANI]", "Adres: [ADRES — sitede yer alan merkez adresi: Bağlarbaşı Mah. İncilik Sok. No:1 B Blok D:2, Maltepe / İstanbul; resmi kayıtlı adresle teyit edilecek]",
          "MERSİS No: [MERSİS NO]", "Vergi Dairesi / No: [VERGİ DAİRESİ / NO]", "KEP adresi: [KEP ADRESİ]", "E-posta: info@bigel360.com", "Telefon: +90 532 293 22 33"]),
        ("Hangi kişisel verileri işliyoruz?", ["Site üzerinden yalnızca formlara kendi girdiğiniz bilgiler toplanır. Formlarda zorunlu olmayan alanları boş bırakabilirsiniz."],
         ["Kimlik ve iletişim bilgileri: ad soyad, e-posta adresi, telefon numarası", "Kurumsal bilgiler: çalıştığınız şirket",
          "Talep bilgileri: lokasyon sayısı, ilgilendiğiniz çözüm veya başlangıç ürünü, sektör, şehir/bölge dağılımı, hedef başlangıç zamanı ve mesaj ya da not alanına yazdığınız açıklamalar",
          "İşlem bilgileri: formun türü (teklif veya pilot), formun gönderildiği dil ve gönderim zamanı",
          "Teknik veriler: siteye ve form sunucusuna eriştiğinizde, hizmet sağlayıcıların sunucu kayıtlarında otomatik olarak oluşan IP adresi, tarayıcı bilgisi ve erişim zamanı gibi bağlantı verileri"]),
        ("Kişisel verilerinizi hangi amaçlarla işliyoruz?", [],
         ["Teklif ve pilot taleplerinizi almak, değerlendirmek ve size geri dönüş yapmak", "Kapsam toplantısı planlamak, pilot kapsamını ve teklifi hazırlamak",
          "Talebinizle ilgili sizinle telefon veya e-posta yoluyla iletişim kurmak", "Sözleşme öncesi görüşmeleri yürütmek ve talep kayıtlarını yönetmek",
          "Formların kötüye kullanımını ve otomatik (spam) gönderimleri engellemek, site ve bilgi güvenliğini sağlamak", "Yasal yükümlülüklerimizi yerine getirmek ve yetkili kurumların talep etmesi halinde bilgi vermek"]),
        ("Hukuki sebepler ve toplama yöntemi", ["Kişisel verileriniz, bigel360.com üzerindeki formlar aracılığıyla elektronik ortamda ve sizin tarafınızdan doğrudan sağlanarak toplanır. Teknik bağlantı verileri ise siteye erişim sırasında otomatik yollarla oluşur.",
                                               "Bu veriler KVKK'nın 5. maddesinin 2. fıkrasında yer alan şu hukuki sebeplere dayanılarak işlenir:"],
         ["Bir sözleşmenin kurulması veya ifasıyla doğrudan ilgili olması kaydıyla, sözleşmenin taraflarına ait kişisel verilerin işlenmesinin gerekli olması (md. 5/2-c)",
          "Veri sorumlusunun hukuki yükümlülüğünü yerine getirebilmesi için zorunlu olması (md. 5/2-ç)",
          "İlgili kişinin temel hak ve özgürlüklerine zarar vermemek kaydıyla, veri sorumlusunun meşru menfaatleri için veri işlenmesinin zorunlu olması (md. 5/2-f)",
          "Yurt dışına aktarım bakımından: [HUKUKİ İNCELEME — KVKK md. 9 kapsamında uygulanacak aktarım mekanizması belirlenecek]"]),
        ("Kişisel verileriniz kimlere aktarılır?", ["Kişisel verileriniz satılmaz ve pazarlama amacıyla üçüncü kişilerle paylaşılmaz. Yukarıdaki amaçlarla sınırlı olarak şu alıcı gruplarına aktarılabilir:"],
         ["Form verilerinin saklandığı BİGEL yönetim panelinin barındırma, veritabanı ve altyapı hizmetlerini sağlayan yurt içi ve/veya yurt dışı sunucu hizmet sağlayıcıları [HUKUKİ İNCELEME — sağlayıcıların adları ve sunucu konumları teyit edilecek]",
          "bigel360.com sitesinin barındırma hizmetini sağlayan hizmet sağlayıcı [HUKUKİ İNCELEME]", "Talebinizin değerlendirilmesi için gerekli olduğu ölçüde BİGEL'in yetkili çalışanları",
          "Yasal olarak yetkili kamu kurum ve kuruluşları ile adli makamlar, mevzuatın gerektirdiği hallerde"]),
        ("Yurt dışına aktarım", ["Site ve yönetim paneli, altyapısı yurt dışında bulunabilen bulut hizmet sağlayıcıları üzerinde çalışmaktadır. Bu nedenle form aracılığıyla ilettiğiniz veriler yurt dışındaki sunucularda saklanabilir veya işlenebilir.",
                                 "Ayrıca site, yazı tiplerini Google Fonts hizmetinden yükler. Bu sırada tarayıcınız Google sunucularına bağlanır ve IP adresiniz ile tarayıcı bilgileriniz Google'a iletilebilir.",
                                 "[HUKUKİ İNCELEME — Yurt dışı aktarımın KVKK md. 9 (2024 değişikliği sonrası) kapsamındaki dayanağı (yeterlilik kararı, standart sözleşme ve Kurum'a bildirim, açık rıza vb.) belirlenene kadar bu bölüm yayımlanmamalıdır.]"], []),
        ("Çerezler ve analiz araçları", ["bigel360.com, ziyaretçi davranışlarını izlemeye yönelik analiz, reklam veya yeniden pazarlama araçları kullanmaz ve kendi çerezini yerleştirmez.",
                                         "Yukarıda belirtilen Google Fonts bağlantısı ile sitenin ve form sunucusunun barındırma hizmet sağlayıcılarının teknik bağlantı kayıtları bunun dışındadır. Sitede LinkedIn sayfamıza bağlantı bulunur. Bu bağlantıya tıkladığınızda LinkedIn'in kendi gizlilik politikası geçerli olur.",
                                         "Sitede analiz veya çerez kullanan bir araç devreye alınırsa bu metin güncellenir ve gerekli durumlarda onayınız alınır."], []),
        ("Saklama süresi", ["Kişisel verileriniz, işlendikleri amacın gerektirdiği süre ve ilgili mevzuatta öngörülen süreler boyunca saklanır. Bu süreler sona erdiğinde veriler silinir, yok edilir veya anonim hale getirilir.",
                            "Sözleşmeye dönüşmeyen teklif ve pilot talepleri, talebin kapanmasından itibaren en fazla [SAKLAMA SÜRESİ] süreyle saklanır. Sözleşmeye dönüşen taleplerde veriler, sözleşme ilişkisi ve yasal saklama yükümlülükleri süresince muhafaza edilir."], []),
        ("Veri güvenliği", ["BİGEL, kişisel verilerin hukuka aykırı olarak işlenmesini ve bunlara erişilmesini önlemek, verilerin korunmasını sağlamak için uygun düzeyde güvenlik sağlamaya yönelik idari ve teknik tedbirleri alır. Form verilerine panel üzerinde yalnızca yetkili kullanıcılar erişebilir ve veriler şifreli bağlantı (HTTPS) üzerinden iletilir."], []),
        ("KVKK kapsamındaki haklarınız", ["KVKK'nın 11. maddesi uyarınca, BİGEL'e başvurarak:"],
         ["Kişisel verilerinizin işlenip işlenmediğini öğrenme", "İşlenmişse buna ilişkin bilgi talep etme", "İşlenme amacını ve bunların amacına uygun kullanılıp kullanılmadığını öğrenme",
          "Yurt içinde veya yurt dışında aktarıldığı üçüncü kişileri bilme", "Eksik veya yanlış işlenmişse düzeltilmesini isteme", "KVKK'nın 7. maddesindeki şartlar çerçevesinde silinmesini veya yok edilmesini isteme",
          "Düzeltme, silme ve yok etme işlemlerinin, verilerin aktarıldığı üçüncü kişilere bildirilmesini isteme",
          "İşlenen verilerin münhasıran otomatik sistemler vasıtasıyla analiz edilmesi suretiyle aleyhinize bir sonucun ortaya çıkmasına itiraz etme",
          "Kanuna aykırı işleme sebebiyle zarara uğramanız halinde zararın giderilmesini talep etme haklarına sahipsiniz."]),
        ("Başvuru yöntemi", ["Haklarınıza ilişkin taleplerinizi, kimliğinizi tespit edici bilgilerle birlikte aşağıdaki yollardan biriyle iletebilirsiniz:"],
         ["Islak imzalı dilekçeyle şahsen veya noter aracılığıyla: [ADRES]", "Kayıtlı elektronik posta (KEP) ile: [KEP ADRESİ]",
          "Daha önce BİGEL'e bildirdiğiniz ve sistemlerimizde kayıtlı e-posta adresinizden: info@bigel360.com"]),
        ("", ["Başvurunuz, talebin niteliğine göre en kısa sürede ve en geç otuz gün içinde ücretsiz olarak sonuçlandırılır. İşlemin ayrıca bir maliyet gerektirmesi halinde Kişisel Verileri Koruma Kurulu'nca belirlenen tarifedeki ücret alınabilir."], []),
        ("Güncellemeler", ["Bu metin, mevzuattaki ya da sitedeki veri işleme faaliyetlerindeki değişikliklere göre güncellenebilir. Güncel metin her zaman bu sayfada yayımlanır.", "Son güncelleme: [TARİH]"], []),
    ],
}
CONTENT["en"]["kvkk"] = {
    "title": "Privacy Notice and Personal Data Protection",
    "desc": "How BİGEL processes personal data from quote and pilot requests on bigel360.com, who receives it, how long it is kept and your rights under KVKK.",
    "crumb": "Privacy",
    "eyebrow": "Privacy",
    "h1": "Privacy Notice and Personal Data Protection",
    "consent_link": "Privacy Notice",
    "sections": [
        ("Scope of this notice", ["This notice explains, under Turkish Personal Data Protection Law No. 6698 (\"KVKK\"), how we process the personal data of people who visit bigel360.com and submit the quote or pilot request forms on the site.",
                                  "Data processed during field services that BİGEL provides under customer contracts is outside the scope of this notice. That data is governed by the relevant contracts and separate notices.",
                                  "The Turkish version of this notice prevails. [LEGAL REVIEW — confirm]"], []),
        ("Data controller", ["Your personal data is processed by [COMPANY LEGAL NAME] (\"BİGEL\") as the data controller."],
         ["Legal name: [COMPANY LEGAL NAME]", "Address: [ADDRESS — office address shown on the site: Bağlarbaşı Mah. İncilik Sok. No:1 Block B Apt. 2, Maltepe / Istanbul, Türkiye; to be confirmed against the registered address]",
          "MERSIS No: [MERSIS NO]", "Tax office / No: [TAX OFFICE / NO]", "Registered e-mail (KEP): [KEP ADDRESS]", "Email: info@bigel360.com", "Phone: +90 532 293 22 33"]),
        ("What personal data we process", ["The site collects only the information you enter in the forms yourself. You may leave optional fields blank."],
         ["Identity and contact details: full name, email address, phone number", "Company details: the company you work for",
          "Request details: number of sites, solution or starting product of interest, sector, city/region distribution, target start date, and anything you write in the message or notes field",
          "Transaction details: form type (quote or pilot), the language of the form and the time of submission",
          "Technical data: connection data such as IP address, browser information and access time that is automatically recorded in our service providers' server logs when you access the site and the form server"]),
        ("Why we process your personal data", [],
         ["To receive and assess your quote and pilot requests and respond to you", "To schedule a scoping meeting and prepare the pilot scope and proposal", "To contact you by phone or email about your request",
          "To conduct pre-contract discussions and manage request records", "To prevent misuse of the forms and automated (spam) submissions, and keep the site and our information secure",
          "To meet our legal obligations and respond to authorised public bodies when required"]),
        ("Legal grounds and method of collection", ["Your personal data is collected electronically, directly from you, through the forms on bigel360.com. Technical connection data is generated automatically when you access the site.",
                                                    "We process this data on the following legal grounds under Article 5(2) of the KVKK:"],
         ["Processing is necessary for entering into or performing a contract, where the data belongs to the parties to that contract (Art. 5(2)(c))",
          "Processing is necessary for BİGEL to comply with a legal obligation (Art. 5(2)(ç))", "Processing is necessary for BİGEL's legitimate interests, provided it does not harm your fundamental rights and freedoms (Art. 5(2)(f))",
          "For transfers abroad: [LEGAL REVIEW — transfer mechanism under KVKK Art. 9 to be determined]"]),
        ("Who we share your data with", ["We do not sell your personal data or share it with third parties for marketing. It may be shared with the following groups only for the purposes above:"],
         ["Domestic and/or foreign server providers that supply hosting, database and infrastructure services for BİGEL's management panel, where form submissions are stored [LEGAL REVIEW — provider names and server locations to be confirmed]",
          "The hosting provider of the bigel360.com website [LEGAL REVIEW]", "BİGEL's authorised employees, to the extent needed to assess your request", "Authorised public bodies and judicial authorities where the law requires"]),
        ("Transfers abroad", ["The site and the management panel run on cloud service providers whose infrastructure may be located outside Türkiye. Data you submit through the forms may therefore be stored or processed on servers abroad.",
                              "The site also loads its fonts from Google Fonts. When it does, your browser connects to Google's servers, and your IP address and browser information may be sent to Google.",
                              "[LEGAL REVIEW — do not publish this section until the legal basis for transfers abroad under KVKK Art. 9 (as amended in 2024) is settled: adequacy decision, standard contract with notification to the Authority, explicit consent, etc.]"], []),
        ("Cookies and analytics", ["bigel360.com does not use analytics, advertising or retargeting tools that track visitor behaviour, and it does not set cookies of its own.",
                                   "The Google Fonts connection described above and the technical connection logs of the site's and form server's hosting providers are outside this. The site links to our LinkedIn page. If you follow that link, LinkedIn's own privacy policy applies.",
                                   "If we add a tool that uses analytics or cookies, we will update this notice and ask for your consent where required."], []),
        ("How long we keep your data", ["We keep your personal data for as long as the purpose of processing requires and for the periods set by applicable law. When these periods end, the data is deleted, destroyed or anonymised.",
                                        "Quote and pilot requests that do not lead to a contract are kept for no longer than [RETENTION PERIOD] after the request is closed. Where a request leads to a contract, the data is kept for the duration of the contractual relationship and any statutory retention period."], []),
        ("Data security", ["BİGEL takes appropriate administrative and technical measures to prevent unlawful processing of and access to personal data and to keep it secure. Only authorised users can access form submissions in the panel, and data is sent over an encrypted (HTTPS) connection."], []),
        ("Your rights under the KVKK", ["Under Article 11 of the KVKK, you may apply to BİGEL to:"],
         ["Find out whether your personal data is being processed", "Request information about the processing if it is", "Find out the purpose of the processing and whether the data is used for that purpose",
          "Know the third parties in Türkiye or abroad to whom your data has been transferred", "Ask for incomplete or inaccurate data to be corrected", "Ask for your data to be erased or destroyed under the conditions of Article 7 of the KVKK",
          "Ask for third parties who received your data to be notified of any correction, erasure or destruction", "Object to an outcome against you that results solely from automated analysis of your data",
          "Claim compensation for damage caused by unlawful processing"]),
        ("How to apply", ["You can send requests about your rights, with information that identifies you, by any of the following means:"],
         ["In person or through a notary, with a signed written application: [ADDRESS]", "By registered electronic mail (KEP): [KEP ADDRESS]",
          "From an email address you have previously given BİGEL and that is recorded in our systems: info@bigel360.com"]),
        ("", ["We will respond free of charge as soon as possible and within thirty days at the latest, depending on the nature of the request. If the process involves an additional cost, a fee may be charged in line with the tariff set by the Personal Data Protection Board."], []),
        ("Updates", ["We may update this notice to reflect changes in the law or in how the site processes data. The current version is always published on this page.", "Last updated: [DATE]"], []),
    ],
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
                f'{img(lang, "logo/"+p+".png", logo_alt(lang, d["name"]))}'
                f'<span class="kicker">{esc(tr_upper(d["cat"], lang))}</span><h3>{esc(d["tag"])}</h3><p>{esc(d["short"])}</p>'
                f'<span class="more">{esc(L["more"])} →</span></a>')
    return f'<div class="grid g4">{out}</div>'

def sector_cards(lang, n=None):
    L = CONTENT[lang]
    items = L["sectors_list"][:n] if n else L["sectors_list"]
    out = ""
    for i, ((title, desc), ic) in enumerate(zip(items, SECTOR_ICONS)):
        if i in SECTOR_LINKS:
            main = SECTOR_LINKS[i][0]
            more = " · ".join(f'<a href="{href(lang,x)}">{esc(L["ui"]["short"][x])}</a>' for x in SECTOR_LINKS[i])
            out += f'<div class="sector">{icon(ic)}<div><h3><a href="{href(lang,main)}">{esc(title)}</a></h3><p>{esc(desc)}</p><p class="sector-links">{more}</p></div></div>'
        else:
            out += f'<div class="sector">{icon(ic)}<div><h3>{esc(title)}</h3><p>{esc(desc)}</p></div></div>'
    return f'<div class="sectors">{out}</div>'

def tier_cards(lang, compact=False):
    L = CONTENT[lang]
    imgs = ["tier-basic.jpg", "tier-pro.jpg", "tier-business.jpg", "tier-360.jpg"]
    out = ""
    for i, (name, sub, one, who, feats) in enumerate(L["tiers_list"]):
        feat = "" if compact else "<ul>" + "".join(f"<li>{esc(f)}</li>" for f in feats) + "</ul>"
        cta = "" if compact else f'<a class="btn btn-outline btn-sm" href="{href(lang,"contact","form")}">{esc(L["tiers"]["cta"])}</a>'
        featured = ' featured' if (i == 3 and not compact) else ""
        out += (f'<div class="card tier{featured}" data-badge="{esc(L["tiers"]["badge"])}">{img(lang, "logo/"+imgs[i], logo_alt(lang, name))}'
                f'<span class="name">{esc(name)}</span><h3>{esc(sub)}</h3><p class="who">{esc(one if compact else who)}</p>{feat}{cta}</div>')
    return f'<div class="tiers">{out}</div>'

def flow(steps):
    return f'<div class="flow{" f4" if len(steps) == 4 else ""}">' + "".join(f'<div class="step"><b>{i+1:02d}</b><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for i, (t, d) in enumerate(steps)) + "</div>"

def cta_band(lang, L=None):
    L = L or CONTENT[lang]["cta"]
    return sec(f'<div class="cta-band"><div><h2>{esc(L["h2"])}</h2><p>{esc(L["p"])}</p></div><div class="btn-row"><a class="btn btn-primary" href="{href(lang,"pilot","basvuru" if lang == "tr" else "apply")}">{esc(L["b1"])}</a><a class="btn btn-ghost" href="{href(lang,"contact","form")}">{esc(L["b2"])}</a></div></div>')

def landing_link(lang, pid):
    """A text link to a sector landing page, named after it (used on product pages)."""
    return f'<a class="link" href="{href(lang,pid)}">{esc(CONTENT[lang]["landings"][pid]["crumb"])} →</a>'

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
    logo = img(lang, "logo/"+s["logo"], logo_alt(lang, "AUDIT 100")) if s["logo"] else f'<div class="score" style="color:{accent};font-size:40px">EV Audit30</div>'
    w = "".join(f'<div class="w"><b>%{v}</b><div>{esc(n)}<i style="--w:{v*100//25}%"></i></div></div>' for n, v in s["weights"])
    th = "".join(f'<span class="{c}">{esc(t)}</span>' for c, t in s["thresholds"])
    b = "".join(f'<span class="badge">{esc(x)}</span>' for x in s["badges"])
    more = f'<p style="margin-top:18px">{landing_link(lang, s["more"])}</p>' if s.get("more") else ""
    return sec(f'<div class="sub-product" id="{s["id"]}" style="--accent:{accent}"><div>{logo}<span class="eyebrow" style="color:{accent};margin-top:16px">{esc(s["eyebrow"])}</span><h2 style="font-size:clamp(26px,3vw,36px)">{esc(s["h2"])}</h2><p class="muted">{esc(s["p"])}</p><div class="badge-row">{b}</div>{more}</div><div><div class="weights">{w}</div><div class="thresholds">{th}</div></div></div>', "alt" if s["id"] == "audit100" else "")

def render_product_section(lang, s, accent):
    t = s["type"]
    if t == "split":
        img_ = f'<div class="photo">{img(lang, "img/"+s["img"], "")}<span class="tag">{esc(s["tag"])}</span></div>'
        note = f'<p class="note" style="margin-top:18px">{esc(s["note"])}</p>' if s.get("note") else ""
        more = f'<p style="margin-top:18px">{landing_link(lang, s["link"])}</p>' if s.get("link") else ""
        txt = f'<div>{head(s["eyebrow"], s["h2"])}<p class="lead">{esc(s["p"])}</p>{ul(s["list"], accent)}{note}{more}</div>'
        inner = (img_ + txt) if s.get("reverse") else (txt + img_)
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
        items = "".join(f'<div class="card"><h3>{esc(it[0])}</h3><p>{esc(it[1])}</p>{f"<p style={chr(34)}margin-top:12px{chr(34)}>{landing_link(lang, it[2])}</p>" if len(it) > 2 else ""}</div>' for it in s["items"])
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
# Lock icon for the portal button (Operasyon Merkezi and customers sign in to the BİGEL software).
LOCK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>'

def page_name(lang, pid):
    """Short page name for breadcrumbs."""
    L = CONTENT[lang]
    if pid in PRODUCTS: return L["products"][pid]["name"]
    if pid in LANDINGS: return L["landings"][pid]["crumb"]
    if pid in GUIDES: return L["guides"][pid]["crumb"]
    if pid == "guides": return L["ui"]["guides"]
    if pid == "kvkk": return L["kvkk"]["crumb"]
    if pid == "contact": return L["footer"]["contact"]
    return L["nav"][pid]

def page_url(lang, pid):
    return (f'https://{SITE["domain"]}/{PAGES[pid][0]}' if lang == "tr" else f'https://{SITE["domain"]}/en/{PAGES[pid][1]}').replace("/index.html", "/")

def layout(lang, pid, title, desc, body, active=None, crumbs=None, ld_nodes=None, robots=None, og_type="website", og_extra=""):
    """crumbs: page ids after Home for the BreadcrumbList (default: just this page; none on home).
    ld_nodes: extra JSON-LD nodes (Service, FAQPage, Article). robots: e.g. "noindex,follow".
    og_type / og_extra: Open Graph type and extra meta tags (e.g. article:published_time on guides)."""
    L = CONTENT[lang]; N = L["nav"]; F = L["footer"]
    portal_btn = f'<a class="btn btn-outline btn-sm btn-portal" href="{SITE["portal_url"] or href(lang,"portal")}">{LOCK}{esc(N["portal"])}</a>' if SHOW_PORTAL else ""
    sub = "".join(f'<li><a href="{href(lang,p)}" style="--accent:{ACCENT[p]}"><span class="dot"></span><span>{esc(L["products"][p]["name"])}<small>{esc(L["products"][p]["cat"])}</small></span></a></li>' for p in PRODUCTS)
    def a(p, label): return f'<li><a href="{href(lang,p)}"{" class=active" if active == p else ""}>{esc(label)}</a></li>'
    nav = (f'<li class="has-sub"><a href="{href(lang,"home","cozumler" if lang=="tr" else "solutions")}"{" class=active" if active in PRODUCTS else ""}>{esc(N["solutions"])}</a><ul class="sub">{sub}</ul></li>'
           + a("sectors", N["sectors"]) + a("tiers", N["tiers"]) + a("how", N["how"]) + a("about", N["about"])
           + (f'<li class="menu-cta"><a class="btn btn-outline btn-portal" href="{SITE["portal_url"] or href(lang,"portal")}">{LOCK}{esc(N["portal"])}</a></li>' if SHOW_PORTAL else "")
           + f'<li class="menu-cta"><a class="btn btn-primary" href="{href(lang,"contact","form")}">{esc(N["cta"])}</a></li>')
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
    base = f'https://{SITE["domain"]}'
    # Search appearance: the site name Google shows ("BİGEL", not the bare domain) and the company card,
    # on the home pages, where Google reads them.
    import json
    ld = ""
    graph = [org_ld(lang)]
    if pid == "home":
        graph.append({"@type": "WebSite", "@id": base + "/#website", "name": "BİGEL", "alternateName": ["BİGEL360", "BİGEL 360", "bigel360.com"], "url": base + "/", "inLanguage": ["tr", "en"], "publisher": {"@id": base + "/#organization"}})
    if pid not in ("home", "thanks", "portal", "notfound"):
        trail = [("home", L["ui"]["home"])] + [(c, page_name(lang, c)) for c in (crumbs or [pid])]
        graph.append({"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": page_url(lang, c)} for i, (c, n) in enumerate(trail)]})
    graph += ld_nodes or []
    if graph:
        ld = '\n<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False) + "</script>"
    hero_preload = (f'\n<link rel="preload" as="image" href="{asset(lang, "img/hero.webp")}" type="image/webp" media="(min-width:841px)" fetchpriority="high">'
                    f'\n<link rel="preload" as="image" href="{asset(lang, "img/hero-800.webp")}" type="image/webp" media="(max-width:840px)" fetchpriority="high">'
                    if pid == "home" and os.path.exists(os.path.join(ROOT, "assets", "img", "hero-800.webp")) else "")
    footer = (f'<footer class="footer"><div class="container"><div class="footer-grid"><div>{img(lang, "logo/bigel-white.png", logo_alt(lang, "BİGEL"))}<p><strong style="display:inline;text-transform:none;letter-spacing:0;font-size:15px">{esc(F["tagline"])}</strong></p><p>{esc(F["desc"])}</p></div>'
              f'<nav aria-label="{esc(F["solutions"])}"><strong>{esc(F["solutions"])}</strong>' + "".join(f'<a href="{href(lang,p)}">{esc(L["products"][p]["name"])}</a>' for p in PRODUCTS) + f'<a href="{href(lang,"ev_audit")}">{esc(F["ev"])}</a></nav>'
              f'<nav aria-label="{esc(N["sectors"])}"><strong>{esc(N["sectors"])}</strong>' + "".join(f'<a href="{href(lang,x)}">{esc(L["ui"]["footer"][x])}</a>' for x in LANDINGS) + f'<a href="{href(lang,"sectors")}">{esc(L["home"]["sec_more"])}</a></nav>'
              f'<nav aria-label="{esc(F["company"])}"><strong>{esc(F["company"])}</strong><a href="{href(lang,"about")}">{esc(N["about"])}</a><a href="{href(lang,"how")}">{esc(N["how"])}</a><a href="{href(lang,"sectors")}">{esc(N["sectors"])}</a><a href="{href(lang,"tiers")}">{esc(N["tiers"])}</a><a href="{href(lang,"guides")}">{esc(L["ui"]["guides"])}</a><a href="{href(lang,"pilot")}">{esc(N["pilot"])}</a></nav>'
              f'<div><strong>{esc(F["contact"])}</strong><address>{esc(SITE["address_tr"])}</address><a href="mailto:{SITE["email"]}">{SITE["email"]}</a><a href="tel:{SITE["phone_href"]}">{SITE["phone"]}</a><a href="{SITE["linkedin"]}" target="_blank" rel="noopener">LinkedIn</a><a href="{href(lang,"contact","form")}">{esc(N["cta"])}</a></div></div>'
              f'<div class="bottom"><span>© {year} BİGEL · {SITE["domain"]} · {esc(F["rights"])}</span><span><a href="{href(lang,"kvkk")}">{esc(F["privacy"])}</a></span></div></div></footer>')
    main_id = "icerik" if lang == "tr" else "content"
    out = f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">{f"{chr(10)}<meta name={chr(34)}robots{chr(34)} content={chr(34)}{robots}{chr(34)}>" if robots else ""}
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="tr" href="{tr_url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="x-default" href="{tr_url}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="{og_type}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="BİGEL">
<meta property="og:locale" content="{"tr_TR" if lang == "tr" else "en_US"}">
<meta property="og:locale:alternate" content="{"en_US" if lang == "tr" else "tr_TR"}">
<meta property="og:image" content="{base}/assets/icons/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="BİGEL — {esc(F["tagline"])}">{og_extra}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{base}/assets/icons/og-image.jpg">
<meta name="theme-color" content="#102A43">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="96x96" href="/assets/icons/icon-96.png">
<link rel="icon" type="image/png" sizes="192x192" href="/assets/icons/icon-192.png">
<link rel="apple-touch-icon" href="/assets/icons/apple-touch-icon.png">{ld}{hero_preload}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;display=swap">
<link rel="stylesheet" href="{versioned(lang,"styles.css")}">
</head>
<body>
<a class="skip" href="#{main_id}">{"İçeriğe atla" if lang == "tr" else "Skip to content"}</a>
<header class="header"><div class="container nav">
<a class="brand" href="{href(lang,"home")}">{img(lang, "logo/bigel.png", "BİGEL — " + F["tagline"], lazy=False, priority=True)}</a>
<nav class="nav-main" aria-label="{"Ana menü" if lang == "tr" else "Main menu"}"><ul class="menu" id="menu">{nav}</ul></nav>
<div class="nav-actions">{lang_sw}{portal_btn}<a class="btn btn-primary btn-sm" href="{href(lang,"contact","form")}">{esc(N["cta"])}</a></div>
<button class="burger" aria-label="{esc(N["menu"])}" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
</div></header>
<main id="{main_id}">
{body}
</main>
{footer}
<script src="{versioned(lang,"site.js")}" defer></script>
</body>
</html>
'''
    return accent_text(out)

def accent_text(out):
    """Small coloured text uses the darker text variant of a brand colour (styles.css --*-text): every
    --accent also sets --accent-text, and inline text colours point to the -text token. Fills keep the brand colour."""
    import re
    out = re.sub(r'--accent:var\(--(clean|care|audit|field|teal)\)', r'\g<0>;--accent-text:var(--\1-text)', out)
    return re.sub(r'(?<![-\w])color:var\(--(clean|care|field|teal)\)', r'color:var(--\1-text)', out)

# ---------------------------------------------------------------- PAGES
def page_home(lang):
    L = CONTENT[lang]; H = L["home"]
    sub = "".join(f"<span><b>{esc(n)}</b>{esc(t)}</span>" for n, t in H["sub"])
    hero = (f'<section class="hero"><div class="container"><div><span class="eyebrow">{esc(H["eyebrow"])}</span><h1>{esc(H["h1"])}</h1><p class="lead">{esc(H["lead"])}</p>'
            f'<div class="btn-row"><a class="btn btn-primary" href="#{"cozumler" if lang=="tr" else "solutions"}">{esc(H["b1"])}</a><a class="btn btn-ghost" href="{href(lang,"contact","form")}">{esc(H["b2"])}</a></div>'
            f'</div></div></section>')
    stats = "".join(f'<div class="card stat"><div class="n">{esc(n)}</div><p>{esc(t)}</p></div>' for n, t in H["stats"])
    trust = sec(head(H["trust_eyebrow"], H["trust_h2"]) + f'<div class="grid g4">{stats}</div>')
    sol = sec(head(H["sol_eyebrow"], H["sol_h2"], H["sol_lead"]) + product_cards(lang), "alt", "cozumler" if lang == "tr" else "solutions")
    ba = "".join(f'<div class="card"><span class="date">{esc(d)}</span><h4>{esc(t)}</h4><p style="font-size:13px">{esc(s)}</p><span class="pill {c}" style="margin-top:10px">{esc(st)}</span></div>' for d, t, s, c, st in H["ba"])
    proof = sec(f'<div class="split"><div>{head(H["proof_eyebrow"], H["proof_h2"])}<p class="lead" style="color:#C9D8E6">{esc(H["proof_p"])}</p>{ul(H["proof_list"])}</div><div><div class="photo" style="margin-bottom:14px">{img(lang, "img/tablet.jpg", "")}<span class="tag">{esc(H["photo_tag"])}</span></div><div class="ba">{ba}</div></div></div>', "navy")
    fl = sec(head(H["flow_eyebrow"], H["flow_h2"]) + flow(H["flow"]) + f'<p style="margin-top:22px"><a class="link" href="{href(lang,"how")}">{esc(H["flow_more"])} →</a></p>')
    secs = sec(head(H["sec_eyebrow"], H["sec_h2"]) + sector_cards(lang, 8) + f'<p style="margin-top:22px"><a class="link" href="{href(lang,"sectors")}">{esc(H["sec_more"])} →</a></p>', "alt")
    tiers = sec(head(H["tier_eyebrow"], H["tier_h2"]) + tier_cards(lang, compact=True) + f'<p style="margin-top:22px"><a class="link" href="{href(lang,"tiers")}">{esc(H["tier_more"])} →</a></p>')
    return layout(lang, "home", H["title"], H["desc"], hero + trust + sol + proof + fl + secs + tiers + cta_band(lang), "home")

def page_product(lang, pid):
    L = CONTENT[lang]; P = L["product_pages"][pid]; d = L["products"][pid]; accent = ACCENT[pid]
    hero = (f'<section class="p-hero" style="--accent:{accent}"><div class="container"><div>{crumb_nav(lang, [("home", L["ui"]["home"]), (pid, d["name"])])}<span class="eyebrow">{esc(d["name"])} · {esc(d["cat"])}</span><h1>{esc(P["title"])}</h1><p class="slogan">{esc(d["tag"])}</p><p class="lead">{esc(P["lead"])}</p>'
            f'<div class="btn-row"><a class="btn btn-primary" href="{href(lang,"contact","form")}">{esc(L["nav"]["cta"])}</a><a class="btn btn-outline" href="{href(lang,"how")}">{esc(L["nav"]["how"])}</a></div></div>'
            f'{img(lang, "logo/"+pid+".png", logo_alt(lang, d["name"]), "logo", lazy=False, priority=True)}</div></section>')
    body = hero + "".join(render_product_section(lang, s, accent) for s in P["sections"]) + cta_band(lang)
    return layout(lang, pid, P["title"], P["desc"], body, pid, ld_nodes=[service_ld(lang, pid, d["name"], d["cat"], P["desc"])])

def service_ld(lang, pid, name, service_type, desc):
    base = f'https://{SITE["domain"]}'
    return {"@type": "Service", "name": name, "serviceType": service_type, "description": desc, "url": page_url(lang, pid),
            "provider": {"@id": base + "/#organization"},
            "areaServed": {"@type": "Country", "name": "Türkiye"}, "inLanguage": lang}

def faq_block(lang, items, accent):
    U = CONTENT[lang]["ui"]
    qa = "".join(f'<details class="faq-item"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in items)
    return sec(head(U["faq_eyebrow"], U["faq_h2"]) + f'<div class="faq" style="--accent:{accent}">{qa}</div>', "alt", "sss" if lang == "tr" else "faq")

def landing_section(lang, s, accent, alt):
    """One content block of a landing page: heading + optional cards, steps, score weights, list, note and links."""
    parts = []
    if s.get("cards"):
        parts.append('<div class="grid g3">' + "".join(f'<div class="card accent" style="--accent:{accent}"><h3>{esc(h)}</h3><p>{esc(d)}</p></div>' for h, d in s["cards"]) + "</div>")
    if s.get("steps"):
        parts.append(flow(s["steps"]))
    if s.get("weights"):
        # same score model as on audit.html
        src = next(x for x in CONTENT[lang]["product_pages"]["audit"]["sections"] if x.get("id") == s["weights"])
        w = "".join(f'<div class="w"><b>%{v}</b><div>{esc(n)}<i style="--w:{v*100//25}%"></i></div></div>' for n, v in src["weights"])
        th = "".join(f'<span class="{c}">{esc(t)}</span>' for c, t in src["thresholds"])
        parts.append(f'<div class="sub-product" style="--accent:{accent};grid-template-columns:1fr;max-width:820px"><div><div class="weights">{w}</div><div class="thresholds">{th}</div></div></div>')
    if s.get("list"):
        parts.append(f'<div style="margin-top:{"28px" if parts else "0"};max-width:820px">{ul(s["list"], accent)}</div>')
    if s.get("p"):
        parts.append(f'<p style="margin-top:22px;max-width:820px">{esc(s["p"])}</p>')
    if s.get("note"):
        parts.append(f'<p class="note" style="margin-top:22px">{esc(s["note"])}</p>')
    if s.get("links"):
        parts.append('<p class="link-row">' + "".join(f'<a class="link" href="{href(lang, p, a)}">{esc(t)} →</a>' for t, p, a in s["links"]) + "</p>")
    return sec(head(s["eyebrow"], s["h2"], s["lead"]) + "".join(parts), "alt" if alt else "")

def page_desc(lang, pid):
    """One-line description of a page for related-page cards."""
    L = CONTENT[lang]
    if pid in LANDINGS: return L["landings"][pid]["desc"]
    if pid in GUIDES: return L["guides"][pid]["desc"]
    return L["products"][pid]["short"]

def related_cards(lang, pids):
    U = CONTENT[lang]["ui"]
    rel = "".join(f'<a class="card accent" style="--accent:{ACCENT.get(r, "var(--teal)")};text-decoration:none;display:block" href="{href(lang,r)}"><h3>{esc(page_name(lang, r))} →</h3><p>{esc(page_desc(lang, r))}</p></a>' for r in pids)
    return sec(head(U["rel_eyebrow"], U["rel_h2"]) + f'<div class="grid g4">{rel}</div>')

def guide_cards(lang, gids, eyebrow=None, h2=None, cls="", lead=""):
    """Cards linking to guide articles ("İlgili rehberler" on landing pages)."""
    if not gids: return ""
    L = CONTENT[lang]; U = L["ui"]
    cards = "".join(f'<a class="card accent" style="--accent:var(--teal);text-decoration:none;display:block" href="{href(lang,g)}" aria-label="{html.escape(L["guides"][g]["h1"])}"><span class="kicker" style="font-size:12px;font-weight:800;letter-spacing:.1em;color:var(--teal)">{esc(tr_upper(U["guides"], lang))}</span><h3 style="margin-top:8px">{esc(L["guides"][g]["h1"])}</h3><p>{esc(L["guides"][g]["desc"])}</p></a>' for g in gids)
    return sec(head(eyebrow or U["guides_eyebrow"], h2 or U["guides_h2"], lead) + f'<div class="grid {"g3" if len(gids) >= 3 else "g2"}">{cards}</div>', cls)

def crumb_nav(lang, trail):
    """Visible breadcrumb trail: [(page id, name), ...]; the last item is the current page."""
    U = CONTENT[lang]["ui"]
    items = " <span aria-hidden=\"true\">/</span> ".join((f'<a href="{href(lang,c)}">{esc(n)}</a>' if i < len(trail) - 1 else f'<span aria-current="page">{esc(n)}</span>') for i, (c, n) in enumerate(trail))
    return f'<nav class="crumbs" aria-label="{esc(U["crumb_label"])}">{items}</nav>'

def page_guides(lang):
    """Guides index (rehber.html / en/guides.html)."""
    L = CONTENT[lang]; G = L["guides_index"]; U = L["ui"]
    hero = (f'<section class="p-hero"><div class="container" style="grid-template-columns:1fr"><div>{crumb_nav(lang, [("home", U["home"]), ("guides", U["guides"])])}'
            f'<span class="eyebrow">{esc(G["eyebrow"])}</span><h1>{esc(G["h1"])}</h1><p class="lead">{esc(G["lead"])}</p></div></div></section>')
    cards = "".join(f'<a class="card accent" style="--accent:var(--teal);text-decoration:none;display:block" href="{href(lang,g)}" aria-label="{html.escape(L["guides"][g]["h1"])}"><h2 style="font-size:22px;margin:0 0 10px">{esc(L["guides"][g]["h1"])}</h2><p>{esc(L["guides"][g]["desc"])}</p><span class="more" style="display:inline-block;margin-top:14px;font-weight:700;color:var(--teal)">{esc(G["read"])} →</span></a>' for g in GUIDES)
    item_list = {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": page_url(lang, g), "name": L["guides"][g]["h1"]} for i, g in enumerate(GUIDES)]}
    body = hero + sec(f'<div class="grid g2">{cards}</div>', "alt") + cta_band(lang)
    return layout(lang, "guides", G["title"] + L["meta_suffix"], G["desc"], body, ld_nodes=[item_list])

def page_guide(lang, gid):
    """Guide article: one readable column, FAQ, related pages, Article + BreadcrumbList + FAQPage JSON-LD."""
    L = CONTENT[lang]; P = L["guides"][gid]; U = L["ui"]; base = f'https://{SITE["domain"]}'
    date_txt = GUIDE_DATE[8:10] + "." + GUIDE_DATE[5:7] + "." + GUIDE_DATE[:4]
    hero = (f'<section class="p-hero"><div class="container" style="grid-template-columns:1fr"><div>{crumb_nav(lang, [("home", U["home"]), ("guides", U["guides"]), (gid, P["crumb"])])}'
            f'<span class="eyebrow">{esc(U["guides"])}</span><h1>{esc(P["h1"])}</h1><p class="lead">{esc(P["lead"])}</p>'
            f'<p class="article-meta">{esc(U["by"])} · {esc(U["published"])}: <time datetime="{GUIDE_DATE}">{date_txt}</time></p></div></div></section>')
    def links(ls):
        return ('<p class="link-row">' + "".join(f'<a class="link" href="{href(lang, p, a)}">{esc(t)} →</a>' for t, p, a in ls) + "</p>") if ls else ""
    def block(s):
        return (f'<h2>{esc(s["h2"])}</h2>' + "".join(f"<p>{esc(x)}</p>" for x in s.get("paragraphs", []))
                + (ul(s["list"]) if s.get("list") else "") + (f'<p>{esc(s["after"])}</p>' if s.get("after") else "") + links(s.get("links")))
    article = (f'<article class="article"><p>{esc(P["intro"])}</p>' + "".join(block(s) for s in P["sections"])
               + f'<div class="article-how">{block(P["how"])}</div></article>')
    body = hero + sec(article) + faq_block(lang, P["faq"], "var(--teal)") + related_cards(lang, GUIDE_RELATED[gid]) + cta_band(lang)
    org = {"@id": base + "/#organization"}
    article_ld = {"@type": "Article", "headline": P["h1"], "description": P["desc"], "inLanguage": lang, "datePublished": GUIDE_DATE, "dateModified": GUIDE_DATE,
                  "author": org, "publisher": org,
                  "image": base + "/assets/icons/og-image.jpg", "mainEntityOfPage": {"@type": "WebPage", "@id": page_url(lang, gid)}}
    faq_ld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in P["faq"]]}
    # One rule for every guide: title + " | BİGEL" (guide titles are written to fit 60 characters with it).
    title = P["title"] + L["meta_suffix"]
    assert len(title) <= 60, title
    og_extra = f'\n<meta property="article:published_time" content="{GUIDE_DATE}">\n<meta property="article:author" content="BİGEL">'
    return layout(lang, gid, title, P["desc"], body, crumbs=["guides", gid], ld_nodes=[article_ld, faq_ld], og_type="article", og_extra=og_extra)

def page_kvkk(lang):
    """KVKK / privacy notice. Draft with placeholders awaiting legal review, so it is noindex and out of the sitemap."""
    L = CONTENT[lang]; K = L["kvkk"]; U = L["ui"]
    hero = (f'<section class="p-hero"><div class="container" style="grid-template-columns:1fr"><div>{crumb_nav(lang, [("home", U["home"]), ("kvkk", K["crumb"])])}'
            f'<span class="eyebrow">{esc(K["eyebrow"])}</span><h1>{esc(K["h1"])}</h1></div></div></section>')
    parts = ""
    for h2, paras, bullets in K["sections"]:
        parts += (f'<h2>{esc(h2)}</h2>' if h2 else "") + "".join(f"<p>{esc(x)}</p>" for x in paras) + (ul(bullets) if bullets else "")
    body = hero + sec(f'<article class="article">{parts}</article>')
    return layout(lang, "kvkk", K["title"] + L["meta_suffix"], K["desc"], body, robots="noindex,follow")

def page_landing(lang, pid):
    """Sector landing page (fuel / EV charging stations), built from CONTENT[lang]["landings"][pid]."""
    L = CONTENT[lang]; P = L["landings"][pid]; U = L["ui"]; accent = ACCENT[pid]
    hero = (f'<section class="p-hero l-hero" style="--accent:{accent}"><div class="container"><div>{crumb_nav(lang, [("home", U["home"]), ("sectors", L["nav"]["sectors"]), (pid, P["crumb"])])}'
            f'<span class="eyebrow">{esc(P["eyebrow"])}</span><h1>{esc(P["h1"])}</h1><p class="lead">{esc(P["lead"])}</p>'
            f'<div class="btn-row"><a class="btn btn-primary" href="{href(lang,"pilot","basvuru" if lang == "tr" else "apply")}">{esc(P["b1"])}</a><a class="btn btn-outline" href="{href(lang,"contact","form")}">{esc(P["b2"])}</a></div></div>'
            f'<div class="l-icon">{icon(LANDING_ICON[pid])}</div></div></section>')
    sections = [dict(s) for s in P["sections"]]
    gid, anchor = LANDING_GUIDE_LINK[pid][0], LANDING_GUIDE_LINK[pid][1 if lang == "tr" else 2]
    k = next((i for i, s in enumerate(sections) if s.get("links")), 0)
    sections[k]["links"] = list(sections[k].get("links") or []) + [(anchor, gid, "")]
    secs = "".join(landing_section(lang, s, accent, i % 2 == 0) for i, s in enumerate(sections))
    related = related_cards(lang, LANDING_RELATED[pid])
    body = hero + secs + faq_block(lang, P["faq"], accent) + guide_cards(lang, LANDING_GUIDES.get(pid, [])) + related + cta_band(lang, P["cta"])
    faq_ld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in P["faq"]]}
    return layout(lang, pid, P["title"] + L["meta_suffix"], P["desc"], body, "sectors", crumbs=["sectors", pid],
                  ld_nodes=[service_ld(lang, pid, P["crumb"], P["service"], P["desc"]), faq_ld])

def simple_hero(eyebrow, h1, lead, crumbs=""):
    return f'<section class="p-hero"><div class="container" style="grid-template-columns:1fr"><div>{crumbs}<span class="eyebrow">{esc(eyebrow)}</span><h1>{esc(h1)}</h1><p class="lead">{esc(lead)}</p></div></div></section>'

def page_crumbs(lang, pid):
    """Visible Home / page breadcrumb, matching the page's BreadcrumbList."""
    return crumb_nav(lang, [("home", CONTENT[lang]["ui"]["home"]), (pid, page_name(lang, pid))])

def webpage_ld(lang, pid, type_, name):
    """Page-role node (AboutPage, ContactPage, CollectionPage) tied to the WebSite and the Organization."""
    base = f'https://{SITE["domain"]}'
    return {"@type": type_, "@id": page_url(lang, pid) + "#webpage", "url": page_url(lang, pid), "name": name, "inLanguage": lang,
            "isPartOf": {"@id": base + "/#website"}, "about": {"@id": base + "/#organization"}}

def page_sectors(lang):
    L = CONTENT[lang]; S = L["sectors"]
    fit = "".join(f'<a class="card accent" style="--accent:{ACCENT[p]};text-decoration:none;display:block" href="{href(lang,p)}"><p style="font-size:13px;font-weight:700;color:var(--muted);margin-bottom:6px">{esc(q)}</p><h3 style="color:{ACCENT[p]};margin:0">{esc(a)} →</h3></a>' for q, a, p in S["fit"])
    body = (simple_hero(S["eyebrow"], S["h1"], S["lead"], page_crumbs(lang, "sectors")) + sec(sector_cards(lang))
            + sec(f'<div class="split"><div>{head(S["fr_eyebrow"], S["fr_h2"])}<p class="lead">{esc(S["fr_p"])}</p>{ul(S["fr_list"])}</div><div class="photo">{img(lang, "img/exterior.jpg", "")}</div></div>', "alt")
            + sec(head(S["fit_eyebrow"], S["fit_h2"]) + f'<div class="grid g3">{fit}</div>') + cta_band(lang))
    return layout(lang, "sectors", S["title"] + L["meta_suffix"], S["desc"], body, "sectors", ld_nodes=[webpage_ld(lang, "sectors", "CollectionPage", S["h1"])])

def page_tiers(lang):
    L = CONTENT[lang]; T = L["tiers"]
    th = "".join(f'<th{" class=center" if i else ""}>{esc(h)}</th>' for i, h in enumerate(T["cmp_head"]))
    rows = "".join("<tr>" + f"<td>{esc(r[0])}</td>" + "".join(f'<td class="center">{"<span style=color:var(--teal);font-weight:800>✓</span>" if v else "<span style=color:#B7C7D6>—</span>"}</td>' for v in r[1:]) + "</tr>" for r in T["cmp_rows"])
    body = (simple_hero(T["eyebrow"], T["h1"], T["lead"], page_crumbs(lang, "tiers")) + sec(tier_cards(lang))
            + sec(head("", T["cmp_h2"]) + f'<div class="table-wrap"><table class="table"><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table></div><p class="note" style="margin-top:22px">{esc(T["note"])}</p>', "alt")
            + cta_band(lang))
    return layout(lang, "tiers", T["title"] + L["meta_suffix"], T["desc"], body, "tiers")

def page_how(lang):
    L = CONTENT[lang]; H = L["how"]
    steps = "".join(f'<div class="card"><span class="eyebrow">{i+1:02d}</span><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for i, (t, d) in enumerate(H["steps"]))
    tl = "".join(f'<div class="card"><span class="when">{esc(w)}</span><h3>{esc(t)}</h3><ul>' + "".join(f"<li>{esc(x)}</li>" for x in items) + "</ul></div>" for w, t, items in H["timeline"])
    scale = "".join(f'<div class="card"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t, d in H["scale"])
    body = (simple_hero(H["eyebrow"], H["h1"], H["lead"], page_crumbs(lang, "how"))
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
    body = (simple_hero(A["eyebrow"], A["h1"], A["lead"], page_crumbs(lang, "about"))
            + sec(f'<div class="split"><div><h2>{esc(A["story_h2"])}</h2>{story}</div><div class="photo">{img(lang, "img/exterior.jpg", "")}</div></div><div class="grid g4" style="margin-top:48px">{facts}</div>')
            + sec(head(A["v_eyebrow"], A["v_h2"]) + f'<div class="value-grid">{values}</div>', "alt")
            + sec(head(A["c_eyebrow"], A["c_h2"]) + f'<div class="grid g3">{ch}</div>')
            + sec(f'<div class="split"><div>{head(A["reg_eyebrow"], A["reg_h2"])}<p class="lead">{esc(A["reg_p"])}</p><div class="badge-row">{regs}</div></div><div class="photo">{img(lang, "img/station.jpg", "")}</div></div>', "alt")
            + cta_band(lang))
    return layout(lang, "about", A["title"] + L["meta_suffix"], A["desc"], body, "about", ld_nodes=[webpage_ld(lang, "about", "AboutPage", A["h1"])])

def page_contact(lang):
    L = CONTENT[lang]; C = L["contact"]; f = C["f"]
    next_url = f'https://{SITE["domain"]}/' + ("" if lang == "tr" else "en/") + PAGES["thanks"][0 if lang == "tr" else 1]
    counts = "".join(f"<option>{esc(c)}</option>" for c in f["counts"])
    sols = "".join(f"<option>{esc(c)}</option>" for c in f["solutions"])
    form = (f'<form class="form" action="{SITE["form_url"]}" method="POST">'
            f'<input type="hidden" name="_kind" value="teklif"><input type="hidden" name="_lang" value="{lang}"><input type="hidden" name="_next" value="{next_url}"><input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">'
            f'<div class="row"><div><label for="name">{esc(f["name"])}</label><input id="name" name="name" autocomplete="name" required></div><div><label for="company">{esc(f["company"])}</label><input id="company" name="company" autocomplete="organization" required></div></div>'
            f'<div class="row"><div><label for="email">{esc(f["email"])}</label><input id="email" type="email" name="email" autocomplete="email" required></div><div><label for="phone">{esc(f["phone"])}</label><input id="phone" type="tel" name="phone" autocomplete="tel"></div></div>'
            f'<div class="row"><div><label for="count">{esc(f["count"])}</label><select id="count" name="{f["count"]}">{counts}</select></div><div><label for="sol">{esc(f["solution"])}</label><select id="sol" name="{f["solution"]}">{sols}</select></div></div>'
            f'<label for="msg">{esc(f["msg"])}</label><textarea id="msg" name="message" placeholder="{esc(f["msg_ph"])}"></textarea>'
            f'<label class="consent"><input type="checkbox" required><span>{esc(f["consent"])} <a href="{href(lang,"kvkk")}" target="_blank" rel="noopener">{esc(L["kvkk"]["consent_link"])}</a></span></label>'
            f'<button class="btn btn-primary" type="submit">{esc(f["send"])}</button></form>')
    info = "".join(f'<div class="card"><b>{esc(t)}</b><p>{esc(v)}</p></div>' for t, v in C["info"])
    # id "form": every "Teklif Al" button opens the page right at the form (#form), past the title.
    body = simple_hero(C["eyebrow"], C["h1"], C["lead"], page_crumbs(lang, "contact")) + sec(f'<div class="split" style="align-items:start">{form}<div class="contact-info">{info}</div></div>', "alt", "form")
    return layout(lang, "contact", C["title"] + L["meta_suffix"], C["desc"], body, "contact", ld_nodes=[webpage_ld(lang, "contact", "ContactPage", C["h1"])])

def page_pilot(lang):
    L = CONTENT[lang]; P = L["pilot"]; f = P["f"]
    stats = "".join(f'<div class="card stat"><div class="n">{esc(n)}</div><p>{esc(t)}</p></div>' for n, t in P["stats"])
    why = "".join(f'<div class="card"><h3>{esc(h)}</h3><p>{esc(d)}</p></div>' for h, d in P["why"])
    steps = "".join(f'<div class="card"><span class="eyebrow">{i+1:02d}</span><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for i, (t, d) in enumerate(P["steps"]))
    prod = "".join(f'<a class="card accent" style="--accent:{ACCENT[pid]};text-decoration:none;display:block" href="{href(lang,pid)}"><span class="kicker" style="font-size:12px;font-weight:800;letter-spacing:.1em;color:{ACCENT[pid]}">{esc(L["products"][pid]["name"])}</span><h3 style="margin-top:8px">{esc(t)}</h3><p>{esc(d)}</p></a>' for pid, t, d in P["prod"])
    next_url = f'https://{SITE["domain"]}/' + ("" if lang == "tr" else "en/") + PAGES["thanks"][0 if lang == "tr" else 1]
    opt = lambda xs: "".join(f"<option>{esc(x)}</option>" for x in xs)
    form = (f'<form class="form" action="{SITE["form_url"]}" method="POST">'
            f'<input type="hidden" name="_kind" value="pilot"><input type="hidden" name="_lang" value="{lang}"><input type="hidden" name="_next" value="{next_url}"><input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">'
            f'<div class="row"><div><label for="name">{esc(f["name"])}</label><input id="name" name="name" autocomplete="name" required></div><div><label for="company">{esc(f["company"])}</label><input id="company" name="company" autocomplete="organization" required></div></div>'
            f'<div class="row"><div><label for="email">{esc(f["email"])}</label><input id="email" type="email" name="email" autocomplete="email" required></div><div><label for="phone">{esc(f["phone"])}</label><input id="phone" type="tel" name="phone" autocomplete="tel"></div></div>'
            f'<div class="row"><div><label for="sector">{esc(f["sector"])}</label><select id="sector" name="{f["sector"]}">{opt(f["sectors"])}</select></div><div><label for="count">{esc(f["count"])}</label><select id="count" name="{f["count"]}">{opt(f["counts"])}</select></div></div>'
            f'<label for="geo">{esc(f["geo"])}</label><input id="geo" name="{f["geo"]}" placeholder="{esc(f["geo_ph"])}">'
            f'<div class="row"><div><label for="product">{esc(f["product"])}</label><select id="product" name="{f["product"]}">{opt(f["products"])}</select></div><div><label for="start">{esc(f["start"])}</label><select id="start" name="{f["start"]}">{opt(f["starts"])}</select></div></div>'
            f'<label for="msg">{esc(f["msg"])}</label><textarea id="msg" name="message" placeholder="{esc(f["msg_ph"])}"></textarea>'
            f'<label class="consent"><input type="checkbox" required><span>{esc(f["consent"])} <a href="{href(lang,"kvkk")}" target="_blank" rel="noopener">{esc(L["kvkk"]["consent_link"])}</a></span></label>'
            f'<button class="btn btn-primary" type="submit">{esc(f["send"])}</button></form>')
    after = "".join(f'<div class="card" style="padding:18px 20px"><span class="eyebrow">{esc(n)}</span><h4 style="margin:2px 0 4px">{esc(t)}</h4><p style="font-size:14px">{esc(d)}</p></div>' for n, t, d in P["after"])
    body = simple_hero(P["form_eyebrow"], P["form_h2"], P["form_lead"], page_crumbs(lang, "pilot")) + sec(f'<div class="split" style="align-items:start">{form}<div class="contact-info"><h3 style="margin:0 0 4px">{esc(P["after_h3"])}</h3>{after}<p class="note">{esc(P["note"])}</p></div></div>', "alt", "basvuru" if lang == "tr" else "apply")
    return layout(lang, "pilot", P["title"] + L["meta_suffix"], P["desc"], body, "pilot")

def page_portal(lang):
    L = CONTENT[lang]; T = L["portal"]
    body = sec(f'<div class="center" style="padding:40px 0"><span class="eyebrow">BİGEL PORTAL</span><h1 style="font-size:clamp(32px,4vw,52px)">{esc(T["h1"])}</h1><p class="lead" style="margin-inline:auto">{esc(T["p"])}</p><div class="btn-row" style="justify-content:center"><a class="btn btn-primary" href="{href(lang,"contact","form")}">{esc(T["b1"])}</a><a class="btn btn-outline" href="{href(lang,"home")}">{esc(T["b2"])}</a></div></div>')
    # "Coming soon" stub; the header button goes to the panel, so the page is noindex and out of the sitemap.
    return layout(lang, "portal", T["title"] + L["meta_suffix"], T["desc"], body, robots="noindex,follow")

def page_thanks(lang):
    L = CONTENT[lang]; T = L["thanks"]
    check = '<svg viewBox="0 0 52 52" aria-hidden="true"><circle cx="26" cy="26" r="24"/><path d="M15 27l7 7 15-16"/></svg>'
    steps = "".join(f'<li class="{"done" if i == 0 else ""}"><span class="dot">{"✓" if i == 0 else i + 1}</span><div><b>{esc(t)}</b><p>{esc(d)}</p></div></li>' for i, (t, d) in enumerate(T["steps"]))
    body = (f'<section class="thanks"><div class="container"><div class="thanks-card">'
            f'<div class="thanks-check">{check}</div><span class="thanks-badge">{esc(T["badge"])}</span>'
            f'<h1>{esc(T["h1"])}</h1><p class="lead">{esc(T["p"])}</p>'
            f'<div class="thanks-steps"><span class="eyebrow">{esc(T["steps_h"])}</span><ol>{steps}</ol></div>'
            f'<div class="btn-row"><a class="btn btn-primary" href="{href(lang,"home")}">{esc(T["b"])}</a><a class="btn btn-outline" href="{href(lang,"how")}">{esc(T["b2"])}</a></div>'
            f'<p class="thanks-urgent">{esc(T["urgent"])} <a href="tel:{SITE["phone_href"]}">{esc(SITE["phone"])}</a> · <a href="mailto:{SITE["email"]}">{esc(SITE["email"])}</a></p>'
            f'</div></div></section>')
    return layout(lang, "thanks", T["title"] + L["meta_suffix"], T["p"], body, robots="noindex,follow")

def page_notfound():
    """/404.html: friendly message, a filterable list of the main pages, noindex. GitHub Pages serves it
    at the missing URL itself (e.g. /en/old/page), so every link and asset path is made root-absolute."""
    import re
    lang = "tr"; L = CONTENT[lang]; N = L["nav"]
    groups = [("Çözümler", [(p, page_name(lang, p)) for p in PRODUCTS]),
              ("Sektör sayfaları", [(p, page_name(lang, p)) for p in LANDINGS] + [("sectors", N["sectors"])]),
              ("Rehber", [("guides", L["ui"]["guides"])] + [(g, L["guides"][g]["h1"]) for g in GUIDES]),
              ("Şirket ve iletişim", [("about", N["about"]), ("how", N["how"]), ("tiers", N["tiers"]), ("contact", page_name(lang, "contact")),
                                       ("contact#form", N["cta"]), ("pilot", N["pilot"])])]
    def link(p, name):
        pid, _, anchor = p.partition("#")
        return f'<li data-k="{html.escape(name.lower())}"><a class="link" href="{href(lang, pid, anchor)}">{esc(name)} →</a></li>'
    cards = "".join(f'<div class="card nf-group"><h3>{esc(t)}</h3><ul class="nf-list">' + "".join(link(p, n) for p, n in items) + "</ul></div>" for t, items in groups)
    body = (simple_hero("404", "Aradığınız sayfa bulunamadı.", "Bağlantı eski olabilir ya da adres yanlış yazılmış olabilir. Aşağıdaki sayfalardan devam edebilir veya bize doğrudan ulaşabilirsiniz.")
            .replace('</p></div></div></section>', '</p><p lang="en" class="nf-en">Page not found. The link may be out of date or mistyped. <a class="link" href="/en/">Continue on the English site →</a></p>'
                     f'<div class="btn-row"><a class="btn btn-primary" href="{href(lang, "home")}">Ana sayfaya dön</a><a class="btn btn-outline" href="{href(lang, "contact", "form")}">{esc(N["cta"])}</a></div></div></div></section>')
            + sec('<label class="nf-search"><span>Sayfa ara</span><input type="search" id="nf-q" placeholder="Örn. şarj, kanopi, denetim, teklif" autocomplete="off"></label>'
                  f'<div class="grid g4 nf-grid">{cards}</div><p class="note nf-none" hidden>Eşleşen sayfa yok. <a class="link" href="{href(lang, "contact", "form")}">Bize yazın →</a></p>'
                  '<script>(function(){var q=document.getElementById("nf-q"),none=document.querySelector(".nf-none");q.addEventListener("input",function(){'
                  'var v=q.value.toLocaleLowerCase("tr").trim(),any=false;document.querySelectorAll(".nf-group").forEach(function(g){var n=0;'
                  'g.querySelectorAll("li").forEach(function(li){var m=!v||li.dataset.k.indexOf(v)>-1||li.textContent.toLocaleLowerCase("tr").indexOf(v)>-1;li.hidden=!m;if(m)n++;});'
                  'g.hidden=!n;if(n)any=true;});none.hidden=any;});})();</script>', "alt"))
    out = layout(lang, "notfound", "Sayfa bulunamadı (404) | BİGEL", "Aradığınız sayfa bulunamadı. BİGEL ana sayfaları, sektör sayfaları ve rehber yazıları.", body, robots="noindex,follow")
    # no canonical / hreflang / og:url for an error page
    out = re.sub(r'\n<link rel="(?:canonical|alternate)"[^>]*>|\n<meta property="og:url"[^>]*>', "", out)
    # root-absolute links and assets, since the page can be served at any depth
    out = re.sub(r'(href|src|srcset)="(?!https?:|/|#|mailto:|tel:)([^"]+)"', r'\1="/\2"', out)
    return out.replace('href="/en/index.html"', 'href="/en/"').replace('href="/index.html"', 'href="/"')

# ---------------------------------------------------------------- BUILD
def build():
    js = """document.querySelector('.burger').addEventListener('click',function(){var m=document.getElementById('menu');var o=m.classList.toggle('open');this.setAttribute('aria-expanded',o);});
document.querySelectorAll('.has-sub>a').forEach(function(a){a.addEventListener('click',function(e){if(window.innerWidth<=840){/* mobile: let the link work, submenu is already expanded */}});});
// A "Teklif Al" / "Pilot başla" link (#form, #basvuru, #apply) lands with the form centred on the
// screen under the header (or at the top when the form is taller than the screen).
(function () {
  var targets = { "#form": 1, "#basvuru": 1, "#apply": 1 };
  function centreForm(smooth) {
    if (!targets[location.hash]) return;
    var section = document.querySelector(location.hash);
    var form = section && section.querySelector("form");
    if (!form) return;
    var header = document.querySelector(".header");
    var top = header ? header.getBoundingClientRect().height : 0;
    var room = window.innerHeight - top;
    var box = form.getBoundingClientRect();
    var gap = box.height < room ? (room - box.height) / 2 : 16;
    var y = window.scrollY + box.top - top - gap;
    if (smooth) return window.scrollTo({ top: y, behavior: "smooth" });
    // The site scrolls smoothly (CSS); on arrival that animation fights the browser's own jump to the
    // anchor, so the first placement is instant.
    var root = document.documentElement;
    root.style.scrollBehavior = "auto";
    window.scrollTo(0, y);
    requestAnimationFrame(function () { root.style.scrollBehavior = ""; });
  }
  // The browser jumps to the anchor itself and fonts/images can still shift the page after that, so
  // centre once the page has loaded and again shortly after, unless the visitor has scrolled since.
  var touched = false;
  ["wheel", "touchstart", "keydown"].forEach(function (ev) { window.addEventListener(ev, function () { touched = true; }, { passive: true }); });
  function settle() { if (!touched) centreForm(false); }
  window.addEventListener("load", function () {
    settle();
    requestAnimationFrame(settle);
    setTimeout(settle, 150);
    setTimeout(settle, 500);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(settle);
  });
  window.addEventListener("hashchange", function () { centreForm(true); });
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a[href]");
    if (!a) return;
    var url = new URL(a.getAttribute("href"), location.href);
    // A link to the form of the page already open: centre it again even if the hash stays the same.
    if (url.pathname === location.pathname && targets[url.hash] && url.hash === location.hash) {
      e.preventDefault();
      centreForm(true);
    }
  });
})();
// Phone fields shaped as a Turkish number while typing: "0532 123 45 67" (+90 is dropped).
document.querySelectorAll('input[type="tel"]').forEach(function (el) {
  el.setAttribute("inputmode", "tel");
  if (!el.placeholder) el.placeholder = "0532 000 00 00";
  el.addEventListener("input", function () {
    var d = el.value.replace(/\D/g, "");
    if (d.indexOf("090") === 0) d = d.slice(1);
    if (d.indexOf("90") === 0) d = d.slice(2);
    if (d && d[0] !== "0") d = "0" + d;
    d = d.slice(0, 11);
    el.value = [d.slice(0, 4), d.slice(4, 7), d.slice(7, 9), d.slice(9, 11)].filter(Boolean).join(" ");
  });
});"""
    with open(os.path.join(ROOT, "assets", "site.js"), "w") as fh: fh.write(js)
    n = 0
    import re
    changed = set()
    # Content comparison ignores the ?v= asset fingerprints (a CSS change alone is not a page update).
    def norm(h): return re.sub(r'\?v=[0-9a-f]{8}', '', h)
    smap = os.path.join(ROOT, "sitemap.xml")
    prev = dict(re.findall(r'<loc>([^<]+)</loc><lastmod>([^<]+)</lastmod>', open(smap).read())) if os.path.exists(smap) else {}
    for lang in ("tr", "en"):
        outdir = ROOT if lang == "tr" else os.path.join(ROOT, "en")
        os.makedirs(outdir, exist_ok=True)
        pages = {"home": page_home(lang), "sectors": page_sectors(lang), "tiers": page_tiers(lang), "how": page_how(lang), "about": page_about(lang), "contact": page_contact(lang), "pilot": page_pilot(lang), "thanks": page_thanks(lang), "portal": page_portal(lang)}
        for p in PRODUCTS: pages[p] = page_product(lang, p)
        for p in LANDINGS: pages[p] = page_landing(lang, p)
        pages["guides"] = page_guides(lang)
        for p in GUIDES: pages[p] = page_guide(lang, p)
        pages["kvkk"] = page_kvkk(lang)
        for pid, html_ in pages.items():
            path = os.path.join(outdir, PAGES[pid][0 if lang == "tr" else 1])
            old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
            if old is None or norm(old) != norm(html_): changed.add((pid, lang))
            with open(path, "w", encoding="utf-8") as fh: fh.write(html_)
            n += 1
    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8") as fh: fh.write(page_notfound())
    n += 1
    # robots + sitemap
    indexed = [p for p in PAGES if p not in ("thanks", "kvkk", "notfound", "portal")]  # kvkk: noindex until legal sign-off; portal: stub
    today = __import__('datetime').date.today().isoformat()
    def entry(p, lang):
        alt = "".join(f'<xhtml:link rel="alternate" hreflang="{h}" href="{page_url(l, p)}"/>' for h, l in (("tr", "tr"), ("en", "en"), ("x-default", "tr")))
        mod = prev.get(page_url(lang, p), today) if (p, lang) not in changed else today
        return f"  <url><loc>{page_url(lang, p)}</loc><lastmod>{mod}</lastmod>{alt}</url>\n"
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
                 + "".join(entry(p, "tr") for p in indexed) + "".join(entry(p, "en") for p in indexed) + "</urlset>\n")
    with open(os.path.join(ROOT, "robots.txt"), "w") as fh:
        fh.write(f"User-agent: *\nAllow: /\nSitemap: https://{SITE['domain']}/sitemap.xml\n")
    print(f"built {n} pages")

if __name__ == "__main__":
    build()
