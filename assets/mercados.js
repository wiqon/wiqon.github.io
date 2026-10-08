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
    t.addEventListener("click", () => {
      abrir(t);
      // si la barra ya está flotando, volver al inicio del panel elegido
      const sec = $("#mercado"), barra = $(".pestanas");
      if (sec && barra && barra.getBoundingClientRect().top <= 80 && sec.getBoundingClientRect().top < 0) {
        window.scrollTo({ top: window.scrollY + barra.getBoundingClientRect().top - 76, behavior: reducido ? "auto" : "smooth" });
      }
    });
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

  // ---------------- planeta de la portada, entero, con el satélite WIQON en órbita ----------------
  const globo = $("#globo");
  if (globo) {
    const logo = new Image(); logo.src = RAIZ + "assets/logo.png";
    const arrancar = () => geo().then((mundo) => {
      const tierra = topojson.feature(mundo, mundo.objects.countries);
      const dpr = Math.min(2, window.devicePixelRatio || 1);
      let S = 0, g = null, R = 0, cx = 0, cy = 0;
      const proy = d3.geoOrthographic().clipAngle(90);
      const camino = d3.geoPath(proy);
      function medir() {
        S = globo.clientWidth; globo.width = S * dpr; globo.height = S * dpr;
        g = globo.getContext("2d"); g.setTransform(dpr, 0, 0, dpr, 0, 0);
        R = S * 0.30; cx = S / 2; cy = S / 2;
        proy.scale(R).translate([cx, cy]); camino.context(g);
      }
      medir();
      let t;
      window.addEventListener("resize", () => { clearTimeout(t); t = setTimeout(medir, 200); });
      const grilla = d3.geoGraticule10();
      const PY = [-57.6, -25.3], destinos = [[-74, 40.7], [-0.1, 51.5], [139.7, 35.7], [-46.6, -23.5], [-58.4, -34.6], [103.8, 1.35]];
      const INCL = -0.38; // inclinación de la órbita (radianes)
      let rot = 40, ang = 0.6, visible = true;
      new IntersectionObserver((es) => { visible = es[0].isIntersecting; }).observe(globo);

      const orbita = (a) => { // punto de la órbita elíptica inclinada; z>0 = delante del planeta
        const ox = Math.cos(a) * R * 1.34, oy = Math.sin(a) * R * 0.40;
        return { x: cx + ox * Math.cos(INCL) - oy * Math.sin(INCL), y: cy + ox * Math.sin(INCL) + oy * Math.cos(INCL), z: Math.sin(a) };
      };
      function trazoOrbita(delante, claro) {
        g.beginPath(); let primero = true;
        for (let a = 0; a <= Math.PI * 2 + 0.01; a += 0.04) {
          const p = orbita(a);
          if ((p.z >= 0) !== delante) { primero = true; continue; }
          primero ? g.moveTo(p.x, p.y) : g.lineTo(p.x, p.y); primero = false;
        }
        g.setLineDash([2, 6]); g.lineWidth = 1.2;
        g.strokeStyle = claro ? "rgba(10,143,184,.45)" : `rgba(95,214,243,${delante ? .55 : .25})`; g.stroke(); g.setLineDash([]);
      }
      function satelite(claro) {
        const p = orbita(ang), esc = 0.75 + 0.25 * (p.z + 1) / 2, r = S * 0.045 * esc;
        g.save(); g.globalAlpha = p.z >= 0 ? 1 : 0.55;
        // estela
        for (let i = 1; i <= 10; i++) {
          const q = orbita(ang - i * 0.035);
          g.beginPath(); g.arc(q.x, q.y, r * (1 - i / 12) * 0.35, 0, 7); g.fillStyle = `rgba(95,214,243,${0.22 * (1 - i / 11)})`; g.fill();
        }
        // corona resplandeciente
        const halo = g.createRadialGradient(p.x, p.y, r * 0.6, p.x, p.y, r * 2.2);
        halo.addColorStop(0, "rgba(139,92,246,.55)"); halo.addColorStop(0.5, "rgba(34,195,238,.25)"); halo.addColorStop(1, "rgba(34,195,238,0)");
        g.beginPath(); g.arc(p.x, p.y, r * 2.2, 0, 7); g.fillStyle = halo; g.fill();
        const anillo = g.createConicGradient ? g.createConicGradient(rot / 30, p.x, p.y) : null;
        if (anillo) { ["#22c3ee", "#2f6bff", "#8b5cf6", "#d946ef", "#22c3ee"].forEach((c, i) => anillo.addColorStop(i / 4, c)); }
        g.beginPath(); g.arc(p.x, p.y, r * 1.12, 0, 7); g.fillStyle = anillo || "#22c3ee"; g.fill();
        // paneles solares
        g.fillStyle = claro ? "rgba(10,60,90,.6)" : "rgba(95,214,243,.55)";
        g.fillRect(p.x - r * 2.1, p.y - r * 0.18, r * 0.8, r * 0.36); g.fillRect(p.x + r * 1.3, p.y - r * 0.18, r * 0.8, r * 0.36);
        // logo
        g.beginPath(); g.arc(p.x, p.y, r, 0, 7); g.fillStyle = "#000"; g.fill();
        if (logo.complete && logo.naturalWidth) { g.save(); g.beginPath(); g.arc(p.x, p.y, r * 0.92, 0, 7); g.clip(); g.drawImage(logo, p.x - r * 0.92, p.y - r * 0.92, r * 1.84, r * 1.84); g.restore(); }
        g.restore();
        return p.z >= 0;
      }
      function cuadro() {
        const claro = document.documentElement.dataset.tema === "claro";
        g.clearRect(0, 0, S, S);
        // atmósfera
        const atm = g.createRadialGradient(cx, cy, R * 0.9, cx, cy, R * 1.25);
        atm.addColorStop(0, claro ? "rgba(10,143,184,.18)" : "rgba(34,195,238,.28)"); atm.addColorStop(1, "rgba(34,195,238,0)");
        g.beginPath(); g.arc(cx, cy, R * 1.25, 0, 7); g.fillStyle = atm; g.fill();
        trazoOrbita(false, claro);
        if (orbita(ang).z < 0) satelite(claro);
        proy.rotate([rot, 18]);
        const mar = g.createRadialGradient(cx - R * .35, cy - R * .35, R * .1, cx, cy, R);
        mar.addColorStop(0, claro ? "#e8f4fa" : "#0f2a44"); mar.addColorStop(1, claro ? "#c9e2ee" : "#07121f");
        g.beginPath(); camino({ type: "Sphere" }); g.fillStyle = mar; g.fill();
        g.lineWidth = 1.2; g.strokeStyle = claro ? "rgba(10,143,184,.5)" : "rgba(34,195,238,.55)"; g.stroke();
        g.beginPath(); camino(grilla); g.strokeStyle = claro ? "rgba(10,143,184,.15)" : "rgba(34,195,238,.12)"; g.lineWidth = .6; g.stroke();
        g.beginPath(); camino(tierra); g.fillStyle = claro ? "rgba(10,90,120,.35)" : "rgba(95,214,243,.30)"; g.fill();
        g.strokeStyle = claro ? "rgba(10,60,90,.35)" : "rgba(95,214,243,.45)"; g.lineWidth = .5; g.stroke();
        destinos.forEach((d) => { g.beginPath(); camino({ type: "LineString", coordinates: [PY, d] }); g.strokeStyle = claro ? "rgba(154,116,40,.75)" : "rgba(231,181,74,.75)"; g.lineWidth = 1.3; g.stroke(); });
        const p = proy(PY);
        if (p && d3.geoDistance(PY, [-rot, -18]) < Math.PI / 2) {
          const pulso = 6 + 4 * Math.abs(Math.sin(Date.now() / 600));
          g.beginPath(); g.arc(p[0], p[1], 4, 0, 7); g.fillStyle = "#e7b54a"; g.fill();
          g.beginPath(); g.arc(p[0], p[1], pulso + 4, 0, 7); g.strokeStyle = "rgba(231,181,74,.5)"; g.lineWidth = 1.5; g.stroke();
        }
        // brillo del lado iluminado
        const luz = g.createRadialGradient(cx - R * .5, cy - R * .5, 0, cx - R * .5, cy - R * .5, R * 1.3);
        luz.addColorStop(0, "rgba(255,255,255,.10)"); luz.addColorStop(1, "rgba(255,255,255,0)");
        g.beginPath(); g.arc(cx, cy, R, 0, 7); g.fillStyle = luz; g.fill();
        trazoOrbita(true, claro);
        if (orbita(ang).z >= 0) satelite(claro);
        if (!reducido && visible) { rot = (rot + 0.08) % 360; ang = (ang + 0.006) % (Math.PI * 2); }
        if (!reducido) requestAnimationFrame(cuadro);
      }
      logo.onload = () => { if (reducido) cuadro(); };
      cuadro();
    }).catch(() => globo.remove());
    if ("requestIdleCallback" in window) requestIdleCallback(arrancar, { timeout: 1500 }); else setTimeout(arrancar, 600);
  }

  // un enlace puede abrir una pestaña directamente: wiqonlab.com/#economia, #b3, #forex…
  const desdeEnlace = () => { const t = $("#t-" + location.hash.slice(1)); if (t) { abrir(t); $("#mercado").scrollIntoView(); } };
  window.addEventListener("hashchange", desdeEnlace); desdeEnlace();
  const qp = new URLSearchParams(location.search).get("tema");
  if (qp === "claro" || qp === "oscuro") { document.documentElement.dataset.tema = qp; document.dispatchEvent(new CustomEvent("wiqon:tema")); }

})();
