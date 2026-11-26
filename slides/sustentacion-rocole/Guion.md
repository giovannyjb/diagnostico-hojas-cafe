# Clasificación de alteraciones visibles en hojas de café

Guion de producción para el video final · 12 diapositivas · duración propuesta de 9 minutos, incluidas las pausas para leer figuras. El reparto es para la exposición. Cada integrante presenta tres diapositivas.

| Tiempo | Voz propuesta | Diapositivas | Pregunta que resuelve |
|---|---|---|---|
| 0:00–2:10 | Gio | 1–3 | ¿Qué se quiere predecir y con qué datos? |
| 2:10–4:30 | Víctor | 4–6 | ¿Cómo evitamos la fuga y qué medimos en cada fotografía? |
| 4:30–6:45 | Camilo | 7–9 | ¿Qué cambió el desempeño y cómo lo validamos? |
| 6:45–9:00 | Dora | 10–12 | ¿Qué modelo funcionó mejor y dónde se equivoca? |

## 01 · Clasificación de alteraciones visibles en hojas de café

**En pantalla**

RoCoLe · Clasificación binaria a partir de fotografías  
Entrada: fotografía de una hoja de café robusta. Salida: sana o afectada.

**Voz · Gio · 0:00–0:30**

“Cuando un caficultor ve un cambio en una hoja, una primera pregunta es si hay una alteración visible que amerite revisión. Tomamos esa pregunta como una tarea de clasificación binaria. Trabajamos con fotografías de RoCoLe y comparamos tres maneras de representar la misma hoja. Al final vamos a mostrar qué modelo distinguió mejor las dos clases y qué tipo de afectación se le escapó con mayor frecuencia.”

**Visual.** Dos fotografías del inventario, lado a lado, rotuladas con la etiqueta de referencia. Usar `C1P1H1.jpg` y `C1P1H2.jpg`. Mantener los colores originales.

## 02 · RoCoLe reúne 1.560 fotografías con etiquetas completas

**En pantalla**

791 sanas · 769 afectadas  
La clase afectada reúne ácaro rojo y cuatro niveles de roya.  
Una observación corresponde a una fotografía. Una hoja puede aparecer por ambas caras.

**Voz · Gio · 0:30–1:10**

“Comprobamos que los 1.560 archivos abrían y tenían nombre y etiquetas. Las dos clases estaban casi equilibradas, pero la composición de la clase afectada era desigual. Antes de depurar había 344 fotografías con roya nivel 1 y solo 30 con nivel 4. Conservamos las etiquetas originales para revisar los errores más adelante. Concentramos el estudio en RoCoLe porque BRACOL cambia la especie de café, las condiciones de captura y la anotación.”

**Visual.** Dos barras con conteos directos. En la segunda, mostrar al hacer una pausa el desglose original: ácaro 167, roya 1: 344, roya 2: 166, roya 3: 62, roya 4: 30. Pie: “Inventario original, antes de depurar”.

## 03 · La revisión de 67 pares duplicados dejó 1.481 fotografías

**En pantalla**

| Situación encontrada | Pares | Decisión | Fotos retiradas |
|---|---:|---|---:|
| Etiquetas concordantes | 40 | Conservar una copia | 40 |
| Diferente severidad de roya | 15 | Revisar y conservar una copia | 15 |
| Ácaro frente a roya | 11 | Apartar ambas copias | 22 |
| Sana frente a ácaro | 1 | Apartar ambas copias | 2 |

1.560 − 79 = **1.481** · 758 sanas y 723 afectadas

**Voz · Gio · 1:10–2:10**

“Los nombres eran únicos, pero el contenido se repetía. Comparamos la huella digital de los archivos y encontramos 67 pares idénticos con nombres diferentes. En 40 bastaba con conservar una copia. En 15, ambas etiquetas indicaban roya y discrepaban en severidad. Revisamos el mosaico con apoyo de IA generativa y registramos la decisión. La etiqueta binaria seguía siendo afectada. En los 12 pares restantes había desacuerdo sobre el tipo de alteración o sobre el propio estado sano. Apartamos ambas copias. Eso explica por qué 67 pares dieron lugar a 79 retiros. La siguiente precaución fue separar las plantas antes de entrenar.”

**Visual.** Primero mostrar dos miniaturas pequeñas del par real `C2P1H1.jpg` y `C3P2H2.jpg` con los nombres debajo. Después sustituirlas por la tabla. Fuente: cuaderno 01. La revisión asistida de severidad debe presentarse como decisión documentada del equipo, sin atribuirle validación independiente de un especialista.

## 04 · La partición mantuvo juntas las fotografías relacionadas

**En pantalla**

357 grupos de planta · 0 grupos compartidos entre particiones

| Partición | Fotografías | Sanas | Afectadas |
|---|---:|---:|---:|
| Entrenamiento | 1.037 | 530 | 507 |
| Validación | 218 | 113 | 105 |
| Prueba | 226 | 115 | 111 |

**Voz · Víctor · 2:10–2:55**

“En el mosaico C1P1 pueden ver las dos caras de cada una de dos hojas. Si repartimos fotos al azar, el modelo podría entrenar con una cara y evaluarse con la otra. Agrupamos por planta y unimos también los identificadores de planta conectados por duplicados exactos. A cada conjunto conectado lo llamamos link_group. Para los experimentos iniciales distribuimos esos grupos en proporciones cercanas a 70, 15 y 15, con semilla 42 y estratificación por la clase predominante del grupo. Verificamos que ningún grupo apareciera en dos particiones.”

**Visual.** `rocole_plant_c1p1_mosaic.png` y la tabla en dos tiempos. Conservar legibles los nombres E1/H1 y E2/H2. Fuente: cuaderno 01 e índice de particiones.

## 05 · Experimento A. Color y textura en la fotografía completa

**En pantalla**

**Color · 4 variables.** Media y desviación estándar de ExG y NGRDI.  
**Textura · 3 variables.** Contraste, homogeneidad y energía de la GLCM.  
**Selección.** Se retiró VARI por valores extremos.

**Voz · Víctor · 2:55–3:45**

“ExG resume cuánto predomina el verde frente al rojo y al azul. NGRDI compara verde y rojo. La media describe la tendencia de la imagen y la desviación estándar cuánto varía entre píxeles. Para textura pasamos a 32 niveles de gris y contamos qué intensidades aparecen juntas en píxeles vecinos, a un píxel de distancia en horizontal. De ahí salen el contraste, la similitud entre vecinos y la concentración de combinaciones. VARI se descartó porque su denominador podía acercarse a cero. En entrenamiento, las distribuciones de sanas y afectadas se solapaban. Eso motivó comprobar cuánto influía el fondo.”

**Visual.** Usar `rocole_sample_exg_map.png`. Después, una sola vista legible de `rocole-featured-exg-by-label-boxplots.png` para mostrar el solape. Rotular “Entrenamiento”. El mapa representa exceso de verde.

## 06 · Experimento B. La máscara delimita la hoja

**En pantalla**

Mismas 7 variables y misma partición que en A.  
Color calculado en los píxeles de la hoja.  
Textura calculada en el recorte que contiene la hoja.

**Voz · Víctor · 3:45–4:30**

“En esta fotografía, la hoja ocupa aproximadamente el 19 % del encuadre. El promedio de color de la foto completa incluye mucho suelo y vegetación de fondo. Usamos el contorno oficial de RoCoLe para medir el color dentro de la hoja. Para la textura recortamos el rectángulo que contiene la hoja y pusimos en cero los píxeles exteriores. Por eso el borde y las zonas en cero todavía pueden influir en la GLCM. La máscara delimita la hoja completa y el conjunto no aporta contornos individuales de lesiones. Con la hoja delimitada probamos otra forma de describir su color.”

**Visual.** `rocole_sample_leaf_mask_overlay.png`, ejemplo C1P1H1. Resaltar el contorno sin cambiar el color de la hoja. El 19 % corresponde a esta fotografía.

## 07 · Experimento C. Los histogramas HSV describen la distribución del color

**En pantalla**

Matiz: 8 rangos · Saturación: 4 rangos · Brillo: 4 rangos  
16 proporciones de color dentro de la hoja + 7 variables previas = **23 características**

**Voz · Camilo · 4:30–5:10**

“Una hoja verde con pequeñas zonas amarillas puede tener una media parecida a otra más uniforme. El histograma conserva algo que esa media pierde: qué proporción de los píxeles cae en cada rango. El matiz representa el tono, la saturación indica qué tan intenso es y el brillo indica qué tan claro u oscuro aparece. Contamos los píxeles de la hoja por separado para cada canal. Por eso sumamos ocho, cuatro y cuatro. Las proporciones de cada canal suman uno. Conservamos las siete medidas de B para poder evaluar qué aportaban las 16 adicionales.”

**Visual.** Usar la figura de salida `rocole-hsv-masked-representative-by-label-boxplots.png` como apoyo o en respaldo. Para el video principal, animar tres filas de 8/4/4 casillas, sin alturas inventadas. Si se representan frecuencias de una hoja, leer sus 16 proporciones reales de la tabla de características de C.

## 08 · En la misma prueba, Random Forest pasó de 0,57 a 0,74

**En pantalla**

| F1 macro en 226 imágenes | A · Foto | B · Máscara | C · Máscara + HSV |
|---|---:|---:|---:|
| Regresión logística | 0,56 | 0,61 | 0,68 |
| Random Forest | 0,57 | 0,68 | 0,74 |

Referencia mayoritaria: **0,34**. Comparación exploratoria.

**Voz · Camilo · 5:10–6:00**

“Elegimos F1 macro porque calcula el F1 de cada clase, combinando precisión y sensibilidad, y luego da el mismo peso a ambas. Las dos familias de modelos mejoraron al pasar de A a B y de B a C. En Random Forest el mayor cambio se observó al introducir la máscara. Aun con HSV, 35 de las 111 imágenes afectadas de prueba se clasificaron como sanas. Como consultamos esa prueba durante el desarrollo, tomamos estos resultados como exploratorios. Para saber cuánto variaba el resultado entre grupos de plantas, pasamos a otra evaluación.”

**Visual.** Dibujar dos líneas con etiquetas numéricas a partir de los CSV individuales de A, B y C incluidos en `datos/`. Mostrar la referencia 0,34 en gris. Mantener D fuera de este gráfico. Matriz original de C disponible en `figuras/rocole_baseline_hsv_masked_rf_confusion.png`.

## 09 · Experimento D. Validación cruzada anidada por planta

**En pantalla**

23 características fijas · 357 grupos · 1.481 fotografías  
**5 pliegues externos** para evaluar · **3 internos** para seleccionar hiperparámetros  
Cada fotografía recibió una predicción fuera de su pliegue de entrenamiento.

**Voz · Camilo · 6:00–6:45**

“Fijamos la representación de C y dividimos los grupos en cinco partes. En cada vuelta, una parte quedó fuera para evaluar. Con las cuatro partes restantes hicimos una validación interna de tres pliegues para escoger los hiperparámetros según F1 macro. Después entrenamos con la configuración elegida y predijimos el pliegue externo. Repetimos hasta que cada fotografía tuvo una predicción obtenida por un modelo que no había entrenado con su grupo. D usa las 1.481 imágenes y responde otra pregunta: cómo se comportan tres modelos con esa representación cuando cambia el grupo evaluado.”

**Visual.** Diagrama nuevo de cinco bloques. Ampliar cuatro para mostrar la división interna en tres. Diferenciar con rótulos “ajuste” y “evaluación”. Esquema conceptual, sin representar tamaños de pliegue iguales como conteos exactos.

## 10 · Random Forest obtuvo el mayor F1 macro medio

**En pantalla**

| Modelo | F1 macro medio | IC aproximado del 95 % |
|---|---:|---:|
| Regresión logística | 0,741 | 0,725–0,757 |
| SVM | 0,767 | 0,719–0,816 |
| Random Forest | **0,796** | **0,778–0,814** |

**Voz · Dora · 6:45–7:25**

“La regresión logística nos dio una referencia lineal. Con SVM comparamos una frontera lineal y otra curva. Con Random Forest evaluamos un conjunto de árboles que permite combinar relaciones entre características. Random Forest obtuvo el promedio más alto en los cinco pliegues, seguido por SVM. Los intervalos resumen la variación entre cinco resultados externos y son aproximados, porque los conjuntos de entrenamiento se solapan. Elegimos el bosque por su mayor media observada. Para entender lo que significa ese promedio, revisamos sus predicciones una por una.”

**Visual.** Gráfico de puntos e intervalos a partir de `rocole_d05_cv_metrics.csv`, con un solo eje y valores directos. Identificar el resultado como F1 macro por pliegue. Evitar asteriscos de significancia.

## 11 · La roya nivel 1 concentró 109 de los 149 falsos negativos

**En pantalla**

| Etiqueta de referencia | Detectadas como afectadas | Sensibilidad |
|---|---:|---:|
| Ácaro rojo | 141 / 155 | 91,0 % |
| Roya nivel 1 | 224 / 333 | **67,3 %** |
| Roya nivel 2 | 132 / 157 | 84,1 % |
| Roya nivel 3 | 53 / 54 | 98,1 % |
| Roya nivel 4 | 24 / 24 | 100,0 % |

**Voz · Dora · 7:25–8:20**

“Sensibilidad significa cuántas imágenes realmente afectadas logramos detectar. Si miramos solo la roya nivel 1, detectamos 224 de 333. Las 109 restantes representan el 73,2 % de todos los falsos negativos. Estas dos fotos del mismo pliegue tienen la misma etiqueta original: una se detectó y la otra pasó como sana. Una explicación posible es que las alteraciones leves ocupen poca superficie y pesen poco en los resúmenes globales. Las anotaciones disponibles no permiten comprobar esa causa. En el otro extremo, el 100 % de nivel 4 corresponde a 24 imágenes. El denominador importa.”

**Visual.** Primero tabla o barras horizontales con fracciones. Después mostrar el par real del pliegue 0: `C1P29H2.jpg`, “Detectada como afectada”; `C2P18H1.jpg`, “Clasificada como sana”. Ambas con etiqueta original «roya nivel 1». El árbol de decisión del modelo no localiza la lesión. Evitar flechas que atribuyan la predicción a un píxel.

## 12 · Alcance del modelo y evidencia reproducible

**En pantalla**

**0,796 F1 macro medio** con Random Forest, máscara y 23 características.  
**1.481 predicciones trazables** por archivo, grupo, pliegue y etiqueta.  
**Límite principal:** detección de roya leve y dependencia de máscaras anotadas.

**Voz · Dora · 8:20–9:00**

“El proyecto deja un inventario depurado, un protocolo por grupos de planta y un registro que permite reconstruir cada acierto y cada error. En RoCoLe, la mejor configuración distinguió hojas sanas de afectadas con un F1 macro medio de 0,796. El resultado más importante para interpretar su uso es que cerca de una de cada tres imágenes con roya leve pasó como sana. Para evaluar el mismo flujo con fotografías nuevas habría que obtener la máscara de cada hoja y probarlo con plantas externas. Esa es la frontera entre lo que demostramos en el proyecto y una aplicación en campo.”

**Visual.** Extracto real de las dos filas de predicción de la diapositiva 11. Mostrar archivo, pliegue, referencia y predicción. Cerrar con los cuatro nombres y el título del proyecto. Fuente: cuadernos 05 y 06 del experimento D.

## Respaldo para preguntas del profesor

Estas tres láminas son opcionales para la sustentación. No se suman al tiempo del video.

**R1 · Espacio de búsqueda de hiperparámetros.** Logística: C = 0,001 / 0,01 / 0,1 / 1 / 10 / 100. SVM: C = 0,1 / 1 / 10 y núcleos lineal o RBF. Random Forest: 100 / 200 / 400 árboles y profundidad 5 / 10 / 20 o sin límite. La mejor configuración se elige en cada pliegue externo mediante el promedio interno de F1 macro. El número de árboles elegido puede cambiar de un pliegue a otro.

**R2 · Matriz completa de Random Forest en D.** Con filas de referencia y columnas de predicción en orden sana, afectada, las celdas son [[605, 153], [149, 574]]. Exactitud global: (605 + 574) / 1.481 = 79,6 %. Sensibilidad de la clase afectada: 574 / 723 = 79,4 %. Esta exactitud agrupa todas las predicciones; el F1 macro 0,796 promedia los cinco F1 externos. La cercanía numérica es circunstancial.

**R3 · EDA de imágenes y límites.** Tras depurar: 758 fotografías sanas, 155 con ácaro y 568 con roya. La cobertura mediana de hoja documentada en el informe fue 24,9 % del encuadre (cuartiles 18,9 % y 31,8 %). La mediana de brillo dentro de la máscara fue 133 en escala 0–255 (cuartiles 117 y 151). La cobertura mide tamaño aparente de la hoja en la foto. El área lesionada individual quedó sin medir. Estas cifras proceden del apartado de EDA del informe.

**Respuestas breves para el ensayo**

- **¿Entrenaron un modelo multiclase?** La salida fue binaria. En el análisis de errores usamos la etiqueta original para calcular qué porcentaje de cada subgrupo recibió la predicción «afectada».
- **¿La máscara fue predicha?** Utilizamos el contorno anotado en RoCoLe. Obtener el contorno de una fotografía nueva es un paso pendiente para evaluar el flujo en campo.
- **¿Por qué no validar por foto?** Una planta puede aportar varias hojas y las dos caras de una misma hoja pueden parecerse. Los grupos también recogen vínculos detectados por duplicados. Separarlos evita que un mismo grupo participe en ajuste y evaluación.
- **¿Cuánto aportó HSV?** En la misma prueba exploratoria y con máscara, el F1 macro de Random Forest pasó de 0,677 a 0,742 al agregar HSV, una diferencia de 0,065. D mantuvo fija esa representación. El paso de 0,74 a 0,796 corresponde a un cambio de protocolo y conjunto de evaluación.
- **¿Qué significa un falso negativo aquí?** La imagen tiene referencia «afectada» y el clasificador devuelve «sana». Las 149 corresponden al experimento D; las 35, al conjunto de prueba de C.
- **¿Qué significa el intervalo del 95 %?** Se calculó con la t de Student sobre los cinco F1 externos. Sirve como resumen aproximado de la variación observada. Una afirmación de superioridad estadística requeriría un análisis adicional.
- **¿Cómo trataron los desacuerdos de severidad?** Entre los pares donde ambas etiquetas eran roya se conservó una copia y se registró la decisión asistida por IA. La incertidumbre puede afectar el desglose por nivel, aunque ambas copias ya coincidían en la etiqueta binaria.
- **¿Qué valor usar para el bosque en A?** 0,5707, procedente de la salida del cuaderno A y su CSV individual. Un consolidado anterior conserva 0,5381; el origen de esa diferencia está pendiente. El gráfico usa los archivos individuales identificados en esta carpeta.

## Indicaciones de montaje para Cursor y HyperFrames

1. Formato 16:9, 1920 × 1080. Fondo marfil claro, texto carbón, verde oscuro para la serie principal y naranja oscuro para errores o para la serie afectada. Definir la leyenda en cada gráfico; acompañar el color con etiquetas.
2. Usar **Poppins** en títulos, textos, ejes y cifras. Usar **Source Serif 4** en un subtítulo breve de apertura y en el cierre. Cuerpo visible desde 30 px en 1080p; títulos desde 52 px. Mantener cifras tabulares y comas decimales.
3. Separar el copy visible de las notas de voz. Una tabla completa y una fotografía grande deben aparecer en momentos sucesivos cuando compitan por espacio. Dejar al menos dos segundos de lectura después de revelar un conteo importante.
4. Usar transiciones breves por corte o fundido. El movimiento debe explicar la comparación: dos caras que permanecen en el mismo grupo, el contorno que aparece sobre la hoja o el pliegue externo que se reserva para evaluar. Conservar encuadre, color original y proporciones de las fotografías.
5. Usar las figuras y datos incluidos. Las tablas y gráficos nuevos deben tomar sus valores de los CSV o de las tablas verificadas de este guion. Añadir pie discreto con el experimento y la población, por ejemplo «C · prueba exploratoria · n = 226» o «D · cinco pliegues externos · n = 1.481».
6. Verificar primero los fotogramas de 03, 08, 10 y 11 a tamaño de reproducción. Las cifras, etiquetas y denominadores deben leerse con claridad. Reservar una pausa antes de cambiar de orador. Cronometrar una lectura a cuatro voces y ajustar los tiempos a la duración que indique el docente.

**Ubicación de las fuentes.** Fotografías de apertura y ejemplos de evaluación: `data/curated/rocole/photos/`. Par duplicado antes de la limpieza: `data/raw/RoCoLe/Photos/`. Mosaico, mapa ExG y máscara: `experiments/results/`. Exploración y métricas: `experiments/results/rocole/`, carpetas A-full, B-masked, C-hsv-masked y D-cv-errores. El índice de particiones procede de `data/featured/rocole/index.csv`. Los CSV de predicciones y métricas se conservan con sus nombres originales.
