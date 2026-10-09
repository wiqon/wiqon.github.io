# El costo invisible de un robot de CFD

**WIQON Lab · octubre de 2026** · *Documentar, no prometer.*

> Informe educativo. Resultados pasados no garantizan rendimientos futuros. No es asesoría financiera.

## Resumen

Pusimos nuestra regla de tendencia en un Expert Advisor para MetaTrader 5 (WIQON Shield) y la probamos con **los costos reales de un broker**: una cuenta demo de Exness, símbolo BTCUSDm, del 23/03/2022 al 25/09/2026, con 10.000 USD de partida.

| Misma ventana (2022 → 2026) | Resultado | Caída máxima |
|---|---|---|
| WIQON Shield en CFD (spread + swaps reales) | **x2,02** | **39%** |
| Comprar y mantener BTC | x1,96 | 67% |
| La misma regla en BTC spot (Binance, 0,1% + 0,05% de slippage) | x2,67 | 37% |

## Qué es el swap

En un CFD no comprás Bitcoin: el broker te presta la posición y te cobra **financiación por cada noche** que la mantenés abierta. Una estrategia de tendencia, que pasa meses comprada, paga ese costo todos los días.

## Cuánto costó

| Concepto | Monto |
|---|---|
| Ganado por movimiento de precio | +14.475 USD |
| Pagado en swaps | **−4.241 USD** |
| Días con la posición abierta | 859 |
| Swap medio por día (0,23 BTC) | −4,94 USD |
| Costo anual aproximado sobre lo invertido | ≈ 10-11% |

Los swaps se llevaron **casi un tercio** de la ganancia que la misma regla obtuvo en spot.

## Otros datos de la prueba

- 33 operaciones; 21% ganadoras. Es normal en seguimiento de tendencia: pocas subidas grandes pagan muchas salidas chicas.
- Factor de beneficio 1,92: por cada dólar perdido se ganaron 1,92.

## Antes de usar cualquier robot en CFD

1. **Mirá el swap de tu broker.** En MT5: clic derecho en el símbolo → Especificación → "Swap largo".
2. **Probalo en el Probador de Estrategias** con esos costos y un período de varios años.
3. **Compará con comprar y mantener** y con la misma regla en spot.
4. **Si podés, usá spot** o una cuenta sin swap para cripto.

---

Informe completo y operaciones: **github.com/wiqon/wiqon-lab/tree/main/resultados/mt5** · wiqonlab.com · contacto@wiqonlab.com
