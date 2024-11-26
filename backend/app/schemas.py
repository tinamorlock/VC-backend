from typing import Optional, List
from datetime import datetime
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

class FileBase(BaseModel):
    filename: str
    file_path: str
    file_size: int
    file_type: str

class FileCreate(BaseModel):
    filename: str
    file_size: int
    file_type: str
    document_id: int  # Associated document

class FileResponse(FileBase):
    id: int
    document_id: int

    class Config:
        orm_mode = True

class CommentBase(BaseModel):
    content: str
    file_id: int
    parent_id: Optional[int] = None  # Optional for nested replies

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    replies: List["Comment"]

    # Initialize replies in the constructor
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.replies is None:
            self.replies = []  # Initialize replies as an empty list if None

    class Config:
        orm_mode = True  # Tells Pydantic to treat data as if it's an SQLAlchemy model instance

# Update forward references for the nested "Comment" class (needed for circular references)
Comment.model_rebuild()