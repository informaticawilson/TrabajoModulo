"""Endpoints de documentos: carga (RF-01), búsqueda (RF-02) y descarga (RF-01)."""
import os
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import get_current_user
from app.database import get_db
from app.repositories import DocumentRepository
from app.services.documents import DocumentService

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("", response_model=schemas.DocumentOut, status_code=201)
def upload_document(
    title: str = Form(...),
    category: str = Form(...),
    description: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    service = DocumentService(db)
    return service.upload(file, title, category, description, current_user.id)


@router.get("/search", response_model=list[schemas.DocumentOut])
def search_documents(
    q: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    service = DocumentService(db)
    return service.search(q, category, limit=limit, offset=offset)


@router.get("/{doc_id}")
def download_document(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Descarga el archivo físico del documento indicado por su id."""
    repo = DocumentRepository(db)
    document = repo.get_by_id(doc_id)
    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Documento con id {doc_id} no encontrado",
        )
    if not os.path.exists(document.filepath):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El archivo físico del documento no está disponible",
        )
    return FileResponse(path=document.filepath, filename=os.path.basename(document.filepath))


@router.delete("/{doc_id}", status_code=204)
def delete_document(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Elimina un documento. Solo el propietario puede borrarlo."""
    repo = DocumentRepository(db)
    document = repo.get_by_id(doc_id)
    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Documento con id {doc_id} no encontrado",
        )
    if document.uploaded_by_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar este documento",
        )
    try:
        os.remove(document.filepath)
    except FileNotFoundError:
        pass
    repo.delete(document)
