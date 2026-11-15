"""
Cabeceras de seguridad para wiqonlab.com.

GitHub Pages no deja configurar cabeceras HTTP, así que la política de contenido (CSP) y la
política de referencias van como <meta> dentro de cada página. El script es idempotente:
si la página ya tiene el bloque, lo reemplaza por el actual. Corre en el workflow después de
todos los generadores, justo antes de publicar.  Uso:  python scripts/seguridad_web.py

Si una página nueva necesita otro origen (un widget, una API), se agrega acá y en ningún otro
lado. Los orígenes salen de lo que el sitio usa de verdad (assets/*.js y las páginas).
"""
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
EXCLUIR = {"conceptos", "node_modules", ".git", "tests"}

SUPABASE = "ffswzcjcrxokoefhykvv.supabase.co"
CSP = "; ".join([
    "default-src 'self'",
    # 'unsafe-inline': las páginas tienen scripts en línea (tema, formularios). Igual bloquea
    # cualquier script que venga de un dominio que no esté en esta lista.
    "script-src 'self' 'unsafe-inline' https://static.cloudflareinsights.com https://s3.tradingview.com",
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
    "font-src 'self' https://fonts.gstatic.com data:",
    "img-src 'self' data: blob: https:",
    "media-src 'self' https:",
    "connect-src 'self' https://data-api.binance.vision https://api.binance.com wss://data-stream.binance.vision "
    f"https://{SUPABASE} wss://{SUPABASE} https://n8n.wiqonlab.com https://cloudflareinsights.com",
    "frame-src https://www.youtube-nocookie.com https://www.youtube.com https://*.tradingview.com https://*.tradingview-widget.com",
    "worker-src 'self' blob:",
    "object-src 'none'",
    "base-uri 'self'",
    "form-action 'self'",
    "upgrade-insecure-requests",
])

INICIO, FIN = "<!-- seguridad:inicio -->", "<!-- seguridad:fin -->"
BLOQUE = (f'{INICIO}\n<meta http-equiv="Content-Security-Policy" content="{CSP}">\n'
          f'<meta name="referrer" content="strict-origin-when-cross-origin">\n{FIN}')
VIEJO = re.compile(re.escape(INICIO) + r".*?" + re.escape(FIN), re.S)
CHARSET = re.compile(r"<meta charset=[\"']?utf-8[\"']?\s*/?>", re.I)


def paginas():
    for p in RAIZ.rglob("*.html"):
        if not EXCLUIR.intersection(p.relative_to(RAIZ).parts):
            yield p


def aplicar(texto):
    """Devuelve el HTML con el bloque de seguridad (o None si la página no tiene <meta charset>)."""
    if VIEJO.search(texto):
        return VIEJO.sub(lambda _: BLOQUE, texto, count=1)
    m = CHARSET.search(texto)
    if not m:
        return None
    return texto[:m.end()] + "\n" + BLOQUE + texto[m.end():]


def main():
    cambiadas, sin_charset = 0, []
    for p in paginas():
        t = p.read_text(encoding="utf-8")
        nuevo = aplicar(t)
        if nuevo is None:
            sin_charset.append(str(p.relative_to(RAIZ)))
        elif nuevo != t:
            p.write_text(nuevo, encoding="utf-8", newline="")
            cambiadas += 1
    print(f"seguridad_web: {cambiadas} páginas actualizadas")
    if sin_charset:
        print("Sin <meta charset> (no se tocaron):", ", ".join(sin_charset))


if __name__ == "__main__":
    main()
