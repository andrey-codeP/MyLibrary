from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


from config import settings

engine = create_async_engine(settings.DATABASE_URL_STR)

new_sessions = async_sessionmaker(bind=engine, expire_on_commit=False)
