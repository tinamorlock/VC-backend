# routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.app import schemas, models
from backend.app.database import get_db
from backend.app.auth import get_current_user
from backend.app.crud import comments as crud_comments

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.get("/comments", response_model=List[schemas.Comment])
def get_comments(db: Session = Depends(get_db)):
    comments = crud_comments.get_comments(db)
    return comments

@router.post("/", response_model=schemas.Comment)
def create_comment(
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Create a new comment. If `parent_id` is provided, it will nest the comment under the parent.
    """
    return crud_comments.create_comment(db=db, comment=comment, user_id=current_user.id)


@router.get("/file/{file_id}", response_model=List[schemas.Comment])
def get_comments(file_id: int, db: Session = Depends(get_db)):
    """
    Get all comments for a specific file, including nested comments.
    """
    comments = crud_comments.get_comments_by_file(db=db, file_id=file_id)
    if not comments:
        raise HTTPException(status_code=404, detail="No comments found for this file")
    return comments


@router.put("/{comment_id}", response_model=schemas.Comment)
def update_comment(
    comment_id: int,
    content: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Update an existing comment. Only the comment's creator can update it.
    """
    updated_comment = crud_comments.update_comment(db=db, comment_id=comment_id, updated_content=content, user_id=current_user.id)
    if not updated_comment:
        raise HTTPException(status_code=404, detail="Comment not found or not authorized to update")
    return updated_comment


@router.delete("/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Delete a comment. Only the comment's creator can delete it.
    """
    deleted_comment = crud_comments.delete_comment(db=db, comment_id=comment_id, user_id=current_user.id)
    if not deleted_comment:
        raise HTTPException(status_code=404, detail="Comment not found or not authorized to delete")
    return {"message": "Comment deleted successfully"}
