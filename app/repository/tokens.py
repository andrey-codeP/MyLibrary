from datetime import datetime
from sqlalchemy import select, delete

from app.database.models.tokens import Tokens
from sqlalchemy.ext.asyncio import AsyncSession


class TokenRepository:
    @classmethod
    async def create_token(
        cls,
        user_id: int,
        hashed_token: str,
        expires_at: datetime,
        session: AsyncSession,
    ) -> Tokens:
        token = Tokens(
            user_id=user_id, hashed_token=hashed_token, expires_at=expires_at
        )

        session.add(token)

        await session.flush()
        await session.refresh(token)

        return token

    @classmethod
    async def get_by_hashed_token(
        cls, hashed_token: str, session: AsyncSession
    ) -> Tokens | None:

        quary = select(Tokens).where(Tokens.hashed_token == hashed_token)
        result = await session.execute(quary)
        token = result.scalar_one_or_none()

        return token

    @classmethod
    async def delete_by_hashed_token(
        cls, hashed_token: str, session: AsyncSession
    ) -> bool:

        result = await session.execute(
            delete(Tokens).where(Tokens.hashed_token == hashed_token)
        )

        return result.rowcount > 0

    @classmethod
    async def delete_by_user_id(cls, user_id: int, session: AsyncSession) -> None:
        await session.execute(delete(Tokens).where(Tokens.user_id == user_id))

    @classmethod
    async def rotate(
        cls,
        token: Tokens,
        new_hashed_token: str,
        new_expires_at: datetime,
        session: AsyncSession,
    ) -> Tokens:
        token.hashed_token = new_hashed_token
        token.expires_at = new_expires_at

        # Не обязателен: token уже загружен этой session.
        # Но оставляем явно, чтобы было понятно, где объект отслеживается.
        session.add(token)

        await session.flush()

        return token
