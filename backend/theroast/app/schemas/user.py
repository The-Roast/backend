from typing import Optional
from pydantic import BaseModel, UUID4, EmailStr, ConfigDict

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr]
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False

class UserCreate(UserBase):
    email: EmailStr
    password: str

class UserUpdate(UserBase):
    uuid: UUID4
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class UserInDBBase(UserBase):
    model_config = ConfigDict(from_attributes = True)
    uuid: UUID4

class User(UserInDBBase):
    email: EmailStr

class UserInDB(UserInDBBase):
    email: EmailStr
    password: str