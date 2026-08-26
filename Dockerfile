# Extra de empacotamento (não substitui o Streamlit Cloud).
# Imagem enxuta: só o necessário para servir o app.

FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    STREAMLIT_SERVER_HEADLESS=true

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip \
    && pip install --root-user-action=ignore -r /app/requirements.txt

COPY app/ /app/app/
COPY src/ /app/src/
COPY api/ /app/api/
COPY data/ /app/data/
COPY .streamlit/ /app/.streamlit/

EXPOSE 8501 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
