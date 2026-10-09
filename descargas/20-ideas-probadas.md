# 20+ ideas de trading probadas: cuál sobrevivió

**WIQON Lab · octubre de 2026** · *Documentar, no prometer.*

> Informe educativo. Resultados pasados no garantizan rendimientos futuros. No es asesoría financiera.

## La conclusión primero

Entre 2025 y 2026 probamos más de 20 familias de ideas de trading (84 variantes, en 8 criptomonedas) para un bot de corto plazo en Binance, y después revisamos las más prometedoras con backtests de portafolio de varios años. **Solo una regla sobrevivió**: el filtro de tendencia diario en Bitcoin. Todo lo demás está acá, con sus números.

## 1. El bot de corto plazo: 22 familias, 84 variantes

Cada familia se probó en la misma ventana corta, en BTC, ETH, SOL, XRP, ADA, DOGE, AVAX y LINK. La columna "mejor variante" muestra el **rendimiento medio por moneda** de la mejor configuración de cada familia.

| Idea probada | Variantes | Operaciones | Mejor variante | Promedio de la familia |
|---|---|---|---|---|
| Grilla (grid trading) | 4 | 8.194 | −6,64% | −10,63% |
| Reversión a la media (RSI bajo) | 9 | 4.987 | −1,78% | −8,83% |
| Divergencias RSI/MACD | 5 | 3.021 | −3,90% | −12,12% |
| Filtro con IA + técnica | 4 | 2.721 | −15,19% | −20,23% |
| Filtro de tendencia + ADX (intradía) | 4 | 2.196 | −14,42% | −18,79% |
| Torneo de estrategias | 3 | 1.443 | −1,70% | −14,25% |
| Combinaciones de filtros | 4 | 933 | −3,24% | −9,42% |
| Pullback con RSI | 5 | 904 | −3,59% | −8,23% |
| Salidas dinámicas (trailing stop) | 6 | 848 | −3,52% | −4,18% |
| TP/SL por volatilidad (ATR) | 6 | 318 | −1,70% | −3,06% |
| ADX mínimo | 4 | 291 | −1,70% | −3,86% |
| Filtros de rechazo | 9 | 280 | −0,25% | −1,33% |
| Pausa después de perder (cooldown) | 7 | 240 | −0,11% | −0,67% |
| Pullback + MACD + ATR | 3 | 225 | −2,77% | −4,08% |
| Cambio de régimen | 2 | 201 | −1,70% | −4,62% |
| Piezas sueltas del bot | 4 | 149 | +0,25% | −0,62% |
| Combo final | 4 | 116 | −0,09% | −0,67% |
| EMA21 + cooldown | 3 | 105 | −0,09% | −0,80% |
| Filtro por funding rate | 5 | 88 | +2,31% | +2,05% |
| EMA21 Bounce | 2 | 78 | −0,17% | −1,16% |
| Mismo bot en Bybit | 1 | 45 | −1,79% | −1,79% |
| Soporte + RSI | 2 | 34 | +0,25% | −0,07% |

**Lectura:** las únicas "mejores variantes" positivas tienen entre 28 y 31 operaciones repartidas en 8 monedas: muy pocas para distinguirlas de la suerte. Las ideas con miles de operaciones, que sí son medibles, perdieron.

## 2. Las candidatas revisadas en serio

| Hipótesis | Prueba | Resultado | Veredicto |
|---|---|---|---|
| Day trade EMA21 Bounce | Portafolio, 3 años, 178 operaciones, con costos | +0,71% total vs +9,3% en Earn; media por operación indistinguible de cero | ✕ No |
| Rotación semanal de altcoins | 5 años, con las monedas que existían en 2021 | 1,0% anual (33,7% si se eligen las monedas de hoy: sesgo de supervivencia) | ✕ No |
| Arbitraje entre 6 exchanges | 24 h observando precios en vivo | 69 oportunidades, casi ninguna real | ✕ No |
| Funding carry (spot + perpetuo) | 6 años de funding real | 7-10% anual promedio, casi todo de 2021; 2-3% en 2025-26 | ✕ No |
| BTC + ETH, tamaño por volatilidad | 36 variantes | No mejora de forma consistente | ✕ No |
| **Filtro de tendencia diario en BTC** | **8 años (2018-2026), con costos** | **56,6% anual vs 37,3% de mantener; caída máxima 34,7% vs 76,6%** | **✓ Sobrevive** |

## 3. Las 4 lecciones

1. **Con pocas operaciones, "la mejor" casi siempre es suerte.** Antes de creer en un resultado, contá operaciones y variantes probadas.
2. **Los costos cambian todo.** Comisiones, slippage y swaps convierten muchas estrategias "ganadoras" en perdedoras.
3. **Cuidado con el sesgo de supervivencia.** Probar solo con las monedas que hoy siguen vivas infla los resultados.
4. **Lo simple y medible le ganó a lo complejo.** La regla que sobrevivió cabe en una línea.

## La regla que sobrevivió

> Estar en BTC solo si el cierre diario está sobre su media de 100 días; si cae debajo, pasar a USDT.

En mercados que suben sin parar rinde menos que mantener. Su valor es **proteger en las caídas**. La operamos con capital real desde septiembre de 2026 y su estado se publica cada día en **wiqonlab.com**.

---

Código y datos de las pruebas de portafolio: **github.com/wiqon/wiqon-lab** · Contacto: contacto@wiqonlab.com
