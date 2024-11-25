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

class Project(ProjectCreate):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class TokenData(BaseModel):
    sub: int