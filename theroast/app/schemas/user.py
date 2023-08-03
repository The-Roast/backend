from typing import Optional
from pydantic import BaseModel, UUID4, EmailStr, ConfigDict

class UserBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    is_active: Optional[bool] = True
    is_superuser: bool = False

class UserCreate(UserBase):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase):
    uuid: UUID4
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        orm_mode = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    password: str