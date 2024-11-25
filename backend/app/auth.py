from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from starlette import status
from . import models, database
from . schemas import TokenData


SECRET_KEY = "ba0d6c9136cfe3f10a7ce9bddd1aedcf0e2976f05aa514f947d4143fab1cfdc9e8fe3e01d55e1927ccafcf618b98272b1b3e0d2539b0cd0584c31ac9a43b47c48f75e557c10b1186c141f3f973514106ac1c409c8539524c2c2862737b2a145a4d62d23c399bf9b90071bc8c133f628fee7fe0916bfee384d21969ab14b4c08b7bb845e4852cf381c581a9b5b44fd451d1f1eb937082a93ca30a34a1f6476f5d9b897ac5cc9ef43e06086c49acd4f24ae1f046d9bc5e67a266a89c8b5ad6c80ae6d593dc0bd9450f3afe048cadf90559026a08945e3485c3153e697d756dc9fb9374a38310d54b7621d50f49eb832c01bba4ec5788d94cc23f8bde03df3dfbd9"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    """
    Get the current user logged in by decoding the JWT token.
    """
    user = get_user_by_token(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    return user

def get_user_by_token(db: Session, token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenData(**payload)
        user=db.query(models.User).filter(models.User.id == token_data.sub).first()
        return user
    except (JWTError, ValueError):
        return None

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)