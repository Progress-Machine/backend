import time
from sqlmodel import SQLModel
from load_env import load_env
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import environ

load_env()
if environ.get("PRODUCTION") == "true":
    time.sleep(10)
engine = create_engine(environ.get("DATABASE_URL"))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
if environ.get("INIT_TABLES") == "true":
    from user import models
    from product import models

    SQLModel.metadata.create_all(engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
