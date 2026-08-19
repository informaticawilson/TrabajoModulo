# Tasks — document-management-mvp

> El código base de este repositorio ya implementa las tareas 1 a 8.
> Al importar esta spec en Kiro, márcalas como completadas y ejecuta
> solo las tareas 9 en adelante (son las que realmente consumen
> créditos de IA; las anteriores son referencia de lo ya construido).

- [x] 1. Crear estructura del proyecto (`app/`, `tests/`, `uploads/`, `docs/`)
- [x] 2. Configurar conexión SQLite y `Base` de SQLAlchemy (`app/database.py`)
- [x] 3. Definir modelos `User` y `Document` (`app/models.py`)
- [x] 4. Definir esquemas Pydantic de entrada/salida (`app/schemas.py`)
- [x] 5. Implementar hashing de contraseñas y JWT (`app/auth.py`)
- [x] 6. Implementar endpoint de login (`app/routers/auth.py`) — cubre RF-03
- [x] 7. Implementar endpoint de carga de documentos (`app/routers/documents.py`, `app/services/documents.py`) — cubre RF-01
- [x] 8. Implementar endpoint de búsqueda con filtros (`app/repositories.py`) — cubre RF-02
- [x] 9. Escribir pruebas básicas con pytest cubriendo los 3 RF (`tests/test_documents.py`)

## Pendientes sugeridas (ejecutar en Kiro, una tarea a la vez)

- [x] 10. Agregar endpoint `GET /documents/{id}` para descargar el archivo físico de un documento.
- [x] 11. Agregar endpoint `DELETE /documents/{id}` restringido al usuario propietario.
- [x] 12. Agregar paginación simple (`limit`, `offset`) al endpoint de búsqueda.
- [x] 13. Agregar endpoint `POST /auth/register` para crear usuarios nuevos (actualmente solo existe el usuario demo sembrado en el arranque).
- [x] 14. (Opcional) Agregar un frontend mínimo en `frontend/` (HTML + fetch) que consuma la API para cumplir la parte de "interfaz mínima" mencionada en la definición del problema.
- [x] 15. (Opcional) Documentar los endpoints con ejemplos adicionales en `docs/especificacion-proyecto.md`.

> Recomendación de créditos: pide a Kiro una tarea a la vez y revisa el
> diff antes de aceptar. Para ajustes menores (nombres, mensajes de
> error, imports), edita el archivo tú mismo en vez de regenerar la
> tarea completa.
