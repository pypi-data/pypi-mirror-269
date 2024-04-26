# Adding a database migration

We are using [Alembic](https://alembic.sqlalchemy.org) to handle the database
migrations. Here is how to proceed in order to add a new migration:

First, do your changes in the code, change the model, add new tables, etc. Once
you're done, you can create a new migration.

```bash
venv/bin/alembic -c argos/server/migrations/alembic.ini revision --autogenerate -m "migration reason"
```

Edit the created file to remove comments and adapt it to make sure the migration is complete (Alembic is not powerful enough to cover all the corner cases).
