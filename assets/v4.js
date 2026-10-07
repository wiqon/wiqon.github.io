// WIQON v4: gráfico de BTC de la portada, estado de la regla, snapshot de mercado,
// News Radar compacto y videos. Datos: Binance (público) y los JSON generados por scripts/.
// Nunca se inventa un valor ni una hora: si falta un dato se dice.
(function () {
  const PT = document.documentElement.lang.toLowerCase().startsWith("pt");
  const LOC = PT ? "pt-BR" : "es-PY";
  const TZ = PT ? "America/Sao_Paulo" : "America/Asuncion";
  const RAIZ = document.body.dataset.raiz || "";
  const API = "https://data-api.binance.vision/api/v3";
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const num = (v, d = 2) => Number(v).toLocaleString(LOC, { minimumFractionDigits: d, maximumFractionDigits: d });
  const fecha = (iso) => { const [a, m, d] = iso.slice(0, 10).split("-"); return `${d}/${m}/${a}`; };
  const hora = (iso) => new Date(iso).toLocaleString(LOC, { timeZone: TZ, day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit", hour12: false });
  const json = (f) => fetch(RAIZ + f + "?t=" + Math.floor(Date.now() / 60000)).then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); });
  const T = PT ? {
    hace: "há", min: "min", h: "h", d: "d", ahora: "agora", act: "Atualizado", ult: "Última atualização", fuentes: "fontes ativas",
    viejo: "Os dados podem estar desatualizados.", caidas: "fonte(s) sem responder; mostramos as últimas notícias conhecidas:",
    vacio: "Não há notícias com esses filtros neste período.", error: "Não foi possível carregar agora. Tente recarregar a página.",
    mas: "mais fonte(s)", sinDatos: "Dado indisponível agora", ultConocido: "último dado conhecido", enBtc: "EM BTC", enUsdt: "EM USDT",
    completo: "Ver radar completo", menos: "Ver menos", masN: "Ver mais notícias", play: "Reproduzir",
    cats: { regulacion: "Regulação", impuestos: "Impostos", criptoactivos: "Criptoativos", stablecoins: "Stablecoins", pagos: "Pagamentos", fintech: "Fintech",
            finanzas: "Finanças", mercados: "Mercados", macroeconomia: "Macroeconomia", empresas: "Empresas", seguridad: "Segurança" },
  } : {
    hace: "hace", min: "min", h: "h", d: "d", ahora: "recién", act: "Actualizado", ult: "Última actualización", fuentes: "fuentes activas",
    viejo: "El dato puede estar desactualizado.", caidas: "fuente(s) sin responder; mostramos sus últimas noticias conocidas:",
    vacio: "No hay noticias con estos filtros en este período.", error: "No pudimos cargar esto ahora. Probá recargar la página.",
    mas: "fuente(s) más", sinDatos: "Dato no disponible ahora", ultConocido: "último dato conocido", enBtc: "EN BTC", enUsdt: "EN USDT",
    completo: "Ver radar completo", menos: "Ver menos", masN: "Ver más noticias", play: "Reproducir",
    cats: { regulacion: "Regulación", impuestos: "Impuestos", criptoactivos: "Criptoactivos", stablecoins: "Stablecoins", pagos: "Pagos", fintech: "Fintech",
            finanzas: "Finanzas", mercados: "Mercados", macroeconomia: "Macroeconomía", empresas: "Empresas", seguridad: "Seguridad" },
  };
  function hace(iso) {
    const m = Math.max(0, Math.round((Date.now() - new Date(iso).getTime()) / 60000));
    if (m < 2) return T.ahora;
    if (m < 60) return `${T.hace} ${m} ${T.min}`;
    if (m < 1440) return `${T.hace} ${Math.round(m / 60)} ${T.h}`;
    return `${T.hace} ${Math.round(m / 1440)} ${T.d}`;
  }

  // ================= portada: velas de BTC + media 100 (solo velas cerradas) =================
  const lienzo = $("#lienzo");
  let velas = null, sma = null, rango = 90;
  function dibujar() {
    if (!velas || !lienzo) return;
    const dpr = window.devicePixelRatio || 1, W = lienzo.clientWidth, H = lienzo.clientHeight;
    lienzo.width = W * dpr; lienzo.height = H * dpr;
    const g = lienzo.getContext("2d"); g.setTransform(dpr, 0, 0, dpr, 0, 0); g.clearRect(0, 0, W, H);
    const v = velas.slice(-rango), m = sma.slice(-rango);
    const lo = Math.min(...v.map((x) => x.l), ...m.filter(Boolean)), hi = Math.max(...v.map((x) => x.h), ...m.filter(Boolean));
    const pad = (hi - lo) * 0.06, min = lo - pad, max = hi + pad, ejeX = W - 46;
    const py = (p) => 6 + (1 - (p - min) / (max - min)) * (H - 14);
    const paso = ejeX / v.length, cuerpo = Math.max(1, paso * 0.62);
    g.font = "10px JetBrains Mono, monospace"; g.fillStyle = "#5f6e82"; g.strokeStyle = "rgba(26,42,64,.8)"; g.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
      const p = min + ((max - min) * i) / 4, y = py(p);
      g.beginPath(); g.moveTo(0, y); g.lineTo(ejeX, y); g.stroke();
      g.fillText((p / 1000).toFixed(0) + "K", ejeX + 6, y + 3);
    }
    v.forEach((c, i) => {
      const x = i * paso + paso / 2, col = c.c >= c.o ? "#2fc47f" : "#ef5f67";
      g.strokeStyle = col; g.fillStyle = col;
      g.beginPath(); g.moveTo(x, py(c.h)); g.lineTo(x, py(c.l)); g.stroke();
      const y1 = py(Math.max(c.o, c.c)), y2 = py(Math.min(c.o, c.c));
      g.fillRect(x - cuerpo / 2, y1, cuerpo, Math.max(1, y2 - y1));
    });
    g.strokeStyle = "#e7b54a"; g.lineWidth = 1.8; g.beginPath(); let ini = false;
    m.forEach((val, i) => { if (!val) return; const x = i * paso + paso / 2; ini ? g.lineTo(x, py(val)) : g.moveTo(x, py(val)); ini = true; });
    g.stroke();
  }
  if (lienzo) {
    fetch(`${API}/klines?symbol=BTCUSDT&interval=1d&limit=500`).then((r) => r.json()).then((k) => {
      const cerradas = k.slice(0, -1); // la última vela sigue abierta: la regla solo usa velas cerradas
      velas = cerradas.map((x) => ({ o: +x[1], h: +x[2], l: +x[3], c: +x[4] }));
      const cs = velas.map((x) => x.c);
      sma = cs.map((_, i) => (i < 99 ? null : cs.slice(i - 99, i + 1).reduce((a, b) => a + b, 0) / 100));
      dibujar();
    }).catch(() => { lienzo.replaceWith(Object.assign(document.createElement("p"), { className: "meta", textContent: T.sinDatos })); });
    $$(".rangos button").forEach((b) => b.addEventListener("click", () => {
      rango = +b.dataset.r; $$(".rangos button").forEach((x) => x.setAttribute("aria-pressed", String(x === b))); dibujar();
    }));
    let t; window.addEventListener("resize", () => { clearTimeout(t); t = setTimeout(dibujar, 200); });
  }
  fetch(`${API}/ticker/24hr?symbol=BTCUSDT`).then((r) => r.json()).then((t) => {
    const c = +t.priceChangePercent, txt = `US$ ${num(+t.lastPrice, 0)}`;
    const var24 = `<small class="${c >= 0 ? "sube" : "baja"}">${c >= 0 ? "▲ +" : "▼ "}${num(c, 2)}% (24 h)</small>`;
    const p = $("#precio-btc"); if (p) p.innerHTML = txt + var24;
    const s = $("#snap-btc"); if (s) { s.textContent = txt; $("#snap-btc-f").innerHTML = `Binance · ${hora(new Date().toISOString())} · <span class="${c >= 0 ? "sube" : "baja"}">${c >= 0 ? "+" : ""}${num(c, 2)}% 24 h</span>`; }
  }).catch(() => { const s = $("#snap-btc"); if (s) s.textContent = "—"; });

  // ================= estado de la regla (estado.json) =================
  json("estado.json").then((e) => {
    const dentro = e.senal === "EN_BTC";
    $$(".est-regla").forEach((el) => { el.textContent = (dentro ? "● " + T.enBtc : "● " + T.enUsdt); el.className = "est est-regla " + (dentro ? "btc" : "usdt"); });
    const set = (id, v) => { const el = $(id); if (el) el.innerHTML = v; };
    set("#h-cierre", `US$ ${num(e.cierre, 0)}`);
    set("#h-dist", `<span class="${e.distancia_pct >= 0 ? "sube" : "baja"}">${e.distancia_pct >= 0 ? "+" : ""}${num(e.distancia_pct, 1)}%</span>`);
    set("#h-desde", fecha(e.desde));
    set("#h-act", `${T.act} ${hora(e.actualizado_utc.replace(" ", "T") + ":00Z")} · ${PT ? "candle de" : "vela del"} ${fecha(e.vela)}`);
  }).catch(() => { const el = $("#h-act"); if (el) el.textContent = T.sinDatos; });

  // ================= snapshot + tabla de cambio oficial (cambio.json) =================
  json("cambio.json").then((c) => {
    const get = (id, mon) => { const f = c.fuentes.find((x) => x.id === id); const v = f && f.valores.find((x) => x.moneda === mon); return v ? { v: v.valor, f } : null; };
    const pinta = (idv, idf, d, pre, dec, fuente) => {
      const v = $(idv), f = $(idf); if (!v) return;
      if (!d) { v.textContent = "—"; f.textContent = T.sinDatos; return; }
      v.textContent = pre + num(d.v, dec);
      f.textContent = `${fuente} · ${fecha(d.f.fecha)}${d.f.ok ? "" : " · " + T.ultConocido}`;
      if (!d.f.ok) f.classList.add("viejo");
    };
    pinta("#snap-pyg", "#snap-pyg-f", get("bcp", "USD"), "₲ ", 2, "BCP");
    pinta("#snap-brl", "#snap-brl-f", get("bcb", "USD"), "R$ ", 4, "BCB PTAX");
    pinta("#snap-brlpyg", "#snap-brlpyg-f", get("bcp", "BRL"), "₲ ", 2, "BCP");
    const tb = $("#tabla-cambio tbody");
    if (tb) {
      const nombrePT = { "Dólar estadounidense": "Dólar americano", "Real brasileño": "Real brasileiro", "Dólar (venta)": "Dólar (venda)" };
      tb.innerHTML = c.fuentes.flatMap((f) => f.valores.map((v) => {
        const nombre = PT ? nombrePT[v.nombre] || v.nombre : v.nombre;
        return `<tr><td>${esc(nombre)} <span class="u">· ${esc(v.unidad)}</span></td><td class="v">${num(v.valor, v.valor >= 100 ? 2 : 4)}</td>
          <td class="om"><a href="${esc(f.url)}" target="_blank" rel="noopener">${esc(f.institucion)}</a> <span class="u">· ${esc(f.serie)}</span></td>
          <td>${fecha(f.fecha)}${f.ok ? "" : ` <span class="u">(${T.ultConocido})</span>`}</td></tr>`;
      })).join("");
    }
    const a = $("#cambio-act"); if (a) a.textContent = `${T.act} ${hora(c.actualizado_utc)}`;
  }).catch(() => { ["#snap-pyg", "#snap-brl", "#snap-brlpyg"].forEach((s) => { const el = $(s); if (el) { el.textContent = "—"; el.nextElementSibling.textContent = T.sinDatos; } }); });

  // ================= News Radar (complementario) =================
  const radar = $("#radar");
  if (radar) {
    const PESOS = radar.dataset.prioridad === "BR" ? { BR: 0.45, PY: 0.30, LATAM: 0.25 } : { PY: 0.45, BR: 0.30, LATAM: 0.25 };
    const est = { region: "todas", idioma: "todos", cat: "todas", horas: 72, completo: false, limite: 12 };
    const lista = $("#radar-lista"), info = $("#radar-info"), aviso = $("#radar-aviso"), btn = $("#radar-btn"), masBtn = $("#radar-mas");
    let datos = null;
    lista.innerHTML = Array(4).fill('<li class="esq"></li>').join("");
    const mezclar = (ns) => {
      const colas = { PY: [], BR: [], LATAM: [] }; ns.forEach((n) => (colas[n.region] || colas.LATAM).push(n));
      const usados = { PY: 0, BR: 0, LATAM: 0 }, out = [];
      while (out.length < ns.length) {
        const r = Object.keys(PESOS).filter((k) => colas[k].length).sort((a, b) => usados[a] / PESOS[a] - usados[b] / PESOS[b])[0];
        out.push(colas[r].shift()); usados[r]++;
      }
      return out;
    };
    const item = (n) => `<li class="nota-n"><div class="lm"><span class="pais">${esc(n.pais_nombre)}</span><span class="cat">${esc(T.cats[n.categorias[0]] || n.categorias[0])}</span>
        <time datetime="${n.publicado_utc}" title="${hora(n.publicado_utc)}">${hace(n.publicado_utc)}</time></div>
      <h3><a href="${esc(n.url)}" target="_blank" rel="noopener" lang="${n.idioma === "pt" ? "pt-BR" : "es"}">${esc(n.titulo)}</a></h3>
      <div class="lm"><span class="fte-b${n.tipo === "oficial" ? " of" : ""}">${esc(n.fuente)}</span><span class="idi">${n.idioma.toUpperCase()}</span></div>
      ${n.relacionadas && n.relacionadas.length ? `<details class="mas-f"><summary>+${n.relacionadas.length} ${T.mas}</summary>${n.relacionadas.map((r) => `<div><a href="${esc(r.url)}" target="_blank" rel="noopener">${esc(r.fuente)}</a></div>`).join("")}</details>` : ""}</li>`;
    function pintar() {
      if (!datos) return;
      const desde = Date.now() - est.horas * 3600e3;
      let ns = datos.noticias.filter((n) => (est.region === "todas" || n.region === est.region) && (est.idioma === "todos" || n.idioma === est.idioma) &&
        (est.cat === "todas" || n.categorias.includes(est.cat)) && new Date(n.publicado_utc).getTime() >= desde);
      if (est.region === "todas") ns = mezclar(ns);
      const max = est.completo ? est.limite : 4;
      lista.classList.toggle("completo", est.completo);
      lista.innerHTML = ns.length ? ns.slice(0, max).map(item).join("") : `<li class="estado-r">${T.vacio}</li>`;
      btn.textContent = est.completo ? T.menos : T.completo;
      btn.setAttribute("aria-expanded", String(est.completo));
      masBtn.hidden = !est.completo || ns.length <= est.limite;
    }
    $$("[data-f]", radar).forEach((b) => b.addEventListener("click", () => {
      const [k, v] = b.dataset.f.split(":"); est[k] = k === "horas" ? +v : v; est.limite = 12;
      $$(`[data-f^="${k}:"]`, radar).forEach((x) => x.setAttribute("aria-pressed", String(x === b))); pintar();
    }));
    $$("select[data-s]", radar).forEach((s) => s.addEventListener("change", () => { est[s.dataset.s] = s.value; est.limite = 12; pintar(); }));
    btn.addEventListener("click", () => { est.completo = !est.completo; est.limite = 12; pintar(); });
    masBtn.addEventListener("click", () => { est.limite += 12; pintar(); });
    json("noticias.json").then((d) => {
      datos = d;
      const ok = d.fuentes.filter((f) => f.ok).length, viejo = Date.now() - new Date(d.actualizado_utc).getTime() > 3 * 3600e3;
      info.innerHTML = viejo ? `<b>${T.ult}:</b> ${hora(d.actualizado_utc)} · ${ok}/${d.fuentes.length} ${T.fuentes}`
                             : `<b>${T.act} ${hace(d.actualizado_utc)}</b> · ${ok}/${d.fuentes.length} ${T.fuentes}`;
      const caidas = d.fuentes.filter((f) => !f.ok).map((f) => f.nombre);
      aviso.textContent = (viejo ? T.viejo + " " : "") + (caidas.length ? `${caidas.length} ${T.caidas} ${caidas.join(", ")}.` : "");
      pintar();
    }).catch(() => { lista.innerHTML = `<li class="estado-r error">${T.error}</li>`; info.textContent = ""; });
  }

  // ================= videos: miniatura primero, reproductor al tocar =================
  const vbox = $("#videos");
  if (vbox) json("videos.json").then((d) => {
    const vs = ((d.canales[vbox.dataset.canal] || {}).videos || []);
    if (!vs.length) return;
    const titulo = (t) => esc(t.replace(/#shorts/ig, "").trim());
    const boton = (v, cal) => `<button class="vid" type="button" data-id="${esc(v.id)}" aria-label="${T.play}: ${titulo(v.titulo)}"><img src="https://i.ytimg.com/vi/${esc(v.id)}/${cal}.jpg" alt="" loading="lazy"><span class="play"></span></button>`;
    const [p, ...r] = vs;
    $("#vid-principal").innerHTML = `${boton(p, "hqdefault")}<p class="vid-t">${titulo(p.titulo)}</p>`;
    $("#vid-lista").innerHTML = r.slice(0, 2).map((v) => `<li>${boton(v, "mqdefault")}<p>${titulo(v.titulo)}</p></li>`).join("");
    $$(".vid", vbox).forEach((b) => b.addEventListener("click", () => {
      b.innerHTML = `<iframe src="https://www.youtube-nocookie.com/embed/${b.dataset.id}?autoplay=1&rel=0" title="YouTube" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>`;
    }, { once: true }));
  }).catch(() => {});

  // ================= aparición suave, una vez =================
  const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("on"); io.unobserve(e.target); } }), { threshold: 0.06 });
  $$(".ap").forEach((el) => io.observe(el));
  const anio = $("#anio"); if (anio) anio.textContent = new Date().getFullYear();
})();
