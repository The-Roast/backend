from typing import Any, Dict, Optional, Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from sqlalchemy.orm import Session, selectinload

from theroast.core.security import get_password_hash, verify_password
from theroast.db.crud.base import CRUDBase
from theroast.db.tables.user import User
from theroast.app.schemas.user import UserCreate, UserUpdate

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    async def get_by_email(self, db: AsyncSession, *, email: str, with_eager: bool = False) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        if with_eager: stmt = stmt.options(selectinload(User.digests))
        scals = await db.scalars(stmt)
        return scals.first()

    async def create(self, db: AsyncSession, *, obj_in: UserCreate, with_eager: bool = False) -> User:
        stmt = insert(User).values(
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
            is_active=obj_in.is_active,
            is_superuser=obj_in.is_superuser
        ).returning(User)
        if with_eager: stmt = stmt.options(selectinload(User.digests))
        scals = await db.scalars(stmt)
        db_obj = scals.first()
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: AsyncSession, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            update_data["password"] = hashed_password
        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    async def authenticate(self, db: AsyncSession, *, email: str, password: str) -> Optional[User]:
        user = await self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        user.is_active = True
        db.add(user)
        await db.commit()
        return user
    
    def sget_by_email(self, db: Session, *, email: str, with_eager: bool = False) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        if with_eager: stmt = stmt.options(selectinload(User.digests))
        scals = db.scalars(stmt)
        return scals.first()

    def screate(self, db: Session, *, obj_in: UserCreate, with_eager: bool = False) -> User:
        stmt = insert(User).values(
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
            is_active=obj_in.is_active,
            is_superuser=obj_in.is_superuser
        ).returning(User)
        if with_eager: stmt = stmt.options(selectinload(User.digests))
        scals = db.scalars(stmt)
        db_obj = scals.first()
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def supdate(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            update_data["password"] = hashed_password
        return super().supdate(db, db_obj=db_obj, obj_in=update_data)

    def sauthenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        user.is_active = True
        db.add(user)
        db.commit()
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)