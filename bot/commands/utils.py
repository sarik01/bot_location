import aiohttp
from aiogram import types

from bot.db.post import create_exl


async def location_from_api(lat, lon) -> dict:
    """

    :param lat:
    :param lon:
    :return:
    """
    url = f'https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json&addressdetails=1'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, allow_redirects=True) as response:
            location = await response.json()

            return location


async def do_query(query, message: types.Message, archive: bool):
    if message.chat.type == 'private':
        doc = create_exl(query, archive)
        docs = types.FSInputFile(doc)

        await message.bot.send_document(message.from_user.id, document=docs)
