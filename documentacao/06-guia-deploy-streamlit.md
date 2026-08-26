# Guia de deploy — Streamlit Cloud

## Pré-requisitos

- Repositório GitHub com `app/model.joblib` versionado (o Cloud **não** treina o modelo).
- `requirements.txt` na **raiz**.
- Python 3.10+ recomendado.

## Passos

1. Acesse [https://share.streamlit.io](https://share.streamlit.io) e autorize o GitHub.
2. **New app** → selecione este repositório e o branch `main` (ou o branch de entrega).
3. Main file path: `app/app.py`.
4. Deploy.

**URL em produção:** [https://avaliapeso.streamlit.app/](https://avaliapeso.streamlit.app/)

A aplicação resolve dados e modelo a partir da raiz do repositório:

- `data/Obesity.csv`
- `app/model.joblib`

## Teste local (antes do Cloud)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.train
streamlit run app/app.py
```

Abrir `http://localhost:8501` e percorrer:

- [ ] Diagnóstico com paciente exemplo
- [ ] Gráfico de probabilidade
- [ ] Painel: quatro KPIs e quatro gráficos principais

## Depois do ar no ar

`entrega_tech_challenge_fase4.txt` já contém:

- App: https://avaliapeso.streamlit.app/
- Painel: a mesma URL, aba *Painel analítico e insights*
- GitHub: https://github.com/DELSOBRINHO/fase4-postech
- Vídeo: ainda pendente

## Problemas comuns

| Sintoma | Causa típica | Correção |
| --- | --- | --- |
| `FileNotFoundError: model.joblib` | Modelo não commitado ou caminho errado | Rodar `python -m src.train` e dar push em `app/model.joblib` |
| App abre em branco / erro de import `src` | `sys.path` sem a raiz | Já tratado em `app/app.py` |
| `ModuleNotFoundError: sklearn` | `requirements.txt` ausente na raiz | Usar o arquivo da raiz no Cloud |
| Gráficos lentos | Dataset inteiro em cada rerun | `st.cache_data` já aplicado em `load_data` |
