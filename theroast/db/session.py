from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from theroast.config import server_config

engine = create_engine(server_config.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
