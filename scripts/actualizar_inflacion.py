"""
Inflación anual por país (FMI, World Economic Outlook, API DataMapper) para el mapa
de la pestaña "Economía". Guarda inflacion.json con el código numérico ISO de cada país
(el mismo que usa el mapa world-atlas), el valor del año elegido y si es estimación.

Fuente: FMI, indicador PCPIPCH (inflación, precios al consumidor promedio, variación % anual).
Sin dependencias: solo biblioteca estándar.
"""
import csv
import io
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SALIDA = Path(__file__).resolve().parent.parent / "inflacion.json"
AGENTE = {"User-Agent": "Mozilla/5.0 (compatible; WIQON/1.0; +https://wiqonlab.com)"}
ISO = "https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv"


def bajar(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=AGENTE), timeout=60) as r:
        return r.read().decode("utf-8")


def main():
    anio = datetime.now(timezone.utc).year
    periodos = f"{anio - 1},{anio}"
    datos = json.loads(bajar(f"https://www.imf.org/external/datamapper/api/v1/PCPIPCH?periods={periodos}"))["values"]["PCPIPCH"]
    nombres = {k: v.get("label") for k, v in json.loads(bajar("https://www.imf.org/external/datamapper/api/v1/countries"))["countries"].items()}
    filas = list(csv.DictReader(io.StringIO(bajar(ISO))))
    iso3_a_num = {f["alpha-3"]: f["country-code"] for f in filas}
    iso3_a_iso2 = {f["alpha-3"]: f["alpha-2"] for f in filas}
    paises = {}
    for iso3, serie in datos.items():
        num = iso3_a_num.get(iso3)
        if not num:
            continue  # agregados regionales del FMI (por ejemplo, "Mundo"), no son países
        valores = {int(a): v for a, v in serie.items() if v is not None}
        if anio in valores:
            paises[num] = {"iso3": iso3, "iso2": iso3_a_iso2.get(iso3), "nombre": nombres.get(iso3) or iso3, "valor": valores[anio], "anio": anio,
                           "anterior": valores.get(anio - 1)}
    salida = {"actualizado_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
              "fuente": "FMI, Perspectivas de la Economía Mundial (WEO) · indicador PCPIPCH",
              "fuente_url": "https://www.imf.org/external/datamapper/PCPIPCH@WEO",
              "anio": anio, "nota": f"Valores de {anio}: estimaciones del FMI para el año en curso.", "paises": paises}
    SALIDA.write_text(json.dumps(salida, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print("países:", len(paises), "· año", anio, "· PY", paises.get("600", {}).get("valor"), "· BR", paises.get("076", {}).get("valor"))


if __name__ == "__main__":
    main()
