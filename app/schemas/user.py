from typing import Optional
from pydantic import BaseModel, EmailStr
from app.models.user import Role

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: Role = Role.viewer
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[Role] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: int

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass
