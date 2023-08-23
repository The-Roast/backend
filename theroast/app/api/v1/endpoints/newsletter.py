from typing import Any, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from http import HTTPStatus
from enum import Enum

from theroast.app import schemas, deps, utils
from theroast.db import base, crud
from theroast.lib import pipeline

router = APIRouter()

@router.get("/all/", response_model=List[schemas.Newsletter])
async def read_newsletters(
    *,
    db: AsyncSession = Depends(deps.get_db),
    order_by: utils.ORDER_BY = utils.ORDER_BY.DATE,
    digest_uuid: Optional[UUID] = None,
    skip: int = 0,
    limit: int = 0,
    current_user: base.User = Depends(deps.get_current_active_user)
) -> Any:
    digest = await crud.digest.get(db, uuid=digest_uuid)
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
    if order_by is utils.ORDER_BY.DATE:
        _get_multi = crud.newsletter.get_multi_by_digest__date
    newsletters = await _get_multi(db, digest_uuid=digest_uuid, skip=skip, limit=limit)
    return newsletters

@router.get("/{uuid}", response_model=schemas.Newsletter)
async def read_newsletter(
    *,
    db: AsyncSession = Depends(deps.get_db),
    uuid: UUID,
) -> Any:
    newsletter = await crud.newsletter.get(db, uuid=uuid)
    if not newsletter:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Newsletter not found."
        )
    return newsletter

@router.post("/", response_model=schemas.Newsletter)
async def create_newsletter(
    *,
    db: AsyncSession = Depends(deps.get_db),
    newsletter_in: schemas.NewsletterCreate,
    current_user: base.User = Depends(deps.get_current_active_user)
) -> Any:
    digest = await crud.digest.get(db, uuid=newsletter_in.digest_uuid)
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
    digest_data = jsonable_encoder(digest)
    sections, structure, articles = pipeline.generate_newsletter(digest_data)
    newsletter_data = pipeline.restructure(sections, structure)
    newsletter = await crud.newsletter.create_with_data(db, obj_in=newsletter_in, data=newsletter_data, with_eager=True)
    article_objs = [schemas.ArticleCreate(**article) for article in articles]
    articles = await crud.article.create_multi_with_newsletter(db, objs_in=article_objs, newsletter=newsletter, with_eager=True)
    return newsletter

@router.put("/{uuid}", response_model=schemas.Newsletter)
async def update_newsletter(
    *,
    db: AsyncSession = Depends(deps.get_db),
    uuid: UUID,
    current_user: base.User = Depends(deps.get_current_active_user)
) -> Any:
    newsletter = await crud.newsletter.get(db, uuid=uuid, with_eager=True)
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
    digest_data = jsonable_encoder(digest)
    articles = await crud.article.get_multi_by_newsletter(db, uuid=uuid)
    articles_di = [{
        "source": article.source,
        "authors": article.authors,
        "title": article.title,
        "content": article.content,
        "keywords": article.keywords,
        "url": article.url,
        "published_at": article.published_at
    } for article in articles]
    sections, structure, _ = pipeline.generate_newsletter(digest_data, articles_di)
    newsletter_data = pipeline.restructure(sections, structure)
    newsletter_in = schemas.NewsletterUpdate(uuid=newsletter.uuid, **newsletter_data)
    newsletter = await crud.newsletter.update(db, db_obj=newsletter, obj_in=newsletter_in)
    return newsletter

@router.delete("/{uuid}", response_model=schemas.Newsletter)
async def delete_newsletter(
    *,
    db: AsyncSession = Depends(deps.get_db),
    uuid: UUID,
    current_user: base.User = Depends(deps.get_current_active_user)
) -> Any:
    newsletter = await crud.newsletter.get(db, uuid=uuid, with_eager=True)
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
    newsletter = await crud.newsletter.remove(db, uuid=uuid)
    return newsletter

@router.get("/{uuid}/chat", response_model=schemas.Message)
async def read_chat(
    *,
    db: AsyncSession = Depends(deps.get_db),
    uuid: UUID,
    current_user: base.User = Depends(deps.get_current_active_user)
) -> Any:
    newsletter = await crud.newsletter.get(db, uuid=uuid)
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
    return {"message": "This is a test response."}

@router.post("/{uuid}/history", response_model=schemas.Message)
async def read_chats(
    *,
    db: AsyncSession = Depends(deps.get_db),
    uuid: UUID,
    current_user: base.User = Depends(deps.get_current_active_user)
) -> Any:
    newsletter = await crud.newsletter.get(db, uuid=uuid)
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
    return {"message": "This is a test response."}