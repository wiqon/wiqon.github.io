// WIQON · portada: "río de operaciones" (versión triángulos). Cada operación real de BTC/USDT en Binance es un
// triángulo que recorre los últimos 3 minutos: ▲ compra (cian), ▼ venta (azul); tamaño: monto. Al cargar, una sola
// vez, el polvo disperso se junta en la W del logo y se suelta en el río (modos "polvo" y "w" para comparar).
// Debajo, la regla de la estrategia con su aguja en vivo (distancia a la media de 100 días de estado.json).
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

  // ---------- intro: "mixto" (polvo → W del logo → río), "polvo" (polvo → río) o "w" (W → río)
  const pedido = new URLSearchParams(location.search).get("intro");
  let modo = ["w", "polvo"].includes(pedido) ? pedido : "mixto", t0 = 0;
  const DUR = { polvo: 1300, w: 2300, mixto: 2350 };
  const zona = () => {  // dónde vive el río: mitad derecha en pantallas anchas, franja de arriba en el celular
    const angosto = W < 860;
    return angosto ? { x: 0, y: H * .035, w: W, h: H * .2 } : { x: W * (1 - Math.max(.5, Math.min(.62, 1 - 760 / W))), y: H * .1, w: W * Math.max(.5, Math.min(.62, 1 - 760 / W)), h: H * .72 };
  };
  // W con el diamante del logo: trazos en coordenadas 0..1, se muestrean puntos a lo largo
  const TRAZOS = [[[0, .18], [.25, 1], [.5, .42], [.75, 1], [1, .18]], [[.5, -.12], [.58, .02], [.5, .16], [.42, .02], [.5, -.12]]];
  const puntoW = () => {
    const z = zona(), lado = Math.min(z.w * (W < 860 ? .5 : .62), z.h * .82), ox = z.x + (z.w - lado) / 2, oy = z.y + (z.h - lado * .9) / 2 + lado * .1;
    const tr = Math.random() < .82 ? TRAZOS[0] : TRAZOS[1];
    const i = Math.floor(Math.random() * (tr.length - 1)), f = Math.random(), a = tr[i], b = tr[i + 1];
    const esp = lado * .028;
    return [ox + (a[0] + (b[0] - a[0]) * f) * lado + (Math.random() - .5) * esp, oy + (a[1] + (b[1] - a[1]) * f) * lado * .9 + (Math.random() - .5) * esp];
  };
  const puntoPolvo = () => { const z = zona(), mx = z.w * .12, my = z.h * .18; return [z.x - mx + Math.random() * (z.w + mx * 2), z.y - my + Math.random() * (z.h + my * 2)]; };  // solo alrededor del río: el texto queda limpio
  function iniciarIntro(m) {
    if (quieto) return;
    modo = m || modo; t0 = performance.now();
    for (const o of ops) { o.s = modo === "w" ? puntoW() : puntoPolvo(); o.w = modo === "mixto" ? puntoW() : null; }
    for (const a of ambiente) a.s = puntoPolvo();
  }
  window.rioIntro = iniciarIntro;  // para la página de conceptos (botón "repetir")
  const suave = (x) => 1 - Math.pow(1 - x, 3);
  // progreso de la intro: [aparición 0..1, mezcla hacia el río 0..1, polvo → W 0..1]
  const fase = (ahora) => {
    if (!t0) return null;
    const e = ahora - t0, d = DUR[modo];
    if (e >= d) { t0 = 0; return null; }
    if (modo === "w") return [Math.min(1, e / 600), suave(Math.max(0, (e - 1000) / 1300)), 0];
    if (modo === "mixto") return [Math.min(1, e / 300), suave(Math.max(0, (e - 1300) / 1050)), suave(Math.min(1, e / 1000))];
    return [Math.min(1, e / 350), suave(Math.min(1, e / d)), 0];
  };

  // ---------- polvo de fondo: pocos triángulos tenues que derivan despacio
  const ambiente = Array.from({ length: W < 860 ? 26 : 60 }, () => ({ x: Math.random(), y: Math.random(), r: 1.2 + Math.random() * 2, v: (Math.random() * .6 + .2) / 1e5, compra: Math.random() > .5, a: .06 + Math.random() * .12, s: null }));

  const agregar = (p, q, compra, t, id) => {
    if (id !== undefined) { if (vistos.has(id)) return; vistos.add(id); if (vistos.size > 20000) vistos.clear(); }
    const usd = p * q, lado = compra ? -1 : 1;
    ops.push({ t, p, usd, compra, j: lado * (0.15 + Math.random() * (0.6 + Math.min(1.6, Math.sqrt(usd / 4000)))), s: null }); ultimo = p;
  };
  // triángulo: ▲ apunta arriba (compra), ▼ abajo (venta); centrado en (x, y) con "radio" r
  const tri = (path, x, y, r, arriba) => {
    const k = arriba ? -1 : 1;
    path.moveTo(x, y + k * r); path.lineTo(x + r * .92, y - k * r * .62); path.lineTo(x - r * .92, y - k * r * .62); path.closePath();
  };
  const NIV = 6;  // niveles de transparencia: un trazo por color y nivel (rápido aunque haya miles)
  function dibujar() {
    const ahora = Date.now(), reloj = performance.now(), f = fase(reloj);
    while (ops.length && ahora - ops[0].t > VENTANA) ops.shift();
    g.clearRect(0, 0, W, H);
    const claro = raiz.dataset.tema === "claro", cc = css("--compra"), cv = css("--venta");
    // fondo
    g.lineWidth = 1;
    for (const a of ambiente) {
      a.x -= a.v * 16; if (a.x < -.02) { a.x = 1.02; a.y = Math.random(); }
      let px = a.x * W, py = a.y * H, al = a.a;
      if (f && a.s) { px = a.s[0] + (px - a.s[0]) * f[1]; py = a.s[1] + (py - a.s[1]) * f[1]; al *= f[0]; }
      g.globalAlpha = claro ? al * 1.4 : al; g.strokeStyle = a.compra ? cc : cv;
      const p = new Path2D(); tri(p, px, py, a.r, a.compra); g.stroke(p);
    }
    g.globalAlpha = 1;
    if (ops.length < 2) return;
    let lo = Infinity, hi = -Infinity; for (const o of ops) { if (o.p < lo) lo = o.p; if (o.p > hi) hi = o.p; }
    const pad = Math.max((hi - lo) * .35, ultimo * .00015);
    bajo = bajo ? bajo + (lo - pad - bajo) * .06 : lo - pad; alto = alto ? alto + (hi + pad - alto) * .06 : hi + pad;
    const angosto = W < 860;
    const y = (p) => H * (angosto ? .05 : .16) + (1 - (p - bajo) / (alto - bajo)) * H * (angosto ? .17 : .58);
    const banda = angosto ? Math.max(6, H * .014) : Math.max(10, H * .035), x = (t) => W - ((ahora - t) / VENTANA) * W * (angosto ? 1 : Math.max(.5, Math.min(.62, 1 - 760 / W)));
    // línea de precio promedio por segundo (aparece cuando el río ya está armado)
    const segs = new Map(); for (const o of ops) { const k = Math.floor(o.t / 1000); const s = segs.get(k) || [0, 0]; s[0] += o.p * o.usd; s[1] += o.usd; segs.set(k, s); }
    g.beginPath(); let primero = true;
    for (const [k, [pv, v]] of [...segs].sort((a, b) => a[0] - b[0])) { const px = x(k * 1000 + 500), py = y(pv / v); if (primero) { g.moveTo(px, py); primero = false; } else g.lineTo(px, py); }
    g.strokeStyle = css("--suave"); g.globalAlpha = (claro ? .35 : .28) * (f ? f[1] : 1); g.lineWidth = 1.2; g.stroke(); g.globalAlpha = 1;
    g.globalCompositeOperation = claro ? "multiply" : "lighter";
    const contorno = { true: Array.from({ length: NIV }, () => new Path2D()), false: Array.from({ length: NIV }, () => new Path2D()) };
    const relleno = { true: Array.from({ length: NIV }, () => new Path2D()), false: Array.from({ length: NIV }, () => new Path2D()) };
    for (const o of ops) {
      const r = Math.min(10, 1.6 + Math.sqrt(o.usd / 3500)), edad = (ahora - o.t) / VENTANA;
      let px = x(o.t), py = y(o.p) + o.j * banda, al = Math.max(.1, 1 - edad * .85);
      if (f && o.s) {
        const ox = o.w ? o.s[0] + (o.w[0] - o.s[0]) * f[2] : o.s[0], oy = o.w ? o.s[1] + (o.w[1] - o.s[1]) * f[2] : o.s[1];
        px = ox + (px - ox) * f[1]; py = oy + (py - oy) * f[1]; al *= f[0];
      }
      const n = Math.min(NIV - 1, Math.floor(al * NIV));
      // estela corta detrás de las operaciones grandes (solo cuando el río ya fluye)
      if (!quieto && !f && r > 5) {
        const largo = Math.min(110, r * 9), grd = g.createLinearGradient(px, 0, px + largo, 0);
        grd.addColorStop(0, o.compra ? cc : cv); grd.addColorStop(1, "transparent");
        g.globalAlpha = al * .55; g.strokeStyle = grd; g.lineWidth = 1; g.beginPath(); g.moveTo(px, py); g.lineTo(px + largo, py); g.stroke();
      }
      tri(r < 3.2 ? relleno[o.compra][n] : contorno[o.compra][n], px, py, r, o.compra);
    }
    g.lineWidth = 1.1; g.lineJoin = "miter";
    for (const lado of [true, false]) {
      g.strokeStyle = g.fillStyle = lado ? cc : cv;
      for (let n = 0; n < NIV; n++) { g.globalAlpha = (n + 1) / NIV; g.fill(relleno[lado][n]); g.stroke(contorno[lado][n]); }
    }
    g.globalAlpha = 1; g.globalCompositeOperation = "source-over";
    if (!f) { g.fillStyle = css("--texto"); g.beginPath(); g.arc(W - 6, y(ultimo), 3.5, 0, Math.PI * 2); g.fill(); }
  }
  function lectura() {
    const ahora = Date.now(), min = ops.filter((o) => ahora - o.t < 60e3);
    const c = min.filter((o) => o.compra).reduce((a, o) => a + o.usd, 0), tot = min.reduce((a, o) => a + o.usd, 0) || 1;
    const pc = Math.round((c / tot) * 100);
    if (ultimo) $("rio-precio").textContent = "US$ " + fmt.format(ultimo);
    if (min.length) $("rio-ritmo").textContent = fmt.format(min.length);
    $("rio-tira").style.width = pc + "%";
    $("rio-compra").textContent = `${T.compras} ${pc} %`; $("rio-venta").textContent = `${T.ventas} ${100 - pc} %`;
    if (sma && ultimo) { const d = (ultimo / sma - 1) * 100; const ag = $("rr-aguja"); if (ag) ag.style.left = (50 + Math.max(-30, Math.min(30, d)) / 60 * 100) + "%"; }
  }
  const bucle = () => { if (!document.hidden) dibujar(); requestAnimationFrame(bucle); };
  if (quieto) setInterval(dibujar, 1000); else requestAnimationFrame(bucle);
  setInterval(lectura, 1000);

  // la intro arranca cuando llega el historial (o a los 1,5 s con lo que haya)
  let introLista = false;
  const arrancarIntro = () => { if (introLista) return; introLista = true; iniciarIntro(); };
  setTimeout(arrancarIntro, 1500);

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
    arrancarIntro();
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
