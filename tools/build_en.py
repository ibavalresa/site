#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""İBAVALRESA — TR içerik sayfalarından /en/ İngilizce sayfaları üretir (Method B).
Çalıştır: python3 build_en.py   (site kökünden)
"""
import re, html, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
# script scratchpad'te; site kökünü argümandan al
SITE = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
BASE = "https://www.ibavalresa.com.tr"

FOLD = r'(?:assets|img|video|brands|belgeler|insta)'

# İngilizce olarak üretilecek içerik sayfaları (slug -> EN title, EN meta description)
PAGES = {
 "index": (
   "Wood Coatings Manufacturer in Turkey — İBAVALRESA",
   "Turkey-based wood coatings manufacturer — acrylic, polyurethane, water-based and UV-curing finishes. 60+ years of expertise, global exports."),
 "hakkimizda": (
   "About Us — Turkish–Spanish Coatings Manufacturer — İBAVALRESA",
   "İBAVALRESA is a Turkish–Spanish manufacturer of wood, furniture and industrial coatings. Data-driven, traceable and sustainable production."),
 "arge": (
   "R&D and Product Development in Coatings — İBAVALRESA",
   "İBAVALRESA R&D develops technological products, innovative formulations and sustainable, eco-friendly coating solutions with Turkish–Spanish know-how."),
 "markalar": (
   "Our Brands: Valresa, Esfera, İbavet, İba — İBAVALRESA",
   "İBAVALRESA brands: Valresa (wood paint & varnish), Esfera, İbavet and İba Industrial Coatings — end-to-end solutions for furniture and industry."),
 "hizmetlerimiz": (
   "Color, Technical Support & Application Services — İBAVALRESA",
   "İBAVALRESA's customer-focused sales and technical support: export strength, after-sales service, strong references and technological color services."),
 "uretim-ve-teknoloji": (
   "Coatings Production & Manufacturing Technology — İBAVALRESA",
   "A 37,000 m² facility with SAP & SCADA automation and fully traceable processes — the same quality in every batch. İBAVALRESA production & technology."),
 "kalite-sertifikalar": (
   "Quality Management, ISO 9001 & Certificates — İBAVALRESA",
   "ISO 9001:2015 quality management, accredited certificates and independent lab testing deliver İBAVALRESA's high, repeatable product quality."),
 "surdurulebilirlik": (
   "Sustainability & Environmental Policy — İBAVALRESA",
   "Focused on environment, occupational health and safety, İBAVALRESA pursues sustainable production and eco-conscious application in the chemical sector."),
 "insan-kaynaklari": (
   "Human Resources & Careers — İBAVALRESA",
   "İBAVALRESA career opportunities: internships, project engineering and jobs. Join a team that grows together, takes responsibility and adds value."),
 "bolge-mudurlukleri": (
   "Regional Offices & Dealer Network — İBAVALRESA",
   "İBAVALRESA regional offices and authorized sales–technical teams. Contact your nearest representative across Türkiye (Turkey) directly."),
 "iletisim": (
   "Contact Us — Get in Touch — İBAVALRESA",
   "Contact İBAVALRESA: reach us for your questions and partnerships."),
 "renk-paleti": (
   "RAL, NCS & NOVA Color Charts — İBAVALRESA",
   "RAL, NCS and NOVA color charts. Requested colors are produced in-house with Valresa Color System machines; download the chart PDFs now."),
 "renk-makinesi": (
   "On-Site Tinting with Color Machines — İBAVALRESA",
   "İBAVALRESA color-machine systems match RAL, NCS and NOVA colors with a spectrophotometer: high accuracy and repeatable color production."),
}
CONTENT = set(PAGES.keys())

# TR slug -> İngilizce /en/ dosya adı (SEO için İngilizce URL'ler)
SLUG = {
 "index": "index",
 "hakkimizda": "about",
 "arge": "research-development",
 "markalar": "brands",
 "hizmetlerimiz": "services",
 "uretim-ve-teknoloji": "production-technology",
 "kalite-sertifikalar": "quality-certificates",
 "surdurulebilirlik": "sustainability",
 "insan-kaynaklari": "careers",
 "bolge-mudurlukleri": "regional-offices",
 "iletisim": "contact",
 "renk-paleti": "color-charts",
 "renk-makinesi": "color-machines",
}

# Görsel alt metinleri: Türkçe -> İngilizce (marka adları korunur; yalnız açıklayıcılar çevrilir)
ALT_MAP = {
 "İbavalresa YouTube": "İbavalresa on YouTube",
 "İbavalresa – Güçlü İş Ortakları Bayi Toplantısı": "İbavalresa — Business Partners Dealer Meeting",
 "İbavalresa Üretim Tesisi — Ankara Sincan 1. OSB (çizim)": "İbavalresa wood coatings production facility — Ankara Sincan 1st OIZ (illustration)",
 "İbavalresa Çevre Politikası": "İbavalresa Environmental Policy",
 "İbavalresa Kampüsü — Ankara Sincan OSB": "İbavalresa campus — Ankara Sincan 1st OIZ",
 "İbavalresa Kampüs — Sincan OSB": "İbavalresa campus — Sincan OIZ",
 "İbavalresa Kalite Politikası": "İbavalresa Quality Policy",
 "İbavalresa Ar-Ge": "İbavalresa R&D laboratory",
 "İba Sanayi Boyaları": "İba Industrial Coatings",
 "İba Sanayi Boyaları — Performance Coatings, 1977": "İba Industrial Coatings — Performance Coatings, 1977",
 "İBAVALRESA — İyi Çevre Uygulamaları": "İBAVALRESA — Good Environmental Practices",
 "İBAVALRESA İnsan Kaynakları": "İBAVALRESA Human Resources",
 "Üretim Teknolojisi": "Wood coating production technology",
 "Valresa 50. Yıl Kutlaması": "Valresa 50th Anniversary Celebration",
 "Spektrofotometre ile merkezi renk yönetim sistemi": "Central color management system with a spectrophotometer",
 "Lojistik Güç - Yüksek Depo": "Logistics power — automated high-bay warehouse",
 "Lojistik Güç - Tesis Kurulumu": "Logistics power — facility installation",
 "Lojistik Güç - Otomatik Raf Sistemi": "Logistics power — automated racking system",
 "Ar-Ge": "R&D laboratory",
 # Instagram bar görselleri (SEO adlı, açıklayıcı alt)
 "İbavalresa — Dünya Kupası": "İbavalresa — World Cup",
 "Valresa — Pantone 2026 yılın rengi": "Valresa — Pantone 2026 Color of the Year",
 "İbavet ahşap boya ambalajları": "İbavet wood coating packaging",
 "Valresa mobilya boyası renk paleti": "Valresa furniture coating color palette",
 "İbavalresa — 1 Mayıs": "İbavalresa — May 1st",
 "İbavalresa otomasyonlu boya üretim hattı": "İbavalresa automated coating production line",
 "İbavalresa Ar-Ge ekibi — TURKCOAT Kongresi": "İbavalresa R&D team — TURKCOAT Congress",
 "İbavalresa boya üretim tesisi (havadan)": "İbavalresa coating production facility (aerial)",
 "İbavalresa bayi toplantısı": "İbavalresa dealer meeting",
 "Esfera su bazlı mobilya boyası": "Esfera water-based furniture coating",
 "Valresa — Tahran fuarı": "Valresa — Tehran exhibition",
 "İbavalresa boya fabrikası — Ankara Sincan": "İbavalresa coating factory — Ankara Sincan",
}

def esc_attr(t):  # HTML attribute-safe (title/desc contain &, quotes)
    return t.replace('&', '&amp;').replace('"', '&quot;')

def tr_url(slug):
    return "/" if slug == "index" else "/" + slug + ".html"

def en_path(slug):
    # /en/ göreli yolu (İngilizce slug ile)
    return "/en/" if slug == "index" else "/en/" + SLUG[slug] + ".html"

def en_canon(slug):
    return BASE + en_path(slug)

def hreflang_block(slug):
    tr = BASE + ("/" if slug == "index" else "/" + slug + ".html")
    en = en_canon(slug)
    return ('<link rel="alternate" hreflang="tr" href="' + tr + '">\n'
            '<link rel="alternate" hreflang="en" href="' + en + '">\n'
            '<link rel="alternate" hreflang="x-default" href="' + tr + '">\n')

# ---- data-en bake ----
BAKE = re.compile(
    r'<(?P<tag>[a-zA-Z0-9]+)(?P<pre>[^>]*?)\sdata-en="(?P<val>[^"]*)"(?P<post>[^>]*?)>(?P<inner>.*?)</(?P=tag)>',
    re.S)

def bake(m):
    val = html.unescape(m.group('val'))
    return f"<{m.group('tag')}{m.group('pre')}{m.group('post')}>{val}</{m.group('tag')}>"

def bake_all(s):
    prev = None
    while prev != s:
        prev = s
        s = BAKE.sub(bake, s)
    # placeholder çevirileri (iki olası sıra)
    s = re.sub(r'placeholder="[^"]*"([^>]*?)\sdata-en-ph="([^"]*)"',
               lambda m: 'placeholder="' + html.unescape(m.group(2)) + '"' + m.group(1), s)
    s = re.sub(r'data-en-ph="([^"]*)"([^>]*?)\splaceholder="[^"]*"',
               lambda m: m.group(2) + ' placeholder="' + html.unescape(m.group(1)) + '"', s)
    # kalan öznitelikleri temizle
    s = re.sub(r'\sdata-en="[^"]*"', '', s)
    s = re.sub(r'\sdata-en-ph="[^"]*"', '', s)
    return s

# ---- iç link haritalama ----
def maplink(m):
    href, frag = m.group(1), (m.group(2) or '')
    slug = href[:-5]
    if slug == 'index':
        return 'href="/en/' + frag + '"'
    if slug in CONTENT:
        return 'href="/en/' + SLUG[slug] + '.html' + frag + '"'
    return 'href="/' + href + frag + '"'  # legal/sunum vb. → Türkçe kök

# ---- switcher + selectLang override (EN sayfası) ----
def switcher_script(slug):
    turl = tr_url(slug)
    return ('\n<script>\n'
            '(function(){\n'
            '  document.querySelectorAll(".lang-option").forEach(function(el){\n'
            '    var a=el.dataset.lang==="EN";\n'
            '    el.classList.toggle("active",a);\n'
            '    var c=el.querySelector(".lang-check"); if(c) c.style.opacity=a?"1":"0";\n'
            '  });\n'
            '  var lc=document.getElementById("lang-current"); if(lc) lc.textContent="EN";\n'
            '  document.querySelectorAll(".mobile-menu-langs button").forEach(function(b){\n'
            '    b.classList.toggle("active", b.textContent.trim().endsWith("EN"));\n'
            '  });\n'
            '  window.selectLang=function(l){ if(l==="TR"){ location.href="' + turl + '"; } };\n'
            '})();\n'
            '</script>\n')

# ---- JSON-LD İngilizce ----
JSONLD_REPL = [
 ('"description":"Türk–İspanyol ortaklığıyla ahşap, mobilya ve sanayi boyaları ile vernik üreten kuruluş."',
  '"description":"A Turkish–Spanish manufacturer of wood, furniture and industrial paints and varnishes."'),
 ('"knowsAbout":["Ahşap boyası","Mobilya boyası","Sanayi boyası","Ahşap verniği","Renk üretimi"]',
  '"knowsAbout":["Wood coatings","Furniture finishes","Industrial coatings","Wood varnish","Color production"]'),
 # breadcrumb item adları (renk-paleti / renk-makinesi)
 ('"name":"Ana Sayfa"', '"name":"Home"'),
 ('"name":"Renk Makinesi"', '"name":"Color Machine"'),
 ('"name":"Renk Paleti"', '"name":"Color Palette"'),
 ('"name":"Hizmetlerimiz"', '"name":"Services"'),
]

# ---- index'e özel EN-only ekler ----
HERO_INTRO = ('  <p class="hero-intro">İBAVALRESA is a Türkiye (Turkey)-based wood coatings manufacturer, '
              'producing acrylic, polyurethane, water-based and UV-curing furniture finishes for both '
              'domestic and export markets. Turkey is among the world\'s leading producers and exporters '
              'of wood coatings and furniture varnishes.</p>\n\n')
HERO_INTRO_CSS = ('.hero-intro{max-width:640px;font-size:15px;color:var(--text2);'
                  'line-height:1.7;position:relative;z-index:2;margin:0 auto 36px;}\n')

def build(slug):
    src = os.path.join(SITE, slug + ".html")
    s = open(src, encoding='utf-8').read()
    title, desc = PAGES[slug]
    et, ed = esc_attr(title), esc_attr(desc)

    s = bake_all(s)
    s = s.replace('<html lang="tr">', '<html lang="en">')

    # title / meta
    s = re.sub(r'<title>.*?</title>', '<title>' + esc_attr(title) + '</title>', s, count=1, flags=re.S)
    s = re.sub(r'(<meta name="description" content=")[^"]*(">)', r'\g<1>' + ed + r'\2', s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*(">)', r'\g<1>' + et + r'\2', s, count=1)
    s = re.sub(r'(<meta property="og:description" content=")[^"]*(">)', r'\g<1>' + ed + r'\2', s, count=1)
    s = re.sub(r'(<meta name="twitter:title" content=")[^"]*(">)', r'\g<1>' + et + r'\2', s, count=1)
    s = re.sub(r'(<meta name="twitter:description" content=")[^"]*(">)', r'\g<1>' + ed + r'\2', s, count=1)
    s = s.replace('content="tr_TR"', 'content="en_US"')

    # canonical + og:url + hreflang
    # TR kaynağındaki mevcut hreflang'leri temizle (çift eklemeyi önle)
    s = re.sub(r'\s*<link rel="alternate" hreflang="[^"]*" href="[^"]*">', '', s)
    canon = en_canon(slug)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*(">)', r'\g<1>' + canon + r'\2', s, count=1)
    s = re.sub(r'(<meta property="og:url" content=")[^"]*(">)', r'\g<1>' + canon + r'\2', s, count=1)
    s = re.sub(r'<link rel="canonical" href="[^"]*">',
               lambda m: m.group(0) + "\n" + hreflang_block(slug), s, count=1)

    # görsel alt metinleri -> İngilizce
    for tr, en in ALT_MAP.items():
        s = s.replace('alt="' + tr + '"', 'alt="' + en + '"')

    # JSON-LD İngilizce
    for a, b in JSONLD_REPL:
        s = s.replace(a, b)

    # mutlak asset yolları
    s = re.sub(r'(src|href|poster)="(' + FOLD + r'/)', r'\1="/\2', s)
    s = re.sub(r'url\((["\']?)(' + FOLD + r'/)', r'url(\1/\2', s)

    # iç sayfa linkleri
    s = re.sub(r'href="([a-z0-9\-]+\.html)(#[^"]*)?"', maplink, s)

    # index EN-only ekler
    if slug == "index":
        s = s.replace('  <div class="hero-actions">', HERO_INTRO + '  <div class="hero-actions">', 1)
        s = s.replace('</style>', HERO_INTRO_CSS + '</style>', 1)
        # H1'e ülke ekle (yalnız EN; hedef "wood coatings turkey")
        s = s.replace(
            '<h1 id="hero-title">Wood, Furniture & Industrial Coatings Manufacturer</h1>',
            '<h1 id="hero-title">Wood, Furniture & Industrial Coatings Manufacturer in Turkey</h1>', 1)

    # Dil butonlarını EN bağlamına normalize et (TR kaynağın redirect'ini devralma):
    # EN butonu no-op olmalı (zaten EN sayfadayız), TR butonu selectLang('TR') ile
    # switcher override üzerinden Türkçe sayfaya yönlenir.
    s = re.sub(r'(data-lang="EN" onclick=")[^"]*(")', r"\1selectLang('EN')\2", s)
    s = re.sub(r'(<button onclick=")[^"]*(">🇬🇧 EN</button>)', r"\1selectLang('EN')\2", s)

    # switcher init + override (</body>'den önce)
    s = s.replace('</body>', switcher_script(slug) + '</body>', 1)

    out = os.path.join(SITE, "en", SLUG[slug] + ".html")
    open(out, 'w', encoding='utf-8').write(s)
    # kalan Türkçe data-en / kontrol
    leftover = len(re.findall(r'data-en', s))
    return leftover

if __name__ == "__main__":
    os.makedirs(os.path.join(SITE, "en"), exist_ok=True)
    for slug in PAGES:
        lo = build(slug)
        print(f"{'OK ' if lo==0 else 'WARN'} en/{SLUG[slug]}.html  (kaynak: {slug}.html)")
