from fastapi import APIRouter, Depends

from auth.dependencies import validate_access_token
from database import get_session
from product.dependencies import product_exist
from product.models import ProductRead, Product, ProductCreate
from product.services import get_text_from_gpt, get_product_from_wb, get_product_list, \
    get_product_stat, product_analytics
from user.models import User

router = APIRouter()


@router.get("/product/gpt", dependencies=[Depends(validate_access_token)])
async def gpt_text(mode: str, description: str):
    return get_text_from_gpt(mode=mode, description=description)


@router.post("/product", response_model=ProductRead)
async def get_statistic(product_url: str, user: User = Depends(validate_access_token),
                        session=Depends(get_session)):
    return await get_product_from_wb(product_url=product_url, user=user, session=session)


@router.get("/product", response_model=list[ProductRead])
def get_products(user: User = Depends(validate_access_token), session=Depends(get_session)):
    return get_product_list(user=user, session=session)


@router.get("/product/{product_id}")
async def get_product(product: Product = Depends(product_exist)):
    return await get_product_stat(product)


@router.post("/product/analytics", dependencies=[Depends(validate_access_token)])
async def get_new_analytic(product: ProductCreate):
    return product_analytics(product)
