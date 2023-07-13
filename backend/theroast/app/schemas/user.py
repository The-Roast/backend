from typing import Optional
from pydantic import BaseModel, UUID4, EmailStr, ConfigDict

class UserBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False

class UserCreate(UserBase):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class UserUpdate(UserBase):
    uuid: UUID4
    password: Optional[str] = None

class UserInDBBase(UserBase):
    model_config = ConfigDict(from_attributes=True)
    uuid: UUID4

class User(UserInDBBase):
    email: EmailStr

class UserInDB(UserInDBBase):
    email: EmailStr
    password: str