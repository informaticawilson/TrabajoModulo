# Especificación del Proyecto — TELBOL DocManager

Este documento resume el caso de estudio. El detalle completo (los 7
puntos del enunciado, incluyendo guía paso a paso de Kiro y GitHub)
está en `TELBOL_Caso_Estudio_Solucion.docx` entregado junto al
repositorio.

## 1. Definición del problema
TELBOL S.A. no cuenta con un sistema centralizado para organizar su
documentación digital, dificultando la búsqueda eficiente y el control
de quién sube cada documento.

## 2. Requisitos funcionales
Ver `.kiro/specs/document-management-mvp/requirements.md` para el
detalle completo con criterios de aceptación en formato EARS.

- RF-01: Carga y almacenamiento de documentos
- RF-02: Búsqueda y filtrado de documentos
- RF-03: Autenticación de usuarios

## 3. Arquitectura
Ver `.kiro/specs/document-management-mvp/design.md` para el diagrama
de componentes y el modelo de datos completo.

Resumen: monolito FastAPI + SQLite + almacenamiento local de archivos,
en capas API → Service → Repository → BD/Storage.

## 4. Pruebas
`tests/test_documents.py` cubre casos de éxito y error para los 3 RF
(9 pruebas en total). Ejecutar con `pytest -v`.

## 5. Control de versiones
Ver la sección 6 del informe completo para el flujo de ramas, commits
(Conventional Commits) y pull requests usado en este proyecto.

## 6. Referencia de endpoints

La API corre por defecto en `http://localhost:8000`. Todos los endpoints protegidos requieren el encabezado `Authorization: Bearer <token>` con un JWT válido obtenido en `/auth/login`.

### Tabla de resumen

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| POST | `/auth/register` | No | Crea un nuevo usuario |
| POST | `/auth/login` | No | Autentica al usuario y devuelve un JWT |
| POST | `/documents` | Sí | Sube un archivo y lo registra en la BD |
| GET | `/documents/search` | Sí | Lista y filtra documentos con paginación |
| GET | `/documents/{id}` | Sí | Descarga el archivo físico del documento |
| DELETE | `/documents/{id}` | Sí | Elimina un documento (solo el propietario) |

---

### POST /auth/register

Crea un nuevo usuario en el sistema.

**Body (JSON)**

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `username` | string | Sí | Nombre de usuario único |
| `password` | string | Sí | Contraseña en texto plano |

**Ejemplo de request**

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "ana.garcia", "password": "S3cr3t0!"}'
```

**Respuesta 201 Created**

```json
{
  "id": 1,
  "username": "ana.garcia"
}
```

**Errores posibles**

- `409 Conflict` — el nombre de usuario ya está en uso.

---

### POST /auth/login

Autentica al usuario y devuelve un JWT con validez de 30 minutos.

**Body (JSON)**

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `username` | string | Sí | Nombre de usuario |
| `password` | string | Sí | Contraseña |

**Ejemplo de request**

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "ana.garcia", "password": "S3cr3t0!"}'
```

**Respuesta 200 OK**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Errores posibles**

- `401 Unauthorized` — usuario o contraseña incorrectos (mensaje genérico para no revelar cuál de los dos falló).

---

### POST /documents

Sube un archivo y lo registra con sus metadatos. El cuerpo debe enviarse como `multipart/form-data`.

**Campos del formulario**

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `title` | string | Sí | Título descriptivo del documento |
| `category` | string | Sí | Categoría (p. ej. `"contratos"`, `"facturas"`) |
| `description` | string | No | Descripción libre |
| `file` | archivo | Sí | Archivo a subir (cualquier tipo MIME) |

**Ejemplo de request**

```bash
curl -X POST http://localhost:8000/documents \
  -H "Authorization: Bearer <token>" \
  -F "title=Contrato de servicios 2024" \
  -F "category=contratos" \
  -F "description=Contrato anual con proveedor TechSupply" \
  -F "file=@/home/ana/documentos/contrato_2024.pdf"
```

**Respuesta 201 Created**

```json
{
  "id": 7,
  "title": "Contrato de servicios 2024",
  "category": "contratos",
  "description": "Contrato anual con proveedor TechSupply",
  "uploaded_at": "2024-06-15T10:32:45.123456"
}
```

**Errores posibles**

- `401 Unauthorized` — token ausente o inválido.
- `422 Unprocessable Entity` — faltan campos requeridos.

---

### GET /documents/search

Devuelve la lista de documentos. Admite filtrado por texto y categoría, más paginación.

**Parámetros de query**

| Parámetro | Tipo | Defecto | Descripción |
|-----------|------|---------|-------------|
| `q` | string | — | Texto a buscar en título y descripción |
| `category` | string | — | Filtra por categoría exacta |
| `limit` | int (1–100) | 20 | Cantidad máxima de resultados |
| `offset` | int (≥ 0) | 0 | Desplazamiento para paginación |

**Ejemplo de request — búsqueda con filtros**

```bash
curl "http://localhost:8000/documents/search?q=contrato&category=contratos&limit=10&offset=0" \
  -H "Authorization: Bearer <token>"
```

**Ejemplo de request — listar todos (primera página)**

```bash
curl "http://localhost:8000/documents/search" \
  -H "Authorization: Bearer <token>"
```

**Respuesta 200 OK**

```json
[
  {
    "id": 7,
    "title": "Contrato de servicios 2024",
    "category": "contratos",
    "description": "Contrato anual con proveedor TechSupply",
    "uploaded_at": "2024-06-15T10:32:45.123456"
  },
  {
    "id": 3,
    "title": "Contrato de arrendamiento oficina",
    "category": "contratos",
    "description": null,
    "uploaded_at": "2024-01-08T09:15:00.000000"
  }
]
```

**Errores posibles**

- `401 Unauthorized` — token ausente o inválido.
- `422 Unprocessable Entity` — valor fuera de rango en `limit` u `offset`.

---

### GET /documents/{id}

Descarga el archivo físico asociado al documento. La respuesta es el contenido binario del archivo con el nombre original en la cabecera `Content-Disposition`.

**Parámetros de ruta**

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `id` | int | Identificador del documento |

**Ejemplo de request**

```bash
curl -OJ http://localhost:8000/documents/7 \
  -H "Authorization: Bearer <token>"
```

> La opción `-OJ` indica a curl que guarde el archivo con el nombre que indica el servidor.

**Respuesta 200 OK**

Cuerpo: contenido binario del archivo.  
Cabecera relevante: `Content-Disposition: attachment; filename="contrato_2024.pdf"`.

**Errores posibles**

- `401 Unauthorized` — token ausente o inválido.
- `404 Not Found` — no existe un documento con ese `id`, o el archivo físico fue removido del servidor.

---

### DELETE /documents/{id}

Elimina el registro del documento y su archivo físico. Solo puede ejecutarlo el usuario que subió el documento.

**Parámetros de ruta**

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `id` | int | Identificador del documento |

**Ejemplo de request**

```bash
curl -X DELETE http://localhost:8000/documents/7 \
  -H "Authorization: Bearer <token>"
```

**Respuesta 204 No Content**

Sin cuerpo de respuesta.

**Errores posibles**

- `401 Unauthorized` — token ausente o inválido.
- `403 Forbidden` — el documento pertenece a otro usuario.
- `404 Not Found` — no existe un documento con ese `id`.
