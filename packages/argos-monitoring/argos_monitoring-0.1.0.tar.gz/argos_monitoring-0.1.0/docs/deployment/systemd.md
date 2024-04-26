# Using systemd

Here are the systemd files that can be used to deploy the server and the agents.

## Agent

```{literalinclude} ../../conf/systemd-agent.service
---
caption: /etc/systemd/system/argos-agent.service
---
```

## Server

```{literalinclude} ../../conf/systemd-server.service
---
caption: /etc/systemd/system/argos-server.service
---
```
