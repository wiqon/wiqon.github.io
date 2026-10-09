# 20+ ideias de trading testadas: qual sobreviveu

**WIQON Lab · outubro de 2026** · *Documentar, não prometer.*

> Relatório educacional. Resultados passados não garantem rendimentos futuros. Não é recomendação de investimento.

## A conclusão primeiro

Entre 2025 e 2026 testamos mais de 20 famílias de ideias de trading (84 variações, em 8 criptomoedas) para um robô de curto prazo na Binance, e depois revisamos as mais promissoras com backtests de portfólio de vários anos. **Só uma regra sobreviveu**: o filtro de tendência diário no Bitcoin. Todo o resto está aqui, com os números.

## 1. O robô de curto prazo: 22 famílias, 84 variações

Cada família foi testada na mesma janela curta, em BTC, ETH, SOL, XRP, ADA, DOGE, AVAX e LINK. A coluna "melhor variação" mostra o **rendimento médio por moeda** da melhor configuração de cada família.

| Ideia testada | Variações | Operações | Melhor variação | Média da família |
|---|---|---|---|---|
| Grade (grid trading) | 4 | 8.194 | −6,64% | −10,63% |
| Reversão à média (RSI baixo) | 9 | 4.987 | −1,78% | −8,83% |
| Divergências RSI/MACD | 5 | 3.021 | −3,90% | −12,12% |
| Filtro com IA + técnica | 4 | 2.721 | −15,19% | −20,23% |
| Filtro de tendência + ADX (intraday) | 4 | 2.196 | −14,42% | −18,79% |
| Torneio de estratégias | 3 | 1.443 | −1,70% | −14,25% |
| Combinações de filtros | 4 | 933 | −3,24% | −9,42% |
| Pullback com RSI | 5 | 904 | −3,59% | −8,23% |
| Saídas dinâmicas (trailing stop) | 6 | 848 | −3,52% | −4,18% |
| TP/SL por volatilidade (ATR) | 6 | 318 | −1,70% | −3,06% |
| ADX mínimo | 4 | 291 | −1,70% | −3,86% |
| Filtros de rejeição | 9 | 280 | −0,25% | −1,33% |
| Pausa depois de perder (cooldown) | 7 | 240 | −0,11% | −0,67% |
| Pullback + MACD + ATR | 3 | 225 | −2,77% | −4,08% |
| Mudança de regime | 2 | 201 | −1,70% | −4,62% |
| Peças soltas do robô | 4 | 149 | +0,25% | −0,62% |
| Combo final | 4 | 116 | −0,09% | −0,67% |
| EMA21 + cooldown | 3 | 105 | −0,09% | −0,80% |
| Filtro por funding rate | 5 | 88 | +2,31% | +2,05% |
| EMA21 Bounce | 2 | 78 | −0,17% | −1,16% |
| Mesmo robô na Bybit | 1 | 45 | −1,79% | −1,79% |
| Suporte + RSI | 2 | 34 | +0,25% | −0,07% |

**Leitura:** as únicas "melhores variações" positivas têm entre 28 e 31 operações divididas em 8 moedas: poucas demais para separar de sorte. As ideias com milhares de operações, que são mensuráveis, perderam.

## 2. As candidatas revisadas a sério

| Hipótese | Teste | Resultado | Veredito |
|---|---|---|---|
| Day trade EMA21 Bounce | Portfólio, 3 anos, 178 operações, com custos | +0,71% total contra +9,3% no Earn; média por operação indistinguível de zero | ✕ Não |
| Rotação semanal de altcoins | 5 anos, com as moedas que existiam em 2021 | 1,0% ao ano (33,7% escolhendo as moedas de hoje: viés de sobrevivência) | ✕ Não |
| Arbitragem entre 6 exchanges | 24 h observando preços ao vivo | 69 oportunidades, quase nenhuma real | ✕ Não |
| Funding carry (spot + perpétuo) | 6 anos de funding real | 7-10% ao ano em média, quase tudo de 2021; 2-3% em 2025-26 | ✕ Não |
| BTC + ETH, tamanho por volatilidade | 36 variações | Não melhora de forma consistente | ✕ Não |
| **Filtro de tendência diário no BTC** | **8 anos (2018-2026), com custos** | **56,6% ao ano contra 37,3% de segurar; queda máxima 34,7% contra 76,6%** | **✓ Sobrevive** |

## 3. As 4 lições

1. **Com poucas operações, "a melhor" quase sempre é sorte.** Antes de acreditar num resultado, conte operações e variações testadas.
2. **Os custos mudam tudo.** Taxas, slippage e swaps transformam muitas estratégias "vencedoras" em perdedoras.
3. **Cuidado com o viés de sobrevivência.** Testar só com as moedas que continuam vivas hoje infla os resultados.
4. **O simples e mensurável venceu o complexo.** A regra que sobreviveu cabe em uma linha.

## A regra que sobreviveu

> Ficar em BTC só se o fechamento diário estiver acima da média de 100 dias; se cair abaixo, passar para USDT.

Em mercados que só sobem, rende menos que segurar. O valor dela é **proteger nas quedas**. Operamos com capital real desde setembro de 2026 e o estado é publicado todo dia em **wiqonlab.com/br**.

---

Código e dados dos testes de portfólio: **github.com/wiqon/wiqon-lab** · Contato: contacto@wiqonlab.com
