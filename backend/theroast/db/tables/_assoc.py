import sqlalchemy as sa
import sqlalchemy.schema as ss
import sqlalchemy.types as st

from theroast.db.base_class import Base

newsletter_article = sa.Table(
    "newsletter_article",
    Base.metadata,
    ss.Column("newsletter", st.UUID, ss.ForeignKey("newsletter.uuid")),
    ss.Column("article", st.UUID, ss.ForeignKey("article.uuid"))
)
