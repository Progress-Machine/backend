from fastapi import APIRouter, Depends

from auth.dependencies import validate_access_token
from database import get_session
from product.models import ProductRead
from product.services import get_text_from_gpt, get_product_from_wb

router = APIRouter()


@router.get("/product/gpt", dependencies=[Depends(validate_access_token)])
def gpt_text(mode: str, description: str):
    return get_text_from_gpt(mode=mode, description=description)


@router.post("/product", dependencies=[Depends(validate_access_token)], response_model=ProductRead)
async def get_statistic(product_url: str, session=Depends(get_session)):
    return await get_product_from_wb(product_url=product_url, session=session)
