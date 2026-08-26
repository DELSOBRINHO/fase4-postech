# Plano Mestre e Estrutura de Entrega

**Tech Challenge Fase 4 (Hospitalar — Previsão de Obesidade)**  
FIAP POSTECH — Data Viz & Production Models

O desafio oficial da Fase 4 consiste em atuar como cientista de dados hospitalar para apoiar a equipe médica no diagnóstico precoce e classificação dos níveis de obesidade por meio de um modelo de Machine Learning, visualizações analíticas (dashboard) e deploy de uma aplicação no Streamlit.

---

## 1. Visão geral dos requisitos e entregáveis

| Requisito do desafio | Critério exigido | Implementação técnica |
| --- | --- | --- |
| **Pipeline de Machine Learning** | Feature engineering, pré-processamento e treino estruturado | `ColumnTransformer` + `Pipeline` (Scikit-Learn) tratando dados numéricos e categóricos, com IMC como atributo clínico |
| **Assertividade do modelo** | Acurácia mínima de **75%** no conjunto de teste | Random Forest / Gradient Boosting, com meta de **>94%** no hold-out estratificado |
| **Painel analítico** | Insights para a equipe médica (fatores de risco, hábitos, correlações) | Aba analítica no Streamlit com gráficos interativos (Plotly) |
| **Deploy da aplicação** | Aplicação web para diagnóstico interativo | Streamlit Cloud: [https://avaliapeso.streamlit.app/](https://avaliapeso.streamlit.app/) |
| **Repositório GitHub** | Código limpo e estruturado | Estrutura modular com `/data`, `/notebooks`, `/src`, `/app` e `/documentacao` |
| **Vídeo de apresentação** | 4 a 10 minutos com foco em visão médica e de negócio | Roteiro estruturado cobrindo problema, dados, arquitetura e demo do app |

---

## 2. Estrutura do repositório

```text
fase4-postech/
├── data/
│   └── Obesity.csv
├── notebooks/
│   ├── 01_eda_analise_medica.ipynb
│   └── 02_pipeline_modelagem.ipynb
├── app/
│   ├── app.py                     # Interface médica + dashboard
│   ├── model.joblib               # Modelo treinado e serializado
│   └── requirements.txt
├── src/
│   ├── data_pipeline.py           # Limpeza, IMC e ColumnTransformer
│   └── train.py                   # Treino, comparação e exportação
├── documentacao/
│   ├── 01-plano-mestre.md
│   ├── 02-plano-desenvolvimento-checklist.md
│   └── ...                        # Demais documentos do app
├── README.md
├── requirements.txt
└── entrega_tech_challenge_fase4.txt
```

---

## 3. Pipeline de Machine Learning e modelagem

### A. Tratamento de dados e engenharia de atributos

**Variáveis numéricas contínuas e de escala:** `Age`, `Height`, `Weight`, `FCVC`, `NCP`, `CH2O`, `FAF`, `TUE`.

**Variáveis categóricas e binárias:** `Gender`, `family_history`, `FAVC`, `CAEC`, `SMOKE`, `SCC`, `CALC`, `MTRANS`.

**Feature engineering:** cálculo do IMC como métrica clínica de apoio:

\[
IMC = \frac{Peso}{Altura^{2}}
\]

Normalização com `StandardScaler` e `OneHotEncoder`.

**Variável alvo (`Obesity`) — 7 classes alinhadas à classificação da OMS:**

1. *Insufficient_Weight*
2. *Normal_Weight*
3. *Overweight_Level_I*
4. *Overweight_Level_II*
5. *Obesity_Type_I*
6. *Obesity_Type_II*
7. *Obesity_Type_III*

### B. Código de treinamento e exportação (`src/train.py`)

O script oficial de treino:

1. Carrega `data/Obesity.csv`.
2. Deriva o IMC e monta `ColumnTransformer` (numérico + categórico).
3. Compara Random Forest e Gradient Boosting.
4. Divide treino/teste com `stratify`, avalia acurácia, CV e relatório por classe.
5. Serializa o campeão em `app/model.joblib`.

Hiperparâmetros de referência do Random Forest: `n_estimators=150`, `max_depth=12`, `random_state=42`.

Critério de aceite: acurácia de teste **≥ 75%**. Meta interna: **≥ 94%**, conforme linha de base validada no dataset (2.111 registros, 17 colunas).

---

## 4. Aplicação Streamlit integrada (`app/app.py`)

A aplicação atende aos dois requisitos principais:

1. **Sistema preditivo clínico** — formulário de dados biométricos, hábitos alimentares e estilo de vida; inferência em tempo real; IMC calculado; gráfico de probabilidade por classe.
2. **Dashboard analítico** — KPIs populacionais, distribuição dos níveis, histórico familiar, atividade física, consumo de água/calorias, correlações e importância de atributos.

Navegação em duas visões na barra lateral:

- Diagnóstico preditivo
- Painel analítico e insights

---

## 5. Roteiro do vídeo de apresentação (5 a 7 minutos)

Ver `documentacao/05-roteiro-video.md`.

- **Minuto 1:** problema de negócio (visão hospitalar)
- **Minuto 2:** exploração de dados e insights clínicos
- **Minuto 3:** engenharia de atributos e modelagem (pipeline + acurácia)
- **Minutos 4–5:** demonstração do Streamlit (diagnóstico + painel)
- **Minuto 6:** impacto no atendimento e conclusão

---

## 6. Arquivo de submissão

O template oficial está em `entrega_tech_challenge_fase4.txt` (raiz do repositório). Deve conter:

1. Link da aplicação em produção (Streamlit): https://avaliapeso.streamlit.app/
2. Link do repositório GitHub: https://github.com/DELSOBRINHO/fase4-postech
3. Link do painel analítico (aba da mesma aplicação): https://avaliapeso.streamlit.app/
4. Link do vídeo (YouTube / Loom) — ainda pendente

---

## 7. Linha de base já observada no dataset

- Shape: **(2111, 17)**
- Alvo: coluna `Obesity` com 7 classes relativamente balanceadas (272 a 351 observações)
- Random Forest de referência (100 árvores, split 80/20 estratificado): **acurácia de teste ≈ 94,09%**

Essa linha de base confirma que o critério mínimo de 75% é alcançável com a pipeline proposta.
