from typing import Optional, List
from pydantic import BaseModel, UUID4, ConfigDict
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

class NewsletterInDBBase(NewsletterBase):
    model_config = ConfigDict(from_attributes=True)
    uuid: UUID4
    digest_uuid: UUID4
    clicks: Optional[int]
    title: Optional[str]
    introduction: Optional[str]
    body: Optional[List[SectionModel]]
    conclusion: Optional[str]
    html: Optional[str]

class Newsletter(NewsletterInDBBase):
    pass

class Newsletters(BaseModel):
    newsletters: List[Newsletter]

class NewsletterInDB(NewsletterInDBBase):
    created_at: datetime
    updated_at: datetime