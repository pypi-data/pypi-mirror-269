from .auth import register_authentication
from .exception import register_exception_handlers
from .logger import register_logger
from .mysql import register_mysql
from .nacos import register_nacos_instance, register_nacos_config

__all__ = [
    "register_exception_handlers",
    "register_nacos_instance",
    "register_nacos_config",
    "register_authentication",
    "register_mysql",
    "register_logger"
]
