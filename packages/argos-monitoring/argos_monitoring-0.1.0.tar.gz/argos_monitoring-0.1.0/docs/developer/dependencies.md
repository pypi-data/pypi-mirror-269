# Main dependencies used by Argos

## Python packages

- [Click](https://click.palletsprojects.com/) for the command-line interface;
- [FastAPI](https://fastapi.tiangolo.com/) is the framework that allows us to expose the HTTP API;
- [HTTPX](https://www.python-httpx.org/) is used to issue asynchronous requests in the agents;
- [Jinja](https://jinja.palletsprojects.com/) is handling the templating;
- [Pydantic](https://pydantic.dev/) is useful to ensure the data matches our expectactions;
- [SQLAlchemy](https://www.sqlalchemy.org/) is the ORM we use, to connect to our database and issue queries;
- [Alembic](https://alembic.sqlalchemy.org) is used for DB migrations;
- [Tenacity](https://github.com/jd/tenacity) a small utility to retry a function in case an error occured;
- [Uvicorn](https://www.uvicorn.org/) is the tool used to run our server;
- [Gunicorn](https://gunicorn.org/) is the recommended WSGI HTTP server for production.

## CSS framework

- [Pico.css](https://picocss.com/), a minimalist CSS framework, which does just what you need :-)
