// WIQON v3: barra de datos, dato del día, News Radar, tipo de cambio oficial y videos.
// Todo sale de archivos generados por scripts/ (noticias.json, cambio.json, videos.json,
// estado.json) o de datos públicos de Binance. Nunca se inventa una hora ni un valor.
(function () {
  const PT = document.documentElement.lang.toLowerCase().startsWith("pt");
  const LOC = PT ? "pt-BR" : "es-PY";
  const TZ = PT ? "America/Sao_Paulo" : "America/Asuncion";
  const RAIZ = document.body.dataset.raiz || "";
  const $ = (s, r = document) => r.querySelector(s);
  const T = PT ? {
    hace: "há", min: "min", h: "h", d: "d", ahora: "agora", act: "Atualizado", ult: "Última atualização",
    viejo: "Os dados podem estar desatualizados.", caidas: "fonte(s) sem responder, mostrando as últimas notícias conhecidas:",
    vacio: "Não há notícias com esses filtros neste período.", error: "Não foi possível carregar o radar agora. Tente recarregar a página.",
    mas: "mais fonte(s)", todos: "Todos", todas: "Todas", py: "Paraguai", br: "Brasil", la: "América hispânica",
    verMas: "Ver mais notícias", fuentes: "fontes ativas", consultado: "consultado",
    ultConocido: "último dado conhecido", cargando: "Carregando…",
    cats: { regulacion: "Regulação", impuestos: "Impostos", criptoactivos: "Criptoativos", stablecoins: "Stablecoins", pagos: "Pagamentos",
            fintech: "Fintech", finanzas: "Finanças", mercados: "Mercados", macroeconomia: "Macroeconomia", empresas: "Empresas", seguridad: "Segurança" },
  } : {
    hace: "hace", min: "min", h: "h", d: "d", ahora: "recién", act: "Actualizado", ult: "Última actualización",
    viejo: "El dato puede estar desactualizado.", caidas: "fuente(s) sin responder, mostramos sus últimas noticias conocidas:",
    vacio: "No hay noticias con estos filtros en este período.", error: "No pudimos cargar el radar ahora. Probá recargar la página.",
    mas: "fuente(s) más", todos: "Todos", todas: "Todas", py: "Paraguay", br: "Brasil", la: "Hispanoamérica",
    verMas: "Ver más noticias", fuentes: "fuentes activas", consultado: "consultado",
    ultConocido: "último dato conocido", cargando: "Cargando…",
    cats: { regulacion: "Regulación", impuestos: "Impuestos", criptoactivos: "Criptoactivos", stablecoins: "Stablecoins", pagos: "Pagos",
            fintech: "Fintech", finanzas: "Finanzas", mercados: "Mercados", macroeconomia: "Macroeconomía", empresas: "Empresas", seguridad: "Seguridad" },
  };
  const json = (f) => fetch(RAIZ + f + "?t=" + Math.floor(Date.now() / 60000)).then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); });
  const num = (v, d = 2) => Number(v).toLocaleString(LOC, { minimumFractionDigits: d, maximumFractionDigits: d });
  const fechaCorta = (iso) => { const [a, m, d] = iso.slice(0, 10).split("-"); return `${d}/${m}/${a}`; };
  const horaLocal = (iso) => new Date(iso).toLocaleString(LOC, { timeZone: TZ, day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit", hour12: false });
  function hace(iso) {
    const m = Math.max(0, Math.round((Date.now() - new Date(iso).getTime()) / 60000));
    if (m < 2) return T.ahora;
    if (m < 60) return `${T.hace} ${m} ${T.min}`;
    if (m < 60 * 24) return `${T.hace} ${Math.round(m / 60)} ${T.h}`;
    return `${T.hace} ${Math.round(m / 1440)} ${T.d}`;
  }
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  // ---------- fecha del día ----------
  const hoy = $("#hoy");
  if (hoy) {
    const t = new Date().toLocaleDateString(LOC, { timeZone: TZ, weekday: "long", day: "numeric", month: "long", year: "numeric" });
    hoy.textContent = t.charAt(0).toUpperCase() + t.slice(1);
  }

  // ---------- Bitcoin en la barra (Binance, dato público) ----------
  fetch("https://data-api.binance.vision/api/v3/ticker/24hr?symbol=BTCUSDT").then((r) => r.json()).then((t) => {
    const el = $("#b-btc"); if (!el) return;
    const c = +t.priceChangePercent;
    el.innerHTML = `US$ ${num(+t.lastPrice, 0)} <span style="color:var(--${c >= 0 ? "sube" : "baja"})">${c >= 0 ? "+" : ""}${num(c, 1)}%</span>`;
  }).catch(() => {});

  // ---------- dato del día: estrategia (estado.json) ----------
  json("estado.json").then((e) => {
    const el = $("#dato-dia"); if (!el) return;
    const dist = (e.distancia_pct > 0 ? "+" : "") + num(e.distancia_pct, 1) + "%";
    el.innerHTML = PT
      ? `Bitcoin fechou a <b>US$ ${num(e.cierre, 0)}</b>, <b>${dist}</b> em relação à média de 100 dias (US$ ${num(e.sma100, 0)}). Nossa regra está <b>${e.senal === "EN_BTC" ? "EM BTC" : "EM USDT"}</b> desde ${fechaCorta(e.desde)}.`
      : `Bitcoin cerró en <b>US$ ${num(e.cierre, 0)}</b>, <b>${dist}</b> respecto a su media de 100 días (US$ ${num(e.sma100, 0)}). Nuestra regla está <b>${e.senal === "EN_BTC" ? "EN BTC" : "EN USDT"}</b> desde el ${fechaCorta(e.desde)}.`;
    const f = $("#dato-dia-f");
    if (f) f.textContent = (PT ? "Fonte: Binance, candle diário fechado de " : "Fuente: Binance, vela diaria cerrada del ") + fechaCorta(e.vela) + (PT ? ". Não é recomendação." : ". No es una recomendación.");
    document.querySelectorAll("[data-vivo='btc']").forEach((s) => (s.textContent = `${dist} ${PT ? "vs. média de 100 dias" : "vs. media de 100 días"}`));
  }).catch(() => {});

  // ---------- tipo de cambio oficial (cambio.json) ----------
  json("cambio.json").then((c) => {
    const filas = [];
    const bandera = { PY: "Paraguay", BR: "Brasil", AR: "Argentina", CO: "Colombia" };
    c.fuentes.forEach((f) => f.valores.forEach((v) => filas.push({ f, v })));
    const tb = $("#tabla-cambio tbody");
    if (tb) {
      tb.innerHTML = filas.map(({ f, v }) => {
        const dec = v.valor >= 100 ? 2 : 4;
        const nombre = PT ? ({ "Dólar estadounidense": "Dólar americano", "Real brasileño": "Real brasileiro", "Dólar (venta)": "Dólar (venda)" }[v.nombre] || v.nombre) : v.nombre;
        return `<tr><td>${esc(nombre)}<span class="u"> · ${esc(v.unidad)}</span></td>
          <td class="v">${num(v.valor, dec)}</td>
          <td class="ocultar-m"><a href="${esc(f.url)}" target="_blank" rel="noopener">${esc(f.institucion)}</a><span class="u"> · ${esc(f.serie)}</span></td>
          <td>${fechaCorta(f.fecha)}${f.ok ? "" : `<span class="vieja">${T.ultConocido}</span>`}</td></tr>`;
      }).join("");
    }
    const act = $("#cambio-act");
    if (act) act.textContent = `${T.consultado} ${horaLocal(c.actualizado_utc)}`;
    const get = (id, mon) => { const f = c.fuentes.find((x) => x.id === id); const v = f && f.valores.find((x) => x.moneda === mon); return v && { v: v.valor, fecha: f.fecha }; };
    const pyg = get("bcp", "USD"), brl = get("bcp", "BRL"), ptax = get("bcb", "USD");
    const b1 = $("#b-pyg"); if (b1 && pyg) b1.textContent = "₲ " + num(pyg.v, 2);
    const b2 = $("#b-brl"); if (b2 && ptax) b2.textContent = "R$ " + num(ptax.v, 4);
    document.querySelectorAll("[data-vivo='pyg']").forEach((s) => pyg && (s.textContent = `₲ ${num(pyg.v, 2)} (BCP, ${fechaCorta(pyg.fecha)})`));
    document.querySelectorAll("[data-vivo='brl']").forEach((s) => brl && ptax && (s.textContent = `₲ ${num(brl.v, 2)} (BCP) · R$ ${num(ptax.v, 4)} ${PT ? "por dólar" : "por dólar"} (PTAX, ${fechaCorta(ptax.fecha)})`));
  }).catch(() => { const tb = $("#tabla-cambio tbody"); if (tb) tb.innerHTML = `<tr><td colspan="4" class="u">${T.error}</td></tr>`; });

  // ---------- News Radar (noticias.json) ----------
  const radar = $("#radar");
  if (radar) {
    const prioridad = radar.dataset.prioridad || "PY";
    const est = { region: "todas", idioma: "todos", cat: "todas", horas: 72, limite: 12 };
    let datos = null;
    const lista = $("#radar-lista"), principal = $("#radar-principal"), info = $("#radar-info"), aviso = $("#radar-aviso");
    principal.innerHTML = `<div class="esq"></div><div class="esq"></div>`;
    lista.innerHTML = Array(5).fill(`<li class="esq"></li>`).join("");

    function meta(n) {
      const regionCls = n.pais === "PY" ? "PY" : n.pais === "BR" ? "BR" : "L";
      const cat = T.cats[n.categorias[0]] || n.categorias[0];
      return `<div class="linea-meta"><span class="pais ${regionCls}">${esc(n.pais_nombre)}</span><span class="cat">${esc(cat)}</span>
        <time datetime="${n.publicado_utc}" title="${horaLocal(n.publicado_utc)}">${hace(n.publicado_utc)}</time>
        <span class="fuente-b${n.tipo === "oficial" ? " of" : ""}">${esc(n.fuente)}</span><span class="idi" title="${n.idioma === "pt" ? "Português" : "Español"}">${n.idioma.toUpperCase()}</span></div>`;
    }
    function relacionadas(n) {
      if (!n.relacionadas || !n.relacionadas.length) return "";
      return `<details class="mas-f"><summary>+${n.relacionadas.length} ${T.mas}</summary>${n.relacionadas.map((r) =>
        `<div><a href="${esc(r.url)}" target="_blank" rel="noopener">${esc(r.fuente)}</a>: ${esc(r.titulo)}</div>`).join("")}</details>`;
    }
    const enlace = (n) => `<a href="${esc(n.url)}" target="_blank" rel="noopener" lang="${n.idioma === "pt" ? "pt-BR" : "es"}">${esc(n.titulo)}</a>`;

    // Con "Todas", intercala regiones según su peso editorial (la de la página primero)
    const PESOS = prioridad === "BR" ? { BR: 0.45, PY: 0.30, LATAM: 0.25 } : { PY: 0.45, BR: 0.30, LATAM: 0.25 };
    function mezclar(ns) {
      const colas = { PY: [], BR: [], LATAM: [] };
      ns.forEach((n) => (colas[n.region] || colas.LATAM).push(n));
      const usados = { PY: 0, BR: 0, LATAM: 0 }, salida = [];
      while (salida.length < ns.length) {
        const r = Object.keys(PESOS).filter((k) => colas[k].length).sort((a, b) => usados[a] / PESOS[a] - usados[b] / PESOS[b])[0];
        salida.push(colas[r].shift()); usados[r]++;
      }
      return salida;
    }

    function pintar() {
      if (!datos) return;
      const limite = Date.now() - est.horas * 3600e3;
      let ns = datos.noticias.filter((n) =>
        (est.region === "todas" || n.region === est.region) &&
        (est.idioma === "todos" || n.idioma === est.idioma) &&
        (est.cat === "todas" || n.categorias.includes(est.cat)) &&
        new Date(n.publicado_utc).getTime() >= limite);
      if (est.region === "todas") ns = mezclar(ns);
      if (!ns.length) {
        principal.innerHTML = ""; lista.innerHTML = `<li class="estado-r">${T.vacio}</li>`; $("#radar-mas").hidden = true; return;
      }
      const [p, ...resto] = ns;
      principal.innerHTML = `${meta(p)}<h3>${enlace(p)}</h3>${relacionadas(p)}`;
      lista.innerHTML = resto.slice(0, est.limite).map((n) => `<li class="nota-n">${meta(n)}<h3>${enlace(n)}</h3>${relacionadas(n)}</li>`).join("");
      $("#radar-mas").hidden = resto.length <= est.limite;
    }

    radar.querySelectorAll("[data-f]").forEach((b) => b.addEventListener("click", () => {
      const [k, v] = b.dataset.f.split(":");
      est[k] = k === "horas" ? +v : v;
      est.limite = 12;
      radar.querySelectorAll(`[data-f^="${k}:"]`).forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
      pintar();
    }));
    radar.querySelectorAll("select[data-s]").forEach((s) => s.addEventListener("change", () => { est[s.dataset.s] = s.value; est.limite = 12; pintar(); }));
    $("#radar-mas").addEventListener("click", () => { est.limite += 12; pintar(); });

    json("noticias.json").then((d) => {
      datos = d;
      const ok = d.fuentes.filter((f) => f.ok).length;
      const viejo = Date.now() - new Date(d.actualizado_utc).getTime() > 3 * 3600e3;
      info.innerHTML = viejo
        ? `<b>${T.ult}:</b> ${horaLocal(d.actualizado_utc)} · ${ok}/${d.fuentes.length} ${T.fuentes}`
        : `<b>${T.act} ${hace(d.actualizado_utc)}</b> · ${ok}/${d.fuentes.length} ${T.fuentes}`;
      const caidas = d.fuentes.filter((f) => !f.ok).map((f) => f.nombre);
      aviso.textContent = (viejo ? T.viejo + " " : "") + (caidas.length ? `${caidas.length} ${T.caidas} ${caidas.join(", ")}.` : "");
      pintar();
    }).catch(() => { principal.innerHTML = ""; lista.innerHTML = `<li class="estado-r error">${T.error}</li>`; info.textContent = ""; });
  }

  // ---------- videos (videos.json): miniatura primero, reproductor al tocar ----------
  const vbox = $("#videos");
  if (vbox) {
    const canal = vbox.dataset.canal;
    json("videos.json").then((d) => {
      const vs = (d.canales[canal] || {}).videos || [];
      if (!vs.length) return;
      const boton = (v, grande) => `<button class="vid" type="button" data-id="${esc(v.id)}" aria-label="${PT ? "Reproduzir" : "Reproducir"}: ${esc(v.titulo)}">
        <img src="https://i.ytimg.com/vi/${esc(v.id)}/${grande ? "hqdefault" : "mqdefault"}.jpg" alt="" loading="lazy"><span class="play"></span></button>`;
      const titulo = (t) => esc(t.replace(/#shorts/ig, "").trim());
      const [p, ...r] = vs;
      $("#vid-principal").innerHTML = `${boton(p, true)}<p class="vid-t">${titulo(p.titulo)}</p><p class="meta">${fechaCorta(p.publicado_utc)}</p>`;
      $("#vid-lista").innerHTML = r.slice(0, 4).map((v) => `<li>${boton(v, false)}<div><p>${titulo(v.titulo)}</p><small>${fechaCorta(v.publicado_utc)}</small></div></li>`).join("");
      vbox.querySelectorAll(".vid").forEach((b) => b.addEventListener("click", () => {
        b.innerHTML = `<iframe src="https://www.youtube-nocookie.com/embed/${b.dataset.id}?autoplay=1&rel=0" title="YouTube" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>`;
      }, { once: true }));
    }).catch(() => {});
  }

  // ---------- aparición suave, una sola vez ----------
  const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("on"); io.unobserve(e.target); } }), { threshold: 0.08 });
  document.querySelectorAll(".ap").forEach((el) => io.observe(el));
})();
