"""
Genera assets/frontera.svg: ilustración propia de WIQON (no foto) con la frontera
Paraguay–Brasil de noche: Ciudad del Este y Foz do Iguaçu, el arco del Puente de la
Amistad sobre el río Paraná y una línea de mercado en el cielo. Colores de la marca.

Uso:  python scripts/ilustracion_frontera.py
"""
import math
import random
from pathlib import Path

SALIDA = Path(__file__).resolve().parent.parent / "assets" / "frontera.svg"
W, H = 1600, 560
RIO = 395  # nivel del agua
rnd = random.Random(27)


def edificios(x0, x1, base, alto_min, alto_max, densidad):
    """Siluetas de edificios con ventanas encendidas (determinístico)."""
    piezas, ventanas = [], []
    x = x0
    while x < x1:
        w = rnd.randint(18, 46)
        h = rnd.randint(alto_min, alto_max)
        if rnd.random() < 0.18:
            h += rnd.randint(40, 90)  # alguna torre
        piezas.append(f'<rect x="{x}" y="{base - h}" width="{w}" height="{h}"/>')
        for wy in range(base - h + 8, base - 6, 9):
            for wx in range(x + 4, x + w - 4, 7):
                if rnd.random() < densidad:
                    c = rnd.choice(["#f5c76b", "#f5c76b", "#ffe2a1", "#5fd6f3"])
                    o = round(rnd.uniform(0.35, 0.95), 2)
                    ventanas.append(f'<rect x="{wx}" y="{wy}" width="3" height="4" fill="{c}" opacity="{o}"/>')
        x += w + rnd.randint(1, 6)
    return piezas, ventanas


def main():
    # barrancas del Paraná (las ciudades están arriba de la barranca)
    BAR = RIO - 70
    cde, cde_v = edificios(-10, 470, BAR, 50, 150, 0.32)
    foz, foz_v = edificios(1140, 1620, BAR + 4, 35, 110, 0.26)

    # Puente de la Amistad: tablero arriba, un gran arco de hormigón debajo
    ax0, ax1, base_arco = 520, 1080, RIO - 6
    tablero = BAR - 22
    cx, rx = (ax0 + ax1) / 2, (ax1 - ax0) / 2
    ry = base_arco - (tablero + 16)
    arco = f"M{ax0},{base_arco} A{rx},{ry} 0 0 1 {ax1},{base_arco}"
    arco_int = f"M{ax0 + 24},{base_arco} A{rx - 24},{ry - 18} 0 0 1 {ax1 - 24},{base_arco}"
    pilares = []
    for i in range(1, 20):
        px = ax0 + (ax1 - ax0) * i / 20
        y_arco = base_arco - ry * math.sqrt(max(0, 1 - ((px - cx) / rx) ** 2))
        if y_arco > tablero + 14:
            pilares.append(f'<line x1="{px:.1f}" y1="{tablero + 8}" x2="{px:.1f}" y2="{y_arco:.1f}"/>')
    luces = "".join(f'<circle cx="{x}" cy="{tablero - 10}" r="2.3" fill="#ffe2a1"/><line x1="{x}" y1="{tablero}" x2="{x}" y2="{tablero - 9}" stroke="#4b5d78" stroke-width="1.2"/>'
                    for x in range(440, 1170, 36))

    # línea de mercado en el cielo (velas suavizadas)
    pts, y = [], 210
    for i in range(0, 41):
        y += rnd.uniform(-16, 13) - 1.2
        y = max(70, min(240, y))
        pts.append((i * 40, y))
    linea = " ".join(f"{x},{y:.1f}" for x, y in pts)
    area = f"M0,{pts[0][1]:.1f} " + " ".join(f"L{x},{y:.1f}" for x, y in pts) + f" L1600,300 L0,300 Z"

    # estrellas
    estrellas = "".join(f'<circle cx="{rnd.randint(0, W)}" cy="{rnd.randint(8, 180)}" r="{rnd.choice([0.6, 0.8, 1.1])}" fill="#cfe9ff" opacity="{rnd.uniform(.2, .7):.2f}"/>'
                        for _ in range(110))

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" role="img" aria-labelledby="t d">
<title id="t">Frontera Paraguay–Brasil</title>
<desc id="d">Ilustración de WIQON: Ciudad del Este y Foz do Iguaçu de noche, el arco del Puente de la Amistad sobre el río Paraná y una línea de mercado en el cielo.</desc>
<defs>
  <linearGradient id="cielo" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#050a14"/><stop offset=".62" stop-color="#0b1d33"/><stop offset="1" stop-color="#123250"/></linearGradient>
  <linearGradient id="agua" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b2236"/><stop offset="1" stop-color="#050a14"/></linearGradient>
  <linearGradient id="mercado" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#22c3ee" stop-opacity=".22"/><stop offset="1" stop-color="#22c3ee" stop-opacity="0"/></linearGradient>
  <radialGradient id="halo" cx=".5" cy=".7" r=".6"><stop offset="0" stop-color="#22c3ee" stop-opacity=".16"/><stop offset="1" stop-color="#22c3ee" stop-opacity="0"/></radialGradient>
  <filter id="brillo" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3"/></filter>
  <mask id="reflejo"><rect width="{W}" height="{H}" fill="url(#agua)"/></mask>
</defs>
<rect width="{W}" height="{H}" fill="url(#cielo)"/>
<rect width="{W}" height="{H}" fill="url(#halo)"/>
<g opacity=".18" stroke="#22c3ee" stroke-width=".6">{"".join(f'<line x1="0" y1="{yy}" x2="{W}" y2="{yy}"/>' for yy in range(60, 300, 48))}</g>
{estrellas}
<path d="{area}" fill="url(#mercado)"/>
<polyline points="{linea}" fill="none" stroke="#22c3ee" stroke-width="5" opacity=".35" filter="url(#brillo)"/>
<polyline points="{linea}" fill="none" stroke="#5fd6f3" stroke-width="2"/>
<circle cx="{pts[-1][0] - 2}" cy="{pts[-1][1]:.1f}" r="5" fill="#5fd6f3"/>
<g fill="#0a1626">{"".join(cde)}{"".join(foz)}</g>
<g>{"".join(cde_v)}{"".join(foz_v)}</g>
<path d="M-10,{BAR} L470,{BAR} C500,{BAR + 6} 515,{RIO - 30} 540,{RIO} L-10,{RIO} Z" fill="#0d1b1a"/>
<path d="M1140,{BAR + 4} L1620,{BAR + 4} L1620,{RIO} L1060,{RIO} C1085,{RIO - 30} 1100,{BAR + 8} 1140,{BAR + 4} Z" fill="#0d1b1a"/>
<rect y="{RIO}" width="{W}" height="{H - RIO}" fill="url(#agua)"/>
<g stroke="#e9eef6" fill="none" stroke-linecap="round">
  <path d="{arco}" stroke-width="12" opacity=".92"/>
  <path d="{arco_int}" stroke-width="3" opacity=".35"/>
  <g stroke-width="2.2" opacity=".55">{"".join(pilares)}</g>
</g>
<rect x="420" y="{tablero}" width="760" height="9" fill="#e9eef6" opacity=".92"/>
<rect x="420" y="{tablero + 9}" width="760" height="3" fill="#0a1626"/>
{luces}
<g transform="translate(0,{2 * RIO}) scale(1,-1)" opacity=".22" mask="url(#reflejo)">
  <path d="{arco}" stroke="#e9eef6" stroke-width="10" fill="none"/>
  <g fill="#f5c76b">{"".join(cde_v[::3])}{"".join(foz_v[::3])}</g>
</g>
<g stroke="#22c3ee" stroke-width="1.2" opacity=".25">{"".join(f'<line x1="{rnd.randint(0, W)}" y1="{yy}" x2="{rnd.randint(0, W)}" y2="{yy}"/>' for yy in range(RIO + 18, H, 22))}</g>
</svg>'''
    SALIDA.write_text(svg, encoding="utf-8")
    print("OK", SALIDA, len(svg) // 1024, "KB")


if __name__ == "__main__":
    main()
