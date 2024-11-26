from sqlalchemy.orm import Session
from ..models import Project, Document, Follows

def timeline (user_id: int, db: Session): # timeline for social media functionality, will add onto
    followed_users = (
        db.query(Follows.following)
        .filter(Follows.follower == user_id)
        .subquery()
    )

    public_projects = (
        db.query(Project)
        .filter(Project.user_id.in_(followed_users))
        .filter(Project.is_public == True)
        .all()
    )

    public_documents = (
        db.query(Document)
        .filter(Document.user_id.in_(followed_users))
        .filter(Document.is_public == True)
        .all()
    )

    timeline_items = {
        "projects": public_projects,
        "documents": public_documents,
    }

    return timeline_items