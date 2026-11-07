# Notebooks

Separados **por dataset**. Estilo compartido: `00-prueba-estilo-cuaderno.ipynb` en la raíz de esta carpeta.

| Carpeta | Dataset | Entrada | Salida |
|---------|---------|---------|--------|
| [`rocole/`](rocole/) | RoCoLe (robusta) | `data/raw/RoCoLe/` | `data/curated/rocole/`, `data/featured/rocole/` |
| [`bracol/`](bracol/) | BRACOL (arábica) | `data/raw/BRACOL/` | `data/curated/bracol/`, `data/featured/bracol/` |

## RoCoLe (en curso)

| Notebook | Qué responde | Quién |
|----------|----------------|-------|
| [`rocole/01-eda-rocole.ipynb`](rocole/01-eda-rocole.ipynb) | EDA, limpieza, curación, split | Equipo |
| [`rocole/02-caracteristicas-rocole.ipynb`](rocole/02-caracteristicas-rocole.ipynb) | GLCM + índices RGB | Víctor, Gio |
| [`rocole/03-modelo-glcm-rf.ipynb`](rocole/03-modelo-glcm-rf.ipynb) | Random Forest con GLCM | Víctor |
| [`rocole/04-modelo-rgb-logistica.ipynb`](rocole/04-modelo-rgb-logistica.ipynb) | Logística con índices RGB | Gio |

## BRACOL (equipo)

Empezar por [`bracol/README.md`](bracol/README.md). El primer cuaderno previsto es `bracol/01-eda-bracol.ipynb`.

## Convenciones

- Desde `notebooks/<dataset>/`: rutas `../../data/...` y `../../experiments/...`.
- Importar código desde `src/` (añadir la raíz del repo al `sys.path`).
- Figuras en `experiments/results/`.
- Semilla `42`. Una celda, una tarea. Markdown corto.
- No mezclar BRACOL y RoCoLe en el mismo acierto; la generalización entre variedades es otro paso.
