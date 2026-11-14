# Notebooks

Separados **por dataset**. Estilo compartido: `00-prueba-estilo-cuaderno.ipynb` en la raíz de esta carpeta.

| Carpeta | Dataset | Entrada | Salida |
|---------|---------|---------|--------|
| [`rocole/`](rocole/) | RoCoLe (robusta) | `data/raw/RoCoLe/` | `data/curated/rocole/`, `data/featured/rocole/` |
| [`bracol/`](bracol/) | BRACOL (arábica) | `data/raw/BRACOL/` | `data/curated/bracol/`, `data/featured/bracol/` |

## RoCoLe (pipelines en rama `experiment/rocole-mask-hsv-pipelines`)

Detalle y mapa canónico vs experimento: [`rocole/README.md`](rocole/README.md).

| Pipeline | Cadena | Idea |
|----------|--------|------|
| A producción | `01` → `02` → `03` → `04` | Foto completa, 7 features sin VARI |
| B máscara | `02-masked` → `03-masked` → `04-masked` → `05` | Mismas hojas, medición COCO Leaf |
| C HSV (dev) | `02-hsv-masked` → `03-hsv-masked` → `04-hsv-masked` | 7 + histograma HSV pequeño; pausa antes de más familias |

Evaluación común en todos los baselines: train / val elige / test una vez; mayoría + logística + RF; seed `42`.

## BRACOL (equipo)

Empezar por [`bracol/README.md`](bracol/README.md). El primer cuaderno previsto es `bracol/01-eda-bracol.ipynb`.

## Convenciones

- Desde `notebooks/rocole/` (p. ej. `01`): rutas `../../data/...` y `../../experiments/...`.
- Desde `notebooks/rocole/A-full|B-masked|C-hsv-masked/`: un nivel más → `../../../data/...` y `../../../experiments/...`.
- Resultados RoCoLe por pipeline: `experiments/results/rocole/{A-full,B-masked,C-hsv-masked,comparacion}/`.
- Importar código desde `src/` (añadir la raíz del repo al `sys.path`).
- Semilla `42`. Una celda, una tarea. Markdown corto.
- No mezclar BRACOL y RoCoLe en el mismo acierto; la generalización entre variedades es otro paso.
