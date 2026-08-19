# TELBOL DocManager — Frontend

Interfaz web mínima (HTML + CSS + JS) que consume la API REST de TELBOL DocManager.
No requiere Node.js, npm ni ninguna dependencia externa.

---

## 1. Arrancar la API

Desde la raíz del proyecto:

```bash
# (activa tu entorno virtual si lo usas)
uvicorn app.main:app --reload
```

La API queda disponible en `http://localhost:8000`.
La documentación interactiva (Swagger) en `http://localhost:8000/docs`.

---

## 2. Abrir el frontend

### Opción A — Directamente desde el sistema de archivos

Abre `frontend/index.html` en tu navegador (doble clic o `File > Open`).

> La API incluye `null` en los orígenes CORS permitidos, lo que cubre
> exactamente este caso (el navegador envía `Origin: null` cuando el
> archivo se abre desde disco).

### Opción B — Con un servidor local (recomendado para evitar restricciones del navegador)

Con Python (incluido en cualquier instalación estándar):

```bash
# Desde la carpeta frontend/
python -m http.server 5500
```

Luego abre `http://localhost:5500` en el navegador.

También puedes usar la extensión **Live Server** de VS Code: clic derecho en
`frontend/index.html` → *Open with Live Server* (escucha en el puerto 5500 por
defecto, que ya está en la lista CORS).

---

## 3. Uso básico

| Acción | Descripción |
|--------|-------------|
| **Registrarse** | Pestaña "Registrarse" → introduce usuario y contraseña → "Crear cuenta" |
| **Iniciar sesión** | Pestaña "Iniciar sesión" → credenciales → "Iniciar sesión" |
| **Subir documento** | Rellena título, categoría (y descripción opcional), selecciona un archivo → "Subir archivo" |
| **Buscar** | Escribe texto y/o elige categoría → "Buscar" (o pulsa Enter) |
| **Descargar** | Botón verde "Descargar" en la fila del documento |
| **Eliminar** | Botón rojo "Eliminar" (solo funciona si eres el propietario del documento) |

El token JWT se almacena en `localStorage` y se reutiliza entre recargas de
página. Para cerrar la sesión usa el botón "Cerrar sesión" en la cabecera.
