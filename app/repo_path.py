"""Carrega o pipeline pelo caminho do arquivo (Streamlit Cloud).

O Cloud clona em `/mount/src/<repo>`. O nome `src` colide com esse mount,
então os módulos são lidos de `src/*.py` por caminho absoluto.
"""

from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path

_APP_DIR = Path(__file__).resolve().parent
ROOT = _APP_DIR.parent
SRC = ROOT / "src"


def _load(mod_name: str, file_path: Path):
    if not file_path.is_file():
        raise ImportError(
            f"Arquivo não encontrado: {file_path} "
            f"(repo_path={Path(__file__).resolve()}, root={ROOT}, "
            f"src_existe={SRC.is_dir()})"
        )
    spec = importlib.util.spec_from_file_location(mod_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Não foi possível criar spec para {mod_name} em {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = module
    spec.loader.exec_module(module)
    return module


def load_project_modules(root: Path | None = None):
    """Devolve (root, data_loader, feature_engineering, model_trainer)."""
    project_root = Path(root) if root is not None else ROOT
    src_dir = project_root / "src"

    pkg = types.ModuleType("src")
    pkg.__path__ = [str(src_dir)]
    pkg.__file__ = str(src_dir / "__init__.py")
    sys.modules["src"] = pkg

    data_loader = _load("src.data_loader", src_dir / "data_loader.py")
    sys.modules["data_loader"] = data_loader
    pkg.data_loader = data_loader

    feature_engineering = _load("src.feature_engineering", src_dir / "feature_engineering.py")
    sys.modules["feature_engineering"] = feature_engineering
    pkg.feature_engineering = feature_engineering

    model_trainer = _load("src.model_trainer", src_dir / "model_trainer.py")
    sys.modules["model_trainer"] = model_trainer
    pkg.model_trainer = model_trainer
    return project_root, data_loader, feature_engineering, model_trainer
