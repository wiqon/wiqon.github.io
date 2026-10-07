"""
Últimos videos de los canales de YouTube de WIQON (feed RSS público de YouTube).
Guarda videos.json; la página muestra la miniatura y carga el reproductor
recién cuando la persona toca play (youtube-nocookie).
Sin dependencias: solo biblioteca estándar.
"""
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

SALIDA = Path(__file__).resolve().parent.parent / "videos.json"
CANALES = {"wiqonlab": "UCZmynZX3WMpMYb-kU0IArrw", "wiqonbr": "UCRzdECWsbHL4tdsB8vzyqoQ"}
NS = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}
MAXIMO = 8


def leer(canal_id):
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={canal_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; WIQON/1.0; +https://wiqonlab.com)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        raiz = ET.fromstring(r.read())
    videos = []
    for e in raiz.findall("a:entry", NS):
        vid = e.find("yt:videoId", NS).text
        titulo = e.find("a:title", NS).text or ""
        videos.append({"id": vid, "titulo": titulo, "publicado_utc": e.find("a:published", NS).text[:19] + "Z",
                       "short": "#shorts" in titulo.lower()})
    return videos[:MAXIMO]


def main():
    previo = {}
    if SALIDA.exists():
        try:
            previo = json.loads(SALIDA.read_text(encoding="utf-8")).get("canales", {})
        except ValueError:
            previo = {}
    canales = {}
    for nombre, cid in CANALES.items():
        try:
            canales[nombre] = {"ok": True, "url": f"https://www.youtube.com/@{nombre}", "videos": leer(cid)}
        except Exception as e:  # canal caído: últimos videos conocidos
            canales[nombre] = dict(previo.get(nombre, {"url": f"https://www.youtube.com/@{nombre}", "videos": []}), ok=False, error=type(e).__name__)
        print(nombre, len(canales[nombre]["videos"]), "videos")
    SALIDA.write_text(json.dumps({"actualizado_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "canales": canales},
                                 ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
