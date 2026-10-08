# Backend — API del prototipo

FastAPI que carga el modelo exportado en `models/modelo.joblib` y expone `/health` y `/predict`. Contrato en [`docs/api.md`](../docs/api.md).

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
curl http://localhost:8000/health
curl -X POST http://localhost:8000/predict -F "file=@../data/raw/bracol/ejemplo.jpg"
```

Mientras no exista el modelo, `/predict` responde **503** (es lo esperado en la Etapa 1).

Para probar desde el teléfono: `uvicorn app.main:app --host 0.0.0.0 --port 8000` y usar la IP local de la laptop en la app.

Pendientes: Dockerfile · despliegue gratuito para la demo · `POST /feedback` · API key.
