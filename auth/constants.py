from datetime import timedelta
from os import environ

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from load_env import load_env

load_env()
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = environ.get("SECRET_KEY")
ALGORITHM = environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = timedelta(minutes=int(environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")))
REFRESH_TOKEN_EXPIRE_HOURS = timedelta(hours=int(environ.get("REFRESH_TOKEN_EXPIRE_HOURS")))
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
