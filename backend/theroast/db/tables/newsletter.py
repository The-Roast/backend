from typing import Optional, List
from uuid import uuid4, UUID
from datetime import datetime

import sqlalchemy.orm as so
import sqlalchemy.schema as ss
import sqlalchemy.types as st
from sqlalchemy_json import NestedMutableJson
from sqlalchemy.dialects.postgresql import ARRAY

from theroast.db.base_class import Base
from theroast.db.tables import BLANK

class Newsletter(Base):

    '''Table definition for Newsletter'''

    __tablename__ = "newsletter"

    uuid: so.Mapped[UUID] = so.mapped_column("uuid", primary_key=True, index=True, default=uuid4)

    digest: so.Mapped["Digest"] = so.relationship(back_populates = "newsletters")
    digest_uuid: so.Mapped[Optional[UUID]] = so.mapped_column("digest_uuid", ss.ForeignKey("digest.uuid", ondelete = "SET NULL"))
    articles: so.Mapped[List["Article"]] = so.relationship(secondary="newsletter_article", back_populates="newsletters")

    clicks: so.Mapped[int] = so.mapped_column("clicks", default=0)
    title: so.Mapped[Optional[str]] = so.mapped_column("title")
    introduction: so.Mapped[Optional[str]] = so.mapped_column("introduction")
    body: so.Mapped[Optional[ARRAY(NestedMutableJson)]] = so.mapped_column("body")
    conclusion: so.Mapped[Optional[str]] = so.mapped_column("conclusion")
    html: so.Mapped[Optional[str]] = so.mapped_column("html")

    created_at: so.Mapped[datetime] = so.mapped_column("created_at", default=datetime.utcnow)
    updated_at: so.Mapped[datetime] = so.mapped_column("updated_at", default=datetime.utcnow, onupdate=datetime.utcnow)
