"""Duygu Çarkı verisini tasarım ekibinin gönderdiği HTML'den alır.

Kullanım (site kökünden):
    python3 tools/duygu_carki_veri_al.py "~/Desktop/Valresa Duygu Çarkı (GG.AA.YYYY)/Valresa Duygu Çarkı.html"
    python3 tools/blog_uret.py

Ekibin dosyası tek parça bir sayfa; içinde `const V = {...};` olarak duygular, alt duygular,
tonlar (kod, hex, aile, ikinci/diğer) ve not duruyor. Sitede yalnız bu VERİ kullanılır;
görünüm ve davranış bizde: tools/duygu_carki.css + tools/duygu_carki.js, yazı tools/blog_uret.py.
Böylece ekip yeni sürüm gönderdiğinde sayfayı yeniden uyarlamak gerekmez.
"""
import json, os, sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEDEF = os.path.join(KOK, "tools", "duygu_carki_veri.json")

if len(sys.argv) != 2:
    sys.exit(__doc__)
s = open(os.path.expanduser(sys.argv[1]), encoding="utf-8").read()
i = s.find("const V = ")
if i < 0:
    sys.exit("Dosyada 'const V = ' bulunamadı; ekibin dosya yapısı değişmiş olabilir.")
V, _ = json.JSONDecoder().raw_decode(s[i + len("const V = "):])

# Sitede verilen yazım kararları — ekibin dosyasında düzelmemiş olsa da her alımda uygulanır.
#   2026-11-23 Berat: mutfak tek tipte yazılsın, "kapak" ayrıca belirtilmesin.
ALAN_DUZELT = {"Mutfak dolabı kapakları": "Mutfak dolabı"}
for d in V.get("duygular", []):
    d["alanlar"] = list(dict.fromkeys(ALAN_DUZELT.get(x, x) for x in d.get("alanlar", [])))

# Temel denetim: beklenen alanlar ve renk biçimi
assert V.get("duygular"), "duygular boş"
for d in V["duygular"]:
    for k in ("ad", "metin", "alanlar", "alt"):
        assert k in d, f"{d.get('ad')}: '{k}' eksik"
    for a in d["alt"]:
        for t in a["tonlar"]:
            assert t["hex"].startswith("#") and len(t["hex"]) == 7, f"{t['kod']}: hex hatalı"

json.dump(V, open(HEDEF, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
ton = len({t["kod"] for d in V["duygular"] for a in d["alt"] for t in a["tonlar"]})
print(f"yazıldı: {os.path.relpath(HEDEF, KOK)} — {len(V['duygular'])} duygu, "
      f"{sum(len(d['alt']) for d in V['duygular'])} alt duygu, {ton} ton")
