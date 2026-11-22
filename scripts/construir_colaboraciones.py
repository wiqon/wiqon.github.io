"""
Kit de medios / página de colaboraciones para marcas (exchanges, billeteras, fintech, herramientas).
  colaboraciones/   br/parcerias/   en/partnerships/
Reutiliza la plantilla, el formulario (webhook contacto-web de n8n) y el pie de construir_legales.py.
Uso:  python scripts/construir_colaboraciones.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from construir_legales import BASE, EMAIL, RAIZ, formulario, pie, FORM_ES

FORM_PT = dict(nombre="Nome e empresa", email="E-mail", mensaje="Proposta (produto, formato, prazos e orçamento)", enviar="Enviar proposta",
               idioma="pt", aviso='Usamos seus dados só para responder (ver <a href="../privacidade/">política de privacidade</a>).',
               falta="Preencha nome, um e-mail válido e a proposta.", enviando="Enviando…",
               ok="Proposta enviada! Respondemos por e-mail em até 2 dias úteis.",
               error=f"Não foi possível enviar. Tente de novo ou escreva para {EMAIL}.")
FORM_EN = dict(nombre="Name and company", email="Email", mensaje="Proposal (product, format, timing and budget)", enviar="Send proposal",
               idioma="en", aviso='We only use your data to reply (see <a href="../privacy/">privacy policy</a>).',
               falta="Please fill in your name, a valid email and the proposal.", enviando="Sending…",
               ok="Proposal sent! We reply by email within 2 business days.",
               error=f"Could not send. Please try again or write to {EMAIL}.")
FORM_COL_ES = dict(FORM_ES, nombre="Nombre y empresa", mensaje="Propuesta (producto, formato, plazos y presupuesto)",
                   enviar="Enviar propuesta", ok="¡Propuesta enviada! Respondemos por correo en hasta 2 días hábiles.")

ES = f"""<h1>Colaboraciones con marcas</h1>
<p>WIQON es un laboratorio de trading de Paraguay y Brasil. Probamos estrategias, bots y plataformas con datos reales y publicamos el resultado tal como sale, también cuando no funciona. Esa es la propuesta para una marca: <strong>una prueba honesta que la audiencia cree</strong>, en español y en portugués.</p>

<h2>Qué ofrecemos</h2>
<div class="tit"><p><strong>Paquete laboratorio · US$ 350</strong><br>Prueba real del producto con método y datos públicos, página en wiqonlab.com, video largo en YouTube en español, versión en portugués y tres videos cortos (Shorts, Reels y TikTok).</p></div>
<div class="tit"><p><strong>A medida · Según alcance</strong><br>Análisis comparativo, guía paso a paso, serie de videos, auditoría de una estrategia o bot, o asesoría técnica para tokenizar vales de compra y garantías digitales de un comercio (<a href="../laboratorio/vale-agm/">ver el laboratorio</a>).</p></div>
<p>Ejemplos de nuestro trabajo: <a href="../laboratorio/">laboratorio de estrategias</a> y <a href="../auditoria-bots/">auditoría de bots</a>.</p>

<h2>Audiencia</h2>
<ul>
<li>Personas de Paraguay, Brasil y Argentina que operan o quieren empezar a operar cripto, con foco en gestión de riesgo.</li>
<li>Canales: wiqonlab.com, YouTube, TikTok, Instagram, Facebook, X y Telegram, en español (@wiqonlab) y portugués (@wiqonbr).</li>
<li>Compartimos las métricas actualizadas de cada canal cuando nos escribís.</li>
</ul>

<h2>Nuestras reglas</h2>
<ul>
<li>El contenido va <strong>marcado como colaboración pagada</strong>.</li>
<li>Publicamos <strong>los resultados reales</strong>. La marca puede revisar los datos antes de publicar para corregir errores, pero no cambiar el resultado.</li>
<li><strong>No promocionamos futuros con apalancamiento</strong>, rendimientos garantizados ni productos sin un responsable identificable.</li>
<li>Verificamos a cada empresa (registro, licencias y alertas de reguladores) antes de aceptar.</li>
<li>Trabajamos con <strong>contrato por escrito</strong>. Nunca hacemos depósitos para «activar» una colaboración.</li>
</ul>

<h2>Cómo empezamos</h2>
<ol>
<li>Nos contás el producto, el formato y los plazos.</li>
<li>Te respondemos en hasta 2 días hábiles con una propuesta y las métricas.</li>
<li>Firmamos el contrato y arrancamos la prueba. El plazo habitual es de 10 días hábiles.</li>
</ol>

<h2>Enviar una propuesta</h2>
<p>Correo: <a href="mailto:{EMAIL}?subject=Colaboración%20con%20WIQON">{EMAIL}</a></p>
{formulario(FORM_COL_ES)}
"""

PT = f"""<h1>Parcerias com marcas</h1>
<p>A WIQON é um laboratório de trading do Paraguai e do Brasil. Testamos estratégias, bots e plataformas com dados reais e publicamos o resultado como ele sai, inclusive quando não funciona. Essa é a proposta para uma marca: <strong>um teste honesto em que o público confia</strong>, em português e em espanhol.</p>

<h2>O que oferecemos</h2>
<div class="tit"><p><strong>Pacote laboratório · US$ 350</strong><br>Teste real do produto com método e dados públicos, página no wiqonlab.com, vídeo longo no YouTube em espanhol, versão em português e três vídeos curtos (Shorts, Reels e TikTok).</p></div>
<div class="tit"><p><strong>Sob medida · Conforme o escopo</strong><br>Análise comparativa, guia passo a passo, série de vídeos, auditoria de uma estratégia ou bot, ou assessoria técnica para tokenizar vales-compra e garantias digitais de um comércio (<a href="../../laboratorio/vale-agm/">ver o laboratório</a>, em espanhol).</p></div>
<p>Exemplos do nosso trabalho: <a href="../../laboratorio/">laboratório de estratégias</a> e <a href="../../auditoria-bots/">auditoria de bots</a>.</p>

<h2>Público</h2>
<ul>
<li>Pessoas do Brasil, Paraguai e Argentina que operam ou querem começar a operar cripto, com foco em gestão de risco.</li>
<li>Canais: wiqonlab.com, YouTube, TikTok, Instagram, X e Telegram, em português (@wiqonbr) e espanhol (@wiqonlab).</li>
<li>Enviamos as métricas atualizadas de cada canal quando você escrever.</li>
</ul>

<h2>Nossas regras</h2>
<ul>
<li>O conteúdo é <strong>identificado como publicidade paga</strong>.</li>
<li>Publicamos <strong>os resultados reais</strong>. A marca pode revisar os dados antes da publicação para corrigir erros, mas não alterar o resultado.</li>
<li><strong>Não divulgamos futuros alavancados</strong>, rendimentos garantidos nem produtos sem um responsável identificável.</li>
<li>Verificamos cada empresa (registro, licenças e alertas de reguladores) antes de aceitar.</li>
<li>Trabalhamos com <strong>contrato por escrito</strong>. Nunca fazemos depósitos para «ativar» uma parceria.</li>
</ul>

<h2>Como começamos</h2>
<ol>
<li>Você conta o produto, o formato e os prazos.</li>
<li>Respondemos em até 2 dias úteis com uma proposta e as métricas.</li>
<li>Assinamos o contrato e começamos o teste. O prazo habitual é de 10 dias úteis.</li>
</ol>

<h2>Enviar uma proposta</h2>
<p>E-mail: <a href="mailto:{EMAIL}?subject=Parceria%20com%20a%20WIQON">{EMAIL}</a></p>
{formulario(FORM_PT)}
"""

EN = f"""<h1>Brand partnerships</h1>
<p>WIQON is a trading lab from Paraguay and Brazil. We test strategies, bots and platforms with real data and publish the result as it comes out, including when it does not work. That is what we offer a brand: <strong>an honest test the audience trusts</strong>, in Spanish and Portuguese.</p>

<h2>What we offer</h2>
<div class="tit"><p><strong>Lab package · US$ 350</strong><br>Real test of the product with public method and data, a page on wiqonlab.com, a long YouTube video in Spanish, a Portuguese version and three short videos (Shorts, Reels and TikTok).</p></div>
<div class="tit"><p><strong>Custom · Depends on scope</strong><br>Comparative analysis, step-by-step guide, video series, an audit of a strategy or bot, or technical advice to tokenize a store's gift vouchers and digital warranties (<a href="../../laboratorio/vale-agm/">see the lab</a>, in Spanish).</p></div>
<p>Examples of our work: <a href="../../laboratorio/">strategy lab</a> and <a href="../../auditoria-bots/">bot audits</a> (in Spanish).</p>

<h2>Audience</h2>
<ul>
<li>People in Paraguay, Brazil and Argentina who trade or want to start trading crypto, with a focus on risk management.</li>
<li>Channels: wiqonlab.com, YouTube, TikTok, Instagram, Facebook, X and Telegram, in Spanish (@wiqonlab) and Portuguese (@wiqonbr).</li>
<li>We share up-to-date metrics for each channel when you contact us.</li>
</ul>

<h2>Our rules</h2>
<ul>
<li>Content is <strong>labeled as a paid partnership</strong>.</li>
<li>We publish <strong>the real results</strong>. The brand may review the data before publication to fix errors, but not change the outcome.</li>
<li><strong>We do not promote leveraged futures</strong>, guaranteed returns or products without an identifiable company behind them.</li>
<li>We check every company (registration, licenses and regulator warnings) before accepting.</li>
<li>We work with a <strong>written contract</strong>. We never make deposits to "activate" a partnership.</li>
</ul>

<h2>How we start</h2>
<ol>
<li>Tell us the product, format and timing.</li>
<li>We reply within 2 business days with a proposal and metrics.</li>
<li>We sign the contract and start the test. The usual timeline is 10 business days.</li>
</ol>

<h2>Send a proposal</h2>
<p>Email: <a href="mailto:{EMAIL}?subject=Partnership%20with%20WIQON">{EMAIL}</a></p>
{formulario(FORM_EN)}
"""

PAGINAS = [
    ("colaboraciones", "es", "Colaboraciones con marcas",
     "Kit de medios de WIQON: pruebas reales de productos cripto en español y portugués, formatos, tarifas y reglas.", ES),
    ("br/parcerias", "pt", "Parcerias com marcas",
     "Mídia kit da WIQON: testes reais de produtos cripto em português e espanhol, formatos, valores e regras.", PT),
    ("en/partnerships", "en", "Brand partnerships",
     "WIQON media kit: real tests of crypto products in Spanish and Portuguese, formats, rates and rules.", EN),
]

if __name__ == "__main__":
    for ruta, lang, titulo, desc, cuerpo in PAGINAS:
        r = "../" * (ruta.count("/") + 1)
        destino = RAIZ / ruta / "index.html"
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(BASE.format(lang={"es": "es", "pt": "pt-BR", "en": "en"}[lang], titulo=titulo, desc=desc, ruta=ruta + "/", r=r,
                                       inicio="../", volver={"es": "Volver a WIQON", "pt": "Voltar para a WIQON", "en": "Back to WIQON"}[lang],
                                       cuerpo=cuerpo, pie=pie(lang)), encoding="utf-8")
        print("ok", destino.relative_to(RAIZ))
