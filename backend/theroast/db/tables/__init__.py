import sqlalchemy as sa
import sqlalchemy.schema as ss

from theroast.db.base_class import Base
from theroast.db.tables.user import User
from theroast.db.tables.digest import Digest
from theroast.db.tables.newsletter import Newsletter
from theroast.db.tables.article import Article

BLANK = ""

newsletter_article = sa.Table(
    "newsletter_article",
    Base.metadata,
    ss.Column("newsletter", ss.ForeignKey("newsletter.uuid"), primary_key = True),
    ss.Column("article", ss.ForeignKey("article.uuid"), primary_key = True)
)
