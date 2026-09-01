# Sistema preditivo do preço do petróleo Brent

Tech Challenge Fase 4 — **Prova Substitutiva** (FIAP POSTECH Data Analytics).

Solução ponta a ponta para projetar o preço diário do barril **Brent FOB em US$**, com pipeline de séries temporais e aplicação Streamlit de apoio à diretoria e à mesa de trading.

## O problema

A oscilação do Brent impacta caixa, CAPEX/OPEX, hedges e precificação de combustíveis. A entrega oficial pede um modelo preditivo instanciado em uma aplicação Streamlit, usando a série do IPEA Data (serid `1650971490` / `EIA366_PBRENT366`).

Este repositório entrega:

1. Extração da série oficial (API OData + fallback HTML) e CSV versionado.
2. Engenharia de lags, médias móveis, volatilidade e calendário — sem shuffle.
3. Comparação temporal (Naive, Random Forest, XGBoost; Prophet/SARIMAX/LightGBM quando disponíveis).
4. Modelo campeão serializado em `app/model.joblib`.
5. App Streamlit com previsão (7/15/30 dias úteis), simulador financeiro, linha do tempo geopolítica e métricas.

Planos: [`documentation/PLANO_MESTRE.md`](documentation/PLANO_MESTRE.md) e [`documentation/PLANO_DESENVOLVIMENTO.md`](documentation/PLANO_DESENVOLVIMENTO.md).

## Estrutura

```text
data/raw/brent_oil_raw.csv
data/processed/brent_oil_features.parquet
notebooks/01_extracao_eda_brent.ipynb
notebooks/02_modelagem_forecasting.ipynb
src/data_loader.py
src/feature_engineering.py
src/model_trainer.py
app/app.py
app/model.joblib
documentation/PLANO_MESTRE.md
entrega_tech_challenge_fase4.txt
```

## Como executar

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.model_trainer
streamlit run app/app.py
```

O treino grava `app/model.joblib`, `data/processed/brent_oil_features.parquet` e `documentation/metricas_modelo.json`.

## Dados

Série IPEA [Petróleo bruto Brent (FOB)](http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view).  
O app tenta atualizar a API; se o IPEA estiver instável, usa o CSV em `data/raw/`.

## Notebooks (entrega obrigatória)

- [`notebooks/01_extracao_eda_brent.ipynb`](notebooks/01_extracao_eda_brent.ipynb) — extração, trajetória, choques, decomposição e ADF.
- [`notebooks/02_modelagem_forecasting.ipynb`](notebooks/02_modelagem_forecasting.ipynb) — pipeline completo de modelagem.

## Produção

Apontar o Streamlit Community Cloud para este branch, arquivo `app/app.py`.  
O Cloud monta o clone em `/mount/src/<repo>`; `app/repo_path.py` carrega `src/*.py` pelo caminho do arquivo para evitar colisão de import.

Links de submissão: [`entrega_tech_challenge_fase4.txt`](entrega_tech_challenge_fase4.txt).

Código-fonte: [https://github.com/DELSOBRINHO/fase4-postech](https://github.com/DELSOBRINHO/fase4-postech)
