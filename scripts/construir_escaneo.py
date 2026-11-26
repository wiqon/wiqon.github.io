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
.esc-res{margin-top:18px;display:none}
.esc-cab{display:flex;align-items:center;gap:14px;padding:16px 18px;border-radius:16px;border:1px solid rgba(127,127,127,.35);margin-bottom:12px}
.esc-cab b{font-size:1.2rem}
.esc-lista{list-style:none;padding:0 !important;margin:0 !important;display:grid;gap:10px}
.esc-lista li{display:grid;grid-template-columns:18px 1fr;gap:12px;padding:14px 16px;border-radius:14px;border:1px solid rgba(127,127,127,.3)}
.esc-lista p{margin:4px 0 0}
.esc-lista .con{opacity:.85;font-size:.95rem}
.pt{width:16px;height:16px;border-radius:50%;margin-top:4px}
.pt.verde{background:#22c55e}.pt.amarillo{background:#eab308}.pt.rojo{background:#ef4444}
.esc-cta{margin-top:18px;padding:16px 18px;border-radius:16px;border:2px solid #2ad4ff}
.sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
</style>"""


def script(t):
    return f"""<script>
(function () {{
  var f = document.getElementById('esc-f'), e = document.getElementById('esc-e'), r = document.getElementById('esc-r');
  var NIVEL = {t['niveles']!r};
  function el(tag, cls, txt) {{ var x = document.createElement(tag); if (cls) x.className = cls; if (txt) x.textContent = txt; return x; }}
  f.addEventListener('submit', function (ev) {{
    ev.preventDefault();
    var d = (f.dominio.value || '').trim();
    if (d.length < 4) {{ e.textContent = {t['falta']!r}; return; }}
    var b = f.querySelector('button'); b.disabled = true; r.style.display = 'none'; e.textContent = {t['escaneando']!r};
    fetch({URL!r}, {{ method: 'POST', body: new URLSearchParams({{ dominio: d }}) }})
      .then(function (x) {{ return x.json(); }})
      .then(function (j) {{
        if (j.aviso || j.error || !j.items) {{ e.textContent = j.aviso || j.error || {t['fallo']!r}; return; }}
        e.textContent = '';
        r.innerHTML = '';
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
        r.appendChild(ul);
        var cta = el('div', 'esc-cta'); cta.innerHTML = {t['cta']!r}; r.appendChild(cta);
        r.style.display = 'block';
      }})
      .catch(function () {{ e.textContent = {t['fallo']!r}; }})
      .finally(function () {{ b.disabled = false; }});
  }});
}})();
</script>"""


T = {
    "es": dict(
        niveles={"verde": "bien", "amarillo": "hay cosas para mejorar", "rojo": "hay puntos urgentes"},
        falta="Escribí un dominio, por ejemplo miempresa.com.py", escaneando="Escaneando… (tarda unos 10 segundos)",
        fallo="No pudimos completar el escaneo. Probá de nuevo en unos minutos.", urg="urgentes", imp="importantes", bien="bien",
        cta='<b>Esto es una muestra.</b> La revisión completa mira además los plugins y versiones con fallas conocidas, '
            'archivos y paneles expuestos, DKIM, dominios que imitan al tuyo y puertos abiertos, con un informe y cómo '
            'corregir cada punto. <a href="../ciberseguridad/">Ver WIQON Ciberseguridad</a>.'),
    "pt": dict(
        niveles={"verde": "tudo bem", "amarillo": "há pontos a melhorar", "rojo": "há pontos urgentes"},
        falta="Digite um domínio, por exemplo minhaempresa.com.br", escaneando="Escaneando… (leva uns 10 segundos)",
        fallo="Não foi possível concluir o escaneamento. Tente de novo em alguns minutos.", urg="urgentes", imp="importantes", bien="ok",
        cta='<b>Isto é uma amostra.</b> A revisão completa também verifica plugins e versões com falhas conhecidas, '
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
<p class="esc-estado" id="esc-e" role="status" aria-live="polite"></p>
<div class="esc-res" id="esc-r"></div>
<h2>Qué hace y qué no</h2>
<ul>
<li><strong>Es pasivo:</strong> mira solo lo que ve cualquier navegador al abrir la portada y los registros públicos del DNS, como lo hacen otros servicios de análisis abiertos.</li>
<li><strong>No</strong> prueba contraseñas, no busca archivos ocultos, no escanea puertos y no cambia nada en el sitio.</li>
<li>Guardamos el dominio consultado y la fecha, para estadísticas y para evitar abusos. No guardamos tu IP en claro.</li>
<li>Hay un límite de escaneos por hora.</li>
</ul>
<p>¿Querés la revisión completa, con informe y cómo corregir cada punto? Mirá <a href="../ciberseguridad/">WIQON Ciberseguridad</a>.</p>
{script(T['es'])}
"""

PT = f"""{ESTILO}<h1>Escaneamento gratuito do seu site</h1>
<p>Digite o domínio do seu site (ou de qualquer site) e em poucos segundos mostramos um semáforo com o básico: conexão segura, certificado, cabeçalhos de segurança, versões à vista, proteção do e-mail (SPF e DMARC) e se aparece em listas públicas de phishing.</p>
<form class="esc-form" id="esc-f" novalidate>
  <label for="esc-d" class="sr-only">Domínio</label>
  <input id="esc-d" name="dominio" placeholder="minhaempresa.com.br" autocomplete="url" inputmode="url" maxlength="200" required>
  <button class="btn p" type="submit">Escanear grátis</button>
</form>
<p class="esc-estado" id="esc-e" role="status" aria-live="polite"></p>
<div class="esc-res" id="esc-r"></div>
<h2>O que faz e o que não faz</h2>
<ul>
<li><strong>É passivo:</strong> olha só o que qualquer navegador vê ao abrir a página inicial e os registros públicos do DNS, como outros serviços abertos de análise.</li>
<li><strong>Não</strong> testa senhas, não procura arquivos ocultos, não escaneia portas e não muda nada no site.</li>
<li>Guardamos o domínio consultado e a data, para estatísticas e para evitar abusos. Não guardamos seu IP em claro.</li>
<li>Há um limite de escaneamentos por hora.</li>
</ul>
<p>Quer a revisão completa, com relatório e como corrigir cada ponto? Veja a <a href="../ciberseguranca/">WIQON Cibersegurança</a>.</p>
{script(T['pt'])}
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
