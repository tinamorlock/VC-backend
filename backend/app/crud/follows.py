from sqlalchemy.orm import Session
from backend.app import models

def timeline (user_id: int, db: Session): # timeline for social media functionality, will add onto
    followed_users = (
        db.query(models.Follows.following)
        .filter(models.Follows.follower == user_id)
        .subquery()
    )

    public_projects = (
        db.query(models.Project)
        .filter(models.Project.user_id.in_(followed_users))
        .filter(models.Project.is_public == True)
        .all()
    )

    public_documents = (
        db.query(models.Document)
        .filter(models.Document.user_id.in_(followed_users))
        .filter(models.Document.is_public == True)
        .all()
    )

    timeline_items = {
        "projects": public_projects,
        "documents": public_documents,
    }

    return timeline_items