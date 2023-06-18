import sqlalchemy as sa
import sqlalchemy.orm as so
import sqlalchemy.schema as ss
import sqlalchemy.types as st
from sqlalchemy_json import NestedMutableJson
from flask_login import UserMixin
from ...extensions import db
import uuid
import random

def create_color(color = None):
    
    if color:
        return color
    
    color = random.randrange(0, 2**24)
    color = hex(color)
    color = "#" + color[2:]
    
    return color

def create_settings():

    return {
        "interests": [],
        "sources": [],
        "personality": "normal"
    }

user_digest = db.Table(
    "user_digest",
    ss.Column("user", ss.ForeignKey("users.id"), primary_key = True),
    ss.Column("digest", ss.ForeignKey("digests.id"), primary_key = True)
)

class Users(db.Model, UserMixin):

    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = ss.Column("id", st.Integer, primary_key = True)

    digests = db.relationship("Digests", secondary = user_digest)

    first_name = ss.Column("first_name", st.String, unique = False, nullable = True)
    last_name = ss.Column("last_name", st.String, unique = False, nullable = True)
    email = ss.Column("email", st.String, unique = True, nullable = False)
    password = ss.Column("password", st.String, unique = False, nullable = True)

    def as_dict(self):
        return {
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
        }

class Digests(db.Model):

    __tablename__ = "digests"
    __table_args__ = {"extend_existing": True}

    id = ss.Column("id", st.Integer, primary_key = True)

    uuid = ss.Column("uuid", st.UUID(as_uuid = True), unique = True, nullable = False, default = uuid.uuid4)
    name = ss.Column("name", st.String, unique = False, nullable = True)
    settings = ss.Column(
        "settings",
        NestedMutableJson, unique = False, nullable = False,
        default = create_settings
    )
    color = ss.Column("color", st.String(7), unique = False, nullable = False, default = create_color)

    def as_dict(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "contentSources": dict(self.settings)["sources"],
            "interests": dict(self.settings)["interests"],
            "personality": dict(self.settings)["personality"],
            "color": {
                "hex": self.color
            }
        }