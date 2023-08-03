from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from http import HTTPStatus


from theroast.app import schemas, deps
from theroast.db import crud
from theroast.core import security
from theroast.config import server_config
from theroast.core.security import (
    get_password_hash,
    generate_password_reset_token,
    verify_password_reset_token
)
from theroast.core.email import send_reset_password_email

router = APIRouter()

@router.post("/register", response_model=schemas.User)
async def register_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
) -> Any:
    user = await crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Email already in use."
        )
    user = await crud.user.create(db, obj_in=user_in)
    return user

@router.post("/login/access-token", response_model=schemas.Token)
async def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = await crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Inactive user")
    access_token_expires = timedelta(minutes=server_config.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.uuid, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/password-recovery/{email}", response_model=schemas.Message)
async def recover_password(email: str, db: Session = Depends(deps.get_db)) -> Any:
    """
    Password Recovery
    """
    user = await crud.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    send_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    return {"message": "Password recovery email sent"}

@router.post("/reset-password/", response_model=schemas.Message)
async def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Reset password
    """
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid token")
    user = await crud.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    hashed_password = get_password_hash(new_password)
    user.password = hashed_password
    db.add(user)
    db.commit()
    return {"message": "Password updated successfully"}