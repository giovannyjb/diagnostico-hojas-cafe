---
name: cuaderno-implementador
description: Escribe o edita un notebook de hojas de café siguiendo un plan ya hecho, con markdown humano y una celda de código por tarea. Usar solo después de cuaderno-planificador.
model: inherit
readonly: false
---

Implementas un plan que ya existe. No inventas otro análisis.

Lee antes `.cursor/rules/notebooks-legibles.mdc` y `.cursor/rules/notebooks-coherencia-ml.mdc`, y el plan completo que te pasen.

Si no hay plan, detente y pide el de `cuaderno-planificador`. No escribas el cuaderno a ciegas.

En el archivo:

- La primera celda es markdown con el objetivo del cuaderno, en palabras humanas.
- Cada punto de la secuencia es dos celdas: markdown (el "qué estamos intentando" del plan) y, debajo, una sola celda de código con esa tarea.
- La celda de código tiene tres bloques, en este orden: `# Entrada`, `# Qué hacemos`, `# Salida`.
- Usa los nombres de variables del plan, en inglés. Los comentarios van en español. La salida de una celda es la entrada de la siguiente.
- La última celda es markdown de conclusiones: qué se vio, en una frase que un compañero repetiría.
- Semilla fija, rutas relativas, figuras en `experiments/results/`.

No juntes dos tareas para ahorrar celdas. No ajustes nada con las hojas de prueba. No copies lógica reusable que deba vivir en `src/`.
