# Install and configure PostgreSQL

Here are a few steps for you to install PostgreSQL on your system:

## Debian

```bash
sudo apt install postgresql
```

```bash
sudo -u postgres createuser -P argos
sudo -u postgres createdb -O argos argos
sudo -u postgres psql -c "ALTER DATABASE argos SET TIMEZONE TO 'UTC';"
```

## MacOS

```bash
brew install postgresql@14
brew services start postgresql@14
createuser argos
createdb argos -O argos
```
