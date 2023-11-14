import asyncio
import logging
import os

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.redis import RedisStorage
from aioredis import Redis

from bot.config import token
from bot.commands import register_user_commands, BotCommand, bot_commands

from bot.db import create_async_engine, get_session_maker, BaseModel
from bot.db.engine import proceed_schemas


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)

    cmd_for_bot = []
    for cmd in bot_commands:
        cmd_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))

    redis = Redis(
        host=os.getenv('REDIS_HOST') or '127.0.0.1',
        password=os.getenv('REDIS_PASSWORD') or None,
        username=os.getenv('REDIS_USER') or None,
    )

    storage = RedisStorage(redis=redis)

    dp = Dispatcher(storage=storage)

    bot = Bot(token=token)
    await bot.set_my_commands(commands=cmd_for_bot)
    register_user_commands(dp)

    postgres_url = os.getenv('db_async')

    async_engine = create_async_engine(postgres_url)
    session_maker = get_session_maker(async_engine)

    await proceed_schemas(async_engine, BaseModel.metadata)

    await dp.start_polling(bot, session_maker=session_maker)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot Stopped')
