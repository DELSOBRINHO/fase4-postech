# Métricas do modelo de forecasting do Brent

Gerado por `python -m src.model_trainer` sobre a série oficial IPEA `EIA366_PBRENT366` (serid `1650971490`).

- **Observações (dias úteis):** 10.049 (1987-05-20 a 2026-08-25)
- **Último preço oficial:** US$ 88,24 (2026-08-25)
- **Campeão de produção:** Random Forest (menor MAPE entre os modelos serializáveis)
- **Baseline:** Naive lag-1 (passeio aleatório) — MAPE 3,19% no teste de 1 passo

## Teste temporal (últimos 60 dias úteis, sem shuffle)

| Modelo | MAPE | RMSE (US$) | MAE (US$) | R² |
| --- | ---: | ---: | ---: | ---: |
| Naive lag-1 | 3,19% | 3,68 | 2,79 | 0,856 |
| Random Forest (campeão) | 3,32% | 3,80 | 2,90 | 0,846 |
| XGBoost | 3,38% | 3,98 | 2,96 | 0,831 |
| SARIMAX | 16,41% | 15,77 | 12,87 | −1,66 |

## Backtest recursivo (a partir do fim do treino)

| Horizonte | MAPE | RMSE (US$) | MAE (US$) |
| ---: | ---: | ---: | ---: |
| 7 dias úteis | 2,24% | 2,68 | 2,15 |
| 15 dias úteis | 12,45% | 12,92 | 10,09 |
| 30 dias úteis | 23,10% | 19,71 | 17,22 |

A meta do plano mestre (MAPE ≤ 5% em 7–15 dias) é atendida no horizonte de **7 dias úteis** e no teste de 1 passo. Em 15 e 30 dias o erro recursivo cresce — padrão esperado em preço de commodity próximo de um passeio aleatório.

JSON máquina-a-máquina: [`metricas_modelo.json`](metricas_modelo.json).
