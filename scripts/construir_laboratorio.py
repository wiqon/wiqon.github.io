"""
Páginas del laboratorio dentro del sitio, en tres idiomas (para que Google encuentre los resultados en
wiqonlab.com y no solo en GitHub):

  laboratorio/                 br/laboratorio/                     en/lab/              índice de experimentos
  laboratorio/grid-bots/       br/laboratorio/robos-de-grid/       en/lab/grid-bots/    experimento #6
  laboratorio/dca-bot/         br/laboratorio/robo-dca/            en/lab/dca-bot/      experimento #7

Los números salen de github.com/wiqon/wiqon-lab (resultados/*.csv) y las series semanales de
scripts/datos_lab/*.json. Cada página lleva datos estructurados (Article + FAQPage + BreadcrumbList).
Uso:  python scripts/construir_laboratorio.py
"""
import html
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SITIO = "https://wiqonlab.com"
LAB = "https://github.com/wiqon/wiqon-lab"
DATOS = Path(__file__).resolve().parent / "datos_lab"
PUBLICADO, MODIFICADO = "2026-10-18", "2026-10-19"

BASE = {"es": "", "pt-BR": "br/", "en": "en/"}
RUTAS = {  # ruta de cada página por idioma
    "indice": {"es": "laboratorio/", "pt-BR": "br/laboratorio/", "en": "en/lab/"},
    "grid": {"es": "laboratorio/grid-bots/", "pt-BR": "br/laboratorio/robos-de-grid/", "en": "en/lab/grid-bots/"},
    "dca": {"es": "laboratorio/dca-bot/", "pt-BR": "br/laboratorio/robo-dca/", "en": "en/lab/dca-bot/"},
}
OTRAS = {
    "es": dict(auditoria="auditoria-bots/", libro="libro/", terminos="terminos/", devoluciones="devoluciones/", contacto="contacto/", privacidad="privacidad/", shield="shield/"),
    "pt-BR": dict(auditoria="br/auditoria-robos/", libro="br/livro/", terminos="br/termos/", devoluciones="br/devolucoes/", contacto="br/contato/", privacidad="br/privacidade/", shield="shield/"),
    "en": dict(auditoria="en/bot-audit/", libro="en/book/", terminos="en/terms/", devoluciones="en/refunds/", contacto="en/contact/", privacidad="en/privacy/", shield="en/shield/"),
}
COMUN = {
    "es": dict(inicio="Inicio", lab="Laboratorio", tema="Cambiar tema", leer="Ver el experimento", codigo="Código y datos en GitHub", fuentes="Fuentes y método",
               rel="Seguí leyendo", faq="Preguntas frecuentes", corta="Respuesta corta", anio="Año", aviso="Simulación con datos pasados: no garantiza resultados futuros. Contenido educativo; no es asesoría financiera.",
               l_terminos="Términos y condiciones", l_devoluciones="Entregas y devoluciones", l_contacto="Contacto", l_privacidad="Privacidad",
               cta_t="¿Usás uno de estos bots?", cta_p="Lo auditamos con tus propios datos: el resultado de tu cuenta, no el del panel. El diagnóstico es gratis.", cta_b="Auditar mi bot", cta_l="Leer el libro «¿Ventaja o suerte?»",
               publicado="Publicado el 18 de octubre de 2026 · Actualizado el 19 de octubre de 2026", autor="Por Avelino González, WIQON Lab"),
    "pt-BR": dict(inicio="Início", lab="Laboratório", tema="Mudar tema", leer="Ver o experimento", codigo="Código e dados no GitHub", fuentes="Fontes e método",
                  rel="Continue lendo", faq="Perguntas frequentes", corta="Resposta curta", anio="Ano", aviso="Simulação com dados passados: não garante resultados futuros. Conteúdo educativo; não é recomendação de investimento.",
                  l_terminos="Termos e condições", l_devoluciones="Entregas e devoluções", l_contacto="Contato", l_privacidad="Privacidade",
                  cta_t="Você usa um desses robôs?", cta_p="Auditamos com os seus próprios dados: o resultado da sua conta, não o do painel. O diagnóstico é grátis.", cta_b="Auditar meu robô", cta_l="Ler o livro «Vantagem ou sorte?»",
                  publicado="Publicado em 18 de outubro de 2026 · Atualizado em 19 de outubro de 2026", autor="Por Avelino González, WIQON Lab"),
    "en": dict(inicio="Home", lab="Lab", tema="Toggle theme", leer="See the experiment", codigo="Code and data on GitHub", fuentes="Sources and method",
               rel="Keep reading", faq="Frequently asked questions", corta="Short answer", anio="Year", aviso="Simulation on past data: no guarantee of future results. Educational content; not financial advice.",
               l_terminos="Terms and conditions", l_devoluciones="Delivery and refunds", l_contacto="Contact", l_privacidad="Privacy",
               cta_t="Do you use one of these bots?", cta_p="We audit it with your own data: your account's result, not the dashboard's. The diagnosis is free.", cta_b="Audit my bot", cta_l="Read the book «Edge or Luck?»",
               publicado="Published October 18, 2026 · Updated October 19, 2026", autor="By Avelino González, WIQON Lab"),
}


def num(v, lang, dec=1, signo=False):
    """12.4 → '12,4' (es/pt) o '12.4' (en); con miles."""
    s = f"{v:+,.{dec}f}" if signo else f"{v:,.{dec}f}"
    if lang != "en":
        s = s.replace(",", "§").replace(".", ",").replace("§", ".")
    return s.replace("-", "−")


def pct(v, lang, dec=1, signo=False):
    return num(v, lang, dec, signo) + (" %" if lang == "es" else "%")  # en Brasil y en inglés, sin espacio


# ---------------------------------------------------------------- gráfico SVG (colores por variables del tema)
def svg_serie(serie, marca, aria, W, H, ml, mr, mt, mb, fuente, cada_anios, clase):
    fechas = serie["fechas"]
    vals = serie["panel"] + serie["cuenta"]
    paso = 10000 if max(vals) < 40000 else 20000
    top = (int(max(vals) / paso) + 1) * paso
    n = len(fechas)
    X = lambda i: ml + i / (n - 1) * (W - ml - mr)
    Y = lambda v: mt + (1 - v / top) * (H - mt - mb)
    linea = lambda s: " ".join(f"{'M' if i == 0 else 'L'}{X(i):.1f} {Y(v):.1f}" for i, v in enumerate(s))
    eje = "".join(f'<line x1="{ml}" x2="{W - mr}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" class="g-r"/><text x="{ml - 8}" y="{Y(v) + 5:.1f}" text-anchor="end" class="g-e" font-size="{fuente}">{v // 1000}k</text>'
                  for v in range(0, top + 1, paso))
    anios = "".join(f'<text x="{X(i):.1f}" y="{H - 12}" text-anchor="middle" class="g-e" font-size="{fuente}">{f[:4]}</text>'
                    for i, f in enumerate(fechas) if f[5:7] == "01" and int(f[8:10]) <= 7 and int(f[:4]) % cada_anios == 0)
    base = f'<line x1="{ml}" x2="{W - mr}" y1="{Y(10000):.1f}" y2="{Y(10000):.1f}" class="g-cap"/>'
    extra = ""
    if marca is not None:
        i = marca
        extra = (f'<line x1="{X(i):.1f}" x2="{X(i):.1f}" y1="{Y(serie["panel"][i]):.1f}" y2="{Y(serie["cuenta"][i]):.1f}" class="g-gap"/>'
                 f'<circle cx="{X(i):.1f}" cy="{Y(serie["panel"][i]):.1f}" r="6" class="g-pp"/><circle cx="{X(i):.1f}" cy="{Y(serie["cuenta"][i]):.1f}" r="6" class="g-pc"/>')
    return f'''<svg class="{clase}" viewBox="0 0 {W} {H}" role="img" aria-label="{html.escape(aria)}">
{eje}{anios}{base}<path d="{linea(serie['cuenta'])}" class="g-c"/><path d="{linea(serie['panel'])}" class="g-p"/>{extra}</svg>'''


def grafico(serie, etiquetas, lang, marca=None, aria=""):
    """Dos versiones del mismo gráfico: ancha para PC y alta con letra grande para el celular."""
    ancho = svg_serie(serie, marca, aria, 960, 400, 64, 16, 20, 40, 13, 1, "g-ancho")
    angosto = svg_serie(serie, marca, aria, 420, 330, 44, 10, 14, 34, 15, 2, "g-angosto")
    return f'''<figure class="graf">{ancho}{angosto}
<figcaption><span class="ley l-p">{etiquetas[0]}</span><span class="ley l-c">{etiquetas[1]}</span><span class="ley l-k">{etiquetas[2]}</span></figcaption></figure>'''


def tabla(cab, filas, clase=""):
    th = "".join(f"<th>{c}</th>" for c in cab)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in f) + "</tr>" for f in filas)
    return f'<div class="tabla-env"><table class="lt {clase}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


# ---------------------------------------------------------------- contenido: grid bots
GS = json.loads((DATOS / "grid_serie.json").read_text(encoding="utf-8"))
DS = json.loads((DATOS / "dca_serie.json").read_text(encoding="utf-8"))
ANUAL_GRID = [(2018, -72.3, -27.7, -63.9), (2019, 94.3, 134.0, 21.2), (2020, 302.0, 168.2, -6.2), (2021, 59.8, 77.9, -10.9), (2022, -64.2, -20.8, -47.0),
              (2023, 155.6, 82.7, 22.2), (2024, 121.3, 65.0, 36.0), (2025, -6.3, 4.8, 1.8), (2026, -4.6, 11.0, -17.3)]
ANUAL_DCA = [(2018, -72.3, -27.7, -54.0), (2019, 94.3, 134.0, 214.1), (2020, 302.0, 168.2, 55.2), (2021, 59.8, 77.9, 51.3), (2022, -64.2, -20.8, -64.2),
             (2023, 155.6, 82.7, 155.6), (2024, 121.3, 65.0, 59.7), (2025, -6.3, 4.8, 24.2), (2026, -4.6, 11.0, 2.2)]


def grid(lang):
    L = lang
    T = {
        "es": dict(
            titulo="¿Los grid bots funcionan? Probamos 64 configuraciones con datos reales | WIQON",
            desc="Grid bot de spot en BTC/USDT con velas de 5 minutos de 2018 a 2026: ninguna de 64 configuraciones superó a comprar y mantener, y la «ganancia del grid» del panel no es el resultado de la cuenta.",
            miga="Grid bots", h1="¿Los grid bots funcionan? Probamos 64 configuraciones con datos reales",
            lead="Un grid bot compra cada vez que el precio baja un escalón y vende cuando sube al siguiente. Lo ofrecen Binance, Pionex, Bitsgap y Cryptohopper, y su panel casi siempre muestra ganancias. Lo probamos con datos reales de BTC/USDT, de 2018 a 2026, con las comisiones de Binance.",
            corta="En nuestra prueba, no: ninguna de las 64 configuraciones le ganó a comprar y mantener BTC, y la mediana perdió 9 % por año. La «ganancia del grid» que muestran los paneles subió +237 % en la mediana mientras la cuenta real caía 56 %.",
            g_aria="Gráfico: lo que mostraba el panel de un grid bot contra lo que valía la cuenta, 2018-2026",
            g_ley=("Lo que mostraba el panel", "Lo que valía la cuenta", "Capital inicial US$ 10.000"),
            g_nota="Grid típico: ±10 %, 20 niveles, reinicio mensual. El panel suma las vueltas cerradas; la cuenta incluye el BTC comprado en las bajas que quedó valiendo menos.",
            cifras=[("0 de 64", "configuraciones superaron a comprar y mantener"), ("−9 %", "por año, la mediana"), ("+237 %", "«ganancia del grid» mediana en el panel"), ("−56 %", "resultado real mediano de la cuenta")],
            metodo_t="Cómo lo probamos",
            metodo=["Grid geométrico de spot, el más común: el rango se arma alrededor del precio y cada escalón maneja la misma parte del capital.",
                    "Velas de 5 minutos del archivo público de Binance, de enero de 2018 a septiembre de 2026 (más de 900.000 velas).",
                    "Comisión de 0,1 % por orden, la de Binance spot sin descuentos. Órdenes límite, sin deslizamiento.",
                    "64 combinaciones: rango de ±5, 10, 20 o 30 %; 10, 20, 50 o 100 niveles; reinicio cada 7, 30 o 90 días, o al salir del rango.",
                    "Medimos dos cosas que los paneles mezclan: la suma de las vueltas cerradas y el valor total de la cuenta."],
            res_t="Resultados", res_cab=["", "Por año", "Peor caída"],
            res=[("Grid, mediana de 64", -9.0, -78.6), ("Mejor grid (±30 %, 10 niveles, reinicio semanal)", 12.4, -48.3), ("Grid típico (±10 %, 20 niveles, mensual)", -13.8, -85.0),
                 ("Comprar y mantener BTC", 23.3, -81.2), ("Regla de tendencia (media de 100 días)", 42.7, -38.5)],
            anual_t="Año por año", anual_cab=["Año", "Comprar y mantener", "Regla de tendencia", "Grid típico"],
            anual_n="2026 llega hasta septiembre. El grid gana en años laterales y pierde fuerte en los bajistas; en el alcista de 2020 hizo −6 % contra +302 % de mantener.",
            porque_t="Por qué el panel engaña",
            porque=["Cada vez que el precio sube un escalón, el bot vende y el panel suma esa ganancia. Son muchas ganancias chicas: en el grid típico, 8.832 vueltas en 8 años.",
                    "Pero cuando el precio baja, el bot compra en cada escalón y se queda con BTC que vale menos. Esa pérdida no figura en la «ganancia del grid».",
                    "Las comisiones también se acumulan: en el grid típico sumaron el 44 % del capital inicial.",
                    "Con rangos angostos y muchos niveles es peor: con ±5 % y 100 niveles la distancia entre escalones (0,1 %) es menor que las dos comisiones de cada vuelta (0,2 %), y cada vuelta pierde."],
            faq=[("¿Un grid bot puede ganar dinero?", "Sí, en mercados laterales: el grid típico ganó en 2019, 2023 y 2024. El problema es que no sabés de antemano si el año va a ser lateral, y en los bajistas pierde casi tanto como tener BTC."),
                 ("¿Qué es la «ganancia del grid»?", "Es la suma de las vueltas cerradas (compra y venta un escalón arriba). No descuenta lo que perdió el BTC comprado en las bajas, así que puede ser positiva mientras la cuenta pierde."),
                 ("¿Cuál fue la mejor configuración?", "Rango de ±30 %, 10 niveles y reinicio semanal: +12,4 % por año con una caída máxima de −48 %. Aun así quedó por debajo de comprar y mantener (+23,3 %)."),
                 ("¿Esto vale para Pionex, Bitsgap o Binance?", "La lógica es la misma en todas: probamos el grid geométrico de spot que usan. Cada plataforma tiene detalles propios (comisiones, reinicios automáticos); si querés medir el tuyo, lo auditamos con tus datos.")]),
        "pt-BR": dict(
            titulo="Robôs de grid funcionam? Testamos 64 configurações com dados reais | WIQON",
            desc="Robô de grid em spot no BTC/USDT com candles de 5 minutos de 2018 a 2026: nenhuma de 64 configurações superou comprar e segurar, e o «lucro do grid» do painel não é o resultado da conta.",
            miga="Robôs de grid", h1="Robôs de grid funcionam? Testamos 64 configurações com dados reais",
            lead="Um robô de grid compra toda vez que o preço cai um degrau e vende quando sobe para o seguinte. Binance, Pionex, Bitsgap e Cryptohopper oferecem, e o painel quase sempre mostra lucro. Testamos com dados reais de BTC/USDT, de 2018 a 2026, com as taxas da Binance.",
            corta="No nosso teste, não: nenhuma das 64 configurações ganhou de comprar e segurar BTC, e a mediana perdeu 9% ao ano. O «lucro do grid» que os painéis mostram subiu +237% na mediana enquanto a conta real caía 56%.",
            g_aria="Gráfico: o que o painel de um robô de grid mostrava contra o que a conta valia, 2018-2026",
            g_ley=("O que o painel mostrava", "O que a conta valia", "Capital inicial US$ 10.000"),
            g_nota="Grid típico: ±10%, 20 níveis, reinício mensal. O painel soma as voltas fechadas; a conta inclui o BTC comprado nas quedas que passou a valer menos.",
            cifras=[("0 de 64", "configurações superaram comprar e segurar"), ("−9%", "ao ano, a mediana"), ("+237%", "«lucro do grid» mediano no painel"), ("−56%", "resultado real mediano da conta")],
            metodo_t="Como testamos",
            metodo=["Grid geométrico em spot, o mais comum: a faixa é montada em torno do preço e cada degrau administra a mesma parte do capital.",
                    "Candles de 5 minutos do arquivo público da Binance, de janeiro de 2018 a setembro de 2026 (mais de 900.000 candles).",
                    "Taxa de 0,1% por ordem, a da Binance spot sem descontos. Ordens limite, sem slippage.",
                    "64 combinações: faixa de ±5, 10, 20 ou 30%; 10, 20, 50 ou 100 níveis; reinício a cada 7, 30 ou 90 dias, ou ao sair da faixa.",
                    "Medimos duas coisas que os painéis misturam: a soma das voltas fechadas e o valor total da conta."],
            res_t="Resultados", res_cab=["", "Ao ano", "Pior queda"],
            res=[("Grid, mediana de 64", -9.0, -78.6), ("Melhor grid (±30%, 10 níveis, reinício semanal)", 12.4, -48.3), ("Grid típico (±10%, 20 níveis, mensal)", -13.8, -85.0),
                 ("Comprar e segurar BTC", 23.3, -81.2), ("Regra de tendência (média de 100 dias)", 42.7, -38.5)],
            anual_t="Ano a ano", anual_cab=["Ano", "Comprar e segurar", "Regra de tendência", "Grid típico"],
            anual_n="2026 vai até setembro. O grid ganha em anos laterais e perde forte nos de baixa; na alta de 2020 fez −6% contra +302% de segurar.",
            porque_t="Por que o painel engana",
            porque=["Cada vez que o preço sobe um degrau, o robô vende e o painel soma esse lucro. São muitos lucros pequenos: no grid típico, 8.832 voltas em 8 anos.",
                    "Mas quando o preço cai, o robô compra em cada degrau e fica com BTC que vale menos. Essa perda não aparece no «lucro do grid».",
                    "As taxas também se acumulam: no grid típico somaram 44% do capital inicial.",
                    "Com faixas estreitas e muitos níveis é pior: com ±5% e 100 níveis a distância entre degraus (0,1%) é menor que as duas taxas de cada volta (0,2%), e cada volta perde."],
            faq=[("Um robô de grid pode ganhar dinheiro?", "Sim, em mercados laterais: o grid típico ganhou em 2019, 2023 e 2024. O problema é que você não sabe antes se o ano vai ser lateral, e nos de baixa ele perde quase tanto quanto ter BTC."),
                 ("O que é o «lucro do grid»?", "É a soma das voltas fechadas (compra e venda um degrau acima). Não desconta o que o BTC comprado nas quedas perdeu, então pode ser positivo enquanto a conta perde."),
                 ("Qual foi a melhor configuração?", "Faixa de ±30%, 10 níveis e reinício semanal: +12,4% ao ano com queda máxima de −48%. Mesmo assim ficou abaixo de comprar e segurar (+23,3%)."),
                 ("Isso vale para Pionex, Bitsgap ou Binance?", "A lógica é a mesma em todas: testamos o grid geométrico em spot que elas usam. Cada plataforma tem detalhes próprios (taxas, reinícios automáticos); se quiser medir o seu, auditamos com os seus dados.")]),
        "en": dict(
            titulo="Do grid bots work? We tested 64 settings on real data | WIQON",
            desc="Spot grid bot on BTC/USDT with 5-minute candles from 2018 to 2026: none of 64 settings beat buy and hold, and the dashboard's «grid profit» is not the account's result.",
            miga="Grid bots", h1="Do grid bots work? We tested 64 settings on real data",
            lead="A grid bot buys every time the price drops one step and sells when it rises to the next. Binance, Pionex, Bitsgap and Cryptohopper offer them, and the dashboard almost always shows profits. We tested it on real BTC/USDT data, from 2018 to 2026, with Binance fees.",
            corta="In our test, no: none of the 64 settings beat buying and holding BTC, and the median lost 9% a year. The «grid profit» dashboards display rose +237% in the median while the real account fell 56%.",
            g_aria="Chart: what a grid bot's dashboard showed versus what the account was worth, 2018-2026",
            g_ley=("What the dashboard showed", "What the account was worth", "Starting capital US$ 10,000"),
            g_nota="Typical grid: ±10%, 20 levels, monthly reset. The dashboard adds up closed round trips; the account includes the BTC bought on the way down that is now worth less.",
            cifras=[("0 of 64", "settings beat buy and hold"), ("−9%", "a year, the median"), ("+237%", "median «grid profit» on the dashboard"), ("−56%", "median real account result")],
            metodo_t="How we tested it",
            metodo=["Geometric spot grid, the most common kind: the range is built around the price and each step handles the same share of capital.",
                    "5-minute candles from Binance's public archive, January 2018 to September 2026 (over 900,000 candles).",
                    "0.1% fee per order, Binance spot with no discounts. Limit orders, no slippage.",
                    "64 combinations: range of ±5, 10, 20 or 30%; 10, 20, 50 or 100 levels; reset every 7, 30 or 90 days, or when the price leaves the range.",
                    "We measured two things dashboards mix up: the sum of closed round trips and the account's total value."],
            res_t="Results", res_cab=["", "Per year", "Worst drawdown"],
            res=[("Grid, median of 64", -9.0, -78.6), ("Best grid (±30%, 10 levels, weekly reset)", 12.4, -48.3), ("Typical grid (±10%, 20 levels, monthly)", -13.8, -85.0),
                 ("Buy and hold BTC", 23.3, -81.2), ("Trend rule (100-day average)", 42.7, -38.5)],
            anual_t="Year by year", anual_cab=["Year", "Buy and hold", "Trend rule", "Typical grid"],
            anual_n="2026 runs through September. The grid wins in sideways years and loses heavily in bear markets; in the 2020 bull run it made −6% versus +302% for holding.",
            porque_t="Why the dashboard misleads",
            porque=["Every time the price rises one step, the bot sells and the dashboard adds that profit. Many small profits: 8,832 round trips in 8 years for the typical grid.",
                    "But when the price falls, the bot buys at every step and is left holding BTC worth less. That loss is not part of the «grid profit».",
                    "Fees add up too: for the typical grid they totaled 44% of the starting capital.",
                    "Narrow ranges with many levels are worse: at ±5% and 100 levels the gap between steps (0.1%) is smaller than the two fees of each round trip (0.2%), so every trip loses."],
            faq=[("Can a grid bot make money?", "Yes, in sideways markets: the typical grid made money in 2019, 2023 and 2024. The problem is you don't know in advance whether the year will be sideways, and in bear markets it loses almost as much as holding BTC."),
                 ("What is «grid profit»?", "It's the sum of closed round trips (buy, then sell one step higher). It doesn't subtract what the BTC bought on the way down lost, so it can be positive while the account loses."),
                 ("What was the best setting?", "A ±30% range, 10 levels and weekly reset: +12.4% a year with a −48% maximum drawdown. Still below buy and hold (+23.3%)."),
                 ("Does this apply to Pionex, Bitsgap or Binance?", "The logic is the same on all of them: we tested the geometric spot grid they use. Each platform has its own details (fees, automatic resets); if you want to measure yours, we audit it with your data.")]),
    }[L]
    T["grafico"] = grafico(GS, T["g_ley"], L, aria=T["g_aria"])
    T["res_html"] = tabla(T["res_cab"], [(n, pct(a, L, 1, True), pct(d, L, 1)) for n, a, d in T["res"]])
    T["anual_html"] = tabla(T["anual_cab"], [(y, pct(a, L, 1, True), pct(b, L, 1, True), pct(c, L, 1, True)) for y, a, b, c in ANUAL_GRID], "num")
    T["seccion_lab"] = "6-grid-bots-la-ganancia-del-grid-no-es-tu-ganancia"
    return T


def dca(lang):
    L = lang
    imin = min(range(len(DS["fechas"])), key=lambda i: DS["cuenta"][i] / DS["panel"][i])
    T = {
        "es": dict(
            titulo="DCA bot: ¿conviene? Probamos 36 configuraciones con datos reales | WIQON",
            desc="DCA bot con órdenes de seguridad (como 3Commas, Cryptohopper o Pionex) en BTC/USDT de 2018 a 2026: mediana de +19 % por año contra +23 % de mantener, caídas de −80 % y un panel que nunca muestra pérdida.",
            miga="DCA bot", h1="DCA bot: ¿conviene? Probamos 36 configuraciones con datos reales",
            lead="Un DCA bot compra una vez, y si el precio baja compra más con «órdenes de seguridad» para bajar el precio promedio; cuando sube un poco sobre ese promedio, vende todo y vuelve a empezar. Lo ofrecen 3Commas, Cryptohopper, Pionex y Bitsgap. Lo probamos con datos reales de BTC/USDT, de 2018 a 2026.",
            corta="Ganó, pero no más que comprar y mantener: la mediana de 36 configuraciones hizo +19 % por año contra +23 %, con caídas del mismo tamaño (−80 %). Sin stop loss, en los bajistas se queda atrapado durante años, y el panel no lo muestra porque solo suma los ciclos cerrados.",
            g_aria="Gráfico: lo que mostraba el panel de un DCA bot contra lo que valía la cuenta, 2018-2026",
            g_ley=("Lo que mostraba el panel", "Lo que valía la cuenta", "Capital inicial US$ 10.000"),
            g_nota=f"DCA bot típico: toma de ganancia 2 %, 8 órdenes de seguridad cada 2 %, escala 1,5. En noviembre de 2022 el panel mostraba US$ {num(DS['panel_en_min'], 'es', 0)} y la cuenta valía US$ {num(DS['cuenta_en_min'], 'es', 0)}.",
            cifras=[("+19 %", "por año, la mediana (mantener: +23 %)"), ("−80 %", "peor caída, la mediana"), ("2,8 años", "duró el ciclo más largo, en la mediana"), ("81 %", "del tiempo sin órdenes disponibles")],
            metodo_t="Cómo lo probamos",
            metodo=["Orden base a mercado; órdenes de seguridad cada 1, 2 o 4 % por debajo de la entrada (4 u 8, de igual tamaño o creciendo x1,5).",
                    "Toma de ganancia de 1, 2 o 3 % sobre el precio promedio, con la comisión incluida. Al cerrar, abre otro ciclo en la vela siguiente.",
                    "Los tamaños se calculan para que la base más todas las órdenes usen el capital disponible: el bot nunca se queda sin plata para la próxima orden.",
                    "Sin stop loss, la configuración habitual. Comisión de 0,1 % por orden. Velas de 5 minutos de Binance, de enero de 2018 a septiembre de 2026.",
                    "Separamos lo que muestra el panel (ganancia de los ciclos cerrados) del valor real de la cuenta, que incluye el ciclo abierto."],
            res_t="Resultados", res_cab=["", "Por año", "Peor caída"],
            res=[("DCA bot, mediana de 36", 19.3, -79.5), ("Mejor (tp 3 %, 8 órdenes cada 2 %, x1,5)", 29.8, -73.6), ("Típico (tp 2 %, 8 órdenes cada 2 %, x1,5)", 23.4, -69.4),
                 ("Comprar y mantener BTC", 23.3, -81.2), ("Regla de tendencia (media de 100 días)", 42.7, -38.5)],
            anual_t="Año por año", anual_cab=["Año", "Comprar y mantener", "Regla de tendencia", "DCA bot típico"],
            anual_n="2026 llega hasta septiembre. En 2022 (−64 %) y 2023 (+156 %) el bot típico hizo exactamente lo mismo que mantener: estuvo atrapado con todo comprado.",
            porque_t="Por qué el panel nunca muestra pérdida",
            porque=["Cada ciclo se cierra solo con ganancia: el bot vende recién cuando el precio supera su promedio. Por eso la lista de ciclos cerrados siempre está en verde.",
                    "Cuando el precio cae más allá de la última orden de seguridad, el bot ya no puede comprar más y espera. Ese ciclo abierto, que puede perder 60 % o más, no figura en la ganancia del panel.",
                    "Sin stop loss, el bot es BTC comprado con más pasos: las 36 configuraciones terminaron en positivo porque BTC subió, con caídas del mismo tamaño que tenerlo.",
                    "Lo que sí cambia el resultado es salir en los bajistas: la regla de tendencia, con el mismo BTC, hizo +42,7 % por año con una caída de −38,5 %."],
            faq=[("¿Un DCA bot pierde plata?", "Sus ciclos cerrados no, pero la cuenta sí: el bot típico llegó a caer −69 % en 2022. Sin stop loss, la pérdida queda en el ciclo abierto hasta que el precio vuelva."),
                 ("¿Es lo mismo que el DCA de ahorro?", "No. El DCA de ahorro es comprar un monto fijo cada semana o mes y quedárselo. El DCA bot compra y vende en ciclos cortos. Los dos están en nuestro laboratorio, con resultados distintos."),
                 ("¿Cuál fue la mejor configuración?", "Toma de ganancia de 3 % con 8 órdenes de seguridad cada 2 % y escala 1,5: +29,8 % por año con una caída de −73,6 %. Solo 4 de las 36 superaron a mantener."),
                 ("¿Sirve para 3Commas, Cryptohopper o Pionex?", "Probamos la lógica que usan todos (orden base, órdenes de seguridad y toma de ganancia sobre el promedio). Si querés medir tu configuración exacta, la auditamos con tus datos.")]),
        "pt-BR": dict(
            titulo="Robô DCA: vale a pena? Testamos 36 configurações com dados reais | WIQON",
            desc="Robô DCA com ordens de segurança (como 3Commas, Cryptohopper ou Pionex) no BTC/USDT de 2018 a 2026: mediana de +19% ao ano contra +23% de segurar, quedas de −80% e um painel que nunca mostra prejuízo.",
            miga="Robô DCA", h1="Robô DCA: vale a pena? Testamos 36 configurações com dados reais",
            lead="Um robô DCA compra uma vez e, se o preço cai, compra mais com «ordens de segurança» para baixar o preço médio; quando sobe um pouco acima desse médio, vende tudo e recomeça. 3Commas, Cryptohopper, Pionex e Bitsgap oferecem. Testamos com dados reais de BTC/USDT, de 2018 a 2026.",
            corta="Ganhou, mas não mais que comprar e segurar: a mediana de 36 configurações fez +19% ao ano contra +23%, com quedas do mesmo tamanho (−80%). Sem stop loss, nos mercados de baixa fica preso por anos, e o painel não mostra porque só soma os ciclos fechados.",
            g_aria="Gráfico: o que o painel de um robô DCA mostrava contra o que a conta valia, 2018-2026",
            g_ley=("O que o painel mostrava", "O que a conta valia", "Capital inicial US$ 10.000"),
            g_nota=f"Robô DCA típico: take profit de 2%, 8 ordens de segurança a cada 2%, escala 1,5. Em novembro de 2022 o painel mostrava US$ {num(DS['panel_en_min'], 'pt-BR', 0)} e a conta valia US$ {num(DS['cuenta_en_min'], 'pt-BR', 0)}.",
            cifras=[("+19%", "ao ano, a mediana (segurar: +23%)"), ("−80%", "pior queda, a mediana"), ("2,8 anos", "durou o ciclo mais longo, na mediana"), ("81%", "do tempo sem ordens disponíveis")],
            metodo_t="Como testamos",
            metodo=["Ordem base a mercado; ordens de segurança a cada 1, 2 ou 4% abaixo da entrada (4 ou 8, de tamanho igual ou crescendo x1,5).",
                    "Take profit de 1, 2 ou 3% sobre o preço médio, com a taxa incluída. Ao fechar, abre outro ciclo no candle seguinte.",
                    "Os tamanhos são calculados para que a base e todas as ordens usem o capital disponível: o robô nunca fica sem dinheiro para a próxima ordem.",
                    "Sem stop loss, a configuração habitual. Taxa de 0,1% por ordem. Candles de 5 minutos da Binance, de janeiro de 2018 a setembro de 2026.",
                    "Separamos o que o painel mostra (lucro dos ciclos fechados) do valor real da conta, que inclui o ciclo aberto."],
            res_t="Resultados", res_cab=["", "Ao ano", "Pior queda"],
            res=[("Robô DCA, mediana de 36", 19.3, -79.5), ("Melhor (tp 3%, 8 ordens a cada 2%, x1,5)", 29.8, -73.6), ("Típico (tp 2%, 8 ordens a cada 2%, x1,5)", 23.4, -69.4),
                 ("Comprar e segurar BTC", 23.3, -81.2), ("Regra de tendência (média de 100 dias)", 42.7, -38.5)],
            anual_t="Ano a ano", anual_cab=["Ano", "Comprar e segurar", "Regra de tendência", "Robô DCA típico"],
            anual_n="2026 vai até setembro. Em 2022 (−64%) e 2023 (+156%) o robô típico fez exatamente o mesmo que segurar: ficou preso com tudo comprado.",
            porque_t="Por que o painel nunca mostra prejuízo",
            porque=["Cada ciclo só fecha com lucro: o robô vende apenas quando o preço supera o seu médio. Por isso a lista de ciclos fechados está sempre no verde.",
                    "Quando o preço cai além da última ordem de segurança, o robô não pode comprar mais e espera. Esse ciclo aberto, que pode perder 60% ou mais, não aparece no lucro do painel.",
                    "Sem stop loss, o robô é BTC comprado com mais passos: as 36 configurações terminaram no positivo porque o BTC subiu, com quedas do mesmo tamanho que tê-lo.",
                    "O que muda o resultado é sair nos mercados de baixa: a regra de tendência, com o mesmo BTC, fez +42,7% ao ano com queda de −38,5%."],
            faq=[("Um robô DCA perde dinheiro?", "Os ciclos fechados não, mas a conta sim: o robô típico chegou a cair −69% em 2022. Sem stop loss, o prejuízo fica no ciclo aberto até o preço voltar."),
                 ("É o mesmo que o DCA de poupança?", "Não. O DCA de poupança é comprar um valor fixo toda semana ou mês e guardar. O robô DCA compra e vende em ciclos curtos. Os dois estão no nosso laboratório, com resultados diferentes."),
                 ("Qual foi a melhor configuração?", "Take profit de 3% com 8 ordens de segurança a cada 2% e escala 1,5: +29,8% ao ano com queda de −73,6%. Só 4 das 36 superaram segurar."),
                 ("Serve para 3Commas, Cryptohopper ou Pionex?", "Testamos a lógica que todos usam (ordem base, ordens de segurança e take profit sobre o médio). Se quiser medir a sua configuração exata, auditamos com os seus dados.")]),
        "en": dict(
            titulo="DCA bots: are they worth it? We tested 36 settings on real data | WIQON",
            desc="DCA bot with safety orders (like 3Commas, Cryptohopper or Pionex) on BTC/USDT from 2018 to 2026: median +19% a year versus +23% for holding, −80% drawdowns and a dashboard that never shows a loss.",
            miga="DCA bot", h1="DCA bots: are they worth it? We tested 36 settings on real data",
            lead="A DCA bot buys once, and if the price drops it buys more with «safety orders» to lower its average price; when the price rises a little above that average, it sells everything and starts over. 3Commas, Cryptohopper, Pionex and Bitsgap offer them. We tested it on real BTC/USDT data, from 2018 to 2026.",
            corta="It made money, but no more than buy and hold: the median of 36 settings made +19% a year versus +23%, with drawdowns just as deep (−80%). Without a stop loss it gets stuck for years in bear markets, and the dashboard doesn't show it because it only counts closed deals.",
            g_aria="Chart: what a DCA bot's dashboard showed versus what the account was worth, 2018-2026",
            g_ley=("What the dashboard showed", "What the account was worth", "Starting capital US$ 10,000"),
            g_nota=f"Typical DCA bot: 2% take profit, 8 safety orders every 2%, 1.5 volume scale. In November 2022 the dashboard showed US$ {num(DS['panel_en_min'], 'en', 0)} while the account was worth US$ {num(DS['cuenta_en_min'], 'en', 0)}.",
            cifras=[("+19%", "a year, the median (holding: +23%)"), ("−80%", "worst drawdown, the median"), ("2.8 years", "longest deal, the median"), ("81%", "of the time with no orders left")],
            metodo_t="How we tested it",
            metodo=["Market base order; safety orders every 1, 2 or 4% below the entry (4 or 8, equal size or growing x1.5).",
                    "Take profit of 1, 2 or 3% over the average price, fees included. After closing, a new deal opens on the next candle.",
                    "Order sizes are set so the base plus all safety orders use the available capital: the bot never runs out of money for the next order.",
                    "No stop loss, the usual setup. 0.1% fee per order. Binance 5-minute candles, January 2018 to September 2026.",
                    "We separated what the dashboard shows (profit from closed deals) from the account's real value, which includes the open deal."],
            res_t="Results", res_cab=["", "Per year", "Worst drawdown"],
            res=[("DCA bot, median of 36", 19.3, -79.5), ("Best (3% tp, 8 orders every 2%, x1.5)", 29.8, -73.6), ("Typical (2% tp, 8 orders every 2%, x1.5)", 23.4, -69.4),
                 ("Buy and hold BTC", 23.3, -81.2), ("Trend rule (100-day average)", 42.7, -38.5)],
            anual_t="Year by year", anual_cab=["Year", "Buy and hold", "Trend rule", "Typical DCA bot"],
            anual_n="2026 runs through September. In 2022 (−64%) and 2023 (+156%) the typical bot did exactly the same as holding: it was stuck fully invested.",
            porque_t="Why the dashboard never shows a loss",
            porque=["Each deal only closes in profit: the bot sells only when the price is above its average. That's why the list of closed deals is always green.",
                    "When the price falls past the last safety order, the bot can't buy more and waits. That open deal, which can be down 60% or more, isn't part of the dashboard's profit.",
                    "Without a stop loss, the bot is BTC bought with extra steps: all 36 settings ended positive because BTC went up, with drawdowns as deep as holding it.",
                    "What does change the result is getting out in bear markets: the trend rule, on the same BTC, made +42.7% a year with a −38.5% drawdown."],
            faq=[("Does a DCA bot lose money?", "Its closed deals don't, but the account does: the typical bot fell as much as −69% in 2022. Without a stop loss, the loss sits in the open deal until the price comes back."),
                 ("Is it the same as savings DCA?", "No. Savings DCA means buying a fixed amount every week or month and keeping it. A DCA bot buys and sells in short cycles. Both are in our lab, with different results."),
                 ("What was the best setting?", "3% take profit with 8 safety orders every 2% and a 1.5 scale: +29.8% a year with a −73.6% drawdown. Only 4 of the 36 beat holding."),
                 ("Does it apply to 3Commas, Cryptohopper or Pionex?", "We tested the logic they all use (base order, safety orders and take profit over the average). If you want to measure your exact setup, we audit it with your data.")]),
    }[L]
    T["grafico"] = grafico(DS, T["g_ley"], L, marca=imin, aria=T["g_aria"])
    T["res_html"] = tabla(T["res_cab"], [(n, pct(a, L, 1, True), pct(d, L, 1)) for n, a, d in T["res"]])
    T["anual_html"] = tabla(T["anual_cab"], [(y, pct(a, L, 1, True), pct(b, L, 1, True), pct(c, L, 1, True)) for y, a, b, c in ANUAL_DCA], "num")
    T["seccion_lab"] = "7-dca-el-de-ahorro-y-el-dca-bot-no-son-lo-mismo"
    return T


# ---------------------------------------------------------------- índice del laboratorio
def indice(lang):
    secc = lambda s: f"{LAB}#{s}"
    E = {
        "es": dict(titulo="Laboratorio WIQON: estrategias y bots de trading probados con datos reales", desc="Probamos estrategias, grid bots, DCA bots y arbitraje con datos y costos reales. Publicamos todo, también lo que no funciona, con el código abierto.",
                   h1="Lo que probamos con datos reales", lead="Cada idea pasa por el mismo proceso: reglas exactas, años de datos y los costos reales de un exchange o un broker. Publicamos todo, también lo que no funciona, con el código abierto para que cualquiera lo repita.",
                   items=[("grid", "Grid bots de spot", "0 de 64 configuraciones superaron a comprar y mantener; el panel mostraba +237 % con la cuenta en −56 %."),
                          ("dca", "DCA bots con órdenes de seguridad", "Mediana de +19 % por año contra +23 % de mantener, con caídas de −80 % y ciclos atrapados hasta 2,8 años."),
                          (secc("3-lo-que-sobrevivió-filtro-de-tendencia-en-btc"), "Filtro de tendencia en BTC", "La única regla que sobrevivió: 56,6 % por año contra 37,3 % de mantener, con la mitad de la caída (2018-2026)."),
                          (secc("1-una-estrategia-validada-que-era-ruido"), "Day trade con EMA21", "+0,71 % en 3 años y 178 operaciones: no se distingue de cero. Dejar el dinero en Earn rendía +9,3 %."),
                          (secc("2-el-sesgo-de-supervivencia-infla-todo"), "Rotación de altcoins", "33,7 % por año con las monedas de hoy, 1,0 % con las de 2021: el sesgo de supervivencia infla todo."),
                          (secc("4-arbitraje-medido-no-supuesto"), "Arbitraje entre exchanges", "Las diferencias grandes eran monedas distintas con el mismo nombre o retiros suspendidos."),
                          (secc("5-arbitraje-de-funding-cash-and-carry"), "Cobrar la tasa de financiación", "7 a 10 % por año en el histórico, casi todo de 2021; 2 a 3 % en 2025 y 2026.")]),
        "pt-BR": dict(titulo="Laboratório WIQON: estratégias e robôs de trading testados com dados reais", desc="Testamos estratégias, robôs de grid, robôs DCA e arbitragem com dados e custos reais. Publicamos tudo, também o que não funciona, com código aberto.",
                      h1="O que testamos com dados reais", lead="Cada ideia passa pelo mesmo processo: regras exatas, anos de dados e os custos reais de uma exchange ou corretora. Publicamos tudo, também o que não funciona, com código aberto para qualquer um repetir.",
                      items=[("grid", "Robôs de grid em spot", "0 de 64 configurações superaram comprar e segurar; o painel mostrava +237% com a conta em −56%."),
                             ("dca", "Robôs DCA com ordens de segurança", "Mediana de +19% ao ano contra +23% de segurar, com quedas de −80% e ciclos presos por até 2,8 anos."),
                             (secc("3-lo-que-sobrevivió-filtro-de-tendencia-en-btc"), "Filtro de tendência no BTC", "A única regra que sobreviveu: 56,6% ao ano contra 37,3% de segurar, com metade da queda (2018-2026)."),
                             (secc("1-una-estrategia-validada-que-era-ruido"), "Day trade com EMA21", "+0,71% em 3 anos e 178 operações: não se distingue de zero. Deixar o dinheiro no Earn rendia +9,3%."),
                             (secc("2-el-sesgo-de-supervivencia-infla-todo"), "Rotação de altcoins", "33,7% ao ano com as moedas de hoje, 1,0% com as de 2021: o viés de sobrevivência infla tudo."),
                             (secc("4-arbitraje-medido-no-supuesto"), "Arbitragem entre exchanges", "As diferenças grandes eram moedas diferentes com o mesmo nome ou saques suspensos."),
                             (secc("5-arbitraje-de-funding-cash-and-carry"), "Cobrar a taxa de financiamento", "7 a 10% ao ano no histórico, quase tudo de 2021; 2 a 3% em 2025 e 2026.")]),
        "en": dict(titulo="WIQON Lab: trading strategies and bots tested on real data", desc="We test strategies, grid bots, DCA bots and arbitrage with real data and real costs. We publish everything, including what doesn't work, as open source.",
                   h1="What we tested on real data", lead="Every idea goes through the same process: exact rules, years of data and the real costs of an exchange or broker. We publish everything, including what doesn't work, as open source so anyone can repeat it.",
                   items=[("grid", "Spot grid bots", "0 of 64 settings beat buy and hold; the dashboard showed +237% with the account at −56%."),
                          ("dca", "DCA bots with safety orders", "Median +19% a year versus +23% for holding, with −80% drawdowns and deals stuck for up to 2.8 years."),
                          (secc("3-lo-que-sobrevivió-filtro-de-tendencia-en-btc"), "BTC trend filter", "The only rule that survived: 56.6% a year versus 37.3% for holding, with half the drawdown (2018-2026)."),
                          (secc("1-una-estrategia-validada-que-era-ruido"), "EMA21 day trading", "+0.71% over 3 years and 178 trades: indistinguishable from zero. Leaving the money in Earn returned +9.3%."),
                          (secc("2-el-sesgo-de-supervivencia-infla-todo"), "Altcoin rotation", "33.7% a year with today's coins, 1.0% with 2021's: survivorship bias inflates everything."),
                          (secc("4-arbitraje-medido-no-supuesto"), "Cross-exchange arbitrage", "The big gaps were different coins sharing a ticker, or suspended withdrawals."),
                          (secc("5-arbitraje-de-funding-cash-and-carry"), "Collecting the funding rate", "7–10% a year historically, almost all from 2021; 2–3% in 2025 and 2026.")]),
    }[lang]
    return E


# ---------------------------------------------------------------- página
CSS = """
.lb { max-width: 1080px; margin: 0 auto; padding: 0 clamp(16px, 4vw, 48px); }
.lb-barra { display: flex; align-items: center; gap: 16px; height: 72px; }
.lb-barra .der { margin-left: auto; display: flex; gap: 10px; align-items: center; }
.miga { font-size: 14px; color: var(--gris); margin-top: 18px; } .miga a { color: var(--gris); } .miga span { margin: 0 8px; }
.lb-hero { padding: clamp(28px, 5vw, 64px) 0 28px; max-width: 860px; }
.lb-hero h1 { font: 500 clamp(32px, 4.6vw, 58px)/1.06 var(--titulos); letter-spacing: -.035em; text-wrap: balance; }
.lb-hero .lead { margin-top: 20px; color: var(--suave); font-size: clamp(17px, 1.4vw, 19px); max-width: 64ch; }
.lb-hero .meta { margin-top: 14px; color: var(--gris); font-size: 14px; }
.corta { margin: 8px 0 36px; border-left: 3px solid var(--cian); background: var(--sup); border-radius: 0 14px 14px 0; padding: 20px 24px; max-width: 860px; }
.corta b { display: block; font: 500 15px var(--titulos); color: var(--cian); margin-bottom: 6px; } .corta p { font-size: 17px; }
.graf { margin: 0; background: var(--sup); border: 1px solid var(--borde); border-radius: 16px; padding: 18px 18px 12px; }
.graf svg { width: 100%; height: auto; display: block; } .graf .g-angosto { display: none; }
@media (max-width: 600px) { .graf .g-ancho { display: none; } .graf .g-angosto { display: block; } }
.g-r { stroke: var(--borde); stroke-width: 1; } .g-e { fill: var(--gris); font-family: var(--sans); font-weight: 500; }
.g-cap { stroke: var(--gris); stroke-width: 1; stroke-dasharray: 4 6; opacity: .7; }
.g-p { fill: none; stroke: var(--cian); stroke-width: 2.4; stroke-linejoin: round; }
.g-c { fill: none; stroke: var(--baja); stroke-width: 3.6; stroke-linejoin: round; }
.g-gap { stroke: var(--texto); stroke-width: 1.4; stroke-dasharray: 4 5; opacity: .7; } .g-pp { fill: var(--cian); } .g-pc { fill: var(--baja); }
.graf figcaption { display: flex; flex-wrap: wrap; justify-content: flex-start; align-items: flex-start; text-align: left; gap: 8px 20px; font-size: 14px; color: var(--suave); margin-top: 8px; }
@media (max-width: 600px) { .graf figcaption { flex-direction: column; gap: 6px; } }
.ley::before { content: ""; display: inline-block; width: 18px; height: 3px; border-radius: 2px; margin-right: 8px; vertical-align: middle; }
.ley.l-p::before { background: var(--cian); } .ley.l-c::before { background: var(--baja); height: 4px; } .ley.l-k::before { border-top: 1px dashed var(--gris); height: 0; }
.g-nota { color: var(--gris); font-size: 14px; margin-top: 10px; max-width: 80ch; }
.cifras { list-style: none; padding: 0; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 14px; margin: 32px 0 8px; }
.cifras li { background: var(--sup); border: 1px solid var(--borde); border-radius: 14px; padding: 18px; }
.cifras b { display: block; font: 500 clamp(24px, 2.6vw, 32px)/1.1 var(--titulos); letter-spacing: -.02em; color: var(--cian); }
.cifras span { display: block; margin-top: 6px; color: var(--suave); font-size: 14px; }
.lb-s { padding: 44px 0 8px; } .lb-s h2 { font: 500 clamp(24px, 2.8vw, 34px)/1.12 var(--titulos); letter-spacing: -.03em; margin-bottom: 18px; }
.lb-s p, .lb-s li { color: var(--suave); font-size: 17px; max-width: 75ch; } .lb-s ol, .lb-s ul.pun { padding-left: 22px; display: grid; gap: 10px; }
.tabla-env { overflow-x: auto; border: 1px solid var(--borde); border-radius: 14px; }
.lt { width: 100%; border-collapse: collapse; font-size: 15px; } .lt th, .lt td { padding: 12px 14px; text-align: left; border-bottom: 1px solid var(--borde); white-space: nowrap; }
.lt th { color: var(--gris); font-weight: 500; font-size: 13px; } .lt tr:last-child td { border-bottom: 0; } .lt td:not(:first-child), .lt th:not(:first-child) { text-align: right; font-variant-numeric: tabular-nums; }
.lt td:first-child { white-space: normal; min-width: 180px; } .lt.num td:first-child { min-width: 0; }
.nota-t { color: var(--gris); font-size: 14px; margin-top: 10px; }
.faq details { border-bottom: 1px solid var(--borde); padding: 16px 0; } .faq summary { cursor: pointer; font-weight: 600; font-size: 17px; color: var(--texto); }
.faq details p { margin-top: 8px; }
.cta-l { margin: 48px 0 8px; background: var(--sup); border: 1px solid var(--cian); border-radius: 18px; padding: clamp(22px, 3vw, 34px); }
.cta-l h2 { font: 500 clamp(22px, 2.6vw, 30px)/1.15 var(--titulos); letter-spacing: -.02em; } .cta-l p { color: var(--suave); margin-top: 8px; max-width: 64ch; }
.cta-l .acc { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 20px; }
.exps { list-style: none; padding: 0; display: grid; gap: 0; border-top: 1px solid var(--borde); }
.exps li { border-bottom: 1px solid var(--borde); } .exps a { display: grid; grid-template-columns: 1fr auto; gap: 6px 20px; padding: 20px 4px; color: inherit; text-decoration: none; }
.exps b { font: 500 19px/1.25 var(--titulos); letter-spacing: -.01em; } .exps span { color: var(--suave); font-size: 15px; grid-column: 1; } .exps i { grid-row: 1 / span 2; grid-column: 2; align-self: center; color: var(--cian); font-style: normal; font-size: 14px; white-space: nowrap; }
.exps a:hover b { color: var(--cian); }
.rel { list-style: none; padding: 0; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; }
.rel a { display: block; height: 100%; background: var(--sup); border: 1px solid var(--borde); border-radius: 14px; padding: 18px; color: var(--texto); text-decoration: none; font-weight: 600; }
.rel a:hover { border-color: var(--cian); }
.lb-pie { border-top: 1px solid var(--borde); margin-top: 56px; padding: 28px 0 48px; color: var(--gris); font-size: 14px; display: grid; gap: 8px; }
.lb-pie a { color: var(--gris); margin-right: 14px; }
@media (max-width: 820px) { .cifras { grid-template-columns: 1fr 1fr; } .rel { grid-template-columns: 1fr; } }
@media (max-width: 420px) { .exps a { grid-template-columns: 1fr; } .exps i { grid-row: auto; grid-column: 1; } .lb-barra .marca span:last-child { display: none; } }
"""


def raiz_rel(ruta):
    return "../" * ruta.count("/")


def pagina(lang, clave, contenido):
    C, O = COMUN[lang], OTRAS[lang]
    ruta = RUTAS[clave][lang]
    r = raiz_rel(ruta)
    url = f"{SITIO}/{ruta}"
    home = f"{r}{BASE[lang]}"
    lab = f"{r}{RUTAS['indice'][lang]}"
    alt = "".join(f'<link rel="alternate" hreflang="{k}" href="{SITIO}/{v}">' for k, v in RUTAS[clave].items()) + f'<link rel="alternate" hreflang="x-default" href="{SITIO}/{RUTAS[clave]["es"]}">'
    idioma = "".join(f'<a {"class=\"on\" " if k == lang else ""}href="{r}{v}" lang="{k}">{ {"es": "ES", "pt-BR": "PT-BR", "en": "EN"}[k] }</a>' for k, v in RUTAS[clave].items())
    t = contenido
    migas = [(C["inicio"], f"{SITIO}/{BASE[lang]}"), (C["lab"], f"{SITIO}/{RUTAS['indice'][lang]}")]
    if clave != "indice":
        migas.append((t["miga"], url))
    ld = [{"@context": "https://schema.org", "@type": "BreadcrumbList",
           "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(migas)]}]
    if clave == "indice":
        cuerpo = f'''<section class="lb-hero"><h1>{t["h1"]}</h1><p class="lead">{t["lead"]}</p></section>
<ul class="exps">{"".join(f'<li><a href="{(r + RUTAS[k][lang]) if k in RUTAS else k}"{"" if k in RUTAS else " target=\"_blank\" rel=\"noopener\""}><b>{n}</b><span>{d}</span><i>{C["leer"] if k in RUTAS else "GitHub"}</i></a></li>' for k, n, d in t["items"])}</ul>
<p class="nota-t"><a class="enl" href="{LAB}" target="_blank" rel="noopener">{C["codigo"]}</a></p>'''
        miga_html = f'<nav class="miga" aria-label="breadcrumb"><a href="{home}">{C["inicio"]}</a><span>›</span>{C["lab"]}</nav>'
    else:
        ld.append({"@context": "https://schema.org", "@type": "Article", "headline": t["h1"], "description": t["desc"], "inLanguage": lang, "url": url,
                   "datePublished": PUBLICADO, "dateModified": MODIFICADO, "image": f"{SITIO}/assets/og.png",
                   "author": {"@type": "Person", "name": "Avelino González"},
                   "publisher": {"@type": "Organization", "@id": f"{SITIO}/#org", "name": "WIQON", "logo": {"@type": "ImageObject", "url": f"{SITIO}/assets/logo.png"}},
                   "isBasedOn": f"{LAB}#{t['seccion_lab']}"})
        ld.append({"@context": "https://schema.org", "@type": "FAQPage",
                   "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]})
        otra = "dca" if clave == "grid" else "grid"
        nombre_otra = {"grid": {"es": "Grid bots: 64 configuraciones", "pt-BR": "Robôs de grid: 64 configurações", "en": "Grid bots: 64 settings"},
                       "dca": {"es": "DCA bots: 36 configuraciones", "pt-BR": "Robôs DCA: 36 configurações", "en": "DCA bots: 36 settings"}}[otra][lang]
        nombre_aud = {"es": "Auditoría de bots", "pt-BR": "Auditoria de robôs", "en": "Bot audit"}[lang]
        nombre_lab = {"es": "Todos los experimentos", "pt-BR": "Todos os experimentos", "en": "All experiments"}[lang]
        cuerpo = f'''<article>
<section class="lb-hero"><h1>{t["h1"]}</h1><p class="lead">{t["lead"]}</p><p class="meta">{C["autor"]} · {C["publicado"]}</p></section>
<div class="corta"><b>{C["corta"]}</b><p>{t["corta"]}</p></div>
{t["grafico"]}<p class="g-nota">{t["g_nota"]}</p>
<ul class="cifras">{"".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in t["cifras"])}</ul>
<section class="lb-s"><h2>{t["metodo_t"]}</h2><ol>{"".join(f"<li>{x}</li>" for x in t["metodo"])}</ol></section>
<section class="lb-s"><h2>{t["res_t"]}</h2>{t["res_html"]}</section>
<section class="lb-s"><h2>{t["porque_t"]}</h2><ul class="pun">{"".join(f"<li>{x}</li>" for x in t["porque"])}</ul></section>
<section class="lb-s"><h2>{t["anual_t"]}</h2>{t["anual_html"]}<p class="nota-t">{t["anual_n"]}</p></section>
<div class="cta-l"><h2>{C["cta_t"]}</h2><p>{C["cta_p"]}</p><div class="acc"><a class="btn p" href="{r}{O["auditoria"]}">{C["cta_b"]}</a><a class="btn" href="{r}{O["libro"]}">{C["cta_l"]}</a></div></div>
<section class="lb-s faq"><h2>{C["faq"]}</h2>{"".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in t["faq"])}</section>
<section class="lb-s"><h2>{C["fuentes"]}</h2><ul class="pun"><li><a class="enl" href="{LAB}#{t["seccion_lab"]}" target="_blank" rel="noopener">{C["codigo"]}</a></li><li><a class="enl" href="https://data.binance.vision/" target="_blank" rel="noopener">Binance public data (data.binance.vision)</a></li></ul></section>
<section class="lb-s"><h2>{C["rel"]}</h2><ul class="rel"><li><a href="{r}{RUTAS[otra][lang]}">{nombre_otra}</a></li><li><a href="{r}{O["auditoria"]}">{nombre_aud}</a></li><li><a href="{lab}">{nombre_lab}</a></li></ul></section>
</article>'''
        miga_html = f'<nav class="miga" aria-label="breadcrumb"><a href="{home}">{C["inicio"]}</a><span>›</span><a href="{lab}">{C["lab"]}</a><span>›</span>{t["miga"]}</nav>'
    lds = "".join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False, separators=(",", ":")) + "</script>" for x in ld)
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(t["titulo"])}</title>
<meta name="description" content="{html.escape(t["desc"])}">
<link rel="canonical" href="{url}">{alt}
<meta property="og:type" content="article"><meta property="og:title" content="{html.escape(t["titulo"])}"><meta property="og:description" content="{html.escape(t["desc"])}"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITIO}/assets/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{r}assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@400;500;600&family=Geist:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}assets/v4.css">
<script>try{{var t=localStorage.getItem("wiqon-tema");if(t)document.documentElement.dataset.tema=t;}}catch(e){{}}</script>
<style>{CSS}</style>
{lds}
</head>
<body>
<div class="lb">
  <header class="lb-barra">
    <a class="marca" href="{home}"><span class="corona s"><img src="{r}assets/logo.png" alt="" width="34" height="34"></span><span>WIQON</span></a>
    <div class="der">
      <div class="idioma" aria-label="Idioma">{idioma}</div>
      <button class="tema-btn" type="button" aria-label="{C["tema"]}" title="{C["tema"]}"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="4.5"/><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8"/></svg></button>
    </div>
  </header>
  {miga_html}
  <main>{cuerpo}</main>
  <footer class="lb-pie">
    <div><a href="{r}{O["terminos"]}">{C["l_terminos"]}</a><a href="{r}{O["devoluciones"]}">{C["l_devoluciones"]}</a><a href="{r}{O["contacto"]}">{C["l_contacto"]}</a><a href="{r}{O["privacidad"]}">{C["l_privacidad"]}</a></div>
    <div>{C["aviso"]}</div><div>© 2026 WIQON</div>
  </footer>
</div>
<script>
  document.querySelector(".tema-btn").addEventListener("click", () => {{
    const r = document.documentElement; r.dataset.tema = r.dataset.tema === "claro" ? "oscuro" : "claro";
    try {{ localStorage.setItem("wiqon-tema", r.dataset.tema); }} catch (e) {{}}
  }});
</script>
<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "c394b4ca4e5144b19a861d3203511d84"}}'></script>
</body>
</html>
'''


if __name__ == "__main__":
    for lang in ("es", "pt-BR", "en"):
        for clave, fn in (("indice", indice), ("grid", grid), ("dca", dca)):
            destino = RAIZ / RUTAS[clave][lang] / "index.html"
            destino.parent.mkdir(parents=True, exist_ok=True)
            destino.write_text(pagina(lang, clave, fn(lang)), encoding="utf-8", newline="\n")
            print("OK", destino.relative_to(RAIZ))
