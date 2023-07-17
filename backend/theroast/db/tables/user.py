from typing import Optional, List

from uuid import uuid4
from datetime import datetime
import sqlalchemy.orm as so
import sqlalchemy.types as st

from theroast.db.base_class import Base

class User(Base):

    '''Table definition for User'''

    __tablename__ = "user"

    uuid: so.Mapped[st.UUID] = so.mapped_column("uuid", primary_key=True, index=True, default=uuid4)

    digests: so.Mapped[List["Digest"]] = so.relationship(back_populates="user", cascade = "all, delete, delete-orphan")

    first_name: so.Mapped[str] = so.mapped_column("first_name")
    last_name: so.Mapped[str] = so.mapped_column("last_name")
    email: so.Mapped[str] = so.mapped_column("email", unique=True, index=True)
    password: so.Mapped[str] = so.mapped_column("password")

    is_active: so.Mapped[bool] = so.mapped_column("is_active", default=True)
    is_superuser: so.Mapped[bool] = so.mapped_column("is_superuser", default=False)

    created_at: so.Mapped[datetime] = so.mapped_column("created_at", default=datetime.utcnow)
    updated_at: so.Mapped[datetime] = so.mapped_column("updated_at", default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at: so.Mapped[Optional[datetime]] = so.mapped_column("deleted_at")
