import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import models, database
from .crud import # START HERE
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "ba0d6c9136cfe3f10a7ce9bddd1aedcf0e2976f05aa514f947d4143fab1cfdc9e8fe3e01d55e1927ccafcf618b98272b1b3e0d2539b0cd0584c31ac9a43b47c48f75e557c10b1186c141f3f973514106ac1c409c8539524c2c2862737b2a145a4d62d23c399bf9b90071bc8c133f628fee7fe0916bfee384d21969ab14b4c08b7bb845e4852cf381c581a9b5b44fd451d1f1eb937082a93ca30a34a1f6476f5d9b897ac5cc9ef43e06086c49acd4f24ae1f046d9bc5e67a266a89c8b5ad6c80ae6d593dc0bd9450f3afe048cadf90559026a08945e3485c3153e697d756dc9fb9374a38310d54b7621d50f49eb832c01bba4ec5788d94cc23f8bde03df3dfbd9"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)