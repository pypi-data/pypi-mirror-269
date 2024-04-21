from functools import lru_cache

from sqlalchemy import Engine
from sqlmodel import create_engine as create_engine_from_sqlmodel, SQLModel, Session, select

from mydev.agent.models import User
from mydev.pm import models as pm_models  # noqa
from mydev.utils.constants import MYDEV_DB_URL


@lru_cache()
def create_engine(db_url: str = MYDEV_DB_URL) -> Engine:
    return create_engine_from_sqlmodel(db_url)


def init_db(db_url: str = MYDEV_DB_URL):
    engine = create_engine(db_url)
    SQLModel.metadata.create_all(engine)


def create_user(username: str) -> User:
    engine = create_engine()
    user = User(name=username)
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
    return user


def get_user_by_name(username: str) -> User:
    engine = create_engine()
    with Session(engine) as session:
        statement = select(User).where(User.name == username)
        user = session.exec(statement).first()
    return user
