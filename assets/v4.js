// WIQON v4: gráfico de BTC de la portada, estado de la regla, snapshot de mercado,
// News Radar compacto y videos. Datos: Binance (público) y los JSON generados por scripts/.
// Nunca se inventa un valor ni una hora: si falta un dato se dice.
(function () {
  const PT = document.documentElement.lang.toLowerCase().startsWith("pt");
  const EN = document.documentElement.lang.toLowerCase().startsWith("en");
  const LOC = (PT ? "pt-BR" : EN ? "en-US" : "es-PY");
  const TZ = (PT ? "America/Sao_Paulo" : EN ? "America/Asuncion" : "America/Asuncion");
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
  } : EN ? {
    hace: "", min: "min ago", h: "h ago", d: "d ago", ahora: "just now", act: "Updated", ult: "Last update", fuentes: "active sources",
    viejo: "The data may be out of date.", caidas: "source(s) not responding; showing their latest known news:",
    vacio: "No news with these filters in this period.", error: "We couldn't load this right now. Try reloading the page.",
    mas: "more source(s)", sinDatos: "Data not available right now", ultConocido: "last known value", enBtc: "IN BTC", enUsdt: "IN USDT",
    completo: "See full radar", menos: "See less", masN: "See more news", play: "Play",
    cats: { regulacion: "Regulation", impuestos: "Taxes", criptoactivos: "Crypto assets", stablecoins: "Stablecoins", pagos: "Payments", fintech: "Fintech",
            finanzas: "Finance", mercados: "Markets", macroeconomia: "Macroeconomics", empresas: "Companies", seguridad: "Security" },
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
    if (m < 60) return T.hace ? `${T.hace} ${m} ${T.min}` : `${m} ${T.min}`;
    if (m < 1440) return T.hace ? `${T.hace} ${Math.round(m / 60)} ${T.h}` : `${Math.round(m / 60)} ${T.h}`;
    return T.hace ? `${T.hace} ${Math.round(m / 1440)} ${T.d}` : `${Math.round(m / 1440)} ${T.d}`;
  }

  // ================= portada: BTC en vivo (velas de 1 min) o diario con media 100 =================
  const lienzo = $("#lienzo");
  let diarias = null, smaDia = null, minutos = null, rango = "vivo", wsVivo = null;
  function pintarVelas(v, m) {
    if (!v || !lienzo) return;
    const dpr = window.devicePixelRatio || 1, W = lienzo.clientWidth, H = lienzo.clientHeight;
    lienzo.width = W * dpr; lienzo.height = H * dpr;
    const g = lienzo.getContext("2d"); g.setTransform(dpr, 0, 0, dpr, 0, 0); g.clearRect(0, 0, W, H);
    const vals = v.flatMap((x) => [x.l, x.h]).concat((m || []).filter(Boolean));
    const lo = Math.min(...vals), hi = Math.max(...vals), pad = (hi - lo) * 0.08 || 1;
    const min = lo - pad, max = hi + pad, ejeX = W - 50;
    const py = (p) => 6 + (1 - (p - min) / (max - min)) * (H - 14);
    const paso = ejeX / v.length, cuerpo = Math.max(1, paso * 0.62);
    const css = getComputedStyle(document.documentElement);
    g.font = "10px JetBrains Mono, monospace"; g.fillStyle = css.getPropertyValue("--eje").trim(); g.strokeStyle = css.getPropertyValue("--grilla").trim(); g.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
      const p = min + ((max - min) * i) / 4, y = py(p);
      g.beginPath(); g.moveTo(0, y); g.lineTo(ejeX, y); g.stroke();
      g.fillText(p >= 10000 ? (p / 1000).toFixed(1) + "K" : p.toFixed(0), ejeX + 6, y + 3);
    }
    v.forEach((c, i) => {
      const x = i * paso + paso / 2, col = c.c >= c.o ? "#2fc47f" : "#ef5f67";
      g.strokeStyle = col; g.fillStyle = col;
      g.beginPath(); g.moveTo(x, py(c.h)); g.lineTo(x, py(c.l)); g.stroke();
      const y1 = py(Math.max(c.o, c.c)), y2 = py(Math.min(c.o, c.c));
      g.fillRect(x - cuerpo / 2, y1, cuerpo, Math.max(1, y2 - y1));
    });
    if (m) {
      g.strokeStyle = "#e7b54a"; g.lineWidth = 1.8; g.beginPath(); let ini = false;
      m.forEach((val, i) => { if (!val) return; const x = i * paso + paso / 2; ini ? g.lineTo(x, py(val)) : g.moveTo(x, py(val)); ini = true; });
      g.stroke();
    }
    // último precio: línea punteada y etiqueta
    const u = v[v.length - 1], yu = py(u.c);
    g.setLineDash([3, 3]); g.strokeStyle = css.getPropertyValue("--gris").trim(); g.beginPath(); g.moveTo(0, yu); g.lineTo(ejeX, yu); g.stroke(); g.setLineDash([]);
    g.fillStyle = u.c >= u.o ? "#2fc47f" : "#ef5f67"; g.fillRect(ejeX + 1, yu - 8, 49, 16);
    g.fillStyle = "#04121c"; g.fillText(u.c >= 10000 ? (u.c / 1000).toFixed(2) + "K" : u.c.toFixed(0), ejeX + 4, yu + 3);
  }
  function dibujar() {
    const vivo = rango === "vivo";
    const vb = $("#vivo-b"); if (vb) vb.hidden = !vivo;
    const lv = $("#ley-velas"); if (lv) lv.textContent = vivo ? lv.dataset.vivo : lv.dataset.dia;
    const lm = $("#ley-media"); if (lm) lm.hidden = vivo;
    if (vivo) pintarVelas(minutos, null);
    else if (diarias) pintarVelas(diarias.slice(-rango), smaDia.slice(-rango));
  }
  const vela = (x) => ({ t: +x[0], o: +x[1], h: +x[2], l: +x[3], c: +x[4] });
  function conectarVivo() {
    if (wsVivo || !("WebSocket" in window)) return;
    try {
      wsVivo = new WebSocket("wss://data-stream.binance.vision/ws/btcusdt@kline_1m");
      let pendiente = false;
      wsVivo.onmessage = (ev) => {
        const k = JSON.parse(ev.data).k, n = { t: k.t, o: +k.o, h: +k.h, l: +k.l, c: +k.c };
        if (!minutos) return;
        const ult = minutos[minutos.length - 1];
        if (ult.t === n.t) minutos[minutos.length - 1] = n; else { minutos.push(n); if (minutos.length > 120) minutos.shift(); }
        const p = $("#precio-num"); if (p) p.textContent = `US$ ${num(n.c, 0)}`;
        if (!pendiente && rango === "vivo") { pendiente = true; requestAnimationFrame(() => { dibujar(); pendiente = false; }); }
      };
      wsVivo.onclose = () => { wsVivo = null; setTimeout(conectarVivo, 5000); };
    } catch (e) { wsVivo = null; }
  }
  if (lienzo) {
    fetch(`${API}/klines?symbol=BTCUSDT&interval=1m&limit=120`).then((r) => r.json()).then((k) => { minutos = k.map(vela); dibujar(); conectarVivo(); })
      .catch(() => { lienzo.replaceWith(Object.assign(document.createElement("p"), { className: "meta", textContent: T.sinDatos })); });
    fetch(`${API}/klines?symbol=BTCUSDT&interval=1d&limit=500`).then((r) => r.json()).then((k) => {
      diarias = k.slice(0, -1).map(vela); // la última vela diaria sigue abierta: la regla solo usa velas cerradas
      const cs = diarias.map((x) => x.c);
      smaDia = cs.map((_, i) => (i < 99 ? null : cs.slice(i - 99, i + 1).reduce((a, b) => a + b, 0) / 100));
      dibujar();
    }).catch(() => {});
    $$(".rangos button").forEach((b) => b.addEventListener("click", () => {
      rango = b.dataset.r === "vivo" ? "vivo" : +b.dataset.r;
      $$(".rangos button").forEach((x) => x.setAttribute("aria-pressed", String(x === b))); dibujar();
    }));
    let t; window.addEventListener("resize", () => { clearTimeout(t); t = setTimeout(dibujar, 200); });
    document.addEventListener("wiqon:tema", dibujar);
  }
  fetch(`${API}/ticker/24hr?symbol=BTCUSDT`).then((r) => r.json()).then((t) => {
    const c = +t.priceChangePercent, txt = `US$ ${num(+t.lastPrice, 0)}`;
    const p = $("#precio-btc");
    if (p) p.innerHTML = `<span id="precio-num">${txt}</span><small class="${c >= 0 ? "sube" : "baja"}">${c >= 0 ? "▲ +" : "▼ "}${num(c, 2)}% (24 h)</small>`;
    const s = $("#snap-btc"); if (s) { s.textContent = txt; $("#snap-btc-f").innerHTML = `Binance · ${hora(new Date().toISOString())} · <span class="${c >= 0 ? "sube" : "baja"}">${c >= 0 ? "+" : ""}${num(c, 2)}% 24 h</span>`; }
  }).catch(() => { const s = $("#snap-btc"); if (s) s.textContent = "—"; });

  // ================= mercado en vivo: tabla de precios en tiempo real =================
  const TF = PT ? { ver: "ver no gráfico", mercado: "Binance · mercado à vista", ultimo: "Último preço", max: "Máxima 24 h", min: "Mínima 24 h", vol: "Volume 24 h",
                    milM: "bi", fuente: "Fonte: API pública da", horario: "opera 24 h, 7 dias", datos: "dado de", ayuda: "Toque numa moeda para vê-la no gráfico." }
           : EN ? { ver: "show on chart", mercado: "Binance · spot market", ultimo: "Last price", max: "24 h high", min: "24 h low", vol: "24 h volume",
                    milM: "bn", fuente: "Source: public API from", horario: "trades 24/7", datos: "data from", ayuda: "Tap a coin to show it on the chart." }
           : { ver: "ver en el gráfico", mercado: "Binance · mercado al contado", ultimo: "Último precio", max: "Máximo 24 h", min: "Mínimo 24 h", vol: "Volumen 24 h",
               milM: "mil M", fuente: "Fuente: API pública de", horario: "opera 24 h, los 7 días", datos: "dato de las", ayuda: "Tocá una moneda para verla en el gráfico." };
  const tbVivo = $("#mercados-vivo");
  if (tbVivo) {
    const ACT = [["BTC", "Bitcoin", "#f7931a"], ["ETH", "Ethereum", "#8c9eff"], ["SOL", "Solana", "#14f195"], ["BNB", "BNB", "#f3ba2f"], ["XRP", "XRP", "#c2ccd8"], ["DOGE", "Dogecoin", "#c2a633"]];
    const dec = (p) => (p >= 1000 ? 2 : p >= 1 ? 2 : 4);
    const spark = (cs) => {
      const lo = Math.min(...cs), hi = Math.max(...cs), W = 90, H = 28;
      const pts = cs.map((c, i) => `${((i / (cs.length - 1)) * W).toFixed(1)},${(H - 2 - ((c - lo) / (hi - lo || 1)) * (H - 4)).toFixed(1)}`).join(" ");
      const col = cs[cs.length - 1] >= cs[0] ? "#2fc47f" : "#ef5f67";
      return `<svg class="spark" viewBox="0 0 ${W} ${H}" preserveAspectRatio="none" aria-hidden="true"><polyline points="${pts}" fill="none" stroke="${col}" stroke-width="1.6"/></svg>`;
    };
    const simbolos = encodeURIComponent(JSON.stringify(ACT.map((a) => a[0] + "USDT")));
    fetch(`${API}/ticker/24hr?symbols=${simbolos}`).then((r) => r.json()).then((lista) => {
      const datos = Object.fromEntries(lista.map((t) => [t.symbol.replace("USDT", ""), t]));
      tbVivo.innerHTML = ACT.map(([s, n, col]) => {
        const t = datos[s]; if (!t) return "";
        const c = +t.priceChangePercent;
        return `<tr data-s="${s}"${s === "BTC" ? ' class="sel"' : ""}><td><button type="button" class="sim" aria-pressed="${s === "BTC"}" aria-label="${n} (${s}/USDT): ${TF.ver}"><i style="background:${col}">${s.slice(0, 1)}</i><span>${s}<small>${n}</small></span></button></td>
          <td class="p" id="mv-${s}">${num(+t.lastPrice, dec(+t.lastPrice))}</td>
          <td class="ch ${c >= 0 ? "sube" : "baja"}" id="mvc-${s}">${c >= 0 ? "+" : ""}${num(c, 2)}%</td><td class="om" id="mvs-${s}"></td></tr>`;
      }).join("");
      document.dispatchEvent(new CustomEvent("wiqon:tabla"));   // favoritos.js agrega la estrella a cada fila
      // ficha del instrumento elegido: todo sale del ticker de 24 h y del WebSocket de Binance
      let elegido = "BTC";
      const NOM = {};   // nombres de monedas favoritas que no están en la tabla
      const ficha = $("#mv-ficha");
      const pintarFicha = () => {
        if (!elegido) return;
        const t = datos[elegido], n = (ACT.find((a) => a[0] === elegido) || [])[1] || NOM[elegido]; if (!ficha || !t) return;
        const p = +($("#mv-" + elegido)?.dataset.v || t.lastPrice);
        const vol = +t.quoteVolume >= 1e9 ? `${num(+t.quoteVolume / 1e9, 2)} ${TF.milM}` : `${num(+t.quoteVolume / 1e6, 1)} M`;
        ficha.innerHTML = `<div class="mf-cab"><b>${esc(n)} · ${elegido}/USDT</b><span>${TF.mercado}</span></div>
          <dl><div><dt>${TF.ultimo}</dt><dd>US$ ${num(p, dec(p))}</dd></div><div><dt>${TF.max}</dt><dd>${num(+t.highPrice, dec(+t.highPrice))}</dd></div>
          <div><dt>${TF.min}</dt><dd>${num(+t.lowPrice, dec(+t.lowPrice))}</dd></div><div><dt>${TF.vol}</dt><dd>US$ ${vol}</dd></div></dl>
          <p class="meta">${TF.fuente} <a href="https://www.binance.com/es/trade/${elegido}_USDT?type=spot" target="_blank" rel="noopener">Binance</a> · ${TF.horario} · ${TF.datos} ${new Date(+t.closeTime).toLocaleTimeString(LOC, { timeZone: TZ, hour12: false })}. ${TF.ayuda}</p>`;
      };
      pintarFicha();
      tbVivo.addEventListener("click", (ev) => {
        const fila = ev.target.closest("tr[data-s]"); if (!fila) return;
        elegido = fila.dataset.s;
        $$("tr[data-s]", tbVivo).forEach((f) => { const on = f === fila; f.classList.toggle("sel", on); $("button.sim", f).setAttribute("aria-pressed", String(on)); });
        const ts = $("#tv-sim"); if (ts) ts.textContent = `${elegido}/USDT`;
        document.dispatchEvent(new CustomEvent("wiqon:simbolo", { detail: { simbolo: `BINANCE:${elegido}USDT`, intervalo: "60" } }));
        pintarFicha();
      });
      // una moneda de «Mis favoritos» que no está en la tabla: misma ficha, con el ticker que trae favoritos.js
      document.addEventListener("wiqon:cripto", (ev) => {
        const { s, n, t } = ev.detail || {}; if (!s || !t) return;
        const fila = $(`tr[data-s="${s}"]`, tbVivo); if (fila) { fila.click(); return; }
        datos[s] = t; NOM[s] = n; elegido = s;
        $$("tr[data-s]", tbVivo).forEach((f) => { f.classList.remove("sel"); $("button.sim", f).setAttribute("aria-pressed", "false"); });
        const ts = $("#tv-sim"); if (ts) ts.textContent = `${s}/USDT`;
        const ti = $("#tv-inst"); if (ti) ti.value = "";
        document.dispatchEvent(new CustomEvent("wiqon:simbolo", { detail: { simbolo: `BINANCE:${s}USDT`, intervalo: "60" } }));
        pintarFicha();
      });
      // ---- selector de instrumento y comparación (Sprint 2): el gráfico de TradingView muestra el precio;
      // para lo que no es cripto la ficha dice qué es y de dónde sale, sin inventar cifras
      const L = (es, pt, en) => (PT ? pt : EN ? en : es);
      const CAB = { idx: L("Índices", "Índices", "Indices"), fx: L("Divisas", "Moedas", "Currencies"), mp: L("Materias primas", "Commodities", "Commodities"), cr: "Cripto" };
      const H24 = L("casi 24 h, de lunes a viernes", "quase 24 h, de segunda a sexta", "nearly 24 h, Monday to Friday");
      const HAB = L("días hábiles", "dias úteis", "business days");
      const PTS = L("puntos", "pontos", "points");
      const INST = {
        SPX: { g: "idx", sym: "FOREXCOM:SPXUSD", n: "S&P 500", hor: H24, mon: "USD",
               tipo: L("CFD que sigue al índice S&P 500 (FOREX.com)", "CFD que acompanha o índice S&P 500 (FOREX.com)", "CFD tracking the S&P 500 index (FOREX.com)") },
        NDX: { g: "idx", sym: "FOREXCOM:NSXUSD", n: "Nasdaq 100", hor: H24, mon: "USD",
               tipo: L("CFD que sigue al índice Nasdaq 100 (FOREX.com)", "CFD que acompanha o índice Nasdaq 100 (FOREX.com)", "CFD tracking the Nasdaq 100 index (FOREX.com)") },
        IBOV: { g: "idx", sym: "BMFBOVESPA:IBOV", n: "Ibovespa", mon: PTS,
                hor: L("10:00 a 17:00 de Brasilia, días hábiles", "10h às 17h de Brasília, dias úteis", "10:00–17:00 Brasília time, business days"),
                tipo: L("Índice principal de la bolsa de Brasil (B3)", "Principal índice da bolsa brasileira (B3)", "Brazil's main stock index (B3)") },
        USDPYG: { g: "fx", sym: "FX_IDC:USDPYG", n: "USD/PYG", hor: HAB, mon: "PYG",
                  tipo: L("Cotización interbancaria agregada (referencial). El oficial lo publica el BCP.", "Cotação interbancária agregada (referencial). A oficial é do BCP.", "Aggregated interbank quote (reference). The official rate is published by the BCP.") },
        USDBRL: { g: "fx", sym: "FX_IDC:USDBRL", n: "USD/BRL", hor: HAB, mon: "BRL",
                  tipo: L("Cotización interbancaria agregada (referencial). La oficial (PTAX) la publica el BCB.", "Cotação interbancária agregada (referencial). A oficial (PTAX) é do BCB.", "Aggregated interbank quote (reference). The official PTAX rate is published by the BCB.") },
        EURUSD: { g: "fx", sym: "FX:EURUSD", n: "EUR/USD", mon: "USD", hor: L("24 h, de lunes a viernes", "24 h, de segunda a sexta", "24 h, Monday to Friday"),
                  tipo: L("Par de divisas más negociado del mundo", "Par de moedas mais negociado do mundo", "The world's most traded currency pair") },
        DXY: { g: "fx", sym: "CAPITALCOM:DXY", n: L("Índice dólar (DXY)", "Índice dólar (DXY)", "Dollar index (DXY)"), hor: H24, mon: PTS,
               tipo: L("Valor del dólar frente a 6 monedas (CFD de Capital.com)", "Valor do dólar contra 6 moedas (CFD da Capital.com)", "Dollar value against 6 currencies (Capital.com CFD)") },
        ORO: { g: "mp", sym: "OANDA:XAUUSD", n: L("Oro", "Ouro", "Gold"), hor: H24, mon: L("USD por onza", "USD por onça", "USD per ounce"),
               tipo: L("Oro contra dólar, precio al contado (OANDA)", "Ouro contra dólar, preço à vista (OANDA)", "Gold vs. dollar, spot price (OANDA)") },
        WTI: { g: "mp", sym: "TVC:USOIL", n: L("Petróleo WTI", "Petróleo WTI", "WTI crude oil"), hor: H24, mon: L("USD por barril", "USD por barril", "USD per barrel"),
               tipo: L("Referencia del petróleo de EE. UU. (índice de TradingView)", "Referência do petróleo dos EUA (índice da TradingView)", "US crude oil benchmark (TradingView index)") },
      };
      const ctl = $("#tv-ctl");
      let comparar = "";
      if (ctl) {
        const opcion = (v, t, sel) => `<option value="${v}"${sel ? " selected" : ""}>${esc(t)}</option>`;
        const grupos = (sel, conNinguno) => (conNinguno ? opcion("", L("Nada", "Nada", "Nothing"), true) : "") +
          `<optgroup label="${CAB.cr}">${ACT.map(([sy, n]) => opcion("c:" + sy, `${n} (${sy})`, !conNinguno && sy === sel)).join("")}</optgroup>` +
          ["idx", "fx", "mp"].map((g) => `<optgroup label="${CAB[g]}">${Object.entries(INST).filter(([, i]) => i.g === g).map(([k, i]) => opcion("i:" + k, i.n, false)).join("")}</optgroup>`).join("");
        ctl.innerHTML = `<label>${L("Instrumento", "Instrumento", "Instrument")} <select class="sel" id="tv-inst">${grupos("BTC", false)}</select></label>
          <label>${L("Comparar con", "Comparar com", "Compare with")} <select class="sel" id="tv-comp">${grupos("", true)}</select></label>`;
        const simDe = (v) => (v.startsWith("c:") ? `BINANCE:${v.slice(2)}USDT` : v.startsWith("i:") ? INST[v.slice(2)].sym : "");
        $("#tv-inst").addEventListener("change", (ev) => {
          const v = ev.target.value;
          if (v.startsWith("c:")) { const f = $(`tr[data-s="${v.slice(2)}"]`, tbVivo); if (f) f.click(); return; }
          const i = INST[v.slice(2)];
          elegido = null;
          $$("tr[data-s]", tbVivo).forEach((f) => { f.classList.remove("sel"); $("button.sim", f).setAttribute("aria-pressed", "false"); });
          const ts = $("#tv-sim"); if (ts) ts.textContent = i.n;
          document.dispatchEvent(new CustomEvent("wiqon:simbolo", { detail: { simbolo: i.sym, intervalo: "D", comparar } }));
          if (ficha) ficha.innerHTML = `<div class="mf-cab"><b>${esc(i.n)}</b><span>${esc(CAB[i.g])}</span></div>
            <dl class="mf-meta"><div><dt>${L("Qué es", "O que é", "What it is")}</dt><dd>${esc(i.tipo)}</dd></div><div><dt>${L("Horario", "Horário", "Hours")}</dt><dd>${esc(i.hor)}</dd></div>
            <div><dt>${L("Unidad", "Unidade", "Unit")}</dt><dd>${esc(i.mon)}</dd></div></dl>
            <p class="meta">${L("El precio está en el gráfico de TradingView (fuente: ", "O preço está no gráfico da TradingView (fonte: ", "The price is on the TradingView chart (source: ")}${esc(i.sym.split(":")[0])}${L("); puede tener demora según el mercado. No lo copiamos ni lo guardamos.", "); pode ter atraso conforme o mercado. Não copiamos nem guardamos o dado.", "); it may be delayed depending on the market. We don't copy or store it.")}</p>`;
        });
        $("#tv-comp").addEventListener("change", (ev) => {
          comparar = simDe(ev.target.value);
          document.dispatchEvent(new CustomEvent("wiqon:simbolo", { detail: { comparar } }));
        });
        // al tocar una fila de la tabla, el selector acompaña
        tbVivo.addEventListener("click", (ev) => { const f = ev.target.closest("tr[data-s]"); if (f) $("#tv-inst").value = "c:" + f.dataset.s; });
      }
      ACT.forEach(([s]) => fetch(`${API}/klines?symbol=${s}USDT&interval=1h&limit=24`).then((r) => r.json())
        .then((k) => { const el = $("#mvs-" + s); if (el) el.innerHTML = spark(k.map((x) => +x[4])); }).catch(() => {}));
      try {
        const ws = new WebSocket(`wss://data-stream.binance.vision/stream?streams=${ACT.map((a) => a[0].toLowerCase() + "usdt@miniTicker").join("/")}`);
        ws.onmessage = (ev) => {
          const d = JSON.parse(ev.data).data, s = d.s.replace("USDT", ""), p = +d.c, c = ((p - +d.o) / +d.o) * 100;
          const me = $("#mv-estado"); if (me) me.dataset.ultimo = Date.now();
          const el = $("#mv-" + s), ec = $("#mvc-" + s); if (!el) return;
          const ant = parseFloat(el.dataset.v || p);
          el.dataset.v = p; el.textContent = num(p, dec(p));
          if (p !== ant) { el.classList.remove("sube-f", "baja-f"); void el.offsetWidth; el.classList.add(p > ant ? "sube-f" : "baja-f"); setTimeout(() => el.classList.remove("sube-f", "baja-f"), 700); }
          ec.textContent = `${c >= 0 ? "+" : ""}${num(c, 2)}%`; ec.className = "ch " + (c >= 0 ? "sube" : "baja");
          if (datos[s]) { datos[s].lastPrice = p; datos[s].highPrice = +d.h; datos[s].lowPrice = +d.l; datos[s].quoteVolume = +d.q; datos[s].closeTime = d.E; }
          if (s === elegido) pintarFicha();
        };
      } catch (e) { /* sin WebSocket: queda el último dato */ }
    }).catch(() => { tbVivo.innerHTML = `<tr><td colspan="4" class="meta">${T.sinDatos}</td></tr>`; });
  }

  // ================= estado de la regla (estado.json) =================
  json("estado.json").then((e) => {
    const dentro = e.senal === "EN_BTC";
    $$(".est-regla").forEach((el) => { el.textContent = (dentro ? "● " + T.enBtc : "● " + T.enUsdt); el.className = "est est-regla " + (dentro ? "btc" : "usdt"); });
    const set = (id, v) => { const el = $(id); if (el) el.innerHTML = v; };
    set("#h-cierre", `US$ ${num(e.cierre, 0)}`);
    set("#h-dist", `<span class="${e.distancia_pct >= 0 ? "sube" : "baja"}">${e.distancia_pct >= 0 ? "+" : ""}${num(e.distancia_pct, 1)}%</span>`);
    set("#h-desde", fecha(e.desde));
    set("#h-act", `${T.act} ${hora(e.actualizado_utc.replace(" ", "T") + ":00Z")} · ${(PT ? "candle de" : EN ? "candle of" : "vela del")} ${fecha(e.vela)}`);
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
        const nombreEN = { "Dólar estadounidense": "US dollar", "Real brasileño": "Brazilian real", "Dólar (venta)": "Dollar (sell)", "Peso argentino": "Argentine peso", "Peso colombiano": "Colombian peso", "Euro": "Euro", "Guaraní": "Guarani" };
        const nombre = PT ? nombrePT[v.nombre] || v.nombre : EN ? nombreEN[v.nombre] || v.nombre : v.nombre;
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
    const mini = (n) => `<a class="mini" href="${esc(n.url)}" target="_blank" rel="noopener" tabindex="-1" aria-hidden="true">${n.imagen
        ? `<img src="${esc(n.imagen)}" alt="" loading="lazy" decoding="async" referrerpolicy="no-referrer">` : ""}<span class="mini-f">${esc(n.fuente)}</span></a>`;
    const item = (n) => `<li class="nota-n${n.imagen ? "" : " sin-img"}">${mini(n)}<div class="lm"><span class="pais">${esc(n.pais_nombre)}</span><span class="cat">${esc(T.cats[n.categorias[0]] || n.categorias[0])}</span>
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
      // si el medio no deja cargar la foto, queda el recuadro con el nombre de la fuente
      $$(".mini img", lista).forEach((im) => im.addEventListener("error", () => { im.closest(".nota-n").classList.add("sin-img"); im.remove(); }, { once: true }));
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


  // ================= estado de cada dato (salud.json) y «EN VIVO» real =================
  // La etiqueta se calcula con la hora del último dato bueno y el plazo de cada fuente; la página
  // vuelve a calcular la edad con la hora del visitante por si salud.json quedó viejo.
  const TS = PT ? { al_dia: "Em dia", atrasado: "Atrasado", caido: "Sem dados novos", error: "Fonte com erro", fuente: "Fonte",
                    ult: "último dado", conectando: "CONECTANDO", vivo: "AO VIVO", sin: "SEM CONEXÃO", ultimo: "último preço" }
           : EN ? { al_dia: "Up to date", atrasado: "Delayed", caido: "No new data", error: "Source error", fuente: "Source",
                    ult: "last data", conectando: "CONNECTING", vivo: "LIVE", sin: "DISCONNECTED", ultimo: "last price" }
           : { al_dia: "Al día", atrasado: "Atrasado", caido: "Sin datos nuevos", error: "Fuente con error", fuente: "Fuente",
               ult: "último dato", conectando: "CONECTANDO", vivo: "EN VIVO", sin: "SIN CONEXIÓN", ultimo: "último precio" };
  const ORD = { al_dia: 0, atrasado: 1, caido: 2, error: 3 };
  const marcas = $$("[data-salud]");
  if (marcas.length) json("salud.json").then((s) => {
    marcas.forEach((el) => {
      const m = s.modulos[el.dataset.salud]; if (!m) return;
      let estado = m.estado;
      if (m.actualizado_utc && estado !== "error") {
        const edad = (Date.now() - new Date(m.actualizado_utc).getTime()) / 60000;
        const local = edad > m.caido_min ? "caido" : edad > m.plazo_min ? "atrasado" : "al_dia";
        if (ORD[local] > ORD[estado]) estado = local;
      }
      const cuando = m.actualizado_utc ? ` · ${T.act.toLowerCase()} ${hace(m.actualizado_utc)}` : "";
      el.className = "est est-" + estado;
      el.innerHTML = `<b>${TS[estado]}</b>${cuando} · ${TS.fuente}: <a href="${esc(m.fuente_url)}" target="_blank" rel="noopener">${esc(m.fuente)}</a>`;
      if (m.avisos && m.avisos.length && estado !== "al_dia") el.title = m.avisos.join(" · ");
      if (m.actualizado_utc) el.setAttribute("data-hora", hora(m.actualizado_utc));
    });
  }).catch(() => {});   // sin salud.json la etiqueta no aparece (cada panel ya muestra su propia hora)

  // tabla de mercados: «EN VIVO» solo si llegó un precio en los últimos 20 segundos
  const mvEst = $("#mv-estado");
  if (mvEst) {
    const pintarEst = () => {
      const ult = +(mvEst.dataset.ultimo || 0), edad = Date.now() - ult;
      const estado = !ult ? "conectando" : edad < 20000 ? "vivo" : "sin";
      mvEst.dataset.estado = estado;
      mvEst.textContent = estado === "sin" ? `${TS.sin} · ${TS.ultimo} ${new Date(ult).toLocaleTimeString(LOC, { timeZone: TZ, hour12: false })}` : TS[estado];
    };
    pintarEst(); setInterval(pintarEst, 5000);
  }

  // ================= aparición suave, una vez =================
  const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("on"); io.unobserve(e.target); } }), { threshold: 0.06 });
  $$(".ap").forEach((el) => io.observe(el));
  const anio = $("#anio"); if (anio) anio.textContent = new Date().getFullYear();
})();
