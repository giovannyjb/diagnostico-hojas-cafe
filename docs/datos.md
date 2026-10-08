# Datos

Los datasets **no se versionan** en git (pesan cientos de MB). Cada integrante los descarga a `data/raw/` siguiendo esta guía; `data/processed/` lo generan los scripts/notebooks.

## Datasets

### BRACOL — Brazilian Arabica Coffee Leaf
- Fuente: https://data.mendeley.com/datasets/yy2k5y8mxg/1
- 1.747 imágenes de hojas de café **arábica**: sanas o con **minador**, **roya**, **phoma**, **cercospora**; incluye etiquetas de **severidad**.
- Licencia: la indicada en la ficha de Mendeley Data (verificar y citar).

### RoCoLe — Robusta Coffee Leaf
- Fuente: https://data.mendeley.com/datasets/c5yvn32dzg/2 · artículo: https://pmc.ncbi.nlm.nih.gov/articles/PMC6727496/
- 1.560 imágenes de hojas de café **robusta**: sanas o con **roya**, con anotaciones de severidad.
- Licencia: la indicada en la ficha de Mendeley Data (verificar y citar).

## Estructura esperada

```
data/
├── raw/
│   ├── bracol/        # contenido descomprimido tal cual viene de Mendeley
│   └── rocole/
└── processed/
    ├── index.csv      # una fila por imagen: ruta, dataset, variedad, clase, severidad, split
    └── ...
```

Documentar aquí, al descargar, **cómo vienen las etiquetas** (carpetas, CSV, XML…) y cualquier limpieza hecha.

## Cuidados

- Antes de dividir train/test, buscar **imágenes duplicadas o de la misma hoja** para que no caigan en ambos lados.
- Guardar el `index.csv` con el `split` fijo (semilla) para que todos los experimentos sean comparables.
- Registrar la **distribución de clases** por dataset (desbalance) en el EDA.
- No subir imágenes del dataset a repos públicos fuera de lo que permita la licencia.
