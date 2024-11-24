from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..auth import create_access_token
from ..security import hash_password, verify_password
from ..database import get_db, SessionLocal
from ..models import User

router = APIRouter()

@router.post("/register")
async def register_user(username: str, firstname: str, lastname: str, email: str, phone: str, raw_password: str):
    hashed_password, salt = hash_password(raw_password)
    db = SessionLocal()
    try:
        user = User(
            username=username,
            firstname=firstname,
            lastname=lastname,
            email=email,
            phone=phone,
            hashed_password=hashed_password,
            salt=salt
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()

@router.post("/login")
async def login_user(email: str, provided_password: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if verify_password(user.hashed_password, user.salt, provided_password):
            return {"message": "Login successful"}
        else:
            raise HTTPException(status_code=404, detail="Incorrect password")
    finally:
        db.close()