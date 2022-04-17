import psycopg2
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.talk_request_db import TalkRequestBase
from web_app.config import load_config


@pytest.fixture(scope="session")
def database():
    dsn_parts = load_config().SQLALCHEMY_DATABASE_URI.split("/")
    database_name = dsn_parts[-1]
    dsn = "/".join(
        dsn_parts[:-1] + ["postgres"]
    )  # to login to postgres database instead of application one
    con = psycopg2.connect(dsn)
    con.autocommit = True
    cur = con.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {database_name};")
    cur.execute(f"CREATE DATABASE {database_name};")


@pytest.fixture
def database_session(database):
    dsn = load_config().SQLALCHEMY_DATABASE_URI
    engine = create_engine(dsn, echo=False)
    db = sessionmaker(bind=engine)()
    TalkRequestBase.metadata.create_all(bind=engine)
    yield db
    db.close()
    TalkRequestBase.metadata.drop_all(bind=engine)
    engine.dispose()
