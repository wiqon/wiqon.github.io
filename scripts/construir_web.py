"""
Genera index.html (español) y br/index.html (português) desde UNA plantilla.
Jerarquía "producto primero": header, portada de producto, pruebas, tres pilares,
metodología, snapshot de mercado, News Radar, bloque humano, footer.

Uso:  python scripts/construir_web.py
Datos dinámicos (los completa el navegador con assets/v4.js y assets/vivo.js):
noticias.json, cambio.json, videos.json, estado.json. Fotos: assets/fotos/creditos.json.
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

# Íconos propios (trazo fino, se colorean con currentColor)
IC = {
    "matraz": '<path d="M9 3h6M10 3v6L4.5 18.5A1.6 1.6 0 0 0 5.9 21h12.2a1.6 1.6 0 0 0 1.4-2.5L14 9V3"/><path d="M7.5 15h9"/>',
    "escudo": '<path d="M12 3 4.5 6v5.5c0 4.6 3.2 8.4 7.5 9.5 4.3-1.1 7.5-4.9 7.5-9.5V6L12 3Z"/><path d="m8.8 12.2 2.2 2.2 4.4-4.6"/>',
    "datos": '<ellipse cx="12" cy="5.5" rx="7" ry="2.5"/><path d="M5 5.5v6c0 1.4 3.1 2.5 7 2.5s7-1.1 7-2.5v-6"/><path d="M5 11.5v6c0 1.4 3.1 2.5 7 2.5s7-1.1 7-2.5v-6"/>',
    "costos": '<path d="M4 7h16M4 12h16M4 17h10"/><circle cx="18" cy="17" r="2.5"/>',
    "muestra": '<path d="M4 19V5"/><path d="M4 19h16"/><path d="M8 15v-3M12 15V9M16 15v-6"/><path d="M14 5h5v5" />',
    "codigo": '<path d="m8 8-4 4 4 4M16 8l4 4-4 4M13.5 5l-3 14"/>',
    "regla": '<path d="M3 17 9 11l4 4 8-8"/><path d="M15 7h6v6"/>',
    "flecha": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "bot": '<rect x="5" y="8" width="14" height="11" rx="3"/><path d="M12 4v4M9 13h.01M15 13h.01M9.5 16h5"/>',
    "panel": '<rect x="3.5" y="4.5" width="17" height="15" rx="2"/><path d="M7 15v-3M11 15V9M15 15v-5M3.5 8h17"/>',
    "api": '<path d="M7 8 3 12l4 4M17 8l4 4-4 4"/><circle cx="12" cy="12" r="1.5"/>',
    "lupa": '<circle cx="11" cy="11" r="6"/><path d="m20 20-4.5-4.5"/><path d="M8.5 11h5"/>',
}


def ic(nombre, extra=""):
    return f'<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"{extra}>{IC[nombre]}</svg>'


def credito(clave, txt):
    f = FOTOS[clave]
    return (f'{txt}: <a href="{f["fuente"]}" target="_blank" rel="noopener">{f["autor"]}</a>, '
            f'<a href="{f["licencia_url"]}" target="_blank" rel="noopener">{f["licencia"]}</a>')


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
<meta name="theme-color" content="#060b14">
<link rel="canonical" href="{{url}}">
<link rel="alternate" hreflang="es" href="https://wiqonlab.com/">
<link rel="alternate" hreflang="pt-BR" href="https://wiqonlab.com/br/">
<link rel="icon" href="{{r}}assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{{r}}assets/v4.css">
<script>try{var t=localStorage.getItem("wiqon-tema");if(t)document.documentElement.dataset.tema=t;if(localStorage.getItem("wiqon-sesion")==="1")document.documentElement.classList.add("logueado");}catch(e){}</script>
</head>
<body data-estado="{{r}}estado.json" data-raiz="{{r}}">
<a class="oculto" href="#productos">{{saltar}}</a>

<header class="nav">
  <div class="c">
    <a class="marca" href="{{inicio}}"><span class="corona s"><img src="{{r}}assets/logo.png" alt="" width="34" height="34"></span><span>WIQON</span></a>
    <nav class="nav-l" aria-label="{{nav_aria}}">
      <a href="#productos">{{n_prod}}</a><a href="#laboratorio">{{n_lab}}</a><a href="#mercado">{{n_datos}}</a>
      <a href="#servicios">{{n_serv}}</a><a href="#radar">{{n_noticias}}</a>
    </nav>
    <div class="nav-d">
      <div class="idioma" aria-label="{{idioma_aria}}"><a {{es_on}} href="{{r}}" lang="es">ES</a><a {{br_on}} href="{{r}}br/" lang="pt-BR">PT-BR</a></div>
      <button class="tema-btn" type="button" aria-label="{{tema_aria}}" aria-pressed="false" title="{{tema_aria}}"><svg class="luna" viewBox="0 0 24 24"><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5Z"/></svg><svg class="sol" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg></button>
      <button class="btn ch solo-visitante" type="button" data-acceso>{{ingresar}}</button>
      <button class="btn p ch solo-visitante" type="button" data-acceso>{{crear_cuenta}}</button>
      <div class="usuario solo-usuario" id="usuario"><span class="ini" aria-hidden="true">W</span><button type="button" id="salir">{{salir}}</button></div>
    </div>
  </div>
</header>

<main>
<section class="hero" aria-labelledby="h1">
  <canvas id="globo" aria-hidden="true"></canvas>
  <div class="c">
    <div class="ap">
      <span class="kicker">{{kicker}}</span>
      <h1 id="h1">{{h1a}}<br><span>{{h1b}}</span></h1>
      <p class="sub">{{sub}}</p>
      <div class="acc">
        <button class="btn p solo-visitante" type="button" data-acceso>{{crear_cuenta}} {{ic_flecha}}</button>
        <a class="btn p solo-usuario" href="#mercado">{{ver_mercados}} {{ic_flecha}}</a>
        <a class="btn" href="#productos">{{cta1}}</a>
      </div>
      <nav class="atajos" aria-label="{{n_prod}}">
        <a class="atajo" href="#productos">{{ic_matraz}}<div><b>{{a_t}}</b><span>{{at_a}}</span></div></a>
        <a class="atajo" href="#shield">{{ic_escudo}}<div><b>WIQON Shield</b><span>{{at_b}}</span></div></a>
        <a class="atajo" href="#servicios">{{ic_datos}}<div><b>{{c_t}}</b><span>{{at_c}}</span></div></a>
      </nav>
    </div>
    <div class="panel ap" aria-label="{{panel_aria}}">
      <div class="grafico">
        <div class="g-cab">
          <div><div class="par"><span class="btc" aria-hidden="true">₿</span>BTC/USDT</div><div class="precio" id="precio-btc">—</div><span class="vivo-b" id="vivo-b">{{en_vivo}}</span></div>
          <span class="est est-regla">…</span>
        </div>
        <canvas id="lienzo" role="img" aria-label="{{graf_aria}}"></canvas>
        <div class="rangos" role="group" aria-label="{{rango_aria}}">
          <button data-r="vivo" aria-pressed="true">{{en_vivo_btn}}</button><button data-r="30" aria-pressed="false">1M</button><button data-r="90" aria-pressed="false">3M</button>
          <button data-r="180" aria-pressed="false">6M</button><button data-r="365" aria-pressed="false">1A</button>
        </div>
        <div class="leyenda"><span id="ley-velas" data-vivo="{{ley_vivo}}" data-dia="{{ley_velas}}">{{ley_vivo}}</span><span id="ley-media" hidden><i style="background:#e7b54a"></i>{{ley_media}}</span><span>Binance</span></div>
      </div>
      <div class="estado">
        <div class="caja">
          <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;margin-bottom:6px"><span class="est est-regla">…</span><span class="act" id="h-act"></span></div>
          <div class="fila"><span>{{h_cierre}}</span><b id="h-cierre">—</b></div>
          <div class="fila"><span>{{h_dist}}</span><b id="h-dist">—</b></div>
          <div class="fila"><span>{{h_desde}}</span><b id="h-desde">—</b></div>
        </div>
        <div class="caja">
          <h4>{{ic_regla}} {{regla_t}}</h4>
          <p>{{regla_p}}</p>
          <a class="enl" href="#laboratorio">{{regla_link}} {{ic_flecha}}</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="s" id="mercado" aria-labelledby="mv-t" style="padding-top:44px">
  <div class="c">
    <div class="cab"><div><span class="vol">{{mv_vol}}</span><h2 class="t" id="mv-t">{{mv_h2}}</h2></div><p class="der">{{mv_p}}</p></div>
    <div class="pestanas" role="tablist" aria-label="{{mv_vol}}">
      <button role="tab" id="t-cripto" aria-controls="p-cripto" aria-selected="true">{{tab_cripto}}</button>
      <button role="tab" id="t-acciones" aria-controls="p-acciones" aria-selected="false" tabindex="-1">{{tab_acciones}}</button>
      <button role="tab" id="t-b3" aria-controls="p-b3" aria-selected="false" tabindex="-1">{{tab_b3}}</button>
      <button role="tab" id="t-futuros" aria-controls="p-futuros" aria-selected="false" tabindex="-1">{{tab_futuros}}</button>
      <button role="tab" id="t-forex" aria-controls="p-forex" aria-selected="false" tabindex="-1">Forex</button>
      <button role="tab" id="t-economia" aria-controls="p-economia" aria-selected="false" tabindex="-1">{{tab_economia}}</button>
    </div>
    <div class="panel-m" id="p-cripto" role="tabpanel" aria-labelledby="t-cripto">
    <div class="envivo">
      <div class="mercados">
        <table aria-describedby="mv-t">
          <thead><tr><th>{{mv_activo}}</th><th class="r">{{mv_precio}}</th><th class="r">24 h</th><th class="r om">{{mv_tend}}</th></tr></thead>
          <tbody id="mercados-vivo"><tr><td colspan="4" class="meta">{{cargando}}</td></tr></tbody>
        </table>
        <p class="meta" style="padding:8px 12px"><span class="vivo-b">{{en_vivo}}</span> {{mv_fuente}}</p>
      </div>
      <div class="tv" id="tv">
        <div class="tv-cab"><b>{{tv_t}}</b><span class="meta">{{tv_nota}} <a href="{{tv_link}}" target="_blank" rel="sponsored noopener" style="color:var(--suave)">TradingView</a> ({{tv_af}})</span></div>
        <div class="tv-cuerpo" id="tv-cuerpo" data-locale="{{tv_locale}}"><div class="tv-espera">{{cargando}}</div></div>
      </div>
    </div>
    </div>
    <div class="panel-m" id="p-acciones" role="tabpanel" aria-labelledby="t-acciones" hidden data-cargar="acciones">
      <div class="widget" id="w-acciones"></div><p class="nota-w">{{nota_acciones}} {{nota_tv}}</p>
    </div>
    <div class="panel-m" id="p-b3" role="tabpanel" aria-labelledby="t-b3" hidden data-cargar="b3">
      <div class="widget" id="w-b3"></div><p class="nota-w">{{nota_b3}} {{nota_tv}}</p>
    </div>
    <div class="panel-m" id="p-futuros" role="tabpanel" aria-labelledby="t-futuros" hidden data-cargar="futuros">
      <div class="widget" id="w-futuros"></div><p class="nota-w">{{nota_futuros}} {{nota_tv}}</p>
    </div>
    <div class="panel-m" id="p-forex" role="tabpanel" aria-labelledby="t-forex" hidden data-cargar="forex">
      <div class="widget" id="w-forex"></div><p class="nota-w">{{nota_forex}} {{nota_tv}}</p>
    </div>
    <div class="panel-m" id="p-economia" role="tabpanel" aria-labelledby="t-economia" hidden data-cargar="mapa calendario">
      <div class="bloqueo solo-visitante"><div class="txt"><span class="candado"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg></span><div><b>{{bl_eco_t}}</b><span>{{bl_eco}}</span></div></div><button class="btn p ch" type="button" data-acceso>{{crear_cuenta}}</button></div>
      <div class="dos privado">
        <div class="mapa" id="mapa-inflacion">
          <h3>{{mapa_t}}</h3><p class="meta">{{mapa_p}}</p>
          <svg id="mapa-svg" role="img" aria-label="{{mapa_t}}"></svg>
          <div class="tip" id="mapa-tip" hidden></div>
          <div class="escala" id="mapa-escala"></div>
          <ul class="ranking" id="mapa-ranking"></ul>
          <p class="nota-w" id="mapa-fuente">{{cargando}}</p>
        </div>
        <div><div class="widget" id="w-calendario"></div><p class="nota-w">{{nota_cal}} {{nota_tv}}</p></div>
      </div>
    </div>
  </div>
</section>

<div class="prueba" aria-label="{{prueba_aria}}">
  <div class="c">
    <div class="pr">{{ic_datos}}<div><b>{{p1}}</b><span>{{p1s}}</span></div></div>
    <div class="pr">{{ic_costos}}<div><b>{{p2}}</b><span>{{p2s}}</span></div></div>
    <div class="pr">{{ic_muestra}}<div><b>{{p3}}</b><span>{{p3s}}</span></div></div>
    <div class="pr">{{ic_codigo}}<div><b>{{p4}}</b><span>{{p4s}}</span></div></div>
    <div class="region-foto"><img src="{{r}}assets/frontera.svg" alt="{{foto_alt}}" width="1600" height="560" loading="lazy"><span>{{ciudades}}</span></div>
  </div>
</div>

<section class="s" id="productos" aria-labelledby="prod-t">
  <div class="c">
    <div class="cab"><div><span class="vol">{{prod_vol}}</span><h2 class="t" id="prod-t">{{prod_h2}}</h2></div><p class="der">{{prod_p}}</p></div>
    <div class="pilares">
      <article class="pilar ap">
        <div class="p-cab"><span class="p-ic">{{ic_matraz}}</span><h3>{{a_t}}</h3><span class="chip-e ok">{{a_chip}}</span></div>
        <p class="que">{{a_que}}</p>
        <p class="problema"><b>{{problema}}</b> {{a_prob}}</p>
        <div class="evid">{{a_evid}}</div>
        <div class="pie-p"><a class="enl" href="#laboratorio">{{a_cta}} {{ic_flecha}}</a><span class="limite">{{a_lim}}</span></div>
      </article>
      <article class="pilar dest ap" id="shield">
        <div class="p-cab"><span class="p-ic">{{ic_escudo}}</span><h3>WIQON Shield</h3><span class="chip-e {{b_chip_cls}}">{{b_chip}}</span></div>
        <p class="que">{{b_que}}</p>
        <p class="problema"><b>{{problema}}</b> {{b_prob}}</p>
        <div class="evid mt5">{{b_evid}}</div>
        <div class="pie-p"><a class="btn p ch" href="{{b_href}}">{{b_cta}}</a><span class="limite">{{b_lim}}</span></div>
      </article>
      <article class="pilar ap" id="servicios">
        <div class="p-cab"><span class="p-ic">{{ic_datos}}</span><h3>{{c_t}}</h3><span class="chip-e ok">{{c_chip}}</span></div>
        <p class="que">{{c_que}}</p>
        <p class="problema"><b>{{problema}}</b> {{c_prob}}</p>
        <ul class="servs">{{c_lista}}</ul>
        <div class="pie-p"><a class="btn wa ch" href="{{c_href}}" target="_blank" rel="noopener">{{c_cta}}</a><a class="enl" href="mailto:contacto@wiqonlab.com">contacto@wiqonlab.com</a></div>
      </article>
    </div>
  </div>
</section>

<section class="s" id="laboratorio" aria-labelledby="met-t">
  <div class="c">
    <div class="cab"><div><span class="vol">{{met_vol}}</span><h2 class="t" id="met-t">{{met_h2}}</h2></div><p class="der">{{met_p}}</p></div>
    <ol class="metodo">{{pasos}}</ol>
    <div class="principios">{{principios}}</div>
    <div class="bloqueo solo-visitante"><div class="txt"><span class="candado"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg></span><div><b>{{bl_lab_t}}</b><span>{{bl_lab}}</span></div></div><button class="btn p ch" type="button" data-acceso>{{crear_cuenta}}</button></div>
    <div class="lab-g vista-previa">
      <div class="ap">
        <table class="tabla">
          <caption class="oculto">{{tabla_cap}}</caption>
          <thead><tr><th>{{lx_hip}}</th><th>{{lx_tipo}}</th><th class="om">{{lx_res}}</th><th>{{lx_ver}}</th></tr></thead>
          <tbody>{{experimentos}}</tbody>
        </table>
        <p class="nota">{{lab_ley}}</p>
      </div>
      <aside class="vivo ap" aria-label="{{vivo_aria}}">
        <div class="et"><span><span class="tipo real">REAL</span> {{vivo_nombre}}</span><span id="vela">—</span></div>
        <div class="senal" id="senal">{{cargando}}</div>
        <div class="meta" id="desde"></div>
        <div class="datos-v"><div><b id="cierre">—</b><span>{{d_cierre}}</span></div><div><b id="sma">—</b><span>{{d_media}}</span></div><div><b id="dist">—</b><span>{{d_dist}}</span></div></div>
        <p class="actualizado" id="actualizado"></p>
        <p class="nota">{{vivo_nota}}</p>
      </aside>
    </div>
  </div>
</section>

<section class="s privado" id="contexto" aria-labelledby="snap-t">
  <div class="c">
    <div class="snap">
      <div class="intro"><span class="vol">{{snap_vol}}</span><h2 id="snap-t">{{snap_h2}}</h2><p>{{snap_p}}</p></div>
      <div class="dato-m"><span class="q">Bitcoin · BTC/USDT</span><span class="v" id="snap-btc">—</span><span class="f" id="snap-btc-f">{{cargando}}</span></div>
      <div class="dato-m"><span class="q"><i>PY</i> USD/PYG</span><span class="v" id="snap-pyg">—</span><span class="f" id="snap-pyg-f">{{cargando}}</span></div>
      <div class="dato-m"><span class="q"><i>BR</i> USD/BRL</span><span class="v" id="snap-brl">—</span><span class="f" id="snap-brl-f">{{cargando}}</span></div>
      <div class="dato-m"><span class="q"><i>PY·BR</i> BRL/PYG</span><span class="v" id="snap-brlpyg">—</span><span class="f" id="snap-brlpyg-f">{{cargando}}</span></div>
    </div>
    <details class="mas">
      <summary>{{snap_mas}}</summary>
      <table class="tabla" id="tabla-cambio">
        <thead><tr><th>{{tc_moneda}}</th><th class="v">{{tc_valor}}</th><th class="om">{{tc_fuente}}</th><th>{{tc_fecha}}</th></tr></thead>
        <tbody><tr><td colspan="4" class="u">{{cargando}}</td></tr></tbody>
      </table>
      <p class="nota" id="cambio-act"></p>
      <p class="nota">{{cambio_nota}}</p>
    </details>
  </div>
</section>

<section class="s" id="radar" data-prioridad="{{prioridad}}" aria-labelledby="radar-t">
  <div class="c">
    <div class="solo-visitante"><div class="bloqueo solo-visitante"><div class="txt"><span class="candado"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg></span><div><b>{{bl_radar_t}}</b><span>{{bl_radar}}</span></div></div><button class="btn p ch" type="button" data-acceso>{{crear_cuenta}}</button></div></div>
    <div class="privado">
    <div class="radar-cab">
      <div><span class="vol">{{radar_vol}}</span><h2 id="radar-t">{{radar_h2}}</h2><p>{{radar_p}}</p></div>
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
        <select class="sel" id="f-idioma" data-s="idioma"><option value="todos">{{f_todos}}</option><option value="es">Español</option><option value="pt">Português</option></select></div>
      <div class="grupo"><label for="f-cat"><span>{{f_cat}}</span></label><select class="sel" id="f-cat" data-s="cat">{{opciones_cat}}</select></div>
    </div>
    <p class="aviso-r" id="radar-aviso" aria-live="polite"></p>
    <ul class="notas" id="radar-lista" aria-live="polite"></ul>
    <div class="radar-pie">
      <p class="meta">{{radar_nota}}</p>
      <div style="display:flex;gap:10px"><button class="btn ch" id="radar-mas" hidden>{{ver_mas}}</button><button class="btn ch" id="radar-btn" aria-expanded="false" aria-controls="radar-lista">{{ver_completo}}</button></div>
    </div>
    <div class="historias">{{historias}}</div>
    </div>
  </div>
</section>

<section class="s solo-usuario" id="descargas" aria-labelledby="desc-t">
  <div class="c">
    <div class="cab"><div><span class="vol">{{desc_vol}}</span><h2 class="t" id="desc-t">{{desc_h2}}</h2></div><p class="der">{{desc_p}}</p></div>
    <div class="pilares">{{descargas}}</div>
  </div>
</section>

<section class="s" id="nosotros" aria-labelledby="nos-t">
  <div class="c humano">
    <div class="ap">
      <span class="vol">{{nos_vol}}</span>
      <blockquote id="nos-t">{{cita}}</blockquote>
      {{nos_texto}}
      <div class="redes">{{redes}}</div>
      <div class="faq">{{faq}}</div>
    </div>
    <div class="ap">
      <span class="vol">{{vid_vol}}</span>
      <div class="videos" id="videos" data-canal="{{canal}}">
        <div id="vid-principal"><p class="meta">{{cargando}}</p></div>
        <ul class="vid-l" id="vid-lista"></ul>
      </div>
      <p style="margin-top:14px"><a class="enl" href="https://www.youtube.com/@{{canal}}?sub_confirmation=1" target="_blank" rel="noopener">{{vid_sub}} {{ic_flecha}}</a></p>
      <img class="ilus" src="{{r}}assets/frontera.svg" alt="{{foto_alt}}" width="1600" height="560" loading="lazy" style="margin-top:26px">
    </div>
  </div>
</section>
<section class="s solo-visitante" id="registro" aria-labelledby="reg-t">
  <div class="c"><div class="registro">
    <div><span class="vol">{{reg_vol}}</span><h2 id="reg-t">{{reg_h2}}</h2><p>{{reg_p}}</p>
      <div class="acc" style="display:flex;gap:12px;flex-wrap:wrap;margin-top:22px"><button class="btn p" type="button" data-acceso>{{crear_cuenta}} {{ic_flecha}}</button></div></div>
    <ul>{{reg_lista}}</ul>
  </div></div>
</section>
</main>

<footer>
  <div class="c">
    <div class="pie">
      <div><a class="marca" href="{{inicio}}"><span class="corona m"><img src="{{r}}assets/logo.png" alt="" width="50" height="50"></span><span>WIQON</span></a><p>{{pie_desc}}</p>
        <p><a href="{{r}}" lang="es" style="display:inline">Español</a> · <a href="{{r}}br/" lang="pt-BR" style="display:inline">Português (Brasil)</a></p></div>
      <div><h5>{{n_prod}}</h5><a href="#laboratorio">{{a_t}}</a><a href="{{b_href}}">WIQON Shield</a><a href="#servicios">{{c_t}}</a><a href="#radar">News Radar</a></div>
      <div><h5>{{pie_fuentes}}</h5>{{pie_fuentes_links}}</div>
      <div><h5>{{pie_her}}</h5>{{pie_her_links}}</div>
      <div><h5>{{pie_cont}}</h5><a href="{{priv_url}}">{{priv_txt}}</a><a href="mailto:contacto@wiqonlab.com">contacto@wiqonlab.com</a><a href="{{wa_hola}}" target="_blank" rel="noopener">WhatsApp +595 987 685 651</a><a href="https://discord.gg/8GDqe8H7R7" target="_blank" rel="noopener">Discord</a><a href="{{lab}}" target="_blank" rel="noopener">GitHub</a></div>
    </div>
    <div class="legal">
      <p><b>{{pie_act_t}}</b> {{pie_act}}</p>
      <p><b>{{pie_met_t}}</b> {{pie_met}}</p>
      <p><b>{{pie_priv_t}}</b> {{pie_priv}}</p>
      <p><b>{{pie_riesgo_t}}</b> {{pie_riesgo}}</p>
      <div class="pie-fund"><img src="{{r}}assets/fotos/fundador.jpg" alt="" width="30" height="30" loading="lazy"><span><b style="color:var(--suave)">Ing. Avelino González</b> · {{fundador_rol}}</span></div>
      <p>© <span id="anio">2026</span> WIQON · Asunción · Ciudad del Este · Foz do Iguaçu</p>
    </div>
  </div>
</footer>

<dialog class="acceso" id="acceso" aria-labelledby="acc-t">
  <form class="cuerpo" id="acc-form" novalidate>
    <div class="cab-d"><h3 id="acc-t">{{acc_t}}</h3><button class="cerrar" type="button" aria-label="{{cerrar}}">×</button></div>
    <p>{{acc_p}}</p>
    <label class="campo" for="acc-email">Email</label>
    <input type="email" id="acc-email" name="email" autocomplete="email" required placeholder="{{acc_ph}}">
    <label class="check"><input type="checkbox" id="acc-priv" required> <span>{{acc_priv}}</span></label>
    <label class="check"><input type="checkbox" id="acc-nov"> <span>{{acc_nov}}</span></label>
    <button class="btn p" type="submit">{{acc_btn}}</button>
    <p class="msg" id="acc-msg" role="status" aria-live="polite"></p>
    <p class="pie-d">{{acc_pie}}</p>
  </form>
</dialog>
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.js"></script>
<script src="{{r}}assets/cuenta.js"></script>
<script src="{{r}}assets/vivo.js"></script>
<script src="{{r}}assets/v4.js"></script>
<script src="{{r}}assets/mercados.js"></script>
<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{"token": "c394b4ca4e5144b19a861d3203511d84"}'></script>
</body>
</html>
"""

CATS = ["regulacion", "impuestos", "criptoactivos", "stablecoins", "pagos", "fintech", "finanzas", "mercados", "macroeconomia", "empresas", "seguridad"]
CAT_ES = ["Regulación", "Impuestos", "Criptoactivos", "Stablecoins", "Pagos", "Fintech", "Finanzas", "Mercados", "Macroeconomía", "Empresas", "Seguridad"]
CAT_PT = ["Regulação", "Impostos", "Criptoativos", "Stablecoins", "Pagamentos", "Fintech", "Finanças", "Mercados", "Macroeconomia", "Empresas", "Segurança"]
ICONOS = {f"ic_{k}": ic(k) for k in IC}


def opciones(todas, nombres):
    return f'<option value="todas">{todas}</option>' + "".join(f'<option value="{c}">{n}</option>' for c, n in zip(CATS, nombres))


def exp(hip, tipo, tipo_txt, res, ver, cls, href):
    return (f'<tr><td><a href="{href}" target="_blank" rel="noopener">{hip}</a></td><td><span class="tipo {tipo}">{tipo_txt}</span></td>'
            f'<td class="om">{res}</td><td class="ver {cls}">{ver}</td></tr>')


def pasos(items):
    return "".join(f'<li class="paso ap"><span class="n">{i}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(items, 1))


def serv(icono, texto, chip, cls):
    return f'<li>{ic(icono)}<span>{texto}</span><span class="chip-e {cls}">{chip}</span></li>'


def faq(items):
    return "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items)


def historia(etq, titulo, texto, firma, lang=""):
    l = f' lang="{lang}"' if lang else ""
    return f'<article class="ap"><span class="etq">{etq}</span><h3{l}>{titulo}</h3><p>{texto}</p><p class="firma">{firma}</p></article>'


FUENTES_PIE = "".join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in [
    ("Banco Central del Paraguay", "https://www.bcp.gov.py/webapps/web/cotizacion/monedas"),
    ("Banco Central do Brasil", "https://www.bcb.gov.br/estabilidadefinanceira/historicocotacoes"),
    ("BCRA · TRM Colombia", "https://www.bcra.gob.ar/PublicacionesEstadisticas/Tipos_de_cambios.asp"),
    ("DNIT · CVM", "https://www.dnit.gov.py/"), ("Binance (datos públicos)", "https://data-api.binance.vision")])


def herr(af_txt, ref_txt):
    return (f'<a href="{TV}" target="_blank" rel="sponsored noopener">TradingView<span class="af">{af_txt}</span></a>'
            f'<a href="{BINANCE}" target="_blank" rel="sponsored noopener">Binance<span class="af">{ref_txt}</span></a>'
            '<a href="https://www.metatrader5.com/" target="_blank" rel="noopener">MetaTrader 5</a>'
            f'<a href="{LAB}" target="_blank" rel="noopener">WIQON Lab (GitHub)</a>')


def redes(lista):
    return " ".join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in lista)


# ============================================ ESPAÑOL ============================================
ES = dict(ICONOS,
    ingresar="Ingresar", crear_cuenta="Crear cuenta gratis", salir="Salir", ver_mercados="Ver mercados", cerrar="Cerrar",
    bl_lab_t="Resultados completos y estrategia en vivo", bl_lab="Con tu cuenta gratis ves la tabla de experimentos y nuestra regla operando en vivo.",
    bl_radar_t="Radar de noticias y tipo de cambio oficial", bl_radar="Noticias de Paraguay, Brasil e Hispanoamérica cada 30 minutos, y las cotizaciones del BCP, BCB, BCRA y TRM.",
    bl_eco_t="Mapa de inflación y calendario económico", bl_eco="La inflación de cada país (datos del FMI) y los próximos indicadores, con tu cuenta gratis.",
    reg_vol="Cuenta gratuita", reg_h2="Creá tu cuenta y <span>mirá todo el laboratorio</span>",
    reg_p="Solo tu email: te enviamos un enlace para entrar, sin contraseñas. Gratis y sin compromiso.",
    reg_lista="<li>Resultados completos del laboratorio y la estrategia en vivo</li><li>Radar de noticias de la región, cada 30 minutos</li><li>Tipo de cambio oficial (BCP, BCB, BCRA, TRM)</li><li>Mapa de inflación mundial y calendario económico</li><li>3 informes en PDF: 20+ ideas probadas, costo de los swaps y guía DNIT 47/2026</li><li class=\"pronto\">Próximamente: alertas por email y lista de seguimiento</li>",
    acc_t="Entrá a WIQON", acc_p="Escribí tu email y te mandamos un enlace para entrar. No usamos contraseñas.", acc_ph="tu@email.com",
    acc_priv='Acepto la <a href="privacidad/" target="_blank">política de privacidad</a>.', acc_nov="Quiero recibir novedades de WIQON (opcional, me puedo dar de baja cuando quiera).",
    acc_btn="Enviar enlace de acceso", acc_pie="Si ya tenés cuenta, el mismo enlace te hace entrar.", priv_url="privacidad/", priv_txt="Política de privacidad",
    desc_vol="Descargas", desc_h2="Informes del laboratorio", desc_p="Material en PDF para leer con calma, con fuentes y fechas. Exclusivo para cuentas registradas.", desc_btn="Descargar PDF", descargas='<a class="pilar" href="{{r}}descargas/20-ideas-probadas.pdf" target="_blank" rel="noopener" style="text-decoration:none"><div class="p-cab"><span class="p-ic"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/></svg></span><h3 style="font-size:1.05rem">20+ ideas probadas: cuál sobrevivió</h3></div><p class="que">22 familias de estrategias, 84 variantes y la única regla que pasó todas las pruebas.</p><span class="enl">{{desc_btn}} ↓</span></a><a class="pilar" href="{{r}}descargas/informe-swaps.pdf" target="_blank" rel="noopener" style="text-decoration:none"><div class="p-cab"><span class="p-ic"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/></svg></span><h3 style="font-size:1.05rem">El costo invisible de un robot de CFD</h3></div><p class="que">Cuánto se llevaron los swaps de un broker real en 4 años, y qué revisar antes de usar un EA.</p><span class="enl">{{desc_btn}} ↓</span></a><a class="pilar" href="{{r}}descargas/guia-dnit-47-2026.pdf" target="_blank" rel="noopener" style="text-decoration:none"><div class="p-cab"><span class="p-ic"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/></svg></span><h3 style="font-size:1.05rem">Guía RG DNIT 47/2026</h3></div><p class="que">Quién tiene que declarar criptoactivos en Paraguay, desde qué monto, y un checklist para prepararte.</p><span class="enl">{{desc_btn}} ↓</span></a>',
    tema_aria="Cambiar entre tema oscuro y claro", tab_cripto="Criptomonedas", tab_acciones="Acciones EE. UU.", tab_b3="Brasil B3", tab_futuros="Futuros", tab_economia="Economía",
    nota_acciones="Las acciones con más movimiento del día en EE. UU.", nota_b3="Ibovespa, acciones y minicontratos de la B3.",
    nota_futuros="Minicontratos de la B3 y, como referencia global, índices y materias primas (incluida la soja) en CFD.", nota_forex="Monedas de la región frente al dólar y los pares principales.",
    nota_cal="Calendario económico: próximos datos e indicadores por país.", nota_tv="Datos de TradingView; algunos mercados se muestran con demora según la bolsa.",
    mapa_t="Inflación en el mundo", mapa_p="Variación anual de los precios al consumidor por país. Pasá el cursor (o tocá) un país.",
    sello_sub="Market Flow Intelligence", at_a="Resultados abiertos", at_b="EA para MetaTrader 5", at_c="Bots, auditorías, paneles",
    en_vivo="EN VIVO", en_vivo_btn="En vivo", ley_vivo="Velas de 1 minuto, en vivo",
    mv_vol="Mercado en vivo", mv_h2="Así se mueve el mercado <span>ahora</span>",
    mv_p="Cripto en tiempo real, acciones de EE. UU. y de la B3, futuros, forex y economía: elegí una pestaña. El gráfico interactivo lo podés usar vos.",
    mv_activo="Activo", mv_precio="Precio", mv_tend="Últimas 24 h", mv_fuente="Precios de Binance en tiempo real. No son recomendaciones.",
    tv_t="Probalo: gráfico interactivo", tv_nota="Gráfico de", tv_af="enlace de afiliado", tv_link=TV, tv_locale="es",
    lang="es", r="", inicio="./", url="https://wiqonlab.com/", og_locale="es_LA", prioridad="PY", canal="wiqonlab",
    titulo="WIQON — Probamos estrategias con datos reales",
    descripcion="Laboratorio de trading de Paraguay y Brasil: probamos estrategias con costos reales, publicamos los resultados y construimos herramientas con lo que sobrevive, como WIQON Shield.",
    saltar="Saltar a los productos", nav_aria="Secciones", idioma_aria="Idioma",
    n_prod="Productos", n_lab="Laboratorio", n_datos="Datos", n_serv="Servicios", n_noticias="Noticias",
    es_on='class="on"', br_on="", cta_nav="Probar Shield gratis", cta_nav_href="shield/",
    kicker="Paraguay · Brasil · Mercados",
    h1a="Probamos estrategias con datos reales.", h1b="Construimos herramientas con lo que sobrevive.",
    sub="Investigamos mercados, medimos costos y validamos ideas antes de convertirlas en software, datos o servicios. Si una idea no sobrevive, también lo publicamos.",
    cta1="Explorar WIQON", cta2="Ver laboratorio",
    panel_aria="Bitcoin y el estado de nuestra regla de tendencia", graf_aria="Velas diarias de Bitcoin con su media de 100 días",
    rango_aria="Período del gráfico", ley_velas="Velas diarias cerradas", ley_media="Media 100 días",
    h_cierre="Cierre diario", h_dist="Distancia a la media 100", h_desde="En este estado desde",
    regla_t="Nuestra regla", regla_p="Estar en BTC solo si el cierre diario está sobre la media de 100 días. Si cae debajo, a USDT. La operamos con capital real.",
    regla_link="Ver metodología",
    prueba_aria="Cómo trabajamos", p1="Datos reales", p1s="Precios públicos, años de historia",
    p2="Costos incluidos", p2s="Comisiones, slippage y swaps", p3="Fuera de muestra", p3s="Validamos en períodos no vistos",
    p4="Código abierto", p4s="Cualquiera puede repetirlo",
    foto_alt="Puente de la Amistad entre Ciudad del Este y Foz do Iguaçu", ciudades="Asunción · Ciudad del Este · Foz do Iguaçu",
    prod_vol="Lo que construimos", prod_h2="Qué <span>ofrecemos</span>",
    prod_p="Investigación abierta, un producto para gestionar el riesgo y servicios técnicos. Todo sale del mismo proceso de pruebas.",
    problema="Para qué sirve:",
    a_t="Laboratorio de estrategias", a_chip="Abierto",
    a_que="Probamos ideas de trading populares con años de datos, costos reales y validación fuera de muestra, y publicamos el resultado.",
    a_prob="saber si una estrategia tiene ventaja antes de arriesgar dinero en ella.",
    a_evid=('<div class="comp"><div><span class="lbl">Probadas</span><div class="num">20+</div></div><div><span class="lbl">Sobrevivió</span><div class="num">1</div></div></div>'
            '<div style="margin-top:12px"><span class="lbl">Filtro de tendencia BTC · 2018-2026, con costos</span>'
            '<div class="comp" style="margin-top:6px"><div><span class="lbl">Regla</span><div class="num" style="font-size:1.15rem">56,6%<small>anual</small></div><div class="barra-c"><i style="width:100%;background:var(--cian)"></i></div></div>'
            '<div><span class="lbl">Mantener</span><div class="num" style="font-size:1.15rem">37,3%<small>anual</small></div><div class="barra-c"><i style="width:66%;background:var(--gris2)"></i></div></div></div></div>'
            '<div class="tags"><span>Costos incluidos</span><span>Fuera de muestra</span><span>Histórico + real</span></div>'),
    a_cta="Ver resultados", a_lim="Resultados pasados no garantizan los futuros.",
    b_chip="Expert Advisor · disponible", b_chip_cls="ok",
    b_que="Gestión de riesgo automática para MetaTrader 5: mantiene la posición en BTC mientras la tendencia sigue y la cierra cuando se rompe.",
    b_prob="no quedarse comprado durante una caída larga, con una regla clara y sin decisiones impulsivas.",
    b_evid=('<div class="t5"><span>MT5 · BTCUSD · D1</span><span>WIQON Shield</span></div>'
            '<ul><li>Regla: cierre &gt; media 100</li><li>Decide con vela cerrada</li><li>Solo comprado, sin apalancamiento propio</li><li>Panel de estado en el gráfico</li></ul>'
            '<div class="comp" style="margin-top:12px;font-family:var(--sans)"><div><span class="lbl">Caída máx. Shield</span><div class="num" style="font-size:1.15rem">39%</div><div class="barra-c"><i style="width:58%;background:var(--sube)"></i></div></div>'
            '<div><span class="lbl">Caída máx. mantener</span><div class="num" style="font-size:1.15rem">67%</div><div class="barra-c"><i style="width:100%;background:var(--baja)"></i></div></div></div>'
            '<p class="limite" style="margin-top:8px;font-family:var(--sans)">Prueba con costos reales de un broker, 2022-2026. Los swaps redujeron un tercio de la ventaja.</p>'),
    b_href="shield/", b_cta="Demo gratis y planes", b_lim="No garantiza ganancias.",
    c_t="Datos y automatización", c_chip="Servicios",
    c_que="Bots, auditorías y paneles hechos con la misma metodología del laboratorio.",
    c_prob="automatizar y medir tu operativa sin depender de promesas.",
    c_lista="".join([serv("lupa", "Auditoría de estrategias", "Disponible", "ok"), serv("bot", "Bots para Binance", "Disponible", "ok"),
                     serv("panel", "Dashboards y capacitación", "Disponible", "ok"), serv("api", "API de datos del laboratorio", "Próximamente", "pronto")]),
    c_href=f"{WA}?text=Hola%20WIQON%2C%20quiero%20consultar%20por%20un%20servicio.", c_cta="Hablemos",
    met_vol="Metodología", met_h2="Cómo decidimos qué <span>sobrevive</span>",
    met_p="No es suerte, es un proceso. Cada idea pasa por los mismos filtros antes de convertirse en una herramienta o un dato.",
    pasos=pasos([("Hipótesis", "Tomamos una idea concreta de mercado."), ("Reglas exactas", "Entradas, salidas y tamaño, sin ambigüedad."),
                 ("Backtest con costos", "Años de datos, comisiones, slippage y swaps."), ("Fuera de muestra", "Validamos en períodos que no vimos."),
                 ("Real, si sobrevive", "Recién ahí se convierte en producto o servicio.")]),
    principios="".join(f"<span><b>{a}</b> · {b}</span>" for a, b in [("Fuentes primero", "cada dato con origen y fecha"), ("Costos reales", "sin resultados maquillados"),
                 ("Lo malo también se publica", "la mayoría no funciona"), ("Noticias no son señales", "informamos, no recomendamos"), ("Código abierto", "podés repetirlo")]),
    tabla_cap="Resultados publicados del laboratorio", lx_hip="Hipótesis", lx_tipo="Tipo", lx_res="Resultado", lx_ver="Veredicto",
    experimentos="".join([
        exp("Filtro de tendencia en BTC", "hist", "HISTÓRICO", "56,6% anual vs 37,3% de mantener; caída 34,7% vs 76,6% (2018-2026)", "Sobrevive", "si", f"{LAB}#3-lo-que-sobrevivió-filtro-de-tendencia-en-btc"),
        exp("La misma regla en MT5 (CFD)", "hist", "HISTÓRICO", "x2,02 vs x1,96; caída 39% vs 67%. Swaps: un tercio de la ventaja", "Con reservas", "ojo", f"{LAB}/tree/main/resultados/mt5"),
        exp("Day trade EMA21 Bounce", "hist", "HISTÓRICO", "+0,71% en 3 años vs +9,3% en Earn", "No", "no", f"{LAB}#1-una-estrategia-validada-que-era-ruido"),
        exp("Rotación de altcoins", "hist", "HISTÓRICO", "33,7% anual con monedas de hoy; 1,0% con las de 2021", "No (sesgo)", "no", f"{LAB}#2-el-sesgo-de-supervivencia-infla-todo"),
        exp("Arbitraje entre 6 exchanges", "med", "MEDICIÓN", "69 oportunidades en 24 h; casi ninguna real", "No", "no", f"{LAB}#4-arbitraje-medido-no-supuesto"),
        exp("Funding carry", "hist", "HISTÓRICO", "7-10% anual, casi todo de 2021; 2-3% en 2025-26", "No", "no", f"{LAB}#5-arbitraje-de-funding-cash-and-carry"),
    ]),
    lab_ley="HISTÓRICO: simulado con datos pasados · MEDICIÓN: observado en vivo, sin operar · REAL: operado con dinero.",
    vivo_aria="Estrategia en vivo", vivo_nombre="Filtro de tendencia en BTC", cargando="Cargando…",
    d_cierre="Cierre", d_media="Media 100", d_dist="Distancia",
    vivo_nota="Se recalcula cada día a las 21:15 (hora de Paraguay) con la vela cerrada. No es una recomendación.",
    snap_vol="Mercado en contexto", snap_h2="La región también importa",
    snap_p="Datos de Paraguay y Brasil de fuentes oficiales, con su fecha. Sin señales, sin promesas.",
    snap_mas="Ver todas las cotizaciones oficiales", tc_moneda="Moneda", tc_valor="Valor", tc_fuente="Institución", tc_fecha="Fecha",
    cambio_nota="Son referencias oficiales (BCP, BCB, BCRA, TRM). Bancos y casas de cambio aplican su propio precio de compra y venta.",
    radar_vol="News Radar", radar_h2="Contexto de mercado",
    radar_p="Negocios, fintech y cripto de la región, con la fuente original. Primero Paraguay, después Brasil e Hispanoamérica.",
    filtros_aria="Filtros del radar", f_region="País", f_todas="Todos", f_la="Hispanoamérica", f_periodo="Período", f_3d="3 días", f_7d="7 días",
    f_idioma="Idioma", f_todos="Todos", f_cat="Tema", opciones_cat=opciones("Todos", CAT_ES),
    radar_nota="Noticias no son señales. Las notas brasileñas conservan su título en portugués.", ver_mas="Ver más", ver_completo="Ver radar completo",
    historias="".join([
        historia("En Paraguay", "Cripto en la declaración jurada: lo que pide la DNIT",
                 "La RG DNIT N.º 47/2026 obliga a informar operaciones con criptoactivos a quienes superen US$ 5.000 al año y a las plataformas que operan en el país.",
                 f'Equipo WIQON · 07/10/2026 · <a href="{DNIT_RG47}" target="_blank" rel="noopener">fuente oficial</a>'),
        historia("Brasil em foco", "Novas regras do BC para prestadoras de ativos virtuais já valem",
                 "Las resoluciones BCB 519, 520 y 521 rigen desde el 1/10/2026; el envío de datos de supervisión empieza el 1/1/2027.",
                 f'Equipo WIQON · 07/10/2026 · <a href="{BCB_RES.format(n=520)}" target="_blank" rel="noopener">fuente oficial</a>', "pt-BR"),
        historia("Por qué importa", "El costo invisible de un robot de CFD",
                 "Nuestro EA ganó US$ 14.475 por precio y pagó US$ 4.241 en swaps con un broker real. Casi un tercio se fue en financiación.",
                 f'Laboratorio WIQON · <a href="{LAB}/tree/main/resultados/mt5" target="_blank" rel="noopener">informe</a>'),
    ]),
    nos_vol="Quiénes somos", cita="Publicamos lo que encontramos, <span>también cuando el resultado es malo.</span>",
    nos_texto=("<p>WIQON nace en la frontera entre Paraguay y Brasil, donde el guaraní, el real y el dólar conviven todos los días. Lo probamos, lo medimos y, si no sobrevive, lo publicamos igual.</p>"
               "<p>No vendemos señales ni administramos dinero de terceros.</p>"),
    fundador_rol="Fundador e investigador",
    redes=redes([("YouTube", "https://www.youtube.com/@wiqonlab"), ("Instagram", "https://www.instagram.com/wiqonlab/"), ("TikTok", "https://www.tiktok.com/@wiqonlab"),
                 ("X", "https://x.com/wiqonlab"), ("Telegram", "https://t.me/wiqonlab"), ("WhatsApp", "https://whatsapp.com/channel/0029Vb8Tk5XCcW4zVk21xx0D"),
                 ("Discord", "https://discord.gg/8GDqe8H7R7"), ("LinkedIn", "https://www.linkedin.com/company/wiqonlab"), ("Facebook", "https://www.facebook.com/wiqonlab/")]),
    faq=faq([("¿Venden señales o manejan dinero de terceros?", "No. Publicamos investigación y ofrecemos software y servicios técnicos."),
             ("¿WIQON Shield garantiza ganancias?", "No. Busca limitar las caídas grandes; en mercados que solo suben rinde menos que mantener."),
             ("¿De dónde salen los datos?", "Precios públicos de Binance, cotizaciones del BCP, BCB, BCRA y TRM, y RSS públicos de medios e instituciones.")]),
    vid_vol="El laboratorio en video", vid_sub="Suscribirme al canal",
    foto2_alt="Centro de Ciudad del Este", foto2_cap="Ciudad del Este, Alto Paraná.", foto2_cred=credito("cde", "Foto"), foto1_cred=credito("puente2", "Puente de la Amistad"),
    pie_desc="Laboratorio de trading y datos de mercado, desde la frontera Paraguay–Brasil.", pie_fuentes="Fuentes de datos", pie_her="Herramientas que usamos",
    pie_her_links=herr("afiliado", "referido"), pie_cont="Contacto", pie_fuentes_links=FUENTES_PIE, wa_hola=f"{WA}?text=Hola%20WIQON", lab=LAB,
    pie_act_t="Actualización.", pie_act="Noticias: cada 30 minutos. Tipo de cambio oficial: cada hora (cada institución publica en su horario). Estrategia: todos los días a las 21:15 (hora de Paraguay). Precio de BTC: al abrir la página.",
    pie_met_t="Metodología.", pie_met="Resultados con costos y código en GitHub. El radar usa solo RSS públicos: título, fuente, fecha y enlace, nunca el texto de los artículos.",
    pie_priv_t="Privacidad.", pie_priv="Sin cookies. Medimos visitas con Cloudflare Web Analytics, que no usa cookies ni identifica personas. Los videos de YouTube se cargan solo al tocar reproducir. El gráfico interactivo lo provee TradingView y se carga al llegar a esa sección. Las tipografías vienen de Google Fonts.",
    pie_riesgo_t="Aviso de riesgo.", pie_riesgo="Contenido informativo y educativo; no es asesoría financiera. Operar implica riesgo de pérdida y los resultados pasados no garantizan los futuros. Los enlaces marcados como afiliado o referido nos dan una comisión sin costo extra para vos.",
)

# ============================================ PORTUGUÊS ============================================
BR = dict(ICONOS,
    ingresar="Entrar", crear_cuenta="Criar conta grátis", salir="Sair", ver_mercados="Ver mercados", cerrar="Fechar",
    bl_lab_t="Resultados completos e estratégia ao vivo", bl_lab="Com a sua conta grátis você vê a tabela de experimentos e a nossa regra operando ao vivo.",
    bl_radar_t="Radar de notícias e câmbio oficial", bl_radar="Notícias do Brasil, Paraguai e América hispânica a cada 30 minutos, e as cotações do BCB, BCP, BCRA e TRM.",
    bl_eco_t="Mapa da inflação e calendário econômico", bl_eco="A inflação de cada país (dados do FMI) e os próximos indicadores, com a sua conta grátis.",
    reg_vol="Conta gratuita", reg_h2="Crie a sua conta e <span>veja todo o laboratório</span>",
    reg_p="Só o seu e-mail: enviamos um link para entrar, sem senha. Grátis e sem compromisso.",
    reg_lista="<li>Resultados completos do laboratório e a estratégia ao vivo</li><li>Radar de notícias da região, a cada 30 minutos</li><li>Câmbio oficial (BCB, BCP, BCRA, TRM)</li><li>Mapa da inflação mundial e calendário econômico</li><li>3 relatórios em PDF: 20+ ideias testadas, custo dos swaps e guia BCB 519-521</li><li class=\"pronto\">Em breve: alertas por e-mail e lista de acompanhamento</li>",
    acc_t="Entre na WIQON", acc_p="Digite o seu e-mail e enviamos um link para entrar. Não usamos senha.", acc_ph="voce@email.com",
    acc_priv='Aceito a <a href="privacidade/" target="_blank">política de privacidade</a>.', acc_nov="Quero receber novidades da WIQON (opcional, posso cancelar quando quiser).",
    acc_btn="Enviar link de acesso", acc_pie="Se você já tem conta, o mesmo link faz você entrar.", priv_url="privacidade/", priv_txt="Política de privacidade",
    desc_vol="Downloads", desc_h2="Relatórios do laboratório", desc_p="Material em PDF para ler com calma, com fontes e datas. Exclusivo para contas cadastradas.", desc_btn="Baixar PDF", descargas='<a class="pilar" href="{{r}}descargas/20-ideias-testadas.pdf" target="_blank" rel="noopener" style="text-decoration:none"><div class="p-cab"><span class="p-ic"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/></svg></span><h3 style="font-size:1.05rem">20+ ideias testadas: qual sobreviveu</h3></div><p class="que">22 famílias de estratégias, 84 variações e a única regra que passou em todos os testes.</p><span class="enl">{{desc_btn}} ↓</span></a><a class="pilar" href="{{r}}descargas/relatorio-swaps.pdf" target="_blank" rel="noopener" style="text-decoration:none"><div class="p-cab"><span class="p-ic"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/></svg></span><h3 style="font-size:1.05rem">O custo invisível de um robô de CFD</h3></div><p class="que">Quanto os swaps de uma corretora real levaram em 4 anos, e o que revisar antes de usar um EA.</p><span class="enl">{{desc_btn}} ↓</span></a><a class="pilar" href="{{r}}descargas/guia-bcb-519-520-521.pdf" target="_blank" rel="noopener" style="text-decoration:none"><div class="p-cab"><span class="p-ic"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/></svg></span><h3 style="font-size:1.05rem">Guia Resoluções BCB 519, 520 e 521</h3></div><p class="que">As novas regras do Banco Central para cripto, desde quando valem e o que muda para você.</p><span class="enl">{{desc_btn}} ↓</span></a>',
    tema_aria="Alternar entre tema escuro e claro", tab_cripto="Criptomoedas", tab_acciones="Ações EUA", tab_b3="Brasil B3", tab_futuros="Futuros", tab_economia="Economia",
    nota_acciones="As ações com mais movimento do dia nos EUA.", nota_b3="Ibovespa, ações e minicontratos da B3.",
    nota_futuros="Minicontratos da B3 e, como referência global, índices e commodities (incluindo a soja) em CFD.", nota_forex="Moedas da região frente ao dólar e os pares principais.",
    nota_cal="Calendário econômico: próximos dados e indicadores por país.", nota_tv="Dados da TradingView; alguns mercados aparecem com atraso conforme a bolsa.",
    mapa_t="Inflação no mundo", mapa_p="Variação anual dos preços ao consumidor por país. Passe o cursor (ou toque) em um país.",
    sello_sub="Inteligência de Fluxo de Mercado", at_a="Resultados abertos", at_b="EA para MetaTrader 5", at_c="Robôs, auditorias, painéis",
    en_vivo="AO VIVO", en_vivo_btn="Ao vivo", ley_vivo="Candles de 1 minuto, ao vivo",
    mv_vol="Mercado ao vivo", mv_h2="Assim o mercado se move <span>agora</span>",
    mv_p="Cripto em tempo real, ações dos EUA e da B3, futuros, forex e economia: escolha uma aba. O gráfico interativo é para você usar.",
    mv_activo="Ativo", mv_precio="Preço", mv_tend="Últimas 24 h", mv_fuente="Preços da Binance em tempo real. Não são recomendações.",
    tv_t="Teste: gráfico interativo", tv_nota="Gráfico da", tv_af="link de afiliado", tv_link=TV, tv_locale="br",
    lang="pt-BR", r="../", inicio="./", url="https://wiqonlab.com/br/", og_locale="pt_BR", prioridad="BR", canal="wiqonbr",
    titulo="WIQON Brasil — Testamos estratégias com dados reais",
    descripcion="Laboratório de trading da fronteira Brasil–Paraguai: testamos estratégias com custos reais, publicamos os resultados e construímos ferramentas com o que sobrevive, como o WIQON Shield.",
    saltar="Ir para os produtos", nav_aria="Seções", idioma_aria="Idioma",
    n_prod="Produtos", n_lab="Laboratório", n_datos="Dados", n_serv="Serviços", n_noticias="Notícias",
    es_on="", br_on='class="on"', cta_nav="WIQON Shield", cta_nav_href="#shield",
    kicker="Brasil · Paraguai · Mercados",
    h1a="Testamos estratégias com dados reais.", h1b="Construímos ferramentas com o que sobrevive.",
    sub="Pesquisamos mercados, medimos custos e validamos ideias antes de transformá-las em software, dados ou serviços. Se uma ideia não sobrevive, também publicamos.",
    cta1="Explorar a WIQON", cta2="Ver laboratório",
    panel_aria="Bitcoin e o estado da nossa regra de tendência", graf_aria="Candles diários do Bitcoin com a média de 100 dias",
    rango_aria="Período do gráfico", ley_velas="Candles diários fechados", ley_media="Média de 100 dias",
    h_cierre="Fechamento diário", h_dist="Distância da média 100", h_desde="Neste estado desde",
    regla_t="Nossa regra", regla_p="Ficar em BTC só se o fechamento diário estiver acima da média de 100 dias. Se cair abaixo, USDT. Operamos com capital real.",
    regla_link="Ver metodologia",
    prueba_aria="Como trabalhamos", p1="Dados reais", p1s="Preços públicos, anos de histórico",
    p2="Custos incluídos", p2s="Taxas, slippage e swaps", p3="Fora da amostra", p3s="Validamos em períodos não vistos",
    p4="Código aberto", p4s="Qualquer pessoa pode refazer",
    foto_alt="Ponte da Amizade entre Foz do Iguaçu e Ciudad del Este", ciudades="Foz do Iguaçu · Ciudad del Este · Asunción",
    prod_vol="O que construímos", prod_h2="O que <span>oferecemos</span>",
    prod_p="Pesquisa aberta, um produto para gestão de risco e serviços técnicos. Tudo sai do mesmo processo de testes.",
    problema="Para que serve:",
    a_t="Laboratório de estratégias", a_chip="Aberto",
    a_que="Testamos ideias populares de trading com anos de dados, custos reais e validação fora da amostra, e publicamos o resultado.",
    a_prob="saber se uma estratégia tem vantagem antes de arriscar dinheiro nela.",
    a_evid=('<div class="comp"><div><span class="lbl">Testadas</span><div class="num">20+</div></div><div><span class="lbl">Sobreviveu</span><div class="num">1</div></div></div>'
            '<div style="margin-top:12px"><span class="lbl">Filtro de tendência BTC · 2018-2026, com custos</span>'
            '<div class="comp" style="margin-top:6px"><div><span class="lbl">Regra</span><div class="num" style="font-size:1.15rem">56,6%<small>ao ano</small></div><div class="barra-c"><i style="width:100%;background:var(--cian)"></i></div></div>'
            '<div><span class="lbl">Segurar</span><div class="num" style="font-size:1.15rem">37,3%<small>ao ano</small></div><div class="barra-c"><i style="width:66%;background:var(--gris2)"></i></div></div></div></div>'
            '<div class="tags"><span>Custos incluídos</span><span>Fora da amostra</span><span>Histórico + real</span></div>'),
    a_cta="Ver resultados", a_lim="Resultados passados não garantem os futuros.",
    b_chip="Expert Advisor · em breve no Brasil", b_chip_cls="pronto",
    b_que="Gestão de risco automática para MetaTrader 5: mantém a posição em BTC enquanto a tendência continua e fecha quando ela quebra.",
    b_prob="não ficar comprado durante uma queda longa, com uma regra clara e sem decisões impulsivas.",
    b_evid=('<div class="t5"><span>MT5 · BTCUSD · D1</span><span>WIQON Shield</span></div>'
            '<ul><li>Regra: fechamento &gt; média 100</li><li>Decide com candle fechado</li><li>Só comprado, sem alavancagem própria</li><li>Painel de estado no gráfico</li></ul>'
            '<div class="comp" style="margin-top:12px;font-family:var(--sans)"><div><span class="lbl">Queda máx. Shield</span><div class="num" style="font-size:1.15rem">39%</div><div class="barra-c"><i style="width:58%;background:var(--sube)"></i></div></div>'
            '<div><span class="lbl">Queda máx. segurar</span><div class="num" style="font-size:1.15rem">67%</div><div class="barra-c"><i style="width:100%;background:var(--baja)"></i></div></div></div>'
            '<p class="limite" style="margin-top:8px;font-family:var(--sans)">Teste com custos reais de uma corretora, 2022-2026. Os swaps reduziram um terço da vantagem.</p>'),
    b_href=f"{WA}?text=Ol%C3%A1%20WIQON%2C%20quero%20entrar%20na%20lista%20do%20WIQON%20Shield.", b_cta="Entrar na lista", b_lim="Não garante lucro.",
    c_t="Dados e automação", c_chip="Serviços",
    c_que="Robôs, auditorias e painéis feitos com a mesma metodologia do laboratório.",
    c_prob="automatizar e medir a sua operação sem depender de promessas.",
    c_lista="".join([serv("lupa", "Auditoria de estratégias", "Disponível", "ok"), serv("bot", "Robôs para Binance", "Disponível", "ok"),
                     serv("panel", "Dashboards e capacitação", "Disponível", "ok"), serv("api", "API de dados do laboratório", "Em breve", "pronto")]),
    c_href=f"{WA}?text=Ol%C3%A1%20WIQON%2C%20quero%20saber%20sobre%20um%20servi%C3%A7o.", c_cta="Fale com a gente",
    met_vol="Metodologia", met_h2="Como decidimos o que <span>sobrevive</span>",
    met_p="Não é sorte, é processo. Cada ideia passa pelos mesmos filtros antes de virar ferramenta ou dado.",
    pasos=pasos([("Hipótese", "Pegamos uma ideia concreta de mercado."), ("Regras exatas", "Entradas, saídas e tamanho, sem ambiguidade."),
                 ("Backtest com custos", "Anos de dados, taxas, slippage e swaps."), ("Fora da amostra", "Validamos em períodos que não vimos."),
                 ("Real, se sobreviver", "Só então vira produto ou serviço.")]),
    principios="".join(f"<span><b>{a}</b> · {b}</span>" for a, b in [("Fontes primeiro", "cada dado com origem e data"), ("Custos reais", "sem resultado maquiado"),
                 ("O ruim também é publicado", "a maioria não funciona"), ("Notícia não é sinal", "informamos, não recomendamos"), ("Código aberto", "você pode refazer")]),
    tabla_cap="Resultados publicados do laboratório", lx_hip="Hipótese", lx_tipo="Tipo", lx_res="Resultado", lx_ver="Veredito",
    experimentos="".join([
        exp("Filtro de tendência no BTC", "hist", "HISTÓRICO", "56,6% ao ano contra 37,3% de segurar; queda 34,7% contra 76,6% (2018-2026)", "Sobrevive", "si", f"{LAB}#3-lo-que-sobrevivió-filtro-de-tendencia-en-btc"),
        exp("A mesma regra no MT5 (CFD)", "hist", "HISTÓRICO", "x2,02 contra x1,96; queda 39% contra 67%. Swaps: um terço da vantagem", "Com ressalvas", "ojo", f"{LAB}/tree/main/resultados/mt5"),
        exp("Day trade EMA21 Bounce", "hist", "HISTÓRICO", "+0,71% em 3 anos contra +9,3% no Earn", "Não", "no", f"{LAB}#1-una-estrategia-validada-que-era-ruido"),
        exp("Rotação de altcoins", "hist", "HISTÓRICO", "33,7% ao ano com as moedas de hoje; 1,0% com as de 2021", "Não (viés)", "no", f"{LAB}#2-el-sesgo-de-supervivencia-infla-todo"),
        exp("Arbitragem entre 6 exchanges", "med", "MEDIÇÃO", "69 oportunidades em 24 h; quase nenhuma real", "Não", "no", f"{LAB}#4-arbitraje-medido-no-supuesto"),
        exp("Funding carry", "hist", "HISTÓRICO", "7-10% ao ano, quase tudo de 2021; 2-3% em 2025-26", "Não", "no", f"{LAB}#5-arbitraje-de-funding-cash-and-carry"),
    ]),
    lab_ley="HISTÓRICO: simulado com dados passados · MEDIÇÃO: observado ao vivo, sem operar · REAL: operado com dinheiro.",
    vivo_aria="Estratégia ao vivo", vivo_nombre="Filtro de tendência no BTC", cargando="Carregando…",
    d_cierre="Fechamento", d_media="Média 100", d_dist="Distância",
    vivo_nota="Recalculada todo dia às 21h15 (Brasília) com o candle fechado. Não é recomendação de investimento.",
    snap_vol="Mercado em contexto", snap_h2="A região também importa",
    snap_p="Dados do Brasil e do Paraguai de fontes oficiais, com a data. Sem sinais, sem promessas.",
    snap_mas="Ver todas as cotações oficiais", tc_moneda="Moeda", tc_valor="Valor", tc_fuente="Instituição", tc_fecha="Data",
    cambio_nota="São referências oficiais (BCB, BCP, BCRA, TRM). Bancos e casas de câmbio aplicam o próprio preço de compra e venda.",
    radar_vol="News Radar", radar_h2="Contexto de mercado",
    radar_p="Negócios, fintech e cripto da região, com a fonte original. Primeiro o Brasil, depois o Paraguai e a América hispânica.",
    filtros_aria="Filtros do radar", f_region="País", f_todas="Todos", f_la="América hispânica", f_periodo="Período", f_3d="3 dias", f_7d="7 dias",
    f_idioma="Idioma", f_todos="Todos", f_cat="Tema", opciones_cat=opciones("Todos", CAT_PT),
    radar_nota="Notícia não é sinal. As notícias em espanhol mantêm o título original.", ver_mas="Ver mais", ver_completo="Ver radar completo",
    historias="".join([
        historia("Brasil em foco", "Novas regras do BC para prestadoras de ativos virtuais já valem",
                 "As Resoluções BCB 519, 520 e 521 valem desde 1º/10/2026; o envio de dados para supervisão começa em 1º/1/2027.",
                 f'Equipe WIQON · 07/10/2026 · <a href="{BCB_RES.format(n=520)}" target="_blank" rel="noopener">fonte oficial</a>'),
        historia("No Paraguai", "Cripto na declaração: o que pede a DNIT",
                 "A RG DNIT nº 47/2026 exige informar operações com criptoativos de quem passa de US$ 5.000 por ano no Paraguai, e das plataformas que atuam no país.",
                 f'Equipe WIQON · 07/10/2026 · <a href="{DNIT_RG47}" target="_blank" rel="noopener">fonte oficial</a>'),
        historia("Por que importa", "O custo invisível de um robô de CFD",
                 "Nosso EA ganhou US$ 14.475 no preço e pagou US$ 4.241 em swaps com uma corretora real. Quase um terço foi para o financiamento.",
                 f'Laboratório WIQON · <a href="{LAB}/tree/main/resultados/mt5" target="_blank" rel="noopener">relatório</a>'),
    ]),
    nos_vol="Quem somos", cita="Publicamos o que encontramos, <span>inclusive quando o resultado é ruim.</span>",
    nos_texto=("<p>A WIQON nasceu na fronteira entre o Brasil e o Paraguai, onde o real, o guaraní e o dólar convivem todos os dias. A gente testa, mede e, se não sobrevive, publica do mesmo jeito.</p>"
               "<p>Não vendemos sinais nem administramos dinheiro de terceiros.</p>"),
    fundador_rol="Fundador e pesquisador",
    redes=redes([("YouTube", "https://www.youtube.com/@wiqonbr"), ("Instagram", "https://www.instagram.com/wiqonbr/"), ("TikTok", "https://www.tiktok.com/@wiqonbr"),
                 ("X", "https://x.com/wiqonbr"), ("Telegram", "https://t.me/wiqonlab"), ("WhatsApp", "https://whatsapp.com/channel/0029Vb8Tk5XCcW4zVk21xx0D"),
                 ("Discord", "https://discord.gg/8GDqe8H7R7"), ("LinkedIn", "https://www.linkedin.com/company/wiqonlab")]),
    faq=faq([("Vocês vendem sinais ou administram dinheiro de terceiros?", "Não. Publicamos pesquisa e oferecemos software e serviços técnicos."),
             ("O WIQON Shield garante lucro?", "Não. Ele busca limitar as grandes quedas; em mercados que só sobem, rende menos que segurar."),
             ("De onde vêm os dados?", "Preços públicos da Binance, cotações do BCB, BCP, BCRA e TRM, e RSS públicos de veículos e instituições.")]),
    vid_vol="O laboratório em vídeo", vid_sub="Inscrever-me no canal",
    foto2_alt="Centro de Ciudad del Este", foto2_cap="Ciudad del Este, Alto Paraná (Paraguai).", foto2_cred=credito("cde", "Foto"), foto1_cred=credito("puente2", "Ponte da Amizade"),
    pie_desc="Laboratório de trading e dados de mercado, direto da fronteira Brasil–Paraguai.", pie_fuentes="Fontes de dados", pie_her="Ferramentas que usamos",
    pie_her_links=herr("afiliado", "indicação"), pie_cont="Contato", pie_fuentes_links=FUENTES_PIE, wa_hola=f"{WA}?text=Ol%C3%A1%20WIQON", lab=LAB,
    pie_act_t="Atualização.", pie_act="Notícias: a cada 30 minutos. Câmbio oficial: a cada hora (cada instituição publica no seu horário). Estratégia: todo dia às 21h15 (Brasília). Preço do BTC: ao abrir a página.",
    pie_met_t="Metodologia.", pie_met="Resultados com custos e código no GitHub. O radar usa só RSS públicos: título, fonte, data e link, nunca o texto das matérias.",
    pie_priv_t="Privacidade.", pie_priv="Sem cookies. Medimos visitas com o Cloudflare Web Analytics, que não usa cookies nem identifica pessoas. Os vídeos do YouTube só carregam ao tocar em reproduzir. O gráfico interativo é fornecido pela TradingView e carrega ao chegar nessa seção. As fontes vêm do Google Fonts.",
    pie_riesgo_t="Aviso de risco.", pie_riesgo="Conteúdo informativo e educacional; não é recomendação de investimento. Operar envolve risco de perda e resultados passados não garantem os futuros. Os links marcados como afiliado ou indicação nos dão uma comissão sem custo extra para você.",
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
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(html, encoding="utf-8", newline="\n")
    print("OK", destino.relative_to(RAIZ))


if __name__ == "__main__":
    construir(ES, RAIZ / "index.html")
    construir(BR, RAIZ / "br" / "index.html")
