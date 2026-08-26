"""Funções de limpeza, engenharia de atributos e montagem da pipeline sklearn."""

from __future__ import annotations

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

TARGET_COL = "Obesity"

CAT_COLS = [
    "Gender",
    "family_history",
    "FAVC",
    "CAEC",
    "SMOKE",
    "SCC",
    "CALC",
    "MTRANS",
]

NUM_COLS_RAW = [
    "Age",
    "Height",
    "Weight",
    "FCVC",
    "NCP",
    "CH2O",
    "FAF",
    "TUE",
]

NUM_COLS = NUM_COLS_RAW + ["IMC"]

FEATURE_COLS = CAT_COLS + NUM_COLS_RAW

CLASS_ORDER = [
    "Insufficient_Weight",
    "Normal_Weight",
    "Overweight_Level_I",
    "Overweight_Level_II",
    "Obesity_Type_I",
    "Obesity_Type_II",
    "Obesity_Type_III",
]

LABEL_PT = {
    "Insufficient_Weight": "Abaixo do peso",
    "Normal_Weight": "Peso normal",
    "Overweight_Level_I": "Sobrepeso grau I",
    "Overweight_Level_II": "Sobrepeso grau II",
    "Obesity_Type_I": "Obesidade tipo I",
    "Obesity_Type_II": "Obesidade tipo II",
    "Obesity_Type_III": "Obesidade tipo III",
}

# Faixas clínicas de IMC (OMS) usadas como referência de apoio, não como rótulo do modelo.
IMC_WHO_BANDS = [
    (0.0, 18.5, "Abaixo do peso"),
    (18.5, 25.0, "Peso normal"),
    (25.0, 30.0, "Sobrepeso"),
    (30.0, 35.0, "Obesidade tipo I"),
    (35.0, 40.0, "Obesidade tipo II"),
    (40.0, float("inf"), "Obesidade tipo III"),
]

# Grau de obesidade pela OMS (I/II/III). Abaixo de 30 kg/m² o modelo decide
# entre abaixo do peso, normal e sobrepeso, onde há mais sobreposição na base.
WHO_OBESITY_CLASS = [
    (40.0, "Obesity_Type_III"),
    (35.0, "Obesity_Type_II"),
    (30.0, "Obesity_Type_I"),
]


def add_clinical_features(df: pd.DataFrame) -> pd.DataFrame:
    """Inclui o IMC como métrica clínica de apoio ao modelo."""
    out = df.copy()
    height = out["Height"].astype(float).clip(lower=0.5)
    out["IMC"] = out["Weight"].astype(float) / (height**2)
    return out


def classify_imc(imc: float) -> str:
    for low, high, label in IMC_WHO_BANDS:
        if low <= imc < high:
            return label
    return "Indeterminado"


def who_obesity_class(imc: float) -> str | None:
    """Classe do dataset alinhada ao grau de obesidade da OMS, ou None se IMC < 30."""
    for cutoff, label in WHO_OBESITY_CLASS:
        if imc >= cutoff:
            return label
    return None


def behavioral_risk(payload: dict) -> dict:
    """Perfil de hábitos para a triagem (não substitui o grau pelo IMC)."""
    score = 0
    if str(payload.get("family_history", "")).lower() == "yes":
        score += 2
    if str(payload.get("FAVC", "")).lower() == "yes":
        score += 2
    if payload.get("CAEC") in {"Frequently", "Always"}:
        score += 1
    if float(payload.get("FCVC", 2)) <= 1.5:
        score += 1
    if float(payload.get("FAF", 1)) <= 1:
        score += 2
    if float(payload.get("TUE", 0)) >= 2:
        score += 1
    if payload.get("CALC") in {"Frequently", "Always"}:
        score += 1
    if payload.get("MTRANS") in {"Automobile", "Public_Transportation"}:
        score += 1
    if float(payload.get("CH2O", 2)) <= 1:
        score += 1
    if str(payload.get("SCC", "")).lower() == "no":
        score += 1

    if score >= 8:
        level, label = "alto", "Hábitos de risco elevado"
    elif score >= 4:
        level, label = "moderado", "Hábitos de risco moderado"
    else:
        level, label = "baixo", "Hábitos de menor risco"
    return {"score": score, "level": level, "label": label}


def load_raw_dataset(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = [c for c in FEATURE_COLS + [TARGET_COL] if c not in df.columns]
    if missing:
        raise ValueError(f"Colunas ausentes no dataset: {missing}")
    return df


def split_xy(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    X = add_clinical_features(df.drop(columns=[TARGET_COL]))
    y = df[TARGET_COL]
    return X, y


def build_preprocessor() -> ColumnTransformer:
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUM_COLS),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CAT_COLS),
        ],
        remainder="drop",
    )


def build_model_pipeline(estimator=None) -> Pipeline:
    if estimator is None:
        estimator = RandomForestClassifier(
            n_estimators=150,
            max_depth=12,
            random_state=42,
            n_jobs=-1,
        )
    return Pipeline(
        steps=[
            ("preprocessor", build_preprocessor()),
            ("classifier", estimator),
        ]
    )


def candidate_estimators() -> dict[str, object]:
    return {
        "random_forest": RandomForestClassifier(
            n_estimators=150,
            max_depth=12,
            random_state=42,
            n_jobs=-1,
        ),
        "gradient_boosting": GradientBoostingClassifier(
            n_estimators=120,
            learning_rate=0.08,
            max_depth=3,
            random_state=42,
        ),
    }
