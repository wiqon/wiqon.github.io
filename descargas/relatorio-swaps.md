# O custo invisível de um robô de CFD

**WIQON Lab · outubro de 2026** · *Documentar, não prometer.*

> Relatório educacional. Resultados passados não garantem rendimentos futuros. Não é recomendação de investimento.

## Resumo

Colocamos a nossa regra de tendência num Expert Advisor para MetaTrader 5 (WIQON Shield) e testamos com **os custos reais de uma corretora**: uma conta demo da Exness, ativo BTCUSDm, de 23/03/2022 a 25/09/2026, com 10.000 USD iniciais.

| Mesma janela (2022 → 2026) | Resultado | Queda máxima |
|---|---|---|
| WIQON Shield em CFD (spread + swaps reais) | **x2,02** | **39%** |
| Comprar e segurar BTC | x1,96 | 67% |
| A mesma regra em BTC spot (Binance, 0,1% + 0,05% de slippage) | x2,67 | 37% |

## O que é o swap

No CFD você não compra Bitcoin: a corretora te empresta a posição e cobra **financiamento por cada noite** que ela fica aberta. Uma estratégia de tendência, que passa meses comprada, paga esse custo todos os dias.

## Quanto custou

| Item | Valor |
|---|---|
| Ganho com o movimento do preço | +14.475 USD |
| Pago em swaps | **−4.241 USD** |
| Dias com a posição aberta | 859 |
| Swap médio por dia (0,23 BTC) | −4,94 USD |
| Custo anual aproximado sobre o investido | ≈ 10-11% |

Os swaps levaram **quase um terço** do ganho que a mesma regra teve no spot.

## Outros dados do teste

- 33 operações; 21% vencedoras. É normal em seguimento de tendência: poucas altas grandes pagam muitas saídas pequenas.
- Fator de lucro 1,92: para cada dólar perdido, ganhou 1,92.

## Antes de usar qualquer robô em CFD

1. **Veja o swap da sua corretora.** No MT5: clique direito no ativo → Especificação → "Swap comprado".
2. **Teste no Testador de Estratégias** com esses custos e um período de vários anos.
3. **Compare com comprar e segurar** e com a mesma regra no spot.
4. **Se puder, use spot** ou uma conta sem swap para cripto.

---

Relatório completo e operações: **github.com/wiqon/wiqon-lab/tree/main/resultados/mt5** · wiqonlab.com/br · contacto@wiqonlab.com
