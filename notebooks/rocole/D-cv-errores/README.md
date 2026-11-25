# Pipeline D — CV por planta y errores (protocolo C)

Profundización sobre el protocolo **C** (7 RGB/GLCM masked sin VARI + 16 HSV). No reabre familias de features ni edita A/B/C.

Orden: `05-cv-grupos-modelos-c` → `06-sensibilidad-multiclass-c` → `07-analisis-falsos-negativos-c`

| Notebook | Rol |
|----------|-----|
| `05-cv-grupos-modelos-c.ipynb` | GroupKFold por `link_group`; logística, RF, SVM, HistGradientBoosting; `f1_macro` con IC 95% |
| `06-sensibilidad-multiclass-c.ipynb` | Sensibilidad por `Multiclass.Label` sobre predicciones OOF (foco `rust_level_1`) |
| `07-analisis-falsos-negativos-c.ipynb` | Caracterización sistemática de falsos negativos OOF |

- Entrada: `index.csv`, `rgb_glcm_features_masked.csv`, `hsv_hist_features_masked.csv`
- Resultados: `experiments/results/rocole/D-cv-errores/`
- Rutas desde esta carpeta: `../../../data/...`, `../../../experiments/...`

**Resumen:** ganador CV = RF (`f1_macro` 0.796); `rust_level_1` sensibilidad OOF ≈ 0.67; 149 FN, mayormente roya leve.
