# Configuration

There are actually two configuration files: one for the service and one for the checks.

## Server configuration

The server configuration is done using environment variables. You can put them in a `.env` file at the root of the project.
Here is a list of the useful variables, in the `.env` format:

```{literalinclude} ../conf/.env.example
---
caption: .env
---
```

### Environment variables

Here are the environment variables you can define to configure how the service will behave :

#### ARGOS_YAML_FILE

The path to the yaml configuration file, defining the checks.

#### ARGOS_DATABASE_URL

The database url, as defined [in SQLAlchemy docs](https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls).

For instance, to connect to a postgres database on localhost with user, pass and dbname "argos":

```
ARGOS_DATABASE_URL = "postgresql://argos:argos@localhost/argos"
```

#### DB_POOL_SIZE
#### DB_MAX_OVERFLOW

You configure the size of the database pool of connection, and the max overflow (until when new connections are accepted ?) These are documented [in the SQLAlchemy docs in greater details](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.QueuePool.params.pool_size)

```bash
DB_POOL_SIZE = 10
DB_MAX_OVERFLOW = 20
```

## Argos "checks" configuration

Argos uses a YAML configuration file to define the websites to monitor and the checks to run on these websites.

Here is a simple configuration file:


```{literalinclude} ../conf/config-example.yaml
---
caption: config.yaml
---

```