from typing import Any, Dict, List, Optional, Union
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from sqlalchemy.orm import Session

from theroast.core.security import get_password_hash, verify_password
from theroast.db.crud.base import CRUDBase
from theroast.db.base import Article, Newsletter, newsletter_article
from theroast.app.schemas.article import ArticleCreate, ArticleUpdate

class CRUDArticle(CRUDBase[Article, ArticleCreate, ArticleUpdate]):

    async def get_multi_by_newsletter(
            self, db: AsyncSession, *, uuid: UUID, skip: Optional[int], limit: Optional[int]
        ) -> List[Article]:
        stmt = select(Newsletter).where(Newsletter.uuid == uuid)
        if skip: stmt = stmt.offset(skip)
        if limit: stmt = stmt.limit(limit)
        scals = await db.scalars(stmt)
        db_obj = scals.first()
        return db_obj.articles

    async def create_multi_with_newsletter(
            self, db: AsyncSession, *, objs_in: List[ArticleCreate], newsletter: Newsletter
        )-> List[Article]:
        stmt = insert(Article).values([
            obj_in.dict() for obj_in in objs_in
        ]).returning(Article)
        scals = await db.scalars(stmt)
        db_objs = scals.all()
        newsletter.articles.extend(db_objs)
        await db.commit()
        await db.refresh(db_objs)
        return db_objs.all()

    async def create_multi(self, db: AsyncSession, *, objs_in: List[ArticleCreate]) -> List[Article]:
        stmt = insert(Article).values([
            obj_in.dict() for obj_in in objs_in
        ]).returning(Article)
        scals = await db.scalars(stmt)
        db_objs = scals.all()
        await db.commit()
        await db.refresh(db_objs)
        return db_objs.all()

    async def create_with_newsletter(
            self, db: AsyncSession, *, obj_in: ArticleCreate, newsletter: Newsletter
        ) -> Article:
        stmt = insert(Article).values(
            source=obj_in.source,
            authors=obj_in.authors,
            title=obj_in.title,
            content=obj_in.content,
            keywords=obj_in.keywords,
            url=obj_in.url,
            published_at=obj_in.published_at
        ).returning(Article)
        scals = await db.scalars(stmt)
        db_obj = scals.first()
        newsletter.articles.extend(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def create(self, db: AsyncSession, *, obj_in: ArticleCreate) -> Article:
        stmt = insert(Article).values(
            source=obj_in.source,
            authors=obj_in.authors,
            title=obj_in.title,
            content=obj_in.content,
            keywords=obj_in.keywords,
            url=obj_in.url,
            published_at=obj_in.published_at
        ).returning(Article)
        scals = await db.scalars(stmt)
        db_obj = scals.first()
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def update_with_newsletter(self, db: AsyncSession, *, uuid: UUID, newsletter: Newsletter) -> Article:
        db_obj = await self.get(db, uuid=uuid)
        db_obj.newsletters.extend(newsletter)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


Article = CRUDArticle(Article)