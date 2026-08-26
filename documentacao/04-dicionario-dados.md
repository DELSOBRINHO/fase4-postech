# Dicionário de dados — Obesity

Fonte: `dicionario_obesity_fiap.pdf` e inspeção de `data/Obesity.csv` (2.111 linhas, 17 colunas, zero nulos).

| Coluna | Significado | Tipo / valores |
| --- | --- | --- |
| `Gender` | Sexo biológico | `Female`, `Male` |
| `Age` | Idade em anos | numérico contínuo (mín. 14, máx. 61 no arquivo) |
| `Height` | Altura em metros | numérico contínuo (ex.: 1,45–1,98 m) |
| `Weight` | Peso em quilogramas | numérico contínuo (ex.: 39–173 kg) |
| `family_history` | Histórico familiar de excesso de peso | `yes`, `no` |
| `FAVC` | Consumo frequente de alimentos muito calóricos | `yes`, `no` |
| `FCVC` | Frequência de consumo de vegetais | escala 1–3 (1 raro, 2 às vezes, 3 sempre). Pode vir com decimais; na interpretação clínica arredonde |
| `NCP` | Número de refeições principais por dia | escala 1–4. Decimais: arredondar para interpretar |
| `CAEC` | Consumo de lanches entre refeições | `no`, `Sometimes`, `Frequently`, `Always` |
| `SMOKE` | Hábito de fumar | `yes`, `no` |
| `CH2O` | Consumo diário de água | 1 = <1 L/dia, 2 = 1–2 L/dia, 3 = >2 L/dia |
| `SCC` | Monitora a ingestão calórica diária | `yes`, `no` |
| `FAF` | Frequência semanal de atividade física | 0 = nenhuma, 1 ≈ 1–2×/sem, 2 ≈ 3–4×/sem, 3 = 5×/sem ou mais |
| `TUE` | Tempo diário em dispositivos eletrônicos | 0 ≈ 0–2 h/dia, 1 ≈ 3–5 h/dia, 2 = >5 h/dia |
| `CALC` | Consumo de álcool | `no`, `Sometimes`, `Frequently`, `Always` |
| `MTRANS` | Meio de transporte habitual | `Automobile`, `Motorbike`, `Bike`, `Public_Transportation`, `Walking` |
| `Obesity` | **Alvo** — nível de peso corporal | ver classes abaixo |

## Classes da variável alvo

| Valor no CSV | Leitura clínica |
| --- | --- |
| `Insufficient_Weight` | Abaixo do peso |
| `Normal_Weight` | Peso normal |
| `Overweight_Level_I` | Sobrepeso grau I |
| `Overweight_Level_II` | Sobrepeso grau II |
| `Obesity_Type_I` | Obesidade tipo I |
| `Obesity_Type_II` | Obesidade tipo II |
| `Obesity_Type_III` | Obesidade tipo III |

## Distribuição observada no arquivo de entrega

| Classe | n |
| --- | ---: |
| Obesity_Type_I | 351 |
| Obesity_Type_III | 324 |
| Obesity_Type_II | 297 |
| Overweight_Level_I | 290 |
| Overweight_Level_II | 290 |
| Normal_Weight | 287 |
| Insufficient_Weight | 272 |

O conjunto está relativamente balanceado; ainda assim o treino usa `stratify` para preservar as proporções no hold-out.

## Atributo derivado

| Atributo | Fórmula | Uso |
| --- | --- | --- |
| `IMC` | `Weight / Height²` | Feature de apoio clínico no modelo e cartão de referência OMS na interface |

O modelo **não** substitui o IMC pela classe da OMS no grau de obesidade: tipo I/II/III no diagnóstico segue as faixas 30 / 35 / 40 kg/m². Hábitos, histórico familiar e rotina entram no perfil de risco da triagem e no treino do modelo (abaixo de 30 kg/m² o classificador decide entre baixo peso, normal e sobrepeso).
