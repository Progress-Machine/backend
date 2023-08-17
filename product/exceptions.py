from fastapi import HTTPException, status


class ProductNotExist(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail="A product not exists")
