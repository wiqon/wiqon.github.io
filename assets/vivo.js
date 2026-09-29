// Tarjeta "Estrategia en vivo": lee estado.json y lo muestra en el idioma
// de la página (atributo lang del <html>): "es" o "pt-BR".
(function () {
  const pt = document.documentElement.lang.toLowerCase().startsWith("pt");
  const T = pt ? {
    btc: "EM BTC", usdt: "EM USDT", desde: "Desde ",
    sobre: " · o fechamento está acima da média", bajo: " · o fechamento está abaixo da média",
    vela: "Candle ", actualizado: "🕒 Atualizado: ", sin: "⚠️ Sem atualização desde ",
    viejo: ". O dado pode estar desatualizado.", zona: " (horário de Brasília)",
    tz: "America/Sao_Paulo", locale: "pt-BR", error: "Indisponível",
  } : {
    btc: "EN BTC", usdt: "EN USDT", desde: "Desde el ",
    sobre: " · el cierre está sobre la media", bajo: " · el cierre está debajo de la media",
    vela: "Vela ", actualizado: "🕒 Actualizado: ", sin: "⚠️ Sin actualizar desde el ",
    viejo: ". El dato puede estar desactualizado.", zona: " (hora de Paraguay)",
    tz: "America/Asuncion", locale: "es-PY", error: "No disponible",
  };
  const $ = id => document.getElementById(id);
  const usd = n => "$" + Math.round(n).toLocaleString(T.locale);
  const fecha = iso => { const [a, m, d] = iso.split("-"); return `${d}/${m}/${a}`; };
  const ruta = document.body.dataset.estado || "estado.json";

  const anio = $("anio");
  if (anio) anio.textContent = new Date().getFullYear();

  fetch(ruta + "?t=" + Date.now())
    .then(r => r.json())
    .then(e => {
      const btc = e.senal === "EN_BTC";
      $("senal").textContent = btc ? T.btc : T.usdt;
      $("senal").className = "senal " + (btc ? "btc" : "usdt");
      $("desde").textContent = T.desde + fecha(e.desde) + (btc ? T.sobre : T.bajo);
      $("vela").textContent = T.vela + fecha(e.vela);
      $("cierre").textContent = usd(e.cierre);
      $("sma").textContent = usd(e.sma100);
      const dist = e.distancia_pct.toFixed(1);
      $("dist").textContent = (e.distancia_pct > 0 ? "+" : "") + (pt ? dist.replace(".", ",") : dist) + "%";
      $("dist").style.color = btc ? "var(--verde)" : "var(--cian)";

      // Hora de la última actualización, en la zona horaria del público de la página
      const act = new Date(e.actualizado_utc.replace(" ", "T") + ":00Z");
      const txt = act.toLocaleString(T.locale, {
        timeZone: T.tz, day: "2-digit", month: "2-digit", year: "numeric",
        hour: "2-digit", minute: "2-digit", hour12: false,
      });
      const a = $("actualizado");
      if ((Date.now() - act.getTime()) / 36e5 > 30) {
        // Honestidad: si el proceso automático falló, avisarlo en vez de mostrar un dato viejo como actual
        a.textContent = T.sin + txt + T.zona + T.viejo;
        a.classList.add("viejo");
      } else {
        a.textContent = T.actualizado + txt + T.zona;
      }
    })
    .catch(() => { $("senal").textContent = T.error; });
})();
