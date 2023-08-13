from fastapi import APIRouter, Depends

from auth.dependencies import validate_access_token
from product.services import get_text_from_gpt

router = APIRouter()


@router.get("/product/gpt", dependencies=[Depends(validate_access_token)])
def gpt_text(mode: str, description: str):
    return get_text_from_gpt(mode=mode, description=description)
