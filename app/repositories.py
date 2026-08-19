"""Repository Layer: acceso a datos vía SQLAlchemy (ver design.md)."""
from typing import Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app import models


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> Optional[models.User]:
        return self.db.query(models.User).filter(models.User.username == username).first()

    def create(self, username: str, password_hash: str) -> models.User:
        user = models.User(username=username, password_hash=password_hash)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user


class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **kwargs) -> models.Document:
        document = models.Document(**kwargs)
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document

    def get_by_id(self, doc_id: int) -> Optional[models.Document]:
        return self.db.query(models.Document).filter(models.Document.id == doc_id).first()

    def search(
        self,
        query: Optional[str],
        category: Optional[str],
        limit: int = 20,
        offset: int = 0,
    ) -> list[models.Document]:
        q = self.db.query(models.Document)
        if query:
            like = f"%{query}%"
            q = q.filter(or_(models.Document.title.ilike(like), models.Document.description.ilike(like)))
        if category:
            q = q.filter(models.Document.category == category)
        return q.order_by(models.Document.uploaded_at.desc()).limit(limit).offset(offset).all()

    def delete(self, document: models.Document) -> None:
        self.db.delete(document)
        self.db.commit()
