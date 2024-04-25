from fastapi import FastAPI
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware


def register_mysql(app: FastAPI, db_url, **kwargs):
    app.add_middleware(
        SQLAlchemyMiddleware,
        db_url=db_url,
        **kwargs
    )
