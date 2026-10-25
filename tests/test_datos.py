"""Pruebas de los lectores de datos y del chequeo de salud (corren en publicar.yml antes de publicar).

    python -m pytest tests -q
"""
import json
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import actualizar_noticias as N  # noqa: E402
import salud as S  # noqa: E402

AHORA = datetime(2026, 10, 27, 15, 0, tzinfo=timezone.utc)   # martes


def hace(minutos):
    return (AHORA - timedelta(minutes=minutos)).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------- noticias
def test_https_corrige_y_descarta():
    assert N.https("http://medio.com/a.jpg") == "https://medio.com/a.jpg"
    assert N.https("//cdn.medio.com/a.jpg?x=1&amp;y=2") == "https://cdn.medio.com/a.jpg?x=1&y=2"
    assert N.https("data:image/png;base64,AAA") == ""
    assert N.https("") == ""


@pytest.mark.parametrize("item, esperada", [
    ('<item xmlns:media="http://search.yahoo.com/mrss/"><title>t</title><media:content url="https://a.com/1.jpg" medium="image"/></item>', "https://a.com/1.jpg"),
    ('<item><title>t</title><enclosure url="http://a.com/2.png" type="image/png"/></item>', "https://a.com/2.png"),
    ('<item><title>t</title><enclosure url="https://a.com/audio.mp3" type="audio/mpeg"/></item>', ""),
    ('<item><title>t</title><description>&lt;p&gt;&lt;img src="https://a.com/3.webp" /&gt;&lt;/p&gt;</description></item>', "https://a.com/3.webp"),
    ('<item><title>t</title><description>sin imagen</description></item>', ""),
])
def test_imagen_del_rss(item, esperada):
    assert N.imagen_de(ET.fromstring(item)) == esperada


def test_og_image_en_ambos_ordenes():
    assert N.og_de_html('<meta property="og:image" content="https://m.com/f.jpg">') == "https://m.com/f.jpg"
    assert N.og_de_html("<meta content='http://m.com/g.jpg' property='og:image'>") == "https://m.com/g.jpg"
    assert N.og_de_html('<meta name="twitter:image" content="https://m.com/t.jpg">') == "https://m.com/t.jpg"
    assert N.og_de_html("<html><title>nada</title></html>") == ""


def test_noticias_europeas_no_son_de_paraguay():
    assert N.pais_de("Miles protestan en Praga contra la ley", {"region": "PY"}) == "INT"
    assert N.pais_de("El BCP mantiene la tasa de política monetaria", {"region": "PY"}) == "PY"


def test_excluye_predicciones_de_precio():
    assert N.re.search(N.EXCLUIR, "bitcoin podría llegar a 200.000 dólares")


# ---------------------------------------------------------------- salud
def escribir(tmp, nombre, datos):
    (tmp / nombre).write_text(json.dumps(datos), encoding="utf-8")


@pytest.fixture
def sitio(tmp_path, monkeypatch):
    """Un sitio con todos los archivos al día; cada prueba rompe lo que necesita."""
    monkeypatch.setattr(S, "RAIZ", tmp_path)
    monkeypatch.setattr(S, "SALIDA", tmp_path / "salud.json")
    escribir(tmp_path, "noticias.json", {"actualizado_utc": hace(10), "fuentes": [{"nombre": "ABC", "ok": True}, {"nombre": "BCB", "ok": True}],
                                         "noticias": [{"titulo": "t", "url": "https://x"}]})
    escribir(tmp_path, "cambio.json", {"actualizado_utc": hace(10), "fuentes": [
        {"institucion": "BCP", "ok": True, "fecha": "2026-10-26", "valores": [{"valor": 5734.31}]}]})
    escribir(tmp_path, "defi.json", {"actualizado_utc": (AHORA - timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M"),
                                     "stablecoins": {"total": 3e11}, "rendimientos": [1], "cadenas": [1]})
    escribir(tmp_path, "inflacion.json", {"actualizado_utc": hace(60), "paises": {str(i): {} for i in range(150)}})
    escribir(tmp_path, "videos.json", {"actualizado_utc": hace(60), "canales": {"wiqonlab": {"ok": True}}})
    escribir(tmp_path, "estado.json", {"actualizado_utc": "2026-10-27 04:46", "senal": "EN_BTC", "sma100": 75330.9, "vela": "2026-10-26"})
    return tmp_path


def test_todo_al_dia(sitio):
    s = S.main(AHORA)
    assert s["general"] == "al_dia"
    assert all(m["estado"] == "al_dia" for m in s["modulos"].values())
    assert json.loads((sitio / "salud.json").read_text(encoding="utf-8"))["general"] == "al_dia"


def test_dato_viejo_es_atrasado_y_luego_caido(sitio):
    datos = json.loads((sitio / "noticias.json").read_text(encoding="utf-8"))
    datos["actualizado_utc"] = hace(120)
    escribir(sitio, "noticias.json", datos)
    assert S.main(AHORA)["modulos"]["radar"]["estado"] == "atrasado"
    datos["actualizado_utc"] = hace(400)
    escribir(sitio, "noticias.json", datos)
    m = S.main(AHORA)["modulos"]["radar"]
    assert m["estado"] == "caido" and m["avisos"][0].startswith("último dato hace 6 h")


def test_fuente_caida_marca_atrasado(sitio):
    datos = json.loads((sitio / "noticias.json").read_text(encoding="utf-8"))
    datos["fuentes"][1]["ok"] = False
    escribir(sitio, "noticias.json", datos)
    m = S.main(AHORA)["modulos"]["radar"]
    assert m["estado"] == "atrasado" and "BCB" in m["avisos"][0]


def test_archivo_roto_o_faltante_es_error(sitio):
    (sitio / "defi.json").write_text("{no es json", encoding="utf-8")
    (sitio / "videos.json").unlink()
    escribir(sitio, "estado.json", {"actualizado_utc": "2026-10-27 04:46", "senal": "COMPRAR", "sma100": 1, "vela": "2026-10-26"})
    s = S.main(AHORA)
    assert s["modulos"]["defi"]["estado"] == "error"
    assert s["modulos"]["videos"]["avisos"] == ["falta el archivo"]
    assert s["modulos"]["estrategia"]["estado"] == "error"
    assert s["general"] == "error"


def test_cambio_respeta_fines_de_semana(sitio):
    # cotización del viernes 23: el martes 27 son 2 días hábiles, todavía al día
    escribir(sitio, "cambio.json", {"actualizado_utc": hace(10), "fuentes": [
        {"institucion": "BCP", "ok": True, "fecha": "2026-10-23", "valores": [{"valor": 5734.31}]}]})
    assert S.main(AHORA)["modulos"]["cambio"]["estado"] == "al_dia"
    escribir(sitio, "cambio.json", {"actualizado_utc": hace(10), "fuentes": [
        {"institucion": "BCP", "ok": True, "fecha": "2026-10-20", "valores": [{"valor": 5734.31}]}]})
    assert S.main(AHORA)["modulos"]["cambio"]["estado"] == "atrasado"


def test_vela_de_estrategia_vieja(sitio):
    escribir(sitio, "estado.json", {"actualizado_utc": "2026-10-27 04:46", "senal": "EN_BTC", "sma100": 75330.9, "vela": "2026-10-22"})
    m = S.main(AHORA)["modulos"]["estrategia"]
    assert m["estado"] == "atrasado" and "2026-10-22" in m["avisos"][0]
