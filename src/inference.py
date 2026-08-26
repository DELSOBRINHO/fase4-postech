"""Inferência compartilhada entre a API FastAPI e o app Streamlit."""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd

from src.data_pipeline import FEATURE_COLS, LABEL_PT, add_clinical_features, classify_imc

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MODEL_PATH = ROOT / "app" / "model.joblib"

_MODEL = None


def load_model(path: Path | None = None):
    global _MODEL
    model_path = path or DEFAULT_MODEL_PATH
    if _MODEL is None:
        if not model_path.exists():
            raise FileNotFoundError(
                f"Modelo não encontrado em {model_path}. Execute `python -m src.train`."
            )
        _MODEL = joblib.load(model_path)
    return _MODEL


def features_to_frame(payload: dict) -> pd.DataFrame:
    missing = [c for c in FEATURE_COLS if c not in payload]
    if missing:
        raise ValueError(f"Campos ausentes: {missing}")
    row = {col: payload[col] for col in FEATURE_COLS}
    return add_clinical_features(pd.DataFrame([row]))


def predict_patient(payload: dict, model=None) -> dict:
    """Devolve classe, IMC e probabilidades a partir das 16 variáveis clínicas."""
    estimator = model if model is not None else load_model()
    frame = features_to_frame(payload)
    prediction = estimator.predict(frame)[0]
    probabilities = estimator.predict_proba(frame)[0]
    classes = list(estimator.classes_)
    imc = float(frame["IMC"].iloc[0])
    return {
        "prediction": str(prediction),
        "prediction_pt": LABEL_PT.get(prediction, str(prediction).replace("_", " ")),
        "imc": round(imc, 2),
        "imc_oms": classify_imc(imc),
        "classes": classes,
        "probabilities": {str(cls): float(prob) for cls, prob in zip(classes, probabilities)},
    }
