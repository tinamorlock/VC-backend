from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..auth import get_current_user
from ..crud.projects import list_all_projects, list_project_by_id, create_project, update_project, delete_project
from ..database import get_db
from ...app import models, schemas
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

@router.put("/projects/{project_id}", response_model=schemas.Project)
def update_project(project_id: int, project_data: schemas.ProjectUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        return update_project(db, project_id, project_data, user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/projects/{project_id}", response_model=dict)
def delete_project(project_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        return delete_project(db, project_id, user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))