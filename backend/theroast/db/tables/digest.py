from typing import Optional, List
from uuid import uuid4, UUID
from datetime import datetime
import random

import sqlalchemy.orm as so
import sqlalchemy.schema as ss
import sqlalchemy.types as st
from sqlalchemy.dialects.postgresql import ARRAY

from theroast.db.base_class import Base

def create_color(color=None):

    '''Default function for randomly creating hex color'''

    if color:
        return color

    color = random.randrange(0, 2 ** 24)
    color = hex(color)
    color = "#" + color[2:].zfill(6)

    return color

class Digest(Base):

    '''Table definition for Digest'''

    __tablename__ = "digest"

    uuid: so.Mapped[UUID] = so.mapped_column("uuid", primary_key=True, index=True, default=uuid4)

    user: so.Mapped["User"] = so.relationship(back_populates="digests")
    user_uuid: so.Mapped[UUID] = ss.Column("user_uuid", ss.ForeignKey("user.uuid"))
    newsletters: so.Mapped[List["Newsletter"]] = so.relationship(back_populates="digest")

    name: so.Mapped[str] = so.mapped_column("name", default=str)
    interests: so.Mapped[ARRAY(str)] = so.mapped_column("interests", default=list)
    sources: so.Mapped[ARRAY(str)] = so.mapped_column("sources", default=list)
    personality: so.Mapped[str] = so.mapped_column("personality", default=str)
    color: so.Mapped[st.String(7)] = so.mapped_column("color", default=create_color)

    is_enabled: so.Mapped[bool] = so.mapped_column("is_enabled", index=True, default=True)

    created_at: so.Mapped[datetime] = ss.Column("created_at", default=datetime.utcnow)
    updated_at: so.Mapped[datetime] = ss.Column("updated_at", default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at: so.Mapped[Optional[datetime]] = ss.Column("deleted_at")
