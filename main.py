from fastapi import FastAPI
from contextlib import asynccontextmanager

from middlewares import log_and_time_middleware
from database.models.base import Base
from database.connections import engine
from routers.books import router as book_router
from routers.frontend import router as front_router
from routers.authorization import router as authorization_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


library = FastAPI(
    lifespan=lifespan,
    title="MyLittleLibrary",
    description="My trial project, I’m writing a library.",
    version="1.0.0",
    redirect_slashes=False,
)

library.middleware("http")(log_and_time_middleware)


library.include_router(book_router)
library.include_router(front_router)
library.include_router(authorization_router)
