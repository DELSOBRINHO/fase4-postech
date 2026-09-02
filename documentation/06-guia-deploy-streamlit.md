# Guia de deploy — Streamlit Cloud (Brent)

## Pré-requisitos

- Repositório com `app/model.joblib` e `data/raw/brent_oil_raw.csv` versionados (o Cloud **não** treina o modelo).
- `requirements.txt` na raiz.
- Python 3.10+ recomendado.

## Passos

1. Acesse [https://share.streamlit.io](https://share.streamlit.io) e autorize o GitHub.
2. **New app** (não edite o app já publicado no `main`) → repositório `DELSOBRINHO/fase4-postech`, branch **`cursor/main-dev-2a05`**.
3. Main file path: `app/app.py`.
4. Deploy.

**App Brent em produção:** [https://precopetroleo.streamlit.app/](https://precopetroleo.streamlit.app/)

O `main` continua com o app de obesidade em [https://avaliapeso.streamlit.app/](https://avaliapeso.streamlit.app/).

Se o Cloud não listar uma branch recém-criada (ex.: `develop`), use o seletor e **digite o nome** ou publique pela branch que já aparece.

A aplicação resolve dados e modelo a partir da raiz:

- `data/raw/brent_oil_raw.csv`
- `app/model.joblib`

## Teste local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.model_trainer
streamlit run app/app.py
```

Percorrer:

- [ ] Aba de previsão: último preço, horizontes 7/15/30, faixa de confiança
- [ ] Simulador de volume de barris
- [ ] Aba histórica: cinco choques geopolíticos
- [ ] Aba de governança: MAPE/RMSE/MAE e real vs. previsto

## Problemas comuns

| Sintoma | Causa típica | Correção |
| --- | --- | --- |
| `FileNotFoundError: model.joblib` | Modelo não commitado | Rodar `python -m src.model_trainer` e dar push |
| Erro de import `src` | Mount `/mount/src` no Cloud | `app/repo_path.py` carrega os `.py` por caminho absoluto |
| Timeout no IPEA | API intermitente | O app usa o CSV versionado se a atualização falhar |
