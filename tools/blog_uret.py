#!/usr/bin/env python3
"""İBAVALRESA blog sayfalarını üretir (yalnız TR, menüde değil).

blog.html ve blog/*.html, sss.html'nin menü/footer/script iskeletinden yeniden
üretilir; yazılar aşağıdaki POSTS listesinde (yeniden eskiye). Yeni yazı: POSTS'a
ekle, görseli img/blog/'a koy, site kökünden çalıştır:
    python3 tools/blog_uret.py
Blog sayfalarını elle düzenleme; bir sonraki çalıştırmada üzerine yazılır.
"""
import json, re, html, os

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.ibavalresa.com.tr"
src = open(os.path.join(KOK, "sss.html"), encoding="utf-8").read()

# ── iskelet: menü (body başı → sayfa içeriği) ve footer+scriptler ──
body_start = src.index("<body>")
nav_end = src.index("<!-- ── PAGE HERO (text) ── -->")
foot_start = src.index("<footer>")
nav = src[body_start:nav_end]
foot = src[foot_start:]
head_tail = src[src.index('<link rel="icon"'):src.index("<style>")]   # favicon, font, base.css

def mutlak(s):
    # /blog/ altında da çalışsın: göreli yolları kökten başlat
    s = re.sub(r'(href|src)="(?!https?:|/|#|mailto:|tel:|javascript:|data:)([^"]+)"', r'\1="/\2"', s)
    s = re.sub(r'\sdata-en="[^"]*"', "", s)          # kullanılmayan çeviri notları
    s = s.replace("location.href='/en/faq.html'", "location.href='/en/'")
    return s

nav, foot, head_tail = mutlak(nav), mutlak(foot), mutlak(head_tail)

CSS = """
.section-tag { display: inline-flex; align-items: center; gap: 8px; font-size: 12px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--accent); }
.section-tag::before { content: ""; width: 22px; height: 1px; background: var(--accent); opacity: .5; }
.blog-h1 { font-size: clamp(32px, 4.5vw, 52px); font-weight: 800; letter-spacing: -1.5px; line-height: 1.06; color: var(--text); margin: 20px 0 22px; max-width: 820px; text-wrap: balance; }
.blog-meta { font-size: 13.5px; color: var(--text3); margin-top: 18px; }
.crumb { font-size: 13px; color: var(--text3); margin-bottom: 22px; }
.crumb a { color: var(--text2); text-decoration: none; }
.crumb a:hover { color: var(--accent); }

/* Blog listesi */
.post-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 24px; }
.post-card { display: flex; flex-direction: column; border: 1px solid var(--border); border-radius: 14px; overflow: hidden; background: #fff; text-decoration: none; color: inherit; transition: transform .35s cubic-bezier(.22,.68,0,1), box-shadow .35s; }
.post-card:hover { transform: translateY(-4px); box-shadow: 0 18px 40px rgba(13,13,16,.10); }
.post-card img { display: block; width: 100%; height: auto; aspect-ratio: 1400 / 722; object-fit: cover; border-bottom: 1px solid var(--border); }
.post-card-body { padding: 24px 26px 26px; display: flex; flex-direction: column; gap: 10px; flex: 1; }
.post-card-tag { font-size: 11px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: var(--accent); }
.post-card-title { font-size: 21px; font-weight: 800; letter-spacing: -.5px; line-height: 1.2; color: var(--text); }
.post-card-desc { font-size: 14.5px; line-height: 1.65; color: var(--text2); }
.post-card-foot { margin-top: auto; padding-top: 8px; display: flex; justify-content: space-between; align-items: center; font-size: 13px; color: var(--text3); }
.post-card-foot span:last-child { color: var(--accent); font-weight: 600; }

/* Yazı */
.post-hero { margin: 8px 0 0; border-radius: 16px; overflow: hidden; border: 1px solid var(--border); background: #fff; }
.post-hero img { display: block; width: 100%; height: auto; }
.post-body { max-width: 760px; }
.post-body p { font-size: 17px; line-height: 1.75; color: var(--text2); margin-bottom: 18px; text-wrap: pretty; }
.post-body p strong, .post-body li strong { color: var(--text); }
.post-body ul, .post-body ol { margin: 4px 0 22px; padding-left: 22px; display: grid; gap: 10px; }
.post-body li { font-size: 17px; line-height: 1.7; color: var(--text2); padding-left: 4px; }
.post-body li::marker { color: var(--accent); font-weight: 700; }
.post-body h2 + p { margin-top: 0; }
.post-body .post-h2 { margin-top: 8px; }
.post-body > * + .post-h2 { margin-top: 40px; }
.post-figcap { font-size: 13px; color: var(--text3); padding: 12px 18px; border-top: 1px solid var(--border); }
.post-body a { color: var(--accent); text-decoration: none; border-bottom: 1px solid rgba(38,53,140,.3); }
.post-body a:hover { border-bottom-color: var(--accent); }
.post-h2 { font-size: clamp(24px, 2.6vw, 32px); font-weight: 800; letter-spacing: -1px; line-height: 1.15; color: var(--text); margin: 0 0 12px; text-wrap: balance; }
.post-sub { font-size: 16px; line-height: 1.65; color: var(--text2); max-width: 720px; margin-bottom: 28px; }

.pdf-box { display: flex; align-items: center; justify-content: space-between; gap: 24px; flex-wrap: wrap; max-width: 760px; margin: 30px 0 4px; padding: 22px 26px; border-radius: 14px; background: #f5f5f7; border: 1px solid var(--border); }
.pdf-box-title { font-size: 17px; font-weight: 700; color: var(--text); letter-spacing: -.3px; }
.pdf-box-meta { font-size: 13.5px; color: var(--text3); margin-top: 3px; }

.nw { white-space: nowrap; }

.post-note { max-width: 760px; margin-top: 22px; font-size: 13.5px; line-height: 1.6; color: var(--text3); }
@media (max-width: 600px) { .pdf-box { flex-direction: column; align-items: stretch; } .pdf-box .btn-primary { justify-content: center; } }
"""

def sayfa(*, yol, title, desc, og_img, og_type, schema, icerik):
    url = SITE + "/" + yol
    e = html.escape
    head = f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)}</title>
<link rel="canonical" href="{url}">
<meta name="description" content="{e(desc)}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="İBAVALRESA">
<meta property="og:locale" content="tr_TR">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}{og_img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{SITE}{og_img}">
"""
    for sc in schema:
        head += '<script type="application/ld+json">' + json.dumps(sc, ensure_ascii=False) + "</script>\n"
    head += "\n" + head_tail + "<style>" + CSS + "</style>\n"
    nav_js = '<script src="/js/nav-line.js' + re.search(r'/js/nav-line\.js(\?v=[0-9a-f]+)', src).group(1) + '" defer></script>\n'
    out = head + nav_js + "</head>\n" + nav + icerik + "\n" + foot
    p = os.path.join(KOK, yol)
    os.makedirs(os.path.dirname(p) or KOK, exist_ok=True)
    open(p, "w", encoding="utf-8").write(out)
    print("yazıldı:", yol, len(out))

# ── yazılar (yeniden eskiye) ──
ARROW = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>'
org = {"@type": "Organization", "name": "İBAVALRESA", "url": SITE + "/", "logo": SITE + "/assets/logos/ibavalresa-black.png"}

def cta(ust, baslik):
    return f"""
<section class="about-section" style="border-top:none; padding-top:8px; padding-bottom:64px;">
  <div class="section-inner">
    <div class="faq-cta" style="display:flex;align-items:center;justify-content:space-between;gap:24px;flex-wrap:wrap;max-width:760px;border:1px solid rgba(38,53,140,0.18);background:#f4f5fb;border-radius:14px;padding:24px 28px;">
      <div><div style="font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);margin-bottom:4px;">{ust}</div>
        <div style="font-size:18px;font-weight:700;letter-spacing:-.4px;color:var(--text);">{baslik}</div></div>
      <a class="btn-primary" href="/iletisim.html"><span>Bize Ulaşın</span>{ARROW}</a>
    </div>
  </div>
</section>
"""

def bas(p):
    return f"""
<section class="about-section" style="padding-top: 140px; padding-bottom: 20px; border-top: none;">
  <div class="section-inner">
    <div class="crumb"><a href="/blog.html">Blog</a> &nbsp;/&nbsp; {p['etiket']}</div>
    <div class="section-tag">{p['etiket']}</div>
    <h1 class="blog-h1">{p['h1']}</h1>
    <p class="about-lead" style="max-width:760px;">{p['lead']}</p>
    <div class="blog-meta"><time datetime="{p['tarih_iso']}">{p['tarih']}</time>{(' · Güncellendi: <time datetime="' + p['guncel_iso'] + '">' + p['guncel'] + '</time>') if p.get('guncel_iso') else ''} · İBAVALRESA</div>
  </div>
</section>
"""

POSTS = []

# 2) Spor salonu parkesi
p = dict(yol="blog/spor-salonu-parke-vernik-yenileme.html", etiket="Uygulama Rehberi",
         baslik="Spor Salonu Parkelerinde Vernik Yenileme: Doğru Ürün Nasıl Seçilir?",
         h1="Spor salonu parkelerinde vernik yenileme: doğru ürün nasıl seçilir?",
         lead="Uluslararası organizasyonlara ev sahipliği yapan bir spor kompleksinin parke sahasını su bazlı sistemimizle yeniledik. Bu uygulama üzerinden, spor parkelerinde vernik seçerken nelere dikkat edilmesi gerektiğini anlatıyoruz.",
         ozet="Spor parkesi vernikten ne bekler, geniş yüzeyde renk bütünlüğü nasıl korunur? Su bazlı 700600 verniğimizle tamamlanan bir saha uygulamasından notlar.",
         desc="Spor salonu parkelerinde vernik seçimi: aşınma dayanımı, kayma direnci, parlaklık ve geniş yüzeyde renk bütünlüğü. Su bazlı 700600 vernikle tamamlanan bir saha yenileme uygulaması.",
         tarih_iso="2026-10-06", tarih="6 Ekim 2026",
         hero="/img/blog/spor-salonu-parke-su-bazli-vernik.jpg", hero_wh=(1400, 584),
         hero_alt="Spor salonu parke sahasında su bazlı vernik uygulaması",
         og="/img/blog/spor-salonu-parke-su-bazli-vernik-og.jpg")
p["govde"] = bas(p) + f"""
<section class="about-section" style="border-top:none; padding-top:12px;">
  <div class="section-inner">
    <figure class="post-hero"><img src="{p['hero']}" alt="{p['hero_alt']}" width="1400" height="584" fetchpriority="high"><figcaption class="post-figcap">Spor salonu parke sahasında vernik yenileme uygulaması.</figcaption></figure>
    <div class="post-body" style="margin-top:40px;">
      <h2 class="post-h2">Spor parkesi vernikten ne bekler?</h2>
      <p>Spor salonu parkesi, konut parkesinden çok daha ağır bir yük altındadır: ani duruş ve dönüşlerde ayakkabı sürtünmesi, top ve ekipman darbeleri, sık temizlik ve neredeyse kesintisiz kullanım. Bu yüzden vernik yalnızca ahşabı korumak için değil, oyunun güvenliği ve sahanın görünümü için de belirleyicidir. Doğru vernik sisteminde şu özellikler aranır:</p>
      <ul>
        <li><strong>Aşınma ve çizilme dayanımı:</strong> yoğun trafiğe ve sürtünmeye karşı uzun ömürlü bir yüzey.</li>
        <li><strong>Dengeli kayma direnci:</strong> oyuncu kaymadan durabilmeli, dönüşlerde de yüzeye takılmamalıdır. Spor zeminleri için EN 14904 gibi standartlar bu dengeyi tanımlar.</li>
        <li><strong>Kontrollü parlaklık:</strong> aşırı parlak bir yüzey salon ışığını yansıtır; oyuncunun görüşünü ve televizyon yayınındaki görüntüyü olumsuz etkiler.</li>
        <li><strong>Düşük koku ve hızlı devreye alma:</strong> kapalı salonlarda su bazlı sistemler, solvent bazlı sistemlere göre genellikle daha düşük koku ve uçucu organik bileşik (VOC) içeriğiyle çalışmayı kolaylaştırır.</li>
        <li><strong>Çizgi ve renk uyumu:</strong> saha çizgileri ve renkli alanlar, vernik katları altında bozulmadan korunmalıdır.</li>
      </ul>

      <h2 class="post-h2">Geniş yüzeyde renk bütünlüğü nasıl korunur?</h2>
      <p>Renkli bir kat uygulandığında en sık karşılaşılan sorun, ek yeri ve tur izleridir. Bir şerit kurumaya başlarken yanına gelen yeni şerit onun üzerine bindiğinde, iki uygulama arasında ton farkı oluşur. Bir basketbol sahası büyüklüğündeki yüzeyde bunu önlemenin yolu, ürünün açık kalma süresini, yani yüzeyin işlenebilir kaldığı süreyi, uygulama hızına göre uzatmaktır.</p>
      <p>Bu uygulamada istenen özel renk tonu, <strong>700400</strong> kodlu ürünümüzün içine su bazlı renk pastalarımız katılarak elde edildi. Geniş yüzeyde renk bütünlüğünü korumak, ek yerlerinde ton farkını önlemek ve kurumayı kontrollü şekilde yavaşlatmak için <a href="/arge.html">Ar-Ge</a> birimimizin bu iş için özel olarak hazırladığı <strong>ZZ 1012 Retarder</strong>, ürüne <strong>%7</strong> oranında ilave edildi.</p>

      <h2 class="post-h2">Uygulama adımları</h2>
      <ol>
        <li>Sahadaki mevcut vernik sisteminin tamamen yenilenmesi için yüzeyin hazırlanması.</li>
        <li>İstenen renk tonunun 700400 kodlu ürüne su bazlı renk pastalarıyla verilmesi.</li>
        <li>Açık kalma süresini uzatmak için ZZ 1012 Retarder'ın %7 oranında eklenmesi ve renkli katın uygulanması.</li>
        <li>18 saatlik bekleme süresi.</li>
        <li>Son kat olarak <strong>700600 su bazlı verniğimizin</strong> uygulanması.</li>
      </ol>

      <h2 class="post-h2">Sahadan sonuç</h2>
      <p>Bu çalışmayla, uluslararası spor organizasyonlarına ev sahipliği yapan bir spor kompleksinin sahasında İBAVALRESA ürünleri <strong>%100 oranında</strong> kullanıldı. Ürünlerimiz daha önce de uluslararası organizasyonlara ev sahipliği yapan bir başka büyük spor kompleksinin parke uygulamasında %100 oranında kullanılmıştı. Böylece iki önemli spor kompleksinde başarılı uygulamalar tamamlanmış oldu.</p>
      <p>Spor zemini projelerinde ürün seçimi; sahanın kullanım yoğunluğuna, istenen renk ve parlaklığa ve uygulama süresine göre birlikte planlanmalıdır. Teknik ekibimiz, projeye özel renk ve uygulama sistemi için destek verir.</p>
    </div>
  </div>
</section>
""" + cta("Teknik destek", "Spor zemini projeniz için sistemi birlikte planlayalım")
POSTS.append(p)

# 1) Valresa Renk Trendleri
PDF = "/belgeler/Valresa-Colour-Trends-2026-2027.pdf"
p = dict(yol="blog/valresa-renk-trendleri-2026-2027.html", etiket="Renk Trendleri",
         baslik="Valresa 2026–2027 Renk Trendleri",
         h1='Valresa <span class="nw">2026–2027</span> Renk Trendleri',
         lead="Renk makinesi sistemlerimizde en çok tercih edilen renklerden derlenen koleksiyon; mimarlar, iç mimarlar ve mobilya tasarımcıları için seçili RAL tonlarını 17 renk ailesinde sunar.",
         ozet="Renk makinesi sistemlerimizde en çok tercih edilen renklerden derlenen, 17 renk ailesinde seçili RAL tonlarından oluşan profesyonel renk paleti.",
         desc="Valresa 2026–2027 Renk Trendleri: renk makinesi sistemlerimizde en çok tercih edilen renklerden derlenen 17 renk ailesi ve 94 seçili RAL tonu. Mimarlar, iç mimarlar ve mobilya tasarımcıları için PDF katalog.",
         tarih_iso="2026-10-05", tarih="5 Ekim 2026", guncel_iso="2026-10-07", guncel="7 Ekim 2026",
         hero="/img/blog/valresa-renk-trendleri-2026-2027.jpg", hero_wh=(1400, 722),
         hero_alt="Valresa 2026–2027 Colour Trends / Renk Trendleri kataloğu kapağı",
         og="/img/blog/valresa-renk-trendleri-2026-2027-og.jpg")
p["govde"] = bas(p) + f"""
<section class="about-section" style="border-top:none; padding-top:12px;">
  <div class="section-inner">
    <figure class="post-hero"><img src="{p['hero']}" alt="{p['hero_alt']}" width="1400" height="722" fetchpriority="high"></figure>
    <div class="post-body" style="margin-top:40px;">
      <h2 class="post-h2">Koleksiyon hakkında</h2>
      <p>Valresa 2026–2027 Renk Trendleri; mimarlar, iç mimarlar ve mobilya tasarımcıları için <strong>seçili RAL tonlarını</strong>, güncel renk yönelimlerini ve zamansız nötrlerden karakterli tonlara uzanan profesyonel bir renk paletinde buluşturur.</p>
      <p>Koleksiyon, <strong>renk makinesi sistemlerimizde en çok tercih edilen renklerden</strong> derlenmiştir. Katalogdaki tonlar, mobilya ve iç mekân uygulamalarında sahada sıkça seçilen renklerdir.</p>
      <p>Renkler, farklı tasarım yaklaşımlarında kolay yorumlanabilmesi ve doğru tonların daha hızlı karşılaştırılabilmesi için tematik renk aileleri altında gruplandırılmıştır. Seçili RAL referanslarıyla hazırlanan koleksiyon, iç mimari, mobilya ve yüzey tasarımında renk kararlarına ilham vermeyi amaçlar.</p>

      <h2 class="post-h2">Katalogda neler var?</h2>
      <ul>
        <li><strong>17 tematik renk ailesi:</strong> Pure Whites (Saf Beyazlar) ve Soft Neutrals (Yumuşak Nötrler) gibi zamansız nötrlerden Red Collection (Kırmızılar) ve Botanical Greens (Botanik Yeşiller) gibi karakterli tonlara.</li>
        <li><strong>94 seçili RAL tonu:</strong> her ailede, renk kartı ve RAL koduyla.</li>
        <li><strong>Pantone Yılın Renkleri 2017–2026:</strong> son on yılın renk yönelimlerini izlemek için referans.</li>
      </ul>
    </div>
    <div class="pdf-box">
      <div><div class="pdf-box-title">Valresa Colour Trends 2026–2027</div><div class="pdf-box-meta">PDF</div></div>
      <a class="btn-primary" href="{PDF}" target="_blank" rel="noopener"><span>Kataloğu İncele</span>{ARROW}</a>
    </div>
  </div>
</section>

<section class="about-section">
  <div class="section-inner">
    <div class="post-body">
      <h2 class="post-h2">Mobilyada renk seçimi neden önemlidir?</h2>
      <p>Mobilyada renk, bir parçanın mekân içindeki rolünü belirleyen ilk karardır. Aynı form; açık bir nötrde mekâna karışan sakin bir arka plana, koyu bir grafitte ise odak noktasına dönüşür. Renk; ahşap dokusu, metal aksesuar, taş ve kumaş gibi malzemelerle birlikte okunduğu için tek başına değil, projenin bütün malzeme paletiyle birlikte değerlendirilmelidir.</p>
      <p>Aynı ton, yüzeyin parlaklık derecesine ve ışığa göre de farklı algılanır. Mat bir yüzeyde daha yumuşak, parlak bir yüzeyde daha derin ve doygun görünür; gün ışığı ve yapay aydınlatma aynı rengi sıcak ya da soğuk gösterebilir. Bu nedenle renk kararı, nihai yüzey ve ışık koşullarında hazırlanmış bir numune üzerinden onaylanmalıdır.</p>
      <p>Seri üretimde ise rengin her partide aynı çıkması belirleyicidir. RAL gibi standart bir referans kullanmak; tasarımcı, mobilya üreticisi ve boya tedarikçisi arasında aynı rengin aynı kodla konuşulmasını sağlar ve tekrar siparişlerde tutarlılığı korur. İBAVALRESA'nın <a href="/renk-makinesi.html">renk makinesi</a> sistemleri, RAL referanslı renklerin farklı zamanlarda ve farklı üretim partilerinde aynı kaliteyle yeniden hazırlanmasını sağlar; standart kartelalar için <a href="/renk-paleti.html">Renk Paleti</a> sayfasına göz atabilirsiniz.</p>
    </div>
    <p class="post-note">Dijital renkler ekran ayarlarına göre farklı görünebilir; katalogdaki tonlar yalnızca yaklaşık renk referansı olarak değerlendirilmelidir.</p>
  </div>
</section>
""" + cta("Kartela ve numune", "Projeniz için tonları birlikte seçelim")
POSTS.append(p)

for p in POSTS:
    url = SITE + "/" + p["yol"]
    sayfa(yol=p["yol"], title=p["baslik"] + " — İBAVALRESA Blog", desc=p["desc"], og_img=p["og"], og_type="article",
          schema=[{"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["baslik"], "description": p["desc"],
                   "image": [SITE + p["hero"]], "datePublished": p["tarih_iso"], "dateModified": p.get("guncel_iso", p["tarih_iso"]), "inLanguage": "tr-TR",
                   "author": org, "publisher": org, "mainEntityOfPage": url},
                  {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                      {"@type": "ListItem", "position": 1, "name": "Blog", "item": SITE + "/blog.html"},
                      {"@type": "ListItem", "position": 2, "name": p["baslik"], "item": url}]}],
          icerik=p["govde"])

# ── blog ana sayfası ──
kartlar = ""
for i, p in enumerate(POSTS):
    w, h = p["hero_wh"]
    yuk = 'fetchpriority="high"' if i == 0 else 'loading="lazy"'
    kartlar += f"""
      <a class="post-card" href="/{p['yol']}">
        <img src="{p['hero']}" alt="{p['hero_alt']}" width="{w}" height="{h}" {yuk}>
        <div class="post-card-body">
          <div class="post-card-tag">{p['etiket']}</div>
          <div class="post-card-title">{p['h1'] if 'nw' in p['h1'] else p['baslik']}</div>
          <p class="post-card-desc">{p['ozet']}</p>
          <div class="post-card-foot"><span>{p['tarih']}</span><span>Yazıyı oku →</span></div>
        </div>
      </a>"""
liste = f"""
<section class="about-section" style="padding-top: 148px; padding-bottom: 24px; border-top: none;">
  <div class="section-inner">
    <div class="section-tag">Blog</div>
    <h1 class="blog-h1">Renk, yüzey ve boya üzerine</h1>
    <p class="about-lead" style="max-width:680px;font-size:clamp(14px,1.3vw,18px);color:var(--text2);">Renk trendleri, uygulama rehberleri ve ahşap, mobilya ve sanayi boyaları üzerine İBAVALRESA'dan notlar.</p>
  </div>
</section>

<section class="about-section" style="border-top:none; padding-top:8px; padding-bottom:72px;">
  <div class="section-inner">
    <div class="post-list">{kartlar}
    </div>
  </div>
</section>
"""
sayfa(yol="blog.html", title="Blog — İBAVALRESA", desc="Renk trendleri, uygulama rehberleri ve ahşap, mobilya ve sanayi boyaları üzerine İBAVALRESA blog yazıları.",
      og_img=POSTS[0]["og"], og_type="website",
      schema=[{"@context": "https://schema.org", "@type": "Blog", "name": "İBAVALRESA Blog", "url": SITE + "/blog.html", "inLanguage": "tr-TR",
               "publisher": org,
               "blogPost": [{"@type": "BlogPosting", "headline": p["baslik"], "url": SITE + "/" + p["yol"], "datePublished": p["tarih_iso"]} for p in POSTS]}],
      icerik=liste)
