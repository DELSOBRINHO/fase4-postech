"""Garante o carregamento dos módulos pelo caminho do arquivo."""

import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent / "app"
sys.path.insert(0, str(APP_DIR))

from repo_path import ROOT, load_project_modules  # noqa: E402


def test_load_project_modules():
    root, data_loader, feature_engineering, model_trainer = load_project_modules(ROOT)
    assert root == ROOT
    assert data_loader.IPEA_SERCODIGO == "EIA366_PBRENT366"
    assert callable(feature_engineering.build_features)
    assert callable(model_trainer.regression_metrics)
    assert "lag_1" in feature_engineering.feature_columns()


if __name__ == "__main__":
    test_load_project_modules()
    print("ok")
