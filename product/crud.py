from sqlalchemy.orm import Session

from product.models import ProductCreate, Product


def create_product(session: Session, product_create: ProductCreate) -> Product:
    product = Product.from_orm(product_create)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product
