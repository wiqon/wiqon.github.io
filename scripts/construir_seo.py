"""
Páginas de búsqueda orgánica (SEO) de WIQON, en español y portugués:
  - Cotizaciones oficiales: dólar–guaraní, real–guaraní, dólar–real, dólar–peso argentino
  - Normas: RG DNIT 47/2026 (criptoactivos, Paraguay) y Resoluciones BCB 519/520/521 (Brasil)
Más sitemap.xml y robots.txt.

El valor de cada cotización se escribe en el HTML al construir (para que Google lo lea)
y la página lo refresca con cambio.json al abrirse. Se ejecuta en el workflow después de
actualizar los datos. Uso:  python scripts/construir_seo.py
"""
import html
import json
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SITIO = "https://wiqonlab.com"
LAB = "https://github.com/wiqon/wiqon-lab"
DNIT_NOTA = "https://www.dnit.gov.py/web/portal-institucional/w/la-dnit-establece-obligaci%C3%B3n-de-informar-las-transacciones-con-criptoactivos"
DNIT_RG = "https://www.dnit.gov.py/web/portal-institucional/w/resolución-general-dnit-n°-47/26"
BCB_RES = "https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolu%C3%A7%C3%A3o%20BCB&numero={n}"

try:
    CAMBIO = json.loads((RAIZ / "cambio.json").read_text(encoding="utf-8"))
except (FileNotFoundError, ValueError):
    CAMBIO = {"fuentes": [], "actualizado_utc": None}


def dato(fuente, moneda):
    f = next((x for x in CAMBIO["fuentes"] if x["id"] == fuente), None)
    v = f and next((x for x in f["valores"] if x["moneda"] == moneda), None)
    return (v["valor"], f) if v else (None, f)


def num(v, dec, pt=False):
    if v is None:
        return "—"
    s = f"{v:,.{dec}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def fecha(iso):
    if not iso:
        return "—"
    a, m, d = iso[:10].split("-")
    return f"{d}/{m}/{a}"


# ---------------------------------------------------------------------------------------------
# Cotizaciones. (slug, fuente, moneda, decimales, simbolo, textos por idioma)
COTIZ = [
    dict(slug="dolar-guarani", fuente="bcp", moneda="USD", dec=2, pre="₲ ",
         es=dict(h1="Dólar hoy en Paraguay: cotización oficial del BCP", kw="cotización del dólar en Paraguay, dólar guaraní hoy",
                 corto="USD/PYG", que="cuántos guaraníes vale un dólar estadounidense según la cotización referencial del Banco Central del Paraguay (BCP)",
                 explica=["El BCP publica cada día hábil una <strong>cotización referencial</strong> del dólar frente al guaraní. Es un promedio del mercado: los bancos y las casas de cambio aplican su propio precio de compra y de venta, que puede ser un poco distinto.",
                          "Un guaraní más fuerte (menos guaraníes por dólar) abarata los productos importados y las deudas en dólares; uno más débil favorece a quienes exportan o cobran en dólares, como la soja, la carne o la energía de las binacionales."],
                 faq=[("¿De dónde sale este valor?", "De la planilla de cotizaciones referenciales que publica el Banco Central del Paraguay en su sitio oficial."),
                      ("¿Es el precio al que compro dólares?", "No exactamente. Es una referencia: bancos y casas de cambio aplican su propio precio de compra y venta."),
                      ("¿Cada cuánto se actualiza?", "El BCP la publica en días hábiles. Nuestra página la consulta cada hora y muestra la fecha del dato.")]),
         pt=dict(h1="Dólar hoje no Paraguai: cotação oficial do BCP", kw="cotação do dólar no Paraguai, dólar guarani hoje",
                 corto="USD/PYG", que="quantos guaranis vale um dólar americano segundo a cotação de referência do Banco Central do Paraguai (BCP)",
                 explica=["O BCP publica todo dia útil uma <strong>cotação de referência</strong> do dólar frente ao guarani. É uma média do mercado: bancos e casas de câmbio aplicam o próprio preço de compra e venda.",
                          "Para quem compra em Ciudad del Este, o guarani forte ou fraco muda o preço final em reais e em dólares dos produtos importados."],
                 faq=[("De onde vem este valor?", "Da planilha de cotações de referência que o Banco Central do Paraguai publica no site oficial."),
                      ("É o preço a que eu compro dólares?", "Não exatamente. É uma referência: bancos e casas de câmbio aplicam o próprio preço."),
                      ("Com que frequência é atualizado?", "O BCP publica em dias úteis. A nossa página consulta a cada hora e mostra a data do dado.")])),
    dict(slug="real-guarani", fuente="bcp", moneda="BRL", dec=2, pre="₲ ",
         es=dict(h1="Real hoy en Paraguay: cotización del real brasileño en guaraníes", kw="cotización del real en Paraguay, real guaraní hoy",
                 corto="BRL/PYG", que="cuántos guaraníes vale un real brasileño según la cotización referencial del Banco Central del Paraguay (BCP)",
                 explica=["En la frontera, el real pesa tanto como el dólar: buena parte de los compradores de Ciudad del Este, Pedro Juan Caballero y Encarnación pagan o piensan en reales.",
                          "Cuando el real se fortalece frente al guaraní, los productos paraguayos resultan más baratos para quien viene de Brasil y el comercio fronterizo suele moverse más; cuando se debilita, pasa lo contrario."],
                 faq=[("¿De dónde sale este valor?", "De la planilla de cotizaciones referenciales del Banco Central del Paraguay."),
                      ("¿Por qué importa en la frontera?", "Porque gran parte del comercio de Ciudad del Este se paga o se compara en reales."),
                      ("¿Es el precio de una casa de cambio?", "No. Es una referencia oficial; cada casa de cambio aplica su precio.")]),
         pt=dict(h1="Real hoje no Paraguai: cotação do real em guaranis", kw="cotação do real no Paraguai, real guarani hoje",
                 corto="BRL/PYG", que="quantos guaranis vale um real segundo a cotação de referência do Banco Central do Paraguai (BCP)",
                 explica=["Na fronteira, o real pesa tanto quanto o dólar: boa parte dos compradores de Ciudad del Este e Pedro Juan Caballero paga ou compara preços em reais.",
                          "Quando o real se valoriza frente ao guarani, comprar no Paraguai fica mais barato para quem vem do Brasil; quando se desvaloriza, acontece o contrário."],
                 faq=[("De onde vem este valor?", "Da planilha de cotações de referência do Banco Central do Paraguai."),
                      ("Por que importa na fronteira?", "Porque grande parte do comércio de Ciudad del Este é pago ou comparado em reais."),
                      ("É o preço de uma casa de câmbio?", "Não. É uma referência oficial; cada casa de câmbio aplica o próprio preço.")])),
    dict(slug="dolar-real", fuente="bcb", moneda="USD", dec=4, pre="R$ ",
         es=dict(h1="Dólar hoy en Brasil: cotización PTAX del Banco Central do Brasil", kw="dólar PTAX hoy, cotización dólar real Brasil",
                 corto="USD/BRL", que="cuántos reales vale un dólar según la PTAX, la tasa de referencia del Banco Central do Brasil (BCB)",
                 explica=["La <strong>PTAX</strong> es la cotización de referencia que calcula el Banco Central do Brasil con las operaciones del mercado interbancario. Se usa en contratos, en la liquidación de derivados y como referencia contable.",
                          "Mostramos la PTAX de cierre (o la última publicada del día). Las tarjetas, los bancos y las casas de cambio aplican su propio precio."],
                 faq=[("¿Qué es la PTAX?", "La tasa de cambio de referencia del Banco Central do Brasil, calculada con las operaciones del mercado interbancario."),
                      ("¿De dónde sale este valor?", "De la API pública Olinda del Banco Central do Brasil."),
                      ("¿Es el precio de la tarjeta de crédito?", "No. Es una referencia; tarjetas y bancos aplican su propio tipo de cambio y comisiones.")]),
         pt=dict(h1="Dólar hoje: cotação PTAX do Banco Central do Brasil", kw="dólar PTAX hoje, cotação do dólar",
                 corto="USD/BRL", que="quantos reais vale um dólar segundo a PTAX, a taxa de referência do Banco Central do Brasil (BCB)",
                 explica=["A <strong>PTAX</strong> é a cotação de referência calculada pelo Banco Central do Brasil com as operações do mercado interbancário. É usada em contratos, na liquidação de derivativos e como referência contábil.",
                          "Mostramos a PTAX de fechamento (ou a última publicada no dia). Cartões, bancos e casas de câmbio aplicam o próprio preço."],
                 faq=[("O que é a PTAX?", "A taxa de câmbio de referência do Banco Central do Brasil, calculada com as operações do mercado interbancário."),
                      ("De onde vem este valor?", "Da API pública Olinda do Banco Central do Brasil."),
                      ("É o dólar do cartão de crédito?", "Não. É uma referência; cartões e bancos aplicam o próprio câmbio e taxas.")])),
    dict(slug="dolar-peso-argentino", fuente="bcra", moneda="USD", dec=2, pre="AR$ ",
         es=dict(h1="Dólar oficial en Argentina hoy: tipo de cambio de referencia del BCRA", kw="dólar oficial hoy Argentina, tipo de cambio BCRA",
                 corto="USD/ARS", que="cuántos pesos argentinos vale un dólar según el tipo de cambio de referencia del Banco Central de la República Argentina (BCRA)",
                 explica=["El BCRA publica cada día hábil un <strong>tipo de cambio de referencia</strong> del dólar mayorista. No incluye los otros tipos de cambio que circulan en Argentina (MEP, contado con liquidación o el informal).",
                          "Lo seguimos porque Argentina es uno de los principales socios comerciales de Paraguay y su tipo de cambio influye en el comercio de toda la región."],
                 faq=[("¿Es el dólar blue o el MEP?", "No. Es el tipo de cambio de referencia oficial que publica el BCRA."),
                      ("¿De dónde sale este valor?", "De la API pública de estadísticas cambiarias del Banco Central de la República Argentina."),
                      ("¿Cada cuánto se actualiza?", "El BCRA lo publica en días hábiles; nuestra página lo consulta cada hora.")]),
         pt=dict(h1="Dólar oficial na Argentina hoje: câmbio de referência do BCRA", kw="dólar oficial Argentina hoje, câmbio BCRA",
                 corto="USD/ARS", que="quantos pesos argentinos vale um dólar segundo o câmbio de referência do Banco Central da República Argentina (BCRA)",
                 explica=["O BCRA publica todo dia útil um <strong>câmbio de referência</strong> do dólar atacado. Não inclui os outros dólares que circulam na Argentina (MEP, CCL ou o informal).",
                          "Acompanhamos porque a Argentina é parceira comercial do Brasil e do Paraguai, e o câmbio de lá afeta o comércio da região."],
                 faq=[("É o dólar blue ou o MEP?", "Não. É o câmbio de referência oficial publicado pelo BCRA."),
                      ("De onde vem este valor?", "Da API pública de estatísticas cambiais do Banco Central da República Argentina."),
                      ("Com que frequência é atualizado?", "O BCRA publica em dias úteis; a nossa página consulta a cada hora.")])),
]

NORMAS = [
    dict(slug="dnit-47-2026-criptoactivos",
         es=dict(h1="RG DNIT N.º 47/2026: qué hay que declarar de criptoactivos en Paraguay",
                 desc="Resumen de la Resolución General DNIT 47/2026: quiénes deben informar sus operaciones con criptoactivos, desde qué monto y cómo se presenta.",
                 cuerpo=f"""<p>La <strong>Dirección Nacional de Ingresos Tributarios (DNIT)</strong> emitió el 10 de marzo de 2026 la <strong>Resolución General N.º 47/2026</strong>, que crea la <strong>Declaración Jurada Informativa de Criptoactivos</strong>. Su objetivo es la trazabilidad: que el fisco conozca las operaciones con criptoactivos que se hacen desde Paraguay.</p>
<h2>Quiénes tienen que informar</h2>
<ul><li><strong>Plataformas:</strong> titulares, administradores o responsables de plataformas de criptoactivos que operan en el país.</li>
<li><strong>Personas y empresas residentes</strong> que operan con criptoactivos cuando superan <strong>US$ 5.000 al año</strong> en transacciones, sumadas de forma individual o en conjunto, <strong>con o sin intermediarios</strong> (es decir, también si usás un exchange del exterior).</li></ul>
<h2>Cómo y cuándo</h2>
<p>La declaración es <strong>anual</strong> y se presenta por el sistema <strong>Marangatu</strong>. Según lo publicado, las primeras presentaciones corresponden al ejercicio 2026 y se realizan a inicios de 2027: confirmá las fechas en el calendario de vencimientos de la DNIT.</p>
<h2>Qué conviene hacer desde ahora</h2>
<ul><li>Descargá periódicamente el historial de operaciones de cada exchange o billetera que uses.</li>
<li>Anotá depósitos, retiros y conversiones con fecha y monto en dólares.</li>
<li>Consultá con tu contador cómo encaja en tu situación (IRP, IRE u otro régimen).</li></ul>""",
                 fuentes=[("DNIT: La DNIT establece obligación de informar las transacciones con criptoactivos", DNIT_NOTA), ("DNIT: Resolución General N.º 47/26", DNIT_RG)],
                 faq=[("¿Desde qué monto tengo que informar?", "Si sos residente en Paraguay, cuando tus operaciones con criptoactivos superan US$ 5.000 en el año, con o sin intermediarios."),
                      ("¿Dónde se presenta?", "Por el sistema Marangatu de la DNIT, en forma anual."),
                      ("¿Esto significa que tengo que pagar un impuesto nuevo?", "La RG 47/2026 crea una declaración informativa. Qué impuesto corresponde depende de tu régimen: consultalo con un contador.")]),
         pt=dict(h1="RG DNIT nº 47/2026: o que declarar de criptoativos no Paraguai",
                 desc="Resumo da Resolução Geral DNIT 47/2026: quem deve informar operações com criptoativos no Paraguai, a partir de qual valor e como.",
                 cuerpo=f"""<p>A <strong>Direção Nacional de Receitas Tributárias (DNIT)</strong> do Paraguai emitiu em 10 de março de 2026 a <strong>Resolução Geral nº 47/2026</strong>, que cria a <strong>Declaração Juramentada Informativa de Criptoativos</strong>.</p>
<h2>Quem precisa informar</h2>
<ul><li><strong>Plataformas</strong> de criptoativos que atuam no Paraguai.</li>
<li><strong>Pessoas e empresas residentes no Paraguai</strong> que operam mais de <strong>US$ 5.000 por ano</strong> em criptoativos, com ou sem intermediários.</li></ul>
<h2>Como e quando</h2>
<p>A declaração é <strong>anual</strong>, pelo sistema <strong>Marangatu</strong>. Segundo o divulgado, as primeiras entregas correspondem ao exercício de 2026 e acontecem no início de 2027.</p>
<p><strong>Mora no Brasil?</strong> Esta norma vale para residentes no Paraguai. No Brasil, as obrigações com criptoativos são outras (Receita Federal e as novas regras do Banco Central).</p>""",
                 fuentes=[("DNIT: La DNIT establece obligación de informar las transacciones con criptoactivos", DNIT_NOTA), ("DNIT: Resolución General N.º 47/26", DNIT_RG)],
                 faq=[("A partir de qual valor é preciso informar?", "Residentes no Paraguai, quando as operações com criptoativos passam de US$ 5.000 no ano."),
                      ("Vale para quem mora no Brasil?", "Não. É uma norma paraguaia para residentes no Paraguai."),
                      ("Onde se entrega?", "Pelo sistema Marangatu da DNIT, uma vez por ano.")])),
    dict(slug="bcb-519-520-521-activos-virtuales",
         es=dict(h1="Resoluciones BCB 519, 520 y 521: las nuevas reglas de cripto en Brasil",
                 desc="Qué cambian las Resoluciones BCB 519, 520 y 521 para las prestadoras de servicios de activos virtuales en Brasil, vigentes desde el 1 de octubre de 2026.",
                 cuerpo=f"""<p>El <strong>Banco Central do Brasil</strong> reguló a las <strong>prestadoras de servicios de activos virtuales (PSAV)</strong>, es decir, exchanges y empresas que custodian o intermedian criptoactivos para clientes en Brasil.</p>
<h2>Qué dice cada resolución</h2>
<ul><li><a href="{BCB_RES.format(n=519)}" target="_blank" rel="noopener"><strong>Resolución BCB 519</strong></a> y <a href="{BCB_RES.format(n=520)}" target="_blank" rel="noopener"><strong>520</strong></a>: el proceso de autorización, la gobernanza y el funcionamiento de las prestadoras.</li>
<li><a href="{BCB_RES.format(n=521)}" target="_blank" rel="noopener"><strong>Resolución BCB 521</strong></a>: incluye ciertas operaciones con activos virtuales en el <strong>mercado de cambio</strong>.</li></ul>
<h2>Desde cuándo</h2>
<p>Las reglas rigen desde el <strong>1 de octubre de 2026</strong>. Las disposiciones sobre envío de datos de supervisión empiezan el <strong>1 de enero de 2027</strong>.</p>
<h2>Qué cambia para el usuario</h2>
<ul><li>Conviene operar con plataformas autorizadas o en proceso de autorización ante el Banco Central.</li>
<li>Según lo informado sobre la regulación de prevención de lavado, las transferencias de activos virtuales hacia o desde billeteras de autocustodia por un valor igual o mayor a US$ 10.000 pasan a ser objeto de comunicación específica al COAF.</li></ul>""",
                 fuentes=[(f"Banco Central do Brasil: Resolución BCB {n}", BCB_RES.format(n=n)) for n in (519, 520, 521)],
                 faq=[("¿Desde cuándo rigen?", "Desde el 1 de octubre de 2026; el envío de datos de supervisión, desde el 1 de enero de 2027."),
                      ("¿A quién alcanzan?", "A las prestadoras de servicios de activos virtuales que atienden clientes en Brasil."),
                      ("¿Qué es una billetera de autocustodia?", "Una billetera en la que vos controlás las claves, sin un exchange de por medio.")]),
         pt=dict(h1="Resoluções BCB 519, 520 e 521: as novas regras de cripto no Brasil",
                 desc="O que mudam as Resoluções BCB 519, 520 e 521 para as prestadoras de serviços de ativos virtuais, em vigor desde 1º de outubro de 2026.",
                 cuerpo=f"""<p>O <strong>Banco Central do Brasil</strong> regulou as <strong>prestadoras de serviços de ativos virtuais (PSAV)</strong>: exchanges e empresas que custodiam ou intermediam criptoativos para clientes no Brasil.</p>
<h2>O que diz cada resolução</h2>
<ul><li><a href="{BCB_RES.format(n=519)}" target="_blank" rel="noopener"><strong>Resolução BCB 519</strong></a> e <a href="{BCB_RES.format(n=520)}" target="_blank" rel="noopener"><strong>520</strong></a>: processo de autorização, governança e funcionamento das prestadoras.</li>
<li><a href="{BCB_RES.format(n=521)}" target="_blank" rel="noopener"><strong>Resolução BCB 521</strong></a>: insere determinadas operações com ativos virtuais no <strong>mercado de câmbio</strong>.</li></ul>
<h2>Desde quando</h2>
<p>As regras valem desde <strong>1º de outubro de 2026</strong>. Os dispositivos sobre envio de dados para supervisão começam em <strong>1º de janeiro de 2027</strong>.</p>
<h2>O que muda para o usuário</h2>
<ul><li>Vale operar com plataformas autorizadas ou em processo de autorização no Banco Central.</li>
<li>Segundo o divulgado sobre a regulação de prevenção à lavagem de dinheiro, transferências de ativos virtuais para ou de carteiras autocustodiadas em valor igual ou superior a US$ 10 mil passam a ser objeto de comunicação específica ao Coaf.</li></ul>""",
                 fuentes=[(f"Banco Central do Brasil: Resolução BCB {n}", BCB_RES.format(n=n)) for n in (519, 520, 521)],
                 faq=[("Desde quando valem?", "Desde 1º de outubro de 2026; o envio de dados de supervisão, desde 1º de janeiro de 2027."),
                      ("Quem é afetado?", "As prestadoras de serviços de ativos virtuais que atendem clientes no Brasil."),
                      ("O que é carteira autocustodiada?", "Uma carteira em que você controla as chaves, sem uma exchange no meio.")])),
]

T = {
    "es": dict(lang="es", base="", raiz_sitio="/", volver="Volver a WIQON", inicio="Inicio", crear="Crear cuenta gratis", lab="Ver el laboratorio",
               cuenta_txt="Con tu cuenta gratis ves todas las cotizaciones oficiales, el radar de noticias de la región y los resultados del laboratorio.",
               valor="Valor", inst="Institución", fecha="Fecha", act="Consultado", que="Qué muestra", faq="Preguntas frecuentes", fuentes="Fuentes",
               otras="Otras cotizaciones", normas="Normas que conviene conocer", aviso="Información de referencia; no es asesoría financiera, legal ni tributaria.",
               cambio_dir="cambio", norma_dir="normas", sitio_nombre="WIQON", hreflang="es", otro="pt-BR", nota_norma="Resumen informativo elaborado por WIQON a partir de las fuentes oficiales citadas. No reemplaza el texto de la norma ni el consejo de un profesional."),
    "pt": dict(lang="pt-BR", base="br/", raiz_sitio="/br/", volver="Voltar para a WIQON", inicio="Início", crear="Criar conta grátis", lab="Ver o laboratório",
               cuenta_txt="Com a sua conta grátis você vê todas as cotações oficiais, o radar de notícias da região e os resultados do laboratório.",
               valor="Valor", inst="Instituição", fecha="Data", act="Consultado", que="O que mostra", faq="Perguntas frequentes", fuentes="Fontes",
               otras="Outras cotações", normas="Normas que vale conhecer", aviso="Informação de referência; não é recomendação de investimento nem orientação jurídica ou tributária.",
               cambio_dir="cambio", norma_dir="normas", sitio_nombre="WIQON", hreflang="pt-BR", otro="es", nota_norma="Resumo informativo elaborado pela WIQON a partir das fontes oficiais citadas. Não substitui o texto da norma nem a orientação de um profissional."),
}

PAGINA = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="{hl}" href="{url}">
<link rel="alternate" hreflang="{hl_otro}" href="{url_otro}">
<meta property="og:title" content="{titulo}"><meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{sitio}/assets/og.png"><meta property="og:type" content="article">
<meta name="theme-color" content="#060b14">
<link rel="icon" href="{r}assets/favicon.png">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}assets/v4.css">
<script>try{{var t=localStorage.getItem("wiqon-tema");if(t)document.documentElement.dataset.tema=t;}}catch(e){{}}</script>
<style>
  .seo {{ max-width: 860px; margin: 0 auto; padding: 40px 20px 70px; }}
  .seo h1 {{ font-size: clamp(1.8rem, 3.6vw, 2.5rem); font-weight: 800; letter-spacing: -.02em; line-height: 1.15; }}
  .seo h2 {{ font-size: 1.2rem; margin: 30px 0 10px; }}
  .seo p, .seo li {{ color: var(--suave); line-height: 1.7; }} .seo p {{ margin: 0 0 12px; }} .seo li {{ margin-bottom: 6px; }}
  .seo ul {{ padding-left: 20px; }} .seo a {{ color: var(--cian); }}
  .migas {{ font-size: .8rem; color: var(--gris); margin-bottom: 14px; }} .migas a {{ color: var(--gris); }}
  .cotiz {{ display: flex; align-items: baseline; gap: 18px; flex-wrap: wrap; margin: 20px 0; padding: 22px; border: 1px solid var(--borde2); border-radius: 14px; background: var(--sup); }}
  .cotiz .v {{ font-family: var(--mono); font-size: 2.6rem; font-weight: 500; }}
  .cotiz .m {{ color: var(--gris); font-size: .86rem; }}
  .cta-b {{ display: flex; gap: 12px; flex-wrap: wrap; margin: 26px 0; padding: 22px; border-radius: 14px; border: 1px solid rgba(34,195,238,.35); background: var(--sup); align-items: center; justify-content: space-between; }}
  .cta-b p {{ margin: 0; max-width: 480px; }}
  .rel {{ display: flex; gap: 8px; flex-wrap: wrap; }} .rel a {{ padding: 6px 12px; border: 1px solid var(--borde2); border-radius: 999px; text-decoration: none; color: var(--suave); font-size: .86rem; }}
  .faq-s details {{ border-bottom: 1px solid var(--borde); padding: 12px 0; }} .faq-s summary {{ cursor: pointer; font-weight: 600; }}
</style>
<script type="application/ld+json">{faq_json}</script>
</head>
<body>
<header class="nav"><div class="c"><a class="marca" href="{r_home}"><span class="corona s"><img src="{r}assets/logo.png" alt="" width="34" height="34"></span><span>WIQON</span></a>
<div class="nav-d"><a class="btn ch" href="{r_home}">{volver}</a><a class="btn p ch" href="{r_home}#ingresar">{crear}</a></div></div></header>
<main class="seo">
<nav class="migas" aria-label="breadcrumb"><a href="{r_home}">{inicio}</a> › {seccion}</nav>
<h1>{h1}</h1>
{cuerpo}
<div class="cta-b"><p>{cuenta_txt}</p><div class="rel"><a class="btn p ch" href="{r_home}#ingresar" style="color:#04121c">{crear}</a><a class="btn ch" href="{r_home}#laboratorio">{lab}</a></div></div>
<h2>{faq_t}</h2>
<div class="faq-s">{faq_html}</div>
<h2>{fuentes_t}</h2>
<ul>{fuentes_html}</ul>
{relacionados}
<p class="nota" style="margin-top:30px">{aviso}</p>
</main>
{script}
<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "c394b4ca4e5144b19a861d3203511d84"}}'></script>
</body>
</html>
"""


def faq_bloques(items):
    jl = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}
    return json.dumps(jl, ensure_ascii=False), "".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in items)


def relacionados(idioma, actual):
    t = T[idioma]
    nombres_c = {c["slug"]: c[idioma]["corto"] for c in COTIZ}
    links_c = "".join(f'<a href="{SITIO}/{t["base"]}cambio/{s}/">{n}</a>' for s, n in nombres_c.items() if s != actual)
    links_n = "".join(f'<a href="{SITIO}/{t["base"]}normas/{n["slug"]}/">{n[idioma]["h1"].split(":")[0]}</a>' for n in NORMAS if n["slug"] != actual)
    return f'<h2>{t["otras"]}</h2><div class="rel">{links_c}</div><h2>{t["normas"]}</h2><div class="rel">{links_n}</div>'


def escribir(ruta, contenido):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(contenido, encoding="utf-8", newline="\n")


def main():
    urls = []
    for idioma in ("es", "pt"):
        t = T[idioma]
        prof = 2 if idioma == "es" else 3
        r = "../" * prof
        r_home = SITIO + t["raiz_sitio"]
        for c in COTIZ:
            x = c[idioma]
            v, f = dato(c["fuente"], c["moneda"])
            url = f"{SITIO}/{t['base']}cambio/{c['slug']}/"
            url_otro = f"{SITIO}/{T['pt' if idioma == 'es' else 'es']['base']}cambio/{c['slug']}/"
            inst = (f or {}).get("institucion", "—")
            cuerpo = (f'<div class="cotiz"><span class="v" id="valor">{c["pre"]}{num(v, c["dec"])}</span>'
                      f'<span class="m">{x["corto"]} · <a href="{(f or {}).get("url", "#")}" target="_blank" rel="noopener">{inst}</a> · {t["fecha"]}: <span id="fecha">{fecha((f or {}).get("fecha"))}</span></span></div>'
                      f'<p><strong>{t["que"]}:</strong> {x["que"]}.</p>' + "".join(f"<p>{p}</p>" for p in x["explica"]))
            fj, fh = faq_bloques(x["faq"])
            script = ('<script>fetch("' + SITIO + '/cambio.json?t="+Math.floor(Date.now()/36e5)).then(r=>r.json()).then(d=>{const f=d.fuentes.find(x=>x.id==="'
                      + c["fuente"] + '");const v=f&&f.valores.find(x=>x.moneda==="' + c["moneda"] + '");if(!v)return;'
                      'document.getElementById("valor").textContent="' + c["pre"] + '"+v.valor.toLocaleString("' + ("pt-BR" if idioma == "pt" else "es-PY") + '",{minimumFractionDigits:' + str(c["dec"]) + ',maximumFractionDigits:' + str(c["dec"]) + '});'
                      'const[a,m,dd]=f.fecha.split("-");document.getElementById("fecha").textContent=dd+"/"+m+"/"+a;}).catch(()=>{});</script>')
            pag = PAGINA.format(lang=t["lang"], titulo=f'{x["h1"]} | WIQON', desc=html.escape(f'{x["h1"]}. {x["que"][0].upper() + x["que"][1:]}.'), url=url, url_otro=url_otro,
                                hl=t["hreflang"], hl_otro=t["otro"], sitio=SITIO, r=r, r_home=r_home, volver=t["volver"], crear=t["crear"], inicio=t["inicio"],
                                seccion=x["corto"], h1=x["h1"], cuerpo=cuerpo, cuenta_txt=t["cuenta_txt"], lab=t["lab"], faq_t=t["faq"], faq_html=fh, faq_json=fj,
                                fuentes_t=t["fuentes"], fuentes_html=f'<li><a href="{(f or {}).get("url", "#")}" target="_blank" rel="noopener">{inst}</a></li>',
                                relacionados=relacionados(idioma, c["slug"]), aviso=t["aviso"], script=script)
            escribir(RAIZ / t["base"] / "cambio" / c["slug"] / "index.html", pag)
            urls.append(url)
        for n in NORMAS:
            x = n[idioma]
            url = f"{SITIO}/{t['base']}normas/{n['slug']}/"
            url_otro = f"{SITIO}/{T['pt' if idioma == 'es' else 'es']['base']}normas/{n['slug']}/"
            fj, fh = faq_bloques(x["faq"])
            pag = PAGINA.format(lang=t["lang"], titulo=f'{x["h1"]} | WIQON', desc=html.escape(x["desc"]), url=url, url_otro=url_otro, hl=t["hreflang"], hl_otro=t["otro"],
                                sitio=SITIO, r=r, r_home=r_home, volver=t["volver"], crear=t["crear"], inicio=t["inicio"], seccion=x["h1"].split(":")[0], h1=x["h1"],
                                cuerpo=x["cuerpo"] + f'<p class="nota">{t["nota_norma"]}</p>', cuenta_txt=t["cuenta_txt"], lab=t["lab"], faq_t=t["faq"], faq_html=fh, faq_json=fj,
                                fuentes_t=t["fuentes"], fuentes_html="".join(f'<li><a href="{u}" target="_blank" rel="noopener">{html.escape(nm)}</a></li>' for nm, u in x["fuentes"]),
                                relacionados=relacionados(idioma, n["slug"]), aviso=t["aviso"], script="")
            escribir(RAIZ / t["base"] / "normas" / n["slug"] / "index.html", pag)
            urls.append(url)

    hoy = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    principales = [f"{SITIO}/", f"{SITIO}/br/", f"{SITIO}/shield/", f"{SITIO}/privacidad/", f"{SITIO}/br/privacidade/"]
    mapa = "".join(f"<url><loc>{u}</loc><lastmod>{hoy}</lastmod></url>" for u in principales + urls)
    escribir(RAIZ / "sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{mapa}</urlset>\n')
    escribir(RAIZ / "robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITIO}/sitemap.xml\n")
    print("páginas:", len(urls), "· sitemap con", len(principales) + len(urls), "URLs")


if __name__ == "__main__":
    main()
