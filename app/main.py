from fastapi import FastAPI

from app.middlewares import log_and_time_middleware
from app.routers.books import router as book_router
from app.routers.frontend import router as front_router
from app.routers.authorization import router as authorization_router





library = FastAPI(
    title="MyLittleLibrary",
    description="My trial project, I’m writing a library.",
    version="1.0.0",
    redirect_slashes=False,
)

library.middleware("http")(log_and_time_middleware)


library.include_router(book_router)
library.include_router(front_router)
library.include_router(authorization_router)
