from email.policy import default
import sqlalchemy as sa
import sqlalchemy.orm as so
import sqlalchemy.schema as ss
import sqlalchemy.types as st
from sqlalchemy_json import NestedMutableJson
from flask_bcrypt import generate_password_hash, check_password_hash
from ...extensions import db
import datetime
import uuid
import random

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

class Users(db.Model):

    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = ss.Column("uuid", st.UUID(as_uuid = True), primary_key = True, index = True, default = uuid.uuid4)

    digests = db.relationship("Digests")

    first_name = ss.Column("first_name", st.String, unique = False, nullable = False)
    last_name = ss.Column("last_name", st.String, unique = False, nullable = False)
    email = ss.Column("email", st.String, unique = True, index = True, nullable = False)
    password = ss.Column("password", st.String, unique = False, nullable = False)

    created_at = ss.Column("created_at", st.DateTime, unique = False, nullable = False, default = datetime.datetime.utcnow)
    updated_at = ss.Column("updated_at", st.DateTime, unique = False, nullable = False, default = datetime.datetime.utcnow, onupdate = datetime.datetime.utcnow)
    deleted_at = ss.Column("deleted_at", st.DateTime, unique = False, nullable = True)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf-8')
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def as_dict(self):
        return {
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
        }

class Digests(db.Model):

    __tablename__ = "digests"
    __table_args__ = {"extend_existing": True}

    uuid = ss.Column("uuid", st.UUID(as_uuid = True), primary_key = True, index = True, default = uuid.uuid4)

    name = ss.Column("name", st.String, unique = False, nullable = True)
    settings = ss.Column(
        "settings",
        NestedMutableJson, unique = False, nullable = False,
        default = create_settings
    )
    color = ss.Column("color", st.String(7), unique = False, nullable = False, default = create_color)

    created_at = ss.Column("created_at", st.DateTime, unique = False, nullable = False, default = datetime.datetime.utcnow)
    updated_at = ss.Column("updated_at", st.DateTime, unique = False, nullable = False, default = datetime.datetime.utcnow, onupdate = datetime.datetime.utcnow)
    deleted_at = ss.Column("deleted_at", st.DateTime, unique = False, nullable = True)

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

class Newsletter(db.Model):

    __tablename__ = "newsletters"
    __table_args__ = {"extend_existing": True}

    uuid = ss.Column("uuid", st.UUID(as_uuid = True), primary_key = True, index = True, default = uuid.uuid4)

    data = ss.Column("data", NestedMutableJson, unique = False, nullable = False)
    articles = db.relationship("Articles")

    created_at = ss.Column("created_at", st.DateTime, unique = False, nullable = False, default = datetime.datetime.utcnow)