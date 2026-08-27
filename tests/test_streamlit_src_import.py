"""Garante o carregamento dos módulos pelo caminho do arquivo."""

import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent / "app"
sys.path.insert(0, str(APP_DIR))

from repo_path import ROOT, load_project_modules  # noqa: E402


def test_load_project_modules():
    root, pipeline, inference = load_project_modules(ROOT)
    assert root == ROOT
    assert "alto" in pipeline.RISK_LABELS
    assert callable(pipeline.behavioral_risk_frame)
    assert callable(inference.predict_patient)


if __name__ == "__main__":
    test_load_project_modules()
    print("ok")
