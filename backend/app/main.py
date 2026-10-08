"""API del prototipo: recibe la foto de una hoja de café y devuelve el diagnóstico.

Correr (desde backend/):  uvicorn app.main:app --reload --port 8000
Docs interactivas:        http://localhost:8000/docs
Contrato:                 docs/api.md · artefacto del modelo: docs/arquitectura.md
"""
from __future__ import annotations

import io
import os
import sys
from pathlib import Path

import joblib
import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))  # para importar src/ sin instalar el paquete (prototipo)

from src.features.extract import FEATURES_VERSION, image_to_features  # noqa: E402

MODEL_PATH = Path(os.getenv("MODEL_PATH", ROOT / "models" / "modelo.joblib"))

RECOMENDACIONES = {
    "sana": "La hoja parece sana. Sigue monitoreando el lote periódicamente.",
    "roya": "Posible roya. Revisa el envés de otras hojas y consulta al técnico; considera manejo preventivo.",
    "minador": "Posible minador. Revisa galerías en las hojas y consulta al técnico sobre control.",
    "phoma": "Posible phoma. Suele asociarse a frío y viento; consulta al técnico.",
    "cercospora": "Posible cercospora (mancha de hierro). Revisa nutrición y sombra; consulta al técnico.",
}

app = FastAPI(title="Diagnóstico de hojas de café", version="0.1.0")
_artefacto: dict | None = None


def cargar_modelo() -> dict:
    global _artefacto
    if _artefacto is None:
        if not MODEL_PATH.exists():
            raise HTTPException(503, f"No hay modelo en {MODEL_PATH}. Entrena y exporta primero (docs/arquitectura.md).")
        _artefacto = joblib.load(MODEL_PATH)
        if _artefacto.get("features_version") != FEATURES_VERSION:
            raise HTTPException(
                503,
                f"El modelo fue entrenado con features {_artefacto.get('features_version')} "
                f"y el backend usa {FEATURES_VERSION}. Reentrena o alinea versiones.",
            )
    return _artefacto


@app.get("/health")
def health():
    return {"status": "ok", "modelo_cargado": MODEL_PATH.exists(), "features_version": FEATURES_VERSION}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if file.content_type not in {"image/jpeg", "image/png"}:
        raise HTTPException(415, "Envía una imagen JPEG o PNG.")
    try:
        img = Image.open(io.BytesIO(await file.read()))
    except UnidentifiedImageError:
        raise HTTPException(415, "El archivo no es una imagen válida.")

    art = cargar_modelo()
    x = image_to_features(img, image_size=tuple(art["image_size"])).reshape(1, -1)
    pipeline, clases = art["pipeline"], art["classes"]

    if hasattr(pipeline, "predict_proba"):
        proba = pipeline.predict_proba(x)[0]
    else:  # p. ej. SVC sin probability=True
        scores = pipeline.decision_function(x)[0]
        scores = np.atleast_1d(scores)
        proba = np.exp(scores - scores.max()); proba /= proba.sum()
    idx = int(np.argmax(proba))
    clase = str(clases[idx])
    return {
        "clase": clase,
        "confianza": round(float(proba[idx]), 4),
        "probabilidades": {str(c): round(float(p), 4) for c, p in zip(clases, proba)},
        "recomendacion": RECOMENDACIONES.get(clase, "Consulta al técnico agrícola."),
        "modelo": {"features_version": art["features_version"], "trained_at": art.get("trained_at")},
    }
