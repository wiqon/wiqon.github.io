// WIQON · panel "Dólares digitales": stablecoins, rendimientos y cadenas desde defi.json (DefiLlama).
(function () {
  const caja = document.getElementById("defi");
  if (!caja) return;
  const $ = (id) => document.getElementById(id);
  const lang = document.documentElement.lang.toLowerCase(), PT = lang.startsWith("pt"), EN = lang.startsWith("en");
  const LOC = PT ? "pt-BR" : EN ? "en-US" : "es-PY";
  const T = PT ? { milM: "bi", total: (n) => `US$ ${n}<small> bilhões</small>`, dias: "em 30 dias", sem: "7 d", premios: "inclui prêmios em tokens", act: "atualizado", resp: { "fiat-backed": "lastro em dólar", "crypto-backed": "lastro cripto", algorithmic: "algorítmica" } }
    : EN ? { milM: "B", total: (n) => `US$ ${n}<small> billion</small>`, dias: "in 30 days", sem: "7 d", premios: "includes token rewards", act: "updated", resp: { "fiat-backed": "dollar-backed", "crypto-backed": "crypto-backed", algorithmic: "algorithmic" } }
    : { milM: "mil M", total: (n) => `US$ ${n}<small> mil millones</small>`, dias: "en 30 días", sem: "7 d", premios: "incluye premios en tokens", act: "actualizado", resp: { "fiat-backed": "respaldo en dólares", "crypto-backed": "respaldo cripto", algorithmic: "algorítmica" } };
  const num = (n, d = 1) => Number(n).toLocaleString(LOC, { minimumFractionDigits: d, maximumFractionDigits: d });
  const milM = (usd) => `US$ ${num(usd / 1e9, usd >= 1e10 ? 0 : 1)} ${T.milM}`;
  const signo = (v) => (v > 0 ? "+" : "") + num(v, 2) + " %";
  const clase = (v) => (v == null ? "" : v >= 0 ? "sube" : "baja");
  const esc = (t) => String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  fetch((document.body.dataset.raiz || "") + "defi.json?t=" + Math.floor(Date.now() / 1800e3)).then((r) => r.json()).then((d) => {
    const s = d.stablecoins;
    if (s) {
      $("df-total").innerHTML = T.total(num(s.total / 1e9, 0));
      if (s.var_30d != null) { const v = $("df-var"); v.textContent = `${signo(s.var_30d)} ${T.dias}`; v.className = "defi-var " + clase(s.var_30d); }
      // serie de 180 días como área
      const serie = (s.historial_mil_millones || []).map((x) => x[1]);
      if (serie.length > 2) {
        const lo = Math.min(...serie), hi = Math.max(...serie), pad = (hi - lo) * .15 || 1;
        const X = (i) => (i / (serie.length - 1)) * 600, Y = (v) => 130 - ((v - lo + pad) / (hi - lo + pad * 2)) * 120;
        const linea = serie.map((v, i) => `${i ? "L" : "M"}${X(i).toFixed(1)} ${Y(v).toFixed(1)}`).join(" ");
        $("df-serie").innerHTML = `<defs><linearGradient id="df-g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="var(--compra)" stop-opacity=".28"/><stop offset="1" stop-color="var(--compra)" stop-opacity="0"/></linearGradient></defs>`
          + `<path d="${linea} L600 140 L0 140 Z" fill="url(#df-g)"/><path d="${linea}" fill="none" stroke="var(--compra)" stroke-width="2" vector-effect="non-scaling-stroke"/>`;
      }
      $("df-monedas").innerHTML = (s.principales || []).map((m) => {
        const parte = (m.circulacion / s.total) * 100;
        return `<li><div class="defi-fila"><b>${esc(m.simbolo)}</b><span class="defi-meta">${esc(m.nombre)} · ${esc(T.resp[m.respaldo] || m.respaldo)}</span>`
          + `<span class="defi-num">${milM(m.circulacion)}</span><span class="defi-cambio ${clase(m.var_7d)}" title="${T.sem}">${m.var_7d == null ? "" : signo(m.var_7d) + " · " + T.sem}</span></div>`
          + `<div class="defi-barra"><i style="width:${Math.max(1.5, parte).toFixed(1)}%"></i></div></li>`;
      }).join("");
    }
    if (d.rendimientos) {
      $("df-rend").innerHTML = d.rendimientos.map((r) => `<tr><td><a href="${esc(r.enlace)}" target="_blank" rel="noopener">${esc(r.protocolo)}</a></td><td>${esc(r.moneda)}</td><td class="om">${esc(r.red)}</td>`
        + `<td class="r"><b>${num(r.apy, 2)} %</b>${r.apy_premios > 0 ? `<small class="defi-premio">${T.premios}</small>` : ""}</td><td class="r om">${milM(r.tvl)}</td></tr>`).join("");
    }
    if (d.cadenas) {
      const max = Math.max(...d.cadenas.map((c) => c.tvl));
      $("df-cadenas").innerHTML = d.cadenas.map((c) => `<li><span>${esc(c.nombre)}</span><span class="defi-num">${milM(c.tvl)}</span><div class="defi-barra"><i style="width:${(c.tvl / max * 100).toFixed(1)}%"></i></div></li>`).join("");
    }
    if (d.actualizado_utc) {
      const h = new Date(d.actualizado_utc.replace(" ", "T") + ":00Z").toLocaleString(LOC, { day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit" });
      $("df-fuente").innerHTML = `${esc($("df-fuente").textContent.replace(/\.$/, ""))} · <a href="https://defillama.com" target="_blank" rel="noopener">defillama.com</a> · ${T.act} ${h}`;
    }
  }).catch(() => { const t = $("df-total"); if (t) t.textContent = "—"; });
})();
