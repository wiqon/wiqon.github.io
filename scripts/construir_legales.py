"""
Genera las páginas legales y de contacto (requisitos de procesadores de pago como dLocal Go):
  terminos/  devoluciones/  contacto/            (español)
  br/termos/ br/devolucoes/ br/contato/          (português)
Uso:  python scripts/construir_legales.py
"""
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
TITULAR, CI = "Avelino González Melgarejo", "4.690.007"
EMAIL, WA_TXT, WA = "contacto@wiqonlab.com", "+595 987 685 651", "https://wa.me/595987685651"
FORM_URL = "https://n8n.wiqonlab.com/webhook/contacto-web"
FECHA_ES, FECHA_PT = "17 de octubre de 2026", "17 de outubro de 2026"
REDES_ES = [("Facebook", "https://www.facebook.com/wiqonlab/"), ("Instagram", "https://www.instagram.com/wiqonlab/"),
            ("YouTube", "https://www.youtube.com/@wiqonlab"), ("Telegram", "https://t.me/wiqonlab"),
            ("TikTok", "https://www.tiktok.com/@wiqonlab"), ("X", "https://x.com/wiqonlab"), ("Discord", "https://discord.gg/8GDqe8H7R7")]
REDES_PT = [("Instagram", "https://www.instagram.com/wiqonbr/"), ("YouTube", "https://www.youtube.com/@wiqonbr"),
            ("TikTok", "https://www.tiktok.com/@wiqonbr"), ("X", "https://x.com/wiqonbr"), ("Telegram", "https://t.me/wiqonlab"),
            ("Discord", "https://discord.gg/8GDqe8H7R7"), ("Facebook", "https://www.facebook.com/wiqonlab/")]

BASE = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo} — WIQON</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index,follow">
<link rel="canonical" href="https://wiqonlab.com/{ruta}">
<link rel="icon" href="{r}assets/favicon.png">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}assets/v4.css">
<script>try{{var t=localStorage.getItem("wiqon-tema");if(t)document.documentElement.dataset.tema=t;}}catch(e){{}}</script>
<style>
  .legal-p {{ max-width: 780px; margin: 0 auto; padding: 48px 20px 80px; }}
  .legal-p h1 {{ font-size: 2rem; font-weight: 800; letter-spacing: -.02em; }}
  .legal-p h2 {{ font-size: 1.15rem; margin: 30px 0 8px; }}
  .legal-p p, .legal-p li, .legal-p td, .legal-p th {{ color: var(--suave); font-size: .95rem; line-height: 1.7; }}
  .legal-p ul, .legal-p ol {{ padding-left: 20px; }}
  .legal-p a {{ color: var(--cian); }}
  .legal-p .meta {{ margin-top: 6px; }}
  .legal-p table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
  .legal-p th, .legal-p td {{ text-align: left; padding: 8px 10px; border-bottom: 1px solid var(--borde); vertical-align: top; }}
  .legal-p .tit {{ border: 1px solid var(--borde); border-radius: 12px; padding: 14px 18px; margin: 18px 0; }}
  .legal-p .redes-l a {{ margin-right: 14px; display: inline-block; }}
  .form-c {{ display: grid; gap: 12px; margin-top: 14px; }}
  .form-c label {{ font-weight: 600; font-size: .9rem; }}
  .form-c input, .form-c textarea {{ width: 100%; box-sizing: border-box; padding: 12px 14px; border-radius: 10px; border: 1px solid var(--borde2); background: var(--fondo2); color: var(--texto); font: 1rem var(--sans); }}
  .form-c input:focus, .form-c textarea:focus {{ outline: 2px solid var(--cian); outline-offset: 1px; }}
  .form-c textarea {{ min-height: 150px; resize: vertical; }}
  .form-c .trampa {{ position: absolute; left: -9999px; width: 1px; height: 1px; overflow: hidden; }}
  .form-c .estado {{ min-height: 1.4em; font-weight: 600; }}
  .form-c .estado.ok {{ color: var(--sube); }}
  .form-c .estado.error {{ color: #e5484d; }}
  .pie-l {{ max-width: 780px; margin: 0 auto; padding: 0 20px 50px; font-size: .85rem; color: var(--gris); }}
  .pie-l a {{ color: var(--gris); margin-right: 14px; }}
</style>
</head>
<body>
<header class="nav"><div class="c"><a class="marca" href="{inicio}"><span class="corona s"><img src="{r}assets/logo.png" alt="" width="34" height="34"></span><span>WIQON</span></a>
<div class="nav-d"><a class="btn ch" href="{inicio}">{volver}</a></div></div></header>
<main class="legal-p">
{cuerpo}
</main>
<footer class="pie-l">{pie}</footer>
<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "c394b4ca4e5144b19a861d3203511d84"}}'></script>
</body>
</html>
"""


def enlaces(lista):
    return "".join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in lista)


# ============================================ ESPAÑOL ============================================
TITULAR_ES = f"""<div class="tit"><p><strong>Titular:</strong> {TITULAR} · Cédula de identidad (Paraguay) N.º {CI} · persona física que opera bajo el nombre comercial <strong>WIQON</strong>.<br>
<strong>Contacto:</strong> <a href="mailto:{EMAIL}">{EMAIL}</a> · WhatsApp <a href="{WA}" target="_blank" rel="noopener">{WA_TXT}</a> · <a href="../contacto/">formulario de contacto</a></p></div>"""

TERMINOS_ES = f"""<h1>Términos y condiciones</h1>
<p class="meta">Última actualización: {FECHA_ES}</p>
{TITULAR_ES}

<h2>1. Qué es WIQON</h2>
<p>WIQON (wiqonlab.com) es un laboratorio de investigación de trading y datos de mercado con base en Paraguay. Publicamos gratis nuestros experimentos, datos de mercado y guías, y vendemos un software para MetaTrader 5, un libro digital y servicios personalizados. Al comprar o usar el sitio aceptás estos términos.</p>

<h2>2. Productos y servicios</h2>
<table>
<tr><th>Producto o servicio</th><th>Tipo</th><th>Precio</th></tr>
<tr><td><strong>WIQON Shield</strong> · demo</td><td>Software (EA para MetaTrader 5), solo cuentas demo</td><td>Gratis</td></tr>
<tr><td><strong>WIQON Shield</strong> · licencia anual</td><td>Licencia de software por 12 meses</td><td>USD 59 (lanzamiento; precio regular USD 99)</td></tr>
<tr><td><strong>WIQON Shield</strong> · licencia vitalicia</td><td>Licencia de software sin vencimiento</td><td>USD 199</td></tr>
<tr><td><strong>Libro «¿Ventaja o suerte?»</strong></td><td>Libro digital en PDF (español, portugués o inglés)</td><td>USD 9,99</td></tr>
<tr><td><strong>Instalación asistida</strong></td><td>Servicio personalizado (unos 30 minutos)</td><td>USD 30</td></tr>
<tr><td><strong>Auditoría de estrategias</strong></td><td>Servicio personalizado con informe escrito</td><td>Diagnóstico inicial gratis · básica desde USD 80 · completa desde USD 200</td></tr>
</table>
<p>Los precios están en dólares estadounidenses. Si pagás por transferencia en Paraguay, el monto se calcula en guaraníes con el tipo de cambio oficial del Banco Central del Paraguay del día. Por ahora WIQON Shield no se vende a residentes en Brasil.</p>

<h2>3. Cómo se compra</h2>
<ol>
<li><strong>Elegís</strong> el producto en el sitio o escribiéndonos por WhatsApp. Un asistente automático te muestra opciones y precios; en cualquier momento podés pedir hablar con una persona.</li>
<li><strong>Pagás</strong> con el medio que prefieras: tarjeta de crédito o débito a través de procesadores de pago habilitados (por ejemplo Hotmart para el libro), Binance Pay o USDT (red TRC20), PYUSD (red Solana) o transferencia bancaria SIPAP en Paraguay.</li>
<li><strong>Nos enviás el comprobante</strong> (no hace falta en pagos con tarjeta). Verificamos cada pago manualmente.</li>
<li><strong>Recibís el producto</strong> en los plazos de la <a href="../devoluciones/">política de entregas y devoluciones</a>. Para la licencia de Shield te pedimos el número de tu cuenta real de MetaTrader 5, porque la licencia queda atada a esa cuenta.</li>
</ol>

<h2>4. Licencia de WIQON Shield</h2>
<ul>
<li>La licencia es personal, no exclusiva e intransferible, y funciona en la cuenta de MetaTrader 5 que nos indicaste. La anual dura 12 meses desde la entrega; la vitalicia no vence.</li>
<li>No está permitido revender, compartir, publicar ni descompilar el software o la clave.</li>
<li>Si cambiás de cuenta o de broker, te generamos una clave nueva gratis una vez por año.</li>
<li>La demo es el mismo programa, gratis y sin límite de tiempo en cuentas demo, para que lo pruebes antes de comprar.</li>
</ul>

<h2>5. Servicios personalizados</h2>
<p><strong>Instalación asistida.</strong> Coordinamos día y horario por WhatsApp. Por videollamada o acceso remoto, con tu autorización y en tu presencia, instalamos y configuramos el EA en tu MetaTrader 5 con la licencia activa y te explicamos cómo leerlo. Necesitás una computadora con Windows (o MetaTrader 5 funcionando) y tu cuenta del bróker.</p>
<p><strong>Auditoría de estrategias.</strong></p>
<ol>
<li>Diagnóstico inicial gratis de 20 a 30 minutos para entender tu estrategia o bot.</li>
<li>Te enviamos por escrito el alcance, el precio y el plazo. Solo pagás si aceptás la propuesta.</li>
<li>Nos compartís las reglas, el código o el historial de operaciones necesarios.</li>
<li>Entregamos un informe con la metodología (costos reales, pruebas fuera de muestra, robustez de parámetros) y la conclusión. El resultado puede ser que la estrategia no tenga ventaja: te lo decimos igual.</li>
</ol>
<p>Tratamos tu estrategia y tus datos como confidenciales y no los publicamos sin tu permiso por escrito.</p>
<p><strong>Seguridad:</strong> nunca te pedimos contraseñas de tu banco o exchange ni claves de API con permiso de retiro.</p>

<h2>6. Riesgo y responsabilidad</h2>
<ul>
<li>Todo el contenido, el software y los servicios son informativos y educativos: no son asesoría financiera ni recomendaciones de inversión.</li>
<li>WIQON no administra dinero de terceros, no recibe fondos para invertir y no vende señales de compra o venta.</li>
<li>Operar en mercados financieros implica riesgo de pérdida. Los resultados pasados, incluidos los nuestros, no garantizan resultados futuros. Las decisiones de operar son de cada usuario.</li>
<li>Nuestra responsabilidad máxima frente a un cliente se limita al monto que pagó por el producto o servicio en cuestión.</li>
</ul>

<h2>7. Propiedad intelectual</h2>
<p>La marca WIQON, los textos, el libro, el software WIQON Shield y los diseños del sitio pertenecen al titular. El código del laboratorio publicado en <a href="https://github.com/wiqon/wiqon-lab" target="_blank" rel="noopener">GitHub</a> se rige por la licencia indicada en ese repositorio.</p>

<h2>8. Privacidad</h2>
<p>El tratamiento de tus datos se explica en la <a href="../privacidad/">política de privacidad</a>.</p>

<h2>9. Cambios y ley aplicable</h2>
<p>Podemos actualizar estos términos; la versión vigente es la publicada en esta página con su fecha. Las compras ya hechas se rigen por los términos vigentes al momento de la compra. Se aplican las leyes de la República del Paraguay, sin perjuicio de los derechos que te otorga la Ley N.º 1334/98 de Defensa del Consumidor y del Usuario. Ante cualquier reclamo, escribinos primero a <a href="mailto:{EMAIL}">{EMAIL}</a>: respondemos en un máximo de 48 horas hábiles.</p>
"""

DEVOLUCIONES_ES = f"""<h1>Política de entregas y devoluciones</h1>
<p class="meta">Última actualización: {FECHA_ES}</p>
{TITULAR_ES}

<h2>1. Entregas</h2>
<p>Todos nuestros productos son digitales: no hacemos envíos físicos ni cobramos costos de envío.</p>
<table>
<tr><th>Producto</th><th>Cómo se entrega</th><th>Plazo</th></tr>
<tr><td>Libro «¿Ventaja o suerte?» con tarjeta (Hotmart)</td><td>Hotmart te envía el PDF por correo</td><td>Inmediato, automático</td></tr>
<tr><td>Libro con cripto o transferencia</td><td>PDF por WhatsApp</td><td>Menos de 1 hora en horario comercial de Paraguay; máximo 24 horas hábiles desde que verificamos el pago</td></tr>
<tr><td>Licencia de WIQON Shield</td><td>Enlace de descarga (EA + manual) y clave de licencia por WhatsApp</td><td>Menos de 1 hora en horario comercial; máximo 24 horas hábiles desde que verificamos el pago y recibimos tu número de cuenta MT5</td></tr>
<tr><td>Instalación asistida</td><td>Videollamada o acceso remoto</td><td>En el día y horario que acordamos</td></tr>
<tr><td>Auditoría de estrategias</td><td>Informe escrito por correo o WhatsApp</td><td>En el plazo indicado en la propuesta aceptada</td></tr>
</table>
<p>Si no recibiste tu compra en esos plazos, escribinos a <a href="mailto:{EMAIL}">{EMAIL}</a> o por WhatsApp al {WA_TXT}.</p>

<h2>2. Devoluciones y reembolsos</h2>
<p>Los reclamos se hacen dentro de los <strong>7 días corridos</strong> desde la entrega.</p>
<p><strong>Libro digital.</strong> Reembolso total si el archivo no abre o está incompleto y no podemos enviarte uno correcto, o si se te cobró dos veces. En compras hechas por Hotmart también rige la garantía de Hotmart, que se pide desde tu cuenta de Hotmart dentro del plazo que figura allí.</p>
<p><strong>Licencia de WIQON Shield.</strong> Como la demo es el mismo programa, gratis y sin límite de tiempo, no hay reembolso por arrepentimiento una vez entregada la clave. Sí hay reembolso total si:</p>
<ul>
<li>la licencia no funciona en la cuenta que indicaste y no lo solucionamos dentro de los 7 días desde tu reclamo;</li>
<li>se te cobró dos veces; o</li>
<li>pagaste y todavía no te entregamos la clave (podés cancelar antes de la entrega).</li>
</ul>
<p>Al reembolsarse una licencia, la clave queda anulada y no debe seguir usándose.</p>
<p><strong>Instalación asistida.</strong> Reembolso total si no se realizó, o si por causas nuestras no logramos dejar el EA funcionando. Podés reprogramar el horario avisando con anticipación.</p>
<p><strong>Auditoría de estrategias.</strong> Reembolso total si cancelás antes de que empecemos el trabajo. Si cancelás una vez iniciado, devolvemos la parte no realizada según la propuesta aceptada.</p>

<h2>3. Cómo pedir un reembolso</h2>
<ol>
<li>Escribinos a <a href="mailto:{EMAIL}">{EMAIL}</a> o por WhatsApp al {WA_TXT} con tu nombre, el producto, la fecha y el comprobante de pago.</li>
<li>Respondemos en un máximo de 48 horas hábiles.</li>
<li>Si corresponde, devolvemos el dinero por el mismo medio de pago en un máximo de 10 días hábiles: a la tarjeta (los tiempos de acreditación dependen de tu banco), a la misma billetera y en la misma moneda en pagos con cripto, o a tu cuenta bancaria en transferencias.</li>
</ol>
<p>Estas condiciones no limitan los derechos que te otorga la Ley N.º 1334/98 de Defensa del Consumidor y del Usuario del Paraguay. Ver también los <a href="../terminos/">términos y condiciones</a>.</p>
"""


def formulario(t):
    return f"""<form class="form-c" id="form-c" novalidate>
  <label for="fc-nombre">{t['nombre']}</label>
  <input id="fc-nombre" name="nombre" autocomplete="name" required maxlength="120">
  <label for="fc-email">{t['email']}</label>
  <input id="fc-email" name="email" type="email" autocomplete="email" required maxlength="200">
  <label for="fc-mensaje">{t['mensaje']}</label>
  <textarea id="fc-mensaje" name="mensaje" required maxlength="5000"></textarea>
  <div class="trampa" aria-hidden="true"><label for="fc-web">Web</label><input id="fc-web" name="web" tabindex="-1" autocomplete="off"></div>
  <p class="meta">{t['aviso']}</p>
  <button class="btn p" type="submit">{t['enviar']}</button>
  <p class="estado" id="fc-estado" role="status" aria-live="polite"></p>
</form>
<script>
(function () {{
  var f = document.getElementById('form-c'), e = document.getElementById('fc-estado'), inicio = Date.now();
  f.addEventListener('submit', function (ev) {{
    ev.preventDefault();
    var d = new FormData(f), nombre = (d.get('nombre') || '').trim(), email = (d.get('email') || '').trim(), mensaje = (d.get('mensaje') || '').trim();
    e.className = 'estado error';
    if (!nombre || !mensaje || !/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email)) {{ e.textContent = {t['falta']!r}; return; }}
    var b = f.querySelector('button'); b.disabled = true; e.className = 'estado'; e.textContent = {t['enviando']!r};
    var datos = new URLSearchParams({{ nombre: nombre, email: email, mensaje: mensaje, web: d.get('web') || '', segundos: String(Math.round((Date.now() - inicio) / 1000)), idioma: {t['idioma']!r}, pagina: location.pathname }});
    fetch({FORM_URL!r}, {{ method: 'POST', body: datos }})
      .then(function (r) {{ if (!r.ok) throw new Error(r.status); e.className = 'estado ok'; e.textContent = {t['ok']!r}; f.reset(); }})
      .catch(function () {{ e.className = 'estado error'; e.textContent = {t['error']!r}; }})
      .finally(function () {{ b.disabled = false; }});
  }});
}})();
</script>"""


FORM_ES = dict(nombre="Nombre", email="Correo electrónico", mensaje="Mensaje", enviar="Enviar mensaje", idioma="es",
               aviso='Usamos tus datos solo para responderte (ver <a href="../privacidad/">política de privacidad</a>).',
               falta="Completá tu nombre, un correo válido y el mensaje.", enviando="Enviando…",
               ok="¡Mensaje enviado! Te respondemos por correo, normalmente en menos de 24 horas hábiles.",
               error=f"No se pudo enviar. Probá de nuevo o escribinos a {EMAIL}.")

CONTACTO_ES = f"""<h1>Contacto</h1>
<p>Escribinos por el canal que prefieras. Respondemos personalmente, normalmente en menos de 24 horas hábiles (horario de Paraguay).</p>
<table>
<tr><th>Correo</th><td><a href="mailto:{EMAIL}">{EMAIL}</a></td></tr>
<tr><th>WhatsApp</th><td><a href="{WA}?text=Hola%20WIQON" target="_blank" rel="noopener">{WA_TXT}</a></td></tr>
<tr><th>Redes</th><td class="redes-l">{enlaces(REDES_ES)}</td></tr>
<tr><th>Ubicación</th><td>Paraguay (Asunción · Ciudad del Este)</td></tr>
</table>
<h2>Formulario de contacto</h2>
{formulario(FORM_ES)}
{TITULAR_ES}
"""

# ============================================ PORTUGUÊS ============================================
TITULAR_PT = f"""<div class="tit"><p><strong>Titular:</strong> {TITULAR} · Cédula de identidade paraguaia n.º {CI} · pessoa física que atua com o nome comercial <strong>WIQON</strong> (Paraguai).<br>
<strong>Contato:</strong> <a href="mailto:{EMAIL}">{EMAIL}</a> · WhatsApp <a href="{WA}" target="_blank" rel="noopener">{WA_TXT}</a> · <a href="../contato/">formulário de contato</a></p></div>"""

TERMOS_PT = f"""<h1>Termos e condições</h1>
<p class="meta">Última atualização: {FECHA_PT}</p>
{TITULAR_PT}

<h2>1. O que é a WIQON</h2>
<p>A WIQON (wiqonlab.com) é um laboratório de pesquisa de trading e dados de mercado com base no Paraguai. Publicamos de graça nossos experimentos, dados de mercado e guias, e vendemos um software para MetaTrader 5, um livro digital e serviços personalizados. Ao comprar ou usar o site, você aceita estes termos.</p>

<h2>2. Produtos e serviços</h2>
<table>
<tr><th>Produto ou serviço</th><th>Tipo</th><th>Preço</th></tr>
<tr><td><strong>WIQON Shield</strong> · demo</td><td>Software (EA para MetaTrader 5), só contas demo</td><td>Grátis</td></tr>
<tr><td><strong>WIQON Shield</strong> · licença anual</td><td>Licença de software por 12 meses</td><td>USD 59 (lançamento; preço normal USD 99)</td></tr>
<tr><td><strong>WIQON Shield</strong> · licença vitalícia</td><td>Licença de software sem vencimento</td><td>USD 199</td></tr>
<tr><td><strong>Livro «Vantagem ou sorte?»</strong></td><td>Livro digital em PDF (português, espanhol ou inglês)</td><td>USD 9,99 · R$ 49,90 na Hotmart</td></tr>
<tr><td><strong>Instalação assistida</strong></td><td>Serviço personalizado (cerca de 30 minutos)</td><td>USD 30</td></tr>
<tr><td><strong>Auditoria de estratégias</strong></td><td>Serviço personalizado com relatório escrito</td><td>Diagnóstico inicial grátis · básica a partir de USD 80 · completa a partir de USD 200</td></tr>
</table>
<p>Os preços estão em dólares americanos (o livro na Hotmart Brasil, em reais). <strong>No momento, o WIQON Shield não é vendido a residentes no Brasil</strong>: a demo continua gratuita.</p>

<h2>3. Como comprar</h2>
<ol>
<li><strong>Escolha</strong> o produto no site ou escrevendo pelo WhatsApp. Um assistente automático mostra opções e preços; a qualquer momento você pode pedir para falar com uma pessoa.</li>
<li><strong>Pague</strong> com o meio que preferir: cartão de crédito ou débito por processadores de pagamento habilitados (por exemplo, Hotmart para o livro, com PIX), Binance Pay ou USDT (rede TRC20), PYUSD (rede Solana) ou transferência SIPAP no Paraguai.</li>
<li><strong>Envie o comprovante</strong> (não precisa em pagamentos com cartão). Verificamos cada pagamento manualmente.</li>
<li><strong>Receba o produto</strong> nos prazos da <a href="../devolucoes/">política de entregas e devoluções</a>.</li>
</ol>

<h2>4. Licença do WIQON Shield</h2>
<ul>
<li>A licença é pessoal, não exclusiva e intransferível, e funciona na conta de MetaTrader 5 informada. A anual vale 12 meses a partir da entrega; a vitalícia não vence.</li>
<li>Não é permitido revender, compartilhar, publicar ou descompilar o software ou a chave.</li>
<li>Se você trocar de conta ou de corretora, geramos uma chave nova grátis uma vez por ano.</li>
<li>A demo é o mesmo programa, grátis e sem limite de tempo em contas demo, para você testar antes de comprar.</li>
</ul>

<h2>5. Serviços personalizados</h2>
<p><strong>Instalação assistida.</strong> Combinamos dia e horário pelo WhatsApp. Por videochamada ou acesso remoto, com sua autorização e na sua presença, instalamos e configuramos o EA no seu MetaTrader 5 com a licença ativa e explicamos como interpretá-lo.</p>
<p><strong>Auditoria de estratégias.</strong> 1) Diagnóstico inicial grátis de 20 a 30 minutos. 2) Enviamos por escrito o escopo, o preço e o prazo; você só paga se aceitar. 3) Você compartilha as regras, o código ou o histórico necessários. 4) Entregamos um relatório com a metodologia e a conclusão, mesmo que a conclusão seja que a estratégia não tem vantagem. Tratamos sua estratégia como confidencial.</p>
<p><strong>Segurança:</strong> nunca pedimos senhas do seu banco ou exchange nem chaves de API com permissão de saque.</p>

<h2>6. Risco e responsabilidade</h2>
<ul>
<li>Todo o conteúdo, o software e os serviços são informativos e educacionais: não são recomendação de investimento.</li>
<li>A WIQON não administra dinheiro de terceiros, não recebe recursos para investir e não vende sinais.</li>
<li>Operar no mercado financeiro envolve risco de perda. Resultados passados não garantem resultados futuros. As decisões de operar são de cada usuário.</li>
<li>Nossa responsabilidade máxima se limita ao valor pago pelo produto ou serviço em questão.</li>
</ul>

<h2>7. Propriedade intelectual e privacidade</h2>
<p>A marca WIQON, os textos, o livro, o software e os designs do site pertencem ao titular. O código do laboratório no <a href="https://github.com/wiqon/wiqon-lab" target="_blank" rel="noopener">GitHub</a> segue a licença indicada no repositório. O tratamento dos seus dados está na <a href="../privacidade/">política de privacidade</a>.</p>

<h2>8. Alterações e lei aplicável</h2>
<p>Podemos atualizar estes termos; vale a versão publicada nesta página com sua data. Aplicam-se as leis da República do Paraguai, sem prejuízo dos direitos do consumidor que se apliquem a você. Para qualquer reclamação, escreva primeiro para <a href="mailto:{EMAIL}">{EMAIL}</a>: respondemos em até 48 horas úteis.</p>
"""

DEVOLUCOES_PT = f"""<h1>Política de entregas e devoluções</h1>
<p class="meta">Última atualização: {FECHA_PT}</p>
{TITULAR_PT}

<h2>1. Entregas</h2>
<p>Todos os nossos produtos são digitais: não fazemos envios físicos nem cobramos frete.</p>
<table>
<tr><th>Produto</th><th>Como é entregue</th><th>Prazo</th></tr>
<tr><td>Livro «Vantagem ou sorte?» na Hotmart (cartão ou PIX)</td><td>A Hotmart envia o PDF por e-mail</td><td>Imediato, automático</td></tr>
<tr><td>Livro com cripto ou transferência</td><td>PDF pelo WhatsApp</td><td>Menos de 1 hora em horário comercial; no máximo 24 horas úteis após verificarmos o pagamento</td></tr>
<tr><td>Licença do WIQON Shield (fora do Brasil)</td><td>Link de download e chave de licença pelo WhatsApp</td><td>No máximo 24 horas úteis após verificarmos o pagamento e recebermos o número da conta MT5</td></tr>
<tr><td>Instalação assistida</td><td>Videochamada ou acesso remoto</td><td>No dia e horário combinados</td></tr>
<tr><td>Auditoria de estratégias</td><td>Relatório escrito</td><td>No prazo da proposta aceita</td></tr>
</table>

<h2>2. Devoluções e reembolsos</h2>
<p>As solicitações devem ser feitas em até <strong>7 dias corridos</strong> após a entrega.</p>
<p><strong>Livro digital.</strong> Reembolso total se o arquivo não abrir ou estiver incompleto e não conseguirmos enviar um correto, ou em caso de cobrança duplicada. Nas compras pela Hotmart também vale a garantia da Hotmart, solicitada na sua conta Hotmart dentro do prazo indicado lá.</p>
<p><strong>Licença do WIQON Shield.</strong> Como a demo é o mesmo programa, grátis e sem limite de tempo, não há reembolso por arrependimento após a entrega da chave. Há reembolso total se a licença não funcionar na conta informada e não resolvermos em até 7 dias da sua reclamação, se houver cobrança duplicada, ou se você pagou e ainda não recebeu a chave. Ao reembolsar uma licença, a chave fica anulada.</p>
<p><strong>Instalação assistida.</strong> Reembolso total se não for realizada ou se, por causas nossas, o EA não ficar funcionando.</p>
<p><strong>Auditoria.</strong> Reembolso total se você cancelar antes de começarmos; depois de iniciada, devolvemos a parte não realizada conforme a proposta.</p>

<h2>3. Como pedir um reembolso</h2>
<p>Escreva para <a href="mailto:{EMAIL}">{EMAIL}</a> ou pelo WhatsApp {WA_TXT} com seu nome, o produto, a data e o comprovante. Respondemos em até 48 horas úteis e, se cabível, devolvemos pelo mesmo meio de pagamento em até 10 dias úteis. Veja também os <a href="../termos/">termos e condições</a>.</p>
"""

FORM_PT = dict(nombre="Nome", email="E-mail", mensaje="Mensagem", enviar="Enviar mensagem", idioma="pt",
               aviso='Usamos seus dados só para responder (veja a <a href="../privacidade/">política de privacidade</a>).',
               falta="Preencha seu nome, um e-mail válido e a mensagem.", enviando="Enviando…",
               ok="Mensagem enviada! Respondemos por e-mail, normalmente em menos de 24 horas úteis.",
               error=f"Não foi possível enviar. Tente de novo ou escreva para {EMAIL}.")

CONTATO_PT = f"""<h1>Contato</h1>
<p>Fale com a gente pelo canal que preferir. Respondemos pessoalmente, normalmente em menos de 24 horas úteis.</p>
<table>
<tr><th>E-mail</th><td><a href="mailto:{EMAIL}">{EMAIL}</a></td></tr>
<tr><th>WhatsApp</th><td><a href="{WA}?text=Ol%C3%A1%20WIQON" target="_blank" rel="noopener">{WA_TXT}</a></td></tr>
<tr><th>Redes</th><td class="redes-l">{enlaces(REDES_PT)}</td></tr>
<tr><th>Localização</th><td>Paraguai (Ciudad del Este · Assunção), na fronteira com Foz do Iguaçu</td></tr>
</table>
<h2>Formulário de contato</h2>
{formulario(FORM_PT)}
{TITULAR_PT}
"""

# ============================================ ENGLISH ============================================
FECHA_EN = "October 17, 2026"
REDES_EN = REDES_ES
TITULAR_EN = f"""<div class="tit"><p><strong>Owner:</strong> {TITULAR} · Paraguayan identity card No. {CI} · individual (sole proprietor) trading as <strong>WIQON</strong> (Paraguay).<br>
<strong>Contact:</strong> <a href="mailto:{EMAIL}">{EMAIL}</a> · WhatsApp <a href="{WA}" target="_blank" rel="noopener">{WA_TXT}</a> · <a href="../contact/">contact form</a></p></div>"""

TERMS_EN = f"""<h1>Terms and conditions</h1>
<p class="meta">Last updated: {FECHA_EN}</p>
{TITULAR_EN}

<h2>1. What WIQON is</h2>
<p>WIQON (wiqonlab.com) is a trading research and market data lab based in Paraguay. We publish our experiments, market data and guides for free, and we sell software for MetaTrader 5, a digital book and personalized services. By buying or using the site you accept these terms.</p>

<h2>2. Products and services</h2>
<table>
<tr><th>Product or service</th><th>Type</th><th>Price</th></tr>
<tr><td><strong>WIQON Shield</strong> · demo</td><td>Software (EA for MetaTrader 5), demo accounts only</td><td>Free</td></tr>
<tr><td><strong>WIQON Shield</strong> · annual license</td><td>12-month software license</td><td>USD 59 (launch price; regular price USD 99)</td></tr>
<tr><td><strong>WIQON Shield</strong> · lifetime license</td><td>Software license with no expiry</td><td>USD 199</td></tr>
<tr><td><strong>Book "Edge or Luck?"</strong></td><td>Digital book in PDF (English, Spanish or Portuguese)</td><td>USD 9.99</td></tr>
<tr><td><strong>Assisted installation</strong></td><td>Personalized service (about 30 minutes)</td><td>USD 30</td></tr>
<tr><td><strong>Strategy audit</strong></td><td>Personalized service with a written report</td><td>Free initial diagnosis · basic from USD 80 · full from USD 200</td></tr>
</table>
<p>Prices are in US dollars. For now, WIQON Shield is not sold to residents of Brazil (the demo remains free).</p>

<h2>3. How to buy</h2>
<ol>
<li><strong>Choose</strong> the product on the site or by messaging us on WhatsApp. An automatic assistant shows you options and prices; you can ask to talk to a person at any time.</li>
<li><strong>Pay</strong> with the method you prefer: credit or debit card through enabled payment processors (for example Hotmart for the book, or Amazon Kindle), Binance Pay or USDT (TRC20 network), PYUSD (Solana network) or SIPAP bank transfer in Paraguay.</li>
<li><strong>Send us the receipt</strong> (not needed for card payments). We verify every payment manually.</li>
<li><strong>Receive the product</strong> within the times in the <a href="../refunds/">delivery and refund policy</a>. For a Shield license we ask for your real MetaTrader 5 account number, because the license is tied to that account.</li>
</ol>

<h2>4. WIQON Shield license</h2>
<ul>
<li>The license is personal, non-exclusive and non-transferable, and works on the MetaTrader 5 account you gave us. The annual license lasts 12 months from delivery; the lifetime license does not expire.</li>
<li>You may not resell, share, publish or decompile the software or the key.</li>
<li>If you change account or broker, we generate a new key for free once a year.</li>
<li>The demo is the same program, free and with no time limit on demo accounts, so you can try it before buying.</li>
</ul>

<h2>5. Personalized services</h2>
<p><strong>Assisted installation.</strong> We agree on a day and time via WhatsApp. Over a video call or remote access, with your authorization and in your presence, we install and configure the EA in your MetaTrader 5 with the license active and explain how to read it.</p>
<p><strong>Strategy audit.</strong> 1) Free 20-30 minute initial diagnosis to understand your strategy or bot. 2) We send you the scope, price and timeline in writing; you only pay if you accept. 3) You share the rules, code or trade history needed. 4) We deliver a report with the methodology (real costs, out-of-sample tests, parameter robustness) and the conclusion, even if the conclusion is that the strategy has no edge. We treat your strategy and data as confidential.</p>
<p><strong>Security:</strong> we never ask for your bank or exchange passwords, or for API keys with withdrawal permission.</p>

<h2>6. Risk and liability</h2>
<ul>
<li>All content, software and services are informational and educational: they are not financial advice or investment recommendations.</li>
<li>WIQON does not manage third-party money, does not receive funds to invest and does not sell buy or sell signals.</li>
<li>Trading financial markets involves risk of loss. Past results, including ours, do not guarantee future results. Trading decisions are each user's own.</li>
<li>Our maximum liability to a customer is limited to the amount paid for the product or service in question.</li>
</ul>

<h2>7. Intellectual property and privacy</h2>
<p>The WIQON brand, texts, book, WIQON Shield software and site designs belong to the owner. The lab code published on <a href="https://github.com/wiqon/wiqon-lab" target="_blank" rel="noopener">GitHub</a> is governed by the license stated in that repository. How we handle your data is explained in the <a href="../privacy/">privacy policy</a>.</p>

<h2>8. Changes and governing law</h2>
<p>We may update these terms; the version in force is the one published on this page with its date. Purchases already made are governed by the terms in force at the time of purchase. The laws of the Republic of Paraguay apply, without prejudice to any consumer rights that apply to you. For any claim, please write to <a href="mailto:{EMAIL}">{EMAIL}</a> first: we reply within 48 business hours. This English version is a translation; the <a href="../../terminos/">Spanish version</a> prevails in case of discrepancy.</p>
"""

REFUNDS_EN = f"""<h1>Delivery and refund policy</h1>
<p class="meta">Last updated: {FECHA_EN}</p>
{TITULAR_EN}

<h2>1. Delivery</h2>
<p>All our products are digital: we don't ship physical items or charge shipping.</p>
<table>
<tr><th>Product</th><th>How it is delivered</th><th>Time</th></tr>
<tr><td>Book "Edge or Luck?" by card (Hotmart)</td><td>Hotmart emails you the PDF</td><td>Immediate, automatic</td></tr>
<tr><td>Book on Amazon (Kindle)</td><td>Amazon delivers it to your Kindle account</td><td>Immediate, under Amazon's terms</td></tr>
<tr><td>Book paid with crypto or bank transfer</td><td>PDF via WhatsApp</td><td>Under 1 hour during Paraguay business hours; at most 24 business hours after we verify the payment</td></tr>
<tr><td>WIQON Shield license</td><td>Download link (EA + manual) and license key via WhatsApp</td><td>At most 24 business hours after we verify the payment and receive your MT5 account number</td></tr>
<tr><td>Assisted installation</td><td>Video call or remote access</td><td>On the agreed day and time</td></tr>
<tr><td>Strategy audit</td><td>Written report by email or WhatsApp</td><td>Within the timeline in the accepted proposal</td></tr>
</table>
<p>If you haven't received your purchase within those times, write to <a href="mailto:{EMAIL}">{EMAIL}</a> or WhatsApp {WA_TXT}.</p>

<h2>2. Returns and refunds</h2>
<p>Requests must be made within <strong>7 calendar days</strong> of delivery.</p>
<p><strong>Digital book.</strong> Full refund if the file doesn't open or is incomplete and we can't send you a correct one, or if you were charged twice. Purchases made on Hotmart are also covered by Hotmart's guarantee, requested from your Hotmart account within the period shown there; Amazon purchases follow Amazon's return policy.</p>
<p><strong>WIQON Shield license.</strong> Since the demo is the same program, free and with no time limit, there are no change-of-mind refunds once the key has been delivered. You do get a full refund if the license doesn't work on the account you gave us and we don't fix it within 7 days of your claim, if you were charged twice, or if you paid and haven't received the key yet (you can cancel before delivery). When a license is refunded, the key is void and must not be used.</p>
<p><strong>Assisted installation.</strong> Full refund if it wasn't carried out, or if for reasons on our side the EA isn't left working. You can reschedule with notice.</p>
<p><strong>Strategy audit.</strong> Full refund if you cancel before we start. If you cancel once work has begun, we refund the part not done according to the accepted proposal.</p>

<h2>3. How to request a refund</h2>
<p>Write to <a href="mailto:{EMAIL}">{EMAIL}</a> or WhatsApp {WA_TXT} with your name, the product, the date and the payment receipt. We reply within 48 business hours and, where applicable, refund through the same payment method within 10 business days. See also the <a href="../terms/">terms and conditions</a>.</p>
"""

PRIVACY_EN = f"""<h1>Privacy policy</h1>
<p class="meta">Last updated: {FECHA_EN}</p>

<h2>1. Who we are</h2>
<p>WIQON (wiqonlab.com) is a market research and software lab based in Paraguay. Data controller: {TITULAR}, on behalf of WIQON. Contact for any privacy matter: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>

<h2>2. What data we keep</h2>
<ul>
<li><strong>If you create an account:</strong> your email, the date you accepted this policy, the page language and whether you agreed to receive news. The authentication service also records the creation date and last sign-in.</li>
<li><strong>We don't ask</strong> for your name, ID, phone, bank details or passwords.</li>
<li><strong>If you write to us</strong> by email, WhatsApp or the contact form, we keep that conversation to answer you.</li>
</ul>

<h2>3. What we use it for</h2>
<ul>
<li>Giving you access to the sections for registered users (legal basis: performing the service you requested).</li>
<li>Sending you WIQON news, only if you ticked that box (legal basis: your consent, which you can withdraw at any time).</li>
<li>We don't sell or rent your data, and we don't use it for third-party advertising.</li>
</ul>

<h2>4. Who processes the data</h2>
<ul>
<li><strong>Supabase</strong> hosts the accounts and sends the sign-in links, as a data processor.</li>
<li><strong>GitHub Pages</strong> and <strong>Cloudflare</strong> serve the site and the domain.</li>
<li>These providers may process data outside Paraguay or Brazil, with their own security measures.</li>
</ul>

<h2>5. Third-party services on the site</h2>
<ul>
<li>Interactive charts and market tables are provided by <strong>TradingView</strong> and load when you reach those sections.</li>
<li><strong>YouTube</strong> videos load only if you press play (privacy-enhanced mode).</li>
<li>Live prices come from <strong>Binance</strong>'s public servers; fonts from <strong>Google Fonts</strong>.</li>
<li>When that content loads, your browser connects to those services, which have their own policies.</li>
</ul>

<h2>6. Storage in your browser</h2>
<p>We don't use cookies. To know how many people visit the site we use <strong>Cloudflare Web Analytics</strong>, which uses no cookies and keeps no data that identifies you (it counts visits, pages and country in aggregate). We store in your browser (local storage) only your session, the light or dark theme and whether you're signed in, so the page works.</p>

<h2>7. How long</h2>
<p>For as long as your account exists. If you ask us to delete it, we erase your data within 15 days, except what the law requires us to keep.</p>

<h2>8. Your rights</h2>
<p>You can ask at any time for access to your data, correction, account deletion, portability, or to withdraw your consent to receive news. If you are in Brazil, these rights are provided by the General Data Protection Law (LGPD, Law 13,709/2018). Write to <a href="mailto:{EMAIL}">{EMAIL}</a> from your account's email and we reply within 15 days.</p>

<h2>9. Minors</h2>
<p>Accounts are for people over 18. If we detect an account belonging to a minor, we delete it.</p>

<h2>10. Changes</h2>
<p>If we change this policy, we update the date above and, if the change is significant, we notify registered users.</p>
"""

FORM_EN = dict(nombre="Name", email="Email", mensaje="Message", enviar="Send message", idioma="en",
               aviso='We use your data only to reply to you (see the <a href="../privacy/">privacy policy</a>).',
               falta="Please enter your name, a valid email and your message.", enviando="Sending…",
               ok="Message sent! We'll reply by email, usually within 24 business hours.",
               error=f"We couldn't send it. Please try again or write to {EMAIL}.")

CONTACT_EN = f"""<h1>Contact</h1>
<p>Reach us through whichever channel you prefer. We reply personally, usually within 24 business hours (Paraguay time).</p>
<table>
<tr><th>Email</th><td><a href="mailto:{EMAIL}">{EMAIL}</a></td></tr>
<tr><th>WhatsApp</th><td><a href="{WA}?text=Hi%20WIQON" target="_blank" rel="noopener">{WA_TXT}</a></td></tr>
<tr><th>Social</th><td class="redes-l">{enlaces(REDES_EN)}</td></tr>
<tr><th>Location</th><td>Paraguay (Asunción · Ciudad del Este)</td></tr>
</table>
<h2>Contact form</h2>
{formulario(FORM_EN)}
{TITULAR_EN}
"""


def pie(lang):
    if lang == "es":
        return (f'<a href="../terminos/">Términos y condiciones</a><a href="../devoluciones/">Entregas y devoluciones</a>'
                f'<a href="../privacidad/">Privacidad</a><a href="../contacto/">Contacto</a><br>© 2026 WIQON · {TITULAR} · C.I. {CI} · Paraguay')
    if lang == "en":
        return (f'<a href="../terms/">Terms and conditions</a><a href="../refunds/">Delivery and refunds</a>'
                f'<a href="../privacy/">Privacy</a><a href="../contact/">Contact</a><br>© 2026 WIQON · {TITULAR} · ID {CI} · Paraguay')
    return (f'<a href="../termos/">Termos e condições</a><a href="../devolucoes/">Entregas e devoluções</a>'
            f'<a href="../privacidade/">Privacidade</a><a href="../contato/">Contato</a><br>© 2026 WIQON · {TITULAR} · C.I. {CI} · Paraguai')


PAGINAS = [
    ("terminos", "es", "Términos y condiciones", "Términos y condiciones de WIQON: productos, cómo se compra, licencias y servicios personalizados.", TERMINOS_ES),
    ("devoluciones", "es", "Política de entregas y devoluciones", "Cómo y cuándo se entregan los productos digitales de WIQON y cuándo corresponde un reembolso.", DEVOLUCIONES_ES),
    ("contacto", "es", "Contacto", "Contacto de WIQON: correo, WhatsApp, redes y formulario.", CONTACTO_ES),
    ("br/termos", "pt", "Termos e condições", "Termos e condições da WIQON: produtos, como comprar, licenças e serviços.", TERMOS_PT),
    ("br/devolucoes", "pt", "Política de entregas e devoluções", "Como e quando os produtos digitais da WIQON são entregues e quando cabe reembolso.", DEVOLUCOES_PT),
    ("br/contato", "pt", "Contato", "Contato da WIQON: e-mail, WhatsApp, redes e formulário.", CONTATO_PT),
    ("en/terms", "en", "Terms and conditions", "WIQON terms and conditions: products, how to buy, licenses and personalized services.", TERMS_EN),
    ("en/refunds", "en", "Delivery and refund policy", "How and when WIQON digital products are delivered and when a refund applies.", REFUNDS_EN),
    ("en/privacy", "en", "Privacy policy", "How WIQON handles your data.", PRIVACY_EN),
    ("en/contact", "en", "Contact", "Contact WIQON: email, WhatsApp, social media and form.", CONTACT_EN),
]

if __name__ == "__main__":
    for ruta, lang, titulo, desc, cuerpo in PAGINAS:
        r = "../" * (ruta.count("/") + 1)
        destino = RAIZ / ruta / "index.html"
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(BASE.format(lang={"es": "es", "pt": "pt-BR", "en": "en"}[lang], titulo=titulo, desc=desc, ruta=ruta + "/", r=r,
                                       inicio="../" if lang == "es" else "../", volver={"es": "Volver a WIQON", "pt": "Voltar para a WIQON", "en": "Back to WIQON"}[lang],
                                       cuerpo=cuerpo, pie=pie(lang)), encoding="utf-8")
        print("ok", destino.relative_to(RAIZ))
