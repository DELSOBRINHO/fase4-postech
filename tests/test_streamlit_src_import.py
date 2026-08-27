"""Garante que o pacote src do repositório não é sombreado por /mount/src."""

import sys
import types
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent / "app"
sys.path.insert(0, str(APP_DIR))

from repo_path import ROOT, prepare_sys_path  # noqa: E402


def test_prepare_sys_path_clears_mount_shadow():
    fake = types.ModuleType("src")
    fake.__path__ = ["/mount/src"]
    sys.modules["src"] = fake
    sys.path.insert(0, "/mount")
    prepare_sys_path(ROOT)
    from data_pipeline import RISK_LABELS, behavioral_risk_frame

    assert "alto" in RISK_LABELS
    assert callable(behavioral_risk_frame)


if __name__ == "__main__":
    test_prepare_sys_path_clears_mount_shadow()
    print("ok")
