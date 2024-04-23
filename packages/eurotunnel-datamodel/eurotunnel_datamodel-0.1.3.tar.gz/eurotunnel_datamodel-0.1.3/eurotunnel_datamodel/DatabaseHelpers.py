from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session
import os


def get_engine() -> Engine:
    # I set these in the compose.yaml
    db_host = os.environ["DB_HOST"]
    db_port = os.environ["DB_PORT"]
    db_name = os.environ["DB"]
    db_username = os.environ["DB_USER"]
    db_password = os.environ["DB_PASSWORD"]
    engine = create_engine(
        f"postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
    )
    return engine


def get_session() -> Session:
    return Session(get_engine())
