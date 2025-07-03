from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from functools import wraps
from typing import TypeVar


T = TypeVar("T")


def handle_db_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except IntegrityError as e:
            msg = str(e.orig).lower()
            if "foreign key" in msg:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Foreign key mistakes.",
                )
            if "unique" in msg:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Object already exists.",
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad data.",
            )
        # except Exception as e:
        #     # Для разработки — показать ошибку полностью
        #     raise HTTPException(status_code=500, detail=str(e))

    return wrapper


def get_or_404(obj: T, message: str = "Not found") -> T:
    if obj is None:
        raise HTTPException(status_code=404, detail=message)
    return obj
