#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""İBAVALRESA — önbellek damgalarını tazeler.

css/base.css veya js/nav-line.js dosyasını her değiştirdiğinizde ÇALIŞTIRIN:

    python3 tools/bust.py            (site kökünden)

Ne yapar: her varlığın içeriğinden kısa bir özet (hash) üretir ve tüm HTML
sayfalarındaki  ?v=...  değerini bununla değiştirir.

Neden gerekli: ziyaretçinin tarayıcısı base.css'i önbelleğe alır. Dosyayı
değiştirip adresi aynı bırakırsanız, siteyi daha önce ziyaret etmiş kişiler
eski CSS ile yeni HTML'i birlikte görür. Bu sitede somut sonucu şudur:
--gualda token'ı eski CSS'te bulunmadığı için footer yazısı sarı yerine
beyaza düşer ve nav çizgisi gri kalır. Adres değişince tarayıcı yeni
dosyayı indirmek zorunda kalır ve sorun ortadan kalkar.
"""
import hashlib, glob, re, os, sys

VARLIKLAR = ["css/base.css", "js/nav-line.js"]

kok = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
os.chdir(kok)

damga = {}
for v in VARLIKLAR:
    if not os.path.exists(v):
        print(f"  ! bulunamadi, atlandi: {v}"); continue
    damga[v] = hashlib.md5(open(v, "rb").read()).hexdigest()[:8]

sayfalar = sorted(glob.glob("*.html") + glob.glob("en/*.html"))
degisen = 0
for f in sayfalar:
    s = open(f, encoding="utf-8").read(); o = s
    for v, d in damga.items():
        # hem damgasiz hem eski damgali hali yakala
        s = re.sub(r'(["\'])/' + re.escape(v) + r'(\?v=[^"\']*)?\1',
                   r'\g<1>/' + v + '?v=' + d + r'\1', s)
    if s != o:
        open(f, "w", encoding="utf-8").write(s); degisen += 1

for v, d in damga.items():
    print(f"  {v}  ->  ?v={d}")
print(f"  guncellenen sayfa: {degisen} / {len(sayfalar)}")
