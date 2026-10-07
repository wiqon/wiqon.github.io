// WIQON · diseño v2: cinta de precios en vivo, gráfico de BTC de la portada y animaciones.
// Datos públicos de Binance (sin claves): data-api.binance.vision y data-stream.binance.vision.
(function () {
  const pt = document.documentElement.lang.toLowerCase().startsWith("pt");
  const locale = pt ? "pt-BR" : "es-PY";
  const API = "https://data-api.binance.vision/api/v3";

  // ---------------- cinta de precios ----------------
  const PARES = ["BTC", "ETH", "SOL", "BNB", "XRP", "DOGE", "ADA", "LINK"];
  const pista = document.getElementById("cinta-pista");
  const fmt = (p) => {
    const d = p >= 1000 ? 0 : p >= 1 ? 2 : 4;
    return "$" + p.toLocaleString(locale, { minimumFractionDigits: d, maximumFractionDigits: d });
  };
  function pintarCinta(datos) {
    if (!pista) return;
    const items = PARES.filter((s) => datos[s]).map((s) => {
      const { p, c } = datos[s];
      const cls = c >= 0 ? "sube" : "baja";
      const pct = (c >= 0 ? "+" : "") + c.toFixed(2).replace(".", pt ? "," : ".") + "%";
      return `<span class="tk"><b>${s}</b><span class="p">${fmt(p)}</span><span class="c ${cls}">${pct}</span></span>`;
    }).join("");
    pista.innerHTML = items + items; // duplicado para el desplazamiento infinito
  }
  const precios = {};
  if (pista) {
    const simbolos = encodeURIComponent(JSON.stringify(PARES.map((s) => s + "USDT")));
    fetch(`${API}/ticker/24hr?symbols=${simbolos}`).then((r) => r.json()).then((lista) => {
      lista.forEach((t) => { precios[t.symbol.replace("USDT", "")] = { p: +t.lastPrice, c: +t.priceChangePercent }; });
      pintarCinta(precios);
      try {
        const streams = PARES.map((s) => s.toLowerCase() + "usdt@miniTicker").join("/");
        const ws = new WebSocket(`wss://data-stream.binance.vision/stream?streams=${streams}`);
        let pendiente = false;
        ws.onmessage = (ev) => {
          const d = JSON.parse(ev.data).data;
          const s = d.s.replace("USDT", "");
          precios[s] = { p: +d.c, c: ((+d.c - +d.o) / +d.o) * 100 };
          if (!pendiente) { pendiente = true; setTimeout(() => { pintarCinta(precios); pendiente = false; }, 3000); }
        };
      } catch (e) { /* sin WebSocket: queda el dato inicial */ }
    }).catch(() => { document.querySelector(".cinta")?.remove(); });
  }

  // ---------------- gráfico de la portada ----------------
  const lienzo = document.getElementById("lienzo");
  if (lienzo) {
    fetch(`${API}/klines?symbol=BTCUSDT&interval=1d&limit=466`).then((r) => r.json()).then((k) => {
      const cerradas = k.slice(0, -1); // la última vela sigue abierta: la estrategia solo usa velas cerradas
      const cierres = cerradas.map((v) => +v[4]);
      const sma = cierres.map((_, i) => i < 99 ? null : cierres.slice(i - 99, i + 1).reduce((a, b) => a + b, 0) / 100);
      const N = 365, c = cierres.slice(-N), m = sma.slice(-N);
      const ultimo = c[c.length - 1], media = m[m.length - 1];
      const dentro = ultimo > media;
      const ins = document.getElementById("insignia");
      if (ins) {
        ins.textContent = dentro ? (pt ? "● EM BTC" : "● EN BTC") : (pt ? "● EM USDT" : "● EN USDT");
        ins.className = "insignia " + (dentro ? "btc" : "usdt");
      }
      const pr = document.getElementById("precio-hero");
      if (pr) pr.textContent = fmt(ultimo);
      dibujar(lienzo, c, m);
    }).catch(() => { lienzo.parentElement.querySelector(".grafico-pie").textContent = pt ? "Dados indisponíveis no momento." : "Datos no disponibles en este momento."; });
  }

  function dibujar(cv, c, m) {
    const dpr = window.devicePixelRatio || 1;
    const W = cv.clientWidth, H = cv.clientHeight;
    cv.width = W * dpr; cv.height = H * dpr;
    const g = cv.getContext("2d");
    g.scale(dpr, dpr);
    const vals = c.concat(m.filter((x) => x));
    const min = Math.min(...vals) * 0.97, max = Math.max(...vals) * 1.02;
    const px = (i) => (i / (c.length - 1)) * (W - 8) + 4;
    const py = (v) => H - 18 - ((v - min) / (max - min)) * (H - 34);
    let t0 = null, hecho = false;
    const dur = 1600;
    function cuadro(ts) {
      if (!t0) t0 = ts;
      const p = Math.min(1, (ts - t0) / dur);
      const e = 1 - Math.pow(1 - p, 3);
      const n = Math.max(2, Math.floor(c.length * e));
      g.clearRect(0, 0, W, H);
      // líneas guía
      g.strokeStyle = "rgba(26,37,66,.55)"; g.lineWidth = 1;
      for (let i = 1; i < 5; i++) { const y = (H - 18) * i / 5; g.beginPath(); g.moveTo(0, y); g.lineTo(W, y); g.stroke(); }
      // zonas "en mercado" (cierre sobre la media)
      g.fillStyle = "rgba(52,214,140,.07)";
      for (let i = 0; i < n; i++) if (m[i] && c[i] > m[i]) g.fillRect(px(i) - (W / c.length) / 2, 0, W / c.length + 1, H - 18);
      // área bajo el precio
      const area = g.createLinearGradient(0, 0, 0, H);
      area.addColorStop(0, "rgba(40,200,255,.28)"); area.addColorStop(1, "rgba(40,200,255,0)");
      g.beginPath(); g.moveTo(px(0), H - 18);
      for (let i = 0; i < n; i++) g.lineTo(px(i), py(c[i]));
      g.lineTo(px(n - 1), H - 18); g.closePath(); g.fillStyle = area; g.fill();
      // precio
      g.beginPath();
      for (let i = 0; i < n; i++) i ? g.lineTo(px(i), py(c[i])) : g.moveTo(px(i), py(c[i]));
      g.strokeStyle = "#e9eef8"; g.lineWidth = 2; g.stroke();
      // media de 100 días
      g.beginPath(); let empezo = false;
      for (let i = 0; i < n; i++) { if (!m[i]) continue; empezo ? g.lineTo(px(i), py(m[i])) : g.moveTo(px(i), py(m[i])); empezo = true; }
      g.strokeStyle = "#28c8ff"; g.lineWidth = 2.5; g.setLineDash([]); g.stroke();
      // punto final
      const x = px(n - 1), y = py(c[n - 1]);
      g.beginPath(); g.arc(x, y, 4.5, 0, Math.PI * 2); g.fillStyle = "#fff"; g.fill();
      g.beginPath(); g.arc(x, y, 9, 0, Math.PI * 2); g.strokeStyle = "rgba(255,255,255,.35)"; g.lineWidth = 2; g.stroke();
      if (p < 1) requestAnimationFrame(cuadro);
      else hecho = true;
    }
    requestAnimationFrame(cuadro);
    // respaldo: si la pestaña está oculta y no hay animación, dibujar el gráfico completo igual
    setTimeout(() => { if (!hecho) { t0 = -1e9; cuadro(0); } }, dur + 400);
    window.addEventListener("resize", () => { clearTimeout(cv._r); cv._r = setTimeout(() => dibujar(cv, c, m), 250); }, { once: true });
  }

  // ---------------- aparición y contadores ----------------
  const obs = new IntersectionObserver((ents) => {
    ents.forEach((en) => {
      if (!en.isIntersecting) return;
      en.target.classList.add("on");
      en.target.querySelectorAll("[data-contar]").forEach((el) => {
        const fin = +el.dataset.contar, suf = el.dataset.suf || "", pre = el.dataset.pre || "";
        const t0 = performance.now();
        const paso = (ts) => {
          const p = Math.min(1, (ts - t0) / 1200);
          el.textContent = pre + Math.round(fin * (1 - Math.pow(1 - p, 3))) + suf;
          if (p < 1) requestAnimationFrame(paso);
        };
        requestAnimationFrame(paso);
      });
      obs.unobserve(en.target);
    });
  }, { threshold: 0.15 });
  document.querySelectorAll(".rev").forEach((el) => obs.observe(el));
})();
