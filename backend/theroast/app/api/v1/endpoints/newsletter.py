from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from pydantic import EmailStr
from uuid import UUID
from http import HTTPStatus

from theroast.config import server_config
from theroast.app import schemas, deps
from theroast.db import base, crud

router = APIRouter()

@router.get("/", response_model=List[schemas.Newsletter])
def read_newsletters(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = Body(None),
    limit: int = Body(None),
    current_user: base.User = Depends(deps.get_current_active_user)
) -> Any:
    newsletters = crud.newsletter.get_multi_by_digest__clicks(db, user_uuid=current_user.uuid, skip=skip, limit=limit)
    return newsletters

@router.get("/{uuid}", response_model=schemas.Newsletter)
def read_newsletter(
    *,
    db: Session = Depends(deps.get_db),
    uuid: UUID,
    current_user: base.User = Depends(deps.get_current_active_user)
) -> Any:
    newsletter = crud.newsletter.get(db, uuid=uuid)
    if not newsletter:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Newsletter not found."
        )
    if not crud.user.is_superuser(current_user) and newsletter.user_uuid != current_user.uuid:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="User does not have enough priviledges and does not own newsletter."
        )
    return newsletter

@router.post("/", response_model=schemas.Newsletter)
def create_newsletter(
    *,
    db: Session = Depends(deps.get_db),
    newsletter_in: schemas.NewsletterCreate,
    current_user: base.User = Depends(deps.get_current_active_user)
) -> Any:
    newsletter = crud.newsletter.create_with_owner(db, obj_in=newsletter_in, user_uuid=current_user.uuid)
    return newsletter

@router.put("/{uuid}", response_model=schemas.Newsletter)
def update_newsletter(
    *,
    db: Session = Depends(deps.get_db),
    uuid: UUID,
    newsletter_in: schemas.NewsletterUpdate,
    current_user: base.User = Depends(deps.get_current_active_user)
) -> Any:
    newsletter = crud.newsletter.get(db, uuid=uuid)
    if not newsletter:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Newsletter not found."
        )
    if not crud.user.is_superuser(current_user) and newsletter.user_uuid != current_user.uuid:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="User does not have enough priviledges and does not own newsletter."
        )
    newsletter = crud.newsletter.update(db, db_obj=newsletter, obj_in=newsletter_in)
    return newsletter

@router.delete("/{uuid}", response_model=schemas.Newsletter)
def delete_newsletter(
    *,
    db: Session = Depends(deps.get_db),
    uuid: UUID,
    current_user: base.User = Depends(deps.get_current_active_user)
) -> Any:
    newsletter = crud.newsletter.get(db, uuid=uuid)
    if not newsletter:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Newsletter not found."
        )
    if not crud.user.is_superuser(current_user) and newsletter.user_uuid != current_user.uuid:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="User does not have enough priviledges and does not own newsletter."
        )
    newsletter = crud.newsletter.remove(db, uuid=uuid)
    return newsletter
