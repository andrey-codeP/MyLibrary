from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from database.connections import new_sessions


async def get_db():
    async with new_sessions() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollbacl()
            raise e
SessionDup = Annotated[AsyncSession, Depends(get_db)]