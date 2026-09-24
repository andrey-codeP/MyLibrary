from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.book import SBookAdd, SBook
from database.models.book_table import Books


class BooksRepository:
    @classmethod
    async def add_book(cls, book: SBookAdd, user_id: int, session: AsyncSession) -> Books:
        book = Books(**book.model_dump(), owner_id=user_id)
        session.add(book)

        await session.flush()
        await session.refresh(book)

        return book

    @classmethod
    async def get_book(cls, user_id: int, book_id: int, session: AsyncSession) -> Books | None:
        query = select(Books).where(Books.owner_id == user_id, Books.id == book_id)
        result = await session.execute(query)

        return result.scalar_one_or_none()

    @classmethod
    async def get_all_books(cls, user_id: int, session: AsyncSession) -> list[Books]:
        query = select(Books).where(user_id == Books.owner_id)
        result = await session.execute(query)

        all_books = result.scalars().all()
        return list(all_books)

    @classmethod
    async def update_book(
        cls,
        user_id: int,
        book: SBookAdd,
        book_id: int,
        session: AsyncSession
    ) -> Books:
        book = book.model_dump(exclude_unset=True)
        query = (update(Books).
                 where(Books.owner_id == user_id, Books.id == book_id).
                 values(**book).
                 returning(Books))

        result = await session.execute(query)

        await session.flush()
        update_book = result.scalar_one_or_none()

        return update_book

    @classmethod
    async def delete_book(cls, book_id: int, user_id, session: AsyncSession) -> Books | None:
        query = delete(Books).where(Books.owner_id == user_id, Books.id == book_id).returning(Books)
        result = await session.execute(query)

        await session.flush()

        delete_book = result.scalar_one_or_none()
        return delete_book
