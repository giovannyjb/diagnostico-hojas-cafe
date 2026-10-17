# Resúmenes de artículos — Gio (Entrega 1)

PDFs locales: `peerj-cs-3172.pdf` (A8) · `sorte-2019-procs.pdf` (R1) · `applsci-13-04565.pdf` (**A7 de Camilo**, apoyo).  
Asignación Gio: **A8 + R1** — ambos leídos (2026-10-17).

Plantilla de la matriz: paráfrasis = información útil · cita textual = fragmento breve con ubicación.

---

## A8 — Principal (asignado a Gio)

**Referencia IEEE (plantilla):**  
N. Baht, E. Dominguez, and S. Aljumaili, “Detection of coffee leaf disease and identification using deep learning,” *PeerJ Computer Science*, vol. 11, art. no. e3172, 2025, doi: 10.7717/peerj-cs.3172.

### Para qué nos sirve
Comparar CNN propias, transfer learning (VGG16, ResNet50, EfficientNetB0) y **híbridos CNN + SVM / Random Forest** — línea cercana a nuestro plan (características + clasificadores clásicos).

### Respuesta a la pregunta de la matriz
| Pregunta | Hallazgo en el texto |
|----------|----------------------|
| ¿Cuántas fotografías **originales** hay antes del aumento? | **No lo reportan con claridad.** Trabajan con JMuBEN / JMuBEN2 (Arabica; 5 clases: Phoma, Cercospora, Rust, Healthy, Miner). Hablan de un corpus “exceeding 50,000 images” (abstract) y de (58,555) imágenes a 128×128 en un pasaje, pero no separan de forma inequívoca el tamaño **antes** de balanceo/aumento. |
| ¿El aumento ocurre **después** de separar train/test? | **No.** El flujo descrito en Materials and Methods es: preprocesamiento (resize 100×100, balanceo por undersampling a la clase minoritaria, Min-Max, **augmentation**) → **luego** split 80–20. Citan explícitamente: *“The preprocessed dataset was split into training and testing sets using an 80–20 split”* (Materials and Methods), con formas (26,284) train y (6,571) test. |

### Información útil (paráfrasis, lista para la columna G)
- Dataset principal: JMuBEN / JMuBEN2 (Kaggle), 5 clases de hoja de arábica; **no es BRACOL ni RoCoLe**.
- Segunda base: ~1.700 imágenes de Kaggle (“coffee leaf disease”) para una prueba externa; reportan ~98 % de exactitud con CNN1. Para igualar 5 clases, **inyectaron Cercospora del conjunto de entrenamiento** → la “external test” no es del todo independiente.
- Modelos: CNN1, CNN2; transfer VGG16, ResNet50, EfficientNetB0; híbridos quitando Softmax y pasando características a SVM o RF (seis híbridos).
- También mencionan LBP / ECS-LBP como extracción de textura en el pipeline (etapa 1).
- Exactitudes reportadas en test: rango ~93–99 %; **CNN1 ~99 %** (mejor del paper).
- Despliegan interfaz (upload / cámara) en notebook/cloud; el modelo “ligero” lo presentan como apto para dispositivos de bajo costo.

### Cita textual breve (columna I)
> “The preprocessed dataset was split into training and testing sets using an 80–20 split.”  
> (Materials and Methods; formas train 26,284 · test 6,571).

### Cómo usarlo en la escritura (y cómo **no** usarlo)
- **Sí:** como evidencia de que CNN + SVM/RF es una línea publicada; como contraste metodológico (nosotros: BRACOL/RoCoLe, fondos y captura reales, split cuidadoso).
- **No** citar el 99 % como benchmark comparable a nuestro problema **sin** advertir: dataset distinto, aumento **antes** del split (riesgo de fuga por versiones aumentadas de la misma hoja en train y test), y test “externo” contaminado al rellenar la quinta clase desde train.
- En el estado del arte: un párrafo de “resultados altos en bancos controlados/Kaggle” + un párrafo de “protocolos frágiles que debemos evitar”.

### Estado sugerido en la matriz
**Leído** (2026-10-17) · PDF en `docs/peerj-cs-3172.pdf`.

---

## A7 — Principal (asignado a **Camilo**; PDF que Gio abrió hoy)

**Referencia IEEE:**  
A. F. Chavarro, D. Renza, and D. M. Ballesteros, “Influence of hyperparameters in deep learning models for coffee rust detection,” *Applied Sciences*, vol. 13, no. 7, art. no. 4565, 2023, doi: 10.3390/app13074565.

### Para qué nos sirve (aunque no sea tu fila)
Justifica un **diseño de experimentos pequeño**: con poco tiempo, conviene comparar pocos *backbones* y fijar el resto.

### Información útil (paráfrasis)
- Tarea: clasificación de **roya** en 3 clases (Healthy / Rust / Other), mezclando RoCoLe, BRACOL, Digipathos, D&P y Licole (fondos e iluminación diversos). Totales aproximados (Table 2): Healthy 1.686 · Rust 1.723 · Other 1.928 (después de limpieza: descartar distractores, hojas con varias enfermedades, etc.).
- Entrenaron **>800** configuraciones (864) variando: 8 backbones × profundidad transferida × neuronas FC × 3 optimizadores × 3 learning rates.
- Ranking de impacto (F1 / accuracy):
  1. **Backbone** — diferencias de hasta ~**70 %** (DenseNet201 mejor; EfficientNetB5 y ResNet50 peores en su set).
  2. **Optimizador** — hasta ~**20 %** (SGD suele ser el peor; Nadam / RMSprop mejores).
  3. **Learning rate** — impacto moderado (~10–20 % según backbone).
  4–5. Neuronas FC y profundidad transferida — impacto bajo (~2–7 %).
- Mejor modelo reportado (Table 5): **DenseNet201** + Nadam + LR 1×10⁻⁵ + 256 neuronas → Acc / F1 ≈ **94,8 % / 94,7 %** en test.
- Mejoraron F1 de **18,4 % a 92,71 %** solo eligiendo hiperparámetros, **sin** retocar el conjunto de imágenes.
- MobileNetV2 queda competitivo y mucho más liviano (útil si algún día hay app): ~16,9 MB / ~2 M parámetros vs DenseNet más pesado.

### Cita textual breve
> “The type of backbone is the hyperparameter with the greatest impact.” (Abstract).

### Cómo usarlo en la escritura
- En metodología / plan experimental: “priorizamos comparar X backbones (o extractores) y mantenemos fijos optimizador/LR”.
- En limitaciones del estado del arte: muchos papers fijan hiperparámetros sin justificarlos; este paper da evidencia de por qué eso importa.
- Coordinar con Camilo para no duplicar la ficha en la matriz (él es el responsable de A7).

### Estado
PDF local `docs/applsci-13-04565.pdf` · lectura de apoyo 2026-10-17.

---

## R1 — Reserva: textura (asignado a Gio) ✅

**Referencia IEEE:**  
L. X. B. Sorte, C. T. Ferraz, F. Fambrini, R. dos Reis Goulart, and J. H. Saito, “Coffee leaf disease recognition based on deep learning and texture attributes,” *Procedia Computer Science*, vol. 159, pp. 135–144, 2019, doi: 10.1016/j.procs.2019.09.168.

### Para qué nos sirve
Contraste directo entre **atributos de textura** (estadísticos + LBP) y una **CNN** sobre las mismas hojas — alineado con nuestro plan de características clásicas vs. extractores profundos.

### Respuesta a la pregunta de la matriz
| Pregunta | Hallazgo en el texto |
|----------|----------------------|
| ¿Qué descriptores? | (1) **Atributos estadísticos** de textura (vector de 4 elementos). (2) **LBP** — variantes uniform / non-uniform / rotation-invariant (vectores de 10 o 36 elementos). |
| ¿Sobre cuántas imágenes originales? | Banco propio (finca del Instituto Federal do Sul de Minas, Muzambinho-MG). Recortes 128×128: **750 subimágenes por clase** (Cercospora, Rust, Healthy). Antes del aumento: **~500 imágenes por clase**. |
| ¿Protocolo de evaluación? | Siempre **50 muestras de test por clase**. En textura (TBDR): train 250 o 550 por clase → red feedforward (`patternnet`). En CNN (DLDR): AlexNet modificada; train 550/clase o hasta 700 en enfermas; validación en runtime con 10 % del input; 20 épocas, Adam lr=0,001. Métricas: **Kappa** y **sensibilidad** (no reportan accuracy sola como métrica principal). |

### Información útil (paráfrasis)
- Motivación: roya y cercospora son “sin forma fija” → textura tiene sentido; objetivo = sistema experto para diagnóstico temprano.
- Dos enfoques: **TBDR** (textura → red feedforward) vs **DLDR** (CNN sobre píxeles RGB o gris, sin textura manual).
- Mejor TBDR: LBP rotation-invariant non-uniform (y la fusión LBP+estadísticos empatan) → **Kappa 0,900 · sensibilidad 0,933** (15 neuronas ocultas).
- Mejor DLDR: Exp. 11 (RGB, más muestras en clases enfermas) → **Kappa 0,970 · sensibilidad 0,980**.
- Resultado sorprendente para los autores: la CNN **supera** a la textura en este set (pocas clases + suficientes muestras).
- En TBDR, subir de 250 a 550 train **empeoró** (sospechan overfitting); en DLDR, subir muestras mejoró el desempeño.
- **No es BRACOL ni RoCoLe**; banco local brasileño. No usan SVM/RF: clasificador de textura = MLP.

### Cita textual breve
> “Surprisingly, this second approach [CNN] showed better results than the texture extraction method.” (Abstract).  
> Mejor Kappa reportado: 0.970; sensibilidad: 0.980 (Abstract / Exp. 11).

### Cómo usarlo en la escritura
- **Sí:** justificar por qué probar LBP/estadísticos *y* un extractor profundo; citar que en 3 clases (sana / roya / cercospora) la CNN ganó, pero la textura ya llega a Kappa 0,90 (línea viable con pocos recursos).
- **Cuidado:** N de test fijo en 50/clase es pequeño; banco distinto al nuestro; no generalizar el “CNN siempre gana” a BRACOL/RoCoLe sin repetir el experimento.
- Encaja con nuestro medio “caracterizar la complejidad de las alteraciones visibles”.

### Estado sugerido en la matriz
**Leído** (2026-10-17) · PDF en `docs/sorte-2019-procs.pdf`.

---

## Frases listas (borrador) para el texto de la Entrega 1

**Sobre A8 (cuidado con el 99 %):**  
Baht, Dominguez y Aljumaili (2025) comparan CNN propias, redes preentrenadas e híbridos CNN+SVM/RF sobre bancos JMuBEN/JMuBEN2 y reportan exactitudes cercanas al 99 % con su CNN1. Sin embargo, el aumento y el balanceo se aplican al conjunto completo **antes** del particionado 80–20 (26.284 / 6.571), por lo que esas cifras no deben tomarse como techo comparable a un protocolo con separación estricta train/test sobre BRACOL o RoCoLe.

**Sobre R1 (textura vs CNN):**  
Sorte et al. (2019) contrastan atributos de textura (estadísticos y LBP) alimentando una red feedforward frente a una CNN tipo AlexNet sobre recortes de hoja sana, roya y cercospora. La CNN alcanza Kappa 0,970 y sensibilidad 0,980, por encima del mejor resultado con LBP (Kappa 0,900). Eso respalda evaluar ambas líneas en nuestro proyecto, sin asumir que la textura manual sea suficiente ni que la CNN sea automáticamente superior en BRACOL/RoCoLe.

**Sobre A7 (diseño experimental):**  
Chavarro, Renza y Ballesteros (2023), al evaluar más de ochocientas configuraciones para detección de roya con imágenes de varios bancos (incluido BRACOL y RoCoLe), encuentran que el tipo de *backbone* es el hiperparámetro de mayor impacto —con diferencias de hasta 70 % en F1— seguido del optimizador. Eso justifica, en nuestro plan, comparar pocos extractores o arquitecturas y fijar el resto de hiperparámetros.
