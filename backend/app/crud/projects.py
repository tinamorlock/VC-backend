from sqlalchemy.orm import Session
from .. import models, schemas
from .. models import Project

def create_project(db: Session, project: schemas.ProjectCreate, user_id: int):
    db_project = models.Project(**project.model_dump(), user_id=user_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def list_all_projects(db: Session, user_id: int):
    return db.query(models.Project).filter(models.Project.user_id == user_id).all()

def list_project_by_id(db: Session, project_id: int, user_id: int):
    return db.query(models.Project).filter(Project.id == project_id, Project.user_id == user_id).first()

def update_project(db: Session, project_id: int, project_data: schemas.ProjectUpdate, user_id: int):
    db_project = db.query(models.Project).filter_by(id=project_id, user_id=user_id).first()
    if not db_project:
        raise ValueError("Project not found or you don't have permission to update it")
    for key, value in project_data.model_dump().items():
        setattr(db_project, key, value)

    db.commit()
    db.refresh(db_project)
    return db_project

def delete_project(db: Session, project_id: int, user_id: int):
    db_project = db.query(models.Project).filter_by(id=project_id, user_id=user_id).first()
    if not db_project:
        raise ValueError("Project not found or you don't have permission to delete it")

    db.delete(db_project)
    db.commit()
    return {"message": "Project deleted"}