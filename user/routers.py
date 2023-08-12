from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_session
from user.dependencies import user_exist
from user.models import UserCreate, UserRead
from user.services import create as user_create

router = APIRouter()


@router.post("/user", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create(user: UserCreate = Depends(user_exist), session: Session = Depends(get_session)):
    return user_create(user=user, session=session)
