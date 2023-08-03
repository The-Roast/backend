from sqlalchemy.orm import Session

from theroast.db import crud, base
from theroast.config import server_config
from theroast.app import schemas

# # make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# # otherwise, SQL Alchemy might fail to initialize relationships properly
# # for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


async def init_db(db: Session) -> None:

    '''Method for initializing DB'''

    user = await crud.user.get_by_email(db, email=server_config.FIRST_SUPERUSER_EMAIL)
    if not user:
        user_in = schemas.UserCreate(
            first_name=server_config.FIRST_SUPERUSER_FIRST_NAME,
            last_name=server_config.FIRST_SUPERUSER_LAST_NAME,
            email=server_config.FIRST_SUPERUSER_EMAIL,
            password=server_config.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = await crud.user.create(db, obj_in=user_in)  # noqa: F841