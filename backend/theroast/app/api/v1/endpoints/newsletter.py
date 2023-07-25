from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from pydantic import EmailStr
from uuid import UUID
from http import HTTPStatus
from enum import Enum

from theroast.config import server_config
from theroast.app import schemas, deps
from theroast.db import base, crud
from theroast.lib import pipeline

router = APIRouter()

class ORDER_BY(str, Enum):
    DATE = "date"
    USAGE = "usage"

@router.get("/all", response_model=List[schemas.Newsletter])
def read_newsletters(
    *,
    db: Session = Depends(deps.get_db),
    digest_uuid: UUID,
    order_by: ORDER_BY,
    skip: int = Body(None),
    limit: int = Body(None),
    current_user: base.User = Depends(deps.get_current_active_user)
) -> Any:
    digest = crud.digest.get(db, uuid=digest_uuid)
    if not digest:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Digest not found."
        )
    if not crud.user.is_superuser and digest.uuid != current_user.uuid:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="User does not have enough priviledges and does not own newsletter."
        )
    _get_multi = crud.newsletter.get_multi_by_digest__clicks
    if order_by is ORDER_BY.DATE:
        _get_multi = crud.newsletter.get_multi_by_digest__date
    newsletters = _get_multi(db, digest_uuid=digest_uuid, skip=skip, limit=limit)
    return newsletters

@router.get("/{uuid}", response_model=schemas.Newsletter)
def read_newsletter(
    *,
    db: Session = Depends(deps.get_db),
    uuid: UUID,
    current_user: base.User = Depends(deps.get_current_active_user)
) -> Any:
    newsletter = crud.newsletter.get(db, uuid=uuid)
    digest: base.Digest = newsletter.digest
    if not newsletter:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Newsletter not found."
        )
    if not crud.user.is_superuser(current_user) and digest.user_uuid != current_user.uuid:
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
    digest = crud.digest.get(db, uuid=newsletter_in.digest_uuid)
    if not digest:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Digest not found."
        )
    if not crud.user.is_superuser(current_user) and digest.user_uuid != current_user.uuid:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="User does not have enough priviledges and does not own digest."
        )
    sections, structure = pipeline.generate_newsletter(digest)
    newsletter_data = pipeline.restructure(sections, structure)
    newsletter = crud.newsletter.create_with_data(db, obj_in=newsletter_in, data=newsletter_data)
    return newsletter

@router.put("/{uuid}", response_model=schemas.Newsletter)
def update_newsletter(
    *,
    db: Session = Depends(deps.get_db),
    uuid: UUID,
    newsletter_in: schemas.NewsletterUpdate,
    current_user: base.User = Depends(deps.get_current_active_user)
) -> Any:
    newsletter = crud.newsletter.get(db, uuid=newsletter_in.uuid)
    digest: base.Digest = newsletter.digest
    if not newsletter:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Newsletter not found."
        )
    if not crud.user.is_superuser(current_user) and digest.user_uuid != current_user.uuid:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="User does not have enough priviledges and does not own newsletter."
        )
    sections, structure = pipeline.generate_newsletter(digest)
    newsletter_data = pipeline.restructure(sections, structure)
    newsletter = crud.newsletter.create_with_data(db, obj_in=newsletter_in, data=newsletter_data)
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
