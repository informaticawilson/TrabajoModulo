"""Punto de entrada de la aplicación TELBOL DocManager."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import auth, models
from app.database import Base, SessionLocal, engine
from app.routers import auth as auth_router
from app.routers import documents as documents_router

# Crea las tablas si no existen (suficiente para el MVP; en un proyecto más
# grande se usaría Alembic para migraciones).
Base.metadata.create_all(bind=engine)


def _seed_demo_user():
    """Crea un usuario demo si no existe, solo para facilitar pruebas manuales."""
    db = SessionLocal()
    try:
        existing = db.query(models.User).filter(models.User.username == "demo").first()
        if not existing:
            demo = models.User(username="demo", password_hash=auth.hash_password("demo123"))
            db.add(demo)
            db.commit()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    _seed_demo_user()
    yield


app = FastAPI(
    title="TELBOL DocManager",
    description="Sistema de gestión documental digital — TELBOL S.A.",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS: permite que el frontend (abierto como archivo local o en servidor de
# desarrollo) pueda llamar a la API desde el navegador.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "null",  # cubre apertura directa de archivo local (file://)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(documents_router.router)


@app.get("/")
def root():
    return {"status": "ok", "service": "TELBOL DocManager"}
