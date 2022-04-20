from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from web_app.config import load_config

settings = load_config()

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
