from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr
from uuid import UUID
from http import HTTPStatus

from theroast.config import server_config
from theroast.app import schemas, deps
from theroast.db import base, crud
from theroast.core.email import send_new_account_email

router = APIRouter()

@router.get("/{uuid}", response_model=schemas.User)
async def read_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    uuid: UUID,
    current_user: base.User = Depends(deps.get_current_active_superuser)
) -> Any:
    user = await crud.user.get(db, uuid=uuid)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found."
        )
    return user

@router.post("/", response_model=schemas.User)
async def create_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    current_user: base.User = Depends(deps.get_current_active_superuser)
) -> Any:
    user = await crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Email already in use."
        )
    if server_config.EMAILS_ENABLED and user_in.email:
        send_new_account_email(
            email_to=user_in.email,
            first_name=user_in.first_name,
            username=user_in.email,
            password=user_in.password
        )
    user = await crud.user.create(db, obj_in=user_in)
    return user

@router.put("/{uuid}", response_model=schemas.User)
async def update_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    uuid: UUID,
    user_in: schemas.UserUpdate,
    current_user: base.User = Depends(deps.get_current_active_superuser)
) -> Any:
    user = await crud.user.get(db, uuid=uuid)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found."
        )
    user = await crud.user.update(db, db_obj=user, obj_in=user_in)
    return user

@router.delete("/{uuid}", response_model=schemas.User)
async def delete_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    uuid: UUID,
    current_user: base.User = Depends(deps.get_current_active_superuser)
) -> Any:
    user = await crud.user.get(db, uuid=uuid)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found."
        )
    user = await crud.user.remove(db, uuid=uuid)
    return user

@router.get("/public/current", response_model=schemas.User)
async def read_current_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    current_user: base.User = Depends(deps.get_current_active_user)
) -> Any:
    return current_user

@router.put("/public/current", response_model=schemas.User)
async def update_current_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    first_name: str = Body(None),
    last_name: str = Body(None),
    email: EmailStr = Body(None),
    password: str = Body(None),
    current_user: base.User = Depends(deps.get_current_active_user)
) -> Any:
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if first_name is not None: user_in.first_name = first_name
    if last_name is not None: user_in.last_name = last_name
    if password is not None: user_in.password = password
    if email is not None: user_in.email = email
    user = await crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user