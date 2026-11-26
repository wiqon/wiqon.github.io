"""
Escaneo gratuito de sitios (prueba pasiva): escaneo/  y  br/escaneo/
El navegador manda el dominio al webhook «escaneo-gratis» de n8n, que llama al servicio escaneo_gratis.py de la
Raspberry (solo lo que ve un navegador y el DNS público). Reutiliza BASE y pie de construir_legales.py.
Uso:  python scripts/construir_escaneo.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from construir_legales import BASE, RAIZ, pie

URL = "https://n8n.wiqonlab.com/webhook/escaneo-gratis"

ESTILO = """<style>
.esc-form{display:flex;gap:10px;flex-wrap:wrap;margin:18px 0 8px}
.esc-form input{flex:1 1 260px;min-width:0;font:inherit;font-size:1.05rem;padding:12px 14px;border-radius:12px;border:1px solid rgba(127,127,127,.45);background:transparent;color:inherit}
.esc-form button{font-size:1.05rem}
.esc-estado{min-height:1.4em;margin:6px 0 0}
.esc-ses{margin:4px 0 0;font-size:.92rem}
.esc-nota{font-weight:600;margin:0 0 10px}
.acceso label.check{display:flex;gap:8px;align-items:flex-start;margin-top:12px;font-size:.88rem;color:var(--suave)}
.acceso .btn{margin-top:16px;width:100%}
.acceso .msg.ok{color:var(--sube)}.acceso .msg.error{color:var(--baja)}
.acceso .pie-d{font-size:.8rem}
.esc-res{margin-top:18px;display:none}
.esc-cab{display:flex;align-items:center;gap:14px;padding:16px 18px;border-radius:16px;border:1px solid rgba(127,127,127,.35);margin-bottom:12px}
.esc-cab b{font-size:1.2rem}
.esc-lista{list-style:none;padding:0 !important;margin:0 !important;display:grid;gap:10px}
.esc-lista li{display:grid;grid-template-columns:18px 1fr;gap:12px;padding:14px 16px;border-radius:14px;border:1px solid rgba(127,127,127,.3)}
.esc-lista p{margin:4px 0 0}
.esc-lista .con{opacity:.85;font-size:.95rem}
.pt{width:16px;height:16px;border-radius:50%;margin-top:4px}
.pt.verde{background:#22c55e}.pt.amarillo{background:#eab308}.pt.rojo{background:#ef4444}
.esc-lista li.bloq{opacity:.9;border-style:dashed}
.esc-lista li.bloq b{filter:blur(0)}
.esc-lista li.bloq span.borroso{display:inline-block;filter:blur(5px);user-select:none}
.esc-cta{margin-top:18px;padding:16px 18px;border-radius:16px;border:2px solid #2ad4ff}
.sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
</style>"""


def script(t):
    return f"""<script>
(function () {{
  var f = document.getElementById('esc-f'), e = document.getElementById('esc-e'), r = document.getElementById('esc-r'),
      ses = document.getElementById('esc-ses'), pendiente = null;
  var NIVEL = {t['niveles']!r};
  function el(tag, cls, txt) {{ var x = document.createElement(tag); if (cls) x.className = cls; if (txt) x.textContent = txt; return x; }}
  function cuenta() {{ return window.wiqonCuenta || {{}}; }}
  function pintarSes(s) {{
    ses.textContent = '';
    if (s && s.user) {{ ses.appendChild(document.createTextNode({t['ses_si']!r}.replace('{{e}}', s.user.email || ''))); }}
    else {{
      ses.appendChild(document.createTextNode({t['ses_no']!r} + ' '));
      var a = el('a', '', {t['entrar']!r}); a.href = '#ingresar';
      a.addEventListener('click', function (ev) {{ ev.preventDefault(); if (cuenta().abrir) cuenta().abrir(); }}); ses.appendChild(a);
    }}
  }}
  document.addEventListener('wiqon:sesion', function (ev) {{
    pintarSes(ev.detail.sesion);
    if (ev.detail.logueado && pendiente) {{ f.dominio.value = pendiente; pendiente = null; f.requestSubmit ? f.requestSubmit() : f.dispatchEvent(new Event('submit')); }}
  }});
  try {{ var d0 = sessionStorage.getItem('esc-pendiente'); if (d0) {{ pendiente = d0; f.dominio.value = d0; sessionStorage.removeItem('esc-pendiente'); }} }} catch (x) {{}}
  function pintar(j) {{
    r.innerHTML = '';
    if (j.repetido) r.appendChild(el('p', 'esc-nota', {t['repetido']!r}.replace('F', (j.fecha_uso || '').slice(0, 10))));
    var cab = el('div', 'esc-cab'); cab.appendChild(el('span', 'pt ' + j.nivel));
    var c = el('div'); c.appendChild(el('b', '', j.dominio + ': ' + NIVEL[j.nivel]));
    c.appendChild(el('p', '', j.resumen.rojo + ' {t['urg']} · ' + j.resumen.amarillo + ' {t['imp']} · ' + j.resumen.verde + ' {t['bien']}'));
    cab.appendChild(c); r.appendChild(cab);
    var ul = el('ul', 'esc-lista');
    j.items.forEach(function (i) {{
      var li = el('li'); li.appendChild(el('span', 'pt ' + i.estado));
      var dv = el('div'); dv.appendChild(el('b', '', i.titulo)); dv.appendChild(el('p', '', i.detalle));
      if (i.consejo) dv.appendChild(el('p', 'con', i.consejo));
      li.appendChild(dv); ul.appendChild(li);
    }});
    var oc = j.ocultos || [];
    oc.forEach(function (o) {{
      var li = el('li', 'bloq'); li.appendChild(el('span', 'pt ' + o.estado));
      var dv = el('div'); dv.appendChild(el('b', '', '🔒 ' + (o.estado === 'rojo' ? {t['oc_rojo']!r} : {t['oc_ama']!r})));
      dv.appendChild(el('p', '', {t['oc_txt']!r})); dv.appendChild(el('span', 'borroso', 'xxxxxxxx xxxxx xxxxxxxxxxxx xxxxxx'));
      li.appendChild(dv); ul.appendChild(li);
    }});
    r.appendChild(ul);
    var cta = el('div', 'esc-cta');
    cta.innerHTML = (oc.length ? '<b>' + {t['cta_n']!r}.replace('N', oc.length) + '</b> ' : '') + {t['cta']!r}; r.appendChild(cta);
    r.style.display = 'block';
  }}
  f.addEventListener('submit', function (ev) {{
    ev.preventDefault();
    var d = (f.dominio.value || '').trim();
    if (d.length < 4) {{ e.textContent = {t['falta']!r}; return; }}
    var s = cuenta().sesion;
    if (!s) {{
      pendiente = d; try {{ sessionStorage.setItem('esc-pendiente', d); }} catch (x) {{}}
      e.textContent = {t['pide_cuenta']!r}; if (cuenta().abrir) cuenta().abrir(); return;
    }}
    var b = f.querySelector('button'); b.disabled = true; r.style.display = 'none'; e.textContent = {t['escaneando']!r};
    fetch({URL!r}, {{ method: 'POST', body: new URLSearchParams({{ dominio: d, token: s.access_token }}) }})
      .then(function (x) {{ return x.json(); }})
      .then(function (j) {{
        if (j.requiere_cuenta) {{ e.textContent = {t['pide_cuenta']!r}; pendiente = d; if (cuenta().abrir) cuenta().abrir(); return; }}
        if (j.usado) {{
          e.textContent = '';
          r.innerHTML = '<div class="esc-cta"><b>' + {t['usado']!r}.replace('D', j.dominio_usado) + '</b> ' + {t['cta']!r} + '</div>';
          r.style.display = 'block'; return;
        }}
        if (j.aviso || j.error || !j.items) {{ e.textContent = j.aviso || j.error || {t['fallo']!r}; return; }}
        e.textContent = ''; pintar(j);
      }})
      .catch(function () {{ e.textContent = {t['fallo']!r}; }})
      .finally(function () {{ b.disabled = false; }});
  }});
}})();
</script>"""


DIALOGO = {
    "es": """<dialog class="acceso" id="acceso" aria-labelledby="acc-t">
  <form class="cuerpo" id="acc-form" novalidate>
    <div class="cab-d"><h3 id="acc-t">Entrá para escanear gratis</h3><button class="cerrar" type="button" aria-label="Cerrar">×</button></div>
    <p>Escribí tu email y te mandamos un enlace para entrar. No usamos contraseñas. Cada cuenta tiene un escaneo gratis.</p>
    <label class="campo" for="acc-email">Email</label>
    <input type="email" id="acc-email" name="email" autocomplete="email" required placeholder="tu@email.com">
    <label class="check"><input type="checkbox" id="acc-priv" required> <span>Acepto la <a href="../privacidad/" target="_blank">política de privacidad</a>.</span></label>
    <label class="check"><input type="checkbox" id="acc-nov"> <span>Quiero recibir novedades de WIQON (opcional, me puedo dar de baja cuando quiera).</span></label>
    <button class="btn p" type="submit">Enviar enlace de acceso</button>
    <p class="msg" id="acc-msg" role="status" aria-live="polite"></p>
    <p class="pie-d">Si ya tenés cuenta, el mismo enlace te hace entrar.</p>
  </form>
</dialog>""",
    "pt": """<dialog class="acceso" id="acceso" aria-labelledby="acc-t">
  <form class="cuerpo" id="acc-form" novalidate>
    <div class="cab-d"><h3 id="acc-t">Entre para escanear grátis</h3><button class="cerrar" type="button" aria-label="Fechar">×</button></div>
    <p>Digite seu e-mail e enviamos um link para entrar. Não usamos senhas. Cada conta tem um escaneamento grátis.</p>
    <label class="campo" for="acc-email">E-mail</label>
    <input type="email" id="acc-email" name="email" autocomplete="email" required placeholder="voce@email.com">
    <label class="check"><input type="checkbox" id="acc-priv" required> <span>Aceito a <a href="../privacidade/" target="_blank">política de privacidade</a>.</span></label>
    <label class="check"><input type="checkbox" id="acc-nov"> <span>Quero receber novidades da WIQON (opcional, posso cancelar quando quiser).</span></label>
    <button class="btn p" type="submit">Enviar link de acesso</button>
    <p class="msg" id="acc-msg" role="status" aria-live="polite"></p>
    <p class="pie-d">Se você já tem conta, o mesmo link faz você entrar.</p>
  </form>
</dialog>""",
}


def cuenta_js(lang):
    r = "../" if lang == "es" else "../../"
    return DIALOGO[lang] + f'\n<script src="{r}assets/vendor/supabase-2.119.0.js"></script>\n<script src="{r}assets/cuenta.js"></script>'


T = {
    "es": dict(
        niveles={"verde": "bien", "amarillo": "hay cosas para mejorar", "rojo": "hay puntos urgentes"},
        falta="Escribí un dominio, por ejemplo miempresa.com.py", escaneando="Escaneando… (tarda unos 10 segundos)",
        fallo="No pudimos completar el escaneo. Probá de nuevo en unos minutos.", urg="urgentes", imp="importantes", bien="bien",
        oc_rojo="Problema urgente", oc_ama="Problema importante",
        oc_txt="El detalle y cómo corregirlo están en el informe completo.",
        ses_si="Entraste como {e}. Tenés un escaneo gratis con esta cuenta.", ses_no="El escaneo gratis es uno por cuenta.",
        entrar="Entrá con tu email", pide_cuenta="Para escanear gratis, entrá con tu email: te mandamos un enlace y volvés acá.",
        usado="Ya usaste tu escaneo gratis con D.", repetido="Este es el resultado de tu escaneo gratis del F.",
        cta_n="Encontramos N problema(s) más.",
        cta='La muestra gratis te enseña uno. La revisión completa te explica todos y mira además los plugins y versiones con fallas conocidas, '
            'archivos y paneles expuestos, DKIM, dominios que imitan al tuyo y puertos abiertos, con un informe y cómo '
            'corregir cada punto. <a href="../ciberseguridad/">Ver WIQON Ciberseguridad</a>.'),
    "pt": dict(
        niveles={"verde": "tudo bem", "amarillo": "há pontos a melhorar", "rojo": "há pontos urgentes"},
        falta="Digite um domínio, por exemplo minhaempresa.com.br", escaneando="Escaneando… (leva uns 10 segundos)",
        fallo="Não foi possível concluir o escaneamento. Tente de novo em alguns minutos.", urg="urgentes", imp="importantes", bien="ok",
        oc_rojo="Problema urgente", oc_ama="Problema importante",
        oc_txt="O detalhe e como corrigir estão no relatório completo.",
        ses_si="Você entrou como {e}. Você tem um escaneamento grátis com esta conta.", ses_no="O escaneamento grátis é um por conta.",
        entrar="Entre com seu e-mail", pide_cuenta="Para escanear grátis, entre com seu e-mail: enviamos um link e você volta aqui.",
        usado="Você já usou seu escaneamento grátis com D.", repetido="Este é o resultado do seu escaneamento grátis de F.",
        cta_n="Encontramos mais N problema(s).",
        cta='A amostra grátis mostra um. A revisão completa explica todos e também verifica plugins e versões com falhas conhecidas, '
            'arquivos e painéis expostos, DKIM, domínios que imitam o seu e portas abertas, com relatório e como '
            'corrigir cada ponto. <a href="../ciberseguranca/">Ver WIQON Cibersegurança</a>.'),
}

ES = f"""{ESTILO}<h1>Escaneo gratuito de tu sitio</h1>
<p>Escribí el dominio de tu web (o de cualquier sitio) y en unos segundos te mostramos un semáforo con lo básico: conexión segura, certificado, cabeceras de seguridad, versiones a la vista, protección del correo (SPF y DMARC) y si aparece en listas públicas de phishing.</p>
<form class="esc-form" id="esc-f" novalidate>
  <label for="esc-d" class="sr-only">Dominio</label>
  <input id="esc-d" name="dominio" placeholder="miempresa.com.py" autocomplete="url" inputmode="url" maxlength="200" required>
  <button class="btn p" type="submit">Escanear gratis</button>
</form>
<p class="esc-ses" id="esc-ses">El escaneo gratis es uno por cuenta.</p>
<p class="esc-estado" id="esc-e" role="status" aria-live="polite"></p>
<div class="esc-res" id="esc-r"></div>
<h2>Qué hace y qué no</h2>
<ul>
<li><strong>Es pasivo:</strong> mira solo lo que ve cualquier navegador al abrir la portada y los registros públicos del DNS, como lo hacen otros servicios de análisis abiertos.</li>
<li><strong>No</strong> prueba contraseñas, no busca archivos ocultos, no escanea puertos y no cambia nada en el sitio.</li>
<li>Guardamos el dominio consultado y la fecha, para estadísticas y para evitar abusos. No guardamos tu IP en claro.</li>
<li>La muestra gratis te detalla un problema; si hay más, te decimos cuántos y qué tan graves son, y el detalle va en el informe completo.</li>
<li><strong>Un escaneo gratis por cuenta.</strong> Entrás con tu email (sin contraseña) y podés volver a ver tu resultado cuando quieras.</li>
</ul>
<p>¿Querés la revisión completa, con informe y cómo corregir cada punto? Mirá <a href="../ciberseguridad/">WIQON Ciberseguridad</a>.</p>
{script(T['es'])}
{cuenta_js('es')}
"""

PT = f"""{ESTILO}<h1>Escaneamento gratuito do seu site</h1>
<p>Digite o domínio do seu site (ou de qualquer site) e em poucos segundos mostramos um semáforo com o básico: conexão segura, certificado, cabeçalhos de segurança, versões à vista, proteção do e-mail (SPF e DMARC) e se aparece em listas públicas de phishing.</p>
<form class="esc-form" id="esc-f" novalidate>
  <label for="esc-d" class="sr-only">Domínio</label>
  <input id="esc-d" name="dominio" placeholder="minhaempresa.com.br" autocomplete="url" inputmode="url" maxlength="200" required>
  <button class="btn p" type="submit">Escanear grátis</button>
</form>
<p class="esc-ses" id="esc-ses">O escaneamento grátis é um por conta.</p>
<p class="esc-estado" id="esc-e" role="status" aria-live="polite"></p>
<div class="esc-res" id="esc-r"></div>
<h2>O que faz e o que não faz</h2>
<ul>
<li><strong>É passivo:</strong> olha só o que qualquer navegador vê ao abrir a página inicial e os registros públicos do DNS, como outros serviços abertos de análise.</li>
<li><strong>Não</strong> testa senhas, não procura arquivos ocultos, não escaneia portas e não muda nada no site.</li>
<li>Guardamos o domínio consultado e a data, para estatísticas e para evitar abusos. Não guardamos seu IP em claro.</li>
<li>A amostra grátis detalha um problema; se houver mais, dizemos quantos e qual a gravidade, e o detalhe vai no relatório completo.</li>
<li><strong>Um escaneamento grátis por conta.</strong> Você entra com seu e-mail (sem senha) e pode ver seu resultado de novo quando quiser.</li>
</ul>
<p>Quer a revisão completa, com relatório e como corrigir cada ponto? Veja a <a href="../ciberseguranca/">WIQON Cibersegurança</a>.</p>
{script(T['pt'])}
{cuenta_js('pt')}
"""

PAGINAS = [
    ("escaneo", "es", "Escaneo gratuito de tu sitio",
     "Escaneo gratuito y pasivo de un sitio web: HTTPS, certificado, cabeceras, versiones, SPF, DMARC y listas de phishing.", ES),
    ("br/escaneo", "pt", "Escaneamento gratuito do seu site",
     "Escaneamento gratuito e passivo de um site: HTTPS, certificado, cabeçalhos, versões, SPF, DMARC e listas de phishing.", PT),
]

if __name__ == "__main__":
    for ruta, lang, titulo, desc, cuerpo in PAGINAS:
        r = "../" * (ruta.count("/") + 1)
        destino = RAIZ / ruta / "index.html"
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(BASE.format(lang={"es": "es", "pt": "pt-BR"}[lang], titulo=titulo, desc=desc, ruta=ruta + "/", r=r,
                                       inicio="../", volver={"es": "Volver a WIQON", "pt": "Voltar para a WIQON"}[lang],
                                       cuerpo=cuerpo, pie=pie(lang)), encoding="utf-8")
        print("ok", destino.relative_to(RAIZ))
