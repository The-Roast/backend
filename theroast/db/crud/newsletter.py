from typing import Dict, Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from sqlalchemy.orm import Session, selectinload, defer
from sqlalchemy.orm.strategy_options import _AttrType

from theroast.db.crud.base import CRUDBase
from theroast.db.tables.article import Article
from theroast.db.tables.newsletter import Newsletter
from theroast.db.tables.digest import Digest
from theroast.app.schemas.newsletter import NewsletterCreate, NewsletterUpdate
from theroast.app.schemas.chat import ChatCreate, Chat
from theroast.app.utils import ORDER_BY

ORDER_BY_MAPPING = {
    ORDER_BY.DATE: Newsletter.updated_at,
    ORDER_BY.USAGE: Newsletter.clicks
}

class CRUDNewsletter(CRUDBase[Newsletter, NewsletterCreate, NewsletterUpdate]):

    async def get_multi_by_digest(
        self,
        db: AsyncSession,
        *,
        digest_uuid: UUID, order_by: ORDER_BY, skip: int = 0, limit: int = 0,
        with_eager: bool = False, with_defer: bool = False,
        _eager_attrs: List[_AttrType] = [Newsletter.digest, Newsletter.articles],
        _defer_attrs: List[_AttrType] = [Newsletter.chat]
    ) -> List[Newsletter]:
        order_col = ORDER_BY_MAPPING[order_by]
        stmt = select(Newsletter).where(Newsletter.digest_uuid == digest_uuid).order_by(order_col.desc())
        if with_eager: stmt = stmt.options(selectinload(_eager_attrs))
        if with_defer: stmt = stmt.options(defer(_defer_attrs))
        if skip: stmt = stmt.offset(skip)
        if limit: stmt = stmt.limit(limit)
        db_objs = await db.scalars(stmt)
        return db_objs.all()

    async def get_multi_by_owner(
        self,
        db: AsyncSession,
        *,
        user_uuid: UUID, order_by: ORDER_BY, skip: int = 0, limit: int = 0,
        with_eager: bool = False, with_defer: bool = False,
        _eager_attrs: List[_AttrType] = [Newsletter.digest, Newsletter.articles],
        _defer_attrs: List[_AttrType] = [Newsletter.chat]
    ) -> List[Newsletter]:
        order_col = ORDER_BY_MAPPING[order_by]
        stmt = select(Newsletter).join(Digest.newsletters).where(Digest.user_uuid == user_uuid).order_by(order_col.desc())
        if with_eager: stmt = stmt.options(selectinload(_eager_attrs))
        if with_defer: stmt = stmt.options(defer(_defer_attrs))
        if skip: stmt = stmt.offset(skip)
        if limit: stmt = stmt.limit(limit)
        db_objs = await db.scalars(stmt)
        return db_objs.all()

    async def create_with_data(
        self,
        db: AsyncSession,
        *,
        obj_in: NewsletterCreate, data: dict,
        with_eager: bool = False, with_defer: bool = False,
        _eager_attrs: List[_AttrType] = [Newsletter.digest, Newsletter.articles],
        _defer_attrs: List[_AttrType] = [Newsletter.chat]
    ) -> Newsletter:
        stmt = insert(Newsletter).values(
            digest_uuid=obj_in.digest_uuid,
            title=data["title"],
            introduction=data["introduction"],
            body=data["body"],
            conclusion=data["conclusion"],
            html=data.get("html", None)
        ).returning(Newsletter)
        if with_eager: stmt = stmt.options(selectinload(_eager_attrs))
        if with_defer: stmt = stmt.options(defer(_defer_attrs))
        db_objs = await db.scalars(stmt)
        db_obj = db_objs.first()
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def create_message(self, db: AsyncSession, *, obj_in: ChatCreate, db_obj: Newsletter) -> Chat:
        pass

    async def update_with_article(self, db: AsyncSession, *, obj_in: Newsletter, db_obj: List[Article]) -> Newsletter:
        obj_in.articles.extend(db_obj)
        await db.commit()
        await db.refresh(obj_in)
        return obj_in

    def sget_multi_by_digest(
        self,
        db: Session,
        *,
        digest_uuid: UUID, order_by: ORDER_BY, skip: int = 0, limit: int = 0,
        with_eager: bool = False, with_defer: bool = False,
        _eager_attrs: List[_AttrType] = [Newsletter.digest, Newsletter.articles],
        _defer_attrs: List[_AttrType] = [Newsletter.chat]
    ) -> List[Newsletter]:
        order_col = ORDER_BY_MAPPING[order_by]
        stmt = select(Newsletter).where(Newsletter.digest_uuid == digest_uuid).order_by(order_col.desc())
        if skip: stmt = stmt.offset(skip)
        if limit: stmt = stmt.limit(limit)
        if with_eager: stmt = stmt.options(selectinload(_eager_attrs))
        if with_defer: stmt = stmt.options(defer(_defer_attrs))
        db_objs = db.scalars(stmt)
        return db_objs.all()

    def screate_with_data(
        self,
        db: Session,
        *,
        obj_in: NewsletterCreate, data: Dict,
        with_eager: bool = False, with_defer: bool = False,
        _eager_attrs: List[_AttrType] = [Newsletter.digest, Newsletter.articles],
        _defer_attrs: List[_AttrType] = [Newsletter.chat]
    ) -> Newsletter:
        stmt = insert(Newsletter).values(
            digest_uuid=obj_in.digest_uuid,
            title=data["title"],
            introduction=data["introduction"],
            body=data["body"],
            conclusion=data["conclusion"],
            html=data.get("html", None)
        ).returning(Newsletter)
        if with_eager: stmt = stmt.options(selectinload(_eager_attrs))
        if with_defer: stmt = stmt.options(defer(_defer_attrs))
        db_objs = db.scalars(stmt)
        db_obj = db_objs.first()
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def is_updated(self, Newsletter: Newsletter) -> bool:
        return Newsletter.created_at != Newsletter.updated_at


newsletter = CRUDNewsletter(Newsletter)