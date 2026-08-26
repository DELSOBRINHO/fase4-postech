# Extra — API REST FastAPI (opcional)

O enunciado oficial pede **Streamlit**. A inferência em produção da banca continua em:

**https://avaliapeso.streamlit.app/**

Esta API é um **extra de MLOps**: o mesmo `app/model.joblib` é servido em REST, e o Docker Compose une **API + frontend**.

## Por que FastAPI e não o Cloud

| Caminho | Papel |
| --- | --- |
| Streamlit Cloud | Entrega oficial (diagnóstico + painel) |
| FastAPI `/predict` | Contrato REST para outro sistema hospitalar integrar o modelo |
| Docker Compose | Sobe API (8000) e Streamlit (8501) juntos; o frontend chama a API |

No Cloud a variável `INFERENCE_API_URL` **não** é definida: o app usa o modelo local, como antes.

## Endpoints

| Método | Rota | Função |
| --- | --- | --- |
| GET | `/health` | Liveness |
| GET | `/classes` | Classes do modelo e rótulos em português |
| POST | `/predict` | Inferência (16 variáveis clínicas) |
| GET | `/docs` | Swagger gerado pelo FastAPI |

Exemplo:

```bash
uvicorn api.main:app --reload --port 8000
```

```bash
curl -s http://localhost:8000/health
curl -s -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Gender":"Female","Age":21,"Height":1.62,"Weight":64,
    "family_history":"yes","FAVC":"no","FCVC":2,"NCP":3,
    "CAEC":"Sometimes","SMOKE":"no","CH2O":2,"SCC":"no",
    "FAF":0,"TUE":1,"CALC":"no","MTRANS":"Public_Transportation"
  }'
```

Resposta típica: `prediction` = `Normal_Weight`, `imc` ≈ 24.39, vetor de `probabilities`.

## API + frontend no Docker

```bash
docker compose up --build
```

- Frontend: http://localhost:8501 (sidebar indica inferência via FastAPI)
- API / Swagger: http://localhost:8000/docs

O serviço `avaliapeso` chama `http://host.docker.internal:8000/predict` (porta publicada da API). Só sobe depois do healthcheck da API.

## Código

| Arquivo | Função |
| --- | --- |
| `api/main.py` | FastAPI, schema Pydantic e rotas |
| `src/inference.py` | Inferência compartilhada (API e Streamlit local) |
| `docker-compose.yml` | Serviços `api` e `avaliapeso` |
