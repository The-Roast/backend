from typing import Any, Dict, List, Optional, Union
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from sqlalchemy.orm import Session, selectinload, defer
from sqlalchemy.orm.strategy_options import _AttrType

from theroast.db.crud.base import CRUDBase
from theroast.db.tables.newsletter import Newsletter
from theroast.db.tables.article import Article
from theroast.app.schemas.article import ArticleCreate, ArticleUpdate

class CRUDArticle(CRUDBase[Article, ArticleCreate, ArticleUpdate]):

    async def get_multi_by_newsletter(
        self,
        db: AsyncSession,
        *,
        uuid: UUID, skip: int = 0, limit: int = 0,
        with_eager: bool = False, with_defer: bool = False,
        _eager_attrs: List[_AttrType] = [Newsletter.digest, Newsletter.articles],
        _defer_attrs: List[_AttrType] = []
    ) -> List[Article]:
        stmt = select(Newsletter).where(Newsletter.uuid == uuid)
        if with_eager: stmt = stmt.options(selectinload(*_eager_attrs))
        if with_defer: stmt = stmt.options(defer(*_defer_attrs))
        if skip: stmt = stmt.offset(skip)
        if limit: stmt = stmt.limit(limit)
        scals = await db.scalars(stmt)
        db_objs = scals.first()
        return db_objs.articles

    async def create_multi_with_newsletter(
        self,
        db: AsyncSession,
        *,
        objs_in: List[ArticleCreate], newsletter: Newsletter,
        with_eager: bool = False, with_defer: bool = False,
        _eager_attrs: List[_AttrType] = [Article.newsletters],
        _defer_attrs: List[_AttrType] = []
    )-> List[Article]:
        stmt = insert(Article).values([
            obj_in.dict() for obj_in in objs_in
        ]).returning(Article)
        if with_eager: stmt = stmt.options(selectinload(*_eager_attrs))
        if with_defer: stmt = stmt.options(defer(*_defer_attrs))
        scals = await db.scalars(stmt)
        db_objs = scals.all()
        newsletter.articles.extend(db_objs)
        await db.commit()
        for db_obj in db_objs:
            await db.refresh(db_obj)
        await db.refresh(newsletter)
        return db_objs

    async def create_multi(
        self,
        db: AsyncSession,
        *,
        objs_in: List[ArticleCreate],
        with_eager: bool = False, with_defer: bool = False,
        _eager_attrs: List[_AttrType] = [Article.newsletters],
        _defer_attrs: List[_AttrType] = []
    ) -> List[Article]:
        stmt = insert(Article).values([
            obj_in.dict() for obj_in in objs_in
        ]).returning(Article)
        if with_eager: stmt = stmt.options(selectinload(*_eager_attrs))
        if with_defer: stmt = stmt.options(defer(*_defer_attrs))
        scals = await db.scalars(stmt)
        db_objs = scals.all()
        await db.commit()
        for db_obj in db_objs:
            await db.refresh(db_obj)
        return db_objs

    async def create_with_newsletter(
        self,
        db: AsyncSession,
        *,
        obj_in: ArticleCreate, newsletter: Newsletter,
        with_eager: bool = False, with_defer: bool = False,
        _eager_attrs: List[_AttrType] = [Article.newsletters],
        _defer_attrs: List[_AttrType] = []
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
        if with_eager: stmt = stmt.options(selectinload(*_eager_attrs))
        if with_defer: stmt = stmt.options(defer(*_defer_attrs))
        scals = await db.scalars(stmt)
        db_obj = scals.first()
        newsletter.articles.extend(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def update_with_newsletter(self, db: AsyncSession, *, obj_in: Article, db_obj: Newsletter) -> Article:
        obj_in.newsletters.extend(db_obj)
        await db.commit()
        await db.refresh(obj_in)
        return obj_in


article = CRUDArticle(Article)