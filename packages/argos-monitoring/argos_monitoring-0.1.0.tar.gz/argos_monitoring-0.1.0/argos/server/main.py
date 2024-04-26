import os
import sys

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from argos.logging import logger
from argos.server import models, routes
from argos.server.settings import get_app_settings, read_yaml_config


def get_application() -> FastAPI:
    """Spawn Argos FastAPI server"""
    settings = get_app_settings()
    appli = FastAPI()

    config = read_config(appli, settings)

    # Settings is the pydantic settings object
    # Config is the argos config object (built from yaml)
    appli.state.config = config
    appli.state.settings = settings

    appli.add_event_handler(
        "startup",
        create_start_app_handler(appli),
    )
    appli.add_event_handler(
        "shutdown",
        create_stop_app_handler(appli),
    )
    appli.include_router(routes.api, prefix="/api")
    appli.include_router(routes.views)

    static_dir = os.path.join(os.path.dirname(__file__), "static")

    appli.mount("/static", StaticFiles(directory=static_dir), name="static")
    return appli


def create_start_app_handler(appli):
    """Warmup the server:
    setup database connection
    """

    async def _get_db():
        setup_database(appli)

        return await connect_to_db(appli)

    return _get_db


async def connect_to_db(appli):
    appli.state.db = appli.state.SessionLocal()
    return appli.state.db


def create_stop_app_handler(appli):
    """Gracefully shutdown the server:
    close database connection.
    """

    async def stop_app():
        appli.state.db.close()

    return stop_app


def read_config(appli, settings):
    try:
        config = read_yaml_config(settings.yaml_file)
        appli.state.config = config
        return config
    except ValidationError as err:
        logger.error("Errors where found while reading configuration:")
        for error in err.errors():
            logger.error("%s is %s", error["loc"], error["type"])
        sys.exit(1)


def setup_database(appli):
    settings = appli.state.settings
    # For sqlite, we need to add connect_args={"check_same_thread": False}
    logger.debug("Using database URL %s", settings.database_url)
    if settings.database_url.startswith("sqlite:////tmp"):
        logger.warning("Using sqlite in /tmp is not recommended for production")

    extra_settings = {}
    if settings.db_pool_size:
        extra_settings.setdefault("pool_size", settings.db_pool_size)

    if settings.db_max_overflow:
        extra_settings.setdefault("max_overflow", settings.db_max_overflow)

    engine = create_engine(settings.database_url, **extra_settings)

    def _fk_pragma_on_connect(dbapi_con, con_record):
        dbapi_con.execute("pragma foreign_keys=ON")

    if settings.database_url.startswith("sqlite:////"):
        event.listen(engine, "connect", _fk_pragma_on_connect)

    appli.state.SessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
    appli.state.engine = engine
    models.Base.metadata.create_all(bind=engine)


app = get_application()
