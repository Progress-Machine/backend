from sqlmodel import SQLModel

from user.models import User


class Token(SQLModel):
    access_token: str
    refresh_token: str
    user: User
