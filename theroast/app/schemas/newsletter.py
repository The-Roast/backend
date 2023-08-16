from typing import Optional, List
from pydantic import BaseModel, UUID4
from datetime import datetime

class SectionModel(BaseModel):
    title: str
    body: str

class Chat(BaseModel):
    type: Optional[str]
    content: Optional[str]

class NewsletterBase(BaseModel):
    pass

class NewsletterCreate(NewsletterBase):
    digest_uuid: UUID4

class NewsletterUpdate(NewsletterBase):
    pass

class NewsletterInDBBase(NewsletterBase):
    uuid: UUID4
    digest_uuid: UUID4
    clicks: Optional[int]
    chat: Optional[List[Chat]]
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
    created_at: datetime
    updated_at: datetime