# Notebooks — RoCoLe

Cuadernos del conjunto **RoCoLe** (robusta). Datos: `data/raw/RoCoLe/` → `data/curated/rocole/` → `data/featured/rocole/`.

| Notebook | Qué hace | Quién |
|----------|----------|-------|
| `01-eda-rocole.ipynb` | EDA, limpieza, curación, `plant_key`, split train/val/test | Equipo |
| `02-caracteristicas-rocole.ipynb` | GLCM + índices RGB; piloto máscara vs full; inventario sin máscara → `rgb_glcm_features.csv` | Víctor, Gio |
| `03-eda-rocole-featured-exploration.ipynb` | Revisar inventario featured: finitos, percentiles, extremos VARI; decisión sobre `vari_*` | Víctor, Gio |
| `04-baseline-logistica-rf.ipynb` | Baseline: mayoría, logística y Random Forest con 7 medidas (sin VARI); hiperparámetros en val, test una vez | Víctor, Gio |

Orden: **01 → 02 → 03** (decidir features) → **04** (baseline).

Rutas desde aquí: `../../data/...`, `../../experiments/...`. Semilla `42`.
