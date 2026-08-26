# Métricas do modelo (último treino)

Gerado por `python -m src.train`. Detalhe em `metricas_modelo.json`.

| Item | Valor |
| --- | --- |
| Linhas | 2.111 |
| Split | 80/20 estratificado, `random_state=42` |
| Atributos no modelo | 16 originais + IMC |
| Mínimo exigido | 75% |
| **Campeão** | **Gradient Boosting** |
| **Acurácia no teste** | **98,35%** |
| CV (5 folds, treino) | 97,51% ± 0,83% |

## Comparação

| Modelo | Acurácia teste | CV média |
| --- | ---: | ---: |
| Gradient Boosting | 98,35% | 97,51% |
| Random Forest (150 árvores, max_depth=12) | 97,87% | 98,28% |

Ambos superam o critério de 75% e a linha de base de ~94% (Random Forest sem IMC). O campeão serializado em `app/model.joblib` é o Gradient Boosting.
