# featured/rocole

- `index.csv` — `File`, `plant_key`, `link_group`, etiquetas, `split`, `photo_path` (seed `42`)
- `rgb_glcm_features.csv` — inventario **sin máscara** (producción): identidad + ExG/NGRDI/VARI (mean/std) + GLCM contraste/homogeneidad/energía + `error`
- `rgb_glcm_features_masked.csv` — inventario **con máscara COCO Leaf**: mismas 9 medidas + `error`; si falta máscara, NaN en features (sin fallback a foto completa)
- `hsv_hist_features_masked.csv` — inventario **HSV masked** (rama de desarrollo): identidad + 16 bins (`hsv_h_b0..b7`, `hsv_s_b0..b3`, `hsv_v_b0..b3`, normalizados a suma 1 por canal dentro de Leaf) + `error`; sin fallback a foto completa

Protocolo sin máscara: foto completa, GLCM 32 niveles, distancia 1, ángulo 0. Protocolo masked RGB/GLCM: solo píxeles Leaf (OR de anotaciones COCO); GLCM en bbox con fuera-hoja en 0, mismos 32 niveles / d=1 / ángulo 0. Protocolo HSV masked: histograma por canal (H=8, S=4, V=4; rangos [0,1] skimage) solo en píxeles Leaf.

Nota: VARI puede dispararse si \(G+R-B \approx 0\); en los baselines se excluyen `vari_*`.

Pipelines de cuadernos (A foto completa / B máscara / C HSV): ver `notebooks/rocole/README.md` y subcarpetas `A-full/`, `B-masked/`, `C-hsv-masked/`. Métricas comparables en `experiments/results/rocole/comparacion/rocole_baselines_test_metrics_extended.csv`.

No se versionan los CSV pesados por defecto (ver `.gitignore`); las excepciones `*.csv` de esta carpeta sí se pueden versionar. Sí este README.
