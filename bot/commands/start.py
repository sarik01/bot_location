import asyncio
from bot.db.post import create_post, create_exl
from sqlalchemy.orm import sessionmaker
import aiohttp
from aiogram import types


# from geopy.geocoders import Nominatim
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import StatesGroup, State
#
# from aiogram.utils.keyboard import (ReplyKeyboardBuilder, ReplyKeyboardMarkup,
#                                     InlineKeyboardBuilder, InlineKeyboardMarkup,
#                                     KeyboardButton, KeyboardButtonPollType)

# from sqlalchemy import select


# from bot.commands.structures import cancel_board

# from bot.db.user import User

# geolocator = Nominatim(user_agent="maps")


async def start(message: types.Message) -> None:
    await message.answer('Welcome!')
    # menu_builder = ReplyKeyboardBuilder()
    # menu_builder.button(
    #     text='Pomosh'
    # )
    # menu_builder.add(
    #     KeyboardButton(text='Otpravit kontkt', request_contact=True),
    #     KeyboardButton(text='Otpravit locaciyu', request_location=True),
    # )
    # menu_builder.row(
    #     KeyboardButton(text='Otpravit golosovanie',
    #                    request_poll=KeyboardButtonPollType(type='quiz')),
    #     KeyboardButton(text='post')
    # )
    # await message.answer('Menu',
    #                      reply_markup=menu_builder.as_markup(resize_keyboard=True)
    #                      )


async def location_from_api(lat, lon):
    url = f'https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json&addressdetails=1'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, allow_redirects=True) as response:
            location = await response.json()

            return location


async def get_location(message: types.Message, session_maker: sessionmaker):
    lat = message.location.latitude
    lon = message.location.longitude

    task = asyncio.create_task(location_from_api(lat, lon))
    location = await asyncio.gather(task)

    await create_post(latitude=lat,
                      longitude=lon,
                      username=message.from_user.username,
                      fullname=message.from_user.full_name,
                      session_maker=session_maker,
                      address=location[0]['display_name'],
                      group_name=message.chat.full_name)
    await message.answer(location[0]['display_name'], reply_markup=types.ReplyKeyboardRemove())


async def get_contact(message: types.Message):
    reply = message.contact.phone_number
    await message.answer(reply, reply_markup=types.ReplyKeyboardRemove())


async def send_exl(message: types.Message):
    doc = create_exl()
    docs = types.FSInputFile(doc)
    await message.bot.send_document(message.from_user.id, document=docs)

    # await message.answer_location(latitude=41.305106, longitude=69.27248)

#
# # FSM
#
#
# class PostStates(StatesGroup):
#     """
#
#     """
#
#     waiting_for_select = State()
#     waiting_for_text = State()
#     waiting_for_url = State()
#     waiting_for_budget = State()
#     waiting_for_pr_type = State()
#     waiting_for_price_url = State()
#     waiting_for_price_publication = State()
#     waiting_for_subs_min = State()
#
#
# async def menu_posts(message: types.Message, session_maker: sessionmaker, state: FSMContext) -> None:
#     """
#
#     :param message:
#     :param session:
#     :return:
#     """
#     print('ffff')
#     post_keyboard = InlineKeyboardBuilder()
#
#     async with session_maker() as session:
#         async with session.begin():
#             result = await session.execute(
#                 select(User).where(User.user_id == message.from_user.id).options(selectinload(User.posts)))
#             user = result.scalar()
#             print(user.posts)
#             for post in user.posts:
#                 post_keyboard.button(text=post.text[:20], callback_data='getpost' + str(post.id))
#             post_keyboard.button(text='Create post', callback_data='createpost')
#             post_keyboard.adjust(1)
#             await message.answer('Your Posts', reply_markup=post_keyboard.as_markup())
#             await state.set_state(PostStates.waiting_for_select)
#
#
# async def menu_post_create(message: types.CallbackQuery, state: FSMContext) -> None:
#     """
#
#     :param message:
#     :return:
#     """
#     await state.set_state(PostStates.waiting_for_text)
#
#     await message.message.answer('Send text of new post', reply_markup=cancel_board())
#
#
# async def menu_post_text(message: types.Message, state: FSMContext) -> None:
#     """
#
#     :param message:
#     :param state:
#     :return:
#     """
#     if message.text == 'cancel':
#         await state.clear()
#         return await start(message)
#
#     await state.update_data(post_text=message.text)
#     await state.set_state(PostStates.waiting_for_url)
#     await message.answer('Ok, now send me url', reply_markup=cancel_board())
#
#
# async def menu_post_url(message: types.Message, state: FSMContext) -> None:
#     """
#
#     :param message:
#     :param state:
#     :return:
#     """
#     if message.text == 'cancel':
#         await state.clear()
#         return await start(message)
#
#     if message.text == 'back':
#         await state.set_state(PostStates.waiting_for_text)
#         await message.answer('Send text of new post', reply_markup=cancel_board())
#
#     else:
#         await state.update_data(post_url=message.text)
#         await state.set_state(PostStates.waiting_for_pr_type)
#         rkm_builder = ReplyKeyboardBuilder()
#         rkm_builder.button(text='Oplata po publikaciyam')
#         rkm_builder.button(text='Oplata za perehod publicacii')
#         await message.answer('Teper varian raskrutki', reply_markup=rkm_builder.as_markup(resize_keyboard=True))
#
#
# async def menu_post_get(message: types.Message) -> None:
#     """
#
#     :param message:
#     :return:
#     """
