from fastapi import APIRouter
from fastapi import status
from schemas.book import SBookAdd, SBook
from database.depends import SessionDup

router = APIRouter(
    prefix="/books",
    tags=["Books"],
)


@router.post("/", response_model=SBookAdd, status_code=status.HTTP_201_CREATED)
async def create_book(book: SBook, session: SessionDup):
    ...