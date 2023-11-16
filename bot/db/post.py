import datetime
import logging
import os
from sqlalchemy import Column, Integer, VARCHAR, Float, DATE, \
    create_engine, Index, ForeignKey, BigInteger  # type: ignore
from sqlalchemy.dialects.mysql import TEXT
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import relationship, sessionmaker, Session, RelationshipProperty, declarative_base  # type: ignore
import pandas as pd
from bot.db.base import BaseModel


def get_time(utc, date=True):
    time = utc + datetime.timedelta(hours=5)
    if date:
        return time.date()
    return time.time().strftime("%H:%M:%S")


class Post(BaseModel):
    __table_args__ = {'extend_existing': True}

    """Модель поста"""
    __tablename__ = 'posts'

    # ID поста
    id = Column(Integer, autoincrement=True, primary_key=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(TEXT, nullable=False)
    group_name = Column(VARCHAR(50))
    date = Column(DATE, index=True)
    time = Column(VARCHAR(50))

    author_id = Column(BigInteger, ForeignKey('users.user_id'))


date_index = Index('date_index', Post.date)


async def create_post(
        session_maker: sessionmaker,
        latitude: float,
        longitude: float,
        address: str,
        group_name: str,
        author_id: int,


) -> None:
    async with session_maker() as session:
        async with session.begin():
            post = Post(
                latitude=latitude,
                longitude=longitude,
                address=address,
                group_name=group_name,
                author_id=author_id,
                date=get_time(utc=datetime.datetime.utcnow()),
                time=get_time(utc=datetime.datetime.utcnow(), date=False)
            )

            try:
                session.add(post)
                await session.commit()
            except ProgrammingError as e:
                logging.error(e)
                return None
            else:
                return None


def create_exl(query, archive: bool = False) -> str:
    """
    Create exl file from Post table
    :return: str
    """
    full_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'saved_exl')
    if not os.path.exists(full_path):
        os.makedirs(full_path)

    db: str = os.getenv('db')
    df = pd.read_sql(
        query,
        create_engine(db)) \
        .drop_duplicates(subset=['address', 'username', 'fullname', 'group_name', 'date']) \
        .rename(columns={'latitude': 'широта',
                         'longitude': 'долгота',
                         'address': 'адрес',
                         'username': 'имя пользователя',
                         'fullname': 'полное имя',
                         'date': 'дата',
                         'time': 'время',
                         'group_name': 'группа'}).fillna(value={'широта': 'empty',
                                                                'долгота': 'empty',
                                                                'адрес': 'empty',
                                                                'имя пользователя': 'empty',
                                                                'полное имя': 'empty',
                                                                'дата': datetime.datetime.now().date().strftime("%Y-%m-%d"),
                                                                'время': 'empty',
                                                                'группа': 'empty'
                                                                })
    date: str = datetime.datetime.now().date().strftime("%Y-%m-%d")
    if archive:
        file_path = os.path.join(full_path,
                                 f'{str(min(df["дата"])) + " -- " + date}.xlsx')
    else:
        file_path = os.path.join(full_path, f'{date}.xlsx')
    df.to_excel(file_path, index=False)
    return str(file_path).replace('\\', '/')
