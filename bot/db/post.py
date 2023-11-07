import datetime
import enum

import logging
import os

from sqlalchemy import Column, Integer, VARCHAR, Float, DATE, \
    create_engine  # type: ignore
from sqlalchemy.dialects.mysql import TEXT
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import relationship, sessionmaker, Session, RelationshipProperty, declarative_base  # type: ignore
import pandas as pd
from bot.db.base import BaseModel


class PRType(enum.Enum):
    """
        Типы раскрутки
    """
    NONE = 0  # не установлен
    CLICKS = 1  # переходы по ссылке
    PUBLICATIONS = 2  # публикации


Base_post = declarative_base()


class Post(BaseModel):
    __table_args__ = {'extend_existing': True}

    """Модель поста"""
    __tablename__ = 'posts'

    # ID поста
    id = Column(Integer, autoincrement=True, primary_key=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(TEXT, nullable=False)
    username = Column(VARCHAR(120))
    fullname = Column(VARCHAR(32))
    group_name = Column(VARCHAR(50))
    date = Column(DATE, default=datetime.datetime.now().date())
    time = Column(VARCHAR(50), default=datetime.datetime.now().time().strftime("%H:%M:%S"))

    # author_id = Column(Integer, ForeignKey('users.user_id'))


async def create_post(
        session_maker: sessionmaker,
        latitude: float,
        longitude: float,
        address: str,
        username: str,
        fullname: str,
        group_name: str

) -> None:
    async with session_maker() as session:
        async with session.begin():
            post = Post(
                latitude=latitude,
                longitude=longitude,
                address=address,
                username=username,
                fullname=fullname,
                group_name=group_name
            )

            try:
                session.add(post)
                await session.commit()
            except ProgrammingError as e:
                logging.error(e)
                return None
            else:
                return None


# async def get_post(post_id: int, session_maker: sessionmaker) -> Post:
#     async with session_maker() as session:
#         async with session.begin():
#             res = await session.execute(
#                 select(Post).where(Post.id == post_id, Post.created == datetime.datetime.date()))
#             res: res.scalars()
#             return res


def create_exl() -> str:
    """
    Create exl file from Post table
    :return: str
    """
    full_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'saved_exl')
    if not os.path.exists(full_path):
        os.makedirs(full_path)

    file_path = os.path.join(full_path, f'{str(datetime.datetime.now().date())}.xlsx')
    db: str = os.getenv('db')
    pd.read_sql(
        f"""SELECT public.posts.fullname,public.posts.username, public.posts.address, public.posts.group_name,
        public.posts.date, public.posts.time, public.posts.latitude, public.posts.longitude
        FROM public.posts WHERE public.posts.date = '{str(datetime.datetime.now().date())}'""",
        create_engine(db))\
        .drop_duplicates(subset=['address', 'username', 'fullname', 'group_name'])\
        .rename(columns={'latitude': 'широта',
                         'longitude': 'долгота',
                         'address': 'адрес',
                         'username': 'имя пользователя',
                         'fullname': 'полное имя',
                         'date': 'дата',
                         'time': 'время',
                         'group_name': 'группа'}) \
        .to_excel(file_path, index=False)

    return str(file_path).replace('\\', '/')