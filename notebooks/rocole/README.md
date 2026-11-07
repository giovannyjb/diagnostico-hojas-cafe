# Notebooks — RoCoLe

Cuadernos del conjunto **RoCoLe** (robusta). Datos: `data/raw/RoCoLe/` → `data/curated/rocole/` → `data/featured/rocole/`.

| Notebook | Qué hace | Quién |
|----------|----------|-------|
| `01-eda-rocole.ipynb` | EDA, limpieza, curación, `plant_key`, split train/val/test | Equipo |
| `02-caracteristicas-rocole.ipynb` | GLCM + índices RGB desde el índice; guarda `glcm_features.csv` y `rgb_features.csv` | Víctor, Gio |
| `03-modelo-glcm-rf.ipynb` | Random Forest con GLCM (train → val → test) | Víctor |
| `04-modelo-rgb-logistica.ipynb` | Regresión logística con índices RGB (train → val → test) | Gio |

Orden: correr **01** (ya curado), luego **02** (genera features), después **03** y **04** en paralelo.

Rutas desde aquí: `../../data/...`, `../../experiments/...`. Semilla `42`.
