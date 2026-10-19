"""
Tipos de cambio OFICIALES (bancos centrales y datos abiertos del Estado) para
la web de WIQON. Guarda cambio.json con valor, fecha y enlace de cada fuente.

  Paraguay   BCP  · Planilla de cotizaciones referenciales del día (₲ por moneda)
  Brasil     BCB  · PTAX, API pública Olinda (R$ por US$)
  Argentina  BCRA · API pública de estadísticas cambiarias (AR$ por US$)
  Colombia   Superfinanciera · TRM en datos.gov.co (COP por US$)

No se inventan valores: si una fuente falla, se conserva el último dato
conocido con su fecha real y se marca como desactualizado.
Sin dependencias: solo biblioteca estándar.
"""
import html
import json
import re
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

SALIDA = Path(__file__).resolve().parent.parent / "cambio.json"
AGENTE = "Mozilla/5.0 (compatible; WIQON/1.0; +https://wiqonlab.com; contacto@wiqonlab.com)"
MESES = {m: i + 1 for i, m in enumerate("enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre".split())}


def bajar(url):
    req = urllib.request.Request(url, headers={"User-Agent": AGENTE})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="replace")


def numero_es(txt):
    return float(txt.replace(".", "").replace(",", "."))


def bcp():
    url = "https://www.bcp.gov.py/webapps/web/cotizacion/monedas"
    texto = html.unescape(re.sub(r"<[^>]+>", " ", bajar(url)))
    texto = re.sub(r"\s+", " ", texto)
    m = re.search(r"COTIZACIONES AL \w+ (\d{1,2}) DE (\w+) DEL? (\d{4})", texto, re.I)
    if not m:
        raise ValueError("sin fecha en la planilla del BCP")
    fecha = f"{int(m.group(3)):04d}-{MESES[m.group(2).lower()]:02d}-{int(m.group(1)):02d}"
    valores = []
    for cod, nombre in (("USD", "Dólar estadounidense"), ("BRL", "Real brasileño"), ("ARS", "Peso argentino"), ("EUR", "Euro")):
        v = re.search(rf"\b{cod}\b \*? ?([\d.,]+) ([\d.,]+)", texto)
        if v:
            valores.append({"moneda": cod, "nombre": nombre, "valor": numero_es(v.group(2)), "unidad": f"₲ por 1 {cod}"})
    if not valores:
        raise ValueError("sin valores en la planilla del BCP")
    return {"id": "bcp", "pais": "PY", "institucion": "Banco Central del Paraguay", "serie": "Cotización referencial diaria",
            "url": url, "fecha": fecha, "valores": valores}


def bcb():
    hoy = datetime.now(timezone.utc)
    ini = (hoy - timedelta(days=10)).strftime("%m-%d-%Y")
    fin = hoy.strftime("%m-%d-%Y")
    api = ("https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,"
           f"dataFinalCotacao=@dataFinalCotacao)?@moeda='USD'&@dataInicial='{ini}'&@dataFinalCotacao='{fin}'&$format=json")
    datos = json.loads(bajar(api))["value"]
    fech = [d for d in datos if d["tipoBoletim"] == "Fechamento"]
    d = (fech or datos)[-1]
    return {"id": "bcb", "pais": "BR", "institucion": "Banco Central do Brasil", "serie": f"PTAX ({d['tipoBoletim'].lower()})",
            "url": "https://www.bcb.gov.br/estabilidadefinanceira/historicocotacoes", "fecha": d["dataHoraCotacao"][:10],
            "valores": [{"moneda": "USD", "nombre": "Dólar (venta)", "valor": d["cotacaoVenda"], "unidad": "R$ por 1 USD"}]}


def bcra():
    d = json.loads(bajar("https://api.bcra.gob.ar/estadisticascambiarias/v1.0/Cotizaciones"))["results"]
    usd = next(x for x in d["detalle"] if x["codigoMoneda"] == "USD")
    return {"id": "bcra", "pais": "AR", "institucion": "Banco Central de la República Argentina", "serie": "Tipo de cambio de referencia",
            "url": "https://www.bcra.gob.ar/PublicacionesEstadisticas/Tipos_de_cambios.asp", "fecha": d["fecha"],
            "valores": [{"moneda": "USD", "nombre": "Dólar", "valor": usd["tipoCotizacion"], "unidad": "AR$ por 1 USD"}]}


def trm():
    d = json.loads(bajar("https://www.datos.gov.co/resource/32sa-8pi3.json?$order=vigenciadesde%20DESC&$limit=1"))[0]
    return {"id": "trm", "pais": "CO", "institucion": "Superintendencia Financiera de Colombia", "serie": "TRM (datos.gov.co)",
            "url": "https://www.datos.gov.co/Econom-a-y-Finanzas/Tasa-de-Cambio-Representativa-del-Mercado-TRM/32sa-8pi3",
            "fecha": d["vigenciadesde"][:10],
            "valores": [{"moneda": "USD", "nombre": "Dólar (TRM)", "valor": float(d["valor"]), "unidad": "COP por 1 USD"}]}


# ---------------------------------------------------------------- historial (últimos 30 datos de cada serie)
DIAS_HIST = 30


def bcp_hist(moneda):
    """Planilla anual del BCP (filas = día, columnas = mes). Si el año recién empieza, suma el anterior."""
    url = "https://www.bcp.gov.py/webapps/web/cotizacion/monedas-historica"
    hoy = datetime.now(timezone.utc)
    serie = []
    for anio in (hoy.year - 1, hoy.year) if hoy.month <= 2 else (hoy.year,):
        req = urllib.request.Request(url, data=f"anho={anio}&moneda={moneda}".encode(), headers={"User-Agent": AGENTE})
        with urllib.request.urlopen(req, timeout=40) as r:
            pagina = r.read().decode("utf-8", errors="replace")
        tablas = re.findall(r"(?s)<table.*?</table>", pagina)
        if len(tablas) < 2:
            raise ValueError("sin tabla en el histórico del BCP")
        for fila in re.findall(r"(?s)<tr.*?</tr>", tablas[1])[1:]:
            celdas = [html.unescape(re.sub(r"<[^>]+>", "", c)).strip() for c in re.findall(r"(?s)<t[hd][^>]*>.*?</t[hd]>", fila)]
            if not celdas or not celdas[0].isdigit():
                continue
            dia = int(celdas[0])
            for mes, v in enumerate(celdas[1:13], 1):
                if re.fullmatch(r"[\d.]+,\d+", v):
                    serie.append([f"{anio:04d}-{mes:02d}-{dia:02d}", numero_es(v)])
    serie.sort()
    if not serie:
        raise ValueError("histórico del BCP vacío")
    return serie[-DIAS_HIST:]


def bcb_hist():
    hoy = datetime.now(timezone.utc)
    ini, fin = (hoy - timedelta(days=55)).strftime("%m-%d-%Y"), hoy.strftime("%m-%d-%Y")
    api = ("https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,"
           f"dataFinalCotacao=@dataFinalCotacao)?@moeda='USD'&@dataInicial='{ini}'&@dataFinalCotacao='{fin}'&$format=json")
    por_dia = {d["dataHoraCotacao"][:10]: d["cotacaoVenda"] for d in json.loads(bajar(api))["value"] if d["tipoBoletim"] == "Fechamento"}
    return sorted([k, v] for k, v in por_dia.items())[-DIAS_HIST:]


def bcra_hist():
    hoy = datetime.now(timezone.utc)
    api = (f"https://api.bcra.gob.ar/estadisticascambiarias/v1.0/Cotizaciones/USD?fechadesde={(hoy - timedelta(days=55)).strftime('%Y-%m-%d')}"
           f"&fechahasta={hoy.strftime('%Y-%m-%d')}")
    datos = json.loads(bajar(api))["results"]
    return sorted([d["fecha"], d["detalle"][0]["tipoCotizacion"]] for d in datos if d.get("detalle"))[-DIAS_HIST:]


HISTORIALES = {"bcp:USD": lambda: bcp_hist("USD"), "bcp:BRL": lambda: bcp_hist("BRL"), "bcb:USD": bcb_hist, "bcra:USD": bcra_hist}


def main():
    ahora = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    previo = {}
    if SALIDA.exists():
        try:
            previo = {f["id"]: f for f in json.loads(SALIDA.read_text(encoding="utf-8"))["fuentes"]}
        except (ValueError, KeyError):
            previo = {}
    fuentes = []
    for fn in (bcp, bcb, bcra, trm):
        nombre = fn.__name__
        try:
            f = fn()
            f.update(ok=True, consultado_utc=ahora)
        except Exception as e:  # fuente caída: último dato conocido, marcado como tal
            ant = previo.get(nombre)
            if not ant:
                print(f"{nombre}: sin datos ({type(e).__name__})")
                continue
            f = dict(ant, ok=False, error=type(e).__name__)
        fuentes.append(f)
        print(f"{f['id']}: {f['fecha']} " + ", ".join(f"{v['moneda']}={v['valor']}" for v in f["valores"]) + ("" if f["ok"] else " (último conocido)"))
    try:
        hist_previo = json.loads(SALIDA.read_text(encoding="utf-8")).get("historial", {}) if SALIDA.exists() else {}
    except ValueError:
        hist_previo = {}
    historial = {}
    for clave, fn in HISTORIALES.items():
        try:
            historial[clave] = fn()
            print(f"historial {clave}: {len(historial[clave])} datos hasta {historial[clave][-1][0]}")
        except Exception as e:  # se conserva el historial anterior
            if clave in hist_previo:
                historial[clave] = hist_previo[clave]
            print(f"historial {clave}: falló ({type(e).__name__})")
    SALIDA.write_text(json.dumps({"actualizado_utc": ahora, "fuentes": fuentes, "historial": historial}, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
