#!/usr/bin/env python3
"""İBAVALRESA — Rusça ve İspanyolca tek sayfa tanıtım (ru/index.html, es/index.html).

Bu iki dil için tam site yerine tek sayfa: kısa tanıtım, rakamlar, markalar,
firma sunumu bağlantısı ve iletişim (telefon, e-posta, WhatsApp, form).
Metinler aşağıdaki DIL sözlüğünde; sayfaları elle düzenleme, buradan üret:
    python3 tools/dil_sayfasi_uret.py
"""
import html, json, os, re

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.ibavalresa.com.tr"
nav_v = re.search(r'/js/nav-line\.js\?v=([0-9a-f]+)', open(os.path.join(KOK, "index.html"), encoding="utf-8").read()).group(1)
base_v = re.search(r'/css/base\.css\?v=([0-9a-f]+)', open(os.path.join(KOK, "index.html"), encoding="utf-8").read()).group(1)

TEL, TEL_HREF = "+90 312 267 56 22", "+903122675622"
WA, WA_HREF = "+90 533 081 25 25", "https://wa.me/905330812525"
MAIL = "info@ibavalresa.com.tr"

DIL = {
 "ru": dict(
  html_lang="ru", og_locale="ru_RU",
  title="IBAVALRESA — производитель покрытий для дерева, мебели и промышленности (Турция)",
  desc="IBAVALRESA — производитель покрытий для дерева, мебели и промышленности из Турции: акриловые, ПУ, полиэфирные, водные и УФ-системы. 60+ лет, 25+ стран.",
  badge="Турецко-испанское партнёрство",
  h1="Покрытия для дерева и общепромышленные покрытия",
  h1_sub="<em>Индивидуальные серии и решения</em> под ваши задачи.",
  lead="IBAVALRESA — турецкий производитель лакокрасочных материалов. Для дерева и мебели мы выпускаем акриловые, полиуретановые, полиэфирные, нитроцеллюлозные, эпоксидные, водные и УФ-отверждаемые системы — в сериях премиум-класса и с оптимальным соотношением цены и качества, а для промышленного сегмента — краски и лаки с оптимальным соотношением цены и качества. Мы работаем на внутреннем рынке и на экспорт.",
  stats=[("60+", "лет опыта"), ("25+", "стран экспорта"), ("30 000", "тонн в год — производственная мощность"), ("50%", "доля экспорта в общем объёме продаж")],
  about_tag="О компании", about_h2="Производитель покрытий для дерева, мебели и промышленности в Турции",
  about=["Благодаря производственному и научно-исследовательскому потенциалу, рождённому турецко-испанским партнёрством, мы поставляем на мировые рынки высококачественные покрытия для дерева, мебельные лаки и решения для промышленной окраски.",
         "IBAVALRESA объединяет опыт <strong>IBA Kimya</strong> (Анкара, 1977) и <strong>Valresa</strong> (Валенсия, 1965). Партнёрство создано в 2005 году, а в 2007 году в Анкаре (Синджан) был запущен современный завод.",
         "Производственная площадка площадью <strong>37 000 м²</strong> и мощностью <strong>30 000 тонн в год</strong> работает с полной прослеживаемостью процессов (SAP, SCADA) и сертифицирована по ISO 9001. Более 100 колеровочных машин в Турции и за рубежом обеспечивают одинаковый цвет в каждой точке."],
  cat_tag="Каталоги продукции", cat_h2="Каталоги наших брендов", cat_open="Открыть каталог",
  cat_desc=("Мебельные краски и лаки премиум-класса", "Водные краски и лаки для дерева", "Мебельные краски и лаки с оптимальным соотношением цены и качества", "Общепромышленные краски"),
  deck_badge="Презентация компании", deck_title="Познакомьтесь с IBAVALRESA подробнее",
  deck_btn="Открыть презентацию",
  contact_tag="Контакты", contact_h2="Свяжитесь с нашим экспортным отделом",
  contact_sub="Заполните форму по вопросам продукции, дистрибуции и сотрудничества — наша команда свяжется с вами в ближайшее время.",
  exp_eyebrow="Экспорт", exp_title="Международные продажи и экспорт",
  l_phone="Телефон", l_mail="E-mail", l_wa="WhatsApp", l_addr="Адрес",
  addr="Oğuz cd. No:24, 1. OSB, Sincan / Анкара, Турция",
  f_name="Имя и фамилия", f_company="Компания", f_country="Страна", f_email="E-mail", f_phone="Телефон", f_msg="Сообщение",
  f_msg_ph="Чем мы можем помочь?", f_consent='Я согласен(на) на обработку моих данных для ответа на запрос (<a href="/kvkk-aydinlatma-metni.html" target="_blank" rel="noopener">политика конфиденциальности, на турецком</a>).',
  f_send="Отправить", ok="Спасибо! Ваше сообщение получено, мы скоро с вами свяжемся.",
  err="Не удалось отправить сообщение. Пожалуйста, напишите на info@ibavalresa.com.tr.",
  subject="İbavalresa — RU sayfası mesajı",
  slogan=("Надёжность.", "Эффективность.", "Качество."),
  slogan_btn="Связаться с нами",
  slogan_p="Мы — надёжный партнёр в области покрытий для дерева, мебели и промышленности на мировых рынках.",
  rights="© 2026 IBAVALRESA. Все права защищены.", other="Сайт на других языках",
 ),
 "es": dict(
  html_lang="es", og_locale="es_ES",
  title="IBAVALRESA — fabricante de pinturas para madera, mueble e industria (Turquía)",
  desc="IBAVALRESA, fabricante turco de pinturas para madera, mueble e industria: sistemas acrílicos, PU, poliéster, al agua y UV. Más de 60 años y 25 países.",
  badge="Alianza turco-española",
  h1="Pinturas para madera y recubrimientos industriales generales",
  h1_sub="<em>Series y soluciones personalizadas</em> para sus necesidades.",
  lead="IBAVALRESA es un fabricante de pinturas y barnices con sede en Turquía. Para madera y mueble producimos sistemas acrílicos, de poliuretano, poliéster, nitrocelulósicos, epoxi, al agua y de curado UV, en series de máxima calidad y con una excelente relación calidad-precio; para el segmento industrial, pinturas y barnices con una excelente relación calidad-precio. Trabajamos para el mercado nacional y la exportación.",
  stats=[("60+", "años de experiencia"), ("25+", "países de exportación"), ("30.000", "toneladas/año de capacidad"), ("50 %", "de las ventas totales es exportación")],
  about_tag="Quiénes somos", about_h2="Fabricante de pinturas para madera, mueble e industria en Turquía",
  about=["Con la capacidad de producción y de I+D nacida de nuestra alianza turco-española, ofrecemos a los mercados internacionales pinturas para madera, barnices para muebles y soluciones de recubrimiento industrial de alta calidad.",
         "IBAVALRESA une la experiencia de <strong>IBA Kimya</strong> (Ankara, 1977) y de <strong>Valresa</strong> (Valencia, 1965). La alianza nació en 2005 y en 2007 se puso en marcha una moderna planta de producción en Ankara (Sincan).",
         "Nuestras instalaciones de <strong>37.000 m²</strong>, con una capacidad de <strong>30.000 toneladas al año</strong>, trabajan con trazabilidad completa (SAP, SCADA) y cuentan con la certificación ISO 9001. Más de 100 máquinas tintométricas en Turquía y en el extranjero garantizan el mismo color en cada punto."],
  cat_tag="Catálogos de productos", cat_h2="Catálogos de nuestras marcas", cat_open="Ver catálogo",
  cat_desc=("Pinturas y barnices para muebles de gama alta", "Pinturas y barnices al agua para madera", "Pinturas y barnices para muebles con buena relación calidad-precio", "Pinturas para la industria general"),
  deck_badge="Presentación corporativa", deck_title="Conozca IBAVALRESA más de cerca",
  deck_btn="Ver la presentación",
  contact_tag="Contacto", contact_h2="Contacte con nuestro departamento de exportación",
  contact_sub="Rellene el formulario sobre productos, distribución y colaboraciones y nuestro equipo se pondrá en contacto con usted lo antes posible.",
  exp_eyebrow="Exportación", exp_title="Ventas internacionales y exportación",
  l_phone="Teléfono", l_mail="Correo electrónico", l_wa="WhatsApp", l_addr="Dirección",
  addr="Oğuz cd. No:24, 1. OSB, Sincan / Ankara, Turquía",
  f_name="Nombre y apellidos", f_company="Empresa", f_country="País", f_email="Correo electrónico", f_phone="Teléfono", f_msg="Mensaje",
  f_msg_ph="¿En qué podemos ayudarle?", f_consent='Acepto el tratamiento de mis datos para responder a mi consulta (<a href="/kvkk-aydinlatma-metni.html" target="_blank" rel="noopener">aviso de privacidad, en turco</a>).',
  f_send="Enviar", ok="¡Gracias! Hemos recibido su mensaje y le responderemos en breve.",
  err="No se ha podido enviar el mensaje. Escríbanos a info@ibavalresa.com.tr.",
  subject="İbavalresa — ES sayfası mesajı",
  slogan=("Fiabilidad.", "Eficiencia.", "Calidad."),
  slogan_btn="Contactar",
  slogan_p="Somos su socio de confianza en pinturas para madera, mueble e industria en los mercados internacionales.",
  rights="© 2026 IBAVALRESA. Todos los derechos reservados.", other="El sitio en otros idiomas",
 ),
}

HREFLANG = [("tr", "/"), ("en", "/en/"), ("ru", "/ru/"), ("es", "/es/")]
DILLER = [("TR", "/", "🇹🇷"), ("EN", "/en/", "🇬🇧"), ("RU", "/ru/", "🇷🇺"), ("ES", "/es/", "🇪🇸")]
ARROW = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>'
KATALOG = [("Valresa", "https://www.valresa.com.tr/urunkatalogu/", "valresa-katalog.jpg", 339, 480),
           ("Esfera", "https://esfera.com.tr/urun-katalogu/", "esfera-katalog.jpg", 339, 480),
           ("Ibavet", "https://www.ibavet.com.tr/urunkatalogu/", "ibavet-katalog.jpg", 339, 480),
           ("Iba Sanayi Boyaları", "http://www.ibasanayiboyalari.com/Sanayi-Boyalari-urun-katalogu.pdf", "iba-sanayi-katalog.jpg", 452, 639)]
OUT = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17 17 7M8 7h9v9"/></svg>'

CSS = """
.lp-nav .nav-inner { justify-content: space-between; }
.lp-langs { display: flex; gap: 4px; }
.lp-langs a { font-size: 13px; font-weight: 600; color: var(--text2); text-decoration: none; padding: 6px 10px; border-radius: 7px; border: 1px solid transparent; }
.lp-langs a:hover { background: rgba(0,0,0,.04); color: var(--text); }
.lp-langs a.on { border-color: var(--border); color: var(--text); }
.lp-hero { padding: 140px 0 40px; }
.lp-badge { display: inline-block; padding: 5px 12px; border: 1px solid rgba(38,53,140,.35); border-radius: 999px; font-size: 11px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--accent); }
.lp-h1 { font-size: clamp(32px, 4.6vw, 54px); font-weight: 800; letter-spacing: -1.6px; line-height: 1.06; margin: 20px 0 12px; max-width: 820px; text-wrap: balance; }
.lp-lead { font-size: clamp(16px, 1.5vw, 19px); line-height: 1.65; color: var(--text2); max-width: 760px; }
.lp-stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 2px; background: var(--border); border: 1px solid var(--border); border-radius: 14px; overflow: hidden; margin-top: 44px; }
.lp-stat { background: var(--bg); padding: 26px 22px; }
.lp-stat b { display: block; font-size: clamp(28px, 3vw, 40px); font-weight: 800; letter-spacing: -1.5px; line-height: 1; color: var(--text); }
.lp-stat span { display: block; font-size: 13.5px; color: var(--text2); margin-top: 8px; line-height: 1.4; }
.lp-sec { padding: 56px 0; border-top: 1px solid var(--border); }
.lp-tag { display: inline-flex; align-items: center; gap: 8px; font-size: 12px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--accent); margin-bottom: 16px; }
.lp-tag::before { content: ""; width: 22px; height: 1px; background: var(--accent); opacity: .5; }
.lp-contact { display: grid; grid-template-columns: .85fr 1.15fr; border: 1px solid var(--border); border-radius: 18px; overflow: hidden; margin-top: 32px; }
.lp-aside { background: #0d0d10; color: #fff; padding: 40px 36px; display: flex; flex-direction: column; gap: 22px; }
.lp-aside dt { font-size: 11px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--gualda); margin-bottom: 4px; }
.lp-aside dd { font-size: 15.5px; color: rgba(240,239,244,.88); line-height: 1.5; }
.lp-aside a { color: #fff; text-decoration: none; border-bottom: 1px solid rgba(255,255,255,.25); }
.lp-aside a:hover { border-bottom-color: var(--gualda); }
.lp-form { padding: 36px 36px 32px; background: #fff; }
.lp-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px 16px; }
.lp-field { display: flex; flex-direction: column; gap: 6px; }
.lp-field.full { grid-column: 1 / -1; }
.lp-field label { font-size: 12px; font-weight: 600; color: var(--text2); }
.lp-field label span { color: var(--accent); }
.lp-field input, .lp-field textarea { font-family: var(--font); font-size: 14px; color: var(--text); background: #fafafb; border: 1px solid var(--border); border-radius: 9px; padding: 11px 13px; }
.lp-field textarea { min-height: 110px; resize: vertical; }
.lp-field input:focus, .lp-field textarea:focus { outline: none; border-color: var(--accent); background: #fff; box-shadow: 0 0 0 3px var(--accent-dim); }
.lp-consent { display: flex; gap: 10px; align-items: flex-start; margin-top: 16px; font-size: 12.5px; line-height: 1.55; color: var(--text2); }
.lp-consent input { margin-top: 2px; width: 16px; height: 16px; accent-color: var(--accent); flex-shrink: 0; }
.lp-consent a { color: var(--accent); }
.lp-actions { display: flex; align-items: center; gap: 16px; margin-top: 20px; flex-wrap: wrap; }
.lp-status { font-size: 13.5px; font-weight: 600; color: #1b7a50; opacity: 0; transition: opacity .25s; }
.lp-status.show { opacity: 1; } .lp-status.error { color: #c0392b; }
.lp-status:not(.error)::before { content: "\\2713\\00a0"; }
/* Ana sayfadaki .finalcta ile aynı ölçüler */
.lp-slogan { padding: 64px 0 56px; border-top: 1px solid var(--border); }
.lp-slogan p { font-size: 17px; max-width: 460px; margin: 0 auto 28px; }
#contact { scroll-margin-top: 70px; }
.lp-cats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 28px; margin-top: 8px; }
.lp-cat { display: flex; flex-direction: column; gap: 6px; text-decoration: none; color: var(--text); }
.lp-cat img { display: block; width: 100%; height: auto; aspect-ratio: 339 / 480; object-fit: cover; border-radius: 6px; margin-bottom: 12px;
  box-shadow: 0 1px 2px rgba(0,0,0,.06), 0 10px 26px rgba(13,13,16,.12); transition: transform .35s cubic-bezier(.22,.68,0,1), box-shadow .35s; }
.lp-cat:hover img { transform: translateY(-5px); box-shadow: 0 1px 2px rgba(0,0,0,.06), 0 22px 44px rgba(13,13,16,.18); }
.lp-cat b { font-size: 16px; font-weight: 700; letter-spacing: -.2px; }
.lp-cat span { font-size: 13.5px; color: var(--text2); line-height: 1.45; }
.lp-cat em { font-style: normal; display: inline-flex; align-items: center; gap: 5px; font-size: 13.5px; font-weight: 600; color: var(--accent); margin-top: 4px; }
@media (max-width: 900px) { .lp-cats { grid-template-columns: 1fr 1fr; gap: 28px 20px; } }
.lp-foot { background: #0d0d10; color: #9997a8; padding: 32px 40px; font-size: 13px; }
.lp-foot-in { max-width: 1100px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; gap: 20px; flex-wrap: wrap; }
.lp-foot img { height: 26px; width: auto; display: block; opacity: .85; }
.lp-foot a { color: #f0eff4; text-decoration: none; margin-left: 12px; }

/* Alıntı bloğu (markalar/arge sayfalarındaki .about-pull) */
.lp-deck { margin-top: 48px; }
.lp-sec .about-pull:only-child { margin: 0; }
.about-pull { margin: 48px 0 0; padding: 40px 40px; border-left: 3px solid var(--accent);
  background: linear-gradient(135deg, rgba(38,53,140,0.04) 0%, rgba(38,53,140,0) 100%); border-radius: 0 14px 14px 0; }
/* İhracat sorumlusu kartı (bolge-mudurlukleri.html ile aynı) */
.region-links { display: flex; flex-direction: column; gap: 10px; }
.region-link { display: flex; align-items: center; gap: 10px; font-size: 14px; color: var(--text2); text-decoration: none; transition: color .2s; }
.region-link svg { width: 16px; height: 16px; color: var(--accent); flex-shrink: 0; }
.region-link:hover { color: var(--accent); }
.export-bar { display: flex; align-items: center; justify-content: space-between; gap: 24px; flex-wrap: wrap; border: 1px solid rgba(38,53,140,0.18); background: #f4f5fb; border-radius: 14px; padding: 22px 28px; margin-top: 28px; }
.export-head { display: flex; align-items: center; gap: 18px; }
.export-icon { flex-shrink: 0; width: 46px; height: 46px; border-radius: 12px; display: flex; align-items: center; justify-content: center; background: var(--accent); color: #fff; }
.export-icon svg { width: 24px; height: 24px; }
.export-eyebrow { font-size: 11px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: var(--accent); margin-bottom: 4px; }
.export-title { font-size: 18px; font-weight: 700; letter-spacing: -.4px; color: var(--text); }
.export-info { display: flex; align-items: center; gap: 28px; flex-wrap: wrap; }
.export-person { font-size: 15px; font-weight: 600; color: var(--text); }
.export-bar .region-links { flex-direction: row; gap: 22px; }
@media (max-width: 680px) {
  .export-bar { flex-direction: column; align-items: flex-start; gap: 18px; padding: 22px 20px; }
  .export-info { flex-direction: column; align-items: flex-start; gap: 12px; width: 100%; }
  .export-bar .region-links { flex-direction: column; gap: 12px; }
  .about-pull { padding: 28px 22px; }
}
@media (max-width: 900px) { .lp-stats { grid-template-columns: 1fr 1fr; } .lp-contact { grid-template-columns: 1fr; } }
@media (max-width: 600px) { .lp-grid { grid-template-columns: 1fr; } .lp-aside, .lp-form { padding: 28px 22px; } .lp-hero { padding-top: 110px; } }
"""

def sayfa(kod, t):
    e = html.escape
    url = f"{SITE}/{kod}/"
    hreflang = "".join(f'<link rel="alternate" hreflang="{h}" href="{SITE}{p}">\n' for h, p in HREFLANG) + f'<link rel="alternate" hreflang="x-default" href="{SITE}/">\n'
    org = {"@context": "https://schema.org", "@type": "Organization", "name": "IBAVALRESA", "url": SITE + "/",
           "logo": SITE + "/assets/logos/ibavalresa-black.png", "telephone": TEL, "email": MAIL,
           "address": {"@type": "PostalAddress", "streetAddress": "Oğuz cd. No:24, 1. OSB", "addressLocality": "Sincan", "addressRegion": "Ankara", "addressCountry": "TR"}}
    aktif = ' class="on" aria-current="page"'
    langs = "".join(f'<a href="{p}" hreflang="{k.lower()}"{aktif if k.lower() == kod else ""}>{k}</a>' for k, p, _ in DILLER)
    stats = "".join(f'<div class="lp-stat"><b>{n}</b><span>{l}</span></div>' for n, l in t["stats"])
    about = "".join(f'<p class="about-p">{p}</p>' for p in t["about"])
    kat = "".join(f'<a class="lp-cat" href="{u}" target="_blank" rel="noopener"><img src="/img/katalog/{img}" alt="{n} — {e(d)}" width="{w}" height="{h}" loading="lazy"><b>{n}</b><span>{e(d)}</span><em>{t["cat_open"]} {OUT}</em></a>'
                  for (n, u, img, w, h), d in zip(KATALOG, t["cat_desc"]))
    req = '<span>*</span>'
    out = f"""<!DOCTYPE html>
<html lang="{t['html_lang']}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(t['title'])}</title>
<link rel="canonical" href="{url}">
{hreflang}<meta name="description" content="{e(t['desc'])}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="IBAVALRESA">
<meta property="og:locale" content="{t['og_locale']}">
<meta property="og:title" content="{e(t['title'])}">
<meta property="og:description" content="{e(t['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/img/kampus-havadan.jpg">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps(org, ensure_ascii=False)}</script>
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="192x192" href="/assets/favicon/favicon-192x192.png">
<link rel="apple-touch-icon" href="/assets/favicon/apple-touch-icon.png">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/base.css?v={base_v}">
<script src="/js/nav-line.js?v={nav_v}" defer></script>
<style>{CSS}</style>
</head>
<body>

<nav class="lp-nav">
  <div class="nav-inner">
    <a href="/{kod}/" class="nav-logo"><img src="/assets/logos/ibavalresa-white.png" alt="ibavalresa" class="nav-logo-img" style="filter:brightness(0);" width="242" height="50"></a>
    <div class="lp-langs" aria-label="{e(t['other'])}">{langs}</div>
  </div>
</nav>

<section class="lp-hero">
  <div class="section-inner">
    <span class="lp-badge">{t['badge']}</span>
    <h1 class="lp-h1">{t['h1']}</h1>
    <p class="lp-lead">{t['lead']}</p>
    <div class="lp-stats">{stats}</div>
  </div>
</section>

<section class="lp-sec">
  <div class="section-inner">
    <div class="about-grid-2">
      <div><div class="lp-tag">{t['about_tag']}</div><h2 class="about-h2">{t['about_h2']}</h2></div>
      <div>{about}</div>
    </div>
    <div class="lp-deck">
    <a class="deck-banner" href="/sunum.html?lang={kod}" target="_blank" rel="noopener nofollow">
      <div>
        <span class="deck-banner-badge">{t['deck_badge']}</span>
        <h2 class="deck-banner-title">{t['deck_title']}</h2>
        <div class="deck-banner-cta">
          <span class="deck-banner-btn"><span>{t['deck_btn']}</span> <span aria-hidden="true">→</span></span>
        </div>
      </div>
      <img class="deck-banner-thumb" src="/img/sunum-kapak-{kod}.jpg" alt="" loading="lazy" width="640" height="360">
    </a>
    </div>
  </div>
</section>

<section class="lp-sec" id="catalogs">
  <div class="section-inner">
    <div class="lp-tag">{t['cat_tag']}</div>
    <h2 class="about-h2">{t['cat_h2']}</h2>
    <div class="lp-cats">{kat}</div>
  </div>
</section>

<section class="lp-sec">
  <div class="section-inner">
    <div class="about-pull lp-pull"><p>{t['h1_sub']}</p></div>
  </div>
</section>

<section class="finalcta lp-slogan">
  <div class="finalcta-glow"></div>
  <div class="section-inner">
    <h2>{t['slogan'][0]}<br><em style="font-style:normal;color:var(--accent)">{t['slogan'][1]}</em><br>{t['slogan'][2]}</h2>
    <p>{t['slogan_p']}</p>
  </div>
</section>

<section class="lp-sec" id="contact">
  <div class="section-inner">
    <div class="lp-tag">{t['contact_tag']}</div>
    <h2 class="about-h2">{t['contact_h2']}</h2>
    <p class="about-p">{t['contact_sub']}</p>
    <div class="export-bar">
      <div class="export-head">
        <div class="export-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg></div>
        <div><div class="export-eyebrow">{t['exp_eyebrow']}</div><div class="export-title">{t['exp_title']}</div></div>
      </div>
      <div class="export-info">
        <div class="export-person">Samet Avcı</div>
        <div class="region-links">
          <a class="region-link" href="mailto:samet.avci@ibavalresa.com.tr"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 5L2 7"/></svg><span>samet.avci@ibavalresa.com.tr</span></a>
          <a class="region-link" href="tel:+905348904852"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg><span>+90 534 890 48 52</span></a>
        </div>
      </div>
    </div>
    <div class="lp-contact">
      <dl class="lp-aside">
        <div><dt>{t['l_phone']}</dt><dd><a href="tel:{TEL_HREF}">{TEL}</a></dd></div>
        <div><dt>{t['l_wa']}</dt><dd><a href="{WA_HREF}" target="_blank" rel="noopener">{WA}</a></dd></div>
        <div><dt>{t['l_mail']}</dt><dd><a href="mailto:{MAIL}">{MAIL}</a></dd></div>
        <div><dt>{t['l_addr']}</dt><dd>{t['addr']}</dd></div>
      </dl>
      <form class="lp-form" id="lp-form" action="https://formsubmit.co/ajax/{MAIL}" method="post" novalidate>
        <input type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px;opacity:0;">
        <input type="hidden" name="_subject" value="{t['subject']}">
        <input type="hidden" name="_template" value="table">
        <input type="hidden" name="_captcha" value="false">
        <input type="hidden" name="dil" value="{kod.upper()}">
        <div class="lp-grid">
          <div class="lp-field"><label for="f-name">{t['f_name']} {req}</label><input id="f-name" name="name" required autocomplete="name"></div>
          <div class="lp-field"><label for="f-company">{t['f_company']}</label><input id="f-company" name="company" autocomplete="organization"></div>
          <div class="lp-field"><label for="f-country">{t['f_country']} {req}</label><input id="f-country" name="country" required autocomplete="country-name"></div>
          <div class="lp-field"><label for="f-email">{t['f_email']} {req}</label><input id="f-email" type="email" name="email" required autocomplete="email"></div>
          <div class="lp-field full"><label for="f-phone">{t['f_phone']}</label><input id="f-phone" type="tel" name="phone" autocomplete="tel"></div>
          <div class="lp-field full"><label for="f-msg">{t['f_msg']} {req}</label><textarea id="f-msg" name="message" required placeholder="{e(t['f_msg_ph'])}"></textarea></div>
        </div>
        <label class="lp-consent"><input type="checkbox" name="consent" required> <span>{t['f_consent']}</span></label>
        <div class="lp-actions">
          <button class="form-submit btn-primary" type="submit"><span>{t['f_send']}</span>{ARROW}</button>
          <span class="lp-status" id="lp-status" role="status" aria-live="polite"></span>
        </div>
      </form>
    </div>
  </div>
</section>

<footer class="lp-foot">
  <div class="lp-foot-in">
    <img src="/assets/logos/ibavalresa-white.png" alt="ibavalresa" loading="lazy" width="242" height="50">
    <div>{t['rights']}<a href="/" hreflang="tr">ibavalresa.com.tr</a></div>
  </div>
</footer>

<script>
(function() {{
  var form = document.getElementById('lp-form'), status = document.getElementById('lp-status');
  var btn = form.querySelector('button[type=submit]');
  form.addEventListener('submit', async function(e) {{
    e.preventDefault();
    if (!form.checkValidity()) {{ form.reportValidity(); return; }}
    btn.disabled = true; status.classList.remove('show', 'error');
    try {{
      var res = await fetch(form.action, {{ method: 'POST', body: new FormData(form), headers: {{ 'Accept': 'application/json' }} }});
      var data = {{}}; try {{ data = await res.json(); }} catch (_) {{}}
      if (res.ok && String(data.success) === 'true') {{ status.textContent = {json.dumps(t['ok'], ensure_ascii=False)}; status.classList.add('show'); form.reset(); }}
      else throw new Error('x');
    }} catch (err) {{ status.textContent = {json.dumps(t['err'], ensure_ascii=False)}; status.classList.add('show', 'error'); }}
    finally {{ btn.disabled = false; setTimeout(function() {{ status.classList.remove('show'); }}, 8000); }}
  }});
}})();
</script>
<!-- Cloudflare Web Analytics --><script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "b339ef40148849a3bd6edd8333dde101"}}'></script><!-- End Cloudflare Web Analytics -->
</body>
</html>
"""
    p = os.path.join(KOK, kod, "index.html")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(out)
    print("yazıldı:", f"{kod}/index.html", len(out))

for kod, t in DIL.items():
    sayfa(kod, t)
