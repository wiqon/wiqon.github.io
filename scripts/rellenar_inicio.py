"""
Rellena la portada (index.html y br/index.html) con los últimos datos ANTES de publicar, para que quien
no ejecuta JavaScript (Google, previsualizaciones de enlaces, conexiones lentas) vea valores reales con su
fecha en vez de "Cargando…". Después, en el navegador, v4.js y vivo.js actualizan todo como siempre.

Lo ejecuta .github/workflows/publicar.yml en cada publicación. No modifica los archivos del repositorio:
trabaja sobre la copia que se publica. Si falta un dato, deja el texto original (nunca inventa).

    python scripts/rellenar_inicio.py
"""
import html
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
UTC_3 = timezone(timedelta(hours=-3))  # Paraguay y Brasília (sin horario de verano)

TEXTOS = {
    "es": dict(btc="EN BTC", usdt="EN USDT", desde="Desde el ", sobre=" · el cierre está sobre la media",
               bajo=" · el cierre está debajo de la media", vela="Vela ", act="🕒 Actualizado: ", zona=" (hora de Paraguay)",
               act_corto="Actualizado", vela_de="vela del", ult="último conocido"),
    "pt": dict(btc="EM BTC", usdt="EM USDT", desde="Desde ", sobre=" · o fechamento está acima da média",
               bajo=" · o fechamento está abaixo da média", vela="Candle ", act="🕒 Atualizado: ", zona=" (horário de Brasília)",
               act_corto="Atualizado", vela_de="candle de", ult="último conhecido"),
}
NOMBRE_PT = {"Dólar estadounidense": "Dólar americano", "Real brasileño": "Real brasileiro", "Dólar (venta)": "Dólar (venda)"}


def num(v, dec=0):
    """Formato es-PY / pt-BR: punto de miles y coma decimal."""
    return f"{v:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def fecha(iso):
    a, m, d = str(iso)[:10].split("-")
    return f"{d}/{m}/{a}"


def hora_local(iso_utc):
    t = datetime.fromisoformat(str(iso_utc).replace("Z", "+00:00").replace(" ", "T"))
    if t.tzinfo is None:
        t = t.replace(tzinfo=timezone.utc)
    return t.astimezone(UTC_3).strftime("%d/%m/%Y %H:%M")


def poner(pagina, id_, contenido, clase=None):
    """Reemplaza el contenido del elemento con ese id (y opcionalmente su clase). Si no está, no toca nada."""
    patron = re.compile(r'(<(\w+)([^>]*?)\bid="%s"([^>]*)>)(.*?)(</\2>)' % re.escape(id_), re.S)
    m = patron.search(pagina)
    if not m:
        return pagina
    apertura = m.group(1)
    if clase is not None:
        apertura = re.sub(r'class="[^"]*"', f'class="{clase}"', apertura, count=1)
    return pagina[:m.start()] + apertura + contenido + m.group(6) + pagina[m.end():]


def leer(nombre):
    try:
        return json.loads((RAIZ / nombre).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def rellenar(pagina, idioma, estado, cambio):
    T = TEXTOS[idioma]
    if estado:
        btc = estado["senal"] == "EN_BTC"
        d = estado["distancia_pct"]
        dist = ("+" if d > 0 else "") + num(d, 1) + "%"
        pagina = poner(pagina, "senal", T["btc"] if btc else T["usdt"], "senal " + ("btc" if btc else "usdt"))
        pagina = poner(pagina, "desde", html.escape(T["desde"] + fecha(estado["desde"]) + (T["sobre"] if btc else T["bajo"])))
        pagina = poner(pagina, "vela", T["vela"] + fecha(estado["vela"]))
        pagina = poner(pagina, "cierre", "$" + num(estado["cierre"]))
        pagina = poner(pagina, "sma", "$" + num(estado["sma100"]))
        pagina = poner(pagina, "dist", dist)
        pagina = poner(pagina, "actualizado", html.escape(T["act"] + hora_local(estado["actualizado_utc"]) + T["zona"]))
        pagina = poner(pagina, "h-cierre", "US$ " + num(estado["cierre"]))
        pagina = poner(pagina, "h-dist", f'<span class="{"sube" if d >= 0 else "baja"}">{dist}</span>')
        pagina = poner(pagina, "h-desde", fecha(estado["desde"]))
        pagina = poner(pagina, "h-act", f'{T["act_corto"]} {hora_local(estado["actualizado_utc"])} · {T["vela_de"]} {fecha(estado["vela"])}')
        etiqueta = "● " + (T["btc"] if btc else T["usdt"])
        pagina = re.sub(r'<span class="est est-regla">[^<]*</span>',
                        f'<span class="est est-regla {"btc" if btc else "usdt"}">{etiqueta}</span>', pagina)
    if cambio:
        def dato(fuente, moneda):
            f = next((x for x in cambio["fuentes"] if x["id"] == fuente), None)
            v = f and next((x for x in f["valores"] if x["moneda"] == moneda), None)
            return (v["valor"], f) if v else None
        for id_, (fuente, moneda), pre, dec, nombre in (("snap-pyg", ("bcp", "USD"), "₲ ", 2, "BCP"),
                                                        ("snap-brl", ("bcb", "USD"), "R$ ", 4, "BCB PTAX"),
                                                        ("snap-brlpyg", ("bcp", "BRL"), "₲ ", 2, "BCP")):
            d = dato(fuente, moneda)
            if d:
                pagina = poner(pagina, id_, pre + num(d[0], dec))
                pagina = poner(pagina, id_ + "-f", f'{nombre} · {fecha(d[1]["fecha"])}' + ("" if d[1].get("ok", True) else f' · {T["ult"]}'))
        filas = []
        for f in cambio["fuentes"]:
            for v in f["valores"]:
                nombre = NOMBRE_PT.get(v["nombre"], v["nombre"]) if idioma == "pt" else v["nombre"]
                filas.append(
                    f'<tr><td>{html.escape(nombre)} <span class="u">· {html.escape(v["unidad"])}</span></td>'
                    f'<td class="v">{num(v["valor"], 2 if v["valor"] >= 100 else 4)}</td>'
                    f'<td class="om"><a href="{html.escape(f["url"])}" target="_blank" rel="noopener">{html.escape(f["institucion"])}</a>'
                    f' <span class="u">· {html.escape(f["serie"])}</span></td><td>{fecha(f["fecha"])}'
                    + ("" if f.get("ok", True) else f' <span class="u">({T["ult"]})</span>') + "</td></tr>")
        if filas:
            pagina = re.sub(r'(<table class="tabla" id="tabla-cambio".*?<tbody>)(.*?)(</tbody>)',
                            lambda m: m.group(1) + "".join(filas) + m.group(3), pagina, count=1, flags=re.S)
        pagina = poner(pagina, "cambio-act", f'{T["act_corto"]} {hora_local(cambio["actualizado_utc"])}')
    return pagina


def main():
    estado, cambio = leer("estado.json"), leer("cambio.json")
    for archivo, idioma in (("index.html", "es"), ("br/index.html", "pt")):
        ruta = RAIZ / archivo
        original = ruta.read_text(encoding="utf-8")
        nuevo = rellenar(original, idioma, estado, cambio)
        ruta.write_text(nuevo, encoding="utf-8")
        print(f"{archivo}: {'rellenado' if nuevo != original else 'sin cambios'}"
              f" · quedan {nuevo.count('Cargando…') + nuevo.count('Carregando…')} textos de carga (widgets externos)")


if __name__ == "__main__":
    main()
