from typing import Any, Dict, List, Optional, Union
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select, insert

from theroast.db.crud.base import CRUDBase
from theroast.db.tables.digest import Digest, create_color
from theroast.app.schemas.digest import DigestCreate, DigestUpdate


class CRUDDigest(CRUDBase[Digest, DigestCreate, DigestUpdate]):

    def get_multi_by_owner(self, db: Session, *, user_uuid: UUID, skip: Optional[int], limit: Optional[int]) -> List[Digest]:
        stmt = select(Digest).where(Digest.user_uuid == user_uuid)
        if skip and limit:
            stmt = stmt.offset(skip).limit(limit)
        elif skip:
            stmt = stmt.offset(skip)
        elif limit:
            stmt = stmt.limit(limit)
        return db.execute(stmt).fetchall()

    def create_with_owner(self, db: Session, *, obj_in: DigestCreate, user_uuid: UUID) -> Digest:
        stmt = insert(Digest).values(
            user_uuid=obj_in.user_uuid,
            name=obj_in.name,
            interests=obj_in.interests,
            sources=obj_in.sources,
            personality=obj_in.personality,
            color=create_color(obj_in.color),
            is_enabled=obj_in.is_enabled
        )
        db_obj = db.execute(stmt).first()
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def is_enabled(self, Digest: Digest) -> bool:
        return Digest.is_enabled


digest = CRUDDigest(Digest)