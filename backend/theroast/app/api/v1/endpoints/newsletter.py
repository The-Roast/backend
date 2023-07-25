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

@router.get("/", response_model=List[schemas.Digest])
def read_digests(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = Body(None),
    limit: int = Body(None),
    current_user: base.User = Depends(deps.get_current_active_user)
) -> Any:
    digests = crud.digest.get_multi_by_owner(db, user_uuid=current_user.uuid, skip=skip, limit=limit)
    return digests

@router.get("/{uuid}", response_model=schemas.Digest)
def read_digest(
    *,
    db: Session = Depends(deps.get_db),
    uuid: UUID,
    current_user: base.User = Depends(deps.get_current_active_user)
) -> Any:
    digest = crud.digest.get(db, uuid=uuid)
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
    return digest

@router.post("/", response_model=schemas.Digest)
def create_digest(
    *,
    db: Session = Depends(deps.get_db),
    digest_in: schemas.DigestCreate,
    current_user: base.User = Depends(deps.get_current_active_user)
) -> Any:
    digest = crud.digest.create_with_owner(db, obj_in=digest_in, user_uuid=current_user.uuid)
    return digest

@router.put("/{uuid}", response_model=schemas.Digest)
def update_digest(
    *,
    db: Session = Depends(deps.get_db),
    uuid: UUID,
    digest_in: schemas.DigestUpdate,
    current_user: base.User = Depends(deps.get_current_active_user)
) -> Any:
    digest = crud.digest.get(db, uuid=uuid)
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
    digest = crud.digest.update(db, db_obj=digest, obj_in=digest_in)
    return digest

@router.delete("/{uuid}", response_model=schemas.Digest)
def delete_digest(
    *,
    db: Session = Depends(deps.get_db),
    uuid: UUID,
    current_user: base.User = Depends(deps.get_current_active_user)
) -> Any:
    digest = crud.digest.get(db, uuid=uuid)
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
    digest = crud.digest.remove(db, uuid=uuid)
    return digest
