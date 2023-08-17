from sqlalchemy import desc
from sqlalchemy.orm import Session

from product.models import ProductCreate, Product


def create_product(session: Session, product_create: ProductCreate) -> Product:
    product = Product.from_orm(product_create)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


def get_products(session: Session, user_id: int) -> list[Product]:
    return session.query(Product).where(Product.user_id == user_id).order_by(
        desc(Product.created_datetime)).all()


def get_product(session: Session, product_id: int) -> Product | None:
    return session.query(Product).where(Product.id == product_id).first()
