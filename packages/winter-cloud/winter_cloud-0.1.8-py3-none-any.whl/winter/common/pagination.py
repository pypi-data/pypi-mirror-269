from typing import Optional, Any, Generic, TypeVar, Sequence

from fastapi_pagination import Params, Page, set_page
from fastapi_pagination.ext.sqlmodel import paginate  # noqa
from fastapi_pagination.bases import BasePage, AbstractParams
from fastapi_pagination.types import GreaterEqualOne, GreaterEqualZero
from fastapi_pagination.utils import create_pydantic_model
from math import ceil
from pydantic import Field


class PagingParams(Params):
    """ 页码 """
    size: int = Field(20, alias="pageSize", description="每页条数")


T = TypeVar("T")


class Pagination(BasePage[T], Generic[T]):
    page: Optional[GreaterEqualOne]
    pageSize: Optional[GreaterEqualOne]
    totalPage: Optional[GreaterEqualZero] = None
    totalItems: Optional[GreaterEqualZero] = None

    __params_type__ = PagingParams

    @classmethod
    def create(
            cls,
            items: Sequence[T],
            params: AbstractParams,
            *,
            total: Optional[int] = None,
            **kwargs: Any,
    ) -> Page[T]:
        if not isinstance(params, Params):
            raise TypeError("Page should be used with Params")

        size = params.size if params.size is not None else total
        page = params.page if params.page is not None else 1

        if size == 0:
            pages = 0
        elif total is not None:
            pages = ceil(total / size)
        else:
            pages = None

        return create_pydantic_model(
            cls,
            total=total,
            totalItems=total,
            items=items,
            page=page,
            pageSize=size,
            totalPage=pages,
            **kwargs,
        )


set_page(Pagination)
