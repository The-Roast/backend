from typing import Optional, List

from uuid import uuid4
from datetime import datetime
import sqlalchemy.orm as so
import sqlalchemy.schema as ss
import sqlalchemy.types as st
from sqlalchemy_json import NestedMutableJson

from theroast.db.base_class import Base

class Newsletter(Base):

    '''Table definition for Newsletter'''

    __tablename__ = "newsletter"

    uuid: so.Mapped[st.UUID] = so.mapped_column("uuid", primary_key=True, index=True, default=uuid4)

    articles: so.Mapped[List["Article"]] = so.relationship(secondary="newsletter_article", back_populates="newsletters")
    
    digest: so.Mapped[List["Digest"]] = so.relationship(back_populates = "newsletters")
    digest_uuid: so.Mapped[Optional[st.UUID]] = ss.Column("digest_uuid", ss.ForeignKey("digest.uuid", ondelete = "SET NULL"))

    data: so.Mapped[NestedMutableJson] = so.mapped_column("data")
    html: so.Mapped[Optional[str]] = so.mapped_column("html")

    created_at: so.Mapped[st.DateTime] = so.mapped_column("created_at", default=datetime.utcnow)
