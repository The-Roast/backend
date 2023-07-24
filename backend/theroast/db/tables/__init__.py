import sqlalchemy as sa
import sqlalchemy.schema as ss

from theroast.db.base_class import Base

newsletter_article = sa.Table(
    "newsletter_article",
    Base.metadata,
    ss.Column("newsletter", ss.ForeignKey("newsletter.uuid"), primary_key = True),
    ss.Column("article", ss.ForeignKey("article.uuid"), primary_key = True)
)
