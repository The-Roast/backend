from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from theroast.config import server_config

engine = create_async_engine(server_config.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, echo=True)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)
