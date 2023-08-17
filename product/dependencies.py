from fastapi import Depends

from auth.dependencies import validate_access_token
from database import get_session
from product.crud import get_product
from product.exceptions import ProductNotExist
from product.models import Product
from user.models import User


def product_exist(product_id: int, user: User = Depends(validate_access_token),
                  session=Depends(get_session)) -> Product:
    product = get_product(product_id=product_id, session=session)
    if product is None or product.user_id != user.id:
        raise ProductNotExist
    return product
