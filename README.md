# TELBOL DocManager

Sistema de gestión documental digital para TELBOL S.A. Permite cargar,
buscar y clasificar documentos con control de acceso básico.

## Problema que resuelve
TELBOL S.A. carecía de un sistema centralizado para organizar su
documentación, dificultando la búsqueda eficiente de archivos.

## Arquitectura
Monolito con FastAPI + SQLite + almacenamiento local de archivos.
Ver `docs/especificacion-proyecto.md` para el detalle de componentes,
diagrama de arquitectura y criterios de aceptación.

## Requisitos funcionales
- **RF-01**: Carga y almacenamiento de documentos
- **RF-02**: Búsqueda y filtrado de documentos
- **RF-03**: Autenticación de usuarios (JWT)

## Instalación
```bash
git clone https://github.com/<tu-usuario>/telbol-docmanager.git
cd telbol-docmanager
python3 -m venv venv
source venv/bin/activate          # en Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

La API queda disponible en `http://127.0.0.1:8000`. Documentación
interactiva automática en `http://127.0.0.1:8000/docs`.

Al arrancar por primera vez se crea un usuario de prueba:
`usuario: demo` / `contraseña: demo123`.

## Uso rápido (curl)
```bash
# Login
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "demo", "password": "demo123"}'

# Subir un documento (reemplaza TOKEN por el access_token recibido)
curl -X POST http://127.0.0.1:8000/documents \
  -H "Authorization: Bearer TOKEN" \
  -F "title=Manual de Usuario" \
  -F "category=manuales" \
  -F "file=@ruta/al/archivo.pdf"

# Buscar documentos
curl "http://127.0.0.1:8000/documents/search?q=Manual" \
  -H "Authorization: Bearer TOKEN"
```

## Pruebas
```bash
pytest -v
```

## Estructura del proyecto
```
telbol-docmanager/
├── app/
│   ├── main.py           # Punto de entrada FastAPI
│   ├── database.py       # Conexión SQLite / sesión
│   ├── models.py         # Modelos ORM (User, Document)
│   ├── schemas.py        # Esquemas Pydantic
│   ├── auth.py           # Hashing de contraseñas y JWT
│   ├── repositories.py   # Acceso a datos
│   ├── routers/          # Endpoints (auth, documents)
│   └── services/         # Lógica de negocio (documents)
├── tests/                 # Pruebas con pytest
├── .kiro/specs/           # Specs de Kiro (requirements, design, tasks)
├── docs/                  # Especificación del proyecto (SDD)
├── uploads/                # Archivos subidos (no versionado)
└── requirements.txt
```

## Tecnologías
Python, FastAPI, SQLAlchemy, SQLite, pytest, JWT (python-jose), bcrypt.

## Desarrollo con Kiro
Este proyecto sigue el flujo spec-driven de Kiro. Las specs ya están
redactadas en `.kiro/specs/document-management-mvp/` (`requirements.md`,
`design.md`, `tasks.md`). El código base de este repositorio ya
implementa los 3 requisitos funcionales; `tasks.md` señala qué tareas
quedan pendientes para ejecutar directamente en Kiro sin regenerar lo
ya construido.

## Autor
[Tu nombre] — Caso de estudio TELBOL S.A.
