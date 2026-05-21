# İbavalresa — Tasarım Sistemi

Bu site bir **design system** üzerine kuruludur. Tüm renk, tipografi, boşluk ve
hareket değerleri tek bir kaynaktan (`assets/css/tokens.css`) yönetilir.
Bu dosyayı değiştirerek tüm siteyi yeniden temalandırabilirsiniz.

> Tema yönü: **aydınlık, temiz kurumsal** · Stil: **dengeli kurumsal** ·
> Diller: **TR (varsayılan) + EN**

---

## 1. Renk

Lacivert taban + mavi vurgu. Boya/kimya sektörü için güven + teknoloji hissi.
Token adları `--navy-*`, `--blue-*`, nötrler `--ink / --slate-* / --line / --bg / --surface`.

| Rol | Token | Değer |
|---|---|---|
| Ana etkileşim (primary) | `--blue-600` | `#1f6bb0` |
| Primary hover | `--blue-700` | `#1b568f` |
| Koyu zemin / footer | `--navy-900` | `#0a2138` |
| Ana metin | `--ink` | `#122031` |
| İkincil metin | `--slate-600` | `#51606e` |
| Kenarlık | `--line` | `#e3e7ec` |
| Sayfa zemini | `--bg` | `#f4f6f8` |
| Kart / panel | `--surface` | `#ffffff` |
| Sıcak ikincil vurgu | `--copper-600` | `#b9682e` (çok az kullanılır) |

Anlamsal eşlemeler (`--color-primary`, `--color-text` …) bileşenler tarafından
kullanılır; markaya özel design system geldiğinde yalnızca token değerleri
güncellenir, bileşen kodu değişmez.

## 2. Tipografi

Google Fonts üzerinden yüklenir (Türkçe karakter desteği tam).

| Rol | Font | Token |
|---|---|---|
| Başlıklar / display | **Bricolage Grotesque** | `--font-display` |
| Gövde metni | **Hanken Grotesk** | `--font-body` |
| Teknik etiket / mono | **JetBrains Mono** | `--font-mono` |

Tip ölçeği akışkandır (`clamp()`) — mobilden masaüstüne pürüzsüz büyür:
`--fs-display, --fs-h1, --fs-h2, --fs-h3, --fs-lead, --fs-body, --fs-sm, --fs-xs`.

## 3. Boşluk & Düzen

- Boşluk skalası: `--space-1` … `--space-10` (0.25rem → 8rem)
- Konteyner: `--container` 1240px · `--container-narrow` 880px
- Kenar boşluğu: `--gutter` (akışkan) · Bölüm dikey ritmi: `--section-y` (akışkan)
- Köşe yarıçapı: `--radius-sm/​-/-lg/-xl/-pill`
- Gölge: `--shadow-xs … -lg`, ayrıca `--shadow-blue`

## 4. Hareket (Animasyon)

emil-kowalski prensipleri — yalnızca `transform` + `opacity` (GPU hızlandırmalı).

- Easing seti: `--ease-out-quint`, `--ease-out-cubic`, `--ease-in-out-cubic`
- Süreler: `--dur-fast` 150ms · `--dur-base` 240ms · `--dur-slow` 420ms
- Giriş animasyonları `ease-out`, 200–420ms
- `[data-reveal]` öğeleri scroll'da kademeli açılır (IntersectionObserver, JS)
- `prefers-reduced-motion` tam desteklenir — hareket kapatılır

## 5. Bileşenler

Tümü `assets/css/style.css` içinde tanımlı. Yeni sayfa yaparken **sadece bu
sınıfları** kullanın; yeni CSS yazmaya gerek yoktur.

| Bileşen | Sınıf |
|---|---|
| Bölüm | `.section`, `.section--alt`, `.section--dark`, `.section--tight` |
| Konteyner | `.container`, `.container--narrow` |
| Bölüm başlığı | `.section-head`, `.section-head--center`, `.eyebrow`, `.lead` |
| Buton | `.btn` + `.btn--primary / --ghost / --on-dark / --lg` |
| Kart | `.card`, `.card--link`, `.card__icon`, `.card__index` |
| Izgara | `.grid` + `.grid--2 / --3 / --4` |
| Bilgi satırı | `.feature-row`, `.feature-row--flip`, `.media-frame` |
| İstatistik | `.stat-band`, `.stat`, `.stat__value`, `.stat__label` |
| Marka kartı | `.brand-card` ve alt öğeleri |
| Akordeon | `.accordion`, `.accordion__item/__trigger/__panel` |
| Zaman çizelgesi | `.timeline`, `.timeline__item`, `.timeline__year` |
| CTA bandı | `.cta-band`, `.cta-band__inner` |
| İletişim | `.contact-grid`, `.contact-item`, `.form`, `.field`, `.map-frame` |
| Liste | `.check-list` · Rozet `.badge` · Bağlantı `.link-arrow` |
| Sayfa banner'ı | `.page-hero`, `.breadcrumb` |

## 6. Header & Footer — tek kaynak

Header ve footer **her sayfaya `assets/js/site.js` tarafından enjekte edilir**.
HTML'de yalnızca boş `<header class="site-header"></header>` ve
`<footer class="site-footer"></footer>` bulunur.

Menüyü değiştirmek için → `site.js` içindeki **`NAV`** dizisini düzenleyin.
Tüm sayfalar otomatik güncellenir.

## 7. Çok dillilik (TR / EN)

- HTML içeriği **Türkçe** yazılır (varsayılan, SEO dostu).
- Çevrilebilir her öğede `data-i18n="anahtar"` bulunur.
- İngilizce karşılıklar her sayfanın `<head>`'inde
  `<script id="i18n-en" type="application/json">` içinde durur.
- Ortak metinler (menü, footer) `site.js` → `EN_COMMON` sözlüğündedir.
- Dil seçimi `localStorage`'da saklanır, fetch gerektirmez — **offline çalışır**.

Yeni dil eklemek için: `site.js` i18n mantığı çok dilli sözlüğe genişletilebilir.

## 8. Erişilebilirlik

- `:focus-visible` görünür odak halkası
- "İçeriğe geç" atlama bağlantısı
- Semantik HMTL (`<nav>`, `<main>`, `aria-current`, `aria-label`)
- `prefers-reduced-motion` desteği
- Renk kontrastı WCAG AA hedefli
