from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..auth import get_current_user
from ..crud.documents import list_all_docs, list_doc_by_id, create_doc, update_doc, delete_doc
from ..database import get_db
from ...app import models, schemas
from ..models import User

router = APIRouter()

@router.post("/document", response_model=schemas.DocumentCreate)
async def create_doc(doc: schemas.DocumentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Creating new project. Current_user automatically assigned."""
    return create_doc(db=db, doc=doc, user_id=current_user.id)

@router.get("/documents")
def get_docs(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    all_docs = list_all_docs(db, user_id=current_user.id)
    if not all_docs:
        return {"message": "No documents found"}
    return all_docs

@router.get("/documents/{doc_id}")
def get_doc(doc_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    doc = list_doc_by_id(db, doc_id, user_id=current_user.id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@router.put("/documents/{doc_id}", response_model=schemas.ProjectUpdate)
def update_doc(doc_id: int, doc_data: schemas.ProjectUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        return update_doc(db, doc_id, doc_data, user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/documents/{doc_id}", response_model=dict)
def delete_doc(doc_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        return delete_doc(db, doc_id, user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))