from sqlalchemy.orm import Session
from .. import models, schemas
from .. models import Document

def create_doc(db: Session, doc: schemas.DocumentCreate, user_id: int):
    db_doc = models.Document(**doc.model_dump(), user_id=user_id)
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc

def list_all_docs(db: Session, user_id: int):
    return db.query(models.Document).filter(models.Document.user_id == user_id).all()

def list_doc_by_id(db: Session, doc_id: int, user_id: int):
    return db.query(models.Document).filter(Document.id == doc_id, Document.user_id == user_id).first()

def update_doc(db: Session, doc_id: int, doc_data: schemas.ProjectUpdate, user_id: int):
    db_doc = db.query(models.Document).filter_by(id=doc_id, user_id=user_id).first()
    if not db_doc:
        raise ValueError("Document not found or you don't have permission to update it")
    for key, value in doc_data.model_dump().items():
        setattr(db_doc, key, value)

    db.commit()
    db.refresh(db_doc)
    return db_doc

def delete_doc(db: Session, doc_id: int, user_id: int):
    db_doc = db.query(models.Document).filter_by(id=doc_id, user_id=user_id).first()
    if not db_doc:
        raise ValueError("Document not found or you don't have permission to delete it")

    db.delete(db_doc)
    db.commit()
    return {"message": "Document deleted"}