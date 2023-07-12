# Import all the models, so that Base has them before being
# imported by Alembic
from theroast.db.base_class import Base  # noqa
from theroast.db.tables import (
    Digest,
    User,
    Newsletter,
    Article
)