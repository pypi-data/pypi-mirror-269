from fastapi import FastAPI

from winter.authentication import (
    AuthenticationMiddleware, AuthenticationBackend
)


def register_authentication(app: FastAPI):
    app.add_middleware(
        AuthenticationMiddleware,
        backend=AuthenticationBackend()
    )
