from typing import TYPE_CHECKING, Optional, List

import sqlalchemy as sa
import sqlalchemy.orm as so
import sqlalchemy.schema as ss
import sqlalchemy.types as st
from sqlalchemy_json import NestedMutableJson

from theroast.db.base import Base
from uuid import uuid4
from datetime import datetime

if TYPE_CHECKING:
    from . import newsletter_article

class Article(Base):

    '''Table definition for Article'''

    __tablename__ = "article"

    uuid: so.Mapped[st.UUID] = so.mapped_column("uuid", primary_key=True, index=True, default=uuid4)

    newsletters: so.Mapped[List["Newsletter"]] = so.relationship(secondary=newsletter_article, back_populates="articles")

    source: so.Mapped[Optional[str]] = so.mapped_column("source", index=True)
    author: so.Mapped[Optional[str]] = so.mapped_column("author", index=True)
    title: so.Mapped[Optional[str]] = so.mapped_column("title")
    content: so.Mapped[str] = so.mapped_column("content")
    url: so.Mapped[str] = so.mapped_column("url", index=True)

    published_at: so.Mapped[datetime] = so.mapped_column("published_at")
    created_at: so.Mapped[datetime] = so.mapped_column("created_at", default = datetime.utcnow)