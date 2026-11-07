# data/

Flujo: `raw` → `curated` → `featured`, **por dataset**.

```
data/
├── raw/BRACOL|RoCoLe
├── curated/bracol|rocole
└── featured/bracol|rocole
```

- `raw/` — descarga Mendeley. **No se versiona.**
- `curated/<dataset>/` — etiquetas, fotos y retiros. **No se versiona** (sí los `.gitkeep` / README de carpeta).
- `featured/<dataset>/` — `index.csv` con `split` y features. **No se versiona.**

Detalle: [`docs/datos.md`](../docs/datos.md).
