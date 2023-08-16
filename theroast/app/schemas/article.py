from typing import Optional, List
from pydantic import BaseModel, UUID4, HttpUrl
from datetime import datetime

class ArticleBase(BaseModel):
    source: Optional[str]
    authors: Optional[List[str]]
    title: Optional[str]
    content: Optional[str]
    keywords: Optional[List[str]]
    url: Optional[HttpUrl]
    published_at: Optional[datetime]

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(ArticleBase):
    pass

class ArticleInDBBase(BaseModel):
    uuid: UUID4

    class Config:
        orm_mode = True

class Article(ArticleInDBBase):
    pass

class ArticleInDB(ArticleInDBBase):
    created_at: datetime