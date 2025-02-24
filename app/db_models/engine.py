from os import getenv

from dotenv import load_dotenv
from sqlalchemy import Engine, create_engine

load_dotenv()

engine = create_engine(getenv("DB_CONNECTION_STRING") or "", echo=True)


def get_engine() -> Engine:
    return engine
