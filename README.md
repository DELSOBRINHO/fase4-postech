# Sistema preditivo hospitalar de diagnóstico de obesidade

Tech Challenge Fase 4 — FIAP POSTECH (Data Viz & Production Models).

Aplicação de apoio à equipe médica para **classificar o nível de obesidade** a partir de dados biométricos, histórico familiar e hábitos, com **painel analítico** para a gestão clínica.

## O problema

A obesidade é uma condição crônica multifatorial. O hospital precisa de um fluxo de triagem padronizado: um modelo com assertividade acima de 75% e uma interface que o corpo clínico consiga usar sem conhecer o código.

Este repositório entrega:

1. Pipeline Scikit-Learn (`ColumnTransformer` + `Pipeline`) com IMC como atributo clínico.
2. Modelo serializado (**Gradient Boosting**, acurácia de teste **98,35%**; Random Forest 97,87%).
3. App Streamlit com diagnóstico individual e dashboard epidemiológico.
4. Extra opcional: `Dockerfile` + `docker-compose.yml` para subir o mesmo app em container.
5. Documentação de produto em [`documentacao/`](documentacao/01-plano-mestre.md).

## Estrutura

```text
data/Obesity.csv
notebooks/01_eda_analise_medica.ipynb
notebooks/02_pipeline_modelagem.ipynb
src/data_pipeline.py
src/train.py
app/app.py
app/model.joblib
documentacao/          # plano mestre, checklist, dicionário, roteiro, deploy
Dockerfile             # extra: imagem do app
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

## Extra: Docker

O deploy da disciplina é o Streamlit Cloud. Para empacotar o mesmo app localmente:

```bash
docker compose up --build
```

Detalhes em [`documentacao/07-guia-docker.md`](documentacao/07-guia-docker.md).

## Dados

Base `Obesity.csv` (2.111 pacientes, 17 colunas, alvo `Obesity` com 7 classes). Dicionário em [`documentacao/04-dicionario-dados.md`](documentacao/04-dicionario-dados.md).

## Documentação do app

| Documento | Conteúdo |
| --- | --- |
| [Plano mestre](documentacao/01-plano-mestre.md) | Requisitos, arquitetura e entregáveis |
| [Plano de desenvolvimento](documentacao/02-plano-desenvolvimento-checklist.md) | Checklist por fase |
| [Enunciado](documentacao/03-enunciado-tech-challenge.md) | Texto oficial do desafio |
| [Dicionário](documentacao/04-dicionario-dados.md) | Variáveis clínicas |
| [Roteiro do vídeo](documentacao/05-roteiro-video.md) | 5–7 minutos, visão de negócio |
| [Deploy Streamlit](documentacao/06-guia-deploy-streamlit.md) | Publicação no Cloud |
| [Docker (extra)](documentacao/07-guia-docker.md) | Container local com Compose |

## Submissão

Preencha os quatro links em [`entrega_tech_challenge_fase4.txt`](entrega_tech_challenge_fase4.txt) após o deploy e a publicação do vídeo.
