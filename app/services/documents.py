"""Document Service: lógica de negocio de carga y búsqueda (RF-01, RF-02)."""
import os
import uuid
from typing import Optional

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.repositories import DocumentRepository

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".xlsx", ".png", ".jpg", ".jpeg"}
MAX_FILE_SIZE_MB = 10
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")


class DocumentService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = DocumentRepository(db)

    def upload(
        self,
        file: UploadFile,
        title: str,
        category: str,
        description: Optional[str],
        user_id: int,
    ):
        ext = os.path.splitext(file.filename or "")[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"Formato de archivo no permitido: '{ext}'. Permitidos: {sorted(ALLOWED_EXTENSIONS)}",
            )

        contents = file.file.read()
        size_mb = len(contents) / (1024 * 1024)
        if size_mb > MAX_FILE_SIZE_MB:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"El archivo supera el tamaño máximo permitido de {MAX_FILE_SIZE_MB} MB",
            )

        os.makedirs(UPLOAD_DIR, exist_ok=True)
        stored_name = f"{uuid.uuid4().hex}{ext}"
        stored_path = os.path.join(UPLOAD_DIR, stored_name)
        with open(stored_path, "wb") as f:
            f.write(contents)

        return self.repo.create(
            title=title,
            category=category,
            description=description,
            filepath=stored_path,
            uploaded_by_id=user_id,
        )

    def search(
        self,
        query: Optional[str],
        category: Optional[str],
        limit: int = 20,
        offset: int = 0,
    ):
        return self.repo.search(query, category, limit=limit, offset=offset)
