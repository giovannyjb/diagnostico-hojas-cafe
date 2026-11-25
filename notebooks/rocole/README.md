# Notebooks — RoCoLe

Cuadernos del conjunto **RoCoLe** (robusta). Datos: `data/raw/RoCoLe/` → `data/curated/rocole/` → `data/featured/rocole/`.

Semilla fija `42`. Split solo en `data/featured/rocole/index.csv` (no se rehace en modelos). Etiqueta de los baselines: `Binary.Label`.

Compartido en la raíz de esta carpeta: `01-eda-rocole.ipynb` (EDA, curación, split).

Los tres pipelines viven en subcarpetas para no mezclar pruebas.

---

## Pipelines

### A — Foto completa (canónico sin máscara)

Carpeta: [`A-full/`](A-full/)

`01` → `A-full/02` → `A-full/03` → `A-full/04`

| Notebook | Rol |
|----------|-----|
| `01-eda-rocole.ipynb` | EDA, curación, `plant_key`, split train/val/test |
| `A-full/02-caracteristicas-rocole.ipynb` | Inventario **sin máscara** → `rgb_glcm_features.csv` |
| `A-full/03-eda-rocole-featured-exploration.ipynb` | EDA featured; drop VARI; 7 columnas |
| `A-full/04-baseline-logistica-rf.ipynb` | Baseline mayoría / logística / RF |

Resultados: `experiments/results/rocole/A-full/`

### B — Máscara COCO (paralelo a A)

Carpeta: [`B-masked/`](B-masked/)

`B-masked/02` → `03` → `04` → `05`

| Notebook | Rol |
|----------|-----|
| `02-caracteristicas-rocole-masked.ipynb` | Inventario **con máscara Leaf** → `rgb_glcm_features_masked.csv` |
| `03-eda-rocole-featured-exploration-masked.ipynb` | Mismo EDA sobre masked; drop VARI |
| `04-baseline-logistica-rf-masked.ipynb` | Mismo protocolo de modelo, sobre masked |
| `05-comparacion-baseline-mascara.ipynb` | Compara A vs B en las **mismas** 226 hojas de test |

Resultados: `experiments/results/rocole/B-masked/`

### C — HSV sobre máscara (desarrollo; no sustituye A/B)

Carpeta: [`C-hsv-masked/`](C-hsv-masked/)

`C-hsv-masked/02` → `03` → `04`

| Notebook | Rol |
|----------|-----|
| `02-caracteristicas-rocole-hsv-masked.ipynb` | Histograma HSV chico (H8/S4/V4) masked → `hsv_hist_features_masked.csv` |
| `03-eda-rocole-hsv-masked.ipynb` | EDA HSV; go: sumar a RGB/GLCM |
| `04-baseline-logistica-rf-hsv-masked.ipynb` | Baseline **7 RGB/GLCM + 16 HSV** |

Resultados: `experiments/results/rocole/C-hsv-masked/`

### D — CV por planta y errores (sobre protocolo C)

Carpeta: [`D-cv-errores/`](D-cv-errores/)

Profundización del protocolo C (23 features) sin reabrir A/B/C ni el holdout histórico de test para elegir ganador.

`D-cv-errores/05` → `06` → `07`

| Notebook | Rol |
|----------|-----|
| `05-cv-grupos-modelos-c.ipynb` | GroupKFold por `link_group`; logística / RF / SVM / HistGB; `f1_macro` + IC 95% |
| `06-sensibilidad-multiclass-c.ipynb` | Sensibilidad OOF por `Multiclass.Label` (foco `rust_level_1`) |
| `07-analisis-falsos-negativos-c.ipynb` | FN OOF: severidad, proxy de lesión HSV, iluminación, cobertura Leaf |

Resultados: `experiments/results/rocole/D-cv-errores/`

**CV por planta (D-05, media ± IC 95% `f1_macro`):** RF **0.796** [0.778, 0.814] · HistGB 0.780 [0.745, 0.815] · SVM 0.767 [0.719, 0.816] · logística 0.741 [0.725, 0.757]. Ganador por CV: **random_forest**.

**Sensibilidad OOF unhealthy (D-06, ganador):** `rust_level_1` **0.67** (109 FN / 333) · `rust_level_2` 0.84 · ácaro 0.91 · niveles 3–4 ≥ 0.98.

**FN (D-07):** 149 unhealthy→healthy; se concentran en roya leve y menor masa de matiz no verde; iluminación y cobertura de máscara casi no separan FN de TP.

---

## Protocolo común de evaluación

1. Mismo `index.csv` / misma columna `split`.
2. Train ajusta; **val** elige hiperparámetros (`f1_macro`); **test** se mira **una vez**.
3. Modelos: mayoría + logística (scaler fit solo train) + Random Forest; `class_weight=balanced`; seed 42.
4. Sin VARI en los baselines.
5. Test = **226** hojas (115 healthy / 111 unhealthy), idénticas en A/B/C.
6. Tabla unificada: `experiments/results/rocole/comparacion/rocole_baselines_test_metrics_extended.csv`

---

## Resultados rápidos (test)

| Protocolo | Logística f1 / kappa | RF f1 / kappa |
|-----------|----------------------|---------------|
| A sin máscara | ~0.56 / ~0.12 | ~0.54 / ~0.08 |
| B máscara 7 cols | ~0.61 / ~0.21 | ~0.68 / ~0.35 |
| C máscara 7+HSV | ~0.68 / ~0.35 | ~0.74 / ~0.49 |

Rutas desde subcarpetas A/B/C/D: `../../../data/...`, `../../../experiments/...`.
Desde esta raíz (`01`): `../../data/...`.
