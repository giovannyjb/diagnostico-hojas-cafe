# Datos

Las **fotos no se versionan** (pesan más de 1 GB y ya se ven dentro de los cuadernos). Cada integrante las descarga a `data/raw/` siguiendo esta guía. En git sí van las tablas de las tres capas, para leer el flujo sin abrir las imágenes:

- `raw/` — CSV y anotaciones de origen. Fuera del repo: fotos y `RoCoLe-voc.tar.gz`.
- `curated/` — CSV depurados y registros de limpieza. La carpeta `photos/` queda en local.
- `featured/` — índice con `split` y matrices de características.

## Flujo

```
raw  →  curated  →  featured
```

- `raw/` — tal cual viene de Mendeley. No se edita.
- `curated/` — por dataset: tablas depuradas, fotos conservadas y registros de limpieza.
- `featured/` — por dataset: índice con `split` fijo y, después, matrices de características.

RoCoLe y BRACOL se procesan **en paralelo y por separado** (carpetas hermanas). No se mezclan en el mismo acierto; entrenar en una variedad y probar en la otra es otro paso, explícito.

## Datasets

### BRACOL — Brazilian Arabica Coffee Leaf
- Fuente: https://data.mendeley.com/datasets/yy2k5y8mxg/1
- 1.747 imágenes de hojas de café **arábica**: sanas o con **minador**, **roya**, **phoma**, **cercospora**; incluye etiquetas de **severidad**.
- Licencia: la indicada en la ficha de Mendeley Data (verificar y citar).
- Trabajo del equipo: `notebooks/bracol/` → `data/curated/bracol/` → `data/featured/bracol/`.

### RoCoLe — Robusta Coffee Leaf
- Fuente: https://data.mendeley.com/datasets/c5yvn32dzg/2 · artículo: https://pmc.ncbi.nlm.nih.gov/articles/PMC6727496/
- 1.560 imágenes de hojas de café **robusta**: sanas o con **roya** / ácaro, con anotaciones de severidad.
- Licencia: la indicada en la ficha de Mendeley Data (verificar y citar).
- Trabajo del equipo: `notebooks/rocole/` → `data/curated/rocole/` → `data/featured/rocole/`.

## Estructura esperada

```
data/
├── raw/
│   ├── BRACOL/                 # descarga Mendeley (árabes)
│   └── RoCoLe/                 # descarga Mendeley (robusta)
├── curated/
│   ├── bracol/                 # salidas EDA BRACOL (equipo BRACOL)
│   │   ├── classes.csv
│   │   ├── photos/
│   │   └── withdrawals/
│   └── rocole/                 # salidas EDA RoCoLe (ya en curso)
│       ├── classes.csv
│       ├── photos/
│       └── withdrawals/
└── featured/
    ├── bracol/
    │   └── index.csv           # split BRACOL (cuando toque)
    └── rocole/
        └── index.csv           # File, plant_key, link_group, etiquetas, split, photo_path
```

```
notebooks/
├── bracol/                           # cuadernos BRACOL
│   └── README.md
└── rocole/                           # cuadernos RoCoLe
    ├── README.md
    ├── 01-eda-rocole.ipynb           # EDA, curación y split
    ├── A-full/                       # foto completa
    ├── B-masked/                     # máscara COCO
    └── C-hsv-masked/                 # HSV sobre máscara
```

### Qué quedó en la curación de RoCoLe (EDA parte 1)

- Partimos de 1.560 fotos → base curada 1.481 con `plant_key` / `leaf_face`.
- Retiros: 40 duplicados misma etiqueta; 15 conflictos de severidad (Astra); 1 par sana/ácaro; 11 pares ácaro/roya (hold-out).
- Split en `data/featured/rocole/index.csv` por `link_group` (planta + duplicados), semilla `42`.

Documentar aquí, al descargar BRACOL, **cómo vienen las etiquetas** y cualquier limpieza hecha.

## Cuidados

- Antes de dividir train/test, buscar **duplicados o la misma hoja/planta** para que no caigan en ambos lados.
- Semilla fija `42`. Índice con `split` en `data/featured/<dataset>/index.csv`.
- Registrar la **distribución de clases** por dataset (desbalance) en el EDA.
- No subir imágenes del dataset a repos públicos fuera de lo que permita la licencia.
