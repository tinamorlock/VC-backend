from pydantic import BaseModel, EmailStr

# schema for user registration

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    phone: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

class ProjectCreate(BaseModel):
    name: str
    title: str
    description: str
    isPublic: bool