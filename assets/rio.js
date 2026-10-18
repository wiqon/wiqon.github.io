// WIQON · portada: "río de operaciones". Cada operación real de BTC/USDT en Binance es un punto que
// recorre los últimos 3 minutos (cian: compra, azul: venta; tamaño: monto). Debajo, la regla de la estrategia
// con su aguja en vivo (distancia del precio a la media de 100 días de estado.json).
(function () {
  const lienzo = document.getElementById("rio");
  if (!lienzo) return;
  const raiz = document.documentElement, $ = (id) => document.getElementById(id);
  const lang = raiz.lang.toLowerCase(), PT = lang.startsWith("pt"), EN = lang.startsWith("en");
  const T = PT ? { compras: "Compras", ventas: "Vendas", vivo: "Ao vivo da Binance.", sin: "Sem conexão com a Binance: mostrando uma simulação." }
    : EN ? { compras: "Buys", ventas: "Sells", vivo: "Live from Binance.", sin: "No connection to Binance: showing a simulation." }
    : { compras: "Compras", ventas: "Ventas", vivo: "En vivo desde Binance.", sin: "Sin conexión con Binance: mostrando una simulación." };
  const LOC = PT ? "pt-BR" : EN ? "en-US" : "es-PY";
  const fmt = new Intl.NumberFormat(LOC, { maximumFractionDigits: 0 });
  const quieto = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const g = lienzo.getContext("2d");
  const VENTANA = 180e3;
  const ops = [], vistos = new Set();
  let W = 0, H = 0, bajo = 0, alto = 0, ultimo = 0, conectado = false, simulado = false, sma = null;
  const css = (v) => getComputedStyle(raiz).getPropertyValue(v).trim();
  const medida = () => { const dpr = Math.min(devicePixelRatio || 1, 2); W = lienzo.clientWidth; H = lienzo.clientHeight; lienzo.width = W * dpr; lienzo.height = H * dpr; g.setTransform(dpr, 0, 0, dpr, 0, 0); };
  addEventListener("resize", medida); medida();
  const sprites = {};
  const sprite = (color) => {
    if (sprites[color]) return sprites[color];
    const c = document.createElement("canvas"); c.width = c.height = 64; const x = c.getContext("2d");
    const grd = x.createRadialGradient(32, 32, 0, 32, 32, 32);
    grd.addColorStop(0, color); grd.addColorStop(.28, color); grd.addColorStop(.32, color + "88"); grd.addColorStop(1, color + "00");
    x.fillStyle = grd; x.fillRect(0, 0, 64, 64); return (sprites[color] = c);
  };
  // cada operación guarda su desvío: compras por encima del precio, ventas por debajo, más lejos cuanto más grande
  const agregar = (p, q, compra, t, id) => {
    if (id !== undefined) { if (vistos.has(id)) return; vistos.add(id); if (vistos.size > 20000) vistos.clear(); }
    const usd = p * q, lado = compra ? -1 : 1;
    ops.push({ t, p, usd, compra, j: lado * (0.15 + Math.random() * (0.6 + Math.min(1.6, Math.sqrt(usd / 4000)))) }); ultimo = p;
  };
  function dibujar() {
    const ahora = Date.now();
    while (ops.length && ahora - ops[0].t > VENTANA) ops.shift();
    g.clearRect(0, 0, W, H);
    if (ops.length < 2) return;
    let lo = Infinity, hi = -Infinity; for (const o of ops) { if (o.p < lo) lo = o.p; if (o.p > hi) hi = o.p; }
    const pad = Math.max((hi - lo) * .35, ultimo * .00015);
    bajo = bajo ? bajo + (lo - pad - bajo) * .06 : lo - pad; alto = alto ? alto + (hi + pad - alto) * .06 : hi + pad;
    const angosto = W < 860;
    const y = (p) => H * (angosto ? .05 : .16) + (1 - (p - bajo) / (alto - bajo)) * H * (angosto ? .17 : .58);
    const banda = angosto ? Math.max(6, H * .014) : Math.max(10, H * .035), x = (t) => W - ((ahora - t) / VENTANA) * W * (angosto ? 1 : Math.max(.5, Math.min(.62, 1 - 760 / W)));  // en pantallas anchas el río ocupa la mitad derecha
    const claro = raiz.dataset.tema === "claro";
    const segs = new Map(); for (const o of ops) { const k = Math.floor(o.t / 1000); const s = segs.get(k) || [0, 0]; s[0] += o.p * o.usd; s[1] += o.usd; segs.set(k, s); }
    g.beginPath(); let primero = true;
    for (const [k, [pv, v]] of [...segs].sort((a, b) => a[0] - b[0])) { const px = x(k * 1000 + 500), py = y(pv / v); if (primero) { g.moveTo(px, py); primero = false; } else g.lineTo(px, py); }
    g.strokeStyle = css("--suave"); g.globalAlpha = claro ? .35 : .28; g.lineWidth = 1.2; g.stroke(); g.globalAlpha = 1;
    g.globalCompositeOperation = claro ? "multiply" : "lighter";
    const cc = css("--compra"), cv = css("--venta"), sc = sprite(cc), sv = sprite(cv);
    for (const o of ops) {
      const r = Math.min(34, 4 + Math.sqrt(o.usd / 700)), edad = (ahora - o.t) / VENTANA;
      g.globalAlpha = Math.max(.08, 1 - edad * .85);
      const px = x(o.t), py = y(o.p) + o.j * banda;
      if (!quieto) { const largo = Math.min(160, 18 + r * 6), grd = g.createLinearGradient(px, 0, px + largo, 0);
        grd.addColorStop(0, o.compra ? cc : cv); grd.addColorStop(1, "transparent");
        g.strokeStyle = grd; g.lineWidth = Math.max(1, r * .35); g.beginPath(); g.moveTo(px, py); g.lineTo(px + largo, py); g.stroke(); }
      g.drawImage(o.compra ? sc : sv, px - r, py - r, r * 2, r * 2);
    }
    g.globalAlpha = 1; g.globalCompositeOperation = "source-over";
    g.fillStyle = css("--texto"); g.beginPath(); g.arc(W - 6, y(ultimo), 3.5, 0, Math.PI * 2); g.fill();
  }
  function lectura() {
    const ahora = Date.now(), min = ops.filter((o) => ahora - o.t < 60e3);
    const c = min.filter((o) => o.compra).reduce((a, o) => a + o.usd, 0), tot = min.reduce((a, o) => a + o.usd, 0) || 1;
    const pc = Math.round((c / tot) * 100);
    if (ultimo) $("rio-precio").textContent = "US$ " + fmt.format(ultimo);
    if (min.length) $("rio-ritmo").textContent = fmt.format(min.length);
    $("rio-tira").style.width = pc + "%";
    $("rio-compra").textContent = `${T.compras} ${pc} %`; $("rio-venta").textContent = `${T.ventas} ${100 - pc} %`;
    // aguja de la regla: distancia en vivo a la media de 100 días (escala de -30 % a +30 %)
    if (sma && ultimo) { const d = (ultimo / sma - 1) * 100; const ag = $("rr-aguja"); if (ag) ag.style.left = (50 + Math.max(-30, Math.min(30, d)) / 60 * 100) + "%"; }
  }
  const bucle = () => { if (!document.hidden) dibujar(); requestAnimationFrame(bucle); };
  if (quieto) setInterval(dibujar, 1000); else requestAnimationFrame(bucle);
  setInterval(lectura, 1000);

  fetch((document.body.dataset.estado || "estado.json") + "?t=" + Date.now()).then((r) => r.json()).then((e) => { sma = e.sma100; }).catch(() => {});
  (async () => {
    for (const base of ["https://api.binance.com", "https://data-api.binance.vision"]) {
      try {
        const d = await (await fetch(`${base}/api/v3/aggTrades?symbol=BTCUSDT&limit=1000`)).json();
        if (!Array.isArray(d) || !d.length) continue;
        const vivos = ops.splice(0);
        for (const x of d) if (Date.now() - x.T < VENTANA) agregar(+x.p, +x.q, !x.m, x.T, x.a);
        for (const o of vivos) ops.push(o);
        ops.sort((a, b) => a.t - b.t);
        if (vivos.length) ultimo = vivos[vivos.length - 1].p;
        break;
      } catch (e) { /* probar la otra fuente */ }
    }
  })();
  const estado = $("rio-estado");
  function arrancarSimulacion() {
    if (simulado || (conectado && ops.length)) return; simulado = true;
    if (estado) estado.textContent = T.sin;
    let p = ultimo || 80000;
    setInterval(() => { for (let i = 0; i < 4; i++) { p += (Math.random() - .5) * 6; agregar(p, Math.random() ** 3 * 2, Math.random() > .48, Date.now()); } }, 120);
  }
  function conectar() {
    try {
      const ws = new WebSocket("wss://data-stream.binance.vision/ws/btcusdt@aggTrade");
      ws.onopen = () => { conectado = true; if (estado) estado.textContent = T.vivo; };
      ws.onmessage = (e) => { const d = JSON.parse(e.data); agregar(+d.p, +d.q, !d.m, d.T, d.a); };
      ws.onclose = () => { conectado = false; setTimeout(conectar, 5000); };
    } catch (e) { arrancarSimulacion(); }
  }
  conectar();
  setTimeout(() => { if (!conectado && !ops.length) arrancarSimulacion(); }, 8000);
})();
