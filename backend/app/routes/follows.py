from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app import schemas, models
from backend.app.auth import get_current_user
from backend.app.database import get_db
from backend.app.main import app

router = APIRouter()

@app.post("/follow", response_model=schemas.Follow)
def follow(follows: schemas.FollowCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    new_follow = models.Follows(follower_id=current_user.id, following_id=follows.following_id)
    db.add(new_follow)
    db.commit()
    db.refresh(new_follow)
    return new_follow

@app.get("/users/{user_id}/followers", response_model=List[schemas.Follow])
def get_followers(
    user_id: int, db: Session = Depends(get_db)
):
    followers = db.query(models.Follows).filter_by(following_id=user_id).all()
    if not followers:
        raise HTTPException(status_code=404, detail="This user doesn't have any followers")
    return followers

@app.get("/users/{user_id}/following", response_model=List[schemas.Follow])
def get_following(user_id: int, db: Session = Depends(get_db)):
    following = db.query(models.Follows).filter_by(follower_id=user_id).all()
    if not following:
        raise HTTPException(status_code=404, detail="This user is not following anyone.")
    return following

@app.delete("/users/{user_id}/unfollow/{following_id}", response_model=schemas.Follow)
def unfollow(user_id: int, following_id: int, db: Session = Depends(get_db)):
    follow_record = db.query(models.Follows).filter_by(follower=user_id, following=following_id).first()
    if not follow_record:
        raise HTTPException(status_code=404, detail="Relationship not found.")
    db.delete(follow_record)
    db.commit()

    return {"detail": f"User {user_id} unfollowed user {following_id}"}

@app.get("/friends", response_model=List[schemas.Follow])
def get_friends(db: Session = Depends(get_db)): ##### START HERE!!