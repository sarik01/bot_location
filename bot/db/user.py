import datetime
from typing import Union

from aiogram import types
from sqlalchemy import Column, VARCHAR, BigInteger, Date, select, CursorResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker, selectinload, relationship
from .base import BaseModel


class User(BaseModel):
    """
    User model
    """
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    # Tg user id
    user_id = Column(BigInteger, unique=True, nullable=False, primary_key=True)
    username = Column(VARCHAR(120), nullable=True)
    fullname = Column(VARCHAR(32))
    posts = relationship('bot.db.post.Post', backref="author")
    created = Column(Date, default=datetime.datetime.now())
    updated = Column(Date, onupdate=datetime.datetime.now())

    def __str__(self) -> str:
        return f"<User: {self.user_id}>"


async def create_user(user_id: int, username: str, full_name: str, first_name: str,
                      session_maker: sessionmaker, message: Union[types.Message, types.ChatMemberUpdated]) -> None:
    """

    :param user_id:
    :param username:
    :param full_name:
    :param first_name:
    :param session_maker:
    :param message:
    :return:
    """
    async with session_maker() as session:
        async with session.begin():
            session: AsyncSession
            result = await session.execute(select(User).where(User.user_id == user_id))
            result: CursorResult
            user = result.one_or_none()

            if user is not None:
                pass
            else:
                user = User(
                    user_id=user_id,
                    username=username,
                    fullname=full_name
                )

                await session.merge(user)
    await message.answer(f"<b>Hi, {first_name}!</b>",
                         parse_mode="HTML")


async def get_user(user_id: int, session: sessionmaker) -> User:
    """

    :param user_id:
    :param session:
    :return:
    """

    async with session() as session:
        async with session.begin():
            result = await session.execute(
                select(User).filter(User.user_id == user_id).options(selectinload(User.posts)))
            res = result.scalar()

    return res
