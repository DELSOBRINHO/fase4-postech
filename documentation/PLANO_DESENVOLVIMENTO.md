# PLANO DE DESENVOLVIMENTO — EXECUÇÃO NO CURSOR

**Projeto:** `tech-challenge-fase4-brent-oil`  
**IDE Recomendada:** Cursor AI / VS Code

---

## Estrutura de Diretórios

```text
tech-challenge-fase4-brent-oil/
├── .gitignore
├── README.md
├── requirements.txt
├── data/
│   ├── raw/
│   │   └── brent_oil_raw.csv
│   └── processed/
│       └── brent_oil_features.parquet
├── notebooks/
│   ├── 01_extracao_eda_brent.ipynb
│   └── 02_modelagem_forecasting.ipynb
├── src/
│   ├── __init__.py
│   ├── data_loader.py          # Extração e atualização IPEA
│   ├── feature_engineering.py  # Lags, médias móveis e sazonalidade
│   └── model_trainer.py        # Treinamento, validação temporal e salvamento
├── app/
│   ├── app.py                  # Aplicação Streamlit
│   ├── model.joblib            # Modelo serializado
│   └── config.py               # Configurações e estilos
└── documentation/
    ├── PLANO_MESTRE.md
    └── PLANO_DESENVOLVIMENTO.md
```

---

## Fases de Desenvolvimento

### FASE 1: Configuração do Ambiente e Extração dos Dados

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Implementar `src/data_loader.py` com extração da série oficial do IPEA Data:

- API OData `ValoresSerie(SERCODIGO='EIA366_PBRENT366')` (serid `1650971490`).
- Fallback HTML da página `ExibeSerie.aspx`.
- Conversão de datas para `datetime` e ordenação ascendente.
- Tratamento de dias sem cotação (calendário de negociação / *forward fill* opcional).
- Persistência em `data/raw/brent_oil_raw.csv` para o Streamlit Cloud não depender da API ao vivo.

### FASE 2: Análise Exploratória (EDA) & Contextualização Histórica

Desenvolver `notebooks/01_extracao_eda_brent.ipynb`:

- Trajetória histórica do Brent (1987 aos dias atuais).
- Anotação dos 5 maiores eventos geopolíticos:
  - 1990: Guerra do Golfo.
  - 2008: Crise dos Subprimes / Pico de US$ 140+.
  - 2014: Guerra de Preços da OPEP / Queda da demanda.
  - 2020: Pandemia de COVID-19.
  - 2022: Conflito Rússia-Ucrânia.
- Decomposição temporal (tendência, sazonalidade e resíduo).
- Teste de estacionariedade (Augmented Dickey-Fuller).

### FASE 3: Engenharia de Recursos & Modelagem Preditiva

Desenvolver `notebooks/02_modelagem_forecasting.ipynb` e `src/feature_engineering.py`:

- Lags: t−1, t−2, t−3, t−5, t−7, t−15, t−30.
- Médias móveis: 7, 14, 30 e 90 dias.
- Volatilidade móvel: 7 e 30 dias.
- Sazonalidade: dia da semana, mês e trimestre.
- Treinamento comparativo: Naive, Prophet (opcional), XGBoost, Random Forest, SARIMAX (opcional).
- Avaliação nos últimos 30 a 90 dias úteis (MAPE, RMSE, MAE, R²).
- Exportação do campeão para `app/model.joblib`.

### FASE 4: Aplicação Web Streamlit (`app/app.py`)

Três abas executivas:

1. **Previsão & Simulador Operacional** — último preço IPEA, curva projetada (7/15/30 dias úteis) com faixa de confiança e impacto financeiro por volume de barris.
2. **Análise Histórica & Geopolítica** — linha do tempo dos choques, volatilidade e médias móveis.
3. **Desempenho e Governança do Modelo** — MAPE, RMSE, MAE e real vs. previsto.

Importação Cloud-safe via `app/repo_path.py` (o mount `/mount/src` do Streamlit Cloud colide com o pacote `src`).

### FASE 5: Deploy e Entrega Final

```bash
python -m src.model_trainer
streamlit run app/app.py
```

Conectar o branch **`develop`** ao Streamlit Community Cloud (`app/app.py`), sem alterar o app já publicado no `main`.  
Preencher `entrega_tech_challenge_fase4.txt` com os links obrigatórios (app + notebook + repositório).
