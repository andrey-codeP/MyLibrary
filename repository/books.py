from sqlalchemy import select, update, delete
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
    async def get_all_books(cls, session: AsyncSession) -> list[Books]:
        query = select(Books)
        result = await session.execute(query)

        all_books = result.scalars().all()
        return list(all_books)


    @classmethod
    async def update_book(cls, book_id: int, book: SBookAdd, session: AsyncSession) -> Books:
        book = book.model_dump(exclude_unset=True)
        query = update(Books).where(Books.id == book_id).values(**book).returning(Books)

        result = await session.execute(query)

        await session.flush()
        update_book = result.scalar_one_or_none()

        return update_book


    @classmethod
    async def delete_book(cls, book_id: int, session: AsyncSession) -> Books | None:
        query = delete(Books).where(Books.id == book_id).returning(Books)
        result = await session.execute(query)

        await session.flush()

        delete_book = result.scalar_one_or_none()
        return delete_book