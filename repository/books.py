from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.book import SBookAdd, SBook
from database.models.book_table import Books

class BooksRepository:
    @classmethod
    async def add_book(cls, book: SBookAdd, session: AsyncSession) -> Books:
        book = Books(**book.model_dump())
        session.add(book)

        await session.flush()
        await session.refresh(book)

        return book

    @classmethod
    async def get_book(cls, book_id: int, session: AsyncSession) -> Books | None:
        query = select(Books).where(Books.id == book_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def get_all_books(cls, session: AsyncSession):
        query = select(Books)
        result = await session.execute(query)
        return result.scalars().all()