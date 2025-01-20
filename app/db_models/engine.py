from os import getenv

from sqlalchemy import Engine, create_engine

engine = create_engine(getenv("DB_CONNECTION_STRING") or "", echo=True)


def get_engine() -> Engine:
    return engine
