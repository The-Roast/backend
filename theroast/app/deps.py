from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from theroast.db import crud, base
from theroast.app import schemas
from theroast.core import security
from theroast.config import server_config
from theroast.db.session import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{server_config.AUTH_STR}/login/access-token"
)

async def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


async def get_current_user(
    db: AsyncSession = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> base.User:
    try:
        payload = jwt.decode(
            token, server_config.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        print(payload)
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await crud.user.get(db, uuid=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_current_active_user(
    current_user: base.User = Depends(get_current_user),
) -> base.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_current_active_superuser(
    current_user: base.User = Depends(get_current_user),
) -> base.User:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user