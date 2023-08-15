from typing import Dict, Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from enum import Enum

from theroast.db.crud.base import CRUDBase
from theroast.db.tables.newsletter import Newsletter
from theroast.app.schemas.newsletter import NewsletterCreate, NewsletterUpdate

class CRUDNewsletter(CRUDBase[Newsletter, NewsletterCreate, NewsletterUpdate]):

    async def get_multi_by_digest__date(self, db: AsyncSession, *, digest_uuid: UUID, skip: Optional[int], limit: Optional[int]) -> List[Newsletter]:
        stmt = select(Newsletter).where(Newsletter.digest_uuid == digest_uuid).order_by(Newsletter.updated_at.desc())
        if skip: stmt = stmt.offset(skip)
        if limit: stmt = stmt.limit(limit)
        db_objs = await db.scalars(stmt)
        return db_objs.all()
    
    async def get_multi_by_digest__clicks(self, db: AsyncSession, *, digest_uuid: UUID, skip: Optional[int], limit: Optional[int]) -> List[Newsletter]:
        stmt = select(Newsletter).where(Newsletter.digest_uuid == digest_uuid).order_by(Newsletter.clicks.desc())
        if skip: stmt = stmt.offset(skip)
        if limit: stmt = stmt.limit(limit)
        db_objs = await db.scalars(stmt)
        return db_objs.all()

    async def create_with_data(self, db: AsyncSession, *, obj_in: NewsletterCreate, data: Dict) -> Newsletter:
        stmt = insert(Newsletter).values(
            digest_uuid=obj_in.digest_uuid,
            title=data["title"],
            introduction=data["introduction"],
            body=data["body"],
            conclusion=data["conclusion"],
            html=data.get("html", None)
        ).returning(Newsletter)
        db_objs = await db.scalars(stmt)
        db_obj = db_objs.first()
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    def sget_multi_by_digest__date(self, db: Session, *, digest_uuid: UUID, skip: Optional[int], limit: Optional[int]) -> List[Newsletter]:
        stmt = select(Newsletter).where(Newsletter.digest_uuid == digest_uuid).order_by(Newsletter.updated_at.desc())
        if skip: stmt = stmt.offset(skip)
        if limit: stmt = stmt.limit(limit)
        db_objs = db.scalars(stmt)
        return db_objs.all()
    
    def sget_multi_by_digest__clicks(self, db: Session, *, digest_uuid: UUID, skip: Optional[int], limit: Optional[int]) -> List[Newsletter]:
        stmt = select(Newsletter).where(Newsletter.digest_uuid == digest_uuid).order_by(Newsletter.clicks.desc())
        if skip: stmt = stmt.offset(skip)
        if limit: stmt = stmt.limit(limit)
        db_objs = db.scalars(stmt)
        return db_objs.all()

    def screate_with_data(self, db: Session, *, obj_in: NewsletterCreate, data: Dict) -> Newsletter:
        stmt = insert(Newsletter).values(
            digest_uuid=obj_in.digest_uuid,
            title=data["title"],
            introduction=data["introduction"],
            body=data["body"],
            conclusion=data["conclusion"],
            html=data.get("html", None)
        ).returning(Newsletter)
        db_objs = db.scalars(stmt)
        db_obj = db_objs.first()
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def is_updated(self, Newsletter: Newsletter) -> bool:
        return Newsletter.created_at != Newsletter.updated_at


newsletter = CRUDNewsletter(Newsletter)