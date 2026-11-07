"""Carga e indexado de los datasets (BRACOL, RoCoLe).

Flujo: raw → curated → featured, por dataset.

Objetivo: leer `data/featured/<dataset>/index.csv` con una fila por imagen:
    ruta, etiquetas, plant_key / link_group (si aplica), split

Cada dataset vive en su carpeta: `featured/rocole/`, `featured/bracol/`.
Ver docs/datos.md.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"
CURATED_DIR = Path(__file__).resolve().parents[2] / "data" / "curated"
FEATURED_DIR = Path(__file__).resolve().parents[2] / "data" / "featured"


def build_index(raw_dir: Path = RAW_DIR) -> pd.DataFrame:
    """Recorre data/raw y devuelve el índice de imágenes."""
    raise NotImplementedError("Completar cuando los datasets estén descargados (docs/datos.md).")


def load_index(
    path: Path | None = None,
    *,
    dataset: str = "rocole",
) -> pd.DataFrame:
    """Carga el índice con split de un dataset (`rocole` o `bracol`)."""
    if path is None:
        path = FEATURED_DIR / dataset / "index.csv"
    return pd.read_csv(path)
