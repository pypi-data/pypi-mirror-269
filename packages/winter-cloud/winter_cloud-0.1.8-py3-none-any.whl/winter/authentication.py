import json
import typing

from starlette.authentication import (
    AuthenticationError,
    UnauthenticatedUser,
    AuthCredentials
)
from starlette.authentication import BaseUser
from starlette.requests import HTTPConnection
from starlette.responses import Response
from starlette.types import ASGIApp, Receive, Scope, Send

from .common.exception import UnauthorizedException, JSONResponseWithException


class AuthUser(BaseUser):
    def __init__(self, user_id: int, user_token_id: int, authorities: typing.List[str]) -> None:
        self.id = user_id
        self.token_id = user_token_id
        self.authorities = authorities

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return f"user<{self.id}>"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "token_id": self.token_id,
            "authorities": self.authorities
        }


class AuthenticationBackend:

    async def authenticate(
            self, conn: HTTPConnection
    ) -> typing.Optional[typing.Tuple["AuthCredentials", "BaseUser"]]:
        user_id = conn.headers.get("user-id")
        user_token_id = conn.headers.get("user-token-id")

        # fix because gateway
        if _authorities := conn.headers.get("authorities"):
            authorities = json.loads(_authorities)
        else:
            authorities = []

        if user_id is None:
            raise UnauthorizedException
        return (
            AuthCredentials(),
            AuthUser(
                user_id=int(user_id),
                user_token_id=int(user_token_id),
                authorities=authorities
            )
        )


class AuthenticationMiddleware:
    def __init__(
            self,
            app: ASGIApp,
            backend: AuthenticationBackend,
            on_error: typing.Optional[
                typing.Callable[[HTTPConnection, AuthenticationError], Response]
            ] = None,
            skip_paths: typing.Optional[typing.List[str]] = None
    ) -> None:
        self.app = app
        self.backend = backend
        self.on_error: typing.Callable[
            [HTTPConnection, AuthenticationError], Response
        ] = (on_error if on_error is not None else self.default_on_error)
        self.skip_paths = skip_paths or []

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ["http", "websocket"]:
            await self.app(scope, receive, send)
            return
        if self.skip_paths and scope["path"] in self.skip_paths:
            await self.app(scope, receive, send)
            return

        conn = HTTPConnection(scope)
        try:
            auth_result = await self.backend.authenticate(conn)
        except UnauthorizedException as exc:
            response = self.on_error(conn, exc)
            if scope["type"] == "websocket":
                await send({"type": "websocket.close", "code": 1000})
            else:
                await response(scope, receive, send)
            return

        if auth_result is None:
            auth_result = AuthCredentials(), UnauthenticatedUser()
        scope["auth"], scope["user"] = auth_result
        await self.app(scope, receive, send)

    @staticmethod
    def default_on_error(conn: HTTPConnection, exc: UnauthorizedException) -> Response:
        content = {"code": exc.code, "message": exc.message}
        return JSONResponseWithException(
            status_code=exc.status_code,
            content=content
        )
