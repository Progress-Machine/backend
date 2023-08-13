from fastapi import Depends

from database import get_session
from user.crud import get_detail_by_id
from user.exceptions import UserNotExist
from user.models import User
from auth.constants import oauth2_scheme
from auth.services import decode_token


def validate_access_token(access_token: str = Depends(oauth2_scheme),
                          session=Depends(get_session)) -> User:
    user_id = decode_token(access_token)
    user = get_detail_by_id(session=session, user_id=user_id)
    if user is None:
        raise UserNotExist
    return user
