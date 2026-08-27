"""Resolve o pacote `src` do repositório no Streamlit Cloud.

O Cloud clona em `/mount/src/<repo>`. Se `/mount` entra no `sys.path`,
`import src` aponta para o diretório de mount, não para `fase4-postech/src`.
"""

from __future__ import annotations

import sys
from pathlib import Path

_APP_DIR = Path(__file__).resolve().parent
ROOT = _APP_DIR.parent


def prepare_sys_path(root: Path | None = None) -> Path:
    project_root = Path(root) if root is not None else ROOT
    filtered = []
    for entry in sys.path:
        try:
            resolved = Path(entry).resolve()
        except OSError:
            filtered.append(entry)
            continue
        if resolved == Path("/mount"):
            continue
        filtered.append(entry)
    sys.path[:] = filtered
    root_s = str(project_root)
    if root_s in sys.path:
        sys.path.remove(root_s)
    sys.path.insert(0, root_s)

    loaded = sys.modules.get("src")
    if loaded is not None:
        project_src = str((project_root / "src").resolve())
        locations = []
        if getattr(loaded, "__file__", None):
            locations.append(str(Path(loaded.__file__).resolve()))
        locations.extend(str(Path(p).resolve()) for p in getattr(loaded, "__path__", []) or [])
        if not any(loc.startswith(project_src) for loc in locations):
            del sys.modules["src"]
            for name in [key for key in sys.modules if key.startswith("src.")]:
                del sys.modules[name]
    return project_root
