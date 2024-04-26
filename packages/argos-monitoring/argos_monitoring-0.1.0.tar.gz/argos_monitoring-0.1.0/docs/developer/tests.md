# Tests and linting

## Tests

To launch the tests suite:
```bash
make test
```

## Linting

There is 4 lintings checks:
- `make djlint` will check the linting of the HTML templates
- `make pylint` will check the linting of Argos source code
- `make pylint-alembic` will check the linting of Alembic’s migrations files
- `make ruff` will check the linting of all files

You can launch all of them with:
```bash
make lint
```
