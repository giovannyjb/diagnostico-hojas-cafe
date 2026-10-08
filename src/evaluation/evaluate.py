"""Métricas y reportes de evaluación.

Pendiente (Etapa 3): matriz de confusión por clase, precision/recall/F1 macro,
curvas por clase y evaluación cruzada entre variedades (arábica → robusta).
"""
from __future__ import annotations

from sklearn.metrics import classification_report, confusion_matrix


def reporte(y_true, y_pred, labels=None) -> dict:
    """Devuelve el classification_report (dict) y la matriz de confusión."""
    return {
        "report": classification_report(y_true, y_pred, labels=labels, output_dict=True, zero_division=0),
        "confusion_matrix": confusion_matrix(y_true, y_pred, labels=labels).tolist(),
    }
