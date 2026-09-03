"""Extração e tratamento da série Brent FOB do IPEA Data.

Série oficial da prova substitutiva (serid 1650971490):
`EIA366_PBRENT366` — preço do petróleo bruto tipo Brent (FOB), US$/barril.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import requests

IPEA_SERID = "1650971490"
IPEA_SERCODIGO = "EIA366_PBRENT366"
ODATA_URL = (
    "https://www.ipeadata.gov.br/api/odata4/"
    f"ValoresSerie(SERCODIGO='{IPEA_SERCODIGO}')"
)
HTML_URL = (
    "http://www.ipeadata.gov.br/ExibeSerie.aspx"
    f"?module=m&serid={IPEA_SERID}&oper=view"
)
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; BrentForecast/1.0; "
        "+https://github.com/DELSOBRINHO/fase4-postech)"
    ),
    "Accept": "application/json,text/html;q=0.9",
}

RAW_COLUMNS = ["date", "price", "sercodigo"]


def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def default_raw_path() -> Path:
    return project_root() / "data" / "raw" / "brent_oil_raw.csv"


def _parse_ipea_frame(frame: pd.DataFrame) -> pd.DataFrame:
    if frame.empty:
        raise ValueError("A resposta do IPEA não contém registros.")

    rename = {}
    if "VALDATA" in frame.columns:
        rename["VALDATA"] = "date"
    if "VALVALOR" in frame.columns:
        rename["VALVALOR"] = "price"
    if "SERCODIGO" in frame.columns:
        rename["SERCODIGO"] = "sercodigo"
    if "Data" in frame.columns:
        rename["Data"] = "date"
    if "Preço - petróleo bruto - Brent (FOB)" in frame.columns:
        rename["Preço - petróleo bruto - Brent (FOB)"] = "price"

    out = frame.rename(columns=rename).copy()
    if "date" not in out.columns:
        date_col = next((c for c in out.columns if "data" in c.lower() or "date" in c.lower()), None)
        if date_col is None:
            raise ValueError(f"Coluna de data não encontrada: {list(out.columns)}")
        out = out.rename(columns={date_col: "date"})
    if "price" not in out.columns:
        price_col = next(
            (c for c in out.columns if "valor" in c.lower() or "preço" in c.lower() or "preco" in c.lower()),
            None,
        )
        if price_col is None:
            raise ValueError(f"Coluna de preço não encontrada: {list(out.columns)}")
        out = out.rename(columns={price_col: "price"})

    out["date"] = pd.to_datetime(out["date"], errors="coerce", utc=True).dt.tz_localize(None).dt.normalize()
    out["price"] = pd.to_numeric(out["price"], errors="coerce")
    if "sercodigo" not in out.columns:
        out["sercodigo"] = IPEA_SERCODIGO
    out = out.dropna(subset=["date"]).sort_values("date").drop_duplicates(subset=["date"], keep="last")
    return out[RAW_COLUMNS].reset_index(drop=True)


ODATA_URLS = (
    ODATA_URL,
    ODATA_URL.replace("https://", "http://"),
)
FRED_BRENT_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DCOILBRENTEU"


def fetch_ipea_odata(timeout: int = 90) -> pd.DataFrame:
    """Lê a série completa via API OData 4 do IPEA.

    A API frequentemente ignora `$top/$skip` e devolve a série inteira de uma vez.
    """
    last_error: Exception | None = None
    for base in ODATA_URLS:
        try:
            response = requests.get(base, headers=HEADERS, timeout=timeout)
            response.raise_for_status()
            payload = response.json()
            rows = payload.get("value", payload if isinstance(payload, list) else [])
            if not rows:
                raise ValueError("API OData do IPEA retornou lista vazia.")
            return _parse_ipea_frame(pd.DataFrame(rows))
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            continue
    raise RuntimeError(f"OData IPEA indisponível: {last_error}")


def fetch_ipea_html(timeout: int = 90) -> pd.DataFrame:
    """Fallback: lê a tabela HTML da página ExibeSerie do IPEA."""
    from io import StringIO

    response = requests.get(HTML_URL, headers=HEADERS, timeout=timeout)
    response.raise_for_status()
    tables = pd.read_html(StringIO(response.text), decimal=",", thousands=".")
    if not tables:
        raise ValueError("Nenhuma tabela HTML encontrada na página do IPEA.")
    candidate = max(tables, key=len)
    return _parse_ipea_frame(candidate)


def fetch_fred_brent(timeout: int = 60) -> pd.DataFrame:
    """Contingência: série diária DCOILBRENTEU (EIA) no FRED, mesma commodity."""
    response = requests.get(FRED_BRENT_URL, headers=HEADERS, timeout=timeout)
    response.raise_for_status()
    from io import StringIO

    frame = pd.read_csv(StringIO(response.text))
    frame = frame.rename(
        columns={
            "DATE": "date",
            "observation_date": "date",
            "DCOILBRENTEU": "price",
        }
    )
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    frame["price"] = pd.to_numeric(frame["price"], errors="coerce")
    frame["sercodigo"] = "FRED_DCOILBRENTEU"
    return trading_days(frame)


def fetch_ipea_brent(timeout: int = 90) -> pd.DataFrame:
    """Tenta OData e, se falhar, a página HTML do IPEA (série oficial da prova)."""
    errors: list[str] = []
    try:
        return fetch_ipea_odata(timeout=timeout)
    except Exception as exc:  # noqa: BLE001
        errors.append(f"OData: {type(exc).__name__}: {exc}")
    try:
        return fetch_ipea_html(timeout=timeout)
    except Exception as exc:  # noqa: BLE001
        errors.append(f"HTML: {type(exc).__name__}")
    raise RuntimeError("Falha ao extrair a série Brent do IPEA. " + " | ".join(errors))


def trading_days(frame: pd.DataFrame) -> pd.DataFrame:
    """Mantém apenas dias com cotação oficial em dias úteis de mercado."""
    out = frame.dropna(subset=["date", "price"]).copy()
    out["date"] = pd.to_datetime(out["date"], errors="coerce")
    out = out.dropna(subset=["date"])
    out = out[out["date"].dt.dayofweek < 5]
    return out.sort_values("date").drop_duplicates(subset=["date"], keep="last").reset_index(drop=True)


def calendar_ffill(frame: pd.DataFrame) -> pd.DataFrame:
    """Calendário contínuo com forward fill nos dias sem cotação."""
    work = frame.dropna(subset=["date"]).sort_values("date").drop_duplicates("date")
    full_idx = pd.date_range(work["date"].min(), work["date"].max(), freq="D")
    filled = (
        work.set_index("date")
        .reindex(full_idx)
        .rename_axis("date")
        .reset_index()
    )
    filled["price"] = filled["price"].ffill()
    filled["sercodigo"] = filled["sercodigo"].ffill().fillna(IPEA_SERCODIGO)
    return filled.dropna(subset=["price"]).reset_index(drop=True)


def save_raw(frame: pd.DataFrame, path: Path | None = None) -> Path:
    target = Path(path) if path is not None else default_raw_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    trading_days(frame)[RAW_COLUMNS].to_csv(target, index=False)
    return target


def load_raw(path: Path | None = None) -> pd.DataFrame:
    target = Path(path) if path is not None else default_raw_path()
    if not target.is_file():
        raise FileNotFoundError(f"Série bruta não encontrada: {target}")
    frame = pd.read_csv(target)
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    frame["price"] = pd.to_numeric(frame["price"], errors="coerce")
    return trading_days(frame)


def load_or_refresh(
    path: Path | None = None,
    refresh: bool = False,
    timeout: int = 90,
) -> pd.DataFrame:
    """Carrega o CSV versionado; opcionalmente tenta atualizar pelo IPEA.

    O FRED só entra se não houver arquivo local — não sobrescreve a série oficial.
    """
    target = Path(path) if path is not None else default_raw_path()
    local: pd.DataFrame | None = None
    if target.is_file():
        local = load_raw(target)
        if not refresh:
            return local
    try:
        remote = trading_days(fetch_ipea_brent(timeout=timeout))
        save_raw(remote, target)
        return remote
    except Exception:
        if local is not None:
            return local
        remote = trading_days(fetch_fred_brent(timeout=min(timeout, 60)))
        save_raw(remote, target)
        return remote


def series_summary(frame: pd.DataFrame) -> dict:
    work = trading_days(frame)
    return {
        "n_obs": int(len(work)),
        "start": str(work["date"].min().date()) if len(work) else None,
        "end": str(work["date"].max().date()) if len(work) else None,
        "last_price": float(work["price"].iloc[-1]) if len(work) else None,
        "min_price": float(work["price"].min()) if len(work) else None,
        "max_price": float(work["price"].max()) if len(work) else None,
        "source": IPEA_SERCODIGO,
        "serid": IPEA_SERID,
    }


if __name__ == "__main__":
    raw = load_or_refresh(refresh=True)
    print(json.dumps(series_summary(raw), indent=2, ensure_ascii=False))
    print(f"salvo em {default_raw_path()}")
