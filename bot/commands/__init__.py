__all__ = ['register_user_commands', 'BotCommand', 'bot_commands']

from aiogram import Router
from aiogram.filters import Command

from bot.commands.callback_data import TestCallbackData
from bot.commands.start import (start, get_location, get_contact, send_exl, send_archive_exl
                                )
from bot.commands.bot_commands import bot_commands
from aiogram.types import BotCommand
from bot.commands.help import help_command, help_func, call_help_func, clear_call_help_func
from aiogram import F
from bot.commands.settings import settings_command, settings_callback
from bot.middlewares.register_check import RegisterCheck


def register_user_commands(router: Router) -> None:
    router.message.register(start, Command(commands=['start']))
    router.message.register(help_command, Command(commands=['help']))
    router.message.register(start, F.text == 'Start')
    router.message.register(help_func, F.text == 'Pomosh')
    router.message.register(settings_command, F.text == 'settings')
    router.message.register(get_location, F.location)
    router.message.register(get_contact, F.contact)
    router.message.register(send_exl, Command(commands=['get']))
    router.message.register(send_archive_exl, Command(commands=['archive']))
    # router.message.register(menu_posts, F.text == 'post')
    #
    # #FSM
    # router.callback_query.register(menu_post_create, F.data == 'createpost', PostStates.waiting_for_select)
    # router.message.register(menu_post_text, PostStates.waiting_for_text)
    # router.message.register(menu_post_url, PostStates.waiting_for_url)
    # router.callback_query.register(menu_post_get, F.data.startwith('getpost'), PostStates.waiting_for_select)

    # Callback
    router.callback_query.register(call_help_func, F.data == 'pzdc')
    # router.callback_query.register(clear_call_help_func, F.data == 'clear')
    router.callback_query.register(settings_callback, TestCallbackData.filter())

    # middleware
    router.message.middleware(RegisterCheck())
    router.callback_query.middleware(RegisterCheck())
