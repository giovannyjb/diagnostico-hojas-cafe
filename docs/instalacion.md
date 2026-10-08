# Instalación

## Requisitos
- Python 3.11 o 3.12 · git
- (App móvil) Node.js LTS + Expo, **o** Flutter — según la decisión en [arquitectura.md](arquitectura.md)

## Entorno de análisis y modelado

```bash
git clone https://github.com/<org-o-usuario>/diagnostico-hojas-cafe.git
cd diagnostico-hojas-cafe
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Datos: ver [datos.md](datos.md).

Notebooks: `jupyter lab` y abrir `notebooks/`. Para importar código del proyecto desde un notebook:

```python
import sys; sys.path.append("..")   # raíz del repo
from src.features.extract import image_to_features
```

## Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
# http://localhost:8000/docs
```

Variables de entorno (opcional, archivo `.env` **no versionado**):

| Variable | Default | Uso |
|----------|---------|-----|
| `MODEL_PATH` | `../models/modelo.joblib` | Ruta del artefacto del modelo |

## Pruebas

```bash
pytest
```

## Problemas comunes

- `ModuleNotFoundError: src` → ejecutar desde la raíz del repo o agregar la raíz a `PYTHONPATH`.
- El backend responde 503 → aún no hay modelo exportado en `models/`.
- La app no llega al backend → teléfono y laptop en la misma red; usar la IP local de la laptop, no `localhost`.
