from fastapi import APIRouter, Depends, Header

from auth.models import Token
from user.dependencies import user_by_email
from user.models import User
from auth.services import login_user

router = APIRouter()


@router.get("/auth/login", response_model=Token)
def login(user: User = Depends(user_by_email), password: str = Header()):
    return login_user(user=user, password=password)
