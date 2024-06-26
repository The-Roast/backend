from typing import Optional, List
from pydantic import BaseModel, UUID4
from datetime import datetime

class SectionModel(BaseModel):
    title: str
    body: str

class NewsletterBase(BaseModel):
    pass

class NewsletterCreate(NewsletterBase):
    digest_uuid: UUID4

class NewsletterUpdate(NewsletterBase):
    uuid: UUID4
    clicks: Optional[int]
    title: Optional[str]
    introduction: Optional[str]
    body: Optional[List[SectionModel]]
    conclusion: Optional[str]
    html: Optional[str]

class NewsletterInDBBase(NewsletterBase):
    uuid: UUID4
    digest_uuid: UUID4
    title: Optional[str]
    introduction: Optional[str]
    body: Optional[List[SectionModel]]
    conclusion: Optional[str]
    html: Optional[str]
    
    class Config:
        orm_mode = True

class Newsletter(NewsletterInDBBase):
    pass

class NewsletterInDB(NewsletterInDBBase):
    clicks: int
    created_at: datetime
    updated_at: datetime