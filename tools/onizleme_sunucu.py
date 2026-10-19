#!/usr/bin/env python3
"""İBAVALRESA yerel önizleme sunucusu.

Site kökünden çalıştır:  python3 tools/onizleme_sunucu.py   → http://127.0.0.1:8931/
Önbelleksiz; bulunmayan adreslerde sunucudaki gibi 404 sayfasını gösterir
(/en/ altında İngilizce 404).
"""
import os, sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8931

class H(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw): super().__init__(*a, directory=SITE, **kw)
    def end_headers(self):
        self.send_header("Cache-Control", "no-store"); super().end_headers()
    def send_error(self, code, message=None, explain=None):
        if code == 404:
            p = "en/404.html" if self.path.startswith("/en/") else "404.html"
            body = open(os.path.join(SITE, p), "rb").read()
            self.send_response(404); self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body); return
        super().send_error(code, message, explain)
    def log_message(self, *a): pass

print(f"önizleme: http://127.0.0.1:{PORT}/", flush=True)
ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
