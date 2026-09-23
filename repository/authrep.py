from datetime import datetime, timezone
from sqlalchemy import select


from database.models.base import UserBase
from database.models.user_table import UserTable
from schemas.user import UserInDb
from database.depends import SessionDep

from security.auth import get_hash_password




class AuthUserRepository:
    @classmethod
    async def create_user(cls, user_for_reg: UserInDb, session: SessionDep) -> UserTable:
        user_data = user_for_reg.model_dump()
        plained_password = user_data.pop("password")

        hashed_password = get_hash_password(plained_password)
        created_at = datetime.now(timezone.utc)

        user_data.update(
            {"hashed_password": hashed_password,
             "created_at": created_at}
        )

        user = UserTable(**user_data)

        session.add(user)

        await session.commit()
        await session.refresh(user)

        return user


    @classmethod
    async def get_user_by_id(cls, user_id: int, session: SessionDep):
        query = select(UserTable).where(UserTable.id == user_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        return user


    @classmethod
    async def get_user_by_username(cls, username: str, session: SessionDep):
        query = select(UserTable).where(UserTable.username == username)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        return user