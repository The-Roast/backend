from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from http import HTTPStatus

from theroast.app import schemas, deps, utils
from theroast.db import base, crud

router = APIRouter()

@router.get("/all/", response_model=List[schemas.Digest])
async def read_digests(
    *,
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 0,
    current_user: base.User = Depends(deps.get_current_active_user)
) -> Any:
    digests = await crud.digest.get_multi_by_owner(db, user_uuid=current_user.uuid, skip=skip, limit=limit)
    return digests

@router.get("/{uuid}", response_model=schemas.Digest)
async def read_digest(
    *,
    db: AsyncSession = Depends(deps.get_db),
    uuid: UUID,
    current_user: base.User = Depends(deps.get_current_active_user)
) -> Any:
    digest = await crud.digest.get(db, uuid=uuid)
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

@router.get("/{uuid}/newsletters", response_model=List[schemas.Newsletter])
async def read_newsletters_by_digest(
    *,
    db: AsyncSession = Depends(deps.get_db),
    uuid: UUID,
    order_by: utils.ORDER_BY = utils.ORDER_BY.DATE,
    skip: int = 0,
    limit: int = 0,
    current_user: base.User = Depends(deps.get_current_active_user)
) -> Any:
    digest = await crud.digest.get(db, uuid=uuid)
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
    _get_multi = crud.newsletter.get_multi_by_digest__date
    if order_by is utils.ORDER_BY.USAGE:
        _get_multi = crud.newsletter.get_multi_by_digest__clicks
    newsletters = await _get_multi(db, digest_uuid=uuid, skip=skip, limit=limit)
    return newsletters

@router.post("/", response_model=schemas.Digest)
async def create_digest(
    *,
    db: AsyncSession = Depends(deps.get_db),
    digest_in: schemas.DigestCreate,
    current_user: base.User = Depends(deps.get_current_active_user)
) -> Any:
    digest = await crud.digest.create_with_owner(db, obj_in=digest_in, user_uuid=current_user.uuid)
    return digest

@router.put("/{uuid}", response_model=schemas.Digest)
async def update_digest(
    *,
    db: AsyncSession = Depends(deps.get_db),
    uuid: UUID,
    digest_in: schemas.DigestUpdate,
    current_user: base.User = Depends(deps.get_current_active_user)
) -> Any:
    digest = await crud.digest.get(db, uuid=uuid, with_eager=True)
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
    digest = await crud.digest.update(db, db_obj=digest, obj_in=digest_in)
    return digest

@router.delete("/{uuid}", response_model=schemas.Digest)
async def delete_digest(
    *,
    db: AsyncSession = Depends(deps.get_db),
    uuid: UUID,
    current_user: base.User = Depends(deps.get_current_active_user)
) -> Any:
    digest = await crud.digest.get(db, uuid=uuid)
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
    digest = await crud.digest.remove(db, uuid=uuid)
    return digest
