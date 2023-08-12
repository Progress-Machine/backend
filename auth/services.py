from datetime import datetime
from jose import jwt

from auth.exceptions import IncorrectPassword
from auth.constants import *
from auth.models import Token
from user.models import User


def _create_token(data: dict, expires_delta: timedelta) -> str:
    expire = datetime.utcnow() + expires_delta
    data["exp"] = expire
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def login_user(user: User, password: str) -> Token:
    if not PWD_CONTEXT.verify(password, user.hashed_password):
        raise IncorrectPassword
    access_token_data = {"sub": str(user.id)}
    access_token = _create_token(access_token_data, ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token = _create_token({"sub": str(user.id), "access": access_token},
                                  REFRESH_TOKEN_EXPIRE_HOURS)
    return Token(access_token=access_token, refresh_token=refresh_token, user=user)
