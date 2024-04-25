# -*- coding: utf-8 -*-
from typing import Optional, Any, Generic, TypeVar, List

from fastapi_async_sqlalchemy import db
from pydantic import BaseModel
from sqlmodel import select, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import Select

from .pagination import PagingParams, Pagination, paginate

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class _ServiceMetaClass(type):
    def __new__(mcs, name, bases, attrs):
        return super().__new__(mcs, name, bases, attrs)


class BaseDAO(Generic[ModelType, CreateSchemaType, UpdateSchemaType], metaclass=_ServiceMetaClass):
    database = db
    model: type[ModelType] = None
    pagination_class = None
    
    def _gen_condition(self, kwargs: dict) -> List:
        conditions = []
        for field, value in kwargs.items():
            conditions.append(getattr(self.model, field) == value)
        return conditions
    
    async def get_one(self, **kwargs) -> ModelType | None:
        query = select(self.model).where(*self._gen_condition(kwargs))
        async with self.database():
            response = await self.database.session.execute(query)
            return response.scalar_one_or_none()
    
    async def get_by_id(self, pk: Any) -> ModelType | None:
        return await self.get_one(id=pk)
    
    async def with_pagination(
            self,
            query: ModelType | Select[ModelType] | None = None,
            params: PagingParams = PagingParams()
    ) -> Pagination[ModelType]:
        """ 分页查询 """
        async with self.database():
            response = await paginate(
                self.database.session,
                query=query,
                params=params
            )
            return response
    
    async def create(self, data: CreateSchemaType | ModelType) -> ModelType:
        """创建对象"""
        data_model = self.model.from_orm(data)
        
        async with self.database():
            self.database.session.add(data_model)
            await self.database.session.commit()
            await self.database.session.refresh(data_model)
            return data_model
