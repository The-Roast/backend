from typing import TYPE_CHECKING, Optional, List

import sqlalchemy as sa
import sqlalchemy.orm as so
import sqlalchemy.schema as ss
import sqlalchemy.types as st
from sqlalchemy_json import NestedMutableJson

from theroast.db.base import Base
from uuid import uuid4
from datetime import datetime

newsletter_article = sa.Table(
    "newsletter_article",
    Base,
    ss.Column("newsletter", ss.ForeignKey("newsletters.uuid"), primary_key = True),
    ss.Column("article", ss.ForeignKey("articles.uuid"), primary_key = True)
)
