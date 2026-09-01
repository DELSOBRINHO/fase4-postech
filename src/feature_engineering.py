"""Atributos temporais para forecasting do Brent (sem vazamento de informação)."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

LAGS = (1, 2, 3, 5, 7, 15, 30)
ROLLING_MEANS = (7, 14, 30, 90)
ROLLING_VOLS = (7, 30)
CALENDAR_COLS = ("weekday", "month", "quarter", "dayofyear")


def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def default_features_path() -> Path:
    return project_root() / "data" / "processed" / "brent_oil_features.parquet"


def feature_columns() -> list[str]:
    cols = [f"lag_{lag}" for lag in LAGS]
    cols += [f"ma_{window}" for window in ROLLING_MEANS]
    cols += [f"vol_{window}" for window in ROLLING_VOLS]
    cols += list(CALENDAR_COLS)
    return cols


def add_calendar(frame: pd.DataFrame, date_col: str = "date") -> pd.DataFrame:
    out = frame.copy()
    dates = pd.to_datetime(out[date_col])
    out["weekday"] = dates.dt.dayofweek.astype(int)
    out["month"] = dates.dt.month.astype(int)
    out["quarter"] = dates.dt.quarter.astype(int)
    out["dayofyear"] = dates.dt.dayofyear.astype(int)
    return out


def add_lag_features(frame: pd.DataFrame, price_col: str = "price") -> pd.DataFrame:
    """Lags e janelas móveis usam apenas informação até t−1."""
    out = frame.sort_values("date").reset_index(drop=True).copy()
    prices = out[price_col]
    for lag in LAGS:
        out[f"lag_{lag}"] = prices.shift(lag)
    shifted = prices.shift(1)
    for window in ROLLING_MEANS:
        out[f"ma_{window}"] = shifted.rolling(window, min_periods=window).mean()
    for window in ROLLING_VOLS:
        out[f"vol_{window}"] = shifted.rolling(window, min_periods=window).std()
    return out


def build_features(frame: pd.DataFrame) -> pd.DataFrame:
    work = frame.dropna(subset=["date", "price"]).sort_values("date").drop_duplicates("date")
    work = add_lag_features(work)
    work = add_calendar(work)
    work = work.dropna(subset=feature_columns()).reset_index(drop=True)
    return work


def save_features(frame: pd.DataFrame, path: Path | None = None) -> Path:
    target = Path(path) if path is not None else default_features_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    frame.to_parquet(target, index=False)
    return target


def load_features(path: Path | None = None) -> pd.DataFrame:
    target = Path(path) if path is not None else default_features_path()
    frame = pd.read_parquet(target)
    frame["date"] = pd.to_datetime(frame["date"])
    return frame


def next_business_day(value) -> pd.Timestamp:
    current = pd.Timestamp(value).normalize() + pd.Timedelta(days=1)
    while int(current.dayofweek) >= 5:
        current += pd.Timedelta(days=1)
    return current


def _safe_lag(prices: pd.Series, lag: int) -> float:
    if len(prices) >= lag:
        return float(prices.iloc[-lag])
    return float(prices.iloc[0])


def next_feature_row(history: pd.DataFrame, next_date) -> pd.DataFrame:
    """Monta o vetor de atributos do próximo dia útil a partir da história conhecida."""
    work = history.sort_values("date")
    prices = work["price"]
    nxt = pd.Timestamp(next_date).normalize()
    row: dict[str, float | int | pd.Timestamp] = {"date": nxt}
    for lag in LAGS:
        row[f"lag_{lag}"] = _safe_lag(prices, lag)
    for window in ROLLING_MEANS:
        row[f"ma_{window}"] = float(prices.iloc[-window:].mean()) if len(prices) else np.nan
    for window in ROLLING_VOLS:
        window_prices = prices.iloc[-window:]
        row[f"vol_{window}"] = float(window_prices.std(ddof=1)) if len(window_prices) > 1 else 0.0
    cal = add_calendar(pd.DataFrame({"date": [nxt]}))
    for col in CALENDAR_COLS:
        row[col] = int(cal[col].iloc[0])
    return pd.DataFrame([row])


def recursive_forecast(
    model,
    history: pd.DataFrame,
    horizon: int,
    feature_cols: list[str] | None = None,
    residual_std: float = 0.0,
) -> pd.DataFrame:
    """Projeção recursiva de N dias úteis, com faixa ±1,96·σ·√h."""
    cols = feature_cols or feature_columns()
    work = history[["date", "price"]].copy().sort_values("date").reset_index(drop=True)
    rows: list[dict] = []
    sigma = float(residual_std) if residual_std and residual_std > 0 else 0.0
    for step in range(1, int(horizon) + 1):
        nxt = next_business_day(work["date"].iloc[-1])
        features = next_feature_row(work, nxt)
        yhat = float(model.predict(features[cols])[0])
        band = 1.96 * sigma * float(np.sqrt(step)) if sigma else 0.0
        rows.append(
            {
                "date": nxt,
                "predicted": yhat,
                "lower": yhat - band,
                "upper": yhat + band,
                "horizon": step,
            }
        )
        work = pd.concat(
            [work, pd.DataFrame([{"date": nxt, "price": yhat}])],
            ignore_index=True,
        )
    return pd.DataFrame(rows)
