# Sistema preditivo hospitalar de diagnóstico de obesidade

Tech Challenge Fase 4 — FIAP POSTECH (Data Viz & Production Models).

Aplicação de apoio à equipe médica para **classificar o nível de obesidade** a partir de dados biométricos, histórico familiar e hábitos, com **painel analítico** para a gestão clínica.

## O problema

A obesidade é uma condição crônica multifatorial. O hospital precisa de um fluxo de triagem padronizado: um modelo com assertividade acima de 75% e uma interface que o corpo clínico consiga usar sem conhecer o código.

Este repositório entrega:

1. Pipeline Scikit-Learn (`ColumnTransformer` + `Pipeline`) com IMC como atributo clínico.
2. Modelo serializado (**Gradient Boosting**, acurácia de teste **98,35%**; Random Forest 97,87%).
3. App Streamlit com diagnóstico individual e dashboard epidemiológico, em produção em [https://avaliapeso.streamlit.app/](https://avaliapeso.streamlit.app/).
4. Extra opcional: FastAPI (`/predict`) + Docker Compose unindo API e frontend Streamlit.
5. Documentação de produto em [`documentacao/`](documentacao/01-plano-mestre.md).

## Estrutura

```text
data/Obesity.csv
notebooks/01_eda_analise_medica.ipynb
notebooks/02_pipeline_modelagem.ipynb
src/data_pipeline.py
src/train.py
src/inference.py
api/main.py                 # extra: API REST
app/app.py
app/model.joblib
documentacao/          # plano mestre, checklist, dicionário, deploy
Dockerfile             # extra: imagem (API + frontend)
docker-compose.yml
entrega_tech_challenge_fase4.txt
```

## Como executar

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m src.train
streamlit run app/app.py
```

O treino grava `app/model.joblib` e `documentacao/metricas_modelo.json`.

## Extra: Docker + FastAPI

O deploy da disciplina é o Streamlit Cloud. Para empacotar **API REST + frontend**:

```bash
docker compose up --build
```

- App: http://localhost:8501
- API (Swagger): http://localhost:8000/docs

API isolada, sem Docker:

```bash
uvicorn api.main:app --reload --port 8000
```

Guias: [`07-guia-docker.md`](documentacao/07-guia-docker.md) e [`08-guia-fastapi.md`](documentacao/08-guia-fastapi.md).

## Dados

Base `Obesity.csv` (2.111 pacientes, 17 colunas, alvo `Obesity` com 7 classes). Dicionário em [`documentacao/04-dicionario-dados.md`](documentacao/04-dicionario-dados.md).

## Documentação do app

| Documento | Conteúdo |
| --- | --- |
| [Plano mestre](documentacao/01-plano-mestre.md) | Requisitos, arquitetura e entregáveis |
| [Plano de desenvolvimento](documentacao/02-plano-desenvolvimento-checklist.md) | Checklist por fase |
| [Enunciado](documentacao/03-enunciado-tech-challenge.md) | Texto oficial do desafio |
| [Dicionário](documentacao/04-dicionario-dados.md) | Variáveis clínicas |
| [Deploy Streamlit](documentacao/06-guia-deploy-streamlit.md) | Publicação no Cloud |
| [Docker (extra)](documentacao/07-guia-docker.md) | Container local: API + Streamlit |
| [FastAPI (extra)](documentacao/08-guia-fastapi.md) | API REST de inferência |

## Produção

Aplicação e painel analítico: [https://avaliapeso.streamlit.app/](https://avaliapeso.streamlit.app/)

Código-fonte: [https://github.com/DELSOBRINHO/fase4-postech/tree/main](https://github.com/DELSOBRINHO/fase4-postech/tree/main)

O arquivo de submissão da disciplina está em [`entrega_tech_challenge_fase4.txt`](entrega_tech_challenge_fase4.txt). Falta apenas o link do vídeo de apresentação.
