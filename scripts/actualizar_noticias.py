"""
News Radar de WIQON: lee RSS públicos, filtra noticias de negocios, mercados,
fintech y criptoactivos, agrupa duplicados, prioriza Paraguay → Brasil →
Hispanoamérica y guarda noticias.json (lo lee la página).

Reglas editoriales (ver brief de rediseño):
  - Solo fuentes con RSS público. Se guarda título, fuente, fecha y enlace:
    nunca el texto de los artículos.
  - No se inventan horas: si una fuente falla, se conservan sus últimas
    noticias con su hora real y se marca la fuente como caída.
  - Se excluyen predicciones, promociones y "precio de hoy".
  - Los títulos en portugués se mantienen en portugués.
Sin dependencias: solo biblioteca estándar.

Uso:  python scripts/actualizar_noticias.py
"""
import hashlib
import json
import re
import unicodedata
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

SALIDA = Path(__file__).resolve().parent.parent / "noticias.json"
AGENTE = "Mozilla/5.0 (compatible; WIQON-NewsRadar/1.0; +https://wiqonlab.com; contacto@wiqonlab.com)"
VENTANA_DIAS = 7
TOTAL = 36
CUOTAS = {"PY": 0.45, "BR": 0.30, "LATAM": 0.25}
MAX_POR_FUENTE = 5

# filtro=True: diario general, solo pasan notas que coinciden con algún tema económico.
FUENTES = [
    {"id": "abc", "nombre": "ABC Color", "web": "https://www.abc.com.py", "region": "PY", "idioma": "es", "tipo": "medio", "filtro": True,
     "url": "https://www.abc.com.py/arc/outboundfeeds/rss/?outputType=xml"},
    {"id": "lanacion", "nombre": "La Nación", "web": "https://www.lanacion.com.py", "region": "PY", "idioma": "es", "tipo": "medio", "filtro": True,
     "url": "https://www.lanacion.com.py/arc/outboundfeeds/rss/?outputType=xml"},
    {"id": "ip", "nombre": "Agencia IP", "web": "https://www.ip.gov.py", "region": "PY", "idioma": "es", "tipo": "oficial", "filtro": True,
     "url": "https://www.ip.gov.py/ip/feed/"},
    {"id": "bcb", "nombre": "Banco Central do Brasil", "web": "https://www.bcb.gov.br", "region": "BR", "idioma": "pt", "tipo": "oficial", "filtro": False,
     "url": "https://www.bcb.gov.br/api/feed/sitebcb/sitefeeds/noticias"},
    {"id": "cvm", "nombre": "CVM", "web": "https://www.gov.br/cvm", "region": "BR", "idioma": "pt", "tipo": "oficial", "filtro": False,
     "url": "https://www.gov.br/cvm/pt-br/assuntos/noticias/RSS"},
    {"id": "infomoney", "nombre": "InfoMoney", "web": "https://www.infomoney.com.br", "region": "BR", "idioma": "pt", "tipo": "medio", "filtro": True,
     "url": "https://www.infomoney.com.br/feed/"},
    {"id": "livecoins", "nombre": "Livecoins", "web": "https://livecoins.com.br", "region": "BR", "idioma": "pt", "tipo": "medio", "filtro": True,
     "url": "https://livecoins.com.br/feed/"},
    {"id": "criptonoticias", "nombre": "CriptoNoticias", "web": "https://www.criptonoticias.com", "region": "LATAM", "idioma": "es", "tipo": "medio", "filtro": True,
     "url": "https://www.criptonoticias.com/feed/"},
    {"id": "diariobitcoin", "nombre": "DiarioBitcoin", "web": "https://www.diariobitcoin.com", "region": "LATAM", "idioma": "es", "tipo": "medio", "filtro": True,
     "url": "https://www.diariobitcoin.com/feed/"},
    {"id": "ambito", "nombre": "Ámbito", "web": "https://www.ambito.com", "region": "LATAM", "pais": "AR", "idioma": "es", "tipo": "medio", "filtro": True,
     "url": "https://www.ambito.com/rss/pages/economia.xml"},
]

# Temas (español y portugués). El orden importa: el primero que coincide es la categoría principal.
TEMAS = {
    "regulacion": r"regula|\bley\b|\blei\b|normativ|resoluci|resolu[cç][aã]o|decreto|supervis|autoriza|sanci[oó]n|multa|marco legal|seprelad|\bcoaf\b|\bcvm\b|\bcnv\b",
    "impuestos": r"impuest|tribut|\biva\b|\birp\b|declaraci[oó]n jurada|imposto|receita federal|evasi[oó]n fiscal|fisco|arancel|recaudaci",
    "criptoactivos": r"bitcoin|\bbtc\b|cripto|crypto|ethereum|blockchain|miner[ií]a de (bitcoin|cripto)|minera[cç][aã]o|binance|\betf\b|altcoin|solana",
    "stablecoins": r"stablecoin|\busdt\b|tether|\busdc\b|\bdrex\b|moneda digital|d[oó]lar digital|real digital",
    "pagos": r"\bpix\b|pagos? (digital|electr[oó]nic|instant)|billetera (digital|electr[oó]nica)|carteira digital|\bsipap\b|\bqr\b|remesas?|tarjetas? de cr[eé]dito|cart[aã]o de cr[eé]dito|meios de pagamento|medios de pago",
    "fintech": r"fintech|neobanco|banco digital|open finance|open banking|insurtech",
    "finanzas": r"\bbancos?\b|bancari|financier|financeir|cr[eé]dito|cooperativa|\bbcp\b|\bbcb\b|banco central|tasa de inter[eé]s|juros|selic|ahorro|depositos|dep[oó]sitos",
    "mercados": r"\bbolsa\b|ibovespa|merval|acciones|a[cç][oõ]es|bonos? |t[ií]tulos p[uú]blicos|tipo de cambio|cotizaci[oó]n del d[oó]lar|d[oó]lar (sube|baja|cierra|se dispara|cae)|guaran[ií] frente|mercado de c[aâ]mbio|taxa de c[aâ]mbio|mercado de valores|mercado de capitais|wall street|\bbvpasa\b",
    "macroeconomia": r"inflaci[oó]n|infla[cç][aã]o|\bpib\b|\bpbi\b|recesi[oó]n|recess[aã]o|d[eé]ficit fiscal|super[aá]vit|exportaci|exporta[cç][oõ]es|importaciones|reservas internacionales|\bfmi\b|banco mundial|deuda p[uú]blica|presupuesto general|crecimiento econ[oó]mico|mipymes",
    "empresas": r"fusiones|adquisici|aquisi[cç]|startup|resultados trimestrales|\blucro\b|facturaci[oó]n|inversi[oó]n extranjera|zona franca|maquila",
    "seguridad": r"hacke|estafa|fraude|golpe financeiro|phishing|ciberataque|ciberseg|lavado de dinero|lavagem de dinheiro|qu[aâ]ntic",
}
# Para que "regulación" cuente, el título tiene que ser financiero.
CONTEXTO_REGULACION = r"financ|banc|cripto|bitcoin|tribut|impuest|mercado|fintech|pago|bolsa|valores|\bbcp\b|\bbcb\b|\bcvm\b|\bcnv\b|cambio|seguro|ativos virtuais|activos virtuales|stablecoin|lavado|lavagem|\bdnit\b"
EXCLUIR = r"predicci[oó]n|previs[aã]o de pre[cç]o|podr[ií]a (llegar|alcanzar|subir)|pode chegar|chegar[aá] a|llegar[aá] a|vai explodir|explotar[aá]|\bpatrocinad|publicidad|\bpromo|cupom|cup[oó]n|precio de .* hoy|pre[cç]o do .* hoje|hor[oó]scopo|\bsorteo\b|ap[uú]esta|\bf[uú]tbol\b|futebol|mega-?sena|lotof[aá]cil|novela|\bbbb\b|\b(sube|cae|avanza|retrocede|repunta|rebota|cai|sobe|salta|se desploma)\b[^%]{0,40}\d+[.,]\d+ ?%|\bel \d{1,2} de (enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\b|\bem \d{1,2} de (janeiro|fevereiro|mar[cç]o|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)\b|el precio (retrocede|avanza|sube|cae)|se[nñ]ales t[eé]cnicas"
# Notas internacionales (sin vínculo regional): solo pasan si son de cripto/stablecoins.
INTERNACIONAL = r"wall street|nasdaq|\bg20\b|\bonu\b|guterres|\brusi|ucrani|\bchina\b|chinos|xi jinping|\beeuu\b|estados unidos|trump|europa|\bue\b|israel|gaza|ir[aá]n|jap[oó]n|india|alemania|francia|reino unido"
PAISES = {
    "PY": r"paraguay|asunci[oó]n|ciudad del este|alto paran[aá]|itaip[uú]|\bdnit\b|\bbcp\b",
    "BR": r"brasil|brazil|s[aã]o paulo|\bpix\b|banco central do brasil|\bbcb\b|\bcvm\b|\bdrex\b",
    "AR": r"argentin|buenos aires|\bmilei\b|merval|\bbcra\b",
    "UY": r"uruguay|montevideo", "CL": r"\bchile\b|santiago de chile", "CO": r"colombia|bogot[aá]",
    "PE": r"\bper[uú]\b|\blima\b", "MX": r"m[eé]xico|banxico", "BO": r"bolivia", "VE": r"venezuela", "EC": r"ecuador",
    "SV": r"el salvador|bukele", "PA": r"panam[aá]", "NI": r"nicaragua", "GT": r"guatemala", "HN": r"honduras", "CR": r"costa rica", "DO": r"rep[uú]blica dominicana", "CU": r"cuba",
}
NOMBRES_PAIS = {"PY": "Paraguay", "BR": "Brasil", "AR": "Argentina", "UY": "Uruguay", "CL": "Chile", "CO": "Colombia",
                "PE": "Perú", "MX": "México", "BO": "Bolivia", "VE": "Venezuela", "EC": "Ecuador", "SV": "El Salvador", "PA": "Panamá", "NI": "Nicaragua", "GT": "Guatemala", "HN": "Honduras", "CR": "Costa Rica", "DO": "Rep. Dominicana", "CU": "Cuba", "LATAM": "Regional", "INT": "Internacional"}
PALABRAS_VACIAS = set("el la los las de del en y a un una por para con que se su sus al lo o e es son como mas mais do da dos das no na nos nas em um uma ao os as pelo pela".split())


def sin_acentos(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def limpiar(texto):
    texto = re.sub(r"<[^>]+>", "", texto or "")
    return re.sub(r"\s+", " ", texto).strip()


def fecha(texto):
    if not texto:
        return None
    try:
        d = parsedate_to_datetime(texto)
    except (TypeError, ValueError):
        try:
            d = datetime.fromisoformat(texto.replace("Z", "+00:00"))
        except ValueError:
            return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    return d.astimezone(timezone.utc)


def leer_feed(f):
    req = urllib.request.Request(f["url"], headers={"User-Agent": AGENTE, "Accept": "application/rss+xml, application/xml, text/xml"})
    with urllib.request.urlopen(req, timeout=30) as r:
        raiz = ET.fromstring(r.read())
    items = []
    for it in raiz.iter():
        etiqueta = it.tag.split("}")[-1]
        if etiqueta not in ("item", "entry"):
            continue
        campos = {c.tag.split("}")[-1]: c for c in it}
        titulo = limpiar(campos["title"].text if "title" in campos else "")
        enlace = ""
        if "link" in campos:
            enlace = (campos["link"].text or campos["link"].get("href") or "").strip()
        publicado = None
        for k in ("pubDate", "published", "updated", "date"):
            if k in campos and campos[k].text:
                publicado = fecha(campos[k].text.strip())
                break
        if titulo and enlace.startswith("http") and publicado:
            items.append({"titulo": titulo, "url": enlace, "publicado": publicado})
    return items


def clasificar(titulo):
    t = titulo.lower()
    temas = [tema for tema, rx in TEMAS.items() if re.search(rx, t)]
    if "regulacion" in temas and not re.search(CONTEXTO_REGULACION, t):
        temas.remove("regulacion")
    return temas


def pais_de(titulo, f):
    t = titulo.lower()
    for codigo, rx in PAISES.items():
        if re.search(rx, t):
            return codigo
    if re.search(INTERNACIONAL, t):
        return "INT"
    return f.get("pais", {"PY": "PY", "BR": "BR"}.get(f["region"], "LATAM"))


def firma(titulo):
    palabras = re.findall(r"[a-z0-9]+", sin_acentos(titulo.lower()))
    return {p for p in palabras if p not in PALABRAS_VACIAS and len(p) > 2}


def parecidas(a, b):
    if not a or not b:
        return False
    return len(a & b) / len(a | b) >= 0.5


def puntaje(n, ahora):
    horas = (ahora - n["_dt"]).total_seconds() / 3600
    p = max(0.0, 100 - horas * 1.2)  # pierde ~29 puntos por día
    if n["tipo"] == "oficial":
        p += 25
    if n["categorias"] and n["categorias"][0] in ("regulacion", "impuestos"):
        p += 15
    if n["pais"] in ("PY", "BR") and n["region"] == "LATAM":
        p += 10  # noticia regional que toca a Paraguay o Brasil
    return p


def main():
    ahora = datetime.now(timezone.utc)
    previo = {}
    if SALIDA.exists():
        try:
            previo = json.loads(SALIDA.read_text(encoding="utf-8"))
        except ValueError:
            previo = {}
    previas_por_fuente = {}
    for n in previo.get("noticias", []):
        previas_por_fuente.setdefault(n["fuente_id"], []).append(n)
    estado_previo = {e["id"]: e for e in previo.get("fuentes", [])}

    candidatas, estado_fuentes = [], []
    for f in FUENTES:
        est = {"id": f["id"], "nombre": f["nombre"], "web": f["web"], "region": f["region"], "tipo": f["tipo"]}
        try:
            items = leer_feed(f)
            est.update(ok=True, ultima_ok=ahora.strftime("%Y-%m-%dT%H:%M:%SZ"), leidas=len(items))
            for it in items:
                if ahora - it["publicado"] > timedelta(days=VENTANA_DIAS) or it["publicado"] > ahora + timedelta(hours=2):
                    continue
                if re.search(EXCLUIR, it["titulo"].lower()):
                    continue
                cats = clasificar(it["titulo"])
                if f["filtro"] and not cats:
                    continue
                pais = pais_de(it["titulo"], f)
                cripto = any(c in cats for c in ("criptoactivos", "stablecoins"))
                if pais == "INT" and not cripto:
                    continue
                candidatas.append({
                    "id": hashlib.sha1(it["url"].encode()).hexdigest()[:12],
                    "titulo": it["titulo"], "url": it["url"], "idioma": f["idioma"],
                    "fuente_id": f["id"], "fuente": f["nombre"], "fuente_web": f["web"], "tipo": f["tipo"],
                    "region": f["region"], "pais": pais,
                    "categorias": cats or ["criptoactivos" if f["id"] in ("livecoins", "criptonoticias", "diariobitcoin") else "mercados"],
                    "publicado_utc": it["publicado"].strftime("%Y-%m-%dT%H:%M:%SZ"), "_dt": it["publicado"],
                })
        except Exception as e:  # fuente caída: conservar lo último conocido, con su hora real
            ant = estado_previo.get(f["id"], {})
            est.update(ok=False, error=type(e).__name__, ultima_ok=ant.get("ultima_ok"))
            for n in previas_por_fuente.get(f["id"], []):
                n = dict(n)
                n["_dt"] = datetime.fromisoformat(n["publicado_utc"].replace("Z", "+00:00"))
                n.pop("relacionadas", None)
                if ahora - n["_dt"] <= timedelta(days=VENTANA_DIAS):
                    candidatas.append(n)
        estado_fuentes.append(est)

    for n in candidatas:
        if n["region"] == "PY" and n["pais"] not in ("PY",):
            n["region"] = "BR" if n["pais"] == "BR" else "LATAM"

    # Agrupar historias repetidas: queda la de mejor puntaje y las demás como fuentes adicionales
    for n in candidatas:
        n["_firma"] = firma(n["titulo"])
        n["_p"] = puntaje(n, ahora)
    candidatas.sort(key=lambda n: -n["_p"])
    grupos = []
    for n in candidatas:
        for g in grupos:
            if parecidas(g["_firma"], n["_firma"]) or g["url"] == n["url"]:
                if g["url"] != n["url"] and all(r["url"] != n["url"] for r in g["relacionadas"]):
                    g["relacionadas"].append({"fuente": n["fuente"], "url": n["url"], "titulo": n["titulo"], "idioma": n["idioma"]})
                break
        else:
            n["relacionadas"] = []
            grupos.append(n)

    # Cuotas por región (las que sobran se reparten entre las demás)
    por_region = {}
    for r in CUOTAS:
        cuenta, lista = {}, []
        for g in grupos:
            if g["region"] == r and cuenta.get(g["fuente_id"], 0) < MAX_POR_FUENTE:
                cuenta[g["fuente_id"]] = cuenta.get(g["fuente_id"], 0) + 1
                lista.append(g)
        por_region[r] = lista
    elegidas, sobrante = [], 0
    for r, cuota in CUOTAS.items():
        lugar = round(TOTAL * cuota)
        elegidas += por_region[r][:lugar]
        sobrante += max(0, lugar - len(por_region[r]))
    if sobrante:
        cuenta = {}
        for g in elegidas:
            cuenta[g["fuente_id"]] = cuenta.get(g["fuente_id"], 0) + 1
        resto = [g for g in sorted(grupos, key=lambda n: -n["_p"]) if g not in elegidas and cuenta.get(g["fuente_id"], 0) < MAX_POR_FUENTE + 2]
        elegidas += resto[:sobrante]
    orden = {"PY": 0, "BR": 1, "LATAM": 2}
    elegidas.sort(key=lambda n: (orden[n["region"]], -n["_p"]))

    salida = {
        "actualizado_utc": ahora.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "ventana_dias": VENTANA_DIAS,
        "fuentes": estado_fuentes,
        "noticias": [{k: v for k, v in n.items() if not k.startswith("_")} | {"pais_nombre": NOMBRES_PAIS.get(n["pais"], n["pais"])}
                     for n in elegidas],
    }
    SALIDA.write_text(json.dumps(salida, ensure_ascii=False, indent=1), encoding="utf-8")
    ok = sum(1 for e in estado_fuentes if e["ok"])
    print(f"noticias: {len(elegidas)} · fuentes ok: {ok}/{len(estado_fuentes)} · "
          + " · ".join(f"{r}: {sum(1 for n in elegidas if n['region'] == r)}" for r in CUOTAS))


if __name__ == "__main__":
    main()
