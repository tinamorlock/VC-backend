from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..auth import get_current_user
from ..crud.projects import list_all_projects, list_project_by_id, create_project
from ..database import get_db
from ...app import models, schemas
from ...app.crud import projects
from ..models import User

router = APIRouter()

@router.post("/project", response_model=schemas.Project)
async def create_project(project: schemas.Project, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Creating new project. Current_user automatically assigned."""
    return create_project(db=db, project=project, user_id=current_user.id)

@router.get("/projects")
def get_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    all_projects = list_all_projects(db, user_id=current_user.id)
    if not all_projects:
        return {"message": "No projects found"}
    return all_projects

@router.get("/projects/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = list_project_by_id(db, project_id, user_id=current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project