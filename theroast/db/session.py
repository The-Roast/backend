from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from theroast.config import server_config

engine = create_async_engine(server_config.ASYNC_SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, echo=True)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)

def get_sync():
    engine = create_engine(server_config.SYNC_SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)
    return engine, SessionLocal