from typing import Optional

from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    phone: str
    password: str

class User(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

class ProjectCreate(BaseModel):
    name: str
    title: str
    description: str
    is_public: bool

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None

    class Config:
        orm_mode = True

class Project(ProjectCreate):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class TokenData(BaseModel):
    sub: int

class DocumentCreate(BaseModel):
    name: str
    title: str
    description: str
    is_public: bool

class DocumentUpdate(BaseModel):
    name: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None

    class Config:
        orm_mode = True

class FollowCreate(BaseModel):
    following_id: int

class Follow(BaseModel):
    id: int
    follower_id: int
    following_id: int
    created_at: str

    class Config:
        orm_mode = True