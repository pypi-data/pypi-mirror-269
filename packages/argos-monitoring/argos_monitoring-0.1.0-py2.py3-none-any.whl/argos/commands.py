import asyncio
import os
from functools import wraps
from uuid import uuid4

import click
import uvicorn
from alembic import command
from alembic.config import Config

from argos import logging
from argos import VERSION
from argos.agent import ArgosAgent


async def get_db():
    from argos.server.main import connect_to_db, get_application, setup_database

    app = get_application()
    setup_database(app)
    return await connect_to_db(app)


def coroutine(f):
    """Decorator to enable async functions in click"""

    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@click.group()
def cli():
    pass


@cli.group()
def server():
    pass


@cli.command()
def version():
    click.echo(VERSION)


@cli.command()
@click.argument("server_url", envvar="ARGOS_AGENT_SERVER_URL")
@click.argument("auth", envvar="ARGOS_AGENT_TOKEN")
@click.option(
    "--max-tasks",
    default=10,
    help="Number of concurrent tasks this agent can run",
)
@click.option(
    "--wait-time",
    default=10,
    help="Waiting time between two polls on the server (seconds)",
)
@click.option(
    "--log-level",
    default="INFO",
    type=click.Choice(logging.LOG_LEVELS, case_sensitive=False),
)
def agent(server_url, auth, max_tasks, wait_time, log_level):
    """Get and run tasks to the provided server. Will wait for new tasks.

    Usage: argos agent https://argos.example.org "auth-token-here"

    Alternatively, you can use the following environment variables to avoid passing
    arguments to the agent on the command line:

      \b
      ARGOS_AGENT_SERVER_URL=https://argos.example.org
      ARGOS_AGENT_TOKEN=auth-token-here
    """
    click.echo("Starting argos agent. Will retry forever.")
    from argos.logging import logger

    logger.setLevel(log_level)
    agent_ = ArgosAgent(server_url, auth, max_tasks, wait_time)
    asyncio.run(agent_.run())


@server.command()
@click.option("--host", default="127.0.0.1", help="Host to bind")
@click.option("--port", default=8000, type=int, help="Port to bind")
@click.option(
    "--config",
    default="config.yaml",
    help="Path of the configuration file. "
    "If ARGOS_YAML_FILE environment variable is set, its value will be used instead.",
    envvar="ARGOS_YAML_FILE",
)
@click.option("--reload", is_flag=True, help="Enable hot reloading")
def start(host, port, config, reload):
    """Starts the server (use only for testing or development!)

    See https://framasoft.frama.io/framaspace/argos/deployment/systemd.html#server
    for advices on how to start the server for production.
    """
    os.environ["ARGOS_YAML_FILE"] = config
    uvicorn.run("argos.server:app", host=host, port=port, reload=reload)


def validate_max_lock_seconds(ctx, param, value):
    if value <= 60:
        raise click.BadParameter("Should be strictly higher than 60")
    return value


def validate_max_results(ctx, param, value):
    if value <= 0:
        raise click.BadParameter("Should be a positive integer")
    return value


@server.command()
@click.option(
    "--max-results",
    default=100,
    help="Number of results per task to keep",
    callback=validate_max_results,
)
@click.option(
    "--max-lock-seconds",
    default=100,
    help=(
        "The number of seconds after which a lock is "
        "considered stale, must be higher than 60 "
        "(the checks have a timeout value of 60 seconds)"
    ),
    callback=validate_max_lock_seconds,
)
@click.option(
    "--config",
    default="config.yaml",
    help="Path of the configuration file. "
    "If ARGOS_YAML_FILE environment variable is set, its value will be used instead.",
    envvar="ARGOS_YAML_FILE",
)
@coroutine
async def cleandb(max_results, max_lock_seconds, config):
    """Clean the database (to run routinely)

    \b
    - Removes old results from the database.
    - Removes locks from tasks that have been locked for too long.
    """
    # The imports are made here otherwise the agent will need server configuration files.
    from argos.server import queries

    os.environ["ARGOS_YAML_FILE"] = config

    db = await get_db()
    removed = await queries.remove_old_results(db, max_results)
    updated = await queries.release_old_locks(db, max_lock_seconds)

    click.echo(f"{removed} results removed")
    click.echo(f"{updated} locks released")


@server.command(short_help="Load or reload tasks’ configuration")
@click.option(
    "--config",
    default="config.yaml",
    help="Path of the configuration file. "
    "If ARGOS_YAML_FILE environment variable is set, its value will be used instead.",
    envvar="ARGOS_YAML_FILE",
)
@coroutine
async def reload_config(config):
    """Read tasks’ configuration and add/delete tasks in database if needed"""
    # The imports are made here otherwise the agent will need server configuration files.
    from argos.server import queries
    from argos.server.main import get_application, read_config
    from argos.server.settings import get_app_settings

    os.environ["ARGOS_YAML_FILE"] = config

    appli = get_application()
    settings = get_app_settings()
    config = read_config(appli, settings)

    db = await get_db()
    changed = await queries.update_from_config(db, config)

    click.echo(f"{changed['added']} tasks added")
    click.echo(f"{changed['vanished']} tasks deleted")


@server.command()
@click.option(
    "--config",
    default="config.yaml",
    help="Path of the configuration file. "
    "If ARGOS_YAML_FILE environment variable is set, its value will be used instead.",
    envvar="ARGOS_YAML_FILE",
)
@coroutine
async def migrate(config):
    """Run database migrations"""
    # The imports are made here otherwise the agent will need server configuration files.
    from argos.server.settings import get_app_settings

    os.environ["ARGOS_YAML_FILE"] = config

    settings = get_app_settings()

    current_dir = os.path.dirname(__file__)
    alembic_cfg = Config(os.path.join(current_dir, "server/migrations/alembic.ini"))
    alembic_cfg.set_main_option("sqlalchemy.url", settings.database_url)
    command.upgrade(alembic_cfg, "head")


@server.command(short_help="Generate a token for agents")
@coroutine
async def generate_token():
    """Generate a token, which can be used as an agent’s authentication token.

    It’s actually an UUID
    """
    click.echo(uuid4())


if __name__ == "__main__":
    cli()
