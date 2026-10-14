"""
Páginas de venta del libro de WIQON en tres idiomas:
  /libro/      ¿Ventaja o suerte?   (español)
  /br/livro/   Vantagem ou sorte?   (português)
  /en/book/    Edge or Luck?        (English)

    python scripts/construir_libro.py
Las imágenes de muestra (libro/img/) salen de los PDF en C:\\wiqon-productos\\ebook.
Los botones de compra con tarjeta se completan en COMPRA cuando estén los links (Lemon Squeezy, Hotmart).
"""
import html
from pathlib import Path
from urllib.parse import quote

RAIZ = Path(__file__).resolve().parent.parent
WHATSAPP = "595987685651"
BEACON = '<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon=\'{"token": "c394b4ca4e5144b19a861d3203511d84"}\'></script>'

# Links de pago con tarjeta: se completan cuando existan (vacío = "próximamente")
COMPRA = {"es": "https://pay.hotmart.com/K108005565Y", "pt": "https://pay.hotmart.com/Y108004979L", "en": "https://pay.hotmart.com/G108005645T"}

T = {
    "es": dict(
        ruta="libro", lang="es", lema_marca="Documentar, no prometer", img="es", raiz="../", titulo="¿Ventaja o suerte?",
        meta="Cómo evaluar una estrategia de trading antes de arriesgar tu dinero. Libro de WIQON Lab con datos reales: las 5 trampas de los backtests, 7 preguntas, 5 casos y un checklist.",
        kicker="LIBRO · WIQON LAB", sub="Cómo evaluar una estrategia de trading antes de arriesgar tu dinero",
        lema="No busques una promesa. Exigí una prueba.",
        intro="Probamos más de 20 ideas de trading con datos reales y costos reales. Sobrevivió una sola. Este libro te da las preguntas que separan una ventaja real de un golpe de suerte, para que puedas evaluar cualquier estrategia, robot o señal antes de poner tu dinero.",
        incluye_t="Qué vas a encontrar",
        incluye=["Las 5 trampas que hacen que un backtest salga demasiado bien",
                 "Las 7 preguntas que tenés que hacerle a cualquier estrategia o robot",
                 "5 casos reales del laboratorio, con sus números: la estrategia que era suerte, el sesgo de supervivencia, el costo de los swaps",
                 "Un protocolo de 7 pasos para auditar antes de arriesgar",
                 "Un checklist para imprimir y un semáforo para decidir"],
        datos="16 páginas · PDF · Edición octubre 2026 · Ing. Avelino González",
        precio="USD 9,99", comprar_wa="Comprar por WhatsApp", wa_texto="Hola WIQON, quiero el libro ¿Ventaja o suerte?",
        medios="Tarjeta de crédito o débito por Hotmart (entrega automática del PDF por correo). También por WhatsApp: transferencia en Paraguay (en guaraníes), Binance / USDT o PYUSD.",
        tarjeta="💳 Pago con tarjeta: muy pronto", tarjeta_btn="Pagar con tarjeta",
        muestra_t="Mirá algunas páginas", otros="También disponible en", otros_l=[("Português", "../br/livro/"), ("English", "../en/book/")],
        aviso="Material educativo. No es asesoría financiera ni garantiza resultados.", volver="← Volver a wiqonlab.com"),
    "pt": dict(
        ruta="br/livro", lang="pt-BR", lema_marca="Documentar, não prometer", img="pt", raiz="../../", titulo="Vantagem ou sorte?",
        meta="Como avaliar uma estratégia de trading antes de arriscar seu dinheiro. Livro da WIQON Lab com dados reais: as 5 armadilhas dos backtests, 7 perguntas, 5 casos e um checklist.",
        kicker="LIVRO · WIQON LAB", sub="Como avaliar uma estratégia de trading antes de arriscar seu dinheiro",
        lema="Não procure uma promessa. Exija uma prova.",
        intro="Testamos mais de 20 ideias de trading com dados reais e custos reais. Só uma sobreviveu. Este livro te dá as perguntas que separam uma vantagem real de um golpe de sorte, para você avaliar qualquer estratégia, robô ou sinal antes de colocar seu dinheiro.",
        incluye_t="O que você vai encontrar",
        incluye=["As 5 armadilhas que fazem um backtest sair bom demais",
                 "As 7 perguntas que você deve fazer a qualquer estratégia ou robô",
                 "5 casos reais do laboratório, com os números: a estratégia que era sorte, o viés de sobrevivência, o custo dos swaps",
                 "Um protocolo de 7 passos para auditar antes de arriscar",
                 "Um checklist para imprimir e um semáforo para decidir"],
        datos="16 páginas · PDF · Edição outubro 2026 · Eng. Avelino González",
        precio="USD 9,99", comprar_wa="Comprar pelo WhatsApp", wa_texto="Olá WIQON, quero o livro Vantagem ou sorte?",
        medios="Cartão ou PIX pela Hotmart (R$ 49,90, entrega automática do PDF). Também aceitamos USDT (rede TRC20) ou PYUSD (rede Solana) pelo WhatsApp.",
        tarjeta="💳 Pagamento com cartão e PIX: em breve", tarjeta_btn="Pagar com cartão ou PIX",
        muestra_t="Veja algumas páginas", otros="Também disponível em", otros_l=[("Español", "../../libro/"), ("English", "../../en/book/")],
        aviso="Material educativo. Não é recomendação de investimento nem garante resultados.", volver="← Voltar para wiqonlab.com/br"),
    "en": dict(
        ruta="en/book", lang="en", lema_marca="Document, don't promise", img="en", raiz="../../", titulo="Edge or Luck?",
        meta="How to evaluate a trading strategy before you risk your money. A WIQON Lab book built on real data: 5 backtest traps, 7 questions, 5 cases and a checklist.",
        kicker="BOOK · WIQON LAB", sub="How to evaluate a trading strategy before you risk your money",
        lema="Don't look for a promise. Demand proof.",
        intro="We tested more than 20 trading ideas with real data and real costs. Only one survived. This book gives you the questions that separate a real edge from a lucky streak, so you can evaluate any strategy, bot or signal before putting your money in.",
        incluye_t="What's inside",
        incluye=["The 5 traps that make a backtest look too good",
                 "The 7 questions to ask any strategy or trading bot",
                 "5 real cases from the lab, with their numbers: the strategy that was luck, survivorship bias, the cost of swaps",
                 "A 7-step protocol to audit before you risk",
                 "A printable checklist and a traffic light to decide"],
        datos="16 pages · PDF · October 2026 edition · Avelino González, Eng.",
        precio="USD 9.99", comprar_wa="Buy via WhatsApp", wa_texto="Hi WIQON, I want the book Edge or Luck?",
        medios="Card payment through Hotmart, with instant delivery of the PDF by email. You can also pay with USDT (TRC20) or PYUSD (Solana) via WhatsApp.",
        tarjeta="💳 Card payments: coming soon", tarjeta_btn="Pay by card",
        muestra_t="Take a look inside", otros="Also available in", otros_l=[("Español", "../../libro/"), ("Português", "../../br/livro/")],
        aviso="Educational material. Not financial advice and no guaranteed results.", volver="← Back to wiqonlab.com"),
}

CSS = """
:root{--tinta:#172334;--gris:#56616d;--crema:#f4f2e9;--papel:#fffdf9;--naranja:#ef7044;--verde:#4b8a82;--noche:#0f1a2a;--linea:#dddbd4}
*{box-sizing:border-box}
body{margin:0;background:var(--crema);color:var(--tinta);font-family:'Lato',system-ui,sans-serif;line-height:1.55}
a{color:inherit}
.cab{background:var(--noche);color:#fffefa}
.cab .in{max-width:1080px;margin:0 auto;padding:16px;display:flex;justify-content:space-between;align-items:center}
.cab a{text-decoration:none;font-weight:900;letter-spacing:.08em;font-size:.9rem}
.cab small{color:#aebbc9;font-size:.8rem}
.hero{background:var(--noche);color:#fffefa;padding:24px 16px 56px}
.hero .in{max-width:1080px;margin:0 auto;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);gap:40px;align-items:center}
.hero .in>*{min-width:0}
.hero img{width:100%;max-width:380px;border-radius:6px;box-shadow:0 18px 50px rgba(0,0,0,.45);display:block;margin:0 auto}
.kicker{color:var(--naranja);font-weight:900;letter-spacing:.1em;font-size:.78rem}
h1{font-size:clamp(2.2rem,5vw,3.4rem);line-height:1.02;margin:.3em 0 .25em;font-weight:900}
.sub{font-size:1.15rem;color:#d7dee6;margin:0 0 1.2em}
.lema{border-left:3px solid var(--verde);padding:.4em .9em;font-weight:900;margin:0 0 1.4em}
.precio{font-size:2rem;font-weight:900;margin:.2em 0}
.btn{display:inline-block;background:var(--naranja);color:#fff;text-decoration:none;font-weight:900;padding:14px 22px;border-radius:8px;margin:6px 8px 6px 0}
.btn.sec{background:transparent;border:1px solid #3a4a63;color:#d7dee6;cursor:default}
.medios{font-size:.88rem;color:#aebbc9;max-width:520px}
main{max-width:1080px;margin:0 auto;padding:40px 16px}
h2{font-size:1.6rem;margin:0 0 .6em;font-weight:900}
.intro{font-size:1.12rem;max-width:760px}
.lista{list-style:none;padding:0;display:grid;gap:10px;max-width:760px}
.lista li{background:var(--papel);border-radius:8px;padding:12px 14px 12px 42px;position:relative}
.lista li::before{content:"";position:absolute;left:16px;top:18px;width:10px;height:10px;border-radius:50%;background:var(--naranja)}
.muestra{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;margin-top:8px}
.muestra img{width:100%;border-radius:6px;box-shadow:0 6px 22px rgba(23,35,52,.15);display:block}
.datos{color:var(--gris);font-size:.9rem;margin-top:1em}
.otros{margin-top:28px;font-size:.95rem}
.otros a{font-weight:700;margin-right:12px}
footer{border-top:1px solid var(--linea);color:var(--gris);font-size:.82rem;text-align:center;padding:24px 16px 40px}
@media (max-width:760px){.hero .in{grid-template-columns:minmax(0,1fr);gap:24px}.hero img{max-width:240px}.cab small{display:none}.btn{display:block;text-align:center;margin:8px 0}}
"""


LEGALES = {  # páginas legales (pedidas por los procesadores de pago); en inglés se enlazan las de español
    "es": '<a href="{r}terminos/">Términos y condiciones</a> · <a href="{r}devoluciones/">Entregas y devoluciones</a> · <a href="{r}contacto/">Contacto</a>',
    "pt": '<a href="{r}br/termos/">Termos e condições</a> · <a href="{r}br/devolucoes/">Entregas e devoluções</a> · <a href="{r}br/contato/">Contato</a>',
    "en": '<a href="{r}terminos/">Terms (Spanish)</a> · <a href="{r}devoluciones/">Delivery &amp; refunds (Spanish)</a> · <a href="{r}contacto/">Contact</a>',
}


def pagina(cod):
    t = T[cod]
    esc = html.escape
    wa = f"https://wa.me/{WHATSAPP}?text={quote(t['wa_texto'])}"
    tarjeta = (f'<a class="btn" href="{esc(COMPRA[cod])}" target="_blank" rel="noopener">{t["tarjeta_btn"]}</a>' if COMPRA[cod]
               else f'<span class="btn sec">{t["tarjeta"]}</span>')
    url = f"https://wiqonlab.com/{t['ruta']}/"
    portada = f"{t['raiz']}libro/img/{t['img']}_p01.jpg"
    return f"""<!doctype html>
<html lang="{t['lang']}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(t['titulo'])} · WIQON Lab</title>
<meta name="description" content="{esc(t['meta'])}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="es" href="https://wiqonlab.com/libro/"><link rel="alternate" hreflang="pt-BR" href="https://wiqonlab.com/br/livro/"><link rel="alternate" hreflang="en" href="https://wiqonlab.com/en/book/">
<meta property="og:type" content="book"><meta property="og:title" content="{esc(t['titulo'])} · WIQON Lab"><meta property="og:description" content="{esc(t['sub'])}">
<meta property="og:image" content="https://wiqonlab.com/libro/img/{t['img']}_p01.jpg"><meta property="og:url" content="{url}">
<link rel="icon" href="{t['raiz']}assets/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700;900&display=swap" rel="stylesheet">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Book","name":"{esc(t['titulo'])}","inLanguage":"{t['lang']}","author":{{"@type":"Person","name":"Avelino González"}},"publisher":{{"@type":"Organization","name":"WIQON Lab","url":"https://wiqonlab.com"}},"numberOfPages":16,"bookFormat":"https://schema.org/EBook","offers":{{"@type":"Offer","price":"9.99","priceCurrency":"USD","availability":"https://schema.org/InStock"}}}}</script>
<style>{CSS}</style></head><body>
<div class="cab"><div class="in"><a href="{t['raiz']}">WIQON LAB</a><small>{t["lema_marca"]}</small></div></div>
<section class="hero"><div class="in">
 <img src="{portada}" alt="{esc(t['titulo'])}" width="642" height="909">
 <div><div class="kicker">{t['kicker']}</div><h1>{esc(t['titulo'])}</h1><p class="sub">{esc(t['sub'])}</p>
  <div class="lema">{esc(t['lema'])}</div>
  <div class="precio">{t['precio']}</div>
  <a class="btn" href="{wa}" target="_blank" rel="noopener">{t['comprar_wa']}</a>{tarjeta}
  <p class="medios">{esc(t['medios'])}</p></div>
</div></section>
<main>
 <p class="intro">{esc(t['intro'])}</p>
 <h2 style="margin-top:1.6em">{t['incluye_t']}</h2>
 <ul class="lista">{''.join(f'<li>{esc(x)}</li>' for x in t['incluye'])}</ul>
 <p class="datos">{esc(t['datos'])}</p>
 <h2 style="margin-top:1.8em">{t['muestra_t']}</h2>
 <div class="muestra">{''.join(f'<img loading="lazy" src="{t["raiz"]}libro/img/{t["img"]}_p{n:02d}.jpg" alt="{esc(t["titulo"])} · {n}" width="642" height="909">' for n in (5, 8, 13))}</div>
 <p class="otros">{t['otros']}: {''.join(f'<a href="{h}">{n}</a>' for n, h in t['otros_l'])}</p>
 <p><a href="{t['raiz']}{'br/' if cod == 'pt' else ''}">{t['volver']}</a></p>
</main>
<footer>{esc(t['aviso'])}<br>{LEGALES[cod].format(r=t['raiz'])}<br>© 2026 WIQON · Avelino González Melgarejo · C.I. 4.690.007 · contacto@wiqonlab.com</footer>
{BEACON}
</body></html>
"""


if __name__ == "__main__":
    for cod in T:
        destino = RAIZ / T[cod]["ruta"] / "index.html"
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(pagina(cod), encoding="utf-8")
        print("OK", destino.relative_to(RAIZ))
