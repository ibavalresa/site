#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""İBAVALRESA — iki dil kontrolü.

Türkçe (kök) ve İngilizce (en/) sayfalar ayrı dosyalardır ve elle güncellenir;
tools/build_en.py kullanım dışıdır. Bu araç, bir sayfanın bir dilde değişip
diğerinde değişmediği durumları yakalar: İngilizcesi unutulan bir güncellemeyi
commit'ten önce görmek için.

Kullanım (site kökünden):
    python3 tools/dil_kontrol.py                 # henüz commit edilmemiş değişiklikler
    python3 tools/dil_kontrol.py --son 5         # son 5 commit + commit edilmemişler
    python3 tools/dil_kontrol.py --beri a5f83be  # o commit'ten bu yana (ör. son yükleme)

Yalnızca içerik değişikliklerine bakar; tools/bust.py'nin güncellediği ?v=
önbellek damgaları sayılmaz. Çevirinin DOĞRULUĞUNU denetlemez, yalnızca bir
tarafın unutulduğunu söyler.
Çıkış kodu: uyarı varsa 1, yoksa 0.
"""
import ast, difflib, os, re, subprocess, sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Sayfa çiftleri: build_en.py'deki SLUG tablosu (dosya ÇALIŞTIRILMADAN, metin olarak okunur)
def sayfa_ciftleri():
    agac = ast.parse(open(os.path.join(KOK, "tools", "build_en.py"), encoding="utf-8").read())
    for d in agac.body:
        if isinstance(d, ast.Assign) and any(getattr(t, "id", None) == "SLUG" for t in d.targets):
            slug = ast.literal_eval(d.value)
            break
    else:
        sys.exit("build_en.py içinde SLUG tablosu bulunamadı.")
    ciftler = {f"{tr}.html": f"en/{en}.html" for tr, en in slug.items()}
    ciftler["404.html"] = "en/404.html"            # 404 sayfaları sonradan eklendi, tabloda yok
    return ciftler

# İngilizce karşılığı bilerek olmayan sayfalar (değişirlerse yalnızca bilgi verilir)
KARSILIKSIZ = {"sunum.html": "sunum kendi içinde TR/EN geçişi yapıyor",
               "cerez-politikasi.html": "İngilizce sayfalar bu Türkçe sayfaya bağlanıyor",
               "kvkk-aydinlatma-metni.html": "İngilizce sayfalar bu Türkçe sayfaya bağlanıyor"}

def git(*a):
    return subprocess.run(["git", *a], cwd=KOK, capture_output=True, text=True)

def normal(metin):
    return None if metin is None else re.sub(r"\?v=[0-9a-f]{6,}", "?v=", metin)

def eski_hal(taban, yol):
    r = git("show", f"{taban}:{yol}")
    return r.stdout if r.returncode == 0 else None

def simdiki_hal(yol):
    p = os.path.join(KOK, yol)
    return open(p, encoding="utf-8").read() if os.path.exists(p) else None

def degisen_satir(a, b):
    a, b = (a or "").splitlines(), (b or "").splitlines()
    return sum(1 for s in difflib.unified_diff(a, b, lineterm="", n=0)
               if s[:1] in "+-" and not s.startswith(("+++", "---")))

def main():
    arg = sys.argv[1:]
    if "--son" in arg:
        taban = f"HEAD~{int(arg[arg.index('--son') + 1])}"
    elif "--beri" in arg:
        taban = arg[arg.index("--beri") + 1]
    else:
        taban = "HEAD"
    if git("rev-parse", "--verify", taban).returncode:
        sys.exit(f"Git'te '{taban}' bulunamadı.")

    def degisti(yol):
        e, s = normal(eski_hal(taban, yol)), normal(simdiki_hal(yol))
        return (e != s), degisen_satir(e, s)

    uyari, bilgi, tamam = [], [], []
    for tr, en in sorted(sayfa_ciftleri().items()):
        tr_d, tr_n = degisti(tr)
        en_d, en_n = degisti(en)
        if tr_d and simdiki_hal(en) is None:
            uyari.append(f"{tr} değişti; İngilizce karşılığı {en} BULUNAMADI")
        elif tr_d and not en_d:
            uyari.append(f"{tr} değişti ({tr_n} satır), karşılığı {en} değişmedi")
        elif en_d and not tr_d:
            bilgi.append(f"yalnızca {en} değişti ({en_n} satır) — İngilizceye özel bir düzeltme olabilir, "
                         f"yoksa {tr} de güncellenmeli")
        elif tr_d and en_d:
            tamam.append(f"{tr} ({tr_n} satır)  ↔  {en} ({en_n} satır)")
    for tr, neden in KARSILIKSIZ.items():
        if degisti(tr)[0]:
            bilgi.append(f"{tr} değişti — İngilizce karşılığı yok ({neden})")

    kapsam = "commit edilmemiş değişiklikler" if taban == "HEAD" else f"{taban} sürümünden bu yana"
    print(f"İki dil kontrolü — {kapsam}\n")
    for baslik, liste, isaret in (("UYARI — İngilizcesi unutulmuş olabilir", uyari, "!"),
                                  ("Bilgi", bilgi, "i"),
                                  ("İki dilde de güncellenmiş", tamam, "✓")):
        if liste:
            print(f"{baslik}:")
            for s in liste:
                print(f"  {isaret} {s}")
            print()
    if not (uyari or bilgi or tamam):
        print("Sayfalarda içerik değişikliği yok.\n")
    print("Uyarı yok." if not uyari else f"{len(uyari)} uyarı — İngilizce sayfaları kontrol edin.")
    return 1 if uyari else 0

if __name__ == "__main__":
    sys.exit(main())
