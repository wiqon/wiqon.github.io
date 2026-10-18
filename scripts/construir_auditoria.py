"""
Genera la página del producto "Auditoría de bots" en tres idiomas:
  auditoria-bots/  (español) · br/auditoria-robos/ (português) · en/bot-audit/ (English)
Los ejemplos salen de experimentos publicados del laboratorio (github.com/wiqon/wiqon-lab).
Uso:  python scripts/construir_auditoria.py
"""
from pathlib import Path
from urllib.parse import quote

RAIZ = Path(__file__).resolve().parent.parent
WA = "https://wa.me/595987685651"
LAB = "https://github.com/wiqon/wiqon-lab"
PLATAFORMAS = "Cryptohopper · Bitsgap · 3Commas · Pionex · grids de Binance · EAs de MetaTrader 5"

T = {
    "es": dict(
        ruta="auditoria-bots", r="../", lang="es", inicio="../", contacto="../contacto/", terminos="../terminos/", devoluciones="../devoluciones/", privacidad="../privacidad/",
        titulo="Auditoría de bots de trading — WIQON", desc="Auditamos bots de Cryptohopper, Bitsgap, Pionex, grids de Binance y EAs de MetaTrader 5 con costos reales y pruebas fuera de muestra. Diagnóstico inicial gratis.",
        volver="← wiqonlab.com", tema="Cambiar entre tema claro y oscuro",
        h1="¿Tu bot gana, o solo tuvo un buen mes?",
        sub="Auditamos tu bot con el mismo método con el que descartamos 20 de nuestras propias ideas: costos reales, pruebas fuera de muestra y una comparación honesta contra no hacer nada. Si no tiene ventaja, te lo decimos.",
        plataformas=PLATAFORMAS + " · scripts propios",
        cta_wa="Pedir el diagnóstico gratis", wa_txt="Hola WIQON, quiero auditar mi bot.", cta_form="Escribir por el formulario",
        rev_t="Qué revisamos",
        revisa=[("Costos reales", "Comisiones, spread, funding y swaps: lo que el panel del bot no siempre descuenta."),
                ("Contra qué compite", "Tu resultado frente a comprar y mantener, y frente a dejar los dólares en una stablecoin que rinde."),
                ("Fuera de muestra", "Si la configuración funciona en períodos que no se usaron para elegirla."),
                ("Robustez", "Qué pasa si movés un poco los parámetros: rango del grid, cantidad de niveles, take profit."),
                ("La peor caída", "Cuánto perdió en su peor momento, cuánto tardó en recuperarse y qué habría pasado en un desplome como el de 2022."),
                ("Sesgos", "Monedas elegidas mirando el pasado, períodos favorables u operaciones que en la realidad no se habrían ejecutado.")],
        pasos_t="Cómo funciona",
        pasos=[("Diagnóstico gratis", "20 a 30 minutos por videollamada o WhatsApp: entendemos tu bot y te decimos si vale la pena auditarlo."),
               ("Propuesta por escrito", "Alcance, precio y plazo. Pagás solo si la aceptás."),
               ("Nos mandás los datos", "La configuración (capturas o exportación) y el historial de operaciones en CSV. Nunca pedimos contraseñas ni claves de API."),
               ("Informe y llamada", "Metodología, resultados con costos y una conclusión clara, explicada en una llamada.")],
        planes_t="Planes",
        planes=[("Diagnóstico", "Gratis", ["Videollamada o WhatsApp de 20 a 30 minutos", "Te decimos si tiene sentido auditar y qué datos hacen falta"]),
                ("Auditoría básica", "Desde USD 80", ["Revisión de la configuración", "Backtest con costos reales sobre el historial disponible", "Comparación contra comprar y mantener", "Informe escrito"]),
                ("Auditoría completa", "Desde USD 200", ["Todo lo de la básica", "Pruebas fuera de muestra y robustez de parámetros", "Escenarios de desplome y la peor caída", "Recomendaciones de tamaño y riesgo", "Llamada de entrega"])],
        planes_n="El precio final depende de la complejidad del bot y queda fijado en la propuesta, antes de pagar. Pagos con Binance / USDT, PYUSD o transferencia en Paraguay.",
        lab_t="Lo que ya encontramos en nuestro laboratorio",
        lab=[("Arbitraje entre 6 exchanges", "69 oportunidades en 24 horas; casi ninguna sobrevivía a las comisiones y al tiempo de transferencia."),
             ("Cobrar la tasa de financiación", "7 a 10 % anual en el histórico, casi todo de 2021; 2 a 3 % en 2025 y 2026."),
             ("Rotación de altcoins", "33,7 % anual con las monedas de hoy, 1,0 % con las de 2021: el sesgo de supervivencia infla todo."),
             ("Day trade con EMA21", "+0,71 % en 3 años, contra +9,3 % de dejar el dinero en Earn.")],
        lab_n="Todos los experimentos, con su código, están publicados en GitHub.", lab_link="Ver el laboratorio",
        faq_t="Preguntas frecuentes",
        faq=[("¿Necesitan acceso a mi cuenta?", "No. Trabajamos con capturas, exportaciones y el historial en CSV. Nunca pedimos contraseñas, códigos 2FA ni claves de API con permiso de retiro."),
             ("¿Y si el bot sí tiene ventaja?", "Te lo decimos, con los números y las condiciones en las que funciona, y también los escenarios en los que dejaría de hacerlo."),
             ("¿Garantizan algún resultado?", "No. Una auditoría mide lo que pasó y qué tan sólido es; ningún análisis garantiza ganancias futuras."),
             ("¿Es confidencial?", "Sí. Tu bot y tus datos no se publican ni se comparten sin tu permiso por escrito."),
             ("¿Cuánto tarda?", "El plazo queda en la propuesta según el alcance. La entrega es un informe escrito y una llamada.")],
        cierre_t="Antes de poner más dinero en tu bot, medilo.", cierre_p="El diagnóstico es gratis y en 30 minutos sabés si vale la pena auditarlo.",
        legal="© 2026 WIQON · Avelino González Melgarejo · C.I. 4.690.007", l_terminos="Términos y condiciones", l_devoluciones="Entregas y devoluciones", l_contacto="Contacto", l_privacidad="Privacidad",
        aviso="Contenido informativo y educativo; no es asesoría financiera. Operar implica riesgo de pérdida.",
    ),
    "pt": dict(
        ruta="br/auditoria-robos", r="../../", lang="pt-BR", inicio="../", contacto="../contato/", terminos="../termos/", devoluciones="../devolucoes/", privacidad="../privacidade/",
        titulo="Auditoria de robôs de trading — WIQON", desc="Auditamos robôs da Cryptohopper, Bitsgap, Pionex, grids da Binance e EAs de MetaTrader 5 com custos reais e testes fora da amostra. Diagnóstico inicial grátis.",
        volver="← wiqonlab.com/br", tema="Alternar entre tema claro e escuro",
        h1="Seu robô ganha, ou só teve um bom mês?",
        sub="Auditamos seu robô com o mesmo método com que descartamos 20 ideias nossas: custos reais, testes fora da amostra e uma comparação honesta contra não fazer nada. Se não tiver vantagem, a gente te diz.",
        plataformas="Cryptohopper · Bitsgap · 3Commas · Pionex · grids da Binance · EAs de MetaTrader 5 · scripts próprios",
        cta_wa="Pedir o diagnóstico grátis", wa_txt="Olá WIQON, quero auditar meu robô.", cta_form="Escrever pelo formulário",
        rev_t="O que revisamos",
        revisa=[("Custos reais", "Comissões, spread, funding e swaps: o que o painel do robô nem sempre desconta."),
                ("Contra o que compete", "Seu resultado contra comprar e segurar, e contra deixar os dólares numa stablecoin que rende."),
                ("Fora da amostra", "Se a configuração funciona em períodos que não foram usados para escolhê-la."),
                ("Robustez", "O que acontece se você mexer um pouco nos parâmetros: faixa do grid, quantidade de níveis, take profit."),
                ("A pior queda", "Quanto perdeu no pior momento, quanto demorou para se recuperar e o que teria acontecido numa queda como a de 2022."),
                ("Vieses", "Moedas escolhidas olhando o passado, períodos favoráveis ou operações que na prática não teriam sido executadas.")],
        pasos_t="Como funciona",
        pasos=[("Diagnóstico grátis", "20 a 30 minutos por videochamada ou WhatsApp: entendemos seu robô e dizemos se vale a pena auditá-lo."),
               ("Proposta por escrito", "Escopo, preço e prazo. Você só paga se aceitar."),
               ("Você envia os dados", "A configuração (prints ou exportação) e o histórico de operações em CSV. Nunca pedimos senhas nem chaves de API."),
               ("Relatório e chamada", "Metodologia, resultados com custos e uma conclusão clara, explicada numa chamada.")],
        planes_t="Planos",
        planes=[("Diagnóstico", "Grátis", ["Videochamada ou WhatsApp de 20 a 30 minutos", "Dizemos se faz sentido auditar e quais dados são necessários"]),
                ("Auditoria básica", "A partir de USD 80", ["Revisão da configuração", "Backtest com custos reais sobre o histórico disponível", "Comparação contra comprar e segurar", "Relatório escrito"]),
                ("Auditoria completa", "A partir de USD 200", ["Tudo da básica", "Testes fora da amostra e robustez de parâmetros", "Cenários de queda e a pior perda", "Recomendações de tamanho e risco", "Chamada de entrega"])],
        planes_n="O preço final depende da complexidade do robô e fica definido na proposta, antes do pagamento. Pagamento com Binance / USDT ou PYUSD.",
        lab_t="O que já encontramos no nosso laboratório",
        lab=[("Arbitragem entre 6 exchanges", "69 oportunidades em 24 horas; quase nenhuma sobrevivia às comissões e ao tempo de transferência."),
             ("Cobrar a taxa de financiamento", "7 a 10% ao ano no histórico, quase tudo de 2021; 2 a 3% em 2025 e 2026."),
             ("Rotação de altcoins", "33,7% ao ano com as moedas de hoje, 1,0% com as de 2021: o viés de sobrevivência infla tudo."),
             ("Day trade com EMA21", "+0,71% em 3 anos, contra +9,3% de deixar o dinheiro no Earn.")],
        lab_n="Todos os experimentos, com o código, estão publicados no GitHub.", lab_link="Ver o laboratório",
        faq_t="Perguntas frequentes",
        faq=[("Vocês precisam de acesso à minha conta?", "Não. Trabalhamos com prints, exportações e o histórico em CSV. Nunca pedimos senhas, códigos 2FA nem chaves de API com permissão de saque."),
             ("E se o robô tiver vantagem?", "A gente te diz, com os números e as condições em que funciona, e também os cenários em que deixaria de funcionar."),
             ("Vocês garantem algum resultado?", "Não. Uma auditoria mede o que aconteceu e o quanto é sólido; nenhuma análise garante lucros futuros."),
             ("É confidencial?", "Sim. Seu robô e seus dados não são publicados nem compartilhados sem sua permissão por escrito."),
             ("Quanto tempo leva?", "O prazo fica na proposta, conforme o escopo. A entrega é um relatório escrito e uma chamada.")],
        cierre_t="Antes de colocar mais dinheiro no seu robô, meça.", cierre_p="O diagnóstico é grátis e em 30 minutos você sabe se vale a pena auditar.",
        legal="© 2026 WIQON · Avelino González Melgarejo · C.I. 4.690.007 (Paraguai)", l_terminos="Termos e condições", l_devoluciones="Entregas e devoluções", l_contacto="Contato", l_privacidad="Privacidade",
        aviso="Conteúdo informativo e educacional; não é recomendação de investimento. Operar envolve risco de perda.",
    ),
    "en": dict(
        ruta="en/bot-audit", r="../../", lang="en", inicio="../", contacto="../contact/", terminos="../terms/", devoluciones="../refunds/", privacidad="../privacy/",
        titulo="Trading bot audit — WIQON", desc="We audit Cryptohopper, Bitsgap and Pionex bots, Binance grids and MetaTrader 5 EAs with real costs and out-of-sample tests. Free initial diagnosis.",
        volver="← wiqonlab.com/en", tema="Switch between light and dark theme",
        h1="Does your bot have an edge, or just a good month?",
        sub="We audit your bot with the same method we used to discard 20 of our own ideas: real costs, out-of-sample tests and an honest comparison against doing nothing. If it has no edge, we tell you.",
        plataformas="Cryptohopper · Bitsgap · 3Commas · Pionex · Binance grids · MetaTrader 5 EAs · custom scripts",
        cta_wa="Get the free diagnosis", wa_txt="Hi WIQON, I want to audit my bot.", cta_form="Use the contact form",
        rev_t="What we review",
        revisa=[("Real costs", "Fees, spread, funding and swaps: what the bot's dashboard doesn't always subtract."),
                ("What it competes against", "Your result against buy and hold, and against leaving the dollars in a yield-bearing stablecoin."),
                ("Out of sample", "Whether the settings work in periods that weren't used to choose them."),
                ("Robustness", "What happens if you nudge the parameters: grid range, number of levels, take profit."),
                ("The worst drawdown", "How much it lost at its worst, how long it took to recover and what a crash like 2022 would have done."),
                ("Biases", "Coins picked with hindsight, favorable periods or trades that wouldn't actually have filled.")],
        pasos_t="How it works",
        pasos=[("Free diagnosis", "20 to 30 minutes by video call or WhatsApp: we understand your bot and tell you whether an audit is worth it."),
               ("Written proposal", "Scope, price and timeline. You only pay if you accept."),
               ("You send the data", "The settings (screenshots or export) and the trade history as CSV. We never ask for passwords or API keys."),
               ("Report and call", "Methodology, results with costs and a clear conclusion, walked through on a call.")],
        planes_t="Plans",
        planes=[("Diagnosis", "Free", ["20 to 30 minute video call or WhatsApp", "We tell you whether an audit makes sense and what data is needed"]),
                ("Basic audit", "From USD 80", ["Settings review", "Backtest with real costs on the available history", "Comparison against buy and hold", "Written report"]),
                ("Full audit", "From USD 200", ["Everything in the basic audit", "Out-of-sample and parameter robustness tests", "Crash scenarios and worst drawdown", "Position sizing and risk recommendations", "Delivery call"])],
        planes_n="The final price depends on the bot's complexity and is fixed in the proposal, before you pay. Payment with Binance / USDT or PYUSD.",
        lab_t="What we've already found in our lab",
        lab=[("Arbitrage across 6 exchanges", "69 opportunities in 24 hours; almost none survived fees and transfer time."),
             ("Collecting the funding rate", "7–10% a year historically, almost all from 2021; 2–3% in 2025 and 2026."),
             ("Altcoin rotation", "33.7% a year with today's coins, 1.0% with 2021's: survivorship bias inflates everything."),
             ("EMA21 day trading", "+0.71% in 3 years, versus +9.3% from leaving the money in Earn.")],
        lab_n="Every experiment, with its code, is published on GitHub.", lab_link="See the lab",
        faq_t="Frequently asked questions",
        faq=[("Do you need access to my account?", "No. We work with screenshots, exports and the CSV trade history. We never ask for passwords, 2FA codes or API keys with withdrawal permission."),
             ("What if the bot does have an edge?", "We tell you, with the numbers and the conditions it works in, plus the scenarios where it would stop working."),
             ("Do you guarantee any result?", "No. An audit measures what happened and how solid it is; no analysis guarantees future profits."),
             ("Is it confidential?", "Yes. Your bot and your data are never published or shared without your written permission."),
             ("How long does it take?", "The timeline is set in the proposal according to scope. You get a written report and a call.")],
        cierre_t="Before you put more money into your bot, measure it.", cierre_p="The diagnosis is free, and in 30 minutes you'll know whether an audit is worth it.",
        legal="© 2026 WIQON · Avelino González Melgarejo · ID 4.690.007 (Paraguay)", l_terminos="Terms and conditions", l_devoluciones="Delivery and refunds", l_contacto="Contact", l_privacidad="Privacy",
        aviso="Informational and educational content; not financial advice. Trading involves risk of loss.",
    ),
}
ALTERNOS = {"es": "https://wiqonlab.com/auditoria-bots/", "pt-BR": "https://wiqonlab.com/br/auditoria-robos/", "en": "https://wiqonlab.com/en/bot-audit/"}


def pagina(t):
    r = t["r"]
    wa = f"{WA}?text={quote(t['wa_txt'])}"
    revisa = "".join(f"<li><h3>{a}</h3><p>{b}</p></li>" for a, b in t["revisa"])
    pasos = "".join(f'<li><span class="n">{i}</span><h3>{a}</h3><p>{b}</p></li>' for i, (a, b) in enumerate(t["pasos"], 1))
    planes = "".join(f'<article class="plan{" destacado" if i == 2 else ""}"><h3>{n}</h3><b>{pr}</b><ul>{"".join(f"<li>{x}</li>" for x in items)}</ul></article>'
                     for i, (n, pr, items) in enumerate(t["planes"]))
    lab = "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in t["lab"])
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in t["faq"])
    alt = "".join(f'<link rel="alternate" hreflang="{k}" href="{v}">' for k, v in ALTERNOS.items())
    return f'''<!doctype html>
<html lang="{t["lang"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t["titulo"]}</title>
<meta name="description" content="{t["desc"]}">
<link rel="canonical" href="https://wiqonlab.com/{t["ruta"]}/">{alt}
<meta property="og:title" content="{t["titulo"]}"><meta property="og:description" content="{t["desc"]}"><meta property="og:image" content="https://wiqonlab.com/assets/og.png">
<link rel="icon" href="{r}assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@400;500;600&family=Geist:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}assets/v4.css">
<script>try{{var t=localStorage.getItem("wiqon-tema");if(t)document.documentElement.dataset.tema=t;}}catch(e){{}}</script>
<style>
  .au {{ max-width: 1180px; margin: 0 auto; padding: 0 clamp(16px, 4vw, 48px); }}
  .au-barra {{ display: flex; align-items: center; gap: 16px; height: 72px; }}
  .au-barra .der {{ margin-left: auto; display: flex; gap: 10px; align-items: center; }}
  .au-hero {{ padding: clamp(40px, 7vw, 96px) 0 48px; max-width: 860px; }}
  .au-hero h1 {{ font: 500 clamp(36px, 5.2vw, 68px)/1.04 var(--titulos); letter-spacing: -.035em; text-wrap: balance; }}
  .au-hero .sub {{ margin-top: 22px; color: var(--suave); font-size: clamp(17px, 1.4vw, 19px); max-width: 60ch; }}
  .au-hero .plat {{ margin-top: 18px; color: var(--gris); font-size: 14px; }}
  .au-hero .acc {{ display: flex; gap: 12px; flex-wrap: wrap; margin-top: 30px; }}
  .au-s {{ padding: 56px 0; border-top: 1px solid var(--borde); }}
  .au-s h2 {{ font: 500 clamp(26px, 3vw, 38px)/1.1 var(--titulos); letter-spacing: -.03em; margin-bottom: 26px; }}
  .revisa {{ list-style: none; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1px; background: var(--borde); border: 1px solid var(--borde); border-radius: 16px; overflow: hidden; }}
  .revisa li {{ background: var(--sup); padding: 24px; }}
  .revisa h3, .pasos h3, .plan h3 {{ font: 500 18px/1.25 var(--titulos); letter-spacing: -.01em; }}
  .revisa p, .pasos p {{ color: var(--suave); font-size: 15px; margin-top: 8px; }}
  .pasos {{ list-style: none; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 20px; }}
  .pasos .n {{ display: inline-grid; place-items: center; width: 34px; height: 34px; border-radius: 50%; border: 1.5px solid var(--cian); color: var(--cian); font-weight: 600; margin-bottom: 12px; }}
  .planes {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 18px; }}
  .plan {{ background: var(--sup); border: 1px solid var(--borde); border-radius: 16px; padding: 26px; display: grid; align-content: start; gap: 10px; }}
  .plan.destacado {{ border-color: var(--cian); }}
  .plan > b {{ font: 500 26px/1.1 var(--titulos); letter-spacing: -.02em; }}
  .plan ul {{ list-style: none; display: grid; gap: 8px; margin-top: 6px; }}
  .plan li {{ color: var(--suave); font-size: 15px; padding-left: 22px; position: relative; }}
  .plan li::before {{ content: ""; position: absolute; left: 2px; top: .62em; width: 9px; height: 5px; border: solid var(--compra); border-width: 0 0 2px 2px; transform: rotate(-45deg); }}
  .nota-p {{ color: var(--gris); font-size: 14px; margin-top: 16px; max-width: 80ch; }}
  .lab {{ list-style: none; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px 28px; }}
  .lab li {{ display: grid; gap: 4px; padding: 16px 0; border-top: 1px solid var(--borde); }}
  .lab b {{ font-weight: 600; }} .lab span {{ color: var(--suave); font-size: 15px; }}
  .faq details {{ border-bottom: 1px solid var(--borde); padding: 16px 0; }}
  .faq summary {{ cursor: pointer; font-weight: 600; font-size: 17px; }}
  .faq p {{ color: var(--suave); margin-top: 8px; max-width: 75ch; }}
  .cierre {{ text-align: left; padding: 64px 0; border-top: 1px solid var(--borde); }}
  .cierre h2 {{ font: 500 clamp(26px, 3.2vw, 42px)/1.1 var(--titulos); letter-spacing: -.03em; max-width: 22ch; }}
  .cierre p {{ color: var(--suave); margin-top: 12px; }}
  .cierre .acc {{ display: flex; gap: 12px; flex-wrap: wrap; margin-top: 24px; }}
  .au-pie {{ border-top: 1px solid var(--borde); padding: 28px 0 48px; color: var(--gris); font-size: 14px; display: grid; gap: 8px; }}
  .au-pie a {{ color: var(--gris); margin-right: 14px; }}
  @media (max-width: 900px) {{ .revisa, .planes {{ grid-template-columns: 1fr; }} .pasos, .lab {{ grid-template-columns: 1fr 1fr; }} }}
  @media (max-width: 560px) {{ .pasos, .lab {{ grid-template-columns: 1fr; }} }}
  @media (max-width: 380px) {{ .au-barra .marca span:last-child {{ display: none; }} }}
</style>
</head>
<body>
<div class="au">
  <header class="au-barra">
    <a class="marca" href="{t["inicio"]}"><span class="corona s"><img src="{r}assets/logo.png" alt="" width="34" height="34"></span><span>WIQON</span></a>
    <div class="der">
      <div class="idioma" aria-label="Idioma"><a {"class=\"on\" " if t["lang"] == "es" else ""}href="{r}auditoria-bots/" lang="es">ES</a><a {"class=\"on\" " if t["lang"] == "pt-BR" else ""}href="{r}br/auditoria-robos/" lang="pt-BR">PT-BR</a><a {"class=\"on\" " if t["lang"] == "en" else ""}href="{r}en/bot-audit/" lang="en">EN</a></div>
      <button class="tema-btn" type="button" aria-label="{t["tema"]}" title="{t["tema"]}"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="4.5"/><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8"/></svg></button>
    </div>
  </header>
  <main>
    <section class="au-hero">
      <h1>{t["h1"]}</h1>
      <p class="sub">{t["sub"]}</p>
      <p class="plat">{t["plataformas"]}</p>
      <div class="acc"><a class="btn p" href="{wa}" target="_blank" rel="noopener">{t["cta_wa"]}</a><a class="btn" href="{t["contacto"]}">{t["cta_form"]}</a></div>
    </section>
    <section class="au-s"><h2>{t["rev_t"]}</h2><ul class="revisa">{revisa}</ul></section>
    <section class="au-s"><h2>{t["pasos_t"]}</h2><ol class="pasos">{pasos}</ol></section>
    <section class="au-s" id="planes"><h2>{t["planes_t"]}</h2><div class="planes">{planes}</div><p class="nota-p">{t["planes_n"]}</p></section>
    <section class="au-s"><h2>{t["lab_t"]}</h2><ul class="lab">{lab}</ul><p class="nota-p">{t["lab_n"]} <a class="enl" href="{LAB}" target="_blank" rel="noopener">{t["lab_link"]}</a></p></section>
    <section class="au-s faq"><h2>{t["faq_t"]}</h2>{faq}</section>
    <section class="cierre"><h2>{t["cierre_t"]}</h2><p>{t["cierre_p"]}</p><div class="acc"><a class="btn p" href="{wa}" target="_blank" rel="noopener">{t["cta_wa"]}</a><a class="btn" href="{t["contacto"]}">{t["cta_form"]}</a></div></section>
  </main>
  <footer class="au-pie">
    <div><a href="{t["terminos"]}">{t["l_terminos"]}</a><a href="{t["devoluciones"]}">{t["l_devoluciones"]}</a><a href="{t["contacto"]}">{t["l_contacto"]}</a><a href="{t["privacidad"]}">{t["l_privacidad"]}</a></div>
    <div>{t["aviso"]}</div><div>{t["legal"]}</div>
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
    for clave, t in T.items():
        destino = RAIZ / t["ruta"] / "index.html"
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(pagina(t), encoding="utf-8", newline="\n")
        print("OK", destino.relative_to(RAIZ))
