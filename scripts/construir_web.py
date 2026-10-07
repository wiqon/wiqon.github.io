"""
Genera index.html (español) y br/index.html (português) desde UNA plantilla,
para que las dos versiones tengan siempre el mismo diseño.

Uso:  python scripts/construir_web.py
Los textos están en TEXTOS["es"] y TEXTOS["br"]; la plantilla usa {{clave}}.
La tarjeta "Estrategia en vivo" la completa assets/vivo.js con estado.json.
"""
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

TV = "https://www.tradingview.com/?aff_id=1171961&aff_sub=web&source=wiqonlab"
BINANCE = "https://www.binance.com/register?ref=WDAVWR75"
WA = "https://wa.me/595987685651"
LAB = "https://github.com/wiqon/wiqon-lab"

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
<meta name="theme-color" content="#04060c">
<link rel="canonical" href="{{url}}">
<link rel="alternate" hreflang="es" href="https://wiqonlab.com/">
<link rel="alternate" hreflang="pt-BR" href="https://wiqonlab.com/br/">
<link rel="icon" href="{{r}}assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{{r}}assets/v2.css">
</head>
<body data-estado="{{r}}estado.json">

<div class="cinta" aria-label="{{cinta_aria}}"><div class="cinta-pista" id="cinta-pista"></div></div>

<nav class="nav">
  <div class="contenedor">
    <a class="marca" href="{{inicio}}"><img src="{{r}}assets/logo.png" alt="WIQON">WIQON</a>
    <div class="nav-links">
      <a href="#vivo">{{nav_vivo}}</a><a href="#experimentos">{{nav_exp}}</a><a href="#shield">Shield</a>
      <a href="#servicios">{{nav_serv}}</a><a href="#comunidad">{{nav_com}}</a>
    </div>
    <div class="nav-der">
      <div class="idiomas"><a {{es_activo}} href="{{r}}" lang="es">ES</a><a {{br_activo}} href="{{r}}br/" lang="pt-BR">PT</a></div>
      <a class="btn prim chico" href="{{shield_href}}">{{nav_cta}}</a>
    </div>
  </div>
</nav>

<header class="hero">
  <div class="contenedor">
    <div class="rev">
      <span class="ceja"><span class="punto-vivo"></span>{{ceja}}</span>
      <h1>{{h1a}} <span class="grad">{{h1b}}</span></h1>
      <p class="bajada">{{bajada}}</p>
      <div class="acciones">
        <a class="btn prim" href="#vivo">{{cta1}}</a>
        <a class="btn" href="{{shield_href}}">{{cta2}}</a>
      </div>
      <div class="confianza"><span>{{conf1}}</span><span>{{conf2}}</span><span>{{conf3}}</span></div>
    </div>
    <div class="grafico rev">
      <div class="grafico-cab">
        <span class="par"><b id="precio-hero">—</b>BTC/USDT · 1D</span>
        <span class="insignia" id="insignia">…</span>
      </div>
      <canvas id="lienzo" aria-label="{{graf_aria}}"></canvas>
      <div class="grafico-pie"><span><i style="background:#e9eef8"></i>{{graf_precio}}</span><span><i style="background:#28c8ff"></i>{{graf_media}}</span><span><i style="background:rgba(52,214,140,.5)"></i>{{graf_zona}}</span></div>
    </div>
  </div>
</header>

<div class="cifras">
  <div class="contenedor rev">
    <div class="cifra"><b data-contar="20" data-suf="+">20+</b><span>{{c1}}</span></div>
    <div class="cifra"><b data-contar="8">8</b><span>{{c2}}</span></div>
    <div class="cifra"><b data-contar="1">1</b><span>{{c3}}</span></div>
    <div class="cifra"><b data-contar="100" data-suf="%">100%</b><span>{{c4}}</span></div>
  </div>
</div>

<section class="bloque" id="vivo">
  <div class="contenedor">
    <div class="titulo rev"><span class="sobre">{{vivo_sobre}}</span><h2>{{vivo_h2}}</h2><p>{{vivo_p}}</p></div>
    <div class="vivo-grid">
      <div class="tarjeta rev">
        <div class="etiqueta"><span class="sello real">REAL</span><span class="punto-vivo"></span>{{vivo_nombre}} <span style="margin-left:auto" id="vela">—</span></div>
        <div class="senal" id="senal">{{cargando}}</div>
        <div class="nota" id="desde" style="margin-top:0"></div>
        <div class="datos">
          <div class="dato"><b id="cierre">—</b><span>{{d_cierre}}</span></div>
          <div class="dato"><b id="sma">—</b><span>{{d_media}}</span></div>
          <div class="dato"><b id="dist">—</b><span>{{d_dist}}</span></div>
        </div>
        <p class="actualizado" id="actualizado"></p>
      </div>
      <div class="tarjeta explica rev">
        <h3>{{reg_h3}}</h3>
        <div class="regla">{{regla}}</div>
        <p>{{reg_p1}}</p>
        <p>{{reg_p2}}</p>
        <p>{{reg_p3}}</p>
      </div>
    </div>
  </div>
</section>

<section class="bloque alt">
  <div class="contenedor">
    <div class="titulo centro rev"><span class="sobre">{{met_sobre}}</span><h2>{{met_h2}}</h2><p>{{met_p}}</p></div>
    <div class="rejilla r4">
      <div class="tarjeta rev"><div class="paso-n">1</div><h3>{{p1t}}</h3><p>{{p1}}</p></div>
      <div class="tarjeta rev"><div class="paso-n">2</div><h3>{{p2t}}</h3><p>{{p2}}</p></div>
      <div class="tarjeta rev"><div class="paso-n">3</div><h3>{{p3t}}</h3><p>{{p3}}</p></div>
      <div class="tarjeta rev"><div class="paso-n">4</div><h3>{{p4t}}</h3><p>{{p4}}</p></div>
    </div>
  </div>
</section>

<section class="bloque" id="experimentos">
  <div class="contenedor">
    <div class="titulo rev"><span class="sobre">{{exp_sobre}}</span><h2>{{exp_h2}}</h2><p>{{exp_p}}</p></div>
    <div class="rejilla r3">{{experimentos}}</div>
    <div class="leyenda"><span><span class="sello real">REAL</span> {{ley_real}}</span><span><span class="sello backtest">BACKTEST</span> {{ley_bt}}</span><span><span class="sello medicion">{{ley_med_s}}</span> {{ley_med}}</span></div>
  </div>
</section>

<section class="bloque alt" id="shield">
  <div class="contenedor producto">
    <img class="rev" src="{{r}}assets/{{shield_img}}" alt="WIQON Shield" width="1080" height="1350" loading="lazy">
    <div class="rev">{{shield_bloque}}</div>
  </div>
</section>

<section class="bloque" id="servicios">
  <div class="contenedor">
    <div class="titulo rev"><span class="sobre">{{serv_sobre}}</span><h2>{{serv_h2}}</h2><p>{{serv_p}}</p></div>
    <div class="rejilla r3">
      <div class="tarjeta rev"><div class="icono-g">🔬</div><h3>{{s1t}}</h3><p>{{s1}}</p></div>
      <div class="tarjeta rev"><div class="icono-g">⚙️</div><h3>{{s2t}}</h3><p>{{s2}}</p></div>
      <div class="tarjeta rev"><div class="icono-g">📊</div><h3>{{s3t}}</h3><p>{{s3}}</p></div>
    </div>
    <div class="acciones rev" style="margin-top:24px">
      <a class="btn wa" href="{{wa_serv}}" target="_blank" rel="noopener">💬 WhatsApp</a>
      <a class="btn" href="https://wa.me/c/595987685651" target="_blank" rel="noopener">🛍 {{catalogo}}</a>
      <a class="btn" href="mailto:contacto@wiqonlab.com?subject={{asunto}}">✉ contacto@wiqonlab.com</a>
    </div>
    <p class="nota rev">{{serv_nota}}</p>
  </div>
</section>

<section class="bloque alt" id="herramientas">
  <div class="contenedor">
    <div class="titulo rev"><span class="sobre">{{her_sobre}}</span><h2>{{her_h2}}</h2><p>{{her_p}}</p></div>
    <div class="rejilla r4">
      <a class="tarjeta herr rev" href="{{tv}}" target="_blank" rel="sponsored noopener"><div class="icono-g">📈</div><h3>TradingView</h3><p>{{her_tv}}</p><div class="pie-herr"><span class="afil">{{afiliado}}</span><span class="ir">{{abrir}} →</span></div></a>
      <a class="tarjeta herr rev" href="{{binance}}" target="_blank" rel="sponsored noopener"><div class="icono-g">🟡</div><h3>Binance</h3><p>{{her_bn}}</p><div class="pie-herr"><span class="afil">{{referido}}</span><span class="ir">{{abrir}} →</span></div></a>
      <a class="tarjeta herr rev" href="https://www.metatrader5.com/" target="_blank" rel="noopener"><div class="icono-g">🖥️</div><h3>MetaTrader 5</h3><p>{{her_mt}}</p><div class="pie-herr"><span></span><span class="ir">{{abrir}} →</span></div></a>
      <a class="tarjeta herr rev" href="{{lab}}" target="_blank" rel="noopener"><div class="icono-g">⌘</div><h3>GitHub · WIQON Lab</h3><p>{{her_gh}}</p><div class="pie-herr"><span></span><span class="ir">{{abrir}} →</span></div></a>
    </div>
    <p class="aviso-afil rev">{{aviso_afil}}</p>
  </div>
</section>

<section class="bloque">
  <div class="contenedor rev">{{brasil_bloque}}</div>
</section>

<section class="bloque alt" id="comunidad">
  <div class="contenedor">
    <div class="titulo centro rev"><span class="sobre">{{com_sobre}}</span><h2>{{com_h2}}</h2><p>{{com_p}}</p></div>
    <div class="redes rev">{{redes}}</div>
  </div>
</section>

<section class="bloque">
  <div class="contenedor">
    <div class="titulo centro rev"><span class="sobre">FAQ</span><h2>{{faq_h2}}</h2></div>
    <div class="faq rev">{{faq}}</div>
  </div>
</section>

<div class="contenedor">
  <div class="final rev">
    <h2>{{fin_h2}}</h2>
    <p>{{fin_p}}</p>
    <div class="acciones">
      <a class="btn prim" href="https://discord.gg/8GDqe8H7R7" target="_blank" rel="noopener">{{fin_cta1}}</a>
      <a class="btn" href="{{lab}}" target="_blank" rel="noopener">{{fin_cta2}}</a>
    </div>
  </div>
</div>

<footer>
  <div class="contenedor">
    <div class="pie-grid">
      <div><a class="marca" href="{{inicio}}"><img src="{{r}}assets/logo.png" alt="WIQON">WIQON</a><p>{{pie_desc}}</p></div>
      <div><h5>{{pie_prod}}</h5><a href="{{shield_href}}">WIQON Shield</a><a href="#vivo">{{nav_vivo}}</a><a href="#experimentos">{{nav_exp}}</a><a href="#servicios">{{nav_serv}}</a></div>
      <div><h5>{{pie_rec}}</h5><a href="{{lab}}" target="_blank" rel="noopener">WIQON Lab (GitHub)</a><a href="#herramientas">{{her_sobre}}</a><a href="{{otro_idioma_href}}">{{otro_idioma}}</a></div>
      <div><h5>{{pie_cont}}</h5><a href="mailto:contacto@wiqonlab.com">contacto@wiqonlab.com</a><a href="{{wa_hola}}" target="_blank" rel="noopener">WhatsApp +595 987 685 651</a><a href="https://discord.gg/8GDqe8H7R7" target="_blank" rel="noopener">Discord</a></div>
    </div>
    <div class="legal">{{legal}}<br>© <span id="anio">2026</span> WIQON · Paraguay · Brasil</div>
  </div>
</footer>

<script src="{{r}}assets/vivo.js"></script>
<script src="{{r}}assets/v2.js"></script>
</body>
</html>
"""


def experimento(sello, sello_txt, etiqueta, num, color, texto, href, leer):
    return (f'<a class="tarjeta exp rev" href="{href}" target="_blank" rel="noopener">'
            f'<div class="etiqueta"><span class="sello {sello}">{sello_txt}</span>{etiqueta}</div>'
            f'<div class="num {color}">{num}</div><p>{texto}</p><span class="leer">{leer} →</span></a>')


def red(href, ic, nombre, sub):
    return f'<a class="red" href="{href}" target="_blank" rel="noopener"><span class="ic">{ic}</span><span>{nombre}<small>{sub}</small></span></a>'


def faq(items):
    return "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items)


ES = dict(
    lang="es", r="", inicio="./", url="https://wiqonlab.com/", og_locale="es_LA",
    titulo="WIQON — Laboratorio de trading con datos reales",
    descripcion="Probamos estrategias de trading con datos reales y publicamos todo: lo que funciona y lo que no. Estrategia en vivo, experimentos con código abierto y WIQON Shield.",
    cinta_aria="Precios en vivo", es_activo='class="activo"', br_activo="",
    nav_vivo="En vivo", nav_exp="Experimentos", nav_serv="Servicios", nav_com="Comunidad", nav_cta="Probar Shield gratis",
    shield_href="shield/",
    ceja="Laboratorio de trading cuantitativo · desde 2026",
    h1a="Probamos estrategias de trading con datos reales.", h1b="Publicamos todo.",
    bajada="La mayoría de las estrategias que “funcionan” en internet no sobreviven a una prueba honesta. Nosotros las medimos con años de datos, costos reales y código abierto: lo que funciona y lo que no.",
    cta1="Ver la estrategia en vivo", cta2="🛡 Probar WIQON Shield gratis",
    conf1="Código abierto", conf2="Sin promesas de rendimiento", conf3="Operamos con capital real",
    graf_aria="Gráfico del precio de Bitcoin y su media de 100 días", graf_precio="Precio BTC (cierre diario)", graf_media="Media 100 días", graf_zona="Cierre sobre la media",
    c1="estrategias probadas", c2="años de datos de BTC", c3="sobrevivió y la operamos", c4="código abierto",
    vivo_sobre="Estrategia en vivo", vivo_h2="La única que sobrevivió, operada con dinero real",
    vivo_p="Se recalcula todos los días con datos públicos de Binance. Si cambia la señal, lo ves acá esa misma noche.",
    vivo_nombre="Filtro de tendencia en BTC", cargando="Cargando…",
    d_cierre="Cierre diario BTC", d_media="Media 100 días", d_dist="Distancia",
    reg_h3="La regla, sin secretos",
    regla='si <span class="c">cierre_diario</span> &gt; <span class="c">media_100</span> → <span class="v">EN BTC</span><br>si no → <span class="c">EN USDT</span> (rindiendo en Earn)',
    reg_p1="Decide una vez por día, con la vela <strong>cerrada</strong> (21:00 de Paraguay). La vela de hoy sigue abierta y su precio cambia minuto a minuto: decidir con ella sería usar un dato incompleto.",
    reg_p2="En 8 años de datos (2018-2026), con comisiones: <strong>56,6% anual y caída máxima de 34,7%</strong>, contra 37,3% y 76,6% de comprar y mantener. En mercados que suben sin parar, rinde menos.",
    reg_p3='La operamos con capital real desde septiembre de 2026. No es una recomendación. <a href="https://github.com/wiqon/wiqon.github.io/blob/main/scripts/actualizar_estado.py" target="_blank" rel="noopener">Ver el código que calcula la señal</a>.',
    met_sobre="Cómo trabajamos", met_h2="Observar → Cuantificar → Verificar → Automatizar",
    met_p="El mismo proceso para cada idea, sea nuestra o de la comunidad. La mayoría no pasa del paso 3.",
    p1t="Observar", p1="Tomamos una idea popular: un indicador, un bot, un “método” que circula en redes.",
    p2t="Cuantificar", p2="La convertimos en reglas exactas y la medimos con años de datos, comisiones y slippage.",
    p3t="Verificar", p3="Ventanas fuera de muestra, intervalos de confianza y control del sesgo de supervivencia.",
    p4t="Automatizar", p4="Solo lo que sobrevive se automatiza y se opera con capital real. Y lo publicamos.",
    exp_sobre="Experimentos", exp_h2="Lo que medimos (y lo que no funcionó)",
    exp_p="Cada número tiene su código y sus datos en GitHub. Podés reproducirlo.", leer="Ver el experimento",
    experimentos="".join([
        experimento("backtest", "BACKTEST", "8 años · con comisiones", "20+ estrategias, una sobrevivió", "c",
                    "Filtro de tendencia en BTC: 56,6% anual vs 37,3% de mantener, con la mitad de caída.", f"{LAB}#3-lo-que-sobrevivió-filtro-de-tendencia-en-btc", "Ver el experimento"),
        experimento("backtest", "BACKTEST", "MT5 · CFD con swaps reales", "Misma ganancia, casi mitad de caída", "v",
                    "El EA con los costos de un broker real (2022-2026): x2,02 vs x1,96; caída 39% vs 67%. Los swaps se llevan un tercio.", f"{LAB}/tree/main/resultados/mt5", "Ver el experimento"),
        experimento("backtest", "BACKTEST", "Day trade · 3 años", "+0,25% … que era suerte", "o",
                    "EMA21 Bounce: en 3 años y 178 operaciones dio +0,71%, contra +9,3% de dejar USDT en Earn.", f"{LAB}#1-una-estrategia-validada-que-era-ruido", "Ver el experimento"),
        experimento("backtest", "BACKTEST", "Altcoins · 5 años", "De 33,7% a 1% anual", "r",
                    "La misma estrategia con las monedas de hoy y con las que existían en 2021 (LUNA y FTT incluidas).", f"{LAB}#2-el-sesgo-de-supervivencia-infla-todo", "Ver el experimento"),
        experimento("medicion", "MEDICIÓN", "Arbitraje · 24 h · 6 exchanges", "69 oportunidades, casi ninguna real", "o",
                    "Monedas distintas con el mismo nombre, retiros bloqueados y diferencias que duraban segundos.", f"{LAB}#4-arbitraje-medido-no-supuesto", "Ver el experimento"),
        experimento("backtest", "BACKTEST", "Funding · 6 años", "7-10% anual… casi todo de 2021", "c",
                    "Spot comprado + perpetuo vendido. En 2025-26 rinde 2-3% anual: igual o menos que Earn.", f"{LAB}#5-arbitraje-de-funding-cash-and-carry", "Ver el experimento"),
    ]),
    ley_real="operado con dinero", ley_bt="simulado con datos históricos", ley_med_s="MEDICIÓN", ley_med="observado en vivo, sin operar",
    shield_img="shield.png",
    shield_bloque=(
        '<span class="sobre">Producto · EA para MetaTrader 5</span>'
        '<h2 style="font-size:clamp(1.8rem,3.2vw,2.6rem);line-height:1.15;margin:10px 0 12px;letter-spacing:-.02em">WIQON Shield: el escudo automático para tu Bitcoin</h2>'
        '<p style="color:var(--gris)">Está comprado mientras BTC sube y sale cuando la tendencia se rompe. Probado con los spreads y swaps reales de un broker: '
        '<strong style="color:var(--texto)">ganó lo mismo que mantener, con casi la mitad de la caída</strong> (39% vs 67%, 2022-2026).</p>'
        '<div class="planes">'
        '<div class="plan"><h4>Demo</h4><div class="precio">Gratis</div><small>Sin licencia en cuentas demo</small></div>'
        '<div class="plan dest"><span class="cinta-plan">LANZAMIENTO</span><h4>Anual</h4><div class="precio"><s>USD 99</s>59</div><small>Primeros 10 clientes</small></div>'
        '<div class="plan"><h4>Vitalicia</h4><div class="precio">USD 199</div><small>Sin vencimiento</small></div>'
        '</div>'
        '<ul class="lista"><li><strong>Manual en español y portugués</strong> y soporte por WhatsApp</li>'
        '<li>Pago con <strong>Binance Pay / USDT, transferencia o PYUSD</strong></li>'
        f'<li><a href="{LAB}/tree/main/resultados/mt5" target="_blank" rel="noopener" style="color:var(--cian);text-decoration:underline">Informe completo</a>, con lo bueno y lo malo</li></ul>'
        '<div class="acciones"><a class="btn prim" href="shield/">🛡 Ver planes y comprar</a>'
        f'<a class="btn wa" href="{WA}?text=Hola%20WIQON%2C%20quiero%20probar%20WIQON%20Shield%20gratis." target="_blank" rel="noopener">💬 Probar gratis</a></div>'
        '<p class="nota">Software educativo. No es asesoría financiera ni garantiza resultados. En CFD, los swaps del broker reducen el rendimiento.</p>'
    ),
    serv_sobre="Servicios", serv_h2="¿Tenés una estrategia o un bot? Lo probamos antes de que arriesgues capital",
    serv_p="Servicios técnicos de software y datos, con la misma metodología del laboratorio.",
    s1t="Auditoría de estrategias", s1="Backtest de portafolio con costos reales, validación fuera de muestra e intervalos de confianza. Te decimos si tiene ventaja… o no.",
    s2t="Bots para Binance", s2="Órdenes protegidas, Earn automático, alertas por Telegram y despliegue 24/7 en tu Raspberry Pi o VPS.",
    s3t="Dashboards y capacitación", s3="Paneles con tus datos y clases de Python aplicado a mercados, individuales o grupales.",
    wa_serv=f"{WA}?text=Hola%20WIQON%2C%20les%20escribo%20desde%20su%20p%C3%A1gina.%20Quiero%20consultar%20sobre%20",
    catalogo="Ver catálogo", asunto="Consulta%20WIQON",
    serv_nota="No brindamos asesoría financiera ni gestionamos fondos de terceros.",
    her_sobre="Herramientas que usamos", her_h2="Lo que usamos todos los días en el laboratorio",
    her_p="Solo recomendamos herramientas que usamos de verdad.", tv=TV, binance=BINANCE, lab=LAB,
    her_tv="Gráficos e indicadores para analizar cualquier mercado. Con nuestro enlace recibís un cupón de USD 15 para tu próximo plan.",
    her_bn="El exchange donde operamos la estrategia en vivo y de donde salen los datos públicos de esta página.",
    her_mt="La plataforma donde corre WIQON Shield. Es gratis y la ofrecen la mayoría de los brokers.",
    her_gh="Todo nuestro código y nuestros resultados, abiertos para que los reproduzcas.",
    afiliado="Afiliado", referido="Referido", abrir="Abrir",
    aviso_afil="🔎 Transparencia: los enlaces marcados como afiliado o referido nos dan una comisión si te registrás o suscribís, sin costo extra para vos. No cambian nuestros análisis: publicamos los resultados igual, sean buenos o malos.",
    brasil_bloque=(
        '<div class="banda-br"><div><span class="sobre" style="color:var(--oro)">🇧🇷 WIQON Brasil</span>'
        '<h3>Desde la frontera Paraguay–Brasil</h3>'
        '<p>Brasil lidera el índice de adopción cripto de base 2026, con una economía cripto de USD 252.500 millones. Por eso producimos contenido nativo en portugués.</p>'
        '<p class="fuente">Fuente: Chainalysis, <a href="https://www.chainalysis.com/blog/2026-global-crypto-adoption-index/" target="_blank" rel="noopener"><em>2026 Global Crypto Adoption Index</em></a> (23/09/2026).</p>'
        '<div class="acciones" style="margin-top:16px"><a class="btn" href="br/">Ver en portugués →</a></div></div>'
        '<div class="gran">n.º 1<small>del mundo en adopción cripto</small></div></div>'
    ),
    com_sobre="Comunidad", com_h2="Seguí cada experimento",
    com_p="Publicamos cada prueba en todas las redes. En Discord podés proponer estrategias para que las probemos.",
    redes="".join([
        red("https://www.youtube.com/@wiqonlab", "▶", "YouTube", "@wiqonlab"),
        red("https://www.instagram.com/wiqonlab/", "◎", "Instagram", "@wiqonlab"),
        red("https://www.tiktok.com/@wiqonlab", "♪", "TikTok", "@wiqonlab"),
        red("https://x.com/wiqonlab", "𝕏", "X", "@wiqonlab"),
        red("https://t.me/wiqonlab", "✈", "Telegram", "Canal"),
        red("https://whatsapp.com/channel/0029Vb8Tk5XCcW4zVk21xx0D", "◉", "WhatsApp", "Canal"),
        red("https://discord.gg/8GDqe8H7R7", "◆", "Discord", "Comunidad"),
        red("https://www.linkedin.com/company/wiqonlab", "in", "LinkedIn", "WIQON"),
        red("https://www.facebook.com/wiqonlab/", "f", "Facebook", "WIQON"),
        red("https://www.threads.net/@wiqonlab", "@", "Threads", "@wiqonlab"),
    ]),
    faq_h2="Preguntas frecuentes",
    faq=faq([
        ("¿Qué es WIQON?", "Un laboratorio independiente que prueba estrategias de trading con datos reales y publica los resultados, buenos y malos, con el código para reproducirlos."),
        ("¿Venden señales o manejan dinero de terceros?", "No. No vendemos señales ni gestionamos fondos. Publicamos investigación, ofrecemos software (WIQON Shield) y servicios técnicos."),
        ("¿Cómo sé que los números son reales?", f'Cada experimento tiene su código y sus datos en <a href="{LAB}" target="_blank" rel="noopener">GitHub</a>. Usamos datos públicos de Binance: cualquiera puede repetir el cálculo.'),
        ("¿Qué es WIQON Shield?", 'Un Expert Advisor para MetaTrader 5 con la estrategia que sobrevivió a nuestras pruebas. Es gratis en cuentas demo. <a href="shield/">Ver planes</a>.'),
        ("¿Los enlaces de afiliado influyen en lo que publican?", "No. Solo recomendamos herramientas que usamos y lo aclaramos en cada enlace. Los resultados se publican igual, sean buenos o malos."),
        ("¿Esto es asesoría financiera?", "No. Es contenido educativo y de investigación. Los resultados pasados no garantizan resultados futuros."),
    ]),
    fin_h2="¿Tenés una estrategia que querés probar?",
    fin_p="Proponela en nuestra comunidad. Si es medible, la probamos con la misma metodología y publicamos el resultado.",
    fin_cta1="Unirme a Discord", fin_cta2="Ver el código en GitHub",
    pie_desc="Laboratorio de trading cuantitativo. Documentar, no prometer.",
    pie_prod="Producto", pie_rec="Recursos", pie_cont="Contacto",
    otro_idioma_href="br/", otro_idioma="Versão em português",
    wa_hola=f"{WA}?text=Hola%20WIQON",
    legal="⚠️ Contenido educativo y de investigación. No es asesoría financiera. Operar en mercados financieros implica riesgo de pérdida; los resultados pasados no garantizan resultados futuros. Algunos enlaces son de afiliado.",
)

BR = dict(
    lang="pt-BR", r="../", inicio="./", url="https://wiqonlab.com/br/", og_locale="pt_BR",
    titulo="WIQON Brasil — Laboratório de trading com dados reais",
    descripcion="Testamos estratégias de trading com dados reais e publicamos tudo: o que funciona e o que não funciona. Estratégia ao vivo, experimentos com código aberto e WIQON Shield.",
    cinta_aria="Preços ao vivo", es_activo="", br_activo='class="activo"',
    nav_vivo="Ao vivo", nav_exp="Experimentos", nav_serv="Serviços", nav_com="Comunidade", nav_cta="WIQON Shield",
    shield_href="#shield",
    ceja="Laboratório de trading quantitativo · direto da fronteira",
    h1a="Testamos estratégias de trading com dados reais.", h1b="Publicamos tudo.",
    bajada="A maioria das estratégias que “funcionam” na internet não sobrevive a um teste honesto. A gente mede com anos de dados, custos reais e código aberto: o que funciona e o que não funciona.",
    cta1="Ver a estratégia ao vivo", cta2="🛡 Conhecer o WIQON Shield",
    conf1="Código aberto", conf2="Sem promessa de rendimento", conf3="Operamos com capital real",
    graf_aria="Gráfico do preço do Bitcoin e da média de 100 dias", graf_precio="Preço BTC (fechamento diário)", graf_media="Média de 100 dias", graf_zona="Fechamento acima da média",
    c1="estratégias testadas", c2="anos de dados de BTC", c3="sobreviveu e operamos", c4="código aberto",
    vivo_sobre="Estratégia ao vivo", vivo_h2="A única que sobreviveu, operada com dinheiro real",
    vivo_p="Recalculada todos os dias com dados públicos da Binance. Se o sinal mudar, você vê aqui na mesma noite.",
    vivo_nombre="Filtro de tendência no BTC", cargando="Carregando…",
    d_cierre="Fechamento diário BTC", d_media="Média de 100 dias", d_dist="Distância",
    reg_h3="A regra, sem segredo",
    regla='se <span class="c">fechamento_diario</span> &gt; <span class="c">media_100</span> → <span class="v">EM BTC</span><br>senão → <span class="c">EM USDT</span> (rendendo no Earn)',
    reg_p1="Decide uma vez por dia, com o candle <strong>fechado</strong> (21h de Brasília). O candle de hoje continua aberto e o preço muda a cada minuto: decidir com ele seria usar um dado incompleto.",
    reg_p2="Em 8 anos de dados (2018-2026), com taxas: <strong>56,6% ao ano e queda máxima de 34,7%</strong>, contra 37,3% e 76,6% de comprar e segurar. Em mercados que só sobem, rende menos.",
    reg_p3='Operamos com capital real desde setembro de 2026. Não é recomendação de investimento. <a href="https://github.com/wiqon/wiqon.github.io/blob/main/scripts/actualizar_estado.py" target="_blank" rel="noopener">Ver o código que calcula o sinal</a>.',
    met_sobre="Como trabalhamos", met_h2="Observar → Quantificar → Verificar → Automatizar",
    met_p="O mesmo processo para cada ideia, nossa ou da comunidade. A maioria não passa do passo 3.",
    p1t="Observar", p1="Pegamos uma ideia popular: um indicador, um robô, um “método” que circula nas redes.",
    p2t="Quantificar", p2="Transformamos em regras exatas e medimos com anos de dados, taxas e slippage.",
    p3t="Verificar", p3="Janelas fora da amostra, intervalos de confiança e controle do viés de sobrevivência.",
    p4t="Automatizar", p4="Só o que sobrevive é automatizado e operado com capital real. E publicamos.",
    exp_sobre="Experimentos", exp_h2="O que medimos (e o que não funcionou)",
    exp_p="Cada número tem código e dados no GitHub. Você pode reproduzir.", leer="Ver o experimento",
    experimentos="".join([
        experimento("backtest", "BACKTEST", "8 anos · com taxas", "20+ estratégias, só uma sobreviveu", "c",
                    "Filtro de tendência no BTC: 56,6% ao ano contra 37,3% de segurar, com metade da queda.", f"{LAB}#3-lo-que-sobrevivió-filtro-de-tendencia-en-btc", "Ver o experimento"),
        experimento("backtest", "BACKTEST", "MT5 · CFD com swaps reais", "Mesmo ganho, quase metade da queda", "v",
                    "O EA com os custos de uma corretora real (2022-2026): x2,02 contra x1,96; queda 39% contra 67%. Os swaps levam um terço.", f"{LAB}/tree/main/resultados/mt5", "Ver o experimento"),
        experimento("backtest", "BACKTEST", "Day trade · 3 anos", "+0,25% … que era sorte", "o",
                    "EMA21 Bounce: em 3 anos e 178 operações deu +0,71%, contra +9,3% de deixar USDT rendendo.", f"{LAB}#1-una-estrategia-validada-que-era-ruido", "Ver o experimento"),
        experimento("backtest", "BACKTEST", "Altcoins · 5 anos", "De 33,7% para 1% ao ano", "r",
                    "A mesma estratégia com as moedas de hoje e com as que existiam em 2021 (LUNA e FTT incluídas).", f"{LAB}#2-el-sesgo-de-supervivencia-infla-todo", "Ver o experimento"),
        experimento("medicion", "MEDIÇÃO", "Arbitragem · 24 h · 6 exchanges", "69 oportunidades, quase nenhuma real", "o",
                    "Moedas diferentes com o mesmo nome, saques bloqueados e diferenças que duravam segundos.", f"{LAB}#4-arbitraje-medido-no-supuesto", "Ver o experimento"),
        experimento("backtest", "BACKTEST", "Funding · 6 anos", "7-10% ao ano… quase tudo de 2021", "c",
                    "Spot comprado + perpétuo vendido. Em 2025-26 rende 2-3% ao ano: igual ou menos que o Earn.", f"{LAB}#5-arbitraje-de-funding-cash-and-carry", "Ver o experimento"),
    ]),
    ley_real="operado com dinheiro", ley_bt="simulado com dados históricos", ley_med_s="MEDIÇÃO", ley_med="observado ao vivo, sem operar",
    shield_img="shield_br.png",
    shield_bloque=(
        '<span class="sobre">Em breve no Brasil · EA para MetaTrader 5</span>'
        '<h2 style="font-size:clamp(1.8rem,3.2vw,2.6rem);line-height:1.15;margin:10px 0 12px;letter-spacing:-.02em">WIQON Shield: o escudo automático para o seu Bitcoin</h2>'
        '<p style="color:var(--gris)">Fica comprado enquanto o BTC sobe e sai quando a tendência quebra. Testado com os spreads e swaps reais de uma corretora: '
        '<strong style="color:var(--texto)">ganhou o mesmo que segurar, com quase metade da queda</strong> (39% contra 67%, 2022-2026).</p>'
        '<ul class="lista"><li><strong>Demo grátis</strong> em contas demo</li><li><strong>Manual em português</strong> e suporte pelo WhatsApp</li>'
        f'<li><a href="{LAB}/tree/main/resultados/mt5" target="_blank" rel="noopener" style="color:var(--cian);text-decoration:underline">Relatório completo</a>, com o bom e o ruim</li></ul>'
        '<p style="color:var(--texto);margin-bottom:18px">A versão para o Brasil está chegando. Entre na lista e receba primeiro a condição de lançamento.</p>'
        f'<div class="acciones"><a class="btn wa" href="{WA}?text=Ol%C3%A1%20WIQON%2C%20quero%20entrar%20na%20lista%20do%20WIQON%20Shield." target="_blank" rel="noopener">💬 Entrar na lista</a></div>'
        '<p class="nota">Software educacional. Não é recomendação de investimento nem garante resultados.</p>'
    ),
    serv_sobre="Serviços", serv_h2="Tem uma estratégia ou um robô? A gente testa antes de você arriscar capital",
    serv_p="Serviços técnicos de software e dados, com a mesma metodologia do laboratório.",
    s1t="Auditoria de estratégias", s1="Backtest de portfólio com custos reais, validação fora da amostra e intervalos de confiança. Dizemos se tem vantagem… ou não.",
    s2t="Robôs para Binance", s2="Ordens protegidas, Earn automático, alertas no Telegram e operação 24/7 no seu Raspberry Pi ou VPS.",
    s3t="Dashboards e capacitação", s3="Painéis com os seus dados e aulas de Python aplicado a mercados, individuais ou em grupo.",
    wa_serv=f"{WA}?text=Ol%C3%A1%20WIQON%2C%20vim%20pelo%20site.%20Quero%20saber%20mais%20sobre%20",
    catalogo="Ver catálogo", asunto="Contato%20WIQON%20Brasil",
    serv_nota="Não oferecemos consultoria de investimentos, recomendação personalizada nem gestão de recursos de terceiros.",
    her_sobre="Ferramentas que usamos", her_h2="O que usamos todos os dias no laboratório",
    her_p="Só recomendamos ferramentas que usamos de verdade.", tv=TV, binance=BINANCE, lab=LAB,
    her_tv="Gráficos e indicadores para analisar qualquer mercado. Com o nosso link você recebe um cupom de US$ 15 para o seu próximo plano.",
    her_bn="A exchange onde operamos a estratégia ao vivo e de onde vêm os dados públicos desta página.",
    her_mt="A plataforma onde roda o WIQON Shield. É grátis e a maioria das corretoras oferece.",
    her_gh="Todo o nosso código e os resultados, abertos para você reproduzir.",
    afiliado="Afiliado", referido="Indicação", abrir="Abrir",
    aviso_afil="🔎 Transparência: os links marcados como afiliado ou indicação nos dão uma comissão se você se cadastrar ou assinar, sem custo extra para você. Isso não muda nossas análises: publicamos os resultados do mesmo jeito, bons ou ruins.",
    brasil_bloque=(
        '<div class="banda-br"><div><span class="sobre" style="color:var(--oro)">🇧🇷 Por que o Brasil</span>'
        '<h3>Direto da fronteira Paraguai–Brasil</h3>'
        '<p>Segundo a Chainalysis, o Brasil lidera o índice global de adoção cripto de base em 2026, com uma economia cripto de US$ 252,5 bilhões, a maior da América Latina. Moramos na fronteira e vivemos os dois lados.</p>'
        '<p class="fuente">Fonte: Chainalysis, <a href="https://www.chainalysis.com/blog/2026-global-crypto-adoption-index/" target="_blank" rel="noopener"><em>2026 Global Crypto Adoption Index</em></a> (23/09/2026).</p></div>'
        '<div class="gran">nº 1<small>do mundo em adoção cripto</small></div></div>'
    ),
    com_sobre="Comunidade", com_h2="Acompanhe cada experimento",
    com_p="Publicamos cada teste em todas as redes. No Discord você pode sugerir estratégias para a gente testar.",
    redes="".join([
        red("https://www.youtube.com/@wiqonbr", "▶", "YouTube", "@wiqonbr"),
        red("https://www.instagram.com/wiqonbr/", "◎", "Instagram", "@wiqonbr"),
        red("https://www.tiktok.com/@wiqonbr", "♪", "TikTok", "@wiqonbr"),
        red("https://x.com/wiqonbr", "𝕏", "X", "@wiqonbr"),
        red("https://t.me/wiqonlab", "✈", "Telegram", "Canal"),
        red("https://whatsapp.com/channel/0029Vb8Tk5XCcW4zVk21xx0D", "◉", "WhatsApp", "Canal"),
        red("https://discord.gg/8GDqe8H7R7", "◆", "Discord", "#brasil"),
        red("https://www.linkedin.com/company/wiqonlab", "in", "LinkedIn", "WIQON"),
        red("https://www.youtube.com/@wiqonlab", "▶", "YouTube ES", "@wiqonlab"),
        red("https://www.instagram.com/wiqonlab/", "◎", "Instagram ES", "@wiqonlab"),
    ]),
    faq_h2="Perguntas frequentes",
    faq=faq([
        ("O que é a WIQON?", "Um laboratório independente que testa estratégias de trading com dados reais e publica os resultados, bons e ruins, com o código para reproduzir."),
        ("Vocês vendem sinais ou administram dinheiro de terceiros?", "Não. Não vendemos sinais nem administramos recursos. Publicamos pesquisa, oferecemos software (WIQON Shield) e serviços técnicos."),
        ("Como sei que os números são reais?", f'Cada experimento tem código e dados no <a href="{LAB}" target="_blank" rel="noopener">GitHub</a>. Usamos dados públicos da Binance: qualquer pessoa pode refazer o cálculo.'),
        ("O que é o WIQON Shield?", "Um Expert Advisor para MetaTrader 5 com a estratégia que sobreviveu aos nossos testes. A versão para o Brasil chega em breve: entre na lista pelo WhatsApp."),
        ("Os links de afiliado influenciam o que vocês publicam?", "Não. Só recomendamos ferramentas que usamos e avisamos em cada link. Os resultados são publicados do mesmo jeito, bons ou ruins."),
        ("Isso é recomendação de investimento?", "Não. É conteúdo educacional e de pesquisa. Resultados passados não garantem resultados futuros."),
    ]),
    fin_h2="Tem uma estratégia que quer testar?",
    fin_p="Sugira na nossa comunidade. Se for mensurável, testamos com a mesma metodologia e publicamos o resultado.",
    fin_cta1="Entrar no Discord", fin_cta2="Ver o código no GitHub",
    pie_desc="Laboratório de trading quantitativo. Documentar, não prometer.",
    pie_prod="Produto", pie_rec="Recursos", pie_cont="Contato",
    otro_idioma_href="../", otro_idioma="Versión en español",
    wa_hola=f"{WA}?text=Ol%C3%A1%20WIQON",
    legal="⚠️ Conteúdo educacional e de pesquisa. Não é recomendação de investimento. Operar nos mercados financeiros envolve risco de perda; resultados passados não garantem resultados futuros. Alguns links são de afiliado.",
)


def construir(textos, destino):
    def reemplazo(m):
        clave = m.group(1)
        if clave not in textos:
            raise KeyError(f"falta la clave '{clave}' para {destino}")
        return textos[clave]
    html = PLANTILLA
    for _ in range(2):  # dos pasadas: algunos bloques usan claves dentro
        html = re.sub(r"\{\{(\w+)\}\}", reemplazo, html)
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(html, encoding="utf-8", newline="\n")
    print("OK", destino.relative_to(RAIZ))


if __name__ == "__main__":
    construir(ES, RAIZ / "index.html")
    construir(BR, RAIZ / "br" / "index.html")
