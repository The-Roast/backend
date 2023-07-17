from typing import Optional, List
from uuid import uuid4
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

    uuid: so.Mapped[st.UUID] = so.mapped_column("uuid", primary_key=True, index=True, default=uuid4)

    digest: so.Mapped["Digest"] = so.relationship(back_populates = "newsletters")
    digest_uuid: so.Mapped[Optional[st.UUID]] = so.mapped_column("digest_uuid", ss.ForeignKey("digest.uuid", ondelete = "SET NULL"))
    articles: so.Mapped[List["Article"]] = so.relationship(secondary="newsletter_article", back_populates="newsletters")

    clicks: so.Mapped[st.Integer] = so.mapped_column("clicks", default=0)

    title: so.Mapped[str] = so.mapped_column("title", default=BLANK)
    introduction: so.Mapped[str] = so.mapped_column("introduction", default=BLANK)
    body: so.Mapped[ARRAY(NestedMutableJson)] = so.mapped_column("body", default=list)
    conclusion: so.Mapped[str] = so.mapped_column("conclusion", default=BLANK)
    html: so.Mapped[Optional[str]] = so.mapped_column("html")

    created_at: so.Mapped[st.DateTime] = so.mapped_column("created_at", default=datetime.utcnow)
