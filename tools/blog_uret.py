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

# 6) CNC yüzeylerde köşe kapatma
p = dict(yol="blog/cnc-kose-kapatma-astar.html", etiket="Ürün Teknolojisi",
         baslik="CNC İşlemeli MDF'de Köşe Kapatma: Astar Kenarlardan Neden Çekilir?",
         h1="CNC işlemeli MDF yüzeylerde astar neden köşeleri kapatmıyor?",
         lead="Derin kanallı ve profil geçişli CNC kapaklarda düz yüzey ilk astarda kapanırken köşeler açık kalabiliyor. Sebebi çoğu zaman astarın yetersizliği değil, frezenin MDF'nin iç yapısını açması. Köşede ne olduğunu ve ikinci astar turunu nasıl gereksiz kıldığımızı anlatıyoruz.",
         ozet="CNC kanal kenarları ve profil geçişleri ilk astarda neden kapanmaz, ikinci astar turu nasıl ortadan kalkar?",
         desc="CNC işlemeli MDF'de köşe kapatma sorunu: freze, MDF'nin düşük yoğunluklu göbeğini açar ve astar oraya çeker. Yüksek katı maddeli, tiksotropik astarlarla köşelere ikinci astar turuna gerek kalmaz.",
         tarih_iso="2026-11-06", tarih="6 Kasım 2026",
         hero="/img/blog/cnc-kose-kapatma-astar.jpg", hero_wh=(1400, 722),
         hero_alt="MDF kesiti şeması: düz yüzeyde astar filmi tam kalınlıkta kalır, frezelenen kanalda göbek astarı emer ve film incelir",
         og="/img/blog/cnc-kose-kapatma-astar-og.jpg")
p["govde"] = bas(p) + f"""
<section class="about-section" style="border-top:none; padding-top:12px;">
  <div class="section-inner">
    <figure class="post-hero"><img src="{p['hero']}" alt="{p['hero_alt']}" width="1400" height="722" fetchpriority="high"><figcaption class="post-figcap">Şematik kesit: düz yüzeyde sıkışmış kabuk astarı emmez, film tam kalınlıkta kalır. Frezelenen bölgede gözenekli göbek açığa çıkar ve astarı içine çeker; yüzeyde kalan film incelir.</figcaption></figure>
    <div class="post-body" style="margin-top:40px;">
      <p>CNC işlemeli kapaklar ve dekoratif MDF paneller mobilya tasarımında giderek daha fazla tercih ediliyor. Derin kanallar, ince çizgiler ve farklı profiller tasarıma değer katıyor — ama boyama sürecinde bu detayların tamamında aynı yüzey kalitesini tutturmak ayrı bir iş hâline geliyor. Köşelerin ve kenarların astarla yeterince kapanmaması, üretimde ek işlem gerektiren sorunların başında geliyor.</p>

      <h2 class="post-h2">Düz yüzey hazır, köşeler için iş devam ediyor</h2>
      <p>Astar uygulamasının ardından geniş alanlarda istenen dolgunluk elde edilir; buna karşılık kanal kenarlarında ve profil geçişlerinde açıklıklar kalabilir. Bu bölgeleri kapatmak için parçaya yeniden astar uygulanması, tekrar kurumaya bırakılması ve yeniden zımparalanması gerekir.</p>
      <p>Sonuç, üretim planını doğrudan etkiler: <strong>küçük bir köşe detayı, parçanın tamamının son kat aşamasına geçmesini geciktirir.</strong> Üstelik her ek tur yalnızca malzeme tüketimi demek değildir — uygulama, bekleme, zımpara ve kontrol adımlarının hepsi yeniden yaşanır.</p>

      <h2 class="post-h2">Köşede ne oluyor? Frezelenmiş yüzey, düz yüzeyle aynı malzeme değildir</h2>
      <p>Sorunun kaynağı genellikle astarın kalitesi değil, MDF'nin kendi yapısıdır. MDF preslenirken yüzeyde <strong>yoğunluğu yüksek, sıkışmış bir kabuk</strong> oluşur; levhanın göbeği ise bu kabuğa göre <strong>daha düşük yoğunluklu ve daha gözeneklidir</strong>.</p>
      <p>Düz yüzeyde astar bu kapalı kabuğun üstünde durur ve olduğu gibi film oluşturur. Freze bıçağı bir kanal ya da profil açtığında ise kabuk kesilir ve <strong>gözenekli göbek açığa çıkar</strong>. Bu yüzey, düz alana göre belirgin biçimde daha emicidir: uygulanan astarın bir bölümü yüzeyde film oluşturmak yerine malzemenin içine çeker. Aynı tabancadan, aynı turda, aynı gramajla çıkan astar düz alanda yeterliyken kanal kenarında yetersiz kalır.</p>
      <p>Yani köşenin açık kalması bir uygulama hatası değil, iki farklı emiciliğe sahip yüzeyin aynı anda boyanmasının doğal sonucudur.</p>

      <h2 class="post-h2">Daha fazla astar atmak neden çözüm değil?</h2>
      <p>Akla gelen ilk çözüm, köşeleri kapatmak için tüm yüzeye daha fazla astar yüklemektir. Ancak fazla astar <strong>kanallarda birikir ve CNC deseninin belirginliğini azaltır</strong>. Tasarıma değer katması için açılan ince çizgiler yumuşar, derin kanalların keskinliği kaybolur.</p>
      <p>Bunun yanında bir risk daha vardır: kanallarda biriken <strong>kalın katmanlı astar, çatlama ihtimali artan bir film</strong> oluşturur. Yani fazla astar yalnız deseni köreltmekle kalmaz, filmin kendi dayanımını da zayıflatabilir.</p>
      <p>Böylece üretici, köşeleri açık bırakmak ile deseni köreltmek arasında sıkışır: ya köşeler açık kalır ve ikinci tura girilir, ya da desen körelir. İhtiyaç duyulan şey, <strong>detayları korurken köşelerde de yeterli kapatmayı sağlayan</strong> bir astardır.</p>

      <h2 class="post-h2">Köşe kapatma performansı geliştirilmiş astarlar</h2>
      <p>İBAVALRESA olarak, köşe kapatma performansı geliştirilmiş astarlarımızı tam da bu ihtiyaç için sunuyoruz. Bu ürünlerde iki özellik birlikte çalışır:</p>
      <ul>
        <li><strong>Yüksek katı madde oranı</strong> — aynı ıslak film içinde daha fazla katı madde bulunur, dolayısıyla bir bölümü göbeğe çektikten sonra bile yüzeyde yeterli kuru film kalır.</li>
        <li><strong>Tiksotropik yapı</strong> — astar tabancadan çıkarken akıcıdır, yüzeye oturduktan sonra kıvamını geri kazanır. Böylece kanal kenarında aşağı doğru akmaz, bulunduğu yerde durur.</li>
      </ul>
      <p>Bu ikisi bir arada, köşelerde ve profil geçişlerinde düz alanla <strong>dengeli bir kapatma</strong> sağlar — kanalları doldurup deseni köreltmeden.</p>

      <h2 class="post-h2">Üretimde ne değişiyor?</h2>
      <p>Doğru uygulama koşullarında elde edilen bu performansın pratik karşılığı şudur: <strong>zımpara aşamasından sonra, parçayı son kata hazırlamak için CNC köşe bölgelerine yeniden astar uygulamaya gerek kalmaz.</strong> Bunun üretim akışındaki yansımaları:</p>
      <ul>
        <li><strong>Daha az ilave uygulama</strong> — köşelerdeki açıklıkları gidermek için parçaya geri dönme ihtiyacı azalır.</li>
        <li><strong>Daha az ek işçilik</strong> — ilave astara bağlı zımpara ve bölgesel düzeltme işlemleri azalır.</li>
        <li><strong>Daha verimli malzeme kullanımı</strong> — yalnızca köşeleri kapatmak için tüm yüzeye fazladan astar yükleme ihtiyacı sınırlanır.</li>
        <li><strong>Öngörülebilir akış</strong> — parçalar hattı tek turda terk ettiği için son kat planlaması tahmin edilebilir hâle gelir.</li>
      </ul>
      <p>Bu astarlar <a href="https://www.ibavet.com.tr/urunkatalogu/" target="_blank" rel="noopener">İbavet ürün kataloğundaki astar grupları</a> içinde yer alıyor.</p>

      <p class="post-note">Köşe kapatma performansı, astarın yanı sıra uygulama koşullarına da bağlıdır: freze sonrası zımpara kademesi, ortam sıcaklığı ve nem, gramaj ve katlar arası bekleme süresi sonucu doğrudan etkiler. Üretiminizdeki CNC desenlerine ve uygulama koşullarınıza uygun astar seçimi için teknik ekibimizle birlikte çalışın.</p>
    </div>
  </div>
</section>
""" + cta("Astar seçimi ve teknik destek", "CNC desenlerinize uygun astarı birlikte belirleyelim")
POSTS.append(p)

# 5) Mobilyada UV uygulaması
p = dict(yol="blog/mobilyada-uv-boya-uygulamasi.html", etiket="Uygulama Rehberi",
         baslik="Mobilyada UV Boya Uygulaması: Hattan İyi Sonuç Almanın Koşulları",
         h1="Mobilya üretiminde UV boya uygularken nelere dikkat edilmeli?",
         lead="UV sistemler mobilya üretiminde hızlı kürlenme ve yüksek yüzey sertliği sağlar; buna karşılık hattın ayarlarına karşı geleneksel sistemlerden çok daha hassastır. Ar-Ge ve saha ekibimizin notlarından derlediğimiz bu yazıda, UV uygulamalarında sonucu belirleyen parametreleri sıralıyoruz.",
         ozet="Flash-off süresi, lamba seçimi, katlar arası zımpara, kürlenme ve yapışma kontrolü: UV hattında sonucu belirleyen parametreler.",
         desc="Mobilyada UV boya uygulaması: uygulama miktarı ve robot ayarları, flash-off süresi, galyum ve cıva lamba seçimi, katlar arası zımpara, kürlenme ve yapışma kontrolü, derin CNC yüzeyler ve PÜ üzerine UV.",
         tarih_iso="2026-11-05", tarih="5 Kasım 2026",
         hero="/img/blog/mobilyada-uv-boya-uygulamasi.jpg", hero_wh=(1400, 722),
         hero_alt="UV kürlenme tünelinde lambaların altından geçen konveyör hattı",
         og="/img/blog/mobilyada-uv-boya-uygulamasi-og.jpg")
p["govde"] = bas(p) + f"""
<section class="about-section" style="border-top:none; padding-top:12px;">
  <div class="section-inner">
    <figure class="post-hero"><img src="{p['hero']}" alt="{p['hero_alt']}" width="1400" height="722" fetchpriority="high"><figcaption class="post-figcap">UV kürlenme tüneli: film, lambaların altından geçerken saniyeler içinde kürlenir.</figcaption></figure>
    <div class="post-body" style="margin-top:40px;">
      <p>UV boyalarda film, ultraviyole ışık altında saniyeler içinde kürlenir. Bu hız seri üretimde büyük bir avantajdır; ancak aynı hız, hatadan dönmeyi de zorlaştırır. Geleneksel bir sistemde kuruma sırasında kendini toparlayan birçok sorun, UV hattında kürlenmiş film olarak sabitlenir. Bu yüzden UV uygulamasında işin büyük kısmı, lamba altına girmeden önce yapılan hazırlıkta biter.</p>

      <h2 class="post-h2">Uygulama miktarı ve robot ayarları neden ölçülmeli?</h2>
      <p>UV sistemlerde film kalınlığı, hem görünümü hem kürlenmeyi doğrudan belirler. Bu nedenle <strong>her denemede uygulama miktarı g/m² cinsinden ölçülmelidir</strong>; "gözle aynı görünüyor" bir ölçüm değildir ve denemeler arasında karşılaştırma yapmayı imkânsız kılar.</p>
      <ul>
        <li><strong>Püskürtme deseni:</strong> robot kollarının deseni mümkün olduğunca <strong>X şeklinde</strong> ayarlanmalıdır; bu, yüzeye bırakılan boyanın daha eşit dağılmasını sağlar.</li>
        <li><strong>Tabanca açısı:</strong> açı arttıkça yüzeye bırakılan boya miktarı da artar. Açı değişikliği, farkında olunmadan film kalınlığını değiştiren en yaygın etkendir.</li>
        <li><strong>CNC işlenmiş yüzeyler:</strong> düz panelde doğru olan robot açısı, profilli bir yüzeyde doğru olmayabilir. Robot açıları parçanın geometrisine göre revize edilmelidir.</li>
      </ul>

      <h2 class="post-h2">Flash-off süresi neden bu kadar kritik?</h2>
      <p>UV kürlenmeden önce solventin yüzeyden yeterince uzaklaşmış olması gerekir. Film içinde solvent kalmışken lamba altına giren panelde, kürlenme yüzeyi hızla kapatır ve altta kalan solvent çıkış yolu bulamaz. Sonuç yüzeyde görülür:</p>
      <ul>
        <li><strong>Kaynama</strong></li>
        <li><strong>Köpüklenme</strong></li>
        <li>Ve bunlara bağlı diğer <strong>yüzey hataları</strong></li>
      </ul>
      <p>Panelin flash-off bölümünde <strong>en az 5–6 dakika</strong> kalması gerekir. Bu süre, konveyör hızının hat uzunluğuna göre ayarlanmasıyla sağlanır: hat kısaysa hızı artırmak değil, azaltmak gerekir. UV hattında üretim hızını belirleyen asıl kısıt çoğu zaman lamba değil, flash-off bölümüdür.</p>

      <h2 class="post-h2">Hangi lamba ne işe yarar?</h2>
      <p>UV kürlenmede lamba tipi, ışığın hangi dalga boyunda yoğunlaştığını belirler; bu da filmin hangi derinlikte kürlendiğini değiştirir.</p>
      <ul>
        <li><strong>Galyum lambası:</strong> pigmentli ve opak sistemlerde <strong>derin kürlenmeyi</strong> artırır. Pigment ışığı emdiği için, opak bir filmde alt katmanlara ulaşmak en zor kısımdır.</li>
        <li><strong>Cıva lambası:</strong> <strong>yüzey kürlenmesinde</strong> daha etkilidir.</li>
        <li><strong>TL lambalar:</strong> yalnızca mat ürün uygulamalarında kullanılması tavsiye edilir.</li>
      </ul>
      <p>Buradan çıkan sıralama şudur: <strong>opak sistemlerde önce galyum, ardından cıva lambası</strong> kullanılmalıdır — önce derinlik, sonra yüzey. <strong>Şeffaf sistemlerde</strong> ise çoğu uygulamada yalnızca cıva lambası yeterlidir.</p>

      <h2 class="post-h2">Katlar arası zımpara atlanabilir mi?</h2>
      <p>Hayır. <strong>Katlar arasında 400 numara zımpara yapılması önerilir.</strong> Ara zımpara yapılmadan uygulanan ikinci kat, katlar arası <strong>yapışma performansını</strong> önemli ölçüde düşürür. Kürlenmiş UV filmin yüzeyi, üzerine gelen katın tutunabileceği bir doku sunmaz; zımpara bu dokuyu oluşturur.</p>
      <p>Zımparanın ne zaman yapılacağı konusunda ise esneklik vardır: <strong>UV astar ve dolgu ürünlerinin zımparalanabilirliği zamanla önemli ölçüde değişmez.</strong> İlk saatlerde yüzey sertliği bir miktar artsa da, 1 saat sonra ile 1 gün sonra yapılan zımparanın performansının benzer olması beklenir. Yani ara zımpara için hattı beklemeye almak ya da acele etmek gerekmez.</p>

      <h2 class="post-h2">Kürlenme ve yapışma nasıl kontrol edilir?</h2>
      <p>İki basit kontrol, hattan çıkan panelde çoğu sorunu erken yakalar:</p>
      <ol>
        <li><strong>Kürlenme kontrolü:</strong> kürlenme sonrası yüzey hafifçe tırnakla kontrol edilir. Yüzeyde <strong>parlama veya iz oluşuyorsa kürlenme yetersiz</strong> olabilir. Bu durumda panel tekrar UV lambalarından geçirilebilir.</li>
        <li><strong>Yapışma kontrolü:</strong> yapışma testi <strong>panel soğuduktan sonra</strong> yapılmalıdır. Kürlenme tünelinden yeni çıkmış sıcak panelde yapılan test yanıltıcı sonuç verir — sıcakken zayıf görünen bir yapışma, panel soğuduğunda normale dönebilir.</li>
      </ol>

      <h2 class="post-h2">Derin CNC yüzeyler, PÜ üzeri UV ve renklendirilmiş sistemler</h2>
      <p>Standart düz panel dışındaki üç durum ayrı bir yaklaşım ister.</p>
      <p><strong>Derin CNC bölgeleri.</strong> Oyuk ve derin profillerde film kalınlığı doğal olarak artar; bu da tam UV kürlenmesini zorlaştırır. Bu tür uygulamalarda <strong>düşük oranda sertleştirici ile dual kürlenme sistemi</strong> tercih edilebilir: UV'nin ulaşamadığı derinlikte kimyasal kürlenme devreye girer. Gerekli performansa göre ayrıca <strong>UV kürlenme ajanı ilavesi</strong> de değerlendirilebilir.</p>
      <p><strong>PÜ üzerine UV son kat.</strong> Poliüretan boya üzerine UV son kat uygulanabilir; ancak bunun için PÜ boyanın <strong>tamamen kürlenmiş</strong> olması gerekir. Tavsiye edilen bekleme süresi <strong>en az 24 saattir</strong>. Kürlenmesini tamamlamamış bir PÜ katman üzerine UV uygulamak, alttaki filmin çözücü ve ısı etkisiyle hareket etmesine yol açar.</p>
      <p><strong>Renklendirilmiş yüzeyler.</strong> Valtinte gibi renklendiricilerle renklendirilmiş yüzeyler üzerine UV ürün uygulanması, yapışma performansını olumsuz etkileyebilir. Bunun nedeni genellikle pigmentlerin kendisi değil, <strong>UV kürlenme mekanizmasının yüzey üzerindeki etkisidir</strong>. Özellikle <strong>kırmızı pigment</strong> içeren renklerde, kürlenme öncesi ve sonrası renk farkı daha belirgin görülebilir. Bu nedenle renk değerlendirmesi mutlaka <strong>UV kürlenmesi tamamlandıktan ve panel soğuduktan sonra</strong> yapılmalıdır; kürlenmemiş yaş film üzerinden verilen renk onayı yanıltır.</p>

      <h2 class="post-h2">Uygulama ortamı neden hattın bir parçası?</h2>
      <p>Uygulama sırasında veya hat çalışırken üretim alanının süpürülmesi ya da toz oluşturacak işlemler yapılmamalıdır. Havalanan toz UV hattına taşındığında doğrudan yüzey kalitesini düşürür; kürlenmiş film üzerinde bu kusurun telafisi zımpara ve yeniden kat demektir.</p>
      <p class="post-note">Bu notlar genel uygulama prensipleridir; hat konfigürasyonu, lamba gücü, panel geometrisi ve kullanılan ürüne göre değerler değişir. Kendi hattınız için doğru parametreleri belirlemek üzere <a href="/arge.html">Ar-Ge</a> ve teknik ekibimizle birlikte deneme yapabilirsiniz.</p>
    </div>
  </div>
</section>
""" + cta("Hat denemesi ve teknik destek", "UV hattınızın parametrelerini birlikte optimize edelim")
POSTS.append(p)

# 4) Multi surface son kat
p = dict(yol="blog/multi-surface-son-kat-boya.html", etiket="Ürün Teknolojisi",
         baslik="Multi Surface Son Kat: Ahşap, Metal, Alüminyum ve Plastiğe Tek Sistem",
         h1="Çok yüzeyli (multi surface) son kat boya nedir, hangi malzemelerde kullanılır?",
         lead="Valresa'nın akrilik multi surface son kat boyaları; ahşap, metal, alüminyum ve plastik yüzeylerde aynı ürünle çalışabilmek için geliştirildi. İç ve dış mekânda kullanılabilen bu sistemin ne yaptığını, nerede işe yaradığını ve nasıl uygulandığını anlatıyoruz.",
         ozet="Tek son kat ile ahşap, metal, alüminyum ve plastik: çok yüzeyli akrilik sistem ne zaman avantaj sağlar, nasıl uygulanır?",
         desc="Valresa multi surface akrilik son kat boya: ahşap, metal, alüminyum ve plastik yüzeylerde yüksek örtücülük, sararmaya karşı direnç ve dış mekân dayanımı. Tabanca, airmix, fırça ve rulo ile uygulanır.",
         tarih_iso="2026-11-03", tarih="3 Kasım 2026",
         hero="/img/blog/multi-surface-son-kat-boya.jpg", hero_wh=(1400, 722),
         hero_alt="Plastik, ahşap, metal ve alüminyum sandalyeler aynı multi surface son kat boyayla boyanmış",
         og="/img/blog/multi-surface-son-kat-boya-og.jpg")
p["govde"] = bas(p) + f"""
<section class="about-section" style="border-top:none; padding-top:12px;">
  <div class="section-inner">
    <figure class="post-hero"><img src="{p['hero']}" alt="{p['hero_alt']}" width="1400" height="722" fetchpriority="high"><figcaption class="post-figcap">Fuar sunumumuzdan: plastik, ahşap, metal ve alüminyum sandalyeler aynı multi surface son katla boyandı.</figcaption></figure>
    <div class="post-body" style="margin-top:40px;">
      <h2 class="post-h2">Çok yüzeyli son kat ne demek?</h2>
      <p>Boyada alışılmış düzen, her malzemenin kendi sistemini istemesidir: ahşaba bir astar, metale başka bir astar, alüminyuma ayrı bir tutunma primeri, plastiğe bir başkası. Bir mobilya ya da mekân birden fazla malzemeden oluştuğunda bu düzen hızla büyür — <strong>birkaç farklı ürün, birkaç farklı stok kalemi ve her malzemede ayrı bir uygulama prosedürü</strong>.</p>
      <p>Çok yüzeyli (multi surface) son kat bu noktada devreye girer. Temel vaadi tek cümleyle şudur: <strong>farklı türde alt zeminlere tutunabilen tek bir son kat</strong>. Fuarda yaptığımız sunumda bunu dört sandalye üzerinden gösterdik — plastik, ahşap, metal ve alüminyum. Dördü de aynı son katla boyandı; sonuçta malzemeler değil, ortak bir yüzey görünüyor.</p>

      <h2 class="post-h2">Hangi yüzeylerde kullanılıyor?</h2>
      <p>Ürün, farklı türdeki alt zeminlere tutunacak şekilde formüle edilmiştir. Uygulamada en sık karşılaşılan malzemeler:</p>
      <ul>
        <li><strong>Ahşap ve ahşap esaslı paneller</strong></li>
        <li><strong>Metal</strong> — demir ve çelik aksam</li>
        <li><strong>Alüminyum</strong></li>
        <li><strong>Plastik</strong></li>
      </ul>
      <p>Bu, özellikle karma malzemeli ürünlerde fark yaratır: ahşap oturma yüzeyi ile metal ayakların aynı tonda olması gereken bir sandalye, alüminyum çerçeveli ahşap bir panel ya da plastik ve metal parçaların bir arada bulunduğu bir mobilya grubunda renk ve parlaklık bütünlüğü tek üründen gelir.</p>

      <h2 class="post-h2">İç mekânda da dış mekânda da kullanılabilir mi?</h2>
      <p>Evet; ürün hem iç hem dış mekân uygulamaları için tanımlanmıştır. Dış mekânda belirleyici olan iki özellik şunlardır:</p>
      <ul>
        <li><strong>Sararmaya karşı direnç:</strong> özellikle beyaz ve açık tonlarda, zamanla oluşan sarı kaymayı geciktirir. Açık renkli dış mekân mobilyasında rengin ilk günkü gibi kalması büyük ölçüde bu özelliğe bağlıdır.</li>
        <li><strong>Dış ortam dayanımı:</strong> güneş, nem ve sıcaklık değişimlerine açık yüzeylerde kullanım için formüle edilmiştir.</li>
      </ul>
      <p>Teknik föyde öne çıkan kullanım alanları bahçe mobilyası, panjur ve jaluziler ile dış mekân metal kapılardır. İç mekânda ise malzeme karışımının yoğun olduğu her mobilya ve doğrama uygulaması için uygundur.</p>

      <h2 class="post-h2">Renk nasıl elde ediliyor?</h2>
      <p>Sistemin çıkış noktası, <strong>beyaz mat baz son kat</strong>tır; bu ürün doğrudan kullanılabildiği gibi, renklendirilmiş son katların hazırlanmasında <strong>baz</strong> olarak da kullanılır. Yüksek örtücülüğü sayesinde koyu ya da alacalı zeminlerde daha az katla kapatma sağlar — karma malzemeli bir üründe farklı alt zeminlerin aynı tonda görünmesi için bu önemlidir.</p>
      <p>İstenen renk, standart kartela referanslarıyla hazırlanabilir. Renk kodları ve kartelalar için <a href="/renk-paleti.html">Renk Paleti</a> sayfamıza, partiden partiye renk tutarlılığının nasıl sağlandığı için <a href="/renk-makinesi.html">renk makinesi</a> sistemlerimize bakabilirsiniz.</p>

      <h2 class="post-h2">Nasıl uygulanır?</h2>
      <p>Ürün iki bileşenlidir. İBAVALRESA olarak kendi teknik föyümüzü hazırladık; karışım <strong>190069 kodlu sertleştirici ile 6+1 oranında</strong> yapılır. Uygulama yöntemi atölyeye göre seçilebilir:</p>
      <ul>
        <li><strong>Tabanca</strong> ile püskürtme</li>
        <li><strong>Airmix / mikser</strong> ile seri uygulama</li>
        <li><strong>Fırça ve rulo</strong> ile el uygulaması</li>
      </ul>
      <p>Fırça ve rulonun da seçenek olması, sahada yerinde yapılan işlerde ya da küçük partilerde tabanca kurulumuna gerek bırakmaz.</p>
      <p>İncelticiyi ortam koşuluna göre seçmek sonucu doğrudan etkiler:</p>
      <ol>
        <li><strong>Standart koşullarda</strong> 510102 kodlu inceltici kullanılır.</li>
        <li><strong>Yaz aylarında ve fırça uygulamasında</strong> yavaş inceltici tercih edilir; yüzeyin işlenebilir kaldığı süreyi uzatır.</li>
        <li><strong>Yüksek sıcaklık veya yüksek nemde</strong> 540414 kullanılır. Bu inceltici <em>anti-blushing</em> özelliğiyle, nemli havada filmin içinde oluşan sisli-beyazımsı görünümü (blushing) engeller.</li>
      </ol>
      <p class="post-note">Çok yüzeyli bir son kat, yüzey hazırlığını ortadan kaldırmaz: her malzeme kendi temizlik, yağ alma ve zımpara gereksinimiyle gelir — özellikle alüminyum ve plastikte. Projenizdeki malzemeler için doğru hazırlık ve sistem kurgusunu teknik föy ve teknik ekibimizle birlikte netleştirin.</p>
    </div>
  </div>
</section>
""" + cta("Numune ve teknik destek", "Projenizdeki yüzeyler için doğru sistemi birlikte seçelim")
POSTS.append(p)

# 3) Yanma geciktirici sistem
p = dict(yol="blog/yanma-geciktirici-ahsap-boya-vernik.html", etiket="Yangın Güvenliği",
         baslik="Yanma Geciktirici Mobilya Boya ve Vernikleri",
         h1="Yanma geciktirici mobilya boya ve vernikleri nedir, nasıl çalışır?",
         lead="Valresa Yanma Geciktirici Sistem; iç mekân ahşap yüzeylerde yangının ilerleme hızını azaltan, akrilik esaslı bir ürün grubudur. Sistemin ne yaptığını, akrilik esaslı olmasının ne anlama geldiğini ve uygulamada nelere dikkat edilmesi gerektiğini anlatıyoruz.",
         ozet="İç mekân ahşabında alevin yayılmasını geciktiren akrilik esaslı sistem: ne yapar, neyi vaat etmez, hangi ürünleri kapsar?",
         desc="Valresa Yanma Geciktirici Sistem: iç mekân ahşap yüzeyler için akrilik esaslı dolgu, astar, vernik ve boya. Yangının ilerleme hızını azaltır, damlama yapmaz, kimyasal salınımı düşüktür.",
         tarih_iso="2026-11-01", tarih="1 Kasım 2026",
         hero="/img/blog/yanma-geciktirici-ahsap-boya-vernik.jpg", hero_wh=(1400, 722),
         hero_alt="Valresa yanma geciktirici ahşap boya ve vernik sistemi",
         og="/img/blog/yanma-geciktirici-ahsap-boya-vernik-og.jpg")
p["govde"] = bas(p) + f"""
<section class="about-section" style="border-top:none; padding-top:12px;">
  <div class="section-inner">
    <figure class="post-hero"><img src="{p['hero']}" alt="{p['hero_alt']}" width="1400" height="722" fetchpriority="high"><figcaption class="post-figcap">Valresa Yanma Geciktirici Sistem — iç mekân ahşap yüzeyler için akrilik esaslı ürün grubu.</figcaption></figure>
    <div class="post-body" style="margin-top:40px;">
      <h2 class="post-h2">Yanma geciktirici kaplama ne yapar?</h2>
      <p>Ahşap yanıcı bir malzemedir ve hiçbir kaplama bunu değiştirmez. Yanma geciktirici bir sistemin işi, ahşabı yanmaz hâle getirmek değil, <strong>alevin yüzeyde yayılma hızını düşürmektir</strong>. Bir yangında en kritik şey ilk dakikalardır; bu dakikalar tahliye için kazanılan zamandır. Yanma geciktirici kaplamanın sağladığı asıl fayda budur.</p>
      <p>Valresa Yanma Geciktirici Sistem, iç mekân ahşap yüzeylerde üç noktada çalışır:</p>
      <ul>
        <li><strong>Alev yayılımını yavaşlatır:</strong> yangının yüzey boyunca ilerleme hızını azaltır.</li>
        <li><strong>Damlama yapmaz:</strong> yanan damlacıklar yangını alt yüzeylere ve komşu malzemelere taşır. Damlama davranışı, Avrupa yangın sınıflandırmasında parlama ve duman kadar ayrı bir ölçüt olarak değerlendirilir.</li>
        <li><strong>Zararlı kimyasal salınımı düşüktür:</strong> hem normal kullanımda hem de uygulama sırasında iç mekân için önemlidir.</li>
      </ul>

      <h2 class="post-h2">Akrilik esaslı olması ne anlama geliyor?</h2>
      <p>Bu ürün grubunu kategorideki yaygın alternatiflerden ayıran en belirgin özellik, <strong>akrilik esaslı</strong> olmasıdır. Yanma geciktirici kaplamalar çoğunlukla başka kimyasal sistemler üzerine kurulur; akrilik kimyası ise düşük salınım hedefiyle birlikte çalışmayı kolaylaştırır.</p>
      <p>Pratik karşılığı şu: yangın performansı için iç mekân hava kalitesinden ödün vermek gerekmez. Okul, otel, hastane, ofis gibi insanların uzun süre bulunduğu kapalı alanlarda bu iki gereksinim çoğu zaman birlikte aranır.</p>

      <h2 class="post-h2">Sistem hangi ürünleri kapsıyor?</h2>
      <p>Ürün grubu, bir ahşap yüzeyin baştan sona kaplanabilmesi için gereken dört katmanı da içerir:</p>
      <ul>
        <li><strong>Dolgu</strong></li>
        <li><strong>Astar</strong></li>
        <li><strong>Vernik</strong> — 10 gloss'tan 80 gloss'a kadar</li>
        <li><strong>Boya</strong> — 10 gloss'tan 60 gloss'a kadar</li>
      </ul>
      <p>Parlaklık aralığının genişliği, yangın performansı için tasarım tercihinden vazgeçmek gerekmediği anlamına gelir: tam mat bir yüzey de, yüksek parlak bir yüzey de aynı sistem içinde elde edilebilir. <strong>Ürünlerin tamamında karışım oranı 20/1'dir.</strong></p>
      <p>Ürün grubu Avrupa sertifikasyon sistemine dâhildir.</p>

      <h2 class="post-h2">Uygulamada nelere dikkat edilmeli?</h2>
      <p>Yanma geciktirici kaplamalarda performans, ürünün kendisi kadar nasıl uygulandığına bağlıdır. Normal bir boyada bir miktar sapma yalnızca görünümü etkilerken, burada doğrudan yangın davranışını etkiler.</p>
      <ol>
        <li><strong>Karışım oranını birebir tutun.</strong> Tüm ürünlerde oran 20/1'dir; göz kararı hazırlanan karışım beklenen performansı vermez.</li>
        <li><strong>Teknik föyde belirtilen sarfiyata uyun.</strong> Yanma geciktirici etki belirli bir film kalınlığında tanımlanır; eksik uygulanan kat, sistemi tanımlandığı performansın dışına çıkarır.</li>
        <li><strong>Sistemi bütün olarak uygulayın.</strong> Astar, dolgu ve son katın birlikte çalışması esastır; katmanlardan birini başka bir üründen seçmek sistemin bütünlüğünü bozar.</li>
        <li><strong>Yüzeyi hazırlayın.</strong> Tozsuz, kuru ve uygun şekilde zımparalanmış bir zemin, katların beklenen kalınlıkta ve tutunmada olmasını sağlar.</li>
      </ol>

      <h2 class="post-h2">Nerelerde kullanılır?</h2>
      <p>Sistem iç mekân ahşap yüzeyler için geliştirilmiştir: mobilya, duvar ve tavan kaplamaları, paneller, ahşap doğrama ve ahşap detaylar. En sık ihtiyaç duyulduğu yerler, yangın yönetmeliklerinin yüzey malzemelerine koşul getirdiği toplu kullanım alanlarıdır — oteller, okullar, hastaneler, ofisler, alışveriş merkezleri ve toplantı salonları.</p>
      <p class="post-note">Yanma geciktirici kaplamaların performansı; uygulanan sistem, film kalınlığı ve alt zemine göre değişir. Projenizde belirli bir yangın sınıfı talep ediliyorsa, hangi sistemin ve hangi uygulama koşullarının bu sınıfı karşıladığını teknik ekibimizle birlikte netleştirin.</p>
    </div>
  </div>
</section>
""" + cta("Teknik destek", "Projenizin yangın performansı gereksinimini birlikte değerlendirelim")
POSTS.append(p)

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
