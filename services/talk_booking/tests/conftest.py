from typing import Generator

import psycopg2
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from web_app.config import load_config
from web_app.main import app
from web_app.migrations import downgrade_migrations, upgrade_migrations


@pytest.fixture(scope="session")
def database_session():
    app_config = load_config()
    dsn_parts = app_config.SQLALCHEMY_DATABASE_URI.split("/")
    database_name = dsn_parts[-1]
    dsn = "/".join(
        dsn_parts[:-1] + ["postgres"]
    )  # to login to postgres database instead of application one
    con = psycopg2.connect(dsn)
    con.autocommit = True
    cur = con.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {database_name};")
    cur.execute(f"CREATE DATABASE {database_name};")

    app_config = load_config()
    dsn = app_config.SQLALCHEMY_DATABASE_URI
    engine = create_engine(dsn, echo=False)
    db = sessionmaker(bind=engine)()
    upgrade_migrations(dsn)
    yield db
    db.close()
    downgrade_migrations(dsn)
    engine.dispose()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
