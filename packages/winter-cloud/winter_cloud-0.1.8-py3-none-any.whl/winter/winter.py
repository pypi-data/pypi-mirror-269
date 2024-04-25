import importlib
import os
from dataclasses import dataclass, field, asdict

from dynaconf import Dynaconf
from fastapi import FastAPI


@dataclass
class SettingOption:
    envvar_prefix: str = "WINTER"
    settings_files: list = field(default_factory=lambda: ["settings.yaml", ".secrets.yaml"])
    environments: bool = True
    load_dotenv: bool = True
    env_switcher: str = "ENV"
    root_path: str = os.getcwd()


@dataclass
class AppOption:
    title: str = "Winter"


class Winter(FastAPI):

    def __init__(
            self,
            *,
            app_option: AppOption | None = AppOption(),
            setting_option: SettingOption | None = SettingOption(),
            register_middlewares: bool = True,
    ):
        self.app_option = app_option
        self._settings = None
        self.setting_option = setting_option

        self._configure_settings()
        super().__init__(**asdict(self.app_option))
        if register_middlewares:
            self.auto_register_middlewares()

    @property
    def settings(self):
        return self._settings

    def _configure_settings(self):
        settings = Dynaconf(**asdict(self.setting_option))
        if not settings._loaded_files:  # noqa
            raise ValueError(
                'Settings files not found, \n'
                'please check your `settings.yaml` file \n'
                'in the root directory of your project'
            )
        self._settings = settings

    def auto_register_middlewares(self):
        middlewares_config = self.settings.winner.middlewares
        for middleware_config in middlewares_config:
            middleware_name = middleware_config.get('name')

            module_name, class_name = middleware_name.split(':')
            module = importlib.import_module(module_name)
            middleware_cls = getattr(module, class_name)

            self.add_middleware(middleware_cls, **middleware_config.get('options', {}))
