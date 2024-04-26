# Argos monitoring

A monitoring and status board for websites.
Test how your websites respond to external checks, get notified when something goes wrong.

## Features

- **Server-Agent architecture**: The server is responsible for storing the configuration and the results of the checks. The agent is responsible for running the checks and sending the results to the server.
- **Extensibility**: New checks can be added using python.
- A **Website** allows to navigate the results of the checks.
- **HTTP API**: An HTTP API is exposed to get the results of the checks.

![Dashboard](dashboard.jpg)

![Domains list](domains.jpg)

## Next

::::{grid} 2
:::{grid-item-card}  Installation
:link: installation/getting-started.html
The best way to get started with argos.
:::
:::{grid-item-card}  Developper docs
:link: developer/overview.html
You want to know more about the internals ?
:::
::::


```{toctree}
:caption: Getting started
:hidden:

installation/getting-started
installation/postgresql
cli
api
changelog
```

```{toctree}
:caption: Deployment
:hidden:
deployment/systemd
deployment/nginx
```

```{toctree}
:caption: Configuration
:hidden:
configuration
checks
```

```{toctree}
:caption: Developer docs
:hidden:
developer/requirements
developer/installation
developer/overview
developer/dependencies
developer/new-check
developer/models
developer/migrations
developer/tests
developer/release
```

