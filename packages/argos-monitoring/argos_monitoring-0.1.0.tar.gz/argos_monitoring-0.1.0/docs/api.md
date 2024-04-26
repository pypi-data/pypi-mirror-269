# The HTTP API

Argos exposes a website and an API. The website is available at "/" and the API at "/api".

## Authentication

To access the API, you need to pass an authentication token in the `Authorization` header, as defined in the configuration file. It's a Bearer token, so you need to pass it as a header like this :

```
    "Authorization": "Bearer " + token
```

See the [CLI documentation](cli.md#server-generate-token-command) to generate tokens.

## Endpoints

You can also have access to the Swagger API documentation at `https://<argos-url>/docs`, and the ReDoc documentation at `https://<argos-url>/redoc`.
