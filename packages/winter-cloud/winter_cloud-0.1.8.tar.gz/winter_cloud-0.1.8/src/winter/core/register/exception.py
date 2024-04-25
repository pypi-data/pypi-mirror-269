from fastapi import FastAPI

from winter.common import exception


def register_exception_handlers(app: FastAPI):
    """ 注册异常处理器 """
    app.add_exception_handler(exception.RequestValidationError, exception.request_validation_exception_handler)
    app.add_exception_handler(exception.ValidationError, exception.request_validation_exception_handler)
    app.add_exception_handler(exception.HTTPException, exception.error_exception_handler)
    app.add_exception_handler(exception.NotFoundException, exception.error_exception_handler)
    app.add_exception_handler(exception.ExistException, exception.error_exception_handler)
    app.add_exception_handler(Exception, exception.error_exception_handler)
