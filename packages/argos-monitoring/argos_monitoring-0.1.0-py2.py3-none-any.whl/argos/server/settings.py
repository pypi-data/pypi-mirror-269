"""Pydantic schemas for server"""
import os
from functools import lru_cache
from os import environ
from typing import Optional, Union

import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict
from yamlinclude import YamlIncludeConstructor

from argos.schemas.config import Config


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="argos_", env_file=".env")
    app_env: str
    database_url: str
    yaml_file: str
    db_pool_size: Optional[int]
    db_max_overflow: Optional[int]


class DevSettings(Settings):
    """Settings for dev environment.

    Uses config.yaml as config file.
    Uses a SQLite database."""

    app_env: str = "dev"
    yaml_file: str = "config.yaml"
    db_pool_size: Optional[int] = None
    db_max_overflow: Optional[int] = None
    database_url: str = "sqlite:////tmp/argos.db"


class TestSettings(Settings):
    """Settings for test environment.

    Uses tests/config.yaml as config file.
    Uses a SQLite database."""

    app_env: str = "test"
    yaml_file: str = "tests/config.yaml"
    database_url: str = "sqlite:////tmp/test-argos.db"
    db_pool_size: Optional[int] = None
    db_max_overflow: Optional[int] = None


class ProdSettings(Settings):
    """Settings for prod environment."""

    app_env: str = "prod"
    db_pool_size: Optional[int] = 10
    db_max_overflow: Optional[int] = 20


environments = {
    "dev": DevSettings,
    "prod": ProdSettings,
    "test": TestSettings,
}


@lru_cache()
def get_app_settings() -> Union[None, Settings]:
    """Load settings depending on the environment"""
    app_env = environ.get("ARGOS_APP_ENV", "dev")
    settings = environments.get(app_env)
    if settings is not None:
        return settings()
    return None


def read_yaml_config(filename):
    parsed = _load_yaml(filename)
    return Config(**parsed)


def _load_yaml(filename):
    base_dir = os.path.dirname(filename)
    YamlIncludeConstructor.add_to_loader_class(
        loader_class=yaml.FullLoader, base_dir=base_dir
    )

    with open(filename, "r", encoding="utf-8") as stream:
        return yaml.load(stream, Loader=yaml.FullLoader)
