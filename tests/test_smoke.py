"""Pruebas mínimas: la extracción de características y el backend arrancan."""
import sys
from pathlib import Path

import numpy as np
import pytest
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.features.extract import HIST_BINS, image_to_features  # noqa: E402


def test_image_to_features_tamano_fijo():
    img = Image.new("RGB", (640, 480), color=(30, 120, 40))
    x = image_to_features(img)
    assert x.shape == (3 * HIST_BINS + 6,)
    assert np.isfinite(x).all()


def test_health_sin_modelo():
    pytest.importorskip("fastapi")
    from fastapi.testclient import TestClient

    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
    from app.main import app

    r = TestClient(app).get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
