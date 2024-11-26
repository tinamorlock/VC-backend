from sqlalchemy.orm import Session

from backend.app import models, schemas

def create_file(db: Session, file_data: schemas.FileCreate):
    db_file = models.File(**file_data.model_dump())
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

def get_files_by_document(db: Session, document_id: int):
    return db.query(models.File).filter(models.File.document_id == document_id).all()

def delete_file(db: Session, file_id: int, document_id: int):
    db_file = db.query(models.File).filter(models.File.id == file_id, models.File.document_id == document_id).first()
    if db_file:
        db.delete(db_file)
        db.commit()
    return db_file
