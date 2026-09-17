from fastapi import FastAPI
from contextlib import asynccontextmanager

from database.models.book_table import BookBase, Books
from database.connections import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(BookBase.metadata.create_all)

    yield





library = FastAPI(
    lifespan=lifespan,
    title="MyLittleLibrary",
    description="My trial project, I’m writing a library.",
    version="1.0.0")

