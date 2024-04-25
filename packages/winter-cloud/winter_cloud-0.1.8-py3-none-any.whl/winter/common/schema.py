from typing import TypeVar, Generic

from pydantic import BaseModel

T = TypeVar('T')
D = TypeVar('D')


class RestfulResponse(BaseModel, Generic[T]):
    code: int = 200
    message: str = 'success'
    data: T


class RestfulPageResponse(BaseModel, Generic[D]):
    code: int = 200
    message: str = 'success'
    page: int = 1
    pageSize: int = 0
    totalItems: int = 0
    totalPage: int = 0
    items: D
