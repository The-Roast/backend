import sqlalchemy as sa
import sqlalchemy.orm as so
import sqlalchemy.schema as ss
import sqlalchemy.types as st
from sqlalchemy_json import NestedMutableJson
from flask_login import UserMixin
from ...extensions import db

def create_sources():

    return {
        "topics": [],
        "traditional": [],
        "non-traditional": []
    }

class Users(db.Model, UserMixin):

    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = ss.Column("id", st.Integer, primary_key = True)

    email = ss.Column("email", st.String, unique = True, nullable = False)
    password = ss.Column("password", st.String, unique = False, nullable = False)

class Digests(db.Model):

    __tablename__ = "digests"
    __table_args__ = {"extend_existing": True}

    id = ss.Column("id", st.Integer, primary_key = True)

    name = ss.Column("name", st.String, unique = True, nullable = False)
    sources = ss.Column(
        "sources",
        NestedMutableJson, unique = False, nullable = False,
        default = create_sources
    )
    color = ss.Column("color", st.String(7), unique = False, nullable = False)


user_digest = db.Table(
    "user_digest",
    ss.Column("user", ss.ForeignKey("users.id"), primary_key = True),
    ss.Column("digest", ss.ForeignKey("digests.id"), primary_key = True)
)
