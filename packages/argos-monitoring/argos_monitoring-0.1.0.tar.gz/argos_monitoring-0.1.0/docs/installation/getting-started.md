# Installation

## Requirements

- Python 3.11+
- PostgreSQL 13+ (for production)

## Install with pip

```bash
pip install argos-monitoring
```

You may want to install Argos in a virtualenv:
```bash
python3 -m venv venv
source venv/bin/activate
pip install argos-monitoring
```

## Install from sources

Once you got the source locally, create a virtualenv and install the dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

## Configure

The quickest way to get started is to get the `config-example.yaml` file from our repository and edit it:

```bash
wget https://framagit.org/framasoft/framaspace/argos/-/raw/main/conf/config-example.yaml -O config.yaml
```

You can read more about the configuration in the [configuration section](../configuration.md).

### Configure the server

Environment variables are used to configure the server. You can also put them in an `.env` file:

```{literalinclude} ../../conf/.env.example
---
caption: .env
---
```

Please note that the only supported database engines are SQLite for development and PostgreSQL for production.

## Apply migrations to database

Create the schema in the database with:

```bash
argos server migrate
```

## Inject tasks into the database

Argos keeps tasks’ configuration in database, take from the config file.

Populate the database with the tasks:

```bash
argos server reload-config
```

## Starting the server

Then you can start the server:

```bash
argos server start
```

The server reads the `yaml` file at startup, and populates the tasks queue with the checks defined in the configuration. 

## Generating a token 

The agent needs an authentication token to be able to communicate with the server.

You can generate an authentication token with the following command:
```bash
argos server generate-token
```

Add the token in the configuration file, in the following setting:

```yaml
service:
  secrets:
    - "auth-token"
```

## Running the agent

You can run the agent on the same machine as the server, or on a different machine.
The only requirement is that the agent can reach the server.

```bash
argos agent http://localhost:8000 "auth-token"
```

## Cleaning the database

You also have to run cleaning tasks periodically. `argos server clean --help` will give you more information on how to do that.

Here is a crontab example, which will clean the db each hour:

```bash
# Run the cleaning tasks every hour (at minute 7)
# Keeps 10 results per task, and remove tasks’ locks older than 1 hour
7 * * * * argos server cleandb --max-results 10 --max-lock-seconds 3600
```
