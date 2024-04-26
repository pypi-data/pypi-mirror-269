# Command-line interface

<!-- [[[cog
    from argos.commands import cli
    from click.testing import CliRunner
    def help(args):
        title = "argos " + " ".join(args)
        cog.out("\n```man\n")
        result = CliRunner().invoke(cli, args)
        output = result.output.replace("Usage: cli ", "Usage: argos ")
        cog.out(output)
        cog.out("```\n\n")
 ]]] -->
<!-- [[[end]]] -->

## The argos cli
<!--
.. [[[cog
    help(["--help"])
.. ]]] -->

```man
Usage: argos [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  agent    Get and run tasks to the provided server.
  server
  version
```

<!--[[[end]]]
-->

## Agent command
<!--
.. [[[cog
    help(["agent", "--help"])
.. ]]] -->

```man
Usage: argos agent [OPTIONS] SERVER_URL AUTH

  Get and run tasks to the provided server. Will wait for new tasks.

  Usage: argos agent https://argos.example.org "auth-token-here"

  Alternatively, you can use the following environment variables to avoid
  passing arguments to the agent on the command line:

      ARGOS_AGENT_SERVER_URL=https://argos.example.org
      ARGOS_AGENT_TOKEN=auth-token-here

Options:
  --max-tasks INTEGER             Number of concurrent tasks this agent can run
  --wait-time INTEGER             Waiting time between two polls on the server
                                  (seconds)
  --log-level [DEBUG|INFO|WARNING|ERROR|CRITICAL]
  --help                          Show this message and exit.
```

<!--[[[end]]]
-->

## Server commands
<!--
.. [[[cog
    help(["server", "--help"])
.. ]]] -->

```man
Usage: argos server [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  cleandb         Clean the database (to run routinely)
  generate-token  Generate a token for agents
  migrate         Run database migrations
  reload-config   Load or reload tasks’ configuration
  start           Starts the server (use only for testing or development!)
```

<!--[[[end]]]
-->

### Server start
<!--
.. [[[cog
    help(["server", "start", "--help"])
.. ]]] -->

```man
Usage: argos server start [OPTIONS]

  Starts the server (use only for testing or development!)

  See https://framasoft.frama.io/framaspace/argos/deployment/systemd.html#server
  for advices on how to start the server for production.

Options:
  --host TEXT     Host to bind
  --port INTEGER  Port to bind
  --config TEXT   Path of the configuration file. If ARGOS_YAML_FILE environment
                  variable is set, its value will be used instead.
  --reload        Enable hot reloading
  --help          Show this message and exit.
```

<!--[[[end]]]
-->

### Server migrate

<!--
.. [[[cog
    help(["server", "migrate", "--help"])
.. ]]] -->

```man
Usage: argos server migrate [OPTIONS]

  Run database migrations

Options:
  --config TEXT  Path of the configuration file. If ARGOS_YAML_FILE environment
                 variable is set, its value will be used instead.
  --help         Show this message and exit.
```

<!--[[[end]]]
-->


### Server cleandb
<!--
.. [[[cog
    help(["server", "cleandb", "--help"])
.. ]]] -->

```man
Usage: argos server cleandb [OPTIONS]

  Clean the database (to run routinely)

  - Removes old results from the database.
  - Removes locks from tasks that have been locked for too long.

Options:
  --max-results INTEGER       Number of results per task to keep
  --max-lock-seconds INTEGER  The number of seconds after which a lock is
                              considered stale, must be higher than 60 (the
                              checks have a timeout value of 60 seconds)
  --config TEXT               Path of the configuration file. If ARGOS_YAML_FILE
                              environment variable is set, its value will be
                              used instead.
  --help                      Show this message and exit.
```

<!--[[[end]]]
-->

### Server reload-config

<!--
.. [[[cog
    help(["server", "reload-config", "--help"])
.. ]]] -->

```man
Usage: argos server reload-config [OPTIONS]

  Read tasks’ configuration and add/delete tasks in database if needed

Options:
  --config TEXT  Path of the configuration file. If ARGOS_YAML_FILE environment
                 variable is set, its value will be used instead.
  --help         Show this message and exit.
```

<!--[[[end]]]
-->

### Server generate-token command

<!--
.. [[[cog
    help(["server", "generate-token", "--help"])
.. ]]] -->

```man
Usage: argos server generate-token [OPTIONS]

  Generate a token, which can be used as an agent’s authentication token.

  It’s actually an UUID

Options:
  --help  Show this message and exit.
```

<!--[[[end]]]
-->
