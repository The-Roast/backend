from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete
from sqlalchemy.orm import Session, selectinload

from theroast.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, db: AsyncSession, uuid: UUID, with_eager: bool = False) -> Optional[ModelType]:
        stmt = select(self.model).where(self.model.uuid == uuid)
        if with_eager: stmt = stmt.options(selectinload("*"))
        db_objs = await db.scalars(stmt)
        return db_objs.first()

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100, with_eager: bool = False
    ) -> List[ModelType]:
        stmt = select(self.model)
        if with_eager: stmt = stmt.options(selectinload("*"))
        if skip: stmt = stmt.offset(skip)
        if limit: stmt = stmt.limit(limit)
        db_objs = await db.scalars(stmt)
        return db_objs.all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType, with_eager: bool = False) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        stmt = insert(self.model).values(obj_in_data).returning(self.model)
        if with_eager: stmt = stmt.options(selectinload("*"))
        db_objs = await db.scalars(stmt)
        db_obj = db_objs.first()
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def remove(self, db: AsyncSession, *, uuid: UUID, with_eager: bool = False) -> ModelType:
        stmt = delete(self.model).where(self.model.uuid == uuid).returning(self.model)
        if with_eager: stmt = stmt.options(selectinload("*"))
        db_objs = await db.scalars(stmt)
        await db.commit()
        return db_objs.first()
    
    def sget(self, db: Session, uuid: UUID, with_eager: bool = False) -> Optional[ModelType]:
        stmt = select(self.model).where(self.model.uuid == uuid)
        if with_eager: stmt = stmt.options(selectinload("*"))
        db_objs = db.scalars(stmt)
        return db_objs.first()
    
    def sget_multi(
        self, db: Session, *, skip: int = 0, limit: int = 0, with_eager: bool = False
    ) -> List[ModelType]:
        stmt = select(self.model).offset(skip).limit(limit)
        if with_eager: stmt = stmt.options(selectinload("*"))
        if skip: stmt = stmt.offset(skip)
        if limit: stmt = stmt.limit(limit)
        db_objs = db.scalars(stmt)
        return db_objs.all()
    
    def screate(self, db: Session, *, obj_in: CreateSchemaType, with_eager: bool = False) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        stmt = insert(self.model).values(obj_in_data).returning(self.model)
        if with_eager: stmt = stmt.options(selectinload("*"))
        db_objs = db.scalars(stmt)
        db_obj = db_objs.first()
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def supdate(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def sremove(self, db: Session, *, uuid: UUID, with_eager: bool = False) -> ModelType:
        stmt = delete(self.model).where(self.model.uuid == uuid).returning(self.model)
        if with_eager: stmt = stmt.options(selectinload("*"))
        db_objs = db.scalars(stmt)
        db.commit()
        return db_objs.first()
