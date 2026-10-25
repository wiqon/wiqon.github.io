"""
Miniaturas reales para los 5 pasos de «Cómo decidimos qué sobrevive» (assets/pasos/<n>_<idioma>.webp, 640 × 360).

  1 Hipótesis          gráfico diario de BTC con su media de 100 días (terminal WIQON Estudio, datos de Binance)
  2 Reglas exactas     tarjeta de la regla en la terminal: estado, cierre, media, distancia y regla escrita
  3 Backtest           curva del backtest 2018–2026 con costos (terminal, escena Backtest)
  4 Fuera de muestra   saldo de la misma regla en un broker real con spreads y swaps (Exness demo, 2022–2026),
                       dibujado desde resultados/mt5/operaciones_exness_btcusdm.csv del laboratorio
  5 Real               captura de MetaTrader 5 con WIQON Shield operando (assets/productos/shield.webp)

Requiere la terminal en C:\\wiqon-terminal y el repo del laboratorio en C:\\agm-backtesting-lab.
Uso (Playwright de ~/herramientas):  python scripts/imagenes_pasos.py
"""
import csv
import io
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "assets" / "pasos"
TERMINAL = Path(r"C:\wiqon-terminal\index.html").as_uri()
OPERACIONES = Path(r"C:\agm-backtesting-lab\resultados\mt5\operaciones_exness_btcusdm.csv")
FONDO = (8, 11, 20)
ANCHO, ALTO = 640, 360


def guardar(img, nombre, modo="cubrir"):
    img = img.convert("RGB")
    if modo == "cubrir":
        r = max(ANCHO / img.width, ALTO / img.height)
        img = img.resize((round(img.width * r), round(img.height * r)), Image.LANCZOS)
        x, y = (img.width - ANCHO) // 2, 0
        img = img.crop((x, y, x + ANCHO, y + ALTO))
    else:   # contener: entra completa, centrada sobre el fondo de la terminal
        lienzo = Image.new("RGB", (ANCHO, ALTO), FONDO)
        img.thumbnail((ANCHO - 24, ALTO - 24), Image.LANCZOS)
        lienzo.paste(img, ((ANCHO - img.width) // 2, (ALTO - img.height) // 2))
        img = lienzo
    img.save(SALIDA / f"{nombre}.webp", "WEBP", quality=84, method=6)


def curva_broker(idioma):
    """SVG con el saldo después de cada operación cerrada, sin suavizar ni recortar."""
    filas = list(csv.DictReader(open(OPERACIONES, encoding="utf-8")))
    puntos = [(f["fecha"][:7].replace(".", "-"), float(f["balance_usd"])) for f in filas if f["direccion"] == "out" or f is filas[0]]
    lo, hi = min(b for _, b in puntos), max(b for _, b in puntos)
    W, H, M = 1200, 675, 70
    xy = [(M + i * (W - 2 * M) / (len(puntos) - 1), H - M - (b - lo) / (hi - lo) * (H - 2 * M - 40)) for i, (_, b) in enumerate(puntos)]
    linea = " ".join(f"{x:.1f},{y:.1f}" for x, y in xy)
    t = {"es": ("Misma regla en un broker real · CFD con spreads y swaps", "saldo de la cuenta demo, US$", "Exness demo · 2022–2026"),
         "pt": ("Mesma regra numa corretora real · CFD com spreads e swaps", "saldo da conta demo, US$", "Exness demo · 2022–2026")}[idioma]
    return f"""<html><body style="margin:0;background:#080b14;font-family:Segoe UI,Arial,sans-serif">
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<text x="{M}" y="52" fill="#e9eef8" font-size="30" font-weight="700">{t[0]}</text>
<text x="{M}" y="88" fill="#8a96ad" font-size="22">{t[1]} · {t[2]}</text>
<polyline points="{M},{H - M} {linea} {W - M},{H - M}" fill="rgba(63,224,255,.10)" stroke="none"/>
<polyline points="{linea}" fill="none" stroke="#3fe0ff" stroke-width="4" stroke-linejoin="round"/>
<line x1="{M}" y1="{H - M}" x2="{W - M}" y2="{H - M}" stroke="#25304a" stroke-width="2"/>
<text x="{M}" y="{H - 28}" fill="#8a96ad" font-size="22">{puntos[0][0]}</text>
<text x="{W - M}" y="{H - 28}" fill="#8a96ad" font-size="22" text-anchor="end">{puntos[-1][0]}</text>
<text x="{W - M}" y="{xy[-1][1] - 18:.0f}" fill="#3fe0ff" font-size="26" font-weight="700" text-anchor="end">US$ {puntos[-1][1]:,.0f}</text>
<text x="{M + 8}" y="{xy[0][1] - 14:.0f}" fill="#8a96ad" font-size="22">US$ {puntos[0][1]:,.0f}</text>
</svg></body></html>"""


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        nav = p.chromium.launch()
        for idioma in ("es", "pt"):
            pag = nav.new_page(viewport={"width": 1100, "height": 980}, device_scale_factor=2)
            pag.goto(TERMINAL); pag.wait_for_timeout(9000)
            if idioma == "pt":
                pag.keyboard.press("p"); pag.wait_for_timeout(1500)
            pag.keyboard.press("2"); pag.wait_for_timeout(5000)
            guardar(Image.open(io.BytesIO(pag.locator("#escena-2 .tarjeta").screenshot())), f"1_{idioma}")
            pag.keyboard.press("1"); pag.wait_for_timeout(2500)
            # la regla escrita: desde la señal hasta el texto de la regla, con el ancho de la tarjeta
            caja = pag.locator(".col-estrategia").bounding_box()
            arriba, abajo = pag.locator(".col-estrategia .senal").bounding_box(), pag.locator(".col-estrategia .regla").bounding_box()
            pag.evaluate("document.querySelector('.col-estrategia .grilla').style.display='none'")
            arriba, abajo = pag.locator(".col-estrategia .senal").bounding_box(), pag.locator(".col-estrategia .regla").bounding_box()
            recorte = {"x": caja["x"], "y": arriba["y"] - 16, "width": caja["width"], "height": abajo["y"] + abajo["height"] - arriba["y"] + 32}
            guardar(Image.open(io.BytesIO(pag.screenshot(clip=recorte))), f"2_{idioma}", "contener")
            pag.evaluate("document.querySelector('.col-estrategia .grilla').style.display=''")
            pag.keyboard.press("4"); pag.wait_for_timeout(6000)
            guardar(Image.open(io.BytesIO(pag.locator("#escena-4 .grafico-caja").screenshot())), f"3_{idioma}", "contener")
            pag.close()
            g = nav.new_page(viewport={"width": 1200, "height": 675})
            g.set_content(curva_broker(idioma))
            guardar(Image.open(io.BytesIO(g.screenshot())), f"4_{idioma}")
            g.close()
        nav.close()
    # 5: MetaTrader con el Shield (zona del panel y las velas recientes)
    mt5 = Image.open(RAIZ / "assets" / "productos" / "shield.webp")
    for idioma in ("es", "pt"):
        guardar(mt5.crop((0, 0, 720, 405)), f"5_{idioma}")
    for f in sorted(SALIDA.glob("*.webp")):
        print(f.name, f.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
