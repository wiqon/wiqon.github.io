"""
Trae al sitio los resultados del comparador y las fichas estándar del laboratorio (github.com/wiqon/wiqon-lab).

    python scripts/importar_comparador.py [carpeta del repo wiqon-lab]     (por defecto C:\\agm-backtesting-lab)

Escribe en scripts/datos_lab/:
  comparador.json          métricas por estrategia y período (copia de resultados/comparador.json)
  comparador_serie.json    curvas semanales con base 100 y caída desde el máximo (calculada sobre la curva DIARIA)
  fichas/<id>.json         fichas estándar de los experimentos
"""
import csv
import json
import shutil
import sys
from pathlib import Path

LAB = Path(sys.argv[1] if len(sys.argv) > 1 else r"C:\agm-backtesting-lab")
RES = LAB / "resultados"
DESTINO = Path(__file__).resolve().parent / "datos_lab"
CLAVES = ("hold", "tendencia", "grid", "dca_bot")


def main():
    filas = list(csv.DictReader(open(RES / "comparador_serie.csv", encoding="utf-8")))
    diaria = {k: [float(f[k]) for f in filas] for k in CLAVES}
    fechas = [f["fecha"] for f in filas]
    caida = {}
    for k, s in diaria.items():
        maximo, dd = 0.0, []
        for v in s:
            maximo = max(maximo, v)
            dd.append(round((v / maximo - 1) * 100, 1))
        caida[k] = dd
    idx = list(range(0, len(fechas), 7))
    if idx[-1] != len(fechas) - 1:
        idx.append(len(fechas) - 1)
    serie = {"fechas": [fechas[i] for i in idx], "base100": {k: [diaria[k][i] for i in idx] for k in CLAVES},
             "caida": {k: [min(caida[k][max(0, a + 1):b + 1]) for a, b in zip([-1] + idx[:-1], idx)] for k in CLAVES},
             "nota": "semanal; la caída se calcula sobre la curva diaria y cada punto es la peor de su semana"}
    DESTINO.mkdir(exist_ok=True)
    (DESTINO / "comparador_serie.json").write_text(json.dumps(serie, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    shutil.copyfile(RES / "comparador.json", DESTINO / "comparador.json")
    (DESTINO / "fichas").mkdir(exist_ok=True)
    for f in sorted((RES / "fichas").glob("*.json")):
        shutil.copyfile(f, DESTINO / "fichas" / f.name)
    comp = json.loads((DESTINO / "comparador.json").read_text(encoding="utf-8"))
    print(f"{len(idx)} semanas ({fechas[0]} → {fechas[-1]}), {len(list((DESTINO / 'fichas').glob('*.json')))} fichas,",
          {k: v["metricas"]["completo"]["cagr_pct"] for k, v in comp["estrategias"].items()})


if __name__ == "__main__":
    main()
