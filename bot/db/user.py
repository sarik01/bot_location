import datetime

from sqlalchemy import Column, VARCHAR, BigInteger, Date, select, Integer, ForeignKey
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

            print(res.user_id)
    return res


