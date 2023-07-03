from typing import TYPE_CHECKING, Optional, List

import sqlalchemy as sa
import sqlalchemy.orm as so
import sqlalchemy.schema as ss
import sqlalchemy.types as st
from sqlalchemy_json import NestedMutableJson

from theroast.db.base import Base
from uuid import uuid4
import datetime
import random

if TYPE_CHECKING:
    from .digest import Digest

def create_color(color=None):
    if color:
        return color

    color = random.randrange(0, 2 ** 24)
    color = hex(color)
    color = "#" + color[2:].zfill(6)

    return color

def create_settings():

    return {
        "interests": [],
        "sources": [],
        "personality": "normal"
    }

class Digest(Base):

    '''Table definition for Digest'''

    uuid: so.Mapped[st.UUID] = so.mapped_column("uuid", primary_key=True, index=True, default=uuid4)

    name: so.Mapped[str] = so.mapped_column("name")
    