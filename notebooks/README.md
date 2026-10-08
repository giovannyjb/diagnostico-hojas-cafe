# Notebooks

Numerados por etapa; cada uno empieza con una celda de **objetivo** y termina con **conclusiones**.

| Notebook | Etapa | Qué responde |
|----------|-------|--------------|
| `01-eda-bracol-rocole.ipynb` | 2 | ¿Cuántas imágenes por clase y severidad? ¿Tamaños, fondos, iluminación? ¿Duplicados? |
| `02-caracteristicas-color-textura.ipynb` | 2–3 | ¿Separan las clases los histogramas HSV y la textura? Baseline SVM / RF |
| `03-embeddings-cnn-y-comparacion.ipynb` | 3 | ¿Mejora una CNN preentrenada como extractor? Comparación de modelos con CV |
| `04-clustering-no-supervisado.ipynb` | 3 | ¿Se agrupan las enfermedades sin etiquetas? (K-Means, jerárquico, PCA) |
| `05-generalizacion-entre-variedades.ipynb` | 3 | Entrenar en arábica → probar en robusta (y viceversa) |

Convenciones: importar código desde `src/` (`sys.path.append("..")`), guardar figuras en `experiments/results/`, fijar semillas, no dejar rutas absolutas.
