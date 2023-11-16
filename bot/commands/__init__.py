__all__ = ['register_user_commands', 'BotCommand', 'bot_commands']

from aiogram import Router
from aiogram.filters import Command, ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER
from aiogram.utils.chat_action import ChatActionMiddleware

from bot.commands.callback_data import TestCallbackData
from bot.commands.handlers import (start, get_location, send_exl, send_archive_exl, new_member,
                                   on_chat_member_updated
                                   )
from bot.commands.bot_commands import bot_commands
from aiogram.types import BotCommand
from aiogram import F
from bot.middlewares.register_check import RegisterCheck


def register_user_commands(router: Router) -> None:
    router.message.register(start, Command(commands=['start']))
    router.message.register(get_location, F.location, flags={'chat_action': 'record_voice'})
    router.message.register(send_exl, Command(commands='get'),
                            flags={'chat_action': 'upload_document'})
    router.message.register(send_archive_exl, Command(commands=['archive']),
                            flags={'chat_action': 'upload_document'})
    router.chat_member.register(new_member, ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
    router.message.register(on_chat_member_updated, F.new_chat_members)

    # middleware
    router.message.middleware(RegisterCheck())
    router.message.middleware(ChatActionMiddleware())
    router.callback_query.middleware(RegisterCheck())
