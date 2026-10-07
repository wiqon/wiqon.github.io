"""
Genera index.html (español) y br/index.html (português) desde UNA plantilla editorial.

Uso:  python scripts/construir_web.py
Datos dinámicos (los completa el navegador): noticias.json, cambio.json, videos.json,
estado.json (ver scripts/actualizar_*.py). Fotos: assets/fotos/creditos.json.
"""
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FOTOS = json.loads((RAIZ / "assets" / "fotos" / "creditos.json").read_text(encoding="utf-8"))

TV = "https://www.tradingview.com/?aff_id=1171961&aff_sub=web&source=wiqonlab"
BINANCE = "https://www.binance.com/register?ref=WDAVWR75"
WA = "https://wa.me/595987685651"
LAB = "https://github.com/wiqon/wiqon-lab"
DNIT_RG47 = "https://www.dnit.gov.py/web/portal-institucional/w/la-dnit-establece-obligaci%C3%B3n-de-informar-las-transacciones-con-criptoactivos"
BCB_RES = "https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolu%C3%A7%C3%A3o%20BCB&numero={n}"


def credito(clave, txt_foto, txt_lic):
    f = FOTOS[clave]
    return (f'{txt_foto}: <a href="{f["fuente"]}" target="_blank" rel="noopener">{f["autor"]}</a>, '
            f'<a href="{f["licencia_url"]}" target="_blank" rel="noopener">{f["licencia"]}</a> {txt_lic}')


PLANTILLA = """<!doctype html>
<html lang="{{lang}}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{titulo}}</title>
<meta name="description" content="{{descripcion}}">
<meta property="og:title" content="{{titulo}}">
<meta property="og:description" content="{{descripcion}}">
<meta property="og:image" content="https://wiqonlab.com/assets/og.png">
<meta property="og:url" content="{{url}}">
<meta property="og:type" content="website">
<meta property="og:locale" content="{{og_locale}}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#070b10">
<link rel="canonical" href="{{url}}">
<link rel="alternate" hreflang="es" href="https://wiqonlab.com/">
<link rel="alternate" hreflang="pt-BR" href="https://wiqonlab.com/br/">
<link rel="icon" href="{{r}}assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;1,9..144,400&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{{r}}assets/v3.css">
</head>
<body data-estado="{{r}}estado.json" data-raiz="{{r}}">
<a class="oculto" href="#radar">{{saltar}}</a>

<div class="barra" role="region" aria-label="{{barra_aria}}">
  <div class="c">
    <span class="hoy" id="hoy"></span>
    <span>BTC <b id="b-btc">—</b> <span class="fte">Binance</span></span>
    <span>USD/PYG <b id="b-pyg">—</b> <span class="fte">BCP</span></span>
    <span>USD/BRL <b id="b-brl">—</b> <span class="fte">BCB PTAX</span></span>
  </div>
</div>
<div class="franja" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>

<nav class="nav" aria-label="{{nav_aria}}">
  <div class="c">
    <a class="marca" href="{{inicio}}"><img src="{{r}}assets/logo.png" alt="">WIQON</a>
    <div class="nav-l">
      <a href="#radar">{{n_radar}}</a><a href="#cambio">{{n_cambio}}</a><a href="#laboratorio">{{n_lab}}</a>
      <a href="#shield">Shield</a><a href="#videos-s">{{n_videos}}</a><a href="#nosotros">{{n_nos}}</a>
    </div>
    <div class="nav-d">
      <span class="idioma"><a {{es_on}} href="{{r}}" lang="es">Español</a> · <a {{br_on}} href="{{r}}br/" lang="pt-BR">Brasil PT-BR</a></span>
      <a class="btn p ch" href="#radar">{{n_cta}}</a>
    </div>
  </div>
</nav>

<main>
<header class="hero">
  <div class="c">
    <div>
      <span class="lugar">{{lugar}}</span>
      <h1>{{h1}}</h1>
      <p class="baj">{{bajada}}</p>
      <div class="acc"><a class="btn p" href="#radar">{{cta1}}</a><a class="btn" href="#nosotros">{{cta2}}</a></div>
      <div class="dia">
        <span class="et">{{dato_et}}</span><p id="dato-dia">{{cargando}}</p><small id="dato-dia-f"></small>
      </div>
    </div>
    <figure class="foto">
      <img src="{{r}}assets/fotos/puente2.jpg" alt="{{foto1_alt}}" width="1600" height="1200">
      <figcaption>{{foto1_cap}} {{foto1_cred}}</figcaption>
    </figure>
  </div>
</header>

<section class="s" id="radar" data-prioridad="{{prioridad}}" aria-labelledby="radar-t">
  <div class="c">
    <div class="cab">
      <div><span class="vol">News Radar</span><h2 class="t" id="radar-t">{{radar_h2}}</h2><p>{{radar_p}}</p></div>
      <div class="meta" id="radar-info" aria-live="polite">{{cargando}}</div>
    </div>
    <div class="filtros" role="group" aria-label="{{filtros_aria}}">
      <div class="grupo"><span>{{f_region}}</span>
        <button class="chip" data-f="region:todas" aria-pressed="true">{{f_todas}}</button>
        <button class="chip" data-f="region:PY" aria-pressed="false">Paraguay</button>
        <button class="chip" data-f="region:BR" aria-pressed="false">Brasil</button>
        <button class="chip" data-f="region:LATAM" aria-pressed="false">{{f_la}}</button>
      </div>
      <div class="grupo"><span>{{f_periodo}}</span>
        <button class="chip" data-f="horas:24" aria-pressed="false">24 h</button>
        <button class="chip" data-f="horas:72" aria-pressed="true">{{f_3d}}</button>
        <button class="chip" data-f="horas:168" aria-pressed="false">{{f_7d}}</button>
      </div>
      <div class="grupo"><label for="f-idioma"><span>{{f_idioma}}</span></label>
        <select class="sel" id="f-idioma" data-s="idioma"><option value="todos">{{f_todos}}</option><option value="es">Español</option><option value="pt">Português</option></select>
      </div>
      <div class="grupo"><label for="f-cat"><span>{{f_cat}}</span></label>
        <select class="sel" id="f-cat" data-s="cat">{{opciones_cat}}</select>
      </div>
    </div>
    <p class="aviso-r" id="radar-aviso" aria-live="polite"></p>
    <div class="radar">
      <div><div class="principal" id="radar-principal"></div><p class="meta" style="margin-top:14px">{{radar_nota}}</p></div>
      <div><ul class="lista-n" id="radar-lista" aria-live="polite"></ul><button class="btn ch ver-mas" id="radar-mas" hidden>{{ver_mas}}</button></div>
    </div>
  </div>
</section>

<section class="s alt" id="cambio" aria-labelledby="cambio-t">
  <div class="c">
    <div class="cab">
      <div><span class="vol">{{cambio_vol}}</span><h2 class="t" id="cambio-t">{{cambio_h2}}</h2><p>{{cambio_p}}</p></div>
      <div class="meta" id="cambio-act"></div>
    </div>
    <div class="cambio-g">
      <table class="tabla" id="tabla-cambio">
        <thead><tr><th>{{tc_moneda}}</th><th class="v">{{tc_valor}}</th><th class="ocultar-m">{{tc_fuente}}</th><th>{{tc_fecha}}</th></tr></thead>
        <tbody><tr><td colspan="4" class="u">{{cargando}}</td></tr></tbody>
      </table>
      <div class="nota-c">{{cambio_nota}}</div>
    </div>
  </div>
</section>

<section class="s" id="observando" aria-labelledby="obs-t">
  <div class="c">
    <div class="cab"><div><span class="vol">{{obs_vol}}</span><h2 class="t" id="obs-t">{{obs_h2}}</h2><p>{{obs_p}}</p></div></div>
    <div class="obs">{{observando}}</div>
  </div>
</section>

<section class="s alt" id="historias" aria-labelledby="hist-t">
  <div class="c">
    <div class="cab"><div><span class="vol">{{hist_vol}}</span><h2 class="t" id="hist-t">{{hist_h2}}</h2></div></div>
    <div class="hist">
      <article class="grande">{{hist_grande}}</article>
      <div>{{hist_chicas}}</div>
    </div>
  </div>
</section>

<section class="s" id="laboratorio" aria-labelledby="lab-t">
  <div class="c">
    <div class="cab"><div><span class="vol">{{lab_vol}}</span><h2 class="t" id="lab-t">{{lab_h2}}</h2><p>{{lab_p}}</p></div></div>
    <div class="lab-g">
      <div>
        <div class="metodo">{{metodo}}</div>
        <table class="tabla exp">
          <thead><tr><th>{{lx_hip}}</th><th>{{lx_tipo}}</th><th class="ocultar-m">{{lx_res}}</th><th>{{lx_ver}}</th></tr></thead>
          <tbody>{{experimentos}}</tbody>
        </table>
        <p class="meta" style="margin-top:14px">{{lab_ley}}</p>
      </div>
      <aside class="vivo" aria-label="{{vivo_aria}}">
        <div class="et"><span><span class="tipo real">REAL</span> {{vivo_nombre}}</span><span id="vela">—</span></div>
        <div class="senal" id="senal">{{cargando}}</div>
        <div class="meta" id="desde"></div>
        <div class="datos-v">
          <div><b id="cierre">—</b><span>{{d_cierre}}</span></div>
          <div><b id="sma">—</b><span>{{d_media}}</span></div>
          <div><b id="dist">—</b><span>{{d_dist}}</span></div>
        </div>
        <p class="actualizado" id="actualizado"></p>
        <div class="regla">{{regla}}</div>
        <p class="nota">{{vivo_nota}}</p>
      </aside>
    </div>
  </div>
</section>

<section class="s alt" id="shield" aria-labelledby="shield-t">
  <div class="c prod">
    <div>
      <span class="vol">{{sh_vol}}</span><h2 class="t" id="shield-t">{{sh_h2}}</h2>
      <p style="color:var(--suave);margin-top:12px;max-width:640px">{{sh_p}}</p>
      <div class="qq">{{sh_qq}}</div>
    </div>
    <div class="lado">
      <img src="{{r}}assets/{{sh_img}}" alt="{{sh_img_alt}}" width="1080" height="1350" loading="lazy">
      {{sh_planes}}
    </div>
  </div>
</section>

<section class="s" id="videos-s" aria-labelledby="vid-t">
  <div class="c">
    <div class="cab">
      <div><span class="vol">{{vid_vol}}</span><h2 class="t" id="vid-t">{{vid_h2}}</h2><p>{{vid_p}}</p></div>
      <a class="btn ch" href="https://www.youtube.com/@{{canal}}?sub_confirmation=1" target="_blank" rel="noopener">{{vid_sub}}</a>
    </div>
    <div class="videos" id="videos" data-canal="{{canal}}">
      <div id="vid-principal"><p class="meta">{{cargando}}</p></div>
      <ul class="vid-l" id="vid-lista"></ul>
    </div>
  </div>
</section>

<section class="s alt" id="servicios" aria-labelledby="serv-t">
  <div class="c dos-col">
    <div>
      <span class="vol">{{serv_vol}}</span><h2 class="t" id="serv-t">{{serv_h2}}</h2>
      <p style="color:var(--gris);margin:10px 0 18px">{{serv_p}}</p>
      <ul class="filas">{{servicios}}</ul>
      <div class="contacto">
        <a class="btn wa" href="{{wa_serv}}" target="_blank" rel="noopener">WhatsApp</a>
        <a class="btn" href="https://wa.me/c/595987685651" target="_blank" rel="noopener">{{catalogo}}</a>
        <a class="btn" href="mailto:contacto@wiqonlab.com?subject={{asunto}}">contacto@wiqonlab.com</a>
      </div>
    </div>
    <div id="herramientas">
      <span class="vol">{{her_vol}}</span><h2 class="t" style="font-size:1.6rem">{{her_h2}}</h2>
      <ul class="filas" style="margin-top:18px">{{herramientas}}</ul>
      <p class="transp">{{her_transp}}</p>
    </div>
  </div>
</section>

<section class="s" id="nosotros" aria-labelledby="nos-t">
  <div class="c nos">
    <div>
      <span class="vol">{{nos_vol}}</span><h2 class="t" id="nos-t">{{nos_h2}}</h2>
      <div style="margin-top:18px">{{nos_texto}}</div>
      <ol class="criterios">{{criterios}}</ol>
      <div class="redes">{{redes}}</div>
      <div class="fundador"><img src="{{r}}assets/fotos/fundador.jpg" alt="" width="42" height="42" loading="lazy"><span><b>Avelino González</b> · {{fundador_rol}}</span></div>
    </div>
    <div>
      <figure class="foto"><img src="{{r}}assets/fotos/cde.jpg" alt="{{foto2_alt}}" width="1600" height="948" loading="lazy" style="aspect-ratio:4/3">
        <figcaption>{{foto2_cap}} {{foto2_cred}}</figcaption></figure>
      <div class="faq" style="margin-top:28px">{{faq}}</div>
    </div>
  </div>
</section>
</main>

<footer>
  <div class="c">
    <div class="pie">
      <div><a class="marca" href="{{inicio}}"><img src="{{r}}assets/logo.png" alt="">WIQON</a><p>{{pie_desc}}</p>
        <p><a href="{{r}}" lang="es" style="display:inline">Español</a> · <a href="{{r}}br/" lang="pt-BR" style="display:inline">Português (Brasil)</a></p></div>
      <div><h5>{{pie_sec}}</h5><a href="#radar">News Radar</a><a href="#cambio">{{n_cambio}}</a><a href="#laboratorio">{{n_lab}}</a><a href="#shield">WIQON Shield</a><a href="#videos-s">{{n_videos}}</a></div>
      <div><h5>{{pie_fuentes}}</h5>{{pie_fuentes_links}}</div>
      <div><h5>{{pie_cont}}</h5><a href="mailto:contacto@wiqonlab.com">contacto@wiqonlab.com</a><a href="{{wa_hola}}" target="_blank" rel="noopener">WhatsApp +595 987 685 651</a><a href="https://discord.gg/8GDqe8H7R7" target="_blank" rel="noopener">Discord</a><a href="{{lab}}" target="_blank" rel="noopener">GitHub</a></div>
    </div>
    <div class="legal">
      <p><b>{{pie_act_t}}</b> {{pie_act}}</p>
      <p><b>{{pie_met_t}}</b> {{pie_met}}</p>
      <p><b>{{pie_priv_t}}</b> {{pie_priv}}</p>
      <p><b>{{pie_riesgo_t}}</b> {{pie_riesgo}}</p>
      <p>© <span id="anio">2026</span> WIQON · Paraguay · Brasil</p>
    </div>
  </div>
</footer>

<script src="{{r}}assets/vivo.js"></script>
<script src="{{r}}assets/v3.js"></script>
</body>
</html>
"""

CATS = ["regulacion", "impuestos", "criptoactivos", "stablecoins", "pagos", "fintech", "finanzas", "mercados", "macroeconomia", "empresas", "seguridad"]
CAT_ES = ["Regulación", "Impuestos", "Criptoactivos", "Stablecoins", "Pagos", "Fintech", "Finanzas", "Mercados", "Macroeconomía", "Empresas", "Seguridad"]
CAT_PT = ["Regulação", "Impostos", "Criptoativos", "Stablecoins", "Pagamentos", "Fintech", "Finanças", "Mercados", "Macroeconomia", "Empresas", "Segurança"]


def opciones(todas, nombres):
    return f'<option value="todas">{todas}</option>' + "".join(f'<option value="{c}">{n}</option>' for c, n in zip(CATS, nombres))


def obs(etq, titulo, texto, pq_t, pq):
    return f'<article class="ap"><span class="etq pq">{etq}</span><h3>{titulo}</h3><p>{texto}</p><p class="pq"><strong>{pq_t}</strong> {pq}</p></article>'


def exp(hip, tipo, tipo_txt, res, ver, ver_cls, href):
    return (f'<tr><td><a href="{href}" target="_blank" rel="noopener">{hip}</a></td><td><span class="tipo {tipo}">{tipo_txt}</span></td>'
            f'<td class="ocultar-m">{res}</td><td class="veredicto {ver_cls}">{ver}</td></tr>')


def fila(titulo, texto, href=None, marca=""):
    cuerpo = f'<div><h3>{titulo}</h3><p>{texto}</p></div>{f"<span class=marca-af>{marca}</span>" if marca else ""}'
    if href:
        rel = "sponsored noopener" if marca else "noopener"
        return f'<li><a class="ir" href="{href}" target="_blank" rel="{rel}">{cuerpo}</a></li>'
    return f"<li>{cuerpo}</li>"


def faq(items):
    return "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items)


FUENTES_PIE = ('<a href="https://www.bcp.gov.py/webapps/web/cotizacion/monedas" target="_blank" rel="noopener">Banco Central del Paraguay</a>'
               '<a href="https://www.bcb.gov.br/estabilidadefinanceira/historicocotacoes" target="_blank" rel="noopener">Banco Central do Brasil</a>'
               '<a href="https://www.bcra.gob.ar/PublicacionesEstadisticas/Tipos_de_cambios.asp" target="_blank" rel="noopener">BCRA</a>'
               '<a href="https://www.datos.gov.co/Econom-a-y-Finanzas/Tasa-de-Cambio-Representativa-del-Mercado-TRM/32sa-8pi3" target="_blank" rel="noopener">TRM · datos.gov.co</a>'
               '<a href="https://www.dnit.gov.py/" target="_blank" rel="noopener">DNIT</a><a href="https://www.gov.br/cvm/" target="_blank" rel="noopener">CVM</a>'
               '<a href="https://data-api.binance.vision" target="_blank" rel="noopener">Binance (datos públicos)</a>')

# ---------------------------------------------------------------------------------------------
ES = dict(
    lang="es", r="", inicio="./", url="https://wiqonlab.com/", og_locale="es_LA", prioridad="PY", canal="wiqonlab",
    titulo="WIQON — Mercados, datos y contexto desde Paraguay",
    descripcion="Noticias de mercados, fintech y cripto de Paraguay, Brasil e Hispanoamérica, tipo de cambio oficial, investigación con datos reales y WIQON Shield.",
    saltar="Saltar al News Radar", barra_aria="Datos de mercado", nav_aria="Navegación principal",
    n_radar="Lo que pasa", n_cambio="Tipo de cambio", n_lab="Laboratorio", n_videos="Videos", n_nos="Cómo trabajamos", n_cta="Ver el radar",
    es_on='class="on"', br_on="",
    lugar="Asunción · Ciudad del Este · Foz do Iguaçu",
    h1="Entendemos los mercados <em>desde acá.</em>",
    bajada="Noticias, datos y contexto para seguir mercados, trading y activos digitales, mirados desde la frontera entre Paraguay y Brasil. Sin señales de compra, sin promesas: con fuentes.",
    cta1="Ver lo que está pasando", cta2="Conocer WIQON", dato_et="Dato del día", cargando="Cargando…",
    foto1_alt="Puente de la Amistad sobre el río Paraná, con Ciudad del Este al fondo",
    foto1_cap="Puente de la Amistad, Ciudad del Este–Foz do Iguaçu.", foto1_cred=credito("puente2", "Foto", ""),
    radar_h2="Lo que está pasando", radar_p="Negocios, mercados, fintech y criptoactivos. Primero Paraguay, después Brasil y el resto de Hispanoamérica. Cada nota enlaza a su fuente original.",
    filtros_aria="Filtros del radar", f_region="Región", f_todas="Todas", f_la="Hispanoamérica", f_periodo="Período", f_3d="3 días", f_7d="7 días",
    f_idioma="Idioma", f_todos="Todos", f_cat="Tema", opciones_cat=opciones("Todos", CAT_ES),
    radar_nota="Las noticias brasileñas se muestran con su título original en portugués. Agrupamos las notas repetidas sobre un mismo hecho. Esto es información, no una recomendación.",
    ver_mas="Ver más noticias",
    cambio_vol="Tipo de cambio oficial", cambio_h2="Lo que publican los bancos centrales",
    cambio_p="Solo cotizaciones de instituciones oficiales, con su fecha. No son precios de casas de cambio.",
    tc_moneda="Moneda", tc_valor="Valor", tc_fuente="Institución", tc_fecha="Fecha",
    cambio_nota="<p><strong>En la frontera, el real importa tanto como el dólar.</strong> El comercio de Ciudad del Este se mueve con la cotización del real, y los precios de importados con la del dólar.</p><p>Las casas de cambio y los bancos aplican su propio precio de compra y venta: usá esta tabla como referencia, no como precio de operación.</p>",
    obs_vol="Lo que estamos viendo", obs_h2="Las variables que mueven la región",
    obs_p="No son señales: es lo que miramos todos los días y por qué.",
    observando="".join([
        obs("Guaraní y dólar", "El guaraní frente al dólar", 'Referencia oficial del BCP hoy: <span class="vivo-v" data-vivo="pyg">—</span>.',
            "¿Por qué importa?", "Define el precio de los importados, el peso de las deudas en dólares y la competitividad de lo que Paraguay vende afuera."),
        obs("Brasil em foco", "El real y el comercio de frontera", 'Hoy: <span class="vivo-v" data-vivo="brl">—</span>.',
            "¿Por qué importa?", "Cuando el real se fortalece, el comercio de Ciudad del Este gana compradores brasileños; cuando se debilita, ocurre lo contrario."),
        obs("Regulación", "Cripto: Paraguay y Brasil ajustan reglas", f'En Paraguay, la <a href="{DNIT_RG47}" target="_blank" rel="noopener">RG DNIT N.º 47/2026</a> pide informar operaciones con criptoactivos. En Brasil, las <a href="{BCB_RES.format(n=520)}" target="_blank" rel="noopener">resoluciones BCB 519, 520 y 521</a> rigen desde el 1/10/2026.',
            "¿Por qué importa?", "Las reglas definen qué plataformas pueden operar y qué tiene que declarar cada persona."),
        obs("Bitcoin", "La tendencia de Bitcoin", 'Cierre diario frente a su media de 100 días: <span class="vivo-v" data-vivo="btc">—</span>.',
            "¿Por qué importa?", "Es la regla que investigamos y operamos. Nos dice si el mercado está en tendencia, no adónde va el precio."),
        obs("Stablecoins", "El dólar digital en la región", "USDT y USDC se usan cada vez más para ahorrar y enviar dinero. En Brasil, la Resolución BCB 521 incluye ciertas operaciones con activos virtuales en el mercado de cambio.",
            "¿Por qué importa?", "Cambian cómo se mueven los dólares entre países y qué controles se aplican."),
        obs("Tasas y liquidez", "Política monetaria: BCP y Copom", "Seguimos las decisiones de tasas del Banco Central del Paraguay y del Copom en Brasil, y su efecto en el crédito y en el tipo de cambio.",
            "¿Por qué importa?", "Con tasas altas, ahorrar rinde más y endeudarse cuesta más; eso también mueve las monedas."),
    ]),
    hist_vol="Historias de mercado", hist_h2="Para leer con calma",
    hist_grande=(
        f'<img src="assets/fotos/asuncion.jpg" alt="Vista de Asunción desde Chaco\'i" width="1600" height="900" loading="lazy">'
        '<span class="etq py">En Paraguay</span><h3>Cripto en la declaración jurada: lo que pide la DNIT</h3>'
        '<p>La Resolución General DNIT N.º 47/2026 obliga a presentar una Declaración Jurada Informativa de Criptoactivos a las plataformas que operan en el país '
        'y a las personas y empresas residentes que superen <strong>US$ 5.000 al año</strong> en operaciones, con o sin intermediarios. Se presenta por el sistema Marangatu.</p>'
        f'<p class="firma">Equipo WIQON · 07/10/2026 · Fuente: <a href="{DNIT_RG47}" target="_blank" rel="noopener">DNIT</a> · '
        + credito("asuncion", "Foto", "") + '</p>'
    ),
    hist_chicas="".join([
        f'<article class="chica ap"><span class="etq br">Brasil em foco</span><h3 lang="pt-BR">Novas regras do BC para prestadoras de ativos virtuais já valem</h3>'
        '<p>Las resoluciones BCB 519, 520 y 521 rigen desde el 1 de octubre de 2026; el envío de datos de supervisión empieza el 1 de enero de 2027.</p>'
        f'<p class="firma">Equipo WIQON · 07/10/2026 · Fuente: <a href="{BCB_RES.format(n=519)}" target="_blank" rel="noopener">BCB 519</a>, <a href="{BCB_RES.format(n=520)}" target="_blank" rel="noopener">520</a>, <a href="{BCB_RES.format(n=521)}" target="_blank" rel="noopener">521</a></p></article>',
        f'<article class="chica ap"><span class="etq pq">Por qué importa</span><h3>El costo invisible de un robot de CFD</h3>'
        '<p>Probamos nuestro EA con los costos reales de un broker: ganó US$ 14.475 por precio y pagó US$ 4.241 en swaps. Casi un tercio de la ganancia se fue en financiación.</p>'
        f'<p class="firma">Laboratorio WIQON · <a href="{LAB}/tree/main/resultados/mt5" target="_blank" rel="noopener">informe y datos</a></p></article>',
        f'<article class="chica ap"><span class="etq dato">Dato que vale la pena mirar</span><h3>1 de 6</h3>'
        '<p>Una estrategia de day trade que parecía ganadora le ganó a dejar el dinero en Earn en solo uno de seis semestres. Con pocas operaciones, "la mejor" suele ser suerte.</p>'
        f'<p class="firma">Laboratorio WIQON · <a href="{LAB}#1-una-estrategia-validada-que-era-ruido" target="_blank" rel="noopener">ver el experimento</a></p></article>',
    ]),
    lab_vol="Laboratorio", lab_h2="Hipótesis, pruebas y resultados",
    lab_p="Probamos ideas de trading populares con años de datos y costos reales. La mayoría no pasa. Publicamos todo, con el código para repetirlo.",
    metodo="<span><b>1</b> Hipótesis</span><span><b>2</b> Reglas exactas</span><span><b>3</b> Backtest con costos</span><span><b>4</b> Fuera de muestra</span><span><b>5</b> Real, si sobrevive</span>",
    lx_hip="Hipótesis", lx_tipo="Tipo", lx_res="Resultado", lx_ver="Veredicto",
    experimentos="".join([
        exp("Filtro de tendencia en BTC (media 100)", "hist", "HISTÓRICO", "56,6% anual vs 37,3% de mantener; caída 34,7% vs 76,6% (2018-2026, con comisiones)", "Sobrevive", "si", f"{LAB}#3-lo-que-sobrevivió-filtro-de-tendencia-en-btc"),
        exp("La misma regla en MT5 (CFD)", "hist", "HISTÓRICO", "x2,02 vs x1,96; caída 39% vs 67%. Los swaps se llevan un tercio", "Con reservas", "ojo", f"{LAB}/tree/main/resultados/mt5"),
        exp("Day trade EMA21 Bounce", "hist", "HISTÓRICO", "+0,71% en 3 años vs +9,3% en Earn; media por operación indistinguible de cero", "No", "no", f"{LAB}#1-una-estrategia-validada-que-era-ruido"),
        exp("Rotación de altcoins", "hist", "HISTÓRICO", "33,7% anual con monedas de hoy; 1,0% con las que existían en 2021", "No (sesgo)", "no", f"{LAB}#2-el-sesgo-de-supervivencia-infla-todo"),
        exp("Arbitraje entre 6 exchanges", "med", "MEDICIÓN", "69 oportunidades en 24 h; casi ninguna real", "No", "no", f"{LAB}#4-arbitraje-medido-no-supuesto"),
        exp("Funding carry", "hist", "HISTÓRICO", "7-10% anual promedio, casi todo de 2021; 2-3% en 2025-26", "No", "no", f"{LAB}#5-arbitraje-de-funding-cash-and-carry"),
    ]),
    lab_ley="HISTÓRICO: simulado con datos pasados · MEDICIÓN: observado en vivo sin operar · REAL: operado con dinero. Un backtest no garantiza resultados futuros.",
    vivo_aria="Estrategia en vivo", vivo_nombre="Filtro de tendencia en BTC",
    d_cierre="Cierre diario", d_media="Media 100 días", d_dist="Distancia",
    regla="si cierre_diario &gt; media_100 → EN BTC<br>si no → EN USDT",
    vivo_nota="La operamos con capital real desde septiembre de 2026. Se recalcula cada día a las 21:15 (hora de Paraguay) con la vela cerrada. No es una recomendación.",
    sh_vol="Producto · gestión de riesgo", sh_img_alt="Resultados de WIQON Shield frente a comprar y mantener: x2,02 contra x1,96 y caída máxima de 39% contra 67%", sh_h2="WIQON Shield", sh_img="shield_resultados.png",
    sh_p="Un Expert Advisor para MetaTrader 5 que aplica la regla de tendencia que sobrevivió a nuestras pruebas: mantiene la posición en BTC mientras la tendencia sigue y la cierra cuando se rompe. Su objetivo es limitar las caídas grandes, no ganar más.",
    sh_qq=("<div><h4 class='si'>Qué hace</h4><ul><li>Decide una vez por día, con la vela cerrada</li><li>Compra si el cierre está sobre la media de 100 períodos y sale si cae debajo</li><li>Opera solo comprado, sin apalancamiento propio</li><li>Muestra su estado en un panel en el gráfico</li></ul>"
           "<h4 class='n'>Qué datos usa</h4><ul><li>Solo los precios de tu broker en MetaTrader 5</li><li>No envía datos tuyos a WIQON</li></ul></div>"
           "<div><h4 class='no'>Qué no hace</h4><ul><li>No garantiza ganancias</li><li>No evita los costos del broker: en CFD, los swaps reducen el resultado</li><li>No reacciona a caídas dentro del día</li><li>No rinde más que mantener en mercados que solo suben</li></ul>"
           "<h4 class='n'>Riesgo que cubre</h4><ul><li>Quedarse comprado durante una caída larga: en la prueba con un broker real (2022-2026), la caída máxima fue 39% contra 67% de mantener</li></ul></div>"),
    sh_planes=("<ul class='planes'><li><span>Demo<small>Sin licencia en cuentas demo</small></span><b>Gratis</b></li>"
               "<li><span>Licencia anual<small>Precio de lanzamiento, primeros 10 clientes</small></span><b><s>USD 99</s>USD 59</b></li>"
               "<li><span>Licencia vitalicia<small>Una cuenta real</small></span><b>USD 199</b></li></ul>"
               "<div class='contacto'><a class='btn p' href='shield/'>Ver planes</a>"
               f"<a class='btn' href='{LAB}/tree/main/resultados/mt5' target='_blank' rel='noopener'>Informe de prueba</a></div>"),
    vid_vol="Videos", vid_h2="El laboratorio en video", vid_p="Cada experimento explicado en pocos minutos, en nuestro canal de YouTube.", vid_sub="Suscribirme",
    serv_vol="Servicios", serv_h2="Probamos tu estrategia antes de que arriesgues capital",
    serv_p="Servicios técnicos de software y datos, con la misma metodología del laboratorio. No gestionamos dinero de terceros.",
    servicios="".join([
        fila("Auditoría de estrategias", "Backtest de portafolio con costos reales, validación fuera de muestra e intervalos de confianza. Te decimos si tiene ventaja, o si no."),
        fila("Bots para Binance", "Órdenes protegidas, Earn automático, alertas por Telegram y despliegue 24/7 en tu Raspberry Pi o VPS."),
        fila("Dashboards y capacitación", "Paneles con tus datos y clases de Python aplicado a mercados."),
    ]),
    wa_serv=f"{WA}?text=Hola%20WIQON%2C%20les%20escribo%20desde%20su%20p%C3%A1gina.", catalogo="Catálogo", asunto="Consulta%20WIQON",
    her_vol="Herramientas que usamos", her_h2="Lo que usamos todos los días",
    herramientas="".join([
        fila("TradingView", "Gráficos e indicadores. Con nuestro enlace recibís un cupón de USD 15 para tu próximo plan.", TV, "Afiliado"),
        fila("Binance", "Donde operamos la estrategia en vivo y de donde salen los datos de precios de esta página.", BINANCE, "Referido"),
        fila("MetaTrader 5", "La plataforma donde corre WIQON Shield. Gratuita.", "https://www.metatrader5.com/"),
        fila("GitHub · WIQON Lab", "Todo nuestro código y resultados, abiertos.", LAB),
    ]),
    her_transp="Transparencia: los enlaces marcados como afiliado o referido nos dan una comisión si te registrás o suscribís, sin costo extra para vos. No cambian lo que publicamos.",
    nos_vol="Cómo trabajamos", nos_h2="Un laboratorio chico, en la frontera",
    nos_texto=("<p>WIQON nace en la frontera entre Paraguay y Brasil, donde el guaraní, el real y el dólar conviven todos los días. Investigamos mercados y estrategias de trading con datos reales y publicamos lo que encontramos, también cuando el resultado es malo.</p>"
               "<p>No vendemos señales ni administramos dinero. Ofrecemos información con fuentes, investigación abierta, software y servicios técnicos.</p>"),
    criterios="".join(f"<li>{c}</li>" for c in [
        "<strong>Fuentes primero.</strong> Cada dato muestra de dónde sale y de qué fecha es. En regulación, enlazamos la norma oficial.",
        "<strong>Costos reales.</strong> Ningún resultado sin comisiones, slippage y, si corresponde, swaps.",
        "<strong>Lo malo también se publica.</strong> La mayoría de las ideas que probamos no funcionan, y lo decimos.",
        "<strong>Noticias no son señales.</strong> El radar informa; no recomienda comprar ni vender.",
        "<strong>Código abierto.</strong> Cualquiera puede repetir nuestros números.",
    ]),
    redes=" ".join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in [
        ("YouTube", "https://www.youtube.com/@wiqonlab"), ("Instagram", "https://www.instagram.com/wiqonlab/"), ("TikTok", "https://www.tiktok.com/@wiqonlab"),
        ("X", "https://x.com/wiqonlab"), ("Telegram", "https://t.me/wiqonlab"), ("WhatsApp", "https://whatsapp.com/channel/0029Vb8Tk5XCcW4zVk21xx0D"),
        ("Discord", "https://discord.gg/8GDqe8H7R7"), ("LinkedIn", "https://www.linkedin.com/company/wiqonlab"), ("Facebook", "https://www.facebook.com/wiqonlab/")]),
    fundador_rol="Fundador e investigador",
    foto2_alt="Centro de Ciudad del Este", foto2_cap="Ciudad del Este, Alto Paraná.", foto2_cred=credito("cde", "Foto", ""),
    faq=faq([
        ("¿Venden señales o manejan dinero de terceros?", "No. Publicamos información e investigación, y ofrecemos software y servicios técnicos."),
        ("¿Cada cuánto se actualiza el radar?", "Cada 30 minutos, a partir de RSS públicos de cada medio o institución. Si una fuente no responde, mostramos sus últimas noticias con la hora real."),
        ("¿De dónde sale el tipo de cambio?", "Del Banco Central del Paraguay, el Banco Central do Brasil (PTAX), el BCRA y la Superfinanciera de Colombia (TRM), con la fecha que publica cada uno."),
        ("¿Esto es asesoría financiera?", "No. Es información y análisis educativo. Operar en mercados implica riesgo de pérdida."),
    ]),
    pie_desc="Mercados, datos y contexto desde la frontera Paraguay–Brasil.", pie_sec="Secciones", pie_fuentes="Fuentes de datos", pie_cont="Contacto",
    pie_fuentes_links=FUENTES_PIE, wa_hola=f"{WA}?text=Hola%20WIQON", lab=LAB,
    pie_act_t="Actualización de datos.", pie_act="News Radar: cada 30 minutos. Tipo de cambio oficial: cada hora (cada institución publica en su horario). Estrategia en vivo: todos los días a las 21:15 (hora de Paraguay). Precio de BTC en la barra: al abrir la página.",
    pie_met_t="Metodología.", pie_met="El radar usa solo RSS públicos: mostramos título, fuente, fecha y enlace, nunca el texto completo de los artículos. Los resultados del laboratorio incluyen costos y su código está en GitHub.",
    pie_priv_t="Privacidad.", pie_priv="No usamos cookies ni herramientas de analítica. Los videos de YouTube se cargan solo si tocás reproducir (modo de privacidad mejorada). Las tipografías se cargan desde Google Fonts.",
    pie_riesgo_t="Aviso de riesgo.", pie_riesgo="Contenido informativo y educativo. No es asesoría financiera ni recomendación de inversión. Operar en mercados financieros implica riesgo de pérdida; los resultados pasados no garantizan resultados futuros. Algunos enlaces son de afiliado.",
)

BR = dict(
    lang="pt-BR", r="../", inicio="./", url="https://wiqonlab.com/br/", og_locale="pt_BR", prioridad="BR", canal="wiqonbr",
    titulo="WIQON Brasil — Mercados, dados e contexto direto da fronteira",
    descripcion="Notícias de mercado, fintech e cripto do Brasil, do Paraguai e da América hispânica, câmbio oficial, pesquisa com dados reais e WIQON Shield.",
    saltar="Ir para o News Radar", barra_aria="Dados de mercado", nav_aria="Navegação principal",
    n_radar="O que acontece", n_cambio="Câmbio", n_lab="Laboratório", n_videos="Vídeos", n_nos="Como trabalhamos", n_cta="Ver o radar",
    es_on="", br_on='class="on"',
    lugar="Foz do Iguaçu · Ciudad del Este · Asunción",
    h1="Entendemos os mercados <em>daqui.</em>",
    bajada="Notícias, dados e contexto para acompanhar mercados, trading e ativos digitais, vistos da fronteira entre o Brasil e o Paraguai. Sem sinais de compra, sem promessas: com fontes.",
    cta1="Ver o que está acontecendo", cta2="Conhecer a WIQON", dato_et="Dado do dia", cargando="Carregando…",
    foto1_alt="Ponte da Amizade sobre o rio Paraná, com Ciudad del Este ao fundo",
    foto1_cap="Ponte da Amizade, Foz do Iguaçu–Ciudad del Este.", foto1_cred=credito("puente2", "Foto", ""),
    radar_h2="O que está acontecendo", radar_p="Negócios, mercados, fintech e criptoativos. Primeiro o Brasil, depois o Paraguai e a América hispânica. Cada notícia leva à fonte original.",
    filtros_aria="Filtros do radar", f_region="Região", f_todas="Todas", f_la="América hispânica", f_periodo="Período", f_3d="3 dias", f_7d="7 dias",
    f_idioma="Idioma", f_todos="Todos", f_cat="Tema", opciones_cat=opciones("Todos", CAT_PT),
    radar_nota="As notícias em espanhol aparecem com o título original. Agrupamos notícias repetidas sobre o mesmo fato. Isto é informação, não recomendação.",
    ver_mas="Ver mais notícias",
    cambio_vol="Câmbio oficial", cambio_h2="O que os bancos centrais publicam",
    cambio_p="Só cotações de instituições oficiais, com a data. Não são preços de casas de câmbio.",
    tc_moneda="Moeda", tc_valor="Valor", tc_fuente="Instituição", tc_fecha="Data",
    cambio_nota="<p><strong>Na fronteira, o real pesa tanto quanto o dólar.</strong> O comércio de Ciudad del Este depende da cotação do real, e o preço dos importados, da do dólar.</p><p>Casas de câmbio e bancos aplicam o próprio preço de compra e venda: use esta tabela como referência, não como preço de operação.</p>",
    obs_vol="O que estamos acompanhando", obs_h2="As variáveis que movem a região",
    obs_p="Não são sinais: é o que olhamos todos os dias, e por quê.",
    observando="".join([
        obs("Brasil em foco", "O real e o comércio de fronteira", 'Hoje: <span class="vivo-v" data-vivo="brl">—</span>.',
            "Por que importa?", "Quando o real se valoriza, o comércio de Ciudad del Este ganha compradores brasileiros; quando se desvaloriza, acontece o contrário."),
        obs("Regulação", "Cripto: novas regras no Brasil e no Paraguai", f'No Brasil, as <a href="{BCB_RES.format(n=520)}" target="_blank" rel="noopener">Resoluções BCB 519, 520 e 521</a> valem desde 1/10/2026. No Paraguai, a <a href="{DNIT_RG47}" target="_blank" rel="noopener">RG DNIT nº 47/2026</a> exige informar operações com criptoativos.',
            "Por que importa?", "As regras definem quais plataformas podem operar e o que cada pessoa precisa declarar."),
        obs("Stablecoins", "O dólar digital na região", "USDT e USDC são cada vez mais usados para guardar e enviar dinheiro. A Resolução BCB 521 inclui certas operações com ativos virtuais no mercado de câmbio.",
            "Por que importa?", "Mudam como os dólares circulam entre países e quais controles se aplicam."),
        obs("Bitcoin", "A tendência do Bitcoin", 'Fechamento diário frente à média de 100 dias: <span class="vivo-v" data-vivo="btc">—</span>.',
            "Por que importa?", "É a regra que pesquisamos e operamos. Mostra se o mercado está em tendência, não para onde o preço vai."),
        obs("Guaraní e dólar", "O guaraní frente ao dólar", 'Referência oficial do BCP hoje: <span class="vivo-v" data-vivo="pyg">—</span>.',
            "Por que importa?", "Afeta o preço dos produtos do lado paraguaio da fronteira e o turismo de compras."),
        obs("Juros e liquidez", "Política monetária: Copom e BCP", "Acompanhamos as decisões de juros do Copom e do Banco Central do Paraguai, e o efeito no crédito e no câmbio.",
            "Por que importa?", "Com juros altos, poupar rende mais e se endividar custa mais; isso também move as moedas."),
    ]),
    hist_vol="Histórias de mercado", hist_h2="Para ler com calma",
    hist_grande=(
        '<img src="../assets/fotos/puente2.jpg" alt="Ponte da Amizade" width="1600" height="900" loading="lazy" style="object-position:center 60%">'
        '<span class="etq br">Brasil em foco</span><h3>Novas regras do BC para prestadoras de ativos virtuais já estão valendo</h3>'
        '<p>As Resoluções BCB 519 e 520 tratam da autorização, da governança e do funcionamento das prestadoras de serviços de ativos virtuais, e a 521 inclui certas operações com ativos virtuais no mercado de câmbio. '
        'As regras valem desde <strong>1º de outubro de 2026</strong>; o envio de dados para supervisão começa em 1º de janeiro de 2027.</p>'
        f'<p class="firma">Equipe WIQON · 07/10/2026 · Fonte: <a href="{BCB_RES.format(n=519)}" target="_blank" rel="noopener">BCB 519</a>, <a href="{BCB_RES.format(n=520)}" target="_blank" rel="noopener">520</a>, <a href="{BCB_RES.format(n=521)}" target="_blank" rel="noopener">521</a></p>'
    ),
    hist_chicas="".join([
        f'<article class="chica ap"><span class="etq py">No Paraguai</span><h3>Cripto na declaração: o que pede a DNIT</h3>'
        '<p>A RG DNIT nº 47/2026 exige uma declaração informativa anual de quem opera mais de US$ 5.000 por ano com criptoativos no Paraguai, e das plataformas que atuam no país.</p>'
        f'<p class="orig" lang="es">“La DNIT establece obligación de informar las transacciones con criptoactivos”</p>'
        f'<p class="firma">Equipe WIQON · Fonte: <a href="{DNIT_RG47}" target="_blank" rel="noopener">DNIT</a></p></article>',
        f'<article class="chica ap"><span class="etq pq">Por que importa</span><h3>O custo invisível de um robô de CFD</h3>'
        '<p>Testamos nosso EA com os custos reais de uma corretora: ganhou US$ 14.475 no preço e pagou US$ 4.241 em swaps. Quase um terço do ganho foi para o financiamento.</p>'
        f'<p class="firma">Laboratório WIQON · <a href="{LAB}/tree/main/resultados/mt5" target="_blank" rel="noopener">relatório e dados</a></p></article>',
        f'<article class="chica ap"><span class="etq dato">Dado que vale a pena olhar</span><h3>1 de 6</h3>'
        '<p>Uma estratégia de day trade que parecia vencedora ganhou de deixar o dinheiro rendendo em só um de seis semestres. Com poucas operações, "a melhor" costuma ser sorte.</p>'
        f'<p class="firma">Laboratório WIQON · <a href="{LAB}#1-una-estrategia-validada-que-era-ruido" target="_blank" rel="noopener">ver o experimento</a></p></article>',
    ]),
    lab_vol="Laboratório", lab_h2="Hipóteses, testes e resultados",
    lab_p="Testamos ideias populares de trading com anos de dados e custos reais. A maioria não passa. Publicamos tudo, com o código para refazer.",
    metodo="<span><b>1</b> Hipótese</span><span><b>2</b> Regras exatas</span><span><b>3</b> Backtest com custos</span><span><b>4</b> Fora da amostra</span><span><b>5</b> Real, se sobreviver</span>",
    lx_hip="Hipótese", lx_tipo="Tipo", lx_res="Resultado", lx_ver="Veredito",
    experimentos="".join([
        exp("Filtro de tendência no BTC (média 100)", "hist", "HISTÓRICO", "56,6% ao ano contra 37,3% de segurar; queda 34,7% contra 76,6% (2018-2026, com taxas)", "Sobrevive", "si", f"{LAB}#3-lo-que-sobrevivió-filtro-de-tendencia-en-btc"),
        exp("A mesma regra no MT5 (CFD)", "hist", "HISTÓRICO", "x2,02 contra x1,96; queda 39% contra 67%. Os swaps levam um terço", "Com ressalvas", "ojo", f"{LAB}/tree/main/resultados/mt5"),
        exp("Day trade EMA21 Bounce", "hist", "HISTÓRICO", "+0,71% em 3 anos contra +9,3% no Earn; média por operação indistinguível de zero", "Não", "no", f"{LAB}#1-una-estrategia-validada-que-era-ruido"),
        exp("Rotação de altcoins", "hist", "HISTÓRICO", "33,7% ao ano com as moedas de hoje; 1,0% com as que existiam em 2021", "Não (viés)", "no", f"{LAB}#2-el-sesgo-de-supervivencia-infla-todo"),
        exp("Arbitragem entre 6 exchanges", "med", "MEDIÇÃO", "69 oportunidades em 24 h; quase nenhuma real", "Não", "no", f"{LAB}#4-arbitraje-medido-no-supuesto"),
        exp("Funding carry", "hist", "HISTÓRICO", "7-10% ao ano em média, quase tudo de 2021; 2-3% em 2025-26", "Não", "no", f"{LAB}#5-arbitraje-de-funding-cash-and-carry"),
    ]),
    lab_ley="HISTÓRICO: simulado com dados passados · MEDIÇÃO: observado ao vivo sem operar · REAL: operado com dinheiro. Backtest não garante resultados futuros.",
    vivo_aria="Estratégia ao vivo", vivo_nombre="Filtro de tendência no BTC",
    d_cierre="Fechamento diário", d_media="Média de 100 dias", d_dist="Distância",
    regla="se fechamento_diario &gt; media_100 → EM BTC<br>senão → EM USDT",
    vivo_nota="Operamos com capital real desde setembro de 2026. Recalculada todo dia às 21h15 (Brasília) com o candle fechado. Não é recomendação de investimento.",
    sh_vol="Produto · gestão de risco · em breve no Brasil", sh_img_alt="Resultados do WIQON Shield frente a comprar e segurar: x2,02 contra x1,96 e queda máxima de 39% contra 67%", sh_h2="WIQON Shield", sh_img="shield_resultados_br.png",
    sh_p="Um Expert Advisor para MetaTrader 5 que aplica a regra de tendência que sobreviveu aos nossos testes: mantém a posição em BTC enquanto a tendência continua e fecha quando ela quebra. O objetivo é limitar as grandes quedas, não ganhar mais.",
    sh_qq=("<div><h4 class='si'>O que faz</h4><ul><li>Decide uma vez por dia, com o candle fechado</li><li>Compra se o fechamento está acima da média de 100 períodos e sai se cai abaixo</li><li>Opera só comprado, sem alavancagem própria</li><li>Mostra o estado num painel no gráfico</li></ul>"
           "<h4 class='n'>Quais dados usa</h4><ul><li>Só os preços da sua corretora no MetaTrader 5</li><li>Não envia seus dados para a WIQON</li></ul></div>"
           "<div><h4 class='no'>O que não faz</h4><ul><li>Não garante lucro</li><li>Não evita os custos da corretora: no CFD, os swaps reduzem o resultado</li><li>Não reage a quedas dentro do dia</li><li>Não rende mais que segurar em mercados que só sobem</li></ul>"
           "<h4 class='n'>Risco que cobre</h4><ul><li>Ficar comprado durante uma queda longa: no teste com uma corretora real (2022-2026), a queda máxima foi 39% contra 67% de segurar</li></ul></div>"),
    sh_planes=("<p style='color:var(--suave);margin:4px 0 16px'>A versão para o Brasil está chegando. Entre na lista e receba primeiro a condição de lançamento.</p>"
               f"<div class='contacto'><a class='btn wa' href='{WA}?text=Ol%C3%A1%20WIQON%2C%20quero%20entrar%20na%20lista%20do%20WIQON%20Shield.' target='_blank' rel='noopener'>Entrar na lista</a>"
               f"<a class='btn' href='{LAB}/tree/main/resultados/mt5' target='_blank' rel='noopener'>Relatório do teste</a></div>"),
    vid_vol="Vídeos", vid_h2="O laboratório em vídeo", vid_p="Cada experimento explicado em poucos minutos, no nosso canal do YouTube.", vid_sub="Inscrever-me",
    serv_vol="Serviços", serv_h2="Testamos sua estratégia antes de você arriscar capital",
    serv_p="Serviços técnicos de software e dados, com a mesma metodologia do laboratório. Não fazemos gestão de recursos de terceiros nem recomendação personalizada.",
    servicios="".join([
        fila("Auditoria de estratégias", "Backtest de portfólio com custos reais, validação fora da amostra e intervalos de confiança. Dizemos se tem vantagem, ou se não tem."),
        fila("Robôs para Binance", "Ordens protegidas, Earn automático, alertas no Telegram e operação 24/7 no seu Raspberry Pi ou VPS."),
        fila("Dashboards e capacitação", "Painéis com os seus dados e aulas de Python aplicado a mercados."),
    ]),
    wa_serv=f"{WA}?text=Ol%C3%A1%20WIQON%2C%20vim%20pelo%20site.", catalogo="Catálogo", asunto="Contato%20WIQON%20Brasil",
    her_vol="Ferramentas que usamos", her_h2="O que usamos todos os dias",
    herramientas="".join([
        fila("TradingView", "Gráficos e indicadores. Com o nosso link você recebe um cupom de US$ 15 para o seu próximo plano.", TV, "Afiliado"),
        fila("Binance", "Onde operamos a estratégia ao vivo e de onde vêm os dados de preço desta página.", BINANCE, "Indicação"),
        fila("MetaTrader 5", "A plataforma onde roda o WIQON Shield. Gratuita.", "https://www.metatrader5.com/"),
        fila("GitHub · WIQON Lab", "Todo o nosso código e resultados, abertos.", LAB),
    ]),
    her_transp="Transparência: os links marcados como afiliado ou indicação nos dão uma comissão se você se cadastrar ou assinar, sem custo extra para você. Isso não muda o que publicamos.",
    nos_vol="Como trabalhamos", nos_h2="Um laboratório pequeno, na fronteira",
    nos_texto=("<p>A WIQON nasceu na fronteira entre o Brasil e o Paraguai, onde o real, o guaraní e o dólar convivem todos os dias. Pesquisamos mercados e estratégias de trading com dados reais e publicamos o que encontramos, inclusive quando o resultado é ruim.</p>"
               "<p>Não vendemos sinais nem administramos dinheiro. Oferecemos informação com fontes, pesquisa aberta, software e serviços técnicos.</p>"),
    criterios="".join(f"<li>{c}</li>" for c in [
        "<strong>Fontes primeiro.</strong> Cada dado mostra de onde vem e de quando é. Em regulação, linkamos a norma oficial.",
        "<strong>Custos reais.</strong> Nenhum resultado sem taxas, slippage e, quando for o caso, swaps.",
        "<strong>O ruim também é publicado.</strong> A maioria das ideias que testamos não funciona, e dizemos isso.",
        "<strong>Notícia não é sinal.</strong> O radar informa; não recomenda comprar nem vender.",
        "<strong>Código aberto.</strong> Qualquer pessoa pode refazer nossos números.",
    ]),
    redes=" ".join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in [
        ("YouTube", "https://www.youtube.com/@wiqonbr"), ("Instagram", "https://www.instagram.com/wiqonbr/"), ("TikTok", "https://www.tiktok.com/@wiqonbr"),
        ("X", "https://x.com/wiqonbr"), ("Telegram", "https://t.me/wiqonlab"), ("WhatsApp", "https://whatsapp.com/channel/0029Vb8Tk5XCcW4zVk21xx0D"),
        ("Discord", "https://discord.gg/8GDqe8H7R7"), ("LinkedIn", "https://www.linkedin.com/company/wiqonlab")]),
    fundador_rol="Fundador e pesquisador",
    foto2_alt="Centro de Ciudad del Este", foto2_cap="Ciudad del Este, Alto Paraná (Paraguai).", foto2_cred=credito("cde", "Foto", ""),
    faq=faq([
        ("Vocês vendem sinais ou administram dinheiro de terceiros?", "Não. Publicamos informação e pesquisa, e oferecemos software e serviços técnicos."),
        ("De quanto em quanto tempo o radar é atualizado?", "A cada 30 minutos, a partir dos RSS públicos de cada veículo ou instituição. Se uma fonte não responde, mostramos as últimas notícias dela com o horário real."),
        ("De onde vem o câmbio?", "Do Banco Central do Brasil (PTAX), do Banco Central do Paraguai, do BCRA e da Superfinanciera da Colômbia (TRM), com a data publicada por cada um."),
        ("Isso é recomendação de investimento?", "Não. É informação e análise educacional. Operar nos mercados envolve risco de perda."),
    ]),
    pie_desc="Mercados, dados e contexto direto da fronteira Brasil–Paraguai.", pie_sec="Seções", pie_fuentes="Fontes de dados", pie_cont="Contato",
    pie_fuentes_links=FUENTES_PIE, wa_hola=f"{WA}?text=Ol%C3%A1%20WIQON", lab=LAB,
    pie_act_t="Atualização dos dados.", pie_act="News Radar: a cada 30 minutos. Câmbio oficial: a cada hora (cada instituição publica no seu horário). Estratégia ao vivo: todo dia às 21h15 (Brasília). Preço do BTC na barra: ao abrir a página.",
    pie_met_t="Metodologia.", pie_met="O radar usa só RSS públicos: mostramos título, fonte, data e link, nunca o texto completo das matérias. Os resultados do laboratório incluem custos e o código está no GitHub.",
    pie_priv_t="Privacidade.", pie_priv="Não usamos cookies nem ferramentas de análise. Os vídeos do YouTube só carregam se você tocar em reproduzir (modo de privacidade aprimorada). As fontes tipográficas vêm do Google Fonts.",
    pie_riesgo_t="Aviso de risco.", pie_riesgo="Conteúdo informativo e educacional. Não é recomendação de investimento. Operar nos mercados financeiros envolve risco de perda; resultados passados não garantem resultados futuros. Alguns links são de afiliado.",
)


def construir(textos, destino):
    def reemplazo(m):
        clave = m.group(1)
        if clave not in textos:
            raise KeyError(f"falta la clave '{clave}' para {destino}")
        return textos[clave]
    html = PLANTILLA
    for _ in range(2):
        html = re.sub(r"\{\{(\w+)\}\}", reemplazo, html)
    if textos["r"]:  # rutas relativas de imágenes dentro de bloques de texto
        html = html.replace('src="assets/', f'src="{textos["r"]}assets/')
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(html, encoding="utf-8", newline="\n")
    print("OK", destino.relative_to(RAIZ))


if __name__ == "__main__":
    construir(ES, RAIZ / "index.html")
    construir(BR, RAIZ / "br" / "index.html")
