from typing import Optional, List
from uuid import uuid4
from datetime import datetime

import sqlalchemy.orm as so
import sqlalchemy.types as st
from sqlalchemy.dialects.postgresql import ARRAY

from theroast.db.base_class import Base

class Article(Base):

    '''Table definition for Article'''

    __tablename__ = "article"

    uuid: so.Mapped[st.UUID] = so.mapped_column("uuid", primary_key=True, index=True, default=uuid4)

    newsletters: so.Mapped[List["Newsletter"]] = so.relationship(secondary="newsletter_article", back_populates="articles")

    source: so.Mapped[Optional[str]] = so.mapped_column("source", index=True)
    authors: so.Mapped[Optional[ARRAY(str)]] = so.mapped_column("authors", index=True)
    title: so.Mapped[Optional[str]] = so.mapped_column("title")
    content: so.Mapped[str] = so.mapped_column("content")
    keywords: so.Mapped[Optional[ARRAY(str)]] = so.mapped_column("keywords", index=True)
    url: so.Mapped[str] = so.mapped_column("url", index=True)

    published_at: so.Mapped[datetime] = so.mapped_column("published_at")
    created_at: so.Mapped[datetime] = so.mapped_column("created_at", default = datetime.utcnow)