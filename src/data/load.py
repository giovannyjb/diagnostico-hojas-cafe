"""Carga e indexado de los datasets (BRACOL, RoCoLe).

Objetivo: construir `data/processed/index.csv` con una fila por imagen:
    ruta, dataset, variedad, clase, severidad, split

Pendiente (Etapa 2): revisar cómo vienen las etiquetas en cada dataset
(carpetas / CSV / XML) y completar `build_index`. Ver docs/datos.md.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"
PROCESSED_DIR = Path(__file__).resolve().parents[2] / "data" / "processed"


def build_index(raw_dir: Path = RAW_DIR) -> pd.DataFrame:
    """Recorre data/raw/{bracol,rocole} y devuelve el índice de imágenes."""
    raise NotImplementedError("Completar cuando los datasets estén descargados (docs/datos.md).")


def load_index(path: Path = PROCESSED_DIR / "index.csv") -> pd.DataFrame:
    return pd.read_csv(path)
