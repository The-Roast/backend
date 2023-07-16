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

newsletter_article = db.Table(
    "newsletter_article",
    ss.Column("newsletter", ss.ForeignKey("newsletters.uuid"), primary_key = True),
    ss.Column("article", ss.ForeignKey("articles.uuid"), primary_key = True)
)

class Users(db.Model): # checked

    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    uuid = ss.Column("uuid", st.UUID(as_uuid = True), primary_key = True, index = True, default = uuid.uuid4)

    digests = db.relationship("Digests", back_populates = "user", cascade = "all, delete, delete-orphan")

    first_name = ss.Column("first_name", st.String, nullable = False)
    last_name = ss.Column("last_name", st.String, nullable = False)
    email = ss.Column("email", st.String, unique = True, index = True, nullable = False)
    password = ss.Column("password", st.String, nullable = False)

    created_at = ss.Column("created_at", st.DateTime, nullable = False, default = datetime.datetime.utcnow)
    updated_at = ss.Column("updated_at", st.DateTime, nullable = False, default = datetime.datetime.utcnow, onupdate = datetime.datetime.utcnow)
    deleted_at = ss.Column("deleted_at", st.DateTime)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf-8')
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def as_dict(self):
        return {
            "uuid": self.uuid,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }

class Digests(db.Model): # checked

    __tablename__ = "digests"
    __table_args__ = {"extend_existing": True}

    uuid = ss.Column("uuid", st.UUID(as_uuid = True), primary_key = True, index = True, default = uuid.uuid4)

    user = db.relationship("Users", back_populates = "digests")
    user_uuid = ss.Column("user_uuid", st.UUID(as_uuid = True), ss.ForeignKey("users.uuid"))
    
    newsletters = db.relationship("Newsletters", back_populates = "digest")

    name = ss.Column("name", st.String)
    settings = ss.Column(
        "settings",
        NestedMutableJson, nullable = False,
        default = create_settings
    )
    color = ss.Column("color", st.String(7), nullable = False, default = create_color)

    created_at = ss.Column("created_at", st.DateTime, nullable = False, default = datetime.datetime.utcnow)
    updated_at = ss.Column("updated_at", st.DateTime, nullable = False, default = datetime.datetime.utcnow, onupdate = datetime.datetime.utcnow)
    deleted_at = ss.Column("deleted_at", st.DateTime)

    def as_dict(self):
        return {
            "uuid": self.uuid,
            "user": self.user_uuid,
            "name": self.name,
            "sources": dict(self.settings)["sources"],
            "interests": dict(self.settings)["interests"],
            "personality": dict(self.settings)["personality"],
            "color": self.color
        }

class Newsletters(db.Model):

    __tablename__ = "newsletters"
    __table_args__ = {"extend_existing": True}

    uuid = ss.Column("uuid", st.UUID(as_uuid = True), primary_key = True, index = True, default = uuid.uuid4)

    articles = db.relationship("Articles", secondary = newsletter_article, back_populates = "newsletters")
    
    digest = db.relationship("Digests", back_populates = "newsletters")
    digest_uuid = ss.Column("digest_uuid", st.UUID(as_uuid = True), ss.ForeignKey("digests.uuid", ondelete = "SET NULL"), nullable = True)

    # cover = ss.Column("cover", st.BLOB)
    data = ss.Column("data", NestedMutableJson, nullable = False)
    # html = ss.Column("html", st.String, nullable = False)

    created_at = ss.Column("created_at", st.DateTime, nullable = False, default = datetime.datetime.utcnow)

    def as_dict(self, exclude_data = True):
        d = {
            "uuid": self.uuid,
            "created_at": self.created_at
        }
        if not exclude_data:
            d["data"] = dict(self.data)
        return d

class Articles(db.Model):

    __tablename__ = "articles"
    __table_args__ = {"extend_existing": True}

    uuid = ss.Column("uuid", st.UUID(as_uuid = True), primary_key = True, index = True, default = uuid.uuid4)

    newsletters = db.relationship("Newsletters", secondary = newsletter_article, back_populates = "articles")

    source = ss.Column("source", st.String, index = True)
    author = ss.Column("author", st.String, index = True)
    title = ss.Column("title", st.String)
    content = ss.Column("content", st.String, nullable = False)
    url = ss.Column("url", st.String, index = True, nullable = False)

    published_at = ss.Column("published_at", st.DateTime, nullable = False)
    created_at = ss.Column("created_at", st.DateTime, nullable = False, default = datetime.datetime.utcnow)

    def as_dict(self):
        return {
            "uuid": self.uuid,
            "source": self.source,
            "author": self.author,
            "title": self.title,
            "content": self.content,
            "url": self.url,
            "published_at": self.published_at
        }