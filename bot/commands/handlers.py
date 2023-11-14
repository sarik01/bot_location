"""

"""
import asyncio
import datetime
from aiogram.types import ChatMemberUpdated
from bot.commands.utils import location_from_api, do_query, allowed_users
from bot.db.post import create_post
from sqlalchemy.orm import sessionmaker
from aiogram import types
from bot.db.user import create_user


async def on_chat_member_updated(message: types.Message, session_maker: sessionmaker) -> None:
    """

    :param message:
    :param session_maker:
    :return:
    """
    for new__member in message.new_chat_members:

        if new__member.id == message.bot.id:
            if message.from_user.id in allowed_users:
                # Бот был добавлен в группу
                chat_id = message.chat.id
                await message.bot.send_message(chat_id, "Спасибо за добавление меня в группу!")
                # Здесь вы можете выполнить дополнительные действия, если бот был добавлен в группу
                break
            await message.chat.leave()
        else:
            await create_user(user_id=new__member.id, username=new__member.username, full_name=new__member.full_name,
                              first_name=new__member.first_name, session_maker=session_maker, message=message)


async def new_member(event: ChatMemberUpdated, session_maker: sessionmaker) -> None:
    """

    :param event:
    :param session_maker:
    :return:
    """
    await create_user(user_id=event.from_user.id, username=event.from_user.username,
                      full_name=event.from_user.full_name,
                      first_name=event.from_user.first_name, session_maker=session_maker, message=event)


async def start(message: types.Message) -> None:
    """

    :param message:
    :return:
    """
    await message.answer('Welcome!')


async def get_location(message: types.Message, session_maker: sessionmaker) -> None:
    """

    :param message:
    :param session_maker:
    :return:
    """
    if message.chat.type == 'group':
        lat = message.location.latitude
        lon = message.location.longitude
        task = asyncio.create_task(location_from_api(lat, lon))
        location = await asyncio.gather(task)
        location_address = location[0]['display_name']
        print(datetime.datetime.now())
        await create_post(latitude=lat,
                          longitude=lon,
                          session_maker=session_maker,
                          address=location_address,
                          group_name=message.chat.full_name,
                          author_id=message.from_user.id,)


async def send_exl(message: types.Message) -> None:
    """

    :param message:
    :return:
    """

    query = f"""SELECT public.users.username, public.users.fullname, public.posts.address, public.posts.group_name,
    public.posts.date as date, public.posts.time, public.posts.latitude, public.posts.longitude
    FROM public.posts RIGHT JOIN public.users on public.posts.author_id = public.users.user_id
    AND public.posts.date = '{datetime.datetime.now().date()}'
    OR public.posts.date IS NULL
    """
    await do_query(query=query, message=message, archive=False)


async def send_archive_exl(message: types.Message):
    """

    :param message:
    :return:
    """

    query = """SELECT public.users.username, public.users.fullname, public.posts.address, public.posts.group_name,
    public.posts.date, public.posts.time, public.posts.latitude, public.posts.longitude
    FROM public.posts JOIN public.users on public.posts.author_id = public.users.user_id """
    await do_query(query=query, message=message, archive=True)

#
