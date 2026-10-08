"""Entrenamiento y exportación del modelo.

Flujo previsto (Etapa 3):
    1. index = load_index()                       # src/data/load.py
    2. X = [image_to_features(Image.open(p)) ...] # src/features/extract.py
    3. pipeline = StandardScaler + {SVC | RandomForest | GradientBoosting}
    4. validación cruzada estratificada (F1 macro) sobre el split de train
    5. ajustar en train, evaluar en test (src/evaluation)
    6. exportar artefacto a models/modelo.joblib con el contrato de docs/arquitectura.md

Uso futuro:  python -m src.training.train --modelo svm --dataset bracol
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

import joblib

from src.features.extract import DEFAULT_IMAGE_SIZE, FEATURES_VERSION

MODELS_DIR = Path(__file__).resolve().parents[2] / "models"


def exportar_artefacto(pipeline, classes: list[str], dataset: str, cv_f1_macro: float,
                       path: Path = MODELS_DIR / "modelo.joblib") -> Path:
    """Guarda el pipeline entrenado con los metadatos que espera el backend."""
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "pipeline": pipeline,
            "classes": list(classes),
            "image_size": list(DEFAULT_IMAGE_SIZE),
            "features_version": FEATURES_VERSION,
            "trained_at": datetime.now().isoformat(timespec="minutes"),
            "dataset": dataset,
            "cv_f1_macro": float(cv_f1_macro),
        },
        path,
    )
    return path


if __name__ == "__main__":
    raise SystemExit("Pendiente: implementar el flujo descrito en el docstring (Etapa 3).")
