"""Testes do pipeline temporal do Brent (sem rede)."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
import sys

sys.path.insert(0, str(ROOT))

from src.data_loader import calendar_ffill, trading_days  # noqa: E402
from src.feature_engineering import (  # noqa: E402
    build_features,
    feature_columns,
    next_business_day,
    recursive_forecast,
)
from src.model_trainer import mape, regression_metrics, temporal_split  # noqa: E402


def _synthetic_brent(n: int = 220) -> pd.DataFrame:
    dates = pd.bdate_range("2024-01-02", periods=n)
    price = 80 + np.linspace(0, 8, n) + np.sin(np.arange(n) / 8.0)
    return pd.DataFrame({"date": dates, "price": price, "sercodigo": "EIA366_PBRENT366"})


def test_trading_days_drops_null_price():
    frame = pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-01-02", "2024-01-03", "2024-01-04"]),
            "price": [80.0, np.nan, 81.5],
            "sercodigo": ["EIA366_PBRENT366"] * 3,
        }
    )
    clean = trading_days(frame)
    assert len(clean) == 2
    assert clean["price"].notna().all()


def test_calendar_ffill_fills_weekend_gap():
    frame = pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-01-05", "2024-01-08"]),
            "price": [80.0, 82.0],
            "sercodigo": ["EIA366_PBRENT366"] * 2,
        }
    )
    filled = calendar_ffill(frame)
    assert len(filled) == 4
    assert filled["price"].iloc[1] == 80.0


def test_features_use_only_past_prices():
    raw = _synthetic_brent()
    feats = build_features(raw)
    cols = feature_columns()
    assert set(cols).issubset(feats.columns)
    row = feats.iloc[40]
    history = raw.set_index("date")["price"]
    assert abs(row["lag_1"] - history.loc[: row["date"]].iloc[-2]) < 1e-9
    past = history.loc[history.index < row["date"]]
    assert abs(row["ma_7"] - past.tail(7).mean()) < 1e-9


def test_temporal_split_is_strict():
    feats = build_features(_synthetic_brent(200))
    train, test = temporal_split(feats, test_days=30)
    assert train["date"].max() < test["date"].min()
    assert len(test) == 30


def test_recursive_forecast_horizon_and_business_days():
    class _Const:
        def predict(self, frame):
            return np.full(len(frame), 90.0)

    history = _synthetic_brent(120)
    forecast = recursive_forecast(_Const(), history, horizon=7, residual_std=1.0)
    assert len(forecast) == 7
    assert forecast["date"].is_monotonic_increasing
    assert (forecast["date"].dt.dayofweek < 5).all()
    assert forecast["upper"].iloc[-1] > forecast["predicted"].iloc[-1]


def test_next_business_day_skips_weekend():
    friday = pd.Timestamp("2024-01-05")
    assert next_business_day(friday) == pd.Timestamp("2024-01-08")


def test_mape_and_metrics():
    y_true = np.array([100.0, 110.0, 90.0])
    y_pred = np.array([100.0, 121.0, 81.0])
    assert abs(mape(y_true, y_pred) - (0 + 10 + 10) / 3) < 1e-9
    metrics = regression_metrics(y_true, y_pred)
    assert set(metrics) == {"mape", "rmse", "mae", "r2"}


if __name__ == "__main__":
    test_trading_days_drops_null_price()
    test_calendar_ffill_fills_weekend_gap()
    test_features_use_only_past_prices()
    test_temporal_split_is_strict()
    test_recursive_forecast_horizon_and_business_days()
    test_next_business_day_skips_weekend()
    test_mape_and_metrics()
    print("ok")
