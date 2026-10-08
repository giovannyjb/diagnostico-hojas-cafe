"""Extracción de características de una imagen de hoja.

Esta función es la ÚNICA puerta entre una imagen y el modelo: la usan igual el
entrenamiento (notebooks/, src/training) y el backend (backend/app/main.py).
Si cambia, sube FEATURES_VERSION y vuelve a entrenar/exportar el modelo.

Baseline v1 (explicable, rápido): histogramas de color en HSV + estadísticas por canal.
Siguientes versiones previstas: textura (LBP, GLCM) y embeddings de una CNN preentrenada.
"""
from __future__ import annotations

import numpy as np
from PIL import Image

FEATURES_VERSION = "hsv-hist-v1"
DEFAULT_IMAGE_SIZE = (128, 128)
HIST_BINS = 16


def image_to_features(
    img: Image.Image,
    image_size: tuple[int, int] = DEFAULT_IMAGE_SIZE,
    bins: int = HIST_BINS,
) -> np.ndarray:
    """Convierte una imagen PIL en un vector 1-D de características.

    Pasos: RGB → redimensionar → HSV → histograma normalizado por canal (bins)
    + media y desviación por canal. Tamaño del vector: 3*bins + 6.
    """
    hsv = np.asarray(img.convert("RGB").resize(image_size).convert("HSV"), dtype=np.float32) / 255.0
    feats: list[np.ndarray] = []
    for c in range(3):
        canal = hsv[..., c].ravel()
        hist, _ = np.histogram(canal, bins=bins, range=(0.0, 1.0))
        feats.append(hist / max(hist.sum(), 1))
        feats.append(np.array([canal.mean(), canal.std()], dtype=np.float32))
    return np.concatenate(feats).astype(np.float32)
