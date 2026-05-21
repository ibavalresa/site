# İbavalresa Kurumsal Web Sitesi

Çok sayfalı, statik (HTML/CSS/JS) kurumsal web sitesi. Framework veya derleme
adımı yoktur — dosyalar olduğu gibi sunucuya/GitHub Pages'e yüklenir.

Tasarım sistemi detayları için → [`DESIGN-SYSTEM.md`](DESIGN-SYSTEM.md)

---

## İçindekiler

- [Dosya yapısı](#dosya-yapısı)
- [Yerel önizleme](#yerel-önizleme)
- [GitHub Pages ile yayınlama](#github-pages-ile-yayınlama)
- [Görselleri ekleme](#görselleri-ekleme) ← **yayından önce yapılmalı**
- [Logo değiştirme](#logo-değiştirme)
- [İletişim formu](#iletişim-formu)
- [İçerik düzenleme ipuçları](#i̇çerik-düzenleme-ipuçları)

---

## Dosya yapısı

```
ibavalresa-site/
├── index.html              Ana sayfa
├── hakkimizda.html         Kurumsal sayfalar
├── uretim-teknoloji.html
├── ar-ge.html
├── insan-kaynaklari.html
├── surdurulebilirlik.html
├── kalite.html
├── markalar.html
├── hizmetler.html
├── iletisim.html
├── assets/
│   ├── css/
│   │   ├── tokens.css      Tasarım token'ları (renk, font, boşluk)
│   │   └── style.css       Tüm bileşen/düzen stilleri
│   ├── js/
│   │   └── site.js         Header/footer enjeksiyonu, menü, i18n, animasyon
│   ├── images/             Sayfa görselleri (+ _placeholder.svg, favicon.svg)
│   ├── brands/             Marka görselleri
│   ├── logos/              Logo dosyası
│   └── videos/             Hero video(ları)
├── DESIGN-SYSTEM.md
└── README.md
```

Header ve footer her sayfaya `site.js` tarafından **otomatik enjekte edilir** —
tek bir yerden yönetilir, 10 dosyada tekrar düzenlemeye gerek yoktur.

---

## Yerel önizleme

`site.js` ve diğer kaynaklar nedeniyle dosyaları doğrudan çift tıklayıp
açmak yerine basit bir yerel sunucu kullanın:

```bash
# Proje klasöründe:
python3 -m http.server 8000
# Tarayıcıda: http://localhost:8000
```

veya VS Code "Live Server" eklentisi.

---

## GitHub Pages ile yayınlama

1. Bu klasörü bir GitHub deposuna yükleyin (kök dizinde `index.html` olmalı):
   ```bash
   git init
   git add .
   git commit -m "İbavalresa kurumsal site"
   git branch -M main
   git remote add origin git@github.com:KULLANICI/DEPO.git
   git push -u origin main
   ```
2. GitHub'da depo → **Settings → Pages**
3. **Source**: `Deploy from a branch` · **Branch**: `main` / `(root)` → **Save**
4. Birkaç dakika içinde `https://KULLANICI.github.io/DEPO/` adresinde yayında olur.

Özel alan adı için (örn. `ibavalresa.com.tr`): Settings → Pages → Custom domain.

> Not: Tüm bağlantılar göreceli yoldadır (`hakkimizda.html`, `assets/...`),
> alt dizinde yayında da sorunsuz çalışır.

---

## Görselleri ekleme

Site şu an her görsel için zarif bir **placeholder** (`_placeholder.svg`)
gösterir — gerçek dosya yoksa otomatik devreye girer. Yayından önce aşağıdaki
dosyaları belirtilen adlarla ilgili klasöre ekleyin (görseller `.jpg` bekleniyor;
`onerror` koruması sayesinde eksik dosya siteyi bozmaz).

### `assets/images/`
| Dosya adı | İçerik |
|---|---|
| `kampus.jpg` | İBA Kampüs genel görünümü |
| `uretim.jpg` | Üretim / SAP süreci |
| `uretim-hatlari.jpg` | Modern üretim hatları |
| `ar-ge.jpg` | Ar-Ge / laboratuvar |
| `formulasyon.jpg` | Formülasyon geliştirme |
| `ik-ekip-kulturu.jpg` | Ekip / çalışma kültürü |
| `surdurulebilirlik-uretim.jpg` | Çevre dostu üretim |
| `esfera-su-bazli.jpg` | Su bazlı ürünler (Esfera) |
| `kalite-yuzey.jpg` | Yüzey kalitesi / kalite kontrol |
| `satis-ofisleri.jpg` | Bölgesel satış ofisleri |
| `og-image.jpg` | Sosyal medya paylaşım görseli (1200×630 px önerilir) |

### `assets/brands/`
| Dosya adı | Marka |
|---|---|
| `valresa.jpg` | Valresa |
| `esfera.jpg` | Esfera |
| `ibavet.jpg` | İbavet |
| `iba-sanayi.jpg` | İba Sanayi Boyaları |

### `assets/videos/`
| Dosya adı | İçerik |
|---|---|
| `hero.mp4` | Ana sayfa hero arka plan videosu (sessiz, döngü; ~10-20 sn, web için sıkıştırılmış MP4/H.264 önerilir) |

> Önerilen görsel boyutları: feature/içerik görselleri en az **1200 px** genişlik,
> JPG kalite ~80. Dosya boyutlarını web için optimize edin.

---

## Logo değiştirme

`assets/logos/ibavalresa-logo.svg` şu an **geçici** bir kelime-işaretidir.
Gerçek logoyu aynı dosya adıyla (`ibavalresa-logo.svg`) değiştirin —
yatay, ~186×34 oranına yakın, tercihen SVG. PNG kullanılacaksa `site.js`
içindeki logo `<img src>` uzantısı güncellenmelidir.

`assets/images/favicon.svg` tarayıcı sekmesi ikonudur; istenirse değiştirilebilir.

---

## İletişim formu

`iletisim.html` içindeki form **statiktir** (`action="#"`) — gönderim için bir
backend bağlanması gerekir. Seçenekler:
- [Formspree](https://formspree.io), [Web3Forms](https://web3forms.com) gibi
  servisler (sadece `action` ve `method` ayarlanır)
- Kurumsal bir e-posta/CRM endpoint'i

Form alanları ve placeholder'lar hazırdır.

---

## İçerik düzenleme ipuçları

- **Menü / site haritası:** `assets/js/site.js` → `NAV` dizisi
- **Footer bağlantıları:** `assets/js/site.js` → `buildFooter()`
- **Renk / font / boşluk:** `assets/css/tokens.css` (tek dosya)
- **Metin (TR):** doğrudan ilgili `.html` dosyasında düzenlenir
- **Metin (EN):** ilgili sayfanın `<head>`'indeki `i18n-en` JSON bloğu +
  ortak metinler için `site.js` → `EN_COMMON`
- **Yeni sayfa:** mevcut bir alt sayfayı kopyalayın, `data-page` değerini ve
  `NAV` dizisini güncelleyin

Çevrilebilir her metin öğesinde `data-i18n="anahtar"` bulunur; TR ve EN
karşılıkları bu anahtarla eşleşmelidir.
