from typing import Optional

from loguru import logger
from fastapi import Depends
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.testing.pickleable import User

from app.database.base import database_client
from app.model.user import User


class LoginRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email_or_name(self, email: Optional[str], username: Optional[str]) -> Optional[User]:
        if email:
            result: Result = await self.db.execute(select(User).where(User.email == email))
        elif username:
            result: Result = await self.db.execute(select(User).where(User.username == username))
        else:
            return
        current_user: User = result.scalars().first()
        return current_user

    async def add_user(self, user: User) -> Optional[User]:
        try:
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
        except Exception as ex:
            await self.db.rollback()
            logger.error(ex)
            raise ex
        return user


async def get_repository(db: AsyncSession = Depends(database_client.get_db)) -> LoginRepository:
    return LoginRepository(db)
