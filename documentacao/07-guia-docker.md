# Extra — Docker (opcional)

O enunciado oficial pede deploy no **Streamlit**. Isso já está em produção:

**https://avaliapeso.streamlit.app/**

Docker e Compose entram como **extra de empacotamento** (disciplina de production models): o mesmo app sobe em container, com as mesmas dependências pinadas, sem substituir o Cloud.

## O que foi incluído

| Arquivo | Função |
| --- | --- |
| `Dockerfile` | Imagem Python 3.12 com app, modelo, dados e `src/` |
| `docker-compose.yml` | Sobe a aplicação na porta 8501 |
| `.dockerignore` | Evita copiar notebooks, documentação e `.git` para a imagem |

## Pré-requisitos

- Docker Engine 24+
- Docker Compose v2 (`docker compose`)

O Cloud **não** usa esta imagem. Ela serve para rodada local reproduzível e para um eventual host próprio (Render, VM, etc.).

## Subir o app

Na raiz do repositório:

```bash
docker compose up --build
```

Abrir http://localhost:8501

Parar:

```bash
docker compose down
```

Equivalente sem Compose:

```bash
docker build -t avaliapeso:local .
docker run --rm -p 8501:8501 avaliapeso:local
```

## O que entra na imagem

- `app/app.py` e `app/model.joblib`
- `src/` (imports da pipeline)
- `data/Obesity.csv` (painel analítico)
- `app/requirements.txt` (pandas, scikit-learn 1.9.0, streamlit, plotly)
- `.streamlit/config.toml`

Notebooks e a pasta `documentacao/` ficam de fora (`.dockerignore`).

## Conferência rápida

- [ ] A home abre com “Diagnóstico preditivo”
- [ ] Botão **Executar diagnóstico clínico** devolve classe + IMC
- [ ] Aba **Painel analítico e insights** mostra 2.111 pacientes
- [ ] `docker inspect --format='{{.State.Health.Status}}' avaliapeso` tende a `healthy` após o start-period

## Relação com o Streamlit Cloud

| Caminho | Uso |
| --- | --- |
| Streamlit Cloud | Entrega oficial da disciplina |
| `docker compose up` | Extra local / portabilidade |

Não é necessário republicar o Cloud depois deste extra: a imagem apenas empacota o código já validado.
