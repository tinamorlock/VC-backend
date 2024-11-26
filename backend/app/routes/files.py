import shutil

from fastapi import APIRouter, HTTPException, UploadFile, Depends, Path
from sqlalchemy.orm import Session

from backend.app import schemas
from backend.app.crud.files import create_file, get_files_by_document, delete_file
from backend.app.database import get_db

router = APIRouter()

UPLOAD_DIR = Path("uploads")
# Create the directory if it doesn't exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/files/upload", response_model=schemas.FileResponse)
def upload_file(
    file: UploadFile,
    document_id: int,  # Document association
    db: Session = Depends(get_db)
):
    file_path = UPLOAD_DIR / file.filename
    if file_path.exists():
        raise HTTPException(status_code=400, detail="File already exists.")

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_data = schemas.FileCreate(
        filename=file.filename,
        file_path=str(file_path),
        file_size=file_path.stat().st_size,
        file_type=file.content_type,
        document_id=document_id
    )
    return create_file(db, file_data)

@router.get("/documents/{document_id}/files", response_model=list[schemas.FileResponse])
def list_files(document_id: int, db: Session = Depends(get_db)):
    return get_files_by_document(db, document_id=document_id)

@router.delete("/files/{file_id}", response_model=schemas.FileResponse)
def delete_file(file_id: int, document_id: int, db: Session = Depends(get_db)):
    db_file = delete_file(db, file_id=file_id, document_id=document_id)
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found.")

    # Delete file from local storage
    file_path = Path(db_file.file_path)
    if file_path.exists():
        file_path.unlink()

    return db_file
