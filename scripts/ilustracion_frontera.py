"""
Genera assets/frontera.svg: ilustración propia de WIQON con el Puente de la Amistad sobre el cañón
del río Paraná, entre Ciudad del Este (izquierda) y Foz do Iguaçu (derecha), de noche.
Mismo lenguaje que la portada (río de operaciones): trazos luminosos finos; los vehículos que cruzan
el puente son trazos cian (hacia Brasil) y azules (hacia Paraguay). Sin texto: sirve en los tres idiomas.
El movimiento (vehículos y reflejos) se apaga con prefers-reduced-motion.

Uso:  python scripts/ilustracion_frontera.py
"""
import math
import random
from pathlib import Path

SALIDA = Path(__file__).resolve().parent.parent / "assets" / "frontera.svg"
W, H = 1600, 560
TABLERO, AGUA = 250, 420                     # altura del tablero del puente y nivel del río
A0, A1, CIMA = 600, 1040, 270                # arranques y cima del arco (parábola)
rnd = random.Random(42)


def f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def arco_y(x, cima=CIMA, base=AGUA - 14):
    m = (A0 + A1) / 2
    return base - (base - cima) * (1 - ((x - m) / ((A1 - A0) / 2)) ** 2)


def curva(fn, x0, x1, paso=6):
    return "M" + " L".join(f"{f(x)} {f(fn(x))}" for x in range(x0, x1 + 1, paso))


def barranca(lado):
    """Silueta de la barranca (cañón del Paraná) de cada lado."""
    if lado == "izq":
        return f"M0 298 C160 292 330 300 470 296 C520 296 548 304 566 330 C584 356 592 392 604 {AGUA} L0 {AGUA} Z"
    return f"M{W} 306 C1440 300 1270 308 1140 302 C1094 300 1068 310 1052 334 C1036 360 1030 394 1022 {AGUA} L{W} {AGUA} Z"


def ciudad(x0, x1, piso, alto_min, alto_max, densidad):
    """Edificios como nubes de ventanas encendidas (puntos), con silueta muy tenue."""
    siluetas, ventanas = [], []
    x = x0
    while x < x1:
        ancho = rnd.choice([24, 30, 36, 42, 54])
        alto = rnd.randint(alto_min, alto_max) if rnd.random() < densidad else rnd.randint(18, 50)
        siluetas.append(f'<rect x="{x}" y="{piso - alto}" width="{ancho - 4}" height="{alto}"/>')
        for wy in range(piso - alto + 6, piso - 4, 7):
            for wx in range(x + 4, x + ancho - 6, 6):
                if rnd.random() < 0.34:
                    calido = rnd.random() < 0.22
                    ventanas.append(f'<rect x="{wx}" y="{wy}" width="2.4" height="2.4" fill="{"#f2c67a" if calido else "#cfe9ff"}" opacity="{f(rnd.uniform(.25, .95))}"/>')
        x += ancho
    return "".join(siluetas), "".join(ventanas)


def curvas_nivel():
    """Líneas de relieve suaves, recortadas por las barrancas."""
    lineas = []
    for i, y in enumerate(range(312, AGUA, 10)):
        d = curva(lambda x, y=y, i=i: y + 3.5 * math.sin(x * .011 + i * .9) + 2 * math.sin(x * .027 + i), -10, W + 10, 10)
        lineas.append(f'<path d="{d}"/>')
    return "".join(lineas)


def puente():
    partes = []
    extra = curva(lambda x: arco_y(x), A0, A1, 4)
    intra = curva(lambda x: arco_y(x, cima=CIMA + 11, base=AGUA - 8), A0 + 14, A1 - 14, 4)
    partes.append(f'<path class="arco" d="{extra}"/>')
    partes.append(f'<path class="arco fino" d="{intra}"/>')
    for x in range(A0 + 30, A1 - 29, 22):                      # columnas entre el arco y el tablero
        y = arco_y(x)
        if y - TABLERO > 10:
            partes.append(f'<line class="col" x1="{x}" y1="{TABLERO + 5}" x2="{x}" y2="{f(y)}"/>')
    for x in list(range(452, 590, 34)) + list(range(1068, 1192, 34)):   # pilares de los accesos
        base = 300 if x < 800 else 306
        partes.append(f'<line class="col" x1="{x}" y1="{TABLERO + 5}" x2="{x}" y2="{base}"/>')
    partes.append(f'<line class="tablero" x1="420" y1="{TABLERO}" x2="1220" y2="{TABLERO}"/>')
    partes.append(f'<line class="baranda" x1="420" y1="{TABLERO - 9}" x2="1220" y2="{TABLERO - 9}"/>')
    for x in range(440, 1210, 38):
        partes.append(f'<line class="poste" x1="{x}" y1="{TABLERO - 9}" x2="{x}" y2="{TABLERO - 20}"/><circle class="farol" cx="{x}" cy="{TABLERO - 21}" r="2.2"/>')
    return "".join(partes)


def vehiculos():
    """Trazos que cruzan el tablero: cian hacia Brasil (→), azul hacia Paraguay (←)."""
    out = []
    for i in range(14):
        ida = i % 2 == 0
        largo = rnd.randint(26, 54)
        dur = rnd.uniform(7, 13)
        y = TABLERO - (4 if ida else 7.5)
        out.append(f'<rect class="auto {"ida" if ida else "vuelta"}" x="0" y="{f(y)}" width="{largo}" height="3.4" rx="1.7" '
                   f'fill="url(#{"estela-ida" if ida else "estela-vuelta"})" style="animation-duration:{f(dur)}s;animation-delay:{f(-rnd.uniform(0, dur))}s"/>')
    return "".join(out)


def reflejos():
    out = []
    for x in range(440, 1210, 38):
        out.append(f'<rect x="{x - 1}" y="{AGUA + 6}" width="2" height="{rnd.randint(30, 90)}" fill="url(#reflejo)" opacity="{f(rnd.uniform(.35, .8))}"/>')
    for _ in range(26):
        color = "#3fe0ff" if rnd.random() < .55 else "#3d6dff"
        out.append(f'<rect class="brillo" x="{rnd.randint(0, W)}" y="{rnd.randint(AGUA + 10, H - 10)}" width="{rnd.randint(40, 220)}" height="1.4" fill="{color}" '
                   f'opacity="{f(rnd.uniform(.08, .28))}" style="animation-delay:{f(-rnd.uniform(0, 18))}s"/>')
    return "".join(out)


def estrellas():
    return "".join(f'<circle cx="{rnd.randint(0, W)}" cy="{rnd.randint(4, 200)}" r="{f(rnd.uniform(.5, 1.3))}" opacity="{f(rnd.uniform(.25, .8))}"/>' for _ in range(90))


sil_cde, ven_cde = ciudad(0, 470, 298, 90, 190, .55)
sil_foz, ven_foz = ciudad(1130, W, 306, 60, 140, .4)
espejo_arco = curva(lambda x: 2 * AGUA - arco_y(x), A0, A1, 6)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Puente de la Amistad sobre el río Paraná, entre Ciudad del Este y Foz do Iguaçu, de noche">
<defs>
  <linearGradient id="cielo" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#02040b"/><stop offset=".55" stop-color="#06122a"/><stop offset="1" stop-color="#0a1c3c"/></linearGradient>
  <linearGradient id="agua" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#071833"/><stop offset="1" stop-color="#02040b"/></linearGradient>
  <linearGradient id="tierra" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#06142a"/><stop offset="1" stop-color="#030a18"/></linearGradient>
  <radialGradient id="resplandor-izq" cx=".16" cy=".5" r=".36"><stop offset="0" stop-color="#3fe0ff" stop-opacity=".13"/><stop offset="1" stop-color="#3fe0ff" stop-opacity="0"/></radialGradient>
  <radialGradient id="resplandor-der" cx=".86" cy=".54" r=".3"><stop offset="0" stop-color="#3d6dff" stop-opacity=".14"/><stop offset="1" stop-color="#3d6dff" stop-opacity="0"/></radialGradient>
  <linearGradient id="estela-ida" x1="0" x2="1"><stop offset="0" stop-color="#3fe0ff" stop-opacity="0"/><stop offset="1" stop-color="#bff6ff"/></linearGradient>
  <linearGradient id="estela-vuelta" x1="1" x2="0"><stop offset="0" stop-color="#3d6dff" stop-opacity="0"/><stop offset="1" stop-color="#9db6ff"/></linearGradient>
  <linearGradient id="reflejo" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#eaf3ff" stop-opacity=".55"/><stop offset="1" stop-color="#eaf3ff" stop-opacity="0"/></linearGradient>
  <clipPath id="barrancas"><path d="{barranca("izq")}"/><path d="{barranca("der")}"/></clipPath>
  <filter id="halo" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<style>
  .arco {{ fill: none; stroke: #eaf3ff; stroke-width: 3.2; stroke-linecap: round; }}
  .arco.fino {{ stroke-width: 1.2; opacity: .55; }}
  .col {{ stroke: #cfe0f7; stroke-width: 1.3; opacity: .7; }}
  .tablero {{ stroke: #eaf3ff; stroke-width: 4.5; }}
  .baranda {{ stroke: #cfe0f7; stroke-width: 1; opacity: .6; }}
  .poste {{ stroke: #9fb2cf; stroke-width: 1; }}
  .farol {{ fill: #fff3d6; }}
  .relieve path {{ fill: none; stroke: #3fe0ff; stroke-width: .8; opacity: .13; }}
  .siluetas rect {{ fill: #050d20; }}
  .auto {{ animation: 9s linear infinite; }}
  .ida {{ animation-name: ida; }} .vuelta {{ animation-name: vuelta; }}
  @keyframes ida {{ from {{ transform: translateX(424px); }} to {{ transform: translateX(1162px); }} }}
  @keyframes vuelta {{ from {{ transform: translateX(1162px); }} to {{ transform: translateX(424px); }} }}
  .brillo {{ animation: deriva 18s linear infinite; }}
  @keyframes deriva {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-60px); }} }}
  @media (prefers-reduced-motion: reduce) {{ .auto, .brillo {{ animation: none; }} .auto {{ transform: translateX(800px); }} }}
</style>
<rect width="{W}" height="{H}" fill="url(#cielo)"/>
<g fill="#eaf3ff">{estrellas()}</g>
<rect width="{W}" height="{H}" fill="url(#resplandor-izq)"/><rect width="{W}" height="{H}" fill="url(#resplandor-der)"/>
<g class="siluetas">{sil_cde}{sil_foz}</g>
<g>{ven_cde}{ven_foz}</g>
<rect y="{AGUA}" width="{W}" height="{H - AGUA}" fill="url(#agua)"/>
<path d="{barranca("izq")}" fill="url(#tierra)"/><path d="{barranca("der")}" fill="url(#tierra)"/>
<g class="relieve" clip-path="url(#barrancas)">{curvas_nivel()}</g>
<path d="{espejo_arco}" fill="none" stroke="#eaf3ff" stroke-width="2" opacity=".12"/>
<g>{reflejos()}</g>
<g filter="url(#halo)">{puente()}</g>
<g filter="url(#halo)">{vehiculos()}</g>
</svg>
'''
SALIDA.write_text(svg, encoding="utf-8")
print(f"OK {SALIDA.name} · {len(svg) // 1024} KB")
