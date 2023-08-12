from datetime import datetime
from pydantic import EmailStr
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, DateTime


class UserBase(SQLModel):
    email: EmailStr


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    hashed_password: str | None = Field(nullable=True)
    created_datetime: datetime | None = Field(sa_column=Column(DateTime, default=datetime.utcnow))


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    email: EmailStr
    created_datetime: datetime
