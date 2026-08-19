# Requirements — document-management-mvp

## Contexto
TELBOL S.A. necesita un sistema para organizar su documentación digital
y realizar búsquedas eficientes. Este documento define el alcance
mínimo (MVP) implementado como monolito FastAPI + SQLite.

## RF-01: Carga y almacenamiento de documentos

**User Story:** Como usuario autenticado, quiero subir un documento con
título, categoría y descripción opcional, para tener mi documentación
organizada y disponible en el sistema.

**Criterios de aceptación (EARS):**
- CUANDO un usuario autenticado sube un archivo válido (≤10 MB, formato
  permitido: pdf, docx, xlsx, png, jpg, jpeg) con título y categoría,
  EL SISTEMA DEBERÁ guardarlo y responder con un identificador único
  (201 Created).
- CUANDO un usuario intenta subir un archivo no permitido o mayor a
  10 MB, EL SISTEMA DEBERÁ rechazar la carga con un mensaje de error
  claro (400 Bad Request).
- CUANDO un usuario no autenticado intenta subir un documento,
  EL SISTEMA DEBERÁ responder 401 Unauthorized.

**Estado:** ✅ Implementado (`app/routers/documents.py`, `app/services/documents.py`).

## RF-02: Búsqueda y filtrado de documentos

**User Story:** Como usuario autenticado, quiero buscar documentos por
texto y filtrarlos por categoría, para encontrar rápidamente lo que
necesito.

**Criterios de aceptación (EARS):**
- CUANDO el usuario busca por una palabra clave contenida en el título
  o descripción, EL SISTEMA DEBERÁ retornar únicamente los documentos
  que coinciden.
- CUANDO se combina un filtro de categoría con una búsqueda por texto,
  EL SISTEMA DEBERÁ retornar solo los documentos que cumplen ambos
  criterios.
- CUANDO no hay coincidencias, EL SISTEMA DEBERÁ retornar una lista
  vacía con código 200 (no error).

**Estado:** ✅ Implementado (`app/repositories.py::DocumentRepository.search`).

## RF-03: Gestión de acceso básico (autenticación)

**User Story:** Como administrador del sistema, quiero que cada acción
quede asociada a un usuario autenticado, para tener trazabilidad de
quién sube y consulta documentos.

**Criterios de aceptación (EARS):**
- CUANDO un usuario registrado ingresa credenciales correctas,
  EL SISTEMA DEBERÁ retornar un token de acceso (JWT) válido.
- CUANDO un usuario ingresa credenciales incorrectas, EL SISTEMA DEBERÁ
  responder 401 sin indicar cuál dato falló.
- CUANDO se llama a un endpoint protegido con un token expirado o
  inválido, EL SISTEMA DEBERÁ responder 401.

**Estado:** ✅ Implementado (`app/auth.py`, `app/routers/auth.py`).

## Fuera de alcance (explícitamente excluido del MVP)
- Versionado de documentos.
- Roles y permisos granulares (solo existe "usuario autenticado").
- Papelera de reciclaje / soft delete.
- Almacenamiento en la nube (se usa filesystem local).
