from sqlalchemy.orm import Session

# from theroast.db import crud, tables
# from theroast.config import server_config
# from theroast.db import base

# # make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# # otherwise, SQL Alchemy might fail to initialize relationships properly
# # for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


# def init_db(db: Session) -> None:

#     '''Method for initializing DB'''

#     user = crud.user.get_by_email(db, email=server_config.FIRST_SUPERUSER)
#     if not user:
#         user_in = schemas.UserCreate(
#             email=server_config.FIRST_SUPERUSER,
#             password=server_config.FIRST_SUPERUSER_PASSWORD,
#             is_superuser=True,
#         )
#         user = crud.user.create(db, obj_in=user_in)  # noqa: F841