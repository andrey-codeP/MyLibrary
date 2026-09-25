from datetime import datetime, timezone
from sqlalchemy import select, delete


from database.models.base import Base
from database.models.tokens import Tokens
from database.depends import SessionDep

from security.auth import get_hash_password


class TokenRepository:
    @classmethod
    async def create_token(
        cls, user_id: int, hashed_token: str, expires_at: datetime, session: SessionDep
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
        cls, hashed_token: str, session: SessionDep
    ) -> Tokens | None:

        quary = session.select(Tokens).where(Tokens.hashed_token == hashed_token)
        result = await session.execute(quary)
        token = result.scalar_one_or_none()

        return token

    @classmethod
    async def delete_by_hashed_token(
        cls, hashed_token: str, session: SessionDep
    ) -> bool:

        result = await session.execute(
            delete(Tokens).where(Tokens.hashed_token == hashed_token)
        )

        return result.rowcount > 0

    @classmethod
    async def delete_by_user_id(cls, user_id: int, session: SessionDep) -> None:
        result = await session.execute(delete(Tokens).where(Tokens.user_id == user_id))
