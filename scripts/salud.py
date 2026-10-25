"""
Salud de los datos de wiqonlab.com: revisa cada archivo que genera el sitio y escribe salud.json.

Por módulo informa la fuente, cuándo llegó el último dato bueno, cuántos minutos tiene y un estado calculado
con umbrales propios de cada fuente (nunca «en vivo» por tener la página abierta):
  al_dia     el dato llegó dentro del plazo esperado
  atrasado   pasó el plazo normal, o una parte de las fuentes no respondió
  caido      hace demasiado que no llega un dato nuevo (se sigue mostrando el último, con su fecha)
  error      el archivo falta o no tiene el formato esperado
«general» es el peor estado de todos. La página (assets/v4.js) y el aviso de n8n leen este archivo.

Uso:  python scripts/salud.py            (al final de cada corrida de publicar.yml)
Sin dependencias: solo biblioteca estándar.
"""
import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "salud.json"
ORDEN = {"al_dia": 0, "atrasado": 1, "caido": 2, "error": 3}

# plazo normal y plazo máximo en minutos, según cada cuánto publica la fuente
MODULOS = {
    "radar": dict(archivo="noticias.json", nombre="Radar de noticias", fuente="RSS de 10 medios y organismos",
                  fuente_url="https://wiqonlab.com/#radar", atrasado=90, caido=360),
    "cambio": dict(archivo="cambio.json", nombre="Tipo de cambio oficial", fuente="BCP, BCB, BCRA y Banco de la República",
                   fuente_url="https://www.bcp.gov.py/webapps/web/cotizacion/monedas", atrasado=120, caido=720),
    "defi": dict(archivo="defi.json", nombre="Dólares digitales", fuente="DefiLlama", fuente_url="https://defillama.com",
                 atrasado=120, caido=1440),
    "inflacion": dict(archivo="inflacion.json", nombre="Inflación por país", fuente="FMI (WEO)",
                      fuente_url="https://www.imf.org/external/datamapper/PCPIPCH@WEO", atrasado=3 * 1440, caido=10 * 1440),
    "videos": dict(archivo="videos.json", nombre="Videos", fuente="YouTube (RSS)", fuente_url="https://www.youtube.com/@wiqonlab",
                   atrasado=1440, caido=4 * 1440),
    "estrategia": dict(archivo="estado.json", nombre="Estado de la estrategia", fuente="Binance (velas diarias, datos públicos)",
                       fuente_url="https://data-api.binance.vision", atrasado=26 * 60, caido=50 * 60),
}
CAMBIO_DIAS_HABILES = 3   # los bancos centrales no publican fines de semana ni feriados


def fecha_utc(texto):
    """Acepta «2026-10-25T21:53:00Z», «2026-10-25 21:53» o con zona horaria."""
    t = str(texto).strip().replace(" ", "T")
    if len(t) == 16:
        t += ":00"
    d = datetime.fromisoformat(t.replace("Z", "+00:00"))
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def dias_habiles_entre(desde, hasta):
    n, d = 0, desde
    while d < hasta:
        d += timedelta(days=1)
        if d.weekday() < 5:
            n += 1
    return n


def por_edad(minutos, cfg):
    if minutos > cfg["caido"]:
        return "caido"
    if minutos > cfg["atrasado"]:
        return "atrasado"
    return "al_dia"


def peor(*estados):
    return max(estados, key=ORDEN.get)


def detalles(clave, datos, ahora):
    """Revisa el formato del archivo y devuelve (estado extra, lista de avisos)."""
    estado, avisos = "al_dia", []
    if clave == "radar":
        fuentes, notas = datos["fuentes"], datos["noticias"]
        assert isinstance(notas, list) and all("titulo" in n and "url" in n for n in notas)
        caidas = [f["nombre"] for f in fuentes if not f.get("ok")]
        if caidas:
            avisos.append(f"{len(caidas)} de {len(fuentes)} fuentes sin responder: {', '.join(caidas)}")
            estado = "atrasado" if len(caidas) < len(fuentes) else "caido"
        if not notas:
            avisos.append("sin noticias en la ventana")
            estado = peor(estado, "atrasado")
    elif clave == "cambio":
        for f in datos["fuentes"]:
            assert f["valores"] and all(isinstance(v["valor"], (int, float)) for v in f["valores"])
            if not f.get("ok"):
                avisos.append(f"{f['institucion']}: no respondió, se muestra el último valor conocido ({f['fecha']})")
                estado = peor(estado, "atrasado")
            elif dias_habiles_entre(date.fromisoformat(f["fecha"]), ahora.date()) > CAMBIO_DIAS_HABILES:
                avisos.append(f"{f['institucion']}: sin cotización nueva desde {f['fecha']}")
                estado = peor(estado, "atrasado")
    elif clave == "defi":
        assert datos["stablecoins"]["total"] > 0 and datos["rendimientos"] and datos["cadenas"]
    elif clave == "inflacion":
        assert len(datos["paises"]) > 100
    elif clave == "videos":
        sin = [k for k, c in datos["canales"].items() if not c.get("ok")]
        if sin:
            avisos.append("canales sin responder: " + ", ".join(sin))
            estado = "atrasado"
    elif clave == "estrategia":
        assert datos["senal"] in ("EN_BTC", "EN_USDT") and datos["sma100"] > 0
        vela = date.fromisoformat(datos["vela"])
        if (ahora.date() - vela).days > 2:
            avisos.append(f"la última vela diaria es del {datos['vela']}")
            estado = "atrasado"
    return estado, avisos


def revisar(clave, cfg, ahora):
    base = {"nombre": cfg["nombre"], "fuente": cfg["fuente"], "fuente_url": cfg["fuente_url"],
            "plazo_min": cfg["atrasado"], "caido_min": cfg["caido"], "archivo": cfg["archivo"]}
    ruta = RAIZ / cfg["archivo"]
    try:
        datos = json.loads(ruta.read_text(encoding="utf-8"))
        actualizado = fecha_utc(datos["actualizado_utc"])
    except FileNotFoundError:
        return base | {"estado": "error", "avisos": ["falta el archivo"]}
    except (ValueError, KeyError, TypeError):
        return base | {"estado": "error", "avisos": ["el archivo no tiene el formato esperado"]}
    edad = max(0, round((ahora - actualizado).total_seconds() / 60))
    try:
        extra, avisos = detalles(clave, datos, ahora)
    except (AssertionError, KeyError, TypeError, ValueError):
        extra, avisos = "error", ["el archivo no tiene el formato esperado"]
    estado = peor(por_edad(edad, cfg), extra)
    if por_edad(edad, cfg) != "al_dia":
        avisos.insert(0, f"último dato hace {edad // 60} h {edad % 60} min")
    return base | {"estado": estado, "actualizado_utc": actualizado.strftime("%Y-%m-%dT%H:%M:%SZ"),
                   "edad_min": edad, "avisos": avisos}


def main(ahora=None):
    ahora = ahora or datetime.now(timezone.utc)
    modulos = {k: revisar(k, cfg, ahora) for k, cfg in MODULOS.items()}
    salida = {"generado_utc": ahora.strftime("%Y-%m-%dT%H:%M:%SZ"),
              "general": peor(*(m["estado"] for m in modulos.values())),
              "modulos": modulos}
    SALIDA.write_text(json.dumps(salida, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"salud: {salida['general']} · " + " · ".join(f"{k}: {m['estado']}" for k, m in modulos.items()))
    return salida


if __name__ == "__main__":
    main()
