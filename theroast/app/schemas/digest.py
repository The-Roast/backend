from typing import Optional, List
from pydantic import BaseModel, UUID4, ConfigDict
from datetime import datetime

class DigestBase(BaseModel):
    user_uuid: Optional[UUID4]
    name: Optional[str]
    interests: Optional[List[str]]
    sources: Optional[List[str]]
    personality: Optional[str]
    color: Optional[str]
    is_enabled: Optional[bool] = True

class DigestCreate(DigestBase):
    pass

class DigestUpdate(DigestBase):
    pass

class DigestInDBBase(DigestBase):
    uuid: UUID4
    user_uuid: UUID4

    class Config:
        orm_mode = True

class Digest(DigestInDBBase):
    pass

class DigestInDB(DigestInDBBase):
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]