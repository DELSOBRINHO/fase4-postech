# Extra — Docker (opcional)

O enunciado oficial pede deploy no **Streamlit**. Isso já está em produção:

**https://avaliapeso.streamlit.app/**

Docker e Compose empacotam o **frontend Streamlit** e a **API FastAPI** na mesma imagem, sem substituir o Cloud.

## O que foi incluído

| Arquivo | Função |
| --- | --- |
| `Dockerfile` | Imagem Python 3.12 (app, API, modelo, dados e `src/`) |
| `docker-compose.yml` | Serviço `api` (8000) + `avaliapeso` (8501) |
| `.dockerignore` | Evita copiar notebooks, documentação e `.git` |

Detalhe da API: [`08-guia-fastapi.md`](08-guia-fastapi.md).

## Subir API + frontend

```bash
docker compose up --build
```

- App: http://localhost:8501
- API: http://localhost:8000/docs

Parar:

```bash
docker compose down
```

Só o frontend (inferência local, sem API):

```bash
docker build -t avaliapeso:local .
docker run --rm -p 8501:8501 avaliapeso:local
```

## O que entra na imagem

- `app/`, `api/`, `src/`
- `app/model.joblib` e `data/Obesity.csv`
- `app/requirements.txt` (inclui FastAPI e uvicorn)
- `.streamlit/config.toml`

## Conferência rápida

- [ ] http://localhost:8000/health responde `ok`
- [ ] http://localhost:8501 abre o diagnóstico; a sidebar cita a API
- [ ] Painel mostra 2.111 pacientes
- [ ] `POST /predict` no Swagger devolve classe + IMC
