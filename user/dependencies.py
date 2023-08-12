from fastapi import Depends, Header
from pydantic import EmailStr

from database import get_session
from user.exceptions import UserNotExist, UserExistWithEmail
from user.models import User, UserCreate
from user.crud import get_detail_by_email


def user_exist(user_create: UserCreate, session=Depends(get_session)) -> UserCreate:
    user = get_detail_by_email(session=session, email=user_create.email)
    if user is not None:
        raise UserExistWithEmail
    return user_create


def user_by_email(email: EmailStr = Header(), session=Depends(get_session)) -> User:
    user = get_detail_by_email(session=session, email=email)
    if user is None:
        raise UserNotExist
    return user
