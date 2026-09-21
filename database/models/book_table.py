from database.models.base import BookBase
from sqlalchemy.orm import Mapped, mapped_column


class Books(BookBase):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]
    year: Mapped[int]
    pages: Mapped[int]  # page count
    is_read: Mapped[bool | None] = mapped_column(default=False, server_default="false")
