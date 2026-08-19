"""Configuración de la conexión a la base de datos (SQLite)."""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./telbol.db")

# check_same_thread=False es necesario porque FastAPI puede usar la conexión
# desde distintos hilos (TestClient incluido).
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency de FastAPI: entrega una sesión de BD y la cierra al finalizar."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
