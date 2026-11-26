"""
Distintivos de producto de WIQON: un sello circular por producto, con el isotipo (W + diamante), el nombre en el
anillo y un ícono propio en el centro. Cada producto tiene su color de acento; la base es siempre la misma.
Salida: assets/distintivos/<producto>.svg (240x240, solo fuentes del sistema: se usan como <img>).
Uso:  python scripts/construir_distintivos.py
"""
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DEST = RAIZ / "assets" / "distintivos"

# producto: (texto de arriba, texto de abajo, acento, ícono en un cuadro de 100x100 centrado en (120,128))
P = {
    "shield": ("WIQON SHIELD", "GESTIÓN DE RIESGO", "#2ad4ff",
               '<path d="M50 6 L86 20 V48 C86 72 70 88 50 95 C30 88 14 72 14 48 V20 Z" fill="none" stroke="{a}" stroke-width="6" stroke-linejoin="round"/>'
               '<path d="M28 64 L42 50 L54 58 L72 36" fill="none" stroke="#fff" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round"/>'
               '<path d="M62 35 H73 V46" fill="none" stroke="#fff" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round"/>'),
    "ciberseguridad": ("CIBERSEGURIDAD", "REVISIÓN DE SITIOS", "#3be08a",
                       '<rect x="26" y="44" width="48" height="40" rx="8" fill="none" stroke="#fff" stroke-width="6"/>'
                       '<path d="M36 44 V34 a14 14 0 0 1 28 0 V44" fill="none" stroke="#fff" stroke-width="6"/>'
                       '<circle cx="50" cy="62" r="5" fill="{a}"/><path d="M50 66 V74" stroke="{a}" stroke-width="5" stroke-linecap="round"/>'
                       '<path d="M10 40 a42 42 0 0 1 14 -24 M90 40 a42 42 0 0 0 -14 -24 M4 54 a50 50 0 0 1 4 -26 M96 54 a50 50 0 0 0 -4 -26" '
                       'fill="none" stroke="{a}" stroke-width="5" stroke-linecap="round"/>'),
    "tokenizacion": ("TOKENIZACIÓN", "PARA COMERCIOS", "#ffd76a",
                     '<polygon points="50,8 86,29 86,71 50,92 14,71 14,29" fill="none" stroke="{a}" stroke-width="6" stroke-linejoin="round"/>'
                     '<polygon points="50,24 72,37 72,63 50,76 28,63 28,37" fill="none" stroke="#fff" stroke-width="5" stroke-linejoin="round"/>'
                     '<path d="M40 44 H60 M50 44 V64" stroke="#fff" stroke-width="6" stroke-linecap="round"/>'),
    "auditoria": ("AUDITORÍA", "ESTRATEGIAS Y BOTS", "#a78bfa",
                  '<rect x="14" y="56" width="10" height="20" rx="2" fill="#fff"/><rect x="30" y="44" width="10" height="32" rx="2" fill="#fff"/>'
                  '<rect x="46" y="62" width="10" height="14" rx="2" fill="#fff"/>'
                  '<circle cx="62" cy="42" r="20" fill="none" stroke="{a}" stroke-width="6.5"/>'
                  '<path d="M76 56 L92 72" stroke="{a}" stroke-width="9" stroke-linecap="round"/>'),
    "libro": ("LIBRO WIQON", "¿VENTAJA O SUERTE?", "#ff9f43",
              '<path d="M50 26 C40 18 24 16 10 20 V80 C24 76 40 78 50 86 C60 78 76 76 90 80 V20 C76 16 60 18 50 26 Z" fill="none" stroke="#fff" stroke-width="6" stroke-linejoin="round"/>'
              '<path d="M50 26 V86" stroke="#fff" stroke-width="5"/>'
              '<path d="M60 52 L67 59 L82 42" fill="none" stroke="{a}" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round"/>'
              '<path d="M20 40 H40 M20 52 H40" stroke="{a}" stroke-width="5" stroke-linecap="round"/>'),
    "laboratorio": ("LABORATORIO", "PROBADO, NO PROMETIDO", "#17c3e6",
                    '<path d="M38 10 H62 M42 10 V38 L18 80 A8 8 0 0 0 25 92 H75 A8 8 0 0 0 82 80 L58 38 V10" fill="none" stroke="#fff" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"/>'
                    '<path d="M28 66 H72 L80 82 A6 6 0 0 1 75 88 H25 A6 6 0 0 1 20 82 Z" fill="{a}" opacity=".85"/>'
                    '<circle cx="44" cy="76" r="4" fill="#06142e"/><circle cx="58" cy="72" r="3" fill="#06142e"/>'),
}

ISOTIPO = ('<g transform="translate(120 58)"><path d="M-17 -8 L-9 12 L0 -4 L9 12 L17 -8" fill="none" stroke="#fff" stroke-width="4.2" '
           'stroke-linejoin="round" stroke-linecap="round"/><rect x="-3.6" y="9" width="7.2" height="7.2" fill="{a}" transform="rotate(45 0 12.6)"/></g>')


def sello(clave, arriba, abajo, acento, icono):
    fuente = 'font-family="Segoe UI, Inter, Arial, sans-serif" font-weight="800"'
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240" width="240" height="240" role="img" aria-label="WIQON · {arriba.title()}">
<defs>
<radialGradient id="f-{clave}" cx="50%" cy="38%" r="70%"><stop offset="0" stop-color="#12306a"/><stop offset=".65" stop-color="#081a3d"/><stop offset="1" stop-color="#040b1f"/></radialGradient>
<path id="a-{clave}" d="M 25 120 A 95 95 0 0 1 215 120"/>
<path id="b-{clave}" d="M 15 120 A 105 105 0 0 0 225 120"/>
</defs>
<circle cx="120" cy="120" r="116" fill="url(#f-{clave})" stroke="{acento}" stroke-width="5"/>
<circle cx="120" cy="120" r="84" fill="none" stroke="{acento}" stroke-opacity=".35" stroke-width="2"/>
<text {fuente} font-size="{15 if len(arriba) <= 14 else 13}" letter-spacing="2.4" fill="{acento}" text-anchor="middle"><textPath href="#a-{clave}" startOffset="50%">{arriba}</textPath></text>
<text {fuente} font-size="{11.5 if len(abajo) <= 18 else 10.5}" letter-spacing="1.8" fill="#dbe8ff" text-anchor="middle"><textPath href="#b-{clave}" startOffset="50%">{abajo}</textPath></text>
<circle cx="22" cy="120" r="3.2" fill="{acento}"/><circle cx="218" cy="120" r="3.2" fill="{acento}"/>
{ISOTIPO.format(a=acento)}
<g transform="translate(70 76)">{icono.format(a=acento)}</g>
</svg>
"""


IDIOMAS = {  # textos del anillo en portugués e inglés (el ícono y el color no cambian)
    "pt": {"shield": ("WIQON SHIELD", "GESTÃO DE RISCO"), "ciberseguridad": ("CIBERSEGURANÇA", "REVISÃO DE SITES"),
           "tokenizacion": ("TOKENIZAÇÃO", "PARA COMÉRCIOS"), "auditoria": ("AUDITORIA", "ESTRATÉGIAS E ROBÔS"),
           "libro": ("LIVRO WIQON", "VANTAGEM OU SORTE?"), "laboratorio": ("LABORATÓRIO", "TESTADO, NÃO PROMETIDO")},
    "en": {"shield": ("WIQON SHIELD", "RISK MANAGEMENT"), "ciberseguridad": ("CYBERSECURITY", "WEBSITE REVIEW"),
           "tokenizacion": ("TOKENIZATION", "FOR BUSINESSES"), "auditoria": ("AUDIT", "STRATEGIES AND BOTS"),
           "libro": ("WIQON BOOK", "EDGE OR LUCK?"), "laboratorio": ("LABORATORY", "TESTED, NOT PROMISED")},
}


if __name__ == "__main__":
    DEST.mkdir(parents=True, exist_ok=True)
    for k, (arriba, abajo, acento, icono) in P.items():
        (DEST / f"{k}.svg").write_text(sello(k, arriba, abajo, acento, icono), encoding="utf-8")
        print("ok", k)
        for idi, tx in IDIOMAS.items():
            (DEST / f"{k}_{idi}.svg").write_text(sello(f"{k}{idi}", *tx[k], acento, icono), encoding="utf-8")
