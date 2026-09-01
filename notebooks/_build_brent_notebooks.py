"""Gera os notebooks oficiais da prova substitutiva (Brent)."""

from __future__ import annotations

from pathlib import Path

import nbformat as nbf

ROOT = Path(__file__).resolve().parent


def _nb() -> nbf.NotebookNode:
    nb = nbf.v4.new_notebook()
    nb.metadata["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    return nb


def _md(text: str):
    return nbf.v4.new_markdown_cell(text)


def _code(text: str):
    return nbf.v4.new_code_cell(text)


def write_eda() -> None:
    nb = _nb()
    nb.cells = [
        _md(
            "# Extração e EDA — Petróleo Brent (IPEA Data)\n\n"
            "Tech Challenge Fase 4 (Prova Substitutiva) — FIAP POSTECH.\n\n"
            "Série oficial: `EIA366_PBRENT366` (serid `1650971490`), preço Brent FOB em US$/barril."
        ),
        _code(
            "from pathlib import Path\n"
            "import sys\n"
            "\n"
            "import matplotlib.pyplot as plt\n"
            "import pandas as pd\n"
            "from statsmodels.tsa.seasonal import seasonal_decompose\n"
            "from statsmodels.tsa.stattools import adfuller\n"
            "\n"
            "ROOT = Path.cwd().resolve()\n"
            "if not (ROOT / 'src').is_dir():\n"
            "    ROOT = ROOT.parent\n"
            "sys.path.insert(0, str(ROOT))\n"
            "\n"
            "from src.data_loader import load_or_refresh, series_summary, IPEA_SERCODIGO, IPEA_SERID\n"
            "\n"
            "raw = load_or_refresh(refresh=False)\n"
            "summary = series_summary(raw)\n"
            "display(pd.Series(summary, name='serie'))\n"
            "raw.tail()"
        ),
        _md("## Trajetória histórica (1987 aos dias atuais)"),
        _code(
            "fig, ax = plt.subplots(figsize=(12, 5))\n"
            "ax.plot(raw['date'], raw['price'], color='#0A3D62', linewidth=1.1)\n"
            "ax.set_title('Brent FOB (US$/barril) — série IPEA')\n"
            "ax.set_xlabel('Data')\n"
            "ax.set_ylabel('US$')\n"
            "ax.grid(True, alpha=0.3)\n"
            "plt.show()"
        ),
        _md(
            "## Cinco choques geopolíticos e econômicos\n\n"
            "- **1990** — Guerra do Golfo.\n"
            "- **2008** — Crise dos subprimes / pico acima de US$ 140.\n"
            "- **2014** — Guerra de preços da OPEP.\n"
            "- **2020** — COVID-19 e choque de demanda.\n"
            "- **2022** — Conflito Rússia–Ucrânia."
        ),
        _code(
            "events = [\n"
            "    ('1990-08-02', 'Guerra do Golfo'),\n"
            "    ('2008-07-11', 'Crise 2008 / pico'),\n"
            "    ('2014-11-27', 'Guerra de preços OPEP'),\n"
            "    ('2020-04-21', 'COVID-19'),\n"
            "    ('2022-02-24', 'Rússia–Ucrânia'),\n"
            "]\n"
            "fig, ax = plt.subplots(figsize=(12, 5))\n"
            "ax.plot(raw['date'], raw['price'], color='#0A3D62', linewidth=1.0)\n"
            "ymax = raw['price'].max()\n"
            "for date, title in events:\n"
            "    ts = pd.Timestamp(date)\n"
            "    ax.axvline(ts, color='#C9A227', linestyle='--', linewidth=1)\n"
            "    ax.text(ts, ymax, title, rotation=90, va='top', ha='right', fontsize=8)\n"
            "ax.set_title('Choques anotados na série do Brent')\n"
            "ax.grid(True, alpha=0.3)\n"
            "plt.show()"
        ),
        _md("## Decomposição temporal (tendência, sazonalidade anual e resíduo)"),
        _code(
            "monthly = raw.set_index('date')['price'].resample('MS').mean().dropna()\n"
            "decomp = seasonal_decompose(monthly, model='additive', period=12)\n"
            "fig = decomp.plot()\n"
            "fig.set_size_inches(12, 8)\n"
            "plt.tight_layout()\n"
            "plt.show()"
        ),
        _md("## Teste de estacionariedade (Augmented Dickey-Fuller)"),
        _code(
            "def adf_report(series, label):\n"
            "    series = series.dropna()\n"
            "    stat, pvalue, lags, nobs, crit, _ = adfuller(series, autolag='AIC')\n"
            "    return {\n"
            "        'serie': label,\n"
            "        'adf': stat,\n"
            "        'p_valor': pvalue,\n"
            "        'lags': lags,\n"
            "        'n': nobs,\n"
            "        'critico_5%': crit['5%'],\n"
            "        'estacionaria_5%': pvalue < 0.05,\n"
            "    }\n"
            "\n"
            "level = raw.set_index('date')['price']\n"
            "reports = [\n"
            "    adf_report(level, 'preco_nivel'),\n"
            "    adf_report(level.diff(), 'primeira_diferenca'),\n"
            "]\n"
            "display(pd.DataFrame(reports))"
        ),
        _md(
            "A série em nível costuma ser não estacionária (passeio próximo a um processo integrado). "
            "A primeira diferença tende a rejeitar a hipótese nula do ADF — padrão típico de preço de commodity."
        ),
    ]
    nbf.write(nb, ROOT / "01_extracao_eda_brent.ipynb")


def write_model() -> None:
    nb = _nb()
    nb.cells = [
        _md(
            "# Pipeline de forecasting — preço do petróleo Brent\n\n"
            "Notebook obrigatório da prova substitutiva: extração, features, treino temporal, "
            "métricas e serialização do modelo campeão."
        ),
        _code(
            "from pathlib import Path\n"
            "import sys\n"
            "\n"
            "import matplotlib.pyplot as plt\n"
            "import pandas as pd\n"
            "\n"
            "ROOT = Path.cwd().resolve()\n"
            "if not (ROOT / 'src').is_dir():\n"
            "    ROOT = ROOT.parent\n"
            "sys.path.insert(0, str(ROOT))\n"
            "\n"
            "from src.data_loader import load_or_refresh, series_summary\n"
            "from src.feature_engineering import build_features, feature_columns, recursive_forecast\n"
            "from src.model_trainer import save_bundle, temporal_split, train_and_select\n"
            "\n"
            "raw = load_or_refresh(refresh=False)\n"
            "display(pd.Series(series_summary(raw), name='serie'))"
        ),
        _md(
            "## Engenharia de atributos\n\n"
            "Lags t−1, t−2, t−3, t−5, t−7, t−15, t−30; médias 7/14/30/90; "
            "volatilidade 7/30; calendário. Janelas móveis usam apenas t−1 para evitar vazamento."
        ),
        _code(
            "features = build_features(raw)\n"
            "cols = feature_columns()\n"
            "print('atributos:', cols)\n"
            "print('shape:', features.shape)\n"
            "features[['date', 'price', *cols[:6]]].tail()"
        ),
        _md(
            "## Treinamento comparativo (Time Series Split)\n\n"
            "Últimos 60 dias úteis ficam no teste. Sem shuffle. "
            "Candidatos: Naive (lag-1), Random Forest, XGBoost; Prophet/SARIMAX/LightGBM se instalados."
        ),
        _code(
            "bundle = train_and_select(refresh=False, test_days=60)\n"
            "path = save_bundle(bundle)\n"
            "print('campeão:', bundle['model_name'])\n"
            "print('modelo salvo em', path)\n"
            "display(pd.DataFrame(bundle['comparison']))"
        ),
        _md("## Métricas no conjunto de teste (1 passo à frente)"),
        _code(
            "display(pd.Series(bundle['metrics'], name='teste_1_passo'))\n"
            "if bundle.get('horizon_metrics'):\n"
            "    display(pd.DataFrame(bundle['horizon_metrics']).T.rename_axis('horizonte'))"
        ),
        _code(
            "fig, ax = plt.subplots(figsize=(12, 4))\n"
            "ax.plot(pd.to_datetime(bundle['y_dates']), bundle['y_true'], label='Real', color='#0A3D62')\n"
            "ax.plot(pd.to_datetime(bundle['y_dates']), bundle['y_pred'], label='Previsto', color='#C9A227', linestyle='--')\n"
            "ax.set_title('Teste temporal — real vs. previsto')\n"
            "ax.legend()\n"
            "ax.grid(True, alpha=0.3)\n"
            "plt.show()"
        ),
        _md("## Projeção recursiva a partir do último preço oficial"),
        _code(
            "forecast = recursive_forecast(\n"
            "    bundle['model'],\n"
            "    raw,\n"
            "    horizon=15,\n"
            "    feature_cols=bundle['feature_columns'],\n"
            "    residual_std=bundle['residual_std'],\n"
            ")\n"
            "display(forecast)\n"
            "fig, ax = plt.subplots(figsize=(12, 4))\n"
            "hist = raw.tail(90)\n"
            "ax.plot(hist['date'], hist['price'], label='Histórico', color='#0A3D62')\n"
            "ax.plot(forecast['date'], forecast['predicted'], label='Projeção 15d', color='#C9A227', linestyle='--')\n"
            "ax.fill_between(forecast['date'], forecast['lower'], forecast['upper'], color='#C9A227', alpha=0.2)\n"
            "ax.set_title('Projeção recursiva — 15 dias úteis')\n"
            "ax.legend()\n"
            "ax.grid(True, alpha=0.3)\n"
            "plt.show()"
        ),
        _md(
            "## Governança\n\n"
            "- Métrica principal: MAPE de curto prazo (meta ≤ 5% em 7–15 dias).\n"
            "- RMSE e MAE em US$ para a mesa de trading.\n"
            "- Validação em janela expansiva registrada em `bundle['rolling_cv']`.\n"
            "- Artefato de produção: `app/model.joblib`."
        ),
        _code(
            "display(pd.DataFrame(bundle.get('rolling_cv', [])))\n"
            "print('train_end', bundle['train_end'], 'teste', bundle['test_start'], '→', bundle['test_end'])"
        ),
    ]
    nbf.write(nb, ROOT / "02_modelagem_forecasting.ipynb")


if __name__ == "__main__":
    write_eda()
    write_model()
    print("notebooks ok")
