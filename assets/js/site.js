/* ==========================================================================
   İBAVALRESA — Site Davranışları
   • Header & footer enjeksiyonu (tek kaynak — tüm sayfalarda tutarlı)
   • Mobil navigasyon, dropdown
   • Scroll header, scroll-reveal animasyonu, akordeon
   • TR/EN dil değiştirici (offline çalışır — fetch yok)

   YENİ SAYFA EKLERKEN: aşağıdaki NAV dizisine ve PAGE_TITLES'a ekleyin.
   ========================================================================== */
(function () {
  "use strict";

  /* --- Site haritası ----------------------------------------------------- */
  var NAV = [
    {
      key: "corporate", label: "Kurumsal", menu: [
        { page: "hakkimizda",        href: "hakkimizda.html",       label: "Hakkımızda",          desc: "60+ yıllık tecrübe ve Türk–İspanyol ortaklığı", icon: "building" },
        { page: "uretim-teknoloji",  href: "uretim-teknoloji.html", label: "Üretim ve Teknoloji", desc: "SAP entegre, uçtan uca izlenebilir proses",       icon: "cog" },
        { page: "ar-ge",             href: "ar-ge.html",            label: "Ar-Ge",               desc: "Sürdürülebilir formülasyon geliştirme",           icon: "flask" },
        { page: "insan-kaynaklari",  href: "insan-kaynaklari.html", label: "İnsan Kaynakları",    desc: "Kariyer fırsatları ve ekip kültürü",              icon: "users" },
        { page: "surdurulebilirlik", href: "surdurulebilirlik.html",label: "Sürdürülebilirlik",   desc: "Çevre dostu teknoloji ve tedarik zinciri",        icon: "leaf" },
        { page: "kalite",            href: "kalite.html",           label: "Kalite & Sertifikalar", desc: "Uluslararası kalite standartları",              icon: "shield" }
      ]
    },
    { key: "brands",   page: "markalar",  href: "markalar.html",  label: "Markalar" },
    { key: "services", page: "hizmetler", href: "hizmetler.html", label: "Hizmetlerimiz" },
    { key: "contact",  page: "iletisim",  href: "iletisim.html",  label: "İletişim" }
  ];

  /* --- İkon seti (inline SVG) -------------------------------------------- */
  var ICONS = {
    building: '<path d="M3 21h18M5 21V7l7-4 7 4v14M9 9h0M9 13h0M9 17h0M15 9h0M15 13h0M15 17h0"/>',
    cog: '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.6 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.6a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>',
    flask: '<path d="M9 3h6M10 3v6.5L4.5 19a2 2 0 0 0 1.7 3h11.6a2 2 0 0 0 1.7-3L14 9.5V3M7.5 14h9"/>',
    users: '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
    leaf: '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10zM2 21c0-3 1.85-5.36 5.08-6"/>',
    shield: '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>'
  };

  /* --- Ortak EN sözlüğü (chrome) ----------------------------------------- */
  var EN_COMMON = {
    "nav.corporate": "Corporate",
    "nav.hakkimizda": "About Us",
    "nav.uretim-teknoloji": "Production & Technology",
    "nav.ar-ge": "R&D",
    "nav.insan-kaynaklari": "Human Resources",
    "nav.surdurulebilirlik": "Sustainability",
    "nav.kalite": "Quality & Certificates",
    "nav.markalar": "Brands",
    "nav.hizmetler": "Services",
    "nav.iletisim": "Contact",
    "nav.hakkimizda.desc": "60+ years of expertise and a Turkish–Spanish partnership",
    "nav.uretim-teknoloji.desc": "SAP-integrated, fully traceable processes",
    "nav.ar-ge.desc": "Sustainable formulation development",
    "nav.insan-kaynaklari.desc": "Career opportunities and team culture",
    "nav.surdurulebilirlik.desc": "Eco-friendly technology and supply chain",
    "nav.kalite.desc": "International quality standards",
    "topbar.online": "Online Services",
    "topbar.order": "Place Order",
    "topbar.payment": "Payment",
    "cta.contact": "Get in Touch",
    "cta.brands": "Explore Brands",
    "cta.discover": "Discover",
    "cta.detail": "Details",
    "cta.online": "Online Services",
    "footer.about": "A Turkish–Spanish partnership delivering high-quality wood paint and varnish solutions to global markets for over 60 years.",
    "footer.corporate": "Corporate",
    "footer.catalogs": "Catalogs",
    "footer.catalog.ral": "RAL-NCS-Nova Color Chart",
    "footer.catalog.valresa": "Valresa Catalog",
    "footer.catalog.ibavet": "İbavet Catalog",
    "footer.online": "Online Services",
    "footer.order": "Place Order",
    "footer.payment": "Collection / Payment",
    "footer.contactus": "Contact Us",
    "footer.legal.info": "Information Society Services",
    "footer.legal.kvkk": "GDPR Disclosure",
    "footer.rights": "All rights reserved.",
    "footer.tagline": "Quality. Always."
  };

  /* --- Yardımcılar ------------------------------------------------------- */
  function svg(path, cls) {
    return '<svg class="' + (cls || "") + '" xmlns="http://www.w3.org/2000/svg" width="20" height="20" ' +
      'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" ' +
      'stroke-linecap="round" stroke-linejoin="round">' + path + '</svg>';
  }
  function t(key, fallback) {
    return '<span data-i18n="' + key + '">' + fallback + '</span>';
  }

  /* ====================================================================== */
  /*  HEADER                                                                */
  /* ====================================================================== */
  function buildHeader(current) {
    var navItems = NAV.map(function (item) {
      if (item.menu) {
        var links = item.menu.map(function (m) {
          return '<a class="nav__menu-link" href="' + m.href + '">' +
            '<span class="nav__menu-link__icon">' + svg(ICONS[m.icon]) + '</span>' +
            '<span><span class="nav__menu-link__title" data-i18n="nav.' + m.page + '">' + m.label + '</span>' +
            '<span class="nav__menu-link__desc" data-i18n="nav.' + m.page + '.desc">' + m.desc + '</span></span></a>';
        }).join("");
        var inMenu = item.menu.some(function (m) { return m.page === current; });
        return '<li class="nav__item nav__item--has-menu">' +
          '<button class="nav__link" aria-expanded="false"' + (inMenu ? ' aria-current="page"' : '') + '>' +
          '<span data-i18n="nav.corporate">' + item.label + '</span>' +
          svg('<polyline points="6 9 12 15 18 9"/>', 'nav__caret') + '</button>' +
          '<div class="nav__menu">' + links + '</div></li>';
      }
      return '<li class="nav__item"><a class="nav__link" href="' + item.href + '"' +
        (item.page === current ? ' aria-current="page"' : '') + '>' +
        '<span data-i18n="nav.' + item.page + '">' + item.label + '</span></a></li>';
    }).join("");

    return '' +
      '<div class="topbar"><div class="container topbar__inner">' +
        '<span data-i18n="topbar.online">Online İşlemler:</span>' +
        '<a href="https://weborder.ibavalresa.com.tr" target="_blank" rel="noopener" data-i18n="topbar.order">Sipariş</a>' +
        '<span class="topbar__sep"></span>' +
        '<a href="https://tahsilat.ibavalresa.com.tr" target="_blank" rel="noopener" data-i18n="topbar.payment">Tahsilat</a>' +
        '<span class="topbar__sep"></span>' +
        '<a class="topbar__contact" href="tel:+903122675622">' +
          svg('<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13 1.05.36 2.07.7 3a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.93.34 1.95.57 3 .7A2 2 0 0 1 22 16.92z"/>') +
          '+90 312 267 56 22</a>' +
      '</div></div>' +
      '<div class="container"><nav class="navbar" aria-label="Ana menü">' +
        '<a class="brand" href="index.html" aria-label="İbavalresa ana sayfa">' +
          '<img class="brand__logo" src="assets/logos/ibavalresa-logo.svg" alt="İbavalresa" ' +
            'onerror="this.style.display=\'none\';this.nextElementSibling.style.display=\'block\'">' +
          '<span class="brand__fallback" style="display:none">İBA<span>VALRESA</span></span>' +
        '</a>' +
        '<ul class="nav">' + navItems + '</ul>' +
        '<div class="nav-actions">' +
          '<div class="lang-switch" role="group" aria-label="Dil / Language">' +
            '<button data-lang="tr" aria-pressed="true">TR</button>' +
            '<button data-lang="en" aria-pressed="false">EN</button>' +
          '</div>' +
          '<a class="btn btn--primary nav-cta" href="iletisim.html" data-i18n="cta.contact">İletişim</a>' +
          '<button class="nav-toggle" aria-label="Menü" aria-expanded="false">' +
            '<span></span><span></span><span></span></button>' +
        '</div>' +
      '</nav></div>' +
      '<div class="nav-overlay" hidden></div>';
  }

  /* ====================================================================== */
  /*  FOOTER                                                                */
  /* ====================================================================== */
  function buildFooter() {
    function social(name, href, path) {
      return '<a href="' + href + '" target="_blank" rel="noopener" aria-label="' + name + '">' + svg(path) + '</a>';
    }
    return '<div class="container">' +
      '<div class="footer__top">' +
        '<div class="footer__brand">' +
          '<span class="brand__fallback">İBA<span>VALRESA</span></span>' +
          '<p class="footer__about" data-i18n="footer.about">Türk–İspanyol ortaklığıyla 60+ yıldır global pazarlara yüksek kaliteli ahşap boya ve vernik çözümleri sunuyoruz.</p>' +
          '<div class="footer__social">' +
            social("LinkedIn", "https://www.linkedin.com/company/ibavalresa", '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6zM2 9h4v12H2zM4 6a2 2 0 1 0 0-4 2 2 0 0 0 0 4z"/>') +
            social("Instagram", "https://www.instagram.com/ibavalresa", '<rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1"/>') +
            social("YouTube", "https://www.youtube.com/@ibavalresa", '<path d="M22.5 6.5a3 3 0 0 0-2.1-2.1C18.5 4 12 4 12 4s-6.5 0-8.4.4A3 3 0 0 0 1.5 6.5 31 31 0 0 0 1 12a31 31 0 0 0 .5 5.5 3 3 0 0 0 2.1 2.1C5.5 20 12 20 12 20s6.5 0 8.4-.4a3 3 0 0 0 2.1-2.1A31 31 0 0 0 23 12a31 31 0 0 0-.5-5.5zM10 15V9l5 3z"/>') +
            social("Facebook", "https://www.facebook.com/ibavalresa", '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>') +
          '</div>' +
        '</div>' +
        '<div class="footer__col">' +
          '<h4 data-i18n="footer.corporate">Kurumsal</h4><ul>' +
            '<li><a href="hakkimizda.html" data-i18n="nav.hakkimizda">Hakkımızda</a></li>' +
            '<li><a href="uretim-teknoloji.html" data-i18n="nav.uretim-teknoloji">Üretim ve Teknoloji</a></li>' +
            '<li><a href="ar-ge.html" data-i18n="nav.ar-ge">Ar-Ge</a></li>' +
            '<li><a href="insan-kaynaklari.html" data-i18n="nav.insan-kaynaklari">İnsan Kaynakları</a></li>' +
            '<li><a href="surdurulebilirlik.html" data-i18n="nav.surdurulebilirlik">Sürdürülebilirlik</a></li>' +
            '<li><a href="kalite.html" data-i18n="nav.kalite">Kalite & Sertifikalar</a></li>' +
          '</ul></div>' +
        '<div class="footer__col">' +
          '<h4 data-i18n="footer.catalogs">Kataloglar</h4><ul>' +
            '<li><a href="#" data-i18n="footer.catalog.ral">RAL-NCS-Nova Kartela</a></li>' +
            '<li><a href="#" data-i18n="footer.catalog.valresa">Valresa Kataloğu</a></li>' +
            '<li><a href="#" data-i18n="footer.catalog.ibavet">İbavet Kataloğu</a></li>' +
            '<li><a href="markalar.html" data-i18n="nav.markalar">Markalar</a></li>' +
          '</ul></div>' +
        '<div class="footer__col">' +
          '<h4 data-i18n="footer.online">Online İşlemler</h4><ul>' +
            '<li><a href="https://weborder.ibavalresa.com.tr" target="_blank" rel="noopener" data-i18n="footer.order">Sipariş</a></li>' +
            '<li><a href="https://tahsilat.ibavalresa.com.tr" target="_blank" rel="noopener" data-i18n="footer.payment">Tahsilat</a></li>' +
            '<li><a href="iletisim.html" data-i18n="footer.contactus">Bize Ulaşın</a></li>' +
            '<li><a href="#" data-i18n="footer.legal.kvkk">KVKK Aydınlatma Metni</a></li>' +
          '</ul></div>' +
      '</div>' +
      '<div class="footer__bottom">' +
        '<span>© <span data-year></span> İbavalresa — <span data-i18n="footer.rights">Tüm hakları saklıdır.</span></span>' +
        '<span class="footer__bottom-links">' +
          '<a href="#" data-i18n="footer.legal.info">Bilgi Toplumu Hizmetleri</a>' +
          '<a href="#" data-i18n="footer.legal.kvkk">KVKK Aydınlatma Metni</a>' +
        '</span>' +
      '</div>' +
    '</div>';
  }

  /* ====================================================================== */
  /*  DAVRANIŞLAR                                                           */
  /* ====================================================================== */

  /* Scroll header */
  function initScrollHeader(header) {
    var onScroll = function () {
      header.setAttribute("data-scrolled", window.scrollY > 8 ? "true" : "false");
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* Mobil menü */
  function initMobileNav() {
    var toggle = document.querySelector(".nav-toggle");
    var overlay = document.querySelector(".nav-overlay");
    if (!toggle) return;
    function setOpen(open) {
      document.body.classList.toggle("nav-open", open);
      toggle.setAttribute("aria-expanded", String(open));
      if (overlay) overlay.hidden = !open;
    }
    toggle.addEventListener("click", function () {
      setOpen(!document.body.classList.contains("nav-open"));
    });
    if (overlay) overlay.addEventListener("click", function () { setOpen(false); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setOpen(false);
    });
    /* Mobilde dropdown aç/kapat */
    document.querySelectorAll(".nav__item--has-menu > .nav__link").forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        if (window.innerWidth > 1080) return;
        e.preventDefault();
        var item = btn.parentElement;
        item.setAttribute("data-open", item.getAttribute("data-open") === "true" ? "false" : "true");
      });
    });
  }

  /* Scroll-reveal — kademeli */
  function initReveal() {
    var els = document.querySelectorAll("[data-reveal]");
    if (!els.length) return;
    if (!("IntersectionObserver" in window)) {
      els.forEach(function (el) { el.classList.add("is-visible"); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        var siblings = Array.prototype.slice.call(
          el.parentElement.querySelectorAll(":scope > [data-reveal]")
        );
        var idx = siblings.indexOf(el);
        el.style.setProperty("--reveal-delay", Math.max(0, idx) * 90 + "ms");
        el.classList.add("is-visible");
        io.unobserve(el);
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    els.forEach(function (el) { io.observe(el); });
  }

  /* Akordeon */
  function initAccordion() {
    document.querySelectorAll(".accordion").forEach(function (acc) {
      acc.querySelectorAll(".accordion__trigger").forEach(function (trigger) {
        var item = trigger.closest(".accordion__item");
        var panel = item.querySelector(".accordion__panel");
        trigger.addEventListener("click", function () {
          var open = item.getAttribute("data-open") === "true";
          if (!acc.hasAttribute("data-multi")) {
            acc.querySelectorAll(".accordion__item").forEach(function (other) {
              other.setAttribute("data-open", "false");
              other.querySelector(".accordion__panel").style.height = "0px";
            });
          }
          item.setAttribute("data-open", String(!open));
          panel.style.height = open ? "0px" : panel.scrollHeight + "px";
        });
      });
    });
  }

  /* ---- i18n ------------------------------------------------------------- */
  function initI18n() {
    var dict = {};
    Object.keys(EN_COMMON).forEach(function (k) { dict[k] = EN_COMMON[k]; });
    var pageNode = document.getElementById("i18n-en");
    if (pageNode) {
      try {
        var pageDict = JSON.parse(pageNode.textContent);
        Object.keys(pageDict).forEach(function (k) { dict[k] = pageDict[k]; });
      } catch (e) { console.warn("i18n-en JSON ayrıştırılamadı", e); }
    }
    /* Orijinal TR metinleri sakla */
    var nodes = document.querySelectorAll("[data-i18n]");
    nodes.forEach(function (el) { el.dataset.i18nTr = el.innerHTML; });
    var phNodes = document.querySelectorAll("[data-i18n-ph]");
    phNodes.forEach(function (el) { el.dataset.i18nPhTr = el.getAttribute("placeholder") || ""; });

    function apply(lang) {
      document.documentElement.lang = lang;
      nodes.forEach(function (el) {
        var key = el.getAttribute("data-i18n");
        if (lang === "en" && dict[key] != null) el.innerHTML = dict[key];
        else el.innerHTML = el.dataset.i18nTr;
      });
      phNodes.forEach(function (el) {
        var key = el.getAttribute("data-i18n-ph");
        el.setAttribute("placeholder", (lang === "en" && dict[key] != null) ? dict[key] : el.dataset.i18nPhTr);
      });
      document.querySelectorAll(".lang-switch button").forEach(function (b) {
        b.setAttribute("aria-pressed", String(b.dataset.lang === lang));
      });
      try { localStorage.setItem("iba-lang", lang); } catch (e) {}
    }

    document.querySelectorAll(".lang-switch button").forEach(function (b) {
      b.addEventListener("click", function () { apply(b.dataset.lang); });
    });

    var saved = "tr";
    try { saved = localStorage.getItem("iba-lang") || "tr"; } catch (e) {}
    if (saved === "en") apply("en");
  }

  /* ====================================================================== */
  /*  BAŞLAT                                                                */
  /* ====================================================================== */
  function init() {
    var current = document.body.getAttribute("data-page") || "";
    var header = document.querySelector(".site-header");
    var footer = document.querySelector(".site-footer");
    if (header) header.innerHTML = buildHeader(current);
    if (footer) footer.innerHTML = buildFooter();

    var yearNode = document.querySelector("[data-year]");
    if (yearNode) yearNode.textContent = new Date().getFullYear();

    if (header) initScrollHeader(header);
    initMobileNav();
    initReveal();
    initAccordion();
    initI18n();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
