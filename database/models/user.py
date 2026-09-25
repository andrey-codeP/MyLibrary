from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, Boolean, func, String

from datetime import datetime, timezone
from typing import List

from database.models.base import Base


class UserTable(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(20), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    books: Mapped[List["Books"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )

    tokens: Mapped[List["Tokens"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
