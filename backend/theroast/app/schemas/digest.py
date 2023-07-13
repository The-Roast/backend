from typing import Optional, Dict
from pydantic import BaseModel, UUID4, EmailStr, ConfigDict, Json

class SettingsModel(BaseModel):
    interests: list
    sources: list
    personality: str

class DigestBase(BaseModel):
    name: Optional[str] = None
    settings: Optional[Dict[str, SettingsModel]] = None
    color: Optional[str] = None
    is_enabled: Optional[bool] = True

class DigestCreate(DigestBase):
    user: UUID4
    name: str
    settings: Dict[str, SettingsModel]
    color: str

class DigestUpdate(DigestBase):
    uuid: UUID4
    user: UUID4

class DigestInDBBase(DigestBase):
    model_config = ConfigDict(from_attributes=True)
    uuid: UUID4
    user: UUID4

class Digest(DigestInDBBase):
    name: str