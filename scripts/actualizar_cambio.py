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
    SALIDA.write_text(json.dumps({"actualizado_utc": ahora, "fuentes": fuentes}, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
