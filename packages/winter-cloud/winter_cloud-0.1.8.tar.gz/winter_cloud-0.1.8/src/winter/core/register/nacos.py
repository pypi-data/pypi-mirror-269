import os
from contextlib import asynccontextmanager
from typing import Optional, Awaitable

from dynaconf import Dynaconf
from fastapi import FastAPI
from loguru import logger
from use_nacos import NacosAsyncClient
from use_nacos.client import BaseClient

from winter._utils import get_host_ip


def register_nacos_instance(app: FastAPI, settings: Dynaconf) -> FastAPI:
    """ 注册nacos实例 """
    router = app.router if isinstance(app, FastAPI) else app  # noqa
    _original_lifespan_context = router.lifespan_context

    @asynccontextmanager
    async def lifespan(app):
        nacos = NacosAsyncClient(**settings.nacos.client)

        await nacos.instance.heartbeat(
            service_name=settings.project_name,
            ip=settings.nacos.get("discovery", {}).get("host", get_host_ip()),
            port=settings.nacos.get("discovery", {}).get("port", os.environ.get("PORT"))
        )

        async with _original_lifespan_context(app) as maybe_state:
            yield maybe_state

    router.lifespan_context = lifespan
    return app


def register_nacos_config(
        app: FastAPI,
        settings: Dynaconf,
        client: Optional[BaseClient] = None,
        config_callback: Optional[Awaitable] = None
) -> FastAPI:
    async def _default_config_callback(config):
        logger.bind(config=config).debug("nacos config changed")
        settings.update(config)

    config_callback = config_callback or _default_config_callback

    router = app.router if isinstance(app, FastAPI) else app  # noqa
    _original_lifespan_context = router.lifespan_context

    @asynccontextmanager
    async def lifespan(app):
        nacos = client or NacosAsyncClient(**settings.nacos.client)

        config_subscriber = await nacos.config.subscribe(
            **settings.nacos.config,
            serializer=True,
            callback=config_callback
        )

        async with _original_lifespan_context(app) as maybe_state:
            yield maybe_state
        config_subscriber.cancel()

    router.lifespan_context = lifespan
    return app
