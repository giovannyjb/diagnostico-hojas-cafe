# featured/rocole

- `index.csv` — `File`, `plant_key`, `link_group`, etiquetas, `split`, `photo_path` (seed `42`)
- `rgb_glcm_features.csv` — inventario **sin máscara** (producción): identidad + ExG/NGRDI/VARI (mean/std) + GLCM contraste/homogeneidad/energía + `error`

Protocolo: foto completa, GLCM 32 niveles, distancia 1, ángulo 0. Comparación con máscara COCO solo en el piloto del cuaderno 02.

Nota: VARI puede dispararse si \(G+R-B \approx 0\); revisar outliers antes de modelar (clip o excluir `vari_*` si hace falta).

No se versionan los CSV pesados por defecto (ver `.gitignore`); sí este README.
