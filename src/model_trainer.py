"""Treinamento comparativo com divisão temporal estrita e serialização do campeão."""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from src.data_loader import load_or_refresh, series_summary
from src.feature_engineering import (
    build_features,
    feature_columns,
    recursive_forecast,
    save_features,
)

TEST_DAYS = 60
HORIZONS = (7, 15, 30)
RANDOM_STATE = 42


def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def default_model_path() -> Path:
    return project_root() / "app" / "model.joblib"


def default_metrics_path() -> Path:
    return project_root() / "documentation" / "metricas_modelo.json"


def mape(y_true, y_pred) -> float:
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    mask = y_true != 0
    if not mask.any():
        return float("nan")
    return float(np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100.0)


def regression_metrics(y_true, y_pred) -> dict[str, float]:
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    return {
        "mape": mape(y_true, y_pred),
        "rmse": rmse,
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "r2": float(r2_score(y_true, y_pred)),
    }


def temporal_split(features: pd.DataFrame, test_days: int = TEST_DAYS):
    if len(features) <= test_days + 30:
        raise ValueError("Série insuficiente para divisão temporal.")
    train = features.iloc[:-test_days].copy()
    test = features.iloc[-test_days:].copy()
    if train["date"].max() >= test["date"].min():
        raise ValueError("A divisão temporal vazou: treino cruza o teste.")
    return train, test


def _fit_sklearn(name: str, estimator, train: pd.DataFrame, test: pd.DataFrame, cols: list[str]) -> dict:
    estimator.fit(train[cols], train["price"])
    pred = estimator.predict(test[cols])
    metrics = regression_metrics(test["price"], pred)
    return {
        "name": name,
        "model": estimator,
        "metrics": metrics,
        "y_pred": np.asarray(pred, dtype=float),
    }


def fit_naive(train: pd.DataFrame, test: pd.DataFrame) -> dict:
    pred = test["lag_1"].to_numpy(dtype=float)
    return {
        "name": "naive_lag1",
        "model": None,
        "metrics": regression_metrics(test["price"], pred),
        "y_pred": pred,
    }


def fit_random_forest(train: pd.DataFrame, test: pd.DataFrame, cols: list[str]) -> dict:
    model = RandomForestRegressor(
        n_estimators=180,
        max_depth=12,
        min_samples_leaf=3,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )
    return _fit_sklearn("random_forest", model, train, test, cols)


def fit_xgboost(train: pd.DataFrame, test: pd.DataFrame, cols: list[str]) -> dict:
    from xgboost import XGBRegressor

    model = XGBRegressor(
        n_estimators=350,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.85,
        colsample_bytree=0.85,
        reg_lambda=1.0,
        objective="reg:squarederror",
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )
    return _fit_sklearn("xgboost", model, train, test, cols)


def fit_lightgbm(train: pd.DataFrame, test: pd.DataFrame, cols: list[str]) -> dict | None:
    try:
        from lightgbm import LGBMRegressor
    except Exception:
        return None
    model = LGBMRegressor(
        n_estimators=350,
        learning_rate=0.05,
        num_leaves=31,
        subsample=0.85,
        colsample_bytree=0.85,
        random_state=RANDOM_STATE,
        verbosity=-1,
    )
    return _fit_sklearn("lightgbm", model, train, test, cols)


def fit_prophet(train: pd.DataFrame, test: pd.DataFrame) -> dict | None:
    try:
        from prophet import Prophet
    except Exception:
        return None
    history = train[["date", "price"]].rename(columns={"date": "ds", "price": "y"})
    model = Prophet(daily_seasonality=True, weekly_seasonality=True, yearly_seasonality=True)
    model.fit(history)
    future = test[["date"]].rename(columns={"date": "ds"})
    forecast = model.predict(future)
    pred = forecast["yhat"].to_numpy(dtype=float)
    return {
        "name": "prophet",
        "model": model,
        "metrics": regression_metrics(test["price"], pred),
        "y_pred": pred,
    }


def fit_sarimax(train: pd.DataFrame, test: pd.DataFrame) -> dict | None:
    try:
        from statsmodels.tsa.statespace.sarimax import SARIMAX
    except Exception:
        return None
    # Janela recente: SARIMAX diário em 9k pontos é lento demais para o treino local.
    window = train.tail(400)
    try:
        fitted = SARIMAX(
            window["price"],
            order=(1, 1, 1),
            enforce_stationarity=False,
            enforce_invertibility=False,
        ).fit(disp=False)
        pred = np.asarray(fitted.forecast(steps=len(test)), dtype=float)
    except Exception:
        return None
    return {
        "name": "sarimax",
        "model": fitted,
        "metrics": regression_metrics(test["price"], pred),
        "y_pred": pred,
    }


def horizon_backtest(model, train: pd.DataFrame, test: pd.DataFrame, cols: list[str]) -> dict[str, dict]:
    """MAPE recursivo em 7/15/30 dias a partir do fim do treino."""
    history = train[["date", "price"]].copy()
    actual = test.set_index("date")["price"]
    residual_std = float(np.std(test["price"] - test["lag_1"], ddof=1))
    out: dict[str, dict] = {}
    for horizon in HORIZONS:
        forecast = recursive_forecast(
            model,
            history,
            horizon=horizon,
            feature_cols=cols,
            residual_std=residual_std,
        )
        aligned = forecast.merge(
            actual.rename("actual").reset_index(),
            on="date",
            how="inner",
        )
        if aligned.empty:
            continue
        out[str(horizon)] = regression_metrics(aligned["actual"], aligned["predicted"])
        out[str(horizon)]["n"] = int(len(aligned))
    return out


def rolling_window_scores(features: pd.DataFrame, cols: list[str], folds: int = 4) -> list[dict]:
    """Validação em janela expansiva (sem shuffle)."""
    from xgboost import XGBRegressor

    n = len(features)
    fold_size = 40
    scores = []
    for fold in range(folds):
        test_end = n - fold * fold_size
        test_start = test_end - fold_size
        if test_start < 400:
            break
        train = features.iloc[:test_start]
        test = features.iloc[test_start:test_end]
        model = XGBRegressor(
            n_estimators=200,
            max_depth=5,
            learning_rate=0.05,
            random_state=RANDOM_STATE,
            n_jobs=-1,
        )
        model.fit(train[cols], train["price"])
        pred = model.predict(test[cols])
        metrics = regression_metrics(test["price"], pred)
        metrics["fold"] = fold + 1
        metrics["test_start"] = str(test["date"].min().date())
        metrics["test_end"] = str(test["date"].max().date())
        scores.append(metrics)
    return scores


def train_and_select(
    refresh: bool = False,
    test_days: int = TEST_DAYS,
) -> dict:
    raw = load_or_refresh(refresh=refresh)
    features = build_features(raw)
    save_features(features)
    cols = feature_columns()
    train, test = temporal_split(features, test_days=test_days)

    candidates = [
        fit_naive(train, test),
        fit_random_forest(train, test, cols),
        fit_xgboost(train, test, cols),
    ]
    optional = [fit_lightgbm(train, test, cols), fit_prophet(train, test), fit_sarimax(train, test)]
    candidates.extend([item for item in optional if item is not None])

    comparison = []
    for item in candidates:
        row = {"model": item["name"], **item["metrics"]}
        comparison.append(row)

    usable = [item for item in candidates if item["model"] is not None]
    champion = min(usable, key=lambda item: item["metrics"]["mape"])
    residual = test["price"].to_numpy(dtype=float) - champion["y_pred"]
    residual_std = float(np.std(residual, ddof=1))

    horizons = horizon_backtest(champion["model"], train, test, cols)
    rolling = rolling_window_scores(features, cols)

    bundle = {
        "model": champion["model"],
        "model_name": champion["name"],
        "feature_columns": cols,
        "metrics": champion["metrics"],
        "comparison": comparison,
        "horizon_metrics": horizons,
        "rolling_cv": rolling,
        "residual_std": residual_std,
        "test_days": test_days,
        "train_end": str(train["date"].max().date()),
        "test_start": str(test["date"].min().date()),
        "test_end": str(test["date"].max().date()),
        "series": series_summary(raw),
        "y_true": test["price"].to_numpy(dtype=float),
        "y_pred": champion["y_pred"],
        "y_dates": test["date"].dt.strftime("%Y-%m-%d").to_list(),
        "history_tail": features[["date", "price"]].tail(180).copy(),
    }
    return bundle


def save_bundle(bundle: dict, model_path: Path | None = None, metrics_path: Path | None = None) -> Path:
    target = Path(model_path) if model_path is not None else default_model_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(bundle, target)

    metrics_target = Path(metrics_path) if metrics_path is not None else default_metrics_path()
    metrics_target.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "model_name": bundle["model_name"],
        "metrics": bundle["metrics"],
        "comparison": bundle["comparison"],
        "horizon_metrics": bundle["horizon_metrics"],
        "rolling_cv": bundle["rolling_cv"],
        "residual_std": bundle["residual_std"],
        "train_end": bundle["train_end"],
        "test_start": bundle["test_start"],
        "test_end": bundle["test_end"],
        "series": bundle["series"],
        "y_dates": bundle["y_dates"],
        "y_true": [float(v) for v in bundle["y_true"]],
        "y_pred": [float(v) for v in bundle["y_pred"]],
    }
    metrics_target.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return target


def main() -> None:
    bundle = train_and_select(refresh=False)
    path = save_bundle(bundle)
    print(json.dumps(
        {
            "champion": bundle["model_name"],
            "metrics": bundle["metrics"],
            "comparison": bundle["comparison"],
            "horizon_metrics": bundle["horizon_metrics"],
            "series": bundle["series"],
            "model_path": str(path),
        },
        indent=2,
        ensure_ascii=False,
    ))


if __name__ == "__main__":
    main()
