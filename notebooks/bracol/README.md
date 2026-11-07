# Notebooks — BRACOL

Cuadernos del conjunto **BRACOL** (arábica). Datos: `data/raw/BRACOL/` → `data/curated/bracol/` → `data/featured/bracol/`.

| Notebook | Qué hace |
|----------|----------|
| *(pendiente)* `01-eda-bracol.ipynb` | EDA y curación (equipo BRACOL) |

## Para el equipo BRACOL

1. Descargar BRACOL a `data/raw/BRACOL/` según [`docs/datos.md`](../../docs/datos.md).
2. Crear aquí `01-eda-bracol.ipynb` (mismo estilo que RoCoLe: markdown corto, una tarea por celda).
3. Salidas de limpieza → `data/curated/bracol/` (`classes.csv`, `photos/`, `withdrawals/`).
4. Índice con split → `data/featured/bracol/index.csv` (semilla `42`).
5. No mezclar filas ni métricas con RoCoLe en el mismo acierto; comparación entre variedades es otro paso explícito.

Rutas desde este folder: `../../data/...`.
