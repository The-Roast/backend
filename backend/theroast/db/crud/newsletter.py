from typing import Dict, Optional, UUID4
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select, insert

from theroast.db.crud.base import CRUDBase
from theroast.db.tables.newsletter import Newsletter
from theroast.app.schemas.newsletter import NewsletterCreate, NewsletterUpdate


class CRUDNewsletter(CRUDBase[Newsletter, NewsletterCreate, NewsletterUpdate]):

    def get_multi_by_digest__date(self, db: Session, *, digest_uuid: UUID4, skip: Optional[int], limit: Optional[int]):
        stmt = select(Newsletter).where(Newsletter.digest_uuid == digest_uuid).order_by(Newsletter.updated_at.desc())
        if skip and limit:
            stmt = stmt.offset(skip).limit(limit)
        elif skip:
            stmt = stmt.offset(skip)
        elif limit:
            stmt = stmt.limit(limit)
        return db.execute(stmt).fetchall()
    
    def get_multi_by_digest__clicks(self, db: Session, *, digest_uuid: UUID4, skip: Optional[int], limit: Optional[int]):
        stmt = select(Newsletter).where(Newsletter.digest_uuid == digest_uuid).order_by(Newsletter.clicks.desc())
        if skip and limit:
            stmt = stmt.offset(skip).limit(limit)
        elif skip:
            stmt = stmt.offset(skip)
        elif limit:
            stmt = stmt.limit(limit)
        return db.execute(stmt).fetchall()

    def create_with_data(self, db: Session, *, obj_in: NewsletterCreate, data: Dict) -> Newsletter:
        stmt = insert(Newsletter).values(
            digest_uuid=obj_in.digest_uuid,
            title=data["title"],
            introduction=data["introduction"],
            body=data["body"],
            conlusion=data["conclusion"],
            html=data["html"]
        )
        db_obj = db.execute(stmt).first()
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def is_updated(self, Newsletter: Newsletter) -> bool:
        return Newsletter.created_at != Newsletter.updated_at


newsletter = CRUDNewsletter(Newsletter)