/* İBAVALRESA — nav alt çizgisi.
   Sayfa başındayken çizgi sitenin sade gri hali; aşağı inildikçe kalınlaşıp
   gualdaya döner. Renk, kalınlık ve geçiş css/base.css'te tanımlı
   (--gualda, --gualda-line, nav.scrolled); bu dosya yalnızca sınıfı takıp çıkarır.

   Eşik neden sabit piksel değil: ana sayfalarda hero 100vh, yani eşiğin anlamı
   ekran yüksekliğine bağlı. IntersectionObserver hero'yu izliyor, rootMargin -40%
   ile ekranın yaklaşık %60'ı kaydırıldığında tetikleniyor. Mobilde adres çubuğu
   açılıp kapandıkça innerHeight değiştiği için piksel/vh hesabı kayardı;
   observer canlı kutuları ölçtüğünden bundan etkilenmiyor.

   Hero'su olmayan sayfalarda (ve IntersectionObserver desteklemeyen eski
   tarayıcılarda) ekran yüksekliğine oranlı eşik kullanılır: açılış %60,
   kapanış %45 — hero'lu sayfalardaki eşikle aynı his. İki kademe, sınırda gidip gelmeyi (titremeyi) engeller. */

(function () {
  const nav = document.querySelector('nav');
  if (!nav) return;

  const set = (on) => nav.classList.toggle('scrolled', on);
  const hero = document.querySelector('.hero-video-section');

  if (hero && 'IntersectionObserver' in window) {
    new IntersectionObserver(
      (entries) => set(!entries[0].isIntersecting),
      { rootMargin: '-40% 0px 0px 0px' }
    ).observe(hero);
    return;
  }

  let on = false;
  const sync = () => {
    const h = window.innerHeight;
    if (!on && window.scrollY > h * 0.60) { on = true; set(true); }
    else if (on && window.scrollY < h * 0.45) { on = false; set(false); }
  };
  window.addEventListener('scroll', sync, { passive: true });
  sync();
})();
