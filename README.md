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

## Produção (dois deploys, `main` intacto)

| Branch | Produto | Streamlit |
| --- | --- | --- |
| `main` | Obesidade (entrega original) | [https://avaliapeso.streamlit.app/](https://avaliapeso.streamlit.app/) — **não alterar** |
| `cursor/main-dev-2a05` | Brent (prova substitutiva) | [https://precopetroleo.streamlit.app/](https://precopetroleo.streamlit.app/) |

O Cloud do Brent está neste branch (`cursor/main-dev-2a05`, arquivo `app/app.py`). A branch `develop` tem o mesmo código; o Streamlit às vezes não lista branch nova logo após o push — dá para digitar o nome `develop` no campo Branch se quiser trocar depois.

O Cloud monta o clone em `/mount/src/<repo>`; `app/repo_path.py` carrega `src/*.py` pelo caminho do arquivo para evitar colisão de import.

## Próximos Passos e Melhorias Futuras para o Negócio

O modelo atual e a aplicação Streamlit atendem aos requisitos de acurácia estatística e de apoio à decisão previstos no escopo da prova substitutiva. As evoluções abaixo ficam mapeadas para fases seguintes de maturidade corporativa — não fazem parte desta entrega.

1. **Acurácia direcional (Mean Directional Accuracy — MDA)**  
   Incorporar a MDA para medir o percentual de acerto da tendência (alta versus baixa). O impacto é direto na mesa de tesouraria e de trading: a direção do preço, mais do que o valor pontual, sustenta a montagem de hedges cambiais e de derivativos.

2. **Simulador de testes de estresse e choques geopolíticos**  
   Incluir na interface um módulo de cenários exógenos (cortes súbitos de produção da OPEP+, desescalada de conflitos ou gargalos logísticos). O tomador de decisão passa a medir a sensibilidade do caixa corporativo em situações extremas, além da trajetória-base do modelo.

3. **Ingestão de variáveis macroeconômicas exógenas**  
   Ampliar a engenharia de atributos com indicadores correlacionados ao petróleo em moeda forte — Índice Dólar (DXY), taxa de juros do Federal Reserve e relatórios semanais de estoques da EIA. A leitura de oferta, demanda e câmbio reduz o risco de projeções isoladas da série de preço.

Links de submissão: [`entrega_tech_challenge_fase4.txt`](entrega_tech_challenge_fase4.txt).

Código-fonte (Brent): [https://github.com/DELSOBRINHO/fase4-postech/tree/cursor/main-dev-2a05](https://github.com/DELSOBRINHO/fase4-postech/tree/cursor/main-dev-2a05)
