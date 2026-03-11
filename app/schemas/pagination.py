from typing import TypeVar, List, Generic
from pydantic import BaseModel


T = TypeVar('T')


class PaginationResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int

    class Config:
        from_attributes = True
