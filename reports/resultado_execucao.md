# Resultado da execução do pipeline Olist

> Gerado pela execução real do pipeline; não contém números inventados.

## RAW: conferência dos dados originais

| Fonte | Linhas carregadas | Referência do curso | Conferência | SHA-256 do arquivo |
|---|---:|---:|---|---|
| orders | 99441 | 99441 | OK | `433c2fcea05d1670934310ad59d05fa8a20d06442b3d1229908bbb96c856dcf3` |
| customers | 99441 | 99441 | OK | `20414eab1e5e1b6178e10536fb4610188f1232253aaa639f6c1aa91aa7d843d2` |
| items | 112650 | 112650 | OK | `86216fee3bd68616cda276673e9aec96c488c6ce6f4e34bbc78de524f412a880` |
| reviews | 99224 | 99224 | OK | `d2353016ccb587437020854adbff359d44a5f5faecffaa198982071006de3b40` |

## REFINED: contagem após transformação

| Tabela | Linhas |
|---|---:|
| orders | 99441 |
| customers | 99441 |
| items | 112650 |
| reviews | 98673 |
| order_financials | 98666 |
| order_analysis | 99441 |

## MARTS: indicadores gerados

| Mart | Linhas |
|---|---:|
| avaliacoes_por_atraso | 2 |
| entregas_por_estado | 27 |
| entregas_por_mes | 23 |
| frete_por_estado | 27 |
| ranking_estados | 27 |

## Qualidade de dados

| Regra | Violações | Resultado |
|---|---:|---|
| unicidade_pedidos | 0 | APROVADO |
| dominio_avaliacoes | 0 | APROVADO |
| reconciliacao_estados_meses | 0 | APROVADO |

## Reconciliação

Os totais de entregas analisadas e atrasos dos marts por UF e por mês são comparados entre si e diretamente à camada REFINED, sem valores fixos.
