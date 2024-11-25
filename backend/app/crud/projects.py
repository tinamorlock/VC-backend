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