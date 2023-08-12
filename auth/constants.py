from datetime import timedelta

from passlib.context import CryptContext
from load_env import load_env
from os import environ

load_env()
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = environ.get("SECRET_KEY")
ALGORITHM = environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = timedelta(minutes=int(environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")))
REFRESH_TOKEN_EXPIRE_HOURS = timedelta(hours=int(environ.get("REFRESH_TOKEN_EXPIRE_HOURS")))
