from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from database.config import setting

engine = create_async_engine(setting.DATABASE_URL)

new_sessions = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)

