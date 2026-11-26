"""
Radar de sucesos y fondos ilustrados de WIQON Ciberseguridad (los usa construir_ciberseguridad.py).
El radar lee https://n8n.wiqonlab.com/webhook/sucesos: un resumen público de los últimos 30 días que arma la Raspberry
(sucesos_publicos.py) con ransomware.live, el catálogo KEV de CISA, Have I Been Pwned y listas de phishing.
Nunca trae nombres de empresas afectadas: solo país, sector, grupo, CVE y cantidades.
"""
from urllib.parse import quote

URL = "https://n8n.wiqonlab.com/webhook/sucesos"


def svg_fondo(svg):
    return "url(\"data:image/svg+xml," + quote(svg, safe=":/=' ") + "\")"


# ilustraciones de fondo de cada plan (trazo cian, se ven tenues en la esquina de la tarjeta)
ICONOS = {
    "vig": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" fill="none" stroke="#3fe0ff" stroke-width="3">'
           '<circle cx="60" cy="60" r="50"/><circle cx="60" cy="60" r="32"/><circle cx="60" cy="60" r="14"/>'
           '<path d="M60 60 L104 36" stroke-width="4" stroke-linecap="round"/><circle cx="88" cy="46" r="5" fill="#3fe0ff"/></svg>',
    "rev": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" fill="none" stroke="#3fe0ff" stroke-width="3">'
           '<rect x="8" y="16" width="84" height="64" rx="8"/><path d="M8 30 H92"/><circle cx="18" cy="23" r="2.5" fill="#3fe0ff"/>'
           '<circle cx="27" cy="23" r="2.5" fill="#3fe0ff"/><path d="M20 44 H60 M20 54 H50 M20 64 H56"/>'
           '<circle cx="78" cy="78" r="20" stroke-width="5"/><path d="M92 92 L110 110" stroke-width="8" stroke-linecap="round"/></svg>',
    "aud": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" fill="none" stroke="#3fe0ff" stroke-width="3">'
           '<path d="M60 8 L102 24 V56 C102 84 84 102 60 112 C36 102 18 84 18 56 V24 Z" stroke-width="4" stroke-linejoin="round"/>'
           '<path d="M40 50 H80 M40 64 H80 M40 78 H66"/><path d="M76 74 L82 80 L94 66" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>',
}
# trama de candados y circuitos para «Cómo trabajamos»
TRAMA = ('<svg xmlns="http://www.w3.org/2000/svg" width="160" height="160" viewBox="0 0 160 160" fill="none" stroke="#3fe0ff" stroke-width="1.4">'
         '<path d="M0 40 H40 L56 24 H90 M90 24 V8 M160 120 H120 L104 136 H70 M70 136 V152 M40 160 V120 L56 104"/>'
         '<circle cx="90" cy="8" r="3"/><circle cx="70" cy="152" r="3"/><circle cx="56" cy="104" r="3"/>'
         '<rect x="104" y="44" width="26" height="22" rx="4"/><path d="M109 44 V37 a8 8 0 0 1 16 0 V44"/>'
         '<rect x="22" y="70" width="20" height="17" rx="3"/><path d="M26 70 V65 a6 6 0 0 1 12 0 V70"/></svg>')

CSS = """<style>
.radar-s{--r-fondo:#030a1a;--r-borde:#17325f;--r-tx:#e6f0ff;--r-sv:#a9bbd8;--rw:#ff5d6c;--kev:#ffc04d;--hibp:#b49cff;--ph:#3fe0ff;
  position:relative;width:min(1120px,calc(100vw - 32px));left:50%;transform:translateX(-50%);margin:26px 0 30px;
  background:radial-gradient(700px 380px at 22% 50%,rgba(42,123,255,.22),transparent 70%),var(--r-fondo);color:var(--r-tx);
  border:1px solid var(--r-borde);border-radius:22px;padding:26px;display:grid;grid-template-columns:minmax(260px,400px) 1fr;gap:28px;align-items:center;overflow:hidden}
.radar-s::before{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(63,224,255,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(63,224,255,.06) 1px,transparent 1px);background-size:32px 32px;pointer-events:none}
.radar-s>*{position:relative}
.radar{aspect-ratio:1;width:100%;border-radius:50%;position:relative;
  background:radial-gradient(circle closest-side,transparent 0 24%,rgba(63,224,255,.28) 24.3% 24.8%,transparent 25% 49%,rgba(63,224,255,.28) 49.3% 49.8%,transparent 50% 74%,rgba(63,224,255,.28) 74.3% 74.8%,transparent 75% 98.6%,rgba(63,224,255,.5) 99% 100%),
  linear-gradient(rgba(63,224,255,.2),rgba(63,224,255,.2)) center/1px 100% no-repeat,linear-gradient(90deg,rgba(63,224,255,.2),rgba(63,224,255,.2)) center/100% 1px no-repeat,#04122a}
.radar .barrido{position:absolute;inset:0;border-radius:50%;background:conic-gradient(from 0deg,transparent 0 280deg,rgba(63,224,255,.12) 320deg,rgba(63,224,255,.55) 360deg);animation:r-gira 6s linear infinite;-webkit-mask:radial-gradient(circle closest-side,#000 98%,transparent 99%);mask:radial-gradient(circle closest-side,#000 98%,transparent 99%);transform-origin:50% 50%}
.radar .blip{position:absolute;width:10px;height:10px;margin:-5px 0 0 -5px;border-radius:50%;background:var(--c);box-shadow:0 0 10px var(--c);opacity:.35;animation:r-blip 6s linear infinite}
.radar .centro{position:absolute;left:50%;top:50%;width:46px;height:46px;margin:-23px;border-radius:50%;background:#06142e;border:2px solid #3fe0ff;display:grid;place-items:center;font:800 15px/1 var(--titulos);color:#fff}
@keyframes r-gira{to{transform:rotate(360deg)}}
@keyframes r-blip{0%{opacity:1;transform:scale(1.9)}18%{opacity:.75;transform:scale(1)}100%{opacity:.25;transform:scale(1)}}
.radar-d h2{margin:0 0 4px !important;font-size:1.3rem !important;color:var(--r-tx)}
.radar-d .sub{color:var(--r-sv) !important;margin:0 0 16px;font-size:.92rem !important}
.r-cifras{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin-bottom:16px}
.r-cifra{border:1px solid var(--r-borde);border-radius:14px;padding:12px 14px;background:rgba(6,20,46,.75)}
.r-cifra b{display:block;font:800 1.7rem/1.1 var(--titulos);color:var(--c)}
.r-cifra span{font-size:.86rem;color:var(--r-sv);line-height:1.35;display:block;margin-top:4px}
.r-lista{list-style:none;margin:0 !important;padding:0 !important;display:grid;gap:6px;min-height:186px}
.r-lista li{display:grid;grid-template-columns:10px auto 1fr;gap:10px;align-items:baseline;font-size:.88rem !important;color:var(--r-tx) !important;line-height:1.4 !important;padding:6px 10px;border-radius:10px;background:rgba(6,20,46,.6);animation:r-entra .5s ease both}
.r-lista li i{width:9px;height:9px;border-radius:50%;background:var(--c);align-self:center}
.r-lista time{font-family:var(--mono);color:var(--r-sv);font-size:.8rem}
@keyframes r-entra{from{opacity:0;transform:translateY(8px)}}
.radar-s .fuente{grid-column:1/-1;margin:0;font-size:.78rem !important;color:var(--r-sv) !important}
.radar-s .fuente a{color:#8aebff}
@media (max-width:760px){.radar-s{grid-template-columns:1fr;padding:18px}.radar{max-width:300px;margin:0 auto}.r-cifra b{font-size:1.4rem}}
@media (prefers-reduced-motion:reduce){.radar .barrido,.radar .blip,.r-lista li{animation:none}.radar .blip{opacity:.9}}
.legal-p .tit.plan{position:relative;padding-right:120px;background-repeat:no-repeat;background-position:right 16px top 16px;background-size:92px}
.legal-p .tit.plan.vig{background-image:%VIG%}.legal-p .tit.plan.rev{background-image:%REV%}.legal-p .tit.plan.aud{background-image:%AUD%}
@media (max-width:560px){.legal-p .tit.plan{padding-right:18px;background-size:64px;background-position:right 12px top 12px}.legal-p .tit.plan strong{display:inline-block;padding-right:70px}}
.trabajo{position:relative;border:1px solid var(--borde);border-radius:16px;padding:6px 22px 10px;margin-top:10px;background-image:linear-gradient(var(--caja-bg),var(--caja-bg)),%TRAMA%;background-size:auto,160px}
.trabajo::before{content:"";position:absolute;inset:0;border-radius:16px;background:linear-gradient(90deg,var(--fondo) 35%,transparent);opacity:.85;pointer-events:none}
.trabajo>*{position:relative}
</style>""".replace("%VIG%", svg_fondo(ICONOS["vig"])).replace("%REV%", svg_fondo(ICONOS["rev"])) \
           .replace("%AUD%", svg_fondo(ICONOS["aud"])).replace("%TRAMA%", svg_fondo(TRAMA.replace('stroke="#3fe0ff"', 'stroke="#3fe0ff" stroke-opacity=".35"')))

T = {
    "es": dict(
        tit="Radar de sucesos · últimos 30 días",
        sub="Lo que está pasando en la región y en el mundo, con datos públicos que vigilamos todos los días.",
        c_rw="ataques de ransomware publicados en Paraguay y Brasil", c_kev="fallas explotadas activamente (CISA)",
        c_hibp="cuentas expuestas en filtraciones nuevas", c_ph="sitios .py usados hoy para phishing",
        rw="Ransomware en {pais}: empresa de {sector} · grupo {grupo}", kev="Falla explotada: {prod} ({cve})",
        kev_rw=" · usada en ransomware", hibp="Filtración nueva: {n} cuentas expuestas",
        paises={"PY": "Paraguay", "BR": "Brasil"}, sin_sector="sector sin dato",
        fuente='Fuentes públicas: ransomware.live, catálogo KEV de CISA, Have I Been Pwned, OpenPhish y Phishing.Database. '
               'No mostramos nombres de empresas afectadas: son víctimas. Actualizado: ',
        cargando="Cargando sucesos…", sin="El radar se actualiza todos los días a la mañana.",
        sectores={"Technology": "tecnología", "Professional Services": "servicios profesionales", "Retail & E-Commerce": "comercio",
                  "Manufacturing": "industria", "Healthcare": "salud", "Financial Services": "finanzas", "Education": "educación",
                  "Construction": "construcción", "Transportation/Logistics": "transporte y logística", "Agriculture": "agro",
                  "Hospitality": "hotelería y turismo", "Government": "gobierno", "Energy": "energía", "Business Services": "servicios",
                  "Consumer Services": "servicios al consumidor", "Telecommunication": "telecomunicaciones", "Public Sector": "sector público",
                  "Legal": "servicios legales", "Real Estate": "inmobiliaria", "Media": "medios"}),
    "pt": dict(
        tit="Radar de ocorrências · últimos 30 dias",
        sub="O que está acontecendo na região e no mundo, com dados públicos que monitoramos todos os dias.",
        c_rw="ataques de ransomware publicados no Paraguai e no Brasil", c_kev="falhas exploradas ativamente (CISA)",
        c_hibp="contas expostas em vazamentos novos", c_ph="sites .py usados hoje para phishing",
        rw="Ransomware no {pais}: empresa de {sector} · grupo {grupo}", kev="Falha explorada: {prod} ({cve})",
        kev_rw=" · usada em ransomware", hibp="Vazamento novo: {n} contas expostas",
        paises={"PY": "Paraguai", "BR": "Brasil"}, sin_sector="setor sem dado",
        fuente='Fontes públicas: ransomware.live, catálogo KEV da CISA, Have I Been Pwned, OpenPhish e Phishing.Database. '
               'Não mostramos nomes de empresas afetadas: são vítimas. Atualizado: ',
        cargando="Carregando ocorrências…", sin="O radar é atualizado todos os dias de manhã.",
        sectores={"Technology": "tecnologia", "Professional Services": "serviços profissionais", "Retail & E-Commerce": "comércio",
                  "Manufacturing": "indústria", "Healthcare": "saúde", "Financial Services": "finanças", "Education": "educação",
                  "Construction": "construção", "Transportation/Logistics": "transporte e logística", "Agriculture": "agro",
                  "Hospitality": "hotelaria e turismo", "Government": "governo", "Energy": "energia", "Business Services": "serviços",
                  "Consumer Services": "serviços ao consumidor", "Telecommunication": "telecomunicações", "Public Sector": "setor público",
                  "Legal": "serviços jurídicos", "Real Estate": "imobiliário", "Media": "mídia"}),
}


def radar(lang):
    t = T[lang]
    import json
    tj = json.dumps(t, ensure_ascii=False)
    return f"""<section class="radar-s" aria-labelledby="radar-t">
<div class="radar" aria-hidden="true"><div class="barrido"></div><div id="r-blips"></div><div class="centro">W</div></div>
<div class="radar-d">
<h2 id="radar-t">{t['tit']}</h2>
<p class="sub">{t['sub']}</p>
<div class="r-cifras" id="r-cifras"></div>
<ul class="r-lista" id="r-lista" aria-live="off"><li><i style="--c:#3fe0ff"></i><time></time><span>{t['cargando']}</span></li></ul>
</div>
<p class="fuente" id="r-fuente">{t['fuente']}…</p>
</section>
<script>
(function () {{
  var T = {tj}, C = {{rw: 'var(--rw)', kev: 'var(--kev)', hibp: 'var(--hibp)', ph: 'var(--ph)'}};
  var lista = document.getElementById('r-lista'), cifras = document.getElementById('r-cifras'), blips = document.getElementById('r-blips');
  var quieto = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var nf = new Intl.NumberFormat(document.documentElement.lang);
  function el(tag, cls, txt) {{ var x = document.createElement(tag); if (cls) x.className = cls; if (txt != null) x.textContent = txt; return x; }}
  function grande(n) {{ return n >= 1e6 ? nf.format(Math.round(n / 1e5) / 10) + ' M' : nf.format(n); }}
  function texto(e) {{
    if (e.t === 'rw') return T.rw.replace('{{pais}}', T.paises[e.pais] || e.pais).replace('{{sector}}', T.sectores[e.sector] || (e.sector && e.sector !== 'Other' ? e.sector : T.sin_sector)).replace('{{grupo}}', e.grupo || '?');
    if (e.t === 'kev') return T.kev.replace('{{prod}}', e.prod).replace('{{cve}}', e.cve) + (e.rw ? T.kev_rw : '');
    return T.hibp.replace('{{n}}', grande(e.n));
  }}
  function hash(s) {{ var h = 0; for (var i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) >>> 0; return h; }}
  function cifra(n, txt, c) {{ var d = el('div', 'r-cifra'); d.style.setProperty('--c', c); d.appendChild(el('b', '', n)); d.appendChild(el('span', '', txt)); cifras.appendChild(d); }}
  function fila(e) {{
    var li = el('li'); var i = el('i'); i.style.setProperty('--c', C[e.t]); li.appendChild(i);
    var f = (e.f || '').split('-'); li.appendChild(el('time', '', f.length === 3 ? f[2] + '/' + f[1] : '')); li.lastChild.setAttribute('datetime', e.f);
    li.appendChild(el('span', '', texto(e))); return li;
  }}
  fetch({URL!r}).then(function (r) {{ return r.json(); }}).then(function (d) {{
    var por = {{rw: [], kev: [], hibp: []}}, ev = [];
    (d.eventos || []).forEach(function (e) {{ if (por[e.t]) por[e.t].push(e); }});
    for (var k = 0; ev.length < (d.eventos || []).length && k < 80; k++) ['rw', 'kev', 'hibp'].forEach(function (t) {{ if (por[t][k]) ev.push(por[t][k]); }});
    if (!ev.length) {{ lista.innerHTML = ''; lista.appendChild(el('li', '', T.sin)); return; }}
    var tt = d.totales || {{}}, ph = d.phishing || {{}};
    cifra(nf.format(tt.rw || 0), T.c_rw, C.rw); cifra(nf.format(tt.kev || 0), T.c_kev, C.kev);
    cifra(grande(tt.hibp_cuentas || 0), T.c_hibp, C.hibp); if (ph.py_sitios != null) cifra(nf.format(ph.py_sitios), T.c_ph, C.ph);
    ev.slice(0, 40).forEach(function (e) {{
      var h = hash((e.cve || '') + e.f + (e.grupo || '') + (e.n || '') + e.t), ang = (h % 360), rad = 0.18 + ((h >> 9) % 70) / 100 * 0.42 + (e.t === 'rw' ? 0 : 0.05);
      var b = el('span', 'blip'); b.style.setProperty('--c', C[e.t]);
      b.style.left = (50 + Math.sin(ang * Math.PI / 180) * rad * 86) + '%'; b.style.top = (50 - Math.cos(ang * Math.PI / 180) * rad * 86) + '%';
      b.style.animationDelay = (ang / 360 * 6 - 6).toFixed(2) + 's'; blips.appendChild(b);
    }});
    var desde = 0, N = 6;
    function mostrar() {{ lista.innerHTML = ''; for (var k = 0; k < N && k < ev.length; k++) lista.appendChild(fila(ev[(desde + k) % ev.length])); }}
    mostrar();
    if (!quieto && ev.length > N) setInterval(function () {{
      if (document.hidden) return;
      desde = (desde + 1) % ev.length; lista.insertBefore(fila(ev[(desde + N - 1) % ev.length]), lista.firstChild);
      while (lista.children.length > N) lista.removeChild(lista.lastChild);
    }}, 3200);
    var a = (d.actualizado || '').replace('T', ' ');
    document.getElementById('r-fuente').textContent = T.fuente + a + '.';
  }}).catch(function () {{ lista.innerHTML = ''; lista.appendChild(el('li', '', T.sin)); }});
}})();
</script>"""
