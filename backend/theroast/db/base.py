# Import all the models, so that Base has them before being
# imported by Alembic
from theroast.db.base_class import Base
from theroast.db.tables._assoc import newsletter_article
from theroast.db.tables.user import User
from theroast.db.tables.digest import Digest
from theroast.db.tables.newsletter import Newsletter
from theroast.db.tables.article import Article