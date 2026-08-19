"""Endpoints de autenticación (RF-03)."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import auth, schemas
from app.database import get_db
from app.repositories import UserRepository

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=schemas.UserOut, status_code=201)
def register(payload: schemas.RegisterRequest, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    if repo.get_by_username(payload.username):
        raise HTTPException(status.HTTP_409_CONFLICT, "El nombre de usuario ya está en uso")
    password_hash = auth.hash_password(payload.password)
    user = repo.create(username=payload.username, password_hash=password_hash)
    return user


@router.post("/login", response_model=schemas.TokenResponse)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    user = repo.get_by_username(payload.username)

    # Mensaje genérico en ambos casos (usuario inexistente o password incorrecta)
    # para no filtrar cuál de los dos datos falló.
    if not user or not auth.verify_password(payload.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Usuario o contraseña incorrectos")

    token = auth.create_access_token({"sub": user.username})
    return schemas.TokenResponse(access_token=token)
