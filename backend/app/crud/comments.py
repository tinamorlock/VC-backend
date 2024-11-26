# crud.py
from typing import List

from sqlalchemy.orm import Session

from backend.app import models, schemas
from backend.app.models import Comments
from backend.app.schemas import Comment


def build_comment_tree(comments: List[Comments]) -> List[Comment]:
    """
    Builds a tree of comments where replies are nested under their parent comments.
    """
    comment_map = {comment.id: comment for comment in comments}
    root_comments = []

    for comment in comments:
        if comment.parent_id:
            parent = comment_map.get(comment.parent_id)
            if parent:
                parent.replies.append(comment)
        else:
            root_comments.append(comment)

    return root_comments

def get_comments(db: Session) -> List[Comment]:
    """
    Fetch all comments from the database and return them as a tree structure.
    """
    comments = db.query(Comments).all()
    return build_comment_tree(comments)

def create_comment(db: Session, comment: schemas.CommentCreate, user_id: int):
    db_comment = models.Comments(
        content=comment.content,
        user_id=user_id,
        file_id=comment.file_id,
        parent_id=comment.parent_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_comments_by_file(db: Session, file_id: int):
    return db.query(models.Comments).filter(models.Comments.file_id == file_id).all()


def get_comment_by_id(db: Session, comment_id: int):
    return db.query(models.Comments).filter(models.Comments.id == comment_id).first()


def update_comment(db: Session, comment_id: int, updated_content: str, user_id: int):
    db_comment = db.query(models.Comments).filter(
        models.Comments.id == comment_id, models.Comments.user_id == user_id
    ).first()
    if db_comment:
        db_comment.content = updated_content
        db.commit()
        db.refresh(db_comment)
    return db_comment


def delete_comment(db: Session, comment_id: int, user_id: int):
    db_comment = db.query(models.Comments).filter(
        models.Comments.id == comment_id, models.Comments.user_id == user_id
    ).first()
    if db_comment:
        db.delete(db_comment)
        db.commit()
    return db_comment
