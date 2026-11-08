# Notebooks — RoCoLe

Cuadernos del conjunto **RoCoLe** (robusta). Datos: `data/raw/RoCoLe/` → `data/curated/rocole/` → `data/featured/rocole/`.

Semilla fija `42`. Split solo en `data/featured/rocole/index.csv` (no se rehace en modelos). Etiqueta de los baselines: `Binary.Label`.

---

## Pipelines (congelados en esta rama)

Tres líneas. No mezclar aciertos entre ellas sin decirlo.

### A — Producción / foto completa (canónico sin máscara)

`01` → `02` → `03` → `04`

| Notebook | Rol |
|----------|-----|
| `01-eda-rocole.ipynb` | EDA, curación, `plant_key`, split train/val/test |
| `02-caracteristicas-rocole.ipynb` | Piloto + inventario **sin máscara** → `rgb_glcm_features.csv` |
| `03-eda-rocole-featured-exploration.ipynb` | EDA featured; drop VARI; 7 columnas |
| `04-baseline-logistica-rf.ipynb` | Baseline mayoría / logística / RF (7 cols, sin VARI) |

### B — Experimento máscara COCO (paralelo al A)

`02-masked` → `03-masked` → `04-masked` → `05`

| Notebook | Rol |
|----------|-----|
| `02-caracteristicas-rocole-masked.ipynb` | Inventario **con máscara Leaf** → `rgb_glcm_features_masked.csv` |
| `03-eda-rocole-featured-exploration-masked.ipynb` | Mismo EDA sobre masked; drop VARI |
| `04-baseline-logistica-rf-masked.ipynb` | Mismo protocolo de modelo que el 04, sobre masked |
| `05-comparacion-baseline-mascara.ipynb` | Compara A vs B en las **mismas** 226 hojas de test (lee métricas; no reentrena) |

### C — Desarrollo HSV (sobre máscara; no sustituye A/B)

`02-hsv-masked` → `03-eda-hsv-masked` → `04-hsv-masked`

| Notebook | Rol |
|----------|-----|
| `02-caracteristicas-rocole-hsv-masked.ipynb` | Histograma HSV chico (H8/S4/V4) masked → `hsv_hist_features_masked.csv` |
| `03-eda-rocole-hsv-masked.ipynb` | EDA HSV; decisión go: sumar a RGB/GLCM |
| `04-baseline-logistica-rf-hsv-masked.ipynb` | Baseline **7 RGB/GLCM + 16 HSV** (no es HSV solo) |

**Pausa:** no abrir más familias ni más baselines hasta decidir selección de variables (permutación / coeficientes en val).

---

## Protocolo común de evaluación (todos los 04)

Para que los modelos sean comparables:

1. Mismo `index.csv` / misma columna `split` (train / val / test).
2. Train ajusta; **val** elige hiperparámetros (`f1_macro`); **test** se mira **una vez**.
3. Modelos: mayoría (`most_frequent`) + logística (`StandardScaler` fit solo train, `class_weight=balanced`) + Random Forest (`class_weight=balanced`, `random_state=42`).
4. Sin VARI en los baselines.
5. Test = holdout del índice: **226** hojas (115 healthy / 111 unhealthy), idénticas en A/B/C tras merge por `File`.
6. Métricas guardadas en `experiments/results/`:
   - por protocolo: `rocole_baseline_*_metrics.csv`, `*_val_comparison.csv`, matrices PNG
   - tabla unificada (accuracy, recall macro, f1 macro, kappa, recalls por clase): `rocole_baselines_test_metrics_extended.csv`

---

## Qué es redundante (y se deja a propósito)

| Pieza | Nota |
|-------|------|
| Piloto máscara vs full **dentro** del `02` | Didáctico; el inventario masked “de verdad” es el `02-masked`. No borrar el piloto. |
| `03` y `03-masked` / `03-hsv` | No son duplicados: misma plantilla EDA, **distinta tabla**. |
| `04` / `04-masked` / `04-hsv` | Misma plantilla de modelo, distinto feature set. |
| `05` vs CSV extended | El `05` narra A vs B y valida alineación; el CSV extended resume números de A/B/C. |

No consolidar cuadernos en esta pausa: primero versionar pipelines claros.

---

## Resultados rápidos (test, f1_macro / kappa)

Referencia; detalle en `rocole_baselines_test_metrics_extended.csv`.

| Protocolo | Logística f1 / kappa | RF f1 / kappa |
|-----------|----------------------|---------------|
| A sin máscara | ~0.56 / ~0.12 | ~0.54 / ~0.08 |
| B máscara 7 cols | ~0.61 / ~0.21 | ~0.68 / ~0.35 |
| C máscara 7+HSV | ~0.68 / ~0.35 | ~0.74 / ~0.49 |

---

Rutas desde aquí: `../../data/...`, `../../experiments/...`.
