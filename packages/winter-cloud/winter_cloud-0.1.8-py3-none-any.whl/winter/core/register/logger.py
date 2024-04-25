from use_logger import useLogger, useLoggerInterceptUvicorn
from use_logger.handlers import logstash_handler


def register_logger(packages=None, extra=None, handler=None, uvicorn=True):
    handler = handler or {}
    extra = extra or {}
    useLogger(
        handlers=[
            logstash_handler(**handler),
        ],
        packages=packages,
        extra=extra
    )
    if uvicorn:
        useLoggerInterceptUvicorn()
