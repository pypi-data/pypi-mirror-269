import asyncio
import os

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

os.environ["ARGOS_APP_ENV"] = "test"


@pytest.fixture
def db() -> Session:
    from argos.server import models

    app = _create_app()
    models.Base.metadata.create_all(bind=app.state.engine)
    yield app.state.SessionLocal()
    models.Base.metadata.drop_all(bind=app.state.engine)


@pytest.fixture
def app() -> FastAPI:
    from argos.server import models

    app = _create_app()
    models.Base.metadata.create_all(bind=app.state.engine)
    yield app
    models.Base.metadata.drop_all(bind=app.state.engine)


@pytest.fixture
def authorized_client(app):
    with TestClient(app) as client:
        token = app.state.config.service.secrets[0]
        client.headers = {"Authorization": f"Bearer {token}"}
        yield client


def _create_app() -> FastAPI:
    from argos.server.main import (  # local import for testing purpose
        get_application,
        setup_database,
        connect_to_db,
    )

    app = get_application()
    # Hardcode the database url and the yaml file for testing purpose
    # Otherwise, the app will try to read the .env file or the environment variables
    app.state.settings.database_url = "sqlite:////tmp/test-argos.db"
    app.state.settings.yaml_file = "tests/config.yaml"

    setup_database(app)
    asyncio.run(connect_to_db(app))
    return app
