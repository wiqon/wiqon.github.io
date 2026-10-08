"""
Genera la política de privacidad: privacidad/index.html (español) y br/privacidade/index.html (português).
Uso:  python scripts/construir_privacidad.py
"""
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FECHA_ES, FECHA_PT = "7 de octubre de 2026", "7 de outubro de 2026"

BASE = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo} — WIQON</title>
<meta name="robots" content="index,follow">
<link rel="icon" href="{r}assets/favicon.png">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}assets/v4.css">
<script>try{{var t=localStorage.getItem("wiqon-tema");if(t)document.documentElement.dataset.tema=t;}}catch(e){{}}</script>
<style>
  .legal-p {{ max-width: 780px; margin: 0 auto; padding: 48px 20px 80px; }}
  .legal-p h1 {{ font-size: 2rem; font-weight: 800; letter-spacing: -.02em; }}
  .legal-p h2 {{ font-size: 1.15rem; margin: 30px 0 8px; }}
  .legal-p p, .legal-p li {{ color: var(--suave); font-size: .95rem; line-height: 1.7; }}
  .legal-p ul {{ padding-left: 20px; }}
  .legal-p a {{ color: var(--cian); }}
  .legal-p .meta {{ margin-top: 6px; }}
</style>
</head>
<body>
<header class="nav"><div class="c"><a class="marca" href="{inicio}"><span class="corona s"><img src="{r}assets/logo.png" alt="" width="34" height="34"></span><span>WIQON</span></a>
<div class="nav-d"><a class="btn ch" href="{inicio}">{volver}</a></div></div></header>
<main class="legal-p">
{cuerpo}
</main>
</body>
</html>
"""

ES = """<h1>Política de privacidad</h1>
<p class="meta">Última actualización: {fecha}</p>

<h2>1. Quiénes somos</h2>
<p>WIQON (wiqonlab.com) es un laboratorio de investigación de mercados y software con base en Paraguay. Responsable del tratamiento: Ing. Avelino González, en nombre de WIQON. Contacto para cualquier tema de privacidad: <a href="mailto:contacto@wiqonlab.com">contacto@wiqonlab.com</a>.</p>

<h2>2. Qué datos guardamos</h2>
<ul>
<li><strong>Si creás una cuenta:</strong> tu email, la fecha en que aceptaste esta política, el idioma de la página y si aceptaste recibir novedades. El servicio de autenticación registra además la fecha de creación y del último ingreso.</li>
<li><strong>No pedimos</strong> nombre, documento, teléfono, datos bancarios ni contraseñas.</li>
<li><strong>Si nos escribís</strong> por email o WhatsApp, guardamos esa conversación para responderte.</li>
</ul>

<h2>3. Para qué los usamos</h2>
<ul>
<li>Darte acceso a las secciones para usuarios registrados (base legal: la ejecución del servicio que pediste).</li>
<li>Enviarte novedades de WIQON, solo si marcaste esa casilla (base legal: tu consentimiento, que podés retirar cuando quieras).</li>
<li>No vendemos ni alquilamos tus datos, y no los usamos para publicidad de terceros.</li>
</ul>

<h2>4. Quién procesa los datos</h2>
<ul>
<li><strong>Supabase</strong> aloja las cuentas y envía los enlaces de acceso, como encargado del tratamiento.</li>
<li><strong>GitHub Pages</strong> y <strong>Cloudflare</strong> sirven la página y el dominio.</li>
<li>Estos proveedores pueden procesar datos fuera de Paraguay o Brasil, con sus propias medidas de seguridad.</li>
</ul>

<h2>5. Servicios de terceros en la página</h2>
<ul>
<li>Los gráficos interactivos y tablas de mercado los provee <strong>TradingView</strong> y se cargan al llegar a esas secciones.</li>
<li>Los videos de <strong>YouTube</strong> se cargan solo si tocás reproducir (modo de privacidad mejorada).</li>
<li>Los precios en vivo vienen de los servidores públicos de <strong>Binance</strong>; las tipografías, de <strong>Google Fonts</strong>.</li>
<li>Al cargar esos contenidos, tu navegador se conecta con esos servicios, que tienen sus propias políticas.</li>
</ul>

<h2>6. Almacenamiento en tu navegador</h2>
<p>No usamos cookies de publicidad ni herramientas de analítica. Guardamos en tu navegador (almacenamiento local) solo tu sesión, el tema claro u oscuro y si estás logueado, para que la página funcione.</p>

<h2>7. Cuánto tiempo</h2>
<p>Mientras tu cuenta exista. Si pedís borrarla, eliminamos tus datos en un plazo de 15 días, salvo lo que la ley nos obligue a conservar.</p>

<h2>8. Tus derechos</h2>
<p>Podés pedir en cualquier momento acceso a tus datos, corrección, eliminación de la cuenta, portabilidad o retirar tu consentimiento para recibir novedades. Si estás en Brasil, estos derechos están previstos en la Ley General de Protección de Datos (LGPD, Ley 13.709/2018). Escribinos a <a href="mailto:contacto@wiqonlab.com">contacto@wiqonlab.com</a> desde el email de tu cuenta y respondemos en un máximo de 15 días.</p>

<h2>9. Menores de edad</h2>
<p>La cuenta es para mayores de 18 años. Si detectamos una cuenta de un menor, la eliminamos.</p>

<h2>10. Cambios</h2>
<p>Si cambiamos esta política, actualizamos la fecha de arriba y, si el cambio es importante, lo avisamos a los usuarios registrados.</p>
"""

PT = """<h1>Política de privacidade</h1>
<p class="meta">Última atualização: {fecha}</p>

<h2>1. Quem somos</h2>
<p>A WIQON (wiqonlab.com) é um laboratório de pesquisa de mercados e software com base no Paraguai. Controlador dos dados: Eng. Avelino González, em nome da WIQON. Contato para qualquer assunto de privacidade: <a href="mailto:contacto@wiqonlab.com">contacto@wiqonlab.com</a>.</p>

<h2>2. Quais dados guardamos</h2>
<ul>
<li><strong>Se você cria uma conta:</strong> o seu e-mail, a data em que aceitou esta política, o idioma da página e se aceitou receber novidades. O serviço de autenticação registra também a data de criação e do último acesso.</li>
<li><strong>Não pedimos</strong> nome, documento, telefone, dados bancários nem senhas.</li>
<li><strong>Se você nos escreve</strong> por e-mail ou WhatsApp, guardamos essa conversa para responder.</li>
</ul>

<h2>3. Para que usamos</h2>
<ul>
<li>Dar acesso às seções para usuários cadastrados (base legal: execução do serviço solicitado, art. 7º, V, da LGPD).</li>
<li>Enviar novidades da WIQON, só se você marcou essa opção (base legal: consentimento, art. 7º, I, que pode ser revogado a qualquer momento).</li>
<li>Não vendemos nem alugamos os seus dados e não os usamos para publicidade de terceiros.</li>
</ul>

<h2>4. Quem trata os dados</h2>
<ul>
<li>A <strong>Supabase</strong> hospeda as contas e envia os links de acesso, como operadora.</li>
<li>O <strong>GitHub Pages</strong> e a <strong>Cloudflare</strong> servem a página e o domínio.</li>
<li>Esses fornecedores podem tratar dados fora do Brasil ou do Paraguai, com as próprias medidas de segurança (transferência internacional, art. 33 da LGPD).</li>
</ul>

<h2>5. Serviços de terceiros na página</h2>
<ul>
<li>Os gráficos interativos e tabelas de mercado são fornecidos pela <strong>TradingView</strong> e carregam ao chegar nessas seções.</li>
<li>Os vídeos do <strong>YouTube</strong> só carregam se você tocar em reproduzir (modo de privacidade aprimorada).</li>
<li>Os preços ao vivo vêm dos servidores públicos da <strong>Binance</strong>; as fontes, do <strong>Google Fonts</strong>.</li>
<li>Ao carregar esses conteúdos, o seu navegador se conecta com esses serviços, que têm as próprias políticas.</li>
</ul>

<h2>6. Armazenamento no seu navegador</h2>
<p>Não usamos cookies de publicidade nem ferramentas de análise. Guardamos no seu navegador (armazenamento local) só a sua sessão, o tema claro ou escuro e se você está logado, para a página funcionar.</p>

<h2>7. Por quanto tempo</h2>
<p>Enquanto a sua conta existir. Se você pedir a exclusão, apagamos os seus dados em até 15 dias, exceto o que a lei nos obrigue a manter.</p>

<h2>8. Os seus direitos (LGPD, art. 18)</h2>
<p>Você pode pedir a qualquer momento: confirmação e acesso aos seus dados, correção, exclusão da conta, portabilidade, informação sobre com quem compartilhamos e revogação do consentimento para novidades. Escreva para <a href="mailto:contacto@wiqonlab.com">contacto@wiqonlab.com</a> a partir do e-mail da sua conta; respondemos em até 15 dias. Você também pode recorrer à Autoridade Nacional de Proteção de Dados (ANPD).</p>

<h2>9. Menores de idade</h2>
<p>A conta é para maiores de 18 anos. Se identificarmos uma conta de menor, ela será excluída.</p>

<h2>10. Mudanças</h2>
<p>Se mudarmos esta política, atualizamos a data acima e, se a mudança for importante, avisamos os usuários cadastrados.</p>
"""


def escribir(destino, **k):
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(BASE.format(**k), encoding="utf-8", newline="\n")
    print("OK", destino.relative_to(RAIZ))


escribir(RAIZ / "privacidad" / "index.html", lang="es", titulo="Política de privacidad", r="../", inicio="../", volver="Volver a WIQON", cuerpo=ES.format(fecha=FECHA_ES))
escribir(RAIZ / "br" / "privacidade" / "index.html", lang="pt-BR", titulo="Política de privacidade", r="../../", inicio="../", volver="Voltar para a WIQON", cuerpo=PT.format(fecha=FECHA_PT))
