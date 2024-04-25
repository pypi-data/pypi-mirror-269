from typing import Optional, Dict, Any

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic_core import ValidationError  # noqa
from starlette.background import BackgroundTask
from starlette.status import HTTP_400_BAD_REQUEST
from starlette.types import Receive, Scope, Send


class JSONResponseWithException(JSONResponse):
    def __init__(
            self,
            content: Any,
            status_code: int = 200,
            headers: Optional[Dict[str, str]] = None,
            media_type: Optional[str] = None,
            background: Optional[BackgroundTask] = None,
            exc: Exception = None,
    ) -> None:
        self.exc = exc
        super().__init__(content, status_code, headers, media_type, background)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        await super().__call__(scope, receive, send)
        if self.exc is not None:
            raise self.exc


class CustomException(Exception):
    status_code = 400
    code = 0
    message = "Bad Request"

    def __init__(self, message: Optional[str] = None):
        if message:
            self.message = message


class NotFoundException(CustomException):
    status_code = 404
    code = -100
    message = "资源不存在"


class ExistException(CustomException):
    code = -101
    message = "资源已存在"


class HTTPException(CustomException):
    status_code = 500
    code = 1
    message = "系统内部错误"


class UnauthorizedException(HTTPException):
    status_code = 401
    code = -200
    message = "Unauthorized"


class NotPermissionException(HTTPException):
    status_code = 403
    code = 1002
    message = "授权失败"


async def request_validation_exception_handler(
        request: Request, exc: RequestValidationError
) -> JSONResponse:
    # 表单异常
    content = {"code": 10, "message": str(exc.errors())}
    return JSONResponseWithException(
        status_code=HTTP_400_BAD_REQUEST,
        content=content,
    )


async def error_exception_handler(request: Request, exc: NotFoundException):
    content = {"code": exc.code, "message": exc.message}
    return JSONResponseWithException(
        status_code=exc.status_code,
        content=content
    )
