from database.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey




class Books(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]
    year: Mapped[int]
    pages: Mapped[int]  # page count
    is_read: Mapped[bool | None] = mapped_column(default=False, server_default="false")

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    owner: Mapped["UserTable"] = relationship(back_populates="books")
