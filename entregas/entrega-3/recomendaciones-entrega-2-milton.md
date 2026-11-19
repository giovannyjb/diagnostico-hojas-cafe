# Recomendaciones Milton → informe final (55 %)

Fuente: retroalimentación Entrega 2 · **4,50 / 5,00** · calificado mié 18 nov 2026, 19:25 · Milton Orlando Sarria Paja.

Usar esta lista como checklist del trabajo técnico del final. No rellenar el informe con texto de Entrega 1.

## Lo que ya quedó bien (no romper)

- [x] Inventario limpio con criterio; BRACOL fuera justificado (especie, captura, anotación)
- [x] Separación por grupos de planta y duplicados (anti-fuga)
- [x] Comparación full / máscaras / máscaras+HSV con hipótesis claras
- [x] Mejora F1 macro **0,57 → 0,74** documentada
- [x] Errores acotados (35/111 afectadas → sanas) y conclusiones limitadas a máscaras disponibles

## Por hacer en el final

### 1. Estructura del informe
- [ ] Priorizar **resultados y análisis**
- [ ] No repetir problema / objetivos / estado del arte de Entrega 1 (solo remisión corta si hace falta)

### 2. EDA de imagen (profundizar)
- [ ] Severidad
- [ ] Tamaño de lesión
- [ ] Condiciones de iluminación
- [ ] Calidad de las máscaras

### 3. Validación
- [ ] Sustituir la partición única por **validación cruzada por grupos de planta**
- [ ] Reportar **intervalos de confianza** de las métricas

### 4. Modelado
- [ ] Ajuste de hiperparámetros (HPO)
- [ ] Probar **más modelos** (no solo los baselines A–B–C)

### 5. Clases (sensibilidad)
- [ ] La clase “afectada” mezcla ácaros y roya → reportar sensibilidad por **clase original**
- [ ] Reportar sensibilidad de **roya nivel 1** por separado

### 6. Errores
- [ ] Análisis **sistemático de falsos negativos** (no solo el conteo 35/111)

## Evidencia de la nota

Copia local de la calificación Intu (repo maestría, no este):  
`semestre-1/05-proyecto-I/mis-practicas/evidencia-entrega-2-nota-450.png`
