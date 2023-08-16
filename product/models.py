from datetime import datetime
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, DateTime


class ProductBase(SQLModel):
    name: str | None = Field(nullable=True)
    url: str | None = Field(nullable=True)
    price: float | None = Field(nullable=True)
    old_price: float | None = Field(nullable=True)
    order_count: float | None = Field(nullable=True)
    celler_sold: int | None = Field(nullable=True)
    celler_rating: float | None = Field(nullable=True)
    name_comp: str | None = Field(nullable=True)
    celler_mean_delivery_time: float | None = Field(nullable=True)
    celler_percent_bad_products: float | None = Field(nullable=True)
    celler_working_time: str | None = Field(nullable=True)
    celler_link: str | None = Field(nullable=True)
    img_link: str | None = Field(nullable=True)
    description: str | None = Field(nullable=True)
    text_params: str | None = Field(nullable=True)
    comments_link: str | None = Field(nullable=True)
    search_category: str | None = Field(nullable=True)


class Product(ProductBase, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    created_datetime: datetime | None = Field(sa_column=Column(DateTime, default=datetime.utcnow))


class ProductCreate(ProductBase):
    pass


class ProductRead(Product):
    pass
