"""Treina, avalia e serializa a pipeline de classificação de obesidade."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.data_pipeline import (  # noqa: E402
    LABEL_PT,
    candidate_estimators,
    build_model_pipeline,
    load_raw_dataset,
    split_xy,
)

DATA_PATH = ROOT / "data" / "Obesity.csv"
MODEL_PATH = ROOT / "app" / "model.joblib"
METRICS_PATH = ROOT / "documentacao" / "metricas_modelo.json"
MIN_ACCURACY = 0.75


def evaluate(name: str, pipeline, X_train, X_test, y_train, y_test) -> dict:
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    acc = float(accuracy_score(y_test, y_pred))
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="accuracy")
    report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
    labels = list(pipeline.classes_)
    cm = confusion_matrix(y_test, y_pred, labels=labels).tolist()
    return {
        "name": name,
        "test_accuracy": acc,
        "cv_accuracy_mean": float(cv_scores.mean()),
        "cv_accuracy_std": float(cv_scores.std()),
        "classification_report": report,
        "confusion_matrix_labels": labels,
        "confusion_matrix": cm,
        "pipeline": pipeline,
        "y_pred": y_pred,
    }


def main() -> None:
    df = load_raw_dataset(DATA_PATH)
    X, y = split_xy(df)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    results = []
    for name, estimator in candidate_estimators().items():
        pipeline = build_model_pipeline(estimator)
        results.append(evaluate(name, pipeline, X_train, X_test, y_train, y_test))

    results.sort(key=lambda r: r["test_accuracy"], reverse=True)
    best = results[0]
    if best["test_accuracy"] < MIN_ACCURACY:
        raise SystemExit(
            f"Acurácia {best['test_accuracy']:.2%} abaixo do mínimo exigido ({MIN_ACCURACY:.0%})."
        )

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(best["pipeline"], MODEL_PATH)

    serializable = []
    for item in results:
        payload = {k: v for k, v in item.items() if k not in {"pipeline", "y_pred"}}
        serializable.append(payload)

    metrics = {
        "n_rows": int(len(df)),
        "n_features": int(X.shape[1]),
        "test_size": 0.2,
        "random_state": 42,
        "min_accuracy_required": MIN_ACCURACY,
        "champion": best["name"],
        "champion_test_accuracy": best["test_accuracy"],
        "models": serializable,
    }
    METRICS_PATH.write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Dataset: {df.shape[0]} linhas x {df.shape[1]} colunas")
    print("Comparação de modelos:")
    for item in results:
        print(
            f"  - {item['name']}: teste={item['test_accuracy']:.4f} | "
            f"CV={item['cv_accuracy_mean']:.4f} ± {item['cv_accuracy_std']:.4f}"
        )
    print(f"\nModelo campeão: {best['name']}")
    print(f"Acurácia no teste: {best['test_accuracy'] * 100:.2f}%")
    print("\nRelatório de classificação:")
    print(
        classification_report(
            y_test,
            best["y_pred"],
            target_names=[LABEL_PT.get(c, c) for c in best["pipeline"].classes_],
            zero_division=0,
        )
    )
    print(f"Modelo salvo em {MODEL_PATH}")
    print(f"Métricas salvas em {METRICS_PATH}")


if __name__ == "__main__":
    pd.set_option("display.max_columns", 20)
    main()
