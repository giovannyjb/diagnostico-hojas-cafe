# App móvil — prototipo

Objetivo del MVP: que un caficultor **fotografíe una hoja y reciba el diagnóstico** en segundos.

## Flujo (3 pantallas)

1. **Inicio** — botón "Tomar foto" / "Elegir de la galería" + instrucciones breves (hoja completa, fondo claro, buena luz).
2. **Enviando** — vista previa de la foto, indicador de carga; `POST /predict` al backend.
3. **Resultado** — clase (sana / roya / minador / phoma / cercospora), barra de confianza, recomendación, botón "¿Fue correcto?" (futuro `POST /feedback`) y "Nueva foto".

## Decisión de framework (pendiente)

| Opción | A favor | En contra |
|--------|---------|-----------|
| **Expo (React Native + TypeScript)** | Se prueba en el teléfono con Expo Go sin compilar; cámara y HTTP resueltos (`expo-camera`, `expo-image-picker`, `fetch`); JS es conocido | Dependencia de Node |
| **Flutter (Dart)** | Rendimiento y UI consistentes; `image_picker` + `http` | Curva de Dart; necesita SDK y emuladores |

Si nadie del equipo tiene preferencia fuerte: **Expo**. Cuando se decida, crear el proyecto dentro de esta carpeta (`npx create-expo-app app` o `flutter create app`) y documentar aquí cómo correrlo.

## Conexión con el backend

- Desarrollo: backend en la laptop con `--host 0.0.0.0`; la app usa `http://<IP-local-laptop>:8000`.
- Demo/sustentación: backend desplegado (Render / Railway / HF Spaces) o Docker; la URL va en una constante de configuración, nunca quemada en varias pantallas.
- Comprimir/redimensionar la foto en el cliente (≤ 1024 px) antes de enviarla.
