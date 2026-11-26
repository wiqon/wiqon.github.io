"""
WIQON Ciberseguridad: sección de servicios de revisión de seguridad para sitios y plataformas online.
  ciberseguridad/   br/ciberseguranca/
Reutiliza la plantilla, el formulario (webhook contacto-web de n8n) y el pie de construir_legales.py.
Uso:  python scripts/construir_ciberseguridad.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from construir_legales import BASE, EMAIL, RAIZ, formulario, pie, FORM_ES
from radar_sucesos import CSS as RADAR_CSS, radar

FORM_SEG_ES = dict(FORM_ES, nombre="Nombre y empresa", mensaje="Sitio o plataforma a revisar y plan que te interesa",
                   enviar="Pedir revisión", ok="¡Pedido enviado! Te respondemos por correo en hasta 2 días hábiles.")
FORM_SEG_PT = dict(nombre="Nome e empresa", email="E-mail", mensaje="Site ou plataforma a revisar e plano de interesse",
                   enviar="Pedir revisão", idioma="pt",
                   aviso='Usamos seus dados só para responder (ver <a href="../privacidade/">política de privacidade</a>).',
                   falta="Preencha nome, um e-mail válido e a mensagem.", enviando="Enviando…",
                   ok="Pedido enviado! Respondemos por e-mail em até 2 dias úteis.",
                   error=f"Não foi possível enviar. Tente de novo ou escreva para {EMAIL}.")

ES = f"""<h1>WIQON Ciberseguridad</h1>
<p>Revisamos la seguridad de sitios web y plataformas online de comercios y pymes. Te entregamos un informe claro, en lenguaje simple, con qué está mal, qué tan grave es y cómo corregirlo. Usamos el mismo método que en el laboratorio: <strong>medir y documentar, no prometer</strong>.</p>
{RADAR_CSS}
{radar('es')}
<p>¿Por qué ahora? En noviembre de 2026 relevamos <strong>63 sitios de empresas paraguayas (.com.py)</strong> que aparecen en listas públicas de phishing: les entraron por un WordPress o un plugin desactualizado y los usaron para alojar estafas. Casi siempre, el dueño no se había enterado.</p>

<div class="tit"><p><strong>Probá gratis el escaneo básico.</strong> Escribí tu dominio y en segundos ves un semáforo con HTTPS, certificado, cabeceras, correo y listas de phishing. <a href="../escaneo/">Escanear mi sitio gratis</a>.</p></div>

<h2>Planes</h2>
<div class="tit plan vig"><p><strong>Vigilancia mensual · US$ 30 por mes</strong><br>Te avisamos si tu sitio se cae, si el certificado está por vencer, si cambia la portada (desfiguración), si aparece en una lista de phishing, si alguien registra un dominio parecido o si sale una vulnerabilidad nueva en lo que usás.</p></div>
<div class="tit plan rev"><p><strong>Revisión externa · US$ 120 de lanzamiento</strong> (precio normal US$ 180)<br>Sin intrusión: miramos lo que cualquiera ve desde afuera. Entrega en 3 días hábiles.</p>
<ul>
<li>Certificado, cabeceras de seguridad, archivos y paneles expuestos.</li>
<li>Versión de WordPress, plugins o framework, y vulnerabilidades conocidas (CVE).</li>
<li>Correo: SPF, DKIM y DMARC, para saber si alguien puede mandar correos en tu nombre.</li>
<li>Reputación: listas de phishing, Navegación segura de Google y dominios que imitan al tuyo.</li>
<li>Puertos abiertos del servidor.</li>
<li>Informe con semáforo (🔴 urgente, 🟡 importante, 🟢 bien) y cómo corregir cada punto.</li>
</ul></div>
<div class="tit plan aud"><p><strong>Auditoría con autorización · US$ 550</strong><br>Todo lo de la revisión externa y además pruebas activas, con autorización firmada. Entrega en 7 a 10 días hábiles.</p>
<ul>
<li>Escaneo activo de vulnerabilidades del sitio y del servidor.</li>
<li>Revisión de formularios, inicio de sesión y permisos, sin explotar fallos ni tocar datos.</li>
<li>Revisión del hosting, del panel y de las copias de seguridad (con acceso de lectura).</li>
<li>Reunión de 30 minutos para explicar el informe.</li>
<li>Segunda verificación sin costo después de que corrijas.</li>
</ul></div>


<h2>Cómo trabajamos</h2>
<div class="trabajo"><ul>
<li><strong>Autorización por escrito</strong> antes de empezar: qué sitio, qué alcance y en qué fechas. Sin autorización no revisamos nada.</li>
<li><strong>Confidencialidad:</strong> el informe es solo para vos. No publicamos hallazgos ni nombres de clientes.</li>
<li><strong>Sin daño:</strong> no explotamos fallos, no accedemos a datos de tus clientes y no cambiamos nada en tu sitio.</li>
<li><strong>Sin promesas imposibles:</strong> ninguna revisión deja un sitio «100 % seguro». Reducimos el riesgo y te decimos qué queda pendiente.</li>
<li>Pago por adelantado en la revisión externa; 50 % al iniciar y 50 % al entregar en la auditoría.</li>
</ul></div>

<h2>Cómo empezamos</h2>
<ol>
<li>Nos contás qué sitio o plataforma querés revisar.</li>
<li>Te enviamos el alcance y la autorización para firmar.</li>
<li>Hacemos la revisión y te entregamos el informe con los pasos para corregir.</li>
</ol>

<h2>Pedir una revisión</h2>
<p>Correo: <a href="mailto:{EMAIL}?subject=Revisión%20de%20seguridad">{EMAIL}</a></p>
{formulario(FORM_SEG_ES)}
"""

PT = f"""<h1>WIQON Cibersegurança</h1>
<p>Revisamos a segurança de sites e plataformas online de lojas e pequenas empresas. Você recebe um relatório claro, em linguagem simples, com o que está errado, a gravidade e como corrigir. Usamos o mesmo método do laboratório: <strong>medir e documentar, não prometer</strong>.</p>
{RADAR_CSS}
{radar('pt')}
<p>Por que agora? Em novembro de 2026 levantamos <strong>63 sites de empresas paraguaias (.com.py)</strong> que aparecem em listas públicas de phishing: foram invadidos por um WordPress ou plugin desatualizado e usados para hospedar golpes. Quase sempre o dono nem sabia.</p>

<div class="tit"><p><strong>Teste grátis o escaneamento básico.</strong> Digite seu domínio e em segundos veja um semáforo com HTTPS, certificado, cabeçalhos, e-mail e listas de phishing. <a href="../escaneo/">Escanear meu site grátis</a>.</p></div>

<h2>Planos</h2>
<div class="tit plan vig"><p><strong>Monitoramento mensal · US$ 30 por mês</strong><br>Avisamos se o site cair, se o certificado estiver para vencer, se a página inicial mudar (desfiguração), se aparecer numa lista de phishing, se alguém registrar um domínio parecido ou se sair uma vulnerabilidade nova no que você usa.</p></div>
<div class="tit plan rev"><p><strong>Revisão externa · US$ 120 de lançamento</strong> (preço normal US$ 180)<br>Sem intrusão: olhamos o que qualquer pessoa vê de fora. Entrega em 3 dias úteis.</p>
<ul>
<li>Certificado, cabeçalhos de segurança, arquivos e painéis expostos.</li>
<li>Versão do WordPress, plugins ou framework, e vulnerabilidades conhecidas (CVE).</li>
<li>E-mail: SPF, DKIM e DMARC, para saber se alguém pode enviar e-mails em seu nome.</li>
<li>Reputação: listas de phishing, Navegação segura do Google e domínios que imitam o seu.</li>
<li>Portas abertas do servidor.</li>
<li>Relatório com semáforo (🔴 urgente, 🟡 importante, 🟢 ok) e como corrigir cada ponto.</li>
</ul></div>
<div class="tit plan aud"><p><strong>Auditoria autorizada · US$ 550</strong><br>Tudo da revisão externa e mais testes ativos, com autorização assinada. Entrega em 7 a 10 dias úteis.</p>
<ul>
<li>Varredura ativa de vulnerabilidades do site e do servidor.</li>
<li>Revisão de formulários, login e permissões, sem explorar falhas nem tocar dados.</li>
<li>Revisão da hospedagem, do painel e dos backups (com acesso de leitura).</li>
<li>Reunião de 30 minutos para explicar o relatório.</li>
<li>Segunda verificação sem custo depois que você corrigir.</li>
</ul></div>


<h2>Como trabalhamos</h2>
<div class="trabajo"><ul>
<li><strong>Autorização por escrito</strong> antes de começar: qual site, qual escopo e em que datas. Sem autorização não revisamos nada.</li>
<li><strong>Confidencialidade:</strong> o relatório é só seu. Não publicamos achados nem nomes de clientes.</li>
<li><strong>Sem dano:</strong> não exploramos falhas, não acessamos dados dos seus clientes e não mudamos nada no seu site.</li>
<li><strong>Sem promessas impossíveis:</strong> nenhuma revisão deixa um site «100 % seguro». Reduzimos o risco e dizemos o que fica pendente.</li>
<li>Pagamento antecipado na revisão externa; 50 % no início e 50 % na entrega na auditoria.</li>
</ul></div>

<h2>Como começamos</h2>
<ol>
<li>Você conta qual site ou plataforma quer revisar.</li>
<li>Enviamos o escopo e a autorização para assinar.</li>
<li>Fazemos a revisão e entregamos o relatório com os passos para corrigir.</li>
</ol>

<h2>Pedir uma revisão</h2>
<p>E-mail: <a href="mailto:{EMAIL}?subject=Revisão%20de%20segurança">{EMAIL}</a></p>
{formulario(FORM_SEG_PT)}
"""

PAGINAS = [
    ("ciberseguridad", "es", "WIQON Ciberseguridad",
     "Revisión de seguridad para sitios web y plataformas de comercios y pymes: revisión externa, auditoría con autorización y vigilancia mensual.", ES),
    ("br/ciberseguranca", "pt", "WIQON Cibersegurança",
     "Revisão de segurança para sites e plataformas de lojas e pequenas empresas: revisão externa, auditoria autorizada e monitoramento mensal.", PT),
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
