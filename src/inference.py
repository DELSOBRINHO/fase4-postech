"""Inferência compartilhada entre a API FastAPI e o app Streamlit."""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd

try:
    from src.data_pipeline import (
        FEATURE_COLS,
        LABEL_PT,
        add_clinical_features,
        behavioral_risk,
        classify_imc,
        who_obesity_class,
    )
except ImportError:
    from data_pipeline import (
        FEATURE_COLS,
        LABEL_PT,
        add_clinical_features,
        behavioral_risk,
        classify_imc,
        who_obesity_class,
    )

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


def _lock_class_probabilities(classes: list, probabilities, locked: str) -> dict[str, float]:
    """Garante que a classe clínica alinhada à OMS seja a de maior probabilidade."""
    probs = {str(cls): float(p) for cls, p in zip(classes, probabilities)}
    current = probs.get(locked, 0.0)
    if current >= 0.5 and locked == max(probs, key=probs.get):
        return probs
    leftover = max(1.0 - 0.85, 0.0)
    others = [(k, v) for k, v in probs.items() if k != locked]
    total_others = sum(v for _, v in others)
    probs[locked] = 0.85
    if total_others > 0:
        for key, value in others:
            probs[key] = leftover * (value / total_others)
    else:
        share = leftover / max(len(others), 1)
        for key, _ in others:
            probs[key] = share
    return probs


def predict_patient(payload: dict, model=None) -> dict:
    """Devolve classe, IMC e probabilidades a partir das 16 variáveis clínicas.

    O Gradient Boosting aprende artefatos da base (em obesidade tipo III o NCP
    é sempre 3 e o gênero é quase só feminino). No app, o grau I/II/III segue
    o IMC da OMS; hábitos alimentares e rotina entram no perfil de risco.
    """
    estimator = model if model is not None else load_model()
    frame = features_to_frame(payload)
    ml_prediction = str(estimator.predict(frame)[0])
    raw_probabilities = estimator.predict_proba(frame)[0]
    classes = list(estimator.classes_)
    imc = float(frame["IMC"].iloc[0])
    locked = who_obesity_class(imc)
    prediction = locked if locked else ml_prediction
    reconciled = bool(locked) and locked != ml_prediction
    probabilities = (
        _lock_class_probabilities(classes, raw_probabilities, prediction)
        if locked
        else {str(cls): float(prob) for cls, prob in zip(classes, raw_probabilities)}
    )
    risk = behavioral_risk(payload)
    return {
        "prediction": prediction,
        "prediction_pt": LABEL_PT.get(prediction, prediction.replace("_", " ")),
        "ml_prediction": ml_prediction,
        "ml_prediction_pt": LABEL_PT.get(ml_prediction, ml_prediction.replace("_", " ")),
        "reconciled": reconciled,
        "imc": round(imc, 2),
        "imc_oms": classify_imc(imc),
        "behavioral_risk": risk,
        "classes": classes,
        "probabilities": probabilities,
    }
