from typing import Optional, List

from uuid import uuid4
from datetime import datetime
import random
import sqlalchemy.orm as so
import sqlalchemy.schema as ss
import sqlalchemy.types as st
from sqlalchemy_json import NestedMutableJson

from theroast.db.base_class import Base

def create_color(color=None):

    '''Default function for randomly creating hex color'''

    if color:
        return color

    color = random.randrange(0, 2 ** 24)
    color = hex(color)
    color = "#" + color[2:].zfill(6)

    return color

def create_settings():

    '''Default function for creating settings JSON'''

    return {
        "interests": [],
        "sources": [],
        "personality": "normal"
    }

class Digest(Base):

    '''Table definition for Digest'''

    __tablename__ = "digest"

    uuid: so.Mapped[st.UUID] = so.mapped_column("uuid", primary_key=True, index=True, default=uuid4)

    newsletters: so.Mapped[List["Newsletter"]] = so.relationship()

    name: so.Mapped[str] = so.mapped_column("name")
    settings: so.Mapped[NestedMutableJson] = so.mapped_column("settings", default=create_settings)
    color: so.Mapped[st.String(7)] = so.mapped_column("color", default=create_color)

    is_enabled: so.Mapped[bool] = so.mapped_column("is_enabled", index=True, default=True)

    created_at: so.Mapped[datetime] = ss.Column("created_at", default=datetime.utcnow)
    updated_at: so.Mapped[datetime] = ss.Column("updated_at", default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at: so.Mapped[Optional[datetime]] = ss.Column("deleted_at")
