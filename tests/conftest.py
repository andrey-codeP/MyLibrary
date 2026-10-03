import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import library
from app.database.depends import get_db
from app.database.models.base import Base
from app.security.login import get_current_user_id

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

async_engine = create_async_engine(
    DATABASE_URL, poolclass=StaticPool, connect_args={"check_same_thread": False}
)

TestingSession = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)


@pytest.fixture(scope="session", autouse=True)
async def get_db_test():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def get_db_sess():
    async with TestingSession() as session:
        try:
            yield session
        finally:
            await session.rollback()


@pytest.fixture
async def client(get_db_sess):
    library.dependency_overrides[get_db] = lambda: get_db_sess
    library.dependency_overrides[get_current_user_id] = lambda: 67

    async with AsyncClient(
        transport=ASGITransport(app=library), base_url="http://test"
    ) as client:
        yield client

    library.dependency_overrides.clear()


@pytest.fixture
def book_dict_test():
    return {
        "title": "моякнижка",
        "author": "я",
        "year": 2021,
        "pages": 12,
    }
