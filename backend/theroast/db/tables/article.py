from typing import Optional, List
from uuid import uuid4, UUID
from datetime import datetime

import sqlalchemy.orm as so
from sqlalchemy.dialects.postgresql import ARRAY

from theroast.db.base_class import Base

class Article(Base):

    '''Table definition for Article'''

    __tablename__ = "article"

    uuid: so.Mapped[UUID] = so.mapped_column("uuid", primary_key=True, index=True, default=uuid4)

    newsletters: so.Mapped[List["Newsletter"]] = so.relationship(secondary="newsletter_article", back_populates="articles")

    source: so.Mapped[str] = so.mapped_column("source", index=True, default=str)
    authors: so.Mapped[ARRAY(str)] = so.mapped_column("authors", ARRAY(str), index=True, default=list)
    title: so.Mapped[str] = so.mapped_column("title", default=str)
    content: so.Mapped[str] = so.mapped_column("content", default=str)
    keywords: so.Mapped[ARRAY(str)] = so.mapped_column("keywords", ARRAY(str), index=True, default=list)
    url: so.Mapped[str] = so.mapped_column("url", index=True)

    published_at: so.Mapped[datetime] = so.mapped_column("published_at")
    created_at: so.Mapped[datetime] = so.mapped_column("created_at", default = datetime.utcnow)