import logging
import asyncio

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from theroast.db.init_db import init_db
from theroast.db.session import SessionLocal, engine
from theroast.db.base import Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init() -> None:
    db = SessionLocal()
    async with db:
        await db.run_sync(Base.metadata.create_all)
    init_db(db)


def main() -> None:
    logger.info("Creating initial data")
    asyncio.run(init())
    logger.info("Initial data created")

if __name__ == "__main__":
    main()