# API del backend

Base URL en desarrollo: `http://localhost:8000` · documentación interactiva: `http://localhost:8000/docs`.

## `GET /health`

Estado del servicio y si el modelo está disponible.

```json
{ "status": "ok", "modelo_cargado": true, "features_version": "hsv-hist-v1" }
```

## `POST /predict`

Diagnóstico de una hoja a partir de una imagen.

**Request:** `multipart/form-data` con el campo `file` (JPEG o PNG).

```bash
curl -X POST http://localhost:8000/predict -F "file=@hoja.jpg"
```

**Response 200:**

```json
{
  "clase": "roya",
  "confianza": 0.87,
  "probabilidades": { "sana": 0.05, "roya": 0.87, "minador": 0.04, "phoma": 0.02, "cercospora": 0.02 },
  "recomendacion": "Posible roya. Revisa el envés de otras hojas y consulta al técnico; considera manejo preventivo.",
  "modelo": { "features_version": "hsv-hist-v1", "trained_at": "…" }
}
```

**Errores:**

| Código | Cuándo |
|-------:|--------|
| 415 | El archivo no es JPEG/PNG |
| 422 | Falta el campo `file` |
| 503 | No hay modelo en `models/modelo.joblib` (entrenar y exportar primero) |

## Pendientes

- `POST /feedback` para que el usuario marque si el diagnóstico fue correcto (datos para mejorar).
- Autenticación simple por *API key* si el backend se publica en Internet.
- Límite de tamaño de imagen y redimensionado en el cliente.
