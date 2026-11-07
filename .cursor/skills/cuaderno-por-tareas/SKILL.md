---
name: cuaderno-por-tareas
description: >-
  Guía el trabajo en notebooks de diagnóstico de hojas de café: planifica,
  implementa una tarea por celda, revisa que un humano lo entienda y valida
  coherencia y data leakage. Usar al crear o modificar cuadernos en notebooks/,
  al proponer EDA, histogramas HSV, características, modelos o splits, o cuando
  un agente vaya a escribir código en un .ipynb de este proyecto.
---

# Cuaderno por tareas

Cualquier edición de un `.ipynb` en `notebooks/` cumple `.cursor/rules/notebooks-legibles.mdc` y `.cursor/rules/notebooks-coherencia-ml.mdc`.

Un retoque de una celda ya existente se hace directo, cumpliendo esas reglas.

Una sección nueva o un cuaderno nuevo no se escribe de un tirón. Van cuatro roles, en este orden. Solo el implementador toca el archivo.

## 1. Planificador

Delega en `cuaderno-planificador`. No escribe código.

Devuelve un plan con esta forma:

```markdown
## Objetivo del cuaderno
Una frase humana.

## Secuencia
1. Markdown: qué estamos intentando.
   Tarea: un verbo, una cosa.
   Entrada: nombre de variable que ya existe, o "ninguna".
   Salida: nombre de variable, en inglés, que queda para la celda siguiente.
   No hacer: el paso que sería otra celda, o un leakage concreto.

## Riesgos
- Dónde se podría colar la prueba, un duplicado o un paso saltado.
```

Si el plan mezcla dos tareas en un punto, se parte antes de implementar.

## 2. Implementador

Delega en `cuaderno-implementador` y pásale el plan completo.

Escribe el objetivo arriba, una celda markdown por tarea, una celda de código debajo, y conclusiones al final. Variables en inglés, comentarios en español. No agrega pasos que el plan no tenga.

## 3. Revisor

Delega en `cuaderno-revisor`. No edita.

Pregunta por cada sección: ¿un compañero sabe qué estamos intentando sin correr la celda? Si una celda hace dos cosas o un nombre no se entiende, lo señala con el número de celda.

## 4. Validador

Delega en `cuaderno-validador`. No edita.

Recorre la secuencia. Confirma que no falte un paso, que el tono y la etiqueta sigan en la misma fila, y que nada se ajuste con las hojas de prueba.

## Si algo falla

El revisor o el validador devuelven una lista corta. Esa lista vuelve al implementador. Después se repite solo el rol que falló. Una sola vuelta de corrección.

El revisor no reescribe el cuaderno para "dejarlo bonito". El validador no agrega modelos nuevos.
