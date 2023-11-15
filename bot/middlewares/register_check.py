from typing import Callable, Dict, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select, CursorResult

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from bot.db.user import User


class RegisterCheck(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any]
    ) -> Any:
        session_maker: sessionmaker = data['session_maker']
        async with session_maker() as session:

            session: AsyncSession
            result = await session.execute(select(User).where(User.user_id == event.from_user.id))
            result: CursorResult
            user = result.scalar_one_or_none()

            if user is not None:
                user.group_name = event.chat.full_name
                await session.commit()
            else:
                user = User(
                    user_id=event.from_user.id,
                    username=event.from_user.username,
                    fullname=event.from_user.full_name,
                    group_name=event.chat.full_name
                )

                await session.merge(user)

        return await handler(event, data)
