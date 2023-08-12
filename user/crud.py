from pydantic import EmailStr
from sqlalchemy.orm import Session

from user.models import User


def get_detail_by_email(session: Session, email: EmailStr) -> User | None:
    return session.query(User).where(User.email == email).first()
