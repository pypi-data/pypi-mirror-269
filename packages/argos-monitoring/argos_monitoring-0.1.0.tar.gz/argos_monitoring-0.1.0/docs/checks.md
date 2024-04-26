# Checks

At its core, argos runs checks and return the results to the service. Here are the implemented checks, with a description of what they do and how to configure them.

## Simple checks

These checks are the most basic ones. They simply check that the response from the service matches what you expect.

| Check | Description | Configuration |
| --- | --- | --- |
| `status-is` | Check that the returned status code matches what you expect. | `status-is: "200"` |
| `body-contains` | Check that the returned body contains a given string. | `body-contains: "Hello world"` |

```{code-block} yaml
---
caption: config.yaml
---
- domain: "https://example.org"
  paths:
    - path: "/"
      checks:
        - status-is: 200
        - body-contains: "Hello world"
```

## SSL certificate expiration

 Checks that the SSL certificate will not expire soon. You need to define the thresholds in the configuration, and set the `on-check` option to enable the check.


```{code-block} yaml
---
caption: config.yaml
---
ssl:
  thresholds:
    - "1d": critical
    - "5d": warning

- domain: "https://example.org"
  paths:
    - path: "/"
      checks:
        - ssl-certificate-expiration: "on-check"
```