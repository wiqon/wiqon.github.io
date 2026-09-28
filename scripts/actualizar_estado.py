"""
Calcula el estado público de la estrategia de tendencia en BTC y lo guarda
en estado.json (lo lee la página).

Regla: estar en BTC si el último cierre DIARIO de BTC/USDT está sobre su
media de 100 días; si no, en USDT. Es la misma regla que corre en vivo.

Solo usa datos públicos de mercado (data-api.binance.vision, que no está
bloqueado para los servidores de GitHub en EE. UU.). No necesita claves y
no toca ninguna cuenta. Sin dependencias: solo biblioteca estándar.
"""
import json
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SMA = 100
URLS = [
    "https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=300",
    "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=300",
]
SALIDA = Path(__file__).resolve().parent.parent / "estado.json"


def descargar_velas():
    ultimo_error = None
    for url in URLS:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "wiqon-site"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except Exception as e:  # probar el siguiente servidor
            ultimo_error = e
    raise RuntimeError(f"No se pudieron obtener las velas: {ultimo_error}")


def main():
    velas = descargar_velas()
    ahora_ms = int(time.time() * 1000)
    # Solo velas CERRADAS: la vela diaria en curso cierra en su close_time (índice 6)
    cerradas = [v for v in velas if int(v[6]) < ahora_ms]
    cierres = [float(v[4]) for v in cerradas]
    fechas = [datetime.fromtimestamp(int(v[0]) / 1000, tz=timezone.utc).date().isoformat() for v in cerradas]

    def sma_en(i):
        return sum(cierres[i - SMA + 1:i + 1]) / SMA

    i = len(cierres) - 1
    cierre, sma = cierres[i], sma_en(i)
    en_btc = cierre > sma

    # ¿Desde cuándo está en el estado actual? (último cruce de la media)
    desde = fechas[SMA - 1]
    for j in range(i, SMA - 1, -1):
        if (cierres[j] > sma_en(j)) != en_btc:
            desde = fechas[j + 1]
            break

    estado = {
        "senal": "EN_BTC" if en_btc else "EN_USDT",
        "vela": fechas[i],
        "cierre": round(cierre, 2),
        "sma100": round(sma, 2),
        "distancia_pct": round((cierre / sma - 1) * 100, 2),
        "desde": desde,
        "actualizado_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"),
    }
    SALIDA.write_text(json.dumps(estado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(estado, ensure_ascii=False))


if __name__ == "__main__":
    main()
