"""
Últimos videos de los canales de YouTube de WIQON vía YouTube Data API v3.

El RSS público (feeds/videos.xml) empezó a devolver 404 a los fetchers
automáticos (GitHub Actions y otras IPs de datacenter), así que se usa la API
oficial. Necesita la variable de entorno YOUTUBE_API_KEY (secret en GitHub
Actions). Si falta la clave o un canal no responde, se conservan los últimos
videos conocidos (ok:false) y la antigüedad del módulo la mide `salud.py` por
el último refresco EXITOSO, no por la hora de escritura.

Guarda videos.json; la página muestra la miniatura y carga el reproductor
recién cuando la persona toca play (youtube-nocookie).
Sin dependencias externas: solo biblioteca estándar.
"""
import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SALIDA = Path(__file__).resolve().parent.parent / "videos.json"
CANALES = {"wiqonlab": "UCZmynZX3WMpMYb-kU0IArrw", "wiqonbr": "UCRzdECWsbHL4tdsB8vzyqoQ"}
API_KEY = os.environ.get("YOUTUBE_API_KEY", "").strip()
MAXIMO = 8


def _playlist_subidas(canal_id):
    """La lista de 'subidas' de un canal UC... es UU... (mismo sufijo)."""
    return "UU" + canal_id[2:]


def leer(canal_id):
    if not API_KEY:
        raise RuntimeError("falta YOUTUBE_API_KEY")
    params = urllib.parse.urlencode({
        "part": "snippet", "maxResults": MAXIMO,
        "playlistId": _playlist_subidas(canal_id), "key": API_KEY,
    })
    url = "https://www.googleapis.com/youtube/v3/playlistItems?" + params
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        datos = json.load(r)
    videos = []
    for it in datos.get("items", []):
        sn = it.get("snippet", {})
        vid = sn.get("resourceId", {}).get("videoId")
        if not vid:
            continue
        titulo = sn.get("title", "") or ""
        pub = sn.get("publishedAt", "")
        publicado = (pub[:19] + "Z") if pub else ""
        videos.append({"id": vid, "titulo": titulo, "publicado_utc": publicado,
                       "short": "#shorts" in titulo.lower()})
    return videos[:MAXIMO]


def main():
    previo_doc = {}
    if SALIDA.exists():
        try:
            previo_doc = json.loads(SALIDA.read_text(encoding="utf-8"))
        except ValueError:
            previo_doc = {}
    previo = previo_doc.get("canales", {})

    canales = {}
    algun_ok = False
    for nombre, cid in CANALES.items():
        try:
            canales[nombre] = {"ok": True, "url": f"https://www.youtube.com/@{nombre}", "videos": leer(cid)}
            algun_ok = True
        except Exception as e:  # canal caído o sin clave: se conservan los últimos videos conocidos
            canales[nombre] = dict(previo.get(nombre, {"url": f"https://www.youtube.com/@{nombre}", "videos": []}),
                                   ok=False, error=type(e).__name__)
        print(nombre, len(canales[nombre]["videos"]), "videos", "" if canales[nombre]["ok"] else "(sin refrescar)")

    # La antigüedad mide el último refresco EXITOSO: si NADA respondió, se conserva
    # la marca anterior para que salud.py la vea envejecer (atrasado → caído).
    ahora = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    actualizado = ahora if algun_ok else (previo_doc.get("actualizado_utc") or ahora)

    SALIDA.write_text(json.dumps({"actualizado_utc": actualizado, "canales": canales},
                                 ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
