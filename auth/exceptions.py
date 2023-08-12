from fastapi import HTTPException, status


class IncorrectPassword(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect password")
