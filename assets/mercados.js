// WIQON · tema claro/oscuro, pestañas de mercados (widgets de TradingView), mapa de inflación
// del FMI y planeta de la portada. Los widgets se cargan recién cuando se abre cada pestaña.
(function () {
  const PT = document.documentElement.lang.toLowerCase().startsWith("pt");
  const LOC = PT ? "pt-BR" : "es-PY";
  const RAIZ = document.body.dataset.raiz || "";
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const tema = () => (document.documentElement.dataset.tema === "claro" ? "light" : "dark");
  const reducido = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ---------------- tema ----------------
  $$(".tema-btn").forEach((b) => b.addEventListener("click", () => {
    const nuevo = document.documentElement.dataset.tema === "claro" ? "oscuro" : "claro";
    document.documentElement.dataset.tema = nuevo;
    try { localStorage.setItem("wiqon-tema", nuevo); } catch (e) { /* sin almacenamiento: vale solo para esta visita */ }
    b.setAttribute("aria-pressed", String(nuevo === "claro"));
    document.dispatchEvent(new CustomEvent("wiqon:tema"));
  }));

  // ---------------- widgets de TradingView ----------------
  const cargados = new Map(); // elemento -> función que lo vuelve a dibujar (para el cambio de tema)
  function widget(el, archivo, config) {
    const dibujar = () => {
      el.innerHTML = '<div class="tradingview-widget-container" style="height:100%;width:100%"><div class="tradingview-widget-container__widget" style="height:100%;width:100%"></div></div>';
      const sc = document.createElement("script");
      sc.src = `https://s3.tradingview.com/external-embedding/${archivo}`; sc.async = true;
      sc.text = JSON.stringify(Object.assign({ locale: PT ? "br" : "es", colorTheme: tema(), theme: tema(), isTransparent: true, width: "100%", height: "100%" }, config()));
      el.firstChild.appendChild(sc);
    };
    cargados.set(el, dibujar); dibujar();
  }
  document.addEventListener("wiqon:tema", () => cargados.forEach((dibujar) => dibujar()));

  const q = (s, n) => ({ name: s, displayName: n });
  const WIDGETS = {
    "tv-cuerpo": () => widget($("#tv-cuerpo"), "embed-widget-advanced-chart.js", () => ({
      autosize: true, symbol: "BINANCE:BTCUSDT", interval: "60", timezone: PT ? "America/Sao_Paulo" : "America/Asuncion", style: "1",
      allow_symbol_change: true, calendar: false, isTransparent: false, backgroundColor: tema() === "dark" ? "#0c1624" : "#ffffff", support_host: "https://www.tradingview.com" })),
    acciones: () => widget($("#w-acciones"), "embed-widget-hotlists.js", () => ({ dateRange: "1D", exchange: "US", showChart: true, showSymbolLogo: true, showFloatingTooltip: false })),
    b3: () => widget($("#w-b3"), "embed-widget-market-quotes.js", () => ({ showSymbolLogo: true, symbolsGroups: [
      { name: PT ? "Índices e ações" : "Índices y acciones", symbols: [q("BMFBOVESPA:IBOV", "Ibovespa"), q("BMFBOVESPA:PETR4", "Petrobras PN"), q("BMFBOVESPA:VALE3", "Vale ON"),
        q("BMFBOVESPA:ITUB4", "Itaú Unibanco PN"), q("BMFBOVESPA:BBAS3", "Banco do Brasil ON"), q("BMFBOVESPA:BBDC4", "Bradesco PN"), q("BMFBOVESPA:WEGE3", "WEG ON")] },
      { name: PT ? "Futuros B3" : "Futuros B3", symbols: [q("BMFBOVESPA:WIN1!", PT ? "Mini Índice" : "Mini Índice (WIN)"), q("BMFBOVESPA:WDO1!", PT ? "Mini Dólar" : "Mini Dólar (WDO)"), q("BMFBOVESPA:IND1!", PT ? "Índice cheio" : "Índice Bovespa (IND)"), q("BMFBOVESPA:DOL1!", PT ? "Dólar cheio" : "Dólar (DOL)")] },
    ] })),
    futuros: () => widget($("#w-futuros"), "embed-widget-market-quotes.js", () => ({ showSymbolLogo: true, symbolsGroups: [
      { name: PT ? "Futuros B3" : "Futuros B3", symbols: [q("BMFBOVESPA:WIN1!", "Mini Índice"), q("BMFBOVESPA:WDO1!", "Mini Dólar"), q("BMFBOVESPA:IND1!", PT ? "Índice cheio" : "Índice Bovespa"), q("BMFBOVESPA:DOL1!", PT ? "Dólar cheio" : "Dólar")] },
      { name: PT ? "Índices globais (CFD)" : "Índices globales (CFD)", symbols: [q("FOREXCOM:SPXUSD", "S&P 500"), q("FOREXCOM:NSXUSD", "Nasdaq 100"), q("FOREXCOM:DJI", "Dow Jones")] },
      { name: PT ? "Commodities (CFD)" : "Materias primas (CFD)", symbols: [q("OANDA:XAUUSD", PT ? "Ouro" : "Oro"), q("OANDA:XAGUSD", PT ? "Prata" : "Plata"), q("TVC:USOIL", "Petróleo WTI"),
        q("OANDA:SOYBNUSD", "Soja"), q("OANDA:CORNUSD", PT ? "Milho" : "Maíz"), q("OANDA:WHEATUSD", PT ? "Trigo" : "Trigo")] },
    ] })),
    forex: () => widget($("#w-forex"), "embed-widget-market-quotes.js", () => ({ showSymbolLogo: true, symbolsGroups: [
      { name: PT ? "América do Sul" : "Sudamérica", symbols: [q("FX_IDC:USDBRL", "USD/BRL"), q("FX_IDC:USDPYG", "USD/PYG"), q("FX_IDC:USDARS", "USD/ARS"),
        q("FX_IDC:USDCLP", "USD/CLP"), q("FX_IDC:USDCOP", "USD/COP"), q("FX_IDC:USDUYU", "USD/UYU")] },
      { name: PT ? "Principais" : "Principales", symbols: [q("FX:EURUSD", "EUR/USD"), q("FX:GBPUSD", "GBP/USD"), q("FX:USDJPY", "USD/JPY"), q("CAPITALCOM:DXY", PT ? "Índice dólar (DXY)" : "Índice dólar (DXY)")] },
    ] })),
    calendario: () => widget($("#w-calendario"), "embed-widget-events.js", () => ({ importanceFilter: "0,1", countryFilter: "br,ar,us,eu,cl,co,mx,cn" })),
  };

  // el gráfico interactivo de la pestaña Cripto: al acercarse a la sección
  const tvc = $("#tv-cuerpo");
  if (tvc) {
    const ot = new IntersectionObserver((es) => { if (es.some((e) => e.isIntersecting)) { ot.disconnect(); WIDGETS["tv-cuerpo"](); } }, { rootMargin: "300px" });
    ot.observe(tvc);
  }

  // ---------------- pestañas ----------------
  const tabs = $$(".pestanas [role=tab]");
  function abrir(tab, foco) {
    tabs.forEach((t) => {
      const on = t === tab;
      t.setAttribute("aria-selected", String(on)); t.tabIndex = on ? 0 : -1;
      $("#" + t.getAttribute("aria-controls")).hidden = !on;
    });
    if (foco) tab.focus();
    const panel = $("#" + tab.getAttribute("aria-controls"));
    (panel.dataset.cargar || "").split(" ").filter(Boolean).forEach((k) => {
      if (k === "mapa") cargarMapa();
      else if (WIDGETS[k] && !panel.dataset["hecho_" + k]) { panel.dataset["hecho_" + k] = "1"; WIDGETS[k](); }
    });
  }
  tabs.forEach((t, i) => {
    t.addEventListener("click", () => abrir(t));
    t.addEventListener("keydown", (e) => {
      const d = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
      if (d) { e.preventDefault(); abrir(tabs[(i + d + tabs.length) % tabs.length], true); }
    });
  });

  // ---------------- librerías de mapas (solo cuando hacen falta) ----------------
  let libs = null;
  const cargarJS = (src) => new Promise((ok, mal) => { const s = document.createElement("script"); s.src = src; s.onload = ok; s.onerror = mal; document.head.appendChild(s); });
  const geo = () => libs || (libs = cargarJS("https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js")
    .then(() => cargarJS("https://cdnjs.cloudflare.com/ajax/libs/topojson/3.0.2/topojson.min.js"))
    .then(() => fetch("https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json").then((r) => r.json())));

  // ---------------- mapa de inflación (FMI) ----------------
  let mapaHecho = false;
  function cargarMapa() {
    if (mapaHecho) return; mapaHecho = true;
    const caja = $("#mapa-inflacion"), svgEl = $("#mapa-svg"), tip = $("#mapa-tip");
    Promise.all([geo(), fetch(RAIZ + "inflacion.json?t=" + Math.floor(Date.now() / 3600e3)).then((r) => r.json())]).then(([mundo, inf]) => {
      // nombres de país en el idioma de la página (código ISO de 2 letras; si no hay, el nombre del FMI)
      let dn = null; try { dn = new Intl.DisplayNames([PT ? "pt-BR" : "es"], { type: "region" }); } catch (e) { dn = null; }
      Object.values(inf.paises).forEach((p) => { try { if (dn && p.iso2) p.nombre = dn.of(p.iso2) || p.nombre; } catch (e) { /* queda el nombre del FMI */ } });
      const paises = topojson.feature(mundo, mundo.objects.countries).features.filter((f) => f.id !== "010"); // sin Antártida
      const W = 960, H = 470;
      const proy = d3.geoNaturalEarth1().fitSize([W, H], { type: "FeatureCollection", features: paises });
      const camino = d3.geoPath(proy);
      const cortes = [0, 2, 4, 6, 10, 20, 50];
      const colores = ["#2b6cb0", "#3a9bd5", "#7cc4a8", "#e9c46a", "#f4a261", "#e76f51", "#c0392b", "#7f1d1d"];
      const color = (v) => colores[cortes.filter((c) => v >= c).length] || colores[0];
      const svg = d3.select(svgEl).attr("viewBox", `0 0 ${W} ${H}`);
      const fmt = (v) => (v > 0 ? "+" : "") + v.toLocaleString(LOC, { maximumFractionDigits: 1 }) + "%";
      svg.selectAll("path").data(paises).join("path")
        .attr("d", camino)
        .attr("class", (f) => "pais" + (inf.paises[f.id] ? "" : " sin") + (["600", "076"].includes(f.id) ? " destacado" : ""))
        .attr("fill", (f) => (inf.paises[f.id] ? (inf.paises[f.id].valor < 0 ? "#6b7fd7" : color(inf.paises[f.id].valor)) : null))
        .attr("tabindex", (f) => (inf.paises[f.id] ? 0 : null))
        .attr("aria-label", (f) => { const p = inf.paises[f.id]; return p ? `${p.nombre}: ${fmt(p.valor)}` : null; })
        .on("mousemove focus", function (ev, f) {
          const p = inf.paises[f.id]; if (!p) { tip.hidden = true; return; }
          tip.innerHTML = `${p.nombre} · <b>${fmt(p.valor)}</b>${p.anterior != null ? ` <span style="color:var(--gris)">(${inf.anio - 1}: ${fmt(p.anterior)})</span>` : ""}`;
          const r = caja.getBoundingClientRect();
          const x = ev.clientX ? ev.clientX - r.left : this.getBoundingClientRect().left - r.left + 10;
          const y = ev.clientY ? ev.clientY - r.top : this.getBoundingClientRect().top - r.top;
          tip.style.left = Math.min(x + 12, r.width - 180) + "px"; tip.style.top = (y + 14) + "px"; tip.hidden = false;
        })
        .on("mouseleave blur", () => { tip.hidden = true; });
      const etiquetas = ["< 0%", "0-2%", "2-4%", "4-6%", "6-10%", "10-20%", "20-50%", "> 50%"];
      $("#mapa-escala").innerHTML = [["#6b7fd7", etiquetas[0]], ...colores.slice(1).map((c, i) => [c, etiquetas[i + 1]])]
        .map(([c, t]) => `<span><i style="background:${c}"></i>${t}</span>`).join("");
      const region = ["PRY", "BRA", "ARG", "URY", "BOL", "CHL", "PER", "COL", "MEX", "USA"];
      const lista = Object.values(inf.paises).filter((p) => region.includes(p.iso3)).sort((a, b) => region.indexOf(a.iso3) - region.indexOf(b.iso3));
      $("#mapa-ranking").innerHTML = lista.map((p) => `<li><span>${p.nombre}</span><b>${fmt(p.valor)}</b></li>`).join("");
      $("#mapa-fuente").innerHTML = `${PT ? "Fonte" : "Fuente"}: <a href="${inf.fuente_url}" target="_blank" rel="noopener">${inf.fuente}</a>. ` +
        (PT ? `Valores de ${inf.anio}: estimativas do FMI para o ano em curso.` : inf.nota);
    }).catch(() => { $("#mapa-fuente").textContent = PT ? "Não foi possível carregar o mapa agora." : "No pudimos cargar el mapa ahora."; });
  }

  // ---------------- planeta de la portada ----------------
  const globo = $("#globo");
  if (globo) {
    const arrancar = () => geo().then((mundo) => {
      const tierra = topojson.feature(mundo, mundo.objects.countries);
      const dpr = Math.min(2, window.devicePixelRatio || 1), S = globo.clientWidth;
      globo.width = S * dpr; globo.height = S * dpr;
      const g = globo.getContext("2d"); g.scale(dpr, dpr);
      const proy = d3.geoOrthographic().scale(S / 2 - 6).translate([S / 2, S / 2]).clipAngle(90);
      const camino = d3.geoPath(proy, g), grilla = d3.geoGraticule10();
      const PY = [-57.6, -25.3], destinos = [[-74, 40.7], [-0.1, 51.5], [139.7, 35.7], [-46.6, -23.5], [-58.4, -34.6]];
      let rot = 40, visible = true;
      new IntersectionObserver((es) => { visible = es[0].isIntersecting; }).observe(globo);
      function cuadro() {
        const claro = document.documentElement.dataset.tema === "claro";
        proy.rotate([rot, 18]);
        g.clearRect(0, 0, S, S);
        g.beginPath(); camino({ type: "Sphere" }); g.fillStyle = claro ? "rgba(10,143,184,.06)" : "rgba(34,195,238,.05)"; g.fill();
        g.lineWidth = 1; g.strokeStyle = claro ? "rgba(10,143,184,.35)" : "rgba(34,195,238,.35)"; g.stroke();
        g.beginPath(); camino(grilla); g.strokeStyle = claro ? "rgba(10,143,184,.12)" : "rgba(34,195,238,.10)"; g.lineWidth = .6; g.stroke();
        g.beginPath(); camino(tierra); g.fillStyle = claro ? "rgba(10,60,90,.18)" : "rgba(95,214,243,.16)"; g.fill();
        g.strokeStyle = claro ? "rgba(10,60,90,.25)" : "rgba(95,214,243,.25)"; g.lineWidth = .5; g.stroke();
        destinos.forEach((d) => { g.beginPath(); camino({ type: "LineString", coordinates: [PY, d] }); g.strokeStyle = claro ? "rgba(154,116,40,.6)" : "rgba(231,181,74,.55)"; g.lineWidth = 1.2; g.stroke(); });
        const p = proy(PY), dentro = d3.geoDistance(PY, [-rot, -18]) < Math.PI / 2;
        if (p && dentro) { g.beginPath(); g.arc(p[0], p[1], 4, 0, 7); g.fillStyle = "#e7b54a"; g.fill(); g.beginPath(); g.arc(p[0], p[1], 9, 0, 7); g.strokeStyle = "rgba(231,181,74,.5)"; g.stroke(); }
        if (!reducido && visible) rot = (rot + 0.08) % 360;
        if (!reducido) requestAnimationFrame(cuadro);
      }
      cuadro();
    }).catch(() => globo.remove());
    // se dibuja cuando el navegador está libre, para no demorar la carga de la página
    if ("requestIdleCallback" in window) requestIdleCallback(arrancar, { timeout: 1500 }); else setTimeout(arrancar, 600);
  }

  // un enlace puede abrir una pestaña directamente: wiqonlab.com/#economia, #b3, #forex…
  const desdeEnlace = () => { const t = $("#t-" + location.hash.slice(1)); if (t) { abrir(t); $("#mercado").scrollIntoView(); } };
  window.addEventListener("hashchange", desdeEnlace); desdeEnlace();
  const qp = new URLSearchParams(location.search).get("tema");
  if (qp === "claro" || qp === "oscuro") { document.documentElement.dataset.tema = qp; document.dispatchEvent(new CustomEvent("wiqon:tema")); }

})();
