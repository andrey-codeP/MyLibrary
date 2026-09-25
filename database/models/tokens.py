from database.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Uuid, String

from datetime import datetime
from uuid import UUID, uuid4


class Tokens(Base):
    __tablename__ = "tokens"

    id: Mapped[int] = mapped_column(Uuid, primary_key=True, default=uuid4)
    hashed_token: Mapped[str] = mapped_column(
        String(255), nullable=True, unique=True, index=True
    )

    expires_at: Mapped[datetime] = mapped_column(nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("UserTable", back_populates="tokens")
