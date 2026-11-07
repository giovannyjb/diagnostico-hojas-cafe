# Cuadernos de hojas de café

Normas solo para Codex (Cursor usa `.cursor/rules/`). Aplica al crear o editar cualquier `.ipynb` bajo `notebooks/`.

# Cuadernos legibles

El cuaderno lo lee el equipo. Cada sección se entiende sin ejecutarla.

## Arriba, en palabras humanas

Antes de cada celda de código va una celda markdown. Dice qué estamos intentando, como se lo contarías a un compañero. Sin jerga de implementación.

El cuaderno abre con el objetivo de todo el archivo y cierra con conclusiones.

## Una celda, una tarea

Una celda de código hace una sola cosa: separar la etiqueta de los números, armar el histograma del matiz, apartar las hojas de prueba. Si la frase necesita "y", son dos celdas.

## Nombres que se leen

Variables en inglés, con el sustantivo de lo que son: `leaves`, `disease_name`, `hue`, `train_leaves`, `test_leaves`. Nada de `df2`, `tmp`, `X`, `data_final`.

Los comentarios van en español. Las columnas que ya trae el dato (`clase`, `severidad`) se dejan como vienen.

Dentro de la celda, tres bloques y en ese orden:

```python
# Entrada
leaves = leaves.copy()

# Qué hacemos
leaf_color = leaves[["hue", "saturation", "brightness"]]
disease_name = leaves["disease"]

# Salida
leaf_color.head()
```

La salida de una celda es la entrada de la siguiente, con el mismo nombre.

## Ejemplo

Markdown: "Queremos ver si el tono cambia entre una hoja sana y una con roya. Miramos solo el matiz: la parte del color que dice si tira a verde o a amarillo."

Código: una figura, histograma de `hue` pintado por `disease`. En esa celda no hay modelo.

# Coherencia del cuaderno

La secuencia se lee de arriba abajo. No se salta un paso ni se calcula nada de prueba antes de apartarla.

## Orden

1. Objetivo del archivo.
2. De dónde salen las hojas (y, con datos reales, cuántas hay por clase).
3. Qué columna es etiqueta y qué columnas son medidas.
4. Mirar (histogramas, conteos). Mirar no elige el corte ni el modelo.
5. Apartar hojas de prueba, con semilla fija, antes de ajustar nada.
6. Ajustar solo con `train_leaves`.
7. Medir solo con `test_leaves`.
8. Conclusiones en palabras humanas.

Cada fila viaja entera: el tono y la enfermedad no se parten en tablas distintas y luego se reordenan por separado.

## Data leakage

- El corte, el escalado, el encoder y el modelo se ajustan solo con las hojas de aprender.
- No elijas columnas ni umbrales mirando el acierto en las hojas de prueba.
- Con fotos reales, antes del reparto busca duplicados y la misma hoja en los dos lados. La limpieza queda en `data/curated/<dataset>/`; el reparto, en `data/featured/<dataset>/index.csv` (`docs/datos.md`).
- No uses la severidad para predecir la enfermedad: es consecuencia de la etiqueta, no una medida independiente.
- Arábica y robusta no se mezclan en el mismo acierto. Entrenar en una y probar en la otra es otro paso, explícito.
- Aumentos de imagen solo en las hojas de aprender.

## Proyecto

- Semilla fija, reutilizada (`seed = 42`). El comentario que la explica va en español.
- Rutas relativas al repo. Nada de `C:\` ni `/Users/`.
- Figuras en `experiments/results/`.
- Lógica que se va a reutilizar vive en `src/`. El cuaderno la llama; no la copia.
