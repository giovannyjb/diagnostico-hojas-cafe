# Entregas

El curso sugiere una carpeta por entrega. Aquí cada carpeta contiene el **índice de la entrega** (qué se entrega y dónde está en el repo), el **reporte en la plantilla Word del curso** y cualquier archivo exclusivo de esa entrega. El código y los documentos vivos siguen en `src/`, `notebooks/` y `docs/`; el estado exacto revisado queda congelado con un *tag* de git.

| Entrega | Peso | Carpeta | Tag | Fecha (Intu) | Estado |
|---------|-----:|---------|-----|--------------|--------|
| 1 — Reporte primera etapa | 20% | [`entrega-1/`](entrega-1/README.md) | `entrega-1` | … | ⏳ |
| 2 — Reporte segunda etapa | 10% | [`entrega-2/`](entrega-2/README.md) | `entrega-2` | … | ⏳ |
| 3 — Reporte final + sustentación + coevaluación | 70% | [`entrega-3/`](entrega-3/README.md) | `entrega-3` | … | ⏳ |

Al cerrar una entrega:

```bash
git tag -a entrega-1 -m "Entrega 1: reporte primera etapa"
git push origin entrega-1
```

Rúbricas y desglose del 70%: Intu → *Entregables, Rúbricas* (`Porcentajes de Evaluación.pdf`).
