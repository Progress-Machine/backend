from sqlalchemy.orm import Session

from auth.constants import PWD_CONTEXT
from user.exceptions import UserUnknownError
from user.models import User, UserCreate


def create(session: Session, user: UserCreate) -> User:
    try:
        d_user = user.dict()
        d_user["hashed_password"] = PWD_CONTEXT.hash(user.password)
        del d_user["password"]
        db_user = User(**d_user)
        session.add(db_user)
        session.commit()
    except Exception as error:
        raise UserUnknownError(error=str(error))
    return db_user
