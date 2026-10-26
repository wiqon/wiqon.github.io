// WIQON · Mis favoritos y alertas de precio (Sprint 3).
// Favoritos y alertas se guardan en Supabase con Row Level Security: cada cuenta ve y cambia solo lo suyo.
// Las alertas NO dependen de esta pestaña: las revisa n8n en la Raspberry cada 2 minutos con precios públicos
// de Binance y avisa una sola vez por email. Esto solo muestra, crea, pausa y borra.
// Precios de la lista: API pública de Binance (mercado al contado), con la hora del dato. Nunca se inventa un valor.
(function () {
  const caja = document.getElementById("favs-cuerpo");
  if (!caja) return;
  const PT = document.documentElement.lang.toLowerCase().startsWith("pt");
  const EN = document.documentElement.lang.toLowerCase().startsWith("en");
  const IDIOMA = PT ? "pt" : EN ? "en" : "es";
  const LOC = PT ? "pt-BR" : EN ? "en-US" : "es-PY";
  const TZ = PT ? "America/Sao_Paulo" : "America/Asuncion";
  const API = "https://data-api.binance.vision/api/v3";
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const L = (es, pt, en) => (PT ? pt : EN ? en : es);
  const MAX_FAV = 30, MAX_AL = 10;

  // mismo catálogo que public.simbolo_valido() en Supabase (pares USDT verificados en Binance)
  const CAT = {
    BTC: "Bitcoin", ETH: "Ethereum", SOL: "Solana", BNB: "BNB", XRP: "XRP", DOGE: "Dogecoin", ADA: "Cardano", AVAX: "Avalanche",
    LINK: "Chainlink", DOT: "Polkadot", TRX: "TRON", TON: "Toncoin", LTC: "Litecoin", BCH: "Bitcoin Cash", SHIB: "Shiba Inu",
    NEAR: "NEAR Protocol", UNI: "Uniswap", ATOM: "Cosmos", SUI: "Sui", PEPE: "Pepe", ARB: "Arbitrum", OP: "Optimism", POL: "Polygon",
    APT: "Aptos", FIL: "Filecoin", XLM: "Stellar", PAXG: L("PAX Gold (oro tokenizado)", "PAX Gold (ouro tokenizado)", "PAX Gold (tokenized gold)"),
  };

  const T = {
    invitaT: L("Tus monedas y tus alertas, en un solo lugar", "Suas moedas e seus alertas, num só lugar", "Your coins and your alerts, in one place"),
    invitaP: L("Con tu cuenta gratis guardás hasta 30 monedas favoritas y creás hasta 10 alertas de precio. Te avisamos por email aunque no tengas la página abierta.",
               "Com sua conta grátis você guarda até 30 moedas favoritas e cria até 10 alertas de preço. Avisamos por e-mail mesmo com a página fechada.",
               "With your free account you can save up to 30 favorite coins and create up to 10 price alerts. We email you even when the page is closed."),
    crear: L("Crear cuenta gratis", "Criar conta grátis", "Create free account"),
    ejemplo: L("Ejemplo: «Avisame cuando BTC baje de US$ 75.000»", "Exemplo: «Me avise quando o BTC cair abaixo de US$ 75.000»", "Example: “Tell me when BTC drops below US$ 75,000”"),
    agregar: L("Agregar moneda", "Adicionar moeda", "Add coin"), elegir: L("Elegí…", "Escolha…", "Choose…"),
    ordenar: L("Ordenar por", "Ordenar por", "Sort by"),
    porCambio: L("Cambio 24 h", "Variação 24 h", "24 h change"), porNombre: L("Nombre", "Nome", "Name"), porRango: L("Rango 24 h", "Faixa 24 h", "24 h range"),
    moneda: L("Moneda", "Moeda", "Coin"), precio: L("Precio", "Preço", "Price"), rango: L("Rango 24 h", "Faixa 24 h", "24 h range"),
    rangoAyuda: L("Distancia entre el máximo y el mínimo de 24 h: mide cuánto se movió.", "Distância entre a máxima e a mínima de 24 h: mede quanto se mexeu.", "Gap between the 24 h high and low: how much it moved."),
    vacio: L("Todavía no tenés favoritos. Tocá la estrella de una moneda en la tabla de arriba o elegí una acá.",
             "Você ainda não tem favoritos. Toque na estrela de uma moeda na tabela acima ou escolha uma aqui.",
             "No favorites yet. Tap the star next to a coin in the table above, or pick one here."),
    ver: L("Ver en el gráfico", "Ver no gráfico", "Show on chart"), quitar: L("Quitar de favoritos", "Remover dos favoritos", "Remove from favorites"),
    poner: L("Agregar a favoritos", "Adicionar aos favoritos", "Add to favorites"), alertar: L("Crear alerta", "Criar alerta", "Create alert"),
    fuente: L("Precios: API pública de Binance (al contado)", "Preços: API pública da Binance (à vista)", "Prices: Binance public API (spot)"),
    dato: L("dato de las", "dado das", "data from"), sinPrecio: L("Precios no disponibles ahora; reintentamos en 30 s.", "Preços indisponíveis agora; tentamos de novo em 30 s.", "Prices unavailable right now; retrying in 30 s."),
    misAlertas: L("Mis alertas", "Meus alertas", "My alerts"),
    avisar: L("Avisame por email cuando", "Me avise por e-mail quando", "Email me when"),
    tipos: {
      sobre: L("suba por encima de", "subir acima de", "rises above"), bajo: L("baje por debajo de", "cair abaixo de", "drops below"),
      sube_pct: L("suba más de (% en 24 h)", "subir mais de (% em 24 h)", "gains more than (% in 24 h)"),
      baja_pct: L("baje más de (% en 24 h)", "cair mais de (% em 24 h)", "loses more than (% in 24 h)"),
    },
    desc: {
      sobre: L("{s} por encima de US$ {v}", "{s} acima de US$ {v}", "{s} above US$ {v}"), bajo: L("{s} por debajo de US$ {v}", "{s} abaixo de US$ {v}", "{s} below US$ {v}"),
      sube_pct: L("{s} sube más de {v} % en 24 h", "{s} sobe mais de {v} % em 24 h", "{s} up more than {v} % in 24 h"),
      baja_pct: L("{s} baja más de {v} % en 24 h", "{s} cai mais de {v} % em 24 h", "{s} down more than {v} % in 24 h"),
    },
    valor: L("Valor", "Valor", "Value"), ahora: L("{s} ahora: US$ {p} · 24 h: {c}", "{s} agora: US$ {p} · 24 h: {c}", "{s} now: US$ {p} · 24 h: {c}"),
    unaVez: L("Te avisamos una sola vez a {e}. Después la alerta queda disparada y la podés reactivar.",
              "Avisamos uma única vez em {e}. Depois o alerta fica disparado e você pode reativá-lo.",
              "We email {e} once. After that the alert stays triggered and you can reactivate it."),
    revisa: L("Revisamos los precios cada 2 minutos: no sirve para movimientos de segundos. Es un aviso informativo, no una recomendación.",
              "Verificamos os preços a cada 2 minutos: não serve para movimentos de segundos. É um aviso informativo, não uma recomendação.",
              "We check prices every 2 minutes, so it won't catch moves that last seconds. It's an informational notice, not a recommendation."),
    sinAlertas: L("No tenés alertas. Creá la primera con el formulario.", "Você não tem alertas. Crie o primeiro com o formulário.", "You have no alerts. Create your first one with the form."),
    est: {
      activa: L("Activa", "Ativo", "Active"), pausada: L("Pausada", "Pausado", "Paused"),
      disparada: L("Disparada", "Disparado", "Triggered"), error: L("Error", "Erro", "Error"),
    },
    creada: L("creada el {f}", "criado em {f}", "created {f}"), disparo: L("se disparó el {f} con US$ {p}", "disparou em {f} com US$ {p}", "triggered {f} at US$ {p}"),
    pausar: L("Pausar", "Pausar", "Pause"), reactivar: L("Reactivar", "Reativar", "Reactivate"), borrar: L("Borrar", "Excluir", "Delete"),
    nueva: L("🔔 Se disparó tu alerta: {d} ({f}).", "🔔 Seu alerta disparou: {d} ({f}).", "🔔 Your alert was triggered: {d} ({f})."),
    errValor: L("Escribí un número mayor que cero.", "Digite um número maior que zero.", "Enter a number greater than zero."),
    errPct: L("El porcentaje tiene que estar entre 0,5 y 100.", "A porcentagem deve estar entre 0,5 e 100.", "The percentage must be between 0.5 and 100."),
    errSobre: L("{s} ya está en US$ {p}: elegí un valor más alto para que tenga sentido avisarte.", "{s} já está em US$ {p}: escolha um valor mais alto.", "{s} is already at US$ {p}: choose a higher value."),
    errBajo: L("{s} ya está en US$ {p}: elegí un valor más bajo para que tenga sentido avisarte.", "{s} já está em US$ {p}: escolha um valor mais baixo.", "{s} is already at US$ {p}: choose a lower value."),
    errYa: L("{s} ya se movió {c} en 24 h: la alerta se dispararía enseguida. Elegí un porcentaje mayor.", "{s} já se moveu {c} em 24 h: o alerta dispararia na hora. Escolha uma porcentagem maior.", "{s} has already moved {c} in 24 h, so it would trigger right away. Choose a larger percentage."),
    limAl: L("Llegaste a 10 alertas activas. Pausá o borrá una para crear otra.", "Você chegou a 10 alertas ativos. Pause ou exclua um para criar outro.", "You've reached 10 active alerts. Pause or delete one to create another."),
    limFav: L("Llegaste a 30 favoritos. Quitá uno para agregar otro.", "Você chegou a 30 favoritos. Remova um para adicionar outro.", "You've reached 30 favorites. Remove one to add another."),
    errGuardar: L("No pudimos guardar el cambio. Revisá tu conexión y probá de nuevo.", "Não foi possível salvar. Verifique sua conexão e tente de novo.", "We couldn't save that. Check your connection and try again."),
    errCargar: L("No pudimos cargar tus favoritos y alertas. Probá recargar la página.", "Não foi possível carregar seus favoritos e alertas. Tente recarregar a página.", "We couldn't load your favorites and alerts. Try reloading the page."),
    creadaOk: L("Alerta creada. Te avisamos por email cuando se cumpla.", "Alerta criado. Avisamos por e-mail quando acontecer.", "Alert created. We'll email you when it happens."),
    errAlerta: L("No pudimos enviar el email de esta alerta. Reactivala para intentar de nuevo.", "Não foi possível enviar o e-mail deste alerta. Reative para tentar de novo.", "We couldn't send this alert's email. Reactivate it to try again."),
    demoT: L("Caso real de esta semana", "Caso real desta semana", "A real case from this week"),
    demoQ: { true: L("«Avisame cuando BTC baje de US$ {v}»", "«Me avise quando o BTC cair abaixo de US$ {v}»", "“Tell me when BTC drops below US$ {v}”"),
             false: L("«Avisame cuando BTC suba por encima de US$ {v}»", "«Me avise quando o BTC subir acima de US$ {v}»", "“Tell me when BTC rises above US$ {v}”") },
    demoR: L("Con esa alerta, el email te llegaba el {f} cerca de las {h}.", "Com esse alerta, o e-mail chegava em {f} por volta das {h}.", "With that alert, the email would have reached you on {f} around {h}."),
    demoAviso: { true: L("BTC bajó de US$ {v}", "BTC caiu abaixo de US$ {v}", "BTC dropped below US$ {v}"), false: L("BTC superó US$ {v}", "BTC passou de US$ {v}", "BTC rose above US$ {v}") },
    demoEmail: L("Email enviado", "E-mail enviado", "Email sent"), demoTu: L("tu alerta", "seu alerta", "your alert"),
    demoFuente: L("Precios reales de BTC/USDT, velas de 1 h de Binance (últimos 7 días).", "Preços reais de BTC/USDT, velas de 1 h da Binance (últimos 7 dias).", "Real BTC/USDT prices, Binance 1 h candles (last 7 days)."),
    puntos: [L("Hasta 30 monedas favoritas con precio y cambio del día", "Até 30 moedas favoritas com preço e variação do dia", "Up to 30 favorite coins with price and daily change"),
             L("Hasta 10 alertas de precio o de % en 24 h", "Até 10 alertas de preço ou de % em 24 h", "Up to 10 price or 24 h % alerts"),
             L("El email llega aunque tengas la página cerrada", "O e-mail chega mesmo com a página fechada", "The email arrives even when the page is closed")],
    confirmar: L("¿Borrar esta alerta?", "Excluir este alerta?", "Delete this alert?"),
  };

  // íconos SVG (heredan el color del texto)
  const IC = {
    estrella: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3.2l2.7 5.5 6 .9-4.35 4.25 1.03 6L12 17l-5.38 2.85 1.03-6L3.3 9.6l6-.9z"/></svg>',
    campana: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 16V11a6 6 0 1 1 12 0v5l1.5 2h-15zM10 20a2 2 0 0 0 4 0"/></svg>',
    grafico: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 19h16M6 15l4-5 3 3 5-7"/></svg>',
    cerrar: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>',
  };

  const fmt = (p) => (p >= 1 ? p.toLocaleString(LOC, { minimumFractionDigits: 2, maximumFractionDigits: 2 })
                             : p.toLocaleString(LOC, { maximumSignificantDigits: 4 }));
  const pct = (c) => `${c >= 0 ? "+" : ""}${c.toLocaleString(LOC, { minimumFractionDigits: 2, maximumFractionDigits: 2 })} %`;
  const cuando = (iso) => new Date(iso).toLocaleString(LOC, { timeZone: TZ, day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit", hour12: false });
  const ocultar = (e) => { const [u, d] = String(e).split("@"); return d ? `${u.slice(0, 2)}•••@${d}` : ""; };
  // «75.000», «75,000», «0,25», «1.234,5» o «1,234.5»: el último separador con 1-2 cifras detrás (o el único que no
  // forma grupos de mil según el idioma) es el decimal
  const numero = (txt) => {
    let t = String(txt).trim().replace(/[\s$US]/g, "");
    const coma = t.lastIndexOf(","), punto = t.lastIndexOf(".");
    if (coma >= 0 && punto >= 0) t = coma > punto ? t.replace(/\./g, "").replace(",", ".") : t.replace(/,/g, "");
    else if (coma >= 0) t = EN && /^\d{1,3}(,\d{3})+$/.test(t) ? t.replace(/,/g, "") : t.replace(/,/g, ".");
    else if (punto >= 0 && !EN && /^\d{1,3}(\.\d{3})+$/.test(t)) t = t.replace(/\./g, "");
    return t && /^\d*\.?\d+$/.test(t) ? Number(t) : NaN;
  };
  const describir = (a) => T.desc[a.tipo].replace("{s}", a.simbolo)
    .replace("{v}", a.tipo.endsWith("pct") ? (+a.valor).toLocaleString(LOC, { maximumFractionDigits: 2 }) : fmt(+a.valor));

  let favs = [], alertas = [], precios = {}, horaDato = null, orden = "cambio", sesion = null, cargado = false, aviso = "";
  const sb = () => window.wiqonCuenta && window.wiqonCuenta.sb;

  // ---------------------------------------------------------------- estrellas en la tabla de arriba
  function estrellas() {
    $$("#mercados-vivo tr[data-s]").forEach((fila) => {
      const s = fila.dataset.s, td = fila.firstElementChild;
      let b = $("button.estrella", td);
      if (!b) {
        b = document.createElement("button");
        b.type = "button"; b.className = "estrella"; b.innerHTML = IC.estrella; b.dataset.s = s;
        td.classList.add("con-estrella"); td.prepend(b);
      }
      const on = favs.includes(s);
      b.setAttribute("aria-pressed", String(on));
      b.setAttribute("aria-label", `${on ? T.quitar : T.poner}: ${CAT[s] || s}`);
      b.title = on ? T.quitar : T.poner;
    });
  }
  document.addEventListener("wiqon:tabla", estrellas);
  document.addEventListener("click", (ev) => {
    const b = ev.target.closest("#mercados-vivo button.estrella"); if (!b) return;
    ev.stopPropagation();   // no cambiar el gráfico al marcar la estrella
    alternarFav(b.dataset.s);
  }, true);

  // ---------------------------------------------------------------- datos
  async function cargar() {
    const [f, a] = await Promise.all([
      sb().from("favoritos").select("simbolo,creado").order("creado"),
      sb().from("alertas").select("id,simbolo,tipo,valor,estado,creada,disparada,precio_disparo,aviso").order("creada", { ascending: false }),
    ]);
    if (f.error || a.error) throw f.error || a.error;
    favs = f.data.map((x) => x.simbolo);
    alertas = a.data;
    cargado = true;
  }

  async function traerPrecios() {
    const lista = [...new Set([...favs, ...alertas.filter((a) => a.estado === "activa").map((a) => a.simbolo), $("#al-sim")?.value].filter((s) => CAT[s]))];
    if (!lista.length) return;
    try {
      const r = await fetch(`${API}/ticker/24hr?symbols=${encodeURIComponent(JSON.stringify(lista.map((s) => s + "USDT")))}`);
      if (!r.ok) throw new Error(r.status);
      (await r.json()).forEach((t) => { precios[t.symbol.replace(/USDT$/, "")] = t; });
      horaDato = Math.max(...Object.values(precios).map((t) => +t.closeTime));
    } catch (e) { horaDato = horaDato || null; }
  }

  async function alternarFav(s) {
    if (!sesion) { window.wiqonCuenta && window.wiqonCuenta.abrir(); return; }
    const estaba = favs.includes(s);
    if (!estaba && favs.length >= MAX_FAV) { avisar(T.limFav, true); return; }
    favs = estaba ? favs.filter((x) => x !== s) : [...favs, s];   // optimista, se revierte si falla
    estrellas(); pintar();
    const { error } = estaba ? await sb().from("favoritos").delete().eq("simbolo", s) : await sb().from("favoritos").insert({ simbolo: s });
    if (error) {
      favs = estaba ? [...favs, s] : favs.filter((x) => x !== s);
      avisar(/limite_favoritos/.test(error.message) ? T.limFav : T.errGuardar, true);
      estrellas(); pintar(); return;
    }
    if (!estaba && !precios[s]) { await traerPrecios(); pintar(); }
  }

  // ---------------------------------------------------------------- pintar
  let borrarAviso = null;
  function avisar(txt, error) {
    aviso = txt ? `<p class="msg ${error ? "error" : "ok"}">${esc(txt)}</p>` : "";
    const m = $("#favs-aviso", caja); if (m) m.innerHTML = aviso;
    clearTimeout(borrarAviso);
    if (txt) borrarAviso = setTimeout(() => avisar(""), 12000);
  }

  // ---------------------------------------------------------------- caso real: una alerta que se habría disparado esta semana
  // Con las velas de 1 h de los últimos 7 días se busca el último número redondo (múltiplo de US$ 1.000) que BTC cruzó
  // y se muestra cuándo habría llegado el email. Todo sale de datos reales; si no hay cruce, no se muestra.
  let velas = null;
  async function cargarDemo() {
    if (velas) return;
    try {
      const r = await fetch(`${API}/klines?symbol=BTCUSDT&interval=1h&limit=168`); if (!r.ok) throw new Error(r.status);
      velas = (await r.json()).map((k) => [+k[0], +k[4]]);
    } catch (e) { velas = []; }
  }
  function demo() {
    const k = velas || [], c = k.map((x) => x[1]), PASO = 1000;
    // el cruce más reciente dentro del tramo central (se lee el antes y el después); si no hay, cualquiera
    const buscar = (desde, hasta) => {
      for (let i = hasta; i > desde; i--) {
        const a = Math.floor(c[i - 1] / PASO), b = Math.floor(c[i] / PASO);
        if (a !== b) { const baja = c[i] < c[i - 1]; return { i, baja, nivel: (baja ? a : b) * PASO }; }
      }
      return null;
    };
    const cruce = buscar(Math.floor(k.length * 0.25), Math.floor(k.length * 0.8)) || buscar(0, k.length - 2);
    if (!cruce) return "";
    const W = 560, H = 210, AR = 16, AB = 22, n = c.length;
    const lo = Math.min(...c, cruce.nivel), hi = Math.max(...c, cruce.nivel);
    const x = (i) => (i / (n - 1)) * W, y = (v) => AR + (1 - (v - lo) / (hi - lo || 1)) * (H - AR - AB);
    const linea = c.map((v, i) => `${x(i).toFixed(1)},${y(v).toFixed(1)}`).join(" ");
    const cx = x(cruce.i), cy = y(cruce.nivel), v = fmt(cruce.nivel).replace(/[.,]00$/, "");
    const t = k[cruce.i][0] + 3600e3;   // cierre de la vela en la que cruzó
    const f = new Date(t).toLocaleDateString(LOC, { timeZone: TZ, day: "2-digit", month: "2-digit" });
    const h = new Date(t).toLocaleTimeString(LOC, { timeZone: TZ, hour: "2-digit", minute: "2-digit", hour12: false });
    const izq = cx > W * 0.55;   // la burbuja va del lado con espacio
    return `<figure class="fi-demo">
      <figcaption><b>${T.demoT}</b> ${T.demoQ[cruce.baja].replace("{v}", v)}</figcaption>
      <div class="fi-graf">
        <svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="none" aria-hidden="true">
          <defs><linearGradient id="fi-g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="var(--cian)" stop-opacity=".28"/><stop offset="1" stop-color="var(--cian)" stop-opacity="0"/></linearGradient></defs>
          <polygon points="0,${H} ${linea} ${W},${H}" fill="url(#fi-g)"/>
          <line x1="0" x2="${W}" y1="${cy.toFixed(1)}" y2="${cy.toFixed(1)}" class="fi-nivel"/>
          <polyline points="${linea}" class="fi-linea"/>
        </svg>
        <span class="fi-etq" style="top:${((cy / H) * 100).toFixed(1)}%">${T.demoTu} · US$ ${v}</span>
        <span class="fi-punto" style="left:${((cx / W) * 100).toFixed(2)}%;top:${((cy / H) * 100).toFixed(2)}%"></span>
        <div class="fi-burbuja ${izq ? "izq" : "der"}" style="${izq ? "right" : "left"}:${(izq ? 100 - (cx / W) * 100 + 3 : (cx / W) * 100 + 3).toFixed(1)}%;${cy < H / 2 ? "bottom" : "top"}:10px">
          ${IC.campana}<div><b>${T.demoAviso[cruce.baja].replace("{v}", v)}</b><small>${T.demoEmail} · ${f} ${h}</small></div>
        </div>
      </div>
      <p>${T.demoR.replace("{f}", f).replace("{h}", h)}</p>
      <p class="meta">${T.demoFuente}</p>
    </figure>`;
  }

  function invitacion() {
    const ok = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.2 4L19 7"/></svg>';
    caja.innerHTML = `<div class="favs-invita">
        <div class="fi-texto"><h4>${T.invitaT}</h4><p>${T.invitaP}</p>
          <ul class="fi-puntos">${T.puntos.map((p) => `<li>${ok}${p}</li>`).join("")}</ul>
          <button type="button" class="btn p" id="favs-crear">${T.crear}</button></div>
        <div id="fi-demo">${demo()}</div></div>`;
    $("#favs-crear", caja).addEventListener("click", () => window.wiqonCuenta && window.wiqonCuenta.abrir());
    if (!velas) cargarDemo().then(() => { const d = $("#fi-demo", caja); if (d && !sesion) d.innerHTML = demo(); });
  }

  function filasFavs() {
    const conDato = favs.map((s) => ({ s, t: precios[s] }));
    const val = (x, k) => (x.t ? k(x.t) : -Infinity);
    if (orden === "nombre") conDato.sort((a, b) => a.s.localeCompare(b.s));
    else if (orden === "rango") conDato.sort((a, b) => val(b, (t) => (t.highPrice - t.lowPrice) / t.lowPrice) - val(a, (t) => (t.highPrice - t.lowPrice) / t.lowPrice));
    else conDato.sort((a, b) => val(b, (t) => +t.priceChangePercent) - val(a, (t) => +t.priceChangePercent));
    return conDato.map(({ s, t }) => {
      const c = t ? +t.priceChangePercent : null, r = t ? ((t.highPrice - t.lowPrice) / t.lowPrice) * 100 : null;
      return `<tr data-s="${s}">
        <th scope="row"><a href="https://www.binance.com/${PT ? "pt-BR" : EN ? "en" : "es"}/trade/${s}_USDT?type=spot" target="_blank" rel="noopener" title="${T.fuente}">${s}<small>${esc(CAT[s])}</small></a></th>
        <td class="r num">${t ? fmt(+t.lastPrice) : "—"}</td>
        <td class="r num ${c == null ? "" : c >= 0 ? "sube" : "baja"}">${c == null ? "—" : pct(c)}</td>
        <td class="r num om">${r == null ? "—" : r.toLocaleString(LOC, { maximumFractionDigits: 1 }) + " %"}</td>
        <td class="acc">
          <button type="button" class="ico" data-acc="ver" aria-label="${T.ver}: ${s}" title="${T.ver}">${IC.grafico}</button>
          <button type="button" class="ico" data-acc="alerta" aria-label="${T.alertar}: ${s}" title="${T.alertar}">${IC.campana}</button>
          <button type="button" class="ico" data-acc="quitar" aria-label="${T.quitar}: ${s}" title="${T.quitar}">${IC.cerrar}</button>
        </td></tr>`;
    }).join("");
  }

  function filasAlertas() {
    if (!alertas.length) return `<li class="vacio">${T.sinAlertas}</li>` + (demo() ? `<li class="demo">${demo()}</li>` : "");
    return alertas.map((a) => {
      const detalle = a.estado === "disparada" && a.disparada
        ? T.disparo.replace("{f}", cuando(a.disparada)).replace("{p}", fmt(+a.precio_disparo))
        : a.estado === "error" ? T.errAlerta : T.creada.replace("{f}", cuando(a.creada));
      const btns = (a.estado === "activa" ? `<button type="button" class="btn-t" data-al="pausada">${T.pausar}</button>`
                                         : `<button type="button" class="btn-t" data-al="activa">${T.reactivar}</button>`)
                 + `<button type="button" class="btn-t" data-al="borrar">${T.borrar}</button>`;
      return `<li data-id="${a.id}" data-estado="${a.estado}"><span class="chip-e">${T.est[a.estado]}</span>
        <div><b>${esc(describir(a))}</b><small>${esc(detalle)}</small></div><div class="al-acc">${btns}</div></li>`;
    }).join("");
  }

  function pistaPrecio() {
    const s = $("#al-sim", caja)?.value, t = precios[s], el = $("#al-pista", caja); if (!el) return;
    el.textContent = t ? T.ahora.replace("{s}", s).replace("{p}", fmt(+t.lastPrice)).replace("{c}", pct(+t.priceChangePercent)) : "";
  }

  function pintar() {
    if (!sesion) { invitacion(); return; }
    if (!cargado) return;
    const foco = document.activeElement && caja.contains(document.activeElement) ? document.activeElement.id : null;
    const enForm = $("#al-form", caja) ? { s: $("#al-sim", caja).value, t: $("#al-tipo", caja).value, v: $("#al-valor", caja).value } : null;
    const opciones = Object.keys(CAT).filter((s) => !favs.includes(s)).map((s) => `<option value="${s}">${s} · ${esc(CAT[s])}</option>`).join("");
    const activas = alertas.filter((a) => a.estado === "activa").length;
    caja.innerHTML = `
      <div id="favs-aviso" role="status" aria-live="polite">${aviso}</div>
      <div class="favs-grid">
        <div class="favs-lista">
          <div class="favs-barra">
            <label>${T.agregar} <select class="sel" id="fav-agregar" ${favs.length >= MAX_FAV ? "disabled" : ""}><option value="">${T.elegir}</option>${opciones}</select></label>
            <label>${T.ordenar} <select class="sel" id="fav-orden">
              <option value="cambio"${orden === "cambio" ? " selected" : ""}>${T.porCambio}</option>
              <option value="nombre"${orden === "nombre" ? " selected" : ""}>${T.porNombre}</option>
              <option value="rango"${orden === "rango" ? " selected" : ""}>${T.porRango}</option></select></label>
          </div>
          ${favs.length ? `<div class="mercados"><table class="favs-tabla">
            <caption class="meta">${T.fuente}${horaDato ? ` · ${T.dato} ${new Date(horaDato).toLocaleTimeString(LOC, { timeZone: TZ, hour12: false })}` : ` · ${T.sinPrecio}`} · ${favs.length}/${MAX_FAV}</caption>
            <thead><tr><th scope="col">${T.moneda}</th><th scope="col" class="r">${T.precio} (US$)</th><th scope="col" class="r">24 h</th>
              <th scope="col" class="r om"><abbr title="${T.rangoAyuda}">${T.rango}</abbr></th><th scope="col"><span class="vh">${T.alertar}</span></th></tr></thead>
            <tbody>${filasFavs()}</tbody></table></div>`
          : `<div class="favs-vacio">${IC.estrella}<p>${T.vacio}</p></div>`}
        </div>
        <div class="favs-alertas">
          <h4>${T.misAlertas} <span class="meta">${activas}/${MAX_AL}</span></h4>
          <form id="al-form" novalidate>
            <p class="al-frase">${T.avisar}</p>
            <div class="al-campos">
              <label class="vh" for="al-sim">${T.moneda}</label>
              <select class="sel" id="al-sim">${Object.keys(CAT).map((s) => `<option value="${s}">${s}</option>`).join("")}</select>
              <label class="vh" for="al-tipo">${T.avisar}</label>
              <select class="sel" id="al-tipo">${Object.entries(T.tipos).map(([k, v]) => `<option value="${k}">${v}</option>`).join("")}</select>
              <label class="vh" for="al-valor">${T.valor}</label>
              <input class="sel" id="al-valor" inputmode="decimal" autocomplete="off" placeholder="${T.valor}" aria-describedby="al-pista">
              <button type="submit" class="btn p" ${activas >= MAX_AL ? "disabled" : ""}>${T.alertar}</button>
            </div>
            <p class="meta" id="al-pista" aria-live="polite"></p>
            <p class="meta">${T.unaVez.replace("{e}", `<b>${esc(ocultar(sesion.user.email || ""))}</b>`)} ${T.revisa}</p>
          </form>
          <ul class="al-lista">${filasAlertas()}</ul>
        </div>
      </div>`;
    if (enForm) { $("#al-sim", caja).value = enForm.s; $("#al-tipo", caja).value = enForm.t; $("#al-valor", caja).value = enForm.v; }
    else if (favs.length) $("#al-sim", caja).value = favs[0];
    pistaPrecio();
    if (foco && document.getElementById(foco)) document.getElementById(foco).focus();
  }

  // ---------------------------------------------------------------- acciones
  caja.addEventListener("change", async (ev) => {
    if (ev.target.id === "fav-agregar" && ev.target.value) alternarFav(ev.target.value);
    if (ev.target.id === "fav-orden") { orden = ev.target.value; pintar(); }
    if (ev.target.id === "al-sim") { if (!precios[ev.target.value]) await traerPrecios(); pistaPrecio(); }
  });

  caja.addEventListener("click", async (ev) => {
    const b = ev.target.closest("button"); if (!b) return;
    const fila = b.closest("tr[data-s]");
    if (fila && b.dataset.acc) {
      const s = fila.dataset.s;
      if (b.dataset.acc === "quitar") alternarFav(s);
      if (b.dataset.acc === "alerta") { $("#al-sim", caja).value = s; pistaPrecio(); $("#al-valor", caja).focus(); }
      if (b.dataset.acc === "ver" && precios[s]) {
        document.dispatchEvent(new CustomEvent("wiqon:cripto", { detail: { s, n: CAT[s], t: { ...precios[s] } } }));
        const tv = document.getElementById("tv"); if (tv && tv.getBoundingClientRect().top < 0) tv.scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" });
      }
      return;
    }
    const li = b.closest("li[data-id]");
    if (li && b.dataset.al) {
      const id = +li.dataset.id;
      if (b.dataset.al === "borrar") {
        if (!confirm(T.confirmar)) return;
        const { error } = await sb().from("alertas").delete().eq("id", id);
        if (error) { avisar(T.errGuardar, true); return; }
        alertas = alertas.filter((a) => a.id !== id);
      } else {
        const { data, error } = await sb().from("alertas").update({ estado: b.dataset.al }).eq("id", id)
          .select("id,simbolo,tipo,valor,estado,creada,disparada,precio_disparo,aviso").single();
        if (error) { avisar(/limite_alertas/.test(error.message) ? T.limAl : T.errGuardar, true); return; }
        alertas = alertas.map((a) => (a.id === id ? data : a));
      }
      avisar(""); pintar();
    }
  });

  caja.addEventListener("submit", async (ev) => {
    if (ev.target.id !== "al-form") return;
    ev.preventDefault();
    const s = $("#al-sim", caja).value, tipo = $("#al-tipo", caja).value, valor = numero($("#al-valor", caja).value);
    const t = precios[s], p = t ? +t.lastPrice : null, c = t ? +t.priceChangePercent : null;
    let err = "";
    if (!(valor > 0)) err = T.errValor;
    else if (tipo.endsWith("pct") && (valor < 0.5 || valor > 100)) err = T.errPct;
    else if (tipo === "sobre" && p != null && valor <= p) err = T.errSobre.replace("{s}", s).replace("{p}", fmt(p));
    else if (tipo === "bajo" && p != null && valor >= p) err = T.errBajo.replace("{s}", s).replace("{p}", fmt(p));
    else if (tipo === "sube_pct" && c != null && c >= valor) err = T.errYa.replace("{s}", s).replace("{c}", pct(c));
    else if (tipo === "baja_pct" && c != null && -c >= valor) err = T.errYa.replace("{s}", s).replace("{c}", pct(c));
    if (err) { avisar(err, true); $("#al-valor", caja).focus(); return; }
    const btn = $("button[type=submit]", ev.target); btn.disabled = true;
    const { data, error } = await sb().from("alertas").insert({ simbolo: s, tipo, valor, idioma: IDIOMA })
      .select("id,simbolo,tipo,valor,estado,creada,disparada,precio_disparo,aviso").single();
    btn.disabled = false;
    if (error) { avisar(/limite_alertas/.test(error.message) ? T.limAl : T.errGuardar, true); return; }
    alertas = [data, ...alertas];
    $("#al-valor", caja).value = "";
    avisar(T.creadaOk, false); pintar();
  });

  // ---------------------------------------------------------------- disparos desde la última visita
  function novedades() {
    let visto = 0;
    try { visto = +localStorage.getItem("wiqon-alertas-visto") || 0; } catch (e) { /* sin almacenamiento */ }
    const nuevas = alertas.filter((a) => a.estado === "disparada" && a.disparada && Date.parse(a.disparada) > visto);
    if (nuevas.length && visto) avisar(nuevas.map((a) => T.nueva.replace("{d}", describir(a)).replace("{f}", cuando(a.disparada))).join(" "), false);
    try { localStorage.setItem("wiqon-alertas-visto", String(Date.now())); } catch (e) { /* sin almacenamiento */ }
  }

  // ---------------------------------------------------------------- ciclo
  let reloj = null;
  async function iniciar(s) {
    sesion = s; clearInterval(reloj); cargado = false; aviso = "";
    if (!sesion || !sb()) { favs = []; alertas = []; estrellas(); invitacion(); return; }
    try { await cargar(); } catch (e) { caja.innerHTML = `<p class="msg error">${T.errCargar}</p>`; return; }
    estrellas(); await Promise.all([traerPrecios(), alertas.length ? null : cargarDemo()]); novedades(); pintar();
    let vuelta = 0;
    reloj = setInterval(async () => {
      if (document.hidden) return;
      vuelta++;
      if (vuelta % 2 === 0) { try { const antes = JSON.stringify(alertas); await cargar(); if (JSON.stringify(alertas) !== antes) novedades(); } catch (e) { /* queda lo último */ } }
      await traerPrecios();
      // no repintar mientras escribe en el formulario
      const f = document.activeElement; if (f && f.id === "al-valor") { pistaPrecio(); return; }
      pintar();
    }, 30000);
  }
  let actual;   // id del usuario con el que se cargó (undefined = todavía nada)
  const alCambiar = (s) => {
    const id = (s && s.user && s.user.id) || null;
    if (id === actual) { if (s) sesion = s; return; }   // renovación del token: mismo usuario
    actual = id; iniciar(s);
  };
  document.addEventListener("wiqon:sesion", (ev) => alCambiar(ev.detail && ev.detail.sesion));
  alCambiar(window.wiqonCuenta ? window.wiqonCuenta.sesion : null);
})();
