"""Pruebas de la política de seguridad que se inserta en cada página (scripts/seguridad_web.py)."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import seguridad_web as W  # noqa: E402

PAGINA = '<!doctype html>\n<html><head>\n<meta charset="utf-8">\n<title>x</title></head><body></body></html>'


def test_inserta_despues_de_charset():
    t = W.aplicar(PAGINA)
    assert t.index('<meta charset="utf-8">') < t.index("Content-Security-Policy") < t.index("<title>")


def test_idempotente_y_reemplaza_bloque_viejo():
    una = W.aplicar(PAGINA)
    assert W.aplicar(una) == una
    vieja = una.replace("object-src 'none'", "object-src *")
    assert W.aplicar(vieja) == una


def test_sin_charset_no_toca():
    assert W.aplicar("<html><head></head></html>") is None


def test_directivas_clave():
    for d in ("object-src 'none'", "base-uri 'self'", "form-action 'self'", "upgrade-insecure-requests"):
        assert d in W.CSP
    assert "cdn.jsdelivr.net" not in W.CSP and "cdnjs" not in W.CSP


def test_paginas_publicadas_no_cargan_scripts_de_cdn():
    """Las librerías van en assets/vendor; un <script src> a un CDN sin control rompería la CSP."""
    for p in W.paginas():
        for src in re.findall(r'<script[^>]+src="(https?://[^"]+)"', p.read_text(encoding="utf-8")):
            assert src.startswith("https://static.cloudflareinsights.com/"), f"{p}: {src}"
