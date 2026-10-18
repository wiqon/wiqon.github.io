"""
Panel de stablecoins y DeFi para la web de WIQON. Guarda defi.json con datos públicos de DefiLlama:

  · Stablecoins en dólares: total en circulación, historial de 180 días y las principales monedas
    (circulación y variación de 7 y 30 días).
  · Rendimientos de stablecoins: los fondos más grandes (más de US$ 300 millones depositados), ordenados
    por tamaño y no por rendimiento, separando el rendimiento base del pagado en premios.
  · Cadenas: dónde está depositado el dinero de DeFi (TVL).

No se inventan valores: si una fuente falla, se conserva la parte anterior de defi.json.
Sin dependencias: solo biblioteca estándar.
"""
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SALIDA = Path(__file__).resolve().parent.parent / "defi.json"
AGENTE = "Mozilla/5.0 (compatible; WIQON/1.0; +https://wiqonlab.com; contacto@wiqonlab.com)"


def bajar(url):
    req = urllib.request.Request(url, headers={"User-Agent": AGENTE})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read().decode("utf-8"))


def nombre(slug):
    """'sky-lending' → 'Sky Lending' (DefiLlama identifica los protocolos por slug)."""
    especiales = {"aave-v3": "Aave V3", "compound-v3": "Compound V3", "ethena-usde": "Ethena", "blackrock-buidl": "BlackRock BUIDL", "makerdao": "MakerDAO"}
    return especiales.get(slug, " ".join(p.capitalize() if not p[:1].isdigit() else p for p in slug.split("-")))


def usd(d):
    return round(float((d or {}).get("peggedUSD") or 0), 2)


def stablecoins():
    activos = [a for a in bajar("https://stablecoins.llama.fi/stablecoins?includePrices=false")["peggedAssets"] if a.get("pegType") == "peggedUSD"]
    activos.sort(key=lambda a: -usd(a.get("circulating")))
    top = []
    for a in activos[:6]:
        ahora, sem, mes = usd(a.get("circulating")), usd(a.get("circulatingPrevWeek")), usd(a.get("circulatingPrevMonth"))
        top.append({"simbolo": a["symbol"], "nombre": a["name"], "respaldo": a.get("pegMechanism", ""), "circulacion": ahora,
                    "var_7d": round((ahora / sem - 1) * 100, 2) if sem else None, "var_30d": round((ahora / mes - 1) * 100, 2) if mes else None})
    hist = bajar("https://stablecoins.llama.fi/stablecoincharts/all")
    serie = [[datetime.fromtimestamp(int(p["date"]), timezone.utc).strftime("%Y-%m-%d"), round(usd(p.get("totalCirculating")) / 1e9, 2)] for p in hist[-180:]]
    total = serie[-1][1] * 1e9 if serie else sum(t["circulacion"] for t in top)
    hace30 = serie[-31][1] * 1e9 if len(serie) > 31 else None
    return {"total": round(total, 2), "var_30d": round((total / hace30 - 1) * 100, 2) if hace30 else None, "historial_mil_millones": serie, "principales": top}


def rendimientos():
    fondos = [p for p in bajar("https://yields.llama.fi/pools")["data"]
              if p.get("stablecoin") and (p.get("tvlUsd") or 0) > 3e8 and p.get("exposure") == "single" and (p.get("apy") or 0) > 0]
    fondos.sort(key=lambda p: -(p.get("tvlUsd") or 0))
    return [{"protocolo": nombre(p["project"]), "moneda": p["symbol"], "red": p["chain"], "apy": round(p.get("apy") or 0, 2),
             "apy_base": round(p.get("apyBase") or 0, 2), "apy_premios": round(p.get("apyReward") or 0, 2),
             "tvl": round(p["tvlUsd"], 0), "enlace": f"https://defillama.com/yields/pool/{p['pool']}"} for p in fondos[:10]]


def cadenas():
    lista = sorted(bajar("https://api.llama.fi/v2/chains"), key=lambda c: -(c.get("tvl") or 0))
    return [{"nombre": c["name"], "tvl": round(c.get("tvl") or 0, 0)} for c in lista[:8]]


def main():
    try:
        datos = json.loads(SALIDA.read_text(encoding="utf-8"))
    except Exception:
        datos = {}
    for clave, funcion in (("stablecoins", stablecoins), ("rendimientos", rendimientos), ("cadenas", cadenas)):
        try:
            datos[clave] = funcion()
            print(f"OK {clave}")
        except Exception as e:  # se conserva el último dato conocido
            print(f"FALLO {clave}: {e}")
    datos["actualizado_utc"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    datos["fuente"] = {"nombre": "DefiLlama", "url": "https://defillama.com"}
    SALIDA.write_text(json.dumps(datos, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"defi.json · {SALIDA.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
