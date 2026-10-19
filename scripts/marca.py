"""
Datos estructurados (schema.org, JSON-LD) de la marca WIQON, compartidos por los generadores de páginas.

Le dicen a Google, Bing y los buscadores con IA qué es WIQON, cuál es su sitio oficial y cuáles son sus
perfiles en redes (sameAs): es lo que ayuda a que una búsqueda de "wiqon" muestre wiqonlab.com y el panel
de la marca. Si se abre una red nueva, agregarla en PERFILES.
"""
import json

SITIO = "https://wiqonlab.com"
ORG_ID = f"{SITIO}/#org"
PERFILES = [
    "https://www.instagram.com/wiqonlab/", "https://www.tiktok.com/@wiqonlab", "https://www.youtube.com/@wiqonlab",
    "https://x.com/wiqonlab", "https://www.facebook.com/wiqonlab/", "https://www.linkedin.com/company/wiqonlab",
    "https://t.me/wiqonlab", "https://github.com/wiqon",
    "https://www.instagram.com/wiqonbr/", "https://www.tiktok.com/@wiqonbr", "https://www.youtube.com/@wiqonbr", "https://x.com/wiqonbr",
]
DESC = {
    "es": "Laboratorio de trading de Paraguay y Brasil: probamos estrategias y bots con datos y costos reales, publicamos los resultados y construimos herramientas con lo que sobrevive.",
    "pt-BR": "Laboratório de trading do Paraguai e do Brasil: testamos estratégias e robôs com dados e custos reais, publicamos os resultados e construímos ferramentas com o que sobrevive.",
    "en": "Trading research lab from Paraguay and Brazil: we test strategies and bots with real data and real costs, publish the results and build tools from what survives.",
}


def _script(datos):
    return '<script type="application/ld+json">' + json.dumps(datos, ensure_ascii=False, separators=(",", ":")) + "</script>"


def organizacion(lang="es"):
    """Organización + sitio web: va en la portada de cada idioma."""
    return _script({"@context": "https://schema.org", "@graph": [
        {"@type": "Organization", "@id": ORG_ID, "name": "WIQON", "alternateName": ["WIQON Lab", "wiqonlab"],
         "url": f"{SITIO}/", "logo": f"{SITIO}/assets/logo.png", "image": f"{SITIO}/assets/og.png",
         "description": DESC.get(lang, DESC["es"]), "slogan": "Market Flow Intelligence",
         "founder": {"@type": "Person", "name": "Avelino González"},
         "address": {"@type": "PostalAddress", "addressCountry": "PY"}, "areaServed": ["PY", "BR", "419"],
         "email": "contacto@wiqonlab.com",
         "contactPoint": {"@type": "ContactPoint", "contactType": "customer support", "email": "contacto@wiqonlab.com",
                          "telephone": "+595987685651", "availableLanguage": ["es", "pt", "en"]},
         "sameAs": PERFILES},
        {"@type": "WebSite", "@id": f"{SITIO}/#web", "url": f"{SITIO}/", "name": "WIQON", "inLanguage": lang,
         "publisher": {"@id": ORG_ID}},
    ]})


def servicio(nombre, descripcion, url, lang, ofertas):
    """Servicio con sus planes. ofertas = [(nombre, precio_desde_usd), ...]; precio 0 = gratis."""
    return _script({"@context": "https://schema.org", "@type": "Service", "name": nombre, "description": descripcion,
                    "url": url, "inLanguage": lang, "serviceType": "Trading bot audit",
                    "provider": {"@type": "Organization", "@id": ORG_ID, "name": "WIQON", "url": f"{SITIO}/"},
                    "areaServed": ["PY", "BR", "419"],
                    "offers": [{"@type": "Offer", "name": n, "price": f"{p:.2f}", "priceCurrency": "USD"} for n, p in ofertas]})
