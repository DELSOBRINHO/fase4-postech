"""Aplicação Streamlit: previsão do Brent e apoio à decisão executiva."""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from config import DEFAULT_BARRELS, DEFAULT_HORIZON, GEOPOLITICAL_EVENTS, HORIZON_OPTIONS
from repo_path import ROOT, load_project_modules

try:
    ROOT, data_loader, feature_engineering, model_trainer = load_project_modules()
except Exception as exc:  # noqa: BLE001
    st.set_page_config(page_title="Erro ao iniciar", layout="wide")
    st.error(f"Falha ao carregar o aplicativo: {type(exc).__name__}: {exc}")
    st.stop()

MODEL_PATH = ROOT / "app" / "model.joblib"
RAW_PATH = ROOT / "data" / "raw" / "brent_oil_raw.csv"
METRICS_PATH = ROOT / "documentation" / "metricas_modelo.json"

st.set_page_config(
    page_title="Previsão do Petróleo Brent",
    layout="wide",
    page_icon="🛢️",
)


@st.cache_data(show_spinner=False)
def load_raw_series(refresh: bool = False) -> pd.DataFrame:
    return data_loader.load_or_refresh(path=RAW_PATH, refresh=refresh, timeout=45)


@st.cache_resource(show_spinner=False)
def load_bundle():
    if not MODEL_PATH.is_file():
        raise FileNotFoundError(f"Modelo não encontrado: {MODEL_PATH}")
    return joblib.load(MODEL_PATH)


@st.cache_data(show_spinner=False)
def load_metrics_fallback() -> dict:
    if METRICS_PATH.is_file():
        return json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    return {}


def format_usd(value: float) -> str:
    return f"US$ {value:,.2f}"


def line_theme(fig: go.Figure, title: str) -> go.Figure:
    fig.update_layout(
        title=title,
        template="plotly_white",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
        margin=dict(l=16, r=16, t=56, b=16),
        height=480,
    )
    return fig


def tab_forecast(series: pd.DataFrame, bundle: dict) -> None:
    last_date = series["date"].max()
    last_price = float(series.loc[series["date"] == last_date, "price"].iloc[0])
    model = bundle["model"]
    cols = bundle["feature_columns"]
    residual_std = float(bundle.get("residual_std") or 0.0)

    left, mid, right = st.columns(3)
    left.metric("Último preço oficial (IPEA)", format_usd(last_price), help=f"Cotação em {last_date.date()}")
    mid.metric("Observações na série", f"{len(series):,}".replace(",", "."))
    right.metric("Modelo campeão", str(bundle.get("model_name", "—")).replace("_", " ").title())

    st.markdown(
        "Projeção recursiva em **dias úteis** a partir da última cotação oficial. "
        "A faixa sombreada é ±1,96 · σ residual · √h (incerteza crescente com o horizonte)."
    )

    horizon = st.radio("Horizonte (dias úteis)", HORIZON_OPTIONS, index=HORIZON_OPTIONS.index(DEFAULT_HORIZON), horizontal=True)
    forecast = feature_engineering.recursive_forecast(
        model,
        series,
        horizon=int(horizon),
        feature_cols=cols,
        residual_std=residual_std,
    )

    recent = series.tail(180).copy()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=recent["date"], y=recent["price"], name="Histórico IPEA", line=dict(color="#0A3D62", width=2)))
    fig.add_trace(
        go.Scatter(
            x=forecast["date"],
            y=forecast["upper"],
            name="Limite superior",
            line=dict(width=0),
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=forecast["date"],
            y=forecast["lower"],
            name="Faixa de confiança",
            fill="tonexty",
            fillcolor="rgba(201,162,39,0.22)",
            line=dict(width=0),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=forecast["date"],
            y=forecast["predicted"],
            name="Projeção",
            line=dict(color="#C9A227", width=3, dash="dash"),
        )
    )
    st.plotly_chart(line_theme(fig, f"Brent FOB — histórico recente e projeção de {horizon} dias úteis"), use_container_width=True)

    end_price = float(forecast["predicted"].iloc[-1])
    delta = end_price - last_price
    c1, c2, c3 = st.columns(3)
    c1.metric(f"Preço projetado (D+{horizon})", format_usd(end_price), f"{delta:+.2f} US$")
    c2.metric("Mínimo da faixa", format_usd(float(forecast["lower"].iloc[-1])))
    c3.metric("Máximo da faixa", format_usd(float(forecast["upper"].iloc[-1])))

    st.subheader("Simulador de impacto financeiro")
    st.caption("Receita estimada = preço × volume. Útil para orçamento de trading, hedge e caixa.")
    barrels = st.number_input("Volume de produção (barris)", min_value=1_000, max_value=50_000_000, value=DEFAULT_BARRELS, step=50_000)
    current_rev = last_price * barrels
    forecast_rev = end_price * barrels
    impact = forecast_rev - current_rev
    s1, s2, s3 = st.columns(3)
    s1.metric("Receita ao preço atual", f"US$ {current_rev:,.0f}")
    s2.metric(f"Receita projetada (D+{horizon})", f"US$ {forecast_rev:,.0f}")
    s3.metric("Impacto estimado", f"US$ {impact:,.0f}", f"{(impact / current_rev) * 100:+.2f}%")

    with st.expander("Tabela da projeção"):
        table = forecast.copy()
        table["date"] = table["date"].dt.strftime("%Y-%m-%d")
        st.dataframe(table, use_container_width=True, hide_index=True)


def tab_history(series: pd.DataFrame) -> None:
    st.markdown(
        "A série oficial do IPEA (`EIA366_PBRENT366`) cobre o Brent FOB em US$/barril. "
        "Os marcadores abaixo são os cinco choques exigidos no plano de EDA."
    )
    events = pd.DataFrame(GEOPOLITICAL_EVENTS)
    events["date"] = pd.to_datetime(events["date"])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=series["date"], y=series["price"], name="Brent (US$)", line=dict(color="#0A3D62", width=1.6)))
    y_max = float(series["price"].max())
    for _, event in events.iterrows():
        fig.add_vline(x=event["date"], line_width=1, line_dash="dot", line_color="#C9A227")
        fig.add_annotation(
            x=event["date"],
            y=y_max,
            text=event["title"],
            showarrow=False,
            textangle=-90,
            yanchor="top",
            font=dict(size=10, color="#1B2838"),
        )
    st.plotly_chart(line_theme(fig, "Trajetória histórica do Brent e choques geopolíticos"), use_container_width=True)

    st.subheader("Linha do tempo")
    for event in GEOPOLITICAL_EVENTS:
        st.markdown(f"**{event['date']} — {event['title']}**  \n{event['impact']}")

    work = series.sort_values("date").copy()
    work["ma_30"] = work["price"].rolling(30).mean()
    work["ma_90"] = work["price"].rolling(90).mean()
    work["vol_30"] = work["price"].rolling(30).std()
    work["vol_annual"] = work["price"].pct_change().rolling(30).std() * (252 ** 0.5) * 100

    c1, c2 = st.columns(2)
    fig_ma = go.Figure()
    fig_ma.add_trace(go.Scatter(x=work["date"], y=work["price"], name="Preço", line=dict(color="#9AA8B5", width=1)))
    fig_ma.add_trace(go.Scatter(x=work["date"], y=work["ma_30"], name="Média 30d", line=dict(color="#0A3D62", width=2)))
    fig_ma.add_trace(go.Scatter(x=work["date"], y=work["ma_90"], name="Média 90d", line=dict(color="#C9A227", width=2)))
    c1.plotly_chart(line_theme(fig_ma, "Médias móveis"), use_container_width=True)

    fig_vol = go.Figure()
    fig_vol.add_trace(go.Scatter(x=work["date"], y=work["vol_annual"], name="Vol. anualizada 30d (%)", line=dict(color="#8C2F39")))
    c2.plotly_chart(line_theme(fig_vol, "Volatilidade anualizada (janela de 30 dias)"), use_container_width=True)


def tab_governance(bundle: dict, metrics_file: dict) -> None:
    metrics = bundle.get("metrics") or metrics_file.get("metrics") or {}
    comparison = bundle.get("comparison") or metrics_file.get("comparison") or []
    horizons = bundle.get("horizon_metrics") or metrics_file.get("horizon_metrics") or {}
    y_true = bundle.get("y_true")
    y_pred = bundle.get("y_pred")
    y_dates = bundle.get("y_dates")

    if y_true is None:
        y_true = metrics_file.get("y_true")
        y_pred = metrics_file.get("y_pred")
        y_dates = metrics_file.get("y_dates")

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("MAPE (teste)", f"{metrics.get('mape', float('nan')):.2f}%")
    k2.metric("RMSE", f"{metrics.get('rmse', float('nan')):.2f} US$")
    k3.metric("MAE", f"{metrics.get('mae', float('nan')):.2f} US$")
    k4.metric("R²", f"{metrics.get('r2', float('nan')):.3f}")

    st.caption(
        f"Validação temporal estrita: treino até {bundle.get('train_end', metrics_file.get('train_end', '—'))}, "
        f"teste {bundle.get('test_start', metrics_file.get('test_start', '—'))} "
        f"a {bundle.get('test_end', metrics_file.get('test_end', '—'))}. Sem embaralhamento."
    )

    if comparison:
        st.subheader("Comparação de modelos")
        st.dataframe(pd.DataFrame(comparison).round(3), use_container_width=True, hide_index=True)

    if horizons:
        st.subheader("MAPE recursivo por horizonte")
        rows = [{"horizonte_dias": key, **value} for key, value in horizons.items()]
        st.dataframe(pd.DataFrame(rows).round(3), use_container_width=True, hide_index=True)

    if y_true is not None and y_pred is not None and y_dates is not None:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=y_dates, y=y_true, name="Real", line=dict(color="#0A3D62", width=2)))
        fig.add_trace(go.Scatter(x=y_dates, y=y_pred, name="Previsto", line=dict(color="#C9A227", width=2, dash="dash")))
        st.plotly_chart(line_theme(fig, "Conjunto de teste — real vs. previsto (1 passo à frente)"), use_container_width=True)

    rolling = bundle.get("rolling_cv") or metrics_file.get("rolling_cv") or []
    if rolling:
        st.subheader("Validação em janela expansiva")
        st.dataframe(pd.DataFrame(rolling).round(3), use_container_width=True, hide_index=True)

    st.info(
        "Meta de governança do plano mestre: MAPE ≤ 5% no curto prazo (7 a 15 dias). "
        "A métrica de 1 passo usa os atributos defasados reais; a métrica recursiva acumula erro de projeção."
    )


def main() -> None:
    st.title("Sistema preditivo do preço do petróleo Brent")
    st.caption(
        "Tech Challenge Fase 4 — Prova Substitutiva (FIAP POSTECH). "
        "Série IPEA Data 1650971490 / EIA366_PBRENT366 · apoio à diretoria e à mesa de trading."
    )

    with st.sidebar:
        st.header("Dados")
        refresh = st.checkbox("Tentar atualizar no IPEA agora", value=False)
        st.markdown(
            "[Série oficial IPEA](http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view)"
        )
        st.markdown("Se a API do IPEA estiver lenta, o app usa o CSV versionado em `data/raw`.")

    try:
        series = load_raw_series(refresh=refresh)
        bundle = load_bundle()
        metrics_file = load_metrics_fallback()
    except Exception as exc:  # noqa: BLE001
        st.error(f"Falha ao carregar dados ou modelo: {type(exc).__name__}: {exc}")
        st.stop()

    forecast_tab, history_tab, gov_tab = st.tabs(
        [
            "Previsão e simulador",
            "Análise histórica e geopolítica",
            "Desempenho e governança",
        ]
    )
    with forecast_tab:
        tab_forecast(series, bundle)
    with history_tab:
        tab_history(series)
    with gov_tab:
        tab_governance(bundle, metrics_file)


if __name__ == "__main__":
    main()
