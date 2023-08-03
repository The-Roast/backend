from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from theroast.db.crud.base import CRUDBase
from theroast.db.tables.digest import Digest, create_color
from theroast.app.schemas.digest import DigestCreate, DigestUpdate


class CRUDDigest(CRUDBase[Digest, DigestCreate, DigestUpdate]):

    async def get_multi_by_owner(self, db: AsyncSession, *, user_uuid: UUID, skip: Optional[int], limit: Optional[int]) -> List[Digest]:
        stmt = select(Digest).where(Digest.user_uuid == user_uuid)
        if skip: stmt = stmt.offset(skip)
        if limit: stmt = stmt.limit(limit)
        db_objs = await db.scalars(stmt)
        return db_objs.all()

    async def create_with_owner(self, db: AsyncSession, *, obj_in: DigestCreate, user_uuid: UUID) -> Digest:
        stmt = insert(Digest).values(
            user_uuid=user_uuid,
            name=obj_in.name,
            interests=obj_in.interests,
            sources=obj_in.sources,
            personality=obj_in.personality,
            color=create_color(obj_in.color),
            is_enabled=obj_in.is_enabled
        ).returning(Digest)
        db_objs = await db.scalars(stmt)
        db_obj = db_objs.first()
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    def is_enabled(self, Digest: Digest) -> bool:
        return Digest.is_enabled


digest = CRUDDigest(Digest)