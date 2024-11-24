from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..auth import get_current_user
from ..security import hash_password, verify_password
from ..database import get_db, SessionLocal
from ..models import User
from ...app import models, schemas
from ...app.crud import projects

router = APIRouter()

@router.post("/project", response_model=schemas.Project)
async def create_project(project: schemas.Project, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Creating new project. Current_user automatically assigned."""
    return projects.create_project(db=db, project=project, user_id=current_user.id)
